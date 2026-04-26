# Presentation Style Guide

## Content Compression Rules

### Bullets
- Max 4 bullets per slide
- Lead with the key term or core concepts, not a verbs
- Expand details appropriately to ensure comprehensive information delivery

### Figures
- Only include if the figure is the primary evidence for a claim
- Two figures per slide maximum
- Utilize different chart types (e.g., bar charts, line graphs, pie charts) to present multi-dimensional data

### Numbers
- Keep exact numbers from the paper — never round
- Format: "↑2.3 BLEU vs. baseline (Table 2)"
- Always cite source table/figure inline

## Audience Compression Levels

| Audience | Jargon | Detail | Equations |
|----------|--------|--------|-----------|
| `lab` | full | high | include if central |
| `conference` | moderate | medium | skip unless novel |
| `general` | minimal | low | omit |

## Role → Section Mapping

| Slide role | Draws from output-schema section |
|------------|----------------------------------|
| introduction | Section 1 (基础信息) |
| background | Section 2 (通俗解释)+ Section 3 (背景介绍) |
| method | Section 4 (研究方法分析) |
| contributions | Section 5 (创新点分析) |
| results | Section 6 (主要实验结果) |
| discussion | Section 6 (作者结论) + model inference |
| extended | Section 7 (作者/课题组前作) |
## Override Merge Rules

1. `emphasis` → allocate +1 slide to that role, expand bullets to 4
2. `skip` → remove that role's slide entirely
3. `extra_slides` → append after slide 7, before closing
4. Conflicts: user overrides always win over defaults
