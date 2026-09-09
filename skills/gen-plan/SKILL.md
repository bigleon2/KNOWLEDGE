---
name: gen-plan
version: 3.11.0
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
  15 étapes (E1-E15), classification Type 1-4 (documents, analyse, développement web, data), 3 profils ressource (NORMAL/ECO/VIEUX PC),
  tagging #token, snippets, scripts Python uniquement,
  règles d'or d'adaptation autonome, disciplines d'ingénierie de prompts
dependencies:
  - skill: correct-work
    version: ">=2.4.0"
    used_at: "E1, E8 hook, contrôle par phase"
  - skill: clone-chat
    version: ">=2.0.0"
    used_at: "E4, E15"
    optional: true
  - skill: skills-inventory
    version: ">=1.0.0"
    used_at: "E5"
---

## §0 — Règle zéro

Écosystème Knowledge : skills auto-contenus sous `{{SKILLS_ROOT}}`, versionnés semver, avec registre KB (`{{KB_PATH}}`) comme source de vérité (SHARED §0). Dépendances inter-skills déclarées en YAML, cross-references bidirectionnelles maintenues. Conventions de nommage SHARED §1.2 : répertoires kebab-case, sections préfixées `§`, tags budget préfixés `#`.

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

### §1.5 Règles d'or (PM v3.7.0 §1.8)

**Règle d'or n°1 — Adaptation autonome** : tout blocage (timeout répété, ressource épuisée, fichier absent, wipe inter-sessions, dépendance indisponible, sortie d'outil perdue) est traité comme un signal d'adaptation, jamais comme un arrêt implicite. Le contournement reste conforme aux conventions (SHARED §1) et à la philosophie §1.4 ; chaque adaptation est journalisée au worklog (cause, solution retenue, coût #token) ; l'objectif final ne change pas, seuls les moyens s'ajustent — si l'objectif devient inatteignable, la pause est explicite et motivée.


**Règle d'or n°2 — Régénération du plan après installation d'un écosystème** (PM v3.11.0 §1.8) : dès qu'un nouvel écosystème est installé, le plan d'actions actuel est régénéré de façon cohérente via le nouveau skill gen-plan — modes, étapes, règles d'or et hooks réalignés sur la version installée, tags #token recalculés si la grille a évolué, régénération journalisée au worklog ; l'objectif final est inchangé (non-régression R2 des étapes terminées).

**Règle d'or n°3 — Mise à jour du plan à chaque nouvelle demande** (PM v3.11.0 §1.8) : toute nouvelle demande utilisateur pendant l'exécution d'un plan déclenche la mise à jour cohérente du plan d'actions actuel via gen-plan (E13) — demandes intégrées comme étapes/priorités, ré-estimation #token des étapes affectées, re-validation E8 si le périmètre change matériellement, journalisation au worklog ; extension du plan, jamais réécriture destructrice (R2).

### §1.6 Disciplines d'ingénierie de prompts (PM v3.11.0 §1.9)

| Discipline | Mécanisme gen-plan |
|------------|--------------------|
| **Context engineering** | Socle SHARED lu en premier ; lecture bloc par bloc avec synthèses intermédiaires |
| **Loop engineering** | Boucle E10-E13 (exécution → surveillance → écart → ajustement) ; auto-calibration E15 |
| **Graph engineering** | Registre KB = graphe de relations bidirectionnelles versionnées ; matrice agent × skill |
| **Harness engineering** | Profils ressource + signaux de pression ; hook E8 correct-work + contrôle par phase (E9-E14) ; worklog structuré |

L'optimisation fine des prompts complexes est déléguée au skill `agent-prompt-engineering` (SHARED §3.1).

**Méthode prompt-engineering (méthode-mère)** : gen-plan est le détenteur principal de la méthode prompt-engineering (définitions : SHARED §7 ; orchestration : PM v3.11.0 §1.9) ; les autres skills de l'écosystème la détiennent en tant que **fonction héritée** (registre d'assignation : SHARED §7).

**Méthode de raisonnement adaptative PEK (v3.11.0, PM §1.9)** : gen-plan mobilise le Prompt Engineering Kit v4.1 (méthode pure) comme couche de raisonnement opérationnelle — 3 modes d'exécution (CoT 7 étapes / Chaining 4 étapes / Hybride à bascule automatique selon la complexité E1-E3) alignés sur la philosophie §1.4 #6 et calibrés par les profils §2.4 ; blocs de sortie adaptatifs A-J mappés sur les Types 1-4 (E3) ; 9 règles critiques + 12 checks de validation (scoring 25 pts, seuil 22/25) intégrés aux hooks correct-work par phase (E9-E14). Contenu opérationnel : `references/prompt-engineering-kit.md`.

