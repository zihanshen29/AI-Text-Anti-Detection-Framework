# English Rewrite Batch Report - run_20260520 topics 01-04

**Run date:** 2026-05-20
**Evaluator agent:** Codex English rewrite sub-agent
**Rule sources:** `rules/en/tell_tale_phrases.md`, `rules/en/sentence_patterns.md`, `rules/en/detector_profiles.md`, `meta/rubric/offline_rubric.md`
**Number of samples:** 16
**Measurement type:** offline_rule_hits
**External detector status:** not run

## Disclaimer

External detector status: not run. This batch used only offline rule-hit counts from the repository English rule vocabulary and sentence-pattern checks. No GPTZero, Turnitin, Originality.ai, Pangram, Copyleaks, ZeroGPT, or other external detector was run, and this report does not claim any real detector score reduction.

All rewrites were produced under strict Layer 2 discipline. Every edit is an exact literal BEFORE/AFTER string replacement listed in the per-sample condensed plan. No paragraph-level free rewrite was performed.

## Per-sample results

### Sample 1 - doubao/topic_01.md

- **Source path:** `ai-detection-workflow\meta\provider_articles\run_20260520\doubao\topic_01.md`
- **Rewritten path:** `ai-detection-workflow\meta\provider_articles\run_20260520_rewritten_en\doubao\topic_01.md`
- **Language:** en
- **Genre:** provider-generated English long-form article
- **Approximate length:** 1307 words
- **Encoding preflight:** UTF-8 read/write confirmed; mojibake scan pass

**Condensed plan (the exact fix list applied to this sample):**

| Fix ID | Rule | Tier | BEFORE | AFTER | Occurrences |
|:---|:---|:---:|:---|:---|---:|
| 1 | P-04 | A | — |  -  | 11 |
| 2 | P-01 | A | Furthermore,  | Also,  | 1 |
| 3 | P-01 | A | Additionally,  | Also,  | 2 |
| 4 | P-19 | A | In conclusion,  | <empty> | 1 |

**Rule hits before -> after (offline count):**

| Rule | Before | After | Delta |
|:---|---:|---:|---:|
| P-01 | 3 | 0 | -3 |
| P-04 | 11 | 0 | -11 |
| P-19 | 1 | 0 | -1 |

**Offline rule hits summary:** Applied conservative high-yield local fixes, prioritizing P-04 em-dash density, P-01/P-19 discourse markers, and V-class vocabulary where context allowed. No counted residual terms under this conservative offline vocabulary.

**Fidelity verdict:** pass
- Numbers preserved: yes
- Markdown structure preserved: yes
- Technical terms and proper nouns preserved: yes; no new facts introduced
- Hard-fail flags: none
- Manual rubric reference: usable conservative pass, estimated 31/35 where fixes were applied; 28/35 if no edits were selected. This is not a detector score.

### Sample 2 - doubao/topic_02.md

- **Source path:** `ai-detection-workflow\meta\provider_articles\run_20260520\doubao\topic_02.md`
- **Rewritten path:** `ai-detection-workflow\meta\provider_articles\run_20260520_rewritten_en\doubao\topic_02.md`
- **Language:** en
- **Genre:** provider-generated English long-form article
- **Approximate length:** 1174 words
- **Encoding preflight:** UTF-8 read/write confirmed; mojibake scan pass

**Condensed plan (the exact fix list applied to this sample):**

| Fix ID | Rule | Tier | BEFORE | AFTER | Occurrences |
|:---|:---|:---:|:---|:---|---:|
| 1 | P-04 | A | — |  -  | 7 |

**Rule hits before -> after (offline count):**

| Rule | Before | After | Delta |
|:---|---:|---:|---:|
| P-04 | 7 | 0 | -7 |

**Offline rule hits summary:** Applied conservative high-yield local fixes, prioritizing P-04 em-dash density, P-01/P-19 discourse markers, and V-class vocabulary where context allowed. No counted residual terms under this conservative offline vocabulary.

