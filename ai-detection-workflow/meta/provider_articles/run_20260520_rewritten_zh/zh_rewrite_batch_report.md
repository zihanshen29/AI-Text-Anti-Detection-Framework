# Chinese Rewrite Batch Report - run_20260520 topics 05-08

**Run date:** 2026-05-20
**Evaluator agent:** Codex Chinese rewrite sub-agent
**Number of samples:** 16
**Measurement type:** offline_rule_hits
**External detector status:** not run

## Disclaimer

External detector status: not run. This batch used only offline rule-hit counts from the repository rule vocabulary. No GPTZero, Turnitin, CNKI, Wanfang, VIP, PaperPass, or other external detector was run, and this report does not claim any real detector score reduction.

All rewrites were produced under strict Layer 2 discipline. Each edit is an exact literal BEFORE/AFTER string replacement listed in the per-sample condensed plan. No creative paragraph-level rewriting was performed.

## Per-sample results

### Sample 1 - doubao/topic_05.md

- **Source path:** `ai-detection-workflow\meta\provider_articles\run_20260520\doubao\topic_05.md`
- **Rewritten path:** `ai-detection-workflow\meta\provider_articles\run_20260520_rewritten_zh\doubao\topic_05.md`
- **Language:** zh
- **Genre:** provider-generated Chinese long-form article
- **Approximate length:** 3116 characters
- **Encoding preflight:** UTF-8 read/write confirmed, mojibake scan pass

**Condensed plan (the exact fix list applied to this sample):**

| Fix ID | Rule | Tier | BEFORE | AFTER | Occurrences |
|:---|:---|:---:|:---|:---|---:|
| 1 | C-02 | A | 近年来， | 近几年， | 1 |
| 2 | C-01 | A | 此外， | 另外， | 1 |
| 3 | C-09 | A | 不仅 | 不只 | 2 |
| 4 | C-04 | A | 赋能 | 提升 | 1 |
| 5 | C-04 | A | 痛点 | 难点 | 1 |
| 6 | C-04 | A | 闭环 | 完整流程 | 1 |
| 7 | C-04 | A | 生态 | 协作体系 | 2 |
| 8 | C-04 | A | 打通 | 连通 | 2 |
| 9 | C-13 | A | 日益 | 逐渐 | 1 |
| 10 | C-13 | A | 进一步 | 继续 | 1 |
| 11 | C-15 | A | 这一 | 这个 | 3 |

**Rule hits before -> after (offline count):**

| Rule | Before | After | Delta |
|:---|---:|---:|---:|
| C-01 | 1 | 0 | -1 |
| C-02 | 2 | 1 | -1 |
| C-03 | 1 | 1 | 0 |
| C-04 | 7 | 0 | -7 |
| C-08 | 6 | 6 | 0 |
| C-09 | 8 | 6 | -2 |
| C-12 | 1 | 0 | -1 |
| C-13 | 2 | 0 | -2 |
| C-15 | 3 | 0 | -3 |
| S-06 | 2 | 2 | 0 |

**Offline rule hits summary:** Applied a light visible cleanup pass focused on C-class clich?s and S-06 `??` phrasing. Residual signals remain where removing more terms could harm facts, enumerations, or normal Chinese transitions: C-02=1, C-03=1, C-08=6, C-09=6, S-06=2.

**Fidelity verdict:** pass
- Numbers preserved: yes
- Technical terms preserved: yes
- Proper nouns preserved: yes
- Residual signal note: further edits should be planned separately if a stricter detector target is supplied.

### Sample 2 - doubao/topic_06.md

- **Source path:** `ai-detection-workflow\meta\provider_articles\run_20260520\doubao\topic_06.md`
- **Rewritten path:** `ai-detection-workflow\meta\provider_articles\run_20260520_rewritten_zh\doubao\topic_06.md`
- **Language:** zh
- **Genre:** provider-generated Chinese long-form article
- **Approximate length:** 2819 characters
- **Encoding preflight:** UTF-8 read/write confirmed, mojibake scan pass

**Condensed plan (the exact fix list applied to this sample):**

| Fix ID | Rule | Tier | BEFORE | AFTER | Occurrences |
|:---|:---|:---:|:---|:---|---:|
| 1 | C-01 | A | 综上所述， | 由此看， | 1 |
| 2 | C-01 | A | 此外， | 另外， | 2 |
| 3 | C-04 | A | 闭环 | 完整流程 | 1 |
| 4 | C-13 | A | 日益 | 逐渐 | 1 |
| 5 | C-13 | A | 愈发 | 更 | 1 |

