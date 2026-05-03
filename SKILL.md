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
| `references/output-schema.md` | Section structure and field rules |
| `references/paper-type-rubric.md` | How to classify paper type |
| `references/quality-checklist.md` | Anti-hallucination checklist |
| `references/presentation-schema.md` | Slide plan JSON schema |
| `references/presentation-style-guide.md` | Content compression rules for slides |
| `references/html-handoff.md` | HTML slide generation spec (default format) |
| `references/pptx-handoff.md` | How to call the pptx skill for PPTX rendering |
| `scripts/extract_pdf_meta.py` | Optional: extract PDF metadata to JSON |
| `scripts/pdf_to_markdown.py` | Convert PDF to structured Markdown before analysis |
| `scripts/extract_pdf_figures.py` | Extract figures from original PDF (used in presentation mode) |
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

### Step 0: PDF → Markdown Preprocessing

Before any analysis, convert the PDF to structured Markdown using markitdown.
This drastically reduces token consumption compared to sending raw PDF binary
to the LLM, and produces cleaner structured text for downstream parsing.

```
python scripts/pdf_to_markdown.py <pdf_path> -o <output.md>
```

The script produces a `.md` file with:
- **YAML front-matter**: source filename, page count, conversion timestamp
- **Structured Markdown**: headings, tables, lists preserved from the PDF

**All subsequent steps (Step 1–4) operate on the generated `.md` file, not the
original PDF.** The only exception is figure extraction in
`presentation_with_figures` mode (Step B0), which reads the original PDF because
images cannot be represented in Markdown.

If the user has not run this step yet, run it automatically before proceeding.

### Step 1: Assess Input Quality

Classify PDF quality before analysis:
- **良好**: Full text extractable
- **降级处理**: Partial text, scanned sections, garbled encoding
- **严重降级**: Minimal text, image-only PDF

If degraded: state reason in header line, proceed with available content,
mark all gaps explicitly. Never fabricate content to fill gaps.

Optional: if user has Python, suggest running `scripts/extract_pdf_meta.py`
first for structured metadata.

### Step 2: Classify Paper Type

Read `references/paper-type-rubric.md` and classify. Do NOT assume AI/ML.
Output the type label and 2–3 evidence indicators before proceeding.

### Step 3: Execute Analysis

Follow `references/output-schema.md` for the selected mode. Apply all rules
from `references/quality-checklist.md` throughout every section.

### Step 4: Self-Check Before Output

Verify before finalizing:
- Every uncertain field marked `[不确定]` or `[未明确给出]`
- Every contribution tagged `[原文声明]` or `[模型归纳]`
- No section silently omitted — skipped sections state why
- Paper type label matches rubric evidence

## Anti-Hallucination Rules

Full rules in `references/quality-checklist.md`. Non-negotiable constraints:

1. **Source tagging**: `[原文声明]` = directly stated in paper (cite location);
   `[模型归纳]` = inferred by model (state reasoning basis)
2. **Uncertainty**: `[未明确给出]` when absent; `[不确定]` when ambiguous
3. **No domain assumption**: classify paper type first, always
4. **No fabrication**: venue, DOI, year, affiliations not in text → `[未明确给出]`
5. **Evidence binding**: each contribution must cite section/figure/table/quote
6. **Degraded PDF**: state which sections were unreadable; do not fill gaps

## Degraded Input Fallback

| Situation | Action |
|-----------|--------|
| Only abstract available | `quick` mode, note limitation |
| Scanned PDF, no text | Ask user for text or OCR first |
| Missing references section | Skip prior work analysis, note absence |
| Figures unreadable | Skip figure analysis, note absence |
| Non-English paper | Translate key sections, note source language |

## Extended Mode: Author Prior Work

Only in `extended` mode:
1. Extract all author names from paper
2. Identify self-citations in reference list (shared authors)
3. Infer research group focus from affiliations + paper title
4. List prior works from reference list only — no web search, no external knowledge
5. Tag all output: `[基于论文内引用，非外部检索]`
6. If insufficient info: explicitly state "信息不足，无法判断前作关系"

## Presentation Mode: PPT Generation

Only in `presentation` or `presentation_with_figures` mode.

### Step A0: Select VI System

Load the Visual Identity (VI) configuration that defines colors, fonts, sizes,
and chart styling for the generated PPT.

- **Default**: `vi_system/example/vi.json` (academic style — light blue `#3E87FA`, white
  background, Inter)
- **User override**: if the user says "用 XX 风格" / "use XX style", look for
  `vi_system/XX/vi.json`. If not found, fall back to default and note the fallback.

Load the chosen `vi.json` and pass its values to the handoff in Step C.

### Step A: Collect Overrides

Before building the slide plan, check if the user specified any of:
- `slide_format` (html / pptx) — default: `html`
- `audience` (lab / conference / general) — default: `lab`
- `duration_hint` (10min / 20min / 30min) — default: `20min`
- `talk_style` (technical / overview / discussion) — default: `technical`
- `emphasis` (which sections to expand)
- `skip` (which sections to omit)

**Format selection**: If the user did not specify `slide_format`, ask them:
"你希望生成哪种格式的幻灯片？HTML（默认，自包含网页文件，浏览器打开即可演示）或 PPTX（需 pptx skill）？"
If they don't respond or say "随便"/"default", use `html`.

HTML is the default because: (1) no external skill dependency, (2) single self-contained file,
(3) lower token consumption (agent generates code directly vs. invoking another LLM skill).

If not specified, use defaults silently for all other fields.

### Step B0: Extract PDF Figures (presentation_with_figures only)

Before building the slide plan, run:
```
python scripts/extract_pdf_figures.py <original_pdf_path>
```
This saves all figures to `figures/` and writes `figures/index.json` with `name`, `path`, and `page` for each image. Use this index when assigning `figure_ref` paths in the handoff.

> **Note**: This step reads the **original PDF** (not the Markdown output),
> because figures/images cannot be represented in Markdown text.
> All other analysis steps use the `.md` file generated in Step 0.

### Step B: Build Slide Plan

Follow `references/presentation-schema.md` for structure.
Follow `references/presentation-style-guide.md` for compression rules.

- Map each slide role to the corresponding output-schema section
- Apply user overrides (emphasis → expand, skip → omit)
- For `presentation_with_figures`: set `figure_needed: true` on method/result slides where a figure is the primary evidence; add `figure_ref` and `figure_hint`
- Slide count from duration_hint (10min→6-7, 20min→9-10, 30min→12-14)

### Step C: Generate Slides

If user said "只要大纲" / "just the outline", output the slide plan as text and skip generation.

#### Step C-html (default: `slide_format = html`)

Follow `references/html-handoff.md` for the exact generation spec.

- Generate a self-contained HTML file with all CSS/JS inline
- Map VI System parameters to CSS custom properties (`--primary`, `--bg`, etc.)
- Use CSS scroll-snap for slide-by-slide navigation, keyboard arrow keys + space + touch swipe
- Support all slide types: cover, bullets, split, table, results, closing
- Figures: reference via relative path (`figures/fig_XXX.png`) or generate inline SVG for charts
- Strip all `[原文声明]` / `[模型归纳]` tags before writing content
- Output filename: sanitized deck title + `.html`
- Do NOT ask the user before generating — just output the file

#### Step C-pptx (`slide_format = pptx`)

Follow `references/pptx-handoff.md` for the exact handoff format.

- Strip all `[原文声明]` / `[模型归纳]` tags before passing to pptx
- Include VI System parameters (colors, fonts, sizes) from the selected `vi.json`
- Do NOT include speaker notes in the handoff
- Call pptx skill automatically — do not ask the user first
