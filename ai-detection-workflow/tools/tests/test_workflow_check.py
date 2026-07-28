from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


TOOLS_DIR = Path(__file__).resolve().parents[1]
TESTDATA = TOOLS_DIR / "testdata"


class WorkflowCheckTests(unittest.TestCase):
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

    def run_tool(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(TOOLS_DIR / "workflow_check.py"), *arguments],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

    def create_manifest(self, root: Path, plan: Path) -> tuple[Path, dict]:
        manifest = root / "plan-manifest.json"
        completed = self.run_tool(
            "plan",
            "--plan",
            str(plan),
            "--round",
            "all",
            "--project-root",
            str(root),
            "--snapshot-dir",
            str(root / "snapshots"),
            "--output",
            str(manifest),
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        return manifest, json.loads(manifest.read_text(encoding="utf-8"))

    def test_discovery_hits_are_evidence_not_failure(self) -> None:
        temporary, root, plan = self.make_project()
        with temporary:
            target = root / "target_one.md"
            target.write_text("Moreover, Alpha source 10 [1].", encoding="utf-8")
            output = root / "discovery.json"
            completed = self.run_tool("discovery", "--text", str(target), "--lang", "en", "--output", str(output))
            self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
            payload = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(payload["result_status"], "complete")
            self.assertEqual(payload["external_detector_status"], "not_run")
            self.assertGreater(payload["component_results"]["rule_scan"]["aggregate"]["actionable_unique_spans"], 0)
            self.assertEqual(payload["target"]["hash_kind"], "worktree_raw_sha256")

    def test_plan_snapshots_preserve_bytes_and_provenance(self) -> None:
        temporary, root, plan = self.make_project()
        with temporary:
            manifest_path, manifest = self.create_manifest(root, plan)
            self.assertEqual(manifest["manifest_kind"], "ai-detection-workflow-plan-manifest")
            self.assertEqual(len(manifest["targets"]), 2)
            for target in manifest["targets"]:
                snapshot = Path(target["snapshot_path"])
                original = Path(target["target_path"])
                self.assertEqual(snapshot.read_bytes(), original.read_bytes())
                self.assertEqual(target["snapshot"]["hash_kind"], "worktree_raw_sha256")
                self.assertEqual(target["snapshot"]["sha256"], hashlib.sha256(snapshot.read_bytes()).hexdigest())
                self.assertTrue(target["target_relative_path"])
                self.assertIn("overlap_settings", target)
            self.assertEqual(manifest_path, root / "plan-manifest.json")

    def test_post_round_number_change_requires_whole_round_rollback(self) -> None:
        temporary, root, plan = self.make_project()
        with temporary:
            manifest, _ = self.create_manifest(root, plan)
            target = root / "target_one.md"
            target.write_text("Alpha revised 11 [1].", encoding="utf-8")
            output = root / "post.json"
            completed = self.run_tool("post-round", "--manifest", str(manifest), "--output", str(output))
            self.assertEqual(completed.returncode, 1, completed.stdout + completed.stderr)
            payload = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(payload["result_status"], "whole_round_rollback_required")
            self.assertEqual(payload["rollback_unit"], "whole_round")

    def test_post_round_rule_and_structure_deltas_require_review_without_detector(self) -> None:
        temporary, root, plan = self.make_project()
        with temporary:
            manifest, _ = self.create_manifest(root, plan)
            target = root / "target_one.md"
            target.write_text("Moreover, Alpha source 10 [1].", encoding="utf-8")
            output = root / "post.json"
            completed = self.run_tool("post-round", "--manifest", str(manifest), "--output", str(output))
            self.assertEqual(completed.returncode, 1, completed.stdout + completed.stderr)
            payload = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(payload["result_status"], "review_required")
            target_result = next(item for item in payload["targets"] if item["target_relative_path"] == "target_one.md")
            self.assertEqual(target_result["components"]["rule_scan"]["status"], "review_required")
            self.assertEqual(payload["external_detector_status"], "not_run")

    def test_post_round_rejects_non_plan_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            bad_manifest = root / "bad.json"
            bad_manifest.write_text('{"command_type": "plan"}', encoding="utf-8")
            output = root / "output.json"
            completed = self.run_tool("post-round", "--manifest", str(bad_manifest), "--output", str(output))
            self.assertEqual(completed.returncode, 2)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
