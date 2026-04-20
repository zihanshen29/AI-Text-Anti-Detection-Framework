# Layer 2 — Execution

> **Entered from:** `SKILL.md` after Layer 1 approval, or directly if the user has an approved `plan.md`.
> **Consumes:** `plan.md` produced by Layer 1.
> **Produces:** One `CHANGES_roundN.md` per round, and a final `CHANGES_summary.md` when all rounds complete.
> **Invocation model:** One call per round. Never batch multiple rounds in one call.

## Purpose

Layer 2 applies the edits from `plan.md` to the actual document. It is deliberately the least creative layer in this skill — its job is to be boring and exact. All the creative work happened in Layer 1; Layer 2 only executes.

Three responsibilities:

1. **Apply one round's edits as exact string replacements**, with no improvisation.
2. **Produce a per-round changelog** that can be diffed, audited, and rolled back.
3. **Force a measurement checkpoint between rounds** so that detector-score deltas are recorded and the next round's decision is informed.

## Why this layer exists as its own layer

Editing is a different cognitive mode from planning. When the same agent plans and edits in one pass, it drifts: it "sees a better phrasing" mid-edit, or it "notices another issue" and fixes that too, or it "merges two small fixes to save time". Every one of those drifts breaks the audit trail and defeats the round-isolation that makes detector-score deltas interpretable.

Separating execution also makes rollback trivial. If Round 3 makes the detector score worse, we need to know exactly what Round 3 changed. A CHANGES_round3.md with every before/after pair and file location gives us that in seconds.

---

## One-round invocation model

Each Layer 2 call handles **exactly one round**. The user invokes this layer N times across a project, once per round in `plan.md`, with a measurement checkpoint between each call.

```
User: "Run Round 1."
  → Layer 2 executes Round 1
  → Writes CHANGES_round1.md
  → STOPS

User: [compiles, runs detector, records score]
User: "Score dropped from 85% to 62%. Run Round 2."
  → Layer 2 executes Round 2
  → Writes CHANGES_round2.md
  → STOPS

... and so on.
```

Do not ask "should I continue to Round 2?" after finishing Round 1. The answer depends on the detector score, which the skill cannot access. Stop after each round. Wait for the user.

## Step 1 — Load the current round

At invocation, the user specifies which round to run (e.g., "Run Round 3"). Load `plan.md` and extract:

- The round's tier and scope.
- The complete list of fixes for this round, in order.
- The guardrails list.
- The measurement protocol (for reference, though the user runs the detector, not the skill).

If the user does not specify a round number, ask which round. Do not assume.

If `plan.md` does not exist or is unapproved, stop and redirect to Layer 1.

## Step 2 — Pre-flight (read-only)

Before modifying anything, do a read-only pass:

1. Open each file that will be edited in this round (listed in `plan.md`).
2. For each fix in the round, verify the BEFORE string exists in the target file verbatim. Use strict string matching, not fuzzy matching.
3. Record which fixes pass pre-flight and which fail.
4. If any fix fails pre-flight, list them for the user and ask how to proceed. Possible responses:
   - The user updates `plan.md` with the correct BEFORE string, then re-runs the round.
   - The user declares the fix no longer applicable (e.g., a prior round already changed that text) and explicitly drops it.
   - Never attempt to "find something close" and apply it. Fuzzy-matched substitution is the single most dangerous failure mode in string-replacement agents.

Only proceed to Step 3 after pre-flight passes cleanly (or user-approved drops are recorded).

## Step 3 — Announce the edit plan (plan mode)

For coding agents with plan mode (Codex, Cursor, Claude Code, etc.), produce a plan listing:

- Every file that will be edited in this round.
- For each file, every BEFORE string that will be replaced and the line range.
- A confirmation that no guardrail element sits within the edit region.

Wait for user approval of the plan before applying. Plan mode here is mandatory, not optional — it is the last checkpoint before the document is modified.

For agents without explicit plan mode, simulate it: output the plan as text and explicitly ask "proceed?" before calling any edit tool.

