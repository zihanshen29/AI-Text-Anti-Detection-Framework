# Workflow Upgrade Plan — 2026-06-10

**Status:** approved-for-execution（执行者按任务更新状态：pending / in-progress / done / blocked）
**Author:** Claude（基于 2026-06-10 全仓评审）
**Executor:** Codex
**Base commit:** b3aa521 (= v1.1.0, main, 与 origin/main 同步)
**评审依据:** `workflow/*.md`、`rules/{en,zh}/*.md`、`templates/*.md`、`meta/rubric/offline_rubric.md`、`meta/prompts/eval_prompt.md`、`meta/reports/workflow_patch_recommendations_20260521.md`、`meta/provider_articles/run_20260520_rewritten_{zh,en}/*_evaluation_report_after_repair.md`

---

## 0. 背景与目标

2026-05-20 批量评测与修复闭环验证了三层工作流的纪律性，但暴露出三个系统性短板：

1. **确定性环节零工具化。** watch-list 计数、规则命中统计、BEFORE 预检、保真校验、反回归重叠度全靠评测 agent 手算，昂贵且不可复现。两份评测报告各自临时拼 watch-list（zh 报告的 31 词清单 ≠ 规则库本体），跨报告数字不可比。
2. **AFTER 侧教训没有回流规则库。** `context_whitelist.md` 只防 BEFORE 侧误触发；实测发现的硬失败几乎全在 AFTER 侧（`先看`、`不只仅`、`协作体系环境` 等），目前只存在于评测报告中，未来运行不会加载。`ai_cliches.md` C-04 至今仍推荐"闭环 → 完整流程"，而复评已判定该替换在部分语境生硬。
3. **定量度量对结构层（S/P 级）是盲的。** 唯一定量指标是字面词表命中数，优化压力全压在词汇层；zh 复评自认"列表式结论、统一段落节奏等 S 级信号仍在"。

本方案分四个 Phase、18 个任务，目标：把确定性操作脚本化、把 AFTER 侧教训机制化回流、补结构层定量指标，并清理一致性债务。

## 0.1 全局执行纪律（适用于所有任务）

- **不改变三层契约。** Layer 0/1/2 的职责边界、门禁、Layer 2 严格禁令（execution.md "Strict prohibitions"）一律不动。
- **不削弱度量诚实性。** 所有"离线分数 ≠ 外部检测器分数"的免责声明必须原样保留；新增工具输出也必须带同样声明。
- **历史评测报告只可追加，不可改写。** 对 `meta/provider_articles/**` 和 `meta/reports/**` 下既有报告，只允许追加明确标注日期的 Erratum 小节，不得修改原文。
- **不动评测语料。** `meta/provider_articles/**` 与 `meta/generated_articles/**` 下的文章内容一律不改（T14 只是追加说明文件）。
- **工具只用 Python 标准库**，显式 UTF-8 读写，Windows / Unix 双平台可运行，统一退出码：0 = 通过，1 = 有发现（findings），2 = 运行错误。每个工具支持 `--help` 与 `--json`。
- **双语文档同步。** 改 README 必须中英两节同改；改 SKILL.md file map 必须与磁盘实际文件一致。
- **提交策略见 §5。** 每个 Phase 一个 commit；全部完成且冒烟报告产出后，停下来等用户审阅，再 push / 打 tag。

---

## Phase 1 — 工具化与机器可读规则（最高优先级）

### T1 — 规则库机器可读化：`rules/en/rules.yaml` + `rules/zh/rules.yaml`

**Task status:** done

**目的：** 让扫描可以脚本化；散文规则文件继续承载"为什么/修改方向"，YAML 承载可机器匹配的表面特征。

**改动：**
- 从 `rules/en/sentence_patterns.md`（P-01..P-20，其 **Detect** 字段本就要求 grep-able）、`rules/en/tell_tale_phrases.md`（V-01..V-45）、`rules/zh/ai_cliches.md`（C-01..C-18，词表字段）、`rules/zh/sentence_patterns.md`（S-01..S-20）提取，生成两个 YAML。
- 每条规则的 schema：

