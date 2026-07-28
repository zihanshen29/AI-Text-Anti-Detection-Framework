from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


TOOLS_DIR = Path(__file__).resolve().parents[1]
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

import scan_rules
from tool_common import load_rules_yaml


WORKFLOW_ROOT = TOOLS_DIR.parent


class ScanRulesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.zh_rules = load_rules_yaml(WORKFLOW_ROOT / "rules" / "zh" / "rules.yaml")
        cls.en_rules = load_rules_yaml(WORKFLOW_ROOT / "rules" / "en" / "rules.yaml")

    def scan_zh(self, text: str) -> dict:
        return scan_rules.scan_text(text, self.zh_rules, "zh")

    def rule(self, result: dict, rule_id: str) -> dict:
        return next(row for row in result["rules"] if row["id"] == rule_id)

    def test_c02_placeholder_patterns_are_bounded(self) -> None:
        positive = self.scan_zh("随着人工智能的发展，研究继续推进。随着政策的不断深入，应用扩大。")
        self.assertEqual(self.rule(positive, "C-02")["raw_rule_hits"], 2)
        cross_sentence = self.scan_zh("随着人工智能。的发展")
        self.assertEqual(self.rule(cross_sentence, "C-02")["raw_rule_hits"], 0)
        overlong = self.scan_zh("随着" + "甲" * 21 + "的发展")
        self.assertEqual(self.rule(overlong, "C-02")["raw_rule_hits"], 0)

    def test_c08_splits_all_malformed_terms(self) -> None:
        result = self.scan_zh("最后，第一，第四，一是。")
        self.assertEqual(self.rule(result, "C-08")["raw_rule_hits"], 4)
        self.assertEqual(result["aggregate"]["actionable_unique_spans"], 4)

    def test_fixed_contexts_are_whitelisted(self) -> None:
        result = self.scan_zh("生态环境、数字化转型和控制闭环均为术语。")
        self.assertEqual(result["aggregate"]["whitelisted_unique_spans"], 3)
        self.assertEqual(result["aggregate"]["actionable_unique_spans"], 0)
        self.assertFalse(scan_rules.has_review_or_actionable(result))
        self.assertTrue(all(hit["whitelist_entry_ids"] for hit in result["hits"]))

    def test_review_and_actionable_contexts_are_distinct(self) -> None:
        review = self.scan_zh("该项目强调业务闭环。")
        self.assertEqual(review["aggregate"]["review_unique_spans"], 1)
        self.assertTrue(scan_rules.has_review_or_actionable(review))
        actionable = self.scan_zh("该项目强调业务生态。")
        self.assertEqual(actionable["aggregate"]["actionable_unique_spans"], 1)

    def test_exact_duplicate_spans_merge_rule_ids(self) -> None:
        result = self.scan_zh("但是，此外，然而。")
        self.assertEqual(result["aggregate"]["raw_rule_hits"], 6)
        self.assertEqual(result["aggregate"]["raw_unique_spans"], 3)
        self.assertEqual(result["aggregate"]["actionable_unique_spans"], 3)
        self.assertEqual({tuple(hit["rule_ids"]) for hit in result["hits"]}, {("C-12", "S-13")})

    def test_baseline_uses_actionable_unique_spans(self) -> None:
        baseline = self.scan_zh("业务生态。")
        current = self.scan_zh("生态环境。")
        baseline["file"] = "before.md"
        current["file"] = "after.md"
        report = scan_rules.render_baseline(baseline, current)
        self.assertIn("Primary aggregate: actionable_unique_spans", report)
        self.assertIn("Actionable unique spans before: 1", report)
        self.assertIn("Actionable unique spans after: 0", report)

    def test_whitelist_only_cli_exits_zero_and_review_exits_one(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            white = directory / "white.md"
            review = directory / "review.md"
            white.write_text("生态环境和数字化转型。", encoding="utf-8")
            review.write_text("业务闭环。", encoding="utf-8")
            command = [sys.executable, str(TOOLS_DIR / "scan_rules.py"), "--text", str(white), "--lang", "zh", "--json"]
            completed = subprocess.run(command, check=False, capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertEqual(json.loads(completed.stdout)["results"][0]["aggregate"]["actionable_unique_spans"], 0)
            command[3] = str(review)
            completed = subprocess.run(command, check=False, capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(completed.returncode, 1, completed.stderr)

    def test_english_rules_still_scan_with_word_boundaries(self) -> None:
        result = scan_rules.scan_text("Moreover, the result is very clear.", self.en_rules, "en")
        self.assertGreaterEqual(self.rule(result, "P-01")["raw_rule_hits"], 1)
        self.assertGreaterEqual(self.rule(result, "P-11")["raw_rule_hits"], 1)


if __name__ == "__main__":
    unittest.main()
