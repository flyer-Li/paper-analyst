---
name: paper-analyst
description: "Analyze academic papers and research PDFs. Use this skill when the user uploads or pastes a research paper and wants to understand it. Triggers: 'analyze this paper', 'read this PDF', 'summarize this research', 'paper summary', 'research paper breakdown', 'explain this study', 'paper critique', 'academic paper analysis', '论文分析', '帮我看这篇论文', '解读这篇文章', '这篇 paper 讲什么', '帮我分析这个 PDF', '论文解读', '文献分析', '读一下这篇论文', '帮我总结这篇文章', '这篇论文的创新点', '论文方法分析', '论文结果', '帮我准备组会汇报', '生成 PPT 大纲'. Do NOT use for non-academic PDFs, spreadsheets, or general document tasks."
---

# Paper Analyst

Analyze academic papers from PDF or pasted text. Output in Chinese by default.

This SKILL.md is the **complete workflow** — read it end-to-end before starting.
The `references/` files are detail specs (schemas, rubrics, style guides, handoff
formats) consulted at the indicated step, **not** workflow shortcuts. Never skip
the workflow described here in favor of a reference summary.

## Quick Reference

| File | When to consult |
|------|-----------------|
| `references/paper-type-rubric.md` | Step 2 — classifying paper type |
| `references/output-schema.md` | Step 3 — section structure & field rules |
| `references/quality-checklist.md` | Step 4 — full self-check verification |
| `references/presentation-schema.md` | Presentation Step B — slide plan JSON |
| `references/presentation-style-guide.md` | Presentation Step B — compression rules |
| `references/html-handoff.md` | Presentation Step C — HTML generation spec |
| `references/pptx-handoff.md` | Presentation Step C — pptx skill format |
| `vi_system/example/vi.json` | Default visual identity (colors / fonts) |
| `scripts/pdf_to_markdown.py` | Step 0 — PDF → Markdown preprocessing |
| `scripts/extract_pdf_meta.py` | Optional — structured PDF metadata |
| `scripts/extract_pdf_figures.py` | Presentation Step B0 (figures mode) |

## Mode Selection

Default mode: `standard`. Detect from the user's request:

| Mode | Trigger | Output |
|------|---------|--------|
| `quick` | "quick", "简单说", "一句话", "简要" | Header + info + abstract + 3 contributions |
| `standard` | (default) | Full analysis: Sections 1–6 |
| `extended` | "前作", "课题组", "prior work" | standard + author/group prior work (Section 7) |
| `presentation` | "PPT", "组会", "汇报大纲", "slides", "图表", "figures", "带图" | standard + slide plan + HTML/PPTX, with paper figures embedded by default |

If ambiguous, use `standard` and offer to switch.

---

## Workflow (every mode)

### Step 0: PDF → Markdown Preprocessing

If input is a PDF, convert to structured Markdown first:

```
python scripts/pdf_to_markdown.py <pdf_path> -o <output.md>
```

Reduces token cost vs. sending the PDF binary, and produces cleaner structured
text (headings, tables, lists preserved) for downstream parsing.

**All later steps operate on the generated `.md` file**, not the original PDF.
The only exception is figure extraction (presentation_with_figures Step B0),
which reads the original PDF because images cannot be represented in Markdown.

If the user has not run this step, run it automatically before proceeding.

### Step 1: Assess Input Quality

Classify the source:
- **良好**: full text extractable
- **降级处理**: partial text, scanned sections, garbled encoding
- **严重降级**: minimal text, image-only PDF

If degraded: state the reason in the header line, proceed with what's
available, mark every gap explicitly. Never fabricate to fill gaps.

### Step 2: Classify Paper Type

Read `references/paper-type-rubric.md` and classify. Do **not** default to
AI/ML. Output the type label and 2–3 evidence indicators before any analysis.

### Step 3: Deep Analysis

Follow `references/output-schema.md` for section structure — but going beyond
the template is the point. The schema is the skeleton; the analysis is the
muscle. Your goal is the kind of read a careful peer reviewer or labmate would
produce, not a fill-in-the-blank summary.

For Sections 4–6 specifically, do all of the following:

**3a. Structural understanding** — for each section of the paper, ask: what
claim is being made? what evidence supports it? what is the logical flow from
problem → method → result → conclusion?

