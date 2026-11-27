---
name: orchestration-disciplines
version: 1.0.0
category: ecosystem
language: fr
tags:
  - orchestration
  - disciplines
  - plan-actions
  - evolution
  - ecosystem
description: >
  Skill d'orchestration des disciplines d'ingénierie de prompts du plan d'actions.
  3 couches : C1 DÉCISION mécanique (routage-disciplines.py — plan de mobilisation
  des disciplines dérivé de la tâche normalisée, du déclencheur, du verdict de
  complexité É5-ROUTAGE et de l'état du plan), C2 EXÉCUTION (mobilisation des
  disciplines matérialisées aux étapes E1-E15 selon les tables sources —
  gen-plan references/disciplines-mobilisation.md = source unique R4, jamais
  dupliquées ici), C3 ÉVOLUTION (plans d'actions optimisés et évolutifs :
  nouvelles requêtes propriétaire via E13 règle d'or n°3 + re-injection MÉCANIQUE
  des résultats vérifiés des tâches parallèles aux checkpoints E11 et frontières
  de groupes — scan du disque KO-L003 : worklog, verdicts d'arbitres, livrables).
  Création Task 12 (session web-220878ed, directive trace 1a21e208f489f7f5 —
  « génère des skills ou des agents spécialisés pour que toutes ces disciplines
  s'exécutent et s'orchestrent »). Consommé par gen-plan (hook É5-DISCIPLINES
  v3.49.0) et mobilisable à toute exécution d'un plan d'actions multi-étapes.
dependencies:
  - skill: gen-plan
    version: ">=3.49.0"
    used_at: "É5-DISCIPLINES (hook consommateur), tables sources references/disciplines-mobilisation.md, verdict complexité É5-ROUTAGE"
  - skill: resource-monitor
    version: ">=1.0.0"
    used_at: "C3 évolution — verdict G-RES aux checkpoints E11 et frontières de groupes"
read_when:
  - Déclencher quand la demande concerne : orchestration des disciplines d'un plan d'actions, mobilisation des disciplines, plan d'actions évolutif, coordination de tâches parallèles liées
  - Déclencher si la demande mentionne : orchestration des disciplines, disciplines du plan, mobilisation des disciplines, plan évolutif, tâches parallèles, résultats vérifiés, re-injection
  - Déclencher à l'exécution de tout plan d'actions gen-plan (hook É5-DISCIPLINES) pour dériver la section « Orchestration des disciplines »
  - Ne pas déclencher pour une demande mono-étape sans plan d'actions (périmètre gen-plan §A requis)
---

## §A — DÉCLENCHEURS

- `orchestration des disciplines` — demande explicite d'organisation de la mobilisation des disciplines
- `disciplines du plan (d'actions)` / `mobilisation des disciplines` — sélection et gestion des disciplines d'un plan
- `plan d'actions évolutif` / `tâches parallèles` — protocole d'évolution C3 (nouvelles requêtes + résultats vérifiés d'autres tâches en cours)
- Hook gen-plan **É5-DISCIPLINES** (v3.49.0) : à E5/E7, gen-plan exécute `routage-disciplines.py` et dérive la section « Orchestration des disciplines » du plan
- Toute exécution d'un plan d'actions multi-groupes où la coordination des disciplines ou de tâches parallèles liées est en jeu

