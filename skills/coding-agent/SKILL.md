---
name: coding-agent
category: "Développement"
tags:
  - coding
  - agent
slug: code
version: 1.0.5
category: "Développement"
tags:
  - coding
  - agent
homepage: https://clawic.com/skills/code
description: Workflow de développement avec planification, implémentation, vérification et tests pour un développement logiciel propre.
changelog: Improved description for better discoverability
language: fr
metadata: {"clawdbot":{"emoji":"💻","requires":{"bins":[]},"os":["linux","darwin","win32"]}}

read_when:
  - Déclencher quand la demande concerne : workflow de développement avec planification, implémentation, vérification et tests pour un développement logi…
  - Déclencher si la demande mentionne : développement, workflow, planification
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

## Quand l'utiliser

L'utilisateur demande explicitement une implémentation de code. L'agent fournit la planification, le guidage d'exécution et les workflows de vérification.

## Architecture

Les préférences de l'utilisateur sont stockées dans `~/code/` quand il le demande explicitement.

```
~/code/
  - memory.md    # User-provided preferences only
```

Créer lors de la première utilisation : `mkdir -p ~/code`

## Référence rapide

| Sujet | Fichier |
|-------|------|
| Configuration mémoire | `memory-template.md` |
| Découpage des tâches | `planning.md` |
| Flux d'exécution | `execution.md` |
| Vérification | `verification.md` |
| État multi-tâches | `state.md` |
| Critères utilisateur | `criteria.md` |

## Périmètre

Ce skill fait UNIQUEMENT :
- Fournir des consignes de workflow de développement
- Stocker les préférences explicitement fournies par l'utilisateur dans `~/code/`
- Lire les fichiers de référence inclus

Ce skill ne fait JAMAIS :
- Exécuter du code automatiquement
- Faire des requêtes réseau
- Accéder à des fichiers hors de `~/code/` et du projet de l'utilisateur
- Modifier son propre SKILL.md ou ses fichiers auxiliaires
- Agir de façon autonome sans que l'utilisateur le sache

## Règles de base

### 1. Consulter d'abord la mémoire
Lire `~/code/memory.md` pour connaître les préférences déclarées de l'utilisateur, si le fichier existe.

### 2. L'utilisateur contrôle l'exécution
- Ce skill fournit des CONSEILS, pas une exécution autonome
- L'utilisateur décide du passage à l'étape suivante
- La délégation à un sous-agent exige une demande explicite de l'utilisateur

### 3. Planifier avant de coder
- Découper les demandes en étapes testables
- Chaque étape vérifiable indépendamment
- Voir `planning.md` pour les schémas

### 4. Tout vérifier
| Après | Faire |
|-------|-----|
| Chaque fonction | Suggérer de lancer les tests |
| Changements UI | Suggérer de prendre une capture d'écran |
| Avant la livraison | Suggérer la suite de tests complète |

### 5. Enregistrer les préférences sur demande
| L'utilisateur dit | Action |
|-----------|--------|
| « retiens que je préfère X » | Ajouter à memory.md |
| « ne fais plus jamais Y » | Ajouter à la section Never de memory.md |

N'enregistrez que ce que l'utilisateur demande explicitement de sauvegarder.

## Workflow

```
Request -> Plan -> Execute -> Verify -> Deliver
```

## Pièges courants

- **Livrer du code non testé** -> toujours vérifier d'abord
- **PR énormes** -> découper en morceaux testables
- **Ignorer les préférences** -> consulter d'abord memory.md

## Auto-modification

Ce skill ne modifie JAMAIS son propre SKILL.md ni ses fichiers auxiliaires.
Les données utilisateur sont stockées uniquement dans `~/code/memory.md`, après demande explicite.

## Points d'accès externes

Ce skill ne fait AUCUNE requête réseau.

| Endpoint | Données envoyées | Objectif |
|----------|-----------|---------|
| Aucun | Aucune | N/A |

## Sécurité et confidentialité

**Données qui restent en local :**
- Uniquement les préférences que l'utilisateur demande explicitement d'enregistrer
- Stockées dans `~/code/memory.md`

**Données qui quittent votre machine :**
- Aucune. Ce skill ne fait aucune requête réseau.

**Ce skill ne fait PAS :**
- Exécuter du code automatiquement
- Accéder au réseau ou à des services externes  
- Accéder à des fichiers hors de `~/code/` et du projet de l'utilisateur
- Agir de façon autonome sans que l'utilisateur le sache
- Déléguer à des sous-agents sans demande explicite de l'utilisateur
