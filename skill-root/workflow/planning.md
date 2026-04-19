# Layer 1 — Planning

> **Entered from:** `SKILL.md` (after Layer 0 completes) or directly if the user already has a `discovery.md`.
> **Consumes:** `discovery.md` produced by Layer 0.
> **Produces:** `plan.md` in the project working directory.
> **Gates:** Layer 2 (Execution) cannot begin until the user has approved `plan.md`.

## Purpose

Layer 1 turns a diagnosis into an execution plan. It does three things:

1. **Classify every detected pattern by risk tier** — mechanical vs. definition-dependent vs. block-rewrite.
2. **Group fixes into rounds** such that each round targets exactly one class of change, so detection-score deltas between rounds remain interpretable.
3. **Produce exact before/after strings for every fix** — Layer 2 is a string-replacement layer, not a creative layer, and it can only execute if planning has done the creative work here.

The output is a single file, `plan.md`, that the user reviews before any editing begins. If the user objects to a specific rewrite, fix it here — not during execution.

## Why this layer exists

A diagnosis is not a plan. Discovery tells us "the document has 14 fragment sentences, 22 tense slips, and 6 AI clichés." That alone does not tell an executor:

- Which of these can safely be merged (some fragments are emphatic and intentional)?
- In what order should they be fixed (tense first, because it affects every later rewrite)?
- What replacement wording avoids both the AI pattern AND any prior human version (anti-regression)?
- Which equations/citations/numbers sit near each edit and must not be disturbed?

A one-shot humanizer skips these questions and hopes. A structured framework answers them explicitly, in writing, before any edit touches the document.

---

## Step 1 — Load `discovery.md`

Read `discovery.md` completely. Extract:

- The language and genre (determines rule-library conventions).
- The external constraints block (these override any generic rewrite advice).
- The detected AI patterns list with verbatim quotes and locations.
- The technical-fidelity inventory (the guardrails).
- Any open questions the user answered after reviewing discovery.

If any section is missing or ambiguous, stop and send the user back to Layer 0 to fix it. Do not improvise.

Also load (read-only, do not re-scan) the language-matched rule files: `rules/{en|zh}/*`. These contain canonical rewrite templates — Layer 1 uses them as starting points for before/after pairs, not as verdicts.

## Step 2 — Classify fixes by risk tier

For every detected pattern in `discovery.md`, assign a tier:

**Tier A — Mechanical.** The edit is a deterministic string transformation. No judgment required.
- Example (EN): tense slip `MPC offers` → `MPC offered` within Chapter 2 body text.
- Example (ZH): 移除固定 AI 套语「综上所述」→ 上下文重写为更自然的总结。
- Risk: low. Can be batched heavily.

**Tier B — Definition-dependent.** The edit requires reading surrounding context to decide the right replacement. The pattern is concrete but the fix is not 1:1.
- Example (EN): fragment merging — "Feet leave. Feet return." merges correctly only if the merged sentence preserves the emphatic quality and the citation position.
- Example (ZH): 四字词组堆叠「全面提升深入优化」的改写，需要看具体语义决定拆分还是替换。
- Risk: medium. Each edit needs an exact before/after in `plan.md` because executors cannot safely improvise.

**Tier C — Block rewrite.** The edit is an entire paragraph or section replacement. Multiple sentences change at once, so the edit can only be reviewed as a block.
- Example: Abstract rewrite (single paragraph, 100–200 words).
- Example: Conclusion §6.1 opening paragraph rewrite.
- Risk: high. These must be reviewed word-by-word by the user during planning, not during execution.

**Tier D — Sweeps.** Global grep-and-review for a pattern class. Each individual hit is Tier A, but the sweep exists because the pattern count is unknown until the executor reads the file.
- Example (EN): final sweep for any remaining present-tense auxiliary (`\bis\b`, `\bare\b`) in Chapters 1–6 after Round 1's targeted fixes.
- Example (ZH): 全局扫描未列举的 AI 连接词残留。
- Risk: low–medium. Requires the executor to list every hit before applying changes, so the user can veto.

