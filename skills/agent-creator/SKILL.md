---
name: agent-creator
version: 2.3.0
category: ecosystem
language: fr
tags:
  - agent
  - agent-creation
  - fabrique
  - memory
  - pipeline
  - multi-llm
  - ecosystem
description: >
  Création et orchestration d'agents : génère des agents autonomes persistants (fichier .agent,
  mémoire interne à deux niveaux, modules internes, boucles, intégration multi-LLM) et orchestre
  plusieurs agents spécialisés sur un flux de tâches.
dependencies:
  - skill: gen-plan
    version: ">=3.6.0"
    used_at: "Planification de tâches complexes (F1 cadrage)"
  - skill: autonomous-agent
    version: ">=1.2.0"
    used_at: "Runtime d'exécution des agents produits"
  - skill: clone-chat
    version: ">=2.0.0"
    used_at: "Persistance État Long entre sessions"
    optional: true
  - skill: correct-work
    version: ">=2.4.0"
    used_at: "Validation cohérence des artefacts produits (F3)"
read_when:
  - Déclencher quand la demande concerne : CRÉATION d'agents persistants (fichier .agent) — cadrer, générer, valider, tester, inscrire un agent
  - Déclencher si la demande mentionne : créer/cadrer/générer un agent, fabrique d'agents, fichier .agent, agent persistant
  - Ne pas déclencher pour EXÉCUTER un agent existant (autonomous-agent) ni pour ORCHESTRER une flotte existante (fleet-engineering) — convention protocole, Task 28/22.
---

# AGENT-CREATOR v2.2.0 — Fabrique d'agents persistants

## §0 — Contexte Système (SHARED v1.7.13)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.

## §1 — Spécification fonctionnelle

### §1.1 Objectif

Fournir la FABRIQUE d'agents persistants de l'écosystème : cadrer un besoin
d'agent, générer son fichier `.agent` (mémoire interne à deux niveaux,
modules, pipeline), valider sa structure, tester son comportement et
l'inscrire aux registres. L'exécution d'un agent produit relève du runtime
autonomous-agent ; l'orchestration d'une flotte existante relève de
fleet-engineering — une responsabilité par élément (non-duplication SHARED §7).

### §1.2 Workflow de fabrique (5 étapes F1-F5)

| Étape | Nom | Description |
|-------|------|-------------|
| **F1** | Cadrer | Analyser le besoin : une responsabilité unique par agent (anti-mega-agent), inputs/outputs, règles de sécurité, niveau de persistance |
| **F2** | Générer | Produire le gabarit `.agent` (format §2.3) spécialisé : objectif 1 phrase, modes, règles, champ `capacites` machine-lisible (style Agent Card A2A) |
| **F3** | Valider | Schéma YAML conforme (references/agent-format.md), YAML parseable, read_when/description-déclencheur dense, correct-work(cible) sur l'artefact |
| **F4** | Tester | Mode M4 Simulation : exécuter le comportement sur des cas représentatifs (positifs + négatifs), vérifier la cohérence des sorties |
| **F5** | Inscrire | skills-inventory (découvrabilité) + registre KB si élément d'écosystème + worklog (provenance) — l'agent non inscrit est invisible |

### §1.3 Les 4 modes

| Mode | Nom | Description |
|------|-----|-------------|
| M1 | **Cadrage** | Analyse du besoin d'agent : responsabilité unique, contraintes, périmètre F1 |
| M2 | **Génération** | Production du gabarit .agent spécialisé + champ capacites, étape F2 |
| M3 | **Validation** | Schéma YAML + parse + déclencheurs + correct-work(cible), étape F3 |
| M4 | **Simulation** | Test comportemental du produit (cas représentatifs), étape F4 ; inscription F5 en sortie |

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

**Persistance** : l'État Long de chaque agent PRODUIT est sauvegardé dans son
fichier `.agent` (format YAML, voir `references/agent-format.md`) ; la
persistance inter-sessions de la fabrique elle-même passe par clone-chat
(optionnel). L'État Court est volatil — il n'existe que dans la session.

### §1.5 Contenu obligatoire d'un agent produit

Un `.agent` validé F3 porte AU MINIMUM : `objectif` (1 phrase, une
responsabilité) ; `modes` explicites ; `regles` de sécurité ; `inputs`/`outputs`
typés ; `memoire` (EC/EL) ; `capacites` (liste machine-lisible — découverte
style Agent Card A2A, consommable par skills-inventory) ; `relations` (skills
dépendants, versions). Le prompt système de l'agent suit l'altitude durable
(Anthropic 09/2025) : langage direct, durabilité > micro-gestion des étapes —
voir agent-prompt-engineering (non-duplication SHARED §7).

### §1.6 Orchestration multi-agents (renvoi)

La fabrique PRODUIT les agents ; l'orchestration d'une flotte est déléguée :
ordre de routage (fleet-engineering §1.9bis) — (a) tâche séquentielle → 1 agent
autonome ; (b) parallélisable/indépendant → flotte M1-M5 ; (c) nœuds
scripts/binaires → inter-scripts ; (d) création d'agents réutilisables →
agent-creator (cette fabrique). Task IDs globaux et agrégation re-vérifiée :
voir fleet-engineering.

