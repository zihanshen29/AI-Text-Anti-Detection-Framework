# English AI Detector Profiles

> **Consumed by:** Layer 0 (Discovery) Step 3 when the user names a target detector, and Layer 1 (Planning) when prioritizing fix order.
> **Not to be read by:** Layer 2 (Execution).

## Purpose

Different English AI detectors weigh different signals. Lowering a GPTZero score does not automatically lower a Turnitin AI score, and a rewrite that helps one detector can sometimes hurt another. This file documents what each major detector actually weights, its known quirks, and the fix priorities that give the best cost-benefit against it.

Use this file in two moments:

1. **During Layer 0 Step 3** — when the user names their target detector(s), load the corresponding profile(s) and use them to filter which rule entries (from `sentence_patterns.md` and `tell_tale_phrases.md`) to prioritize.
2. **During Layer 1 Step 3** — when deciding round ordering, put high-weight-for-target-detector fixes in earlier rounds (so the score drop is front-loaded).

**None of these profiles are published by the detector vendors.** They are reconstructed from empirical observation, public research, and testing patterns. Treat the profiles as well-grounded heuristics, not ground truth. Re-verify when a detector updates its model.

---

## GPTZero

### Model family and features

GPTZero's scoring is primarily **perplexity + burstiness** — the two canonical statistical signals. Perplexity measures how "predictable" the text is to a reference language model; burstiness measures the variance of sentence-level perplexity (and indirectly, sentence-length variance).

On top of the statistical core, GPTZero has overlaid vocabulary and phrase detection that catches specific LLM tells.

### What it weighs heavily

- **Sentence-length uniformity** (P-06 in `sentence_patterns.md`) — the highest-weight single feature. A document with standard deviation < 6 words over a 500-word window will score highly AI regardless of vocabulary.
- **Elevated vocabulary cluster** (V-01 through V-18) — `delve`, `nuanced`, `tapestry`, `multifaceted` each individually move the score by several percentage points.
- **Em-dash density** (P-04) — GPTZero specifically trained on this after GPT-4's em-dash habit became well-known.
- **"Not just X but Y" construction** (P-12) — a named-feature signal in their model.
- **Opener clichés** (P-03, V-31, V-32, V-33) — heavily weighted when appearing in the first 200 words.
- **Summary and future-work clichés** (P-19, P-20, V-35) — heavily weighted when appearing in the last 500 words.

### What it weighs lightly

- Latinate vs Germanic verb preference (V-19–V-25) — Pangram and Originality catch this better.
- Nested relative clauses (P-14) — not a GPTZero priority.

### Known quirks

- **Short documents (< 250 words) produce false positives routinely.** GPTZero itself warns users about this. If the user's document is short, some of the reported AI score is noise.
- **Scientific or highly technical vocabulary can flag as AI** because it's low-perplexity to the reference model. Medical, legal, and ML papers sometimes score artificially high even when fully human-written.
- **Citation-dense paragraphs lower the AI score** because citation strings are high-entropy and increase local perplexity. Not a reason to add citations artificially, but worth knowing.
- **Edit the first and last paragraphs first.** GPTZero's per-sentence probabilities weight the beginning and end of a document disproportionately in their aggregate calculation.

### Round-priority recommendation when GPTZero is the target

1. Round 1: P-06 (sentence-length burstiness injection) + V-01 through V-18 (vocabulary cluster).
2. Round 2: P-04 (em-dash), P-12 ("not just X but Y"), P-09 (fragment clusters).
3. Round 3: Opener and closer clean-up (P-03, P-19, V-31, V-35).
4. Round 4: Block rewrites of Abstract and Introduction opening paragraph (GPTZero weights document opening heavily).
5. Round 5: Audit.

### Typical score delta expectations

Fully cooperative rewrite of a GPT-4-generated academic paragraph: 90% AI → 30-45% AI is realistic. 90% → < 20% usually requires either non-trivial restructuring or content-level editing beyond style.

---

## Turnitin AI Detection

### Model family and features

Turnitin's AI detector is primarily **vocabulary and phrase-density focused**, with a secondary check on sentence-structure regularity. It was built to differentiate AI-assisted student work from fully-human work, so it's calibrated for academic register specifically.

### What it weighs heavily

- **Latinate-verb preference** (V-19–V-25) — `utilize`, `facilitate`, `implement` (in non-technical contexts) are heavily weighted. This is Turnitin's distinctive strength.
- **Filler intensifiers and empty modifiers** (P-11, V-29, V-30) — `very`, `relatively`, `largely` without specific comparisons.
- **Hedging stack** (P-10) and individual hedges (V-26, V-27, V-28) — moderate weight.
- **Padding phrases** (V-37 `the fact that`, V-39 `in order to`, V-40 `plays a role in`) — Turnitin catches these well.
- **Nested relative clauses** (P-14) — Turnitin actively flags these.

