# Chinese Rewrite Evaluation Report - run_20260520 topics 05-08

**Evaluation date:** 2026-05-20
**Evaluator:** Codex Chinese effect evaluation sub-agent
**Scope:** 16 Chinese source/rewrite pairs, topics 05-08 for doubao, deepseek, wenxin, and gemini
**Measurement type:** offline manual rubric + offline rule-hit report review
**External detector status:** not run

## Disclaimer

External detector status: not run. This report does not use or claim GPTZero, Turnitin, CNKI, Wanfang, VIP, PaperPass, or any other external detector result. The numeric scores below are offline manual rubric scores only, using `ai-detection-workflow/meta/rubric/offline_rubric.md`.

No source article or rewritten article was modified during this evaluation. No workflow, template, rule, or SKILL.md file was modified.

## Materials Reviewed

- Source directory: `ai-detection-workflow/meta/provider_articles/run_20260520/<model>/topic_05.md` through `topic_08.md`
- Rewrite directory: `ai-detection-workflow/meta/provider_articles/run_20260520_rewritten_zh/<model>/topic_05.md` through `topic_08.md`
- Batch report: `ai-detection-workflow/meta/provider_articles/run_20260520_rewritten_zh/zh_rewrite_batch_report.md`
- Rubric: `ai-detection-workflow/meta/rubric/offline_rubric.md`
- Chinese rule references: `ai-detection-workflow/rules/zh/ai_cliches.md`, `ai-detection-workflow/rules/zh/sentence_patterns.md`

## Offline Rule-Hit Movement

The batch report's offline rule-hit totals were summed by sample. These are literal repository rule hits, not detector scores.

| Model | Rule hits before | Rule hits after | Delta | Reduction |
|:---|---:|---:|---:|---:|
| doubao | 112 | 40 | -72 | 64.3% |
| deepseek | 47 | 20 | -27 | 57.4% |
| wenxin | 56 | 27 | -29 | 51.8% |
| gemini | 89 | 33 | -56 | 62.9% |
| **Total** | **304** | **120** | **-184** | **60.5%** |

An auxiliary literal count over common terms such as `近年来`, `进行`, `赋能`, `闭环`, `不仅`, `而且`, `因此`, `同时`, `首先`, `其次`, `最后`, `痛点`, `生态`, `打通`, `进一步`, `这一`, `此外`, `然而`, and `随着` showed the same direction: doubao 100 -> 49, deepseek 36 -> 17, wenxin 28 -> 10, gemini 81 -> 36.

## Layer 2 Compliance Check

The batch report contains per-sample exact BEFORE/AFTER replacement tables. Spot checks with `git diff --no-index --word-diff=plain` confirm that the rewrites are composed of local literal substitutions and preserve article structure. No creative paragraph-level rewriting was found in the sampled diffs.

However, the same strict literal strategy caused context-insensitive substitutions. Examples include `一方面` -> `先看` producing `另先看`, `不仅仅` -> `不只仅`, and `生态环境` -> `协作体系环境`. This is not a Layer 2 process violation, but it is a quality and targeting defect: the replacements were exact, yet not always context-safe.

## Per-Sample Rubric Scores

Dimensions: AI signal reduction, naturalness, factual fidelity, genre/register fit, rule-hit targeting, workflow executability, over-rewriting control. Maximum total: 35.

| Sample | AI | Natural | Fidelity | Register | Targeting | Workflow | Overwrite | Total | Verdict |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|:---|
| doubao/topic_05 | 4 | 3 | 4 | 4 | 4 | 5 | 4 | 28 | Usable with light revision |
| doubao/topic_06 | 4 | 4 | 5 | 4 | 4 | 5 | 5 | 31 | Strong |
| doubao/topic_07 | 4 | 3 | 3 | 4 | 4 | 5 | 3 | 26 | Usable with revision |
| doubao/topic_08 | 4 | 4 | 4 | 4 | 4 | 5 | 5 | 30 | Usable/strong boundary |
| deepseek/topic_05 | 4 | 3 | 4 | 4 | 4 | 5 | 3 | 27 | Usable with revision |
| deepseek/topic_06 | 4 | 4 | 5 | 4 | 4 | 5 | 5 | 31 | Strong |
| deepseek/topic_07 | 4 | 4 | 5 | 4 | 4 | 5 | 5 | 31 | Strong |
| deepseek/topic_08 | 3 | 4 | 5 | 4 | 4 | 5 | 5 | 30 | Usable/strong boundary |
| wenxin/topic_05 | 4 | 4 | 4 | 4 | 4 | 5 | 5 | 30 | Usable/strong boundary |
| wenxin/topic_06 | 3 | 2 | 4 | 2 | 3 | 5 | 5 | 24 | Needs revision |
| wenxin/topic_07 | 3 | 2 | 4 | 3 | 3 | 5 | 5 | 25 | Usable only after local repair |
| wenxin/topic_08 | 4 | 4 | 5 | 4 | 4 | 5 | 4 | 30 | Usable/strong boundary |
| gemini/topic_05 | 4 | 3 | 4 | 3 | 4 | 5 | 3 | 26 | Usable with revision |
| gemini/topic_06 | 4 | 4 | 4 | 4 | 4 | 5 | 5 | 30 | Usable/strong boundary |
| gemini/topic_07 | 3 | 2 | 4 | 2 | 3 | 5 | 4 | 25 | Usable only after local repair |
| gemini/topic_08 | 4 | 3 | 4 | 3 | 4 | 5 | 4 | 27 | Usable with revision |