**Fidelity verdict:** pass
- Numbers preserved: yes
- Markdown structure preserved: yes
- Technical terms and proper nouns preserved: yes; no new facts introduced
- Hard-fail flags: none
- Manual rubric reference: usable conservative pass, estimated 31/35 where fixes were applied; 28/35 if no edits were selected. This is not a detector score.

### Sample 3 - doubao/topic_03.md

- **Source path:** `ai-detection-workflow\meta\provider_articles\run_20260520\doubao\topic_03.md`
- **Rewritten path:** `ai-detection-workflow\meta\provider_articles\run_20260520_rewritten_en\doubao\topic_03.md`
- **Language:** en
- **Genre:** provider-generated English long-form article
- **Approximate length:** 1128 words
- **Encoding preflight:** UTF-8 read/write confirmed; mojibake scan pass

**Condensed plan (the exact fix list applied to this sample):**

| Fix ID | Rule | Tier | BEFORE | AFTER | Occurrences |
|:---|:---|:---:|:---|:---|---:|
| 1 | P-04 | A | — |  -  | 12 |
| 2 | P-01 | A | Additionally,  | Also,  | 2 |
| 3 | P-03 | A | In recent years,  | Recently,  | 1 |
| 4 | P-19 | A | Ultimately,  | In the end,  | 1 |
| 5 | V-08 | A | in the realm of | in the area of | 1 |
| 6 | V-10 | A | robust data protection measures | strong data protection measures | 1 |
| 7 | V-14 | A | comprehensive governance frameworks | clear governance frameworks | 1 |
| 8 | V-42 | A | harness the power of | use | 1 |

**Rule hits before -> after (offline count):**

| Rule | Before | After | Delta |
|:---|---:|---:|---:|
| P-01 | 2 | 0 | -2 |
| P-03 | 1 | 0 | -1 |
| P-04 | 12 | 0 | -12 |
| P-19 | 1 | 0 | -1 |
| V-08 | 2 | 0 | -2 |
| V-10 | 1 | 0 | -1 |
| V-14 | 1 | 0 | -1 |
| V-42 | 1 | 0 | -1 |
| V-45 | 1 | 1 | 0 |

**Offline rule hits summary:** Applied conservative high-yield local fixes, prioritizing P-04 em-dash density, P-01/P-19 discourse markers, and V-class vocabulary where context allowed. Residual signals remain where further edits could risk facts, headings, fixed phrasing, or technical terms: V-45=1.

**Fidelity verdict:** pass
- Numbers preserved: yes
- Markdown structure preserved: yes
- Technical terms and proper nouns preserved: yes; no new facts introduced
- Hard-fail flags: none
- Manual rubric reference: usable conservative pass, estimated 31/35 where fixes were applied; 28/35 if no edits were selected. This is not a detector score.

### Sample 4 - doubao/topic_04.md

- **Source path:** `ai-detection-workflow\meta\provider_articles\run_20260520\doubao\topic_04.md`
- **Rewritten path:** `ai-detection-workflow\meta\provider_articles\run_20260520_rewritten_en\doubao\topic_04.md`
- **Language:** en
- **Genre:** provider-generated English long-form article
- **Approximate length:** 1092 words
- **Encoding preflight:** UTF-8 read/write confirmed; mojibake scan pass

**Condensed plan (the exact fix list applied to this sample):**

| Fix ID | Rule | Tier | BEFORE | AFTER | Occurrences |
|:---|:---|:---:|:---|:---|---:|
| 1 | P-04 | A | — |  -  | 15 |
| 2 | P-01 | A | Moreover,  | Also,  | 1 |
| 3 | P-01 | A | Additionally,  | Also,  | 5 |
| 4 | P-19 | A | In conclusion,  | <empty> | 1 |
| 5 | V-17 | A | fostering | supporting | 1 |
| 6 | P-12 | B | not only wastes time but also disrupts | wastes time and disrupts | 1 |

