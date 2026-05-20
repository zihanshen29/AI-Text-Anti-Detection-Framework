# Workflow Patch Recommendations - 2026-05-21

## Accepted Changes

### P0.4 - Chinese Context Whitelist

Status: implemented as a two-layer defense.

- Layer 0 filters obvious fixed contexts using `rules/zh/context_whitelist.md`.
- Layer 1 re-checks every Chinese C-NN/S-NN fix before writing BEFORE/AFTER.
- Ambiguous hits are marked `whitelisted: review` rather than passed to Layer 2 as mechanical replacements.

Primary failures addressed:

- `生态环境` must not become `协作体系环境`.
- `不仅仅` must not become `不只仅`.
- `一方面...另一方面` must not be edited one side at a time.
- `对 X 进行 Y` should be targeted, while normal uses such as `进行得很顺利` should not.

### P0.5 - AFTER Secondary Rule Scan

Status: implemented in Layer 1 planning instructions and plan template.

Every proposed AFTER string now needs a secondary scan before it enters `plan.md`. If the AFTER introduces another high-risk rule hit, Layer 1 must revise once, justify the residual, or move the fix to Open Questions.

### P1.1 - Batch Evaluation Template

Status: implemented in `templates/batch_eval_output.md` and `meta/prompts/eval_prompt.md`.

Added:

- `signal_vs_naturalness_balance`
- outlier rule: `total < 25/35` or any hard-fail flag excludes the sample from aggregate averages, while keeping it visible in the report
- explicit `/35` rubric scale
- reminder that offline scores are not external detector scores

## P1.2 - Layer 1 Secondary-Scan Cost Control

Status: implemented as guidance in `workflow/planning.md`; keep monitoring in future runs.

Problem:

If Layer 1 scans every AFTER against the full English and Chinese rule libraries, planning cost grows quickly. A 10-fix plan can become 20+ full scans, raising token cost, latency, and prompt complexity.

Decision:

Layer 1 should scan only the high-yield subset:

- Rules already detected in the document by Layer 0.
- The rule family of the original hit.
- Universal high-frequency rules:
  - English: `P-01`, `P-04`, `P-06`, `P-08`, `P-12`, `P-16`, `P-19`, `V-01`, `V-02`, `V-03`, `V-08`, `V-11`, `V-19`, `V-20`.
  - Chinese: `C-01`, `C-04`, `C-05`, `C-06`, `C-08`, `C-09`, `C-12`, `C-14`, `S-01`, `S-04`, `S-06`, `S-11`, `S-12`, `S-14`.

Rationale:

This catches the known second-order failure mode, where a fix removes one signal but introduces another, without forcing Layer 1 to run every low-frequency rule on every tiny AFTER string.

## Follow-Up

After the next real-document run, inspect the `Context Whitelist / Exemption Log` and `AFTER secondary scan` fields. If new context-sensitive Chinese failures appear, add them to `rules/zh/context_whitelist.md` before adding more replacement candidates.
