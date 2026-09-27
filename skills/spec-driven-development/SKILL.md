---
name: spec-driven-development
version: "1.0.0"
category: ecosystem
language: fr
tags:
  - spec-driven-development
  - sdd
  - specification
  - contrat
  - acceptance-criteria
  - cadrage
description: >-
 Skill discipline spec-driven development : la spécification comme contrat exécutable — spec AVANT code (workflow inversé), décomposition plan→tâches, critères d'acceptation mécaniques, constitution (guardrails), re-spécification à la dérive. Spécialise la discipline SDD (source de vérité : SHARED §7). Opérationnalisation 2026 : arXiv « From Code to Contract » (janv. 2026), spec-first AI-native engineering (Microsoft), GitHub Spec Kit. Fondements documentés : references/fondements-academiques.md.
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
Faire de la spécification la SOURCE DE VÉRITÉ dont le code/livrable est un artefact généré et vérifiable : cadrer une tâche complexe par une spec exécutable (exigences, contraintes, critères d'acceptation mécaniques), décomposer en tâches, implémenter par dérivation, vérifier contre la spec — et re-spécifier explicitement quand la réalité dérive, au lieu de laisser le code diverger en silence. Dans cet écosystème, la spec est l'équivalent du plan d'actions + answer key pour une tâche unitaire : le détenteur principal est gen-plan (§1.9) qui impose le cadrage spec-first aux tâches complexes avant toute exécution.

### §1.2 Modes
- **M1 SPÉCIFIER** — rédiger la spec : objectif, hors-périmètre, exigences (exigibles), contraintes (protocoles, verrous, budget), critères d'acceptation mécaniques (checks exécutables), constitution (invariants non négociables — R3, D017, D013).
- **M2 DÉCOMPOSER** — plan → tâches atomiques avec livrable et preuve attendus par tâche (Task IDs) ; ordonnancement et verrous.
- **M3 IMPLÉMENTER** — dériver l'implémentation de la spec ; toute décision hors spec est consignée comme AMENDEMENT, jamais dissoute dans le code.
- **M4 VÉRIFIER** — exécuter les critères d'acceptation (arbitres, checks) ; un critère non exécutable est reformulé jusqu'à l'être.
- **M5 RE-SPEC** — à la dérive prouvée : amender la spec d'abord (versionnée), puis le code — jamais l'inverse ; lignée des amendes documentée.

### §1.3 Mécanismes écosystème
Answer key (décisions D0NN = amendements de spec ratifiés), plan d'actions (spec de session), worklog (journal d'exécution tracé), arbitres mécaniques (les critères d'acceptation SDD SONT des arbitres : checks exécutables), hooks gen-plan (E4 cadrage, E7 re-validation). Une spec sans critère mécanique n'est pas une spec SDD mais une intention.

### §1.4 Règles opérationnelles
1. **Spec avant exécution** pour toute tâche complexe (multi-étapes, multi-fichiers, ou non-réversible) ; micro-spécification pour les sous-tâches de flotte.
2. **Critères d'acceptation exécutables** : chaque exigence porte son check (script, grep, arbitre) — sinon ce n'est pas exigible.
3. **Constitution** : les invariants écosystème (R3 honnêteté, D017 adaptation, D013 quota, kebab-case/semver) sont préambule de toute spec — non amendables par tâche.
4. **Amendement tracé** : la spec vit ; toute dérive réelle → amendement versionné (answer key/worklog) AVANT correction du code.
5. **Pas de spec rétroactive** : si l'exécution a précédé, la consolidation re-specifie honnêtement l'état atteint (fait foi) et les écarts restants.
6. **Idempotence** : ré-exécuter une spec = même résultat (checks déterministes).

### §1.5 Mémoire
La spec versionnée est l'État Long de l'intention ; l'answer key journalise ses amendements ; le worklog journalise son exécution. Référence croisée : memory-engineering (l'écriture sélective s'applique à ce que la spec retient — exigences, pas récits) et graph-engineering (les exigences reliées aux décisions forment un graphe traçable).

### §1.6 Cycle opérationnel
1. **Reconnaître** le besoin de spec (complexité, irréversibilité, flou d'acceptation).
2. **Rédiger** la spec (M1) — courte, exigible, critères mécaniques.
3. **Faire valider** (propriétaire ou hook) si périmètre neuf ou candidat d'intégration (protocole approbation n°52/n°54).
4. **Décomposer** (M2) puis exécuter (M3) avec journalisation.
5. **Vérifier** (M4) — tous les critères verts, sinon boucle M5/itération.
6. **Archiver** la lignée spec→amendements→preuves (worklog/rapport).

### §1.7 Fondements académiques et veille (N34, 2026-09-21 — n°54)
Recherches N31/N34 vérifiées (preuves `tmp/n31-recherche/`) : **« From Code to Contract in the Age of AI Coding Assistants »** (arXiv, 30 janv. 2026) — le SDD inverse le flux : la spécification devient source de vérité, le code un artefact généré/vérifié ; **Spec-first AI-native engineering** (Microsoft Developer, juin 2026) — guardrails, exigences, contraintes et critères d'acceptation définis en amont par l'équipe ; **GitHub Spec Kit** — outillage spec→plan→tasks ; **guides SDD 2026** (augmentcode, dev.to) — la spec comme contrat exécutable qui prévient la dérive des agents. Détail et sources : `references/fondements-academiques.md`.

## §2 — SPÉCIFICATION TECHNIQUE
Format spec (canon écosystème) : en-tête (objectif, version, statut) → hors-périmètre → exigences E# (chacune + critère mécanique C#) → constitution → amendements (table datée) → preuves (chemins). Les checks des critères sont des scripts/arbitres persistés — jamais des assertions en l'air.

## §3 — RELATIONS (extrait de SHARED §3.1)
- `gen-plan` §1.9 — détenteur principal : impose le cadrage spec-first (E4) et la re-validation (E7).
- `harness-engineering` — les critères d'acceptation deviennent gardes-fous exécutés à chaque boucle.
- `loop-engineering` — le vérifier (M4) alimente la boucle externe de génération-vérification.
- `fleet-engineering` — micro-specs par sous-tâche de flotte.
- `graph-engineering` — traçabilité exigences↔décisions↔preuves dans le registre KB.

## §4 — CONVENTIONS
Kebab-case pour dossiers/fichiers ; semver strict ; tags `#token` ; `{{VARIABLE}}` pour les variables de contexte ; journalisation au worklog (`Task ID` + preuves) pour toute exécution réelle ; aucune fabrication de résultats (R3).

## §5 — ÉVALUATIONS ET DÉCLENCHEURS
`evals/trigger_evals.json` : 7 requêtes (5 positives, 2 contrôles négatifs) ; déclenchement sur les demandes de cadrage/spécification/contrat d'acceptation ; seuil 0.5 (confirm 3 runs armé — QUOTA_OK). Baseline A2 : EN ATTENTE (`baseline-pending-n34.json`).

## §6 — TRAÇABILITÉ
- v1.0.0 (N34, 2026-09-21, session B12-r56) : matérialisation de la discipline approuvée n°54 (candidat prioritaire N31) ; sources N31 ; intégration gen-plan v3.15.0 §1.9 ; baseline en attente QUOTA (D017).

## §7 — RÉFÉRENCES
- `references/fondements-academiques.md` — sources vérifiées, signaux de veille, interactions.
- SHARED §7 (PROMPT-MAITRE-SHARED.md, corpus) — source de vérité des disciplines.
- gen-plan v3.15.0 §1.9 — routage autonome ; plan d'actions B12 — spec de session opérante.

## §8 — Registre d'assignation des disciplines (décentralisé du SHARED §7)
| Discipline | Détenteur principal | Fonction héritée |
|------------|--------------------|------------------|
| spec-driven development | gen-plan (§1.9 — cadrage E4, re-validation E7) | correct-work (critères = checks de round), toute tâche complexe |
