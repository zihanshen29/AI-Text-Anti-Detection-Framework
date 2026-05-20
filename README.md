# AI Text Anti-Detection Framework

<p align="right">
  <a href="#中文">中文</a> | <a href="#english">English</a>
</p>

<a id="中文"></a>
<details open>
<summary><strong>中文 README</strong></summary>

## 这是什么

AI Text Anti-Detection Framework 是一套面向长文档的 AI 痕迹降低工作流。它不是“一键洗稿器”，而是把诊断、计划、执行和复盘拆开，让写作者能在保留事实、术语、引用和文体要求的前提下，逐轮减少文本里的 AI 味。

适用对象包括论文草稿、研究报告、技术说明、长篇博客和其他需要严肃编辑的文档。当前工作流同时支持中文和英文，并为两种语言维护了独立规则库，因为中文检测器更依赖套话词和固定搭配，英文检测器更关注句法节奏、并列结构和模板化表达。

## 核心能力

- 三层工作流：先发现问题，再制定逐轮修改计划，最后按计划执行。
- 中英文分离规则：英文规则偏句式和词汇信号，中文规则偏套话、欧化句式和上下文保护。
- 上下文保护：中文固定搭配如“生态环境”“数字化转型”“控制闭环”等不会被粗暴替换。
- 二次扫描：每个 AFTER 改写结果都需要检查，避免修掉旧 AI 信号时引入新 AI 信号。
- 批量评估模板：统一使用 35 分 rubric，并记录自然度、语义保真、异常样本和外部检测器状态。
- 可回滚：每一轮修改都要求记录 BEFORE/AFTER 和 CHANGES 日志，便于审查、复盘和撤回。

## 工作流

### Layer 0: Discovery

读取文档，判断语言、体裁和外部限制，扫描真正出现在文档里的 AI 信号，并标记不应替换的上下文。

产出：`discovery.md`

### Layer 1: Planning

把诊断结果转成可执行计划。每个修复项都必须包含精确的 BEFORE/AFTER、风险说明、语义检查、文体检查和 AFTER 二次扫描结果。

产出：`plan.md`

### Layer 2: Execution

按轮次执行修改。执行层只能做计划中批准的字面替换，不允许临场发挥。每一轮结束后记录改动、运行检测或人工评估，再决定是否进入下一轮。

产出：`CHANGES_roundN.md`

## 快速开始

### 在 Claude Code、Codex、Cursor 或其他 agent 中使用

1. 将本仓库克隆到本地。
2. 让 agent 读取 `ai-detection-workflow/SKILL.md`。
3. 上传或粘贴待处理文档，并说明目标检测器、文体要求和禁止修改的内容。
4. 先运行 Layer 0，确认 `discovery.md`。
5. 再运行 Layer 1，审查并批准 `plan.md`。
6. 最后按轮运行 Layer 2，每轮结束后记录检测分数或人工评估结果。

示例提示：

```text
请使用 ai-detection-workflow 处理这篇中文研究报告。
目标是降低 AI 痕迹，但不要改变事实、引用、专有名词和数据。
先只做 Layer 0 discovery，不要直接改正文。
```

### 手动使用 prompt

1. 使用 `workflow/discovery.md` 作为第一轮系统提示。
2. 审查 discovery 后，使用 `workflow/planning.md` 生成修改计划。
3. 批准计划后，使用 `workflow/execution.md` 按轮执行。
4. 每轮后填写 `templates/changes_log.md`，必要时使用 `templates/batch_eval_output.md` 做批量评估。

## 项目结构

```text
ai-detection-workflow/
├── SKILL.md
├── workflow/
│   ├── discovery.md
│   ├── planning.md
│   └── execution.md
├── rules/
│   ├── en/
│   │   ├── detector_profiles.md
│   │   ├── sentence_patterns.md
│   │   └── tell_tale_phrases.md
│   └── zh/
│       ├── ai_cliches.md
│       ├── context_whitelist.md
│       ├── detector_profiles.md
│       └── sentence_patterns.md
├── templates/
│   ├── batch_eval_output.md
│   ├── changes_log.md
│   ├── discovery_output.md
│   └── plan_output.md
└── meta/
    ├── prompts/
    ├── provider_articles/
    ├── reports/
    └── rubric/
```

## 评估标准

离线评估默认使用 35 分制：

- AI 信号下降：5 分
- 可读性与自然度：5 分
- 语义与事实保真：5 分
- 体裁适配：5 分
- 结构与逻辑：5 分
- 修改可控性：5 分
- 检测与复盘记录：5 分

批量报告必须注明是否运行外部检测器。如果未运行 GPTZero、Turnitin、Originality.ai、知网、万方等外部检测器，报告只能称为离线评估，不能伪装成检测器结果。

## 状态

- 已完成三层工作流。
- 已完成中英文规则库。
- 已加入中文上下文白名单。
- 已加入 AFTER 二次扫描要求。
- 已加入批量评估模板和 35 分 rubric。
- 仍需更多真实文档和真实检测器结果来继续校准规则权重。

## 使用边界

本项目用于编辑和复核文本，尤其适合处理被过度检测器误伤的人工写作，或对 AI 辅助草稿进行负责任的人工修订。它不能替代学术诚信要求，也不能让使用者规避学校、期刊或机构对 AI 使用披露的规定。

