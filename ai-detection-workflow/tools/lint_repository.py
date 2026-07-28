#!/usr/bin/env python3
"""Lint active deterministic workflow configuration without third-party packages."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from tool_common import ToolError, auto_literal_issues, load_context_whitelist, load_rules_yaml, print_error


WORKFLOW_ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lint active workflow configuration and documentation contracts.")
    parser.add_argument("mode", choices=["rules", "contract", "gates", "all"], help="Lint target.")
    return parser.parse_args()


def lint_rules() -> list[str]:
    issues: list[str] = []
    for language in ("en", "zh"):
        rules = load_rules_yaml(WORKFLOW_ROOT / "rules" / language / "rules.yaml")
        issues.extend(auto_literal_issues(rules))
        references = {rule["whitelist_ref"] for rule in rules if rule.get("whitelist_ref")}
        for reference in references:
            load_context_whitelist(reference, WORKFLOW_ROOT)
    return issues


def lint_contract() -> list[str]:
    contract = WORKFLOW_ROOT / "workflow" / "contract.json"
    return [] if contract.exists() else ["workflow/contract.json is missing"]


def lint_gates() -> list[str]:
    required = [
        WORKFLOW_ROOT / "tools" / "preflight_plan.py",
        WORKFLOW_ROOT / "tools" / "workflow_check.py",
        WORKFLOW_ROOT / "workflow" / "contract.json",
    ]
    return [f"required gate artifact is missing: {path.relative_to(WORKFLOW_ROOT)}" for path in required if not path.exists()]


def main() -> int:
    args = parse_args()
    try:
        issues: list[str] = []
        if args.mode in {"rules", "all"}:
            issues.extend(lint_rules())
        if args.mode in {"contract", "all"}:
            issues.extend(lint_contract())
        if args.mode in {"gates", "all"}:
            issues.extend(lint_gates())
        if issues:
            for issue in issues:
                print(f"FAIL: {issue}")
            return 1
        print(f"{args.mode}: pass")
        return 0
    except ToolError as exc:
        print_error(exc)
        return 2


if __name__ == "__main__":
    sys.exit(main())
