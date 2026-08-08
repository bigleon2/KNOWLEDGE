# PROMPT MAÎTRE — Installation du skill correct-work v2.3.0

> **Version du prompt** : 1.0.0
> **Skill cible** : correct-work v2.3.0
> **Date** : 2026-08-09
> **Source** : Écosystème Skills DJ — Clone de discussion
> **Dépend** : `PROMPT-MAITRE-SHARED.md` (lire en premier)

---

## PRÉREQUIS

Lire `PROMPT-MAITRE-SHARED.md` avant de continuer. Ce fichier contient le contexte commun, les conventions écosystème, les variables d'installation et le registre des relations.

Résumé des variables utiles (SHARED §1.1) :
- `{{SKILLS_ROOT}}` = `skills/`
- `{{KB_PATH}}` = `skills/KNOWLEDGE.md`
- `{{KB_ENABLED}}` = `true`

---

## §1 — SPÉCIFICATION FONCTIONNELLE

### 1.1 Description

correct-work est un skill de **vérification et correction** du travail réalisé par l'assistant IA. Il fournit un cadre structuré en 5 étapes et 3 modes pour inspecter, diagnostiquer et corriger tout artefact produit au cours d'une session.

### 1.2 Les 3 modes

| Mode | Nom | Description | Cas d'usage |
|------|-----|-------------|-------------|
| **PROJET** | Prompt-maître | Vérification complète d'un projet via son prompt maître | Validation finale d'un projet complexe |
| **CIBLE** | Ciblé | Vérification ciblée d'un skill ou fichier spécifique | Vérification d'un skill (ex: clone-chat) |
| **DIRECT** | Rapide | Vérification directe sans plan préalable | Correction rapide d'un fichier |

### 1.3 Les 5 étapes

| Étape | Nom | Description |
|-------|------|-------------|
| **1** | Plan d'actions via gen-plan | Création du plan de vérification via gen-plan (Étape 1) |
| **2** | Erreurs et omissions | Détection des erreurs factuelles, omissions, incohérences logiques |
| **3** | Structure et conflits | Vérification de la structure, conflits entre sections, cohérence du format |
| **4** | Vérification des interactions | Inspection des relations inter-skills, dépendances, interfaces |
| **5** | Cohérence des raisonnements | Vérification de la logique globale, cohérence argumentaire, décisions |

### 1.4 Intégration KB

Si `{{KB_ENABLED}}` est `true`, correct-work utilise le Registre KB de gen-plan :

- **`kb_path`** : chemin vers `{{KB_PATH}}`
- **`--kb-skill`** : flag pour cibler un skill spécifique
- **Matrice statique** : voir SHARED §4.1
- **Matrice dynamique** : construite à l'exécution en scannant `KNOWLEDGE.md` (SHARED §2.3)

---

## §2 — SPÉCIFICATION TECHNIQUE

### 2.1 Stack technique

- **Langage** : Markdown (documentation), YAML (frontmatter)
- **Environnement** : `{{SKILLS_ROOT}}correct-work/`
- **Pas de dépendance externe** (sauf gen-plan pour Étape 1)

### 2.2 Dépendances