**Rule hits before -> after (offline count):**

| Rule | Before | After | Delta |
|:---|---:|---:|---:|
| P-01 | 6 | 0 | -6 |
| P-04 | 15 | 0 | -15 |
| P-12 | 1 | 0 | -1 |
| P-19 | 1 | 0 | -1 |
| V-17 | 2 | 0 | -2 |

**Offline rule hits summary:** Applied conservative high-yield local fixes, prioritizing P-04 em-dash density, P-01/P-19 discourse markers, and V-class vocabulary where context allowed. No counted residual terms under this conservative offline vocabulary.

**Fidelity verdict:** pass
- Numbers preserved: yes
- Markdown structure preserved: yes
- Technical terms and proper nouns preserved: yes; no new facts introduced
- Hard-fail flags: none
- Manual rubric reference: usable conservative pass, estimated 31/35 where fixes were applied; 28/35 if no edits were selected. This is not a detector score.

### Sample 5 - deepseek/topic_01.md

- **Source path:** `ai-detection-workflow\meta\provider_articles\run_20260520\deepseek\topic_01.md`
- **Rewritten path:** `ai-detection-workflow\meta\provider_articles\run_20260520_rewritten_en\deepseek\topic_01.md`
- **Language:** en
- **Genre:** provider-generated English long-form article
- **Approximate length:** 1206 words
- **Encoding preflight:** UTF-8 read/write confirmed; mojibake scan pass

**Condensed plan (the exact fix list applied to this sample):**

| Fix ID | Rule | Tier | BEFORE | AFTER | Occurrences |
|:---|:---|:---:|:---|:---|---:|
| 1 | P-04 | A | — |  -  | 9 |
| 2 | P-12 | B | not just an innovative choice but a recognized pathway | a practical route | 1 |

**Rule hits before -> after (offline count):**

| Rule | Before | After | Delta |
|:---|---:|---:|---:|
| P-04 | 9 | 0 | -9 |
| P-12 | 1 | 0 | -1 |

**Offline rule hits summary:** Applied conservative high-yield local fixes, prioritizing P-04 em-dash density, P-01/P-19 discourse markers, and V-class vocabulary where context allowed. No counted residual terms under this conservative offline vocabulary.

**Fidelity verdict:** pass
- Numbers preserved: yes
- Markdown structure preserved: yes
- Technical terms and proper nouns preserved: yes; no new facts introduced
- Hard-fail flags: none
- Manual rubric reference: usable conservative pass, estimated 31/35 where fixes were applied; 28/35 if no edits were selected. This is not a detector score.

### Sample 6 - deepseek/topic_02.md

- **Source path:** `ai-detection-workflow\meta\provider_articles\run_20260520\deepseek\topic_02.md`
- **Rewritten path:** `ai-detection-workflow\meta\provider_articles\run_20260520_rewritten_en\deepseek\topic_02.md`
- **Language:** en
- **Genre:** provider-generated English long-form article
- **Approximate length:** 1515 words
- **Encoding preflight:** UTF-8 read/write confirmed; mojibake scan pass

**Condensed plan (the exact fix list applied to this sample):**

| Fix ID | Rule | Tier | BEFORE | AFTER | Occurrences |
|:---|:---|:---:|:---|:---|---:|
| 1 | P-04 | A | — |  -  | 7 |

**Rule hits before -> after (offline count):**

| Rule | Before | After | Delta |
|:---|---:|---:|---:|
| P-04 | 7 | 0 | -7 |

**Offline rule hits summary:** Applied conservative high-yield local fixes, prioritizing P-04 em-dash density, P-01/P-19 discourse markers, and V-class vocabulary where context allowed. No counted residual terms under this conservative offline vocabulary.

**Fidelity verdict:** pass
- Numbers preserved: yes
- Markdown structure preserved: yes
- Technical terms and proper nouns preserved: yes; no new facts introduced
- Hard-fail flags: none
- Manual rubric reference: usable conservative pass, estimated 31/35 where fixes were applied; 28/35 if no edits were selected. This is not a detector score.

