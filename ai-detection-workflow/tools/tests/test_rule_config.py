from __future__ import annotations

import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path


TOOLS_DIR = Path(__file__).resolve().parents[1]
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

import scan_rules
from tool_common import ToolError, auto_literal_issues, load_context_whitelist, load_rules_yaml


WORKFLOW_ROOT = TOOLS_DIR.parent


class RuleConfigTests(unittest.TestCase):
    def test_auto_rules_have_no_placeholder_or_delimiter_literals(self) -> None:
        rules = load_rules_yaml(WORKFLOW_ROOT / "rules" / "zh" / "rules.yaml")
        self.assertEqual(auto_literal_issues(rules), [])

    def test_auto_rule_requires_executable_matcher(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            rules_path = Path(temporary) / "rules" / "zh" / "rules.yaml"
            rules_path.parent.mkdir(parents=True)
            rules_path.write_text(
                """- id: T-01\n  name: \"test\"\n  family: T\n  match_type: literal\n  literals: []\n  pattern: null\n  patterns: []\n  scan: auto\n  frequency: low\n  whitelist_ref: null\n  source: test\n""",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ToolError, "no executable matcher"):
                load_rules_yaml(rules_path)

    def test_invalid_whitelist_reference_is_configuration_error(self) -> None:
        rules = load_rules_yaml(WORKFLOW_ROOT / "rules" / "zh" / "rules.yaml")
        target = next(rule for rule in rules if rule["id"] == "C-04")
        target["whitelist_ref"] = "rules/zh/not-present.json"
        with self.assertRaisesRegex(ToolError, "cannot read context whitelist"):
            scan_rules.scan_text("生态环境", rules, "zh")

    def test_equal_length_conflicting_contexts_are_configuration_error(self) -> None:
        rules = load_rules_yaml(WORKFLOW_ROOT / "rules" / "zh" / "rules.yaml")
        with tempfile.TemporaryDirectory() as temporary:
            conflict = Path(temporary) / "conflict.json"
            conflict.write_text(
                json.dumps(
                    {
                        "entries": [
                            {"id": "one", "rule_ids": ["C-04"], "trigger": "生态", "context_matcher": "生态环境", "disposition": "whitelisted"},
                            {"id": "two", "rule_ids": ["C-04"], "trigger": "生态", "context_matcher": "生态环境", "disposition": "review"},
                        ]
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
            target = next(rule for rule in rules if rule["id"] == "C-04")
            target["whitelist_ref"] = str(conflict)
            with self.assertRaisesRegex(ToolError, "conflicting equal-length"):
                scan_rules.scan_text("生态环境", rules, "zh")

    def test_context_source_has_required_entries(self) -> None:
        entries = load_context_whitelist("rules/zh/context_whitelist.json", WORKFLOW_ROOT)
        self.assertGreaterEqual(len(entries), 4)
        self.assertTrue(all(entry["id"] and entry["rule_ids"] for entry in entries))

    def test_linter_flags_bad_literal_forms(self) -> None:
        rules = load_rules_yaml(WORKFLOW_ROOT / "rules" / "zh" / "rules.yaml")
        malformed = copy.deepcopy(next(rule for rule in rules if rule["id"] == "C-08"))
        malformed["literals"] = ["最后；第一", "随着...的发展"]
        issues = auto_literal_issues([malformed])
        self.assertEqual(len(issues), 2)


if __name__ == "__main__":
    unittest.main()
