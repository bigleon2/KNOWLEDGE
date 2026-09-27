---
name: fleet-engineering
version: "1.0.0"
category: ecosystem
language: fr
tags:
  - fleet-engineering
  - flotte
  - agents
  - orchestration
  - multi-agents
  - supervisor
  - fan-out
description: >-
 Skill discipline fleet engineering : orchestration de flottes d'agents — Agent Teams / Managed Agents, découplage cerveau/exécution, 5 patterns production fan-out-pipeline-debate-supervisor-swarm, coordination multi-instances avec Task IDs, agrégation et arbitrage des résultats. Spécialise la discipline fleet engineering (source de vérité : SHARED §7). Opérationnalisation 2026 : Anthropic Agent Teams & Managed Agents (2026), multi-agent research system (Anthropic, juin 2025), State of Agent Engineering (LangChain, 2026). Fondements documentés : references/fondements-academiques.md.
dependencies: []
---

## §0 — Contexte Système (SHARED v1.5.2)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (exception)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.

## §0 — RÈGLE ZÉRO (résumé de SHARED §0)

1. **Auto-contenu** : ce skill porte tout ce dont il a besoin ; pas de référence hors écosystème hors `references/`.
2. **Versionné semver** : toute modification majeure de comportement → bump MINOR/MAJOR + KB synchronisé.
3. **KB source de vérité** : la description et la version du présent SKILL.md sont répliquées dans `{{KB_PATH}}`.
4. **Dépendances déclarées** : YAML `dependencies` uniquement ; pas d'import implicite.

## §1 — SPÉCIFICATION FONCTIONNELLE

### §1.1 Mission
Orchestrer plusieurs agents/instances comme une FLOTTE ingénierée — pas un essai spontané : choisir le pattern de coordination, assigner des tâches identifiées (Task ID), borner les ressources, agréger les résultats, arbitrer les divergences et journaliser la lignée de chaque sous-tâche. La flotte existe pour un objectif explicite du plan (gen-plan E-série) ; sa taille, son pattern et son budget sont des décisions d'ingénierie documentées, jamais un effet de bord. Le détenteur principal est gen-plan (§1.9) ; les autres skills en détiennent la fonction héritée.

