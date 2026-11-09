---
name: wechat-cover-pair
description: WeChatgabarit de paire de couvertures pour compte officiel — image principale (headline + subline + ancre visuelle）+ image secondaire/partage（titre court + logo / étiquette de compte）+ en-tête d'image longue（titre d'article + aperçu de chapitres). Titres plus épais que pour une couverture Xiaohongshu, zones de sécurité plus explicites, rythme de lecture plus retenu. Lire canvas-and-device.md。Déclencheurs :"fais-moi une couverture de compte officiel / paire première-seconde image WeChat / couverture de chaîne vidéo / image de partage / en-tête d'image longue"。NOT XHS 3:4 comme dimension, NOT le style XHS dense en autocollants.
visibility: public
mode: template
carrier: fixed-image
scenario: social-content
pattern_source: pattern.html
source_priority: skill-first
triggers:
  - "fais-moi une couverture de compte officiel"
  - "paire première-seconde image WeChat"
  - "couverture de chaîne vidéo"
  - "image de partage de compte officiel"
  - "couverture en-tête d'image longue"
  - "couverture écosystème WeChat"
related_patterns: social-card-editorial
---

# WeChat Cover Pair Template

Use for première image de compte officiel WeChat, image de couverture, image de partage, couverture de chaîne vidéo/écosystème WeChat et autres fixed-image surfaces.

## Core Rule

WeChat covers are not Xiaohongshu covers. They need stronger headline legibility, clearer safe areas, and a calmer reading rhythm.

## Structure Options

- main cover: headline + subline + visual anchor
- secondary cover: shorter title + logo/account label
- long image header: article title + section preview
- cover pair: large main cover + smaller share-safe variant

## Must Do

- Read `canvas-and-device.md` for current WeChat dimensions and safe areas.
- Keep title readable in thumbnail contexts.
- Avoid placing important text too close to edges.
- Do not assume XHS 3:4 dimensions.

## Avoid

- XHS-style crowded sticker layouts.
- Long headline squeezed into one line.
- Tiny subtitle that disappears in feed preview.

## Pattern Source Rule

Read this `SKILL.md` first. Do **not** read `pattern.html` by default.

Read `pattern.html` only when you need concrete layout rhythm, spatial relationships, or interaction/annotation behavior that this markdown cannot fully specify. When read, extract patterns only; do not copy DOM, CSS classes, exact spacing, placeholder copy, or styling wholesale.
