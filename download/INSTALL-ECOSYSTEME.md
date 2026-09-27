PROMPT MAÎTRE — Installation complète de l'écosystème
Version : 1.0.0
Dépend : CONTEXTE SYSTÈME (embarqué ci-dessous)
Ordre d'exécution et critères de passage : voir PROMPT-MAITRE-INSTALL-ECOSYSTEME.md

---
## ⚙️ CONTEXTE SYSTÈME (Extrait SHARED v1.5.2)
> **INSTRUCTION** : Ce bloc remplace la dépendance de lecture externe.

### Règle Zéro (§0)
L'écosystème Knowledge est un ensemble de 80 skills conçus pour un assistant IA.

### Variables d'installation (§1.1)
| Variable | Défaut | Description |
|----------|--------|-------------|
| `{{SKILLS_ROOT}}` | `skills/` | Racine |
| `{{KB_PATH}}` | `skills/KNOWLEDGE.md` | Registre KB |

### Conventions de nommage (§1.2)
- **Répertoires** : kebab-case
- **Fichiers** : kebab-case avec extension
- **Versions** : format semver

---
-------|--------|-------------|
| `{{SKILLS_ROOT}}` | `skills/` | Racine du répertoire des skills |
| `{{KB_PATH}}` | `skills/KNOWLEDGE.md` | Chemin vers le registre KB |
| `{{KB_ENABLED}}` | `true` | Activation/désactivation du registre KB |
| `{{PROFILE_DEFAULT}}` | `NORMAL` | Profil ressource par défaut |

### Conventions de nommage (§1.2)
- **Répertoires** : kebab-case (`gen-plan`, `correct-work`). Exception : `@mon-ecosysteme/` (dossier des prompts maîtres).
- **Fichiers** : kebab-case avec extension (`SKILL.md`, `etapes-detaillees.md`).
- **Versions** : format semver (`3.11.0`, `2.5.1`).
- **Tags** : préfixe `#` pour les tokens (`#token 3500`).
- **Variables** : double accolades (`{{SKILLS_ROOT}}`).

---


§1.2 Périmètre : 26 fichiers répartis sur 4 zones.

§1.3 Les 8 phases P0-P7.
Note P4 : les SKILL.md + références des 4 skills sont créés en
suivant le §5 de chaque prompt maître (ou via gen-plan). Le
bootstrap install-ecosystem.py couvre P0-P3, P5-P7.

§9.1 KNOWLEDGE.md (14 entrées)
## gen-plan v3.10.0
## correct-work v2.5.1
## clone-chat v2.0.0
## skills-inventory v1.0.0
## skill-creator v1.0.0
## agent-creator v1.0.0
## script-mon-ecosysteme-infrastructure v1.0.0
## install-ecosystem v1.0.0
## prompt-engineering v1.0.1
## verify-by-sha v1.0.0
## context-engineering v1.0.1
## loop-engineering v1.0.1
## graph-engineering v1.0.1
## harness-engineering v1.0.1
- **Category** : ecosystem (4 matérialisations skills des disciplines d'exécution, socle SHARED §7 — session A12)
- **Utilisé par** : gen-plan (couche disciplines), sessions d'ingénierie
- **Matérialisé** : 2026-09-07 (forme installée : `<discipline>/` — SKILL.md + evals/evals.json + evals/trigger_evals.json, déclenchement automatique ; matérialisations agent `_disciplines/` retirées, SHA prouvés)