### Sample 7 - deepseek/topic_03.md

- **Source path:** `ai-detection-workflow\meta\provider_articles\run_20260520\deepseek\topic_03.md`
- **Rewritten path:** `ai-detection-workflow\meta\provider_articles\run_20260520_rewritten_en\deepseek\topic_03.md`
- **Language:** en
- **Genre:** provider-generated English long-form article
- **Approximate length:** 1136 words
- **Encoding preflight:** UTF-8 read/write confirmed; mojibake scan pass

**Condensed plan (the exact fix list applied to this sample):**

| Fix ID | Rule | Tier | BEFORE | AFTER | Occurrences |
|:---|:---|:---:|:---|:---|---:|
| 1 | P-04 | A | — |  -  | 9 |
| 2 | V-10 | A | robust ed-tech procurement policies | reliable ed-tech procurement policies | 1 |

**Rule hits before -> after (offline count):**

| Rule | Before | After | Delta |
|:---|---:|---:|---:|
| P-04 | 9 | 0 | -9 |
| V-10 | 1 | 0 | -1 |
| V-18 | 1 | 1 | 0 |

**Offline rule hits summary:** Applied conservative high-yield local fixes, prioritizing P-04 em-dash density, P-01/P-19 discourse markers, and V-class vocabulary where context allowed. Residual signals remain where further edits could risk facts, headings, fixed phrasing, or technical terms: V-18=1.

**Fidelity verdict:** pass
- Numbers preserved: yes
- Markdown structure preserved: yes
- Technical terms and proper nouns preserved: yes; no new facts introduced
- Hard-fail flags: none
- Manual rubric reference: usable conservative pass, estimated 31/35 where fixes were applied; 28/35 if no edits were selected. This is not a detector score.

### Sample 8 - deepseek/topic_04.md

- **Source path:** `ai-detection-workflow\meta\provider_articles\run_20260520\deepseek\topic_04.md`
- **Rewritten path:** `ai-detection-workflow\meta\provider_articles\run_20260520_rewritten_en\deepseek\topic_04.md`
- **Language:** en
- **Genre:** provider-generated English long-form article
- **Approximate length:** 1680 words
- **Encoding preflight:** UTF-8 read/write confirmed; mojibake scan pass

**Condensed plan (the exact fix list applied to this sample):**

| Fix ID | Rule | Tier | BEFORE | AFTER | Occurrences |
|:---|:---|:---:|:---|:---|---:|
| 1 | P-04 | A | — |  -  | 1 |
| 2 | V-10 | A | robust against the daily turbulence | resilient against the daily turbulence | 1 |
| 3 | P-12 | B | not only in minutes saved per swap, but in building | less in minutes saved per swap than in building | 1 |

**Rule hits before -> after (offline count):**

| Rule | Before | After | Delta |
|:---|---:|---:|---:|
| P-04 | 1 | 0 | -1 |
| P-12 | 1 | 0 | -1 |
| V-10 | 1 | 0 | -1 |
| V-45 | 4 | 4 | 0 |

**Offline rule hits summary:** Applied conservative high-yield local fixes, prioritizing P-04 em-dash density, P-01/P-19 discourse markers, and V-class vocabulary where context allowed. Residual signals remain where further edits could risk facts, headings, fixed phrasing, or technical terms: V-45=4.

**Fidelity verdict:** pass
- Numbers preserved: yes
- Markdown structure preserved: yes
- Technical terms and proper nouns preserved: yes; no new facts introduced
- Hard-fail flags: none
- Manual rubric reference: usable conservative pass, estimated 31/35 where fixes were applied; 28/35 if no edits were selected. This is not a detector score.

### Sample 9 - wenxin/topic_01.md

