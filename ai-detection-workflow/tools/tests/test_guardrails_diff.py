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

import guardrails_diff


RICH_SOURCE = r"""# Overview
Values −1, +2.5, 1,234.5e-6, 25%, and v1.2.3 are fixed.
[1, 2-3] \citep[see][p. 3]{alpha,beta} [@gamma; @delta]
\label{fig:main} Figure 2.1, Fig. A-2, Table 3-2, Equation 4.1, Eq. 5-2, 图1.2 表3-4 式5.1.
"""


class GuardrailsDiffTests(unittest.TestCase):
    def test_cjk_quantities_and_attached_units_are_guarded(self) -> None:
        cases = (
            ("样本量为30人。", "样本量为80人。", "zh"),
            ("增长10%。", "增长20%。", "zh"),
            ("增长10％。", "增长20％。", "zh"),
            ("温度为−2.5℃。", "温度为−3.5℃。", "zh"),
            ("共有1,234人。", "共有1,235人。", "zh"),
            ("Delay is 10ms.", "Delay is 90ms.", "en"),
            ("Delay is 1.2e−3ms.", "Delay is 1.2e−4ms.", "en"),
            ("Value is .5%.", "Value is .6%.", "en"),
            ("版本v1.2已发布。", "版本v1.3已发布。", "zh"),
        )
        for source, rewrite, language in cases:
            with self.subTest(source=source):
                self.assertTrue(guardrails_diff.extract_entities(source))
                self.assertTrue(guardrails_diff.compare_texts(source, rewrite, language)["hard_failure"])
                self.assertFalse(guardrails_diff.compare_texts(source, source, language)["hard_failure"])

    def test_numeric_boundaries_do_not_extract_identifier_fragments(self) -> None:
        self.assertEqual(guardrails_diff.numbers("sha256 encoder2 item_42"), {})
        self.assertEqual(guardrails_diff.numbers("1.2.3"), {"1.2.3": 1})
        same_values = guardrails_diff.compare_texts("样本量为30人。", "样本总数为30人。", "zh")
        self.assertFalse(same_values["hard_failure"])

    def test_extracts_required_numeric_citation_heading_and_label_forms(self) -> None:
        entities = guardrails_diff.extract_entities(RICH_SOURCE)
        numbers = guardrails_diff.numbers(RICH_SOURCE)
        citations = guardrails_diff.citation_keys(RICH_SOURCE)
        label_values = guardrails_diff.labels(RICH_SOURCE)
        self.assertIn("-1", numbers)
        self.assertIn("+2.5", numbers)
        self.assertIn("1,234.5e-6", numbers)
        self.assertIn("25%", numbers)
        self.assertIn("v1.2.3", numbers)
        self.assertIn("alpha", citations)
        self.assertIn("beta", citations)
        self.assertIn("gamma", citations)
        self.assertIn("delta", citations)
        self.assertIn("latex_label:fig:main", label_values)
        self.assertIn("figure:2.1", label_values)
        self.assertIn("fig:a-2", label_values)
        self.assertIn("table:3-2", label_values)
        self.assertIn("equation:4.1", label_values)
        self.assertTrue(any(entity["kind"] == "markdown_heading" for entity in entities))

    def test_multiset_order_and_scope_changes_are_hard_failures(self) -> None:
        changed_number = guardrails_diff.compare_texts(RICH_SOURCE, RICH_SOURCE.replace("25%", "26%"), "en")
        self.assertTrue(changed_number["hard_failure"])
        self.assertTrue(any(item["check"] == "entity multiset" and item["status"] == "hard_fail" for item in changed_number["checks"]))

        source = "# One\nValue 1.\n# Two\nValue 2.\n"
        rewrite = "# One\nValue 2.\n# Two\nValue 1.\n"
        moved = guardrails_diff.compare_texts(source, rewrite, "en")
        self.assertTrue(moved["hard_failure"])
        self.assertTrue(any(item["check"] == "entity occurrence order" and item["status"] == "hard_fail" for item in moved["checks"]))
        self.assertTrue(any(item["check"] == "nearest heading scope" and item["status"] == "hard_fail" for item in moved["checks"]))

    def test_short_version_and_bare_pandoc_citation_are_guarded(self) -> None:
        source = "Release v1.2 cites @smith2020."
        rewrite = "Release v1.3 cites @jones2024."
        entities = guardrails_diff.extract_entities(source)
        self.assertTrue(any(item["kind"] == "version" and item["value"] == "v1.2" for item in entities))
        self.assertTrue(any(item["kind"] == "pandoc_citation" and item["value"] == "smith2020" for item in entities))
        self.assertTrue(guardrails_diff.compare_texts(source, rewrite, "en")["hard_failure"])

    def test_local_context_change_is_a_review_warning_not_hard_failure(self) -> None:
        source = "Value 10 appears in original wording."
        rewrite = "Value 10 appears in revised wording."
        result = guardrails_diff.compare_texts(source, rewrite, "en")
        self.assertFalse(result["hard_failure"])
        self.assertTrue(result["review_warning"])
        self.assertTrue(result["context_changes"])
        markdown = guardrails_diff.render_markdown(result)
        self.assertIn("review warning", markdown.lower())

    def test_cli_exit_codes_and_json_severity(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "source.md"
            same = root / "same.md"
            warning = root / "warning.md"
            broken = root / "broken.md"
            source.write_text("Value 10 appears in original wording.", encoding="utf-8")
            same.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")
            warning.write_text("Value 10 appears in revised wording.", encoding="utf-8")
            broken.write_bytes(b"\xff\xfe")
            command = [sys.executable, str(TOOLS_DIR / "guardrails_diff.py"), "--source", str(source), "--rewrite", str(same), "--lang", "en", "--json"]
            completed = subprocess.run(command, check=False, capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(completed.returncode, 0, completed.stderr)
            self.assertFalse(json.loads(completed.stdout)["hard_failure"])
            command[5] = str(warning)
            completed = subprocess.run(command, check=False, capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(completed.returncode, 1, completed.stderr)
            payload = json.loads(completed.stdout)
            self.assertTrue(payload["review_warning"])
            self.assertEqual(next(item for item in payload["checks"] if item["check"] == "local context fingerprints")["severity"], "review_warning")
            command[5] = str(broken)
            completed = subprocess.run(command, check=False, capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(completed.returncode, 2)


if __name__ == "__main__":
    unittest.main()
