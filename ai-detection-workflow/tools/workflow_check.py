#!/usr/bin/env python3
"""Run deterministic Layer 0, Layer 1, and Layer 2 workflow evidence gates."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import guardrails_diff
import overlap_check
import preflight_plan
import scan_rules
import structure_metrics
from tool_common import ToolError, infer_lang, load_rules_yaml, print_error, read_text_checked, repo_path


TOOL_VERSION = "1.3.0"
MANIFEST_KIND = "ai-detection-workflow-plan-manifest"
MANIFEST_VERSION = 1
HASH_KIND = "worktree_raw_sha256"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run deterministic workflow gates without external detector calls.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    discovery = subparsers.add_parser("discovery", help="Generate Layer 0 discovery evidence.")
    discovery.add_argument("--text", required=True, help="Document to inspect.")
    discovery.add_argument("--lang", choices=["en", "zh", "auto"], required=True, help="Language selection.")
    discovery.add_argument("--output", required=True, help="JSON evidence output path.")

    plan = subparsers.add_parser("plan", help="Validate Layer 1 plan evidence and optionally snapshot targets.")
    plan.add_argument("--plan", required=True, help="Plan path.")
    plan.add_argument("--round", required=True, help="Round number or all.")
    plan.add_argument("--project-root", required=True, help="Target project root.")
    plan.add_argument("--snapshot-dir", help="Optional directory for immutable pre-round snapshots.")
    plan.add_argument("--output", required=True, help="JSON evidence output path.")

    post_round = subparsers.add_parser("post-round", help="Validate Layer 2 post-round evidence.")
    post_round.add_argument("--manifest", required=True, help="Plan-generated JSON manifest.")
    post_round.add_argument("--output", required=True, help="JSON evidence output path.")
    return parser.parse_args()


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _hash_file(path: Path) -> dict[str, str]:
    try:
        payload = path.read_bytes()
    except OSError as exc:
        raise ToolError(f"cannot hash {path}: {exc}") from exc
    return {"hash_kind": HASH_KIND, "sha256": hashlib.sha256(payload).hexdigest()}


def _validate_hash_record(record: Any, label: str) -> None:
    if not isinstance(record, dict) or record.get("hash_kind") != HASH_KIND:
        raise ToolError(f"{label} must use {HASH_KIND}")
    digest = record.get("sha256")
    if not isinstance(digest, str) or len(digest) != 64 or any(character not in "0123456789abcdef" for character in digest.lower()):
        raise ToolError(f"{label} has an invalid SHA-256 digest")


def _load_contract() -> dict[str, Any]:
    path = repo_path("workflow/contract.json")
    try:
        contract = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ToolError(f"cannot read workflow contract {path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ToolError(f"invalid workflow contract {path}: {exc}") from exc
    if contract.get("schema_version") != 1 or contract.get("release") != TOOL_VERSION:
        raise ToolError("workflow contract is not compatible with workflow_check.py 1.3.0")
    return contract


def _base_evidence(command: str, contract: dict[str, Any]) -> dict[str, Any]:
    return {
        "tool_version": TOOL_VERSION,
        "command_type": command,
        "contract_version": contract["schema_version"],
        "timestamp_utc": _utc_now(),
        "external_detector_status": "not_run",
    }


def _write_json(path_value: str, payload: dict[str, Any]) -> Path:
    path = Path(path_value).resolve()
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    except OSError as exc:
        raise ToolError(f"cannot write JSON evidence {path}: {exc}") from exc
    return path


def run_discovery(text_path: str, language: str, contract: dict[str, Any]) -> dict[str, Any]:
    target = repo_path(text_path).resolve()
    text = read_text_checked(target)
    selected_language = infer_lang([text]) if language == "auto" else language
    rules = load_rules_yaml(repo_path(Path("rules") / selected_language / "rules.yaml"))
    scan = scan_rules.scan_file(str(target), rules, selected_language)
    structure = structure_metrics.compute(str(target), selected_language)
    result = _base_evidence("discovery", contract)
    result.update(
        {
            "normalized_paths": {"text": str(target)},
            "target": {"path": str(target), **_hash_file(target)},
            "language": selected_language,
            "component_results": {
                "encoding_language_preflight": {"status": "pass"},
                "rule_scan": {"status": "evidence", "aggregate": scan["aggregate"], "hits": scan["hits"]},
                "structure_metrics": {"status": "evidence", "metrics": structure},
            },
            "result_status": "complete",
        }
    )
    return result


def _snapshot_targets(preflight: dict[str, Any], snapshot_dir: Path, contract: dict[str, Any]) -> list[dict[str, Any]]:
    try:
        snapshot_dir.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        raise ToolError(f"cannot create snapshot directory {snapshot_dir}: {exc}") from exc
    grouped: dict[str, list[dict[str, Any]]] = {}
    for fix in preflight["fixes"]:
        grouped.setdefault(fix["target"], []).append(fix)
    targets: list[dict[str, Any]] = []
    root = Path(preflight["project_root"]).resolve()
    for index, (target_value, fixes) in enumerate(grouped.items(), start=1):
        target = Path(target_value).resolve()
        snapshot = snapshot_dir / f"{index:02d}_{target.name}"
        preflight_target = _hash_file(target)
        try:
            shutil.copyfile(target, snapshot)
        except OSError as exc:
            raise ToolError(f"cannot snapshot {target} to {snapshot}: {exc}") from exc
        prior_paths = sorted({fix["prior_path"] for fix in fixes if fix.get("prior_path")})
        prior_inputs = [{"path": value, **_hash_file(Path(value).resolve())} for value in prior_paths]
        snapshot_hash = _hash_file(snapshot)
        if snapshot_hash != preflight_target:
            raise ToolError(f"snapshot bytes differ from target immediately after copy: {target}")
        targets.append(
            {
                "target_path": str(target),
                "target_relative_path": str(target.relative_to(root)),
                "language": fixes[0]["language"],
                "rounds": sorted({fix["round"] for fix in fixes}),
                "fixes": [
                    {
                        "round": fix["round"],
                        "fix_id": fix["fix_id"],
                        "before_count": fix["before_count"],
                        "secondary_scan_disposition": fix["secondary_scan_disposition"],
                    }
                    for fix in fixes
                ],
                "prior_paths": prior_paths,
                "overlap_settings": {
                    "window_tokens": contract["anti_regression"]["window_tokens"],
                    "overlap_threshold": contract["anti_regression"]["overlap_threshold"],
                },
                "snapshot_path": str(snapshot.resolve()),
                "snapshot": snapshot_hash,
                "preflight_target": preflight_target,
                "prior_inputs": prior_inputs,
            }
        )
    return targets


def run_plan(
    plan_path: str,
    round_selection: str,
    project_root: str,
    snapshot_dir: str | None,
    output_path: str,
    contract: dict[str, Any],
) -> dict[str, Any]:
    preflight = preflight_plan.preflight(plan_path, project_root, round_selection, contract)
    contract_path = repo_path("workflow/contract.json").resolve()
    plan_input_path = Path(preflight["plan_path"]).resolve()
    output = Path(output_path).resolve()
    protected_inputs = {plan_input_path, contract_path}
    parsed_plan = preflight_plan.parse_plan(read_text_checked(plan_input_path))
    project = Path(preflight["project_root"]).resolve()
    for fix in parsed_plan["fixes"]:
        for key in ("file", "prior_file"):
            if not fix.get(key):
                continue
            candidate, issue = preflight_plan._resolve_inside_root(fix[key], project)
            if issue is None and candidate is not None:
                protected_inputs.add(candidate)
    if output in protected_inputs:
        raise ToolError(f"plan output must not overwrite an input file: {output}")
    result = _base_evidence("plan", contract)
    result.update(
        {
            "normalized_paths": {
                "plan": preflight["plan_path"],
                "project_root": preflight["project_root"],
                "output": str(output),
            },
            "plan_input": {"path": str(plan_input_path), **_hash_file(plan_input_path)},
            "contract_input": {"path": str(contract_path), **_hash_file(contract_path)},
            "round_selection": round_selection,
            "preflight": preflight,
            "result_status": preflight["result_status"],
            "manifest_generated": False,
        }
    )
    if snapshot_dir and preflight["result_status"] == "executable":
        snapshots = Path(snapshot_dir).resolve()
        result.update(
            {
                "manifest_kind": MANIFEST_KIND,
                "manifest_version": MANIFEST_VERSION,
                "generated_by": "workflow_check.py",
                "manifest_generated": True,
                "snapshot_dir": str(snapshots),
                "targets": _snapshot_targets(preflight, snapshots, contract),
            }
        )
    return result


def _guardrail_component(source: str, rewrite: str, language: str) -> dict[str, Any]:
    comparison = guardrails_diff.compare_texts(source, rewrite, language)
    status = "hard_fail" if comparison["hard_failure"] else "review_warning" if comparison["review_warning"] else "pass"
    return {
        "status": status,
        "checks": comparison["checks"],
        "hard_failure": comparison["hard_failure"],
        "review_warning": comparison["review_warning"],
        "context_changes": comparison["context_changes"],
    }


def _overlap_component(current: str, prior: str, language: str, window: int, threshold: float) -> dict[str, Any]:
    result = overlap_check.analyze_texts(current, prior, language, window, threshold)
    return {
        "status": "review_required" if result["findings"] else "pass",
        "window_tokens": window,
        "overlap_threshold": threshold,
        "over_threshold_count": result["over_threshold_count"],
        "findings": result["findings"],
        "algorithm": result["algorithm"],
    }


def _load_plan_manifest(path_value: str, contract: dict[str, Any]) -> tuple[Path, dict[str, Any]]:
    path = repo_path(path_value).resolve()
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ToolError(f"cannot read plan manifest {path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ToolError(f"invalid plan manifest JSON {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise ToolError("plan manifest must be a JSON object")
    required = {
        "tool_version",
        "command_type",
        "contract_version",
        "external_detector_status",
        "result_status",
        "manifest_kind",
        "manifest_version",
        "generated_by",
        "manifest_generated",
        "snapshot_dir",
        "round_selection",
        "targets",
        "normalized_paths",
        "plan_input",
        "contract_input",
    }
    missing = required - set(payload)
    if missing:
        raise ToolError("plan manifest is missing required fields: " + ", ".join(sorted(missing)))
    if (
        payload.get("manifest_kind") != MANIFEST_KIND
        or payload.get("manifest_version") != MANIFEST_VERSION
        or payload.get("generated_by") != "workflow_check.py"
        or payload.get("command_type") != "plan"
        or payload.get("tool_version") != TOOL_VERSION
        or payload.get("contract_version") != contract["schema_version"]
        or payload.get("external_detector_status") != "not_run"
        or payload.get("result_status") != "executable"
        or payload.get("manifest_generated") is not True
    ):
        raise ToolError("post-round accepts only a compatible executable workflow_check plan manifest")
    if not isinstance(payload["normalized_paths"], dict):
        raise ToolError("plan manifest normalized_paths must be an object")
    if not isinstance(payload["snapshot_dir"], str) or not payload["snapshot_dir"]:
        raise ToolError("plan manifest snapshot_dir must be a non-empty path")
    for key in ("plan", "project_root", "output"):
        if not isinstance(payload["normalized_paths"].get(key), str) or not payload["normalized_paths"][key]:
            raise ToolError(f"plan manifest normalized_paths is missing {key}")
    if Path(payload["normalized_paths"]["output"]).resolve() != path:
        raise ToolError("plan manifest output identity does not match its current path")
    for key in ("plan_input", "contract_input"):
        record = payload[key]
        if not isinstance(record, dict) or not isinstance(record.get("path"), str):
            raise ToolError(f"plan manifest {key} is invalid")
        _validate_hash_record(record, f"plan manifest {key}")
    if not isinstance(payload["targets"], list) or not payload["targets"]:
        raise ToolError("plan manifest has no snapshot targets")
    required_target = {
        "target_path",
        "target_relative_path",
        "language",
        "rounds",
        "fixes",
        "prior_paths",
        "prior_inputs",
        "overlap_settings",
        "snapshot_path",
        "snapshot",
        "preflight_target",
    }
    for index, target in enumerate(payload["targets"], start=1):
        if not isinstance(target, dict):
            raise ToolError(f"plan manifest target {index} is not an object")
        target_missing = required_target - set(target)
        if target_missing:
            raise ToolError(f"plan manifest target {index} is missing: {', '.join(sorted(target_missing))}")
        for key in ("target_path", "target_relative_path", "snapshot_path"):
            if not isinstance(target[key], str) or not target[key]:
                raise ToolError(f"plan manifest target {index} has an invalid {key}")
        if not Path(target["target_path"]).is_absolute() or not Path(target["snapshot_path"]).is_absolute():
            raise ToolError(f"plan manifest target {index} paths must be absolute")
        relative_target = Path(target["target_relative_path"])
        if relative_target.is_absolute() or ".." in relative_target.parts:
            raise ToolError(f"plan manifest target {index} target_relative_path must stay relative")
        if target["language"] not in {"en", "zh"}:
            raise ToolError(f"plan manifest target {index} has an invalid language")
        if not isinstance(target["rounds"], list) or not target["rounds"] or not all(isinstance(value, int) for value in target["rounds"]):
            raise ToolError(f"plan manifest target {index} has invalid rounds")
        if not isinstance(target["fixes"], list) or not target["fixes"]:
            raise ToolError(f"plan manifest target {index} has no fixes")
        for fix in target["fixes"]:
            if (
                not isinstance(fix, dict)
                or not isinstance(fix.get("round"), int)
                or not isinstance(fix.get("fix_id"), str)
                or not isinstance(fix.get("secondary_scan_disposition"), str)
            ):
                raise ToolError(f"plan manifest target {index} has an invalid fix record")
        if not isinstance(target["prior_paths"], list) or not all(isinstance(value, str) for value in target["prior_paths"]):
            raise ToolError(f"plan manifest target {index} has invalid prior paths")
        if not isinstance(target["prior_inputs"], list):
            raise ToolError(f"plan manifest target {index} has invalid prior inputs")
        for prior in target["prior_inputs"]:
            if not isinstance(prior, dict) or not isinstance(prior.get("path"), str):
                raise ToolError(f"plan manifest target {index} has an invalid prior input")
            _validate_hash_record(prior, f"plan manifest target {index} prior input")
        if {str(Path(value).resolve()) for value in target["prior_paths"]} != {
            str(Path(value["path"]).resolve()) for value in target["prior_inputs"]
        }:
            raise ToolError(f"plan manifest target {index} prior paths do not match prior inputs")
        if not isinstance(target["overlap_settings"], dict):
            raise ToolError(f"plan manifest target {index} has invalid overlap settings")
        _validate_hash_record(target["snapshot"], f"plan manifest target {index} snapshot")
        _validate_hash_record(target["preflight_target"], f"plan manifest target {index} preflight target")
    return path, payload


def _manifest_declaration_issues(manifest: dict[str, Any], root: Path) -> list[str]:
    """Compare manifest declarations with the immutable plan without reading target text."""

    plan_path = Path(manifest["plan_input"]["path"]).resolve()
    parsed = preflight_plan.parse_plan(read_text_checked(plan_path))
    selection = manifest["round_selection"]
    if selection == "all":
        selected_rounds = {item["number"] for item in parsed["rounds"]}
    elif isinstance(selection, str) and selection.isdigit():
        selected_rounds = {int(selection)}
    else:
        return ["manifest round_selection is invalid"]

    plan_language = (parsed["metadata"]["plan_language"] or "").lower()
    expected: dict[str, dict[str, Any]] = {}
    issues: list[str] = []
    for fix in parsed["fixes"]:
        if fix["round"] not in selected_rounds:
            continue
        if not all(fix.get(field) for field in ("file", "secondary_scan_disposition")):
            issues.append(f"plan fix {fix['fix_id']} lacks manifest declaration fields")
            continue
        target, target_issue = preflight_plan._resolve_inside_root(fix["file"], root)
        if target_issue or target is None:
            issues.append(target_issue or f"cannot resolve target for {fix['fix_id']}")
            continue
        language = (fix.get("language") or plan_language).lower()
        group = expected.setdefault(
            str(target),
            {
                "target_relative_path": str(target.relative_to(root)),
                "languages": set(),
                "rounds": set(),
                "fixes": [],
                "prior_paths": set(),
            },
        )
        group["languages"].add(language)
        group["rounds"].add(fix["round"])
        group["fixes"].append(
            (
                fix["round"],
                fix["fix_id"],
                fix["secondary_scan_disposition"],
            )
        )
        if fix.get("prior_file"):
            prior, prior_issue = preflight_plan._resolve_inside_root(fix["prior_file"], root)
            if prior_issue or prior is None:
                issues.append(prior_issue or f"cannot resolve prior file for {fix['fix_id']}")
            else:
                group["prior_paths"].add(str(prior))

    actual = {str(Path(item["target_path"]).resolve()): item for item in manifest["targets"]}
    if set(actual) != set(expected):
        issues.append("manifest target set does not match the selected plan fixes")
        return issues
    for target_path, declaration in expected.items():
        target = actual[target_path]
        languages = declaration["languages"]
        if len(languages) != 1 or target["language"] not in languages:
            issues.append(f"{declaration['target_relative_path']}: manifest language does not match the plan")
        if target["target_relative_path"] != declaration["target_relative_path"]:
            issues.append(f"{declaration['target_relative_path']}: manifest relative target path does not match the plan")
        if sorted(target["rounds"]) != sorted(declaration["rounds"]):
            issues.append(f"{declaration['target_relative_path']}: manifest rounds do not match the plan")
        actual_fixes = sorted(
            (
                fix["round"],
                fix["fix_id"],
                fix["secondary_scan_disposition"],
            )
            for fix in target["fixes"]
        )
        if actual_fixes != sorted(declaration["fixes"]):
            issues.append(f"{declaration['target_relative_path']}: manifest fixes do not match the plan")
        if {str(Path(value).resolve()) for value in target["prior_paths"]} != declaration["prior_paths"]:
            issues.append(f"{declaration['target_relative_path']}: manifest prior paths do not match the plan")
    return issues


def run_post_round(manifest_path: str, contract: dict[str, Any], output_path: str | None = None) -> dict[str, Any]:
    manifest_file, manifest = _load_plan_manifest(manifest_path, contract)
    if output_path is not None:
        output = Path(output_path).resolve()
        protected_inputs = {
            manifest_file,
            Path(manifest["plan_input"]["path"]).resolve(),
            Path(manifest["contract_input"]["path"]).resolve(),
        }
        for target in manifest["targets"]:
            protected_inputs.add(Path(target["target_path"]).resolve())
            protected_inputs.add(Path(target["snapshot_path"]).resolve())
            protected_inputs.update(Path(value).resolve() for value in target["prior_paths"])
        if output in protected_inputs:
            raise ToolError(f"post-round output must not overwrite an input file: {output}")
    root = Path(manifest["normalized_paths"]["project_root"]).resolve()
    if not root.is_dir():
        raise ToolError(f"manifest project root is unavailable: {root}")
    result = _base_evidence("post-round", contract)
    target_results: list[dict[str, Any]] = []
    manifest_identity_issues: list[str] = []
    for key, expected_path in (
        ("plan_input", Path(manifest["normalized_paths"]["plan"]).resolve()),
        ("contract_input", repo_path("workflow/contract.json").resolve()),
    ):
        record = manifest[key]
        recorded_path = Path(record["path"]).resolve()
        if recorded_path != expected_path:
            manifest_identity_issues.append(f"{key} path does not match normalized provenance")
            continue
        try:
            if _hash_file(recorded_path) != {"hash_kind": record["hash_kind"], "sha256": record["sha256"]}:
                manifest_identity_issues.append(f"{key} changed after plan preflight")
        except ToolError as exc:
            manifest_identity_issues.append(str(exc))
    try:
        manifest_identity_issues.extend(_manifest_declaration_issues(manifest, root))
    except ToolError as exc:
        manifest_identity_issues.append(str(exc))
    hard_failure = bool(manifest_identity_issues)
    review_required = False
    snapshot_root = Path(manifest["snapshot_dir"]).resolve()
    for target_data in manifest["targets"]:
        target_result: dict[str, Any] = {
            "target_path": target_data.get("target_path"),
            "target_relative_path": target_data.get("target_relative_path"),
            "components": {},
        }
        try:
            target = Path(target_data["target_path"]).resolve()
            expected = (root / target_data["target_relative_path"]).resolve()
            target.relative_to(root)
            if target != expected:
                raise ToolError("target identity does not match the manifest relative path")
            snapshot = Path(target_data["snapshot_path"]).resolve()
            snapshot.relative_to(snapshot_root)
            recorded_snapshot = target_data["snapshot"]
            if _hash_file(snapshot) != recorded_snapshot:
                raise ToolError("snapshot identity hash does not match the plan manifest")
            if target_data["preflight_target"] != recorded_snapshot:
                raise ToolError("snapshot hash does not match the target hash recorded at plan preflight")
            expected_overlap_settings = {
                "window_tokens": contract["anti_regression"]["window_tokens"],
                "overlap_threshold": contract["anti_regression"]["overlap_threshold"],
            }
            if target_data["overlap_settings"] != expected_overlap_settings:
                raise ToolError("overlap settings do not match the active workflow contract")
            source = read_text_checked(snapshot)
            current = read_text_checked(target)
            target_result["components"]["identity"] = {"status": "pass", "snapshot": recorded_snapshot, "current": _hash_file(target)}
        except (KeyError, OSError, ToolError, ValueError) as exc:
            target_result["components"]["identity"] = {"status": "hard_fail", "error": str(exc)}
            target_results.append(target_result)
            hard_failure = True
            continue

        language = target_data["language"]
        guardrails = _guardrail_component(source, current, language)
        target_result["components"]["guardrails"] = guardrails
        if guardrails["status"] == "hard_fail":
            hard_failure = True
        if guardrails["status"] == "review_warning":
            review_required = True

        rules = load_rules_yaml(repo_path(Path("rules") / language / "rules.yaml"))
        before_scan = scan_rules.scan_text(source, rules, language)
        after_scan = scan_rules.scan_text(current, rules, language)
        rule_regression = after_scan["aggregate"]["actionable_unique_spans"] > before_scan["aggregate"]["actionable_unique_spans"]
        context_warning = bool(after_scan["aggregate"]["review_unique_spans"])
        rule_status = "review_required" if rule_regression or context_warning else "pass"
        target_result["components"]["rule_scan"] = {
            "status": rule_status,
            "before": before_scan["aggregate"],
            "after": after_scan["aggregate"],
            "rule_regression": rule_regression,
            "context_warning": context_warning,
        }
        review_required = review_required or rule_status == "review_required"

        before_structure = structure_metrics.compute(str(snapshot), language)
        after_structure = structure_metrics.compute(str(target), language)
        changed_metrics = [key for key in structure_metrics.METRIC_KEYS if before_structure.get(key) != after_structure.get(key)]
        structure_status = "review_required" if changed_metrics else "pass"
        target_result["components"]["structure_metrics"] = {
            "status": structure_status,
            "changed_metrics": changed_metrics,
            "before": before_structure,
            "after": after_structure,
        }
        review_required = review_required or structure_status == "review_required"

        prior_components = []
        settings = target_data["overlap_settings"]
        prior_records = {str(Path(item["path"]).resolve()): item for item in target_data["prior_inputs"]}
        for prior_value in target_data.get("prior_paths", []):
            prior = Path(prior_value).resolve()
            try:
                prior.relative_to(root)
                prior_record = prior_records.get(str(prior))
                if prior_record is None or _hash_file(prior) != {
                    "hash_kind": prior_record["hash_kind"],
                    "sha256": prior_record["sha256"],
                }:
                    raise ToolError("prior-version identity hash does not match the plan manifest")
                prior_text = read_text_checked(prior)
            except (ValueError, ToolError) as exc:
                prior_components.append({"prior_path": str(prior), "status": "hard_fail", "error": str(exc)})
                hard_failure = True
                continue
            component = _overlap_component(
                current,
                prior_text,
                language,
                settings["window_tokens"],
                settings["overlap_threshold"],
            )
            component["prior_path"] = str(prior)
            prior_components.append(component)
            review_required = review_required or component["status"] == "review_required"
        target_result["components"]["prior_overlap"] = prior_components or [{"status": "not_configured"}]
        target_results.append(target_result)

    status = "whole_round_rollback_required" if hard_failure else "review_required" if review_required else "complete"
    result.update(
        {
            "normalized_paths": {"manifest": str(manifest_file), "project_root": str(root)},
            "manifest_hash": _hash_file(manifest_file),
            "component_results": {
                "manifest_identity": {
                    "status": "hard_fail" if manifest_identity_issues else "pass",
                    "issues": manifest_identity_issues,
                }
            },
            "targets": target_results,
            "result_status": status,
            "rollback_unit": contract["rollback"]["unit"],
            "next_round_allowed": status == "complete",
        }
    )
    return result


def main() -> int:
    args = parse_args()
    try:
        contract = _load_contract()
        if args.command == "discovery":
            if Path(args.output).resolve() == repo_path(args.text).resolve():
                raise ToolError("discovery output must not overwrite the input document")
            result = run_discovery(args.text, args.lang, contract)
        elif args.command == "plan":
            result = run_plan(args.plan, args.round, args.project_root, args.snapshot_dir, args.output, contract)
        else:
            result = run_post_round(args.manifest, contract, args.output)
        _write_json(args.output, result)
        return 0 if result["result_status"] in {"complete", "executable"} else 1
    except ToolError as exc:
        print_error(exc)
        return 2


if __name__ == "__main__":
    sys.exit(main())
