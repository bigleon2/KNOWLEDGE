# PROMPT MAÎTRE — Installation du skill gen-plan v3.6.0

> **Version du prompt** : 1.0.0
> **Skill cible** : gen-plan v3.6.0
> **Date** : 2026-08-09
> **Source** : Écosystème Knowledge — Clone de discussion
> **Dépend** : `PROMPT-MAITRE-SHARED.md` (lire en premier)

---

## DÉCLENCHEURS

- `gen-plan:` suivi d'une description de tâche
- `gen-plan:correct-work(projet)` — vérification et correction d'un projet complet
- `gen-plan:correct-work(<cible>)` — vérification/correction d'un élément spécifique
- `plan d'actions` — demande explicite de planification
- `orchestre` — orchestration multi-agents
- Toute demande impliquant plusieurs étapes séquentielles avec des livrables
- `gen-plan:generate(<description>)` — génération d'un plan auto-exécutable

## PRÉREQUIS

Lire `PROMPT-MAITRE-SHARED.md` avant de continuer. Ce fichier contient le contexte commun, les conventions écosystème, les variables d'installation et le registre des relations.

Résumé des variables utiles (SHARED §1.1) :
- `{{SKILLS_ROOT}}` = `skills/`
- `{{KB_PATH}}` = `skills/KNOWLEDGE.md`
- `{{KB_ENABLED}}` = `true`
- `{{PROFILE_DEFAULT}}` = `NORMAL`

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
| E3 | Classification du type de tâche | Routage Type 1-4 (voir §8.3 pour le détail complet) | M1 |
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
| E15 | Bilan et auto-calibration | Retour d'expérience, mise à jour des grilles, enrichment KNOWLEDGE.md | M1/M4 |

### 1.4 Tagging #token (Norme N1)

Chaque étape et chaque skill utilisé reçoit un tag `#token` indiquant le coût estimé en tokens. La grille est auto-calibrée après exécutions (voir §8.2).

### 1.5 Snippets (Norme N2)

gen-plan peut générer des snippets de code réutilisables pendant l'exécution. Chaque snippet est tagué et versionné.

### 1.6 Python uniquement (Norme N3)

**Règle #7** : Tous les scripts générés par gen-plan doivent être en Python. Aucun script shell (bash, sh, powershell). Cette règle garantit la portabilité cross-platform.

### 1.7 Philosophie

1. **Read before planning** — Toujours lire le projet avant de planifier. Un plan sans connaissance du projet est générique et probablement inadéquat. La lecture exhaustive est un investissement nécessaire.
2. **Performance-driven selection** — Le choix entre skill, agent spécialisé ou agent général est dicté par le gain de performance, pas par une hiérarchie rigide. Un skill avec un protocole pertinent bat toujours un agent nu.
3. **Skills can launch specialized agents** — Les skills ne sont pas des terminaisons mais des orchestrateurs. Un skill chargé peut lancer en interne un agent spécialisé (full-stack-developer, ppt-expert, etc.). Modèle à deux couches : Skill (protocole + connaissances domaine) → Agent Spécialisé (exécution).
4. **Serial execution by DEFAULT** — Toutes les tâches s'exécutent UNE À LA UNE. Le parallélisme est INTERDIT sauf demande explicite de l'utilisateur ET preuve que les sous-tâches sont indépendantes.
5. **Visible progress** — L'utilisateur sait toujours quelle phase est en cours, ce qui est terminé, et ce qui vient ensuite.
6. **CoT + Chaining avec auto-correction** — Chaque étape est exécutée avec un raisonnement structuré (Chain-of-Thought) avant l'action. Le chainage suit un pipeline hiérarchique où chaque sortie est vérifiée et corrigée avant de passer à la suivante.
7. **Lecture bloc par bloc** — Les fichiers volumineux (> 500 lignes) sont lus par blocs successifs avec une synthèse intermédiaire à chaque bloc, évitant la surcharge de contexte et garantissant une couverture totale.

---

## §2 — SPÉCIFICATION TECHNIQUE

### 2.1 Stack technique

- **Langage** : Python (scripts), Markdown (documentation), YAML (frontmatter)
- **Environnement** : `{{SKILLS_ROOT}}gen-plan/`
- **Pas de dépendance externe** (sauf intégration KB si `{{KB_ENABLED}}`)