```yaml
- id: C-04
  name: 互联网/商业黑话
  family: C            # P / V / C / S
  match_type: literal  # literal | regex | structural
  literals: [赋能, 抓手, 痛点, 闭环, 生态, ...]   # match_type=literal 时必填，与散文词表逐项一致
  pattern: null        # match_type=regex 时填（如 em-dash U+2014 计数）
  scan: auto           # auto | manual（structural 无法机检的标 manual）
  frequency: high      # high | normal（high 集合见 T12，初始值取自 planning.md Step 4.2 现行清单）
  whitelist_ref: rules/zh/context_whitelist.md   # 有上下文白名单的规则填
  source: rules/zh/ai_cliches.md#c-04
```

- `frequency: high` 的初始集合（与 `workflow/planning.md` Step 4.2 现行清单一致）：
  - EN: P-01, P-04, P-06, P-08, P-12, P-16, P-19, V-01, V-02, V-03, V-08, V-11, V-19, V-20
  - ZH: C-01, C-04, C-05, C-06, C-08, C-09, C-12, C-14, S-01, S-04, S-06, S-11, S-12, S-14
- 在四个散文规则文件头部加一行维护说明：修改词表/Detect 时必须同步更新对应 rules.yaml。

**验收：**
- 散文文件中每条 C/V 规则的词表项在 YAML 中逐项可找到（抽查每族 ≥ 3 条规则全量比对）。
- 无法字面化的结构规则（如句长均匀性）标 `scan: manual`，不得伪造成 literal。
- T2 的扫描器能直接加载两个 YAML 不报错。

### T2 — `tools/scan_rules.py`：规则命中扫描器

**Task status:** done

**目的：** 取代各报告临时手拼 watch-list，统一定量口径。

**改动：** 新建 `tools/scan_rules.py`：
- 参数：`--text <file>`（可多个）、`--lang {en,zh,auto}`、`--rules <yaml>`（默认按 lang 取 `rules/<lang>/rules.yaml`）、`--baseline <file>`（对比模式：source vs rewrite，输出每规则 before/after/delta）、`--json` / 默认输出 Markdown 表。
- 匹配语义：EN literal 用单词边界（`\b`），ZH literal 用纯子串；regex 规则按 pattern 执行；`scan: manual` 规则在输出尾部列为 "manual-only，未计数"。
- 输出包含：每规则命中数、每千字归一化密度、合计；尾部固定打印免责声明行："Offline literal hits only; not a detector score."
- 读入前做编码预检：发现 U+FFFD 或 GBK 乱码标记串（`锟斤拷` 及 discovery.md Step 1 列出的标记）即退出码 2 并报告，不输出统计。

**验收：** 对 `meta/provider_articles/run_20260520/deepseek/topic_05.md` 与 `run_20260520_rewritten_zh/deepseek/topic_05.md` 跑通 `--baseline` 模式；对 `run_20260520/gemini/topic_04.md` 能以退出码 2 报编码异常（衔接 T14）。

### T3 — `tools/structure_metrics.py`：结构层指标

**Task status:** done

**目的：** 补上 S/P 级结构信号的定量盲区。**不声称对应任何检测器分数。**

**改动：** 新建 `tools/structure_metrics.py`，输入单文件或 `--baseline` 对比，输出以下确定性指标（JSON + Markdown 表）：
- 通用：句子数；句长均值与变异系数 CV（burstiness 代理）；段落长度均值与 CV；标点多样性（每千字不同标点种数）；em-dash（U+2014）计数；spaced hyphen `" - "` 计数；滑动窗口 type-token ratio（窗口 500 token）。
- 相邻段落开头重复率：相邻两段首 5 个 token 完全一致的比例。
- ZH 专属：每句"的"出现次数的均值/最大值；句长以字符计。EN 以词计。
- 分句规则写死并在 `--help` 里注明局限：ZH 按 `。！？；` 切，EN 按 `.!?` + 空白切（不处理缩写歧义，保持确定性优先）。
- 输出尾部固定免责声明："Structural proxies only; no validated correlation to any external detector."

**验收：** 对 zh、en 各取 2 对 source/rewrite 跑通对比模式，报告中能看出改写后句长 CV 等指标的变化方向（不设硬阈值，只要求可输出、可复现）。

### T4 — `tools/preflight_plan.py`：BEFORE 串预检

**Task status:** done

**目的：** 把 execution.md Step 2 的预检（每条 BEFORE 在目标文件恰好出现一次）自动化。

