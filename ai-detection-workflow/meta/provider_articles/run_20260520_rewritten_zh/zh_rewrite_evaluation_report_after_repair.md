# Chinese Rewrite Re-Evaluation Report After Repair - run_20260520 topics 05-08

**Evaluation date:** 2026-05-20
**Evaluator:** Codex Chinese effect evaluation sub-agent
**Scope:** 16 repaired Chinese source/rewrite pairs, topics 05-08 for doubao, deepseek, wenxin, and gemini
**Measurement type:** offline manual rubric + offline literal rule/watch-list statistics
**External detector status:** not run

## Disclaimer

External detector status: not run. This report uses only offline manual review, the project offline rubric, local file diffs, and literal rule/watch-list counts. It does not use or claim GPTZero, Turnitin, CNKI, Wanfang, VIP, PaperPass, or any other external detector result.

No source article was modified during this re-evaluation. No workflow, template, rule, or SKILL.md file was modified.

## Inputs

- Source directory: `ai-detection-workflow/meta/provider_articles/run_20260520/<model>/topic_05.md` through `topic_08.md`
- Repaired rewrite directory: `ai-detection-workflow/meta/provider_articles/run_20260520_rewritten_zh/<model>/topic_05.md` through `topic_08.md`
- Prior batch report: `ai-detection-workflow/meta/provider_articles/run_20260520_rewritten_zh/zh_rewrite_batch_report.md`
- Prior evaluation: `ai-detection-workflow/meta/provider_articles/run_20260520_rewritten_zh/zh_rewrite_evaluation_report.md`
- Rubric: `ai-detection-workflow/meta/rubric/offline_rubric.md`

## Repair Verification

The requested hard-failure strings were searched across all repaired rewrite files. No matches were found for:

| Checked string | Status |
|:---|:---|
| `不只仅` | absent |
| `先看` | absent |
| `另先看` | absent |
| `协作体系环境` | absent |
| `完整流程的响应机制` | absent |
| `合作协作体系` | absent |
| `数据的提升作用` | absent |
| `提升者` | absent |
| `到最后` | absent |
| `再往下` | absent |
| `激励与惩戒完整流程` | absent |

Spot-check diffs confirm the repair pass was localized. Examples: wenxin/topic_06 no longer rewrites `一方面...另一方面` into `先看...另先看`; gemini/topic_05 restored formal sequence markers where the prior rewrite used `先看`, `再往下`, and `到最后`; gemini/topic_08 restored `生态环境` where the prior rewrite produced `协作体系环境`.

## Offline Watch-List Movement

The following table uses a local literal watch-list derived from the project Chinese rules and the prior failure list: `近年来`, `总体而言`, `需要注意的是`, `通过这种方式`, `进行`, `赋能`, `抓手`, `闭环`, `不仅`, `而且`, `因此`, `同时`, `首先`, `其次`, `最后`, `痛点`, `生态`, `打通`, `进一步`, `这一`, `此外`, `然而`, `随着`, `一方面`, `另一方面`, `不只`, `由此看`, `先看`, `再往下`, `到最后`, `完整流程`.

These counts are offline literal hits only; they are not detector scores.

| Model | Source hits | Repaired rewrite hits | Delta | Reduction |
|:---|---:|---:|---:|---:|
| doubao | 100 | 61 | -39 | 39.0% |
| deepseek | 36 | 23 | -13 | 36.1% |
| wenxin | 34 | 19 | -15 | 44.1% |
| gemini | 84 | 56 | -28 | 33.3% |
| **Total** | **254** | **159** | **-95** | **37.4%** |

Interpretation: the repaired set intentionally gives back some lexical reductions to remove ungrammatical or register-breaking replacements. The AI-signal drop is therefore smaller than the pre-repair batch report, but the repaired outputs are more usable and more faithful.

## Per-Sample Rubric Scores

Dimensions: AI signal reduction, readability/naturalness, technical/factual fidelity, genre/register fit, rule-hit targeting accuracy, workflow executability, over-rewriting control. Maximum total: 35.

