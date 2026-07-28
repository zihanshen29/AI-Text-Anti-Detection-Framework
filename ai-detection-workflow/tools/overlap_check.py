#!/usr/bin/env python3
"""Detect high token-window overlap against a prior version."""

from __future__ import annotations

import argparse
import collections
import json
import math
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
        return ["".join(chars[index : index + 2]) for index in range(len(chars) - 1)]
    return [match.group(0).lower() for match in re.finditer(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)?", text)]


def windows(items: list[str], size: int) -> list[tuple[int, list[str]]]:
    if size <= 0:
        raise ToolError("--window must be positive")
    if len(items) < size:
        return [(0, items)] if items else []
    return [(index, items[index : index + size]) for index in range(0, len(items) - size + 1)]


def overlap_ratio(left: list[str], right: list[str]) -> float:
    if not left or not right:
        return 0.0
    left_counts = collections.Counter(left)
    right_counts = collections.Counter(right)
    overlap = sum(min(count, right_counts[token]) for token, count in left_counts.items())
    return overlap / len(left)


def best_prior(current_window: list[str], prior_windows: list[tuple[int, list[str]]]) -> tuple[int, float, list[str]]:
    """Naive reference implementation retained for equivalence tests."""

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


def build_token_postings(prior_windows: list[tuple[int, list[str]]]) -> tuple[dict[str, list[tuple[int, int]]], dict[int, list[str]]]:
    """Index each prior token to the windows and multiplicities that contain it."""

    postings: dict[str, list[tuple[int, int]]] = collections.defaultdict(list)
    by_position: dict[int, list[str]] = {}
    for position, prior_window in prior_windows:
        by_position[position] = prior_window
        for token, count in collections.Counter(prior_window).items():
            postings[token].append((position, count))
    return dict(postings), by_position


def indexed_best_prior(
    current_window: list[str],
    token_postings: dict[str, list[tuple[int, int]]],
    prior_by_position: dict[int, list[str]],
) -> tuple[int, float, list[str]]:
    """Find the exact best Counter-overlap candidate using token postings."""

    current_counts = collections.Counter(current_window)
    candidate_overlap: dict[int, int] = collections.defaultdict(int)
    for token, current_count in current_counts.items():
        for position, prior_count in token_postings.get(token, []):
            candidate_overlap[position] += min(current_count, prior_count)
    best_position = -1
    best_overlap = 0
    for position, overlap in candidate_overlap.items():
        if overlap > best_overlap or (overlap == best_overlap and overlap > 0 and (best_position == -1 or position < best_position)):
            best_position = position
            best_overlap = overlap
    if best_position == -1:
        return -1, 0.0, []
    return best_position, best_overlap / len(current_window), prior_by_position[best_position]


def excerpt(tokens: list[str], lang: str) -> str:
    if lang == "zh":
        if not tokens:
            return ""
        return (tokens[0][0] + "".join(token[-1] for token in tokens))[:80]
    return " ".join(tokens[:24])


def _findings(
    current_windows: list[tuple[int, list[str]]],
    prior_windows: list[tuple[int, list[str]]],
    lang: str,
    threshold: float,
    indexed: bool,
) -> list[dict[str, Any]]:
    token_postings, prior_by_position = build_token_postings(prior_windows)
    findings: list[dict[str, Any]] = []
    for current_index, current_window in current_windows:
        if indexed:
            prior_index, score, prior_window = indexed_best_prior(current_window, token_postings, prior_by_position)
        else:
            prior_index, score, prior_window = best_prior(current_window, prior_windows)
        if score >= threshold:
            findings.append(
                {
                    "current_pos": current_index,
                    "prior_pos": prior_index,
                    "overlap": round(score, 3),
                    "current_excerpt": excerpt(current_window, lang),
                    "prior_excerpt": excerpt(prior_window, lang),
                }
            )
    return findings


def analyze_texts(current_text: str, prior_text: str, lang: str, window: int, threshold: float) -> dict[str, Any]:
    if not math.isfinite(threshold) or not 0.0 <= threshold <= 1.0:
        raise ToolError("--threshold must be a finite value between 0 and 1")
    current_tokens = tokenize(current_text, lang)
    prior_tokens = tokenize(prior_text, lang)
    current_windows = windows(current_tokens, window)
    prior_windows = windows(prior_tokens, window)
    findings = _findings(current_windows, prior_windows, lang, threshold, indexed=True)
    ratio = len(findings) / len(current_windows) if current_windows else 0.0
    return {
        "lang": lang,
        "window": window,
        "threshold": threshold,
        "current_window_count": len(current_windows),
        "over_threshold_count": len(findings),
        "over_threshold_ratio": round(ratio, 3),
        "findings": findings,
        "algorithm": "token_postings_exact_counter_overlap",
    }


def naive_analyze_texts(current_text: str, prior_text: str, lang: str, window: int, threshold: float) -> dict[str, Any]:
    """Reference output used only by deterministic equivalence tests."""

    if not math.isfinite(threshold) or not 0.0 <= threshold <= 1.0:
        raise ToolError("--threshold must be a finite value between 0 and 1")
    current_tokens = tokenize(current_text, lang)
    prior_tokens = tokenize(prior_text, lang)
    current_windows = windows(current_tokens, window)
    prior_windows = windows(prior_tokens, window)
    findings = _findings(current_windows, prior_windows, lang, threshold, indexed=False)
    ratio = len(findings) / len(current_windows) if current_windows else 0.0
    return {
        "lang": lang,
        "window": window,
        "threshold": threshold,
        "current_window_count": len(current_windows),
        "over_threshold_count": len(findings),
        "over_threshold_ratio": round(ratio, 3),
        "findings": findings,
        "algorithm": "naive_reference",
    }


def render_markdown(result: dict[str, Any]) -> str:
    rows = [
        [item["current_pos"], item["prior_pos"], item["overlap"], item["current_excerpt"], item["prior_excerpt"]]
        for item in result["findings"][:50]
    ]
    return "\n".join(
        [
            f"Over-threshold windows: {result['over_threshold_count']} / {result['current_window_count']} ({result['over_threshold_ratio']:.3f})",
            markdown_table(["Current pos", "Prior pos", "Overlap", "Current excerpt", "Prior excerpt"], rows or [["-", "-", 0, "No over-threshold windows", ""]]),
            "Candidate selection uses exact token postings. Inputs dominated by one repeated token can still produce many candidates and approach quadratic work.",
        ]
    )


def main() -> int:
    args = parse_args()
    try:
        current_text = read_text_checked(args.current)
        prior_text = read_text_checked(args.prior)
        lang = infer_lang([current_text, prior_text]) if args.lang == "auto" else args.lang
        result = analyze_texts(current_text, prior_text, lang, args.window, args.threshold)
        result.update({"current": args.current, "prior": args.prior})
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(render_markdown(result))
        return 1 if result["findings"] else 0
    except ToolError as exc:
        print_error(exc)
        return 2


if __name__ == "__main__":
    sys.exit(main())
