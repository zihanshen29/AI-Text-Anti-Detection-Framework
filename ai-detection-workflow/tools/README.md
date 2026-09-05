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
python .\tools\workflow_check.py plan --plan <plan.md> --round all --project-root <project-root> --snapshot-dir <snapshots> --output <baseline.json>
python .\tools\workflow_check.py plan --plan <plan.md> --round <N> --project-root <project-root> --snapshot-dir <snapshots> --output <plan-manifest.json>
python .\tools\workflow_check.py post-round --manifest <plan-manifest.json> --output <post-round.json>
python .\tools\workflow_check.py plan --plan <plan.md> --round <final-N> --project-root <project-root> --baseline-manifest <baseline.json> --output <audit-manifest.json>
python .\tools\workflow_check.py post-round --manifest <audit-manifest.json> --output <audit-results.json>
```

Layer 0 handoff requires discovery JSON. Layer 1 approval requires a successful
`plan --round all` gate. Layer 2 editing requires a successful snapshot gate;
Layer 2 handoff requires `post-round` evidence. JSON output labels every
file-byte hash as `worktree_raw_sha256` and records `external_detector_status:
not_run`. Plan manifests freeze the plan, workflow contract, target snapshots,
and configured prior versions. Post-round validation rejects drift in those
inputs or in the contract overlap settings. An output path may not alias an
input file.

Snapshot manifests now use schema version 2; generate a new baseline before
editing instead of reusing a version 1 manifest. Each snapshot call creates a
unique directory under the supplied parent and never overwrites an existing
snapshot. Preserve the original all-round baseline for the final audit, and
use separate output JSON filenames for the baseline and every round.

All-round preflight simulates dependent replacements in plan order. Post-round
requires the actual text to equal the snapshot plus exactly those approved
edits. Comparison normalizes UTF-8 BOM and CRLF/LF line endings only, leaving
spaces and trailing newlines significant. Its textual digests are explicitly
labeled `utf8_lf_text_sha256`; raw file hashes retain their separate meaning.
Discovery also exposes pending `manual_rules` for human or agent review.

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
