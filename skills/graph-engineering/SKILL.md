---
name: graph-engineering
version: "1.0.1"
category: ecosystem
language: fr
tags:
  - graph-engineering
  - graphe
  - connaissances
  - kb
description: >-
  Skill discipline graph engineering : graphe de connaissances, nœuds et arêtes
  versionnés, requêtes ancrées dans le registre KB (anti-hallucination).
  Spécialise la discipline graph engineering (source de vérité : SHARED §7).
dependencies: []
---

## §0 — RÈGLE ZÉRO (résumé de SHARED §0)

Les fichiers des sessions précédentes n'existent pas dans une nouvelle session : tout est
à reconstruire à partir des documents de la lignée. Ne jamais utiliser le verbe « conserver ».
Voir `PROMPT-MAITRE-SHARED.md §0` pour la règle complète.

## §1 — SPÉCIFICATION FONCTIONNELLE

### §1.1 Mission

graph-engineering opérationnalise la discipline **graph engineering** de l'écosystème Knowledge : construire et maintenir le graphe de connaissances (nœuds = skills et artefacts, arêtes = relations versionnées, schéma = template KB) pour ancrer les décisions (sélection E5, dépendances, vérifications croisées) dans des faits enregistrés.
Il n'ajoute aucune définition normative : la définition et l'ancrage de la discipline restent dans
**SHARED §7** (source de vérité, session A12) ; le registre d'assignation de SHARED §7 situe ce skill
comme matérialisation dédiée. Ce fichier enregistre uniquement les modes, mécanismes, règles et sorties
qui rendent la discipline exécutable et déclenchable automatiquement.

### §1.2 Modes

| Mode | Nom | Description |
|------|-----|-------------|
| **M1** | Lecture | Requêtes graphe : Protocole de Découverte (SHARED §2.3), sélection des candidats par catégorie, tags et compatibilité de version. |
| **M2** | Écriture | Matérialisations : entrées KB (template SHARED §2.2), arêtes bidirectionnelles (SHARED §3.1), déclarations dependencies des frontmatters. |
| **M3** | Cohérence | Vérification du graphe : cross-references dans les deux sens (SHARED §3.2), planchers de version gradués, arbitre verify-cross. |
| **M4** | Enrichissement | E15 : nouvelles entrées, calibration, historique des interactions. |

### §1.3 Mécanismes écosystème

- KNOWLEDGE.md : nœuds du graphe (skills, versions, catégories, statuts).
- SHARED §3.1-§3.2 : arêtes orientées maintenues bidirectionnellement, planchers de version = versions d'intégration validées.
- SHARED §2.2 : schéma du graphe (template d'entrée).
- SHARED §4 : matrice agent × skill (nœuds agents × nœuds skills).
- frontmatter YAML dependencies : arêtes déclarées au niveau des formes installées.
- verify-cross : arbitre de cohérence du graphe (relations, versions, sections).

### §1.4 Règles opérationnelles

- Règle d'or n°1 : adaptation autonome sur blocage (détection, contournement conforme, journalisation, continuité de l'objectif).
- Aucune redéfinition de la discipline : SHARED §7 est la source de vérité ; le présent skill enregistre uniquement son opérationnalisation.
- Provenance obligatoire pour toute information produite (fichier, section, SHA si scellement).
- Règle 0 écriture GitHub : dépôts locaux uniquement ; aucune suppression sans preuve ni journalisation.
- Toute arête est déclarée dans les deux sens (SHARED §3.2 règle 3) — jamais d'arête orpheline.
- R4 : ne jamais dupliquer (entrées KB, relations) ; R2 : ne jamais rétrograder une version dans le graphe.

### §1.5 Mémoire

| Mémoire | Contenu |
|---------|---------|
| **État Court** | requête courante et sous-graphe concerné ; candidats sélectionnés et leurs versions. |
| **État Long** | graphe complet : KB + registre SHARED §3.1 + matrice §4 ; historique des matérialisations et calibrations. |

### §1.6 Cycle opérationnel

| Étape | Action |
|-------|--------|
| **A** | Requête (quel nœud, quelle décision à ancrer). |
| **B** | Traversal : voisins, compatibilité de versions, planchers. |
| **C** | Réponse fondée sur le graphe (avec référence d'entrée KB). |
| **D** | Écriture éventuelle : nouvelle entrée / arête (M2, bidirectionnelle). |
| **E** | Cohérence : arbitre verify-cross (M3). |
| **F** | Enrichissement E15 (M4) + journalisation. |

## §2 — SPÉCIFICATION TECHNIQUE

- Markdown (KB, registres), YAML (frontmatter dependencies), JSON (preuves), Python (arbitres).
- Environnement : `{{SKILLS_ROOT}}graph-engineering/`.
- Nœuds : `skills/KNOWLEDGE.md` ; schéma : SHARED §2.2 ; arêtes : SHARED §3.1-§3.2.
- Sorties : requêtes ancrées, entrées/arêtes mises à jour, rapport de cohérence du graphe.

## §3 — RELATIONS (extrait de SHARED §3.1)

| Avec | Nature | Détails |
|------|--------|---------|
| gen-plan | consulte/interagit | E5 (sélection ancrée), E15 (enrichissement du graphe). |
| skills-inventory | consulte/interagit | Scan des skills (nœuds disponibles). |
| correct-work | consulte/interagit | Scan dynamique KB (vérification des versions). |
| KNOWLEDGE.md | consulte/interagit | Nœuds et arêtes du registre (source de vérité). |

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

