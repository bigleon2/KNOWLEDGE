---
name: knowledge-observer
version: 1.0.0
category: ecosystem
language: fr
tags:
  - observation
  - apprentissage
  - auto-amélioration
description: >
  Skill d'observation automatique des sessions pour détecter les patterns
  d'erreur et améliorer les skills de l'écosystème. Cycle A-H (Task Observer),
  4 modes M1-M4 (observation, analyse, proposition, application), journal
  lessons-learned, propositions idempotentes validées par correct-work.
dependencies:
  - skill: gen-plan
    version: ">=3.13.0"
    used_at: "E15 (analyse post-session)"
  - skill: correct-work
    version: ">=2.6.0"
    used_at: "Validation des lessons learned (étape F)"
  - skill: skill-creator
    version: ">=1.0.0"
    used_at: "Application des mises à jour"
---

## §0 — Contexte Système (SHARED v1.6.0)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (exception)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.

## §1 — SPÉCIFICATION FONCTIONNELLE

### §1.1 Mission

knowledge-observer matérialise le pattern **Task Observer** (propositions-qwen.md §1.5,
intégré phase N20) : industrialiser le cycle d'apprentissage continu de l'écosystème en
détection mécanique des récurrences. Le worklog + les boucles R3 + KB Décisions remplissent
déjà le cycle de manière agent-driven ; ce skill le rend **observé, journalisé et validé**.
Source de vérité du pattern : `{{SKILLS_ROOT}}gen-plan/references/observation-patterns.md`.

### §1.2 Le cycle A-H

| Étape | Action | Sortie |
|-------|--------|--------|
| A | Observation passive (M1) | journal de session |
| B | Détection erreurs/patterns récurrents | liste de patterns |
| C | Enregistrement | `data/lessons-learned.json` |
| D | Analyse post-session (M2, E15 gen-plan) | rapport d'analyse |
| E | Proposition de mises à jour (M3) | propositions idempotentes |
| F | Validation correct-work | verdict |
| G | Application si validé (M4) | correctifs appliqués |
| H | Mise à jour KB | entrée + Décisions |

### §1.3 Les 4 modes

| Mode | Nom | Étapes | Description |
|------|-----|--------|-------------|
| M1 | **OBSERVATION** | A-B | Journalise et détecte les récurrences, ne modifie rien |
| M2 | **ANALYSE** | C-D | Enregistre les lessons, rapport d'analyse post-session (E15) |
| M3 | **PROPOSITION** | E-F | Propose des mises à jour idempotentes, fait valider par correct-work |
| M4 | **APPLICATION** | G-H | Applique les correctifs validés, met à jour le KB |

### §1.4 Garde-fous

1. **Observation passive par défaut** : M1 n'écrit que dans `data/lessons-learned.json`.
2. **Aucune auto-modification non validée** : les modes M3-M4 exigent un verdict correct-work (étape F) avant application.
3. **Garde anti-boucle** : max 2 rounds de correction par artefact (SHARED §4.4) — identique pour les lessons.
4. **Idempotence** : toute proposition appliquée porte un marqueur et est rejouable sans effet (R1-R6).

### §1.5 Déclencheurs

- Automatique : invoqué par gen-plan à **E15** (bilan et auto-calibration) en modes M1-M2.
- Manuel : « observe la session », « lessons learned », « analyse les patterns d'erreur ».

## §2 — SPÉCIFICATION TECHNIQUE

- **Langage** : Markdown (rapports), JSON (données), YAML (frontmatter)
- **Environnement** : `{{SKILLS_ROOT}}knowledge-observer/`
- **Données** : `data/lessons-learned.json` (journal des lessons — schéma §4 de la référence)
- **Seuil de récurrence** : un pattern est « récurrent » à 3 occurrences documentées (2 si S1).
- **Arbitres mobilisés** : verify-cross.py (cohérence KB), answer-key-checker.py (décisions), certification-complete.py (5/5 après application M4).

## §3 — RELATIONS

| Avec | Nature | Détails |
|------|--------|---------|
| gen-plan | invoqué par | E15 (analyse post-session, modes M1-M2), version >= v3.13.0 |
| correct-work | valide | Étape F du cycle A-H (validation des lessons, modes M3-M4), version >= v2.6.0 |
| skill-creator | applique via | Application des mises à jour de skills (conventions), version >= v1.0.0 |
| KNOWLEDGE.md | enrichit | Étape H (entrée + Décisions) |

## §4 — CONVENTIONS

- Nommage kebab-case (SHARED §1.2) ; worklog SHARED §1.4 ; idempotence R1-R6 (gen-plan §1.8).
- Non-duplication (SHARED §6.3) : la définition du pattern Task Observer reste dans
  `gen-plan/references/observation-patterns.md` ; le présent skill enregistre uniquement
  son cycle, ses modes et son journal.
- Toute lesson appliquée est tracée au worklog et au KB (étape H) — jamais d'édition silencieuse.