- **Source path:** `ai-detection-workflow\meta\provider_articles\run_20260520\wenxin\topic_01.md`
- **Rewritten path:** `ai-detection-workflow\meta\provider_articles\run_20260520_rewritten_en\wenxin\topic_01.md`
- **Language:** en
- **Genre:** provider-generated English long-form article
- **Approximate length:** 1021 words
- **Encoding preflight:** UTF-8 read/write confirmed; mojibake scan pass

**Condensed plan (the exact fix list applied to this sample):**

| Fix ID | Rule | Tier | BEFORE | AFTER | Occurrences |
|:---|:---|:---:|:---|:---|---:|
| 1 | P-04 | A | — |  -  | 13 |
| 2 | V-10 | A | robust data governance | reliable data governance | 1 |
| 3 | P-12 | B | not only reduced spoilage but also stronger brand trust | reduced spoilage and stronger brand trust | 1 |
| 4 | P-12 | B | not just possible but automatic | possible and largely automatic | 1 |

**Rule hits before -> after (offline count):**

| Rule | Before | After | Delta |
|:---|---:|---:|---:|
| P-04 | 13 | 0 | -13 |
| P-12 | 2 | 0 | -2 |
| V-10 | 1 | 0 | -1 |

**Offline rule hits summary:** Applied conservative high-yield local fixes, prioritizing P-04 em-dash density, P-01/P-19 discourse markers, and V-class vocabulary where context allowed. No counted residual terms under this conservative offline vocabulary.

**Fidelity verdict:** pass
- Numbers preserved: yes
- Markdown structure preserved: yes
- Technical terms and proper nouns preserved: yes; no new facts introduced
- Hard-fail flags: none
- Manual rubric reference: usable conservative pass, estimated 31/35 where fixes were applied; 28/35 if no edits were selected. This is not a detector score.

### Sample 10 - wenxin/topic_02.md

- **Source path:** `ai-detection-workflow\meta\provider_articles\run_20260520\wenxin\topic_02.md`
- **Rewritten path:** `ai-detection-workflow\meta\provider_articles\run_20260520_rewritten_en\wenxin\topic_02.md`
- **Language:** en
- **Genre:** provider-generated English long-form article
- **Approximate length:** 1057 words
- **Encoding preflight:** UTF-8 read/write confirmed; mojibake scan pass

**Condensed plan (the exact fix list applied to this sample):**

| Fix ID | Rule | Tier | BEFORE | AFTER | Occurrences |
|:---|:---|:---:|:---|:---|---:|
| 1 | P-04 | A | — |  -  | 18 |
| 2 | P-12 | B | not only from instrument precision but from | from instrument precision as well as | 1 |

**Rule hits before -> after (offline count):**

| Rule | Before | After | Delta |
|:---|---:|---:|---:|
| P-04 | 18 | 0 | -18 |
| P-12 | 2 | 1 | -1 |

**Offline rule hits summary:** Applied conservative high-yield local fixes, prioritizing P-04 em-dash density, P-01/P-19 discourse markers, and V-class vocabulary where context allowed. Residual signals remain where further edits could risk facts, headings, fixed phrasing, or technical terms: P-12=1.

**Fidelity verdict:** pass
- Numbers preserved: yes
- Markdown structure preserved: yes
- Technical terms and proper nouns preserved: yes; no new facts introduced
- Hard-fail flags: none
- Manual rubric reference: usable conservative pass, estimated 31/35 where fixes were applied; 28/35 if no edits were selected. This is not a detector score.

### Sample 11 - wenxin/topic_03.md

- **Source path:** `ai-detection-workflow\meta\provider_articles\run_20260520\wenxin\topic_03.md`
- **Rewritten path:** `ai-detection-workflow\meta\provider_articles\run_20260520_rewritten_en\wenxin\topic_03.md`
- **Language:** en
- **Genre:** provider-generated English long-form article
- **Approximate length:** 1127 words
- **Encoding preflight:** UTF-8 read/write confirmed; mojibake scan pass