**Rule hits before -> after (offline count):**

| Rule | Before | After | Delta |
|:---|---:|---:|---:|
| C-01 | 3 | 0 | -3 |
| C-02 | 1 | 1 | 0 |
| C-04 | 1 | 0 | -1 |
| C-12 | 2 | 0 | -2 |
| C-13 | 2 | 0 | -2 |
| S-06 | 1 | 1 | 0 |

**Offline rule hits summary:** Applied a light visible cleanup pass focused on C-class clich?s and S-06 `??` phrasing. Residual signals remain where removing more terms could harm facts, enumerations, or normal Chinese transitions: C-02=1, S-06=1.

**Fidelity verdict:** pass
- Numbers preserved: yes
- Technical terms preserved: yes
- Proper nouns preserved: yes
- Residual signal note: further edits should be planned separately if a stricter detector target is supplied.

### Sample 3 - doubao/topic_07.md

- **Source path:** `ai-detection-workflow\meta\provider_articles\run_20260520\doubao\topic_07.md`
- **Rewritten path:** `ai-detection-workflow\meta\provider_articles\run_20260520_rewritten_zh\doubao\topic_07.md`
- **Language:** zh
- **Genre:** provider-generated Chinese long-form article
- **Approximate length:** 2923 characters
- **Encoding preflight:** UTF-8 read/write confirmed, mojibake scan pass

**Condensed plan (the exact fix list applied to this sample):**

| Fix ID | Rule | Tier | BEFORE | AFTER | Occurrences |
|:---|:---|:---:|:---|:---|---:|
| 1 | C-01 | A | 与此同时， | 同时， | 2 |
| 2 | C-01 | A | 此外， | 另外， | 1 |
| 3 | C-12 | A | 然而， | 但 | 1 |
| 4 | C-09 | A | 不仅 | 不只 | 4 |
| 5 | C-08 | A | 首先， | 先看， | 1 |
| 6 | C-08 | A | 其次， | 接着， | 1 |
| 7 | C-08 | A | 最后， | 到最后， | 1 |
| 8 | C-04 | A | 赋能 | 提升 | 2 |
| 9 | C-04 | A | 痛点 | 难点 | 2 |
| 10 | C-13 | A | 进一步 | 继续 | 1 |
| 11 | S-06 | A | 进行沟通 | 沟通 | 1 |

**Rule hits before -> after (offline count):**

| Rule | Before | After | Delta |
|:---|---:|---:|---:|
| C-01 | 3 | 0 | -3 |
| C-02 | 1 | 1 | 0 |
| C-04 | 4 | 0 | -4 |
| C-08 | 4 | 2 | -2 |
| C-09 | 12 | 8 | -4 |
| C-12 | 4 | 0 | -4 |
| C-13 | 1 | 0 | -1 |
| S-06 | 5 | 4 | -1 |

**Offline rule hits summary:** Applied a light visible cleanup pass focused on C-class clich?s and S-06 `??` phrasing. Residual signals remain where removing more terms could harm facts, enumerations, or normal Chinese transitions: C-02=1, C-08=2, C-09=8, S-06=4.

**Fidelity verdict:** pass
- Numbers preserved: yes
- Technical terms preserved: yes
- Proper nouns preserved: yes
- Residual signal note: further edits should be planned separately if a stricter detector target is supplied.

### Sample 4 - doubao/topic_08.md

- **Source path:** `ai-detection-workflow\meta\provider_articles\run_20260520\doubao\topic_08.md`
- **Rewritten path:** `ai-detection-workflow\meta\provider_articles\run_20260520_rewritten_zh\doubao\topic_08.md`
- **Language:** zh
- **Genre:** provider-generated Chinese long-form article
- **Approximate length:** 3665 characters
- **Encoding preflight:** UTF-8 read/write confirmed, mojibake scan pass

**Condensed plan (the exact fix list applied to this sample):**

| Fix ID | Rule | Tier | BEFORE | AFTER | Occurrences |
|:---|:---|:---:|:---|:---|---:|
| 1 | C-02 | A | 近年来， | 近几年， | 1 |
| 2 | C-01 | A | 此外， | 另外， | 8 |
| 3 | C-09 | A | 不仅 | 不只 | 3 |
| 4 | C-04 | A | 痛点 | 难点 | 4 |
| 5 | C-13 | A | 日益 | 逐渐 | 1 |
| 6 | C-13 | A | 进一步 | 继续 | 3 |