### 2.2 Structure des fichiers

```
{{SKILLS_ROOT}}gen-plan/
├── SKILL.md                          # Skill principal (~275 lignes)
├── references/
│   ├── etapes-detaillees.md          # Détail des 15 étapes
│   ├── grille-token.md               # Grille de calibration #token
│   ├── classification-types.md       # Routage Type 1-4
│   ├── profils-ressource.md          # NORMAL / ECO / VIEUX PC
│   └── guide-selection-agent-skill.md # Arbre de décision + tableau
└── evals/
    └── evals.json                    # Cas de test d'évaluation
```

### 2.3 Auto-calibration E15

| Écart estimé vs réel | Action |
|----------------------|--------|
| 0-20% | Aucune action (estimation fiable) |
| 20-35% | Ajustement de la grille (paramétrage fin) |
| >35% | Recalibration complète (révision des coefficients) |

La calibration porte sur : la grille #token par agent/skill, les seuils de profil ressource, les ratios de complexité par type de tâche.

### 2.4 Profils ressource

Détail complet dans §8.4. Résumé :

| Profil | Contexte | Règles clés |
|--------|----------|-------------|
| **NORMAL** | Par défaut | 15 étapes complètes, tous les skills, surveillance complète |
| **ECO** | Discussion < 5 sessions, #token < 3500 | Étapes réduites, 1 checkpoint, pas de matrice dynamique KB |
| **VIEUX PC** | Matériel limité | Règles ECO + scripts < 100 lignes, pas de graphiques |

### 2.5 Intégration KB

Si `{{KB_ENABLED}}` est `true` :

- **`kb_path`** : chemin vers `{{KB_PATH}}`
- **`--kb-skill`** : flag pour activer la consultation KB
- **Protocole de Découverte** : scan du registre pour identifier les skills pertinents (voir SHARED §2.3)

---

## §3 — RELATIONS

Voir `PROMPT-MAITRE-SHARED.md §3` pour le registre complet des relations inter-skills.

Relations directes de gen-plan (extrait de SHARED §3.1) :

| Avec | Nature | Détails |
|------|--------|--------|
| correct-work | Invocation à E1 | Validation du plan initial, version >= v2.3.0 |
| clone-chat | Calibration + archivage | E1-E7, E4, E15, optionnel, version >= v1.2.0 |
| skills-inventory | Consultation à E5 | Sélection des skills, version >= v1.0.0 |
| knowledge.md | Enrichissement à E15 | Mise à jour registre et calibration |

---

## §4 — YAML FRONTMATTER

```yaml
---
name: gen-plan
version: 3.6.0
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
    version: ">=2.3.0"
    used_at: "E1"
  - skill: clone-chat
    version: ">=1.2.0"
    used_at: "E1-E7, E4, E15"
    optional: true
  - skill: skills-inventory
    version: ">=1.0.0"
    used_at: "E5"
---
```

---

## §5 — INSTRUCTIONS D'INSTALLATION

### 5.1 Créer la structure

```bash
mkdir -p {{SKILLS_ROOT}}gen-plan/references
mkdir -p {{SKILLS_ROOT}}gen-plan/evals
```

### 5.2 Créer le fichier SKILL.md

Le fichier `SKILL.md` (~275 lignes, in extenso) doit contenir :

1. **YAML frontmatter** (voir §4)
2. **§0 — Règle zéro** (voir SHARED §0)
3. **§1 — Spécification fonctionnelle** : 4 modes, 15 étapes, normes N1-N3
4. **§2 — Spécification technique** : Stack, structure, auto-calibration, profils, KB
5. **§3 — Relations** : Voir SHARED §3 (résumé des relations directes)
6. **§4 — Grille #token** : Résumé de §8.2
7. **§5 — Conventions** : Nommage (SHARED §1.2), Python uniquement (N3), tagging

### 5.3 Créer les fichiers de référence

Le contenu in extenso de chaque fichier est en §8.

### 5.4 Créer evals/evals.json

