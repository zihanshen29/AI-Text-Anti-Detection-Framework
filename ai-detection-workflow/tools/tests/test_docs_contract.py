from __future__ import annotations

import sys
import unittest
from pathlib import Path


TOOLS_DIR = Path(__file__).resolve().parents[1]
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

import lint_repository


WORKFLOW_ROOT = TOOLS_DIR.parent


class DocumentationContractTests(unittest.TestCase):
    def test_every_active_consumer_references_contract(self) -> None:
        for relative_path in lint_repository.ACTIVE_CONTRACT_PATHS:
            text = (WORKFLOW_ROOT / relative_path).read_text(encoding="utf-8")
            self.assertIn("workflow/contract.json", text, relative_path)

    def test_known_contradictory_forms_are_absent(self) -> None:
        for relative_path in lint_repository.ACTIVE_CONTRACT_PATHS:
            text = (WORKFLOW_ROOT / relative_path).read_text(encoding="utf-8")
            self.assertEqual(lint_repository.stale_contract_forms(text), [], relative_path)

    def test_contract_lint_excludes_protected_historical_paths(self) -> None:
        protected_prefixes = (
            Path("meta/proposals"),
            Path("meta/reports"),
            Path("meta/provider_articles"),
            Path("meta/generated_articles"),
        )
        for relative_path in lint_repository.ACTIVE_CONTRACT_PATHS:
            self.assertFalse(any(relative_path.is_relative_to(prefix) for prefix in protected_prefixes), relative_path)
        self.assertEqual(lint_repository.lint_contract(), [])

    def test_batch_template_names_full_primary_population(self) -> None:
        text = (WORKFLOW_ROOT / "templates" / "batch_eval_output.md").read_text(encoding="utf-8")
        self.assertIn("all_valid_inputs", text)
        self.assertIn("All-valid mean", text)
        self.assertIn("All-valid median", text)
        self.assertIn("Hard-fail count/rate", text)

    def test_stale_forms_are_detectable_without_scanning_history(self) -> None:
        stale = "Use 3-6 rounds, Tier D, threshold 0.7, and exclude hard-fail outliers from aggregate."
        issues = lint_repository.stale_contract_forms(stale)
        self.assertGreaterEqual(len(issues), 4)

    def test_ci_covers_both_operating_systems_and_checks_the_tracked_tree(self) -> None:
        text = (WORKFLOW_ROOT.parent / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
        self.assertIn("windows-latest", text)
        self.assertIn("ubuntu-latest", text)
        self.assertIn("python -m unittest discover", text)
        self.assertIn("lint_repository.py all", text)
        self.assertIn("git hash-object -t tree -w --stdin", text)
        self.assertIn("git diff --check $EmptyTree HEAD", text)


if __name__ == "__main__":
    unittest.main()