**改动：** 新建工具：解析 `plan.md` 的 fix block（`BEFORE (verbatim from current document):` 后的引用块，格式见 planning.md Step 4），对 `--doc <file>` 逐条检查出现次数；输出表格：Fix ID / 出现次数 / pass-zero-multi。任一非 1 → 退出码 1。
- 解析器对模板变体要宽容（容忍 BOM、CRLF/LF），但匹配本身严格字面，不做任何模糊匹配。

**验收：** 用一个手工构造的最小 plan.md + 目标文档样例验证三种情形（恰好 1 次 / 0 次 / 2 次）各自的输出与退出码；样例放 `tools/testdata/`。

### T5 — `tools/guardrails_diff.py`：保真校验

**Task status:** done

**目的：** 自动化 5-20 评测中手工做的数字/标题/引用保真检查（discovery.md Step 5 清单）。

**改动：** 新建工具，对 source/rewrite 一对文件检查并输出 pass/fail 表：
- 数字 token 多重集一致（含百分比、小数）；
- 引用键集合一致（`[N]`、`\cite{...}` 两种形态）；
- Markdown 标题序列一致（数量与文本）；
- 公式/图表标签（`\label{...}`、`图 N` / `表 N` / `Figure N` / `Table N`）集合一致；
- EN 文档中不应出现 CJK 字符（出现即 fail，对应 5-20 中文残留事故）；
- 乱码标记扫描（同 T2）。

**验收：** 对 en 正常 15 对中任取 4 对跑通且全 pass；人为构造一个数字被改动的样例能 fail（样例放 `tools/testdata/`）。

### T6 — `tools/overlap_check.py`：反回归重叠度

**Task status:** done

**目的：** 把 planning.md Step 5 的">70% token overlap / 10-word window"从 LLM 心算变成脚本。

**改动：** 新建工具：`--current <file> --prior <file> [--window 10] [--threshold 0.7]`，滑动窗口逐一比对 token 重叠率，输出超阈值窗口列表（位置 + 双侧文本摘录）与总体超阈值窗口占比。ZH 按字符 bigram 分词或逐字处理（实现里写明选择）。

**验收：** 同一文件 vs 自身 → 100% 超阈值；两篇无关文章 → 接近 0%；输出含位置信息可定位。

### T7 — `tools/README.md` + 冒烟报告

**Task status:** done

**目的：** 工具可被未来的评测 agent 与人类直接使用；并用真实语料验证 Phase 1 全部产出。

**改动：**
- 写 `tools/README.md`：每个工具一段用途 + 一行示例命令 + 退出码约定 + 统一免责声明。
- 跑一次完整冒烟：用 T2/T3/T5 对 run_20260520 的 zh 全部 16 对（topics 05-08 × 4 模型，source vs `run_20260520_rewritten_zh`）和 en 正常 15 对跑对比，汇总写入 `meta/reports/tooling_smoke_20260610.md`。
- 冒烟报告必须包含：与两份 after_repair 报告手算数字的对照段落。**预期不一致**（当时的 watch-list 是临时拼的，与 rules.yaml 口径不同），报告需解释差异来源，并声明今后以 rules.yaml 口径为准。

**验收：** 冒烟报告落盘；其中 zh 合计命中数与 after_repair 报告的 254→159 同方向（下降），en 同理（196→9 同方向），差异有解释。

---

## Phase 2 — AFTER 侧教训回流规则库

### T8 — 新建 `rules/zh/replacement_blacklist.md`

**Task status:** done

**目的：** 把 5-20 实测的 AFTER 侧失败固化为未来运行必加载的规则文件。

