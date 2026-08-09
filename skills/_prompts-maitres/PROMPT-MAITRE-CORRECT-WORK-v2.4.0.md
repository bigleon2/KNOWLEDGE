# PROMPT MAÎTRE — Installation du skill correct-work v2.4.0

> **Version du prompt** : 1.1.0
> **Skill cible** : correct-work v2.4.0
> **Date** : 2026-08-09
> **Source** : Écosystème Knowledge
> **Dépend** : `PROMPT-MAITRE-SHARED.md` (lire en premier)

---

## §A — DÉCLENCHEURS

- `verifie ton travail`
- `verifie tes résultats`
- `verifie ton code`
- `correct-work` ou `correct_work`
- `verify-work` (alias anglais)
- `correct-work(projet)` — vérification complète du projet
- `correct-work(<cible>)` — vérification ciblée sur un livrable
- `correct-work()` — vérification rapide sans analyse approfondie

Options avancées (gen-plan >= v3.6.0) :
- `correct-work(projet, kb_path=/chemin/KB)` — vérification avec scan des skills KB
- `correct-work(cible, --kb-skill=<name>)` — forcer l'utilisation d'un skill KB spécifique

## §B — PRÉREQUIS

Lire `PROMPT-MAITRE-SHARED.md` avant de continuer. Ce fichier contient le contexte commun, les conventions écosystème, les variables d'installation et le registre des relations.

Résumé des variables utiles (SHARED §1.1) :
- `{{SKILLS_ROOT}}` = `skills/`
- `{{KB_PATH}}` = `skills/KNOWLEDGE.md`
- `{{KB_ENABLED}}` = `true`

---

## §1 — SPÉCIFICATION FONCTIONNELLE

### §1.1 Description

correct-work est un skill de **vérification et correction** du travail réalisé par l'assistant IA. Il fournit un cadre structuré en 5 étapes et 3 modes pour inspecter, diagnostiquer et corriger tout artefact produit au cours d'une session. Supporte le multi-cibles, le découplage gen-plan optionnel, et les métriques de performance.

### §1.2 Les 3 modes

| Mode | Nom | Description | Cas d'usage |
|------|-----|-------------|-------------|
| **PROJET** | Prompt-maître | Vérification complète d'un projet via son prompt maître | Validation finale d'un projet complexe |
| **CIBLE** | Ciblé | Vérification ciblée d'un skill ou fichier spécifique (défaut) | Vérification d'un skill (ex: clone-chat) |
| **DIRECT** | Rapide | Vérification directe sans plan préalable | Correction rapide d'un fichier |

### §1.3 Les 5 étapes

| Étape | Nom | Description |
|-------|------|-------------|
| **1** | Plan d'actions | Création du plan de vérification (gen-plan si dispo, sinon autonome) |
| **2** | Erreurs et omissions | Détection des erreurs factuelles, omissions, incohérences logiques |
| **3** | Structure et conflits | Vérification de la structure, conflits entre sections, cohérence du format |
| **4** | Vérification des interactions | Inspection des relations inter-skills, dépendances, interfaces |
| **5** | Cohérence des raisonnements | Vérification de la logique globale, cohérence argumentaire, décisions |

### §1.4 Support multi-cibles

correct-work peut vérifier plusieurs artefacts dans une même session. Chaque cible reçoit un sous-rapport indépendant, et le rapport final agrège les résultats. Les verdicts sont calculés par cible puis globalement (le verdict global est le pire des verdicts individuels).

### §1.5 Découplage gen-plan

