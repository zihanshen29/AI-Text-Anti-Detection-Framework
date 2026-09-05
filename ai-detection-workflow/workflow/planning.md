# Layer 1 - Planning

**Workflow contract:** `workflow/contract.json` is authoritative. Do not
replace its decisions with informal exceptions.

Planning turns Layer 0 evidence into an executable multi-file plan. It does
not edit target files or call external detectors.

## Required Gate

```powershell
python .\tools\workflow_check.py plan --plan <plan-path> --round all --project-root <project-root> --snapshot-dir <snapshot-parent> --output <baseline-manifest.json>
```

Approval is blocked unless this command exits 0. Each target must resolve
inside `project-root`; path escapes, ambiguous BEFORE strings, and unacknowledged
AFTER hits are blocking review findings.

The all-round gate simulates exact edits in execution order without changing
the documents. Save this complete baseline before the first edit: the final
audit uses it to replay the full plan. If the plan changes before execution,
regenerate the baseline and its approval record. A selected edit round checks
the current document state after the preceding rounds.

Carry discovery's manual-rule checklist into planning. Record the applicable
sentence-level judgments; a zero automatic hit count is not a manual-rule pass.

## Plan Rules

- If Layer 2 will run, declare 3/5/7 total rounds and make the final round
  audit-only.
- Every editing round has a single A, B, or C risk tier. Sweeps must be
  expanded into individual fixes before approval.
- Each fix declares target file, language for mixed plans, exact BEFORE and
  AFTER quote blocks, and a secondary-scan disposition.
- The plan uses the ten-token 0.70 anti-regression setting from the contract.
- A hard preflight or post-round fidelity result requires whole-round rollback
  and stops the round. Later fixes cannot continue.

Use `templates/plan_output.md` and preserve the required headings and fields.
The JSON preflight output is part of the approval record.
