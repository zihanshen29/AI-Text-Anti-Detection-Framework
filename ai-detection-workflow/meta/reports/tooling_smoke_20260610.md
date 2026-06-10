# Tooling Smoke Report — 2026-06-10

Generated locally by Codex with the repository offline tools. No external detector was run.

## Scope

- ZH: 16 source/rewrite pairs from `run_20260520` topics 05-08 across deepseek, doubao, gemini, and wenxin.
- EN: 15 source/rewrite pairs from `run_20260520` topics 01-04, excluding `gemini/topic_04` because it is the designated encoding/language anomaly fixture.
- Tools exercised: `scan_rules.py`, `structure_metrics.py`, and `guardrails_diff.py`.

## Aggregate Rule-Hit Results

| Language | Pairs | Rules source | Before hits | After hits | Direction |
| --- | --- | --- | --- | --- | --- |
| zh | 16 | `rules/zh/rules.yaml` | 414 | 277 | down |
| en | 15 | `rules/en/rules.yaml` | 441 | 227 | down |

## Comparison With 2026-05-20 Manual after_repair Counts

| Language | after_repair manual count | rules.yaml smoke count | Same direction? | Notes |
| --- | --- | --- | --- | --- |
| zh | 254 -> 159 | 414 -> 277 | yes | Different watch-list: after_repair used an ad hoc 31-term list; this report uses canonical `rules/zh/rules.yaml` auto rules only. |
| en | 196 -> 9 | 441 -> 227 | yes | Different watch-list: after_repair used hand-counted repair targets; this report uses canonical `rules/en/rules.yaml` auto rules only. |

Expected mismatch: the two after_repair reports used temporary manual watch-lists and included judgment calls. Future offline counts should use the `rules.yaml` path as the canonical, reproducible mouthpiece. Offline literal hits only; not a detector score.

## Guardrail Summary

| Language | Pairs checked | Pass | Fail |
| --- | --- | --- | --- |
| zh | 16 | 13 | 3 |
| en | 15 | 15 | 0 |

Guardrail failures are listed in the pair tables below for review; they are deterministic findings, not detector scores.

## ZH Pair Details

| Model | Topic | Before hits | After hits | Delta | Guardrails | Sent CV Δ | Para CV Δ | Em-dash Δ | Spaced hyphen Δ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| deepseek | topic_05 | 24 | 14 | -10 | pass | 0.003 | -0.001 | 0 | 0 |
| deepseek | topic_06 | 15 | 15 | 0 | pass | 0.0 | 0.0 | 0 | 0 |
| deepseek | topic_07 | 20 | 13 | -7 | pass | -0.002 | -0.001 | 0 | 0 |
| deepseek | topic_08 | 11 | 8 | -3 | pass | -0.001 | 0.001 | 0 | 0 |
| doubao | topic_05 | 39 | 25 | -14 | pass | -0.001 | 0.0 | 0 | 0 |
| doubao | topic_06 | 30 | 22 | -8 | pass | 0.0 | 0.001 | 0 | 0 |
| doubao | topic_07 | 31 | 18 | -13 | pass | -0.001 | 0.0 | 0 | 0 |
| doubao | topic_08 | 46 | 21 | -25 | fail: headings | -0.001 | -0.001 | 0 | 0 |
| gemini | topic_05 | 38 | 25 | -13 | pass | 0.0 | -0.001 | 0 | 0 |
| gemini | topic_06 | 32 | 25 | -7 | fail: headings | -0.002 | -0.001 | 0 | 0 |
| gemini | topic_07 | 30 | 20 | -10 | pass | 0.0 | 0.001 | 0 | 0 |
| gemini | topic_08 | 29 | 17 | -12 | fail: headings | 0.0 | -0.003 | 0 | 0 |
| wenxin | topic_05 | 16 | 9 | -7 | pass | 0.001 | 0.0 | 0 | 0 |
| wenxin | topic_06 | 17 | 14 | -3 | pass | 0.0 | 0.0 | 0 | 0 |
| wenxin | topic_07 | 16 | 15 | -1 | pass | 0.0 | 0.0 | 0 | 0 |
| wenxin | topic_08 | 20 | 16 | -4 | pass | 0.0 | -0.001 | 0 | 0 |

## EN Pair Details

| Model | Topic | Before hits | After hits | Delta | Guardrails | Sent CV Δ | Para CV Δ | Em-dash Δ | Spaced hyphen Δ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| deepseek | topic_01 | 25 | 14 | -11 | pass | -0.002 | -0.001 | -9 | 9 |
| deepseek | topic_02 | 26 | 19 | -7 | pass | 0.0 | 0.0 | -7 | 7 |
| deepseek | topic_03 | 22 | 11 | -11 | pass | -0.001 | 0.0 | -9 | 9 |
| deepseek | topic_04 | 20 | 15 | -5 | pass | -0.001 | 0.001 | -1 | 1 |
| doubao | topic_01 | 27 | 11 | -16 | pass | -0.041 | -0.148 | -11 | 11 |
| doubao | topic_02 | 23 | 16 | -7 | pass | -0.023 | -0.091 | -7 | 7 |
| doubao | topic_03 | 39 | 13 | -26 | pass | -0.051 | -0.149 | -12 | 12 |
| doubao | topic_04 | 45 | 19 | -26 | pass | -0.034 | -0.15 | -15 | 15 |
| gemini | topic_01 | 32 | 17 | -15 | pass | -0.005 | 0.004 | -6 | 6 |
| gemini | topic_02 | 36 | 17 | -19 | pass | -0.001 | 0.001 | -7 | 7 |
| gemini | topic_03 | 35 | 19 | -16 | pass | 0.0 | 0.0 | -6 | 6 |
| wenxin | topic_01 | 25 | 7 | -18 | pass | -0.001 | 0.003 | -13 | 13 |
| wenxin | topic_02 | 31 | 10 | -21 | pass | -0.001 | 0.001 | -18 | 18 |
| wenxin | topic_03 | 35 | 19 | -16 | pass | 0.002 | 0.0 | -15 | 15 |
| wenxin | topic_04 | 20 | 20 | 0 | pass | 0.0 | 0.0 | 0 | 0 |

## Fixed Disclaimers

- `scan_rules.py`: Offline literal hits only; not a detector score.
- `structure_metrics.py`: Structural proxies only; no validated correlation to any external detector.
