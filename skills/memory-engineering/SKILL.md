---
name: memory-engineering
version: "1.0.0"
category: ecosystem
language: fr
tags:
  - memory-engineering
  - mémoire
  - etat-long
  - compaction
  - retrieval
  - contexte
description: >-
 Skill discipline memory engineering : mémoire des agents — État Court/État Long, écriture sélective, budget d'attention fini, compaction paramétrable long-horizon, mémoire externe par retrieval (IR/RAG), isolation des contextes. Spécialise la discipline memory engineering (source de vérité : SHARED §7). Opérationnalisation 2026 : AgeMem (arXiv 2026, 110+ citations), Memory in the Age of AI Agents (survey), checkpointing LangGraph/Redis. Fondements documentés : references/fondements-academiques.md.
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
Ingénierer la mémoire des agents plutôt que la subir : décider CE QUI est écrit (sélectivement), où (État Long versionné : worklog, KB, answer key, registres), comment c'est compacté (compaction paramétrable pour les sessions longues), ce qui est isolé (cloisonnement des contextes par tâche/agent) et comment c'est récupéré (retrieval par ancrage, anti-hallucination). Le budget d'attention est FINI : le plus petit ensemble de tokens à fort signal gagne, jamais « tout stocker ». Détenteur principal : gen-plan (§1.9) — qui impose État Long = plan + worklog + KB à toute exécution longue.

### §1.2 Modes
- **M1 ÉCRIRE (write)** — append-only, daté, traçable : worklog (sections Task), KB (calibrations), answer key (décisions). Écrire est une décision d'ingénierie : une information non réutilisable ne mérite pas l'État Long.
- **M2 SÉLECTIONNER (select)** — au moment de lire : choisir le plus petit ensemble à fort signal (ancres, index, résumés condensés) ; la relecture intégrale est l'exception motivée.
- **M3 COMPACTER (compress)** — sessions long-horizon : compaction paramétrable (résumés hiérarchiques, historique condensé « fait foi ») sans perdre les ancrages de reprise (REPRISE, Task IDs, SHA).
- **M4 ISOLER (isolate)** — un contexte par tâche/agent : pas de fuite inter-tâches ; les sous-agents reçoivent un prompt auto-contenu, pas l'historique brut.
- **M5 RÉCUPÉRER (retrieve)** — mémoire externe par retrieval : requêtes ancrées dans le registre KB/answer key (jamais de paraphrase de mémoire) ; la citation pointe une entrée versionnée.

### §1.3 Mécanismes écosystème
Worklog append-only (fait foi), KB (registre des skills/décisions), answer key (D0NN), plan d'actions (intention versionnée), marqueurs d'état (flags, snapshots zip, SHA de référence), caches de reprise (--skip-done) — le tout constitue l'architecture mémoire de l'écosystème ; la présente discipline l'explicite et le gouverne.

### §1.4 Règles opérationnelles
1. **Budget d'attention fini** : sélectionner, ne pas accumuler ; tout mécanisme qui « relit tout » est un bug de conception.
2. **Append-only** : l'État Long n'est jamais réécrit a posteriori (corrections = nouvelle entrée datée) ; R3 interdit la fabrication.
3. **Ancrage anti-hallucination** : toute mémoire citée pointe une entrée versionnée (KB/D0NN/SHA) ; une « mémoire » sans ancre est une supposition.
4. **Compaction paramétrable** : le condensé historique du plan est « fait foi » ; les dérives de compaction sont des drifts consignés (types 15-23).
5. **Isolation par défaut** : contextes cloisonnés par Task ; le partage passe par artefacts (fichiers, KB), pas par mémoire résiduelle.
6. **Adaptation D017** : perte/oubli d'état → reconstitution depuis l'État Long (plan/worklog/SHA), jamais depuis l'invention.

