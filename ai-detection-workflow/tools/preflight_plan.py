#!/usr/bin/env python3
"""Parse executable edit plans and verify their exact preconditions."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import guardrails_diff
import scan_rules
from tool_common import ToolError, infer_lang, load_rules_yaml, markdown_table, print_error, read_text_checked, repo_path


ROUND_RE = re.compile(r"^##\s+Round\s+(\d+)\b(.*)$", re.IGNORECASE)
FIX_RE = re.compile(r"^#{3,6}\s+Fix\s+([^—:\-]+?)(?:\s*[—:\-].*)?$", re.IGNORECASE)
FIELD_RE = re.compile(r"^\s*(?:[-*]\s+)?\*\*([^:]+):\*\*\s*(.*?)\s*$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Validate a contract-format multi-file plan. The legacy --doc mode remains available "
            "for one document and existing BEFORE-only fixtures."
        )
    )
    parser.add_argument("--plan", required=True, help="Plan file containing round and fix blocks.")
    parser.add_argument("--doc", help="Legacy single target document; bypasses contract-format plan fields.")
    parser.add_argument("--round", default="all", help="Round number or all. Requires --project-root unless --doc is used.")
    parser.add_argument("--project-root", help="Root containing every plan target.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown.")
    return parser.parse_args()


def _field_value(lines: list[str], name: str) -> str | None:
    for line in lines:
        match = FIELD_RE.match(line)
        if match and match.group(1).strip().lower() == name.lower():
            return match.group(2).strip().strip("`")
    return None


def _quote_block(lines: list[str], label: str) -> str | None:
    label_lower = label.lower()
    for index, line in enumerate(lines):
        lowered = line.lower()
        if label_lower not in lowered or "verbatim" not in lowered:
            continue
        collected: list[str] = []
        cursor = index + 1
        while cursor < len(lines) and not lines[cursor].strip():
            cursor += 1
        while cursor < len(lines) and lines[cursor].lstrip().startswith(">"):
            collected.append(re.sub(r"^\s*>\s?", "", lines[cursor]))
            cursor += 1
        if collected:
            return "\n".join(collected)
    return None


def _plan_metadata(lines: list[str]) -> dict[str, Any]:
    metadata = {
        "project_root": _field_value(lines, "Project root"),
        "plan_language": _field_value(lines, "Plan language"),
        "secondary_scan_disposition": _field_value(lines, "Secondary scan disposition"),
        "total_rounds": None,
    }
    total = _field_value(lines, "Total rounds")
    if total:
        match = re.search(r"\b(\d+)\b", total)
        if match:
            metadata["total_rounds"] = int(match.group(1))
    return metadata


def parse_plan(plan_text: str) -> dict[str, Any]:
    """Parse the documented plan template without accepting implicit fixes."""

    lines = plan_text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    rounds: list[dict[str, Any]] = []
    fixes_at: list[tuple[int, dict[str, Any]]] = []
    current_round: dict[str, Any] | None = None
    for index, line in enumerate(lines):
        round_match = ROUND_RE.match(line.strip())
        if round_match:
            number = int(round_match.group(1))
            if any(round_item["number"] == number for round_item in rounds):
                raise ToolError(f"duplicate Round {number} heading")
            current_round = {"number": number, "title": round_match.group(2).strip(), "fixes": []}
            rounds.append(current_round)
            continue
        fix_match = FIX_RE.match(line.strip())
        if fix_match:
            fix_id = fix_match.group(1).strip()
            if any(item[1]["fix_id"] == fix_id for item in fixes_at):
                raise ToolError(f"duplicate fix id {fix_id}")
            fixes_at.append(
                (
                    index,
                    {
                        "fix_id": fix_id,
                        "round": current_round["number"] if current_round else None,
                        "round_title": current_round["title"] if current_round else "",
                    },
                )
            )

    all_fixes: list[dict[str, Any]] = []
    for position, (start, fix) in enumerate(fixes_at):
        end = fixes_at[position + 1][0] if position + 1 < len(fixes_at) else len(lines)
        for line_index in range(start + 1, end):
            if ROUND_RE.match(lines[line_index].strip()):
                end = line_index
                break
        block = lines[start:end]
        fix.update(
            {
                "file": _field_value(block, "File"),
                "language": _field_value(block, "Language"),
                "prior_file": _field_value(block, "Prior file"),
                "secondary_scan_disposition": _field_value(block, "Secondary scan disposition"),
                "before": _quote_block(block, "before"),
                "after": _quote_block(block, "after"),
            }
        )
        all_fixes.append(fix)
        if fix["round"] is not None:
            round_item = next(item for item in rounds if item["number"] == fix["round"])
            round_item["fixes"].append(fix)
    return {"metadata": _plan_metadata(lines), "rounds": rounds, "fixes": all_fixes}


def extract_before_blocks(plan_text: str) -> list[dict[str, str]]:
    """Backward-compatible extractor used by the legacy --doc mode."""

    parsed = parse_plan(plan_text)
    blocks: list[dict[str, str]] = []
    for index, fix in enumerate(parsed["fixes"], start=1):
        if fix["before"]:
            blocks.append({"fix_id": fix["fix_id"] or str(index), "before": fix["before"]})
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
    return "pass" if count == 1 else "zero" if count == 0 else "multi"


def _contract_blockers(parsed: dict[str, Any], contract: dict[str, Any]) -> list[str]:
    blockers: list[str] = []
    metadata = parsed["metadata"]
    total_rounds = metadata["total_rounds"]
    allowed = contract["rounds"]["allowed_total_round_counts"]
    if total_rounds not in allowed:
        blockers.append(f"total rounds must be one of {allowed}")
    round_numbers = [round_item["number"] for round_item in parsed["rounds"]]
    if total_rounds and round_numbers != list(range(1, total_rounds + 1)):
        blockers.append("round headings must be contiguous from 1 through declared total rounds")
    if total_rounds and parsed["rounds"]:
        final_round = parsed["rounds"][-1]
        if "audit" not in final_round["title"].lower() or final_round["fixes"]:
            blockers.append("final round must be audit-only and contain no fixes")

    plan_language = (metadata["plan_language"] or "").lower()
    if plan_language not in {"en", "zh", "mixed"}:
        blockers.append("plan language must be en, zh, or mixed")
    for fix in parsed["fixes"]:
        if fix["round"] is None:
            blockers.append(f"{fix['fix_id']}: fix must appear inside a numbered round")
    tiers = set(contract["editing"]["risk_tiers"])
    for round_item in parsed["rounds"]:
        if not round_item["fixes"]:
            continue
        title_match = re.search(r"\btier\s+([A-Za-z])\b", round_item["title"], flags=re.IGNORECASE)
        if not title_match or title_match.group(1).upper() not in tiers:
            blockers.append(f"Round {round_item['number']} must declare one A/B/C tier")
        for fix in round_item["fixes"]:
            for field in ("file", "before", "after", "secondary_scan_disposition"):
                if not fix.get(field):
                    blockers.append(f"{fix['fix_id']}: missing required {field.replace('_', ' ')}")
            if plan_language == "mixed" and not fix.get("language"):
                blockers.append(f"{fix['fix_id']}: mixed plan requires per-fix language")
            language = (fix.get("language") or plan_language).lower()
            if language not in {"en", "zh"}:
                blockers.append(f"{fix['fix_id']}: language must resolve to en or zh")
            if fix.get("secondary_scan_disposition") and fix["secondary_scan_disposition"].lower() not in {"acknowledged", "none"}:
                blockers.append(f"{fix['fix_id']}: secondary scan disposition must be acknowledged or none")
    return blockers


def _resolve_inside_root(value: str, project_root: Path) -> tuple[Path | None, str | None]:
    candidate = Path(value)
    resolved = candidate.resolve() if candidate.is_absolute() else (project_root / candidate).resolve()
    try:
        resolved.relative_to(project_root)
    except ValueError:
        return None, f"path escapes project root: {value}"
    return resolved, None


def _guardrail_preserved(before: str, after: str, language: str) -> tuple[bool, list[str]]:
    comparison = guardrails_diff.compare_texts(before, after, language)
    failures = [item["check"] for item in comparison["checks"] if item["severity"] == "hard_failure" and item["status"] == "hard_fail"]
    return not comparison["hard_failure"], failures


def preflight(
    plan_path: str | Path,
    project_root: str | Path,
    round_selection: str,
    contract: dict[str, Any],
) -> dict[str, Any]:
    """Validate all selected fixes and return machine-readable evidence."""

    if round_selection != "all" and not round_selection.isdigit():
        raise ToolError("--round must be all or a positive integer")
    root = Path(project_root).resolve()
    if not root.is_dir():
        raise ToolError(f"project root is not a directory: {root}")
    plan_full_path = Path(plan_path).resolve()
    parsed = parse_plan(read_text_checked(plan_full_path))
    blockers = _contract_blockers(parsed, contract)
    selected_rounds = {round_item["number"] for round_item in parsed["rounds"]} if round_selection == "all" else {int(round_selection)}
    if round_selection != "all" and int(round_selection) not in {round_item["number"] for round_item in parsed["rounds"]}:
        blockers.append(f"requested round {round_selection} does not exist")

    rules_cache: dict[str, list[dict[str, Any]]] = {}
    fix_results: list[dict[str, Any]] = []
    plan_language = (parsed["metadata"]["plan_language"] or "").lower()
    for fix in parsed["fixes"]:
        if fix["round"] not in selected_rounds:
            continue
        result: dict[str, Any] = {
            "round": fix["round"],
            "fix_id": fix["fix_id"],
            "target": None,
            "target_relative": None,
            "language": (fix.get("language") or plan_language).lower(),
            "before_count": None,
            "guardrail_preserved": None,
            "guardrail_failures": [],
            "after_actionable_hits": None,
            "after_review_hits": None,
            "secondary_scan_disposition": fix.get("secondary_scan_disposition"),
            "status": "blocking",
            "blockers": [],
            "prior_path": None,
        }
        if not all(fix.get(field) for field in ("file", "before", "after", "secondary_scan_disposition")):
            result["blockers"].append("required fix fields are missing")
            fix_results.append(result)
            continue
        target, path_issue = _resolve_inside_root(fix["file"], root)
        if path_issue:
            result["blockers"].append(path_issue)
            fix_results.append(result)
            continue
        result["target"] = str(target)
        result["target_relative"] = str(target.relative_to(root))
        if fix.get("prior_file"):
            prior, prior_issue = _resolve_inside_root(fix["prior_file"], root)
            if prior_issue:
                result["blockers"].append(prior_issue)
            else:
                result["prior_path"] = str(prior)
        try:
            target_text = read_text_checked(target)
        except ToolError as exc:
            result["blockers"].append(str(exc))
            fix_results.append(result)
            continue
        result["before_count"] = count_literal(target_text, fix["before"])
        if result["before_count"] != 1:
            result["blockers"].append(f"BEFORE occurs {result['before_count']} times")
        language = result["language"]
        guardrail_language = language if language in {"en", "zh"} else infer_lang([fix["before"], fix["after"]])
        preserved, guardrail_failures = _guardrail_preserved(fix["before"], fix["after"], guardrail_language)
        result["guardrail_preserved"] = preserved
        result["guardrail_failures"] = guardrail_failures
        if not preserved:
            result["blockers"].append("guardrail text changed: " + ", ".join(guardrail_failures))
        if language in {"en", "zh"}:
            if language not in rules_cache:
                rules_cache[language] = load_rules_yaml(repo_path(Path("rules") / language / "rules.yaml"))
            after_scan = scan_rules.scan_text(fix["after"], rules_cache[language], language)
            result["after_actionable_hits"] = after_scan["aggregate"]["actionable_unique_spans"]
            result["after_review_hits"] = after_scan["aggregate"]["review_unique_spans"]
            if (result["after_actionable_hits"] or result["after_review_hits"]) and fix["secondary_scan_disposition"].lower() != "acknowledged":
                result["blockers"].append("AFTER rule hits require an acknowledged secondary scan disposition")
        else:
            result["blockers"].append("language did not resolve to en or zh")
        result["status"] = "pass" if not result["blockers"] else "blocking"
        fix_results.append(result)

    target_languages: dict[str, set[str]] = {}
    for result in fix_results:
        if result["target"] and result["language"] in {"en", "zh"}:
            target_languages.setdefault(result["target"], set()).add(result["language"])
    for target, languages in sorted(target_languages.items()):
        if len(languages) > 1:
            blockers.append(
                f"{Path(target).relative_to(root)}: target has inconsistent per-fix languages "
                + ", ".join(sorted(languages))
            )

    blockers.extend(
        f"Round {result['round']} {result['fix_id']}: {message}"
        for result in fix_results
        for message in result["blockers"]
    )
    return {
        "plan_path": str(plan_full_path),
        "project_root": str(root),
        "round_selection": round_selection,
        "metadata": parsed["metadata"],
        "fixes": fix_results,
        "blockers": blockers,
        "result_status": "executable" if not blockers else "blocking_review",
    }


def legacy_preflight(plan_path: str | Path, document_path: str | Path) -> dict[str, Any]:
    plan_text = read_text_checked(plan_path)
    document_text = read_text_checked(document_path)
    blocks = extract_before_blocks(plan_text)
    if not blocks:
        raise ToolError(f"no BEFORE blocks found in {plan_path}")
    results = []
    for block in blocks:
        count = count_literal(document_text, block["before"])
        results.append({"fix_id": block["fix_id"], "occurrences": count, "status": status_for(count)})
    return {"mode": "legacy_single_file", "plan": str(plan_path), "document": str(document_path), "results": results}


def render_preflight(result: dict[str, Any]) -> str:
    if result.get("mode") == "legacy_single_file":
        rows = [[item["fix_id"], item["occurrences"], item["status"]] for item in result["results"]]
        return markdown_table(["Fix ID", "Occurrences", "pass-zero-multi"], rows)
    rows = [
        [
            item["round"],
            item["fix_id"],
            item["target_relative"] or "-",
            item["before_count"],
            item["guardrail_preserved"],
            item["after_actionable_hits"],
            item["secondary_scan_disposition"] or "-",
            item["status"],
        ]
        for item in result["fixes"]
    ]
    return "\n".join(
        [
            markdown_table(["Round", "Fix", "Target", "BEFORE", "Guardrails", "AFTER actionable", "Disposition", "Status"], rows or [["-", "-", "-", "-", "-", "-", "-", "pass"]]),
            "",
            f"Result: {result['result_status']}",
            *( ["Blockers:", *[f"- {item}" for item in result["blockers"]]] if result["blockers"] else [] ),
        ]
    )


def main() -> int:
    args = parse_args()
    try:
        if args.doc:
            result = legacy_preflight(args.plan, args.doc)
            if args.json:
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print(render_preflight(result))
            return 1 if any(item["occurrences"] != 1 for item in result["results"]) else 0
        if not args.project_root:
            raise ToolError("--project-root is required unless --doc is used")
        contract_path = repo_path("workflow/contract.json")
        contract = json.loads(contract_path.read_text(encoding="utf-8"))
        result = preflight(args.plan, args.project_root, args.round, contract)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(render_preflight(result))
        return 0 if result["result_status"] == "executable" else 1
    except (ToolError, OSError, json.JSONDecodeError) as exc:
        print_error(exc)
        return 2


if __name__ == "__main__":
    sys.exit(main())