## §0 — Contexte Système (SHARED v1.7.46)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.
> Langue : FRANÇAIS exclusif pour tous les échanges avec le propriétaire (règle d'or n°6 gen-plan — directive 2026-10-31, renforcée 2026-11-06) : dès le PREMIER mot de toute session ou reprise, la langue d'un message, d'un résumé de continuation ou d'un canal ne dérive JAMAIS la réponse ; toute dérive est corrigée immédiatement.
> Référence canonique skill/agent (directive propriétaire 2026-11-07 — SHARED §0/§1.2) : toute référence à « mon skill X »/« mon agent X » désigne la forme installée à la racine `skills/X/SKILL.md`, JAMAIS le prompt maître du corpus `@mon-ecosysteme/` — les PMs sont des spécifications générées mécaniquement (KO-L004), les skills installés sont les formes exécutables.

## §1 — Spécification fonctionnelle : la méthode 3 couches

### §1.1 C1 — DÉCISION mécanique (qui, quand)

`scripts/routage-disciplines.py` dérive le **plan de mobilisation** des disciplines à partir de 4 entrées : (1) la tâche normalisée (PROMPT-GATEWAY si complexe), (2) le déclencheur gen-plan (NULL / step / step-ok / orchestre / generate / correct-work / reprise E1-RES), (3) le verdict de complexité É5-ROUTAGE (SIMPLE / COMPLEXE ≥ 2/5), (4) l'état du plan (groupes restants, tâches parallèles liées déclarées). Sortie JSON : socle commun + mobilisation par étape E1-E15 + extensions de complexité + protocole d'évolution. La décision est MÉCANIQUE et idempotente — l'arbitre `--check-coherence` vérifie que chaque discipline recommandée existe comme forme installée (dérivation depuis `skills/`, KO-L003) et que la matrice embarquée reste synchronisée avec les tables sources.

### §1.2 C2 — EXÉCUTION (comment les disciplines s'exécutent)

Les disciplines s'exécutent par leurs **formes matérialisées** (`skills/<discipline>/`, déclenchement automatique SHARED §7) aux étapes prescrites par les **tables sources** : `gen-plan/references/disciplines-mobilisation.md` (tables E1-E8, matérialisations n°54/n°55, mobilisation par déclencheur, hook continu E9-E14) — SOURCE UNIQUE R4 : le présent skill ne duplique JAMAIS ces tables, il pointe vers elles et orchestre leur application. Le socle commun (context-engineering, loop-engineering, graph-engineering, harness-engineering + méthode-mère prompt-engineering) s'applique à tout plan ; les extensions n°54 (spec-driven-development, memory-engineering, fleet-engineering), n°55 (refactoring-engineering + refactoring-test + refactor-guard) et n°56 (agent-engineering) se mobilisent selon les tables et le verdict de complexité (agent-engineering uniquement sur délégation d'agents — porte gen-plan §1.17).

### §1.3 C3 — ÉVOLUTION (plans optimisés et évolutifs)

Le protocole d'évolution couvre les DEUX sources de changement d'un plan en vol :

1. **Nouvelle requête propriétaire** → règle d'or n°3 gen-plan : « intègre dans le plan d'actions » = extension E13 en place (jamais réécriture destructrice R2) ; « met à jour » = re-génération d'un NOUVEAU plan consolidé (statuts dérivés du disque, restes-à-faire re-planifiés, re-estimation #token, answer key re-numérotée).
2. **Résultats vérifiés de tâches parallèles liées** → aux checkpoints E11 et à CHAQUE frontière de groupe : scan MÉCANIQUE du disque (KO-L003 — jamais la mémoire : worklog des suites concurrentes, verdicts d'arbitres JSON, empreintes de livrables) ; si un résultat vérifié touche le périmètre du plan courant → ajustement E13 + re-validation E8 + PLAN-AFFICHE rejoué + décision journalisée. Les tâches parallèles non liées (périmètres disjoints) sont ignorées — le scan croise les périmètres déclarés du plan.

**Garde-fous d'évolution** : verdict G-RES re-collecté à chaque checkpoint (PRESSION → ECO, CRITIQUE → série/PAUSE — hook continu E9-E14) ; FAIL découvert → règle FAIL-CLOSE §1.18 gen-plan (correction avant fermeture d'étape, journal-fails.md) ; secret exposé → KO-L009 ; toute adaptation journalisée (règle d'or n°1).

### §1.4 Ce que ce skill N'EST PAS (garde anti-duplication R4)

- PAS une copie des tables de mobilisation (source unique : gen-plan `references/disciplines-mobilisation.md` + SHARED §7)
- PAS un remplacement de gen-plan (le plan d'actions, ses modes et ses étapes E1-E15 demeurent la propriété de gen-plan — ce skill est une COUCHE d'orchestration consommée par le hook É5-DISCIPLINES)
- PAS un arbitre (les verdicts demeurent ceux de correct-work et des arbitres mécaniques — ce skill produit des DÉCISIONS de mobilisation, jamais des verdicts de conformité)

## §2 — Spécification technique

### §2.1 Structure

```
skills/orchestration-disciplines/
├── SKILL.md                          # la méthode 3 couches (présent fichier)
├── scripts/
│   └── routage-disciplines.py        # C1 décision mécanique (--json, --check-coherence, --selftest)
└── evals/
    └── trigger_evals.json            # 6 positifs / 4 négatifs
```

### §2.2 Interface du script

`python3 skills/orchestration-disciplines/scripts/routage-disciplines.py --tache "<demande>" [--declencheur step] [--complexite COMPLEXE] [--etat-plan <chemin>] [--json]` — sortie : plan de mobilisation JSON compact (socle, mobilisation par étape, extensions, protocole d'évolution, source déclarée). `--check-coherence` : vérifie l'existence des disciplines recommandées comme formes installées + la synchronisation de la matrice avec les tables sources. Codes retour : 0 OK · 1 incohérence détectée · 2 usage invalide. Python stdlib uniquement, idempotent ×2.

## §3 — Relations

| Avec | Nature | Détails |
|------|--------|---------|
| gen-plan | Consommateur (hook É5-DISCIPLINES v3.49.0) + source des tables | gen-plan exécute routage-disciplines.py à E5/E7 et dérive la section « Orchestration des disciplines » du plan ; tables sources `references/disciplines-mobilisation.md` (R4 — jamais dupliquées ici) |
| disciplines matérialisées (context/loop/graph/harness + n°54 spec-driven/memory/fleet + n°55 refactoring-engineering/refactoring-test/refactor-guard + n°56 agent-engineering) | Orchestration | Mobilisées selon les tables sources aux étapes prescrites — formes installées à déclenchement automatique (SHARED §7) |
| resource-monitor | Mobilisation C3 | Verdict G-RES aux checkpoints E11 et frontières de groupes (bascule ECO/série/PAUSE) |
| correct-work | Frontière de responsabilité | Les verdicts de conformité demeurent ceux de correct-work et des arbitres — ce skill ne produit que des décisions de mobilisation |
| PM SHARED | Socle | §0 contexte système, §7 registre des disciplines (source de vérité des définitions) |

## §4 — Grille #token

- Décision mécanique (routage-disciplines.py) : ~300 #token par plan (sortie JSON 1-2 Kio, < 1 s)
- Application de la couche C3 en vol : ~500-1500 #token par frontière de groupe touchée (scan disque + ajustement E13 éventuel)
- Le catalogue des tables N'EST PAS incrusté dans le corps (R4 + poids maîtrisé)

## §5 — Conventions et journal des versions

- Nommage kebab-case, semver, #token, {{VARIABLE}} (SHARED §1.2) ; Python stdlib uniquement (N3) ; idempotence R1-R6 (§1.8 gen-plan).
- **v1.0.0 (2026-11-28, web-220878ed — Task 12, directive trace 1a21e208f489f7f5)** : création — méthode 3 couches (C1 décision mécanique / C2 exécution par les disciplines matérialisées selon les tables sources R4 / C3 évolution : E13 + re-injection mécanique des résultats vérifiés des tâches parallèles aux checkpoints E11 et frontières de groupes) ; `scripts/routage-disciplines.py` (matrice de décision embarquée + --check-coherence + selftest, stdlib, idempotent ×2) ; evals 6 positifs / 4 négatifs ; KB 57ᵉ entrée ; inscription ECO_SKILLS integrity. Consommé par gen-plan v3.49.0 (hook É5-DISCIPLINES).