### §1.5 Mémoire
Deux niveaux (pattern établi de l'écosystème) : **État Court** — la fenêtre de travail courante, volatile, compactable ; **État Long** — worklog/KB/answer key/plan/SHA, persistant et fait foi. La reprise après interruption ou compaction suit : pré-check B-11 → lecture plan (REPRISE) → worklog tail → vérification SHA. Références croisées : context-engineering (curation du contexte lu), graph-engineering (nœuds/arêtes versionnés comme mémoire relationnelle).

### §1.6 Cycle opérationnel
1. **Capturer** : à chaque étape terminée — worklog + preuves (S1-S3) ; décision → answer key.
2. **Indexer** : ancres B-14, SHA de référence, marqueurs d'état — la reprise doit être mécanique.
3. **Compacter** : en fin de tour/tâche longue — condensé fait foi + tombstones honnêtes pour les pertes avérées.
4. **Isoler** : prompts auto-contenus par sous-tâche ; artefacts partagés plutôt que contextes croisés.
5. **Récupérer** : requêtes ancrées (grep/arbitres/registre) au moment du besoin — just-à-temps, pas par loyauté envers l'historique.
6. **Auditer** : drifts de mémoire (B-21 tombstone, 15-23) consignés, jamais dissimulés.

### §1.7 Fondements académiques et veille (N34, 2026-09-21 — n°54)
Recherches N31/N34 vérifiées (preuves `tmp/n31-recherche/`) : **AgeMem** (arXiv 2026, 110+ citations) — opérations mémoire exposées comme outils : l'agent décide de façon autonome quoi/quand stocker, récupérer, mettre à jour ; **« Memory in the Age of AI Agents »** (survey, github.com) — taxonomie mémoire conversationnelle court/long terme ; **checkpointing & mémoire vectorielle** (Redis × LangGraph, juil. 2026) — persistance d'état et retrieval ; **panorama des frameworks mémoire** (machinelearningmastery, avr. 2026) — mémoire long terme, retrieval, gestion de contexte. Détail et sources : `references/fondements-academiques.md`.

## §2 — SPÉCIFICATION TECHNIQUE
Répliques de l'État Long : worklog (unique), KB (unique), answer key (unique), plan (unique) — les « copies » (miroir prompts-maîtres, canal download, archive) sont des répliques BYTE-IDENTIQUES vérifiées, pas des variantes. Toute divergence clone↔original est un écart-attendu documenté (B9/D016) ou un drift à corriger.

## §3 — RELATIONS (extrait de SHARED §3.1)
- `gen-plan` §1.9 — détenteur principal : impose l'État Long aux exécutions longues (E-série).
- `context-engineering` — le frère amont : ce que la mémoire retient, le contexte l'éclaire (budget partagé).
- `graph-engineering` — la mémoire relationnelle : nœuds/arêtes versionnés, requêtes ancrées.
- `loop-engineering` — les itérations longues appellent compaction + reprise mécanique.
- `fleet-engineering` — l'État Long de flotte est collectif (worklog/KB), jamais agent-local.

## §4 — CONVENTIONS
Kebab-case pour dossiers/fichiers ; semver strict ; tags `#token` ; `{{VARIABLE}}` pour les variables de contexte ; journalisation au worklog (`Task ID` + preuves) pour toute exécution réelle ; aucune fabrication de résultats (R3).

## §5 — ÉVALUATIONS ET DÉCLENCHEURS
`evals/trigger_evals.json` : 7 requêtes (5 positives, 2 contrôles négatifs) ; déclenchement sur les demandes mémoire/état/compaction/reprise ; seuil 0.5 (confirm 3 runs armé — QUOTA_OK). Baseline A2 : EN ATTENTE (`baseline-pending-n34.json`).

## §6 — TRAÇABILITÉ
- v1.0.0 (N34, 2026-09-21, session B12-r56) : matérialisation de la discipline approuvée n°54 (proposition N31 — AgeMem 110+ citations) ; sources N31 ; intégration gen-plan v3.15.0 §1.9 ; baseline en attente QUOTA (D017).

## §7 — RÉFÉRENCES
- `references/fondements-academiques.md` — sources vérifiées, signaux de veille, interactions.
- SHARED §7 (PROMPT-MAITRE-SHARED.md, corpus) — source de vérité des disciplines.
- gen-plan v3.15.0 §1.9 — routage autonome ; worklog.md — État Long opérant de la session.

## §8 — Registre d'assignation des disciplines (décentralisé du SHARED §7)
| Discipline | Détenteur principal | Fonction héritée |
|------------|--------------------|------------------|
| memory engineering | gen-plan (§1.9 — État Long obligatoire) | clone-chat (captation), correct-work (reprise), toute session longue |
