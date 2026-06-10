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

Also load (read-only, do not re-scan the whole document) the language-matched rule files: `rules/{en|zh}/*`. These contain canonical rewrite templates — Layer 1 uses them as starting points for before/after pairs, not as verdicts. For Chinese documents, `rules/zh/context_whitelist.md` is mandatory and must be used before writing any C-NN or S-NN fix.

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

Round 4 fixes still require sentence-level exact BEFORE/AFTER strings. If a burstiness change needs multi-sentence linked restructuring, classify it as Tier C and move it to Round 5.

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
Context whitelist check: <Chinese only; note checked, whitelisted:true, whitelisted:review, or not applicable>
Naturalness preflight: <pass / revise / open question, with one sentence; include replacement blacklist/guidance checks where applicable>
AFTER secondary scan: <pass / revise / open question, rules checked and any hits>
```

For Tier C (block rewrite) fixes, the BEFORE block may be a full paragraph. The AFTER block is the full replacement paragraph. The Rationale section explains what structural change was made (e.g., "removed list-subject construction in sentence 2; normalized tense; broke three-sentence fragment chain into two sentences of differing length").

**Exact-string discipline.** The BEFORE text must be character-for-character identical to the current document, including LaTeX commands, footnote markers, and line breaks. If the executor cannot find the BEFORE string verbatim in the document, the fix fails and the user is notified — no fuzzy matching. This is the single most common failure mode of one-shot rewriters; eliminate it here.

### Step 4.1 — P0.4 Chinese context defense

Before proposing an AFTER string for any Chinese C-NN or S-NN hit:

1. Re-check the BEFORE string against `rules/zh/context_whitelist.md`.
2. If the hit is `whitelisted: true`, do not create a mechanical fix. Record the item as deferred/intentional in the plan summary.
3. If the hit is `whitelisted: review`, either write a phrase-level or pair-level fix with exact BEFORE/AFTER, or move it to Open Questions. Do not substring-replace the trigger.
4. For paired structures such as `一方面...另一方面` or `不仅...而且`, the BEFORE string must include the full pair if the plan changes it.

### Step 4.2 — P0.5 AFTER secondary rule scan

After drafting every AFTER string, scan the AFTER itself for newly introduced AI signals before adding the fix to `plan.md`.

This check must catch the failure mode where a fix removes one rule hit but creates another, such as replacing a phrase with a balanced P-08/C-09 structure or a new high-risk cliche.

Efficiency rule: do not run the full rule library blindly for every fix. Scan the high-yield subset:

- Rules already detected in this document by Layer 0.
- The rule family of the original hit.
- Universal high-frequency rules: take every rule with `frequency: high` from `rules/<lang>/rules.yaml`. Current snapshot, with YAML as the source of truth: English `P-01`, `P-04`, `P-06`, `P-08`, `P-12`, `P-16`, `P-19`, `V-01`, `V-02`, `V-03`, `V-08`, `V-11`, `V-19`, `V-20`; Chinese `C-01`, `C-04`, `C-05`, `C-06`, `C-08`, `C-09`, `C-12`, `C-14`, `S-01`, `S-04`, `S-06`, `S-11`, `S-12`, `S-14`.

If the AFTER string hits any scanned rule:

1. Rewrite the AFTER once and scan again.
2. If the second version still hits a rule, either justify why the hit is factual/genre-legitimate or move the fix to Open Questions.
3. Record the result in the fix block under `AFTER secondary scan`.

### Step 4.3 — Naturalness and meaning preflight

Each fix must pass three quick checks before it enters the plan:

- **Grammar/naturalness:** the AFTER must not create an obvious malformed phrase or register break.
- **Meaning/terminology:** the AFTER must not flatten a technical term, fixed compound, proper noun, or domain term.
- **Genre fit:** the AFTER must match the genre recorded in `discovery.md`; a conversational replacement may be acceptable in an essay but not in a policy report.
- **Replacement blacklist/guidance:** Chinese AFTER strings must be checked against `rules/zh/replacement_blacklist.md`; English AFTER strings must be checked against `rules/en/replacement_guidance.md`. Hard-prohibited replacement products must be rewritten. Disfavored Chinese replacements require a one-sentence justification at the fix site.

If any check fails, revise the AFTER or move the item to Open Questions. Do not leave the repair burden to Layer 2.

### Step 4.4 — Replacement diversity check (plan-level)

After all fix blocks are drafted, aggregate AFTER strings by rule family. If a family has four or more fixes and more than 50% of them use the same replacement word or the same sentence structure, diversify the replacements or justify the convergence in `plan.md` §4.

Record the result with the anti-regression summary so Layer 2 sees the plan-level constraint, not only per-fix checks.

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

**If the user has no access to an external detector:** the round can still proceed using offline rule-hit counts as a proxy signal. In this case the plan must state `measurement_type: offline_rule_hits` and every round's success threshold must be defined in terms of rule-hit reduction (e.g., "Round 1 should reduce P-06 hit count by at least 5"), not detector-score reduction. The plan must NOT specify percentage drops in detector scores when no detector is being run.

Without a measurement protocol the rounds are untestable. This is the second most common failure mode of humanizer frameworks — they rewrite but never verify.

## Step 8 — Write `plan.md`

Use the template at `templates/plan_output.md`. Required sections, numbered to match the template (§0 through §6):

- **§0 Meta** — document path, language, genre, target detector(s), round count.
- **§1 Guardrails** — technical-fidelity inventory copied from discovery.
- **§2 Round Roster** — table of rounds with tier, scope, and justification.
- **§3 Per-Round Fix Plans** — the fix-block format from Step 4 for every fix.
- **§4 Anti-Regression Summary** — aggregate view of prior-version overlap checks.
- **§5 Measurement Protocol** — Step 7.
- **§6 Open Questions** — any fix the planner could not resolve without user input.

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
- [ ] Context whitelist checks are done for every Chinese C-NN/S-NN fix.
- [ ] AFTER secondary scans are done for every proposed AFTER against the high-yield rule subset.
- [ ] Naturalness, meaning, and genre preflight checks are recorded for every fix.
- [ ] Chinese replacement blacklist / English replacement guidance checks are recorded where applicable.
- [ ] Replacement diversity check is recorded in `plan.md` §4 for any rule family with four or more fixes.
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