```json
{
  "skill": "gen-plan",
  "version": "3.6.0",
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

---

## §6 — VÉRIFICATION POST-INSTALLATION

| # | Check | Critère | Résultat attendu |
|---|-------|---------|------------------|
| 1 | SKILL.md existe | `{{SKILLS_ROOT}}gen-plan/SKILL.md` | File exists |
| 2 | Taille SKILL.md | ~275 lignes | Within range |
| 3 | YAML frontmatter valide | name, version, category, language, tags | All present |
| 4 | 6 fichiers référence | `references/` contient 6 fichiers | 6 files |
| 5 | evals.json valide | JSON parsable, 5 evals | Valid JSON |
| 6 | Norme N3 (Python) | Aucune mention shell/bash | No shell refs |
| 7 | Intégration KB | Mention kb_path, --kb-skill | Present |
| 8 | KNOWLEDGE.md | Entrée gen-plan présente (SHARED §2.2) | Present |
| 9 | Cross-refs | correct-work et clone-chat mis à jour (SHARED §3.2) | Present |

---

## §7 — HISTORIQUE DES VERSIONS

| Version | Date | Changements |
|---------|------|-------------|
| v2.0.0 | 2026-07-18 | Version initiale (refusée par l'utilisateur) |
| v3.1.0 | 2026-07-18 | Refactoring complet suite refus v2.0.0 |
| v3.3.0 | 2026-07-29 | Ajout Registre KB, Protocole de Découverte |
| v3.5.0 | 2026-07-29 | Intégration clone-chat, calibration #token, normes N1-N3 |
| v3.6.0 | 2026-08-09 | Refactoring prompt maître : extraction du socle commun SHARED, suppression de la duplication |

---

## §8 — NOTES DE CONCEPTION

### 8.1 Pourquoi 15 étapes ?

Les 15 étapes couvrent le cycle de vie complet d'une tâche complexe : de l'analyse initiale (E1) au bilan post-exécution (E15). Chaque étape a un objectif clair, des inputs/outputs définis, et des critères de validation. La séquence E1-E8 (planification) est suivie de E9-E14 (exécution/surveillance) et clôturée par E15 (calibration). Ce découpage permet un parallélisme partiel (E9-E14 peuvent chevaucher M2/M3) tout en gardant un contrôle strict via E11 (checkpoint) et E12 (détection d'écart).

### 8.2 Pourquoi 3 profils ?

Les profils NORMAL/ECO/VIEUX PC permettent d'adapter la planification aux contraintes matérielles et à la complexité de la tâche. Le profil ECO est conçu pour les discussions courtes (< 5 sessions) ou les tâches simples (1 skill, 1 livrable), évitant la surcharge de planification. Le profil VIEUX PC ajoute des restrictions matérielles (scripts < 100 lignes, pas de graphiques, token plafonné à 2000) pour les environnements limités.

### 8.3 Pourquoi auto-calibration ?

L'estimation en tokens est intrinsèquement imprécise. L'auto-calibration E15 permet d'améliorer continuellement les estimations en comparant le prévu au réel, avec des seuils d'action clairs (20-35% ajustement paramétrage fin, >35% recalibration complète). L'historique de calibration (voir §9.2) trace les écarts successifs pour identifier les biais systématiques.

### 8.4 Pourquoi Python uniquement ?

La règle N3 (Python uniquement) garantit la portabilité cross-platform. Les scripts shell sont dépendants du système d'exploitation, tandis que Python est universellement disponible dans l'environnement de l'assistant. Cette contrainte simplifie aussi la maintenance et réduit les risques d'incompatibilité.

---

## §9 — CONTENU IN EXTENSO DES FICHIERS RÉFÉRENCE

Les 6 fichiers suivants doivent être créés dans `{{SKILLS_ROOT}}gen-plan/references/`. Voici leur contenu intégral.

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

---

## E2 — Inventaire des ressources

**Objectif** : Faire le bilan de tout ce qui est disponible pour accomplir la tâche.

**Inputs** :
- Sortie de E1 (livrables, contraintes)
- `{{SKILLS_ROOT}}` (liste des skills installés)
- `{{KB_PATH}}` (registre KB)
- Fichiers existants dans le projet

**Outputs** :
- Liste des skills disponibles et pertinents
- Liste des fichiers/sources de données existants
- Gaps identifiés (ressources manquantes)

**Critères de validation** :
- [ ] Skills pertinents identifiés
- [ ] Gaps clairement listés
- [ ] Pas de ressource critique manquante sans contournement

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
- Livrables (E1), Skills (E5), Profil (E6), #token (E4)

**Outputs** :
- Plan structuré : étapes, dépendances, checkpoints, #token par étape
- TODO list ordonnée
- Identification des étapes parallélisables

**Critères de validation** :
- [ ] Toutes les étapes E9-E14 couvertes
- [ ] Dépendances explicites
- [ ] Au moins 1 checkpoint
- [ ] #token total cohérent avec E4

---

## E8 — Validation du plan

**Objectif** : Vérifier cohérence, complétude et faisabilité.

**Inputs** :
- Plan brut (E7), Contraintes (E1)

**Outputs** :
- Plan validé (ou révisé)
- Liste des risques et plans de contournement

**Critères de validation** :
- [ ] Cohérence interne (pas de contradiction)
- [ ] Complétude (tous les livrables couverts)
- [ ] Faisabilité (ressources suffisantes)
- [ ] Pas de cycle dans les dépendances

---

## E9 — Lancement de l'exécution

**Objectif** : Démarrer l'exécution selon le plan validé.

**Inputs** : Plan validé (E8), Contexte session

**Outputs** : Première étape lancée, Entrée worklog initialisée

**Critères** : [ ] Exécution démarrée, [ ] Worklog initialisé

---

## E10 — Suivi d'étape

**Objectif** : Monitorer chaque étape en cours.

**Inputs** : Plan en cours (E8), État réel

**Outputs** : Entrée worklog par étape, #token réel, Écarts éventuels

**Critères** : [ ] Chaque étape terminée loggée, [ ] #token réel mesuré

---

## E11 — Checkpoint intermédiaire

**Objectif** : Vérification à mi-parcours.

**Inputs** : Avancement (E10), Plan initial (E8)

**Outputs** : Bilan mi-parcours, Ajustements mineurs, Décision (continuer/ajuster/arrêter)

**Critères** : [ ] Checkpoint à ~50%, [ ] Décision documentée

---

## E12 — Détection d'écart

**Objectif** : Comparer réel vs estimé.

**Inputs** : #token estimé (E4), #token réel (E10)

**Outputs** : Tableau des écarts, Alertes si > 20%

**Critères** : [ ] Écarts calculés, [ ] Alertes si seuil dépassé

---

## E13 — Ajustement

**Objectif** : Modifier le plan en cas de dérive.

**Inputs** : Écarts (E12), Plan en cours (E8)

**Outputs** : Plan révisé (si nécessaire), Justification, Nouvelle estimation

**Critères** : [ ] Modifications justifiées, [ ] Plan révisé cohérent

---

## E14 — Finalisation

**Objectif** : Achèvement des étapes restantes.

**Inputs** : Plan (révisé ou non), État d'avancement

**Outputs** : Toutes les étapes terminées, Livrables finaux, Worklog complet

**Critères** : [ ] Tous les livrables produits, [ ] Worklog à jour

---

## E15 — Bilan et auto-calibration

**Objectif** : Retour d'expérience et mise à jour des grilles.

**Inputs** : Plan initial (E8), Worklog complet, #token estimé vs réel

**Outputs** :
- Bilan de la session
- Mise à jour grille #token (si écart > 20%)
- Enrichissement KNOWLEDGE.md (si `{{KB_ENABLED}}`)
- Déclenchement éventuel de clone-chat

**Critères** : [ ] Bilan produit, [ ] Calibration mise à jour si nécessaire, [ ] KNOWLEDGE.md enrichi si pertinent
```

