# HTML Slide Generation Spec

## When to Use

When `slide_format` is `html` (default), the agent generates a **self-contained HTML file** directly — no external skill invocation needed. This is the default and recommended path because:
- No `pptx` skill dependency required
- Single `.html` file, open in any browser
- Lower token consumption (agent generates code directly vs. invoking another LLM skill)

## Output

- **Filename**: `<deck_title>.html` (sanitized, e.g. `paper-analysis.html`)
- **Format**: Single self-contained HTML file, all CSS/JS inline
- **Aspect ratio**: 16:9 viewport (1280×720 default)
- **Navigation**: Keyboard (← → Space) + touch swipe + click arrows

## VI System → CSS Variable Mapping

Before generating, read the selected `vi_system/<name>/vi.json` and map to CSS custom properties:

```css
:root {
  --primary:       /* colors.primary       */ #3E87FA;
  --secondary:     /* colors.secondary     */ #1E5FD9;
  --accent:        /* colors.accent        */ #DC2626;
  --bg:            /* colors.background     */ #FFFFFF;
  --text:          /* colors.text          */ #0F172A;
  --text-secondary:/* colors.text_secondary */ #475569;
  --title-bar:     /* colors.slide_title_bar */ #3E87FA;
  --title-font:    /* fonts.title          */ 'Inter', sans-serif;
  --body-font:     /* fonts.body           */ 'Inter', sans-serif;
  --code-font:     /* fonts.code           */ 'Menlo', monospace;
  --title-size:    /* sizes.title          */ 44px;
  --subtitle-size: /* sizes.subtitle       */ 24px;
  --heading-size:  /* sizes.heading        */ 28px;
  --body-size:     /* sizes.body           */ 16px;
  --caption-size:  /* sizes.caption        */ 11px;
}
```

Chart colors from `chart.colors` array are used for inline SVG/CSS bar charts.

## HTML File Structure

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{deck_title}}</title>
<style>
/* === Reset & Base === */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body { height: 100%; overflow: hidden; font-family: var(--body-font); color: var(--text); }

/* === CSS Variables (from vi.json) === */
:root { /* ... mapping above ... */ }

/* === Slide Container === */
.deck {
  height: 100vh;
  overflow-y: scroll;
  scroll-snap-type: y mandatory;
  scroll-behavior: smooth;
}
.slide {
  width: 100vw;
  height: 100vh;
  scroll-snap-align: start;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 60px 80px;
  background: var(--bg);
  position: relative;
}

/* === Slide Types === */
/* cover, bullets, split, table, results, closing — see templates below */

/* === Navigation === */
.nav { position: fixed; bottom: 24px; right: 24px; display: flex; gap: 8px; z-index: 10; }
.nav button { /* styled with --primary */ }
.page-indicator { position: fixed; bottom: 28px; left: 24px; font-size: 14px; color: var(--text-secondary); }

/* === Responsive === */
@media (max-width: 768px) {
  .slide { padding: 30px 24px; }
  /* ... scale down fonts ... */
}
</style>
</head>
<body>
<div class="deck">
  <!-- slides here -->
</div>
<script>
// Keyboard nav, touch swipe, page counter
</script>
</body>
</html>
```

## Slide Type Templates

### cover
```html
<div class="slide slide-cover" style="justify-content: center; align-items: center; text-align: center;">
  <div style="width: 100%; height: 6px; background: var(--primary); position: absolute; top: 0;"></div>
  <h1 style="font-family: var(--title-font); font-size: var(--title-size); color: var(--text);">{{title}}</h1>
  <p style="font-size: var(--subtitle-size); color: var(--text-secondary); margin-top: 16px;">{{subtitle}}</p>
  <p style="font-size: var(--body-size); color: var(--text-secondary); margin-top: 32px;">{{authors}}</p>
  <p style="font-size: var(--caption-size); color: var(--text-secondary);">{{venue_year}}</p>
</div>
```

### bullets
```html
<div class="slide">
  <div class="slide-title-bar" style="border-left: 5px solid var(--primary); padding-left: 16px; margin-bottom: 32px;">
    <h2 style="font-family: var(--title-font); font-size: var(--heading-size);">{{title}}</h2>
  </div>
  <ul style="font-size: var(--body-size); line-height: 1.8; list-style: none;">
    <li style="padding: 8px 0; border-bottom: 1px solid #eee;"><span style="color: var(--primary); margin-right: 12px;">●</span>{{bullet_1}}</li>
    <!-- more bullets -->
  </ul>
