from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


TOOLS_DIR = Path(__file__).resolve().parents[1]
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

import lint_repository


WORKFLOW_ROOT = TOOLS_DIR.parent


class WorkflowContractTests(unittest.TestCase):
    def test_contract_equals_frozen_decisions(self) -> None:
        contract = json.loads((WORKFLOW_ROOT / "workflow" / "contract.json").read_text(encoding="utf-8"))
        self.assertEqual(contract, lint_repository.EXPECTED_CONTRACT)

    def test_round_editing_and_rollback_decisions(self) -> None:
        contract = lint_repository.load_contract()
        self.assertEqual(contract["rounds"]["allowed_total_round_counts"], [3, 5, 7])
        self.assertTrue(contract["rounds"]["zero_round_discovery_allowed"])
        self.assertTrue(contract["rounds"]["final_audit_required_when_layer2_runs"])
        self.assertEqual(contract["editing"]["risk_tiers"], ["A", "B", "C"])
        self.assertFalse(contract["editing"]["sweep_is_a_tier"])
        self.assertFalse(contract["editing"]["tier_mixing_allowed"])
        self.assertTrue(contract["editing"]["exact_before_after_required"])
        self.assertEqual(contract["rollback"]["unit"], "whole_round")
        self.assertFalse(contract["rollback"]["continue_after_fix_failure"])

    def test_anti_regression_and_batch_decisions(self) -> None:
        contract = lint_repository.load_contract()
        self.assertEqual(contract["anti_regression"], {"window_tokens": 10, "overlap_threshold": 0.7})
        self.assertEqual(contract["batch_evaluation"]["primary_population"], "all_valid_inputs")
        self.assertEqual(contract["batch_evaluation"]["quality_failure_threshold"], 25)
        self.assertFalse(contract["batch_evaluation"]["hard_fail_excluded_from_primary"])
        self.assertTrue(contract["batch_evaluation"]["only_input_invalid_excluded"])

    def test_contract_lint_cli(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(TOOLS_DIR / "lint_repository.py"), "contract"],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)


if __name__ == "__main__":
    unittest.main()
