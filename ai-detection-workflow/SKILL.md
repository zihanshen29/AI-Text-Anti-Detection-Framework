---
name: ai-detection-workflow
description: Guide a structured three-layer workflow for reducing AI-detection signals in academic or long-form documents while preserving technical accuracy, citations, and the author's voice. Use this whenever the user asks to "reduce AI signals", "humanize AI text", "lower AI detection score", "pass AI detection", "降 AI 率", "降 AIGC", "降重", "论文 AI 检测", "降 ai 味", or shares a document flagged by GPTZero, Turnitin AI, Originality, Pangram, Copyleaks, 知网 AIGC, 万方 AIGC, 维普, 笔灵, or PaperPass. Handles English and Chinese with separate rule sets. The workflow is Layer 0 Discovery (detect language and genre, surface hidden constraints, diagnose actual AI patterns in THIS document), Layer 1 Planning (produce a round-by-round edit plan for user approval), Layer 2 Execution (apply edits one round at a time with detection-score measurement between rounds). Never run a single blind rewrite pass; always start at Layer 0.
---

# AI Detection Workflow

## When to use this skill

Any request to make a document "less AI-detectable", "more human", "pass AI detection", or to reduce a detector score. Applies equally to English and Chinese documents and to academic, editorial, or long-form content. Traditional similarity reduction / "降重" is handled only as an anti-regression constraint against prior versions or source overlap; it is not the optimization target. If the request is "rewrite this paragraph in a more natural style" for a short snippet (< ~300 words) with no detection concern, do NOT use this skill — answer inline.

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
                          OUTPUT → CHANGES_roundN.md per round
                                + final CHANGES_summary.md
```

## File map

```
SKILL.md                         ← you are here
workflow/
  discovery.md                   Layer 0 prompt
  planning.md                    Layer 1 prompt
  execution.md                   Layer 2 per-round prompt (one call per round)
rules/
  en/                            loaded when document is English
    rules.yaml                    machine-readable P/V rules for deterministic scans
    sentence_patterns.md         P-01..P-20  structural: burstiness, em-dash,
                                             triplets, fragment clusters, openers
    tell_tale_phrases.md         V-01..V-45  vocabulary: delve/nuanced/leverage,
                                             Latinate verbs, hedges, filler
    replacement_guidance.md      AFTER-side replacement guidance and spaced-hyphen guard
    detector_profiles.md         6 detectors: GPTZero, Turnitin AI, Originality,
                                             Pangram, Copyleaks, ZeroGPT
  zh/                            中文文档时加载
    rules.yaml                    machine-readable C/S rules for deterministic scans
    ai_cliches.md                C-01..C-18  词汇套语：赋能/抓手/综上所述/
                                             任重道远/完美列举
    sentence_patterns.md         S-01..S-20  句法：句长均匀、长定语、被字句、
                                             "对...进行..."、欧化句式
    context_whitelist.md         P0.4 中文上下文白名单：生态环境/控制闭环/
                                             不仅仅/一方面...另一方面 等不替换场景
    replacement_blacklist.md     AFTER-side hard blacklist, disfavored replacements,
                                             and context-specific replacement pools
    detector_profiles.md         5 检测器：知网 AIGC、万方、维普、笔灵、
                                          PaperPass
tools/                           deterministic offline scanners; not detector simulators
templates/                       skeletons each layer fills when producing output
  discovery_output.md            template for Layer 0 → discovery.md
  plan_output.md                 template for Layer 1 → plan.md
  changes_log.md                 template for Layer 2 → CHANGES_roundN.md
  batch_eval_output.md           template for batch offline evaluation runs
  eval_report_header.md          fixed offline-evaluation report header
