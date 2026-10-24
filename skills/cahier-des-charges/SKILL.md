---
name: cahier-des-charges
version: 1.0.0
category: ecosystem
language: fr
tags:
  - cahier-des-charges
  - cdc
  - exigences
  - cadrage
  - specification
  - conception
  - projet
description: >-
  Skill de conception de cahiers des charges : rédige le document de cadrage complet d'un projet
  (contexte et problématique, objectifs mesurables, parties prenantes, périmètre inclus/exclus,
  exigences fonctionnelles EF-xx et non-fonctionnelles ENF-xx, contraintes, livrables, jalons,
  critères d'acceptation MÉCANIQUES, glossaire, annexes) à partir d'un besoin exprimé, d'une
  discussion de cadrage ou d'un document à consolider. 4 modes (M1 CADRER, M2 RÉDIGER, M3 VALIDER,
  M4 FAIRE ÉVOLUER), structure canonique en 12 sections, exigences numérotées atomiques et
  traçables, critères d'acceptation exécutables (aligné spec-driven-development), versionné
  semver et idempotent (re-rédaction = consolidation, jamais de duplication). Utiliser dès que
  l'utilisateur demande de concevoir, rédiger, établir, produire ou faire évoluer un cahier des
  charges, un CDC, un document d'exigences, une spécification de projet, ou qu'un projet doit
  être cadré avant exécution — même sans mention explicite de « cahier des charges ».
dependencies:
  - skill: skill-creator
    version: ">=1.0.0"
    used_at: "conventions structurelles (frontmatter, evals, registre KB)"
read_when:
  - Déclencher quand la demande concerne : concevoir, rédiger, établir, produire ou faire évoluer un cahier des charges (CDC) ou un document d'exigences de projet, cadrer un projet en amont de l'exécution…
  - Déclencher si la demande mentionne : cahier des charges, CDC, exigences, fonctionnelles, cadrage, conception, rédaction, spécification de projet, parties prenantes, périmètre, livrables
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

## §0 — Contexte Système (SHARED v1.7.13)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.

# Cahier des charges

Skill de conception de cahiers des charges — le document de cadrage qui précède tout plan d'actions.
Là où gen-plan organise l'EXÉCUTION et où spec-driven-development contractualise une TÂCHE, le
présent skill produit le CONTRAT DE PROJET : ce qui est attendu, par qui, dans quel périmètre,
avec quels critères d'acceptation — avant qu'aucune ligne de plan ou de code ne soit écrite.

## §1 — Spécification fonctionnelle

### §1.1 Mission

Faire du cahier des charges la source de vérité du projet : transformer un besoin exprimé (demande
utilisateur, discussion de cadrage — y compris une discussion partagée à analyser —, document
existant à consolider) en un document de cadrage complet, exigible et vérifiable. Un projet non
cadré dérive en silence ; le CDC est le contrat qui prévient cette dérive : chaque exigence y est
numérotée, atomique, tracée à sa source et porte un critère d'acceptation exécutable. Le CDC
produit devient l'entrée du plan d'actions (gen-plan E1) — les exigences y deviennent des tâches,
les critères d'acceptation y deviennent des verdicts.

### §1.2 Les 4 modes

| Mode | Nom | Description |
|------|-----|-------------|
| M1 | **CADRER** | Collecter et structurer : besoin, contexte, parties prenantes, sources (demande, discussion, documents), risques, budget/planning indicatifs, indicateurs de succès |
| M2 | **RÉDIGER** | Produire le livrable selon la structure canonique (§1.3) : exigences numérotées EF-xx/ENF-xx, chacune portant son critère d'acceptation |
| M3 | **VALIDER** | Revue de complétude (grille 12 sections), critères d'acceptation exécutables (sinon reformulés), cohérence interne (aucune exigence orpheline, redondante ou contradictoire), validation du propriétaire si le périmètre est neuf |
| M4 | **FAIRE ÉVOLUER** | Amender sans réécrire : table d'amendements datée, version du document bumpée, jamais de modification silencieuse ; re-validation M3 sur les sections touchées |

