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

---

## §9 — CONTENU IN EXTENSO DES FICHIERS RÉFÉRENCE

Les 4 fichiers de référence doivent être créés dans `skills/gen-plan/references/`. Voici leur contenu intégral :

### 9.1 `references/etapes-detaillees.md`

```markdown
# Détail des 15 étapes gen-plan

## E1 — Analyse de la demande

**Objectif** : Décortiquer la demande utilisateur pour en extraire les livrables, contraintes et critères de succès.

**Inputs** :
- Message ou demande brute de l'utilisateur
- Contexte de session (worklog, artefacts précédents)
- KNOWLEDGE.md (si disponible via KB)

**Outputs** :
- Liste des livrables identifiés
- Liste des contraintes (techniques, temporelles, ressources)
- Critères de succès explicites
- Questions clarificatoires (si ambiguïté)

**Critères de validation** :
- [ ] Au moins 1 livrable identifié
- [ ] Les contraintes sont explicites
- [ ] Le type de tâche est identifiable

**Exemple** :
> Demande : « Crée un rapport d'analyse des ventes du Q3 »
> Livrables : rapport.docx, graphiques PNG
> Contraintes : données Q3, format professionnel
> Critères : données exactes, visuels clairs

---

## E2 — Inventaire des ressources

**Objectif** : Faire le bilan de tout ce qui est disponible pour accomplir la tâche.

**Inputs** :
- Sortie de E1 (livrables, contraintes)
- `skills/` (liste des skills installés)
- `skills/KNOWLEDGE.md` (registre KB)
- Fichiers existants dans le projet

**Outputs** :
- Liste des skills disponibles et pertinents
- Liste des fichiers/sources de données existants
- Outils système disponibles
- Gaps identifiés (ressources manquantes)

**Critères de validation** :
- [ ] Skills pertinents identifiés
- [ ] Gaps clairement listés
- [ ] Pas de ressource critique manquante sans plan de contournement

---

## E3 — Classification du type de tâche

**Objectif** : Router la tâche vers le bon type de traitement (Type 1-4).

**Inputs** :
- Sortie de E1 (livrables)
- Sortie de E2 (ressources)
- Grille de classification (voir classification-types.md)

**Outputs** :
- Type assigné (1, 2, 3 ou 4)
- Skill principal à invoquer
- Skills secondaires éventuels
- Mode par défaut (M1-M4)

**Critères de validation** :
- [ ] Exactement 1 type assigné
- [ ] Skill principal identifié
- [ ] Pas de conflit type/skill

---

## E4 — Estimation #token

**Objectif** : Calculer le budget token de la tâche.

**Inputs** :
- Type de tâche (E3)
- Complexité estimée (simple/moyenne/complexe)
- Profil ressource cible (E6, si connu)
- Grille #token (voir grille-token.md)

**Outputs** :
- Estimation #token totale
- Estimation par étape
- Tag #token pour chaque skill utilisé

**Critères de validation** :
- [ ] Estimation dans la plage du profil
- [ ] Tags #token présents sur chaque élément du plan

---

## E5 — Sélection des skills

**Objectif** : Identifier les skills pertinents pour la tâche.

**Inputs** :
- Type de tâche (E3)
- Ressources disponibles (E2)
- skills-inventory (scan)
- KNOWLEDGE.md (KB)

**Outputs** :
- Liste ordonnée des skills à utiliser
- Version minimale requise pour chaque skill
- Nature de l'utilisation de chaque skill

**Critères de validation** :
- [ ] Chaque skill cité existe dans le registre ou l'inventaire
- [ ] Versions minimales cohérentes
- [ ] Pas de doublon

---

## E6 — Profilage ressource

**Objectif** : Choisir le profil de ressource adapté.

**Inputs** :
- Estimation #token (E4)
- Complexité de la tâche
- Contraintes matérielles (si connues)
- Grille des profils (voir profils-ressource.md)

**Outputs** :
- Profil assigné (NORMAL/ECO/VIEUX PC)
- Justification du choix
- Restrictions activées (si profil réduit)

**Critères de validation** :
- [ ] 1 profil assigné
- [ ] Justification cohérente avec les inputs

---

## E7 — Création du plan

**Objectif** : Assembler le plan d'exécution structuré.

**Inputs** :
- Livrables (E1)
- Skills sélectionnés (E5)
- Profil (E6)
- Estimation #token (E4)

**Outputs** :
- Plan structuré avec : étapes, dépendances, checkpoints, #token par étape
- TODO list ordonnée
- Identification des étapes parallélisables

**Critères de validation** :
- [ ] Toutes les étapes E9-E14 couvertes
- [ ] Dépendances explicites
- [ ] Checkpoints identifiés (au moins 1)
- [ ] #token total cohérent avec E4

---

## E8 — Validation du plan

**Objectif** : Vérifier la cohérence, la complétude et la faisabilité du plan.

**Inputs** :
- Plan brut (E7)
- Contraintes (E1)
- Grille de vérification interne

**Outputs** :
- Plan validé (ou plan révisé si corrections)
- Liste des risques identifiés
- Plan de contournement pour chaque risque

**Critères de validation** :
- [ ] Cohérence interne (pas de contradiction entre étapes)
- [ ] Complétude (tous les livrables couverts)
- [ ] Faisabilité (ressources suffisantes)
- [ ] Pas de cycle dans les dépendances

---

## E9 — Lancement de l'exécution

**Objectif** : Démarrer l'exécution selon le plan validé.

**Inputs** :
- Plan validé (E8)
- Contexte session

**Outputs** :
- Première étape lancée
- Entrée worklog initialisée

**Critères de validation** :
- [ ] Exécution démarrée
- [ ] Worklog initialisé

---

## E10 — Suivi d'étape

**Objectif** : Monitorer chaque étape en cours d'exécution.

**Inputs** :
- Plan en cours (E8)
- État réel de l'avancement

**Outputs** :
- Entrée worklog par étape terminée
- #token réel consommé par étape
- Écarts éventuels (réel vs estimé)

**Critères de validation** :
- [ ] Chaque étape terminée est loggée
- [ ] #token réel mesuré

---

## E11 — Checkpoint intermédiaire

**Objectif** : Vérification à mi-parcours.

**Inputs** :
- État d'avancement (E10)
- Plan initial (E8)

**Outputs** :
- Bilan mi-parcours
- Ajustements mineurs si nécessaire
- Decision : continuer / ajuster / arrêter

**Critères de validation** :
- [ ] Checkpoint effectué à ~50% du plan
- [ ] Décision documentée

---

## E12 — Détection d'écart

**Objectif** : Comparer le réel vs l'estimé.

**Inputs** :
- #token estimé (E4)
- #token réel (E10)
- Délais estimés vs réels

**Outputs** :
- Tableau des écarts
- Alertes si seuils dépassés

**Critères de validation** :
- [ ] Écarts calculés
- [ ] Alertes émises si > 20%

---

## E13 — Ajustement

**Objectif** : Modifier le plan en cas de dérive.

**Inputs** :
- Écarts (E12)
- Plan en cours (E8)

**Outputs** :
- Plan révisé (si nécessaire)
- Justification des modifications
- Nouvelle estimation si recalibration

**Critères de validation** :
- [ ] Modifications justifiées
- [ ] Plan révisé cohérent

---

## E14 — Finalisation

**Objectif** : Achèvement des étapes restantes.

**Inputs** :
- Plan (révisé ou non)
- État d'avancement

**Outputs** :
- Toutes les étapes terminées
- Livrables finaux produits
- Worklog complet

**Critères de validation** :
- [ ] Tous les livrables produits
- [ ] Worklog à jour

---

## E15 — Bilan et auto-calibration

**Objectif** : Retour d'expérience et mise à jour des grilles.

**Inputs** :
- Plan initial (E8)
- Worklog complet (E10-E14)
- #token estimé vs réel

**Outputs** :
- Bilan de la session
- Mise à jour grille #token (si écart > 20%)
- Enrichissement KNOWLEDGE.md
- Déclenchement éventuel de clone-chat

**Critères de validation** :
- [ ] Bilan produit
- [ ] Calibration mise à jour si nécessaire
- [ ] KNOWLEDGE.md enrichi si pertinent
```

