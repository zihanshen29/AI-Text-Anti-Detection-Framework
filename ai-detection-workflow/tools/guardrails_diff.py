#!/usr/bin/env python3
"""Check deterministic fidelity guardrails between source and rewrite."""

from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from typing import Any

from tool_common import ToolError, infer_lang, markdown_table, print_error, read_text_checked


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare source/rewrite guardrails without semantic scoring.")
    parser.add_argument("--source", required=True, help="Original/source document.")
    parser.add_argument("--rewrite", required=True, help="Rewritten document.")
    parser.add_argument("--lang", choices=["en", "zh", "auto"], default="auto", help="Document language. Defaults to auto.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown.")
    return parser.parse_args()


def multiset(values: list[str]) -> dict[str, int]:
    return dict(collections.Counter(values))


def numbers(text: str) -> dict[str, int]:
    return multiset(re.findall(r"(?<![\w.])-?\d+(?:\.\d+)?%?", text))


def citation_keys(text: str) -> dict[str, int]:
    keys: list[str] = []
    keys.extend(re.findall(r"\[(\d+)\]", text))
    for group in re.findall(r"\\cite\{([^}]+)\}", text):
        keys.extend(key.strip() for key in group.split(",") if key.strip())
    return multiset(keys)


def headings(text: str) -> list[str]:
    return [m.group(0).strip() for m in re.finditer(r"^#{1,6}\s+.+$", text, flags=re.M)]


def labels(text: str) -> dict[str, int]:
    found: list[str] = []
    found.extend(f"label:{x}" for x in re.findall(r"\\label\{([^}]+)\}", text))
    found.extend(f"figure:{x}" for x in re.findall(r"\bFigure\s+(\d+(?:\.\d+)*)", text, flags=re.I))
    found.extend(f"table:{x}" for x in re.findall(r"\bTable\s+(\d+(?:\.\d+)*)", text, flags=re.I))
    found.extend(f"图:{x}" for x in re.findall(r"图\s*([0-9一二三四五六七八九十]+)", text))
    found.extend(f"表:{x}" for x in re.findall(r"表\s*([0-9一二三四五六七八九十]+)", text))
    return multiset(found)


def cjk_count(text: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", text))


def compare_value(name: str, before: Any, after: Any) -> dict[str, Any]:
    passed = before == after
    return {
        "check": name,
        "status": "pass" if passed else "fail",
        "source": before,
        "rewrite": after,
    }


def summarize(value: Any) -> str:
    text = json.dumps(value, ensure_ascii=False, sort_keys=True)
    if len(text) > 120:
        return text[:117] + "..."
    return text


def main() -> int:
    args = parse_args()
    try:
        source = read_text_checked(args.source)
        rewrite = read_text_checked(args.rewrite)
        lang = infer_lang([source, rewrite]) if args.lang == "auto" else args.lang

        checks = [
            compare_value("number token multiset", numbers(source), numbers(rewrite)),
            compare_value("citation key multiset", citation_keys(source), citation_keys(rewrite)),
            compare_value("markdown heading sequence", headings(source), headings(rewrite)),
            compare_value("formula/figure/table label multiset", labels(source), labels(rewrite)),
        ]
        if lang == "en":
            checks.append(
                {
                    "check": "EN rewrite CJK residual",
                    "status": "pass" if cjk_count(rewrite) == 0 else "fail",
                    "source": cjk_count(source),
                    "rewrite": cjk_count(rewrite),
                }
            )

        if args.json:
            print(json.dumps({"source": args.source, "rewrite": args.rewrite, "lang": lang, "checks": checks}, ensure_ascii=False, indent=2))
        else:
            rows = [[item["check"], item["status"], summarize(item["source"]), summarize(item["rewrite"])] for item in checks]
            print(markdown_table(["Check", "Status", "Source", "Rewrite"], rows))
        return 1 if any(item["status"] != "pass" for item in checks) else 0
    except ToolError as exc:
        print_error(exc)
        return 2


if __name__ == "__main__":
    sys.exit(main())
