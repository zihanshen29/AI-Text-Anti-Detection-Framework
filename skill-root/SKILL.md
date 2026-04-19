---
name: ai-detection-workflow
description: Guide a structured three-layer workflow for reducing AI-detection signals in academic or long-form documents while preserving technical accuracy, citations, and the author's voice. Use this whenever the user asks to "reduce AI signals", "humanize AI text", "lower AI detection score", "pass AI detection", "降 AI 率", "降 AIGC", "降重", "论文 AI 检测", "降 ai 味", or shares a document flagged by GPTZero, Turnitin AI, Originality, Pangram, Copyleaks, 知网 AIGC, 万方 AIGC, 维普, 笔灵, or PaperPass. Handles English and Chinese with separate rule sets. The workflow is Layer 0 Discovery (detect language and genre, surface hidden constraints, diagnose actual AI patterns in THIS document), Layer 1 Planning (produce a round-by-round edit plan for user approval), Layer 2 Execution (apply edits one round at a time with detection-score measurement between rounds). Never run a single blind rewrite pass; always start at Layer 0.
---

# AI Detection Workflow

## When to use this skill

Any request to make a document "less AI-detectable", "more human", "pass AI detection", or to reduce a detector score. Applies equally to English and Chinese documents and to academic, editorial, or long-form content. If the request is "rewrite this paragraph in a more natural style" for a short snippet (< ~300 words) with no detection concern, do NOT use this skill — answer inline.

## Why three layers, never one

Single-pass AI humanizers fail in three predictable ways:

1. **Unknown constraints poison the output.** School style guides, journal rules, and the author's earlier revision history usually arrive mid-conversation, not upfront. A one-shot rewrite locks in a wrong premise before the constraint is even revealed.
2. **The rewrite introduces new AI patterns.** Fixing fragment sentences can create uniform mid-length sentences; swapping clichés can create new clichés. Without a measurement checkpoint, the second round never happens.
3. **Language-specific signals get averaged out.** English and Chinese detectors look for almost non-overlapping patterns. A generic prompt produces generic output that scores mediocre on both.

This skill enforces three separated layers. Each layer has one job and one output artifact. The user approves each handoff.

## Architecture

```
Layer 0 — Discovery       Read document, detect language/genre,
(workflow/discovery.md)   surface external constraints by asking user,
                          scan for actual AI patterns present in THIS doc.
                          OUTPUT → discovery.md (user reviews)

Layer 1 — Planning        Consume discovery.md, produce round-by-round
(workflow/planning.md)    edit plan with exact before/after for every fix,
                          split into 3–6 rounds by risk tier.
                          OUTPUT → plan.md (user approves)

Layer 2 — Execution       Run ONE round at a time. Between rounds:
(workflow/execution.md)   compile, run detector, log delta, decide next round.
                          OUTPUT → round_N_changes.md per round
                                + final CHANGES.md
```

## File map

```
SKILL.md                         ← you are here
workflow/
  discovery.md                   Layer 0 prompt
  planning.md                    Layer 1 prompt
  execution.md                   Layer 2 per-round prompt
rules/
  en/
    tell_tale_phrases.md         words/phrases detectors latch onto in EN
    sentence_patterns.md         em-dash, triplets, uniform length, etc.
    detector_profiles.md         GPTZero vs Turnitin vs Originality
  zh/
    ai_cliches.md                赋能/抓手/综上所述/全方位 etc.
    sentence_patterns.md         句长均匀、完美列举、四字堆叠
    detector_profiles.md         知网 vs 万方 vs 维普 vs 笔灵
templates/
  discovery_output.md            template for Layer 0 output
  plan_output.md                 template for Layer 1 output
  changes_log.md                 template for Layer 2 per-round logs
```

## How to start

ALWAYS begin by loading `workflow/discovery.md`. Do not open `rules/` or `workflow/planning.md` directly — they are downstream resources that Layer 0 and Layer 1 load for themselves.

If the user wants to skip ahead (e.g., "I already have a diagnosis, just plan the edits"), it is acceptable to enter at Layer 1 directly, but the user must produce or paste a `discovery.md` first. Never enter at Layer 2 without a `plan.md`.

## Core principles

- **Discover before planning.** Never write a plan before confirming language, genre, constraints, and the actual patterns present in the document. Assumed patterns are the single biggest source of wasted rewrites.
- **Ask, don't guess.** External constraints (school rules, journal guides, target detector) are worth one round-trip with the user. An incorrect premise here invalidates every downstream round.
- **One round, one focus.** Each execution round should target one class of change (tense sweep, fragment merging, cliché removal, block rewrites). Mixing classes inside a round makes it impossible to tell which edit moved the detector score.
- **Measure between rounds.** After each round, the user compiles the document, runs the detector, and records the delta. Without measurement, rounds can silently make things worse.
- **Technical fidelity is non-negotiable.** Equations, numbers, code identifiers, citation keys, figure/table labels, and reference lists must be byte-identical before and after every round. Any rewrite that would touch them gets flagged, not applied.
- **Anti-regression.** If the target document has a prior version (v1, v2, …), new wording must differ from both the AI-flagged current version AND the older human version. Otherwise similarity scores rise while AI scores fall — a net loss.

## Common pitfalls

- **Skipping Layer 0 because the user is in a hurry.** The five minutes saved here cost fifty minutes later when the first round produces nonsense because an unstated constraint was violated.
- **Running "tense fix + fragment merge + cliché removal" in one round.** Each has different risk levels and different detector impact. Separate them.
- **Trusting AI-pattern intuition instead of grepping the document.** Every document has its own signature. The rule library in `rules/` is a candidate list, not a verdict — Layer 0 must check each candidate against the actual text.
- **Not recording what each round produced.** Without a per-round `changes_log.md`, a later round can accidentally undo an earlier fix.

## Notes on the Chinese vs English split

English detectors (GPTZero, Turnitin AI, Originality, Pangram) weight perplexity + burstiness statistics and a tell-tale vocabulary (`delve`, `nuanced`, `multifaceted`, em-dash overuse, tripled parallel structures). Chinese detectors (知网 AIGC, 万方, 维普, 笔灵, PaperPass) weight fixed academic connectives (综上所述、由此可见), four-character cliché chains (全面提升、深入探讨), perfect enumeration (首先/其次/再次/最后), uniform sentence length, and AI-buzzword vocabulary (赋能、抓手、痛点、生态、闭环). The rule sets overlap less than 20%. Always load the matching language folder under `rules/`; for mixed documents load both.

## When this skill should hand off

After Layer 2's final round, the user may request manual polish or a final human read. That is expected and encouraged. This skill does not promise a score below any specific threshold — it promises a structured, reviewable, reversible path toward a lower score with preserved technical content.
