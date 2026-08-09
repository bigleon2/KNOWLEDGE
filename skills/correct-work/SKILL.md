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

## §0 — Règle zéro

Écosystème Knowledge : 78 skills (6 écosystème + 72 métier). Chaque skill versionné semver, dépendances déclarées en YAML, cross-refs bidirectionnelles, registre KB unique (`skills/KNOWLEDGE.md`). Voir `PROMPT-MAITRE-SHARED.md §0`.

---

## §1 — Spécification fonctionnelle

### §1.1 Description

Skill de vérification et correction du travail réalisé. 5 étapes progressives, 3 modes de vérification, support multi-cibles, intégration au registre KB.

### §1.2 Les 3 modes

| Mode | Nom | Quand l'utiliser |
|------|-----|-----------------|
| M1 | **PROJET** | Un prompt maître existe ; vérification exhaustive |
| M2 | **CIBLE** | Un skill/fichier spécifique à vérifier (défaut) |
| M3 | **DIRECT** | Correction rapide d'un fichier isolé |

### §1.3 Les 5 étapes

| Étape | Nom | Description |
|-------|------|-------------|
| E1 | Plan d'actions | Identifier sections, ordre, estimation #token (gen-plan si dispo, sinon autonome) |
| E2 | Erreurs et omissions | Comparer spécifications → livrable, classer S1-S4 |
| E3 | Structure et conflits | Imports, conventions, chemins, doublons, gestion erreurs |
| E4 | Interactions | Dépendances inter-skills, API frontend-backend, refs croisées |
| E5 | Cohérence | Raisonnement logique, cohérence numérique/temporelle, fichiers |

### §1.4 Support multi-cibles

Correct-work peut vérifier plusieurs artefacts dans une même session. Chaque cible reçoit un sous-rapport indépendant, et le rapport final agrège les résultats. Les verdicts sont calculés par cible puis globalement (le verdict global est le pire des verdicts individuels).

### §1.5 Découplage gen-plan

