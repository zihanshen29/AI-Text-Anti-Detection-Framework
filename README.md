# AI Detection Workflow

A structured, three-layer framework for reducing AI-detection signals in long-form documents — theses, research papers, reports, long blog posts — **without** destroying technical content or leaving you guessing whether anything actually improved.

支持中文和英文文档，两种语言各有独立的规则库。

---

## Why this exists

Most "one-click AI humanizer" tools fail in predictable ways:

- They touch content that shouldn't be touched — numbers, equations, citations, proper nouns.
- They miss external constraints (school style guides, journal house rules) because they never ask.
- They introduce new AI patterns while fixing old ones.
- They give you no way to measure whether the rewrite actually lowered the detector score.

This framework **never rewrites in a single pass**. The work is split into three layers. You review between layers. You run the detector between rounds. If a round makes things worse, you can roll back exactly what changed.

---

## The three layers

### Layer 0 — Discovery
Read the document, detect language and genre, **ask** about external constraints (school guide? previous drafts? which detector are you targeting?), and scan for AI patterns actually present in *your* document — not the generic checklist every humanizer uses.

→ produces `discovery.md` (you review)

### Layer 1 — Planning
Turn the diagnosis into a round-by-round plan. Every fix gets an exact **before/after** pair, an anti-regression check against your earlier drafts (so you don't accidentally drift back toward a version that would raise similarity scores), and a technical-fidelity check so no citation or equation reference gets disturbed.

→ produces `plan.md` (you approve)

### Layer 2 — Execution
Apply one round at a time. Strict literal string replacement — the agent is forbidden from improvising. Between rounds, you compile the document, run the detector, and record the score. If the score dropped, continue. If not, pause and diagnose.

→ produces `CHANGES_round1.md`, `CHANGES_round2.md`, … (one per round)

---

## What a session looks like

```
You:     Here's my thesis. I need to lower the AI score.

Claude:  Before I start, a few questions:
         - Which detector did you use? What score did it give?
         - Is there a school style guide or thesis manual?
         - Do you have earlier drafts (v1, v2...)?
         - Anything I must not change?

You:     GPTZero, 87%. Here's the Heriot-Watt guide.
         Earlier drafts v10 and v12 attached. Don't touch 
         equations or citations.

Claude:  [Layer 0 scans the document]
         Here's discovery.md. I found 14 fragment sentences,
         22 tense slips that violate your school guide, 6 AI 
         cliché phrases. Recommended 5 rounds. Approve?

You:     Looks right. Go.

Claude:  [Layer 1 plans]
         Here's plan.md with 42 fixes across 5 rounds. Every 
         fix has a verbatim before/after, checked against 
         v10 and v12. Review?

You:     Approved.

Claude:  [Layer 2 runs Round 1]
         Round 1 complete. 12 fixes applied. Compile, run 
         the detector, fill in the Measurement section of 
         CHANGES_round1.md, then tell me when to start Round 2.

You:     [compiles, runs GPTZero: 87% → 64%]
         Good drop. Run Round 2.

...
```

---

## Structure

```
ai-detection-workflow/
├── SKILL.md                   # entry point, skill metadata
├── workflow/
│   ├── discovery.md           # Layer 0 prompt
│   ├── planning.md            # Layer 1 prompt
│   └── execution.md           # Layer 2 prompt
├── rules/
│   ├── en/                    # English — syntactic patterns
│   │   └── sentence_patterns.md
│   └── zh/                    # 中文 — 词汇和套语
│       └── ai_cliches.md
└── templates/                 # output file skeletons
    ├── discovery_output.md
    ├── plan_output.md
    └── changes_log.md
```

The English and Chinese rule libraries are deliberately **asymmetric**. English AI detectors mostly weight syntactic features (burstiness, em-dash density, parallel structure), so `rules/en/` is pattern-heavy. Chinese detectors mostly weight fixed vocabulary (赋能/抓手/综上所述 …), so `rules/zh/` is word-list-heavy. Forcing the two into the same format would produce a worse skill for both languages.

---

## How to use it

This is an [Anthropic Skill](https://docs.claude.com/en/docs/claude-code/skills). You can also drop the individual prompt files into Cursor, Codex, Claude Code, Cline, or any other agent that accepts markdown prompts.

**With Claude.ai or Claude Code:**
1. Clone this repo into your skill directory.
2. Start a chat: *"I want to lower the AI detection score on this document"* or *"帮我降低这篇论文的 AI 率"*.
3. Upload the document. Claude loads Layer 0 automatically and asks you the discovery questions.

**Manually (with any agent):**
1. Start with `workflow/discovery.md` as the system prompt.
2. After the agent produces `discovery.md`, start a new conversation with `workflow/planning.md` and paste in the approved discovery.
3. For each round, open a new conversation with `workflow/execution.md` and paste in the approved plan plus "run Round N".

---

## Supported detectors

**English:** GPTZero · Turnitin AI · Originality.ai · Pangram · ZeroGPT · Copyleaks

**中文:** 知网 AIGC · 万方 AIGC · 维普 · 笔灵 · PaperPass

Rules are organized so you can prioritize by target detector. If you only care about GPTZero, Layer 1 will weight the fixes that GPTZero specifically flags. If you care about 知网, it picks a different priority order.

---

## Status

Work in progress. Completed so far:

- [x] Three-layer workflow prompts (`SKILL.md` + `workflow/*`)
- [x] Output templates (3 files)
- [x] English rule library — sentence patterns (20 rules)
- [x] Chinese rule library — AI clichés (18 rules)
- [ ] English — tell-tale phrases, detector profiles
- [ ] Chinese — sentence patterns, detector profiles
- [ ] End-to-end validation on a real document

---

## What this is NOT for

This tool is for writers whose **legitimately human-written content** was flagged by overactive detectors, or for revising **AI-drafted content** that needs to preserve technical accuracy (e.g., a researcher who used AI as a drafting aid but needs to submit work that reflects their own technical judgment).

It is **not** a tool for academic dishonesty. Using it does not remove your responsibility to follow the academic integrity rules of your institution. If your university requires you to declare AI assistance, declare it.

---

## License

MIT
