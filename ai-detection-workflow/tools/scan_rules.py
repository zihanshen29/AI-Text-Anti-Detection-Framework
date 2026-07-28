#!/usr/bin/env python3
"""Scan prose with deterministic, context-aware machine-readable rules."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

from tool_common import (
    ToolError,
    infer_lang,
    load_context_whitelist,
    load_rules_yaml,
    markdown_table,
    print_error,
    read_text_checked,
    repo_path,
    unit_count,
)


DISCLAIMER = "Offline rule hits only; not a detector score."


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Collect literal and regex rule spans, apply configured context dispositions, "
            "and report unique actionable evidence."
        )
    )
    parser.add_argument("--text", action="append", required=True, help="Text file to scan. May be passed multiple times.")
    parser.add_argument("--lang", choices=["en", "zh", "auto"], default="auto", help="Language. Defaults to auto.")
    parser.add_argument("--rules", help="Rules YAML. Defaults to rules/<lang>/rules.yaml.")
    parser.add_argument("--baseline", help="Optional source file for before/after comparison.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown.")
    return parser.parse_args()


def literal_spans(text: str, literal: str, lang: str) -> list[tuple[int, int, str]]:
    if not literal:
        return []
    if lang == "zh":
        spans: list[tuple[int, int, str]] = []
        start = 0
        while True:
            index = text.find(literal, start)
            if index == -1:
                return spans
            spans.append((index, index + len(literal), text[index : index + len(literal)]))
            start = index + len(literal)
    escaped = re.escape(literal)
    left = r"(?<![A-Za-z0-9_])" if re.match(r"^[A-Za-z0-9_]", literal) else ""
    right = r"(?![A-Za-z0-9_])" if re.search(r"[A-Za-z0-9_]$", literal) else ""
    return [(match.start(), match.end(), match.group(0)) for match in re.finditer(left + escaped + right, text, flags=re.IGNORECASE)]


def regex_spans(text: str, pattern: str, lang: str) -> list[tuple[int, int, str]]:
    flags = re.IGNORECASE if lang == "en" else 0
    try:
        return [(match.start(), match.end(), match.group(0)) for match in re.finditer(pattern, text, flags=flags) if match.start() != match.end()]
    except re.error as exc:
        raise ToolError(f"invalid regex pattern {pattern!r}: {exc}") from exc


def literal_count(text: str, literal: str, lang: str) -> int:
    """Compatibility helper retained for callers of the original scanner."""

    return len(literal_spans(text, literal, lang))


def regex_count(text: str, pattern: str, lang: str) -> int:
    """Compatibility helper retained for callers of the original scanner."""

    return len(regex_spans(text, pattern, lang))


def matcher_spans(text: str, rule: dict[str, Any], lang: str) -> list[dict[str, Any]]:
    spans: list[dict[str, Any]] = []
    for literal in rule.get("literals", []):
        for start, end, matched in literal_spans(text, literal, lang):
            spans.append({"start": start, "end": end, "text": matched, "rule_id": rule["id"]})
    patterns = list(rule.get("patterns", []))
    if rule.get("pattern"):
        patterns.insert(0, rule["pattern"])
    for pattern in patterns:
        for start, end, matched in regex_spans(text, pattern, lang):
            spans.append({"start": start, "end": end, "text": matched, "rule_id": rule["id"]})
    return spans


def _context_disposition(
    text: str,
    start: int,
    end: int,
    rule_ids: set[str],
    rules_by_id: dict[str, dict[str, Any]],
    whitelist_cache: dict[tuple[str, str], list[dict[str, Any]]],
) -> tuple[str, list[str]]:
    """Return the longest containing whitelist context for one unique span."""

    candidates: list[tuple[int, str, str]] = []
    matched_text = text[start:end]
    for rule_id in rule_ids:
        rule = rules_by_id[rule_id]
        reference = rule.get("whitelist_ref")
        if not reference:
            continue
        workflow_root = str(rule["_workflow_root"])
        cache_key = (workflow_root, reference)
        if cache_key not in whitelist_cache:
            whitelist_cache[cache_key] = load_context_whitelist(reference, workflow_root)
        for entry in whitelist_cache[cache_key]:
            if rule_id not in entry["rule_ids"] or entry["trigger"] not in matched_text:
                continue
            for match in re.finditer(entry["context_matcher"], text):
                if match.start() <= start and end <= match.end():
                    candidates.append((match.end() - match.start(), entry["disposition"], entry["id"]))
    if not candidates:
        return "actionable", []

    longest = max(item[0] for item in candidates)
    winners = [(disposition, entry_id) for length, disposition, entry_id in candidates if length == longest]
    dispositions = {disposition for disposition, _ in winners}
    if len(dispositions) != 1:
        details = ", ".join(sorted(f"{entry_id}:{disposition}" for disposition, entry_id in winners))
        raise ToolError(f"conflicting equal-length context whitelist entries for {matched_text!r}: {details}")
    disposition = next(iter(dispositions))
    return disposition, sorted({entry_id for _, entry_id in winners})


def scan_text(text: str, rules: list[dict[str, Any]], lang: str) -> dict[str, Any]:
    """Scan one text payload, preserving raw hits and merging exact spans."""

    rules_by_id = {rule["id"]: rule for rule in rules}
    raw_hits: list[dict[str, Any]] = []
    manual_rules: list[dict[str, Any]] = []
    for rule in rules:
        if rule["scan"] != "auto":
            manual_rules.append({"id": rule["id"], "name": rule["name"], "reason": "manual-only, not counted"})
            continue
        raw_hits.extend(matcher_spans(text, rule, lang))

    grouped: dict[tuple[int, int], list[dict[str, Any]]] = defaultdict(list)
    for hit in raw_hits:
        grouped[(hit["start"], hit["end"])].append(hit)

    per_rule = {
        rule["id"]: {
            "id": rule["id"],
            "name": rule["name"],
            "family": rule["family"],
            "raw_rule_hits": 0,
            "whitelisted_unique_spans": 0,
            "review_unique_spans": 0,
            "actionable_unique_spans": 0,
        }
        for rule in rules
        if rule["scan"] == "auto"
    }
    for hit in raw_hits:
        per_rule[hit["rule_id"]]["raw_rule_hits"] += 1

    whitelist_cache: dict[tuple[str, str], list[dict[str, Any]]] = {}
    unique_hits: list[dict[str, Any]] = []
    for (start, end), hits in sorted(grouped.items()):
        rule_ids = {hit["rule_id"] for hit in hits}
        disposition, whitelist_entry_ids = _context_disposition(text, start, end, rule_ids, rules_by_id, whitelist_cache)
        for rule_id in rule_ids:
            per_rule[rule_id][f"{disposition}_unique_spans"] += 1
        unique_hits.append(
            {
                "start": start,
                "end": end,
                "text": text[start:end],
                "rule_ids": sorted(rule_ids),
                "disposition": disposition,
                "whitelist_entry_ids": whitelist_entry_ids,
            }
        )

    aggregate = {
        "raw_rule_hits": len(raw_hits),
        "raw_unique_spans": len(unique_hits),
        "whitelisted_unique_spans": sum(hit["disposition"] == "whitelisted" for hit in unique_hits),
        "review_unique_spans": sum(hit["disposition"] == "review" for hit in unique_hits),
        "actionable_unique_spans": sum(hit["disposition"] == "actionable" for hit in unique_hits),
    }
    for row in per_rule.values():
        row["per_1000_units"] = round(row["actionable_unique_spans"] * 1000 / unit_count(text, lang), 3)
    return {
        "lang": lang,
        "units": unit_count(text, lang),
        "rules": list(per_rule.values()),
        "manual_rules": manual_rules,
        "hits": unique_hits,
        "aggregate": aggregate,
    }


def scan_file(path: str, rules: list[dict[str, Any]], lang: str) -> dict[str, Any]:
    text = read_text_checked(path)
    cjk_count = len(re.findall(r"[\u4e00-\u9fff]", text))
    latin_count = len(re.findall(r"[A-Za-z]", text))
    if lang == "en" and cjk_count > 100 and cjk_count > latin_count * 0.1:
        raise ToolError(f"encoding/language preflight failed for {path}: EN scan found substantial CJK content")
    result = scan_text(text, rules, lang)
    result["file"] = str(path)
    return result


def default_rules_path(lang: str) -> Path:
    return repo_path(Path("rules") / lang / "rules.yaml")


def has_review_or_actionable(result: dict[str, Any]) -> bool:
    aggregate = result["aggregate"]
    return bool(aggregate["review_unique_spans"] or aggregate["actionable_unique_spans"])


def render_single(results: list[dict[str, Any]]) -> str:
    chunks: list[str] = []
    for result in results:
        rows = [
            [
                row["id"],
                row["name"],
                row["raw_rule_hits"],
                row["whitelisted_unique_spans"],
                row["review_unique_spans"],
                row["actionable_unique_spans"],
            ]
            for row in result["rules"]
            if row["raw_rule_hits"]
        ]
        chunks.extend(
            [
                f"## {result['file']}",
                "",
                markdown_table(
                    ["Rule", "Name", "Raw", "Whitelisted", "Review", "Actionable"],
                    rows or [["-", "No auto-rule hits", 0, 0, 0, 0]],
                ),
                "",
                "Aggregate: " + json.dumps(result["aggregate"], ensure_ascii=False, sort_keys=True),
            ]
        )
    chunks.append(DISCLAIMER)
    return "\n".join(chunks)


def render_baseline(baseline: dict[str, Any], current: dict[str, Any]) -> str:
    before = {row["id"]: row for row in baseline["rules"]}
    after = {row["id"]: row for row in current["rules"]}
    rows = []
    for rule_id in sorted(before):
        b = before[rule_id]
        a = after[rule_id]
        if b["raw_rule_hits"] or a["raw_rule_hits"]:
            rows.append(
                [
                    rule_id,
                    b["actionable_unique_spans"],
                    a["actionable_unique_spans"],
                    a["actionable_unique_spans"] - b["actionable_unique_spans"],
                ]
            )
    return "\n".join(
        [
            "## Baseline comparison",
            "",
            f"Baseline: {baseline['file']}",
            f"Current: {current['file']}",
            "",
            markdown_table(["Rule", "Before actionable", "After actionable", "Delta"], rows or [["-", 0, 0, 0]]),
            "",
            "Primary aggregate: actionable_unique_spans",
            f"Actionable unique spans before: {baseline['aggregate']['actionable_unique_spans']}",
            f"Actionable unique spans after: {current['aggregate']['actionable_unique_spans']}",
            DISCLAIMER,
        ]
    )


def main() -> int:
    args = parse_args()
    try:
        preload_texts = [read_text_checked(path) for path in args.text]
        if args.baseline:
            preload_texts.append(read_text_checked(args.baseline))
        lang = infer_lang(preload_texts) if args.lang == "auto" else args.lang
        rules_path = Path(args.rules) if args.rules else default_rules_path(lang)
        rules = load_rules_yaml(rules_path)

        if args.baseline:
            baseline = scan_file(args.baseline, rules, lang)
            comparisons = []
            outputs = []
            exit_code = 0
            for path in args.text:
                current = scan_file(path, rules, lang)
                comparisons.append({"baseline": baseline, "current": current})
                outputs.append(render_baseline(baseline, current))
                if has_review_or_actionable(baseline) or has_review_or_actionable(current):
                    exit_code = 1
            if args.json:
                print(json.dumps({"comparisons": comparisons, "disclaimer": DISCLAIMER}, ensure_ascii=False, indent=2))
            else:
                print("\n\n".join(outputs))
            return exit_code

        results = [scan_file(path, rules, lang) for path in args.text]
        if args.json:
            print(json.dumps({"results": results, "disclaimer": DISCLAIMER}, ensure_ascii=False, indent=2))
        else:
            print(render_single(results))
        return 1 if any(has_review_or_actionable(result) for result in results) else 0
    except ToolError as exc:
        print_error(exc)
        return 2


if __name__ == "__main__":
    sys.exit(main())
