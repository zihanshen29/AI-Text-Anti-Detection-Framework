# Layer 0 — Discovery

> **Entered from:** `SKILL.md`
> **Produces:** `discovery.md` in the project working directory
> **Gates:** Layer 1 (Planning) cannot begin until the user has reviewed `discovery.md`.

## Purpose

Layer 0 is a diagnostic layer, not an editing layer. It does exactly three things:

1. **Detect what kind of document this is** (language, genre, length, structure).
2. **Surface external constraints** by actively asking the user — never guessing.
3. **Scan for AI patterns that are actually present in THIS document** — not patterns that might be present in documents like this.

The output is a single file, `discovery.md`, that the user reviews before any planning begins. If the user refuses to review it, do not proceed to Layer 1.

## Why this layer exists

Most AI-humanizer tools skip this step. They load a fixed rule list, apply it to the document, and hope. This fails because:

- Every document has a different AI signature. A thesis written with GPT-4 looks nothing like a blog post written with Claude 3, which looks nothing like a translation polished by DeepSeek. The telltale patterns differ.
- External constraints (school style guides, journal house style, previous revision history) are almost never in the initial upload. If we plan edits without knowing the school requires past tense, we produce a plan that makes the document worse.
- The user's priorities vary. Some users care about one specific detector; some care about similarity vs. a prior version; some have a hard page limit; some need to preserve "self-reflection" content because it's explicitly graded.

Five minutes of discovery saves fifty minutes of wasted rewrites.

---

## Step 1 — Read the document

**Encoding preflight.** Before reading the document, confirm UTF-8 encoding explicitly. On PowerShell use `Get-Content -Raw -Encoding UTF8`; on Unix shells use `cat` directly (UTF-8 is usually default, but verify with `file -bi <path>` when uncertain). After reading, scan the first 500 characters for mojibake markers: `�`, `锟斤拷`, `鍘`, `鐗`, `涓` appearing in suspicious contexts. If any appears, stop and report an encoding failure to the user before proceeding. Do not attempt to "interpret around" broken encoding; downstream rule hits will be unreliable.

Read the document. If it's long (> 10,000 words), read:

- The first 1,500 words (opening, usually includes abstract/intro),
- A 1,000-word block from the middle,
- The last 1,500 words (conclusion, usually includes reflection/future work),
- Any table of contents or section headings.

Do NOT skim the whole document with summary-style reading. AI patterns hide in sentence-level rhythm and micro-vocabulary; they are invisible at paragraph-summary resolution.

**Record while reading:**
- Exact sentences that read as AI-generated. Quote them verbatim with section/page references.
- Sentences that are clearly human-voice (for contrast).
- Any explicit markers of genre (thesis, paper, blog, report).
- Citation style, equation style, figure-reference style — these must not be disturbed later.

## Step 2 — Detect language and route rules

Determine the document's primary language:

- **English only** → load `rules/en/*` files.
- **Chinese only** → load `rules/zh/*` files.
- **Mixed** (e.g., Chinese thesis with English abstract, or English paper with Chinese citations) → load both, and flag mixed sections explicitly in `discovery.md`.

Do not load rule files yet — just note which set applies. Loading happens in Step 4.

## Step 3 — Surface external constraints (ASK THE USER)

This is the step most frameworks skip. Do not skip it.

Optional memory check: if the user has a personal memory system such as BrainMem, query it first for existing project constraints (target detectors, institution rules, style guides, version history) using portable placeholders rather than machine-specific paths. Example local-only command:

```powershell
mem ask "AI detection workflow constraints for this project: target detector, institution rules, prior versions" --brain-root ${BRAIN_ROOT} --mode keyword-only --top 5
```

Treat this as optional context gathering. Only ask the user for constraints still missing after the local memory check.

Ask the user these questions explicitly, in one message, before doing any scanning:

