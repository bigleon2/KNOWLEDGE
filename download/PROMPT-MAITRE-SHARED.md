# PROMPT MAÎTRE SHARED — Écosystème Skills DJ

> **Version** : 1.0.0
> **Date** : 2026-08-09
> **Source** : Écosystème Skills DJ — Clone de discussion (30 sessions)
> **Usage** : Ce fichier est inclus par référence dans les prompts maîtres de chaque skill écosystème.

---

## §0 — CONTEXTE COMMUN

Tu es un assistant IA (Z AI / GLM) dans l'environnement `{{SKILLS_ROOT}}/`. L'utilisateur souhaite installer un skill de l'écosystème (72+ skills). Tu dois créer l'intégralité des fichiers du skill à partir du prompt maître qui t'est fourni, combiné à ce fichier shared.

**Règle zéro** : Ne pas utiliser le verbe « conserver » — tout est à créer.

---

## §1 — VARIABLES D'INSTALLATION

| Variable | Valeur par défaut | Description |
|----------|------------------|-------------|
| `{{SKILLS_ROOT}}` | `skills/` | Chemin racine du répertoire des skills (relatif au projet) |
| `{{KB_PATH}}` | `skills/KNOWLEDGE.md` | Chemin vers le registre KB |
| `{{WORKLOG_PATH}}` | `worklog.md` | Chemin vers le worklog partagé |
| `{{KB_ENABLED}}` | `true` | Activer l'intégration Registre KB |
| `{{PROFILE_DEFAULT}}` | `NORMAL` | Profil ressource par défaut (NORMAL / ECO / VIEUX PC) |
| `{{IN_EXTENSO_THRESHOLD}}` | `200` | Seuil en lignes : en dessous = contenu intégral, au-dessus = résumé structuré |

**Utilisation** : Lors de l'installation, remplacer les variables `{{...}}` par leurs valeurs. Si l'utilisateur ne précise pas, utiliser les valeurs par défaut.

---

## §2 — CONVENTIONS ÉCOSYSTÈME

### 2.1 Nommage des skills

```
{{SKILLS_ROOT}}/<nom-skill>/SKILL.md
```

Exemples : `skills/gen-plan/SKILL.md`, `skills/correct-work/SKILL.md`, `skills/clone-chat/SKILL.md`.

### 2.2 YAML frontmatter

Tout fichier `SKILL.md` doit commencer par un bloc YAML frontmatter avec ces champs obligatoires :

```yaml
---
name: <nom-du-skill>
version: <x.y.z>
category: ecosystem
language: fr
tags:
  - <tag1>
  - <tag2>
description: >
  Description concise du skill (1-3 phrases).
dependencies:
  - skill: <nom-skill-dep>
    version: ">=x.y.z"
    used_at: "<où/comment>"
    optional: true  # si applicable
---
```

### 2.3 Numérotation des sections

Les skills écosystème utilisent une numérotation `§0` à `§N` (pas `1-N`).

### 2.4 Règle in extenso

| Taille du contenu | Traitement |
|--------------------|------------|
| < {{IN_EXTENSO_THRESHOLD}} lignes | Contenu intégral (in extenso) |
| > 500 lignes | Résumé structuré |
| Entre 200 et 500 lignes | Au choix, préférer in extenso si référence unique |

### 2.5 Conventions de chemins dans les clones

Tous les chemins dans les artefacts de clone-chat sont **relatifs** (jamais absolus). Exemple : `skills/clone-chat/SKILL.md`, jamais `/home/user/...`.

### 2.6 Format des entrées worklog

Chaque exécution d'un skill génère une entrée worklog :

```markdown
---
Task ID: <task-id>
Agent: <skill-name> v<x.y.z>
Task: <description brève>

Work Log:
- <action 1>
- <action 2>
- ...

Stage Summary:
- <résultat clé 1>
- <résultat clé 2>
```

---

## §3 — REGISTRE KB (KNOWLEDGE.md)

### 3.1 Présentation

`KNOWLEDGE.md` est le registre central des skills de l'écosystème. Il contient 72+ entrées et permet aux skills de découvrir dynamiquement les autres skills disponibles.

### 3.2 Template d'entrée

Chaque skill installé doit ajouter son entrée dans `KNOWLEDGE.md` :

```markdown
## <nom-skill>
- **Version** : <x.y.z>
- **Catégorie** : <category>
- **Fichier** : `<chemin-relatif>/SKILL.md`
- **Description** : <description courte>
- **Relations** : <skill-A> (<nature>), <skill-B> (<nature>)
```

### 3.3 Protocole de Découverte

Quand `{{KB_ENABLED}}` est `true`, un skill peut :
1. Scanner `KNOWLEDGE.md` pour lister les skills disponibles
2. Vérifier la version minimale de chaque dépendance
3. Détecter les skills manquants
4. Signaler les conflits de dépendances

