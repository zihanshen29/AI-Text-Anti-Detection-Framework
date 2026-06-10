# English AFTER-Side Replacement Guidance

> **Consumed by:** Layer 1 (Planning) during Step 4.3 naturalness preflight.
> **Not to be read by:** Layer 2 (Execution) — executors take exact before/after pairs from `plan.md`.
> **Boundary:** This file constrains replacement products. It does not add new Layer 0 detector rules.

## 1. Em-Dash (P-04) Replacement Diversity

When removing em-dashes, vary the replacement according to sentence meaning:

- commas for light parenthetical asides;
- colons for explanation or specification;
- semicolons for independent clauses with a close relation;
- sentence splits where the second clause deserves emphasis;
- parentheses for true insertions.

Do not default to the spaced hyphen form `" - "`. The 2026-05-20 English after_repair review found that replacing many em-dashes with spaced hyphens created a new mechanical rhythm.

## 2. Case Repair After Deletion

When a fix deletes a sentence-opening phrase, repair the capitalization of the remaining first word. The after_repair review found lowercase paragraph starts after deletion-style fixes in `doubao/topic_04` and `gemini/topic_03`.

Examples:

- `Moreover, battery queues...` -> `Battery queues...`
- `In conclusion, the model...` -> `The model...`

## 3. AFTER Foreign-Language Residual Check

For English documents, AFTER strings must not introduce CJK characters or Chinese generation notes. If the source contains a provider-side foreign-language artifact, the rewrite should either remove it or flag it as an open question; do not preserve it silently.

Record this check in the fix block's `Naturalness / meaning / genre preflight` or `AFTER secondary scan` note, depending on where it is caught.
