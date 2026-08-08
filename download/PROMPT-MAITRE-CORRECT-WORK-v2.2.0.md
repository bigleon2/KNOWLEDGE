# PROMPT MAÎTRE — Installation du skill correct-work v2.2.0

> **Version du prompt** : 1.0.0
> **Skill cible** : correct-work v2.2.0
> **Date** : 2026-08-09
> **Source** : Écosystème Skills DJ — Clone de discussion

---

## §0 — CONTEXTE

Tu es un assistant IA (Z AI / GLM) dans l'environnement `my-project/`. L'utilisateur souhaite installer le skill **correct-work v2.2.0**, un skill de vérification et correction du travail réalisé. Ce skill fait partie d'un écosystème de 72+ skills. Tu dois créer l'intégralité des fichiers du skill à partir de ce prompt maître.

**Règle zéro** : Ne pas utiliser le verbe « conserver » — tout est à créer.

---

## §1 — SPÉCIFICATION FONCTIONNELLE

### 1.1 Description

correct-work est un skill de **vérification et correction** du travail réalisé par l'assistant IA. Il fournit un cadre structuré en 5 étapes et 3 modes pour inspecter, diagnostiquer et corriger tout artefact produit au cours d'une session.

### 1.2 Les 3 modes

| Mode | Nom | Description | Cas d'usage |
|------|-----|-------------|-------------|
| **PROJET** | Prompt-maître | Vérification complète d'un projet via son prompt maître. Parcourt toutes les sections du prompt et vérifie la conformité du livrable. | Validation finale d'un projet complexe |
| **CIBLE** | Ciblé | Vérification ciblée d'un skill ou fichier spécifique. Se concentre sur un périmètre défini. | Vérification d'un skill particulier (ex: clone-chat) |
| **DIRECT** | Rapide | Vérification directe sans plan préalable. Inspection immédiate d'un artefact. | Correction rapide d'un fichier |

### 1.3 Les 5 étapes

| Étape | Nom | Description | Détail |
|-------|------|-------------|--------|
| **1** | Plan d'actions via gen-plan | Création du plan de vérification en utilisant gen-plan (Étape 1) | Identification des points à vérifier, priorisation, estimation |
| **2** | Erreurs et omissions | Détection des erreurs factuelles, des omissions de contenu, des incohérences logiques | Comparaison livrable vs spécifications, checklist de complétude |
| **3** | Structure et conflits | Vérification de la structure documentaire, des conflits entre sections, de la cohérence du format | Conventions de nommage, structure de fichiers, conflits cross-réferences |
| **4** | Vérification des interactions | Inspection des relations entre skills, des dépendances, des interfaces | Appels inter-skills, paramètres partagés, compatibilité versions |
| **5** | Cohérence des raisonnements | Vérification de la logique globale, de la cohérence argumentaire, des décisions | Chaîne de raisonnement, cohérence temporelle, alignement décisions/actions |

### 1.4 Intégration gen-plan v3.3.0+ (Registre KB)

Depuis v2.2.0, correct-work intègre le **Registre KB** de gen-plan :

- **`kb_path`** : chemin vers `skills/KNOWLEDGE.md` pour consulter le registre des skills
- **`--kb-skill`** : flag pour cibler un skill spécifique dans le registre KB
- **Matrice de décision agent × skill** : matrice statique (codée dans le skill) + matrice dynamique (construite via KB)
- **Protocole de Découverte** : scan du registre pour vérifier la compatibilité des skills référencés

---

## §2 — SPÉCIFICATION TECHNIQUE

### 2.1 Stack technique

- **Langage** : Markdown (documentation), YAML (frontmatter)
- **Environnement** : `my-project/skills/correct-work/`
- **Pas de dépendance externe** (sauf gen-plan optionnel pour Étape 1)

### 2.2 Dépendances