**3b. Method critique** — what are the key design choices, and why might the
authors have made them? what trade-offs (accuracy vs. efficiency, generality
vs. specialization)? what alternatives did they not consider, and why might
those alternatives matter? what assumptions does the method rely on?

**3c. Results interpretation** — go beyond listing numbers: which results are
most/least convincing? are the benchmarks/datasets sufficient, or are there
gaps in evaluation? do the results actually support the claims, or is there
overclaiming? how do the numbers compare to what you'd expect from the field?
(this is analytical reasoning, **not** fabrication — see Principle 2 below.)

**3d. Impact assessment** — how important is the problem this solves? how does
the work relate to the current state of the field? what downstream research or
applications could it enable? what are the practical limits for real deployment?

**3e. Critical gaps** — what does the paper *not* address? missing ablations,
unstated assumptions or scope limits, potential failure modes not discussed.

Apply the anti-hallucination rules (next section) throughout. Those rules
prohibit fabricating **facts**, not analytical reasoning.

### Step 4: Self-Check Before Output

Verify line-by-line before finalizing:
- [ ] Header line includes PDF quality + paper type + mode
- [ ] Every uncertain field marked `[不确定]` or `[未明确给出]` (not blank, not guessed)
- [ ] Every contribution tagged `[原文声明]` or `[模型归纳]`
- [ ] `[原文声明]` items cite a section / figure / table / quote
- [ ] `[模型归纳]` items state their reasoning basis
- [ ] No section silently omitted — skipped sections explain why
- [ ] Paper type label matches the rubric evidence given in Step 2
- [ ] Output contains genuine analytical insight, not just templated bullets

For the full pre-output checklist (factual accuracy, hallucination patterns,
degraded-PDF protocol, evidence binding format), see
`references/quality-checklist.md`.

---

## Anti-Hallucination Rules

Two principles. Both must hold simultaneously.

### Principle 1: Don't fabricate facts

Venue, DOI, year, affiliations, exact numerical results — if not in the paper,
mark `[未明确给出]`. Copy numbers verbatim; never round or paraphrase metrics.
Never guess architecture details, dataset sizes, or hyperparameters that the
paper doesn't state.

| Wrong | Correct |
|-------|---------|
| "Published at NeurIPS" (not in text) | `[未明确给出]` |
| "Achieves SOTA on all benchmarks" | quote exact benchmark + metric |
| Inventing a future-work direction | only cite paper's own future-work section |
| Guessing hidden architecture details | mark as `[未明确给出]` |
| Inflating contributions beyond paper claims | only list what the paper claims |

### Principle 2: DO analyze deeply

Anti-hallucination prevents fabrication of **facts**, not analytical reasoning.
You are *expected* to:
- Critique the method's design choices and trade-offs
- Compare with other approaches using your domain knowledge
- Evaluate whether results actually support the claims
- Assess significance and identify limitations beyond what the authors state
- Reason about downstream impact

Tag factual claims `[原文声明]` and analytical insights `[模型归纳]` — both are
legitimate output. **`[模型归纳]` is a transparency marker, not a warning.**
A paper analysis with no `[模型归纳]` items is a failed analysis: it means
you skipped the thinking.

### Tagging format

```
[原文声明] 提出了 X 方法
证据：Section 3.2，"We propose X, which..."

[模型归纳] 该方法在低资源场景下可能有优势
依据：实验仅在小数据集上测试，作者未明确声明此优势
```

Other non-negotiable rules:
1. **No domain assumption**: classify paper type first, always (Step 2)
2. **Evidence binding**: each contribution must cite section / figure / table / quote
3. **Degraded PDF**: state which sections were unreadable; do not fill gaps

---

## Degraded Input Fallback

| Situation | Action |
|-----------|--------|
| Only abstract available | switch to `quick` mode, note limitation |
| Scanned PDF, no text | ask user for OCR or text version |
| Missing references section | skip prior-work analysis, note absence |
| Figures unreadable | skip figure analysis, note absence |
| Non-English paper | translate key sections, note source language |

---

## Extended Mode: Author Prior Work

Run after Steps 0–4. Adds Section 7 (extended) to the output:

1. Extract all author names from the paper
2. Identify self-citations in the reference list (shared authors)
3. Infer research-group focus from affiliations + paper title
4. List prior works **from the paper's reference list only** — no web search,
   no external knowledge