---
### §1.9bis — Apports de veille 2025-2026 (Task 22 — recherches web ciblées)

- **Fabrique ≠ runtime (sub-agents Claude Code, 2025)** : la création d'agents persistants est une responsabilité distincte de leur exécution et de leur orchestration — une responsabilité par élément (anti-mega-agent). → *Application locale* : workflow F1-F5 (cadrer→générer→valider→tester→inscrire) ; exécution → autonomous-agent ; orchestration → fleet-engineering (routage §1.6).
- **Champ capacités machine-lisible (Agent Card A2A)** : tout agent produit expose ses capacités en style Agent Card — découvrabilité par défaut, consommable par des registres externes. → *Application locale* : §2.3 format .agent (champ `capacites` obligatoire) + inscription skills-inventory (F5 — l'agent non inscrit est invisible).
- **Skill authoring / progressive disclosure (Anthropic, Agent Skills 10/2025)** : les artefacts d'agents suivent le standard ouvert — description dense (déclencheur), corps (instructions), détails à la demande (references/). → *Application locale* : gabarits de la fabrique + read_when denses des agents produits (rédaction : agent-prompt-engineering).
- **Sources** : anthropic.com (sub-agents Claude Code · Agent Skills 10/2025) · a2a-protocol (Agent Card) · anthropic.com/engineering/effective-context-engineering-for-ai-agents.

> **Ajout Task 24** (2026-10-23, session web-fdf5963c — directive propriétaire « révisez les §1.9bis des 16 éléments ») : §1.9bis créée pour le 16e élément — apports de veille de la réécriture v2.2.0 (Task 22) alignés au format commun des 15 autres.

## §2 — Spécification technique

### §2.1 Stack technique

- **Langage** : Markdown (documentation), YAML (fichier .agent, frontmatter)
- **Environnement** : `{{SKILLS_ROOT}}agent-creator/`
- **Pas de dépendance externe** (sauf gen-plan pour la planification)

### §2.2 Structure des fichiers

```
{{SKILLS_ROOT}}agent-creator/
├── SKILL.md
└── references/
    └── agent-format.md
```

### §2.3 Format .agent

Les fichiers `.agent` stockent l'État Long d'un agent produit. Format YAML
(schéma complet : `references/agent-format.md`) — champ `capacites` obligatoire
(style Agent Card A2A, découverte machine-lisible) :

```yaml
agent:
  nom: <nom-agent>              # kebab-case
  objectif: <objectif en 1 phrase — une responsabilité>
  modes: <modes disponibles>
  regles: <règles strictes>
  inputs: <types d'entrées>
  outputs: <types de sorties>
  capacites: <liste machine-lisible — style Agent Card A2A>
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
| autonomous-agent | Runtime | Exécution des agents produits (la fabrique produit, le runtime exécute) |
| fleet-engineering | Délégation | Orchestration de flottes — la fabrique n'orchestre pas (routage §1.6) |
| clone-chat | Persistance | Sauvegarde État Long entre sessions, optionnel, version >= v2.0.0 |
| skills-inventory | Inscription | F5 — découvrabilité des agents produits |
| agent-prompt-engineering | Rédaction | Altitude durable des prompts système des agents produits |
| correct-work | Vérification | Validation de la cohérence des artefacts produits, version >= v2.4.0 |

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
| 2.3.0 | 2026-10-23 | Task 24 — §1.9bis créée (16e élément — apports de veille 2025-2026 de la réécriture v2.2.0 alignés au format commun des 15 autres : fabrique ≠ runtime, champ capacites Agent Card A2A, progressive disclosure) — bump MINOR (recalibrage KO-L004 : ECO_SKILLS + KB) |
| 2.2.0 | 2026-10-23 | Task 22 — DÉRIVE CRITIQUE résorbée : le corps était une copie quasi verbatim d'autonomous-agent (titre erroné « AUTONOMOUS-AGENT v1.0.0 », aucun workflow de fabrique malgré la description frontmatter) ; §1 re-écrit comme VRAIE fabrique (workflow F1-F5 cadrer→générer→valider→tester→inscrire), modes M1-M4 réalignés, §1.5 contenu obligatoire + champ capacites (Agent Card A2A), §1.6 renvoi orchestration (fleet-engineering), relations §3 étendues (autonomous-agent runtime, fleet, agent-prompt-engineering), read_when réparé (tronqué mid-phrase — 1/94 Task 28), .agent ré-écrit (objectif fabrique, champ capacites, pipeline F1-F5) ; veille 2025-2026 : sub-agents Claude Code, A2A Agent Card, skill authoring Anthropic |
| 2.1.0 | 2026-10 | Version antérieure (corps hérité non aligné — défaut documenté ci-dessus) |
| 1.0.0 | 2026-08-09 | Version initiale (corps autonome copié — origine de la dérive) |

---

## Baseline A2 — statut de mesure
> **Baseline A2 (Task 21 P3/F3, 2026-10-03)** : MESURÉE 2 voies (voie mécanique SHARED §7 v2 + voie L 3 runs réels) — score baseline 6/7 (nulls : 1) ; détail par cas : `scripts/baseline-a2-all-report.json` ; cas structurels consignés au registre KB (décision Task 21) ; re-mesure idempotente `--skip-done` armée pour les nulls 429 restants.