**Rule hits before -> after (offline count):**

| Rule | Before | After | Delta |
|:---|---:|---:|---:|
| C-01 | 8 | 0 | -8 |
| C-02 | 3 | 2 | -1 |
| C-04 | 4 | 0 | -4 |
| C-08 | 1 | 1 | 0 |
| C-09 | 6 | 3 | -3 |
| C-12 | 8 | 0 | -8 |
| C-13 | 4 | 0 | -4 |
| S-06 | 1 | 1 | 0 |

**Offline rule hits summary:** Applied a light visible cleanup pass focused on C-class clich?s and S-06 `??` phrasing. Residual signals remain where removing more terms could harm facts, enumerations, or normal Chinese transitions: C-02=2, C-08=1, C-09=3, S-06=1.

**Fidelity verdict:** pass
- Numbers preserved: yes
- Technical terms preserved: yes
- Proper nouns preserved: yes
- Residual signal note: further edits should be planned separately if a stricter detector target is supplied.

### Sample 5 - deepseek/topic_05.md

- **Source path:** `ai-detection-workflow\meta\provider_articles\run_20260520\deepseek\topic_05.md`
- **Rewritten path:** `ai-detection-workflow\meta\provider_articles\run_20260520_rewritten_zh\deepseek\topic_05.md`
- **Language:** zh
- **Genre:** provider-generated Chinese long-form article
- **Approximate length:** 2811 characters
- **Encoding preflight:** UTF-8 read/write confirmed, mojibake scan pass

**Condensed plan (the exact fix list applied to this sample):**

| Fix ID | Rule | Tier | BEFORE | AFTER | Occurrences |
|:---|:---|:---:|:---|:---|---:|
| 1 | C-01 | A | 与此同时， | 同时， | 1 |
| 2 | C-12 | A | 然而， | 但 | 1 |
| 3 | C-09 | A | 不仅 | 不只 | 3 |
| 4 | C-04 | A | 生态 | 协作体系 | 1 |
| 5 | C-04 | A | 打通 | 连通 | 3 |
| 6 | C-13 | A | 进一步 | 继续 | 1 |
| 7 | C-03 | A | 十分 | 很 | 1 |
| 8 | C-15 | A | 这一 | 这个 | 1 |

**Rule hits before -> after (offline count):**

| Rule | Before | After | Delta |
|:---|---:|---:|---:|
| C-01 | 1 | 0 | -1 |
| C-02 | 1 | 1 | 0 |
| C-03 | 1 | 0 | -1 |
| C-04 | 4 | 0 | -4 |
| C-08 | 3 | 3 | 0 |
| C-09 | 10 | 7 | -3 |
| C-12 | 2 | 0 | -2 |
| C-13 | 1 | 0 | -1 |
| C-15 | 1 | 0 | -1 |

**Offline rule hits summary:** Applied a light visible cleanup pass focused on C-class clich?s and S-06 `??` phrasing. Residual signals remain where removing more terms could harm facts, enumerations, or normal Chinese transitions: C-02=1, C-08=3, C-09=7.

**Fidelity verdict:** pass
- Numbers preserved: yes
- Technical terms preserved: yes
- Proper nouns preserved: yes
- Residual signal note: further edits should be planned separately if a stricter detector target is supplied.

### Sample 6 - deepseek/topic_06.md

- **Source path:** `ai-detection-workflow\meta\provider_articles\run_20260520\deepseek\topic_06.md`
- **Rewritten path:** `ai-detection-workflow\meta\provider_articles\run_20260520_rewritten_zh\deepseek\topic_06.md`
- **Language:** zh
- **Genre:** provider-generated Chinese long-form article
- **Approximate length:** 2922 characters
- **Encoding preflight:** UTF-8 read/write confirmed, mojibake scan pass

**Condensed plan (the exact fix list applied to this sample):**

| Fix ID | Rule | Tier | BEFORE | AFTER | Occurrences |
|:---|:---|:---:|:---|:---|---:|
| 1 | C-02 | A | 近年来， | 近几年， | 1 |
| 2 | C-09 | A | 不仅 | 不只 | 1 |
| 3 | C-15 | A | 这一 | 这个 | 1 |

