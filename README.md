# AI-Text-Anti-Detection-Framework

## Overview (项目概述)
[cite_start]本框架利用逆向工程原理，针对困惑度（Perplexity）、突发性（Burstiness）和N元语法（N-grams），通过负面词汇约束和句法方差控制，将机器文本转化为具有自然人类统计特征的文本 [cite: 143][cite_start]。本项目旨在恢复AI文本的人类认知流动性、消除机器生成的统计学刻板印象，并提升自动化报告的可读性与真实感 [cite: 141, 143]。

## Detection Theory (检测机制解构)
[cite_start]主流检测系统（如 GPTZero, Turnitin）之所以能够精准发现 AI 文本，是因为它们捕捉到了当前生成式AI在追求全局概率最优解时表现出的高度统一性 [cite: 143, 146][cite_start]。本框架通过强制拉升局部可预测性的困惑度 ($PPL$) 以及宏观结构上的句子长度标准差 ($\sigma_l$)，从数学层面上摧毁这些检测算法赖以生存的平滑度特征 [cite: 143]。

## Installation & Usage (部署与使用)

**1. 网页端大模型 (ChatGPT, Claude 等) 使用：**
直接前往 `prompts/` 目录，复制 `english_humanizer.md` 或 `chinese_humanizer.md` 的全部内容，作为 System Prompt 或对话的首条指令发送给模型即可。

**2. 自动化 Agent (Claude Code, Cursor 等) 部署：**
[cite_start]将 `skills/` 目录下的相应 `SKILL.md` 下载并克隆到你的本地工作流技能目录中（例如 `~/.claude/skills/`），实现一键式 API 调用 [cite: 143]。

## Empirical Results (基准测试对比)
[cite_start]基于多轮内部基准测试 [cite: 143]：
* [cite_start]**未优化原始 AI 文本**（高频触发 "delve", "landscape", "首先" 等红色预警词）：AI 判定率通常 **> 99%** [cite: 143]
* [cite_start]**经本框架 Humanizer 重构后文本**：AI 判定率稳定降至 **< 5%** [cite: 143]

## Continuous Updates (迭代与演进)
[cite_start]随着 Turnitin 等检测系统在 2026 年及未来的持续架构升级，AI 的写作指纹也在不断变化 [cite: 143][cite_start]。欢迎全球开发者与研究人员通过提交 Pull Request，持续贡献新发现的高危词汇和语法模板，共同维护并演进本反侦察规则库 [cite: 143]！
