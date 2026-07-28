# Discovery Record

**Workflow contract:** `workflow/contract.json`

- **Target:** `<absolute normalized path>`
- **Language:** `en | zh | auto result`
- **Discovery JSON:** `<path>`
- **Evidence hash:** `worktree_raw_sha256:<digest>`
- **External detector status:** `not run`

## Deterministic Evidence

| Component | Result | Notes |
| --- | --- | --- |
| Encoding/language preflight | pass/fail | |
| Rule scan | pass/evidence | actionable/review/whitelisted counts |
| Structure metrics | pass/evidence | |

## Candidate Disposition

- Zero edits recommended: `yes/no`
- Whitelisted contexts retained: `<IDs>`
- Review contexts: `<IDs or none>`
- Planning handoff: `allowed/blocked`

If Layer 2 is proposed, planning must use 3/5/7 total rounds, A/B/C editing
tiers, and a required final audit-only round.
