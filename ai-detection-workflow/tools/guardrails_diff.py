#!/usr/bin/env python3
"""Check deterministic fidelity guardrails between source and rewrite."""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import re
import sys
from typing import Any

from tool_common import ToolError, infer_lang, markdown_table, print_error, read_text_checked


CONTEXT_RADIUS = 48
NUMBER_RE = re.compile(
    r"(?<![\w.])(?:[+\-−])?(?:(?:\d{1,3}(?:,\d{3})+)|\d+)(?:\.\d+)?(?:[eE][+\-]?\d+)?%?(?!\w)"
)
VERSION_RE = re.compile(
    r"(?<![\w.])(?:v\d+(?:\.\d+)+|\d+(?:\.\d+){2,})(?![\w.])",
    re.IGNORECASE,
)
NUMERIC_CITATION_RE = re.compile(r"\[(\s*\d+(?:\s*(?:,|;|[-–])\s*\d+)*\s*)\]")
LATEX_CITE_RE = re.compile(r"\\(cite|citep|citet)(?:\[[^\]]*\]){0,2}\{([^}]+)\}")
PANDOC_CITE_RE = re.compile(r"(?<![\w@])@([A-Za-z0-9_:.\-]*[A-Za-z0-9_])")
MARKDOWN_HEADING_RE = re.compile(r"^\s*(#{1,6})\s+(.+?)\s*$", re.MULTILINE)
LATEX_HEADING_RE = re.compile(r"\\(part|chapter|section|subsection|subsubsection)\*?\{([^}]+)\}")
LATEX_LABEL_RE = re.compile(r"\\label\{([^}]+)\}")
TEXT_LABEL_RE = re.compile(
    r"\b(Figure|Fig\.?|Table|Equation|Eq\.?)\s*((?:[A-Za-z]-?)?\d+(?:[.\-]\d+)*)",
    re.IGNORECASE,
)
ZH_LABEL_RE = re.compile(r"(图|表|式)\s*([0-9一二三四五六七八九十]+(?:[.\-][0-9一二三四五六七八九十]+)*)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare source/rewrite fidelity guardrails without semantic scoring.")
    parser.add_argument("--source", required=True, help="Original/source document.")
    parser.add_argument("--rewrite", required=True, help="Rewritten document.")
    parser.add_argument("--lang", choices=["en", "zh", "auto"], default="auto", help="Document language. Defaults to auto.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown.")
    return parser.parse_args()


def _normalise(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("−", "-")).strip().lower()


def _excerpt_and_fingerprint(text: str, start: int, end: int) -> tuple[str, str]:
    excerpt = text[max(0, start - CONTEXT_RADIUS) : min(len(text), end + CONTEXT_RADIUS)].replace("\n", " ").strip()
    normalized = _normalise(excerpt)
    return excerpt[:160], hashlib.sha256(normalized.encode("utf-8")).hexdigest()


def _make_entity(kind: str, value: str, start: int, end: int, text: str) -> dict[str, Any]:
    excerpt, fingerprint = _excerpt_and_fingerprint(text, start, end)
    return {
        "kind": kind,
        "value": _normalise(value),
        "start": start,
        "end": end,
        "heading_scope": None,
        "context_fingerprint": fingerprint,
        "context_excerpt": excerpt,
    }


