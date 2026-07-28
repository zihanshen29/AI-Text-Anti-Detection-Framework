from __future__ import annotations

import json
import random
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path


TOOLS_DIR = Path(__file__).resolve().parents[1]
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

import overlap_check


class OverlapCheckTests(unittest.TestCase):
    def test_indexed_algorithm_matches_naive_reference_for_seeded_english_and_chinese(self) -> None:
        randomizer = random.Random(20260728)
        english_vocab = [f"term{index}" for index in range(31)]
        chinese_vocab = list("可靠性验证流程文本上下文证据计划审计")
        cases = [
            ("en", " ".join(randomizer.choice(english_vocab) for _ in range(160)), " ".join(randomizer.choice(english_vocab) for _ in range(155))),
            ("zh", "".join(randomizer.choice(chinese_vocab) for _ in range(180)), "".join(randomizer.choice(chinese_vocab) for _ in range(175))),
        ]
        for language, current, prior in cases:
            optimized = overlap_check.analyze_texts(current, prior, language, 10, 0.7)
            naive = overlap_check.naive_analyze_texts(current, prior, language, 10, 0.7)
            self.assertEqual({key: value for key, value in optimized.items() if key != "algorithm"}, {key: value for key, value in naive.items() if key != "algorithm"})

    def test_counter_semantics_and_tie_breaking_are_preserved(self) -> None:
        current = "alpha alpha beta gamma delta epsilon"
        prior = "alpha beta alpha gamma delta epsilon zeta"
        optimized = overlap_check.analyze_texts(current, prior, "en", 4, 0.7)
        naive = overlap_check.naive_analyze_texts(current, prior, "en", 4, 0.7)
        self.assertEqual(optimized["findings"], naive["findings"])

    def test_two_thousand_token_performance_regression(self) -> None:
        current = " ".join(f"token{index % 503}" for index in range(2000))
        prior = " ".join(f"token{(index * 7) % 503}" for index in range(2000))
        started = time.perf_counter()
        result = overlap_check.analyze_texts(current, prior, "en", 10, 0.7)
        elapsed = time.perf_counter() - started
        self.assertLess(elapsed, 8.0, f"indexed overlap took {elapsed:.3f}s")
        self.assertEqual(result["current_window_count"], 1991)

    def test_cli_exit_codes_and_algorithm_output(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            current = root / "current.md"
            prior = root / "prior.md"
            unrelated = root / "unrelated.md"
            current.write_text("alpha beta gamma delta epsilon", encoding="utf-8")
            prior.write_text("alpha beta gamma delta epsilon", encoding="utf-8")
            unrelated.write_text("one two three four five", encoding="utf-8")
            command = [sys.executable, str(TOOLS_DIR / "overlap_check.py"), "--current", str(current), "--prior", str(prior), "--window", "3", "--threshold", "0.7", "--json"]
            completed = subprocess.run(command, check=False, capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(completed.returncode, 1, completed.stderr)
            self.assertEqual(json.loads(completed.stdout)["algorithm"], "token_postings_exact_counter_overlap")
            command[5] = str(unrelated)
            completed = subprocess.run(command, check=False, capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(completed.returncode, 0, completed.stderr)
            command[7] = "0"
            completed = subprocess.run(command, check=False, capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(completed.returncode, 2)


if __name__ == "__main__":
    unittest.main()
