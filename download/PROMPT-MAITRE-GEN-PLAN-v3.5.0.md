# PROMPT MAÎTRE — Installation du skill gen-plan v3.5.0

> **Version du prompt** : 1.0.0
> **Skill cible** : gen-plan v3.5.0
> **Date** : 2026-08-09
> **Source** : Écosystème Skills DJ — Clone de discussion

---

## §0 — CONTEXTE

Tu es un assistant IA (Z AI / GLM) dans l'environnement `my-project/`. L'utilisateur souhaite installer le skill **gen-plan v3.5.0**, un skill de planification de tâches pour assistant IA. Ce skill fait partie d'un écosystème de 72+ skills. Tu dois créer l'intégralité des fichiers du skill à partir de ce prompt maître.

**Règle zéro** : Ne pas utiliser le verbe « conserver » — tout est à créer.

---

## §1 — SPÉCIFICATION FONCTIONNELLE

### 1.1 Description

gen-plan est un skill de **planification de tâches** pour assistant IA. Il fournit un cadre structuré en 4 modes de fonctionnement et 15 étapes (E1-E15) pour analyser, planifier, exécuter, surveiller et adapter toute tâche complexe.

### 1.2 Les 4 modes

| Mode | Nom | Description |
|------|-----|-------------|
| M1 | **Planification** | Analyse de la demande, classification, estimation, création du plan d'exécution |
| M2 | **Exécution** | Passage à l'action selon le plan établi, suivi des étapes |
| M3 | **Surveillance** | Monitoring en temps réel de l'avancement, détection d'écarts |
| M4 | **Adaptation** | Ajustement du plan en cas de dérive, recalibration |

### 1.3 Les 15 étapes (E1-E15)

| Étape | Nom | Description | Mode par défaut |
|-------|------|-------------|----------------|
| E1 | Analyse de la demande | Décortication de la demande utilisateur, identification des livrables, contraintes et critères de succès | M1 |
| E2 | Inventaire des ressources | Bilan des skills disponibles, outils, fichiers, contexte | M1 |
| E3 | Classification du type de tâche | Routage Type 1 (Document), Type 2 (Visualisation), Type 3 (Web Dev), Type 4 (Data Processing) | M1 |
| E4 | Estimation #token | Calcul budgétaire en tokens de la tâche | M1 |
| E5 | Sélection des skills | Identification des skills pertinents via skills-inventory et KNOWLEDGE.md | M1 |
| E6 | Profilage ressource | Choix du profil NORMAL / ECO / VIEUX PC | M1 |
| E7 | Création du plan | Assemblage du plan structuré avec étapes, dépendances, checkpoints | M1 |
| E8 | Validation du plan | Vérification cohérence, complétude, faisabilité | M1 |
| E9 | Lancement de l'exécution | Démarrage des étapes selon le plan | M2 |
| E10 | Suivi d'étape | Monitoring de chaque étape, log worklog | M2/M3 |
| E11 | Checkpoint intermédiaire | Vérification à mi-parcours, ajustements mineurs | M3 |
| E12 | Détection d'écart | Comparaison réel vs estimé, alertes | M3 |
| E13 | Ajustement | Modification du plan si nécessaire | M4 |
| E14 | Finalisation | Achèvement des étapes restantes | M2 |
| E15 | Bilan et auto-calibration | Retour d'expérience, mise à jour des grilles de calibration, enrichment KNOWLEDGE.md | M1/M4 |

### 1.4 Classification E3 — Routage des types de tâches

| Type | Nom | Indicateurs | Action |
|------|-----|-------------|--------|
| Type 1 | Document Creation | Rapport, PPT, DOCX, PDF, XLSX, script, manuscrit | Invoquer skill document (docx/pdf/xlsx/pptx) |
| Type 2 | Data Visualization | Charts, graphes, diagrammes, mind maps, Mermaid | Invoquer skill charts |
| Type 3 | Interactive Web Dev | Pages web, dashboards, apps, Next.js | Invoquer skill fullstack-dev |
| Type 4 | Data Processing | Traitement de données, analyse de fichiers, calculs | Écrire script Python |