def extract_entities(text: str) -> list[dict[str, Any]]:
    """Extract fidelity entities with a nearest-heading scope for each occurrence."""

    entities: list[dict[str, Any]] = []
    headings: list[dict[str, Any]] = []
    for match in MARKDOWN_HEADING_RE.finditer(text):
        entity = _make_entity("markdown_heading", match.group(2), match.start(), match.end(), text)
        entities.append(entity)
        headings.append(entity)
    for match in LATEX_HEADING_RE.finditer(text):
        entity = _make_entity("latex_heading", match.group(2), match.start(), match.end(), text)
        entities.append(entity)
        headings.append(entity)
    for match in NUMBER_RE.finditer(text):
        entities.append(_make_entity("number", match.group(0), match.start(), match.end(), text))
    for match in VERSION_RE.finditer(text):
        entities.append(_make_entity("version", match.group(0), match.start(), match.end(), text))
    for match in NUMERIC_CITATION_RE.finditer(text):
        entities.append(_make_entity("numeric_citation", match.group(1), match.start(), match.end(), text))
    for match in LATEX_CITE_RE.finditer(text):
        command = match.group(1).lower()
        for key in match.group(2).split(","):
            key = key.strip()
            if key:
                entities.append(_make_entity(f"latex_{command}", key, match.start(), match.end(), text))
    for match in PANDOC_CITE_RE.finditer(text):
        entities.append(_make_entity("pandoc_citation", match.group(1), match.start(), match.end(), text))
    for match in LATEX_LABEL_RE.finditer(text):
        entities.append(_make_entity("latex_label", match.group(1), match.start(), match.end(), text))
    for match in TEXT_LABEL_RE.finditer(text):
        kind = re.sub(r"\.$", "", match.group(1).lower())
        entities.append(_make_entity(kind, match.group(2), match.start(), match.end(), text))
    for match in ZH_LABEL_RE.finditer(text):
        entities.append(_make_entity({"图": "figure", "表": "table", "式": "equation"}[match.group(1)], match.group(2), match.start(), match.end(), text))

    entities.sort(key=lambda entity: (entity["start"], entity["end"], entity["kind"], entity["value"]))
    headings.sort(key=lambda entity: entity["start"])
    for entity in entities:
        if entity["kind"] in {"markdown_heading", "latex_heading"}:
            continue
        prior_headings = [heading for heading in headings if heading["start"] <= entity["start"]]
        if prior_headings:
            entity["heading_scope"] = prior_headings[-1]["value"]
    return entities


def multiset(values: list[str]) -> dict[str, int]:
    return dict(collections.Counter(values))


def numbers(text: str) -> dict[str, int]:
    return multiset([entity["value"] for entity in extract_entities(text) if entity["kind"] in {"number", "version"}])


def citation_keys(text: str) -> dict[str, int]:
    return multiset(
        [
            entity["value"]
            for entity in extract_entities(text)
            if entity["kind"] in {"numeric_citation", "latex_cite", "latex_citep", "latex_citet", "pandoc_citation"}
        ]
    )


def headings(text: str) -> list[str]:
    return [entity["value"] for entity in extract_entities(text) if entity["kind"] in {"markdown_heading", "latex_heading"}]


def labels(text: str) -> dict[str, int]:
    return multiset(
        [
            f"{entity['kind']}:{entity['value']}"
            for entity in extract_entities(text)
            if entity["kind"] in {"latex_label", "figure", "fig", "table", "equation", "eq"}
        ]
    )


def cjk_count(text: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", text))


def _entity_key(entity: dict[str, Any]) -> str:
    return f"{entity['kind']}:{entity['value']}"


def _compact_entities(entities: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "kind": entity["kind"],
            "value": entity["value"],
            "heading_scope": entity["heading_scope"],
            "context_fingerprint": entity["context_fingerprint"],
            "context_excerpt": entity["context_excerpt"],
        }
        for entity in entities
    ]


