---
name: social-card-screenshot-explainer
description: carte sociale d'explication capture / UI / flux d'outil — la capture doit avoir une "scène"：recadrage lisible + hiérarchie d'annotations + raison d'être. Squelette : couverture + grande capture + 3 annotations / recadrage de capture + détail agrandi + conclusion / paire de captures before-after / cadre UI produit + callouts numérotés / workflow en 3 étapes. La capture doit être assez grande pour être lisible sur mobile, flèches avec retenue, ajouter un titre takeaway. Déclencheurs :"fais-moi une carte tutoriel d'outil / carte workflow IA / carte explication UI / carte capture expliquée / carte before-after"。NOT l'image d'origine balancée sur le canevas, NOT captures décoratives hors sujet.
visibility: public
mode: template
carrier: fixed-image
scenario: social-content
pattern_source: pattern.html
source_priority: skill-first
triggers:
  - "fais-moi une carte tutoriel d'outil"
  - "AI carte workflow"
  - "UI carte explication"
  - "carte capture expliquée"
  - "before-after carte"
  - "carte décorticage de fonctionnalité produit"
related_patterns: social-card-swiss
---

# Social Card Screenshot Explainer

Use for tool walkthroughs, product UI explanations, app feature breakdowns, AI workflow screenshots, or before/after UI captures.

## Core Rule

Never drop a raw screenshot onto the canvas and call it designed. A screenshot needs a stage, readable crop, annotation hierarchy, and a reason to be there.

## Structure Options

- cover + large screenshot + 3 annotations
- screenshot crop + zoomed detail + conclusion
- before / after screenshot pair
- product UI frame + numbered callouts
- 3-step workflow with one screenshot per step

## Must Do

- Keep the screenshot large enough to inspect on phone.
- Crop irrelevant browser chrome unless it helps context.
- Use device/browser frames only when they clarify the source.
- Use arrows/callouts sparingly; labels must not cover key UI.
- Add one takeaway title so the card is not just a screenshot.

## Avoid

- Tiny unreadable UI captures.
- Too many callout bubbles.
- Fake product screenshots.
- Decorative screenshots unrelated to the point.

## Related Pattern

Use `social-card-swiss` as the closest pattern if a visual reference is needed.

## Pattern Source Rule

Read this `SKILL.md` first. Do **not** read `pattern.html` by default.

Read `pattern.html` only when you need concrete layout rhythm, spatial relationships, or interaction/annotation behavior that this markdown cannot fully specify. When read, extract patterns only; do not copy DOM, CSS classes, exact spacing, placeholder copy, or styling wholesale.
