# Template: `CHANGES_roundN.md`

<!--
  About this template:
  - Filled by Layer 2 (Execution) after applying one round's fixes.
  - Sections 1–4 are filled by Layer 2 during execution.
  - Sections 5 and 6 are filled by the USER after compiling and running the detector.
  - Produce one of these files per round. Do NOT reuse a file across rounds.
  - File naming: CHANGES_round1.md, CHANGES_round2.md, …
  - At the end of the project, a separate CHANGES_summary.md aggregates all rounds.
-->

# Changes — Round <N>

**Round started:** <YYYY-MM-DD HH:MM>
**Round completed:** <YYYY-MM-DD HH:MM>
**Source plan:** `plan.md` (commit / hash if version-controlled: `<hash>`)
**Prior round:** <`CHANGES_round{N-1}.md` | "first round of project">

---

## 0. Round Header

- **Round number:** <N>
- **Tier:** A | B | C | D | audit
- **Scope (from plan §3):** <copy the one-line scope descriptor>
- **Files touched:** <list>
- **Fix count declared in plan:** <X>
- **Fix count actually applied:** <Y>
- **Fix count skipped / failed:** <X − Y>

---

## 1. Pre-Flight Results

<!--
  Read-only verification pass before any edits. For every fix in this round,
  the executor checked whether the BEFORE string from plan.md matches the
  current document exactly once. Record the outcome below.
-->

**Declared fixes for this round:** <X>
**Passed pre-flight:** <P>
**Failed pre-flight:** <F>

### Failed pre-flight detail

<!-- For each failed fix, state the failure mode. "BEFORE not found" usually
     means a prior round already changed that text, or plan.md has a typo.
     "BEFORE matched N times (N>1)" means plan.md's BEFORE string is not
     unique enough — escalate to re-plan with more surrounding context.
     Never attempt fuzzy fallback. -->

- **Fix <N.M>** — <one-line descriptor from plan>
  - Failure: <"BEFORE not found" | "BEFORE matched N times" | "target file missing" | other>
  - Action: <"dropped with user approval" | "deferred to re-plan" | "superseded by Fix <other>">

### User-approved drops

<!-- Fixes the user explicitly chose to skip during pre-flight review. -->

- **Fix <N.M>** — dropped because <reason as stated by user>

---

## 2. Applied Edits

<!--
  One block per applied fix, in execution order. Use the same Fix IDs as plan.md
  so the two files can be cross-referenced. BEFORE and AFTER strings are copied
  verbatim from plan.md; do NOT paraphrase here.
-->

### Fix <N.M> — <descriptor copied from plan>

- **File:** `<file path>`
- **Post-edit line range:** <L1>–<L2>
  <!-- Line numbers AFTER the edit was applied. This is what the user will
       see when opening the file to review. If multiple edits land in the
       same file, later line numbers may shift from earlier estimates. -->
- **Status:** applied
- **Rule reference:** `rules/<en|zh>/<file>.md#<pattern-id>`

**BEFORE (verbatim, copied from plan):**
> <exact string>

**AFTER (verbatim, copied from plan and applied):**
> <exact string>

**Notes during application:** <usually "none". Record any surprises here — e.g.,
"AFTER string introduced a formatting issue that was resolved by adding a
trailing newline; note for future planning.">

### Fix <N.M+1> — <descriptor>

<same structure>

### Fix <N.P> — <descriptor>

- **File:** `<file path>`
- **Status:** skipped
- **Reason:** <"pre-flight failed: BEFORE not found" | "user-approved drop" | other>

<!-- Skipped fixes still appear in this section so the round's Fix IDs are
     contiguous and the audit trail is complete. -->

---

## 3. Guardrail Verification

<!--
  For every edited region, spot-check that guardrail items are unchanged.
  Confirm at least three representative guardrails per round. If any edited
  region contained a guardrail element, check it explicitly.
-->

**Guardrail items in edited regions:** <list>

**Spot-check results:**

- Numerical value `<value>` at `<location>`: unchanged ✓
- Citation `[<N>]` at `<location>`: unchanged ✓
- Equation reference `<eq:N.M>` at `<location>`: unchanged ✓
- Figure reference `figure <N.M>` at `<location>`: unchanged ✓
- File identifier `<code>` at `<location>`: unchanged ✓

**Overall guardrail status:** all preserved ✓ | **<list violations>**

<!-- If any guardrail item was modified, STOP. Roll back the fix that caused
     it. Do not continue the round with a violated guardrail. Record the
     violation and the rollback in §4 Observations. -->

---

## 4. Observations for Future Planning

<!--
  Things noticed during execution that Layer 0 or Layer 1 might want to
  consider for later rounds. These are NOT applied as ad-hoc edits in this
  round. Recording them here closes the feedback loop without violating the
  "no improvisation" rule.
-->

