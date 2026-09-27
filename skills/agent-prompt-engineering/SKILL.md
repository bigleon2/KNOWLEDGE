---
name: agent-prompt-engineering
version: 1.0.1
category: infrastructure
language: fr
tags:
  - prompt-engineering
  - optimisation
  - evaluation
  - iteration
  - ecosystem
description: >
  Skill d'optimisation fine des prompts complexes : rédaction, restructuration
  (restructure, restructurer), évaluation, itération et validation des
  déclencheurs (trigger_evals) des artefacts de prompts (PMs, SKILL.md, évals).
  Spécialise la méthode prompt-engineering (méthode-mère : gen-plan ; source de vérité : SHARED §7)
  ; matérialisé le 2026-09-06 (recommandation de session, §5.2).
dependencies:
  - skill: gen-plan
    version: ">=3.7.0"
    used_at: "Consultation du contexte écosystème (planification E1-E8, méthode-mère §1.9)"
---

## §0 — RÈGLE ZÉRO (résumé de SHARED §0)

Les fichiers des sessions précédentes n'existent pas dans une nouvelle session : tout est
à reconstruire à partir des documents de la lignée. Ne jamais utiliser le verbe « conserver ».
Voir `PROMPT-MAITRE-SHARED.md §0` pour la règle complète.

## §1 — SPÉCIFICATION FONCTIONNELLE

### §1.1 Mission

agent-prompt-engineering est le skill d'**optimisation fine des prompts complexes** de l'écosystème. Il reçoit en délégation (gen-plan §1.9, SHARED §3.1) les artefacts de prompts exigeant un travail spécialisé : rédaction, restructuration, évaluation et itération. Il ne redéfinit JAMAIS la méthode prompt-engineering (source de vérité : SHARED §7 ; registre d'assignation : SHARED §7 ; orchestration gen-plan : PM gen-plan §1.9) — il la spécialise sur les artefacts de haut niveau (Prompts Maîtres, SKILL.md, evals, rapports de vérification).

### §1.2 Les 4 opérations

| Opération | Description | Artefacts typiques |
|-----------|-------------|--------------------|
| **Rédaction** | Production d'un prompt nouveau à partir d'une intention (objectif, contraintes, formats de sortie) | PM, SKILL.md, evals |
| **Restructuration** | Réorganisation d'un prompt existant (sections, hiérarchie, tableaux, suppression de duplication) | PM, SKILL.md |
| **Évaluation** | Notation d'un prompt selon la grille (§1.4) : clarté, précision, structure, économie, robustesse | Tout artefact de prompt |
| **Itération** | Boucle évaluer → ajuster → re-évaluer jusqu'au seuil de qualité (loop engineering) | Tout artefact de prompt |

### §1.3 Modes

| Mode | Nom | Description |
|------|-----|-------------|
| M1 | **CIBLE** | Optimisation d'un artefact unique (un SKILL.md, une section de PM) |
| M2 | **PROJET** | Optimisation d'un ensemble cohérent (les §5 de plusieurs PMs, un corpus) |
| M3 | **ÉVALUATION** | Notation seule, sans modification (rapport + recommandations) |
| M4 | **DÉCLENCHEURS** | Validation Description Optimization : trigger_evals (true/false) sur le frontmatter d'un skill |

### §1.4 Grille d'évaluation (5 axes)

| Axe | Question | Seuil PASS |
|-----|----------|------------|
| Clarté | Chaque instruction a-t-elle une seule lecture possible ? | 0 ambiguïté S1/S2 |
| Précision | Les critères sont-ils mesurables (seuils, formats, versions) ? | Critères vérifiables |
| Structure | Les sections suivent-elles les conventions (SHARED §5) ? | Conformes |
| Économie | Le prompt évite-t-il duplication et verbiage (SHARED §6.3) ? | 0 duplication détectée |
| Robustesse | Le prompt survit-il aux cas limites (blocage, wipe, ressource) ? | Règle d'or n°1 couverte |

Détail d'usage : `references/grille-evaluation-prompt.md`.

### §1.5 Boucle d'itération

1. Évaluation initiale (grille §1.4) — rapport M3.
2. Ajustements proposés (un par axe sous seuil), classés par impact.
3. Re-évaluation après application. L'itération s'arrête quand tous les axes PASS, ou après 3 itérations (dérive documentée au worklog, décision utilisateur).

## §2 — SPÉCIFICATION TECHNIQUE

- **Langage** : Markdown (rapports), Python (scripts de mesure), YAML (frontmatter)
- **Environnement** : `{{SKILLS_ROOT}}agent-prompt-engineering/`
- **Arbitres mobilisés** : verify-cross.py (cohérence PM ↔ formes), spell-check.py, verify-correct-work.py
- **Sorties** : rapport d'évaluation (grille §1.4), prompt restructuré (diff documenté), trigger_evals.json (M4)

## §3 — RELATIONS (extrait de SHARED §3.1)

| Avec | Nature | Détails |
|------|--------|---------|
| gen-plan | consulte | Contexte écosystème, planification E1-E8, méthode-mère (SHARED §7), version >= v3.7.0 |
| gen-plan | délégué par | Optimisation fine des prompts complexes (SHARED §3.1) |
| install-ecosystem | utilisé par | Bootstrap P6-P7 (INSTALL-ECOSYSTEME §9.1) |
| correct-work | vérifié par | Conformité des artefacts produits, version >= v2.5.0 |

## §4 — CONVENTIONS

- Nommage kebab-case (SHARED §1.2) ; worklog SHARED §1.4 ; Python uniquement (N3).
- Non-duplication (SHARED §6.3) : la définition des disciplines reste dans SHARED §7 (source de vérité, session A11) ; l'orchestration gen-plan dans PM gen-plan §1.9 ; le présent skill enregistre uniquement ses opérations et sa grille.
- Toute optimisation d'un artefact PM-gouverné passe par une révision de prompt (modèle de toilettage, SHARED en-tête) — jamais d'édition silencieuse.