**Rule hits before -> after (offline count):**

| Rule | Before | After | Delta |
|:---|---:|---:|---:|
| C-02 | 1 | 0 | -1 |
| C-08 | 2 | 2 | 0 |
| C-09 | 2 | 1 | -1 |
| C-15 | 1 | 0 | -1 |
| S-06 | 1 | 1 | 0 |

**Offline rule hits summary:** Applied a light visible cleanup pass focused on C-class clich?s and S-06 `??` phrasing. Residual signals remain where removing more terms could harm facts, enumerations, or normal Chinese transitions: C-08=2, C-09=1, S-06=1.

**Fidelity verdict:** pass
- Numbers preserved: yes
- Technical terms preserved: yes
- Proper nouns preserved: yes
- Residual signal note: further edits should be planned separately if a stricter detector target is supplied.

### Sample 7 - deepseek/topic_07.md

- **Source path:** `ai-detection-workflow\meta\provider_articles\run_20260520\deepseek\topic_07.md`
- **Rewritten path:** `ai-detection-workflow\meta\provider_articles\run_20260520_rewritten_zh\deepseek\topic_07.md`
- **Language:** zh
- **Genre:** provider-generated Chinese long-form article
- **Approximate length:** 2765 characters
- **Encoding preflight:** UTF-8 read/write confirmed, mojibake scan pass

**Condensed plan (the exact fix list applied to this sample):**

| Fix ID | Rule | Tier | BEFORE | AFTER | Occurrences |
|:---|:---|:---:|:---|:---|---:|
| 1 | C-01 | A | 与此同时， | 同时， | 2 |
| 2 | C-04 | A | 痛点 | 难点 | 1 |
| 3 | C-04 | A | 闭环 | 完整流程 | 1 |
| 4 | C-13 | A | 日益 | 逐渐 | 1 |
| 5 | C-13 | A | 进一步 | 继续 | 2 |

**Rule hits before -> after (offline count):**

| Rule | Before | After | Delta |
|:---|---:|---:|---:|
| C-01 | 2 | 0 | -2 |
| C-04 | 2 | 0 | -2 |
| C-08 | 1 | 1 | 0 |
| C-09 | 2 | 2 | 0 |
| C-12 | 2 | 0 | -2 |
| C-13 | 3 | 0 | -3 |

**Offline rule hits summary:** Applied a light visible cleanup pass focused on C-class clich?s and S-06 `??` phrasing. Residual signals remain where removing more terms could harm facts, enumerations, or normal Chinese transitions: C-08=1, C-09=2.

**Fidelity verdict:** pass
- Numbers preserved: yes
- Technical terms preserved: yes
- Proper nouns preserved: yes
- Residual signal note: further edits should be planned separately if a stricter detector target is supplied.

### Sample 8 - deepseek/topic_08.md

- **Source path:** `ai-detection-workflow\meta\provider_articles\run_20260520\deepseek\topic_08.md`
- **Rewritten path:** `ai-detection-workflow\meta\provider_articles\run_20260520_rewritten_zh\deepseek\topic_08.md`
- **Language:** zh
- **Genre:** provider-generated Chinese long-form article
- **Approximate length:** 2248 characters
- **Encoding preflight:** UTF-8 read/write confirmed, mojibake scan pass

**Condensed plan (the exact fix list applied to this sample):**

| Fix ID | Rule | Tier | BEFORE | AFTER | Occurrences |
|:---|:---|:---:|:---|:---|---:|
| 1 | C-12 | A | 然而， | 但 | 1 |
| 2 | C-04 | A | 闭环 | 完整流程 | 1 |

**Rule hits before -> after (offline count):**

| Rule | Before | After | Delta |
|:---|---:|---:|---:|
| C-03 | 1 | 1 | 0 |
| C-04 | 1 | 0 | -1 |
| C-12 | 1 | 0 | -1 |
| S-06 | 1 | 1 | 0 |

**Offline rule hits summary:** Applied a light visible cleanup pass focused on C-class clich?s and S-06 `??` phrasing. Residual signals remain where removing more terms could harm facts, enumerations, or normal Chinese transitions: C-03=1, S-06=1.

**Fidelity verdict:** pass
- Numbers preserved: yes
- Technical terms preserved: yes
- Proper nouns preserved: yes
- Residual signal note: further edits should be planned separately if a stricter detector target is supplied.

