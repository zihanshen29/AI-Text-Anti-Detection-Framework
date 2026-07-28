# Round Changes Record

**Workflow contract:** `workflow/contract.json`
- **Round:** `<N>`
- **Target files:** `<relative paths>`
- **Plan manifest:** `<path>`
- **Plan manifest hash:** `worktree_raw_sha256:<digest>`
- **Post-round JSON:** `<path>`
- **Post-round JSON hash:** `worktree_raw_sha256:<digest>`
- **External detector status:** `not run`

## Fixes

| Fix ID | File | Tier | BEFORE count | AFTER scan disposition | Applied |
| --- | --- | --- | ---: | --- | --- |
| `<N.M>` | `<path>` | `A/B/C` | `1` | `acknowledged/none` | `yes/no` |

## Deterministic Checks

| Component | Outcome | Disposition |
| --- | --- | --- |
| Target identity | pass/fail | |
| Guardrails | pass/fail/warning | |
| Rule scan | pass/evidence | |
| Structure metrics | pass/evidence | |
| Prior overlap | pass/evidence/not configured | |

## Round Outcome

- **Result:** `complete | review required | whole-round rollback required`
- **Reason:** `<evidence-based reason>`
- **Next step:** `<stop, review, or final audit>`

The ten-token 0.70 overlap policy applies to every configured prior check. A
hard failure rolls back the whole round and stops the round after its first
failed fix or guardrail.
