---
name: charts
version: 1.0.0
category: ecosystem
language: fr
tags:
  - graphiques
  - diagrammes
  - visualisation
  - matplotlib
  - echarts
  - playwright-css
  - plateforme
description: >
  Création professionnelle de graphiques et diagrammes : graphiques de données
  (barres, lignes, camembert, nuage de points, heatmap, radar, chandeliers,
  boxplot, histogramme, aires, cascade, régression/distribution) ; diagrammes
  structurels (organigrammes, cartes mentales, arbres, architecture, graphes de
  réseaux, ER, classes, Gantt, couloirs, séquences) ; tableaux de bord et panneaux
  KPI. Routage par scène vers le bon framework (matplotlib, seaborn, ECharts, D3.js,
  Mermaid, Playwright+CSS), systèmes de couleurs professionnels, règles anti-chevauchement,
  sorties prêtes pour la publication. Déclencher quand l'utilisateur veut créer,
  dessiner, tracer, visualiser ou peaufiner un graphique, un diagramme ou un tableau
  de bord.
dependencies:
  - skill: pdf
    version: ">=1.0.0"
    used_at: "Frontière — mise en page PDF (le présent skill produit le graphique)"
read_when:
  - Déclencher quand la demande concerne : créer/dessiner/tracer/peaufiner un
    graphique, un diagramme (structurel ou de données) ou un tableau de bord.
  - Déclencher si la demande mentionne : graphique, diagramme, courbe, camembert,
    histogramme, carte mentale, organigramme, flowchart, heatmap, radar, tableau de
    bord, visualisation de données, Mermaid, ECharts, D3, matplotlib.
  - Ne pas déclencher pour la mise en page PDF (pdf), les diaporamas (pptx), les
    tableurs avec graphiques intégrés (xlsx), la génération d'images par IA
    (image-generation), les affiches/infographies (pdf Creative) — convention
    protocole, Task 28. INTERDIT : matplotlib/seaborn pour cartes mentales, arbres,
    organigrammes, organigrammes de flux et tout diagramme structurel — ces derniers
    passent OBLIGATOIREMENT par Playwright+CSS.
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

# CHARTS v1.0.0 — Graphiques et diagrammes professionnels

## §0 — Contexte Système (SHARED v1.7.44)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.
> Langue : FRANÇAIS exclusif pour tous les échanges avec le propriétaire (règle d'or n°6 gen-plan — directive 2026-10-31, renforcée 2026-11-06) : dès le PREMIER mot de toute session ou reprise, la langue d'un message, d'un résumé de continuation ou d'un canal ne dérive JAMAIS la réponse ; toute dérive est corrigée immédiatement.
> Règles d'or & lecture SHARED à l'exécution (directive propriétaire 2026-11-06 — SHARED §9) : tout skill/agent/script exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or de l'écosystème (résumé §9 — canonique gen-plan §1.5).
> Référence canonique skill/agent (directive propriétaire 2026-11-07 — SHARED §0/§1.2) : toute référence à « mon skill X »/« mon agent X » désigne la forme installée à la racine `skills/X/SKILL.md`, JAMAIS le prompt maître du corpus `@mon-ecosysteme/` (ex-nommé `@PM-SKILLS/`) — les PMs sont des spécifications générées mécaniquement (KO-L004), les skills installés sont les formes exécutables.

## §0 — RÈGLE ZÉRO (résumé de SHARED §0)

Skill OUTIL PLATEFORME importé aux normes de l'écosystème via skill-creator —
directive propriétaire Task 113 (trace 1a201e4bda5a2289). Les commandes CLI, le
code et les identifiants de framework restent en anglais verbatim (artefacts
techniques, règle d'or n°6) ; la documentation, les titres et les notes sont en
français. Contenu intégral d'origine conservé byte-identité :
`references/plateforme-original.md` (archive R4 — règles détaillées, arbres de
décision complets, cas d'erreur).

## §1 — Spécification fonctionnelle

Rendre chaque graphique et diagramme professionnel, pas « généré par IA ». Ordre
de chargement : lire le présent fichier → choisir le framework → lire le fichier
template du framework dans `references/` → coder.

### Règle de contrainte de format (PRIORITÉ MAXIMALE)

Quand l'utilisateur SPÉCIFIE un format ou un outil, on s'y conforme — jamais de
substitution :

| L'utilisateur dit | Faire | Interdit |
|-------------------|-------|----------|
| « code Mermaid » / « format Mermaid » | Livrer le bloc de code `mermaid` + un aperçu image rendu | Ne pas livrer l'image seule ; ne pas photographier le code brut |
| « code markdown » | Livrer la hiérarchie markdown | Ne pas basculer en HTML/CSS |
| « via mermaid ou markdown » | Choisir l'un des deux, livrer le texte | Ne pas basculer vers un format non demandé |
| « echarts/d3 » | Utiliser le framework demandé | Ne pas changer de framework |

INTERDIT ABSOLU : livrer une capture d'écran du code source Mermaid comme « image
du diagramme ». Si le rendu échoue : livrer le bloc de code et diriger vers
mermaid.live. Si le contenu déclencherait une montée en gamme automatique (plus de
8 nœuds, texte dense CJK) alors que Mermaid a été demandé : le choix utilisateur
gagne, puis suggérer a posteriori d'essayer sans contrainte.

### Routage (décision)

- **Diagrammes structurels** :
  - organigramme de flux demandé sans format → défaut = vertical par phases
    (Layout C de `references/playwright-css.md`) ;
  - 6 nœuds ou moins, vraiment plat, sans phase → Mermaid ;
  - carte mentale / arbre / organigramme hiérarchique → Playwright + CSS
    (`references/mindmap-css.md`) ;
  - relations / graphe de réseau → ECharts graph ;
  - analyses en grille radiale (SWOT, BSC, Porter, PEST) → `references/radial-grid.md`.
- **Graphiques de données** : barres/lignes/nuages/heatmap/radar/camembert standards
  → matplotlib ; régression/distribution/boxplot → seaborn.
- **Interactif / tableaux de bord** : dashboard, chandeliers, temps réel → ECharts ;
  personnalisé intégral → D3.js.

Une scène = un outil. Les règles détaillées (détection de phases, anti-chevauchement,
couleurs) vivent dans l'archive R4 et les templates de `references/`.

## §2 — Spécification technique

### Emplacement

`{{SKILLS_ROOT}}charts/` — `setup.sh` (vérification et installation de
l'environnement) ; templates par framework dans `references/` (notamment
`playwright-css.md`, `mindmap-css.md`, `radial-grid.md`).

### Frontière avec les autres skills

pdf (mise en page), pptx (diaporamas), xlsx (tableurs avec graphiques intégrés),
image-generation (images par IA), pdf Creative (affiches/infographies) — le présent
skill produit le graphique ou le diagramme lui-même.

## §3 — Relations

| Avec | Nature | Détails |
|------|--------|---------|
| pdf / docx / pptx / xlsx | Consommateurs | Les documents intègrent les graphiques produits ici |
| image-generation | Frontière | Génération artistique vs tracé précis de données/structures |

---

## HISTORIQUE DES VERSIONS

| Version | Date | Changements |
|---------|------|-------------|
| 1.0.0 | 2026-11-22 | Task 113 — import aux normes skill-creator : frontmatter écosystème (semver, category, language, tags, read_when triptyque), §0 Contexte Système, corps français, retrait des emojis décoratifs ; original anglais archivé byte-identité references/plateforme-original.md (R4) |
