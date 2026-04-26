# paper-analyst

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code Skill](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://docs.anthropic.com/en/docs/claude-code)

一个用于学术论文深度分析的 Claude Code Skill，支持从 PDF 解析到组会 PPT 自动生成的完整工作流。

> **English summary**: A Claude Code skill for academic paper analysis. Supports 5 analysis modes (quick/standard/extended/presentation/presentation_with_figures), anti-hallucination source tagging, paper-type-aware method templates, and automated PPT generation via the `pptx` skill.

---

## 功能亮点

- **5 种分析模式**：从一句话速览到带图表的组会 PPT，按需选择
- **反幻觉机制**：每个观点强制标注 `[原文声明]` 或 `[模型归纳]`，并绑定原文位置证据
- **论文类型感知**：先分类（AI/深度学习、传统算法、系统工程、实验实证、综述、跨学科），再套对应方法分析模板
- **PDF 质量分层**：良好 / 降级 / 严重降级三档处理，优雅降级而非直接报错
- **PPT 自动化管道**：演讲模式下自动提取 PDF 图表、构建幻灯片计划、调用 `pptx` skill 生成文件
- **前作关系追踪**：`extended` 模式从参考文献中识别自引，推断课题组研究脉络（仅基于论文内部，不做外部检索）
- **中英双语触发**：中英文触发词均支持

---

## 快速开始

### 前置条件

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI 已安装
- Python 3.8+（用于 PDF 图表提取脚本）
- Python 依赖：`pip install pymupdf pypdf`
- 如需生成 PPT，还需安装 anthropics官方的[`pptx` skill]及其依赖

### 安装

```bash
npx skills add flyer-Li/paper-analyst
```

> 也可以手动克隆：`git clone https://github.com/flyer-Li/paper-analyst ~/.claude/skills/paper-analyst`

### 使用

在 Claude Code 中，直接用自然语言触发：

```
/paper-analyst 使用这个skill来分析文献，当前目录下的 paper.pdf
/paper-analyst quick summary of this paper
/paper-analyst 分析这篇文献与前作的关系
/paper-analyst 将以上分析内容做成一个可以直接用来汇报的组会ppt，要求美观带图片
```

---

## 分析模式

| 模式 | 触发词 | 输出内容 |
|------|--------|--------|
| `quick` | "quick"、"简单说"、"一句话"、"简要" | 基础信息 + 摘要译文 + 3 个核心贡献 |
| `standard` | （默认，最推荐） | 完整 6 节分析（基础信息 → 结论与局限） |
| `extended` | "前作"、"课题组"、"prior work" | standard + 作者自引识别 + 研究脉络分析 |
| `presentation` | "PPT"、"组会"、"汇报大纲"、"slides" | standard + 幻灯片大纲 + 自动生成 PPTX |
| `presentation_with_figures` | "图表"、"带图"、"关键图"、"figures" | presentation + PDF 图表提取 + 图表标注 |

---

## 输出结构

`standard` 及以上模式输出以下 6 个章节：

| 章节 | 内容 |
|------|------|
| **基础信息** | 标题、作者、单位、Venue、年份、DOI、关键词 |
| **摘要翻译与通俗解释** | 直译 + 面向非专业读者的 3-5 句解释 |
| **背景介绍** | 研究背景与开展此研究的意义 |
| **研究方法分析** | 按论文类型套用对应模板（见下方） |
| **创新点分析** | 最多 5 条，每条绑定原文位置证据 |
| **研究结果与结论** | 具体数字 + 基线对比 + 局限性（原文声明 & 模型识别） |

### 方法分析模板（按论文类型）

- **AI/深度学习**：任务定义与输入输出 / 模型架构 / 训练策略 / 推理流程
- **传统算法/理论**：问题形式化 / 算法步骤 / 复杂度分析 / 关键假设
- **系统/工程**：系统架构 / 关键组件 / 性能指标 / 与现有系统对比
- **实验/实证**：实验设计 / 数据收集 / 统计分析方法
- **综述/Survey**：综述范围与检索策略 / 分类框架 / 对比维度

---

## 反幻觉机制

这是本 skill 的核心设计，所有输出遵循以下规则：

**双标签系统**

```
[原文声明] 提出了 X 方法
证据：Section 3.2，"We propose X, which..."

[模型归纳] 该方法在低资源场景下可能有优势
依据：实验仅在小数据集上测试，作者未明确声明此优势
```

**不确定性标记**

- 论文中未提及的字段 → `[未明确给出]`，不猜测
- 信息有歧义 → `[不确定]` + 说明歧义原因

**PDF 质量分层处理**

| 质量等级 | 处理方式 |
|---------|---------|
| 良好 | 全量分析 |
| 降级处理 | 标注不可读章节，已有内容正常分析 |
| 严重降级 | 自动切换 quick 模式，建议用户提供更好来源 |

详细规则见 [`references/quality-checklist.md`](references/quality-checklist.md)。

---

## 文件结构

```
paper-analyst/
├── SKILL.md                        # Skill 主配置（Claude Code 入口）
├── references/
│   ├── output-schema.md            # 输出格式规范（7 节结构）
│   ├── paper-type-rubric.md        # 论文类型分类规则
│   ├── quality-checklist.md        # 反幻觉检查清单
│   ├── presentation-schema.md      # PPT 幻灯片结构 JSON 规范
│   ├── presentation-style-guide.md # 演讲内容压缩规则
│   └── pptx-handoff.md             # pptx skill 调用接口规范
└── scripts/
    ├── extract_pdf_meta.py         # PDF 元数据提取
    └── extract_pdf_figures.py      # PDF 图表提取
```

---

## 依赖项

| 依赖 | 用途 | 安装 |
|------|------|------|
| `pymupdf` | PDF 图表提取 | `pip install pymupdf` |
| `pypdf` | PDF 元数据读取 | `pip install pypdf` |
| `pptx` skill | PPT 文件生成 | 单独安装，见其 README |

---

## License

MIT License — Copyright (c) 2026 Yifei Li

本项目以 MIT 许可证开源。你可以自由使用、修改和分发，但需保留原始版权声明。

完整许可证文本见 [LICENSE](LICENSE) 文件。

---

## Contributing

欢迎提交 Issue 和 Pull Request。

如果你在使用中发现幻觉案例、分类错误或输出格式问题，欢迎在 Issue 中附上复现步骤（论文类型 + 触发词 + 错误输出片段）。
