#!/usr/bin/env python3
"""Shared helpers for deterministic offline workflow tools."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable


WORKFLOW_ROOT = Path(__file__).resolve().parents[1]
# Retained for callers of the original helper API.
REPO_ROOT = WORKFLOW_ROOT

MOJIBAKE_MARKERS = (
    "\ufffd",
    "锟斤拷",
)


class ToolError(Exception):
    """Error that should be reported with exit code 2."""


def force_utf8_stdio() -> None:
    """Force UTF-8 output independently of the Windows console code page."""

    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8")
            except (ValueError, OSError):
                pass


force_utf8_stdio()


def repo_path(value: str | Path) -> Path:
    """Resolve relative tool inputs from the workflow root."""

    path = Path(value)
    return path if path.is_absolute() else WORKFLOW_ROOT / path


def read_text_checked(path: str | Path) -> str:
    """Read strict UTF-8 text and reject common mojibake markers."""

    full_path = repo_path(path)
    try:
        data = full_path.read_bytes()
    except OSError as exc:
        raise ToolError(f"cannot read {full_path}: {exc}") from exc

    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ToolError(f"encoding preflight failed for {full_path}: not valid UTF-8 ({exc})") from exc

    for marker in MOJIBAKE_MARKERS:
        if marker in text[:2000]:
            raise ToolError(f"encoding preflight failed for {full_path}: mojibake marker {marker!r} found")
    return text


def _read_utf8(path: Path, description: str) -> str:
    try:
        return path.read_text(encoding="utf-8-sig")
    except OSError as exc:
        raise ToolError(f"cannot read {description} {path}: {exc}") from exc
    except UnicodeDecodeError as exc:
        raise ToolError(f"{description} is not valid UTF-8: {path}: {exc}") from exc


def parse_yaml_scalar(value: str) -> Any:
    """Parse the intentionally constrained scalar subset used by rules.yaml."""

    if value == "null":
        return None
    if value in {"true", "false"}:
        return value == "true"
    if value.startswith("[") or value.startswith('"'):
        try:
            return json.loads(value)
        except json.JSONDecodeError as exc:
            raise ToolError(f"invalid JSON-style YAML scalar {value!r}: {exc}") from exc
    return value


def load_rules_yaml(path: str | Path) -> list[dict[str, Any]]:
    """Load the repository's constrained rules.yaml format with stdlib only.

    Auto rules may combine direct ``literals``, the legacy ``pattern`` field,
    and an optional JSON-style ``patterns`` list. This keeps rule matching
    explicit while avoiding a runtime YAML dependency.
    """

    full_path = repo_path(path)
    lines = _read_utf8(full_path, "rules file").splitlines()
    records: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    for raw in lines:
        line = raw.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if line.startswith("- id:"):
            if current is not None:
                records.append(current)
            current = {"id": line.split(":", 1)[1].strip()}
            continue
        if current is None:
            continue
        if not line.startswith("  ") or ":" not in line:
            raise ToolError(f"unsupported rules.yaml line in {full_path}: {line}")
        key, value = line.strip().split(":", 1)
        current[key] = parse_yaml_scalar(value.strip())
    if current is not None:
        records.append(current)

    required = {"id", "name", "family", "match_type", "literals", "scan", "frequency", "whitelist_ref", "source"}
    workflow_root = full_path.parents[2] if len(full_path.parents) >= 3 else WORKFLOW_ROOT
    for record in records:
        missing = required - set(record)
        if missing:
            raise ToolError(f"rule {record.get('id', '<unknown>')} missing keys: {', '.join(sorted(missing))}")
        record.setdefault("pattern", None)
        record.setdefault("patterns", [])
        if record["match_type"] not in {"literal", "regex", "structural"}:
            raise ToolError(f"rule {record['id']} has unsupported match_type {record['match_type']!r}")
        if record["scan"] not in {"auto", "manual"}:
            raise ToolError(f"rule {record['id']} has unsupported scan {record['scan']!r}")
        if not isinstance(record["literals"], list) or not all(isinstance(item, str) for item in record["literals"]):
            raise ToolError(f"rule {record['id']} literals must be a JSON-style string list")
        if record["pattern"] is not None and not isinstance(record["pattern"], str):
            raise ToolError(f"rule {record['id']} pattern must be a string or null")
        if not isinstance(record["patterns"], list) or not all(isinstance(item, str) for item in record["patterns"]):
            raise ToolError(f"rule {record['id']} patterns must be a JSON-style string list")
        if record["scan"] == "auto" and not (record["literals"] or record["pattern"] or record["patterns"]):
            raise ToolError(f"auto rule {record['id']} has no executable matcher")
        record["_workflow_root"] = workflow_root
    return records


def resolve_workflow_path(reference: str | Path, workflow_root: str | Path) -> Path:
    """Resolve a rules reference relative to the workflow root, never cwd."""

    path = Path(reference)
    return path if path.is_absolute() else Path(workflow_root) / path


def load_context_whitelist(reference: str | Path, workflow_root: str | Path) -> list[dict[str, Any]]:
    """Load and validate the JSON context source used by Chinese rules."""

    path = resolve_workflow_path(reference, workflow_root)
    try:
        payload = json.loads(_read_utf8(path, "context whitelist"))
    except json.JSONDecodeError as exc:
        raise ToolError(f"invalid context whitelist JSON {path}: {exc}") from exc
    entries = payload.get("entries") if isinstance(payload, dict) else payload
    if not isinstance(entries, list):
        raise ToolError(f"context whitelist {path} must contain an entries list")

    seen_ids: set[str] = set()
    validated: list[dict[str, Any]] = []
    required = {"id", "rule_ids", "trigger", "context_matcher", "disposition"}
    for entry in entries:
        if not isinstance(entry, dict):
            raise ToolError(f"context whitelist {path} has a non-object entry")
        missing = required - set(entry)
        if missing:
            raise ToolError(f"context whitelist {path} entry missing keys: {', '.join(sorted(missing))}")
        entry_id = entry["id"]
        if not isinstance(entry_id, str) or not entry_id or entry_id in seen_ids:
            raise ToolError(f"context whitelist {path} has invalid or duplicate entry id {entry_id!r}")
        if not isinstance(entry["rule_ids"], list) or not entry["rule_ids"] or not all(isinstance(item, str) for item in entry["rule_ids"]):
            raise ToolError(f"context whitelist {path} entry {entry_id} has invalid rule_ids")
        if not isinstance(entry["trigger"], str) or not entry["trigger"]:
            raise ToolError(f"context whitelist {path} entry {entry_id} has an invalid trigger")
        if entry["disposition"] not in {"whitelisted", "review"}:
            raise ToolError(f"context whitelist {path} entry {entry_id} has invalid disposition")
        if not isinstance(entry["context_matcher"], str) or not entry["context_matcher"]:
            raise ToolError(f"context whitelist {path} entry {entry_id} has an invalid context_matcher")
        try:
            re.compile(entry["context_matcher"])
        except re.error as exc:
            raise ToolError(f"context whitelist {path} entry {entry_id} has invalid matcher: {exc}") from exc
        seen_ids.add(entry_id)
        validated.append(entry)
    return validated


def auto_literal_issues(rules: Iterable[dict[str, Any]]) -> list[str]:
    """Return configuration errors that make an auto literal ambiguous."""

    issues: list[str] = []
    for rule in rules:
        if rule.get("scan") != "auto":
            continue
        for literal in rule.get("literals", []):
            if "..." in literal or "…" in literal:
                issues.append(f"{rule['id']}: placeholder ellipsis in auto literal {literal!r}")
            if "；" in literal or ";" in literal:
                issues.append(f"{rule['id']}: suspicious delimiter-concatenated auto literal {literal!r}")
    return issues


def infer_lang(texts: Iterable[str]) -> str:
    sample = "\n".join(texts)[:5000]
    cjk = len(re.findall(r"[\u4e00-\u9fff]", sample))
    letters = len(re.findall(r"[A-Za-z]", sample))
    return "zh" if cjk > max(20, letters // 4) else "en"


def unit_count(text: str, lang: str) -> int:
    if lang == "zh":
        return max(1, len(re.findall(r"[\u4e00-\u9fffA-Za-z0-9]", text)))
    return max(1, len(re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)?", text)))


def markdown_table(headers: list[str], rows: list[list[Any]]) -> str:
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        out.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(out)


def print_error(exc: Exception) -> None:
    print(f"ERROR: {exc}", file=sys.stderr)
