---
nom: script-mon-ecosysteme-infrastructure
version: 1.1.0
source: skills/script-mon-ecosysteme-infrastructure/SKILL.md
sha256_source: 4dbb0f077e24
genere: 2026-10-26 (phase P2 — directive 10 tâches, tâche 2)
usage: AUTONOME hors écosystème (dossier « Prompt Maitre » — non lu par l'orchestration)
---

> ⚠️ **MARQUEUR D'EXCLUSION (garde D010)** — CE DOSSIER N'EST PAS LU PAR L'ORCHESTRATION. Les dossiers « Prompt Maitre » sont des prompts autonomes à usage HORS écosystème : ils ne sont pas indexés au registre KB, ne sont mobilisés par aucun arbitre, et ne remplacent jamais la forme installée `skills/<skill>/` (source de vérité).

# Prompt Maître autonome — script-mon-ecosysteme-infrastructure (v1.1.0)

## Comment utiliser ce prompt (hors écosystème)

Ce document encapsule la compétence sous forme autonome : copiez-le intégralement
dans un assistant IA (ou ouvrez-le en référence directe) — aucune installation,
aucun registre, aucune dépendance à l'écosystème Knowledge d'origine n'est requise.
Les variables de l'écosystème d'origine ont été résolues en valeurs littérales ;
si des ressources `references/` accompagnent ce dossier, elles sont jointes au même
emplacement et le prompt y renvoie par leur chemin relatif. La version d'origine
(source de vérité) vit dans `skills/script-mon-ecosysteme-infrastructure/SKILL.md` du dépôt KNOWLEDGE.

---

## Le prompt

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

## §0 — Contexte Système (SHARED v1.7.14)

> Écosystème Knowledge : `skills/`=skills/ | `skills/KNOWLEDGE.md`=skills/KNOWLEDGE.md | `true`=true | `NORMAL`=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
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


---

## Ressources locales du dossier

Aucune ressource annexe — ce prompt est auto-suffisant.
