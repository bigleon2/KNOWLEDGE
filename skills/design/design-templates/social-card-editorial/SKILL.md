---
name: social-card-editorial
description: carte sociale style magazine / encre électronique — blancs papier, titres en tension, décor retenu ; rôles de cartes : couverture / couverture numérotée / citation / courts textes éditoriaux en colonnes / photo field note / gros plan de preuve / conclusion / séparateur de chapitre / question hero. Pour opinions / extraits de livres / voyage / lifestyle / culture / récits de marque / explications approfondies. Déclencheurs :"fais-moi une carte magazine / couverture de compte officiel / carte à blancs / carte éditoriale / carte citation"。NOT carte KPI de growth agressive, NOT ton cyber/tech industriel, NOT grande affiche commerciale.
visibility: public
mode: template
carrier: fixed-image
scenario: social-content
pattern_source: pattern.html
source_priority: skill-first
triggers:
  - "fais-moi une carte magazine"
  - "couverture de compte officiel"
  - "carte à blancs"
  - "carte éditoriale"
  - "carte citation"
  - "carte encre électronique"
  - "carte papier"
related_patterns: social-card-quote, social-card-image-led
---

# Social Card Editorial Template

Use this template for social cards that should feel editorial, literary, reflective, premium, or magazine-like.

## Use When

- Couvertures Xiaohongshu / compte officiel / réseaux sociaux nécessitant effet magazine, toucher papier, blancs, tension de titre.
- Le contenu est opinion, extrait de livre, voyage, lifestyle, culture, récit de marque, explication approfondie.
- Images, citations, titres et courts paragraphes doivent former ensemble une carte “sauvegardable” au sens fort.
- The artifact is fixed-canvas and will be delivered as HTML-to-image.

## Avoid When

- The card is highly operational, KPI-heavy, or dashboard-like.
- The content needs dense tables, multiple metrics, or system UI explanation.
- The user asks for a loud commercial poster or cyber/industrial tech look.

## Required Reading

Read this `SKILL.md` first. Do **not** read `pattern.html` by default.

Read `pattern.html` only if you need to inspect visual rhythm or layout relationships. When read, extract patterns only; do not copy DOM, CSS classes, exact spacing, placeholder copy, or WebGL behavior wholesale.

## Design Strategy

This template offers an editorial stance, not a fixed layout. Start from the current brief and choose one card role:

- cover / issue cover
- pull quote / thesis
- editorial essay split
- field note photo
- evidence feature
- closing note
- section divider
- hero question

Then adapt the card around the chosen role.

## Layout Bias

Prefer:

- large title blocks with intentional line breaks
- paper-like background or quiet monochrome surfaces
- hairline rules, issue strips, captions, marginal notes
- one strong image crop or one dominant quote
- restrained accent marks rather than decorative stickers

Avoid:

- generic rounded card grids
- under-filled portrait canvases
- treating photos as small decorative thumbnails
- adding ornamental Chinese motifs without content reason

## Platform / Size

Use `canvas-and-device.md` to select the exact output size. For Xiaohongshu/RED, WeChat covers, or other platform-specific surfaces, do not hard-code sizes in this template.