1. **Target detector(s).** "Which AI detector are you trying to pass? GPTZero, Turnitin AI, Originality, Pangram, 知网 AIGC, 万方, 维普, 笔灵, PaperPass, something else? If you've already run one, what score did it give?"
2. **Institutional or publication rules.** "Is there a school style guide, thesis preparation manual, journal submission guide, or style sheet I should follow? If yes, please upload it. These documents often require specific voice/tense and can override normal humanization advice."
3. **Revision history.** "Is this a revision of an earlier version? If there are earlier drafts (v1, v2, …) please upload them — I need to make sure the new wording doesn't drift back toward an older version, which would raise similarity scores even as AI scores fall."
4. **Hard constraints.** "Are there elements that must not be changed — specific quotes, named contributions, equations, a fixed abstract, citation keys? Any page/word limit?"
5. **Grading or reader priorities.** "Is there anything the reader explicitly rewards? For example, some thesis rubrics grade 'self-reflection' — we should preserve that content, not sanitize it."
6. **Language preference for conversation.** "Do you want me to respond in English, Chinese, or mixed?"

Wait for answers before continuing. If the user says "just run it, I don't have extra info", accept that and proceed — but record in `discovery.md` that no external constraints were provided, so the user cannot later claim surprise if a school rule was violated.

## Step 4 — Actually scan the document

Now load the language-matched rule files:

- English: `rules/en/tell_tale_phrases.md`, `rules/en/sentence_patterns.md`, `rules/en/detector_profiles.md`.
- Chinese: `rules/zh/ai_cliches.md`, `rules/zh/sentence_patterns.md`, `rules/zh/context_whitelist.md`, `rules/zh/detector_profiles.md`.

For each pattern in the rule files:

1. Grep or search the actual document for concrete instances.
2. Record every hit with: location (section/page), verbatim quote, pattern category.
3. Count frequency. Patterns with zero hits are irrelevant for this document and should NOT be included in later rounds — including them wastes the user's time and invites errors.
4. If the same pattern hits heavily (> 5 instances), elevate it to a "primary target" for Layer 1.

Also scan for patterns the rule files do NOT cover. AI models evolve; new signatures appear. Record anything that felt AI-generated while reading in Step 1 but isn't in the rule list. Add a "novel patterns" section to the output.

**Do not plan edits in this step.** Discovery only describes what is present; it does not prescribe what to do about it.

### Step 4.5 — Context whitelist filtering for Chinese hits

For Chinese or mixed-language documents, apply the P0.4 context whitelist before forwarding any C-NN or S-NN hit to Layer 1.

Layer 0 must not treat a trigger word as a fix candidate until it has checked the surrounding phrase. Some Chinese triggers are high-risk only when they are isolated buzzwords, but are legitimate inside fixed terms, technical terms, or paired structures.

Known fixed-context filters:

- `生态`: whitelist `生态环境`, `生态系统`, `生态保护`, `市场生态`, `平台生态` unless the surrounding sentence uses the term as vague business filler.
- `闭环`: whitelist `控制闭环`, `闭环控制`; treat `业务闭环` as genre-dependent, not mechanical.
- `赋能`: distinguish `赋能教师` / `赋能学生` from business phrases such as `数字赋能`; the former usually needs semantic redesign, not one-word replacement.
- `痛点`: distinguish concrete `用户痛点` or `行业痛点` from empty slogan use.
- `不仅`: whitelist `不仅仅`, `不仅如此`; handle `不仅 X 而且 Y` as a paired structure, not a single-token replacement.
- `一方面`: if paired with `另一方面`, mark both sides as a paired structure. Do not rewrite only one side.
- `同时`: distinguish `与此同时` from adverbial uses such as `同时进行`.
- `进行`: flag `对 X 进行 Y` patterns, but whitelist normal verb uses such as `进行得很顺利`.
- `化` suffixes: whitelist established terms such as `数字化转型`, `自动化控制`, `信息化建设`; flag vague suffix stacking such as `个性化呈现` only when density or genre makes it suspicious.

For each filtered hit, record it in `discovery.md` as `whitelisted: true` with the matched context. Whitelisted hits are evidence for rule-library calibration, but they do not enter the Layer 1 candidate fix list. Ambiguous cases should be marked `whitelisted: review`, with a short note for Layer 1 rather than silently passed through as mechanical edits.

## Step 5 — Technical-fidelity inventory

