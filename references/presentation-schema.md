# Presentation Schema

## Slide Plan JSON Structure

```json
{
  "deck_title": "string",
  "content_source": "standard | extended",
  "audience": "lab | conference | general",
  "talk_style": "technical | overview | discussion",
  "duration_hint": "10min | 20min | 30min",
  "slide_count_target": 9,
  "user_overrides": {
    "emphasis": ["method", "results", "contributions"],
    "skip": ["limitations", "prior_work"],
    "extra_slides": []
  },
  "slides": [
    {
      "n": 1,
      "type": "cover",
      "title": "string",
      "subtitle": "string",
      "authors": "string",
      "venue_year": "string"
    },
    {
      "n": 2,
      "type": "table",
      "role": "metadata",
      "title": "论文基本信息",
      "table_source": "output-schema Section 1",
      "fields": ["标题", "作者", "单位", "Venue", "年份", "DOI/arXiv", "关键词"],
      "omit_if_missing": true
    },
    {
      "n": 3,
      "type": "split",
      "role": "background",
      "title": "string",
      "left": {
        "format": "paragraph",
        "content": "string"
      },
      "right": {
        "format": "figure | bullets",
        "figure_ref": "Fig. X",
        "figure_hint": "string",
        "bullets": ["string"]
      },
      "right_prefer_figure": true
    },
    {
      "n": 4,
      "type": "split",
      "role": "method",
      "title": "方法概述",
      "left": {
        "format": "bullets",
        "bullets": ["string"]
      },
      "right": {
        "format": "figure",
        "figure_ref": "Fig. X",
        "figure_type": "architecture | flowchart | equation | diagram",
        "figure_hint": "string"
      },
      "right_prefer_figure": true,
      "overflow": {
        "enabled": true,
        "max_pages": 2,
        "split_at": "模型架构 / 训练策略"
      }
    },
    {
      "n": 5,
      "type": "contributions",
      "role": "contributions",
      "title": "创新点分析",
      "items": [
        {
          "headline": "string",
          "detail": "string",
          "bold_keywords": ["string"]
        }
      ],
      "source": "output-schema Section 4",
      "max_items": 4
    },
    {
      "n": 6,
      "type": "results",
      "role": "results",
      "title": "实验结果",
      "source": "output-schema Section 5",
      "required_figure": true,
      "figure_ref": "Fig. X / Table X",
      "figure_type": "bar_chart | line_graph | pie_chart | table | figure",
      "figure_hint": "string",
      "content_blocks": [
        {
          "format": "text | bullets | table | figure",
          "content": "string"
        }
      ],
      "overflow": {
        "enabled": true,
        "max_pages": 3,
        "split_strategy": "per_case"
      }
    },
    {
      "n": 7,
      "type": "conclusion",
      "role": "discussion",
      "title": "作者结论",
      "source": "output-schema Section 5 作者结论 [原文声明]",
      "quotes": ["string"],
      "summary_bullets": ["string"]
    },
    {
      "n": 8,
      "type": "prior_work",
      "role": "prior_work",
      "title": "与前作的关系",
      "source": "output-schema Section 6 (extended mode only)",
      "group_focus": "string",
      "prior_papers": ["string"],
      "relationship": "string",
      "note": "[基于论文内引用，非外部检索]"
    },
    {
      "n": 9,
      "type": "closing",
      "title": "string",
      "questions": ["string", "string", "string"]
    }
  ]
}
```

## Field Rules

| Field | Required | Notes |
|-------|----------|-------|
| `deck_title` | yes | Paper title (Chinese OK) |
| `content_source` | yes | Which analysis layer feeds this |
| `audience` | yes | Affects compression level |
| `slide_count_target` | yes | Default 9; adjust per duration_hint |
| `user_overrides.emphasis` | no | Sections to expand |
| `user_overrides.skip` | no | Sections to omit |
| `slides[].role` | yes for bullets | Maps to output-schema section |
| `figure_needed` | yes | true only if figure meaningfully aids understanding |
| `right_prefer_figure` | for split | true = use figure if available; false = use bullets |
| `right.format` | for split | "figure" or "bullets" — set after checking paper content |
| `right.figure_type` | for split | "architecture", "flowchart", "equation", or "diagram" |
| `overflow.enabled` | for method | true = allow slide to expand to max_pages if content is dense |
| `overflow.split_at` | for method | natural break point between page 1 and page 2 |
| `items[].headline` | for contributions | one-sentence summary of the contribution |
| `items[].detail` | for contributions | 1-2 sentence elaboration |
| `items[].bold_keywords` | for contributions | key terms to bold in the detail text |
| `max_items` | for contributions | cap at 4; pick most substantiated from Section 4 |
| `required_figure` | for results | true = must include at least one figure/chart |
| `figure_type` | for results | preferred visualization type from paper |
| `content_blocks` | for results | ordered mix of text/bullets/table/figure blocks |
| `overflow.split_strategy` | for results | "per_case" = one slide per experiment case |

## duration_hint → slide_count_target

| Duration | Slides |
|----------|--------|
| 10min | 6–7 |
| 20min | 9–10 |
| 30min | 12–14 |
