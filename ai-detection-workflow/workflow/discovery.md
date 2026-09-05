# Layer 0 - Discovery

**Workflow contract:** `workflow/contract.json` controls the layer decisions
below.

Discovery reads a UTF-8 document, determines `en`, `zh`, or `auto`, and
records deterministic evidence before planning. It does not edit text and does
not call external detectors.

## Required Gate

From the workflow root in PowerShell:

```powershell
python .\tools\workflow_check.py discovery --text <document-path> --lang auto --output <discovery-json>
```

Layer 1 cannot begin until this JSON exists and the reviewer has accepted the
scope. A successful discovery may contain rule hits; an unreadable file,
encoding failure, or invalid rule configuration is an error.

## Record

- target path and inferred language;
- document type, fixed technical constraints, and prior versions if supplied;
- scanner aggregates using `actionable_unique_spans` as the primary total;
- whitelist and review-context evidence;
- the `manual_rules` checklist: record each rule as passed, not applicable,
  or needing an edit, with a short reason; pending rules are not automated passes;
- structural metrics and the path/hash of the discovery JSON; and
- either zero edits or the candidate evidence sent to planning.

Chinese context policy comes from `rules/zh/context_whitelist.json`. Fixed
terms such as `生态环境`, `数字化转型`, and `控制闭环` stay protected. A review
context requires sentence-level planning judgment rather than a mechanical
replacement.

## Handoff

Discovery can recommend no editing. If it recommends Layer 2 work, planning
must construct 3/5/7 total rounds, reserve the final audit-only round, and use
only A/B/C editing tiers under the workflow contract.
