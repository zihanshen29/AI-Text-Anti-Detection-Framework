# AI Detection Workflow

写在开头
是什么？这个工作流是我为了降低文章的ai率自己跑出来的，目前只试了英文文本。实测效果：修改之后对比修改之前，读起来的“ai味”明显变少，“人味”更浓。
如何使用？此工作流建议配合Claude Code或者Codex等智能体使用，文章建议使用latex格式，这两者结合可以将文章内容和格式完全交给ai来做，你只需要写提示词和审查。跑完这个工作流后，先把文章送检，查出来的报告把里面ai率较高的段落再重点过一遍，最多2遍后ai率即可达标。

<!-- What this is · 它是什么 -->

**A structured, three-layer framework for reducing AI-detection signals in long-form documents** — theses, research papers, reports, long blog posts — **without** destroying technical content or leaving you guessing whether anything actually improved.

**一个用于降低长文档 AI 检测信号的三层结构化框架** —— 适用于毕业论文、学术论文、研究报告、长篇博客等 —— **不破坏**原文的技术内容，也不让你猜测"到底有没有改好"。

Supports both English and Chinese. The two languages have independent rule libraries because the detectors behave differently.

同时支持英文和中文。两种语言使用独立的规则库，因为检测器对中英文的工作机制并不相同。

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
├── SKILL.md                      # entry point, skill metadata
├── workflow/
│   ├── discovery.md              # Layer 0 prompt
│   ├── planning.md               # Layer 1 prompt
│   └── execution.md              # Layer 2 prompt
├── rules/
│   ├── en/                       # English — syntactic + vocabulary signals
│   │   ├── sentence_patterns.md  # P-01..P-20 structural patterns
│   │   ├── tell_tale_phrases.md  # V-01..V-45 vocabulary
│   │   └── detector_profiles.md  # GPTZero, Turnitin, Originality, ...
│   └── zh/                       # 中文 —— 词汇套语为主，句法为辅
│       ├── ai_cliches.md         # C-01..C-18 套话词表
│       ├── sentence_patterns.md  # S-01..S-20 句法模式
│       └── detector_profiles.md  # 知网、万方、维普、笔灵、PaperPass
└── templates/                    # output file skeletons
    ├── discovery_output.md
    ├── plan_output.md
    └── changes_log.md
```

The English and Chinese rule libraries are deliberately **asymmetric**. English AI detectors mostly weight syntactic features (burstiness, em-dash density, parallel structure), so `rules/en/` is pattern-heavy. Chinese detectors mostly weight fixed vocabulary (赋能/抓手/综上所述 …), so `rules/zh/` is word-list-heavy. Forcing the two into the same format would produce a worse skill for both languages.

---

## How to use it · 如何使用

This is an [Anthropic Skill](https://docs.claude.com/en/docs/claude-code/skills). You can also drop the individual prompt files into Cursor, Codex, Claude Code, Cline, or any other agent that accepts markdown prompts.

本项目是一个 [Anthropic Skill](https://docs.claude.com/en/docs/claude-code/skills)。你也可以把里面的 prompt 文件直接放进 Cursor、Codex、Claude Code、Cline 或任何能读 markdown prompt 的 agent 里使用。

### With Claude.ai or Claude Code · 在 Claude.ai 或 Claude Code 里使用

1. Clone this repo into your skill directory.
2. Start a chat: *"I want to lower the AI detection score on this document"* or *"帮我降低这篇论文的 AI 率"*.
3. Upload the document. Claude loads Layer 0 automatically and asks you the discovery questions.

——

1. 把本仓库 clone 到你的 skill 目录下。
2. 开始新对话："I want to lower the AI detection score on this document" 或 "帮我降低这篇论文的 AI 率"。
3. 上传文档。Claude 会自动加载 Layer 0，向你提问若干诊断问题。

### Manually (with any agent) · 手动使用（任意 agent）

1. Start with `workflow/discovery.md` as the system prompt.
2. After the agent produces `discovery.md`, start a new conversation with `workflow/planning.md` and paste in the approved discovery.
3. For each round, open a new conversation with `workflow/execution.md` and paste in the approved plan plus "run Round N".

——

1. 用 `workflow/discovery.md` 作为 system prompt，上传文档开始第一轮对话。
2. Agent 产出 `discovery.md` 后，开一段新对话，这次用 `workflow/planning.md` 作为 system prompt，把上一步确认好的 discovery 贴进去。
3. 每一个执行轮次都新开一段对话，用 `workflow/execution.md` 作为 system prompt，粘入已批准的 `plan.md`，并指定 "run Round N"。

### Important: one round per invocation · 关键：一次对话只跑一轮

Between rounds you **must** compile the document, run the detector, record the score, and only then invoke the next round. This measurement checkpoint is the difference between a framework that works and one that pretends to.

每一轮之间你**必须**先编译文档、跑检测器、记录分数，**然后**再启动下一轮。这个测量断点是本框架与"一键降 AI"工具最核心的区别 —— 没有它，你无法判断改写到底是变好了还是变差了。

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
- [x] English rules — sentence patterns (P-01..P-20), tell-tale phrases (V-01..V-45), detector profiles (6 detectors)
- [x] Chinese rules — AI clichés (C-01..C-18), sentence patterns (S-01..S-20), detector profiles (5 detectors)
- [ ] End-to-end validation on a real document
- [ ] Iteration based on real-run feedback

---

## What this is NOT for

This tool is for writers whose **legitimately human-written content** was flagged by overactive detectors, or for revising **AI-drafted content** that needs to preserve technical accuracy (e.g., a researcher who used AI as a drafting aid but needs to submit work that reflects their own technical judgment).

It is **not** a tool for academic dishonesty. Using it does not remove your responsibility to follow the academic integrity rules of your institution. If your university requires you to declare AI assistance, declare it.

---

## License

MIT