### Sample 9 - wenxin/topic_05.md

- **Source path:** `ai-detection-workflow\meta\provider_articles\run_20260520\wenxin\topic_05.md`
- **Rewritten path:** `ai-detection-workflow\meta\provider_articles\run_20260520_rewritten_zh\wenxin\topic_05.md`
- **Language:** zh
- **Genre:** provider-generated Chinese long-form article
- **Approximate length:** 1804 characters
- **Encoding preflight:** UTF-8 read/write confirmed, mojibake scan pass

**Condensed plan (the exact fix list applied to this sample):**

| Fix ID | Rule | Tier | BEFORE | AFTER | Occurrences |
|:---|:---|:---:|:---|:---|---:|
| 1 | C-02 | A | 近年来， | 近几年， | 1 |
| 2 | C-01 | A | 此外， | 另外， | 1 |
| 3 | C-04 | A | 形成闭环 | 形成完整流程 | 1 |
| 4 | C-04 | A | 打通 | 连通 | 2 |
| 5 | C-13 | A | 进一步 | 继续 | 1 |
| 6 | C-15 | A | 这一 | 这个 | 3 |

**Rule hits before -> after (offline count):**

| Rule | Before | After | Delta |
|:---|---:|---:|---:|
| C-01 | 1 | 0 | -1 |
| C-02 | 2 | 1 | -1 |
| C-04 | 4 | 0 | -4 |
| C-09 | 1 | 1 | 0 |
| C-12 | 2 | 1 | -1 |
| C-13 | 1 | 0 | -1 |
| C-15 | 3 | 0 | -3 |
| S-06 | 1 | 1 | 0 |

**Offline rule hits summary:** Applied a light visible cleanup pass focused on C-class clich?s and S-06 `??` phrasing. Residual signals remain where removing more terms could harm facts, enumerations, or normal Chinese transitions: C-02=1, C-09=1, C-12=1, S-06=1.

**Fidelity verdict:** pass
- Numbers preserved: yes
- Technical terms preserved: yes
- Proper nouns preserved: yes
- Residual signal note: further edits should be planned separately if a stricter detector target is supplied.

### Sample 10 - wenxin/topic_06.md

- **Source path:** `ai-detection-workflow\meta\provider_articles\run_20260520\wenxin\topic_06.md`
- **Rewritten path:** `ai-detection-workflow\meta\provider_articles\run_20260520_rewritten_zh\wenxin\topic_06.md`
- **Language:** zh
- **Genre:** provider-generated Chinese long-form article
- **Approximate length:** 2336 characters
- **Encoding preflight:** UTF-8 read/write confirmed, mojibake scan pass

**Condensed plan (the exact fix list applied to this sample):**

| Fix ID | Rule | Tier | BEFORE | AFTER | Occurrences |
|:---|:---|:---:|:---|:---|---:|
| 1 | C-01 | A | 此外， | 另外， | 1 |
| 2 | C-09 | A | 不仅 | 不只 | 1 |
| 3 | C-09 | A | 一方面， | 先看， | 2 |
| 4 | C-15 | A | 这一 | 这个 | 1 |

**Rule hits before -> after (offline count):**

| Rule | Before | After | Delta |
|:---|---:|---:|---:|
| C-01 | 1 | 0 | -1 |
| C-03 | 1 | 1 | 0 |
| C-08 | 8 | 8 | 0 |
| C-09 | 4 | 0 | -4 |
| C-12 | 1 | 0 | -1 |
| C-15 | 1 | 0 | -1 |
| S-06 | 1 | 1 | 0 |

**Offline rule hits summary:** Applied a light visible cleanup pass focused on C-class clich?s and S-06 `??` phrasing. Residual signals remain where removing more terms could harm facts, enumerations, or normal Chinese transitions: C-03=1, C-08=8, S-06=1.

**Fidelity verdict:** pass
- Numbers preserved: yes
- Technical terms preserved: yes
- Proper nouns preserved: yes
- Residual signal note: further edits should be planned separately if a stricter detector target is supplied.

### Sample 11 - wenxin/topic_07.md

- **Source path:** `ai-detection-workflow\meta\provider_articles\run_20260520\wenxin\topic_07.md`
- **Rewritten path:** `ai-detection-workflow\meta\provider_articles\run_20260520_rewritten_zh\wenxin\topic_07.md`
- **Language:** zh
- **Genre:** provider-generated Chinese long-form article
- **Approximate length:** 2125 characters
- **Encoding preflight:** UTF-8 read/write confirmed, mojibake scan pass

