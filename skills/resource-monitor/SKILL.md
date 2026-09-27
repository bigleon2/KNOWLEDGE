---
name: resource-monitor
version: 1.0.0
category: ecosystem
language: fr
tags:
  - monitoring
  - ressources
  - parallelisme
  - adaptation
  - ecosystem
description: >
  Surveillance permanente de la consommation des ressources de l'écosystème.
  Collecte en continu les indicateurs critiques (budget #token, timeouts consécutifs,
  quota API 429, espace disque, mémoire, stagnation de tâche) et émet un verdict
  machine-à-machine : OK / PRESSION / CRITIQUE avec une recommandation de mode
  d'exécution (PARALLELE / PARALLELE_REDUIT / SERIE / PAUSE). Détenteur de la
  fonction de surveillance permanente (gen-plan §1.14) ; consommé par gen-plan
  à E6 (profilage) et en continu à E9-E14 (exécution/surveillance), et par toute
  tâche longue qui a besoin d'un signal de pression exploitable.
dependencies: []
---

## §0 — Contexte Système (SHARED v1.6.0)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.

## §1 — Spécification fonctionnelle

### §1.1 Mission

Le budget d'attention et les ressources matérielles sont FINIS. La surveillance permanente consiste à collecter les indicateurs de consommation AVANT qu'une tâche ne consomme tout son budget — pas après. resource-monitor est le détenteur de cette fonction : il produit un verdict structuré, exploitable par un agent ou par gen-plan, sans décision humaine requise.

### §1.2 Les 4 fonctions

| Fonction | Nom | Description |
|----------|-----|-------------|
| F1 | **Collecte** | Lecture des indicateurs système et d'exécution (disque, mémoire, charge, budget #token, timeouts, quota API, stagnation) |
| F2 | **Seuils** | Application des seuils d'alerte (hérités de gen-plan §2.4, étendus v3.16.0) sur chaque indicateur |
| F3 | **Verdict** | Agrégation en verdict unique : OK / PRESSION / CRITIQUE |
| F4 | **Recommandation** | Recommandation de mode d'exécution : PARALLELE / PARALLELE_REDUIT / SERIE / PAUSE + causes listées |

### §1.3 Indicateurs surveillés et seuils

| Indicateur | Source | Seuil PRESSION | Seuil CRITIQUE |
|------------|--------|----------------|----------------|
| Espace disque | `os.statvfs` | < 5 Go | < 3 Go |
| Mémoire disponible | `/proc/meminfo` | < 1,5 Go | < 700 Mo |
| Charge système (loadavg 1 min) | `/proc/loadavg` | > 4,0 | > 8,0 |
| Budget #token consommé | paramètre `--used-tokens` / `--budget-tokens` | > 80 % | > 95 % |
| Timeouts consécutifs | fichier d'état (`--state-file`) | >= 2 | >= 4 |
| Quota API (erreurs 429) | fichier d'état | 1 erreur | >= 2 erreurs |
| Stagnation de tâche | fichier d'état (dernière progression) | > 15 min | > 40 min |

> Signaux de pression d'origine : gen-plan §2.4 (disque, timeouts, budget tokens). La v1.0.0 de resource-monitor étend la surveillance à la mémoire, à la charge, au quota API et à la stagnation de tâche (v3.16.0, demande du propriétaire).

### §1.4 Verdicts et recommandations

| Verdict | Condition | Recommandation |
|---------|-----------|----------------|
| **OK** | Aucun seuil franchi | `mode: PARALLELE` — largeur de parallélisme pleine (défaut gen-plan §1.13) |
| **PRESSION** | >= 1 seuil PRESSION (non critique) | `mode: PARALLELE_REDUIT` — largeur réduite (2 tâches max) ou bascule série des tâches les plus lourdes |
| **CRITIQUE** | >= 1 seuil CRITIQUE ou 2+ seuils PRESSION | `mode: SERIE` — exécution sérielle stricte, tâche la plus légère d'abord ; ou `PAUSE` si pausable |

La recommandation est un AVIS structuré : la décision de bascule reste à gen-plan (§1.13, E9-E14), qui la journalise au worklog (règle d'or n°1).

### §1.5 Fichier d'état

Le collecteur est sans état global : les indicateurs qui ne sont pas mesurables en un instant T (timeouts consécutifs, erreurs 429, dernière progression) sont lus dans un fichier d'état JSON passé en argument `--state-file`. Chaque exécution appelante (gen-plan, agent, tâche) met à jour ce fichier — format :

```json
{
  "timeouts_consecutifs": 0,
  "erreurs_429": 0,
  "derniere_progression_epoch": 0,
  "tache_courante": ""
}
```

## §2 — Spécification technique

### §2.1 Stack

- **Langage** : Python 3 (stdlib uniquement — aucun paquet externe)
- **Environnement** : `skills/resource-monitor/`
- **Sortie** : JSON sur stdout (verdict machine-à-machine) ; code retour 0 (OK), 1 (PRESSION), 2 (CRITIQUE)

### §2.2 Structure

```
skills/resource-monitor/
├── SKILL.md              # Skill opérationnel compact
├── scripts/
│   └── monitor.py        # Collecteur F1-F4 (stdlib, JSON stdout)
└── evals/
    └── evals.json        # Cas de test d'évaluation
```

### §2.3 Usage du collecteur

```bash
python -m skills.resource-monitor.scripts.monitor \
  --budget-tokens 3500 --used-tokens 900 \
  --state-file /home/z/my-project/tmp/resource-monitor-state.json
```

- Sans `--state-file`, les indicateurs d'état sont traités à zéro.
- Sans `--budget-tokens`, l'indicateur budget est ignoré.
- La sortie JSON contient : `verdict`, `mode_recommande`, `causes[]`, `indicateurs{}`.

## §3 — Relations

| Avec | Nature | Détails |
|------|--------|---------|
| gen-plan | Consommé par | E6 (profilage initial) + hook continu E9-E14 (v3.16.0 §1.14) ; les signaux de pression §1.3 étendent gen-plan §2.4 |
| harness-engineering | Fonction héritée | La surveillance permanente est une extension du harnais d'exécution (profils ressource, hooks) — source de vérité : SHARED §7 |
| loop-engineering | Complément | La collecte s'insère dans la boucle E10-E13 (surveillance → écart → ajustement) |

> Provenance : matérialisation v1.0.0 (session B13-r1, 2026-09-26) de la demande du propriétaire « intégrer de surveiller la consommation des ressources en permanence (crée un skill ou un agent dédié) » — réalisée en skill (convention gen-plan §1.9 : matérialisation en skill à déclenchement automatique, pas en agent).
