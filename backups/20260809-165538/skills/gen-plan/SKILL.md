---
name: gen-plan
version: 3.6.1
category: ecosystem
language: fr
tags:
  - planning
  - task-management
  - token-estimation
  - auto-calibration
  - ecosystem
description: >
  Skill de planification de tâches pour assistant IA.
  4 modes (Planification, Exécution, Surveillance, Adaptation),
  15 étapes (E1-E15), 3 profils ressource (NORMAL/ECO/VIEUX PC),
  tagging #token, snippets, scripts Python uniquement.
dependencies:
  - skill: correct-work
    version: ">=2.4.0"
    used_at: "E1, E8 hook"
  - skill: clone-chat
    version: ">=2.0.0"
    used_at: "E4, E15"
    optional: true
  - skill: skills-inventory
    version: ">=1.0.0"
    used_at: "E5"
---

## §0 — Règle zéro

Écosystème Knowledge : 78 skills auto-contenus sous `skills/`, versionnés semver, avec registre KB (`skills/KNOWLEDGE.md`) comme source de vérité. Dépendances inter-skills déclarées en YAML, cross-references bidirectionnelles maintenues.

---

## §1 — Spécification fonctionnelle

### §1.1 Les 4 modes

| Mode | Nom | Description |
|------|-----|-------------|
| M1 | **Planification** | Analyse, classification, estimation, création du plan |
| M2 | **Exécution** | Passage à l'action selon le plan |
| M3 | **Surveillance** | Monitoring temps réel, détection d'écarts |
| M4 | **Adaptation** | Ajustement du plan en cas de dérive |

### §1.2 Les 15 étapes (E1-E15)

| Étape | Nom | Mode |
|-------|------|------|
| E1 | Analyse de la demande | M1 |
| E2 | Inventaire des ressources | M1 |
| E3 | Classification du type de tâche (Type 1-4) | M1 |
| E4 | Estimation #token | M1 |
| E5 | Sélection des skills | M1 |
| E6 | Profilage ressource (NORMAL/ECO/VIEUX PC) | M1 |
| E7 | Création du plan | M1 |
| E8 | Validation du plan | M1 |
| E9 | Lancement de l'exécution | M2 |
| E10 | Suivi d'étape | M2/M3 |
| E11 | Checkpoint intermédiaire | M3 |
| E12 | Détection d'écart | M3 |
| E13 | Ajustement | M4 |
| E14 | Finalisation | M2 |
| E15 | Bilan et auto-calibration | M1/M4 |

> Détail complet de chaque étape : `references/etapes-detaillees.md`

### §1.3 Normes

- **N1 — Tagging #token** : chaque étape et skill reçoit un tag `#token` avec le coût estimé. Grille auto-calibrée après exécutions.
- **N2 — Snippets** : snippets de code réutilisables générés pendant l'exécution, tagués et versionnés.
- **N3 — Python uniquement** : tous les scripts générés doivent être en Python (aucun bash/sh/powershell).

### §1.4 Philosophie clés

1. **Read before planning** — Toujours lire le projet avant de planifier.
2. **Performance-driven sélection** — Le choix skill/agent est dicté par le gain de performance.
3. **Skills can launch specialized agents** — Modèle à deux couches : Skill → Agent Spécialisé.
4. **Serial exécution by DEFAULT** — Tâches UNE À LA UNE. Parallélisme INTERDIT sauf demande explicite.
5. **Visible progress** — L'utilisateur sait toujours où on en est.
6. **CoT + Chaining avec auto-correction** — Raisonnement structuré avant chaque action.
7. **Lecture bloc par bloc** — Fichiers > 500 lignes : lire par blocs successifs (limit/offset), produire une synthèse intermédiaire entre chaque bloc. Ne jamais lire un fichier > 500 lignes d'un seul coup. Voir `references/profils-ressource.md` (VIEUX PC règle 4 : troncature 500 lignes).
8. **Downgrade irréversible** — Le profil ressource ne remonte jamais automatiquement.

