from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


TOOLS_DIR = Path(__file__).resolve().parents[1]


class StructureMetricsTests(unittest.TestCase):
    def test_metrics_cli_and_encoding_failure_exit_codes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "source.md"
            current = root / "current.md"
            invalid = root / "invalid.md"
            source.write_text("First sentence. Second sentence.\n\nAnother paragraph.", encoding="utf-8")
            current.write_text("First sentence changed. Second sentence.\n\nAnother paragraph.", encoding="utf-8")
            invalid.write_bytes(b"\xff")
            command = [sys.executable, str(TOOLS_DIR / "structure_metrics.py"), "--text", str(current), "--baseline", str(source), "--lang", "en", "--json"]
            completed = subprocess.run(command, check=False, capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(completed.returncode, 0, completed.stderr)
            payload = json.loads(completed.stdout)
            self.assertIn("baseline", payload)
            self.assertIn("current", payload)
            command[3] = str(invalid)
            completed = subprocess.run(command, check=False, capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(completed.returncode, 2)


if __name__ == "__main__":
    unittest.main()
