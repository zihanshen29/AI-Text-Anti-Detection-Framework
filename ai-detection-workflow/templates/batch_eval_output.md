# Batch Offline Evaluation - <batch ID or date>

**Run date:** <YYYY-MM-DD>
**Evaluator agent:** <Codex / Claude / other>
**Rule library commit:** <hash>
**Number of samples:** <N>
**Measurement type:** offline_rule_hits (all samples)
**External detector status:** not run
**Rubric scale:** 35 points (seven dimensions, each 1-5)
**Batch averaging rule:** samples with total `< 25/35` or any hard-fail flag are marked `outlier` and excluded from aggregate averages, but they must remain visible in the report.

## Disclaimer

External detector status: not run for this batch. This batch evaluation used the framework's offline rule-hit measurement only. No GPTZero, Turnitin, CNKI, Wanfang, VIP, PaperYY, PaperPass, or other external detector was run. Results are expected signal reductions based on the framework's own pattern rules. They have no validated correlation to real detector outputs and must not be reported as AI-detection score reductions.

All rewrites in this batch were produced under strict Layer 2 discipline: every edit is an exact before/after string replacement listed in the per-sample condensed plan section below. No creative paragraph-level rewriting was performed.

## Per-sample results

### Sample 1 - <sample ID>

- **Source path:** <path>
- **Rewritten path:** <path>
- **Language:** en / zh
- **Genre:** <thesis / paper / report / blog / other>
- **Approximate length:** <N> words or <N> characters
- **Encoding preflight:** UTF-8 confirmed, mojibake scan pass

**Condensed plan (the exact fix list applied to this sample):**

| Fix ID | Rule | Tier | BEFORE | AFTER |
|:---|:---|:---:|:---|:---|
| 1 | <P-NN> | A | <verbatim> | <verbatim> |
| 2 | <C-NN> | B | <verbatim> | <verbatim> |
| ... | ... | ... | ... | ... |

**Rule hits before -> after (offline count):**

| Rule | Before | After | Delta |
|:---|:---:|:---:|:---:|
| <P-NN / V-NN / C-NN / S-NN> | <X> | <Y> | <+/-Z> |
| ... | ... | ... | ... |

**Offline rule hits summary:** <one-paragraph summary of highest-impact rules, unchanged rules, and any new rule hits introduced>

**Manual rubric (per `meta/rubric/offline_rubric.md`):**

| Dimension | Score | Notes |
|:---|:---:|:---|
| AI signal reduction | _/5 | |
| Readability and naturalness | _/5 | |
| Technical and factual fidelity | _/5 | |
| Genre and register fit | _/5 | |
| Rule-hit targeting accuracy | _/5 | |
| Workflow executability | _/5 | |
| Over-rewriting control | _/5 | |
| **Total** | **_/35** | |

**signal_vs_naturalness_balance:**

- **Balance status:** healthy | signal-heavy | under-targeted | failed
- **Rule:** compare AI signal reduction (dimension 1) against readability/naturalness (dimension 2).
- **Interpretation:** dim1=5 and dim2=1-2 means the rewrite likely sacrificed naturalness for signal reduction; dim1=5 and dim2=4-5 is healthy; dim1<=2 and dim2>=4 means the text stayed natural but did not address the core signal.
- **Notes:** <one sentence>

**Outlier status:**

- **Included in batch averages:** yes | no
- **Reason if excluded:** total < 25/35 | hard-fail flag | wrong-language anomaly | unusable source | other

**Hard-fail flags (if any):** none | <list with quoted offending passages>

**Fidelity verdict:** pass / caution / fail
- Numbers preserved: yes / no (list violations)
- Citations preserved: yes / no
- Technical terms preserved: yes / no
- Proper nouns preserved: yes / no

**New issues introduced (if any):** <list>

**Residual signals to keep (factual content not to erase):** <list with one-sentence justification each>

### Sample 2 - <sample ID>

[same structure]

### Sample N - <sample ID>

[same structure]

## Cross-sample observations

- Patterns that appeared in multiple samples and behaved similarly: <list>
- Patterns that appeared in multiple samples but behaved differently across genres: <list>
- Rules that fired in zero samples (candidates for deprecation or rewrite): <list>
- Patterns observed but matching no current rule (candidates for the rule library): <list>
- Naturalness tradeoffs: <summarize samples where rule-hit reduction lowered readability/naturalness>
- Outliers excluded from averages: <list sample IDs and reasons; write "none" if all included>

## Signals for the middle loop

At most 5 bullets, each pointing to a specific rule ID, with evidence quantified across samples.

## Caveats

- Sample size: <N>. Cross-sample claims require at least 3 samples agreeing in direction.
- All evidence is offline rule-hit counts and manual rubric. No external detector results.
- The framework's rule library version: <commit hash>. Results are not portable to a future rule library version without re-running.
- Manual rubric totals are always out of 35, not 36 or any detector percentage.