**Condensed plan (the exact fix list applied to this sample):**

| Fix ID | Rule | Tier | BEFORE | AFTER | Occurrences |
|:---|:---|:---:|:---|:---|---:|
| 1 | C-09 | A | 一方面， | 先看， | 2 |
| 2 | C-04 | A | 闭环 | 完整流程 | 1 |

**Rule hits before -> after (offline count):**

| Rule | Before | After | Delta |
|:---|---:|---:|---:|
| C-03 | 2 | 2 | 0 |
| C-04 | 1 | 0 | -1 |
| C-08 | 3 | 3 | 0 |
| C-09 | 3 | 0 | -3 |
| C-13 | 1 | 1 | 0 |

**Offline rule hits summary:** Applied a light visible cleanup pass focused on C-class clich?s and S-06 `??` phrasing. Residual signals remain where removing more terms could harm facts, enumerations, or normal Chinese transitions: C-03=2, C-08=3, C-13=1.

**Fidelity verdict:** pass
- Numbers preserved: yes
- Technical terms preserved: yes
- Proper nouns preserved: yes
- Residual signal note: further edits should be planned separately if a stricter detector target is supplied.

### Sample 12 - wenxin/topic_08.md

- **Source path:** `ai-detection-workflow\meta\provider_articles\run_20260520\wenxin\topic_08.md`
- **Rewritten path:** `ai-detection-workflow\meta\provider_articles\run_20260520_rewritten_zh\wenxin\topic_08.md`
- **Language:** zh
- **Genre:** provider-generated Chinese long-form article
- **Approximate length:** 2487 characters
- **Encoding preflight:** UTF-8 read/write confirmed, mojibake scan pass

**Condensed plan (the exact fix list applied to this sample):**

| Fix ID | Rule | Tier | BEFORE | AFTER | Occurrences |
|:---|:---|:---:|:---|:---|---:|
| 1 | C-09 | A | 而且 | 也 | 1 |
| 2 | C-04 | A | 闭环 | 完整流程 | 1 |
| 3 | C-13 | A | 日益 | 逐渐 | 1 |
| 4 | C-13 | A | 进一步 | 继续 | 1 |
| 5 | C-03 | A | 特别是 | 尤其是 | 1 |
| 6 | C-15 | A | 这一 | 这个 | 2 |

**Rule hits before -> after (offline count):**

| Rule | Before | After | Delta |
|:---|---:|---:|---:|
| C-03 | 1 | 0 | -1 |
| C-04 | 1 | 0 | -1 |
| C-08 | 7 | 7 | 0 |
| C-09 | 1 | 0 | -1 |
| C-13 | 2 | 0 | -2 |
| C-15 | 2 | 0 | -2 |

**Offline rule hits summary:** Applied a light visible cleanup pass focused on C-class clich?s and S-06 `??` phrasing. Residual signals remain where removing more terms could harm facts, enumerations, or normal Chinese transitions: C-08=7.

**Fidelity verdict:** pass
- Numbers preserved: yes
- Technical terms preserved: yes
- Proper nouns preserved: yes
- Residual signal note: further edits should be planned separately if a stricter detector target is supplied.

### Sample 13 - gemini/topic_05.md

- **Source path:** `ai-detection-workflow\meta\provider_articles\run_20260520\gemini\topic_05.md`
- **Rewritten path:** `ai-detection-workflow\meta\provider_articles\run_20260520_rewritten_zh\gemini\topic_05.md`
- **Language:** zh
- **Genre:** provider-generated Chinese long-form article
- **Approximate length:** 2982 characters
- **Encoding preflight:** UTF-8 read/write confirmed, mojibake scan pass

**Condensed plan (the exact fix list applied to this sample):**

| Fix ID | Rule | Tier | BEFORE | AFTER | Occurrences |
|:---|:---|:---:|:---|:---|---:|
| 1 | C-02 | A | 近年来， | 近几年， | 1 |
| 2 | C-01 | A | 此外， | 另外， | 1 |
| 3 | C-12 | A | 然而， | 但 | 3 |
| 4 | C-09 | A | 不仅 | 不只 | 2 |
| 5 | C-08 | A | 首先， | 先看， | 1 |
| 6 | C-08 | A | 其次， | 接着， | 1 |
| 7 | C-08 | A | 再次， | 再往下， | 1 |
| 8 | C-08 | A | 最后， | 到最后， | 1 |
| 9 | C-04 | A | 赋能 | 提升 | 1 |
| 10 | C-04 | A | 痛点 | 难点 | 1 |

