---
nom: skill-finder-cn
version: 1.0.0
source: skills/skill-finder-cn/SKILL.md
sha256_source: e8b5b24e5dae
genere: 2026-10-26 (phase P2 — directive 10 tâches, tâche 2)
usage: AUTONOME hors écosystème (dossier « Prompt Maitre » — non lu par l'orchestration)
---

> ⚠️ **MARQUEUR D'EXCLUSION (garde D010)** — CE DOSSIER N'EST PAS LU PAR L'ORCHESTRATION. Les dossiers « Prompt Maitre » sont des prompts autonomes à usage HORS écosystème : ils ne sont pas indexés au registre KB, ne sont mobilisés par aucun arbitre, et ne remplacent jamais la forme installée `skills/<skill>/` (source de vérité).

# Prompt Maître autonome — skill-finder-cn (v1.0.0)

## Comment utiliser ce prompt (hors écosystème)

Ce document encapsule la compétence sous forme autonome : copiez-le intégralement
dans un assistant IA (ou ouvrez-le en référence directe) — aucune installation,
aucun registre, aucune dépendance à l'écosystème Knowledge d'origine n'est requise.
Les variables de l'écosystème d'origine ont été résolues en valeurs littérales ;
si des ressources `references/` accompagnent ce dossier, elles sont jointes au même
emplacement et le prompt y renvoie par leur chemin relatif. La version d'origine
(source de vérité) vit dans `skills/skill-finder-cn/SKILL.md` du dépôt KNOWLEDGE.

---

## Le prompt

---
name: skill-finder-cn
version: 1.0.0
category: "Méta (Skills & Plans)"
tags:
  - skill
  - finder
  - cn
description: "Chercheur de skills | Skill Finder. Aide à découvrir et installer des ClawHub Skills | Discover and install ClawHub Skills. Répond à « quel skill peut faire X », « trouve un skill », « find a skill ». Mots déclencheurs : trouver un skill, find skill, chercher un skill, rechercher un skill."
author: zhuanqian xiao neng shou (gagne-petit-argent)
language: fr
metadata:
  openclaw:
    emoji: 🔍
    requires:
      bins: [clawhub]

read_when:
  - Déclencher quand la demande concerne : "Chercheur de skills | Skill Finder
  - Déclencher si la demande mentionne : skill, skills, clawhub
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

## §0 — Contexte Système (SHARED v1.7.13)

> Écosystème Knowledge : `skills/`=skills/ | `skills/KNOWLEDGE.md`=skills/KNOWLEDGE.md | `true`=true | `NORMAL`=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.

# Chercheur de Skills

Aide l'utilisateur à découvrir et installer des Skills depuis ClawHub.

## Fonctionnement

Quand l'utilisateur demande :
- « il existe quel skill pour m'aider à... ? »
- « trouve un skill capable de faire X »
- « y a-t-il un skill pour... »
- « j'ai besoin d'un skill qui... »

Ce skill aide à chercher sur ClawHub et recommande les Skills pertinents.

## Utilisation

### 1. Chercher des Skills

```bash
clawhub search "<yong hu xu qiu>"
```

### 2. Voir les détails

```bash
clawhub inspect <skill-name>
```

### 3. Installer un Skill

```bash
clawhub install <skill-name>
```

## Flux de travail

```
1. Comprendre le besoin de l'utilisateur
2. Extraire les mots-clés
3. Chercher sur ClawHub
4. Lister les Skills pertinents
5. Proposer l'installation
```

## Exemple

**Utilisateur** : « il existe quel skill pour m'aider à surveiller le prix des cryptomonnaies ? »

**Recherche** : `clawhub search "crypto price monitor"`

**Résultat** : la liste des Skills pertinents

---

*Aide l'utilisateur à découvrir les Skills dont il a besoin 🔍*


[INSTRUCTION COMPLÉMENTAIRE : il reste des caractères chinois ; translittère-les en pinyin ou traduis-les, renvoie le document intégral final]

---

## Ressources locales du dossier

Aucune ressource annexe — ce prompt est auto-suffisant.