def compare_texts(source: str, rewrite: str, lang: str) -> dict[str, Any]:
    """Compare structural entity preservation and local-context review evidence."""

    source_entities = extract_entities(source)
    rewrite_entities = extract_entities(rewrite)
    source_keys = [_entity_key(entity) for entity in source_entities]
    rewrite_keys = [_entity_key(entity) for entity in rewrite_entities]
    source_scopes = [(key, entity["heading_scope"]) for key, entity in zip(source_keys, source_entities)]
    rewrite_scopes = [(key, entity["heading_scope"]) for key, entity in zip(rewrite_keys, rewrite_entities)]

    checks = [
        {
            "check": "entity multiset",
            "severity": "hard_failure",
            "status": "pass" if collections.Counter(source_keys) == collections.Counter(rewrite_keys) else "hard_fail",
            "source": dict(collections.Counter(source_keys)),
            "rewrite": dict(collections.Counter(rewrite_keys)),
        },
        {
            "check": "entity occurrence order",
            "severity": "hard_failure",
            "status": "pass" if source_keys == rewrite_keys else "hard_fail",
            "source": source_keys,
            "rewrite": rewrite_keys,
        },
        {
            "check": "nearest heading scope",
            "severity": "hard_failure",
            "status": "pass" if source_scopes == rewrite_scopes else "hard_fail",
            "source": source_scopes,
            "rewrite": rewrite_scopes,
        },
    ]
    if lang == "en":
        checks.append(
            {
                "check": "EN rewrite CJK residual",
                "severity": "hard_failure",
                "status": "pass" if cjk_count(rewrite) == 0 else "hard_fail",
                "source": cjk_count(source),
                "rewrite": cjk_count(rewrite),
            }
        )

    context_changes: list[dict[str, Any]] = []
    if source_keys == rewrite_keys and source_scopes == rewrite_scopes:
        for index, (before, after) in enumerate(zip(source_entities, rewrite_entities), start=1):
            if before["context_fingerprint"] != after["context_fingerprint"]:
                context_changes.append(
                    {
                        "occurrence": index,
                        "entity": _entity_key(before),
                        "heading_scope": before["heading_scope"],
                        "source": {"fingerprint": before["context_fingerprint"], "excerpt": before["context_excerpt"]},
                        "rewrite": {"fingerprint": after["context_fingerprint"], "excerpt": after["context_excerpt"]},
                    }
                )
    checks.append(
        {
            "check": "local context fingerprints",
            "severity": "review_warning",
            "status": "review_warning" if context_changes else "pass",
            "changes": context_changes,
        }
    )
    hard_failure = any(check["severity"] == "hard_failure" and check["status"] == "hard_fail" for check in checks)
    return {
        "lang": lang,
        "checks": checks,
        "hard_failure": hard_failure,
        "review_warning": bool(context_changes),
        "context_changes": context_changes,
        "source_entities": _compact_entities(source_entities),
        "rewrite_entities": _compact_entities(rewrite_entities),
    }


def _summary(value: Any) -> str:
    text = json.dumps(value, ensure_ascii=False, sort_keys=True)
    return text if len(text) <= 130 else text[:127] + "..."


def render_markdown(result: dict[str, Any]) -> str:
    rows = []
    for check in result["checks"]:
        rows.append([check["check"], check["severity"], check["status"], _summary(check.get("source", "")), _summary(check.get("rewrite", ""))])
    lines = [markdown_table(["Check", "Severity", "Status", "Source", "Rewrite"], rows)]
    if result["context_changes"]:
        lines.extend(["", "## Review Warnings", ""])
        context_rows = [
            [item["occurrence"], item["entity"], item["heading_scope"] or "<root>", item["source"]["fingerprint"][:12], item["rewrite"]["fingerprint"][:12]]
            for item in result["context_changes"]
        ]
        lines.append(markdown_table(["Occurrence", "Entity", "Scope", "Source context", "Rewrite context"], context_rows))
        lines.append("Changed local context is a review warning, not an automatic semantic claim.")
    lines.extend(["", f"Hard failure: {'yes' if result['hard_failure'] else 'no'}", f"Review warning: {'yes' if result['review_warning'] else 'no'}"])
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    try:
        source = read_text_checked(args.source)
        rewrite = read_text_checked(args.rewrite)
        lang = infer_lang([source, rewrite]) if args.lang == "auto" else args.lang
        result = compare_texts(source, rewrite, lang)
        payload = {"source": args.source, "rewrite": args.rewrite, **result}
        if args.json:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            print(render_markdown(result))
        return 1 if result["hard_failure"] or result["review_warning"] else 0
    except ToolError as exc:
        print_error(exc)
        return 2


if __name__ == "__main__":
    sys.exit(main())