**Rule hits before -> after (offline count):**

| Rule | Before | After | Delta |
|:---|---:|---:|---:|
| C-01 | 1 | 0 | -1 |
| C-02 | 2 | 1 | -1 |
| C-04 | 2 | 0 | -2 |
| C-08 | 5 | 2 | -3 |
| C-09 | 2 | 0 | -2 |
| C-12 | 4 | 0 | -4 |
| S-06 | 2 | 2 | 0 |

**Offline rule hits summary:** Applied a light visible cleanup pass focused on C-class clich?s and S-06 `??` phrasing. Residual signals remain where removing more terms could harm facts, enumerations, or normal Chinese transitions: C-02=1, C-08=2, S-06=2.

**Fidelity verdict:** pass
- Numbers preserved: yes
- Technical terms preserved: yes
- Proper nouns preserved: yes
- Residual signal note: further edits should be planned separately if a stricter detector target is supplied.

### Sample 14 - gemini/topic_06.md

- **Source path:** `ai-detection-workflow\meta\provider_articles\run_20260520\gemini\topic_06.md`
- **Rewritten path:** `ai-detection-workflow\meta\provider_articles\run_20260520_rewritten_zh\gemini\topic_06.md`
- **Language:** zh
- **Genre:** provider-generated Chinese long-form article
- **Approximate length:** 2791 characters
- **Encoding preflight:** UTF-8 read/write confirmed, mojibake scan pass

**Condensed plan (the exact fix list applied to this sample):**

| Fix ID | Rule | Tier | BEFORE | AFTER | Occurrences |
|:---|:---|:---:|:---|:---|---:|
| 1 | C-02 | A | 近年来， | 近几年， | 1 |
| 2 | C-01 | A | 综上所述， | 由此看， | 1 |
| 3 | C-09 | A | 不仅 | 不只 | 3 |
| 4 | C-04 | A | 痛点 | 难点 | 1 |
| 5 | C-04 | A | 闭环 | 完整流程 | 2 |
| 6 | C-15 | A | 这一 | 这个 | 1 |

**Rule hits before -> after (offline count):**

| Rule | Before | After | Delta |
|:---|---:|---:|---:|
| C-01 | 1 | 0 | -1 |
| C-02 | 3 | 2 | -1 |
| C-04 | 3 | 0 | -3 |
| C-08 | 1 | 1 | 0 |
| C-09 | 3 | 0 | -3 |
| C-15 | 1 | 0 | -1 |
| S-06 | 2 | 2 | 0 |

**Offline rule hits summary:** Applied a light visible cleanup pass focused on C-class clich?s and S-06 `??` phrasing. Residual signals remain where removing more terms could harm facts, enumerations, or normal Chinese transitions: C-02=2, C-08=1, S-06=2.

**Fidelity verdict:** pass
- Numbers preserved: yes
- Technical terms preserved: yes
- Proper nouns preserved: yes
- Residual signal note: further edits should be planned separately if a stricter detector target is supplied.

### Sample 15 - gemini/topic_07.md

- **Source path:** `ai-detection-workflow\meta\provider_articles\run_20260520\gemini\topic_07.md`
- **Rewritten path:** `ai-detection-workflow\meta\provider_articles\run_20260520_rewritten_zh\gemini\topic_07.md`
- **Language:** zh
- **Genre:** provider-generated Chinese long-form article
- **Approximate length:** 2920 characters
- **Encoding preflight:** UTF-8 read/write confirmed, mojibake scan pass

**Condensed plan (the exact fix list applied to this sample):**

| Fix ID | Rule | Tier | BEFORE | AFTER | Occurrences |
|:---|:---|:---:|:---|:---|---:|
| 1 | C-02 | A | 近年来， | 近几年， | 1 |
| 2 | C-01 | A | 此外， | 另外， | 1 |
| 3 | C-12 | A | 然而， | 但 | 2 |
| 4 | C-09 | A | 不仅 | 不只 | 3 |
| 5 | C-09 | A | 一方面， | 先看， | 2 |
| 6 | C-04 | A | 生态 | 协作体系 | 1 |
| 7 | C-13 | A | 日益 | 逐渐 | 1 |
| 8 | C-13 | A | 进一步 | 继续 | 1 |
| 9 | C-03 | A | 尤为 | 尤其 | 1 |
| 10 | C-15 | A | 这一 | 这个 | 1 |