### 9.2 `references/grille-token.md`

```markdown
# Grille de calibration #token — gen-plan v3.6.0

## Grille par agent/skill

| Agent/Skill | #token sortie (min) | #token sortie (max) | Coeff. complexité |
|-------------|--------------------|--------------------|------------------|
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

| Mode | Longueur discussion | #token estimé | Profil min. |
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

**Indicateurs** :
- Mots-clés : rapport, document, article, analyse, proposition, PRD, script, manuscrit, présentation, tableur
- Formats : DOCX, PDF, XLSX, PPTX, MD
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

**Contre-exemples** :
- "Affiche ces données en graphique" → Type 2
- "Construis une page web" → Type 3

---

## Type 2 — Data Visualization

**Indicateurs** :
- Mots-clés : graphique, chart, diagramme, mind map, flowchart, architecture, visualisation
- Formats : PNG, SVG, Mermaid, D3, ECharts
- Verbes : tracer, dessiner, visualiser, représenter

**Skill** : `charts`

**Sous-routage** :
- Données chiffrées → matplotlib/seaborn/echarts
- Structure/diagramme → Mermaid ou Playwright+CSS
- Mind map → Playwright+CSS (pas matplotlib)
- Dashboard → charts d'abord, puis Type 3 si interactif

---

## Type 3 — Interactive Web Development

**Indicateurs** :
- Mots-clés : site web, application, dashboard interactif, page, interface, Next.js, React
- Interactivité : cliquable, dynamique, temps réel, formulaire, navigation
- Verbes : construis, développe, crée une app, build

**Skill** : `fullstack-dev`

**Contre-exemples** :
- "Génère un dashboard en PDF" → Type 1
- "Affiche des données en graphique statique" → Type 2

---

## Type 4 — Data Processing

**Indicateurs** :
- Mots-clés : analyse, traiter, transformer, calculer, extraire, filtrer, convertir
- Absence de livrable document final
- Focus sur le traitement de données

**Action** : Écrire un script Python directement

---

## Cas ambigus — Règle de décision

| Situation | Règle | Type |
|-----------|-------|------|
| "Dashboard" sans précision | Demander : interactif ou statique ? | 3 si interactif, 1/2 si statique |
| "Analyse" avec sortie document | Finalité = document | Type 1 |
| "Analyse" sans sortie | Traitement de données | Type 4 |
| "Visualisation" dans un document | Finalité = document | Type 1 (charts embarqués) |
| "Visualisation" autonome | Finalité = visuel | Type 2 |
| Mention Next.js/React | Toujours web dev | Type 3 |
```