Le mode PROJET utilise gen-plan à l'Étape 1 pour créer le plan de vérification. Si gen-plan n'est pas disponible, correct-work fonctionne en mode autonome : il génère un plan simplifié (sections à vérifier dans l'ordre logique) sans estimation #token ni sélection de skills. Les modes CIBLE et DIRECT n'utilisent jamais gen-plan.

### §1.6 Intégration KB

Si `{{KB_ENABLED}}` = true, correct-work consulte `{{KB_PATH}}` pour découvrir dynamiquement les skills, versions et dépendances via le Protocole de Découverte (SHARED §2.3). Paramètre `--kb-skill` pour cibler un skill. La matrice dynamique est construite via `verify-cross.py --mode correct-work`.

---

## §2 — Spécification technique

### §2.1 Stack technique

- **Langage** : Markdown (rapports), Python (scripts)
- **Environnement** : `{{SKILLS_ROOT}}correct-work/`
- **Pas de dépendance externe** (sauf intégration KB)

### §2.2 Dépendances

| Dépendance | Version | Utilisation | Optionnelle |
|------------|---------|-------------|-------------|
| gen-plan | >= v3.6.0 | Étape 1 mode PROJET | Oui (autonome sinon) |
| clone-chat | >= v2.0.0 | Mode CIBLE §3.5 | Oui |
| fullstack-dev | >= v1.0.0 | Projets web | Oui |

### §2.3 Structure des fichiers

```
correct-work/
├── SKILL.md              # Skill opérationnel (~280 lignes)
├── scripts/
│   └── verify-correct-work.py  # 16 checks post-install automatisés
└── evals/
    └── evals.json        # Cas de test d'évaluation
```

### §2.4 Format du rapport

- **Métadonnées** : mode, portée, date, agent, cible(s)
- **Par cible** : findings classés par sévérité S1-S4, sous-rapport Étapes 1-5
- **Résumé** : verdict par cible + verdict global (PASS / PASS AVEC RÉSERVES / FAIL)

### §2.5 Sévérité

| Sévérité | Description | Action obligatoire |
|----------|-------------|-------------------|
| S1 | Critique : erreur fonctionnelle bloquante | Corriger immédiatement |
| S2 | Majeur : inexactitude ou manque significatif | Corriger |
| S3 | Mineur : incohérence légère, convention | Corriger si rapide |
| S4 | Suggestion : amélioration possible | Accepter tel quel |

### §2.6 Matrice de décision

- **Matrice statique** : voir SHARED §4.1
- **Matrice dynamique** (si `{{KB_ENABLED}}`) : `verify-cross.py --mode correct-work` scanne `{{KB_PATH}}` pour vérifier présence, version, compatibilité.

### §2.7 Logging worklog

Format SHARED §1.4. Spécifiquement pour correct-work : chaque entrée inclut le mode, la cible, le nombre de findings par sévérité et le verdict.

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

## §3 — Relations

Voir `PROMPT-MAITRE-SHARED.md §3` pour le registre complet.

| Avec | Nature | Détails |
|------|--------|--------|
| gen-plan | Invocation à E1 | Plan de vérification (optionnel), version >= v3.6.0 |
| clone-chat | Vérification Mode CIBLE | §3.5 Context Drift, version >= v2.0.0 |
| fullstack-dev | Vérification | Projets web : structure et dépendances |
| knowledge.md | Scan dynamique | Découverte versions et dépendances |

---

## §4 — Checklists

### §4.1 Mode PROJET

**Pré-vérification** :
- [ ] Le prompt maître est disponible et lisible
- [ ] La version du prompt maître est identifiée
- [ ] Les livrables attendus sont listés

**Phase 1 — Plan** :
- [ ] Plan de vérification créé (gen-plan ou autonome)
- [ ] Sections à vérifier identifiées
- [ ] Ordre de vérification défini
- [ ] Estimation #token faite (si gen-plan disponible)

**Phase 2 — Erreurs et omissions** :
- [ ] Chaque section du prompt comparée au livrable
- [ ] Erreurs factuelles listées
- [ ] Omissions listées
- [ ] Chaque problème classé S1-S4

**Phase 3 — Structure et conflits** :
- [ ] Structure des fichiers vérifiée
- [ ] Conventions de nommage respectées
- [ ] Cross-references cohérentes
- [ ] Conflits entre sections détectés

**Phase 4 — Interactions** :
- [ ] Dépendances inter-skills vérifiées
- [ ] Versions minimales respectées
- [ ] Interfaces cohérentes

**Phase 5 — Cohérence** :
- [ ] Chaîne de raisonnement logique
- [ ] Décisions cohérentes entre elles
- [ ] Alignement décisions/actions vérifié

**Post-vérification** :
- [ ] Rapport produit
- [ ] Verdict assigné (PASS / PASS AVEC RÉSERVES / FAIL)
- [ ] Worklog mis à jour

### §4.2 Mode CIBLE

**Pré-vérification** :
- [ ] Skill/fichier cible identifié
- [ ] Spécifications chargées (via KB si disponible)
- [ ] Version actuelle identifiée

**Vérification ciblée** :
- [ ] Structure cohérente
- [ ] Contenu correspond aux spécifications
- [ ] Cross-references correctes
- [ ] Dépendances vérifiées
- [ ] Format respecte les conventions

**Clone-chat** (si applicable) :
- [ ] §3.5 Context Drift présent
- [ ] Règle « drift vide » documentée
- [ ] 5 types de drift listés
- [ ] Table des drifts cohérente avec le worklog
- [ ] Format « 7+1 étapes » cohérent partout
- [ ] Chemins relatifs (pas absolus)
- [ ] Seuil in extenso < 200 lignes

**Post-vérification** :
- [ ] Corrections appliquées avec justification
- [ ] Worklog mis à jour
- [ ] Verdict assigné

### §4.3 Mode DIRECT

**Inspection** :
- [ ] Artefact cible accessible
- [ ] Problèmes évidents identifiés
- [ ] Corrections appliquées immédiatement

**Post-correction** :
- [ ] La correction ne casse rien d'autre
- [ ] Worklog mis à jour (optionnel)

### §4.4 Sélection du mode

| Condition | Mode |
|-----------|-------|
| Un prompt maître existe pour le projet | PROJET |
| Un skill spécifique doit être vérifié | CIBLE |
| Correction rapide d'un fichier isolé | DIRECT |
| L'utilisateur ne précise pas | CIBLE (défaut) |
| Vérification complète + historique | PROJET |
| Le skill a déjà été vérifié (round 2+) | CIBLE |

### §4.5 Verdicts

- **PASS** : 0 problème S1-S2
- **PASS AVEC RÉSERVES** : 0 S1 mais >= 1 S2, ou >= 2 S3
- **FAIL** : >= 1 S1

### §4.6 Adaptation au type de projet

| Type de projet | Étape 2 focus | Étape 3 focus | Étape 4 focus |
|---------------|---------------|---------------|---------------|
| **Fullstack** | Schema BDD, auth, endpoints | Imports circulaires, state | API frontend-backend, props, data flow |
| **Frontend only** | Responsive, accessibilité, composants | Conventions CSS, composants | Props, state management |
| **Backend/API** | Endpoints, validation, sécurité | Gestion erreurs, imports | Services, timeouts, CORS |
| **Document/PDF** | Contenu, mise en page, données | Cohérence sections, refs croisées | Références entre livrables |
| **Script/automatisation** | I/O, paramètres, sorties | Chemins en dur, gestion erreurs | Dépendances externes |
| **Écosystème skills** | Versions, frontmatter, deps | Cross-refs, conventions SHARED | Relations bidirectionnelles, KB |

### §4.7 Étape 2 — Erreurs et omissions (détail)

1. Relire les spécifications initiales et vérifier que chaque exigence est satisfaite
2. Vérifier les données factuelles : noms, chemins, numéros de version, tailles, counts
3. Vérifier la cohérence linguistique (même langue que la demande initiale)
4. Vérifier les fichiers de sortie : existence, lisibilité, non-vide
5. Vérifier les dépendances : imports, chemins de skill, références croisées
6. Adapter la vérification au type de projet (cf. §4.6)
7. Corriger chaque erreur ou omission identifiée

### §4.8 Étape 3 — Structure et conflits (détail)

1. Imports circulaires (code) : aucun module n'importe un autre qui l'importe
2. Conflits de noms : fonctions/classes/variables dans des scopes qui pourraient interférer
3. Variables non initialisées ou utilisées avant d'être définies
4. Chemins en dur qui ne fonctionneraient pas dans un autre environnement
5. Gestion des erreurs : cas d'erreur traités, pas d'échec silencieux
6. Doublons : code dupliqué à factoriser, contenu dupliqué dans un document
7. Convention de nommage : cohérence du style (snake_case, PascalCase, kebab-case)
8. Matrice de cohérence logique : conditions booléennes complexes vérifiées (combinaisons, branches mortes)
9. Corriger chaque problème identifié

### §4.9 Étape 4 — Interactions (détail)

1. API frontend-backend : endpoints existants, paramètres correspondants, codes d'erreur gérés
2. Props et communication inter-composants : types, noms, optionnalité cohérents
3. State management : store expose les données nécessaires, actions au bon moment
4. Flux de données bout en bout : scénario complet tracé (clic → API → store → re-render)
5. Communications entre services : ports/URLs, WebSockets, timeouts et réessais
6. Références croisées entre livrables : numéros de section, données cohérentes, liens valides
7. Corriger chaque problème d'interaction identifié

### §4.10 Étape 5 — Cohérence des raisonnements (détail)

1. Cohérence logique : enchaînement des étapes de raisonnement, pas de saut non justifié
2. Cohérence numérique : les chiffres s'additionnent, pourcentages cohérents avec les valeurs absolues
3. Cohérence temporelle : dates, versions, chronologies cohérentes entre elles
4. Résultat attendu vs obtenu : ce qui a été promis correspond à ce qui a été livré
5. Cohérence entre fichiers : pas de contradiction entre le contenu de deux livrables
6. Corriger toute incohérence identifiée

---

## §5 — Conventions

### §5.1 Nommage

- Répertoires : kebab-case
- Fichiers : kebab-case avec extension
- Sections : préfixe `§`

### §5.2 Rapport

Structure normalisée en 5 sections (Métadonnées + Étapes 1-5 + Résumé). Support multi-cibles : un sous-rapport par cible, verdict global = pire des verdicts. Worklog au format SHARED §1.4.
