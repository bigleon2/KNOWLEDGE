# Sous-registre KB — Design (conteneur-routeur)

> **Parent** : `skills/design/SKILL.md`
> **Rôle** : Routeur vers 112 sous-skills de design HTML
> **Date** : 2026-08-10
> **Version** : 1.0.0

---

## Architecture

```
design/                          ← Routeur (SKILL.md)
├── horizontal-craft/           ← 20 fichiers de contraintes transversales (pas des skills)
├── design-templates/           ← 36 sous-skills de templates
│   ├── [23 templates généraux]
│   └── ppt/                    ← 8 sous-skills de présentations + 5 thèmes zhangzara
└── design-systems/
    ├── style-skills/           ← 76 sous-skills de vocabulaire visuel
    └── brand-inspiration/      ← 89 dirs de données (DESIGN.md, pas de SKILL.md)
```

---

## Style-skills (76)

Vocabulaires visuels auto-contenus. Chaque dossier contient `SKILL.md` + `DESIGN.md`.

| # | Style | Fichier |
|---|-------|---------|
| 1 | agentic | style-skills/agentic/SKILL.md |
| 2 | ant | style-skills/ant/SKILL.md |
| 3 | application | style-skills/application/SKILL.md |
| 4 | artistic | style-skills/artistic/SKILL.md |
| 5 | atelier-zero | style-skills/atelier-zero/SKILL.md |
| 6 | bento | style-skills/bento/SKILL.md |
| 7 | bold | style-skills/bold/SKILL.md |
| 8 | brutalism | style-skills/brutalism/SKILL.md |
| 9 | cafe | style-skills/cafe/SKILL.md |
| 10 | claude | style-skills/claude/SKILL.md |
| 11 | claymorphism | style-skills/claymorphism/SKILL.md |
| 12 | clean | style-skills/clean/SKILL.md |
| 13 | codex | style-skills/codex/SKILL.md |
| 14 | colorful | style-skills/colorful/SKILL.md |
| 15 | contemporary | style-skills/contemporary/SKILL.md |
| 16 | corporate | style-skills/corporate/SKILL.md |
| 17 | cosmic | style-skills/cosmic/SKILL.md |
| 18 | creative | style-skills/creative/SKILL.md |
| 19 | dashboard | style-skills/dashboard/SKILL.md |
| 20 | default | style-skills/default/SKILL.md |
| 21 | dithered | style-skills/dithered/SKILL.md |
| 22 | doodle | style-skills/doodle/SKILL.md |
| 23 | dramatic | style-skills/dramatic/SKILL.md |
| 24 | editorial | style-skills/editorial/SKILL.md |
| 25 | elegant | style-skills/elegant/SKILL.md |
| 26 | energetic | style-skills/energetic/SKILL.md |
| 27 | enterprise | style-skills/enterprise/SKILL.md |
| 28 | expressive | style-skills/expressive/SKILL.md |
| 29 | fantasy | style-skills/fantasy/SKILL.md |
| 30 | fiction | style-skills/fiction/SKILL.md |
| 31 | flat | style-skills/flat/SKILL.md |
| 32 | friendly | style-skills/friendly/SKILL.md |
| 33 | futuristic | style-skills/futuristic/SKILL.md |
| 34 | glassmorphism | style-skills/glassmorphism/SKILL.md |
| 35 | gradient | style-skills/gradient/SKILL.md |
| 36 | hud | style-skills/hud/SKILL.md |
| 37 | immersive | style-skills/immersive/SKILL.md |
| 38 | impeccable | style-skills/impeccable/SKILL.md |
| 39 | levels | style-skills/levels/SKILL.md |
| 40 | lingo | style-skills/lingo/SKILL.md |
| 41 | luxury | style-skills/luxury/SKILL.md |
| 42 | material | style-skills/material/SKILL.md |
| 43 | matrix | style-skills/matrix/SKILL.md |
| 44 | minimal | style-skills/minimal/SKILL.md |
| 45 | mission-control | style-skills/mission-control/SKILL.md |
| 46 | modern | style-skills/modern/SKILL.md |
| 47 | mono | style-skills/mono/SKILL.md |
| 48 | neobrutalism | style-skills/neobrutalism/SKILL.md |
| 49 | neon | style-skills/neon/SKILL.md |
| 50 | neumorphism | style-skills/neumorphism/SKILL.md |
| 51 | pacman | style-skills/pacman/SKILL.md |
| 52 | paper | style-skills/paper/SKILL.md |
| 53 | parchment | style-skills/parchment/SKILL.md |
| 54 | perspective | style-skills/perspective/SKILL.md |
| 55 | premium | style-skills/premium/SKILL.md |
| 56 | professional | style-skills/professional/SKILL.md |
| 57 | publication | style-skills/publication/SKILL.md |
| 58 | refined | style-skills/refined/SKILL.md |
| 59 | retro | style-skills/retro/SKILL.md |
| 60 | riso | style-skills/riso/SKILL.md |
| 61 | sega | style-skills/sega/SKILL.md |
| 62 | shadcn | style-skills/shadcn/SKILL.md |
| 63 | simple | style-skills/simple/SKILL.md |
| 64 | sketch | style-skills/sketch/SKILL.md |
| 65 | skeumorphism | style-skills/skeumorphism/SKILL.md |
| 66 | sleek | style-skills/sleek/SKILL.md |
| 67 | spacious | style-skills/spacious/SKILL.md |
| 68 | storytelling | style-skills/storytelling/SKILL.md |
| 69 | terracotta | style-skills/terracotta/SKILL.md |
| 70 | tetris | style-skills/tetris/SKILL.md |
| 71 | totality-festival | style-skills/totality-festival/SKILL.md |
| 72 | trading-terminal | style-skills/trading-terminal/SKILL.md |
| 73 | urdu | style-skills/urdu/SKILL.md |
| 74 | vibrant | style-skills/vibrant/SKILL.md |
| 75 | vintage | style-skills/vintage/SKILL.md |
| 76 | warm-editorial | style-skills/warm-editorial/SKILL.md |

