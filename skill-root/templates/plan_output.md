# Template: `plan.md`

<!--
  About this template:
  - Filled by Layer 1 (Planning) based on an approved discovery.md.
  - Reviewed and approved by the user before Layer 2 (Execution) begins.
  - HARD RULE: every Tier A/B/D fix must have verbatim BEFORE and exact AFTER strings.
    Fuzzy descriptions are not acceptable. If Layer 1 cannot extract a verbatim BEFORE,
    escalate to Open Questions instead of guessing.
  - HARD RULE: one tier per round. Never mix A-fixes and C-fixes in the same round.
  - This file is the single source of truth for Layer 2. Anything not written here
    does not get executed.
-->

# Plan — <document title or project name>

**Generated:** <YYYY-MM-DD HH:MM>
**Layer 1 version:** 1
**Based on discovery:** `discovery.md` (generated <date>)
**Awaiting user approval.**

---

## 0. Meta

- **Document path:** <path>
- **Language:** en | zh | mixed
- **Genre:** <from discovery §1>
- **Target detector(s):** <from discovery §2>
- **Round count:** <N>
- **Prior versions (for anti-regression):**
  - v<X> at `<path>` — role: <earliest human draft | intermediate | most recent flagged version>
  - v<Y> at `<path>` — role: <...>
- **Current version label:** v<14> (the version being edited)
- **Output label:** v<15> (the version produced after all rounds)

---

## 1. Guardrails (copied verbatim from discovery.md §5)

<!--
  Do not rephrase. Do not reorganise. Copy the lists exactly as they appear in
  discovery. Layer 2 will diff this list before and after every round.
-->

### Numerical values
<verbatim copy>

### Citations
<verbatim copy>

### Equation labels
<verbatim copy>

### Figure and Table cross-references
<verbatim copy>

### Code, file, and parameter identifiers
<verbatim copy>

### Proper nouns
<verbatim copy>

### Section / chapter titles
<verbatim copy>

---

## 2. Round Roster

| Round | Tier | Scope | Fix count | Expected risk | Justification |
|:---:|:---:|:---|:---:|:---:|:---|
| 1 | A | <e.g., tense + first-person sweep> | <N> | low | <one clause> |
| 2 | B | <e.g., fragment merging> | <N> | med | <one clause> |
| 3 | A+D | <e.g., cliché vocabulary + residual sweep> | <N> | low | <one clause> |
| 4 | C | <e.g., Abstract + §6.1 rewrite> | <N> | high | <one clause> |
| 5 | — | Audit (no new edits) | 0 | low | <one clause> |

<!-- If round count differs from 5, adjust the table. Never mix tiers within a
     row. If a round needs both A and D work, mark as "A+D" and list the fixes
     separately in §3. -->

---

## 3. Per-Round Fix Plans

### Round 1 — <short descriptor>

- **Tier:** A
- **Scope:** <what class of fix this round covers>
- **Fix count:** <N>
- **Files touched:** <list>
- **Expected detector-score impact:** <qualitative, e.g., "moderate — this round
  addresses the highest-weighted pattern from discovery (P-06 uniform length)">
- **Dependencies:** <none | depends on Round N>

#### Fix 1.1 — <short descriptor>

- **Location:** `<file>`, §<X.Y> (p. <N>, line <L>)
- **Pattern category:** <P-NN or C-NN>
- **Risk tier:** A
- **Rule reference:** `rules/<en|zh>/<file>.md#<pattern-id>`

**BEFORE (verbatim from v<14>):**
> <exact string, character-for-character — preserve LaTeX commands, citation
> brackets, footnote markers, whitespace as much as possible. The executor will
> match this string literally.>

**AFTER (proposed for v<15>):**
> <exact replacement string. This is what gets written into the document.>

**Rationale:** <one sentence explaining what AI-signal this fix removes>

**Anti-regression check:**
- vs v<10>: <"differs substantially — v10 used phrasing X; the AFTER uses phrasing Y">
- vs v<12>: <"differs — v12 used first person; AFTER is third person past tense">
- <Add a line per prior version>

**Technical-fidelity check:**
- Numbers in edit region: <list, all unchanged>
- Citations in edit region: <list, all unchanged>
- Equation references in edit region: <list, all unchanged>
- If any of the above would be touched by the AFTER string: STOP, flag in Open
  Questions, do NOT include this fix.

#### Fix 1.2 — <short descriptor>

<same structure>

#### Fix 1.N — <short descriptor>

<same structure>

---

### Round 2 — <short descriptor>

<same structure as Round 1>

#### Fix 2.1 — <descriptor>

…

---

### Round 3 — <short descriptor>

<same structure>

---

### Round 4 — <short descriptor> (Tier C, block rewrites)

- **Tier:** C
- **Scope:** full-paragraph or full-section replacements
- **Fix count:** <N>
- **Expected risk:** high — these must be word-by-word approved by the user
  during this planning review; do not defer review to execution time.

#### Fix 4.1 — Abstract full replacement

- **Location:** `<file>`, Abstract section
- **Risk tier:** C
- **Rule reference:** <multiple applicable: P-NN, P-MM, …>

