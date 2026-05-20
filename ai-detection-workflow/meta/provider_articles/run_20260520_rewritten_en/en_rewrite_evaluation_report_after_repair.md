# English Rewrite Evaluation Report After Repair

Work address: `E:\app\AI-Text-Anti-Detection-Framework`

Source root: `E:\app\AI-Text-Anti-Detection-Framework\ai-detection-workflow\meta\provider_articles\run_20260520`

Rewrite root: `E:\app\AI-Text-Anti-Detection-Framework\ai-detection-workflow\meta\provider_articles\run_20260520_rewritten_en`

External detector status: not run. This review uses only the project offline rubric, offline watch-list statistics, Layer 2 batch-report checks, and manual source/rewrite comparison.

## Scope

Normal English evaluation set: 15 source/rewrite pairs:

- `doubao/topic_01.md` through `doubao/topic_04.md`
- `deepseek/topic_01.md` through `deepseek/topic_04.md`
- `wenxin/topic_01.md` through `wenxin/topic_04.md`
- `gemini/topic_01.md` through `gemini/topic_03.md`

Excluded anomaly: `gemini/topic_04.md`.

Reason: the source is not a normal English article. It is Chinese/non-English content in mojibake-like form, and the rewrite remains effectively unchanged. It is listed separately and is not included in normal English model averages or overall English effectiveness conclusions.

## Repair Verification

Requested hard-fix checks on the normal 15 English rewrites:

| Check | Result |
| --- | --- |
| Chinese residual text | Pass: no CJK matches found in the normal 15 rewrites |
| Chinese generation notices / prompt tail notes | Pass: no matches for Chinese generation-note patterns |
| Lowercase paragraph starts after deletion edits | Pass: no case-sensitive lowercase paragraph starts found |
| Numeric preservation | Pass: source numeric tokens are preserved in all 16 checked pairs |
| Markdown heading preservation | Pass: heading counts/text are preserved in all 16 checked pairs |

The previously observed Chinese prompt tail notes in `doubao`/`wenxin`, mixed Chinese terms in `doubao`, and lowercase paragraph starts in `doubao/topic_04.md` and `gemini/topic_03.md` are no longer present in the normal English set.

## Offline Watch-List Statistics

Watch-list terms included common transitional/cliche markers and flagged vocabulary such as `Furthermore`, `Additionally`, `Moreover`, `Consequently`, `Notably`, `Importantly`, `In addition`, `In particular`, `Indeed`, `In recent years`, `In conclusion`, `Ultimately`, `Overall`, `not just`, `not only`, `delve`, `nuanced`, `multifaceted`, `tapestry`, `intricate`, `pivotal`, `paramount`, `realm of`, `landscape of`, `robust`, `leverage`, `crucial`, `comprehensive`, `fostering`, `utilize`, `facilitate`, `game-changer`, `harness the power of`, `state-of-the-art`, and em dash.

Normal 15 aggregate:

| Metric | Source | Rewrite | Change |
| --- | ---: | ---: | ---: |
| Watch-list hits | 196 | 9 | -187 |
| Reduction |  |  | 95.4% |

By model, excluding `gemini/topic_04.md`:

| Model | Source hits | Rewrite hits | Reduction | Notes |
| --- | ---: | ---: | ---: | --- |
| doubao | 67 | 1 | 98.5% | Strong lexical cleanup after repair; remaining risk is mostly punctuation/phrase polish |
| deepseek | 31 | 1 | 96.8% | Cleanest procedural rewrite style; low residual signal |
| wenxin | 57 | 6 | 89.5% | Improved after footer removal, but `topic_04` remains comparatively under-edited |
| gemini | 41 | 1 | 97.6% | Normal 3 English samples are clean after lowercase fix; anomaly excluded |

Per-sample local watch-list results:

| Sample | Source hits | Rewrite hits | Delta |
| --- | ---: | ---: | ---: |
| doubao/topic_01.md | 15 | 0 | -15 |
| doubao/topic_02.md | 7 | 0 | -7 |
| doubao/topic_03.md | 20 | 0 | -20 |
| doubao/topic_04.md | 25 | 1 | -24 |
| deepseek/topic_01.md | 10 | 0 | -10 |
| deepseek/topic_02.md | 7 | 0 | -7 |
| deepseek/topic_03.md | 10 | 0 | -10 |
| deepseek/topic_04.md | 4 | 1 | -3 |
| wenxin/topic_01.md | 16 | 0 | -16 |
| wenxin/topic_02.md | 20 | 1 | -19 |
| wenxin/topic_03.md | 16 | 0 | -16 |
| wenxin/topic_04.md | 5 | 5 | 0 |
| gemini/topic_01.md | 11 | 0 | -11 |
| gemini/topic_02.md | 16 | 1 | -15 |
| gemini/topic_03.md | 14 | 0 | -14 |

## Offline Rubric Scores

Scale: 0-36, following the offline rubric categories: AI-signal reduction, naturalness, factual fidelity, genre/register fit, rule-targeting precision, workflow executability, and over-rewrite control. Scores are offline human/rule judgments, not detector scores.