### What it weighs lightly

- Em-dash density — not a focus.
- Fragment clusters (P-09) — not a primary signal.
- Burstiness variance — Turnitin is less reliant on this than GPTZero.

### Known quirks

- **Turnitin integrates with the LMS.** The AI score the user sees is often the same number the grader sees. Reducing it matters for institutional reasons, not only for the final submission.
- **False positives on ESL writing are documented.** ESL students often use more formal register; Turnitin's AI detector has been reported to flag their writing at elevated rates. This is not the student's fault, and rewrite strategies differ — preserving voice matters.
- **Turnitin does not disclose threshold behavior.** A score change from 15% to 22% may or may not cross a reporting threshold at the institution level; check with the user's institution if relevant.
- **Passages with citations score lower** similarly to GPTZero. Integrated citation density helps.

### Round-priority recommendation when Turnitin AI is the target

1. Round 1: V-19–V-25 (Latinate verbs) across the whole document.
2. Round 2: V-29, V-30, V-37, V-39 (padding and filler) sweep.
3. Round 3: P-10 and V-26–V-28 (hedging); P-14 (nested clauses).
4. Round 4: Block rewrites if the document has obviously AI-styled sections (Abstract, Introduction).
5. Round 5: Audit.

### Typical score delta expectations

Turnitin's AI score is often more resistant to rewriting than GPTZero's because vocabulary-based signals are harder to mask without content change. 70% AI → 35-50% AI is typical; dropping below 25% usually requires deep paraphrasing.

---

## Originality.ai

### Model family and features

Originality is vocabulary-heavy and plagiarism-integrated. It combines an AI-text classifier with a traditional similarity check, and its UI reports both.

### What it weighs heavily

- **Vocabulary cluster** (V-01–V-18) — similar to GPTZero.
- **Latinate verb preference** (V-19–V-25) — comparable to Turnitin.
- **Hedging vocabulary** (V-26–V-30) — heavily weighted.
- **Nested relative clauses** (P-14) — a named feature.
- **Filler intensifiers** (P-11) — heavily weighted.

### What it weighs lightly

- Em-dash density.
- Fragment clusters.
- Opener and closer clichés (catches some but not the main signal).

### Known quirks

- **Dual-axis reporting.** The user sees both an AI score and a plagiarism score. A rewrite that reduces AI score by drifting toward a prior human version will raise the plagiarism score. **Anti-regression checks are especially critical for Originality.ai targets.**
- **The plagiarism checker uses a large web index.** Paraphrases that accidentally echo a well-known paper will flag on plagiarism even though the AI score drops.
- **Originality updates its AI classifier frequently.** A rewrite strategy that worked six months ago may not work today.

### Round-priority recommendation when Originality.ai is the target

1. Round 1: V-01–V-18 (vocabulary cluster) + V-19–V-25 (Latinate verbs).
2. Round 2: P-10, P-11, V-26–V-30 (hedge and filler sweep).
3. Round 3: P-14 (nested clauses) + fragment or other structural issues.
4. Round 4: Block rewrites with **extra anti-regression checks** against prior versions; Originality will catch regression via its plagiarism score.
5. Round 5: Audit that checks both AI score and similarity score.

### Typical score delta expectations

Similar to Turnitin; vocabulary-heavy signals are harder to suppress. Plan for 50-60% of the AI-score reduction you'd see on GPTZero for the same amount of work.

---

## Pangram

### Model family and features

Pangram is the newest major detector and specifically marketed as detecting **"AI humanizer"** output — text that has been run through a first-pass humanization tool. Its training explicitly includes humanizer outputs.

### What it weighs heavily

- **Em-dash overuse** (P-04) — Pangram's signature feature.
- **Paragraph symmetry** (P-07) — consecutive sentences with similar structural templates.
- **Tricolon density** (P-05) — three-item parallel lists.
- **Balanced parallel constructions** (P-08) — "not just X but Y" family.
- **Fragment clusters** (P-09) — specifically catches humanizer outputs that inject fragments.
- **Vocabulary cluster** (V-01–V-18) — standard.
- **"This/That" sentence starts** (P-18).
- **Thought-leader vocabulary** (V-41–V-43).

### What it weighs lightly

- Hedging vocabulary — not a priority signal.
- Pure Latinate verb preference — overlaps with vocabulary cluster but not independently weighted.

### Known quirks

- **Pangram catches naive humanizer output.** If a document has already been run through an "AI humanizer" service, Pangram specifically flags the humanizer's characteristic introduction of fragments, em-dashes, and broken parallelism. A second pass through a humanizer usually makes Pangram scores *worse*, not better.
- **Pangram is less forgiving of structural repetition.** Two consecutive paragraphs that open with demonstrative pronouns (`This`, `That`) flag heavily.
- **Pangram publishes less about its methodology** than GPTZero or Turnitin. Profile entries for Pangram are reconstructed from output testing.

