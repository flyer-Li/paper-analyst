# Analysis Workflow

Used by: all modes. This is the core intellectual engine of paper-analyst.

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

**All subsequent steps operate on the generated `.md` file, not the
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

## Step 3: Deep Analysis

This is the most important step. Follow `references/output-schema.md` for
section structure, but go **far beyond filling in a template**. Your goal is
to provide the kind of analysis a knowledgeable peer reviewer or labmate would
give after reading the paper carefully.

### 3a. Structural Understanding

Read the paper systematically. For each section of the paper, identify:
- What claim is being made?
- What evidence supports it?
- What is the logical flow from problem → method → result → conclusion?

### 3b. Method Critique

Don't just describe the method — analyze it:
- What are the key design choices, and why might the authors have made them?
- What trade-offs does this approach involve (accuracy vs. efficiency, generality vs. specialization)?
- Are there alternative approaches the authors didn't consider? Why might those alternatives be relevant?
- What assumptions does the method rely on, and how reasonable are they?

### 3c. Results Interpretation

Go beyond listing numbers:
- Which results are most convincing, and which are weakest?
- Are the benchmarks/datasets sufficient, or are there gaps in evaluation?
- Do the results actually support the claims made, or is there overclaiming?
- How do the numbers compare to what you'd expect from the field? (Use your knowledge — this is analytical reasoning, not fabrication.)

### 3d. Impact Assessment

Think about the broader implications:
- What problem does this solve, and how important is that problem?
- How does this relate to the current state of the field?
- What downstream research or applications could this enable?
- What are the practical limitations for real-world deployment?

### 3e. Critical Gaps

Identify what the paper doesn't address:
- Missing ablations, comparisons, or evaluations
- Unstated assumptions or scope limitations
- Potential failure modes not discussed

Apply all rules from `references/quality-checklist.md` throughout — but
remember that **analytical reasoning is encouraged**. The checklist prevents
fabrication of facts, not thinking.

## Step 4: Self-Check Before Output

Verify before finalizing:
- Every uncertain field marked `[不确定]` or `[未明确给出]`
- Every contribution tagged `[原文声明]` or `[模型归纳]`
- No section silently omitted — skipped sections state why
- Paper type label matches rubric evidence
- Analysis includes genuine insights, not just regurgitation

## Degraded Input Fallback

| Situation | Action |
|-----------|--------|
| Only abstract available | `quick` mode, note limitation |
| Scanned PDF, no text | Ask user for text or OCR first |
| Missing references section | Skip prior work analysis, note absence |
| Figures unreadable | Skip figure analysis, note absence |
| Non-English paper | Translate key sections, note source language |
