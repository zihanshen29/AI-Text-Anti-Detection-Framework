# Layer 2 - Execution

**Workflow contract:** `workflow/contract.json` defines the only permitted
round counts, tiers, rollback unit, and anti-regression policy.

Layer 2 executes one approved round at a time. It makes no external detector
calls and treats offline rule hits as internal workflow evidence only.

## Before Editing

For the selected round, create snapshot evidence before modifying a target:

```powershell
python .\tools\workflow_check.py plan --plan <plan-path> --round <N> --project-root <project-root> --snapshot-dir <snapshot-dir> --output <plan-manifest.json>
```

Only exit code 0 permits the round to begin. The plan manifest names each
target, snapshot, prior path, configured overlap setting, and a labeled
`worktree_raw_sha256` value.

## After Editing

```powershell
python .\tools\workflow_check.py post-round --manifest <plan-manifest.json> --output <post-round-json>
```

Record the result, JSON paths, hashes, and disposition in CHANGES. Hard
encoding, identity, path, parse, application, or fidelity failures require a
whole-round rollback and stop the round. Rule regressions, review-context
warnings, structural deltas, and overlap findings require review before the
next round.

## Completion

Every Layer 2 plan has 3/5/7 total rounds and a required final audit-only
round. The final audit is complete only after `post-round` evidence is
recorded. The ten-token 0.70 overlap threshold and A/B/C tier policy remain in
force throughout the run.