### 1.5 Tagging #token (Norme N1)

Chaque étape et chaque skill utilisé reçoit un tag `#token` indiquant le coût estimé en tokens. La grille est auto-calibrée après exécutions.

**Grille de calibration (après 4 exécutions)** :

| Agent/Skill | #token estimé (par 1000 tokens sortie) |
|-------------|---------------------------------------|
| Planification (E1-E8) | 1500-3000 |
| Exécution simple | 2000-5000 |
| Exécution complexe | 5000-15000 |
| Surveillance (E10-E12) | 500-1500 |
| Auto-calibration (E15) | 800-2000 |

### 1.6 Snippets (Norme N2)

gen-plan peut générer des snippets de code réutilisables pendant l'exécution. Chaque snippet est tagué et versionné.

### 1.7 Python uniquement (Norme N3)

**Règle #7** : Tous les scripts générés par gen-plan doivent être en Python. Aucun script shell (bash, sh, powershell). Cette règle garantit la portabilité cross-platform.

---

## §2 — SPÉCIFICATION TECHNIQUE

### 2.1 Stack technique

- **Langage** : Python (scripts), Markdown (documentation), YAML (frontmatter)
- **Environnement** : `my-project/skills/gen-plan/`
- **Pas de dépendance externe** (sauf intégration KB optionnelle)

### 2.2 Structure des fichiers

```
skills/gen-plan/
├── SKILL.md                          # Skill principal (8.5 Ko)
├── references/
│   ├── etapes-detaillees.md          # Détail des 15 étapes
│   ├── grille-token.md               # Grille de calibration #token
│   ├── classification-types.md       # Routage Type 1-4
│   └── profils-ressource.md          # NORMAL / ECO / VIEUX PC
└── evals/
    └── evals.json                    # Cas de test d'évaluation
```

### 2.3 Auto-calibration E15

Mécanisme d'auto-calibration à l'étape E15 :

| Écart estimé vs réel | Action |
|----------------------|--------|
| 0-20% | Aucune action (estimation fiable) |
| 20-35% | Ajustement de la grille (paramétrage fin) |
| >35% | Recalibration complète (révision des coefficients) |

La calibration porte sur :
- La grille #token par agent/skill
- Les seuils de profil ressource
- Les ratios de complexité par type de tâche

### 2.4 Profils ressource (3 profils)

| Profil | Contexte | Règles |
|--------|----------|--------|
| **NORMAL** | Ressources standards | Aucune restriction, utilisation de tous les skills |
| **ECO** | Discussion courte (< 5 sessions) | Réduction des étapes de surveillance, snippets simplifiés |
| **VIEUX PC** | Environnement limité | Scripts légers, pas de graphiques lourds, profil ECO renforcé |

### 2.5 Intégration KB (gen-plan >= v3.3.0)

Depuis v3.3.0, gen-plan intègre un **Registre KB** (Knowledge Base) :

- **`kb_path`** : chemin vers `skills/KNOWLEDGE.md`
- **`--kb-skill`** : flag pour activer la consultation KB
- **Protocole de Découverte** : scan du registre pour identifier les skills pertinents
- **Matrice de décision** : agent × skill (statique + dynamique via KB)

---

## §3 — RELATIONS AVEC LES AUTRES SKILLS

### 3.1 correct-work
- **Relation** : Utilisé à l'**Étape 1** (validation initiale)
- **Sens** : gen-plan invoque correct-work pour vérifier la cohérence du plan initial
- **Version minimale** : correct-work >= v2.2.0

### 3.2 clone-chat
- **Relation** : Intervient aux étapes **E1-E7, E4, E15**
- **Sens** : clone-chat utilise les données de calibration de gen-plan pour le tagging #token. En retour, gen-plan peut déclencher clone-chat à E15 pour archiver la session.
- **Version minimale** : clone-chat >= v1.2.0
- **Optionnel** : clone-chat fonctionne sans gen-plan (autonome)

