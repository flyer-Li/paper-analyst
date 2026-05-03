---
name: paper-analyst
description: "Analyze academic papers and research PDFs. Use this skill when the user uploads or pastes a research paper and wants to understand it. Triggers: 'analyze this paper', 'read this PDF', 'summarize this research', 'paper summary', 'research paper breakdown', 'explain this study', 'paper critique', 'academic paper analysis', '论文分析', '帮我看这篇论文', '解读这篇文章', '这篇 paper 讲什么', '帮我分析这个 PDF', '论文解读', '文献分析', '读一下这篇论文', '帮我总结这篇文章', '这篇论文的创新点', '论文方法分析', '论文结果', '帮我准备组会汇报', '生成 PPT 大纲'. Do NOT use for non-academic PDFs, spreadsheets, or general document tasks."
---

# Paper Analyst

Analyze academic papers from PDF or pasted text. Output in Chinese by default.
All outputs follow `references/output-schema.md`. Paper type detection uses
`references/paper-type-rubric.md`. Anti-hallucination rules in
`references/quality-checklist.md`.

## Quick Reference

| File | Purpose |
|------|---------|
| `workflows/analysis.md` | Core analysis steps (Step 0–4) |
| `workflows/extended.md` | Extended mode: author prior work |
| `workflows/presentation.md` | Presentation mode: slide plan + generation |
| `references/output-schema.md` | Output format rules |
| `references/paper-type-rubric.md` | How to classify paper type |
| `references/quality-checklist.md` | Anti-hallucination checklist |
| `references/presentation-schema.md` | Slide plan JSON schema |
| `references/presentation-style-guide.md` | Content compression rules for slides |
| `references/html-handoff.md` | HTML slide generation spec (default format) |
| `references/pptx-handoff.md` | How to call the pptx skill for PPTX rendering |
| `vi_system/vi-schema.json` | VI System JSON Schema |
| `vi_system/example/vi.json` | Default VI scheme (academic style) |

## Mode Selection

Default mode: `standard`. Detect from user's request:

| Mode | Trigger | Output |
|------|---------|--------|
| `quick` | "quick", "简单说", "一句话", "简要" | Header + info + abstract + 3 contributions |
| `standard` | (default) | Full analysis: sections 1–5 |
| `extended` | "前作", "课题组", "prior work" | standard + author/group prior work |
| `presentation` | "PPT", "组会", "汇报大纲", "slides" | standard + slide outline + HTML/PPTX slides |
| `presentation_with_figures` | "图表", "figures", "带图", "关键图" | presentation + figure annotations |

If ambiguous, use `standard` and offer to switch.

## Workflow

### Analysis (all modes)

Read `workflows/analysis.md` for the full steps. Summary:

1. **Step 0**: Convert PDF → Markdown (`scripts/pdf_to_markdown.py`)
2. **Step 1**: Assess input quality (良好 / 降级 / 严重降级)
3. **Step 2**: Classify paper type using `references/paper-type-rubric.md`
4. **Step 3**: Execute analysis following `references/output-schema.md`
5. **Step 4**: Self-check — tag sources, mark uncertainties

### Extended mode (only)

After analysis, read `workflows/extended.md` and add author prior work analysis.

### Presentation mode (only)

After analysis, read `workflows/presentation.md` for the full slide generation flow:
1. Select VI System → 2. Collect overrides (format, audience, duration) → 3. Extract figures (if `_with_figures`) → 4. Build slide plan → 5. Generate HTML or PPTX

## Anti-Hallucination Rules

Full rules in `references/quality-checklist.md`. Non-negotiable constraints:

1. **Source tagging**: `[原文声明]` = directly stated in paper (cite location);
   `[模型归纳]` = inferred by model (state reasoning basis)
2. **Uncertainty**: `[未明确给出]` when absent; `[不确定]` when ambiguous
3. **No domain assumption**: classify paper type first, always
4. **No fabrication**: venue, DOI, year, affiliations not in text → `[未明确给出]`
5. **Evidence binding**: each contribution must cite section/figure/table/quote
6. **Degraded PDF**: state which sections were unreadable; do not fill gaps