Le flag `--kb-skill <nom>` cible un skill spécifique dans le registre.

---

## §4 — REGISTRE DES RELATIONS

### 4.1 Matrice de relations inter-skills

| Skill A | Skill B | Relation | Version min A | Version min B | Optionnel ? |
|---------|---------|----------|---------------|---------------|------------|
| **gen-plan** | correct-work | gen-plan invoque correct-work à E1 pour valider le plan | >= v3.5.0 | >= v2.2.0 | Non |
| **gen-plan** | clone-chat | gen-plan fournit calibration #token à clone-chat (E1-E7, E4, E15) | >= v3.5.0 | >= v1.2.0 | Oui |
| **gen-plan** | skills-inventory | gen-plan consulte l'inventaire à E5 pour sélectionner les skills | >= v3.5.0 | >= v1.0.0 | Non |
| **gen-plan** | knowledge.md | gen-plan enrichit le registre à E15 (bilan, calibration) | >= v3.5.0 | >= v1.0.0 | Non |
| **correct-work** | gen-plan | correct-work utilise gen-plan à son Étape 1 pour créer le plan de vérification | >= v2.2.0 | >= v3.1.0 | Non |
| **correct-work** | clone-chat | correct-work vérifie clone-chat en Mode CIBLE (§3.5 Context Drift) | >= v2.2.0 | >= v1.2.0 | Non |
| **correct-work** | fullstack-dev | correct-work vérifie les projets web | >= v2.2.0 | any | Non |
| **clone-chat** | gen-plan | clone-chat utilise les données calibration gen-plan pour le tagging #token | >= v1.2.0 | >= v3.3.0 | Oui |

### 4.2 Matrice de décision agent × skill (statique)

Cette matrice est la référence unique pour toutes les interactions agent × skill :

| Agent / Type de tâche | gen-plan | correct-work | clone-chat | skills-inventory | fullstack-dev |
|----------------------|----------|--------------|------------|------------------|---------------|
| Planification | orchestre | valide | — | consulte | — |
| Création document | E3 route | vérifie | — | — | — |
| Web dev | E3 route | vérifie | — | — | exécute |
| Clonage discussion | E1-E7 | Mode CIBLE | exécute | — | — |
| Data processing | E3 route | vérifie | — | — | — |

### 4.3 Règles de cross-references

Lors de l'installation d'un skill, mettre à jour les autres skills :

| Skill installé | Skills à mettre à jour | Contenu de la mise à jour |
|----------------|----------------------|--------------------------|
| gen-plan | correct-work, clone-chat, skills-inventory | Mentionner l'utilisation par gen-plan avec les étapes |
| correct-work | gen-plan, clone-chat | Mentionner la vérification par correct-work avec le mode |
| clone-chat | gen-plan, correct-work | Mentionner l'intégration optionnelle et la vérification croisée |

---

## §5 — HISTORIQUE DE L'ÉCOSYSTÈME

| Période | Événements clés |
|---------|---------------|
| 2026-07-18 | Création gen-plan v3.5.0, normalisation 67 skills, Prompt Maître DJ v2.0→v3.4 |
| 2026-07-20 | Bundle skill-all-days.zip |
| 2026-07-29 | Naissance clone-chat v1.0.0→v1.2.0, correct-work v1.0.0→v2.2.0, 3 rounds de vérification |
| 2026-07-30 | Intégration écosystème : KNOWLEDGE.md 72 skills, cross-references bidirectionnelles |
| 2026-08-09 | Clone final 30 sessions, 18 drifts, 17/17 compat checks PASS |

---

## §6 — MÉTA-INFORMATIONS SUR LES PROMPTS MAÎTRES

### 6.1 Fichiers du bundle

| Fichier | Version du prompt | Skill cible | Dépend de |
|---------|-------------------|-------------|------------|
| `PROMPT-MAITRE-SHARED.md` | 1.0.0 | (commun) | Aucun |
| `PROMPT-MAITRE-GEN-PLAN-v3.5.0.md` | 2.0.0 | gen-plan v3.5.0 | SHARED §0-§4 |
| `PROMPT-MAITRE-CORRECT-WORK-v2.2.0.md` | 2.0.0 | correct-work v2.2.0 | SHARED §0-§4 |

### 6.2 Ordre de lecture

Pour installer un skill, l'assistant doit lire les fichiers dans cet ordre :

1. `PROMPT-MAITRE-SHARED.md` (contexte, conventions, relations)
2. `PROMPT-MAITRE-<SKILL>-v<X.Y.Z>.md` (spécifications du skill cible)

### 6.3 Versionnage des prompts maîtres

| Prompt version | Signification |
|----------------|---------------|
| 1.0.0 | Première génération (fichiers autonomes, duplication ~15%) |
| 2.0.0 | Refactoring en 3 fichiers (shared + 2 spécifiques), duplication ~0% |