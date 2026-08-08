# PROMPT MAÎTRE SHARED — Socle commun écosystème Knowledge

> **Version** : 1.0.0
> **Date** : 2026-08-09
> **Source** : Écosystème Knowledge — Clone de discussion
> **Usage** : Ce fichier doit être lu en premier avant tout prompt maître spécifique (gen-plan, correct-work, etc.)

---

## §0 — Règle zéro (Contexte commun)

L'écosystème Knowledge est un ensemble de 77 skills conçus pour un assistant IA (5 skills écosystème + 72 skills métier). Chaque skill est auto-contenu dans son répertoire sous `{{SKILLS_ROOT}}`, dispose d'un fichier `SKILL.md` principal, d'un frontmatter YAML, et de références optionnelles dans `references/`.

**Principes fondamentaux** :
- Chaque skill est versionné sémantiquement (MAJEUR.MINEUR.PATCH)
- Les dépendances inter-skills sont déclarées dans le frontmatter YAML avec versions minimales
- Les cross-references entre skills doivent être maintenues bidirectionnellement
- Le registre KB (`KNOWLEDGE.md`) est la source de vérité pour l'état de l'écosystème

---

## §1 — Conventions écosystème

### §1.1 Variables d'installation

| Variable | Défaut | Description |
|----------|--------|-------------|
| `{{SKILLS_ROOT}}` | `skills/` | Racine du répertoire des skills |
| `{{KB_PATH}}` | `skills/KNOWLEDGE.md` | Chemin vers le registre KB |
| `{{KB_ENABLED}}` | `true` | Activation/désactivation du registre KB |
| `{{PROFILE_DEFAULT}}` | `NORMAL` | Profil ressource par défaut |

### §1.2 Conventions de nommage

- **Répertoires** : kebab-case (`gen-plan`, `correct-work`, `clone-chat`)
- **Fichiers** : kebab-case avec extension (`SKILL.md`, `etapes-detaillees.md`, `evals.json`)
- **Versions** : format semver (`3.6.0`, `2.3.0`)
- **Tags** : préfixe `#` pour les tokens (`#token 3500`)
- **Variables** : double accolades (`{{SKILLS_ROOT}}`)

### §1.3 Conventions YAML frontmatter

Chaque `SKILL.md` commence par un bloc YAML délimité par `---` contenant au minimum :

```yaml
---
name: [kebab-case]
version: [X.Y.Z]
category: ecosystem
language: fr
tags:
  - [tag1]
  - [tag2]
description: >
  [Description en 1-3 phrases]
dependencies:
  - skill: [nom-skill]
    version: ">=X.Y.Z"
    used_at: "[étape/mode d'utilisation]"
---
```

### §1.4 Format worklog

Tous les agents partagent un worklog unique. Chaque entrée suit ce format :

```markdown
---
Task ID: [task-id]
Agent: [nom-agent] [version]
Task: [description de la tâche]

Work Log:
- [action concrète 1]
- [action concrète 2]

Stage Summary:
- [résultats clés / décisions / artefacts produits]
```

---

## §2 — Registre KB (KNOWLEDGE.md)

### §2.1 Rôle

`KNOWLEDGE.md` est le registre central de l'écosystème. Il contient :
- La liste de tous les skills installés avec leurs versions
- Les relations inter-skills
- Les métadonnées de calibration
- L'historique des interactions

### §2.2 Format d'une entrée (template)

```markdown
## [nom-skill] v[X.Y.Z]

- **Category** : [category]
- **Description** : [description courte]
- **Dépend de** : [liste des skills et versions min]
- **Utilisé par** : [liste des skills qui utilisent celui-ci]
- **Dernière calibration** : [date ou N/A]
- **Statut** : [stable | expérimental | en cours]
```

### §2.3 Protocole de Découverte

Quand un skill doit identifier les skills pertinents pour une tâche :
1. Scanner les entrées de `KNOWLEDGE.md` par catégorie et tags
2. Filtrer par compatibilité de version
3. Vérifier les dépendances croisées
4. Produire une liste ordonnée des skills candidats

---

## §3 — Registre des relations inter-skills

### §3.1 Tableau complet

| Skill A | Relation | Skill B | Nature | Détails |
|---------|----------|---------|--------|--------|
| gen-plan | invoque | correct-work | Étape 1 | Validation plan initial, >= v2.3.0 |
| gen-plan | utilise | clone-chat | Calibration + archivage | E1-E7, E4, E15, optionnel, >= v1.2.0 |
| gen-plan | consulte | skills-inventory | Sélection skills | E5, >= v1.0.0 |
| gen-plan | enrichit | KNOWLEDGE.md | Calibration | E15, mise à jour registre |
| correct-work | utilise | gen-plan | Plan de vérification | Étape 1, >= v3.6.0 |
| correct-work | vérifie | clone-chat | Mode CIBLE | §3.5 Context Drift, >= v1.2.0 |
| correct-work | vérifie | fullstack-dev | Projets web | Structure et dépendances |
| clone-chat | archivé par | gen-plan | Sessions longues | Optionnel, >= v1.2.0 |
| clone-chat | vérifié par | correct-work | Validation croisée | §3.5 drift, >= v1.2.0 |
| clone-chat | conventions par | skill-creator | Conventions structurelles | >= v1.0.0 |

