# pptx Skill Handoff Format

## When to Call pptx Skill

After generating the slide plan (presentation-schema.md), automatically invoke the `pptx` skill with the structured prompt below. Do NOT ask the user — call it directly.

## Handoff Prompt Template

```
/pptx

Create a presentation with the following slides:

**Deck:** {{deck_title}}
**Style:** {{talk_style}}, audience: {{audience}}

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