---

## §2 — Spécification technique

### §2.1 Stack

- **Langage** : Python (scripts), Markdown (documentation), YAML (frontmatter)
- **Environnement** : `skills/gen-plan/`
- **Pas de dépendance externe** (sauf intégration KB si activée)

### §2.2 Structure

```
skills/gen-plan/
├── SKILL.md                          # Skill opérationnel compact (~180 lignes)
├── references/
│   ├── etapes-detaillees.md          # Détail des 15 étapes
│   ├── grille-token.md               # Grille de calibration #token
│   ├── classification-types.md       # Routage Type 1-4
│   ├── profils-ressource.md          # NORMAL / ECO / VIEUX PC
│   └── guide-selection-agent-skill.md # Arbre de décision + tableau
└── evals/
    └── evals.json                    # Cas de test d'évaluation
```

### §2.3 Auto-calibration E15

| Écart estimé vs réel | Action |
|----------------------|--------|
| 0-20% | Aucune action |
| 20-35% | Ajustement de la grille (paramétrage fin) |
| >35% | Recalibration complète |

### §2.4 Profils ressource

| Profil | Contexte | Règles clés |
|--------|----------|-------------|
| **NORMAL** | Par défaut | 15 étapes, tous les skills, surveillance complète |
| **ECO** | < 5 sessions, #token < 3500 | Étapes réduites, 1 checkpoint, pas de matrice dynamique KB |
| **VIEUX PC** | Matériel limité | Règles ECO + scripts < 100 lignes, pas de graphiques |

**Signaux de pression** (détectés à E2) :
- Espace disque < 5 Go (critique < 3 Go), Timeout 2+ consécutifs (critique 4+), Budget tokens > 80% (critique > 95%)
- **1 signal pression** → ECO. **2+ signaux** ou **1 critique** → VIEUX PC.

**Filtrage #token par profil** : NORMAL = aucun filtre. ECO = exclut > 8000 #token. VIEUX PC = exclut > 5000 #token.

> Détail complet : `references/profils-ressource.md`

### §2.5 Intégration KB

Si activé : consultation de `skills/KNOWLEDGE.md`, scan du registre pour identifier les skills pertinents (Protocole de Découverte SHARED §2.3), enrichissement à E15.

---

## §3 — Relations

| Avec | Nature | Détails |
|------|--------|--------|
| correct-work | Invocation à E1 | Validation du plan initial, version >= v2.4.0 |
| clone-chat | Calibration + archivage | E4, E15, optionnel, version >= v2.0.0 |
| skills-inventory | Consultation à E5 | Sélection des skills, version >= v1.0.0 |
| knowledge.md | Enrichissement à E15 | Mise à jour registre et calibration |

---

## §4 — Grille #token

Résumé des plages clés (voir `references/grille-token.md` pour la grille complète) :

- **Planification E1-E2** : 800-1500 #token
- **Exécution simple (1 skill)** : 2000-5000 #token
- **Exécution complexe (4+ skills)** : 10000-20000 #token
- **Coefficients** : 0.8x (faible) → 1.5x (critique), ECO 0.7x, VIEUX PC 0.5x

---

## §5 — Conventions

### §5.1 Nommage

- Répertoires et fichiers : kebab-case (`gen-plan`, `etapes-detaillees.md`)
- Versions : semver (`3.6.1`)
- Tags : préfixe `#` (`#token 3500`)
- Variables : double accolades (`{{SKILLS_ROOT}}`)

### §5.2 Python uniquement (N3)

Tous les scripts générés en Python. Aucun script shell (bash, sh, powershell). Portabilité cross-platform garantie.

### §5.3 Tagging #token (N1)

Chaque étape du plan et chaque skill utilisé reçoit un tag `#token` indiquant le coût estimé. La grille est auto-calibrée à E15.