### §3.2 Règles de cross-references

Quand un skill A référence un skill B :
1. La référence dans A doit inclure la version minimale requise de B
2. Le fichier de B doit mentionner A dans sa section « Utilisé par » de KNOWLEDGE.md
3. Si A modifie le comportement de B (ex : correct-work modifie clone-chat), la relation doit être documentée dans les deux sens
4. Les mises à jour de version d'un skill doivent déclencher une vérification des dépendances

---

## §4 — Matrice agent × skill (statique)

Cette matrice définit quels agents peuvent utiliser quels skills et dans quel contexte.

### §4.1 Matrice principale

| Agent | gen-plan | correct-work | clone-chat | skills-inventory | fullstack-dev | KB |
|-------|----------|-------------|------------|-----------------|---------------|-----|
| **Main** | Planification complète | Vérification finale | Archivage sessions | Consultation | Développement web | Lecture/écriture |
| **Subagent** | Exécution étapes | Vérification ciblée | Non | Non | Développement délégué | Lecture seule |
| **gen-plan (E1)** | — | Validation plan | Non | Scan skills | Non | Consultation |
| **correct-work (E1)** | Création plan | — | Vérification | Non | Vérification | Scan dynamique |
| **clone-chat** | Non | Non | — | Non | Non | Lecture seule |

### §4.2 Légende des droits

- **Planification complète** : toutes les étapes E1-E15
- **Exécution étapes** : E9-E14 uniquement, sans E15
- **Vérification finale** : mode PROJET complet
- **Vérification ciblée** : mode CIBLE ou DIRECT uniquement
- **Consultation** : lecture des données du skill
- **Scan dynamique** : vérifie les versions et la présence via KB
- **Lecture/écriture** : accès complet au registre
- **Lecture seule** : peut consulter mais pas modifier

---

## §5 — Format du fichier SKILL.md (conventions structurelles)

### §5.1 Structure type

Tout `SKILL.md` suit cette structure :

1. **YAML frontmatter** (obligatoire)
2. **§0 — Règle zéro** : contexte écosystème (résumé de SHARED §0)
3. **§1 — Spécification fonctionnelle** : modes, étapes, normes propres au skill
4. **§2 — Spécification technique** : stack, structure fichiers, intégrations
5. **§3 — Relations** : extrait de SHARED §3.1 pour les relations directes
6. **Sections spécifiques** : grille de vérification, grille #token, checklists, etc.
7. **§N — Conventions** : nommage (SHARED §1.2), règles propres

### §5.2 Tailles cibles

| Type de skill | Lignes SKILL.md | Fichiers references | Note |
|---------------|-----------------|-------------------|-------|
| Complexe (gen-plan) | ~170 lignes | 5 fichiers | Version compacte ; le prompt maître (866 lignes) contient la spec complète et le contenu in extenso des références |
| Moyen (correct-work) | ~130 lignes | 0 fichier | Version compacte ; le prompt maître (490 lignes) contient les checklists complètes (§10) |
| Simple | < 100 lignes | 0-1 fichier | |

---

## §6 — Prompt maîtres : architecture et workflow

### §6.1 Fichiers

| Fichier | Rôle | Version skill |
|---------|------|---------------|
| `PROMPT-MAITRE-SHARED.md` | Socle commun (ce fichier) | — |
| `PROMPT-MAITRE-GEN-PLAN-v3.6.0.md` | Spécification gen-plan | v3.6.0 |
| `PROMPT-MAITRE-CORRECT-WORK-v2.3.0.md` | Spécification correct-work | v2.3.0 |

### §6.2 Workflow d'utilisation

1. **Lire SHARED** en premier pour le contexte, conventions, variables et relations
2. **Lire le prompt maître spécifique** (gen-plan ou correct-work)
3. Suivre les instructions d'installation du fichier spécifique
4. Utiliser les références vers SHARED pour éviter la duplication
5. Mettre à jour KNOWLEDGE.md et les cross-references (SHARED §2.2 et §3.2)

### §6.3 Maintenance

- Toute modification d'une info commune (convention, relation, variable) se fait **une seule fois** dans SHARED
- Les prompts spécifiques contiennent uniquement la logique propre à leur skill
- La vérification croisée régulière garantit la cohérence (relations bidirectionnelles, versions)
