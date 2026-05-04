# Quality Checklist & Anti-Hallucination Rules

## Core Principle

**Prevent fabrication of facts, not thinking.**

The anti-hallucination rules exist to ensure you don't invent specific facts
(venue names, DOIs, numerical results, author affiliations) that aren't in
the paper. They do **NOT** prevent you from:

- Analyzing the method's design choices and trade-offs
- Comparing approaches using your domain knowledge
- Evaluating whether results support claims
- Assessing the paper's significance for the field
- Identifying potential weaknesses or limitations
- Making informed predictions about impact

This kind of analytical reasoning is your **primary value** — don't suppress it.

## Source Tagging System

Two tags, both legitimate:

| Tag | Meaning | Use for |
|-----|---------|---------|
| `[原文声明]` | Directly stated in the paper | Author claims, quoted results, stated limitations |
| `[模型归纳]` | Model's analytical inference | Method critique, comparative analysis, impact assessment, identified limitations |

`[模型归纳]` is not a "warning" label — it's a transparency marker. It tells
the reader "this is the model's analysis, not the author's words." Analytical
insights tagged `[模型归纳]` are **expected and valuable**.

## What NOT to Fabricate (Hard Rules)

These are non-negotiable. If the information isn't in the paper, mark it `[未明确给出]`:

1. **Venue/conference/journal name** — don't guess from context
2. **DOI, arXiv ID, page numbers** — must be verbatim from text
3. **Author affiliations** — only from the author block
4. **Exact numerical results** — copy verbatim, never round or paraphrase
5. **Publication year** — only if explicitly stated
6. **Author's unstated intentions** — don't claim "the authors intended X" unless stated

## What IS Encouraged (Analytical Reasoning)

Tag as `[模型归纳]` and provide reasoning basis. This is the analysis that makes
the output useful:

1. **Method comparison**: "与 Transformer 相比，该方法在长序列场景下可能更高效，
   因为其注意力复杂度为 O(n log n) 而非 O(n²)"
2. **Results critique**: "实验仅在英文数据集上验证，跨语言泛化能力未经考察"
3. **Impact assessment**: "该方法解决了 X 领域的一个关键瓶颈，可能推动 Y 方向的研究"
4. **Limitation identification**: "基于方法分析：该模型假设输入无噪声，但在实际部署中..."
5. **Future direction**: "根据实验结果的 gap，一个自然的后续方向是..."
6. **Cross-paper comparison**: "与同期工作 [paper name] 相比，该方法的优势在于..."

The only requirement: state your reasoning basis. "Based on the method design..."
or "From the experimental setup, I infer..."

## Uncertainty Marking

- Missing fields → `[未明确给出]` (not blank or guessed)
- Ambiguous info → `[不确定]` + explanation of the ambiguity
- Skipped sections → explicitly noted with reason

## Pre-Output Checklist

### Factual Accuracy
- [ ] Metadata (title, authors, venue, year, DOI) taken directly from provided text
- [ ] Numerical results copied verbatim, not rounded or paraphrased
- [ ] Author affiliations from paper's author block, not guessed

### Source Tagging
- [ ] Every contribution tagged `[原文声明]` or `[模型归纳]`
- [ ] `[原文声明]` items have location reference (section, figure, table, or quote)
- [ ] `[模型归纳]` items have stated reasoning basis

### Analytical Depth
- [ ] Analysis goes beyond description — includes critique, comparison, or insight
- [ ] Method section discusses design choices and trade-offs, not just "what" but "why"
- [ ] Results section evaluates evidence strength, not just reports numbers
- [ ] Limitations include both author-acknowledged and model-identified issues

### Domain Assumption Check
- [ ] Paper type determined by rubric, not assumed
- [ ] Method template matches determined paper type
- [ ] No domain-specific terminology injected inappropriately

### Degraded Input Check
- [ ] Header line states PDF quality if degraded
- [ ] Sections from unreadable content explicitly skipped
- [ ] No content fabricated to fill gaps

## Common Hallucination Patterns

| Pattern | Wrong | Right |
|---------|-------|-------|
| Venue guessing | "Published at NeurIPS" (not in text) | `[未明确给出]` |
| Result fabrication | Inventing benchmark numbers | Quote exact numbers from paper |
| Author intent | "The authors aimed to..." (not stated) | Describe what they did, not why |
| **Overcaution** | Only restating paper text verbatim | **Analyze, critique, compare — tag `[模型归纳]`** |

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
依据：方法采用了参数共享机制（Section 3.4），在小数据条件下可以减少需要学习的参数量，
      这与迁移学习的理论直觉一致
```