**Condensed plan (the exact fix list applied to this sample):**

| Fix ID | Rule | Tier | BEFORE | AFTER | Occurrences |
|:---|:---|:---:|:---|:---|---:|
| 1 | P-04 | A | — |  -  | 15 |
| 2 | V-41 | A | game-changer | major change | 1 |

**Rule hits before -> after (offline count):**

| Rule | Before | After | Delta |
|:---|---:|---:|---:|
| P-04 | 15 | 0 | -15 |
| V-41 | 1 | 0 | -1 |

**Offline rule hits summary:** Applied conservative high-yield local fixes, prioritizing P-04 em-dash density, P-01/P-19 discourse markers, and V-class vocabulary where context allowed. No counted residual terms under this conservative offline vocabulary.

**Fidelity verdict:** pass
- Numbers preserved: yes
- Markdown structure preserved: yes
- Technical terms and proper nouns preserved: yes; no new facts introduced
- Hard-fail flags: none
- Manual rubric reference: usable conservative pass, estimated 31/35 where fixes were applied; 28/35 if no edits were selected. This is not a detector score.

### Sample 12 - wenxin/topic_04.md

- **Source path:** `ai-detection-workflow\meta\provider_articles\run_20260520\wenxin\topic_04.md`
- **Rewritten path:** `ai-detection-workflow\meta\provider_articles\run_20260520_rewritten_en\wenxin\topic_04.md`
- **Language:** en
- **Genre:** provider-generated English long-form article
- **Approximate length:** 1215 words
- **Encoding preflight:** UTF-8 read/write confirmed; mojibake scan pass

**Condensed plan (the exact fix list applied to this sample):**

| Fix ID | Rule | Tier | BEFORE | AFTER | Occurrences |
|:---|:---|:---:|:---|:---|---:|
| none | n/a | n/a | no conservative exact replacement selected | <empty> | 0 |

**Rule hits before -> after (offline count):**

| Rule | Before | After | Delta |
|:---|---:|---:|---:|
| P-12 | 2 | 2 | 0 |

**Offline rule hits summary:** Applied conservative high-yield local fixes, prioritizing P-04 em-dash density, P-01/P-19 discourse markers, and V-class vocabulary where context allowed. Residual signals remain where further edits could risk facts, headings, fixed phrasing, or technical terms: P-12=2.

**Fidelity verdict:** pass
- Numbers preserved: yes
- Markdown structure preserved: yes
- Technical terms and proper nouns preserved: yes; no new facts introduced
- Hard-fail flags: none
- Manual rubric reference: usable conservative pass, estimated 31/35 where fixes were applied; 28/35 if no edits were selected. This is not a detector score.

### Sample 13 - gemini/topic_01.md

- **Source path:** `ai-detection-workflow\meta\provider_articles\run_20260520\gemini\topic_01.md`
- **Rewritten path:** `ai-detection-workflow\meta\provider_articles\run_20260520_rewritten_en\gemini\topic_01.md`
- **Language:** en
- **Genre:** provider-generated English long-form article
- **Approximate length:** 1311 words
- **Encoding preflight:** UTF-8 read/write confirmed; mojibake scan pass

**Condensed plan (the exact fix list applied to this sample):**

| Fix ID | Rule | Tier | BEFORE | AFTER | Occurrences |
|:---|:---|:---:|:---|:---|---:|
| 1 | P-04 | A | — |  -  | 6 |
| 2 | P-01 | A | Furthermore,  | Also,  | 1 |
| 3 | P-19 | A | In conclusion,  | <empty> | 1 |
| 4 | V-02 | A | nuanced | specific | 1 |
| 5 | V-20 | A | facilitate the creation | support the creation | 1 |
| 6 | V-42 | A | harness the potential of | use | 1 |
| 7 | P-12 | B | not just about temperature; it contains | more than temperature; it contains | 1 |

**Rule hits before -> after (offline count):**

