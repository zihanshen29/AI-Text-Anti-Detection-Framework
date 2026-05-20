# English Rewrite Evaluation Report - run_20260520 topics 01-04

**Evaluation date:** 2026-05-20
**Evaluator:** Codex English effect evaluation sub-agent
**Scope:** doubao/deepseek/wenxin/gemini `topic_01.md` through `topic_04.md`, 16 source/rewrite pairs
**Normal English evaluation set:** 15 samples; `gemini/topic_04.md` is an anomalous non-English source and is excluded from normal English-effect averages
**Measurement type:** offline manual rubric + offline rule/watch-list statistics
**External detector status:** not run

## Disclaimer

External detector status: not run. This report uses only the project offline rubric, English rule files, local file comparisons, batch report review, and offline literal rule/watch-list counts. No GPTZero, Turnitin, Originality.ai, Pangram, Copyleaks, ZeroGPT, or other external detector was run, and no score below is a detector score.

No source article was modified during this evaluation. No workflow, template, rule, or SKILL.md file was modified.

## Materials Reviewed

- Source root: `ai-detection-workflow/meta/provider_articles/run_20260520`
- Rewrite root: `ai-detection-workflow/meta/provider_articles/run_20260520_rewritten_en`
- Batch report: `ai-detection-workflow/meta/provider_articles/run_20260520_rewritten_en/en_rewrite_batch_report.md`
- Rubric: `ai-detection-workflow/meta/rubric/offline_rubric.md`
- English rules: `rules/en/tell_tale_phrases.md`, `rules/en/sentence_patterns.md`, `rules/en/detector_profiles.md`

## Batch Rule-Hit Movement

The batch report's offline rule-hit totals were summed from the per-sample rule tables. `gemini/topic_04.md` had 0 English hits and is excluded from normal English-effect totals because the source is Chinese, not English prose.

| Model | Samples counted | Rule hits before | Rule hits after | Delta | Reduction |
|:---|---:|---:|---:|---:|---:|
| doubao | 4 | 69 | 1 | -68 | 98.6% |
| deepseek | 4 | 35 | 5 | -30 | 85.7% |
| wenxin | 4 | 54 | 3 | -51 | 94.4% |
| gemini | 3 | 44 | 1 | -43 | 97.7% |
| **Normal English total** | **15** | **202** | **10** | **-192** | **95.0%** |

A separate local watch-list count over common P/V-rule strings showed the same direction: 196 -> 9 across the 15 normal English samples. These are literal offline counts, not detector outputs.

## Layer 2 Compliance

The batch report includes an exact condensed BEFORE/AFTER plan for every edited sample. Samples with no safe edit selected are explicitly recorded as `none` (`wenxin/topic_04.md`, `gemini/topic_04.md`). Diff checks show small local substitutions rather than free paragraph rewriting: edited samples generally changed only 2-13 lines each, with equal added/deleted line counts.

No evidence of paragraph-level free rewrite was found. Numbers and Markdown heading counts were preserved across all 16 source/rewrite pairs. The main Layer 2 quality issue is that exact substitutions were sometimes too literal: replacing `In conclusion, ` with empty text can leave a paragraph beginning with lowercase (`battery swapping...`, `the integration...`), and replacing em dashes with spaced hyphens fixes P-04 but leaves typographically rough prose.

## Anomalous Sample

`gemini/topic_04.md` is not an English source article. It is Chinese prose about battery swapping for urban delivery fleets. The rewrite copy is unchanged and correctly received no English-rule edits. This sample is marked with `language_or_register_mismatch` for the English batch scope and is not included in normal English model averages.

This is a dataset/source-selection issue rather than a rewrite failure: English reduction cannot be evaluated against a Chinese source using English rules.

## Per-Sample Rubric Scores

Dimensions: AI signal reduction, readability/naturalness, technical/factual fidelity, genre/register fit, rule-hit targeting accuracy, workflow executability, over-rewriting control. Maximum total: 35. Scores are offline manual rubric scores only.

