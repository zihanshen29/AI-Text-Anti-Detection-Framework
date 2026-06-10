#!/usr/bin/env python3
"""Check that each plan BEFORE string appears exactly once in the target document."""

from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any

from tool_common import ToolError, markdown_table, print_error, read_text_checked


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Parse plan.md fix blocks and verify each BEFORE block appears exactly once in --doc. "
            "Matching is strict literal text; no fuzzy matching is attempted."
        )
    )
    parser.add_argument("--plan", required=True, help="Plan file containing fix blocks.")
    parser.add_argument("--doc", required=True, help="Current document to check.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown.")
    return parser.parse_args()


def extract_before_blocks(plan_text: str) -> list[dict[str, str]]:
    lines = plan_text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    blocks: list[dict[str, str]] = []
    current_fix = "unknown"
    fix_counter = 0
    i = 0
    while i < len(lines):
        line = lines[i]
        fix_match = re.match(r"^#{3,6}\s+Fix\s+([^—:]+)", line.strip())
        if fix_match:
            current_fix = fix_match.group(1).strip()
        before_label = line.strip().lower()
        if before_label.startswith("**before (") or before_label.startswith("before ("):
            collected: list[str] = []
            i += 1
            while i < len(lines) and lines[i].strip() == "":
                i += 1
            while i < len(lines) and lines[i].lstrip().startswith(">"):
                quote = re.sub(r"^\s*>\s?", "", lines[i])
                collected.append(quote)
                i += 1
            if collected:
                fix_counter += 1
                blocks.append({"fix_id": current_fix if current_fix != "unknown" else str(fix_counter), "before": "\n".join(collected)})
            continue
        i += 1
    return blocks


def count_literal(haystack: str, needle: str) -> int:
    if not needle:
        return 0
    count = 0
    start = 0
    while True:
        index = haystack.find(needle, start)
        if index == -1:
            return count
        count += 1
        start = index + len(needle)


def status_for(count: int) -> str:
    if count == 1:
        return "pass"
    if count == 0:
        return "zero"
    return "multi"


def main() -> int:
    args = parse_args()
    try:
        plan_text = read_text_checked(args.plan)
        doc_text = read_text_checked(args.doc)
        blocks = extract_before_blocks(plan_text)
        if not blocks:
            raise ToolError(f"no BEFORE blocks found in {args.plan}")
        results: list[dict[str, Any]] = []
        for block in blocks:
            count = count_literal(doc_text, block["before"])
            results.append({"fix_id": block["fix_id"], "occurrences": count, "status": status_for(count)})
        if args.json:
            print(json.dumps({"results": results}, ensure_ascii=False, indent=2))
        else:
            rows = [[row["fix_id"], row["occurrences"], row["status"]] for row in results]
            print(markdown_table(["Fix ID", "Occurrences", "pass-zero-multi"], rows))
        return 1 if any(row["occurrences"] != 1 for row in results) else 0
    except ToolError as exc:
        print_error(exc)
        return 2


if __name__ == "__main__":
    sys.exit(main())