### §1.3 Structure canonique du livrable (12 sections)

1. **Contexte et problématique** — situation, douleur, opportunité
2. **Objectifs et indicateurs de succès** — mesurables (sinon reformulés)
3. **Parties prenantes et rôles** — qui demande, qui utilise, qui valide, qui subit
4. **Périmètre** — inclus ET exclus explicites (le périmètre exclu protège des dérives)
5. **Exigences fonctionnelles (EF-xx)** — ce que le système fait : fonctions, comportements
6. **Exigences non-fonctionnelles (ENF-xx)** — comment il est : performance, fiabilité, sécurité, maintenabilité, utilisabilité, portabilité, conformité
7. **Contraintes** — techniques, réglementaires, budgétaires, temporelles
8. **Livrables attendus** — nature, format, critère de complétude de chaque livrable
9. **Jalons et planning indicatif** — séquence et dépendances, sans dates inventées
10. **Critères d'acceptation** — mécaniques, rattachés aux exigences (par exigence ou par lot)
11. **Glossaire** — termes du domaine, unités, acronymes
12. **Annexes et sources** — discussions, documents, décisions citées

> Template exécutable (structure, formats, exemples) : `references/template-cahier-des-charges.md`

### §1.4 Règles opérationnelles

1. **Exigence atomique** : une exigence = un besoin testable ; pas de « et » logique — scinder sinon.
2. **Critère d'acceptation exécutable** : chaque exigence porte son check (commande, mesure, arbitre, seuil observable) — un critère non exécutable est reformulé jusqu'à l'être (aligné spec-driven-development : un critère non mécanique n'est pas exigible).
3. **EF vs ENF** : EF = ce que le système FAIT (fonction, comportement observable) ; ENF = comment il EST (qualité attribuable). Les choix de mise en œuvre (techno, architecture) restent hors CDC — ils appartiennent au plan d'actions, sauf contrainte explicite du propriétaire.
4. **Hors-périmètre explicite** : ce que le projet ne fera PAS est écrit noir sur blanc.
5. **Idempotence (R1/R4)** : re-rédaction = consolidation — vérifier présence avant insertion, jamais de duplication ; un CDC existant fait foi, son évolution passe par M4.
6. **Traçabilité** : chaque exigence cite sa source (demande, discussion, décision) ; les amendements sont versionnés (table datée).
7. **Honnêteté (R3)** : les incertitudes et hypothèses sont marquées `[HYP-xx]` avec leur portée — jamais dissoutes dans le texte.
8. **Densité** : chaque section est substantielle (le CDC n'est pas une liste de titres) ; les sections sans contenu réel sont marquées « à compléter en M1 » plutôt que remplies de texte creux.

### §1.5 Cycle opérationnel

1. **Reconnaître** le besoin de cadrage (projet multi-étapes, périmètre neuf, demande explicite — verbatim « conçois/rédige/établis le cahier des charges »).
2. **M1 CADRER** — collecter les sources, les lister, marquer les lacunes à combler par le propriétaire.
3. **M2 RÉDIGER** — remplir la structure canonique section par section, du contexte vers les critères.
4. **M3 VALIDER** — grille 12 sections, critères mécaniques, cohérence interne ; corriger puis re-vérifier (boucle courte).
5. **Livrer** — `download/cahier-des-charges-<projet>.md` (kebab-case), en-tête version + statut + date ; journalisation worklog (Task ID + livrable).
6. **M4 sur demande** — amendement tracé, bump de version, re-validation M3 des sections touchées.

### §1.6 Articulation écosystème

- **gen-plan** : le CDC est l'entrée E1 du plan d'actions — les exigences deviennent les tâches (E7), les critères d'acceptation deviennent les verdicts des phases.
- **spec-driven-development** : le CDC applique le principe spec-first au niveau PROJET ; les specs unitaires (contrat d'une tâche) restent du ressort de SDD — pas de duplication (R4).
- **correct-work** : les critères d'acceptation du CDC servent de checks au mode CIBLE sur les livrables du projet.
- **writing-plans / plans d'implémentation** : en aval du CDC — ils dérivent, ils ne cadrent pas.

## §2 — Spécification technique

- **Livrable** : Markdown, `download/cahier-des-charges-<projet>.md`, en-tête canonique (projet, version, statut BROUILLON/VALIDÉ/ÉVOLUÉ, date, sources).
- **Format d'exigence** : `EF-xx : <capacité observable> — Critère : <check exécutable>` (idem ENF-xx).
- **Format d'hypothèse** : `[HYP-xx] <hypothèse> (portée : ce qui se casse si elle est fausse)`.
- **Format d'amendement** : table `Date | Version | Section | Motif | Source`.
- **Versionnement du document** : semver — MAJOR = refonte du périmètre, MINOR = ajout/retrait d'exigences, PATCH = corrections éditoriales.
- **Aucune dépendance externe** ; tout script de vérification des critères produit est en Python (N3), persisté, idempotent.

## §3 — Relations

| Avec | Nature | Détails |
|------|--------|---------|
| spec-driven-development | Alignement méthode | Critères d'acceptation mécaniques, spec-first — le CDC est la spec de niveau projet, SDD celle de niveau tâche |
| gen-plan | Amont → aval | Le CDC alimente E1-E7 du plan d'actions ; les exigences dérivent en tâches, les critères en verdicts |
| correct-work | Vérification | Les critères d'acceptation du CDC = checks du mode CIBLE sur les livrables du projet |
| skill-creator | Conventions | Frontmatter, evals, registre KB (dépendance déclarée) |

## §4 — Conventions

Kebab-case (dossiers/fichiers) ; semver strict ; tags `#token` ; `{{VARIABLE}}` pour les variables de contexte ; journalisation au worklog (`Task ID` + livrable) pour toute rédaction réelle ; aucune fabrication de résultats (R3) ; idempotence R1-R6 (SHARED §1).

## §5 — Évaluations et déclencheurs

`evals/trigger_evals.json` : 7 requêtes (5 positives, 2 contrôles négatifs — disciplines voisines spec-driven-development et gen-plan) ; déclenchement sur les demandes de conception/rédaction/évolution de cahier des charges. Baseline voie mécanique : MESURÉE à la création (test structurel + arbitres, 2026-10-23) ; voie L (votes LLM 3 runs) : NON MESURÉE — campagne à armer (KO-L001, QUOTA_OK).

## §6 — Traçabilité

- **v1.0.0 (2026-10-23, directive propriétaire session web-f90062ce)** : création — « génère-moi un skill (cohérent, optimisé et fonctionnel) qui aura pour objectif de concevoir des cahiers des charges tel que celui que tu dois concevoir pour ce projet ». SKILL.md + `references/template-cahier-des-charges.md` + evals 5+2 ; inscription registre KB + ECO_SKILLS + porteur evals §8 (recalibrage KO-L004) ; ULTRA régénéré (route §1 + ligne §3). Nom interprété « cahier-des-charges » (coquille « chier-des-charges » dans la directive — interprétation évidente, tracée). Première application : projet Serre CBD Automatisée (directive « conçois le cahier des charges », 2026-10-23).

## §7 — Références

- `references/template-cahier-des-charges.md` — template canonique 12 sections : structure exécutable, formats EF/ENF/HYP/amendements, exemples.
- spec-driven-development (SKILL.md §1) — critères d'acceptation mécaniques, workflow inversé.
- PROMPT-MAITRE-SHARED.md (corpus) — Règle Zéro, conventions, règles R1-R6.
