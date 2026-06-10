# Consistency Sweep Report — 2026-06-10

| Check | Status | Detail |
| --- | --- | --- |
| 0-36 scan | explained | 5 occurrences limited to the upgrade plan instructions and the historical report/Erratum. Historical report text is append-only; Erratum records /35. |
| SKILL file map existence | pass | all listed paths exist |
| rules/tools reference coverage | pass | all rules/tools files referenced by SKILL or tools/README |
| planning/execution/SKILL path refs | pass | all concrete backticked paths exist |
| tool help and testdata exits | pass | all expected exit codes observed |
| changed/new files UTF-8 no BOM | pass | all changed/new files decode as UTF-8 without BOM |

Notes: `0-36` remains in the upgrade plan instructions and historical report body because this upgrade keeps historical reports append-only. The appended Erratum records the corrected /35 scale.
