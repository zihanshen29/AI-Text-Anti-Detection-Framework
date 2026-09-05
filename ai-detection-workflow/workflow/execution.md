# Layer 2 - Execution

**Workflow contract:** `workflow/contract.json` defines the only permitted
round counts, tiers, rollback unit, and anti-regression policy.

Layer 2 executes one approved round at a time. It makes no external detector
calls and treats offline rule hits as internal workflow evidence only.

## Before Editing

Preserve the all-round baseline manifest created during planning before any
document is changed. It must contain every target's original snapshot and the
complete approved plan. Use a distinct JSON filename for each round.

For the selected round, create snapshot evidence before modifying a target:

```powershell
python .\tools\workflow_check.py plan --plan <plan-path> --round <N> --project-root <project-root> --snapshot-dir <snapshot-dir> --output <plan-manifest.json>
```

Only exit code 0 permits the round to begin. The plan manifest names each
target, snapshot, prior path, configured overlap setting, and a labeled
`worktree_raw_sha256` value. It also freezes the plan, active contract, target
bytes, and every configured prior version. The JSON output path must be
different from all of those inputs.

Reusing the snapshot parent is safe: each call creates a unique subdirectory
and creates snapshot files exclusively, preserving earlier snapshots.

## After Editing

```powershell
python .\tools\workflow_check.py post-round --manifest <plan-manifest.json> --output <post-round-json>
```

Record the result, JSON paths, hashes, and disposition in CHANGES. Hard
encoding, identity, path, parse, application, or fidelity failures require a
whole-round rollback and stop the round. Rule regressions, review-context
warnings, structural deltas, and overlap findings require review before the
next round. `post-round` rejects incompatible or moved manifests, plan or
contract drift, changed prior versions, snapshot provenance mismatches, and
overlap settings that differ from the active contract.

The approved-edits check replays exact BEFORE/AFTER replacements from the
snapshot in plan order. Skipped edits and any additional change require
whole-round rollback. UTF-8 BOM presence and CRLF/LF line endings may differ;
all remaining text, including spaces and trailing newlines, must match.

## Completion

Every Layer 2 plan has 3/5/7 total rounds and a required final audit-only
round. Select its number and supply the original all-round baseline instead
of a new snapshot directory:

```powershell
python .\tools\workflow_check.py plan --plan <plan-path> --round <final-N> --project-root <project-root> --baseline-manifest <baseline-manifest.json> --output <audit-manifest.json>
python .\tools\workflow_check.py post-round --manifest <audit-manifest.json> --output <audit-results.json>
```

The final audit compares every target with the full plan replayed from the
original baseline, including targets not edited in the immediately preceding
round. An empty audit target set is not accepted. Record the final evidence
and resolve review findings before declaring completion. The ten-token 0.70
overlap threshold and A/B/C tier policy remain in force throughout the run.
