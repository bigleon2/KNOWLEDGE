---
name: harness-engineering
version: "1.0.1"
category: ecosystem
language: fr
tags:
  - harness-engineering
  - harnais
  - gardes-fous
  - arbitres
description: >-
  Skill discipline harness engineering : harnais d'exécution, gardes-fous,
  profilage ressource, arbitres et resserrage après chaque dérive. Spécialise
  la discipline harness engineering (source de vérité : SHARED §7).
dependencies: []
---

## §0 — RÈGLE ZÉRO (résumé de SHARED §0)

Les fichiers des sessions précédentes n'existent pas dans une nouvelle session : tout est
à reconstruire à partir des documents de la lignée. Ne jamais utiliser le verbe « conserver ».
Voir `PROMPT-MAITRE-SHARED.md §0` pour la règle complète.

## §1 — SPÉCIFICATION FONCTIONNELLE

### §1.1 Mission

harness-engineering opérationnalise la discipline **harness engineering** de l'écosystème Knowledge : le harnais (outillage, gardes-fous, journalisation, boucles de feedback) est un artefact réel de l'écosystème — versionné et resserré à chaque dérive constatée — qui transforme un modèle en agent fiable.
Il n'ajoute aucune définition normative : la définition et l'ancrage de la discipline restent dans
**SHARED §7** (source de vérité, session A12) ; le registre d'assignation de SHARED §7 situe ce skill
comme matérialisation dédiée. Ce fichier enregistre uniquement les modes, mécanismes, règles et sorties
qui rendent la discipline exécutable et déclenchable automatiquement.

### §1.2 Modes

| Mode | Nom | Description |
|------|-----|-------------|
| **M1** | Harnais d'exécution | Profils ressource NORMAL/ECO/VIEUX PC, signaux de pression, downgrade irréversible, budget #token par phase, N3 (Python uniquement). |
| **M2** | Harnais de vérification | Arbitres (verify-cross, verify-correct-work, spell-check, sync-download, verify-by-sha) ; hooks correct-work ; resserrage : tout écart détecté devient un nouveau check. |
| **M3** | Journalisation | Worklog structuré (SHARED §1.4), preuves JSON (data/audit/), traçabilité cause / solution / coût #token. |
| **M4** | Sécurité | Règle 0 écriture GitHub, anti-rétrogradation (R2), aucune suppression sans preuve ni journalisation, scellement byte-identique. |

### §1.3 Mécanismes écosystème

- gen-plan §2.4 : profils ressource + signaux de pression (disque, timeouts, budget tokens).
- correct-work : hooks E8 + E9-E14 (contrôle par phase, 3 verdicts).
- Arbitres du dépôt : verify-cross, verify-correct-work, spell-check, sync-download, verify-by-sha.
- SHARED §1.4 : format worklog (observabilité partagée).
- gen-plan §1.11 : idempotence R1-R6 (harnais de ré-exécutabilité).

### §1.4 Règles opérationnelles

- Règle d'or n°1 : adaptation autonome sur blocage (détection, contournement conforme, journalisation, continuité de l'objectif).
- Aucune redéfinition de la discipline : SHARED §7 est la source de vérité ; le présent skill enregistre uniquement son opérationnalisation.
- Provenance obligatoire pour toute information produite (fichier, section, SHA si scellement).
- Règle 0 écriture GitHub : dépôts locaux uniquement ; aucune suppression sans preuve ni journalisation.
- Tout écart détecté par le harnais donne lieu à un resserrage documenté (nouveau check ou correction), jamais à un contournement silencieux.
- Aucun livrable non certifié n'est publié (sync-download + archive round-trip obligatoires).

### §1.5 Mémoire

| Mémoire | Contenu |
|---------|---------|
| **État Court** | profil ressource courant et signaux de pression ; checks en cours et verdicts. |
| **État Long** | historique des versions du harnais (verify-cross v1 → v5 : 60 → 68 → 74 → 84 → 90 checks) ; preuves data/audit/ (JSON datés) ; worklog de session. |

### §1.6 Cycle opérationnel

| Étape | Action |
|-------|--------|
| **A** | Profilage de la tâche (E6) et budget #token (E4). |
| **B** | Mise en place des gardes-fous (hooks, planchers, règles). |
| **C** | Exécution sous surveillance (signaux de pression, M1). |
| **D** | Vérification par arbitres (M2) — verdicts consignés. |
| **E** | Resserrage : écarts → nouveaux checks / corrections (M2). |
| **F** | Journalisation et preuves (M3) ; sécurité et scellement (M4). |

## §2 — SPÉCIFICATION TECHNIQUE

- Python uniquement (N3) pour tout script du harnais ; JSON pour les preuves ; Markdown pour le worklog.
- Environnement : `{{SKILLS_ROOT}}harness-engineering/`.
- Arbitres : verify-cross, verify-correct-work, spell-check, sync-download, verify-by-sha.
- Sorties : profils de ressource, verdicts d'arbitres, preuves JSON, checks de resserrage.

## §3 — RELATIONS (extrait de SHARED §3.1)

| Avec | Nature | Détails |
|------|--------|---------|
| gen-plan | consulte/interagit | E4, E6, E8, E9-E14 (budget, profilage, hooks). |
| correct-work | consulte/interagit | Graders et verdicts (hooks, PROJET). |
| verify-cross / sync-download / verify-by-sha | consulte/interagit | Arbitres du dépôt. |
| KNOWLEDGE.md | consulte/interagit | Entrée script-mon-ecosysteme-infrastructure (outillage). |

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

