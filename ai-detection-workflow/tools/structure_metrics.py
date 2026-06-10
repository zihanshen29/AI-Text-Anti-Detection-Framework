#!/usr/bin/env python3
"""Compute deterministic structural proxy metrics for prose."""

from __future__ import annotations

import argparse
import json
import math
import re
import statistics
import sys
from typing import Any

from tool_common import ToolError, infer_lang, markdown_table, print_error, read_text_checked, unit_count


DISCLAIMER = "Structural proxies only; no validated correlation to any external detector."


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Compute structural proxy metrics. Sentence splitting is deterministic and limited: "
            "ZH splits on 。！？；; EN splits on .!? followed by whitespace and does not handle abbreviations."
        )
    )
    parser.add_argument("--text", required=True, help="Current text file.")
    parser.add_argument("--baseline", help="Optional baseline/source file.")
    parser.add_argument("--lang", choices=["en", "zh", "auto"], default="auto", help="Language. Defaults to auto.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown.")
    return parser.parse_args()


def tokens(text: str, lang: str) -> list[str]:
    if lang == "zh":
        cjk = re.findall(r"[\u4e00-\u9fff]", text)
        if cjk:
            return cjk
    return [m.group(0).lower() for m in re.finditer(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)?", text)]


def sentence_split(text: str, lang: str) -> list[str]:
    if lang == "zh":
        parts = re.split(r"[。！？；]+", text)
    else:
        parts = re.split(r"(?<=[.!?])\s+", text)
    return [part.strip() for part in parts if part.strip()]


def paragraphs(text: str) -> list[str]:
    return [p.strip() for p in re.split(r"\n\s*\n+", text) if p.strip()]


def length_of(segment: str, lang: str) -> int:
    if lang == "zh":
        return len(re.findall(r"[\u4e00-\u9fffA-Za-z0-9]", segment))
    return len(tokens(segment, lang))


def mean(values: list[float]) -> float:
    return statistics.fmean(values) if values else 0.0


def cv(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    avg = mean(values)
    return statistics.pstdev(values) / avg if avg else 0.0


def sliding_ttr(all_tokens: list[str], window: int = 500) -> float:
    if not all_tokens:
        return 0.0
    if len(all_tokens) <= window:
        return len(set(all_tokens)) / len(all_tokens)
    ratios = []
    step = window
    for start in range(0, len(all_tokens) - window + 1, step):
        chunk = all_tokens[start : start + window]
        ratios.append(len(set(chunk)) / len(chunk))
    return mean(ratios)


def adjacent_prefix_repeat(paras: list[str], lang: str) -> float:
    if len(paras) < 2:
        return 0.0
    repeats = 0
    total = 0
    for left, right in zip(paras, paras[1:]):
        lt = tokens(left, lang)[:5]
        rt = tokens(right, lang)[:5]
        if len(lt) == 5 and len(rt) == 5:
            total += 1
            if lt == rt:
                repeats += 1
    return repeats / total if total else 0.0


def compute(path: str, lang: str) -> dict[str, Any]:
    text = read_text_checked(path)
    sents = sentence_split(text, lang)
    paras = paragraphs(text)
    sent_lengths = [length_of(sentence, lang) for sentence in sents if length_of(sentence, lang) > 0]
    para_lengths = [length_of(paragraph, lang) for paragraph in paras if length_of(paragraph, lang) > 0]
    all_tokens = tokens(text, lang)
    punctuation = set(re.findall(r"[^\w\s\u4e00-\u9fff]", text, flags=re.UNICODE))
    units = unit_count(text, lang)
    de_counts = [sentence.count("的") for sentence in sents] if lang == "zh" else []

    return {
        "file": path,
        "lang": lang,
        "units": units,
        "sentence_count": len(sents),
        "sentence_length_mean": round(mean(sent_lengths), 3),
        "sentence_length_cv": round(cv(sent_lengths), 3),
        "paragraph_length_mean": round(mean(para_lengths), 3),
        "paragraph_length_cv": round(cv(para_lengths), 3),
        "punctuation_diversity_per_1000": round(len(punctuation) * 1000 / units, 3),
        "em_dash_count": text.count("—"),
        "spaced_hyphen_count": text.count(" - "),
        "sliding_window_ttr_500": round(sliding_ttr(all_tokens), 3),
        "adjacent_paragraph_prefix_repeat_rate": round(adjacent_prefix_repeat(paras, lang), 3),
        "de_per_sentence_mean": round(mean(de_counts), 3) if lang == "zh" else None,
        "de_per_sentence_max": max(de_counts) if de_counts else None,
    }


METRIC_KEYS = [
    "sentence_count",
    "sentence_length_mean",
    "sentence_length_cv",
    "paragraph_length_mean",
    "paragraph_length_cv",
    "punctuation_diversity_per_1000",
    "em_dash_count",
    "spaced_hyphen_count",
    "sliding_window_ttr_500",
    "adjacent_paragraph_prefix_repeat_rate",
    "de_per_sentence_mean",
    "de_per_sentence_max",
]


def render_single(result: dict[str, Any]) -> str:
    rows = [[key, result[key]] for key in METRIC_KEYS if result.get(key) is not None]
    return "\n".join([f"## {result['file']}", "", markdown_table(["Metric", "Value"], rows), "", DISCLAIMER])


def render_compare(before: dict[str, Any], after: dict[str, Any]) -> str:
    rows = []
    for key in METRIC_KEYS:
        if before.get(key) is None and after.get(key) is None:
            continue
        b = before.get(key)
        a = after.get(key)
        delta = None if b is None or a is None else round(a - b, 3)
        rows.append([key, b, a, delta])
    return "\n".join(
        [
            "## Structural baseline comparison",
            "",
            f"Baseline: {before['file']}",
            f"Current: {after['file']}",
            "",
            markdown_table(["Metric", "Before", "After", "Delta"], rows),
            "",
            DISCLAIMER,
        ]
    )


def main() -> int:
    args = parse_args()
    try:
        preload = [read_text_checked(args.text)]
        if args.baseline:
            preload.append(read_text_checked(args.baseline))
        lang = infer_lang(preload) if args.lang == "auto" else args.lang
        current = compute(args.text, lang)
        if args.baseline:
            baseline = compute(args.baseline, lang)
            if args.json:
                print(json.dumps({"baseline": baseline, "current": current, "disclaimer": DISCLAIMER}, ensure_ascii=False, indent=2))
            else:
                print(render_compare(baseline, current))
        else:
            if args.json:
                print(json.dumps({"result": current, "disclaimer": DISCLAIMER}, ensure_ascii=False, indent=2))
            else:
                print(render_single(current))
        return 0
    except ToolError as exc:
        print_error(exc)
        return 2


if __name__ == "__main__":
    sys.exit(main())