| Dépendance | Version minimale | Utilisation |
|------------|-----------------|-------------|
| gen-plan | >= v3.1.0 | Étape 1 (plan d'actions) |
| clone-chat | >= v1.2.0 | Mode CIBLE (§3.5 Context Drift) |
| fullstack-dev | any | Vérification de projets web |

### 2.3 Structure des fichiers

```
skills/correct-work/
└── SKILL.md                          # Skill principal (24 Ko, ~481 lignes)
```

### 2.4 Rapport de vérification

Le rapport produit par correct-work suit cette structure :

```markdown
# Rapport correct-work — [Nom du projet/skill]

## Métadonnées
- **Date** : YYYY-MM-DD
- **Mode** : PROJET | CIBLE | DIRECT
- **Version correct-work** : 2.2.0
- **Cible** : [nom du skill/fichier]

## Étape 1 — Plan d'actions
[Plan généré via gen-plan]

## Étape 2 — Erreurs et omissions
| # | Sévérité | Description | Emplacement | Correction proposée |
|---|----------|-------------|-------------|---------------------|

## Étape 3 — Structure et conflits
| # | Type | Description | Fichiers concernés | Résolution |
|---|------|-------------|-------------------|------------|

## Étape 4 — Interactions
| # | Skill A | Skill B | Type d'interaction | Statut |
|---|--------|--------|-------------------|--------|

## Étape 5 — Cohérence des raisonnements
| # | Point vérifié | Résultat | Détail |
|---|---------------|----------|--------|

## Résumé
- **Problèmes trouvés** : N
- **Corrections appliquées** : N
- **Problèmes restants** : N
- **Verdict** : PASS | PASS AVEC RÉSERVES | FAIL
```

### 2.5 Matrice de décision agent × skill

#### Matrice statique (codée dans le skill)

| Agent/Task Type | gen-plan | correct-work | clone-chat | skills-inventory | fullstack-dev |
|-----------------|----------|--------------|------------|------------------|---------------|
| Planification | ✅ orchestre | ✅ valide | — | ✅ consulte | — |
| Création document | ✅ E3 route | ✅ vérifie | — | — | — |
| Web dev | ✅ E3 route | ✅ vérifie | — | — | ✅ exécute |
| Clonage discussion | ✅ E1-E7 | ✅ Mode CIBLE | ✅ exécute | — | — |
| Data processing | ✅ E3 route | ✅ vérifie | — | — | — |

#### Matrice dynamique (via KB)

Construite à l'exécution en scannant `KNOWLEDGE.md` :
- Pour chaque skill référencé, vérifier sa présence dans le registre
- Vérifier la compatibilité de version
- Détecter les skills manquants
- Signaler les conflits de dépendances

### 2.6 Logging worklog

Chaque exécution de correct-work génère une entrée dans le worklog :

```markdown
---
Task ID: [task-id]
Agent: correct-work v2.2.0
Task: Vérification [mode] de [cible]

Work Log:
- Étape 1 : Plan d'actions créé (gen-plan)
- Étape 2 : N erreurs détectées
- Étape 3 : N conflits structurels
- Étape 4 : N interactions vérifiées
- Étape 5 : Cohérence vérifiée

Stage Summary:
- N problèmes trouvés, N corrections appliquées
- Verdict : [PASS|PASS AVEC RÉSERVES|FAIL]
```

---

## §3 — RELATIONS AVEC LES AUTRES SKILLS

### 3.1 gen-plan
- **Relation** : correct-work utilise gen-plan à l'**Étape 1** pour créer le plan de vérification
- **Sens** : gen-plan orchestre la vérification, correct-work exécute
- **Version minimale** : gen-plan >= v3.1.0
- **Registre KB** : Depuis gen-plan v3.3.0, correct-work utilise `kb_path` et `--kb-skill`

### 3.2 clone-chat
- **Relation** : correct-work opère en **Mode CIBLE** sur clone-chat
- **Sens** : Vérification spécifique du skill clone-chat, notamment le §3.5 Context Drift
- **Version minimale** : clone-chat >= v1.2.0
- **Historique** : 3 rounds de correction ont été effectués (sessions 17, 21-23) :
  - Round 1 (session 17) : 8 corrections
  - Round 2 (session 21-22) : 9 problèmes, 7 corrections
  - Round 3 (session 23) : 2 problèmes, 2 corrections (stabilisation)

### 3.3 fullstack-dev
- **Relation** : correct-work vérifie les projets web
- **Sens** : Validation de la structure, des dépendances, des interfaces

### 3.4 Skills KB
- **Relation** : correct-work consulte le registre des skills
- **Sens** : Vérification de la présence et compatibilité des skills référencés

---

## §4 — YAML FRONTMATTER

Le fichier `SKILL.md` doit commencer par ce YAML frontmatter :

```yaml
---
name: correct-work
version: 2.2.0
category: ecosystem
language: fr
tags:
  - verification
  - correction
  - quality-assurance
  - ecosystem
  - kb-integration
description: >
  Skill de vérification et correction du travail réalisé.
  5 étapes, 3 modes (PROJET/CIBLE/DIRECT),
  intégration gen-plan v3.3.0+ (Registre KB, kb_path, --kb-skill),
  matrice de décision agent/skill (statique + dynamique KB).
dependencies:
  - skill: gen-plan
    version: ">=3.1.0"
    used_at: "Étape 1"
  - skill: clone-chat
    version: ">=1.2.0"
    used_at: "Mode CIBLE, §3.5 Context Drift"
  - skill: fullstack-dev
    version: ">=1.0.0"
    used_at: "Vérification projets web"
---
```

---

## §5 — INSTRUCTIONS D'INSTALLATION

### 5.1 Créer la structure de répertoires

```bash
mkdir -p skills/correct-work
```

### 5.2 Créer le fichier SKILL.md

Le fichier `SKILL.md` (environ 24 Ko, ~481 lignes) doit contenir :

1. **YAML frontmatter** (voir §4)
2. **§0 — Règle zéro** : Tout est à créer, pas de « conserver »
3. **§1 — Spécification fonctionnelle** : 3 modes, 5 étapes, intégration KB
4. **§2 — Spécification technique** : Stack, dépendances, rapport, matrices, logging
5. **§3 — Relations** : gen-plan, clone-chat, fullstack-dev, Skills KB
6. **§4 — Grille de vérification** : Checklist par mode et par étape
7. **§5 — Conventions** : Nommage, format rapport, critères de sévérité

### 5.3 Contenu détaillé du SKILL.md

#### Section « Grille de vérification par mode »

**Mode PROJET (prompt-maître)** :
- Lire le prompt maître complet
- Pour chaque section du prompt, vérifier la conformité du livrable
- Comparer les spécifications vs la réalisation
- Produire un rapport complet 5 étapes

**Mode CIBLE (ciblé)** :
- Identifier le skill/fichier cible
- Charger les spécifications du skill (via KB si disponible)
- Vérifier la structure, le contenu, les relations
- Appliquer les corrections avec justification
- Cas d'usage typique : vérification de clone-chat (§3.5 Context Drift)

**Mode DIRECT (rapide)** :
- Inspecter directement l'artefact cible
- Identifier les problèmes évidents
- Appliquer les corrections immédiates
- Pas de plan préalable, pas de rapport structuré

#### Section « Critères de sévérité »

| Sévérité | Label | Description | Action requise |
|----------|-------|-------------|----------------|
| **S1** | Critique | Empêche le fonctionnement du skill | Correction immédiate obligatoire |
| **S2** | Majeur | Altère significativement le comportement | Correction dans cette session |
| **S3** | Mineur | Impact limité, cosmétique | Correction souhaitable, non bloquante |
| **S4** | Suggestion | Amélioration possible, pas de problème | Optionnel, pour info |

### 5.4 Mettre à jour KNOWLEDGE.md

Ajouter l'entrée correct-work dans le registre des skills (`skills/KNOWLEDGE.md`) :

```markdown
## correct-work
- **Version** : 2.2.0
- **Catégorie** : ecosystem
- **Fichier** : `skills/correct-work/SKILL.md`
- **Description** : Vérification et correction, 5 étapes, 3 modes (PROJET/CIBLE/DIRECT), intégration gen-plan KB
- **Relations** : gen-plan (Étape 1), clone-chat (Mode CIBLE, §3.5), fullstack-dev (projets web)
```

### 5.5 Mettre à jour les cross-references

Mettre à jour les skills suivants pour référencer correct-work :

- **gen-plan** : Mentionner « correct-work utilisé à l'Étape 1 pour validation du plan »
- **clone-chat** : Mentionner « Vérifié par correct-work en Mode CIBLE (3 rounds, sessions 17, 21-23) »

---

## §6 — VÉRIFICATION POST-INSTALLATION

Après installation, vérifier :

| # | Check | Critère | Résultat attendu |
|---|-------|---------|------------------|
| 1 | Fichier SKILL.md existe | `skills/correct-work/SKILL.md` | File exists |
| 2 | Taille SKILL.md | ~24 Ko, ~481 lignes | Within range |
| 3 | YAML frontmatter valide | name, version, category, language, tags | All present |
| 4 | 3 modes documentés | PROJET, CIBLE, DIRECT | All present |
| 5 | 5 étapes documentées | E1-E5 | All present |
| 6 | Intégration KB | Mention kb_path, --kb-skill, Registre KB | Present |
| 7 | Matrice statique | Tableau agent × skill | Present |
| 8 | Matrice dynamique KB | Description du scan KNOWLEDGE.md | Present |
| 9 | Critères de sévérité | S1-S4 documentés | All present |
| 10 | Format rapport | Structure 5 sections | Present |
| 11 | Cross-reference gen-plan | Mention Étape 1, version >=3.1.0 | Present |
| 12 | Cross-reference clone-chat | Mention Mode CIBLE, §3.5 | Present |
| 13 | KNOWLEDGE.md mis à jour | Entrée correct-work présente | Present |
| 14 | Logging worklog | Format d'entrée worklog documenté | Present |
| 15 | Dépendance gen-plan | >= v3.1.0 dans frontmatter | Correct |
| 16 | Dépendance clone-chat | >= v1.2.0 dans frontmatter | Correct |
| 17 | Compatibilité écosystème | 17/17 checks PASS | All PASS |

---

## §7 — HISTORIQUE DES VERSIONS

| Version | Date | Changements |
|---------|------|-------------|
| v1.0.0 | 2026-07-18 | Version initiale, vérification basique |
| v2.0.0 | 2026-07-29 | Ajout Mode CIBLE, amélioration du rapport |
| v2.1.0 | 2026-07-29 | Intégration gen-plan pour Étape 1 |
| v2.2.0 | 2026-07-29 | Ajout Registre KB (gen-plan >=3.3.0), kb_path, --kb-skill, matrice dynamique, 3 rounds de correction clone-chat |

---

## §8 — HISTORIQUE DES CORRECTIONS (clone-chat)

Ce skill a été utilisé intensivement pour vérifier clone-chat. Voici l'historique des corrections appliquées :

### Round 1 (Session 17, correct-work v1.0.0 → clone-chat v1.1.0)

| # | Problème | Sévérité | Correction |
|---|----------|----------|------------|
| 1 | Seuil in extenso < 500 lignes trop haut | S2 | Réduit à < 200 lignes (recommandation correct-work) |
| 2 | Chemins absolus dans §3.3 | S1 | Remplacés par chemins relatifs (convention clone-chat) |
| 3-8 | Autres corrections structurelles | S2-S3 | Alignement SKILL.md ↔ template |

**Bilan** : 8 corrections, clone-chat v1.0.0 → v1.1.0

### Round 2 (Sessions 21-22, correct-work v2.2.0)

| # | Problème | Sévérité | Correction |
|---|----------|----------|------------|
| 1 | Template §5 ne mentionnait pas §0 | S2 | Ajout référence §0 dans template §5 |
| 2 | Règle « drift vide » absente | S2 | Ajout : « Aucune évolution détectée » certifie l'analyse |
| 3 | Décision #12 absente | S3 | Ajout décision « Intégrer correct-work v2.2.0 » |
| 4-9 | Autres problèmes | S2-S4 | Corrections diverses |

**Bilan** : 9 problèmes détectés, 7 corrections appliquées

### Round 3 (Session 23, correct-work v2.2.0)

| # | Problème | Sévérité | Correction |
|---|----------|----------|------------|
| 1 | Cohérence « 7 étapes » vs « 7+1 étapes » | S2 | Unification en « 7+1 étapes » partout |
| 2 | Template §5 incomplet | S3 | Enrichissement du template |

**Bilan** : 2 problèmes, 2 corrections → **stabilisation atteinte**

---

## §9 — NOTES DE CONCEPTION

### 9.1 Pourquoi 3 modes ?

Les 3 modes couvrent les 3 niveaux de vérification nécessaires :
- **PROJET** : validation complète d'un projet (lourde mais exhaustive)
- **CIBLE** : vérification ciblée d'un skill (équilibre précision/effort)
- **DIRECT** : correction rapide (légère mais immédiate)

### 9.2 Pourquoi 5 étapes ?

Les 5 étapes suivent un progression logique : plan → contenu → structure → interactions → cohérence. Chaque étape ajoute une couche de vérification, des plus évidentes (erreurs factuelles) aux plus subtiles (cohérence des raisonnements).

### 9.3 Pourquoi l'intégration KB ?

L'intégration du Registre KB de gen-plan permet à correct-work de vérifier automatiquement la compatibilité des skills référencés. Sans KB, correct-work ne peut vérifier que ce qui est codé en dur (matrice statique). Avec KB, il peut découvrir dynamiquement les skills disponibles et leurs versions.

### 9.4 Pourquoi la matrice agent × skill ?

La double matrice (statique + dynamique) permet de couvrir à la fois les relations connues (codées en dur) et les relations découvertes (via KB). La matrice statique garantit un fonctionnement minimum même sans KB, tandis que la matrice dynamique enrichit la vérification quand KB est disponible.

### 9.5 Pourquoi le logging worklog ?

Le logging systématique dans le worklog permet de tracer l'historique des vérifications. C'est essentiel pour le suivi qualité au fil des sessions et pour le Context Drift de clone-chat (qui utilise le worklog comme source).