- <observation 1 — e.g., "Fix 2.3's AFTER introduced a consecutive short-sentence pair
  that triggers P-09 (fragment cluster). Consider adding a Round 4 fix to merge them.">
- <observation 2 — e.g., "Noticed an unflagged instance of 'delve' in §3.4 during
  edit of adjacent paragraph. Not in discovery. Recommend re-running P-16 scan
  before the audit round.">
- <observation 3 — e.g., "The repeated phrase 'also lined up with' appeared three
  times in §5.6 after Round 1's tense sweep. Not a discovery-flagged pattern but
  reads repetitive. Candidate for Round 3 or a novel-pattern entry.">

<!-- If no observations: "No observations for future planning." -->

---

## 5. Measurement (user fills after compile + detect)

<!--
  After the executor finishes Sections 0–4, the user compiles the document,
  runs the detector(s), and fills this section. Do NOT proceed to Round N+1
  until this section is complete.
-->

### Compile status

- [ ] Document compiles without error
- [ ] Visual sanity check of edited sections passed
- **Compile notes:** <any warnings, formatting issues, manual fixes applied>

### Detector A: <name, e.g., GPTZero>

| Metric | Pre-round | Post-round | Delta |
|:---|:---:|:---:|:---:|
| AI probability % | <X> | <Y> | <±Z pp> |
| Perplexity | <X> | <Y> | <±Z> |
| Burstiness | <X> | <Y> | <±Z> |

### Detector B: <name, e.g., Turnitin AI>

| Metric | Pre-round | Post-round | Delta |
|:---|:---:|:---:|:---:|
| AI probability % | <X> | <Y> | <±Z pp> |

### Similarity vs prior versions

| vs version | Pre-round similarity | Post-round similarity | Delta |
|:---|:---:|:---:|:---:|
| v<10> | <X>% | <Y>% | <±Z pp> |
| v<12> | <X>% | <Y>% | <±Z pp> |

<!-- Similarity going UP after a round means the rewrite drifted toward an
     older human version — a failed anti-regression check. Investigate before
     proceeding to the next round. -->

### Round-success evaluation (against plan §5 threshold)

- **Threshold from plan:** <quote, e.g., "AI probability should drop by ≥ 10 pp">
- **Observed delta:** <value>
- **Verdict:** met | partially met | not met

### User notes

<free text — anything unexpected, qualitative observations, decisions about
manual touch-ups the user applied outside the plan>

---

## 6. Decision for Next Round (user fills)

<!-- Based on §5, the user decides how to proceed. -->

Select one:

- [ ] **Proceed to Round <N+1>** as planned
- [ ] **Proceed to Round <N+1>** with plan amendments (describe below)
- [ ] **Pause** — re-diagnose before continuing (return to Layer 0 or Layer 1)
- [ ] **Rollback** this round (see §7 below)
- [ ] **Skip** to audit round (project effectively complete after this round)

**Reasoning:** <one to three sentences>

**Plan amendments for next round (if any):** <describe which fixes to add, drop,
or modify in plan.md before Round N+1 begins>

---

## 7. Rollback (only fill if rolling this round back)

<!--
  If §6 selected "Rollback", record the rollback here. Rollback procedure:
  1. User reverts the changed files to the pre-round state (git revert or
     manual str_replace(AFTER, BEFORE) for each fix in §2).
  2. Record the rollback timestamp and reason here.
  3. Either re-plan this round's fixes (return to Layer 1) or skip the round.
-->

- **Rollback timestamp:** <YYYY-MM-DD HH:MM>
- **Rollback method:** <"git revert <commit>" | "manual str_replace per fix" | other>
- **Reason:** <detector score went up | guardrail violation | compile broke | other>
- **Next action:** <"re-plan this round in Layer 1 with amended BEFORE strings" |
  "skip this round entirely" | other>
- **Lesson recorded for future planning:** <one sentence>

---

## Quality checklist (executor confirms before handing off)

- [ ] Every declared fix has a block in §2 (applied or explicitly skipped).
- [ ] No edits were made outside the round's declared scope in plan.md.
- [ ] No guardrail item was modified (§3 shows all preserved).
- [ ] Every BEFORE/AFTER pair in §2 is verbatim from plan.md (not paraphrased).
- [ ] §4 Observations captures any mid-flight urge that was resisted.
- [ ] §5 and §6 are left as placeholders for the user.
- [ ] Document still compiles / parses after all applied fixes.
- [ ] File saved as `CHANGES_round<N>.md` with the correct round number.

---

## Appendix (optional): full diff

<!-- If version control is available, the full diff of the round can be pasted
     here as a reference. This is optional — §2 already records every change
     by Fix ID, which is the primary audit trail. The diff is a secondary
     convenience for visual review. -->

```diff
<paste `git diff HEAD~1..HEAD` or equivalent>
```
