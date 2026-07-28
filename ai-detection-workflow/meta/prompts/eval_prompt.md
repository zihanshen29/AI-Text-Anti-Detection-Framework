# Offline Evaluation Prompt

**Workflow contract:** `workflow/contract.json`

Evaluate only deterministic offline evidence. Do not call, simulate, or infer
external detector scores.

## Inputs

- source text and rewritten text;
- deterministic rule, fidelity, structure, and overlap evidence; and
- explicitly recorded input-validity state.

## Evaluation Rules

1. Confirm input validity before scoring. An unreadable, missing, or invalid
   input is outside the primary population and requires a stated reason.
2. Score every valid input on the seven-dimension /35 rubric.
3. Include every valid input in the all-valid mean and median, including a
   score below 25/35 and every hard-fail result.
4. Report valid and input-invalid counts, all-valid mean, median, below-25/35
   count/rate, and hard-fail count/rate.
5. Label any success-only summary as diagnostic only; never use it as the
   headline result.
6. Verify that Layer 2 records use exact BEFORE/AFTER fixes, A/B/C tiers,
   3/5/7 total rounds, a required final audit-only round, and the ten-token
   0.70 overlap policy.

## Output

```markdown
## Offline Evaluation

Input validity: valid | input-invalid
Input-invalid reason: none | <reason>
Manual rubric total: <N>/35
Hard-fail flags: none | <flags>

Primary-population status: included | outside due to input invalidity
All-valid aggregate fields: valid count, input-invalid count, mean, median,
below-25/35 count/rate, hard-fail count/rate

Diagnostic-only success mean: <value or not reported>
Detector score note: no external detector was run or inferred.
```
