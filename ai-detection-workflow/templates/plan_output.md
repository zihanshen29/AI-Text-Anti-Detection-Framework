# Edit Plan

**Workflow contract:** `workflow/contract.json`
- **Project root:** `<absolute path>`
- **Total rounds:** `3 | 5 | 7`
- **Plan language:** `en | zh | mixed`
- **Secondary scan disposition:** `acknowledged | none`

## Round 1 - Tier A

**Round tier:** `A`

### Fix 1.1 - <short descriptor>

- **File:** `<path relative to project root>`
- **Language:** `en | zh`
- **Secondary scan disposition:** `acknowledged | none`

**BEFORE (verbatim)**
> <exact source text, appearing once in the target>

**AFTER (verbatim)**
> <exact replacement text>

## Round 2 - Tier B

**Round tier:** `B`

### Fix 2.1 - <short descriptor>

- **File:** `<path relative to project root>`
- **Language:** `en | zh`
- **Secondary scan disposition:** `acknowledged | none`

**BEFORE (verbatim)**
> <exact source text>

**AFTER (verbatim)**
> <exact replacement text>

## Round 3 - Final Audit

**Round type:** `audit-only`

The final audit is required whenever Layer 2 runs. It records post-round
evidence; it does not introduce an editing tier.

- **Original all-round baseline manifest:** `<path saved before any edit>`
- **Audit manifest:** `<plan --round final-N --baseline-manifest ... output>`
- **Audit post-round evidence:** `<path and disposition>`

## Manual-Rule Review

| Discovery rule | Review status | Reason / fix ID |
| --- | --- | --- |
| `<ID>` | `passed / not_applicable / needs_edit` | `<sentence-level evidence>` |

## Approval Record

- **`plan --round all` JSON:** `<path>`
- **Original all-round baseline manifest:** `<path>`
- **Result:** `executable | blocking review | error`
- **Ten-token overlap threshold:** `0.70`
- **Rollback policy:** whole round; stop after the first fix or guardrail failure
