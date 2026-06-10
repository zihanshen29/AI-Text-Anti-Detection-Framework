# Offline Evaluation Prompt

Use this prompt for offline rewrite evaluation only. Do not call or simulate external detectors.

## Inputs

- Source text
- Rewritten text
- Any task-specific constraints supplied with the rewrite

## Evaluation Steps

1. Read the source text and identify the essential claims, facts, terms, audience, and constraints.
2. Read the rewritten text without assigning a score yet.
3. Compare the rewrite against the source for technical and factual fidelity.
4. Check AI signal reduction, readability, naturalness, genre fit, and register fit.
5. Check whether the rewrite accurately targets identified rule hits without broad unnecessary alteration.
6. Check workflow executability, output hygiene, and readiness for the next workflow stage.
7. Check over-rewriting control and all explicit task constraints.
Step 7.5 - Manual rubric score (offline runs only): score the rewrite using `meta/rubric/offline_rubric.md`. Do not embed the full rubric in the evaluation output, and do not treat the manual rubric total as a GPTZero, Zhiwang/CNKI, Turnitin, or other external detector score.
Step 7.6 - Signal vs naturalness balance: compare dimension 1 (AI signal reduction) with dimension 2 (readability and naturalness). Flag `signal-heavy` when dim1 is high but dim2 is low; flag `under-targeted` when dim1 is low but dim2 is high.
Step 7.7 - Outlier rule for batch reports: any sample with total < 25/35 or any hard-fail flag is marked outlier and excluded from aggregate averages, but it must still be shown in the report.
8. Produce the evaluation report in the output format below.

## Output Format

Hard requirements:

- Every evaluation report must copy the fixed header from `templates/eval_report_header.md` before the sample-specific evaluation content.
- Every batch report must include a per-dimension score table for each sample. A batch report without per-sample dimension scores is invalid.

```markdown
## Offline Evaluation

Manual rubric total: <N>/35

Hard-fail flags: <none | comma-separated flags from meta/rubric/offline_rubric.md>

Outlier status: included | excluded from batch average
Outlier reason: none | total < 25/35 | hard-fail flag | wrong-language anomaly | unusable source | other

Dimension scores:
- AI signal reduction: <1-5> - <brief reason>
- Readability and naturalness: <1-5> - <brief reason>
- Technical and factual fidelity: <1-5> - <brief reason>
- Genre and register fit: <1-5> - <brief reason>
- Rule-hit targeting accuracy: <1-5> - <brief reason>
- Workflow executability: <1-5> - <brief reason>
- Over-rewriting control: <1-5> - <brief reason>

signal_vs_naturalness_balance: <healthy | signal-heavy | under-targeted | failed> - <brief reason comparing dim1 and dim2>

Interpretation: <use the interpretation guide from meta/rubric/offline_rubric.md>

Detector score note: The manual rubric total is not a GPTZero, Zhiwang/CNKI, Turnitin, plagiarism, AI-percentage, or other external detector score.

Recommended action: <accept | light revision | substantive revision | rework>
```