### 3.3 skills-inventory
- **Relation** : Utilisé à l'**Étape 5** (sélection des skills)
- **Sens** : gen-plan interroge skills-inventory pour lister les skills disponibles et leurs capacités

### 3.4 knowledge.md
- **Relation** : Utilisé à l'**Étape 15** (bilan)
- **Sens** : gen-plan enrichit KNOWLEDGE.md avec les retours d'expérience de la session (nouvelles calibrations, corrections de specs)

---

## §4 — YAML FRONTMATTER

Le fichier `SKILL.md` doit commencer par ce YAML frontmatter :

```yaml
---
name: gen-plan
version: 3.5.0
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
    version: ">=2.2.0"
    used_at: "E1"
  - skill: clone-chat
    version: ">=1.2.0"
    used_at: "E1-E7, E4, E15"
    optional: true
  - skill: skills-inventory
    version: ">=1.0.0"
    used_at: "E5"
  - skill: knowledge.md
    version: ">=1.0.0"
    used_at: "E15"
---
```

---

## §5 — INSTRUCTIONS D'INSTALLATION

### 5.1 Créer la structure de répertoires

```bash
mkdir -p skills/gen-plan/references
mkdir -p skills/gen-plan/evals
```

### 5.2 Créer le fichier SKILL.md

Le fichier `SKILL.md` (environ 8.5 Ko, ~275 lignes) doit contenir :

1. **YAML frontmatter** (voir §4)
2. **§0 — Règle zéro** : Tout est à créer, pas de « conserver »
3. **§1 — Spécification fonctionnelle** : 4 modes, 15 étapes, classification, tagging, normes N1-N3
4. **§2 — Spécification technique** : Stack, structure fichiers, auto-calibration, profils, intégration KB
5. **§3 — Relations** : correct-work, clone-chat, skills-inventory, knowledge.md
6. **§4 — Grille #token** : Tableau de calibration par agent/skill
7. **§5 — Conventions** : Nommage, Python uniquement, tagging, snippets

### 5.3 Créer les fichiers de référence

#### `references/etapes-detaillees.md`
Détail de chaque étape E1-E15 avec :
- Objectif précis
- Inputs attendus
- Outputs produits
- Critères de validation
- Exemples concrets

#### `references/grille-token.md`
Grille complète de calibration #token :
- Par type de tâche (court/moyen/long)
- Par agent/skill
- Historique de calibration
- Coefficients d'ajustement

#### `references/classification-types.md`
Routage détaillé Type 1-4 :
- Indicateurs de déclenchement
- Skills à invoquer
- Exemples et contre-exemples
- Cas ambigus et règle de décision

#### `references/profils-ressource.md`
Détail des 3 profils :
- Seuils de déclenchement
- Restrictions spécifiques
- Optimisations par profil

### 5.4 Créer le fichier d'évaluation

#### `evals/evals.json`
Cas de test pour évaluer gen-plan :

```json
{
  "skill": "gen-plan",
  "version": "3.5.0",
  "evals": [
    {
      "id": "E1-classification",
      "name": "Classification correcte Type 1-4",
      "input": "Crée un rapport d'analyse",
      "expected_type": 1,
      "expected_skill": "docx"
    },
    {
      "id": "E2-token-estimation",
      "name": "Estimation #token cohérente",
      "input": "Tâche moyenne, 5-15 sessions",
      "expected_token_range": [3500, 5500],
      "expected_profile": "NORMAL"
    },
    {
      "id": "E3-plan-complet",
      "name": "Plan E1-E15 complet",
      "input": "Planifier la création d'un dashboard Next.js",
      "expected_steps": 15,
      "expected_type": 3
    },
    {
      "id": "E4-auto-calibration",
      "name": "Auto-calibration E15",
      "input": "Écart estimé 28%",
      "expected_action": "Ajustement paramétrage fin"
    },
    {
      "id": "E5-python-only",
      "name": "Scripts Python uniquement",
      "input": "Générer un script de traitement",
      "expected_language": "python",
      "forbidden": ["bash", "sh", "powershell"]
    }
  ]
}
```

