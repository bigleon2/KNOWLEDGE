---
name: skill-finder-cn
version: "1.0.0"
category: "Méta (Skills & Plans)"
tags:
  - skill
  - finder
  - cn
description: "Chercheur de skills | Skill Finder. Aide à découvrir et installer des ClawHub Skills | Discover and install ClawHub Skills. Répond à « quel skill peut faire X », « trouve un skill », « find a skill ». Mots déclencheurs : trouver un skill, find skill, chercher un skill, rechercher un skill."
author: 赚钱小能手
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

## §0 — Contexte Système (SHARED v1.6.8)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
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
clawhub search "<用户需求>"
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