**Rule hits before -> after (offline count):**

| Rule | Before | After | Delta |
|:---|---:|---:|---:|
| C-01 | 1 | 0 | -1 |
| C-02 | 3 | 2 | -1 |
| C-03 | 2 | 1 | -1 |
| C-04 | 1 | 0 | -1 |
| C-08 | 1 | 1 | 0 |
| C-09 | 11 | 5 | -6 |
| C-12 | 3 | 0 | -3 |
| C-13 | 2 | 0 | -2 |
| C-15 | 1 | 0 | -1 |
| S-06 | 3 | 3 | 0 |

**Offline rule hits summary:** Applied a light visible cleanup pass focused on C-class clich?s and S-06 `??` phrasing. Residual signals remain where removing more terms could harm facts, enumerations, or normal Chinese transitions: C-02=2, C-03=1, C-08=1, C-09=5, S-06=3.

**Fidelity verdict:** pass
- Numbers preserved: yes
- Technical terms preserved: yes
- Proper nouns preserved: yes
- Residual signal note: further edits should be planned separately if a stricter detector target is supplied.

### Sample 16 - gemini/topic_08.md

- **Source path:** `ai-detection-workflow\meta\provider_articles\run_20260520\gemini\topic_08.md`
- **Rewritten path:** `ai-detection-workflow\meta\provider_articles\run_20260520_rewritten_zh\gemini\topic_08.md`
- **Language:** zh
- **Genre:** provider-generated Chinese long-form article
- **Approximate length:** 2941 characters
- **Encoding preflight:** UTF-8 read/write confirmed, mojibake scan pass

**Condensed plan (the exact fix list applied to this sample):**

| Fix ID | Rule | Tier | BEFORE | AFTER | Occurrences |
|:---|:---|:---:|:---|:---|---:|
| 1 | C-02 | A | 近年来， | 近几年， | 1 |
| 2 | C-01 | A | 与此同时， | 同时， | 1 |
| 3 | C-12 | A | 然而， | 但 | 2 |
| 4 | C-09 | A | 不仅 | 不只 | 3 |
| 5 | C-04 | A | 痛点 | 难点 | 1 |
| 6 | C-04 | A | 闭环 | 完整流程 | 1 |
| 7 | C-04 | A | 生态 | 协作体系 | 4 |
| 8 | C-15 | A | 这一 | 这个 | 4 |

**Rule hits before -> after (offline count):**

| Rule | Before | After | Delta |
|:---|---:|---:|---:|
| C-01 | 1 | 0 | -1 |
| C-02 | 1 | 0 | -1 |
| C-03 | 1 | 1 | 0 |
| C-04 | 6 | 0 | -6 |
| C-08 | 2 | 2 | 0 |
| C-09 | 5 | 2 | -3 |
| C-12 | 3 | 0 | -3 |
| C-15 | 4 | 0 | -4 |
| S-06 | 6 | 6 | 0 |

**Offline rule hits summary:** Applied a light visible cleanup pass focused on C-class clich?s and S-06 `??` phrasing. Residual signals remain where removing more terms could harm facts, enumerations, or normal Chinese transitions: C-03=1, C-08=2, C-09=2, S-06=6.

**Fidelity verdict:** pass
- Numbers preserved: yes
- Technical terms preserved: yes
- Proper nouns preserved: yes
- Residual signal note: further edits should be planned separately if a stricter detector target is supplied.

## Cross-sample observations

- Common high-yield edits were C-01 transition clich?s, C-08 sequence markers, C-09 paired connective wording, C-04 business buzzwords, and S-06 `??` verb padding.
- Remaining hits are expected because this was a constrained, light pass. Some terms such as `??`, `??`, `??`, or `??` can be ordinary Chinese when tied to facts, lists, or technical process descriptions.
- No source files under `run_20260520` were modified. English topics 01-04 were not read or rewritten by this script.

## Caveats

- measurement_type: offline_rule_hits
- External detector status: not run
- Offline counts are literal vocabulary hits, not validated detector scores.