### 9.2 `references/grille-token.md`

```markdown
# Grille de calibration #token — gen-plan v3.5.0

## Grille par agent/skill

| Agent/Skill | #token sortie (min) | #token sortie (max) | Coefficient complexité |
|-------------|--------------------|--------------------|----------------------|
| Planification E1-E2 | 800 | 1500 | 1.0x |
| Classification E3 | 200 | 500 | 1.0x |
| Estimation E4 | 300 | 800 | 1.0x |
| Sélection E5 | 500 | 1200 | 1.2x |
| Profilage E6 | 200 | 400 | 1.0x |
| Création plan E7 | 1000 | 2500 | 1.5x |
| Validation E8 | 500 | 1500 | 1.0x |
| Exécution simple (1 skill) | 2000 | 5000 | 1.0x |
| Exécution moyenne (2-3 skills) | 5000 | 10000 | 1.3x |
| Exécution complexe (4+ skills) | 10000 | 20000 | 1.5x |
| Surveillance E10-E12 | 500 | 1500 | 1.0x |
| Auto-calibration E15 | 800 | 2000 | 1.0x |

## Grille par type de tâche (usage clone-chat)

| Mode | Longueur discussion | #token estimé | Profil minimum |
|------|---------------------|---------------|-------------|
| clone-court | < 5 sessions | 2000-3500 | ECO |
| clone-moyen | 5-15 sessions | 3500-5500 | NORMAL |
| clone-long | > 15 sessions | 5500-9000 | NORMAL |

> Note v1.2.0 : estimation +10% pour couvrir l'Étape 3.5 Context Drift et l'intégration gen-plan.

## Coefficients d'ajustement

| Facteur | Coefficient | Condition |
|---------|-------------|-----------|
| Complexité faible | 0.8x | Tâche routinière, template existant |
| Complexité standard | 1.0x | Cas nominal |
| Complexité élevée | 1.3x | Multi-skills, dépendances croisées |
| Complexité critique | 1.5x | Projet nouveau, aucune référence |
| Profil ECO | 0.7x | Réduction surveillance, snippets simplifiés |
| Profil VIEUX PC | 0.5x | Scripts légers, pas de graphiques |

## Historique de calibration

| Exécution | Date | Type tâche | #token estimé | #token réel | Écart | Action |
|-----------|------|-----------|---------------|-------------|-------|--------|
| 1 | 2026-07-18 | Planification 66 skills | 4500 | 5200 | +15.6% | Aucune (0-20%) |
| 2 | 2026-07-18 | Test E2E gen-plan | 3000 | 3600 | +20.0% | Aucune (seuil) |
| 3 | 2026-07-29 | clone-chat v1.1.0 | 4000 | 5200 | +30.0% | Ajustement grille |
| 4 | 2026-07-29 | clone-chat v1.2.0 | 4400 | 4600 | +4.5% | Aucune (0-20%) |
```