| Model | Topic | Score | Assessment |
| --- | --- | ---: | --- |
| doubao | topic_01 | 31 | Chinese notice removed; rule hits eliminated; facts and structure preserved |
| doubao | topic_02 | 31 | Good targeted cleanup; no Chinese residue; minor mechanical punctuation remains |
| doubao | topic_03 | 31 | Mixed Chinese terms removed; good preservation with lower AI signal |
| doubao | topic_04 | 29 | Lowercase paragraph-start issue fixed; residual phrasing/punctuation roughness remains |
| deepseek | topic_01 | 31 | Strong signal reduction with stable register and facts |
| deepseek | topic_02 | 31 | Clean, controlled rewrite; minimal residual rule hits |
| deepseek | topic_03 | 30 | Good overall, with some remaining formulaic sentence rhythm |
| deepseek | topic_04 | 29 | Adequate but less transformative because source had fewer obvious hits |
| wenxin | topic_01 | 31 | Chinese footer removed; clean enough for normal batch use |
| wenxin | topic_02 | 30 | Footer removed; one residual transition/cliche pattern remains |
| wenxin | topic_03 | 32 | Strongest wenxin sample after repair; clean and faithful |
| wenxin | topic_04 | 29 | Footer removed, but local hits did not decline; under-edited compared with other samples |
| gemini | topic_01 | 31 | Low residual signal and stable Markdown structure |
| gemini | topic_02 | 31 | Strong targeted reduction; minor residual lexical marker |
| gemini | topic_03 | 31 | Lowercase paragraph-start issue fixed; clean normal English sample |
| gemini | topic_04 | n/a | Chinese/non-English anomaly; excluded from English averages |

Model averages after repair:

| Model | Included samples | Average score |
| --- | ---: | ---: |
| gemini | 3 | 31.0 |
| doubao | 4 | 30.5 |
| wenxin | 4 | 30.5 |
| deepseek | 4 | 30.3 |
| Overall normal English set | 15 | 30.5 |

Compared with the earlier English evaluation, the normal-set average rises from 29.3 to 30.5. The gain comes primarily from removing non-English contamination and fixing casing artifacts, not from a new broad rewrite pass.

## Layer 2 Compliance

The batch report remains usable for Layer 2 auditing: edits are recorded as targeted BEFORE/AFTER replacement entries rather than opaque full-document rewrites. Manual spot checks against repaired outputs show that the normal English changes are still consistent with targeted replacements and local cleanup.

No evidence was found of creative large-section rewriting in the normal 15 samples. Article structure, Markdown headings, numeric details, and core claims remain stable.

The remaining Layer 2 weakness is not record completeness but style control: several replacements use plain spaced hyphen punctuation where an em dash was removed. This reduces one detector-like signal but can sound mechanical in finished prose.

## Anomaly: gemini/topic_04.md

`gemini/topic_04.md` remains a non-English anomaly:

- It contains Chinese/non-English mojibake-like content rather than normal English source prose.
- The rewrite is effectively unchanged relative to the source.
- It should not be used to judge English rewrite quality.
- If the English batch must contain 16 valid English samples, this pair needs source-level replacement or regeneration before evaluation.

## Main Changes After Repair

- Normal 15 now pass the explicit repair checks: no Chinese residuals, no Chinese generation notices, and no lowercase paragraph starts.
- The most severe previous hard failures are resolved.
- The effective model ranking shifts upward because doubao and wenxin no longer carry non-English contamination penalties.
- `gemini/topic_04.md` is unchanged as an anomaly and remains outside the English average.

## Remaining Risks

- `wenxin/topic_04.md` still has 5 local watch-list hits after rewrite, the same count as source. It is acceptable but comparatively under-edited.
- Some outputs replace em dashes with spaced hyphens (` - `), which avoids one watch-list pattern but creates slightly mechanical typography.
- A small number of formulaic connective patterns remain in `deepseek/topic_04.md`, `wenxin/topic_02.md`, `wenxin/topic_04.md`, and `gemini/topic_02.md`.
- The offline review cannot predict external detector behavior. External detector status is not run.

## Repair/Go Decision

Broad返工 is not required for the normal English 15. The repaired batch is suitable for the next internal comparison/evaluation step under the offline rubric.

Optional polish before any public-facing use:

- Lightly revise `wenxin/topic_04.md` to reduce remaining transition/cliche hits.
- Normalize spaced hyphen punctuation where sentence flow would read better with a comma, colon, or sentence split.
- Replace or regenerate `gemini/topic_04.md` if a complete 16-sample English batch is required.

## Verification

Performed local-only checks:

- CJK scan across normal 15 rewrites: no matches.
- Chinese generation-note scan across normal 15 rewrites: no matches.
- Case-sensitive lowercase paragraph-start scan across normal 15 rewrites: no matches.
- Offline watch-list counts on all normal English source/rewrite pairs.
- Numeric-token preservation check across all 16 pairs.
- Markdown heading preservation check across all 16 pairs.

No source files, workflow files, templates, rules, or `SKILL.md` files were modified.
