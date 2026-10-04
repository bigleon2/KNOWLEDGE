---
name: script-mon-ecosysteme-infrastructure
version: 1.1.0
category: ecosystem
language: fr
tags:
  - infrastructure
  - generation-fichiers
  - contexte-systeme
  - ecosystem
description: >
  Skill d'infrastructure de génération de fichiers de l'écosystème Knowledge.
  Injection automatique du Contexte Système à 3 niveaux, gardes d'intégrité
  et conventions de déploiement des artefacts (règles INFRA-1..INFRA-3).
dependencies:
  - skill: skill-creator
    version: ">=1.0.0"
    used_at: "conventions structurelles"
read_when:
  - Déclencher quand la demande concerne : skill d'infrastructure de génération de fichiers de l'écosystème Knowledge
  - Déclencher si la demande mentionne : infra, skill, infrastructure
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

## §0 — Contexte Système (SHARED v1.6.4)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (exception)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.

## §1 — Spécification fonctionnelle

Skill d'infrastructure (pas un skill métier) : il génère et déploie les fichiers de l'écosystème (scripts d'arbitres, blocs de Contexte Système, artefacts d'installation) en appliquant l'injection automatique des 3 niveaux de Contexte Système.

### INFRA-1 (injection systématique)
Tout fichier généré par l'infrastructure embarque le Contexte Système à son niveau :
- **Niveau 1** — prompts maîtres (`skills/@mon-ecosysteme/PROMPT-MAITRE-*.md`) : bloc complet après l'en-tête ;
- **Niveau 2** — SKILL.md et fichiers `.agent` : bloc §0 compact après le frontmatter/titre ;
- **Niveau 3** — scripts Python (`scripts/*.py`) : docstring après le shebang.

### INFRA-2 (intégrité et idempotence)
La génération est idempotente (R1 : vérifier présence avant insertion ; R4 : ne jamais dupliquer) ; les remplacements passent par `scripts/sync-context-block.py`, les propagations par `scripts/propagate-context.py` ; toute divergence est détectée par `scripts/verify-cross.py --check-context`.

### INFRA-3 (enregistrement et traçabilité)
Tout artefact généré est enregistré dans `KNOWLEDGE.md` (template : `skills-inventory` §2.1), journalisé au worklog (format : `agent-creator` §6.1) et couvert par au moins un arbitre (gardes anti-boucle : SHARED §4.4).

## §2 — Spécification technique

- Stack : Python 3 (scripts), Markdown, YAML
- Emplacements : `scripts/` (arbitres et bootstrap), `skills/@mon-ecosysteme/` (prompts maîtres), `config.json` (configuration centralisée)
- Validation : `verify-cross.py --check-context` (score 100 %), `verify-correct-work.py` (16 checks)

## §3 — Relations

| Avec | Nature | Détails |
|------|--------|---------|
| install-ecosystem | utilise cette infrastructure | Phases P6-P7 du bootstrap (SHARED §3.1) |
| skill-creator | conventions | Conventions structurelles, >= v1.0.0 |
| correct-work | vérifié par | Conformité des artefacts générés, >= v2.4.0 |
| knowledge.md | enregistrement | Toute matérialisation est inscrite au registre |

## §4 — Conventions

Nommage kebab-case, versions semver, tags `#token`, variables `{{VARIABLE}}` (SHARED §1.2 — pointeur décentralisé : `skill-creator` §2).

---

## Baseline A2 — statut de mesure
> **Baseline A2 (Task 21 P3/F3, 2026-10-03)** : MESURÉE 2 voies (voie mécanique SHARED §7 v2 + voie L 3 runs réels) — score baseline 6/7 (nulls : 2) ; détail par cas : `scripts/baseline-a2-all-report.json` ; cas structurels consignés au registre KB (décision Task 21) ; re-mesure idempotente `--skip-done` armée pour les nulls 429 restants.
