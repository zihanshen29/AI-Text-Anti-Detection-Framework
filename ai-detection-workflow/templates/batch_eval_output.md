# Batch Offline Evaluation

**Workflow contract:** `workflow/contract.json`
- **Measurement type:** `offline_rule_hits`
- **External detector status:** `not run`
- **Primary population:** `all_valid_inputs`

## Population Summary

| Metric | Value |
| --- | ---: |
| Valid inputs | `<N>` |
| Input-invalid cases | `<N>` |
| All-valid mean | `<score>/35` |
| All-valid median | `<score>/35` |
| Below 25/35 count/rate | `<N> / <rate>` |
| Hard-fail count/rate | `<N> / <rate>` |

Only input-invalid cases are outside the primary population; list each reason.
Low-quality results and hard-fail results remain in the all-valid mean and
median. A success-only mean may appear under Diagnostics only and is never
headline data.

## Input-Invalid Cases

| Sample | Reason | Excluded from primary population |
| --- | --- | --- |
| `<ID>` | `<unreadable/missing/invalid input reason>` | yes |

## Per-Sample Results

| Sample | Valid input | Total /35 | Below 25/35 | Hard fail | Included in primary |
| --- | --- | ---: | --- | --- | --- |
| `<ID>` | yes/no | `<N>` | yes/no | yes/no | yes/no |

## Diagnostics

- **Success-only mean (diagnostic only):** `<score>/35`
- **Rule-hit and fidelity notes:** `<evidence>`
- **Contract policy:** exact BEFORE/AFTER edits, A/B/C tiers, 3/5/7 total
  rounds where Layer 2 runs, and a required final audit-only round.