**改动：** 新建文件，含三部分：
1. **硬禁止替换产物**（出现在任何 AFTER 中即拒绝，来源：zh after_repair 报告的修复核对表）：`不只仅`、`先看`、`另先看`、`再往下`、`到最后`、`协作体系环境`、`合作协作体系`、`完整流程的响应机制`、`数据的提升作用`、`提升者`、`激励与惩戒完整流程`。
2. **正式文体降格替换（disfavored，需逐处论证才可用）**：`不只`（替代"不仅"在正式报告体中通常降格）；`协作体系`（替代"生态"时语义变平）；`完整流程`（作为"闭环"的默认替换，在标题/抽象语境生硬，如实测出现的"信任的完整流程"）。
3. **分语境推荐替换池**（按触发词组织，给 Layer 1 当起点而非机械映射）：
   - `闭环`：控制/工程语境保留或用"反馈回路"；管理语境用"全流程"或改写为具体机制描述；禁止默认无脑替换"完整流程"。
   - `生态`：白名单语境保留（见 context_whitelist.md）；确属空泛填充时改写整个短语而非换名词。
   - `赋能`：改为"提升…的能力"/"为…提供支持"等动宾结构，禁止单词替换。
   - 序数/列举标记（首先/其次/最后）：可变换或省略，但禁止降格为口语序列（`先看`/`再往下`/`到最后` 一族）。
   - 通用要求：**同一规则族在一份 plan 中的替换应当多样化**（详见 T11 的计划级检查）。
- 文件头注明：由 Layer 1 在 Step 4.3 naturalness preflight 强制加载；Layer 2 不读（同白名单的分层约定）。

**验收：** 文件存在且三部分齐全；T11 完成后 planning.md 明确引用它。

### T9 — 新建 `rules/en/replacement_guidance.md`

**Task status:** done

**目的：** 英文侧对称回流（5-20 英文实测的失败模式）。

**改动：** 新建文件，内容：
1. **Em-dash（P-04）替换多样化**：移除 em-dash 时在 逗号 / 冒号 / 分号 / 拆句 / 括号插入语 中按句意轮换；**禁止默认替换为 spaced hyphen `" - "`**（实测产生新的机械感，见 en after_repair 报告 "Remaining Risks"）。
2. **删除式修复的大小写守则**：删除句首短语后必须修正后续首词大小写（实测 doubao/topic_04、gemini/topic_03 出现 lowercase paragraph starts）。
3. **AFTER 残留外语检查**：EN 文档的 AFTER 不得引入 CJK 字符或中文生成说明尾注（实测 doubao/wenxin 出现过）。
- 同步在 `rules/en/sentence_patterns.md` P-04 的 **Fix direction** 末尾追加一句指向本文件。

**验收：** 文件存在；P-04 含交叉引用。

### T10 — 修订 `rules/zh/ai_cliches.md` C-04 与 `rules/zh/context_whitelist.md`

**Task status:** done

**目的：** 消除规则库主动推荐已被实测否定的替换；把白名单的扩充规则延伸到 AFTER 侧。

**改动：**
- `ai_cliches.md` C-04 修改方向中，"闭环"的建议由"完整流程/反馈回路"改为指向 `replacement_blacklist.md` 的分语境池（保留"反馈回路"作为控制语境示例即可）。整个文件 grep 一遍，其余"修改方向"凡是给出单一映射且该映射在 T8 黑名单内的，一并修订。
- `context_whitelist.md` 的 "Expansion Rule" 小节扩写：批量评测发现的 **BEFORE 侧**新失败进白名单表，**AFTER 侧**新失败进 `replacement_blacklist.md`，两侧都要在加新替换候选之前完成。

**验收：** `grep -n "完整流程" rules/zh/ai_cliches.md` 不再出现在无条件推荐位置；Expansion Rule 同时覆盖两个回流方向。

### T11 — `workflow/planning.md` + `templates/plan_output.md`：黑名单接入与计划级替换多样性检查

**Task status:** done

**目的：** 让 T8/T9 真正进入执行路径；堵住"逐条扫描看不见跨条目单调性"的缺口（12 个 em-dash 全换 `" - "` 这类问题，P0.5 逐条扫描永远不会报警）。

**改动：**
- planning.md Step 4.3 增加一条检查：AFTER 必须对照 `rules/zh/replacement_blacklist.md` / `rules/en/replacement_guidance.md`，命中硬禁止项必须改写，命中 disfavored 项需逐处一句话论证。fix block 模板的 `Naturalness preflight` 字段说明随之更新（不新增字段，避免计划膨胀）。
- 新增 **Step 4.4 — Replacement diversity check（计划级）**：完成全部 fix block 后，按规则族聚合 AFTER；同族修复数 ≥ 4 且超过 50% 使用同一替换词/同一结构时，必须多样化或在计划中论证。结果写入 plan.md §4（与反回归汇总同节）。
- `templates/plan_output.md` §4 增加小表：规则族 / 修复数 / 不同替换数 / 单一替换占比 / 处理说明。
- planning.md 末尾 Quality checklist 增加两个勾选项（黑名单检查、多样性检查）。