### 5.5 Mettre à jour KNOWLEDGE.md

Ajouter l'entrée gen-plan dans le registre des skills (`skills/KNOWLEDGE.md`) :

```markdown
## gen-plan
- **Version** : 3.5.0
- **Catégorie** : ecosystem
- **Fichier** : `skills/gen-plan/SKILL.md`
- **Description** : Planification de tâches, 4 modes, 15 étapes, 3 profils ressource, tagging #token, auto-calibration
- **Relations** : correct-work (E1), clone-chat (E1-E7, E4, E15), skills-inventory (E5), knowledge.md (E15)
```

### 5.6 Mettre à jour les cross-references

Mettre à jour les skills suivants pour référencer gen-plan :

- **correct-work** : Mentionner « Utilisé par gen-plan à l'Étape 1 »
- **clone-chat** : Mentionner « Intégration gen-plan optionnelle (E1-E7, E4, E15) »
- **skills-inventory** : Mentionner « Consulté par gen-plan à l'Étape 5 »

---

## §6 — VÉRIFICATION POST-INSTALLATION

Après installation, vérifier :

| # | Check | Critère | Résultat attendu |
|---|-------|---------|------------------|
| 1 | Fichier SKILL.md existe | `skills/gen-plan/SKILL.md` | File exists |
| 2 | Taille SKILL.md | ~8.5 Ko, ~275 lignes | Within range |
| 3 | YAML frontmatter valide | name, version, category, language, tags | All present |
| 4 | 4 fichiers référence | references/ contient 4 fichiers | 4 files |
| 5 | evals.json valide | JSON parsable, 5 evals | Valid JSON, 5 entries |
| 6 | Norme N3 (Python) | Aucune mention de shell/bash | No shell references |
| 7 | Cross-reference correct-work | Mention Étape 1 | Present |
| 8 | Cross-reference clone-chat | Mention E1-E7, E4, E15 | Present |
| 9 | Intégration KB | Mention kb_path, --kb-skill | Present |
| 10 | KNOWLEDGE.md mis à jour | Entrée gen-plan présente | Present |

---

## §7 — HISTORIQUE DES VERSIONS

| Version | Date | Changements |
|---------|------|-------------|
| v2.0.0 | 2026-07-18 | Version initiale (refusée par l'utilisateur) |
| v3.1.0 | 2026-07-18 | Refactoring complet suite refus v2.0.0 |
| v3.3.0 | 2026-07-29 | Ajout Registre KB, Protocole de Découverte |
| v3.5.0 | 2026-07-29 | Intégration clone-chat, calibration #token, normes N1-N3 |

---

## §8 — NOTES DE CONCEPTION

### 8.1 Pourquoi 15 étapes ?

Les 15 étapes couvrent le cycle de vie complet d'une tâche complexe : de l'analyse initiale (E1) au bilan post-exécution (E15). Chaque étape a un objectif clair, des inputs/outputs définis, et des critères de validation.

### 8.2 Pourquoi 3 profils ?

Les profils NORMAL/ECO/VIEUX PC permettent d'adapter la planification aux contraintes matérielles. Le profil ECO est conçu pour les discussions courtes, le profil VIEUX PC pour les environnements limités.

### 8.3 Pourquoi auto-calibration ?

L'estimation en tokens est intrinsèquement imprécise. L'auto-calibration E15 permet d'améliorer continuellement les estimations en comparant le prévu au réel, avec des seuils d'action clairs (20-35% ajustement, >35% recalibration).

### 8.4 Pourquoi Python uniquement ?

La règle N3 (Python uniquement) garantit la portabilité cross-platform. Les scripts shell sont dépendants du système d'exploitation, tandis que Python est universellement disponible dans l'environnement.