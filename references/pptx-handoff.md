# pptx Skill Handoff Format

## When to Call pptx Skill

After generating the slide plan (presentation-schema.md), automatically invoke the `pptx` skill with the structured prompt below. Do NOT ask the user — call it directly.

## VI System Parameters

Before calling pptx, load the selected `vi_system/<name>/vi.json` and extract
the following parameters for the handoff prompt.

| Parameter | Source | Example |
|-----------|--------|---------|
| `vi_primary_color` | `colors.primary` | `#3E87FA` |
| `vi_secondary_color` | `colors.secondary` | `#1E5FD9` |
| `vi_accent_color` | `colors.accent` | `#DC2626` |
| `vi_background_color` | `colors.background` | `#FFFFFF` |
| `vi_text_color` | `colors.text` | `#0F172A` |
| `vi_title_font` | `fonts.title` | `Inter` |
| `vi_body_font` | `fonts.body` | `Inter` |
| `vi_code_font` | `fonts.code` | `Menlo` |
| `vi_title_size` | `sizes.title` | `44` |
| `vi_heading_size` | `sizes.heading` | `28` |
| `vi_body_size` | `sizes.body` | `16` |
| `vi_chart_colors` | `chart.colors` | `#3E87FA, #1E5FD9, ...` |

These are passed as **style hints** to the pptx skill, which will honor them
as closely as the rendering engine allows.

## Handoff Prompt Template

```
/pptx

Create a presentation with the following slides:

**Deck:** {{deck_title}}
**Style:** {{talk_style}}, audience: {{audience}}
**Visual Style:**
- Primary color: {{vi_primary_color}}
- Secondary color: {{vi_secondary_color}}
- Accent color: {{vi_accent_color}}
- Background: {{vi_background_color}}
- Text color: {{vi_text_color}}
- Title font: {{vi_title_font}}, {{vi_title_size}}pt
- Body font: {{vi_body_font}}, {{vi_body_size}}pt
- Code font: {{vi_code_font}}
- Chart colors: {{vi_chart_colors}}

{{for each slide}}
---
Slide {{n}}: {{title}}
Type: {{type}}
{{if bullets}}Bullets:
{{bullets joined by newline}}{{/if}}
{{if figure_needed}}[Insert {{figure_ref}}: {{figure_hint}}]{{/if}}
{{if questions}}Discussion questions:
{{questions joined by newline}}{{/if}}
{{/for}}
```

## Trigger Condition

Call pptx skill automatically when ALL of these are true:
1. Mode is `presentation` or `presentation_with_figures`
2. Slide plan has been generated and confirmed (or user gave no objection within the same turn)
3. User has not explicitly said "just the outline" / "只要大纲" / "不用生成PPT"

## What to Pass

- The filled slide plan as a structured prompt (not raw JSON)
- The filled slide plan described by prompt should be as similar as possible to the JSON
structure of `references/presentation-schema.md` 
- Deck title and style context in the opening line
- Each slide as a labeled block with title + bullets + figure hints

## What NOT to Pass

- Raw slides.json — pptx skill takes natural language, not JSON
- Internal tags like `[原文声明]` — strip these before handoff
- Speaker notes — these are for the analyst output only, not the PPT
