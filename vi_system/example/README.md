# VI System — Academic Style

This is the default VI (Visual Identity) configuration for paper-analyst presentations.
It provides a clean, professional academic look with light blue primary color (`#3E87FA`),
white background, and Inter sans-serif typography. Derived from the `slides.html` VI System v2.

## Quick Start

This VI scheme is used by default. No configuration needed.

To explicitly select it, say:

```
用 academic 风格生成 PPT
use the academic VI style
```

## Field Reference

### `colors`

| Field | Value | Used For |
|-------|-------|----------|
| `primary` | `#3E87FA` (light blue) | Title bars, slide headers, key highlights, progress bar |
| `secondary` | `#1E5FD9` (dark blue) | Stat numbers, markers, sub-headers, borders |
| `accent` | `#DC2626` (red) | Emphasis, extreme risk badges, important callouts |
| `background` | `#FFFFFF` (white) | Slide background |
| `text` | `#0F172A` (ink) | Primary body text |
| `text_secondary` | `#475569` (ink-2) | Captions, footnotes, secondary text |
| `slide_title_bar` | `#3E87FA` | Slide title stripe / header bar bottom border |

### `fonts`

| Field | Value | Notes |
|-------|-------|-------|
| `title` | Inter | Used for slide titles and deck title |
| `body` | Inter | Used for bullet points and body paragraphs |
| `code` | Menlo | Used for code snippets, formulas, technical notation |

> **Tip**: For Chinese presentations, consider swapping to `"Noto Sans SC"` or
> `"PingFang SC"` for `title` and `body`. Inter has good Latin coverage but
> limited CJK — the `pptx` skill will fall back to system fonts as needed.

### `sizes`

| Field | Value | Description |
|-------|-------|-------------|
| `title` | 44pt | Deck title on the title slide (60px in slides.html) |
| `subtitle` | 24pt | Subtitle / author line |
| `heading` | 28pt | Section headings on content slides (22px in slides.html) |
| `body` | 16pt | Bullet points and body text (13.5px in slides.html) |
| `caption` | 11pt | Footnotes, page numbers, figure captions |

### `chart`

The `chart.colors` array defines the color sequence for chart series (bars, lines,
pie slices). Colors are applied in order — the first series uses `colors[0]`, etc.

| Field | Value |
|-------|-------|
| `colors` | 8-color palette: blue → dark blue → light blue → green → gold → orange → red → purple |
| `grid_color` | `#E5E9F0` (light gray, matches `--border` in slides.html) |
| `background` | `#FFFFFF` (white) |

### `layout`

All values are in inches.

| Field | Value | Description |
|-------|-------|-------------|
| `margin_top` | 0.35 | Top margin |
| `margin_bottom` | 0.3 | Bottom margin |
| `margin_left` | 0.5 | Left margin |
| `margin_right` | 0.5 | Right margin |
| `title_alignment` | left | Title text alignment |
| `body_alignment` | left | Body text alignment |

---

## How to Create a New VI Scheme

1. Copy this directory:
   ```bash
   cp -r vi_system/example vi_system/my-style
   ```

2. Edit `vi_system/my-style/vi.json` — change colors, fonts, sizes, etc.

3. Use it by saying:
   ```
   用 my-style 风格生成 PPT
   ```

No code changes required. The `SKILL.md` workflow reads `vi_system/<name>/vi.json`
directly based on user trigger words.

## Schema Validation

To validate your custom `vi.json` against the schema:

```bash
python -c "
import json
schema = json.load(open('vi_system/vi-schema.json'))
data = json.load(open('vi_system/my-style/vi.json'))
from jsonschema import validate
validate(data, schema)
print('Valid!')
"
```

All required fields must be present. Optional fields (`layout`, `slide_title_bar`,
`chart.grid_color`, `chart.background`) have sensible defaults if omitted.
