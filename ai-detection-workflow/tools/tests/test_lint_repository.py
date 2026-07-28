from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


TOOLS_DIR = Path(__file__).resolve().parents[1]


class LintRepositoryTests(unittest.TestCase):
    def test_all_active_lint_modes_pass(self) -> None:
        for mode in ("rules", "contract", "gates", "all"):
            completed = subprocess.run(
                [sys.executable, str(TOOLS_DIR / "lint_repository.py"), mode],
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)

    def test_unknown_mode_is_argument_error(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(TOOLS_DIR / "lint_repository.py"), "unknown"],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(completed.returncode, 2)


if __name__ == "__main__":
    unittest.main()
