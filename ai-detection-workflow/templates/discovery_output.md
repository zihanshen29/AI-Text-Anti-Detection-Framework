# Template: `discovery.md`

<!--
  About this template:
  - Filled by Layer 0 (Discovery) at the end of its scan.
  - Reviewed and approved by the user before Layer 1 (Planning) begins.
  - HARD RULE: no proposed rewrites in this file. Rewrites belong in plan.md.
  - HARD RULE: no pattern with zero hits should appear here. Absence is information,
    not an empty section.
  - When filling, replace angle-bracketed placeholders. Delete instructional HTML
    comments after filling (or keep them — they render invisibly in markdown).
-->

# Discovery — <document title or project name>

**Generated:** <YYYY-MM-DD HH:MM>
**Layer 0 version:** 1
**Awaiting user review.**

---

## 1. Document Summary

- **Path:** <relative or absolute path to the document being analysed>
- **Language:** en | zh | mixed
  <!-- If mixed, quantify: "80% en (Chapters 1–6), 20% zh (Appendix C glossary)". -->
- **Genre:** <academic thesis | research paper | blog post | report | book chapter | other>
- **Length:** <word count, character count for zh>
- **Section structure:**
  - Chapter 1 — <title> (≈ <N> words)
  - Chapter 2 — <title> (≈ <N> words)
  - …
  - Appendix <X> — <title> (≈ <N> words)

---

## 2. External Constraints (verbatim from Layer 0 Step 3 interview)

### Target detector(s)
<verbatim user answer. If user declined to name one, write "not specified — assuming
general academic detectors (GPTZero + Turnitin AI baseline)".>

### Institutional or publication rules
<verbatim. If the user uploaded a style guide, reference it here: "Heriot-Watt
Final Year Report Preparation Guidelines, uploaded as guidelines.pdf — requires
third-person past tense throughout Chapters 1–6".>

### Revision history supplied
- v<N>: <path>, role: <current | anti-regression baseline | earliest human draft>
- v<M>: <path>, role: <...>
<!-- If none supplied, write "none supplied — anti-regression check in Layer 1 will
     be based only on the current document." -->

### Hard constraints (do-not-touch list)
<list, verbatim from user>

### Grading or reader priorities to preserve
<verbatim. Example: "Marking rubric rewards self-reflection — retain reflective
sentences in §6.1/§6.2 even when they look AI-flavoured.">

### Language preference for our conversation
en | zh | mixed

---

## 3. Detected AI Patterns

<!--
  For each pattern with hit count ≥ 1, produce a block with the structure below.
  Patterns with zero hits in this document MUST NOT appear. If the document is
  clean on a rule, the rule was still useful — it ruled out a candidate. That
  information lives in §6 (round-count recommendation), not here.
-->

### Pattern <P-NN or C-NN>: <name from rule library>

- **Rule library reference:** `rules/<en|zh>/<file>.md#<pattern-id>`
- **Hit count:** <N>
- **Severity:** high | medium | low
  <!-- Severity combines hit count, detector weight, and genre relevance. A
       P-16 hit (vocabulary `delve`) in academic prose is high even at count=1;
       a C-07 (抽象名词) at count=4 in commercial writing is low. -->
- **Genre relevance for this document:** ★★★ | ★★ | ★ | ○
- **Detector sensitivity for user's target(s):** <quote from rule library table
  for the detectors listed in §2 target>

**Sample hits (verbatim with location):**

1. §<X.Y> (p. <N>, line <L>):
   > "<exact quoted text, preserving punctuation and formatting>"

2. §<X.Y> (p. <N>, line <L>):
   > "<exact quoted text>"

3. …

<!-- Include up to 5 samples per pattern. If hit count > 5, note "N total hits;
     5 representative samples shown above." -->

### Pattern <next>: <name>

…

---

## 4. Novel Patterns (not in rule library)

<!--
  Anything that read AI-generated during Layer 0 Step 1 but doesn't match any
  existing P-NN / C-NN. Each novel pattern becomes a candidate for addition to
  the rule library after the project completes.
-->

### Novel pattern <A>: <short descriptor>

- **First observed at:** §<X.Y> (p. <N>)
- **Why it reads AI-generated:** <one or two sentences>
- **Hit count:** <N>
- **Sample hits:**
  1. §<X.Y>:
     > "<exact quote>"
  2. …