### 9.3 `references/classification-types.md`

```markdown
# Classification des types de tâches — gen-plan E3

## Type 1 — Document Creation

**Indicateurs de déclenchement** :
- Mots-clés : rapport, document, article, analyse, proposition, PRD, script, manuscrit, présentation, tableur
- Formats mentionnés : DOCX, PDF, XLSX, PPTX, MD
- Verbes : rédiger, créer, générer, produire, écrire, composer

**Skill à invoquer** :
- docx → `docx`
- PDF → `pdf`
- Tableur → `xlsx`
- Présentation → `pptx`
- Markdown seul → aucun skill (rédaction directe)

**Exemples** :
- "Écris un rapport d'analyse" → Type 1, skill docx
- "Génère une présentation" → Type 1, skill pptx
- "Crée un tableur de suivi" → Type 1, skill xlsx

**Contre-exemples** :
- "Affiche ces données en graphique" → Type 2 (visualisation)
- "Construis une page web" → Type 3 (web dev)

---

## Type 2 — Data Visualization

**Indicateurs de déclenchement** :
- Mots-clés : graphique, chart, diagramme, mind map, flowchart, architecture, visualisation
- Formats mentionnés : PNG, SVG, Mermaid, D3, ECharts
- Verbes : tracer, dessiner, visualiser, représenter, générer un graphe

**Skill à invoquer** : `charts`

**Sous-routage charts** :
- Données chiffrées → matplotlib/seaborn/echarts
- Structure/diagramme → Mermaid ou Playwright+CSS
- Mind map → Playwright+CSS (pas matplotlib)
- Dashboard → charts d'abord, puis Type 3 si interactif

**Exemples** :
- "Trace un graphique d'évolution des ventes" → Type 2, charts (matplotlib)
- "Fais un diagramme de Gantt" → Type 2, charts (Mermaid)
- "Génère une mind map" → Type 2, charts (Playwright+CSS)

---

## Type 3 — Interactive Web Development

**Indicateurs de déclenchement** :
- Mots-clés : site web, application, dashboard interactif, page, interface, Next.js, React
- Mots-clés d'interactivité : cliquable, dynamique, temps réel, formulaire, navigation
- Verbes : construis, développe, crée une app, build

**Skill à invoquer** : `fullstack-dev`

**Exemples** :
- "Construis un dashboard interactif" → Type 3, fullstack-dev
- "Crée une application de gestion" → Type 3, fullstack-dev
- "Développe une page de landing" → Type 3, fullstack-dev

**Contre-exemples** :
- "Génère un dashboard en PDF" → Type 1 (document)
- "Affiche des données en graphique statique" → Type 2 (visualisation)

---

## Type 4 — Data Processing

**Indicateurs de déclenchement** :
- Mots-clés : analyse, traiter, transformer, calculer, extraire, filtrer, convertir
- Absence de livrable document final
- Focus sur le traitement de données

**Action** : Écrire un script Python directement

**Exemples** :
- "Analyse ce fichier CSV" → Type 4, script Python
- "Transforme ces données" → Type 4, script Python
- "Extrais les informations de ce PDF" → Type 4, script Python

---

## Cas ambigus — Règle de décision

| Situation | Règle | Type assigné |
|-----------|-------|-------------|
| "Dashboard" sans précision | Demander : interactif ou statique ? | Type 3 si interactif, Type 1/2 si statique |
| "Analyse" avec sortie document | Livrable = document | Type 1 |
| "Analyse" sans sortie | Traitement de données | Type 4 |
| "Visualisation" dans un document | Finalité = document | Type 1 (avec charts embarqués) |
| "Visualisation" autonome | Finalité = visuel | Type 2 |
| Mention de Next.js/React | Toujours web dev | Type 3 |
```