5. Tag all extended output: `[基于论文内引用，非外部检索]`
6. If insufficient info: state explicitly "信息不足，无法判断前作关系"

---

## Presentation Mode: Slide Generation

Run after Steps 0–4. Generates a slide deck (HTML by default, PPTX optional).

### Step A0: Select VI System

Load the visual identity (colors, fonts, sizes) for the deck:
- **Default**: `vi_system/example/vi.json` (academic style — light blue
  `#3E87FA`, white background, Inter)
- **User override**: if the user says "用 XX 风格" / "use XX style", look for
  `vi_system/XX/vi.json`. If not found, fall back to default and note the fallback.

Pass the loaded `vi.json` values to Step C.

### Step A: Collect Overrides

Check whether the user specified any of:
- `slide_format` — `html` (default) or `pptx`
- `audience` — `lab` (default) / `conference` / `general`
- `duration_hint` — `10min` / `20min` (default) / `30min`
- `talk_style` — `technical` (default) / `overview` / `discussion`
- `emphasis` — sections to expand
- `skip` — sections to omit
- `figures` — `auto` (default, attempt extraction in Step B0) or `none` (triggered by "只要文字" / "no figures" / "纯文字" / "text only")

Use defaults silently for everything not specified, **except** `slide_format`:
if not given, ask once:

> "你希望生成哪种格式的幻灯片？HTML（默认，自包含网页文件，浏览器打开即可演示）或 PPTX（需 pptx skill）？"

If they don't respond or say "随便" / "default", use `html`. HTML is the default
because: (1) no external skill dependency, (2) single self-contained file,
(3) lower token cost (the agent generates code directly vs. invoking another LLM skill).

### Step B0: Extract Figures (default)

Before building the slide plan, attempt to extract figures from the original PDF:

```
python scripts/extract_pdf_figures.py <original_pdf_path>
```

Saves figures to `figures/` and writes `figures/index.json` with `name`, `path`,
and `page` for each image. Use this index when assigning `figure_ref` paths in
Step B / Step C. Reads the **original PDF** (not the Markdown), because figures
aren't represented in Markdown text.

**Skip extraction if any of the following:**
- `figures = none` (user said "只要文字" / "no figures" / "纯文字" / "text only")
- The original PDF is not available (e.g. user pasted text only)
- Extraction script fails (e.g. PDF is image-only with no embedded figures) —
  log the failure briefly to the user, fall back to text-only deck

**If figures already exist in another folder** (e.g. `paper/<name>_files/` from
an arxiv HTML download, or a user-provided directory), use those directly
without re-running the script. Copy/symlink the relevant ones into the deck's
`figures/` folder so the HTML references resolve cleanly.

### Step B: Build Slide Plan

Follow `references/presentation-schema.md` for the JSON structure.
Follow `references/presentation-style-guide.md` for compression rules.

- Map each slide role to its corresponding output-schema section
- Apply user overrides (`emphasis` → expand, `skip` → omit)
- When figures are available (Step B0 succeeded), set `figure_needed: true` on
  method/result slides where a figure is the primary evidence; add `figure_ref`
  and `figure_hint`. The architecture diagram (typically Figure 1) and result
  charts/tables are the highest-value embeds for academic decks.
- Slide count from `duration_hint`: 10min → 6–7, 20min → 9–10, 30min → 12–14

### Step C: Generate Slides

If the user said "只要大纲" / "just the outline", output the slide plan as text and stop.

#### Step C-html (default)

Follow `references/html-handoff.md` for the full generation spec.

- Generate one self-contained HTML file (all CSS/JS inline, no external CDN)
- Map VI System parameters to CSS custom properties (`--primary`, `--bg`, `--title-font`, ...)
- Use CSS scroll-snap for slide-by-slide navigation; keyboard arrows + space + touch swipe
- Strip all `[原文声明]` / `[模型归纳]` tags before writing slide content
- Output filename: sanitized deck title + `.html`
- Do NOT ask the user before generating — just write the file

#### Step C-pptx

Follow `references/pptx-handoff.md` for the handoff format.

- Strip all `[原文声明]` / `[模型归纳]` tags before passing to pptx
- Include VI System parameters (colors, fonts, sizes) from the selected `vi.json`
- Do NOT include speaker notes in the handoff
- Call pptx skill automatically — do not ask the user first
