#!/usr/bin/env python3
"""Detect high token-window overlap against a prior version."""

from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from typing import Any

from tool_common import ToolError, infer_lang, markdown_table, print_error, read_text_checked


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Compare sliding token windows against a prior version. EN uses word tokens; "
            "ZH uses overlapping CJK character bigrams for deterministic matching."
        )
    )
    parser.add_argument("--current", required=True, help="Current rewrite.")
    parser.add_argument("--prior", required=True, help="Prior version to compare against.")
    parser.add_argument("--window", type=int, default=10, help="Window size in tokens/bigrams. Default: 10.")
    parser.add_argument("--threshold", type=float, default=0.7, help="Overlap ratio threshold. Default: 0.7.")
    parser.add_argument("--lang", choices=["en", "zh", "auto"], default="auto", help="Language. Defaults to auto.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown.")
    return parser.parse_args()


def tokenize(text: str, lang: str) -> list[str]:
    if lang == "zh":
        chars = re.findall(r"[\u4e00-\u9fff]", text)
        if len(chars) <= 1:
            return chars
        return ["".join(chars[i : i + 2]) for i in range(len(chars) - 1)]
    return [m.group(0).lower() for m in re.finditer(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)?", text)]


def windows(items: list[str], size: int) -> list[tuple[int, list[str]]]:
    if size <= 0:
        raise ToolError("--window must be positive")
    if len(items) < size:
        return [(0, items)] if items else []
    return [(i, items[i : i + size]) for i in range(0, len(items) - size + 1)]


def overlap_ratio(left: list[str], right: list[str]) -> float:
    if not left or not right:
        return 0.0
    left_counts = collections.Counter(left)
    right_counts = collections.Counter(right)
    overlap = sum(min(count, right_counts[token]) for token, count in left_counts.items())
    return overlap / max(len(left), 1)


def best_prior(current_window: list[str], prior_windows: list[tuple[int, list[str]]]) -> tuple[int, float, list[str]]:
    best_index = -1
    best_score = 0.0
    best_tokens: list[str] = []
    for index, prior_window in prior_windows:
        score = overlap_ratio(current_window, prior_window)
        if score > best_score:
            best_index = index
            best_score = score
            best_tokens = prior_window
    return best_index, best_score, best_tokens


def excerpt(tokens: list[str], lang: str) -> str:
    if lang == "zh":
        if not tokens:
            return ""
        text = tokens[0][0] + "".join(token[-1] for token in tokens)
        return text[:80]
    return " ".join(tokens[:24])


def main() -> int:
    args = parse_args()
    try:
        current_text = read_text_checked(args.current)
        prior_text = read_text_checked(args.prior)
        lang = infer_lang([current_text, prior_text]) if args.lang == "auto" else args.lang
        current_tokens = tokenize(current_text, lang)
        prior_tokens = tokenize(prior_text, lang)
        current_windows = windows(current_tokens, args.window)
        prior_windows = windows(prior_tokens, args.window)

        findings: list[dict[str, Any]] = []
        for current_index, current_window in current_windows:
            prior_index, score, prior_window = best_prior(current_window, prior_windows)
            if score >= args.threshold:
                findings.append(
                    {
                        "current_pos": current_index,
                        "prior_pos": prior_index,
                        "overlap": round(score, 3),
                        "current_excerpt": excerpt(current_window, lang),
                        "prior_excerpt": excerpt(prior_window, lang),
                    }
                )
        ratio = len(findings) / len(current_windows) if current_windows else 0.0
        result = {
            "current": args.current,
            "prior": args.prior,
            "lang": lang,
            "window": args.window,
            "threshold": args.threshold,
            "current_window_count": len(current_windows),
            "over_threshold_count": len(findings),
            "over_threshold_ratio": round(ratio, 3),
            "findings": findings,
        }
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            rows = [
                [f["current_pos"], f["prior_pos"], f["overlap"], f["current_excerpt"], f["prior_excerpt"]]
                for f in findings[:50]
            ]
            print(f"Over-threshold windows: {len(findings)} / {len(current_windows)} ({ratio:.3f})")
            print(markdown_table(["Current pos", "Prior pos", "Overlap", "Current excerpt", "Prior excerpt"], rows or [["-", "-", 0, "No over-threshold windows", ""]]))
        return 1 if findings else 0
    except ToolError as exc:
        print_error(exc)
        return 2


if __name__ == "__main__":
    sys.exit(main())