**验收：** planning.md 与模板互相一致；checklist 项与正文步骤一一对应。

### T12 — planning.md 高频子集改为派生自 `frequency` 字段

**Task status:** done

**目的：** 消除 Step 4.2 硬编码清单与规则库演化失同步的风险。

**改动：** Step 4.2 的"Universal high-frequency rules"改述为："取 `rules/<lang>/rules.yaml` 中 `frequency: high` 的规则（当前快照如下，以 YAML 为准）"，保留现行清单作为快照。

**验收：** 文字修改后快照与 T1 的 YAML `frequency: high` 集合一致。

---

## Phase 3 — 一致性与语料治理

### T13 — 评测报告头模板化 + 历史报告勘误

**Task status:** done

**目的：** 杜绝已实际发生的量表漂移（en after_repair 报告写了 "Scale: 0-36"，而量表与批量模板三处强调 /35）；统一逐维度报告结构（zh 报告有逐维表、en 报告没有）。

**改动：**
- 新建 `templates/eval_report_header.md`：固定报告头片段（Measurement type / External detector status: not run / Rubric scale: 35 points (seven dimensions, each 1-5) / 免责声明），要求所有评测报告原样复制。
- `meta/prompts/eval_prompt.md` 增补两条硬性要求：报告头必须使用该片段；批量报告每个样本必须有逐维度分数表（缺逐维表的报告无效）。
- 在 `meta/provider_articles/run_20260520_rewritten_en/en_rewrite_evaluation_report_after_repair.md` 末尾追加 "## Erratum (2026-06-10)" 小节：注明原文 "Scale: 0-36" 为笔误，量表为 /35；原文不动。

**验收：** 模板存在；eval_prompt.md 含两条硬性要求；Erratum 为追加且原文未改动（git diff 验证）。

### T14 — `gemini/topic_04` 转正为编码回归用例

**Task status:** done

**目的：** 结束该乱码样本两轮评测"被排除"的悬置状态，变废为宝。

**改动：**
- 新建 `meta/provider_articles/run_20260520/gemini/topic_04_ANOMALY_NOTE.md`：说明该样本是乱码异常源（非正常英文文章）、两轮评测均排除、现指定为 **discovery.md Step 1 编码预检与 T2/T5 工具乱码检测的标准回归用例**；不得修复或删除该文件。
- `tools/README.md` 的 scan_rules 示例中加入对该样本的负向用例（预期退出码 2）。
- 重新生成干净的 topic_04 以凑足 16 样本：**本期不做**，列入 Open Items。

**验收：** NOTE 文件存在；`python tools/scan_rules.py --text meta/provider_articles/run_20260520/gemini/topic_04.md --lang en` 退出码 2。

### T15 — `SKILL.md` / `workflow/discovery.md` / `workflow/planning.md` 增补

**Task status:** done

**目的：** 文档层收口：file map 反映新文件；边界澄清；brainmem 可选接入；heavy 计划粒度说明。

**改动：**
- SKILL.md file map 增加：`rules/{en,zh}/rules.yaml`、`rules/zh/replacement_blacklist.md`、`rules/en/replacement_guidance.md`、`tools/`（一行：deterministic offline scanners; not detector simulators）。
- SKILL.md Core principles 增加一条："**Replacement diversity.** 同族修复不得收敛到单一替换；plan 级多样性检查见 planning.md Step 4.4。"
- SKILL.md "When to use this skill" 增加一句边界澄清：本框架主目标是降 AI 检测信号；传统"降重"（降低与既有文献/旧版本的文本相似度）仅作为反回归约束处理，不是优化目标。
- `workflow/discovery.md` Step 3 前加一段可选项：若用户配有 BrainMem 等个人记忆系统，先用可移植占位符方式查询项目既有约束（目标检测器、院校规范、版本史），仅向用户追问缺失项；示例命令用 `${BRAIN_ROOT}` 占位符（遵循公共仓库不写机器路径的既有约定），标注 optional。
- `workflow/planning.md` heavy 7 轮表 Round 4（burstiness injection）加一句：该轮修复仍须以句子粒度的 exact BEFORE/AFTER 表达；需要多句联动重构的项归 Tier C 并移入 Round 5。