Record the tier for every fix. The round grouping in Step 3 uses these tiers.

## Step 3 — Group fixes into rounds

Each round targets **one tier** — never mix tiers within a round. Mixing makes the detector-score delta uninterpretable and makes errors hard to isolate.

### Standard 5-round plan (default)

| Round | Tier | Scope |
|:---:|:---:|:---|
| 1 | A | Hard-rule compliance — tense unification, voice normalization, first-person removal. Pure string substitutions. |
| 2 | B | Fragment merging and definition-dependent fixes with exact before/after pairs. |
| 3 | A + D | Cliché vocabulary removal (A for listed phrases, D for sweep of unlisted hits). |
| 4 | C | Block rewrites of structurally important sections (Abstract, Conclusion §6.1, or equivalents). |
| 5 | — | Verification and audit. No new edits. Grep for remaining patterns, diff against earlier versions, confirm technical fidelity. |

### Light 3-round plan

Use when discovery reports fewer than 15 total hits and the user's target detector score is close to acceptable.

| Round | Tier | Scope |
|:---:|:---:|:---|
| 1 | A | Hard-rule compliance only. |
| 2 | B | Fragment merging. |
| 3 | — | Audit. |

### Heavy 7-round plan

Use when discovery reports more than 40 total hits or when the user reports a high detector score (> 70% AI) despite prior rewrites.

| Round | Tier | Scope |
|:---:|:---:|:---|
| 1 | A | Mechanical compliance sweep. |
| 2 | A | Vocabulary cliché removal (list-based). |
| 3 | B | Fragment merging. |
| 4 | B | Sentence-rhythm diversification (burstiness injection). |
| 5 | C | Block rewrites. |
| 6 | D | Final grep sweep for residual patterns. |
| 7 | — | Audit. |

The user may request a custom round count. Accept it, but do not mix tiers within a round regardless of count.

## Step 4 — Produce exact before/after for every fix

For each Tier A, B, or D fix, write a block with this structure:

```
### Fix N.M — <short descriptor>

Section / page: §X.Y (p. N)
Pattern category: <from discovery>
Risk tier: A | B | C | D

BEFORE (verbatim from current document):
> <exact string, preserving whitespace, punctuation, citations>

AFTER (proposed):
> <exact replacement string>

Rationale: <one sentence>
Anti-regression check: <note whether this wording differs from v10/v12/prior versions>
Technical-fidelity check: <list any numbers, citations, equation refs in the edit region>
```

For Tier C (block rewrite) fixes, the BEFORE block may be a full paragraph. The AFTER block is the full replacement paragraph. The Rationale section explains what structural change was made (e.g., "removed list-subject construction in sentence 2; normalized tense; broke three-sentence fragment chain into two sentences of differing length").

**Exact-string discipline.** The BEFORE text must be character-for-character identical to the current document, including LaTeX commands, footnote markers, and line breaks. If the executor cannot find the BEFORE string verbatim in the document, the fix fails and the user is notified — no fuzzy matching. This is the single most common failure mode of one-shot rewriters; eliminate it here.

## Step 5 — Anti-regression check against prior versions

If the user supplied earlier versions (v10, v12, …) in Layer 0, scan each proposed AFTER string against each prior version. If an AFTER string closely matches a prior version's phrasing (> 70% token overlap over a 10-word window), rewrite it once more. Note this in the fix block.

This matters because AI-detection scores and similarity scores move in opposite directions only when the new wording is genuinely new. A "rewrite" that reverts to an earlier human draft looks great to the AI detector but terrible to the similarity detector. We need both to pass.

## Step 6 — Declare the guardrails (copy from discovery)

