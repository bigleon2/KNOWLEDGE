---
name: pptx
version: 1.0.0
category: ecosystem
language: fr
tags:
  - powerpoint
  - pptx
  - presentations
  - diaporamas
  - html-slides
  - beamer
  - plateforme
description: >
  Création, édition et analyse de présentations .pptx : créer une présentation
  depuis zéro (pipeline HTML 1280x720 en quatre stages stricts, rendu parallélisé),
  modifier ou éditer le contenu, travailler les mises en page, ajouter des
  commentaires et des notes du présentateur ; les présentations académiques/fondées
  sur un article passent par le module Beamer embarqué (sortie PDF uniquement).
  Déclencher dès qu'un fichier .pptx est l'entrée ou la sortie de la tâche, ou que
  l'utilisateur demande un diaporama, des slides ou une présentation.
dependencies:
  - skill: pdf
    version: ">=1.0.0"
    used_at: "Module Beamer embarqué (présentations académiques, sortie PDF)"
read_when:
  - Déclencher quand la demande concerne : créer un .pptx (ou un diaporama HTML),
    éditer une présentation existante, extraire/analyser son contenu, ajouter
    commentaires ou notes du présentateur.
  - Déclencher si la demande mentionne : PowerPoint, .pptx, présentation, diaporama,
    slides, notes du présentateur, Beamer, deck, pitch deck.
  - Ne pas déclencher pour les documents Word (docx), les PDF non-diaporama (pdf),
    les tableurs (xlsx) — convention protocole, Task 28.
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

# PPTX v1.0.0 — Atelier de présentations

## §0 — Contexte Système (SHARED v1.7.45)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.
> Langue : FRANÇAIS exclusif pour tous les échanges avec le propriétaire (règle d'or n°6 gen-plan — directive 2026-10-31, renforcée 2026-11-06) : dès le PREMIER mot de toute session ou reprise, la langue d'un message, d'un résumé de continuation ou d'un canal ne dérive JAMAIS la réponse ; toute dérive est corrigée immédiatement.
> Règles d'or & lecture SHARED à l'exécution (directive propriétaire 2026-11-06 — SHARED §9) : tout skill/agent/script exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or de l'écosystème (résumé §9 — canonique gen-plan §1.5).
> Référence canonique skill/agent (directive propriétaire 2026-11-07 — SHARED §0/§1.2) : toute référence à « mon skill X »/« mon agent X » désigne la forme installée à la racine `skills/X/SKILL.md`, JAMAIS le prompt maître du corpus `@mon-ecosysteme/` (ex-nommé `@PM-SKILLS/`) — les PMs sont des spécifications générées mécaniquement (KO-L004), les skills installés sont les formes exécutables.

## §0 — RÈGLE ZÉRO (résumé de SHARED §0)

Skill OUTIL PLATEFORME importé aux normes de l'écosystème via skill-creator —
directive propriétaire Task 113 (trace 1a201e4bda5a2289). Les commandes CLI, le
code et les identifiants d'API restent en anglais verbatim (artefacts techniques,
règle d'or n°6) ; la documentation, les titres et les notes sont en français.
Contenu intégral d'origine conservé byte-identité :
`references/plateforme-original.md` (archive R4 — les quatre stages complets avec
leurs listes de contrôle, scripts de conversion, module Beamer).

## §1 — Spécification fonctionnelle

Un .pptx est une archive ZIP de XML. Trois familles de tâches :

### 1. Lire et analyser

- Extraction de texte : `python -m markitdown chemin.pptx` (conversion markdown).
- Accès XML brut (commentaires, notes, mises en page, animations) : dépaqueter
  via `ooxml/scripts/unpack.py <fichier> <dossier_sortie>` — structures clés :
  `ppt/presentation.xml` (métadonnées), `ppt/slides/slideN.xml` (contenu),
  `ppt/notesSlides/` (notes), `ppt/slideLayouts/` + `ppt/slideMasters/`
  (gabarits), `ppt/theme/` (styles), `ppt/media/` (médias).
- Émulation d'un design existant : extraire d'abord la typographie et les couleurs
  (theme1.xml : `clrScheme`/`fontScheme` ; usages réels dans les slides ;
  rechercher `solidFill`, `srgbClr`).

### 2. Créer depuis zéro (sans gabarit fourni)

Pipeline HTML de diaporamas 1280x720 en QUATRE STAGES STRICTS (ne jamais sauter
ni réordonner) — détail intégral dans l'archive R4 :

1. **CLARIFY** — collecter les entrées obligatoires par questions à l'utilisateur
   (thème et but, audience, longueur, style, palette unifiée, typographie, densité
   par page, notes) ; détecter au préalable un éventuel HTML de référence et
   exécuter `scripts/extract_html_style.py` pour en hériter le style.
2. Planification du contenu (structure en sections, brief de slides).
3. Rendu des slides HTML (pages autonomes écrites sur disque ; parallélisation
   possible du rendu des slides de corps).
4. Conversion et vérification.

Si l'utilisateur fournit un .pptx à imiter comme gabarit : suivre la voie
« éditer une présentation existante » plutôt que ce pipeline.

### 3. Éditer une présentation existante

Dépaqueter, modifier le XML ciblé, rempaqueter — en préservant mises en page,
métadonnées et médias intacts.

## §2 — Spécification technique

### Emplacement

`{{SKILLS_ROOT}}pptx/` — `ooxml/scripts/unpack.py` (dépaquetage) ;
`html2pptx1.js` et `batch_html2pptx.js` (conversion HTML vers .pptx) ; module
Beamer académique en fin d'archive R4 (sortie PDF uniquement).

### Bonnes pratiques de création

Une question = une slide ; densité contrôlée ; palette et typographie posées UNE
fois pour tout le diaporama (variables globales) ; notes du présentateur si
demandées ; vérification visuelle des slides avant conversion.

## §3 — Relations

| Avec | Nature | Détails |
|------|--------|---------|
| pdf | Complément | Module Beamer (PDF) ; export PDF de contrôle |
| docx / xlsx | Frontières | Documents Word, tableurs |
| charts | Amont | Graphiques intégrés aux slides |

---

## HISTORIQUE DES VERSIONS

| Version | Date | Changements |
|---------|------|-------------|
| 1.0.0 | 2026-11-22 | Task 113 — import aux normes skill-creator : frontmatter écosystème (name pptx aligné sur le dossier — l'original portait « ppt », semver, category, language, tags, read_when triptyque), §0 Contexte Système, corps français, retrait des emojis décoratifs et des métadonnées plateforme externes ; original anglais archivé byte-identité references/plateforme-original.md (R4) |
