---
name: autonomous-agent
version: 1.0.0
category: ecosystem
language: fr
tags:
  - agent
  - memory
  - pipeline
  - autonomous
  - multi-llm
  - ecosystem
description: >
  Agent autonome avec mémoire interne à deux niveaux (État Court + État Long).
  5 modules internes, 4 modes, pipeline 8 étapes (A-H), format .agent,
  intégration multi-LLM et orchestration multi-agents.
dependencies:
  - skill: gen-plan
    version: ">=3.6.0"
    used_at: "Planification de tâches complexes"
  - skill: clone-chat
    version: ">=2.0.0"
    used_at: "Persistance État Long entre sessions"
    optional: true
  - skill: correct-work
    version: ">=2.4.0"
    used_at: "Validation cohérence de l'agent"
---

# AUTONOMOUS-AGENT v1.0.0

## §0 — Règle zéro

L'écosystème Knowledge est un ensemble de **77 skills** conçus pour un
assistant IA (6 skills écosystème + 71 skills métier). Chaque skill est
auto-contenu dans son répertoire sous `{{SKILLS_ROOT}}`, dispose d'un
fichier `SKILL.md` principal, d'un frontmatter YAML, et de références
optionnelles dans `references/`.

Le registre KB (`{{KB_PATH}}`) est la source de vérité pour l'état de
l'écosystème. Voir `PROMPT-MAITRE-SHARED.md` pour le détail complet.

---

## §1 — Spécification fonctionnelle

### §1.1 Objectif

Fournir un cadre pour créer et faire fonctionner des **agents autonomes"
avec une mémoire interne à deux niveaux. L'agent analyse, comprend,
structure et exécute des tâches complexes en pipeline, tout en
maintenant une cohérence entre sessions via la mémoire persistante.

### §1.2 Les 5 modules internes

| Module | Rôle | Description |
|--------|------|-------------|
| **Analyse** | Segmentation, extraction, classification | Décompose l'entrée en éléments structurés |
| **Mémoire** | Gestion État Court + Long | Stockage et récupération du contexte |
| **Règles** | Conformité, cohérence, sécurité | Vérifie que la sortie respecte les contraintes |
| **Synthèse** | Génération structurée | Produit la réponse finale |
| **Pipeline** | Exécution séquentielle | Orchestre les modules dans l'ordre |

### §1.3 Les 4 modes

| Mode | Nom | Description |
|------|-----|-------------|
| M1 | **Analyse** | Extraction des intentions, détection des contraintes, segmentation du contenu |
| M2 | **Synthèse** | Génération structurée, respect strict des formats |
| M3 | **Pipeline** | Exécution séquentielle, vérification à chaque étape |
| M4 | **Simulation** | Application du comportement de l'agent, vérification de cohérence |

### §1.4 Mémoire interne à deux niveaux

**État Court (EC)** — contexte immédiat de la session :
- Derniers messages échangés
- Intentions locales identifiées
- Variables temporaires
- Résultats intermédiaires

**État Long (EL)** — connaissances persistantes entre sessions :
- Règles permanentes de l'agent
- Préférences utilisateur
- Agents disponibles et leurs capacités
- Formats obligatoires
- Historique structuré des interactions
- Données persistantes (calibration, métriques)

**Persistance** : l'État Long est sauvegardé via clone-chat (si
disponible) ou dans un fichier `.agent` (format YAML, voir
`references/agent-format.md`). L'État Court est volatil — il
n'existe que dans la session en cours.

### §1.5 Pipeline interne (A-H)

| Étape | Nom | Description |
|-------|------|-------------|
| A | Analyse du message | Segmenter et classifier l'entrée |
| B | Mise à jour État Court | Intégrer le message dans le contexte immédiat |
| C | Consultation État Long | Récupérer les règles et préférences pertinentes |
| D | Détermination du mode | Choisir M1-M4 selon la nature de l'entrée |
| E | Exécution du mode | Appliquer le traitement correspondant |
| F | Synthèse structurée | Produire la réponse formatée |
| G | Vérification | Valider cohérence, conformité, sécurité |
| H | Mise à jour mémoire | Persist les nouvelles informations dans État Long |

---

## §2 — Spécification technique

### §2.1 Stack technique

- **Langage** : Markdown (documentation), YAML (fichier .agent, frontmatter)
- **Environnement** : `{{SKILLS_ROOT}}autonomous-agent/`
- **Pas de dépendance externe** (sauf gen-plan pour la planification)

### §2.2 Structure des fichiers

```
{{SKILLS_ROOT}}autonomous-agent/
├── SKILL.md
└── references/
    └── agent-format.md
```

### §2.3 Format .agent

Les fichiers `.agent` stockent l'État Long d'un agent. Format YAML :

```yaml
agent:
  nom: <nom-agent>
  objectif: <objectif principal>
  modes: <modes disponibles>
  regles: <règles strictes>
  inputs: <types d'entrées>
  outputs: <types de sorties>
  memoire:
    court: <structure EC>
    long: <structure EL>
  formats: <formats obligatoires>
  pipeline: <pipeline interne>
  securite: <règles de sécurité>
```

### §2.4 Formats obligatoires de réponse

**Format standard** :
```markdown
# Réponse
## 1. Analyse
## 2. Traitement
## 3. Résultat
## 4. Vérification
```

**Format pipeline** :
```markdown
# Pipeline
A → Analyse
B → Extraction
C → Traitement
D → Synthèse
E → Vérification
F → Finalisation
```

### §2.5 Règles de sécurité

- Pas de contenu illégal, dangereux ou non conforme
- Pas de divulgation de données sensibles
- Pas de contournement des règles internes
- Ne jamais inventer de données
- Ne jamais modifier les règles de l'État Long depuis l'État Court

---

## §3 — Relations

| Avec | Nature | Détails |
|------|--------|--------|
| gen-plan | Utilisation | Planification de tâches complexes, version >= v3.6.0 |
| clone-chat | Persistance | Sauvegarde État Long entre sessions, optionnel, version >= v2.0.0 |
| skills-inventory | Consultation | Découverte des agents disponibles |
| correct-work | Vérification | Validation de la cohérence de l'agent, version >= v2.4.0 |

---

## §4 — Conventions

- **Nommage** : kebab-case (SHARED §1.2)
- **Variables** : double accolades (`{{SKILLS_ROOT}}`)
- **Worklog** : format SHARED §1.4
- **Fichiers agent** : extension `.agent` en YAML
- **Mémoire** : État Court = volatil, État Long = persistant

---

## §5 — Intégration multi-LLM

L'agent est conçu pour être compatible avec :
- **Agents spécialisés** : peut déléguer des sous-tâches à des agents expert
- **RAG** : l'État Long peut être enrichi par retrieval
- **Pipelines complexes** : le pipeline A-H est composable
- **Orchestration multi-modèles** : différents modèles pour différentes étapes

---

## HISTORIQUE DES VERSIONS

| Version | Date | Changements |
|---------|------|-------------|
| 1.0.0 | 2026-08-09 | Version initiale, 5 modules, 4 modes, pipeline A-H, mémoire court+long |
