# Offline Evaluation Rubric

This rubric is for offline manual evaluation only. It produces a 35-point manual quality total and does not represent, predict, or replace GPTZero, Zhiwang/CNKI, Turnitin, or any other external detector score.

## Score Shape

- Seven dimensions, each scored from 1 to 5.
- Use the 1, 3, and 5 anchors below as fixed reference points.
- Scores 2 and 4 are allowed as interpolation when the output falls between adjacent anchors.
- Maximum total: 35 points.
- Apply hard-fail flags before interpreting the total.

## Dimensions

### 1. AI signal reduction

- 1: The rewrite remains visibly AI-like, with formulaic structure, uniform sentence rhythm, generic transitions, or over-polished phrasing.
- 3: The rewrite reduces some AI signals but still has repeated patterns, predictable sentence shapes, or occasional synthetic phrasing.
- 5: The rewrite substantially reduces AI signals through natural variation, context-grounded phrasing, and human-like unevenness without becoming sloppy.

### 2. Readability and naturalness

- 1: The rewrite is awkward, choppy, confusing, or hard to read in normal use.
- 3: The rewrite is generally readable but has occasional stiffness, weak transitions, or unnatural phrasing.
- 5: The rewrite reads smoothly and naturally, with clear flow, appropriate sentence variety, and minimal friction.

### 3. Technical and factual fidelity

- 1: The rewrite changes important facts, technical meaning, claims, entities, numbers, terms, or evidence relationships.
- 3: The rewrite preserves the main meaning but weakens some qualifiers, loses technical nuance, or introduces minor imprecision.
- 5: The rewrite preserves facts, technical details, terminology, scope, qualifiers, and source intent.

### 4. Genre and register fit

- 1: The rewrite does not fit the required genre, audience, language, formality, or domain register.
- 3: The rewrite mostly fits but has occasional tone drift, mismatched formality, or genre-inappropriate phrasing.
- 5: The rewrite fits the expected genre, audience, language, formality, and domain conventions throughout.

### 5. Rule-hit targeting accuracy

- 1: The rewrite misses the targeted detection-risk rules or applies irrelevant changes that do not address the identified issues.
- 3: The rewrite addresses some targeted rules but leaves important rule hits unresolved or applies changes unevenly.
- 5: The rewrite accurately targets the identified rule hits and reduces those signals without broad, unnecessary alteration.

### 6. Workflow executability

- 1: The output violates required workflow steps, omits required sections, includes process leakage, or is not usable by the next workflow stage.
- 3: The output is mostly executable but has minor formatting drift, incomplete reporting, or small downstream cleanup needs.
- 5: The output follows workflow requirements cleanly and is ready for the next stage without extra repair.

### 7. Over-rewriting control

- 1: The rewrite over-edits the source, changes structure unnecessarily, removes useful specificity, or replaces precise wording with generic paraphrase.
- 3: The rewrite keeps the source mostly intact but still makes some unnecessary changes, flattening, or avoidable restructuring.
- 5: The rewrite changes only what is needed, preserves useful specificity and structure, and avoids unnecessary paraphrase churn.

## Hard-Fail Flags

Mark every applicable flag. A hard fail does not change the arithmetic total, but it must be reported and should dominate the final interpretation.

- `meaning_break`: Core meaning, claim direction, technical meaning, or author intent is materially changed.
- `fabrication`: New facts, sources, numbers, citations, entities, examples, or technical claims are introduced without support.
- `instruction_violation`: Explicit user, workflow, safety, formatting, or scope constraints are violated.
- `detector_score_claim`: The manual rubric total is presented as a GPTZero, Zhiwang/CNKI, Turnitin, or other external detector score.
- `prompt_or_process_leak`: The output includes hidden prompt text, workflow notes, internal analysis, or evaluator-only instructions.
- `language_or_register_mismatch`: The rewrite uses the wrong language, dialect, formality level, genre, or audience register.
- `unusable_output`: The output is incomplete, corrupted, mostly nonresponsive, or cannot be evaluated as a rewrite.

## Interpretation Guide

- 31-35: Strong offline rewrite quality. Use if no hard-fail flags are present.
- 25-30: Usable with light revision. Review lower-scored dimensions and any hard-fail flags.
- 18-24: Needs substantive revision before use. Identify repeat pattern failures before rerunning.
- 7-17: Not acceptable for normal use. Rework from the source and inspect workflow assumptions.

The manual rubric total is a human evaluation signal for offline runs. It is not a detector probability, AI percentage, plagiarism score, or external service result.