如果你的机构要求声明 AI 辅助，请按规定声明。

## 许可证

MIT

</details>

---

<a id="english"></a>
<details>
<summary><strong>English README</strong></summary>

## What This Is

AI Text Anti-Detection Framework is a structured workflow for reducing AI-like signals in long-form documents. It is not a one-click paraphraser. It separates diagnosis, planning, execution, and review so writers can reduce machine-like phrasing without damaging facts, terminology, citations, or genre requirements.

It is intended for theses, research papers, technical reports, long-form essays, blog posts, and other documents that need careful editing. The framework supports both Chinese and English with separate rule libraries because Chinese detectors tend to react more strongly to fixed phrases and cliches, while English detectors tend to emphasize syntax, rhythm, parallelism, and templated phrasing.

## Key Features

- Three-layer workflow: discover the problem, plan controlled fixes, then execute round by round.
- Separate Chinese and English rules: English rules focus on sentence patterns and tell-tale phrases; Chinese rules focus on cliches, Europeanized syntax, and context-sensitive terms.
- Context protection: fixed Chinese collocations such as "生态环境", "数字化转型", and "控制闭环" are protected from blunt replacement.
- Secondary scan: every AFTER string must be checked so a fix does not introduce a new AI signal.
- Batch evaluation template: uses a 35-point rubric with naturalness, semantic fidelity, outlier handling, and external-detector status.
- Reviewable changes: each round records BEFORE/AFTER pairs and a CHANGES log, making the process auditable and reversible.

## Workflow

### Layer 0: Discovery

Read the document, identify language, genre, external constraints, and the AI-signal patterns that actually appear in the text. Also mark contexts that should be exempt from replacement.

Output: `discovery.md`

### Layer 1: Planning

Turn the diagnosis into a controlled plan. Every fix must include exact BEFORE/AFTER text, risk notes, semantic checks, genre checks, and a secondary scan of the AFTER string.

Output: `plan.md`

### Layer 2: Execution

Apply approved changes one round at a time. The execution layer is restricted to the approved literal replacements and must not improvise. After each round, record the changes, run detection or manual evaluation, and decide whether another round is needed.

Output: `CHANGES_roundN.md`

## Quick Start

### Use with Claude Code, Codex, Cursor, or another agent

1. Clone this repository.
2. Ask the agent to read `ai-detection-workflow/SKILL.md`.
3. Upload or paste the document, then specify the target detector, style constraints, and content that must not be changed.
4. Run Layer 0 first and review `discovery.md`.
5. Run Layer 1 next and approve `plan.md`.
6. Run Layer 2 round by round, recording detector scores or manual evaluation results after each round.

Example prompt:

```text
Use ai-detection-workflow on this English technical report.
The goal is to reduce AI-like signals without changing facts, citations, terms, or data.
Start with Layer 0 discovery only. Do not rewrite the document yet.
```

### Manual prompt workflow

1. Use `workflow/discovery.md` as the first system prompt.
2. After reviewing discovery, use `workflow/planning.md` to create the fix plan.
3. After approving the plan, use `workflow/execution.md` to run each round.
4. After each round, fill in `templates/changes_log.md`; use `templates/batch_eval_output.md` for batch evaluation when needed.

## Repository Structure

```text
ai-detection-workflow/
├── SKILL.md
├── workflow/
│   ├── discovery.md
│   ├── planning.md
│   └── execution.md
├── rules/
│   ├── en/
│   │   ├── detector_profiles.md
│   │   ├── sentence_patterns.md
│   │   └── tell_tale_phrases.md
│   └── zh/
│       ├── ai_cliches.md
│       ├── context_whitelist.md
│       ├── detector_profiles.md
│       └── sentence_patterns.md
├── templates/
│   ├── batch_eval_output.md
│   ├── changes_log.md
│   ├── discovery_output.md
│   └── plan_output.md
└── meta/
    ├── prompts/
    ├── provider_articles/
    ├── reports/
    └── rubric/
```

## Evaluation Rubric

Offline evaluation uses a 35-point rubric:

- AI-signal reduction: 5 points
- Readability and naturalness: 5 points
- Semantic and factual fidelity: 5 points
- Genre fit: 5 points
- Structure and logic: 5 points
- Change controllability: 5 points
- Measurement and review record: 5 points

Batch reports must state whether external detectors were run. If GPTZero, Turnitin, Originality.ai, CNKI, Wanfang, or similar detectors were not run, the result must be described as offline evaluation rather than an external detector score.

## Status

- Three-layer workflow is implemented.
- Chinese and English rule libraries are implemented.
- Chinese context whitelist is included.
- AFTER-string secondary scanning is required.
- Batch evaluation template and 35-point rubric are included.
- More real documents and real detector reports are still needed to calibrate rule weights.

## Responsible Use

This project is for text editing and review, especially when human writing is over-flagged by unreliable detectors or when AI-assisted drafts need responsible human revision. It does not replace academic integrity rules and does not remove any disclosure obligations required by a school, journal, employer, or institution.

If your institution requires AI-use disclosure, disclose it.

## License

MIT

</details>