### 9.4 `references/profils-ressource.md`

```markdown
# Profils ressource — gen-plan v3.6.0

## NORMAL

**Contexte** : Ressources standards, sans contrainte.
**Déclenchement** : Par défaut.

**Règles** :
- 15 étapes exécutées
- Tous les skills disponibles
- Surveillance complète (E10-E12)
- Snippets complets et versionnés
- Graphiques et visuels autorisés

**Seuils** : #token sans plafond, E10+E11+E12 obligatoires.

---

## ECO

**Contexte** : Discussion courte ou tâche simple.

**Déclenchement** :
- Discussion < 5 sessions
- #token estimé < 3500
- Tâche simple (1 skill, 1 livrable)
- Demande explicite de l'utilisateur

**Règles** :
- Étapes réduites : E1-E9 puis E14-E15 (E10-E13 fusionnées)
- Snippets simplifiés (pas de versionnage)
- 1 checkpoint unique à E11
- Pas de matrice dynamique KB (statique seulement)

**Restrictions** :
- Pas de rapport de vérification détaillé
- Auto-calibration E15 simplifiée (ajustement seulement si > 35%)
- Pas de déclenchement clone-chat automatique

---

## VIEUX PC

**Contexte** : Environnement matériel limité.

**Déclenchement** :
- Demande explicite de l'utilisateur
- Environnement détecté comme limité

**Règles** :
- Toutes les règles ECO s'appliquent
- Scripts Python légers uniquement (pas de bibliothèques lourdes)
- Pas de graphiques Matplotlib/Seaborn
- Pas de Playwright
- Préférer les sorties Markdown/texte

**Restrictions supplémentaires** :
- Pas de génération d'images
- Scripts < 100 lignes
- Préférer O(n) à O(n²)
- Pas de chargement de gros fichiers en mémoire

**Seuils** : #token plafond 2000, pas de graphiques.
```

### 9.5 `references/guide-selection-agent-skill.md`