| Sample | AI | Natural | Fidelity | Register | Targeting | Workflow | Overwrite | Total | Change vs prior |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|:---|
| doubao/topic_05 | 4 | 4 | 4 | 4 | 4 | 5 | 5 | 30 | +2 |
| doubao/topic_06 | 4 | 4 | 5 | 4 | 4 | 5 | 5 | 31 | 0 |
| doubao/topic_07 | 4 | 4 | 4 | 4 | 4 | 5 | 4 | 29 | +3 |
| doubao/topic_08 | 4 | 4 | 4 | 4 | 4 | 5 | 5 | 30 | 0 |
| deepseek/topic_05 | 4 | 4 | 4 | 4 | 4 | 5 | 5 | 30 | +3 |
| deepseek/topic_06 | 4 | 4 | 5 | 4 | 4 | 5 | 5 | 31 | 0 |
| deepseek/topic_07 | 4 | 4 | 5 | 4 | 4 | 5 | 5 | 31 | 0 |
| deepseek/topic_08 | 3 | 4 | 5 | 4 | 4 | 5 | 5 | 30 | 0 |
| wenxin/topic_05 | 4 | 4 | 4 | 4 | 4 | 5 | 5 | 30 | 0 |
| wenxin/topic_06 | 4 | 4 | 5 | 4 | 4 | 5 | 5 | 31 | +7 |
| wenxin/topic_07 | 3 | 4 | 5 | 4 | 3 | 5 | 5 | 29 | +4 |
| wenxin/topic_08 | 4 | 4 | 5 | 4 | 4 | 5 | 4 | 30 | 0 |
| gemini/topic_05 | 4 | 4 | 4 | 4 | 4 | 5 | 4 | 29 | +3 |
| gemini/topic_06 | 4 | 4 | 4 | 4 | 4 | 5 | 5 | 30 | 0 |
| gemini/topic_07 | 3 | 4 | 4 | 4 | 3 | 5 | 5 | 28 | +3 |
| gemini/topic_08 | 4 | 3 | 4 | 3 | 4 | 5 | 5 | 28 | +1 |

## Model Averages

| Model | Prior average | After-repair average | Change | Interpretation |
|:---|---:|---:|---:|:---|
| deepseek | 30.0 | 30.5 | +0.5 | Best overall after repair; fewest visible quality defects. |
| doubao | 28.8 | 30.0 | +1.2 | Signal reduction remains good; local semantic bluntness mostly reduced. |
| wenxin | 27.3 | 30.0 | +2.7 | Largest improvement because the `先看/另先看` failures were removed. |
| gemini | 27.0 | 28.8 | +1.8 | Improved substantially, though topic_08 still has some stiff replacements. |
| **Overall** | **28.3** | **29.8** | **+1.5** | Repaired set is now generally usable with light review. |

## Main Changes Since Prior Evaluation

- The hard Chinese病句 and register breaks identified in the prior report are gone.
- Layer 2 discipline still appears intact: sampled diffs show local replacements and localized repairs, not creative paragraph-level rewrites.
- Naturalness improved most in wenxin/topic_06, wenxin/topic_07, gemini/topic_05, and gemini/topic_07.
- The offline watch-list reduction is now less aggressive because some high-risk but contextually necessary terms were restored. This is the right tradeoff for fidelity and readability.
- No external detector was run, and no offline score is presented as an external detector score.

## Remaining Risks

No rubric hard-fail flags remain at the article level.

Residual quality risks:

- `不只` remains in several places. It is grammatical, but in formal report prose `不仅` is often more natural; avoid replacing every occurrence mechanically.
- `完整流程` still appears in some contexts where `闭环`, `全流程`, or a more concrete phrase may be more idiomatic, for example gemini/topic_08 title `信任的完整流程`.
- `协作体系` remains acceptable in some governance contexts, but it can still be semantically broader or flatter than `生态` when the source means market ecology or platform ecology.
- Some S-level AI signals remain: list-like conclusions, repeated formal paragraph structure, and uniform report rhythm. The repair pass addressed lexical hard failures more than sentence/paragraph patterning.
- Residual offline signals are highest in doubao and gemini by the current watch-list count, though their readability is now better than before repair.

## Recommendation

The repaired Chinese topic_05-08 set can proceed to the next stage, including the planned English four-piece work, with one caveat: treat the current Chinese output as "usable with light final review," not as a detector-verified final. The next rewrite strategy should keep exact replacement discipline but add phrase-boundary guards and compound-word exceptions before execution, especially for `不仅`, `一方面/另一方面`, `生态`, `赋能`, and `闭环`.