### §1.2 Modes
- **M1 SUPERVISOR (défaut)** — un coordinateur + N workers spécialisés ; s'applique à toute tâche parallélisable avec points de fusion clairs (arbitrage central).
- **M2 FAN-OUT** — N tâches indépendantes lancées simultanément (recherches web multi-requêtes, balayages de répertoires) ; agrégation en une passe.
- **M3 PIPELINE** — chaîne séquentielle avec handoffs typés (spécifier → implémenter → vérifier) ; chaque étage valide l'entrée du suivant.
- **M4 DEBATE** — N agents proposent, un arbitre tranche sur pièces (décisions à controverses, arbitrages d'architecture) ; trace des arguments conservée.
- **M5 SWARM (rare)** — exploration émergente sans coordinateur unique ; réservé aux balayages exploratoires à faible coût unitaire, avec quota strict.

### §1.3 Mécanismes écosystème
Registre KB (source de vérité), worklog append-only (lignée des Task ID), hooks gen-plan (E1-E15, Graph Diamond E9-E14 pour la parallélisation), arbitres mécaniques (integrity/interactions/n15) comme critères de sortie de flotte, answer key pour les décisions. Chaque agent reçoit : Task ID global, lecture du worklog préalable, obligation d'appendre sa section — la flotte ne remplace jamais la traçabilité individuelle.

### §1.4 Règles opérationnelles
1. **Choix du pattern documenté AVANT le lancement** (M1-M5 + pourquoi, dans le plan ou le worklog) ; M1 par défaut, M5 exception motivée.
2. **Bornes de coût** : nombre d'agents, timeout par sous-tâche, budget #token — fixés au cadrage ; un agent sans borne ne part pas.
3. **Verrous de fichiers partagés** : deux agents n'éditent jamais le même fichier ; les éditions planaires/worklog restent mono-writer.
4. **Agrégation arbitrée** : les résultats convergent vers un consolidateur unique qui re-vérifie mécaniquement (arbitres) avant de déclarer le statut.
5. **R3** : un livrable non validé est « en attente de validation », jamais « validé » — y compris quand il vient d'un agent de la flotte.
6. **Adaptation autonome (D017)** : l'échec d'un agent est un signal de re-planification (pattern, bornes, découpage), jamais un arrêt implicite.

### §1.5 Mémoire
État Long : worklog (sections par Task ID), KB, answer key — écrits par l'agrégateur ; État Court : contexte de chaque agent, mort avec lui. Le plan d'actions (`download/plan-actions-*.md`) est la mémoire d'intention de la flotte : toute reprise (REPRISE) repart du plan et du worklog, jamais de la mémoire d'un agent disparu. Référence croisée : memory-engineering (pilliers write/select/compress/isolate).

### §1.6 Cycle opérationnel
1. **Cadrer** : objectif final, pattern, bornes, Task IDs globaux (du plan).
2. **Assigner** : prompt auto-contenu par agent (contexte, lecture worklog, livrable attendu, journalisation obligatoire).
3. **Exécuter** : surveiller signaux D017 (timeout, blocage, ressource) ; re-planifier au besoin sans changer l'objectif.
4. **Agréger** : consolidation unique, re-vérification mécanique, conflits tranchés sur pièces (M4 si divergence persistante).
5. **Journaliser** : worklog (Stage Summary), KB si décision d'architecture, answer key si décision E1.
6. **Démobiliser** : aucune flotte résiduelle ; process tués, verrous libérés, états « EN ATTENTE » consignés honnêtement.

### §1.7 Fondements académiques et veille (N34, 2026-09-21 — n°54)
Recherches N31/N34 vérifiées (preuves `tmp/n31-recherche/`) : **Agent Teams** (Claude Code, code.claude.com) — plusieurs instances coordonnées, un team lead assigne et fusionne ; **Managed Agents** (Anthropic, avr. 2026) — découplage du « cerveau » et de l'exécution pour scaler ; **5 patterns production 2026** (fan-out, pipeline, debate, supervisor, swarm — digitalapplied, mai 2026) avec best-fit par usage ; **multi-agent research system** (Anthropic, juin 2025) — leçons d'ingénierie (orchestrateur + sous-agents, citation obligatoire) ; **State of Agent Engineering** (LangChain, 2026) — la coordination multi-agents devient une discipline d'ingénierie (test, déploiement). Détail et sources : `references/fondements-academiques.md`.

## §2 — SPÉCIFICATION TECHNIQUE
Artefacts : matrice d'assignation (Task ID × agent × livrable × bornes) ; journal d'agrégation (résultats, verdicts d'arbitres, divergences) ; les prompts d'agents sont auto-contenus et citent leur Task ID. Transport : outils `Task` (sous-agents) du harnais ; aucune exécution SDK hors demande explicite (D013). Idempotence : le relancement d'une flotte ne duplique pas les livrables (reprise par Task ID, pattern --skip-done).

## §3 — RELATIONS (extrait de SHARED §3.1)
- `gen-plan` §1.6/§1.9 — détenteur principal : décide du pattern et des bornes à E5/E7.
- `harness-engineering` — l'arbitrage mécanique des livrables de flotte est un critère de harnais.
- `loop-engineering` — la boucle externe génère/vérifie sur les sorties agrégées.
- `memory-engineering` — État Long de la flotte (worklog, KB) ; jamais dans la mémoire d'un agent.
- `spec-driven-development` — chaque sous-tâche de flotte porte une micro-spécification vérifiable.

## §4 — CONVENTIONS
Kebab-case pour dossiers/fichiers ; semver strict ; tags `#token` ; `{{VARIABLE}}` pour les variables de contexte ; journalisation au worklog (`Task ID` + preuves) pour toute exécution réelle ; aucune fabrication de résultats (R3).

## §5 — ÉVALUATIONS ET DÉCLENCHEURS
`evals/trigger_evals.json` : 7 requêtes (5 positives, 2 contrôles négatifs — disciplines voisines) ; déclenchement attendu sur les requêtes d'orchestration multi-agents explicites ; seuil de routage 0.5 (vote majoritaire confirm 3 runs — N34 armé, exécution au QUOTA_OK : D017/R3). Baseline A2 : EN ATTENTE (les 3 skills n°54 sont hors baseline 85 — marqueur `baseline-pending-n34.json`).

## §6 — TRAÇABILITÉ
- v1.0.0 (N34, 2026-09-21, session B12-r56) : matérialisation de la discipline approuvée n°54 ; sources N31 ; intégration gen-plan v3.15.0 §1.9 ; baseline en attente QUOTA (D017).

## §7 — RÉFÉRENCES
- `references/fondements-academiques.md` — sources vérifiées, signaux de veille, interactions.
- SHARED §7 (PROMPT-MAITRE-SHARED.md, corpus) — source de vérité des disciplines.
- gen-plan v3.15.0 §1.9 — routage autonome ; `references/orchestration-skills-agents.md` — matrice.

## §8 — Registre d'assignation des disciplines (décentralisé du SHARED §7)
| Discipline | Détenteur principal | Fonction héritée |
|------------|--------------------|------------------|
| fleet engineering | gen-plan (§1.9 — choix pattern/bornes à E5/E7) | correct-work (arbitrage consolidé), tout agent coordinateur |