</div>
```

### split (text + figure/text)
```html
<div class="slide">
  <div class="slide-title-bar" style="border-left: 5px solid var(--primary); padding-left: 16px; margin-bottom: 24px;">
    <h2 style="font-family: var(--title-font); font-size: var(--heading-size);">{{title}}</h2>
  </div>
  <div style="display: flex; gap: 40px; flex: 1;">
    <div style="flex: 1;">{{left_content}}</div>
    <div style="flex: 1;">{{right_content: figure or bullets}}</div>
  </div>
</div>
```

### table
```html
<div class="slide">
  <div class="slide-title-bar" style="border-left: 5px solid var(--primary); padding-left: 16px; margin-bottom: 24px;">
    <h2 style="font-family: var(--title-font); font-size: var(--heading-size);">{{title}}</h2>
  </div>
  <table style="width: 100%; border-collapse: collapse; font-size: var(--body-size);">
    <thead><tr style="background: var(--primary); color: white;">
      <th style="padding: 10px 16px;">{{header}}</th>
    </tr></thead>
    <tbody><tr style="border-bottom: 1px solid #eee;">
      <td style="padding: 10px 16px;">{{cell}}</td>
    </tr></tbody>
  </table>
</div>
```

### results
```html
<div class="slide">
  <div class="slide-title-bar" style="border-left: 5px solid var(--primary); padding-left: 16px; margin-bottom: 24px;">
    <h2 style="font-family: var(--title-font); font-size: var(--heading-size);">{{title}}</h2>
  </div>
  <div style="flex: 1; display: flex; flex-direction: column; gap: 16px;">
    <!-- content blocks: text, bullets, table, or figure -->
  </div>
</div>
```

### closing
```html
<div class="slide" style="justify-content: center; align-items: center; text-align: center;">
  <h2 style="font-family: var(--title-font); font-size: var(--title-size); color: var(--primary);">Thank You</h2>
  <div style="margin-top: 40px; text-align: left; max-width: 600px;">
    <p style="font-size: var(--heading-size); color: var(--text); margin-bottom: 16px;">Discussion</p>
    <ul style="font-size: var(--body-size); line-height: 2; list-style: none;">
      <li style="color: var(--text-secondary);">{{question_1}}</li>
      <!-- more questions -->
    </ul>
  </div>
</div>
```

## Navigation Script

```html
<script>
(function() {
  const deck = document.querySelector('.deck');
  const slides = document.querySelectorAll('.slide');
  const total = slides.length;
  let current = 0;

  function goTo(n) {
    if (n < 0 || n >= total) return;
    current = n;
    slides[n].scrollIntoView({ behavior: 'smooth' });
    document.querySelector('.page-indicator').textContent = (n + 1) + ' / ' + total;
  }

  // Keyboard
  document.addEventListener('keydown', function(e) {
    if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'ArrowDown') { e.preventDefault(); goTo(current + 1); }
    if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') { e.preventDefault(); goTo(current - 1); }
  });

  // Touch swipe
  let touchY = 0;
  deck.addEventListener('touchstart', function(e) { touchY = e.touches[0].clientY; });
  deck.addEventListener('touchend', function(e) {
    const dy = touchY - e.changedTouches[0].clientY;
    if (Math.abs(dy) > 50) { dy > 0 ? goTo(current + 1) : goTo(current - 1); }
  });

  // Scroll detection
  const observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        current = Array.from(slides).indexOf(entry.target);
        document.querySelector('.page-indicator').textContent = (current + 1) + ' / ' + total;
      }
    });
  }, { threshold: 0.5 });
  slides.forEach(function(s) { observer.observe(s); });

  goTo(0);
})();
</script>
```

## Image Handling

- **Figures from paper**: reference via relative path `figures/fig_001.png` (if user has run `extract_pdf_figures.py`)
- **Inline SVG**: for simple bar charts / line graphs, generate inline SVG using chart colors from VI config
- **Base64**: only if the image must be fully embedded (e.g. single-file distribution requirement). Note: this increases file size significantly.

```html
<!-- Relative path (preferred) -->
<img src="figures/fig_001.png" style="max-width: 100%; max-height: 100%; object-fit: contain;" alt="Figure 1">

<!-- Inline SVG bar chart -->
<svg viewBox="0 0 400 200" style="width: 100%; height: auto;">
  <rect x="10" y="40" width="60" height="160" fill="var(--primary)"/>
  <text x="40" y="30" text-anchor="middle" font-size="12">Model A</text>
  <!-- more bars -->
</svg>
```

## Checklist Before Output

1. All VI colors/fonts applied via CSS variables — no hardcoded colors except structural grays (#eee borders etc.)
2. Every slide has a title bar with left border accent
3. Cover slide is centered with top color stripe
4. Bullets ≤ 4 per slide, as per style guide
5. Navigation works: keyboard arrows, space, touch swipe
6. Page indicator shows "N / total"
7. Responsive: readable on mobile (stack split layouts vertically)
8. File is fully self-contained — no external CDN links
