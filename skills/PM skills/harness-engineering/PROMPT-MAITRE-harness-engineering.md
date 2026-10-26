---
nom: harness-engineering
version: 1.2.1
source: skills/harness-engineering/SKILL.md
sha256_source: 14b8aa055e03
genere: 2026-10-26 (phase P2 — directive 10 tâches, tâche 2)
usage: AUTONOME hors écosystème (dossier « Prompt Maitre » — non lu par l'orchestration)
---

> ⚠️ **MARQUEUR D'EXCLUSION (garde D010)** — CE DOSSIER N'EST PAS LU PAR L'ORCHESTRATION. Les dossiers « Prompt Maitre » sont des prompts autonomes à usage HORS écosystème : ils ne sont pas indexés au registre KB, ne sont mobilisés par aucun arbitre, et ne remplacent jamais la forme installée `skills/<skill>/` (source de vérité).

# Prompt Maître autonome — harness-engineering (v1.2.1)

## Comment utiliser ce prompt (hors écosystème)

Ce document encapsule la compétence sous forme autonome : copiez-le intégralement
dans un assistant IA (ou ouvrez-le en référence directe) — aucune installation,
aucun registre, aucune dépendance à l'écosystème Knowledge d'origine n'est requise.
Les variables de l'écosystème d'origine ont été résolues en valeurs littérales ;
si des ressources `references/` accompagnent ce dossier, elles sont jointes au même
emplacement et le prompt y renvoie par leur chemin relatif. La version d'origine
(source de vérité) vit dans `skills/harness-engineering/SKILL.md` du dépôt KNOWLEDGE.

---

## Le prompt

---
name: harness-engineering
version: 1.2.1
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
  Contrôles automatiques anti-dérive des processus, gardes anti-régression.
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

### §1.9bis — Apports de veille 2025-2026 (Task 22 — recherches web ciblées)

- **Mode checkpoint/reprise (M1)** (Anthropic « effective harnesses for long-running agents », 11/2025) : sérialiser l'état de session à chaque phase (snapshots tar, fichier d'état JSON daté) pour reprendre après interruption/timeout sans re-exécution intégrale — pattern des snapshots Task 18 ; le checkpoint est un artefact d'état : déterministe ou exclu du périmètre projeté (leçon Task 20). → *Application locale* : snapshots tar par phase + état JSON daté — reprise sans re-exécution intégrale.
- **Budget de resserrage** : tout nouveau check doit être idempotent ET documenté (quoi, pourquoi, coût) ; revue périodique des checks dormants/redondants avec archivage — le harnais doit rester mince, sinon il devient lui-même la dette (90+ checks sans revue = friction permanente). → *Application locale* : chaque arbitre = idempotent + documenté (provenance en en-tête) ; archivage @historique des checks supplantés.
- **Frontière du vocabulaire** (table commune avec loop-engineering) : ARBITRE = script stdlib déterministe du dépôt (verdict machine, pas de LLM) ; GRADER = mécanique OU agentique d'évaluation, calibré selon loop-engineering M2 ; les deux sont des points de contrôle du harnais, seuls leurs moyens diffèrent. → *Application locale* : vocabulaire uniforme dans les plans et rapports — un arbitre n'est jamais appelé « grader ».
- **Sources** : Anthropic « effective harnesses for long-running agents » (11/2025) · héritage TRACE (arXiv 2601.20103).

> **Révision Task 24** (2026-10-23, session web-fdf5963c — directive propriétaire « révisez les §1.9bis des 16 éléments ») : restructuration en bullets actionnables — chaque apport porte son application locale explicite ; bullet Sources normalisé ; contenu factuel Task 22 inchangé (garde anti-perte : lead-ins et sources préservés).

## §2 — SPÉCIFICATION TECHNIQUE

- Python uniquement (N3) pour tout script du harnais ; JSON pour les preuves ; Markdown pour le worklog.
- Environnement : ``skills/`harness-engineering/`.
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

- **Révision v1.1.0** : Task 21 P2 (2026-10-03 — Description Optimization A10/A14 : description frontmatter étendue des radicaux discriminants, chirurgies incidents-FP, validation locale zéro-API, contrôles négatifs préservés, arbite V6 re-jeu — cf. calibration KB) (entrée complétée rétrospectivement — Task 12, 2026-10-12, session web-b4d7dd19 — gen-plan(step), directive « appliquer les corrections ») (constat F-d2 : montée non tracée).
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