```

### How the rule files are loaded

Layer 0 detects the document's language first, then loads the matching language folder. For a typical scan:

- **English document** → load `rules/en/sentence_patterns.md`, `rules/en/tell_tale_phrases.md`, and `rules/en/detector_profiles.md`; use `rules/en/rules.yaml` for deterministic tooling and `rules/en/replacement_guidance.md` during Layer 1 replacement checks. Run P-NN structural checks first because they are the most interpretable signals; then run V-NN as a vocabulary grep pass; consult detector profiles only after the user names a target detector.
- **Chinese document** → load `rules/zh/ai_cliches.md`, `rules/zh/sentence_patterns.md`, `rules/zh/context_whitelist.md`, and `rules/zh/detector_profiles.md`; use `rules/zh/rules.yaml` for deterministic tooling and `rules/zh/replacement_blacklist.md` during Layer 1 replacement checks. Run C-NN first, then apply the context whitelist before forwarding hits to Layer 1, then run S-NN for residual syntactic patterns; consult detector profiles when the target is named.
- **Mixed document** → load both folders. Identify which sections are which language and scan each with the matching ruleset.

Never load both language families for a document that is monolingual — it doubles scan time and produces noise. Loading the Chinese context whitelist with the Chinese rule family is required and does not count as cross-language loading.

## How to start

ALWAYS begin by loading `workflow/discovery.md`. Do not open `rules/` or `workflow/planning.md` directly — they are downstream resources that Layer 0 and Layer 1 load for themselves.

If the user wants to skip ahead (e.g., "I already have a diagnosis, just plan the edits"), it is acceptable to enter at Layer 1 directly, but the user must produce or paste a `discovery.md` first. Never enter at Layer 2 without a `plan.md`.

### Batch offline evaluation

For multi-sample regression tests (e.g., evaluating framework behavior across 3-10 generated samples), use the batch template `templates/batch_eval_output.md` to consolidate per-sample results into one report instead of producing separate `discovery.md` / `plan.md` / `CHANGES_round*.md` file sets per sample.

**Important:** batch mode does not relax Layer 2 discipline. Each sample's rewriting is still plan-driven exact string replacement. The batch template provides condensed per-sample plan and changes inline within the batch report; it does not authorize creative paragraph-level rewriting. The user has formally decided that Layer 2 stays strict in all execution contexts including batch evaluation. Evaluator agents that rewrite samples without a per-sample exact-string plan are producing invalid batch reports.

Batch mode requires `measurement_type: offline_rule_hits` and produces no claim about external detector scores. Use the rubric defined in `meta/rubric/offline_rubric.md` for scoring.

## Core principles

- **Discover before planning.** Never write a plan before confirming language, genre, constraints, and the actual patterns present in the document. Assumed patterns are the single biggest source of wasted rewrites.
- **Ask, don't guess.** External constraints (school rules, journal guides, target detector) are worth one round-trip with the user. An incorrect premise here invalidates every downstream round.
- **One round, one focus.** Each execution round should target one class of change (tense sweep, fragment merging, cliché removal, block rewrites). Mixing classes inside a round makes it impossible to tell which edit moved the detector score.
- **Layer 2 is universally strict.** Exact before/after string replacement is the contract in every execution context. There is no offline mode, creative mode, batch mode, or dry-run mode that relaxes this. Batch evaluation uses condensed plan tables within `templates/batch_eval_output.md`, not creative rewriting.
- **Chinese trigger words require context protection.** Before `生态`, `闭环`, `赋能`, `痛点`, `不仅`, `一方面`, `同时`, `进行`, or `化` suffixes become fixes, Layer 0 and Layer 1 must check `rules/zh/context_whitelist.md`.
- **AFTER strings must be scanned.** Layer 1 must check each proposed AFTER against the detected rules and universal high-frequency rules so a fix does not remove one AI signal while introducing another.
- **Replacement diversity.** Fixes in the same rule family must not collapse into one replacement; plan-level diversity checks are defined in `workflow/planning.md` Step 4.4.
- **Measure between rounds.** After each round, the user compiles the document, runs the detector, and records the delta. Without measurement, rounds can silently make things worse.
- **Technical fidelity is non-negotiable.** Equations, numbers, code identifiers, citation keys, figure/table labels, and reference lists must be byte-identical before and after every round. Any rewrite that would touch them gets flagged, not applied.
- **Anti-regression.** If the target document has a prior version (v1, v2, …), new wording must differ from both the AI-flagged current version AND the older human version. Otherwise similarity scores rise while AI scores fall — a net loss.

## Common pitfalls

- **Skipping Layer 0 because the user is in a hurry.** The five minutes saved here cost fifty minutes later when the first round produces nonsense because an unstated constraint was violated.
- **Running "tense fix + fragment merge + cliché removal" in one round.** Each has different risk levels and different detector impact. Separate them.
- **Trusting AI-pattern intuition instead of grepping the document.** Every document has its own signature. The rule library in `rules/` is a candidate list, not a verdict — Layer 0 must check each candidate against the actual text.
- **Not recording what each round produced.** Without a per-round `CHANGES_roundN.md`, a later round can accidentally undo an earlier fix.

## Notes on the Chinese vs English split

The two languages do not share the same AI signal space, and the rule libraries reflect that asymmetry.

**English detectors** (GPTZero, Turnitin AI, Originality, Pangram, Copyleaks, ZeroGPT) weight two families of signals roughly equally:

- **Structural** — perplexity + burstiness, em-dash density, tricolon overuse, paragraph symmetry, fragment clusters. These live in `rules/en/sentence_patterns.md` as P-01..P-20.
- **Vocabulary** — tell-tale words (`delve`, `nuanced`, `multifaceted`, `tapestry`, `leverage`), Latinate-verb preference (`utilize`, `facilitate`), hedge vocabulary, filler phrases. These live in `rules/en/tell_tale_phrases.md` as V-01..V-45.

**Chinese detectors** (知网 AIGC, 万方, 维普, 笔灵, PaperPass) are dominated by vocabulary and fixed-phrase matching:

- **Vocabulary** — academic connectives (综上所述、由此可见), four-character cliché chains (全面提升、深入探讨), perfect enumeration (首先/其次/再次/最后), closing-sentence tropes (必将、任重道远、未来可期), commercial buzzwords (赋能、抓手、痛点、生态、闭环). These live in `rules/zh/ai_cliches.md` as C-01..C-18.
- **Structural signals** play a smaller role than in English but still matter after the vocabulary layer is cleaned: uniform sentence length, long adnominal modifiers ("的" chains), passive-voice overuse, "它" pronoun repetition, Europeanized syntax. These live in `rules/zh/sentence_patterns.md` as S-01..S-20.
- **Context whitelist** — Chinese trigger words must be checked against fixed phrases and technical/paired contexts before planning. These safeguards live in `rules/zh/context_whitelist.md` and are applied in both Layer 0 and Layer 1.

The practical upshot: English rewrite plans almost always involve both the P and V layers in early rounds. Chinese rewrite plans benefit most from front-loading the C layer (cheap wins, highest detector weight) before moving to the S layer (higher-cost restructuring).

For mixed-language documents, load both language folders. When a section switches language, apply the matching language's rule set to that section; never apply the wrong language's rules even when the document is mostly one language.

## When this skill should hand off

After Layer 2's final round, the user may request manual polish or a final human read. That is expected and encouraged. This skill does not promise a score below any specific threshold — it promises a structured, reviewable, reversible path toward a lower score with preserved technical content.
