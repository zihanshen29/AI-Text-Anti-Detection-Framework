# Chinese Context Whitelist - P0.4

> Consumed by Layer 0 during Chinese discovery and by Layer 1 during planning.
> Layer 2 must not read this file directly; it only executes exact BEFORE/AFTER pairs already approved in `plan.md`.

## Purpose

Chinese trigger words are not always AI signals. Some are legitimate inside fixed terms, technical terms, paired structures, or genre-specific phrases. This whitelist prevents substring-level replacements such as `生态环境` -> `协作体系环境` and `不仅仅` -> `不只仅`.

Layer 0 uses this file to mark obvious fixed-context matches as `whitelisted: true` so they do not enter Layer 1 as mechanical fixes. Layer 1 uses it again as a defensive check for ambiguous contexts.

## Required Output Statuses

- `whitelisted: true`: fixed or technical context; do not plan a replacement.
- `whitelisted: review`: context is ambiguous or genre-dependent; Layer 1 may propose a fix only after reading the sentence.
- `checked, no whitelist match`: normal candidate hit; Layer 1 may plan a replacement.

## Mandatory Whitelist Table

| Trigger | Rule family | Do not replace when context matches | Notes |
|:---|:---|:---|:---|
| `生态` | C-04 | `生态环境`, `生态系统`, `生态保护`, `市场生态`, `平台生态` | Fixed or semi-fixed compounds. Replace only when the word is vague business filler. |
| `闭环` | C-04 | `控制闭环`, `闭环控制` | Technical control-theory terms are not internet jargon. `业务闭环` is genre-dependent. |
| `赋能` | C-04 | `数字赋能`, `技术赋能`, `数据赋能` in business/report genres | `赋能教师` or `赋能学生` usually needs phrase-level semantic redesign, not a one-word synonym. |
| `痛点` | C-04 | `用户痛点`, `行业痛点`, `业务痛点` when tied to concrete evidence | Keep concrete analytical uses; replace slogan-like uses. |
| `不仅` | C-09 | `不仅仅`, `不仅如此` | Never substring-replace inside these longer phrases. |
| `不仅...而且` | C-09 | paired contrast structures that carry real logic | Rewrite the whole pair or leave it; never edit one side only. |
| `一方面` | C-09 / S-12 | `一方面...另一方面` | Treat as one paired structure. Do not create `先看...另先看`. |
| `同时` | C-12 / S-13 | `与此同时`, `同时进行`, literal simultaneity | Flag discourse-marker density, not normal time/adverbial use. |
| `进行` | S-06 | `进行得很顺利`, `正在进行`, literal progress/process use | Only flag padded verb patterns such as `对 X 进行 Y`. |
| `化` suffix | C-05 | `数字化转型`, `自动化控制`, `信息化建设`, `标准化接口`, `智能化调度` | Accepted domain terms. Flag vague suffix stacking or density, not every suffix. |

## Layer 0 Procedure

1. When a Chinese C-NN or S-NN trigger is found, inspect the shortest containing phrase first, then the full sentence.
2. If the phrase exactly matches this table, record it in `discovery.md` as `whitelisted: true`.
3. If the phrase is close to a whitelist form but genre-dependent, record `whitelisted: review`.
4. Only `checked, no whitelist match` hits become Layer 1 candidate fixes.

## Layer 1 Procedure

Before writing any BEFORE/AFTER pair for a Chinese C-NN or S-NN hit:

1. Re-check the BEFORE string against this table.
2. If the BEFORE string contains a whitelist context, drop the mechanical fix or move it to Open Questions.
3. If the trigger is part of a paired structure, write one exact pair-level fix or leave the pair unchanged.
4. Do not use substring replacements for Chinese triggers unless the surrounding phrase was explicitly checked.

## Expansion Rule

When a batch evaluation finds a new context-sensitive failure, add the failed trigger and safe context here before adding more replacement candidates to `ai_cliches.md` or `sentence_patterns.md`.
