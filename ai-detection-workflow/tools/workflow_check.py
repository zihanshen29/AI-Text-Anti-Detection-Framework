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
    return {"hash_kind": "worktree_raw_sha256", "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


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
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
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


def _snapshot_targets(preflight: dict[str, Any], snapshot_dir: Path, contract: dict[str, Any], output_path: Path) -> list[dict[str, Any]]:
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    grouped: dict[str, list[dict[str, Any]]] = {}
    for fix in preflight["fixes"]:
        grouped.setdefault(fix["target"], []).append(fix)
    targets: list[dict[str, Any]] = []
    root = Path(preflight["project_root"]).resolve()
    for index, (target_value, fixes) in enumerate(grouped.items(), start=1):
        target = Path(target_value).resolve()
        snapshot = snapshot_dir / f"{index:02d}_{target.name}"
        shutil.copyfile(target, snapshot)
        prior_paths = sorted({fix["prior_path"] for fix in fixes if fix.get("prior_path")})
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
                "snapshot": _hash_file(snapshot),
                "preflight_target": _hash_file(target),
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
    result = _base_evidence("plan", contract)
    result.update(
        {
            "normalized_paths": {
                "plan": preflight["plan_path"],
                "project_root": preflight["project_root"],
                "output": str(Path(output_path).resolve()),
            },
            "round_selection": round_selection,
            "preflight": preflight,
            "result_status": preflight["result_status"],
            "manifest_generated": False,
        }
    )
    if snapshot_dir and preflight["result_status"] == "executable":
        output = Path(output_path).resolve()
        snapshots = Path(snapshot_dir).resolve()
        result.update(
            {
                "manifest_kind": MANIFEST_KIND,
                "manifest_version": 1,
                "generated_by": "workflow_check.py",
                "manifest_generated": True,
                "snapshot_dir": str(snapshots),
                "targets": _snapshot_targets(preflight, snapshots, contract, output),
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


def _load_plan_manifest(path_value: str) -> tuple[Path, dict[str, Any]]:
    path = repo_path(path_value).resolve()
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ToolError(f"cannot read plan manifest {path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ToolError(f"invalid plan manifest JSON {path}: {exc}") from exc
    required = {"manifest_kind", "manifest_version", "generated_by", "command_type", "targets", "normalized_paths"}
    missing = required - set(payload)
    if missing or payload.get("manifest_kind") != MANIFEST_KIND or payload.get("generated_by") != "workflow_check.py" or payload.get("command_type") != "plan":
        raise ToolError("post-round accepts only a plan-generated workflow_check manifest")
    if not isinstance(payload["targets"], list) or not payload["targets"]:
        raise ToolError("plan manifest has no snapshot targets")
    return path, payload


def run_post_round(manifest_path: str, contract: dict[str, Any]) -> dict[str, Any]:
    manifest_file, manifest = _load_plan_manifest(manifest_path)
    root = Path(manifest["normalized_paths"]["project_root"]).resolve()
    if not root.is_dir():
        raise ToolError(f"manifest project root is unavailable: {root}")
    result = _base_evidence("post-round", contract)
    target_results: list[dict[str, Any]] = []
    hard_failure = False
    review_required = False
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
            recorded_snapshot = target_data["snapshot"]
            if recorded_snapshot.get("hash_kind") != "worktree_raw_sha256" or _hash_file(snapshot) != recorded_snapshot:
                raise ToolError("snapshot identity hash does not match the plan manifest")
            source = read_text_checked(snapshot)
            current = read_text_checked(target)
            target_result["components"]["identity"] = {"status": "pass", "snapshot": recorded_snapshot, "current": _hash_file(target)}
        except (KeyError, OSError, ToolError) as exc:
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
        for prior_value in target_data.get("prior_paths", []):
            prior = Path(prior_value).resolve()
            try:
                prior.relative_to(root)
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
            result = run_discovery(args.text, args.lang, contract)
        elif args.command == "plan":
            result = run_plan(args.plan, args.round, args.project_root, args.snapshot_dir, args.output, contract)
        else:
            result = run_post_round(args.manifest, contract)
        _write_json(args.output, result)
        return 0 if result["result_status"] in {"complete", "executable"} else 1
    except ToolError as exc:
        print_error(exc)
        return 2


if __name__ == "__main__":
    sys.exit(main())
