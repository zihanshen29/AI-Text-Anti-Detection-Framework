# AI Detection Workflow

## English

This repository defines a three-layer workflow for reducing AI-detection signals in English and Chinese documents while preserving technical fidelity, citations, numbers, and author intent.

- Layer 0 (`workflow/discovery.md`) diagnoses the actual document, language, genre, external constraints, and rule hits.
- Layer 1 (`workflow/planning.md`) produces exact before/after edit plans for user approval.
- Layer 2 (`workflow/execution.md`) applies approved edits one round at a time and records measurement results.
- `tools/` contains deterministic offline scanners and guardrail checks. They provide reproducible local statistics and are not detector simulators.
- AFTER-side replacement guidance now includes a Chinese blacklist/disfavored list and English replacement guidance, plus a plan-level replacement diversity check to avoid collapsing many fixes into one mechanical phrase.

The workflow does not promise any external detector result. Offline rule hits, structural metrics, and rubric totals are local aids for planning and review.

## 中文

本仓库定义了一套三层工作流，用于在保留技术事实、引用、数字和作者意图的前提下，降低中英文文档中的 AI 检测信号。

- Layer 0（`workflow/discovery.md`）诊断当前文档的语言、体裁、外部约束和实际规则命中。
- Layer 1（`workflow/planning.md`）生成可审阅的 exact before/after 修改计划。
- Layer 2（`workflow/execution.md`）按轮次执行已批准的修改，并记录测量结果。
- `tools/` 提供确定性的离线扫描器和保真检查工具，用于生成可复现的本地统计；这些工具不是检测器模拟器。
- AFTER 侧替换规则现包含中文黑名单/降格替换提示、英文替换指导，以及计划级替换多样性检查，避免大量修复收敛成同一个机械表达。

本工作流不承诺任何外部检测器结果。离线规则命中、结构指标和人工量表总分只用于本地规划与审阅。