Produce a list of elements that Layer 2 must preserve byte-identically:

- All numerical values appearing in the text (with context).
- All citation keys (`[1]`, `\cite{foo}`, etc.) — list them.
- All equation numbers and labels.
- All figure/table labels and cross-references.
- All code identifiers, file names, paths, version strings.
- All proper nouns the author has chosen (product names, project names, acronyms).
- Any section or chapter titles the user wants fixed.

This inventory is the guardrail for every downstream round.

## Step 6 — Produce `discovery.md`

Write a single file named `discovery.md` in the project's working directory (or the skill's output directory if no project). Use the template at `templates/discovery_output.md`.

Required sections, in order:

1. **Document summary** — language, genre, length, section structure.
2. **External constraints** — the user's answers to Step 3 questions, verbatim. If the user declined to answer, note that explicitly.
3. **Detected AI patterns** — grouped by category (fragments, clichés, tense slips, cliché vocabulary, etc.). Each group lists: pattern name, hit count, sample quotes with locations.
3A. **Context whitelist / exemption log** — required for Chinese or mixed documents; list trigger hits that were excluded or marked for review by Step 4.5.
4. **Novel patterns** — anything AI-sounding found in Step 4 but not in the rule library.
5. **Technical-fidelity inventory** — the guardrails list from Step 5.
6. **Recommended round count** — 3 rounds (light), 5 rounds (standard), 7 rounds (heavy). Base this on the number and severity of detected patterns, not on the document's length. Justify the recommendation in one paragraph.
7. **Open questions** — anything that still needs a user decision before Layer 1 can run.

Do NOT include proposed rewrites in `discovery.md`. Proposed rewrites belong in `plan.md` (Layer 1). Mixing them here tempts reviewers to approve rewrites they haven't seen in context.

## Step 7 — Hand off to the user

Present `discovery.md` to the user. Ask them to:

- Confirm the language and genre detection.
- Confirm the external constraints were captured correctly.
- Flag any detected pattern they disagree with (e.g., a stylistic choice they intend to keep).
- Flag any missed pattern they already know about.
- Approve the recommended round count or request a different number.

Once approved, the user moves to Layer 1. If the user rejects discovery significantly (e.g., "you missed the main thing"), redo the relevant step before proceeding — do not plan on broken diagnosis.

---

## Quality checklist for Layer 0

Before handing off `discovery.md`, verify:

- [ ] Language is detected and matching rule set is loaded.
- [ ] User has answered the six constraint questions (or explicitly declined).
- [ ] Every detected pattern has at least one verbatim quote with location.
- [ ] Chinese context whitelist hits are marked `whitelisted: true` or `whitelisted: review`.
- [ ] Patterns with zero hits in the document are not mentioned (no noise).
- [ ] Technical-fidelity inventory is complete and byte-exact.
- [ ] No proposed rewrites have leaked into `discovery.md`.
- [ ] Recommended round count is justified.
- [ ] File is saved as `discovery.md` in the correct directory.

If any box is unchecked, loop back and fix it. A bad discovery poisons every downstream round.

## What Layer 0 does NOT do

- It does not propose rewrites.
- It does not rank patterns by fix priority (that's Layer 1's job).
- It does not touch the document.
- It does not run the detector itself — the user does that, between Layer 2 rounds.
- It does not guess at constraints. When unsure, ask.

## Edge cases

**Document is already low-AI.** If the scan finds < 5 patterns total and the user's reported detector score is already acceptable, say so plainly in `discovery.md` and recommend zero rounds. Not every document needs rewriting.

**User uploads mid-project.** If the user says "I've already done some rewriting, here's v3 vs v7", treat v7 as the current document and v3 as a reference for anti-regression (note it in external constraints). Do not re-do work already done.

**Rule library has no entry for a detected pattern.** Record it under "novel patterns" and propose it as a candidate for the rule library after the project concludes. Do not silently drop it.

**User refuses to upload the school guide but mentions it exists.** Record that a guide exists but wasn't shared, and assume conservative defaults (third-person past tense, formal voice, no first person). Flag this explicitly so the user knows the plan is based on assumptions.
