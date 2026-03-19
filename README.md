# AI-Text-Anti-Detection-Framework

## 项目概述
本框架利用逆向工程原理，针对困惑度（Perplexity）、突发性（Burstiness）和N元语法（N-grams），通过负面词汇约束和句法方差控制，将机器文本转化为具有自然人类统计特征的文本。本项目旨在恢复AI文本的人类认知流动性、消除机器生成的统计学刻板印象，并提升自动化报告的可读性与真实感。

## 检测机制解构
主流检测系统（如 GPTZero, Turnitin）之所以能够精准发现 AI 文本，是因为它们捕捉到了当前生成式AI在追求全局概率最优解时表现出的高度统一性。本框架通过强制拉升局部可预测性的困惑度 ($PPL$) 以及宏观结构上的句子长度标准差 ($\sigma_l$)，从数学层面上摧毁这些检测算法赖以生存的平滑度特征。

## 部署与使用

**1. 网页端大模型 (ChatGPT, Claude 等) 使用：**
直接前往 `prompts/` 目录，复制 `english_humanizer.md` 或 `chinese_humanizer.md` 的全部内容，作为 System Prompt 或对话的首条指令发送给模型即可。

**2. 自动化 Agent (Claude Code, Cursor 等) 部署：**
将 `skills/` 目录下的相应 `SKILL.md` 下载并克隆到你的本地工作流技能目录中（例如 `~/.claude/skills/`），实现一键式 API 调用。

## 基准测试对比
基于多轮内部基准测试：
***未优化原始 AI 文本**（高频触发 "delve", "landscape", "首先" 等红色预警词）：AI 判定率通常 **> 99%**
**经本框架 Humanizer 重构后文本**：AI 判定率稳定降至 **< 5%**

## 迭代与演进
随着 Turnitin 等检测系统在 2026 年及未来的持续架构升级，AI 的写作指纹也在不断变化。欢迎全球开发者与研究人员通过提交 Pull Request，持续贡献新发现的高危词汇和语法模板，共同维护并演进本反侦察规则库！

# AI-Text-Anti-Detection-Framework

## Overview
This framework utilizes reverse engineering principles targeting Perplexity, Burstiness, and N-grams. By applying negative lexical constraints and controlling syntactic variance, it transforms machine-generated text into text with natural human statistical features[c. This project aims to restore human cognitive fluidity to AI text, eliminate machine-generated statistical stereotypes, and enhance the readability and authenticity of automated reports.

## Detection Theory
Mainstream detection systems (such as GPTZero and Turnitin) can accurately identify AI text because they capture the high degree of uniformity exhibited by current generative AI when pursuing the global optimal probability solution. This framework destroys the smoothness features these detection algorithms rely on at a mathematical level by forcibly inflating the local predictability's perplexity ($PPL$) and the macro-structural standard deviation of sentence length ($\sigma_l$).

## Installation & Usage

**1. Web-based LLM Usage (ChatGPT, Claude, etc.):**
Navigate directly to the `prompts/` directory, copy the entire content of `english_humanizer.md` or `chinese_humanizer.md`, and send it to the model as a System Prompt or the first instruction in your conversation.

**2. Automated Agent Deployment (Claude Code, Cursor, etc.):**
Download and clone the corresponding `SKILL.md` from the `skills/` directory into your local workflow skills directory (e.g., `~/.claude/skills/`) to enable one-click API invocation.

## Empirical Results
Based on multiple rounds of internal benchmarking:
***Unoptimized raw AI text** (frequently triggering red flag words like "delve", "landscape", "首先"): AI detection rate is typically **> 99%**.
***Text reconstructed by this framework's Humanizer**: AI detection rate stably drops to **< 5%**.

## Continuous Updates
As detection systems like Turnitin undergo continuous architectural upgrades in 2026 and beyond, AI writing fingerprints are also constantly evolving. Developers and researchers worldwide are welcome to continuously contribute newly discovered high-risk vocabulary and syntactic templates by submitting Pull Requests, collaboratively maintaining and evolving this anti-detection rule base!