- **Proposed rule-library addition:**
  - Proposed ID: <P-NN or C-NN>
  - Proposed detect rule: <grep pattern or structural check>
  - Proposed category: <which file — sentence_patterns / ai_cliches / tell_tale_phrases>

<!-- If no novel patterns were found, write "None identified during this pass."
     and delete the sub-section. Do not leave empty placeholders. -->

---

## 5. Technical-Fidelity Inventory

<!--
  This is the guardrail list. Layer 2 must preserve every item here
  byte-identically. Any proposed rewrite in Layer 1 that would touch a listed
  item must be flagged, not silently applied.
-->

### Numerical values (with context, grouped)

- Results region: `+0.9338 m`, `+0.9339 m`, `+0.3956 m`, `600 steps`, `1200 steps`, `step 872`, …
- Training scalars: `mean reward 34.15`, `mean episode length 956.94`, …
- <continue by region>

### Citations

- IEEE numeric: `[1]`, `[2]`, …, `[N]` — total <N> references.
- LaTeX `\cite{}` keys (if source accessible): <list or note "not inspected">.

### Equation labels

- `eq:2.1` through `eq:6.3`, numbered sequentially — do not renumber.

### Figure and Table cross-references

- Figures: `figure 1.1`, `figure 2.2`, … `figure 5.5`.
- Tables: `table 1.1`, `table 2.1`, `table 3.1`, `table 4.1`, `table 4.2`, `table 5.1`, `table 5.2`.

### Code, file, and parameter identifiers

- Model checkpoints: `model_298.pt`, `model_596.pt`
- Runtime flags: `--post_step_app_update`, `mpc_rate_div`, `lock_contact_to_trot`
- Timestamps / run IDs: `2026-04-08_14-25-55`
- Task IDs: `Isaac-LocoManip-B1-Walk-RL-v0`
- <continue>

### Proper nouns (author-chosen)

- Product / library names: <list>
- Project names: <list>
- Acronyms to preserve: <list>

### Section / chapter titles (fixed)

- Chapter 1 "Introduction", Chapter 2 "Literature Review", …
<!-- Titles are fixed because changing them breaks cross-references and the
     Table of Contents. -->

---

## 6. Recommended Round Count

**Recommendation:** <3 | 5 | 7> rounds

**Justification:**
<One paragraph. Base the recommendation on:
  - Total pattern hit count (light < 15, standard 15–40, heavy > 40).
  - Severity mix (many high-severity → leans heavier).
  - User's starting detector score and target delta.
  - Presence of block-rewrite targets (Abstract, Conclusion openings) → forces Round C.
  - Genre strictness (formal academic → needs audit round; informal → may skip).
Do NOT justify by document length alone. A 100-page thesis with clean language
needs fewer rounds than a 20-page paper saturated with P-16 vocabulary.>

**Proposed round map (for user review, final version produced in plan.md):**

| Round | Tier | Indicative scope |
|:---:|:---:|:---|
| 1 | A | <e.g., tense + first-person sweep> |
| 2 | B | <e.g., fragment merging, ~14 fixes> |
| 3 | A+D | <e.g., vocabulary cliché sweep> |
| 4 | C | <e.g., Abstract + §6.1 block rewrites> |
| 5 | — | Audit |

---

## 7. Open Questions (user decision needed before Layer 1)

<!--
  Anything that blocks Layer 1 from producing a complete plan. Do NOT proceed
  to Layer 1 until these are resolved. If the user can answer in one message,
  update this file in place and mark resolved.
-->

1. **<question>**
   - Options: <A | B | C>
   - Default if no response: <what Layer 1 will assume>
2. **<question>** …

<!-- If no open questions exist, write "No open questions — ready for Layer 1."
     and delete the numbered list. -->

---

## Reviewer checklist

Before the user approves this document:

- [ ] Language and genre detection match the document.
- [ ] External constraints captured accurately (user checks verbatim quotes).
- [ ] Every listed pattern has at least one verbatim quote with location.
- [ ] No pattern with zero hits is included.
- [ ] Novel patterns have clear enough quotes to be actionable.
- [ ] Guardrail inventory is complete (numbers, citations, figures, code).
- [ ] Recommended round count is justified.
- [ ] No proposed rewrites leaked into this file.

Once approved, run Layer 1 against this discovery.