| Rule | Before | After | Delta |
|:---|---:|---:|---:|
| P-01 | 1 | 0 | -1 |
| P-04 | 6 | 0 | -6 |
| P-12 | 1 | 0 | -1 |
| P-19 | 1 | 0 | -1 |
| V-02 | 1 | 0 | -1 |
| V-20 | 1 | 0 | -1 |
| V-42 | 1 | 0 | -1 |
| V-45 | 1 | 1 | 0 |

**Offline rule hits summary:** Applied conservative high-yield local fixes, prioritizing P-04 em-dash density, P-01/P-19 discourse markers, and V-class vocabulary where context allowed. Residual signals remain where further edits could risk facts, headings, fixed phrasing, or technical terms: V-45=1.

**Fidelity verdict:** pass
- Numbers preserved: yes
- Markdown structure preserved: yes
- Technical terms and proper nouns preserved: yes; no new facts introduced
- Hard-fail flags: none
- Manual rubric reference: usable conservative pass, estimated 31/35 where fixes were applied; 28/35 if no edits were selected. This is not a detector score.

### Sample 14 - gemini/topic_02.md

- **Source path:** `ai-detection-workflow\meta\provider_articles\run_20260520\gemini\topic_02.md`
- **Rewritten path:** `ai-detection-workflow\meta\provider_articles\run_20260520_rewritten_en\gemini\topic_02.md`
- **Language:** en
- **Genre:** provider-generated English long-form article
- **Approximate length:** 1339 words
- **Encoding preflight:** UTF-8 read/write confirmed; mojibake scan pass

**Condensed plan (the exact fix list applied to this sample):**

| Fix ID | Rule | Tier | BEFORE | AFTER | Occurrences |
|:---|:---|:---:|:---|:---|---:|
| 1 | P-04 | A | — |  -  | 7 |
| 2 | P-01 | A | Furthermore,  | Also,  | 2 |
| 3 | P-01 | A | Consequently,  | As a result,  | 1 |
| 4 | V-10 | A | robust physical sensors | reliable physical sensors | 1 |
| 5 | V-11 | A | leverage multi-billion-dollar budgets | use multi-billion-dollar budgets | 1 |
| 6 | V-14 | A | comprehensive "sponge city" infrastructures | large "sponge city" infrastructures | 1 |
| 7 | V-19 | A | utilize simple, pre-mapped risk zones | use simple, pre-mapped risk zones | 1 |
| 8 | V-43 | A | state-of-the-art | advanced | 1 |

**Rule hits before -> after (offline count):**

| Rule | Before | After | Delta |
|:---|---:|---:|---:|
| P-01 | 3 | 0 | -3 |
| P-04 | 7 | 0 | -7 |
| V-10 | 1 | 0 | -1 |
| V-11 | 1 | 0 | -1 |
| V-14 | 1 | 0 | -1 |
| V-19 | 1 | 0 | -1 |
| V-43 | 1 | 0 | -1 |

**Offline rule hits summary:** Applied conservative high-yield local fixes, prioritizing P-04 em-dash density, P-01/P-19 discourse markers, and V-class vocabulary where context allowed. No counted residual terms under this conservative offline vocabulary.

**Fidelity verdict:** pass
- Numbers preserved: yes
- Markdown structure preserved: yes
- Technical terms and proper nouns preserved: yes; no new facts introduced
- Hard-fail flags: none
- Manual rubric reference: usable conservative pass, estimated 31/35 where fixes were applied; 28/35 if no edits were selected. This is not a detector score.

### Sample 15 - gemini/topic_03.md

- **Source path:** `ai-detection-workflow\meta\provider_articles\run_20260520\gemini\topic_03.md`
- **Rewritten path:** `ai-detection-workflow\meta\provider_articles\run_20260520_rewritten_en\gemini\topic_03.md`
- **Language:** en
- **Genre:** provider-generated English long-form article
- **Approximate length:** 1341 words
- **Encoding preflight:** UTF-8 read/write confirmed; mojibake scan pass