## Step 4 — Apply the edits

For each approved fix, in the order listed in `plan.md`:

1. Use a strict string-replacement tool (`str_replace`, `sed`-like exact match, etc.).
2. The BEFORE string must match exactly once. If it matches zero times, the fix was already applied or the pre-flight was wrong — stop and ask. If it matches more than once, the BEFORE string in `plan.md` was insufficiently specific — stop and ask Layer 1 to provide more surrounding context.
3. Replace with the AFTER string exactly as written in `plan.md`. Do not "improve" it mid-application.
4. After each successful replacement, verify the file still parses / compiles if applicable. For LaTeX, a full rebuild is overkill per-edit; a syntactic sanity check (balanced braces in the edit region) is sufficient.

**Forbidden during Step 4:**
- Rewriting a proposed AFTER string because "this phrasing is better."
- Merging two adjacent fixes into one larger fix because "they overlap."
- Adding edits not listed in `plan.md`, even if you spot an AI pattern while reading.
- Skipping a fix because "it doesn't look necessary anymore."

If any of these urges appear, the correct response is to stop, finish the round with only the in-plan fixes, and note the observation in `CHANGES_roundN.md` under an "Observations for future planning" section. Mid-flight plan changes are a reliability hazard.

## Step 5 — Produce `CHANGES_roundN.md`

Use the template at `templates/changes_log.md`. Required sections, numbered to match the template (§0 through §7):

- **§0 Round Header** — round number, tier, scope, invocation timestamp.
- **§1 Pre-Flight Results** — which fixes passed, which failed, any user-approved drops.
- **§2 Applied Edits** — one block per fix, with:
   - Fix ID (matching `plan.md`).
   - File path and line range (post-edit line numbers).
   - BEFORE string (verbatim).
   - AFTER string (verbatim).
   - Application status: applied / skipped (with reason).
- **§3 Guardrail Verification** — explicit confirmation that the guardrail inventory items in the edited regions are byte-identical. Spot-check at least three guardrails per round.
- **§4 Observations for Future Planning** — anything noticed during execution that Layer 1 might want to consider for later rounds (but NOT applied as ad-hoc edits in this round).
- **§5 Measurement** — placeholder for the user to fill after compile + detect. Include fields for: detector name, pre-round score, post-round score, delta, similarity score if applicable, notes. Leave empty when handing off.
- **§6 Decision for Next Round** — placeholder for the user. Lists: proceed / proceed-with-amendments / pause / rollback / skip-to-audit. Leave empty when handing off.
- **§7 Rollback** — only filled if §6 selects rollback. Leave entirely omitted otherwise.

The executor fills §0 through §4. The user fills §5 and §6 after measuring. §7 appears only if rollback occurs.

Save `CHANGES_roundN.md` in the same directory as `plan.md`.

## Step 6 — Hand off for measurement

Present `CHANGES_roundN.md` to the user and request:

- Compile the document and visually sanity-check the edited sections.
- Run the target detector(s) from the measurement protocol in `plan.md`.
- Record the score in the measurement placeholder of `CHANGES_roundN.md`.
- If the document had a prior human version, run the similarity checker and record that score too.
- Decide whether to proceed to the next round.

Then STOP. Do not proactively start the next round.

## Step 7 — When called for the next round

When the user invokes Layer 2 for the next round number, before doing anything else:

1. Read `CHANGES_round{N-1}.md`. Note the recorded detector delta.
2. If the delta is in the wrong direction (score went up instead of down), pause and ask the user. Possible causes: a fix that introduced a new AI pattern, a guardrail violation, or a detector quirk. Do not mechanically proceed into the next round on top of a regression.
3. If the prior round had "Observations for future planning" notes, surface them to the user in case the current round's plan needs amendment.
4. Then proceed with Steps 1–6 for the current round.

## Step 8 — Final round (audit)

The last round in every plan is an audit round with no new edits. In the audit round:

