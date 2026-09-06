---
name: context-engineering
version: "1.0.1"
category: ecosystem
language: fr
tags:
  - context-engineering
  - contexte
  - compaction
  - memoire-externe
description: >-
  Skill discipline context engineering : curation du contexte, compaction,
  clairage juste-à-temps, mémoire externe et budget d'attention. Spécialise
  la discipline context engineering (source de vérité : SHARED §7) pour
  composer, contrôler et restituer ce que le système lit avant de répondre.
dependencies: []
---

## §0 — RÈGLE ZÉRO (résumé de SHARED §0)

Les fichiers des sessions précédentes n'existent pas dans une nouvelle session : tout est
à reconstruire à partir des documents de la lignée. Ne jamais utiliser le verbe « conserver ».
Voir `PROMPT-MAITRE-SHARED.md §0` pour la règle complète.

## §1 — SPÉCIFICATION FONCTIONNELLE

### §1.1 Mission

context-engineering opérationnalise la discipline **context engineering** de l'écosystème Knowledge : composer et contrôler ce que le système lit avant de répondre (socle SHARED, registre KB, fichiers corpus, demandes), dans les limites du budget d'attention, pour toute tâche, session ou reconstruction.
Il n'ajoute aucune définition normative : la définition et l'ancrage de la discipline restent dans
**SHARED §7** (source de vérité, session A12) ; le registre d'assignation de SHARED §7 situe ce skill
comme matérialisation dédiée. Ce fichier enregistre uniquement les modes, mécanismes, règles et sorties
qui rendent la discipline exécutable et déclenchable automatiquement.

### §1.2 Modes

| Mode | Nom | Description |
|------|-----|-------------|
| **M1** | Composition | Assembler le contexte pertinent : règle zéro (SHARED §0), socle SHARED lu en premier, registre KB, fichiers corpus et demande (clairage juste-à-temps). |
| **M2** | Contrôle | Respecter le budget d'attention : lecture bloc par bloc pour tout fichier > 500 lignes avec synthèses intermédiaires (compaction), filtrage par profil ressource, priorité au signal fort. |
| **M3** | Restitution | Fournir le contexte au bon consommateur (skill, agent, humain) au bon format, avec provenance (sections, SHAs). |
| **M4** | Réparation | Après wipe inter-sessions ou perte de sortie d'outil : reconstruction du contexte depuis les sources scellées (mon-ecosysteme/, miroir, dépôt, archive). |

### §1.3 Mécanismes écosystème

- SHARED §0 : règle zéro et contexte commun.
- SHARED §2.3 : Protocole de Découverte (clairage juste-à-temps dans le graphe KB).
- gen-plan §1.7 #7 : lecture bloc par bloc avec synthèses intermédiaires (compaction).
- gen-plan §2.4 : filtrage #token par profil (budget d'attention).
- autonomous-agent : mémoire État Court / État Long (mémoire externe).
- clone-chat : contexte de session cloné (compaction inter-sessions).

### §1.4 Règles opérationnelles

- Règle d'or n°1 : adaptation autonome sur blocage (détection, contournement conforme, journalisation, continuité de l'objectif).
- Aucune redéfinition de la discipline : SHARED §7 est la source de vérité ; le présent skill enregistre uniquement son opérationnalisation.
- Provenance obligatoire pour toute information produite (fichier, section, SHA si scellement).
- Règle 0 écriture GitHub : dépôts locaux uniquement ; aucune suppression sans preuve ni journalisation.
- Lecture bloc par bloc pour tout fichier > 500 lignes, avec synthèse intermédiaire.
- Downgrade irréversible du profil ressource (NORMAL → ECO → VIEUX PC) sur signal de pression.

### §1.5 Mémoire

| Mémoire | Contenu |
|---------|---------|
| **État Court** | demande courante et livrables identifiés ; synthèses intermédiaires des fichiers volumineux ; état d'avancement de la tâche. |
| **État Long** | socle SHARED (règle zéro, conventions, relations) ; registre KB (graphe de connaissances) ; clones de session scellés (clone-chat) ; worklog de session (continuité inter-sessions). |

### §1.6 Cycle opérationnel

| Étape | Action |
|-------|--------|
| **A** | Analyse du besoin de contexte (quel consommateur, quelles décisions). |
| **B** | Composition (socle SHARED + KB + corpus + demande). |
| **C** | Contrôle du budget d'attention (compaction si dépassement). |
| **D** | Restitution avec provenance. |
| **E** | Surveillance (dérive, wipe, perte d'outil). |
| **F** | Réparation depuis les sources scellées. |
| **G** | Journalisation (worklog SHARED §1.4). |
| **H** | Enrichissement (E15 : KB, grille). |

## §2 — SPÉCIFICATION TECHNIQUE

- Markdown (SKILL.md), YAML (frontmatter), JSON (evals), Python (scripts de vérification).
- Environnement : `{{SKILLS_ROOT}}context-engineering/`.
- Sources scellées de réparation : `mon-ecosysteme/`, `skills/_prompts-maitres/`, `data/knowledge-repo/`, `_archive/`.
- Sorties : contexte assemblé avec provenance, synthèses intermédiaires, rapport de réparation post-wipe.

## §3 — RELATIONS (extrait de SHARED §3.1)

| Avec | Nature | Détails |
|------|--------|---------|
| gen-plan | consulte/interagit | E2 (inventaire), E5 (sélection), E9-E14 (contexte d'exécution et de vérification). |
| autonomous-agent | consulte/interagit | Mémoire EC/EL (État Court / État Long). |
| clone-chat | consulte/interagit | Contexte de session cloné (persistance). |
| correct-work | consulte/interagit | Contexte de vérification (cibles, verdicts antérieurs). |

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