**BEFORE (full paragraph 1, verbatim):**
> <entire paragraph as it currently appears>

**AFTER (full paragraph 1, proposed):**
> <entire replacement paragraph>

**BEFORE (full paragraph 2, verbatim):**
> <entire paragraph as it currently appears>

**AFTER (full paragraph 2, proposed):**
> <entire replacement paragraph>

<!-- Continue per paragraph within the block. Each paragraph's BEFORE/AFTER is
     a separate diff so the executor can apply them independently if any one
     fails preflight. -->

**Rationale:** <what structural changes were made — e.g., "removed list-subject
construction in paragraph 1; normalised tense from present to past throughout;
broke the three-sentence fragment chain in paragraph 3 into one compound
sentence and one emphatic short sentence">

**Anti-regression check:**
- vs v<10>: <explicit comparison — "opens with 'presented' vs v10's 'investigated';
  the phrase 'matched the validated hardcoded baseline' used in both v10 and v12
  is avoided; closing sentence is restructured">
- vs v<12>: <explicit comparison — "v12 opens with first-person 'I built'; AFTER
  is third-person 'This dissertation presented'">

**Technical-fidelity check:** <list every number and citation appearing in the
block; confirm all unchanged in AFTER>

#### Fix 4.2 — Conclusion §6.1 opening paragraph

<same structure>

---

### Round 5 — Audit

- **Tier:** — (verification only)
- **Scope:** No new edits. Verify the document state after Rounds 1–4.

**Audit checklist (executor runs in Layer 2):**

- [ ] Grep for every P-NN / C-NN pattern from discovery; record residual hit counts.
- [ ] Diff guardrail list against the document; confirm byte-identical for every item.
- [ ] Diff against v<10> and v<12>; confirm no AFTER string drifted toward either prior version.
- [ ] Run the final detector measurement (user).
- [ ] Produce `CHANGES_summary.md` aggregating all rounds' deltas.

**Expected outcome:** clean grep (< 3 residual hits per pattern, none high-severity),
guardrails preserved, detector score in target range.

---

## 4. Anti-Regression Summary

<!--
  Aggregate view of the anti-regression checks from all fixes above.
  List any AFTER string whose token overlap with a prior version exceeded 40%
  over any 10-word window. For each, note whether Layer 1 rewrote it a second
  time, and the current status.
-->

**Fixes requiring second rewrite to avoid drifting toward prior version:**

- Fix <N.M>: initial AFTER had <X>% overlap with v<Y>; rewrote to achieve <new>% overlap. Current AFTER shown in the fix block.
- <continue>

**Fixes where user must choose between two rewrites:** <list in Open Questions>

**If no regressions occurred:** "All AFTER strings pass the anti-regression threshold (<40% overlap with any prior version over 10-word windows)."

---

## 5. Measurement Protocol

- **Detector(s):** <list, e.g., "GPTZero (primary), Turnitin AI (secondary)">
- **Metrics recorded per round:** <e.g., "AI probability %, perplexity, burstiness score (if GPTZero), similarity score vs v10">
- **Success threshold per round:**
  - Round 1 (Tier A): AI probability should drop by ≥ <N> pp; if not, pause and diagnose.
  - Round 2 (Tier B): AI probability should drop by ≥ <N> pp.
  - Round 3 (Tier A+D): ≥ <N> pp or clean residual grep; whichever first.
  - Round 4 (Tier C): qualitative — block rewrites should look natural; AI score is a secondary signal.
  - Round 5 (Audit): no regressions expected; final measurement for report.
- **Similarity checker:** <tool, e.g., "Turnitin similarity, or local diff-based token overlap">
- **Similarity target:** <X>% vs v<10> <= <threshold>
- **Between-round action (for user):**
  1. Commit the round's changes.
  2. Compile the document.
  3. Run the detector(s).
  4. Run similarity checker vs prior versions.
  5. Record in `CHANGES_roundN.md` §5 Measurement.
  6. Decide whether to proceed, pause, or rollback.

---

## 6. Open Questions

<!--
  Anything Layer 1 could not resolve without user input. Do NOT proceed to
  Layer 2 until these are resolved (either inline here or through a user
  response that updates this file).
-->

1. **<question summary>**
   - Context: <why Layer 1 paused>
   - Options: A: <...>, B: <...>
   - Default if no answer by Round <N>: <...>
2. **<question summary>** …

<!-- If no open questions: "No open questions — plan is ready for approval." -->

---

## Reviewer checklist

Before the user approves this plan:

- [ ] Round roster covers every pattern from `discovery.md` §3 (or explicitly defers it with rationale).
- [ ] No round mixes tiers.
- [ ] Every Tier A/B/D fix has a verbatim BEFORE string and a proposed AFTER string.
- [ ] Every Tier C fix has full-paragraph BEFORE/AFTER per paragraph.
- [ ] Anti-regression check is present for every fix.
- [ ] Technical-fidelity check is present for every fix.
- [ ] Guardrails section was copied verbatim from discovery.
- [ ] Measurement protocol is specific and testable per round.
- [ ] Open Questions are answerable with a single user response.

Once approved, invoke Layer 2 one round at a time.