### Round-priority recommendation when Pangram is the target

1. Round 1: P-04 (em-dash), P-09 (fragment clusters), P-18 (demonstrative openers).
2. Round 2: P-05 (tricolon), P-07 (paragraph symmetry), P-08 (balanced parallel).
3. Round 3: V-01–V-18 (vocabulary), V-41–V-43 (thought-leader).
4. Round 4: Block rewrites focused on structural variation.
5. Round 5: Audit.

### Typical score delta expectations

Pangram is often the most resistant detector for documents that have been pre-humanized. For fresh LLM output, dropping from 95% to 40% is achievable. For humanizer-processed output, some documents cannot drop below 60-70% without substantial restructuring.

---

## Copyleaks AI Content Detector

### Model family and features

Copyleaks is plagiarism-first, AI-detection-second. Its AI-detection module is vocabulary and structure based, similar to Turnitin but with its own training set.

### What it weighs heavily

- **Metalinguistic filler** (P-02) — "it is important to note that" and similar.
- **Summary clichés** (P-19, V-35) — closing-sentence patterns.
- **Dummy-subject openers** (P-13) — "it is worth noting", "it is essential to".
- **Vocabulary cluster** (V-01–V-18).
- **Thought-leader cluster** (V-41–V-43).

### What it weighs lightly

- Sentence-length burstiness.
- Fragment clusters.
- Em-dash density.

### Known quirks

- **Copyleaks reports confidence bands, not just percentages.** A score of "likely AI" is more actionable than the raw percentage.
- **Educational integrations exist.** Some universities subscribe to Copyleaks instead of Turnitin; the user may not have a choice of detector.
- **Copyleaks is weaker on structural signals** than GPTZero or Pangram — a rewrite optimized for vocabulary alone often succeeds here.

### Round-priority recommendation when Copyleaks is the target

1. Round 1: P-02 (metalinguistic filler) + P-13 (dummy-subject openers) sweep.
2. Round 2: V-01–V-18 (vocabulary) + V-41–V-43 (thought-leader).
3. Round 3: P-19, V-35 (summary clichés) + remaining style issues.
4. Round 4: Block rewrites if needed.
5. Round 5: Audit.

---

## ZeroGPT

### Model family and features

ZeroGPT is a free / freemium detector with a simpler model than the paid competitors. Its weighting is heavily vocabulary-driven with less sophisticated structural analysis.

### What it weighs heavily

- **Vocabulary cluster** (V-01–V-18) — dominant signal.
- **Opener clichés** (P-03, V-31, V-32).
- **Future-work clichés** (P-20).

### What it weighs lightly

- Most structural patterns.
- Latinate verb preference.

### Known quirks

- **ZeroGPT has a higher false-positive rate** than the paid competitors. A document that scores "70% AI" on ZeroGPT may score 30% on GPTZero.
- **Short passages score unreliably.** Similar issue to GPTZero but more pronounced.
- **ZeroGPT is often used as the first check** because it's free. If the user reports a ZeroGPT score without naming another detector, assume the paid detectors will score differently and recommend running at least one paid detector for confirmation.

### Round-priority recommendation when ZeroGPT is the target

Essentially the same as GPTZero, with extra weight on the vocabulary cluster. If the user has only run ZeroGPT, recommend running GPTZero or one paid detector for calibration before committing to rounds.

---

## Handling multiple targets

If the user names two or more detectors:

1. **Find the intersection of high-priority rules** across target detectors. Fixes that score ●●● against two or more targets go in Round 1.
2. **Handle detector-specific priorities in separate rounds.** If GPTZero priorities differ from Turnitin priorities, put the GPTZero-specific fixes in one round and the Turnitin-specific fixes in another.
3. **Measure against all targets after each round.** Users often discover that a rewrite which drops GPTZero by 30 points drops Turnitin by only 10, or vice versa.

Universal-priority rules — high weight across nearly all detectors:

- **V-01 (`delve`) through V-18 (`navigate`) — vocabulary cluster.** Near-universal.
- **P-06 (sentence-length uniformity).** Universal except Copyleaks.
- **P-16 in `sentence_patterns.md` (the cross-referenced vocabulary entry).**
- **V-31–V-33 (establishing openers).** Near-universal.

If the user hasn't named a target, default to these four rule clusters in Round 1 — they improve the document against every detector listed above.

---

## What this file is not

This file is not a guarantee that following the recommendations will produce a specific score. Detector behavior varies with:

- Document length (short documents behave differently).
- Subject matter (technical writing in low-entropy domains flags higher regardless).
- Formatting and tokenization (some detectors tokenize aggressively on punctuation).
- Detector version (profiles shift with updates).

Treat the priorities as a disciplined starting point. Between rounds, always verify the delta empirically and adjust.