| Sample | AI | Natural | Fidelity | Register | Targeting | Workflow | Overwrite | Total | Notes |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|:---|
| doubao/topic_01 | 4 | 4 | 5 | 3 | 4 | 5 | 4 | 29 | Strong hit reduction; residual Chinese term/notice affects English register. |
| doubao/topic_02 | 5 | 4 | 5 | 4 | 5 | 5 | 3 | 31 | Effective conservative pass; only rough hyphen style remains. |
| doubao/topic_03 | 4 | 3 | 5 | 3 | 4 | 5 | 4 | 28 | Several Chinese fragments remain (`教师`, `弱势学生`); residual `In the end`. |
| doubao/topic_04 | 4 | 2 | 4 | 2 | 5 | 5 | 2 | 24 | Mixed Chinese terms, lowercase paragraph after conclusion-marker deletion; needs repair. |
| deepseek/topic_01 | 4 | 5 | 5 | 5 | 4 | 5 | 3 | 31 | Clean, factual, conservative. |
| deepseek/topic_02 | 4 | 5 | 5 | 5 | 4 | 5 | 3 | 31 | Clean reduction with no factual/Markdown issue found. |
| deepseek/topic_03 | 4 | 4 | 5 | 5 | 4 | 5 | 3 | 30 | Residual `navigate`-class signal noted by batch report. |
| deepseek/topic_04 | 3 | 4 | 5 | 5 | 4 | 5 | 3 | 29 | Residual connector count remains; `less...than...` rewrite is acceptable but slightly awkward. |
| wenxin/topic_01 | 4 | 4 | 5 | 4 | 5 | 5 | 3 | 30 | Good reduction; Chinese generated-content notice remains. |
| wenxin/topic_02 | 4 | 4 | 5 | 4 | 4 | 5 | 3 | 29 | Residual P-12 and Chinese notice remain. |
| wenxin/topic_03 | 5 | 4 | 5 | 4 | 5 | 5 | 3 | 31 | Strong reduction; Chinese notice remains but article body is clean. |
| wenxin/topic_04 | 3 | 4 | 5 | 4 | 3 | 5 | 4 | 28 | No edit selected; residual P-12 remains. |
| gemini/topic_01 | 4 | 5 | 5 | 5 | 4 | 5 | 3 | 31 | Strong pass; only minor residual connector. |
| gemini/topic_02 | 5 | 4 | 5 | 5 | 5 | 5 | 2 | 31 | Strong reduction; spaced hyphen style is rough but usable. |
| gemini/topic_03 | 4 | 3 | 5 | 4 | 5 | 5 | 2 | 28 | Lowercase paragraph start after deleting `In conclusion`; needs small repair. |
| gemini/topic_04 | n/a | n/a | n/a | n/a | n/a | 5 | 5 | n/a | Anomalous Chinese source; excluded from English scoring. |

## Model Averages

| Model | Average total | Normal samples | Interpretation |
|:---|---:|---:|:---|
| deepseek | 30.3 | 4 | Best overall quality: clean English, strong fidelity, few register issues. |
| gemini | 30.0 | 3 | Strong on valid English samples, but source batch has one excluded Chinese anomaly. |
| wenxin | 29.5 | 4 | Effective reduction; residual Chinese AI-generated notice and one no-op sample keep it below deepseek. |
| doubao | 28.0 | 4 | Highest rule-hit reduction, but mixed-language leftovers and lowercase conclusion repair needs lower usability. |
| **Overall normal English set** | **29.3** | **15** | Usable with targeted repairs. |

If `gemini/topic_04.md` were forced into the model average as an English sample, gemini would receive a dominant language/register hard fail. The more defensible interpretation is to exclude it from English-effect scoring and report it as a source-batch anomaly.

## Model-Level Findings

**doubao:** Strong offline rule-hit reduction, mostly by removing em dashes and explicit transitions. Quality is uneven because source/rewrite text still contains Chinese fragments (`预警`, `教师`, `弱势学生`, `station选址`, `energy补给`) and Chinese generated-content notices. `topic_04` also has a lowercase paragraph after `In conclusion,` deletion. Needs repair before final use.

**deepseek:** Most stable English batch. Edits are narrow, numbers and structure hold, and the prose remains natural. Remaining signals are mostly residual connectors or vocabulary that were consciously left to avoid over-editing.

**wenxin:** Good reduction on topics 01-03; topic_04 had no conservative edit, so residual `not only/not just` style remains. All wenxin files retain the Chinese generated-content footer, which is a language/register issue for an English deliverable.

**gemini:** Valid English samples show strong reduction and good fidelity. `topic_03` needs a capitalization repair after deleting `In conclusion,`. `topic_04` is a Chinese article and should be routed to the Chinese workflow or replaced by an English source.

## Hard-Fail Flags

| Sample | Flags | Rationale |
|:---|:---|:---|
| gemini/topic_04 | `language_or_register_mismatch`, `unusable_output` for English evaluation | Source and rewrite are Chinese, outside English rule scope. |
| doubao/topic_04 | localized `language_or_register_mismatch` | Mixed Chinese terms remain in otherwise English prose; not a whole-sample hard fail, but repair is needed. |

No `fabrication`, `meaning_break`, `detector_score_claim`, or `prompt_or_process_leak` was found in the normal English samples. Numbers and Markdown headings were preserved in all checked pairs.

## Remaining Risks

- P-04 em-dash removal is highly effective for the offline rule count, but replacing every em dash with ` - ` can leave rough punctuation and should be polished selectively.
- Deleting conclusion markers without capitalizing the following word caused at least two lowercase paragraph starts: doubao/topic_04 and gemini/topic_03.
- Several English-batch outputs retain Chinese metadata/footer text or Chinese terms from the source. This is especially visible in doubao and wenxin.
- The pass focuses mainly on literal phrase cleanup. Higher-level sentence-pattern signals such as uniform rhythm, paragraph symmetry, and repeated rhetorical structure may remain.
- `wenxin/topic_04.md` received no edit; it is valid English but still has residual P-12 hits.

## Repair Recommendation

Do a small targeted repair pass before treating the English batch as final:

- Replace or translate remaining Chinese fragments in English files, or mark those source files as mixed-language anomalies if translation is out of scope.
- Capitalize paragraph starts created by deleting `In conclusion,`.
- Replace mechanical ` - ` punctuation with commas, semicolons, parentheses, or retained hyphens where appropriate.
- Revisit `wenxin/topic_04.md` for safe P-12 fixes if strict rule reduction is required.
- Remove or standardize Chinese AI-generated-content notices if the deliverable is expected to be English-only.

The batch does not need broad paragraph-level rework. It needs localized cleanup and anomaly handling.