1. Grep the document for every pattern class listed in `discovery.md`. Record residual hit counts.
2. Diff the current document against the original (pre-Layer-2) version and against each prior human version. Verify all guardrail elements are byte-identical.
3. Run the final detector measurement.
4. Produce `CHANGES_summary.md` summarizing every round's delta, residual issues, and any remaining manual polish recommendations.

The audit round is not optional. Skipping it leaves the project in an unverified state.

---

## Strict prohibitions

Layer 2 must never:

- Apply a fix not listed in the current round of `plan.md`.
- Apply a fix with a modified AFTER string from what `plan.md` specifies.
- Continue to the next round without the user's explicit invocation.
- Use fuzzy matching, regex with wildcards, or semantic similarity to locate a BEFORE string. Only exact literal match.
- Modify any element in the guardrail list.
- Touch equations, citation keys, figure/table labels, code identifiers, or numeric values anywhere, even outside the guardrail list.
- "Fix in passing" a pattern noticed during execution. Record it in observations; do not apply.

These are not style preferences. They are the contract that makes the framework auditable. Breaking any of them forfeits the audit trail.

## Rollback procedure

If any round produces a regression or breaks the document:

1. The user reverts the changed files to the previous commit (or to a pre-round snapshot).
2. Layer 2 marks `CHANGES_roundN.md` as "rolled back" with a reason.
3. Either fix the round's plan in `plan.md` and re-run, or skip the round and continue. Do not attempt to partially undo in place — it leaves hybrid state.

This is why every round's CHANGES file records exact BEFORE and AFTER strings: rollback is a pure `str_replace(AFTER, BEFORE)` over the round's file list. If CHANGES is incomplete, rollback is unsafe.

---

## Quality checklist per round

Before declaring a round complete, verify:

- [ ] Every fix in the round was either applied or explicitly dropped with user approval.
- [ ] No edits were made outside the round's declared scope.
- [ ] No guardrail element was modified.
- [ ] `CHANGES_roundN.md` lists every BEFORE/AFTER pair verbatim.
- [ ] The measurement placeholder is present and ready for the user.
- [ ] The document still compiles / parses cleanly.
- [ ] Any observation that might affect future rounds is recorded but not acted on.

## What Layer 2 does NOT do

- It does not plan. If a fix's AFTER string feels wrong, record it and stop; do not rewrite it on the fly.
- It does not diagnose. If a new AI pattern appears in the text, record it for the next Layer 0/1 cycle; do not fix it here.
- It does not measure. The detector is run by the user outside this skill; the skill only reads the recorded score.
- It does not decide round order. `plan.md` is the ordering authority.

## Edge cases

**Pre-flight fails on most fixes.** Usually means `plan.md` was written against a different version of the document than the one currently on disk. Stop, ask the user which file is the source of truth, and route back to Layer 1 to regenerate BEFORE strings against the correct version.

**A fix applies successfully but the surrounding compile breaks.** Likely the AFTER string introduced a LaTeX / Markdown / code syntax issue (unbalanced braces, broken citation macro). Revert that single fix, mark it as failed in `CHANGES_roundN.md`, and continue with the remaining fixes. The user can re-plan that fix in a later iteration.

**The detector score goes down but similarity to a prior version goes up.** The round drifted toward a prior human version despite anti-regression checks in Layer 1. Record it in the observations, stop the round early, and route back to Layer 1 to re-do the anti-regression check for subsequent fixes.

**The user wants to "just do rounds 2 and 3 together to save time."** Decline. Offer to run them back-to-back without the user needing to switch context, but keep them as separate invocations with separate CHANGES files and a measurement between. The audit trail is the product.

**The user invokes Layer 2 without a `plan.md`.** Stop. Redirect to Layer 1. Do not accept an inline list of fixes from chat — it bypasses the planning review and the anti-regression check.

**The document is version-controlled (git).** Commit after each round with a message like `round N: <scope>`. This creates natural rollback points that align with `CHANGES_roundN.md` files.