## Model Averages

| Model | Average total | Interpretation |
|:---|---:|:---|
| deepseek | 30.0 | Best overall post-rewrite quality; fewer original signals and fewer serious local damage cases. |
| doubao | 28.8 | Strongest absolute signal reduction, but residual signal count remains high and some substitutions are semantically blunt. |
| wenxin | 27.3 | Good on lighter files, but topic_06 and topic_07 contain clear Chinese sentence damage from `一方面` replacement. |
| gemini | 27.0 | High-yield reduction, but several visible naturalness failures remain in list transitions and `生态` replacements. |

## Qualitative Findings

**AI signal reduction:** The pass materially reduced high-risk lexical signals, especially C-01, C-04, C-09, C-12, C-13, and C-15. Doubao and gemini were easiest to lower because their originals had more formulaic transitions and business-style terms. Residual signals are still visible in long enumerative conclusions, repeated `同时`, `首先/其次/最后` style structures, `进行` padding, and uniform paragraph rhythm.

**Naturalness:** The strongest naturalness issue is context-free substitution. `不只` is acceptable in many contexts, but replacing inside `不仅仅` creates `不只仅`, which is ungrammatical. Replacing `一方面` with `先看` works only in enumerative prose, not in paired contrast structures, where it produced `先看...另先看`. `到最后` is also less formal than the surrounding report style.

**Factual fidelity:** No broad factual fabrication or article-level meaning break was found. Numbers, entities, and topic structures were preserved. Minor semantic drift exists where `生态` became `协作体系` in compounds such as `生态环境`, and where `赋能者` became `提升者`; these are localized meaning/idiom degradations rather than wholesale factual failures.

**Genre/register fit:** Most rewrites remain in Chinese policy/report prose. The replacements `先看`, `再往下`, and `到最后` are too colloquial for several formal report passages, especially gemini/topic_05 and doubao/topic_07.

**Rule-hit targeting:** The pass accurately targeted many literal C-rule hits and reduced counts substantially. It was weaker on S-level patterns: sentence rhythm, list structure, and paragraph-template signals mostly remain. Some targeted replacements reduced counts at the expense of idiomatic Chinese.

**Workflow executability:** The batch report is executable and transparent: paths, exact replacements, counts, disclaimer, and fidelity notes are present. It correctly states external detectors were not run and does not present offline counts as detector scores. Minor issue: the summary text contains placeholder-looking `??` for S-06 phrasing in some places, but it does not block evaluation.

**Over-rewriting control:** Structurally, over-rewriting was well controlled. The edits are narrow and reversible. The main drawback is under-contextualized substitution rather than too much rewriting.

## Model-Level Ranking

**Original easiest to lower:** doubao, then gemini. They had the highest initial offline rule-hit totals and the largest absolute reductions.

**Best post-rewrite quality:** deepseek. Its average quality is highest because fewer edits were needed and most replacements did not damage sentence flow.

**Most residual signal after rewrite:** doubao by absolute residual count, followed by gemini. Wenxin retains fewer total hits but has more obvious local grammar failures in two samples.

## Hard Failures and Quality Failures

Rubric hard-fail flags:

| Flag | Status |
|:---|:---|
| meaning_break | none at article level; localized semantic drift noted |
| fabrication | none found |
| instruction_violation | none found |
| detector_score_claim | none found |
| prompt_or_process_leak | none found |
| language_or_register_mismatch | localized, not whole-sample |
| unusable_output | none found |

Concrete localized failures requiring repair:

| Sample | Issue |
|:---|:---|
| deepseek/topic_05 | `不只仅` appears after replacing inside `不仅仅`; Chinese病句. |
| doubao/topic_05 | `完整流程的响应机制`, `合作协作体系`, and `数据的提升作用` are stiff or semantically weaker. |
| doubao/topic_07 | `赋能者` -> `提升者` weakens the role label; `到最后` is register-inappropriate. |
| wenxin/topic_06 | `先看...另先看` is an obvious Chinese sentence failure. |
| wenxin/topic_07 | `先看...另先看` and `激励与惩戒完整流程` are unnatural. |
| gemini/topic_05 | `先看`, `再往下`, `到最后` read too colloquial in a formal closing list. |
| gemini/topic_07 | `先看...另先看` is an obvious Chinese sentence failure. |
| gemini/topic_08 | `协作体系环境` is an unnatural replacement for `生态环境`. |

No encoding corruption was found in the actual source/rewrite UTF-8 files checked. Earlier mojibake was terminal-output related when PowerShell encoding was not set.

## Recommendations

The Chinese batch should receive a small repair pass before being treated as final. The repair pass should not broaden into creative rewriting; it should add context guards and exact fixes for known bad outputs:

- Do not replace `不仅` inside `不仅仅`; handle the longer phrase first or skip it.
- Do not replace `一方面` blindly when paired with `另一方面`; use a pair-safe replacement or leave it.
- Do not replace `生态` inside `生态环境`, `生态系统`, or other fixed compounds.
- Avoid `先看`, `再往下`, and `到最后` in formal reports unless the surrounding register is already conversational.
- Treat `赋能者`, `数据赋能`, and similar compounds with term-specific alternatives rather than generic `提升`.

After these localized Chinese repairs, the workflow can proceed to the English four-piece stage. The English stage should carry forward the main lesson from this run: exact replacements are operationally clean, but the replacement plan needs phrase-boundary and compound-word guards before execution.
