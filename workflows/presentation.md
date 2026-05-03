# Presentation Workflow

Used by: `presentation` and `presentation_with_figures` modes.
Executes after the core analysis workflow.

## Step A0: Select VI System

Load the Visual Identity (VI) configuration that defines colors, fonts, sizes,
and chart styling for the generated slides.

- **Default**: `vi_system/example/vi.json` (academic style — light blue `#3E87FA`, white
  background, Inter)
- **User override**: if the user says "用 XX 风格" / "use XX style", look for
  `vi_system/XX/vi.json`. If not found, fall back to default and note the fallback.

Load the chosen `vi.json` and pass its values to the handoff in Step C.

## Step A: Collect Overrides

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

## Step B0: Extract PDF Figures (presentation_with_figures only)

Before building the slide plan, run:
```
python scripts/extract_pdf_figures.py <original_pdf_path>
```
This saves all figures to `figures/` and writes `figures/index.json` with `name`, `path`, and `page` for each image. Use this index when assigning `figure_ref` paths in the handoff.

> **Note**: This step reads the **original PDF** (not the Markdown output),
> because figures/images cannot be represented in Markdown text.
> All other analysis steps use the `.md` file generated in Step 0.

## Step B: Build Slide Plan

Follow `references/presentation-schema.md` for structure.
Follow `references/presentation-style-guide.md` for compression rules.

- Map each slide role to the corresponding output-schema section
- Apply user overrides (emphasis → expand, skip → omit)
- For `presentation_with_figures`: set `figure_needed: true` on method/result slides where a figure is the primary evidence; add `figure_ref` and `figure_hint`
- Slide count from duration_hint (10min→6-7, 20min→9-10, 30min→12-14)

## Step C: Generate Slides

If user said "只要大纲" / "just the outline", output the slide plan as text and skip generation.

### Step C-html (default: `slide_format = html`)

Follow `references/html-handoff.md` for the exact generation spec.

- Generate a self-contained HTML file with all CSS/JS inline
- Map VI System parameters to CSS custom properties (`--primary`, `--bg`, etc.)
- Use CSS scroll-snap for slide-by-slide navigation, keyboard arrow keys + space + touch swipe
- Support all slide types: cover, bullets, split, table, results, closing
- Figures: reference via relative path (`figures/fig_XXX.png`) or generate inline SVG for charts
- Strip all `[原文声明]` / `[模型归纳]` tags before writing content
- Output filename: sanitized deck title + `.html`
- Do NOT ask the user before generating — just output the file

### Step C-pptx (`slide_format = pptx`)

Follow `references/pptx-handoff.md` for the exact handoff format.

- Strip all `[原文声明]` / `[模型归纳]` tags before passing to pptx
- Include VI System parameters (colors, fonts, sizes) from the selected `vi.json`
- Do NOT include speaker notes in the handoff
- Call pptx skill automatically — do not ask the user first