**Matérialisation des disciplines (état A12, mise à jour session A13)** : les 4 disciplines d'exécution sont matérialisées en skills complets à déclenchement automatique (`context-engineering`, `loop-engineering`, `graph-engineering`, `harness-engineering` — SKILL.md + evals + trigger_evals ; les matérialisations agent intermédiaires `_disciplines/` A11 et `gen-plan.agent` A9 sont retirées, SHA prouvés) et la discipline prompt-engineering en skill (`agent-prompt-engineering`). Source de vérité des disciplines : SHARED §7 ; orchestration : PM v3.11.0 §1.9.

---

### §1.7 Pipeline d'optimisation écosystème Z0-Z6 (PM v3.11.0 §1.10)

| Phase | Nom | Règles clés |
|-------|-----|-------------|
| Z0 | Inventaire | Règle zéro (SHARED §0) |
| Z1 | Normalisation | Frontmatters YAML complets (SHARED §1.3) |
| Z2 | Optimisation par fichier | Règles d'or, disciplines (§1.6), dépendances, cohérence |
| Z3 | Optimisation scripts Python | N3 ; arbitres (verify-cross, spell-check, sync-download) |
| Z4 | Vérifications croisées | SHARED §3.2 ; hooks correct-work |
| Z5 | Journalisation | Worklog (SHARED §1.4) |
| Z6 | Idempotence | R1-R6 (§1.8) |

### §1.8 Règles d'idempotence R1-R6 (PM v3.11.0 §1.11)

R1 vérifier présence avant insertion · R2 ne jamais rétrograder · R3 fusionner les frontmatters ·
R4 ne jamais dupliquer · R5 journaliser · R6 auto-adaptation sans duplication.

---

## §2 — Spécification technique

### §2.1 Stack

- **Langage** : Python (scripts), Markdown (documentation), YAML (frontmatter)
- **Environnement** : `skills/gen-plan/`
- **Pas de dépendance externe** (sauf intégration KB si activée)

### §2.2 Structure

```
skills/gen-plan/
├── SKILL.md                          # Skill opérationnel compact (~232 lignes)
├── references/
│   ├── etapes-detaillees.md          # Détail des 15 étapes
│   ├── grille-token.md               # Grille de calibration #token
│   ├── classification-types.md       # Routage Type 1-4
│   ├── profils-ressource.md          # NORMAL / ECO / VIEUX PC
│   ├── guide-selection-agent-skill.md # Arbre de décision + tableau
│   └── prompt-engineering-kit.md     # PEK v4.1 — raisonnement adaptatif (CoT/Chaining/Hybride, blocs A-J, 9 règles, 12 checks)
└── evals/
    └── evals.json                    # Cas de test d'évaluation (6 evals)
```

### §2.3 Auto-calibration E15

| Écart estimé vs réel | Action |
|----------------------|--------|
| 0-20% | Aucune action |
| 20-35% | Ajustement de la grille (paramétrage fin) |
| >35% | Recalibration complète |

L'historique de calibration (11 entrées, rows 1-11) est maintenu dans `references/grille-token.md`.

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

Si activé : consultation de `{{KB_PATH}}`, scan du registre pour identifier les skills pertinents (Protocole de Découverte SHARED §2.3), enrichissement à E15. Environnement bac à sable : registre minimal `skills/KNOWLEDGE.md` (skills écosystème installés), extensible à chaque matérialisation.

---

## §3 — Relations

| Avec | Nature | Détails |
|------|--------|--------|
| correct-work | Invocation à E1 + hook E8 + contrôle par phase | Validation du plan initial + vérification post-plan et à chaque phase terminée (E9-E14), version >= v2.4.0 |
| clone-chat | Calibration + archivage | E4, E15, optionnel, version >= v2.0.0 |
| skills-inventory | Consultation à E5 | Sélection des skills, version >= v1.0.0 |
| agent-prompt-engineering | Délégation (§1.6) | Optimisation des prompts complexes, version >= v1.0.0 |
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
- Versions : semver (`3.7.0`)
- Tags : préfixe `#` (`#token 3500`)
- Variables : double accolades (`{{SKILLS_ROOT}}`)

### §5.2 Python uniquement (N3)

Tous les scripts générés en Python. Aucun script shell (bash, sh, powershell). Portabilité cross-platform garantie.

### §5.3 Tagging #token (N1)

Chaque étape du plan et chaque skill utilisé reçoit un tag `#token` indiquant le coût estimé. La grille est auto-calibrée à E15.

### §5.4 Hook correct-work par phase (E9-E14)

Dès qu'une phase du plan d'actions vient de se terminer, lancer `correct-work(livrables de la phase, mode=CIBLE)` AVANT d'entamer la phase suivante : PASS → phase suivante ; PASS AVEC RÉSERVES → réserves loggées au worklog, exécution continue ; FAIL → pause jusqu'à correction puis re-vérification. Le hook E8 (fin de plan) reste la vérification finale.