### 9.4 `references/profils-ressource.md`

```markdown
# Profils ressource — gen-plan v3.5.0

## NORMAL

**Contexte** : Ressources standards, environnement sans contrainte particulière.

**Déclenchement** : Par défaut, sauf si critères ECO ou VIEUX PC sont remplis.

**Règles** :
- Toutes les 15 étapes sont exécutées
- Tous les skills sont disponibles
- Surveillance complète (E10-E12)
- Snippets complets et versionnés
- Pas de restriction sur la taille des scripts
- Graphiques et visuels autorisés

**Seuils** :
- #token : pas de plafond
- Étapes de surveillance : E10, E11, E12 obligatoires
- Checkpoints : au moins 1 (E11)

---

## ECO

**Contexte** : Discussion courte ou tâche simple nécessitant une planification allégée.

**Déclenchement** :
- Discussion < 5 sessions
- #token estimé < 3500
- Tâche simple (1 skill, 1 livrable)
- Explicitement demandé par l'utilisateur

**Règles** :
- Étapes réduites : E1-E9 puis E14-E15 (E10-E13 fusionnées)
- Snippets simplifiés (pas de versionnage)
- Surveillance allégée (1 checkpoint unique à E11)
- Pas de matrice dynamique KB (statique seulement)

**Restrictions** :
- Pas de rapport de vérification détaillé
- Auto-calibration E15 simplifiée (ajustement seulement si > 35%)
- Pas de déclenchement clone-chat automatique

**Seuils** :
- #token plafond : 3500
- Surveillance : E11 uniquement

---

## VIEUX PC

**Contexte** : Environnement matériel limité (CPU lent, RAM limitée, pas de GPU).

**Déclenchement** :
- Explicitement demandé par l'utilisateur
- Environnement détecté comme limité

**Règles** :
- Toutes les règles ECO s'appliquent
- Scripts Python légers uniquement (pas de bibliothèques lourdes)
- Pas de graphiques Matplotlib/Seaborn (trop lourds)
- Pas de Playwright (trop lourd)
- Préférer les sorties Markdown/texte
- Templates minimalistes

**Restrictions supplémentaires** (par rapport à ECO) :
- Pas de génération d'images
- Pas de scripts > 100 lignes
- Préférer les algorithms O(n) aux O(n²)
- Pas de chargement de gros fichiers en mémoire

**Seuils** :
- #token plafond : 2000
- Taille script max : 100 lignes
- Pas de graphiques
```