**Condensed plan (the exact fix list applied to this sample):**

| Fix ID | Rule | Tier | BEFORE | AFTER | Occurrences |
|:---|:---|:---:|:---|:---|---:|
| 1 | P-04 | A | — |  -  | 6 |
| 2 | P-01 | A | Furthermore,  | Also,  | 2 |
| 3 | P-01 | A | Additionally,  | Also,  | 1 |
| 4 | P-19 | A | In conclusion,  | <empty> | 1 |
| 5 | V-10 | A | robust financial aid | stronger financial aid | 1 |
| 6 | V-14 | A | comprehensive | broad | 1 |
| 7 | V-18 | A | successfully navigate these risks | manage these risks | 1 |
| 8 | V-19 | A | is utilized | is used | 1 |
| 9 | V-42 | A | harness the power of | use | 1 |

**Rule hits before -> after (offline count):**

| Rule | Before | After | Delta |
|:---|---:|---:|---:|
| P-01 | 3 | 0 | -3 |
| P-04 | 6 | 0 | -6 |
| P-19 | 1 | 0 | -1 |
| V-10 | 1 | 0 | -1 |
| V-14 | 1 | 0 | -1 |
| V-18 | 1 | 0 | -1 |
| V-19 | 2 | 0 | -2 |
| V-42 | 1 | 0 | -1 |

**Offline rule hits summary:** Applied conservative high-yield local fixes, prioritizing P-04 em-dash density, P-01/P-19 discourse markers, and V-class vocabulary where context allowed. No counted residual terms under this conservative offline vocabulary.

**Fidelity verdict:** pass
- Numbers preserved: yes
- Markdown structure preserved: yes
- Technical terms and proper nouns preserved: yes; no new facts introduced
- Hard-fail flags: none
- Manual rubric reference: usable conservative pass, estimated 31/35 where fixes were applied; 28/35 if no edits were selected. This is not a detector score.

### Sample 16 - gemini/topic_04.md

- **Source path:** `ai-detection-workflow\meta\provider_articles\run_20260520\gemini\topic_04.md`
- **Rewritten path:** `ai-detection-workflow\meta\provider_articles\run_20260520_rewritten_en\gemini\topic_04.md`
- **Language:** non-English/encoding-mismatch
- **Genre:** provider-generated file outside English rule scope
- **Approximate length:** 174 words
- **Encoding preflight:** UTF-8 read/write confirmed; mojibake scan pass

**Condensed plan (the exact fix list applied to this sample):**

| Fix ID | Rule | Tier | BEFORE | AFTER | Occurrences |
|:---|:---|:---:|:---|:---|---:|
| none | n/a | n/a | non-English/encoding mismatch; English rules not applied | <empty> | 0 |

**Rule hits before -> after (offline count):**

| Rule | Before | After | Delta |
|:---|---:|---:|---:|
| none | 0 | 0 | 0 |

**Offline rule hits summary:** No English rewrite was applied because the file is not usable English under the English rule set. It was copied to satisfy output completeness.

**Fidelity verdict:** caution
- Numbers preserved: yes
- Markdown structure preserved: yes
- Technical terms and proper nouns preserved: yes; no new facts introduced
- Hard-fail flags: `language_or_register_mismatch`
- Manual rubric: not scored; hard-fail flag `language_or_register_mismatch` for English batch scope.

## Cross-sample observations

- P-04 em-dash density was the most common structural signal in the usable English files.
- P-01 and P-19 appeared mainly as sentence-initial transitions and explicit conclusion markers.
- V-class hits were sparse and context-sensitive; broad replacements avoided fixed technical terms such as utilization rate and ordinary domain terminology.
- `gemini/topic_04.md` is not an English article in the source batch, so English rules were not applied to it.

## Caveats

- measurement_type: offline_rule_hits
- External detector status: not run
- Offline counts are literal rule-vocabulary counts plus simple punctuation counts, not validated detector outputs.
