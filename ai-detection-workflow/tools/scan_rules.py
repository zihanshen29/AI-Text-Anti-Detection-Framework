#!/usr/bin/env python3
"""Scan prose with machine-readable AI-signal rules."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

from tool_common import ToolError, infer_lang, load_rules_yaml, markdown_table, print_error, read_text_checked, repo_path, unit_count


DISCLAIMER = "Offline literal hits only; not a detector score."


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Deterministically count literal/regex rule hits. EN sentence splitting and word boundaries "
            "are simple regex proxies; manual structural rules are listed but not counted."
        )
    )
    parser.add_argument("--text", action="append", required=True, help="Text file to scan. May be passed multiple times.")
    parser.add_argument("--lang", choices=["en", "zh", "auto"], default="auto", help="Language. Defaults to auto.")
    parser.add_argument("--rules", help="Rules YAML. Defaults to rules/<lang>/rules.yaml.")
    parser.add_argument("--baseline", help="Optional source file for before/after comparison.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown.")
    return parser.parse_args()


def literal_count(text: str, literal: str, lang: str) -> int:
    if not literal:
        return 0
    if lang == "zh":
        return text.count(literal)
    escaped = re.escape(literal)
    left = r"(?<![A-Za-z0-9_])" if re.match(r"^[A-Za-z0-9_]", literal) else ""
    right = r"(?![A-Za-z0-9_])" if re.search(r"[A-Za-z0-9_]$", literal) else ""
    return len(re.findall(left + escaped + right, text, flags=re.IGNORECASE))


def regex_count(text: str, pattern: str, lang: str) -> int:
    flags = re.IGNORECASE if lang == "en" else 0
    try:
        return len(re.findall(pattern, text, flags=flags))
    except re.error as exc:
        raise ToolError(f"invalid regex pattern {pattern!r}: {exc}") from exc


def scan_text(text: str, rules: list[dict[str, Any]], lang: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    units = unit_count(text, lang)
    counted: list[dict[str, Any]] = []
    manual: list[dict[str, Any]] = []
    for rule in rules:
        if rule["scan"] != "auto":
            manual.append({"id": rule["id"], "name": rule["name"], "reason": "manual-only, not counted"})
            continue
        count = 0
        if rule["match_type"] == "literal":
            for literal in rule.get("literals", []):
                count += literal_count(text, literal, lang)
        elif rule["match_type"] == "regex":
            count += regex_count(text, rule.get("pattern") or "", lang)
        else:
            manual.append({"id": rule["id"], "name": rule["name"], "reason": "manual-only, not counted"})
            continue
        counted.append(
            {
                "id": rule["id"],
                "name": rule["name"],
                "family": rule["family"],
                "count": count,
                "per_1000_units": round(count * 1000 / units, 3),
            }
        )
    return counted, manual


def scan_file(path: str, rules: list[dict[str, Any]], lang: str) -> dict[str, Any]:
    text = read_text_checked(path)
    cjk_count = len(re.findall(r"[\u4e00-\u9fff]", text))
    latin_count = len(re.findall(r"[A-Za-z]", text))
    if lang == "en" and cjk_count > 100 and cjk_count > latin_count * 0.1:
        raise ToolError(f"encoding/language preflight failed for {path}: EN scan found substantial CJK content")
    counted, manual = scan_text(text, rules, lang)
    return {
        "file": str(path),
        "lang": lang,
        "units": unit_count(text, lang),
        "rules": counted,
        "manual_rules": manual,
        "total_hits": sum(row["count"] for row in counted),
    }


def default_rules_path(lang: str) -> Path:
    return repo_path(Path("rules") / lang / "rules.yaml")


def render_single(results: list[dict[str, Any]]) -> str:
    chunks: list[str] = []
    for result in results:
        rows = [
            [row["id"], row["name"], row["family"], row["count"], row["per_1000_units"]]
            for row in result["rules"]
            if row["count"] > 0
        ]
        chunks.append(f"## {result['file']}\n")
        chunks.append(markdown_table(["Rule", "Name", "Family", "Hits", "Per 1k units"], rows or [["-", "No auto-rule hits", "-", 0, 0]]))
        chunks.append(f"\n\nTotal hits: {result['total_hits']}")
        if result["manual_rules"]:
            manual_ids = ", ".join(row["id"] for row in result["manual_rules"])
            chunks.append(f"\nManual-only rules not counted: {manual_ids}")
    chunks.append(f"\n{DISCLAIMER}")
    return "\n\n".join(chunks)


def render_baseline(baseline: dict[str, Any], current: dict[str, Any]) -> str:
    before = {row["id"]: row for row in baseline["rules"]}
    after = {row["id"]: row for row in current["rules"]}
    rows = []
    for rule_id in sorted(before):
        b = before[rule_id]
        a = after[rule_id]
        delta = a["count"] - b["count"]
        if b["count"] or a["count"]:
            rows.append([rule_id, b["name"], b["count"], a["count"], delta, a["per_1000_units"]])
    if not rows:
        rows = [["-", "No auto-rule hits", 0, 0, 0, 0]]
    manual_ids = ", ".join(row["id"] for row in baseline["manual_rules"])
    return "\n".join(
        [
            f"## Baseline comparison",
            "",
            f"Baseline: {baseline['file']}",
            f"Current: {current['file']}",
            "",
            markdown_table(["Rule", "Name", "Before", "After", "Delta", "After per 1k units"], rows),
            "",
            f"Total before: {baseline['total_hits']}",
            f"Total after: {current['total_hits']}",
            f"Manual-only rules not counted: {manual_ids}",
            DISCLAIMER,
        ]
    )


def main() -> int:
    args = parse_args()
    try:
        preload_texts = []
        if args.baseline:
            preload_texts.append(read_text_checked(args.baseline))
        for path in args.text:
            preload_texts.append(read_text_checked(path))
        lang = infer_lang(preload_texts) if args.lang == "auto" else args.lang
        rules_path = Path(args.rules) if args.rules else default_rules_path(lang)
        rules = load_rules_yaml(rules_path)

        if args.baseline:
            baseline = scan_file(args.baseline, rules, lang)
            outputs = []
            exit_code = 0
            json_results = []
            for path in args.text:
                current = scan_file(path, rules, lang)
                json_results.append({"baseline": baseline, "current": current})
                outputs.append(render_baseline(baseline, current))
                if current["total_hits"] or baseline["total_hits"]:
                    exit_code = 1
            if args.json:
                print(json.dumps({"comparisons": json_results, "disclaimer": DISCLAIMER}, ensure_ascii=False, indent=2))
            else:
                print("\n\n".join(outputs))
            return exit_code

        results = [scan_file(path, rules, lang) for path in args.text]
        if args.json:
            print(json.dumps({"results": results, "disclaimer": DISCLAIMER}, ensure_ascii=False, indent=2))
        else:
            print(render_single(results))
        return 1 if any(result["total_hits"] for result in results) else 0
    except ToolError as exc:
        print_error(exc)
        return 2


if __name__ == "__main__":
    sys.exit(main())
