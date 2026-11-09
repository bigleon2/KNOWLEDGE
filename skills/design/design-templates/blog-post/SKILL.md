---
name: blog-post
description: Long-form Chinese article / blog-post template — two voices: a wildstay-style lifestyle launch piece with editorial grid + oversized display type, and a WeChat-Official-Account-style serif beauty/longform with measured prose and quiet hairlines.
visibility: public
mode: template
carrier: long-form-article
scenario: editorial-content
pattern_source: qiye-wildstay.html, 肌肤专题｜关于屏障的一次重读.html
source_priority: skill-first
triggers:
  - "fais-moi une page longform"
  - "article long style compte officiel"
  - "page grand titre lifestyle bivouac"
  - "article long spécial beauté"
  - "article de blog chinois"
  - "editorial longform"
---

# Blog Post Template

Use this template for **single-page long-form Chinese articles** — brand stories, lifestyle features, beauty / wellness deep-reads, cultural essays, articles longs style compte officiel rendus en pages web autonomes.

This template ships two variants. Pick before building.

## Variants

### `qiye-wildstay.html` — Lifestyle / brand-launch editorial

- Voice: aspirational, energetic, image-led, asymmetric.
- Use for: plein air / voyage / camping / lancements lifestyle, brand-launch features, récits de marque avec forte photographie.
- Distinctive moves: oversized display numerals (date as poster), Helvetica + PingFang stack, grid-scattered title characters, rotated accent bars, pill CTAs.

### `肌肤专题｜关于屏障的一次重读.html` — Serif long-read

- Voice: introspective, scholarly, text-first.
- Use for: beauté / skincare / santé / vulgarisation / essais culturels approfondis, chroniques sérialisées style compte officiel.
- Distinctive moves: Songti SC display title + Cormorant Garamond italic English subtitle, blue-grey accent rules, justified body, restrained metadata header.

## Use When

- The artifact is a **scrolling web article**, not a fixed-image card.
- Content is paragraph-led with images, pull-quotes, possibly a few module breaks.
- The user wants ambiance compte officiel / spécial magazine / long format de marque — pas une landing SaaS, not a social card.

## Avoid When

- The piece is < 200 words — use a social card instead.
- The content is operational (KPIs, dashboards, schedules, OKRs).
- The output is meant to be exported as one image (use social-card-editorial).
- The user wants a deck (use a `ppt/` template).

## Required Reading

Read this `SKILL.md` first. Then read **only the chosen variant** in full to lift typographic rhythm and section transitions.

Do not mix the two voices in one piece. They embody different reading contracts.

## Design Strategy

Pick the variant from voice, not topic:

- Energy + photography forward → **wildstay**
- Quiet + reasoned + paragraphs → **肌肤专题**

Then decide the spine:

- masthead / metadata strip (issue, date, author, kicker)
- title block (display + sub + dek)
- hero image or hero quote (not both)
- 3–6 body sections with clear hierarchy
- inline images with captions (numbered if many)
- closing / colophon

## Layout Bias

Prefer:

- generous line-height for CJK body (≥ 1.75)
- one display font + one body font, not three
- hairline rules over decorative dividers
- justified or natural ragged-right body — never centered
- captions and metadata in small caps / mono / Latin to break the Chinese rhythm

Avoid:

- emoji decorations inside body copy
- generic blog-card grids ("related posts" tiles)
- background gradients behind body copy
- multi-column body on desktop unless variant explicitly supports it
