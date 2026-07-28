# Offline Tooling

These standard-library tools produce deterministic workflow evidence. They do
not call external AI detectors, simulate scores, or claim detector correlation.
The governing policy is `workflow/contract.json`.

## Exit Codes

- `0`: a complete gate or metric run with no blocking result;
- `1`: a completed scan, plan, or post-round gate that needs review or
  whole-round rollback; and
- `2`: a tool, encoding, path, configuration, or manifest error.

## Core Commands

Run commands from `ai-detection-workflow` on PowerShell:

```powershell
python .\tools\workflow_check.py discovery --text <document> --lang auto --output <discovery.json>
python .\tools\workflow_check.py plan --plan <plan.md> --round all --project-root <project-root> --output <plan.json>
python .\tools\workflow_check.py plan --plan <plan.md> --round <N> --project-root <project-root> --snapshot-dir <snapshots> --output <plan-manifest.json>
python .\tools\workflow_check.py post-round --manifest <plan-manifest.json> --output <post-round.json>
```

Layer 0 handoff requires discovery JSON. Layer 1 approval requires a successful
`plan --round all` gate. Layer 2 editing requires a successful snapshot gate;
Layer 2 handoff requires `post-round` evidence. JSON output labels every
runtime hash as `worktree_raw_sha256` and records `external_detector_status:
not_run`.

## Supporting Tools

- `scan_rules.py`: context-aware rule spans and actionable unique-span totals.
- `structure_metrics.py`: deterministic structural proxy metrics.
- `preflight_plan.py`: direct plan preflight; `--doc` preserves the legacy
  single-file BEFORE-count mode.
- `guardrails_diff.py`: source/rewrite fidelity checks.
- `overlap_check.py`: exact token-postings overlap evidence using the ten-token
  0.70 contract threshold when called by workflow gates. Ordinary inputs avoid
  the old all-window scan; a degenerate corpus dominated by one repeated token
  can still create enough candidates to approach quadratic work.
- `lint_repository.py`: `rules`, `contract`, `gates`, or `all` active-policy
  lint modes.

The post-round gate requires whole-round rollback for hard identity, encoding,
path, or fidelity failures. Rule regressions, context warnings, structure
deltas, and configured overlap findings require review before the next round.
