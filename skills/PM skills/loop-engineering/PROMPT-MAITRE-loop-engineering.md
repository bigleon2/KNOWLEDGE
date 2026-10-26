---
nom: loop-engineering
version: 1.2.1
source: skills/loop-engineering/SKILL.md
sha256_source: b7b539d0117b
genere: 2026-10-26 (phase P2 — directive 10 tâches, tâche 2)
usage: AUTONOME hors écosystème (dossier « Prompt Maitre » — non lu par l'orchestration)
---

> ⚠️ **MARQUEUR D'EXCLUSION (garde D010)** — CE DOSSIER N'EST PAS LU PAR L'ORCHESTRATION. Les dossiers « Prompt Maitre » sont des prompts autonomes à usage HORS écosystème : ils ne sont pas indexés au registre KB, ne sont mobilisés par aucun arbitre, et ne remplacent jamais la forme installée `skills/<skill>/` (source de vérité).

# Prompt Maître autonome — loop-engineering (v1.2.1)

## Comment utiliser ce prompt (hors écosystème)

Ce document encapsule la compétence sous forme autonome : copiez-le intégralement
dans un assistant IA (ou ouvrez-le en référence directe) — aucune installation,
aucun registre, aucune dépendance à l'écosystème Knowledge d'origine n'est requise.
Les variables de l'écosystème d'origine ont été résolues en valeurs littérales ;
si des ressources `references/` accompagnent ce dossier, elles sont jointes au même
emplacement et le prompt y renvoie par leur chemin relatif. La version d'origine
(source de vérité) vit dans `skills/loop-engineering/SKILL.md` du dépôt KNOWLEDGE.

---

## Le prompt

---
name: loop-engineering
version: 1.2.1
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
  Critères d'arrêt des processus itératifs, définition des graders.
dependencies: []
read_when:
  - Déclencher quand la demande concerne : >-
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

## §0 — Contexte Système (SHARED v1.7.13)

> Écosystème Knowledge : `skills/`=skills/ | `skills/KNOWLEDGE.md`=skills/KNOWLEDGE.md | `true`=true | `NORMAL`=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.



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
- prompt-engineering §1.5 : boucle d'itération évaluer → ajuster → re-évaluer (max 3, dérive documentée).
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

### §1.9bis — Apports de veille 2025-2026 (Task 22 — recherches web ciblées)

- **Calibration des graders agentiques (M2)** : avant tout usage d'un grader agentique dans une boucle — échantillon golden de verdicts attendus, accord ≥ 80 % avec la voie mécanique exigé, juge ≠ rédacteur, ordre des cas randomisé (anti-biais positionnel/self-preference). → *Application locale* : voie L des baselines A2 — 3 runs réels, juge ≠ rédacteur, décisions d'arbitrage consignées.
- **Critères d'arrêt quantifiés** : toute boucle porte (a) un max d'itérations N, (b) un plateau (gain marginal < ε sur 2 cycles consécutifs → arrêt), (c) une escalade propriétaire ; le hash des graders est scellé AVANT le run — toute modification du grader en cours de boucle est un signal de reward hacking (TRACE, arXiv 2601.20103) et invalide les verdicts. → *Application locale* : boucle E12-E13 — max d'itérations + escalade ; instruments figés pendant la boucle (0 fix instrument, leçon Task 22).
- **Vérification intermédiaire** (VPR — Verifiable Process Rewards, arXiv 2605.10325) : un grader léger par étape (contrôle de convergence en cours de route) réduit le coût des échecs découverts tardivement — la vérification unique en fin de phase demeure le filet, pas le seul point de contrôle. → *Application locale* : arbitres par groupe (G-A→G-G) — verdicts intermédiaires avant la certification finale.
- **Limite documentée** (« The Limit of RLVR ») : itérer sans changer de méthode améliore l'efficacité d'échantillonnage, pas la capacité — une boucle qui ne converge pas exige un changement de méthode, pas plus d'itérations. → *Application locale* : échec E12-E13 répété = changement de méthode (ré-écriture du check ou de la couche), jamais plus d'itérations à l'identique.
- **Sources** : TRACE arXiv 2601.20103 · VPR arXiv 2605.10325 · « The Limit of RLVR ».

> **Révision Task 24** (2026-10-23, session web-fdf5963c — directive propriétaire « révisez les §1.9bis des 16 éléments ») : restructuration en bullets actionnables — chaque apport porte son application locale explicite ; bullet Sources normalisé ; contenu factuel Task 22 inchangé (garde anti-perte : lead-ins et sources préservés).

## §2 — SPÉCIFICATION TECHNIQUE

- Markdown (rapports), JSON (benchmarks), Python (graders déterministes et scripts d'évaluation).
- Environnement : ``skills/`loop-engineering/`.
- Arbitres mobilisés : correct-work (hooks E8, E9-E14), verify-cross, scripts de benchmark.
- Sorties : verdicts, feedback exploitable (delta exact, cause d'échec), benchmark itération-N.

## §3 — RELATIONS (extrait de SHARED §3.1)

| Avec | Nature | Détails |
|------|--------|---------|
| gen-plan | consulte/interagit | E10-E15 (boucles d'exécution, calibration). |
| correct-work | consulte/interagit | Graders déterministes (hooks E8, E9-E14). |
| skill-creator | consulte/interagit | Workspaces itératifs (with_skill vs baseline). |
| prompt-engineering | consulte/interagit | Boucle d'itération des artefacts de prompts (§1.5). |

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

- **Révision v1.1.0** : Task 21 P2 (2026-10-03 — Description Optimization A10/A14 : description frontmatter étendue des radicaux discriminants, chirurgies incidents-FP, validation locale zéro-API, contrôles négatifs préservés, arbite V6 re-jeu — cf. calibration KB) (entrée complétée rétrospectivement — Task 12, 2026-10-12, session web-b4d7dd19 — gen-plan(step), directive « appliquer les corrections ») (constat F-d1 : montée non tracée).
- **Origine** : session A11 — matérialisation intermédiaire en agent `_disciplines/` (format §2.3 agent-creator).
- **Matérialisation skill** : session A12, 2026-09-07 — levée de la réserve A11 « agents sans trigger_evals ».
- **Preuve de retrait** : SHA-256 des agents `_disciplines/` consignés avant suppression ; contenu normatif repris ici et en SHARED §7.
- **Statut** : stable ; déclenchement automatique requis.
- **Révision v1.0.1** : session A14 — heuristique de déclenchement v2 (stemmer français léger sous garde de collision, SHARED §7) ; cas trigger_evals inchangés (4/4 v1 et v2).

## §7 — RÉFÉRENCES

- `PROMPT-MAITRE-SHARED.md §7` — source de vérité de la discipline, registre d'assignation et ancrage état de l'art.
- `PROMPT-MAITRE-GEN-PLAN-v3.10.0.md §1.9` — orchestration gen-plan des disciplines.
- `skills/prompt-engineering/SKILL.md` — modèle de matérialisation skill (évals + triggers).
- `skills/KNOWLEDGE.md` — entrée du registre et relations bidirectionnelles.

---

## §8 — Registre d'assignation des disciplines (décentralisé du SHARED §7)

> 📎 Les définitions des disciplines restent dans `PROMPT-MAITRE-SHARED.md §7` (source de vérité conservée) ; le registre d'assignation est copié ici pour l'autonomie du skill (Architecture v2.0).

| Détenteur | Mode de détention | Usage |
|-----------|-------------------|-------|
| `gen-plan` | **Application principale** (méthode-mère) — orchestration : PM gen-plan v3.26.0 §1.9 (PM corpus antérieur toléré — garde R2) | Applique les 5 disciplines à E1-E15 ; délègue l'optimisation fine à `prompt-engineering` |
| `correct-work` | **Fonction héritée** | Lecture et validation d'artefacts de prompts (specs, SKILL.md, rapports de vérification) |
| `clone-chat` | **Fonction héritée** | Assemblage de documents-clones, produits d'ingénierie de prompts |
| `prompt-engineering` | Compétence spécialisée (matérialisé v1.0.1) | Optimisation fine des prompts complexes (délégation gen-plan) |
| `agent-creator` | Fonction héritée (auto-définition : `references/agent-creator.agent` §2.3) | Contexte (mémoire EC/EL) et boucles (pipeline A-H) |
| `context-engineering` / `loop-engineering` / `graph-engineering` / `harness-engineering` | **Matérialisations skills des disciplines** (déclenchement automatique) | Application dédiée de leur discipline respective ; socle normatif : SHARED §7 |

---

## Ressources locales du dossier

Aucune ressource annexe — ce prompt est auto-suffisant.
