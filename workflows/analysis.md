# Analysis Workflow

Used by: `quick`, `standard`, `extended`, `presentation`, `presentation_with_figures` modes.

## Step 0: PDF → Markdown Preprocessing

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

## Step 1: Assess Input Quality

Classify PDF quality before analysis:
- **良好**: Full text extractable
- **降级处理**: Partial text, scanned sections, garbled encoding
- **严重降级**: Minimal text, image-only PDF

If degraded: state reason in header line, proceed with available content,
mark all gaps explicitly. Never fabricate content to fill gaps.

Optional: if user has Python, suggest running `scripts/extract_pdf_meta.py`
first for structured metadata.

## Step 2: Classify Paper Type

Read `references/paper-type-rubric.md` and classify. Do NOT assume AI/ML.
Output the type label and 2–3 evidence indicators before proceeding.

## Step 3: Execute Analysis

Follow `references/output-schema.md` for the selected mode. Apply all rules
from `references/quality-checklist.md` throughout every section.

## Step 4: Self-Check Before Output

Verify before finalizing:
- Every uncertain field marked `[不确定]` or `[未明确给出]`
- Every contribution tagged `[原文声明]` or `[模型归纳]`
- No section silently omitted — skipped sections state why
- Paper type label matches rubric evidence

## Degraded Input Fallback

| Situation | Action |
|-----------|--------|
| Only abstract available | `quick` mode, note limitation |
| Scanned PDF, no text | Ask user for text or OCR first |
| Missing references section | Skip prior work analysis, note absence |
| Figures unreadable | Skip figure analysis, note absence |
| Non-English paper | Translate key sections, note source language |