Le mode PROJET utilise gen-plan à l'Étape 1 pour créer le plan de vérification. Si gen-plan n'est pas disponible, correct-work fonctionne en mode autonome : il génère un plan simplifié (sections à vérifier dans l'ordre logique) sans estimation #token ni sélection de skills. Les modes CIBLE et DIRECT n'utilisent jamais gen-plan.

### §1.6 Intégration KB

Si `{{KB_ENABLED}}` est `true`, correct-work utilise le Registre KB :

- **`kb_path`** : chemin vers `{{KB_PATH}}`
- **`--kb-skill`** : flag pour cibler un skill spécifique
- **Matrice statique** : voir SHARED §4.1
- **Matrice dynamique** : construite à l'exécution en scannant `KNOWLEDGE.md` (SHARED §2.3)
- **verify-cross.py --mode correct-work** : 8 checks KB spécifiques

---

## §2 — SPÉCIFICATION TECHNIQUE

### §2.1 Stack technique

- **Langage** : Markdown (rapports), Python (scripts), YAML (frontmatter)
- **Environnement** : `{{SKILLS_ROOT}}correct-work/`
- **Pas de dépendance externe** (sauf intégration KB)

### §2.2 Dépendances

| Dépendance | Version minimale | Utilisation | Optionnelle |
|------------|-----------------|-------------|-------------|
| gen-plan | >= v3.6.0 | Étape 1 (plan d'actions) | Oui (autonome sinon) |
| clone-chat | >= v2.0.0 | Mode CIBLE (§3.5 Context Drift) | Oui |
| fullstack-dev | >= v1.0.0 | Vérification de projets web | Oui |

### §2.3 Structure des fichiers

```
{{SKILLS_ROOT}}correct-work/
├── SKILL.md              # Skill opérationnel (~315 lignes)
├── scripts/
│   └── verify-correct-work.py  # 16 checks post-install automatisés
└── evals/
    └── evals.json        # Cas de test d'évaluation
```

### §2.4 Format du rapport de vérification

```markdown
# Rapport correct-work — [Nom du projet/skill]

## Métadonnées
- **Date** : YYYY-MM-DD
- **Mode** : PROJET | CIBLE | DIRECT
- **Version correct-work** : 2.4.0
- **Cible** : [nom du skill/fichier] (ou multi-cibles)

## Étape 1 — Plan d'actions
[Plan généré via gen-plan ou autonome]

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

### §2.5 Matrice de décision

- **Matrice statique** : voir `PROMPT-MAITRE-SHARED.md §4` (référence unique)
- **Matrice dynamique** (si `{{KB_ENABLED}}`) : scan `{{KB_PATH}}` pour vérifier présence, version, compatibilité de chaque skill référencé.

### §2.6 Logging worklog

Voir SHARED §1.4 pour le format. Spécifiquement pour correct-work :

```markdown
---
Task ID: [task-id]
Agent: correct-work v2.4.0
Task: Vérification [mode] de [cible]

Work Log:
- Étape 1 : Plan d'actions créé (gen-plan ou autonome)
- Étape 2 : N erreurs détectées
- Étape 3 : N conflits structurels
- Étape 4 : N interactions vérifiées
- Étape 5 : Cohérence vérifiée

Stage Summary:
- N problèmes trouvés, N corrections appliquées
- Verdict : [PASS|PASS AVEC RÉSERVES|FAIL]
```

### §2.7 Critères de sévérité

| Sévérité | Label | Description | Action requise |
|----------|-------|-------------|----------------|
| **S1** | Critique | Empêche le fonctionnement du skill | Correction immédiate obligatoire |
| **S2** | Majeur | Altère significativement le comportement | Correction dans cette session |
| **S3** | Mineur | Impact limité, cosmétique | Correction souhaitable, non bloquante |
| **S4** | Suggestion | Amélioration possible, pas de problème | Optionnel, pour info |

### §2.8 Métriques de performance

Les métriques suivantes sont collectées pour chaque exécution de correct-work :

| Métrique | Description | Cible |
|----------|-------------|-------|
| `findings_total` | Nombre total de findings | Réduire au fil des sessions |
| `findings_par_étape` | Répartition E1-E5 | Identifier les étapes les plus productives |
| `taux_correction` | Corrections appliquées / findings trouvés | > 80% |
| `temps_par_mode` | Durée par mode (PROJET/CIBLE/DIRECT) | Baseline pour calibration |
| `faux_positifs` | Findings reclassés ou annulés | < 10% |

---

## §3 — RELATIONS

Voir `PROMPT-MAITRE-SHARED.md §3` pour le registre complet des relations inter-skills.

Relations directes de correct-work (extrait de SHARED §3.1) :

| Avec | Nature | Détails |
|------|--------|--------|
| gen-plan | Invocation à E1 | Plan de vérification (optionnel, autonome sinon), version >= v3.6.0 |
| clone-chat | Vérification Mode CIBLE | §3.5 Context Drift, version >= v2.0.0 |
| fullstack-dev | Vérification | Projets web : structure et dépendances, version >= v1.0.0 |
| knowledge.md | Scan dynamique | Découverte versions et dépendances |

---

## §4 — YAML FRONTMATTER

```yaml
---
name: correct-work
version: 2.4.0
category: ecosystem
language: fr
tags:
  - vérification
  - correction
  - quality-assurance
  - ecosystem
  - kb-integration
description: >
  Skill de vérification et correction du travail réalisé.
  5 étapes, 3 modes (PROJET/CIBLE/DIRECT),
  support multi-cibles, découplage gen-plan optionnel,
  intégration KB (Registre, kb_path, --kb-skill),
  matrice de décision agent/skill (statique + dynamique KB),
  métriques de performance.
dependencies:
  - skill: gen-plan
    version: ">=3.6.0"
    used_at: "Étape 1 (optionnel, mode PROJET)"
  - skill: clone-chat
    version: ">=2.0.0"
    used_at: "Mode CIBLE, §3.5 Context Drift"
  - skill: fullstack-dev
    version: ">=1.0.0"
    used_at: "Vérification projets web"
---
```

---

## §5 — INSTRUCTIONS D'INSTALLATION

### §5.1 Créer la structure

```bash
mkdir -p {{SKILLS_ROOT}}correct-work/scripts
mkdir -p {{SKILLS_ROOT}}correct-work/evals
```

### §5.2 Créer le fichier SKILL.md

Le fichier `SKILL.md` (~315 lignes, version compacte avec checklists intégrées) doit contenir :

1. **YAML frontmatter** (voir §4)
2. **§0 — Règle zéro** (voir SHARED §0)
3. **§1 — Spécification fonctionnelle** : 3 modes, 5 étapes, multi-cibles, découplage gen-plan, intégration KB
4. **§2 — Spécification technique** : Stack, dépendances, rapport (§2.4), matrice (§2.5), logging (§2.6), sévérité (§2.7), métriques (§2.8)
5. **§3 — Relations** : Voir SHARED §3 (résumé des relations directes)
6. **§4 — Checklists** : Par mode (§4.1-§4.3), sélection (§4.4), verdicts (§4.5), types projet (§4.6), détail étapes 2-5 (§4.7-§4.10)
7. **§5 — Conventions** : Nommage (SHARED §1.2), format rapport, verdicts

---

## §6 — VÉRIFICATION POST-INSTALLATION

| # | Check | Critère | Résultat attendu |
|---|-------|---------|------------------|
| 1 | SKILL.md existe | `{{SKILLS_ROOT}}correct-work/SKILL.md` | File exists |
| 2 | Taille SKILL.md | 200-350 lignes | Within range |
| 3 | YAML frontmatter valide | name, version, category, language, tags, dependencies | All present |
| 4 | 3 modes documentés | PROJET, CIBLE, DIRECT | All present |
| 5 | 5 étapes documentées | E1-E5 | All present |
| 6 | Intégration KB | Mention kb_path, --kb-skill | Present |
| 7 | Matrice statique | Voir SHARED §4 | Referenced |
| 8 | Matrice dynamique KB | Description du scan | Present |
| 9 | Critères de sévérité | S1-S4 | All present |
| 10 | Format rapport | Structure 5 sections, support multi-cibles | Present |
| 11 | Cross-ref gen-plan | Mention Étape 1, >= v3.6.0 | Present |
| 12 | Cross-ref clone-chat | Mention Mode CIBLE, §3.5 | Present |
| 13 | KNOWLEDGE.md | Entrée correct-work (SHARED §2.2) | Present |
| 14 | Logging worklog | Format documenté | Present |
| 15 | Dépendances frontmatter | gen-plan >=3.6.0, clone-chat >=2.0.0, fullstack-dev >=1.0.0 | Correct |
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
| v2.4.0 | 2026-08-09 | Support multi-cibles, découplage gen-plan (autonome), métriques de performance, checklists opérationnelles (§4.6-§4.10), scripts/ + evals/, hook gen-plan E8, verify-cross --mode correct-work (8 checks KB) |

---

## §8 — HISTORIQUE DES CORRECTIONS (clone-chat)

### §8.1 Round 1 (Session 17 → clone-chat v1.1.0)

| # | Problème | Sévérité | Correction |
|---|----------|----------|------------|
| 1 | Seuil in extenso < 500 lignes trop haut | S2 | Réduit à < 200 lignes |
| 2 | Chemins absolus dans §3.3 | S1 | Remplacés par chemins relatifs |
| 3-8 | Corrections structurelles | S2-S3 | Alignement SKILL.md ↔ template |

**Bilan** : 8 corrections.

### §8.2 Round 2 (Sessions 21-22)

| # | Problème | Sévérité | Correction |
|---|----------|----------|------------|
| 1 | Template §5 ne mentionnait pas §0 | S2 | Ajout référence §0 |
| 2 | Règle « drift vide » absente | S2 | Ajout règle obligatoire |
| 3 | Décision #12 absente | S3 | Ajout décision intégration v2.2.0 |
| 4-9 | Autres problèmes | S2-S4 | Corrections diverses |

**Bilan** : 9 problèmes, 7 corrections.

### §8.3 Round 3 (Session 23 → stabilisation)

| # | Problème | Sévérité | Correction |
|---|----------|----------|------------|
| 1 | « 7 étapes » vs « 7+1 étapes » | S2 | Unification en « 7+1 étapes » |
| 2 | Template §5 incomplet | S3 | Enrichissement |

**Bilan** : 2 problèmes, 2 corrections → **stabilisation atteinte**.

---

## §9 — NOTES DE CONCEPTION

### §9.1 Pourquoi 3 modes ?

Les 3 modes couvrent 3 niveaux de vérification : PROJET (lourd mais exhaustif, utilise le prompt maître comme référence), CIBLE (équilibre précision/effort, vérifie un skill précis), DIRECT (léger mais immédiat, correction rapide d'un fichier isolé). Le mode par défaut est CIBLE si l'utilisateur ne précise pas.

### §9.2 Pourquoi 5 étapes ?

Progression logique du plus évident au plus subtil : plan (via gen-plan ou autonome) → contenu factuel → structure formelle → interactions entre composants → cohérence globale des raisonnements. Cette séquence garantit que les erreurs grossières (S1) sont détectées avant les problèmes subtils (S3-S4).

### §9.3 Pourquoi l'intégration KB ?

Sans KB, correct-work vérifie uniquement la matrice statique (SHARED §4). Avec KB, il découvre dynamiquement les skills disponibles, leurs versions réelles et leurs dépendances. La matrice dynamique est construite en temps réel via le Protocole de Découverte (SHARED §2.3), offrant une vérification plus précise et à jour.

### §9.4 Pourquoi la double matrice ?

La matrice statique garantit un fonctionnement minimum sans KB (fallback). La matrice dynamique enrichit la vérification quand KB est disponible. Ce pattern « statique + dynamique » assure la résilience : si KNOWLEDGE.md est absent ou corrompu, correct-work peut encore fonctionner avec la matrice intégrée.

### §9.5 Pourquoi le découplage gen-plan ?

gen-plan est un skill lourd (15 étapes). Pour les vérifications simples (modes CIBLE et DIRECT), correct-work n'a pas besoin de gen-plan. Le mode PROJET l'utilise à l'Étape 1, mais si gen-plan est indisponible, correct-work bascule en mode autonome avec un plan simplifié. Cela réduit les dépendances et améliore la résilience.

### §9.6 Pourquoi le support multi-cibles ?

Une session de travail peut produire plusieurs livrables (ex : un SKILL.md + un script + un evals.json). Le support multi-cibles permet de tous les vérifier dans une seule exécution, avec un sous-rapport par cible et un verdict global.

---

## §10 — CHECKLISTS (SKILL.md)

Ces checklists sont intégrées dans la section §4 du SKILL.md. Elles sont divisées en deux parties : les checklists par mode de vérification (§10.1-§10.5) et les checklists opérationnelles détaillées par étape et type de projet (§10.6-§10.10).

### §10.1 Mode PROJET

```markdown
### Pré-vérification
- [ ] Le prompt maître est disponible et lisible
- [ ] La version du prompt maître est identifiée
- [ ] Les livrables attendus sont listés

### Phase 1 — Plan (via gen-plan ou autonome)
- [ ] Plan de vérification créé (gen-plan ou autonome)
- [ ] Sections à vérifier identifiées
- [ ] Ordre de vérification défini
- [ ] Estimation #token faite (si gen-plan disponible)

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

### §10.2 Mode CIBLE

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

### §10.3 Mode DIRECT

```markdown
### Inspection
- [ ] Artefact cible accessible
- [ ] Problèmes évidents identifiés
- [ ] Corrections appliquées immédiatement

### Post-correction
- [ ] La correction ne casse rien d'autre
- [ ] Worklog mis à jour (optionnel)
```

### §10.4 Sélection du mode

| Condition | Mode |
|-----------|-------|
| Un prompt maître existe pour le projet | PROJET |
| Un skill spécifique doit être vérifié | CIBLE |
| Correction rapide d'un fichier isolé | DIRECT |
| L'utilisateur ne précise pas | CIBLE (défaut) |
| Vérification complète + historique | PROJET |
| Le skill a déjà été vérifié (round 2+) | CIBLE |

### §10.5 Verdicts

- **PASS** : 0 problème S1-S2
- **PASS AVEC RÉSERVES** : 0 S1 mais >= 1 S2, ou >= 2 S3
- **FAIL** : >= 1 S1

---

## §10b — Checklists opérationnelles (Étapes 2-5)

Ces checklists sont utilisées pendant l'exécution du skill (Étapes 2-5). Elles sont adaptées au type de projet vérifié.

### §10.6 Adaptation au type de projet

| Type de projet | Étape 2 focus | Étape 3 focus | Étape 4 focus |
|---------------|---------------|---------------|---------------|
| **Fullstack** | Schema BDD, auth, endpoints | Imports circulaires, state | API frontend-backend, props, data flow |
| **Frontend only** | Responsive, accessibilité, composants | Conventions CSS, composants | Props, state management |
| **Backend/API** | Endpoints, validation, sécurité | Gestion erreurs, imports | Services, timeouts, CORS |
| **Document/PDF** | Contenu, mise en page, données | Cohérence sections, refs croisées | Références entre livrables |
| **Script/automatisation** | I/O, paramètres, sorties | Chemins en dur, gestion erreurs | Dépendances externes |
| **Écosystème skills** | Versions, frontmatter, deps | Cross-refs, conventions SHARED | Relations bidirectionnelles, KB |

### §10.7 Étape 2 — Erreurs et omissions (détail)

1. **Relire les spécifications initiales** de l'utilisateur et vérifier que chaque exigence a été satisfaite. Si une exigence a été oubliée, la réaliser maintenant.
2. **Vérifier les données factuelles** : noms, chemins, numéros de version, tailles de fichiers, counts — tout chiffre ou valeur assertée doit être vérifié contre la source réelle.
3. **Vérifier la cohérence linguistique** : la langue utilisée doit être identique à celle de la demande initiale. Pas de mélange incohérent.
4. **Vérifier les fichiers de sortie** : chaque fichier promis existe-t-il ? Est-il lisible ? Pas de fichier vide ou corrompu.
5. **Vérifier les dépendances** : les imports, les chemins de skill, les références croisées entre fichiers sont-ils corrects ?
6. **Adapter la vérification au projet** : les erreurs sont évaluées relativement au type de projet (cf. §10.6).
7. **Corriger** chaque erreur ou omission identifiée.

### §10.8 Étape 3 — Structure et conflits (détail)

1. **Imports circulaires** (code) : vérifier qu'aucun module n'importe un autre qui l'importe.
2. **Conflits de noms** : deux fonctions/classes/variables avec le même nom dans des scopes qui pourraient interférer.
3. **Variables non initialisées** ou utilisées avant d'être définies (code).
4. **Chemins en dur** qui ne fonctionneraient pas dans un autre environnement.
5. **Gestion des erreurs** : les cas d'erreur sont-ils traités ou le code échouerait silencieusement ?
6. **Doublons** : du code dupliqué qui devrait être factorisé, ou du contenu dupliqué dans un document.
7. **Convention de nommage** : cohérence dans le style (snake_case, PascalCase, kebab-case).
8. **Matrice de cohérence logique** : si des conditions booléennes complexes sont identifiées (XOR, exclusions mutuelles, guard clauses multiples), lister toutes les combinaisons possibles, vérifier que chaque combinaison est couverte par exactement une branche, détecter les branches mortes et les conflits.
9. **Corriger** chaque problème de structure ou conflit identifié.

### §10.9 Étape 4 — Interactions (détail)

1. **API frontend-backend** : chaque endpoint appelé existe-t-il ? Paramètres correspondants ? Codes d'erreur gérés ?
2. **Props et communication inter-composants** : types, noms, optionnalité, valeurs par défaut cohérents ?
3. **State management** : store expose-t-il toutes les données nécessaires ? Actions appelées aux bons moments ? State mort ?
4. **Flux de données bout en bout** : tracer un scénario complet (clic → API → store → re-render). Race conditions ?
5. **Communications entre services** : bons ports/URLs ? WebSockets ? Timeouts et réessais ?
6. **Références croisées entre livrables** : numéros de section corrects ? Données cohérentes ? Liens valides ?
7. **Corriger** chaque problème d'interaction identifié.

### §10.10 Étape 5 — Cohérence des raisonnements (détail)

1. **Cohérence logique** : les étapes de raisonnement s'enchaînent-elles logiquement ? Pas de saut non justifié.
2. **Cohérence numérique** : les chiffres s'additionnent-ils ? Pourcentages cohérents avec les valeurs absolues ?
3. **Cohérence temporelle** : dates, versions, chronologies cohérentes entre elles ?
4. **Résultat attendu vs obtenu** : ce qui a été promis correspond-il à ce qui a été livré ?
5. **Cohérence entre fichiers** : pas de contradiction entre le contenu de deux livrables.
6. **Corriger** toute incohérence identifiée.