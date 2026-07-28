---
name: ai-detection-workflow
description: Run a deterministic, offline three-layer editing workflow that preserves technical fidelity and records reviewable evidence.
---

# AI Detection Workflow

**Workflow contract:** `workflow/contract.json` is the sole machine-readable
policy for this workflow. Active instructions, templates, and runtime gates
must agree with it.

This workflow does not call, simulate, or predict external detector results.
Its offline evidence is limited to deterministic rule, structure, fidelity, and
overlap checks.

## Layers

1. **Layer 0 - Discovery.** Run `workflow_check.py discovery` before handing
   the document to planning. Rule hits are evidence, not a failed discovery.
2. **Layer 1 - Planning.** A plan can request approval only after
   `workflow_check.py plan --round all` reports an executable plan.
3. **Layer 2 - Execution.** Before any edit, run snapshot preflight for the
   selected round. After the round, run `workflow_check.py post-round` and
   record its JSON evidence in CHANGES.

Discovery may recommend zero edits. Once Layer 2 runs, the full plan has 3/5/7
total rounds, the final round is audit-only, and the final audit is required.

## Editing Contract

- Every fix has an exact BEFORE and AFTER quotation.
- Editing risk tiers are A, B, and C. A sweep is a planning method, never a
  risk tier; every sweep result becomes an enumerated A/B/C fix before approval.
- An edit round contains one risk tier only.
- Anti-regression compares ten-token windows at the 0.70 threshold.
- Any parse, encoding, application, or guardrail failure rolls back the whole
  round and stops that round. Do not continue with later fixes.
- Layer 2 evidence includes rule scans, structural metrics, fidelity checks,
  and any configured prior-version overlap check.

## Batch Evaluation

The primary batch mean and median include every valid input. A result below
25/35 or with a hard-fail flag remains in that population. Only input-invalid
cases are outside the primary population, and each requires a recorded reason.
Success-only summaries are diagnostic only and cannot be headline results.

## Tooling

Use the standard-library tools in `tools/` from the workflow root. Their JSON
outputs are deterministic evidence, not detector evidence. See
`workflow/discovery.md`, `workflow/planning.md`, and `workflow/execution.md`
for the layer-specific gate sequence.
