from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


TOOLS_DIR = Path(__file__).resolve().parents[1]
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

import preflight_plan


WORKFLOW_ROOT = TOOLS_DIR.parent
TESTDATA = TOOLS_DIR / "testdata"
CONTRACT = json.loads((WORKFLOW_ROOT / "workflow" / "contract.json").read_text(encoding="utf-8"))


class PreflightPlanTests(unittest.TestCase):
    def make_project(self) -> tuple[tempfile.TemporaryDirectory[str], Path, Path]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        for source, destination in (
            ("workflow_plan_two_targets.md", "plan.md"),
            ("workflow_target_one.md", "target_one.md"),
            ("workflow_target_two.md", "target_two.md"),
            ("workflow_prior_one.md", "prior_one.md"),
        ):
            shutil.copyfile(TESTDATA / source, root / destination)
        return temporary, root, root / "plan.md"

    def test_multi_file_plan_and_round_selection(self) -> None:
        temporary, root, plan = self.make_project()
        with temporary:
            all_rounds = preflight_plan.preflight(plan, root, "all", CONTRACT)
            self.assertEqual(all_rounds["result_status"], "executable")
            self.assertEqual(len(all_rounds["fixes"]), 2)
            self.assertEqual({item["target_relative"] for item in all_rounds["fixes"]}, {"target_one.md", "target_two.md"})
            selected = preflight_plan.preflight(plan, root, "1", CONTRACT)
            self.assertEqual(selected["result_status"], "executable")
            self.assertEqual([item["fix_id"] for item in selected["fixes"]], ["1.1"])

    def test_path_escape_and_before_count_are_blocking(self) -> None:
        temporary, root, plan = self.make_project()
        with temporary:
            text = plan.read_text(encoding="utf-8").replace("`target_one.md`", "`../escape.md`")
            plan.write_text(text, encoding="utf-8")
            result = preflight_plan.preflight(plan, root, "all", CONTRACT)
            self.assertEqual(result["result_status"], "blocking_review")
            self.assertTrue(any("path escapes" in item for item in result["blockers"]))

            shutil.copyfile(TESTDATA / "workflow_plan_two_targets.md", plan)
            target = root / "target_one.md"
            target.write_text("Alpha source 10 [1].\nAlpha source 10 [1].\n", encoding="utf-8")
            result = preflight_plan.preflight(plan, root, "1", CONTRACT)
            self.assertEqual(result["result_status"], "blocking_review")
            self.assertTrue(any("BEFORE occurs 2" in item for item in result["blockers"]))

    def test_after_hits_and_guardrail_changes_need_review(self) -> None:
        temporary, root, plan = self.make_project()
        with temporary:
            text = plan.read_text(encoding="utf-8").replace("Alpha revised 10 [1].", "Moreover, Alpha revised 10 [1].")
            plan.write_text(text, encoding="utf-8")
            result = preflight_plan.preflight(plan, root, "1", CONTRACT)
            self.assertEqual(result["result_status"], "blocking_review")
            self.assertTrue(any("AFTER rule hits" in item for item in result["blockers"]))

            shutil.copyfile(TESTDATA / "workflow_plan_two_targets.md", plan)
            text = plan.read_text(encoding="utf-8").replace("Alpha revised 10 [1].", "Alpha revised 11 [1].")
            plan.write_text(text, encoding="utf-8")
            result = preflight_plan.preflight(plan, root, "1", CONTRACT)
            self.assertTrue(any("guardrail text changed" in item for item in result["blockers"]))

    def test_mixed_plan_requires_per_fix_language(self) -> None:
        temporary, root, plan = self.make_project()
        with temporary:
            text = plan.read_text(encoding="utf-8").replace("`en`\n", "`mixed`\n", 1).replace("- **Language:** `en`\n", "")
            plan.write_text(text, encoding="utf-8")
            result = preflight_plan.preflight(plan, root, "all", CONTRACT)
            self.assertEqual(result["result_status"], "blocking_review")
            self.assertTrue(any("mixed plan requires per-fix language" in item for item in result["blockers"]))

    def test_fix_outside_round_and_inconsistent_target_languages_are_blocking(self) -> None:
        temporary, root, plan = self.make_project()
        with temporary:
            text = plan.read_text(encoding="utf-8")
            rogue = """### Fix ROGUE - outside round

- **File:** `target_one.md`
- **Language:** `en`
- **Secondary scan disposition:** `none`

**BEFORE (verbatim)**
> hidden

**AFTER (verbatim)**
> hidden replacement

"""
            plan.write_text(text.replace("## Round 1 - Tier A", rogue + "## Round 1 - Tier A"), encoding="utf-8")
            result = preflight_plan.preflight(plan, root, "all", CONTRACT)
            self.assertTrue(any("ROGUE: fix must appear inside a numbered round" in item for item in result["blockers"]))

            text = text.replace("`target_two.md`", "`target_one.md`")
            marker = "- **Language:** `en`\n- **Secondary scan disposition:** `none`\n\n**BEFORE (verbatim)**\n> Beta"
            text = text.replace(marker, marker.replace("`en`", "`zh`"), 1)
            plan.write_text(text, encoding="utf-8")
            result = preflight_plan.preflight(plan, root, "all", CONTRACT)
            self.assertTrue(any("inconsistent per-fix languages en, zh" in item for item in result["blockers"]))

    def test_legacy_single_file_mode_remains_available(self) -> None:
        command = [
            sys.executable,
            str(TOOLS_DIR / "preflight_plan.py"),
            "--plan",
            str(TESTDATA / "preflight_plan_sample.md"),
            "--doc",
            str(TESTDATA / "preflight_doc_once.md"),
            "--json",
        ]
        completed = subprocess.run(command, check=False, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(json.loads(completed.stdout)["mode"], "legacy_single_file")
        command[5] = str(TESTDATA / "preflight_doc_zero.md")
        completed = subprocess.run(command, check=False, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(completed.returncode, 1, completed.stderr)


if __name__ == "__main__":
    unittest.main()