---

## Design-templates (36)

Templates HTML réutilisables. Chaque dossier contient `SKILL.md` + fichiers de build.

| # | Template | Chemin relatif |
|---|----------|----------------|
| 1 | ascii-cosmos | design-templates/ascii-cosmos |
| 2 | pricing-page | design-templates/pricing-page |
| 3 | wechat-cover-pair | design-templates/wechat-cover-pair |
| 4 | riso-product | design-templates/riso-product |
| 5 | industrial-archive | design-templates/industrial-archive |
| 6 | dashboard | design-templates/dashboard |
| 7 | social-card-map | design-templates/social-card-map |
| 8 | digital-eguide | design-templates/digital-eguide |
| 9 | xianying-tool | design-templates/xianying-tool |
| 10 | project-brief | design-templates/project-brief |
| 11 | social-card-swiss | design-templates/social-card-swiss |
| 12 | social-card-quote | design-templates/social-card-quote |
| 13 | waitlist-page | design-templates/waitlist-page |
| 14 | social-card-screenshot-explainer | design-templates/social-card-screenshot-explainer |
| 15 | saas-landing | design-templates/saas-landing |
| 16 | video-shortform | design-templates/video-shortform |
| 17 | portfolio-detail | design-templates/portfolio-detail |
| 18 | blog-post | design-templates/blog-post |
| 19 | social-card-data-kpi | design-templates/social-card-data-kpi |
| 20 | social-card-image-led | design-templates/social-card-image-led |
| 21 | team-okrs | design-templates/team-okrs |
| 22 | social-carousel | design-templates/social-carousel |
| 23 | social-card-editorial | design-templates/social-card-editorial |
| 24 | html-ppt-zhangzara-8-bit-orbit | design-templates/ppt/html-ppt-zhangzara-8-bit-orbit |
| 25 | html-ppt-zhangzara-retro-zine | design-templates/ppt/html-ppt-zhangzara-retro-zine |
| 26 | guizang-ppt | design-templates/ppt/guizang-ppt |
| 27 | html-ppt-zhangzara-grove | design-templates/ppt/html-ppt-zhangzara-grove |
| 28 | ib-pitch-book | design-templates/ppt/ib-pitch-book |
| 29 | html-ppt-zhangzara-retro-windows | design-templates/ppt/html-ppt-zhangzara-retro-windows |
| 30 | html-ppt-zhangzara-pin-and-paper | design-templates/ppt/html-ppt-zhangzara-pin-and-paper |
| 31 | html-ppt-zhangzara-biennale-yellow | design-templates/ppt/html-ppt-zhangzara-biennale-yellow |
| 32 | audio-jingle | design-templates/audio-jingle |
| 33 | wireframe-sketch | design-templates/wireframe-sketch |
| 34 | html-ppt-xhs-post | design-templates/html-ppt-xhs-post |
| 35 | vr-canvas | design-templates/vr-canvas |
| 36 | dot-matrix-xhs | design-templates/dot-matrix-xhs |

---

## Horizontal-craft (20 fichiers, pas des skills)

Contraintes transversales chargées à la demande par le routeur.

Fichiers : `chinese-typography.md`, `color-convention.md`, `color-system.md`, `image-convention.md`, `icon-system.md`, `layout-convention.md`, `no-ai-slop.md`, `responsive-convention.md`, `spacing-convention.md`, `text-style-convention.md`, et 10 autres fichiers de référence.

---

## Brand-inspiration (89 dirs, données uniquement)

Références de tokens design par marque. Chaque dossier contient `DESIGN.md` (pas de `SKILL.md`). Ces dirs sont des données de référence, pas des skills.

---

## Convention d'accès

Le routeur `design/SKILL.md` sélectionne automatiquement le sous-skill approprié. Pour un accès direct par `skills-inventory`, scanner `design/SUB-KB.md` au lieu de parcourir l'arborescence.
