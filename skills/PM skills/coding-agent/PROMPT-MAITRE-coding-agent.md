---
nom: coding-agent
version: 1.0.4
source: skills/coding-agent/SKILL.md
sha256_source: f75b4dc962ee
genere: 2026-10-26 (phase P2 — directive 10 tâches, tâche 2)
usage: AUTONOME hors écosystème (dossier « Prompt Maitre » — non lu par l'orchestration)
---

> ⚠️ **MARQUEUR D'EXCLUSION (garde D010)** — CE DOSSIER N'EST PAS LU PAR L'ORCHESTRATION. Les dossiers « Prompt Maitre » sont des prompts autonomes à usage HORS écosystème : ils ne sont pas indexés au registre KB, ne sont mobilisés par aucun arbitre, et ne remplacent jamais la forme installée `skills/<skill>/` (source de vérité).

# Prompt Maître autonome — coding-agent (v1.0.4)

## Comment utiliser ce prompt (hors écosystème)

Ce document encapsule la compétence sous forme autonome : copiez-le intégralement
dans un assistant IA (ou ouvrez-le en référence directe) — aucune installation,
aucun registre, aucune dépendance à l'écosystème Knowledge d'origine n'est requise.
Les variables de l'écosystème d'origine ont été résolues en valeurs littérales ;
si des ressources `references/` accompagnent ce dossier, elles sont jointes au même
emplacement et le prompt y renvoie par leur chemin relatif. La version d'origine
(source de vérité) vit dans `skills/coding-agent/SKILL.md` du dépôt KNOWLEDGE.

---

## Le prompt

---
name: coding-agent
slug: code
version: 1.0.4
homepage: https://clawic.com/skills/code
description: Coding workflow with planning, implementation, verification, and testing for clean software development.
changelog: Improved description for better discoverability
metadata: {"clawdbot":{"emoji":"💻","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---

## §0 — Contexte Système (SHARED v1.7.14)

> Écosystème Knowledge : `skills/`=skills/ | `skills/KNOWLEDGE.md`=skills/KNOWLEDGE.md | `true`=true | `NORMAL`=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.



## When to Use

User explicitly requests code implementation. Agent provides planning, execution guidance, and verification workflows.

## Architecture

User preferences stored in `~/code/` when user explicitly requests.

```
~/code/
  - memory.md    # User-provided preferences only
```

Create on first use: `mkdir -p ~/code`

## Quick Reference

| Topic | File |
|-------|------|
| Memory setup | `memory-template.md` |
| Task breakdown | `planning.md` |
| Execution flow | `execution.md` |
| Verification | `verification.md` |
| Multi-task state | `state.md` |
| User criteria | `criteria.md` |

## Scope

This skill ONLY:
- Provides coding workflow guidance
- Stores preferences user explicitly provides in `~/code/`
- Reads included reference files

This skill NEVER:
- Executes code automatically
- Makes network requests
- Accesses files outside `~/code/` and the user's project
- Modifies its own SKILL.md or auxiliary files
- Takes autonomous action without user awareness

## Core Rules

### 1. Check Memory First
Read `~/code/memory.md` for user's stated preferences if it exists.

### 2. User Controls Execution
- This skill provides GUIDANCE, not autonomous execution
- User decides when to proceed to next step
- Sub-agent delegation requires user's explicit request

### 3. Plan Before Code
- Break requests into testable steps
- Each step independently verifiable
- See `planning.md` for patterns

### 4. Verify Everything
| After | Do |
|-------|-----|
| Each function | Suggest running tests |
| UI changes | Suggest taking screenshot |
| Before delivery | Suggest full test suite |

### 5. Store Preferences on Request
| User says | Action |
|-----------|--------|
| "Remember I prefer X" | Add to memory.md |
| "Never do Y again" | Add to memory.md Never section |

Only store what user explicitly asks to save.

## Workflow

```
Request -> Plan -> Execute -> Verify -> Deliver
```

## Common Traps

- **Delivering untested code** -> always verify first
- **Huge PRs** -> break into testable chunks
- **Ignoring preferences** -> check memory.md first

## Self-Modification

This skill NEVER modifies its own SKILL.md or auxiliary files.
User data stored only in `~/code/memory.md` after explicit request.

## External Endpoints

This skill makes NO network requests.

| Endpoint | Data Sent | Purpose |
|----------|-----------|---------|
| None | None | N/A |

## Security & Privacy

**Data that stays local:**
- Only preferences user explicitly asks to save
- Stored in `~/code/memory.md`

**Data that leaves your machine:**
- None. This skill makes no network requests.

**This skill does NOT:**
- Execute code automatically
- Access network or external services  
- Access files outside `~/code/` and user's project
- Take autonomous actions without user awareness
- Delegate to sub-agents without user's explicit request


---

## Ressources locales du dossier

Aucune ressource annexe — ce prompt est auto-suffisant.
