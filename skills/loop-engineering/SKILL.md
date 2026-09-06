---
name: loop-engineering
version: "1.0.1"
category: ecosystem
language: fr
tags:
  - loop-engineering
  - boucles
  - graders
  - calibration
description: >-
  Skill discipline loop engineering : boucle d'exécution, boucle de vérification
  avec graders et feedback exploitable, boucle externe d'amélioration continue.
  Spécialise la discipline loop engineering (source de vérité : SHARED §7).
dependencies: []
---

## §0 — RÈGLE ZÉRO (résumé de SHARED §0)

Les fichiers des sessions précédentes n'existent pas dans une nouvelle session : tout est
à reconstruire à partir des documents de la lignée. Ne jamais utiliser le verbe « conserver ».
Voir `PROMPT-MAITRE-SHARED.md §0` pour la règle complète.

## §1 — SPÉCIFICATION FONCTIONNELLE

### §1.1 Mission

loop-engineering opérationnalise la discipline **loop engineering** de l'écosystème Knowledge : structurer l'exécution en cycles itératifs à feedback exploitable (boucle d'exécution, boucle de vérification, boucle externe) pour converger vers les critères de succès et améliorer le système à chaque cycle.
Il n'ajoute aucune définition normative : la définition et l'ancrage de la discipline restent dans
**SHARED §7** (source de vérité, session A12) ; le registre d'assignation de SHARED §7 situe ce skill
comme matérialisation dédiée. Ce fichier enregistre uniquement les modes, mécanismes, règles et sorties
qui rendent la discipline exécutable et déclenchable automatiquement.

### §1.2 Modes

| Mode | Nom | Description |
|------|-----|-------------|
| **M1** | Boucle d'exécution | Agent loop : exécuter → observer → corriger jusqu'à complétion (gen-plan E9-E10, E14). |
| **M2** | Boucle de vérification | Grader vs critères : hook E8 (fin de plan) + hooks correct-work CIBLE par phase (E9-E14) ; graders déterministes (checklists S1-S4) privilégiés, graders agentiques à défaut. |
| **M3** | Boucle externe | Chaque cycle rend les boucles internes plus efficaces : E15 auto-calibration (seuils 20 % / 35 %), workspaces skill-creator, Description Optimization. |
| **M4** | Clôture et apprentissage | Verdict final, écarts documentés, gains mesurés consignés (worklog, KB, grille #token). |

### §1.3 Mécanismes écosystème

- gen-plan E10-E13 : boucle exécution → surveillance → détection d'écart → ajustement.
- gen-plan E15 : auto-calibration (prévu → réel → recalibrage, seuils 20 % / 35 %).
- correct-work : hooks E8 + E9-E14 (3 verdicts : PASS / PASS AVEC RÉSERVES / FAIL).
- agent-prompt-engineering §1.5 : boucle d'itération évaluer → ajuster → re-évaluer (max 3, dérive documentée).
- skill-creator : workspaces d'évaluation itératifs (iteration-N, gates mesurées).

### §1.4 Règles opérationnelles

- Règle d'or n°1 : adaptation autonome sur blocage (détection, contournement conforme, journalisation, continuité de l'objectif).
- Aucune redéfinition de la discipline : SHARED §7 est la source de vérité ; le présent skill enregistre uniquement son opérationnalisation.
- Provenance obligatoire pour toute information produite (fichier, section, SHA si scellement).
- Règle 0 écriture GitHub : dépôts locaux uniquement ; aucune suppression sans preuve ni journalisation.
- Tout verdict non-PASS déclenche un ajustement avant re-vérification (jamais de passage en force).
- Tout gain ou écart est mesuré (avant → après) et journalisé — pas d'itération aveugle.

### §1.5 Mémoire

| Mémoire | Contenu |
|---------|---------|
| **État Court** | cycle courant, verdicts et écarts en cours ; deltas mesurés de l'itération en cours. |
| **État Long** | historique des itérations (workspaces, benchmark.json) ; gains mesurés et calibrations (grille #token, KB) ; worklog de session. |

### §1.6 Cycle opérationnel

| Étape | Action |
|-------|--------|
| **A** | Définition des critères (rubrique de vérification). |
| **B** | Exécution du cycle (M1). |
| **C** | Vérification par grader (M2) — verdict + feedback exploitable. |
| **D** | Ajustement si non-PASS, re-vérification. |
| **E** | Boucle externe : bilan du cycle, recalibration des boucles internes (M3). |
| **F** | Clôture : gains consignés, KB et worklog enrichis (M4). |

## §2 — SPÉCIFICATION TECHNIQUE

- Markdown (rapports), JSON (benchmarks), Python (graders déterministes et scripts d'évaluation).
- Environnement : `{{SKILLS_ROOT}}loop-engineering/`.
- Arbitres mobilisés : correct-work (hooks E8, E9-E14), verify-cross, scripts de benchmark.
- Sorties : verdicts, feedback exploitable (delta exact, cause d'échec), benchmark itération-N.

## §3 — RELATIONS (extrait de SHARED §3.1)

| Avec | Nature | Détails |
|------|--------|---------|
| gen-plan | consulte/interagit | E10-E15 (boucles d'exécution, calibration). |
| correct-work | consulte/interagit | Graders déterministes (hooks E8, E9-E14). |
| skill-creator | consulte/interagit | Workspaces itératifs (with_skill vs baseline). |
| agent-prompt-engineering | consulte/interagit | Boucle d'itération des artefacts de prompts (§1.5). |

## §4 — CONVENTIONS

- Nommage kebab-case (SHARED §1.2) ; worklog SHARED §1.4 ; Python uniquement (N3) pour tout script.
- Non-duplication (SHARED §6.3) : la définition de la discipline reste dans SHARED §7 ; ce skill ne la redéfinit pas.
- Toute évolution normative passe par SHARED §7 ; toute évolution opérationnelle passe par une révision de prompt documentée.
- Le déclenchement automatique repose sur `evals/trigger_evals.json` (Description Optimization, heuristique v2).

## §5 — ÉVALUATIONS ET DÉCLENCHEURS

- `evals/evals.json` : 4 évals comportementales au schéma skill-creator, couvrant les modes M1-M4 et la sécurité.
- `evals/trigger_evals.json` : 4 cas de déclenchement (true/false) calibrés pour l'heuristique v2 (v1 : nom du skill normalisé découpé sur « - » + mots de la description ≥ 5 caractères ; radicalisation légère : stemmer français déterministe sous garde de collision avec les cas négatifs officiels — SHARED §7).
- La validation s'exécute à frais dans les workspaces skill-creator (itération-6, session A14 — 40/40 v1 et v2, 3 gains v2 uniques, 0 faux positif).

## §6 — TRAÇABILITÉ

- **Origine** : session A11 — matérialisation intermédiaire en agent `_disciplines/` (format §2.3 autonomous-agent).
- **Matérialisation skill** : session A12, 2026-09-07 — levée de la réserve A11 « agents sans trigger_evals ».
- **Preuve de retrait** : SHA-256 des agents `_disciplines/` consignés avant suppression ; contenu normatif repris ici et en SHARED §7.
- **Statut** : stable ; déclenchement automatique requis.
- **Révision v1.0.1** : session A14 — heuristique de déclenchement v2 (stemmer français léger sous garde de collision, SHARED §7) ; cas trigger_evals inchangés (4/4 v1 et v2).

## §7 — RÉFÉRENCES

- `PROMPT-MAITRE-SHARED.md §7` — source de vérité de la discipline, registre d'assignation et ancrage état de l'art.
- `PROMPT-MAITRE-GEN-PLAN-v3.10.0.md §1.9` — orchestration gen-plan des disciplines.
- `skills/agent-prompt-engineering/SKILL.md` — modèle de matérialisation skill (évals + triggers).
- `skills/KNOWLEDGE.md` — entrée du registre et relations bidirectionnelles.