| Dépendance | Version minimale | Utilisation |
|------------|-----------------|-------------|
| gen-plan | >= v3.6.0 | Étape 1 (plan d'actions) |
| clone-chat | >= v1.2.0 | Mode CIBLE (§3.5 Context Drift) |
| fullstack-dev | any | Vérification de projets web |

### 2.3 Structure des fichiers

```
{{SKILLS_ROOT}}correct-work/
└── SKILL.md                          # Skill principal (~481 lignes)
```

### 2.4 Format du rapport de vérification

```markdown
# Rapport correct-work — [Nom du projet/skill]

## Métadonnées
- **Date** : YYYY-MM-DD
- **Mode** : PROJET | CIBLE | DIRECT
- **Version correct-work** : 2.3.0
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

### 2.5 Matrice de décision

- **Matrice statique** : voir `PROMPT-MAITRE-SHARED.md §4` (référence unique)
- **Matrice dynamique** (si `{{KB_ENABLED}}`) : scan `{{KB_PATH}}` pour vérifier présence, version, compatibilité de chaque skill référencé.

### 2.6 Logging worklog

Voir SHARED §1.4 pour le format. Spécifiquement pour correct-work :

```markdown
---
Task ID: [task-id]
Agent: correct-work v2.3.0
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

### 2.7 Critères de sévérité

| Sévérité | Label | Description | Action requise |
|----------|-------|-------------|----------------|
| **S1** | Critique | Empêche le fonctionnement du skill | Correction immédiate obligatoire |
| **S2** | Majeur | Altère significativement le comportement | Correction dans cette session |
| **S3** | Mineur | Impact limité, cosmétique | Correction souhaitable, non bloquante |
| **S4** | Suggestion | Amélioration possible, pas de problème | Optionnel, pour info |

---

## §3 — RELATIONS

Voir `PROMPT-MAITRE-SHARED.md §3` pour le registre complet des relations inter-skills.

Relations directes de correct-work (extrait de SHARED §3.1) :

| Avec | Nature | Détails |
|------|--------|--------|
| gen-plan | Utilisation à Étape 1 | Création du plan de vérification, version >= v3.6.0 |
| clone-chat | Mode CIBLE | Vérification spécifique, §3.5 Context Drift, version >= v1.2.0 |
| fullstack-dev | Vérification | Validation de la structure et dépendances projets web |
| Skills KB | Consultation | Vérification présence et compatibilité des skills référencés |

---

## §4 — YAML FRONTMATTER

```yaml
---
name: correct-work
version: 2.3.0
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
    version: ">=3.6.0"
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

### 5.1 Créer la structure

```bash
mkdir -p {{SKILLS_ROOT}}correct-work
```

### 5.2 Créer le fichier SKILL.md

Le fichier `SKILL.md` (~481 lignes) doit contenir :

1. **YAML frontmatter** (voir §4)
2. **§0 — Règle zéro** (voir SHARED §0)
3. **§1 — Spécification fonctionnelle** : 3 modes, 5 étapes, intégration KB
4. **§2 — Spécification technique** : Stack, dépendances, rapport (§2.4), matrice dynamique (§2.5), logging (§2.6), sévérité (§2.7)
5. **§3 — Relations** : Voir SHARED §3 (résumé des relations directes)
6. **§4 — Grille de vérification** : Checklists par mode (voir §8)
7. **§5 — Conventions** : Nommage (SHARED §1.2), format rapport, verdicts (§7)

---

## §6 — VÉRIFICATION POST-INSTALLATION

| # | Check | Critère | Résultat attendu |
|---|-------|---------|------------------|
| 1 | SKILL.md existe | `{{SKILLS_ROOT}}correct-work/SKILL.md` | File exists |
| 2 | Taille SKILL.md | ~481 lignes | Within range |
| 3 | YAML frontmatter valide | name, version, category, language, tags | All present |
| 4 | 3 modes documentés | PROJET, CIBLE, DIRECT | All present |
| 5 | 5 étapes documentées | E1-E5 | All present |
| 6 | Intégration KB | Mention kb_path, --kb-skill | Present |
| 7 | Matrice statique | Voir SHARED §4 | Referenced |
| 8 | Matrice dynamique KB | Description du scan | Present |
| 9 | Critères de sévérité | S1-S4 | All present |
| 10 | Format rapport | Structure 5 sections | Present |
| 11 | Cross-ref gen-plan | Mention Étape 1, >= v3.6.0 | Present |
| 12 | Cross-ref clone-chat | Mention Mode CIBLE, §3.5 | Present |
| 13 | KNOWLEDGE.md | Entrée correct-work (SHARED §2.2) | Present |
| 14 | Logging worklog | Format documenté | Present |
| 15 | Dépendances frontmatter | gen-plan >=3.6.0, clone-chat >=1.2.0 | Correct |
| 16 | Compatibilité écosystème | 16/16 checks PASS | All PASS |

---

## §7 — HISTORIQUE DES VERSIONS

| Version | Date | Changements |
|---------|------|-------------|
| v1.0.0 | 2026-07-18 | Version initiale, vérification basique |
| v2.0.0 | 2026-07-29 | Ajout Mode CIBLE, amélioration du rapport |
| v2.1.0 | 2026-07-29 | Intégration gen-plan pour Étape 1 |
| v2.2.0 | 2026-07-29 | Registre KB (gen-plan >=3.3.0), kb_path, --kb-skill, matrice dynamique |
| v2.3.0 | 2026-08-09 | Refactoring prompt maître : extraction du socle commun SHARED, suppression de la duplication |

---

## §8 — HISTORIQUE DES CORRECTIONS (clone-chat)

### Round 1 (Session 17 → clone-chat v1.1.0)

| # | Problème | Sévérité | Correction |
|---|----------|----------|------------|
| 1 | Seuil in extenso < 500 lignes trop haut | S2 | Réduit à < 200 lignes |
| 2 | Chemins absolus dans §3.3 | S1 | Remplacés par chemins relatifs |
| 3-8 | Corrections structurelles | S2-S3 | Alignement SKILL.md ↔ template |

**Bilan** : 8 corrections.

### Round 2 (Sessions 21-22)

| # | Problème | Sévérité | Correction |
|---|----------|----------|------------|
| 1 | Template §5 ne mentionnait pas §0 | S2 | Ajout référence §0 |
| 2 | Règle « drift vide » absente | S2 | Ajout règle obligatoire |
| 3 | Décision #12 absente | S3 | Ajout décision intégration v2.2.0 |
| 4-9 | Autres problèmes | S2-S4 | Corrections diverses |

**Bilan** : 9 problèmes, 7 corrections.

### Round 3 (Session 23 → stabilisation)

| # | Problème | Sévérité | Correction |
|---|----------|----------|------------|
| 1 | « 7 étapes » vs « 7+1 étapes » | S2 | Unification en « 7+1 étapes » |
| 2 | Template §5 incomplet | S3 | Enrichissement |

**Bilan** : 2 problèmes, 2 corrections → **stabilisation atteinte**.

---

## §9 — NOTES DE CONCEPTION

### 9.1 Pourquoi 3 modes ?

Les 3 modes couvrent 3 niveaux de vérification : PROJET (lourd mais exhaustif, utilise le prompt maître comme référence), CIBLE (équilibre précision/effort, vérifie un skill précis), DIRECT (léger mais immédiat, correction rapide d'un fichier isolé). Le mode par défaut est CIBLE si l'utilisateur ne précise pas.

### 9.2 Pourquoi 5 étapes ?

Progression logique du plus évident au plus subtil : plan (via gen-plan) → contenu factuel → structure formelle → interactions entre composants → cohérence globale des raisonnements. Cette séquence garantit que les erreurs grossières (S1) sont détectées avant les problèmes subtils (S3-S4).

### 9.3 Pourquoi l'intégration KB ?

Sans KB, correct-work vérifie uniquement la matrice statique (SHARED §4). Avec KB, il découvre dynamiquement les skills disponibles, leurs versions réelles et leurs dépendances. La matrice dynamique est construite en temps réel via le Protocole de Découverte (SHARED §2.3), offrant une vérification plus précise et à jour.

### 9.4 Pourquoi la double matrice ?

La matrice statique garantit un fonctionnement minimum sans KB (fallback). La matrice dynamique enrichit la vérification quand KB est disponible. Ce pattern « statique + dynamique » assure la résilience : si KNOWLEDGE.md est absent ou corrompu, correct-work peut encore fonctionner avec la matrice intégrée.

---

## §10 — CHECKLISTS POUR LE SKILL.MD

Ces checklists doivent être intégrées dans la section §4 du SKILL.md.

### 10.1 Mode PROJET

```markdown
### Pré-vérification
- [ ] Le prompt maître est disponible et lisible
- [ ] La version du prompt maître est identifiée
- [ ] Les livrables attendus sont listés

### Phase 1 — Plan (via gen-plan E1)
- [ ] Plan de vérification créé via gen-plan
- [ ] Sections à vérifier identifiées
- [ ] Ordre de vérification défini
- [ ] Estimation #token faite

### Phase 2 — Erreurs et omissions
- [ ] Chaque section du prompt comparée au livrable
- [ ] Erreurs factuelles listées
- [ ] Omissions listées
- [ ] Chaque problème classé S1-S4

### Phase 3 — Structure et conflits
- [ ] Structure des fichiers vérifiée
- [ ] Conventions de nommage respectées
- [ ] Cross-references cohérentes
- [ ] Conflits entre sections détectés

### Phase 4 — Interactions
- [ ] Dépendances inter-skills vérifiées
- [ ] Versions minimales respectées
- [ ] Interfaces cohérentes

### Phase 5 — Cohérence
- [ ] Chaîne de raisonnement logique
- [ ] Décisions cohérentes entre elles
- [ ] Alignement décisions/actions vérifié

### Post-vérification
- [ ] Rapport produit
- [ ] Verdict assigné (PASS / PASS AVEC RÉSERVES / FAIL)
- [ ] Worklog mis à jour
```

### 10.2 Mode CIBLE

```markdown
### Pré-vérification
- [ ] Skill/fichier cible identifié
- [ ] Spécifications chargées (via KB si disponible)
- [ ] Version actuelle identifiée

### Vérification ciblée
- [ ] Structure cohérente
- [ ] Contenu correspond aux spécifications
- [ ] Cross-references correctes
- [ ] Dépendances vérifiées
- [ ] Format respecte les conventions

### Spécifique clone-chat (si applicable)
- [ ] §3.5 Context Drift présent
- [ ] Règle « drift vide » documentée
- [ ] 5 types de drift listés
- [ ] Table des drifts cohérente avec le worklog
- [ ] Format « 7+1 étapes » cohérent partout
- [ ] Chemins relatifs (pas absolus)
- [ ] Seuil in extenso < 200 lignes

### Post-vérification
- [ ] Corrections appliquées avec justification
- [ ] Worklog mis à jour
- [ ] Verdict assigné
```

### 10.3 Mode DIRECT

```markdown
### Inspection
- [ ] Artefact cible accessible
- [ ] Problèmes évidents identifiés
- [ ] Corrections appliquées immédiatement

### Post-correction
- [ ] La correction ne casse rien d'autre
- [ ] Worklog mis à jour (optionnel)
```

### 10.4 Sélection du mode

| Condition | Mode |
|-----------|-------|
| Un prompt maître existe pour le projet | PROJET |
| Un skill spécifique doit être vérifié | CIBLE |
| Correction rapide d'un fichier isolé | DIRECT |
| L'utilisateur ne précise pas | CIBLE (défaut) |
| Vérification complète + historique | PROJET |
| Le skill a déjà été vérifié (round 2+) | CIBLE |

### 10.5 Verdicts

- **PASS** : 0 problème S1-S2
- **PASS AVEC RÉSERVES** : 0 S1 mais >= 1 S2, ou >= 2 S3
- **FAIL** : >= 1 S1