```markdown
# Guide de Sélection Agent/Skill — gen-plan E5/E7

## Arbre de décision

```
1. Existe-t-il un SKILL correspondant ?
   |-- OUI -> Charger le skill
   |   |-- Le skill bénéficie-t-il d'un agent spécialisé ?
   |       |-- OUI -> Skill + Agent Spécialisé (OPTIMAL)
   |       |-- NON -> Skill seul via agent général (BON)
   |-- NON -> Existe-t-il un agent spécialisé ?
       |-- OUI -> Agent Spécialisé seul
       |-- NON -> Agent général (DERNIER RECOURS)
```

## Critères de sélection (ordonnés par impact performance)

1. **Skill + agent spécialisé** (meilleure performance) — Un skill dont le protocole correspond à la tâche ET qui délègue en interne à un agent spécialisé.
2. **Skill seul** (bonne performance) — Un skill dont le protocole couvre entièrement la tâche.
3. **Agent spécialisé seul** (performance modérée) — Aucun skill correspondant, mais un agent spécialisé couvre la tâche.
4. **Agent général** (fallback) — Ni skill ni agent spécialisé. Ne jamais utiliser comme premier choix.

## Tableau de correspondance

| Type de tâche | Skill | Agent | Performance |
|--------------|-------|-------|-------------|
| Dev web Next.js | fullstack-dev | full-stack-developer | OPTIMAL |
| Création PPT/slides | pptx | ppt-expert | OPTIMAL |
| Génération PDF | pdf | general-purpose | OPTIMAL |
| Compréhension images | VLM | general-purpose | OPTIMAL |
| Charts/diagrammes | charts | general-purpose | OPTIMAL |
| Documents Word | docx | general-purpose | BON |
| Fichiers Excel | xlsx | general-purpose | BON |
| Recherche web | web-search | general-purpose | BON |
| Extraction web | web-reader | general-purpose | BON |
| Création skills | skill-creator | general-purpose | BON |
| Génération images | image-generation | general-purpose | BON |
| Édition images | image-edit | general-purpose | BON |
| Speech-to-text | ASR | general-purpose | BON |
| Text-to-speech | TTS | general-purpose | BON |
| Video understanding | video-understand | general-purpose | BON |
| LLM chat | LLM | general-purpose | BON |
| Recherche images | image-search | general-purpose | BON |
| Navigation web | agent-browser | general-purpose | BON |
| Exploration fichiers | — | Explore | Agent seul |
| Architecture/planif | — | Plan | Agent seul |
| Styling CSS | — | frontend-styling-expert | Agent seul |
| Vérification correction | correct-work | general-purpose | BON |
```

### 9.6 Portées des étapes E8, E14 et E15 (qualité, intégration, auto-réapplication)

Les étapes E8, E14 et E15 incluent des portées héritées des versions antérieures du protocole :

**E8 — Validation du plan** inclut aussi les vérifications de qualité pré-intégration :
- [ ] Chaque fichier candidat à l'intégration est classifié : Skill / Écosystème / Utilitaire
- [ ] Les fichiers Skill ont un YAML frontmatter valide (name, description, > 200 chars)
- [ ] Les scripts Python compilent (pas de syntax error, imports valides)
- [ ] Les fichiers Markdown sont structurés (titres, sections cohérentes, pas de contenu tronqué)
- [ ] Les fichiers de configuration (JSON/YAML) sont valides
- [ ] Les références croisées entre fichiers sont valides

**E14 — Finalisation** inclut l'intégration écosystème :
- [ ] Les fichiers Skill sont placés dans `{{SKILLS_ROOT}}<nom>/SKILL.md`
- [ ] Les fichiers de référence vont dans `{{SKILLS_ROOT}}<nom>/references/`
- [ ] Aucun skill existant n'est écrasé sans confirmation utilisateur
- [ ] Le YAML frontmatter est conforme (SHARED §1.3)
- [ ] L'inventaire des skills est mis à jour si nécessaire

**E15 — Bilan** inclut l'auto-réapplication :
- [ ] Si le SKILL.md de gen-plan a été modifié pendant l'exécution, les tâches restantes sont réévaluées
- [ ] Les tâches affectées sont marquées `[REEVALUER]` avec la raison et les sections impactées
- [ ] Chaque réévaluation est documentée dans le worklog