# Quality Checklist & Anti-Hallucination Rules

## Pre-Output Checklist

### Factual Accuracy
- [ ] Metadata (title, authors, venue, year, DOI) taken directly from provided text
- [ ] Numerical results copied verbatim, not rounded or paraphrased
- [ ] Author affiliations from paper's author block, not guessed

### Source Tagging
- [ ] Every contribution tagged `[原文声明]` or `[模型归纳]`
- [ ] `[原文声明]` items have location reference (section, figure, table, or quote)
- [ ] `[模型归纳]` items have stated reasoning basis

### Uncertainty Marking
- [ ] Missing fields marked `[未明确给出]`, not blank or guessed
- [ ] Ambiguous info marked `[不确定]` with explanation
- [ ] Skipped sections explicitly noted with reason

### Domain Assumption Check
- [ ] Paper type determined by rubric, not assumed
- [ ] Method template matches determined paper type
- [ ] No AI/ML terminology injected into non-AI papers

### Degraded Input Check
- [ ] Header line states PDF quality if degraded
- [ ] Sections from unreadable content explicitly skipped
- [ ] No content fabricated to fill gaps

## Common Hallucination Patterns

| Pattern | Wrong | Correct |
|---------|-------|---------|
| Venue guessing | "Published at NeurIPS" (not in text) | `[未明确给出]` |
| Contribution inflation | Adding contributions not in paper | Only list what paper claims |
| Result extrapolation | "Achieves SOTA on all benchmarks" | Quote exact benchmark + metric |
| Author expertise | "Expert in computer vision" | Only state what paper says |
| Future work fabrication | Inventing future directions | Only cite paper's own future work section |
| Method gap filling | Guessing architecture details | Mark as `[未明确给出]` |

## Degraded PDF Protocol

**Level: Degraded** (partial text extractable)
1. Header: `PDF 质量：降级处理 - [具体原因]`
2. Complete sections where text is available
3. Unavailable sections: `[该部分文本不可读，已跳过]`
4. Offer to re-analyze if user provides better source

**Level: Poor** (minimal text)
1. Header: `PDF 质量：严重降级 - 仅能提取部分内容`
2. Auto-switch to `quick` mode
3. Only output reliably extractable content
4. Recommend: OCR tool, copy-paste from PDF reader, or arXiv HTML version

## Evidence Binding Format

```
[原文声明] 提出了 X 方法
证据：Section 3.2，"We propose X, which..."

[模型归纳] 该方法在低资源场景下可能有优势
依据：实验仅在小数据集上测试，作者未明确声明此优势
```