At the top of `plan.md`, copy the technical-fidelity inventory from `discovery.md` verbatim. This becomes the Layer 2 contract: anything listed here must be byte-identical before and after every round. If a proposed fix would alter a guardrail element, flag it, do not silently include it.

## Step 7 — Declare the measurement protocol

At the end of `plan.md`, declare how the user will measure between rounds:

- Which detector(s) will be run.
- Which score metric counts (AI probability, similarity, perplexity).
- What counts as success for each round (e.g., "Round 1 should reduce AI probability by at least 10 points; if it doesn't, pause and diagnose before Round 2").
- What the user records after each round (score, unexpected issues, any manual touch-ups).

Without a measurement protocol the rounds are untestable. This is the second most common failure mode of humanizer frameworks — they rewrite but never verify.

## Step 8 — Write `plan.md`

Use the template at `templates/plan_output.md`. Required sections in order:

1. **Meta** — document path, language, genre, target detector(s), round count.
2. **Guardrails** — technical-fidelity inventory copied from discovery.
3. **Round roster** — table of rounds with tier, scope, and justification.
4. **Per-round fix blocks** — Step 4 format for every fix.
5. **Anti-regression notes** — summary of prior-version overlap checks.
6. **Measurement protocol** — Step 7.
7. **Open questions** — any fix the planner could not resolve without user input.

## Step 9 — Hand off to the user

Present `plan.md` to the user. Ask them to:

- Scan the round roster — does the grouping feel right?
- Spot-check 3–5 fix blocks from different rounds — are the proposed AFTER strings what they want?
- Flag any fix to drop, modify, or promote to a different round.
- Approve the measurement protocol or suggest adjustments.
- Confirm the guardrails list is complete.

Do not enter Layer 2 until the user explicitly approves. Silence is not approval.

---

## Quality checklist for Layer 1

Before handing off `plan.md`, verify:

- [ ] Every detected pattern from `discovery.md` is either addressed in the plan or explicitly marked "deferred / intentional / not a fix".
- [ ] Every Tier A/B/D fix has a verbatim BEFORE string and a proposed AFTER string.
- [ ] Every Tier C fix has a full-paragraph BEFORE and AFTER.
- [ ] No round mixes tiers.
- [ ] Anti-regression checks are done for every proposed AFTER.
- [ ] The guardrails list is present and copied correctly from discovery.
- [ ] The measurement protocol is explicit and testable.
- [ ] File is saved as `plan.md` in the correct directory.

If any box is unchecked, loop back and fix it. An under-specified plan forces Layer 2 to improvise, which is exactly the failure mode this skill was built to prevent.

## What Layer 1 does NOT do

- It does not re-scan the document for AI patterns. That was Layer 0's job. If Layer 1 finds a new pattern mid-planning, the correct response is to amend `discovery.md` and restart Layer 1 — not to silently add the fix.
- It does not touch the document.
- It does not run the detector.
- It does not merge rounds to "save time". Rounds are separated for a reason.

## Edge cases

**Discovery lists a pattern the planner doesn't know how to fix.** Record it in the Open Questions section with a note ("candidate patterns, no obvious rewrite"). Either ask the user or defer the fix to a future round. Do not skip it silently.

**Two fixes conflict — applying one changes the BEFORE string of the other.** Order them explicitly within the round. Mark the downstream fix with "depends on Fix N.M" and note the post-dependency BEFORE string.

**A proposed AFTER string violates a guardrail (touches a number, shifts a citation).** Reject the fix and either (a) redesign it to leave the guardrail intact, or (b) demote to Open Questions for user decision. Never quietly move the guardrail.

**User wants to approve with changes.** Apply the user's changes to `plan.md` first, then begin Layer 2. Do not let verbal amendments live only in chat history — they won't survive into the next round.

**User approves only some rounds.** Fine. Layer 2 can run round-by-round with pauses. Mark unapproved rounds as "pending approval" and stop after each approved round for re-review.
