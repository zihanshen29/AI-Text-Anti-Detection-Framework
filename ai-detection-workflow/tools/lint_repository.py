#!/usr/bin/env python3
"""Lint active deterministic workflow configuration without third-party packages."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from tool_common import ToolError, auto_literal_issues, load_context_whitelist, load_rules_yaml, print_error


WORKFLOW_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = WORKFLOW_ROOT / "workflow" / "contract.json"
EXPECTED_CONTRACT = {
    "schema_version": 1,
    "release": "1.3.0",
    "rounds": {
        "allowed_total_round_counts": [3, 5, 7],
        "zero_round_discovery_allowed": True,
        "final_audit_required_when_layer2_runs": True,
    },
    "editing": {
        "risk_tiers": ["A", "B", "C"],
        "sweep_is_a_tier": False,
        "tier_mixing_allowed": False,
        "exact_before_after_required": True,
    },
    "anti_regression": {"window_tokens": 10, "overlap_threshold": 0.7},
    "rollback": {"unit": "whole_round", "continue_after_fix_failure": False},
    "batch_evaluation": {
        "primary_population": "all_valid_inputs",
        "quality_failure_threshold": 25,
        "hard_fail_excluded_from_primary": False,
        "only_input_invalid_excluded": True,
    },
}
ACTIVE_CONTRACT_PATHS = (
    Path("SKILL.md"),
    Path("workflow/discovery.md"),
    Path("workflow/planning.md"),
    Path("workflow/execution.md"),
    Path("templates/discovery_output.md"),
    Path("templates/plan_output.md"),
    Path("templates/changes_log.md"),
    Path("templates/batch_eval_output.md"),
    Path("meta/prompts/eval_prompt.md"),
)
STALE_CONTRACT_PATTERNS = (
    (r"3\s*(?:-|–|to)\s*6", "stale total-round range; use 3/5/7"),
    (r"\b(?:risk\s+)?tier\s+D\b", "D is not an editing risk tier"),
    (r"\b0\.7\b(?!0)", "stale overlap threshold; express the policy as 0.70"),
    (r"(?:optional|skip(?:ped)?|omit(?:ted)?)\s+(?:the\s+)?(?:final\s+)?audit", "final audit is required after Layer 2"),
    (r"(?:rollback|roll back).{0,64}(?:single|individual|one)[ -]?(?:fix|change)", "rollback unit must be a whole round"),
    (
        r"(?:outlier|hard[ -]?fail|<\s*25\s*/\s*35).{0,128}exclude(?:d)?\s+from\s+(?:aggregate|average|primary)"
        r"|exclude(?:d)?\s+(?:outlier|hard[ -]?fail|<\s*25\s*/\s*35).{0,128}from\s+(?:aggregate|average|primary)",
        "valid low-quality and hard-fail inputs remain in the primary aggregate",
    ),
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lint active workflow configuration and documentation contracts.")
    parser.add_argument("mode", choices=["rules", "contract", "gates", "all"], help="Lint target.")
    return parser.parse_args()


def load_contract() -> dict:
    try:
        return json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ToolError(f"cannot read workflow contract {CONTRACT_PATH}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ToolError(f"invalid workflow contract JSON {CONTRACT_PATH}: {exc}") from exc


def stale_contract_forms(text: str) -> list[str]:
    return [message for pattern, message in STALE_CONTRACT_PATTERNS if re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL)]


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
    issues: list[str] = []
    contract = load_contract()
    if contract != EXPECTED_CONTRACT:
        issues.append("workflow/contract.json does not equal the frozen v1.3.0 contract")
    for relative_path in ACTIVE_CONTRACT_PATHS:
        path = WORKFLOW_ROOT / relative_path
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            issues.append(f"cannot read active contract consumer {relative_path}: {exc}")
            continue
        if "workflow/contract.json" not in text:
            issues.append(f"{relative_path}: missing workflow/contract.json reference")
        for message in stale_contract_forms(text):
            issues.append(f"{relative_path}: {message}")
    return issues


def lint_gates() -> list[str]:
    required = [
        WORKFLOW_ROOT / "tools" / "preflight_plan.py",
        WORKFLOW_ROOT / "tools" / "workflow_check.py",
        CONTRACT_PATH,
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
