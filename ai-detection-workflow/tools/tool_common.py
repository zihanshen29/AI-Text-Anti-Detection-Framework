#!/usr/bin/env python3
"""Shared helpers for deterministic offline workflow tools."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable


REPO_ROOT = Path(__file__).resolve().parents[1]

MOJIBAKE_MARKERS = (
    "\ufffd",
    "锟斤拷",
    "鍘",
    "鐗",
    "涓",
)


class ToolError(Exception):
    """Error that should be reported with exit code 2."""


def repo_path(value: str | Path) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return REPO_ROOT / path


def read_text_checked(path: str | Path) -> str:
    """Read UTF-8 text and fail on common mojibake markers."""

    full_path = repo_path(path)
    try:
        data = full_path.read_bytes()
    except OSError as exc:
        raise ToolError(f"cannot read {full_path}: {exc}") from exc

    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ToolError(f"encoding preflight failed for {full_path}: not valid UTF-8 ({exc})") from exc

    sample = text[:2000]
    for marker in MOJIBAKE_MARKERS:
        if marker in sample:
            raise ToolError(f"encoding preflight failed for {full_path}: mojibake marker {marker!r} found")
    return text


def load_rules_yaml(path: str | Path) -> list[dict[str, Any]]:
    """Load the repository's constrained rules.yaml format using stdlib only."""

    full_path = repo_path(path)
    try:
        lines = full_path.read_text(encoding="utf-8-sig").splitlines()
    except OSError as exc:
        raise ToolError(f"cannot read rules file {full_path}: {exc}") from exc
    except UnicodeDecodeError as exc:
        raise ToolError(f"rules file is not valid UTF-8: {full_path}: {exc}") from exc

    records: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    for raw in lines:
        line = raw.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue
        if line.startswith("- id:"):
            if current:
                records.append(current)
            current = {"id": line.split(":", 1)[1].strip()}
            continue
        if current is None:
            continue
        if not line.startswith("  ") or ":" not in line:
            raise ToolError(f"unsupported rules.yaml line in {full_path}: {line}")
        key, value = line.strip().split(":", 1)
        current[key] = parse_yaml_scalar(value.strip())
    if current:
        records.append(current)

    required = {"id", "name", "family", "match_type", "literals", "pattern", "scan", "frequency", "source"}
    for record in records:
        missing = required - set(record)
        if missing:
            raise ToolError(f"rule {record.get('id', '<unknown>')} missing keys: {', '.join(sorted(missing))}")
    return records


def parse_yaml_scalar(value: str) -> Any:
    if value == "null":
        return None
    if value.startswith("[") or value.startswith('"'):
        return json.loads(value)
    return value


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