**验收：** file map 与磁盘文件一一对应（逐项核对）；四处增补全部落地。

### T16 — README 双语同步更新

**Task status:** done

**目的：** 对外说明面与新能力一致。

**改动：** `README.md`（仓库根）中英两节各增加：tools/ 离线扫描器一句话介绍（强调"确定性离线统计，非检测器模拟"）、AFTER 侧替换黑名单/多样性检查一句话。两节内容必须语义对齐。

**验收：** 中英两节均更新且对齐；不引入任何"可过检"承诺性表述（与既有基调一致）。

---

## Phase 4 — 收尾验证与记忆同步

### T17 — 全仓一致性扫描

**Task status:** done

**改动 / 验收（即检查清单）：**
- `grep -rn "0-36" ai-detection-workflow/` → 仅出现在 Erratum 引用原文处。
- SKILL.md file map 列出的每个文件磁盘上存在；磁盘上每个 rules/tools 文件都被 file map 或 tools/README 引用。
- planning.md / execution.md / SKILL.md 中所有交叉引用路径有效。
- 所有新工具 `--help` 可运行；`tools/testdata/` 自检用例全部按预期退出码工作。
- 全部新文件 UTF-8（无 BOM 优先；若工具链产生 BOM 须统一去除）。

### T18 — BrainMem 记忆同步（机器侧操作，非仓库内容）

**Task status:** done

**目的：** 记忆库中本项目页已过时（记录停在 v1.0.0 / f71f071，实际已 v1.1.0 / b3aa521），本次升级完成后一并刷新。

**改动：** 在用户机器环境执行（需 `E:\docu\brain\.venv\Scripts\mem.exe` 可用）：

```powershell
@'
source_agent: codex
source_context: ai-detection-workflow upgrade plan 20260610 executed

AI-Text-Anti-Detection-Framework upgraded per meta/proposals/upgrade_plan_20260610.md:
repo now at <new tag/commit>; added tools/ (scan_rules, structure_metrics, preflight_plan,
guardrails_diff, overlap_check; stdlib-only, offline-only), machine-readable rules.yaml for
en/zh, AFTER-side replacement blacklist (zh) and replacement guidance (en), plan-level
replacement-diversity check (planning.md Step 4.4), eval report header template enforcing
/35 rubric, gemini/topic_04 designated as encoding regression fixture. Prior memory of
v1.0.0/f71f071 is superseded.
'@ | & E:\docu\brain\.venv\Scripts\mem.exe capture --brain-root E:\docu\brain-root --stdin
```

- 只做 `mem capture`（本地落 laundry）；**不得**执行 ingest/review 审批（BrainMem SOP：review 队列非 agent 自治）。
- 若 Codex 运行环境无法访问该路径，标记本任务 blocked 并在收尾摘要中提醒用户手工执行。

### 提交与放行

1. 每个 Phase 完成后本地 commit 一次，建议 message：
   - `phase 1: offline tooling + machine-readable rule tables`
   - `phase 2: AFTER-side replacement blacklist and plan-level diversity check`
   - `phase 3: eval report consistency, encoding fixture, doc updates`
   - `phase 4: consistency sweep`
2. 全部完成后输出收尾摘要（含冒烟报告路径、T17 清单逐项结果、blocked 项）。
3. **push 与打 tag（建议 v1.2.0）等待用户审阅冒烟报告后再执行，不要自动 push。**

## Out of scope（本期明确不做）

- 任何外部检测器的调用、模拟或对接（保持纯离线边界）。
- 重写/重新生成评测语料（含 gemini/topic_04 的干净重生成 → Open Item）。
- Layer 2 契约、轮次模型、量表维度定义的任何改动。
- 规则库新增检测规则条目（本期只做机器可读化与 AFTER 侧回流，不扩规则面）。

## Open Items（留给下一期）

- 重新生成 gemini/topic_04 干净英文样本，凑足 16 样本批次。
- 用 T2/T3 工具对下一次真实文档运行做一次"工具口径 vs 人工口径"标定。
- 散文规则文件与 rules.yaml 的一致性 lint（可作为 tools/ 的后续脚本）。
