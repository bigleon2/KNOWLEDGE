---
name: docx
version: 1.0.0
category: ecosystem
language: fr
tags:
  - word
  - documents
  - docx
  - creation
  - edition
  - revision
  - plateforme
description: >
  Création, édition et analyse de documents Word (.docx) : création de nouveaux
  documents, modification de contenu, révisions suivies (tracked changes), commentaires,
  préservation du formatage, extraction de texte. Déclencher dès qu'un fichier
  professionnel .docx doit être produit, modifié, annoté, relu ou analysé — rapports,
  contrats, thèses, CV, examens, documents officiels, scripts.
dependencies:
  - skill: pdf
    version: ">=1.0.0"
    used_at: "Frontière — conversion PDF et documents formels imprimables"
read_when:
  - Déclencher quand la demande concerne : créer un document Word, modifier/éditer
    un .docx existant, travailler avec des révisions suivies, ajouter des
    commentaires, analyser ou extraire le contenu d'un .docx.
  - Déclencher si la demande mentionne : document Word, .docx, traitement de texte,
    révisions suivies, tracked changes, commentaires de relecture, première de
    couverture, table des matières Word.
  - Ne pas déclencher pour les PDF natifs (pdf), les diaporamas (pptx) ni les
    tableurs (xlsx) — convention protocole, Task 28.
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

# DOCX v1.0.0 — Atelier de documents Word

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
`references/plateforme-original.md` (archive R4 — listes de contrôle complètes,
règles de couverture, détails API).

## §1 — Spécification fonctionnelle

Un .docx est une archive ZIP de fichiers XML. Le skill couvre création, édition,
lecture et relecture. Route de chargement : (1) déterminer le type de tâche →
charger le fichier de route ; (2) déterminer la scène métier → charger le fichier
de scène ; (3) charger `references/design-system.md` (recettes de couverture,
palettes, couleurs de graphiques) ; (4) charger `references/common-rules.md`
(règles partagées de mise en page, polices, qualité) ; (5) exécuter selon la
route ; (6) passer la liste de contrôle post-génération.

OBLIGATION COUVERTURE : toute première de couverture DOIT utiliser l'une des 7
recettes validées (R1 à R7) de `design-system.md` — le code de couverture libre
est INTERDIT (sources d'incompatibilités : pages blanches MS Office, bordures
manquantes, débordements). Passer par `selectCoverRecipe(docType, industry)` puis
le builder `buildCoverRX()` correspondant.

### Routeur de tâches

| Intention | Route | Fichiers à charger |
|-----------|-------|--------------------|
| Créer/rédiger/générer (sans pièce jointe) | Create | `routes/create.md` + `references/docx-js-core.md` |
| Modifier/réviser (avec pièce jointe) | Edit | `routes/edit.md` + `references/ooxml.md` |
| Format/mise en page/police/marges | Format | `routes/format.md` |
| Commenter/annoter/relire | Comment | `routes/comment.md` |
| Lire/analyser/extraire | Read | `routes/read.md` |

### Routeur de scènes (après la route)

thèse/mémoire/article → `scenes/academic.md` | rapport/analyse/synthèse/proposition →
`scenes/report.md` | contrat/accord/NDA/confidentialité → `scenes/contract.md` |
CV → `scenes/resume.md` | examen/quiz/lesson plan → `scenes/exam.md` | document
officiel/avis/courrier/procès-verbal → `scenes/official-doc.md` | script de
diffusion/copywriting/discours → `scenes/copywriting.md`. Sans scène : règles par
défaut de `references/design-system.md` + `references/common-rules.md`.

## §2 — Spécification technique

### Emplacement et chemins (OBLIGATOIRE avant tout appel de script)

```bash
DOCX_SCRIPTS="<repertoire_du_skill>/scripts"
python3 "$DOCX_SCRIPTS/postcheck.py" output.docx
python3 "$DOCX_SCRIPTS/add_toc_placeholders.py" output.docx --auto
```

Ne JAMAIS utiliser un chemin relatif nu `python3 scripts/...` — toujours le chemin
absolu. Pour les imports Python : insérer `DOCX_SCRIPTS` dans `sys.path`.

### Règles de formatage clés (référence rapide)

- Interligne 1,3 (`line: 312`) OBLIGATOIRE — exceptions : CV 1,15, document
  officiel 28 pt fixes, copywriting `400`, contrat 1,5.
- Corps CJK : justifié + retrait 2 caractères (`firstLine: 480` SimSun / `420` YaHei).
- Tableaux : `margins` renseignés, `ShadingType.CLEAR`, `tableHeader: true`,
  `cantSplit: true`, titre `keepNext: true`.
- Images : paramètre `type` requis, ratio préservé via `image-size`, PageBreak
  dans un Paragraph.
- Échappement des guillemets chinois dans les chaînes JS : source n°1 des bugs —
  utiliser les échappements Unicode.
- Unités : 1 cm = 567 twips | 1 pouce = 1440 twips | A4 = 11906 x 16838 twips.

### Vérification post-génération (deux couches)

1. Liste de contrôle manuelle pendant la génération (couverture, TOC, sauts de
   page, en-têtes/pieds — détail intégral dans l'archive R4) ;
2. `postcheck.py` — 14 règles métier automatisées (pages blanches, débordement de
   couverture, interligne, marges de tableaux, ratio d'images, TOC, propreté du
   document...). Toute erreur doit être corrigée avant livraison.

### Ressources spécialisées

Formules mathématiques : `references/math-formulas.md` (LaTeX converti ; repli
matplotlib PNG pour les cas complexes). Graphiques : `references/chart-templates.md`
(6 modèles matplotlib, couleurs dérivées de la palette du document). TOC complet :
`references/toc.md`.

### Dépendances

pandoc (extraction de texte) | docx via bun/npm (création) | LibreOffice
(conversion PDF) | Poppler (PDF vers image) | defusedxml | python-docx (commentaires).

## §3 — Relations

| Avec | Nature | Détails |
|------|--------|---------|
| pdf | Frontière | PDF natifs et impressions formelles |
| pptx / xlsx | Sœurs | Diaporamas et tableurs — mêmes frontières de format |
| charts | Amont | Graphiques intégrés aux documents |

---

## HISTORIQUE DES VERSIONS

| Version | Date | Changements |
|---------|------|-------------|
| 1.0.0 | 2026-11-22 | Task 113 — import aux normes skill-creator : frontmatter écosystème (semver, category, language, tags, read_when triptyque), §0 Contexte Système, corps français, retrait des emojis décoratifs, suppression des métadonnées plateforme externes du frontmatter ; original anglais archivé byte-identité references/plateforme-original.md (R4) |
