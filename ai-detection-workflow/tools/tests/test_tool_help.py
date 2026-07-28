from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


TOOLS_DIR = Path(__file__).resolve().parents[1]


class ToolHelpTests(unittest.TestCase):
    def test_every_executable_tool_accepts_help(self) -> None:
        tools = (
            "scan_rules.py",
            "structure_metrics.py",
            "preflight_plan.py",
            "guardrails_diff.py",
            "overlap_check.py",
            "workflow_check.py",
            "lint_repository.py",
        )
        for tool in tools:
            with self.subTest(tool=tool):
                completed = subprocess.run(
                    [sys.executable, str(TOOLS_DIR / tool), "--help"],
                    check=False,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                )
                self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)


if __name__ == "__main__":
    unittest.main()
