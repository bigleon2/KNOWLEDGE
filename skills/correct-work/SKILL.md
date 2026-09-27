---
name: correct-work
version: 2.6.0
category: ecosystem
language: fr
tags:
  - vérification
  - correction
  - quality-assurance
  - ecosystem
  - kb-integration
description: >
  Skill de vérification et correction du travail réalisé (erreurs, omissions, incohérences).
  5 étapes, 4 modes (PROJET/CIBLE/DIRECT/AVEUGLE),
  support multi-cibles, découplage gen-plan optionnel,
  intégration KB (Registre, kb_path, --kb-skill),
  matrice de décision agent/skill (statique + dynamique KB),
  métriques de performance.
dependencies:
  - skill: gen-plan
    version: ">=3.7.0"
    used_at: "Étape 1 (optionnel, mode PROJET)"
  - skill: clone-chat
    version: ">=2.0.0"
    used_at: "Mode CIBLE, §3.5 Context Drift"
  - skill: fullstack-dev
    version: ">=1.0.0"
    used_at: "Vérification projets web"
---

## §0 — Contexte Système (SHARED v1.5.2)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (exception)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.



## §0 — RÈGLE ZÉRO (résumé de SHARED §0)

Les fichiers des sessions précédentes n'existent pas dans une nouvelle session : tout est
à reconstruire à partir des documents de la lignée. Ne jamais utiliser le verbe « conserver ».
Voir `PROMPT-MAITRE-SHARED.md §0` pour la règle complète.

## §A — DÉCLENCHEURS

- `verifie ton travail`
- `verifie tes résultats`
- `verifie ton code`
- `correct-work` ou `correct_work`
- `verify-work` (alias anglais)
- `correct-work(projet)` — vérification complète du projet
- `correct-work(<cible>)` — vérification ciblée sur un livrable
- `correct-work()` — vérification rapide sans analyse approfondie
- `correct-work(aveugle)` — re-vérification aveugle (Second Opinion) sans accès au premier verdict

Options avancées (gen-plan >= v3.6.0) :
- `correct-work(projet, kb_path=/chemin/KB)` — vérification avec scan des skills KB
- `correct-work(cible, --kb-skill=<name>)` — forcer l'utilisation d'un skill KB spécifique


## §1 — SPÉCIFICATION FONCTIONNELLE

### §1.1 Description

correct-work est un skill de **vérification et correction** du travail réalisé par l'assistant IA. Il fournit un cadre structuré en 5 étapes et 4 modes pour inspecter, diagnostiquer et corriger tout artefact produit au cours d'une session. Supporte le multi-cibles, le découplage gen-plan optionnel, et les métriques de performance.

### §1.2 Les 4 modes

| Mode | Nom | Description | Cas d'usage |
|------|-----|-------------|-------------|
| **PROJET** | Prompt-maître | Vérification complète d'un projet via son prompt maître | Validation finale d'un projet complexe |
| **CIBLE** | Ciblé | Vérification ciblée d'un skill ou fichier spécifique (défaut) | Vérification d'un skill (ex: clone-chat) |
| **DIRECT** | Rapide | Vérification directe sans plan préalable | Correction rapide d'un fichier |
| **AVEUGLE** | Second Opinion | Re-vérification sans accès au premier verdict (élimine le biais de confirmation) | Divergence ou FAIL persistant à l'Étape 5 ; déclencheur `correct-work(aveugle)` |

### §1.3 Les 5 étapes

| Étape | Nom | Description |
|-------|------|-------------|
| **1** | Plan d'actions | Création du plan de vérification (gen-plan si dispo, sinon autonome) |
| **2** | Erreurs et omissions | Détection des erreurs factuelles, omissions, incohérences logiques |
| **3** | Structure et conflits | Vérification de la structure, conflits entre sections, cohérence du format |
| **4** | Vérification des interactions | Inspection des relations inter-skills, dépendances, interfaces |
| **5** | Cohérence des raisonnements | Vérification de la logique globale, cohérence argumentaire, décisions |

**Hook Second Opinion à l'Étape 5 (v2.6.0, phase N20)** : en cas de FAIL ou de divergence persistante à l'Étape 5 (Cohérence des raisonnements), une re-vérification **AVEUGLE** est lancée (**2nd opinion agent-driven**, déclencheur `correct-work(aveugle)`) : le vérificateur rejoue les étapes 2-5 sans accès au premier verdict, avec les inputs filtrés (`references/verification-protocol.md`). Maximum 2 rounds de correction par artefact (SHARED §4.4) ; le verdict final retenu est celui de la re-vérification aveugle.

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
| gen-plan | >= v3.7.0 | Étape 1 (plan d'actions) | Oui (autonome sinon) |
| clone-chat | >= v2.0.0 | Mode CIBLE (§3.5 Context Drift) | Oui |
| fullstack-dev | >= v1.0.0 | Vérification de projets web | Oui |

### §2.3 Structure des fichiers

```
{{SKILLS_ROOT}}correct-work/
├── SKILL.md              # Skill opérationnel (~330 lignes)
├── references/
│   └── verification-protocol.md  # Second Opinion — inputs filtrés, 4 étapes (v2.6.0)
├── scripts/
│   └── verify-correct-work.py  # 16 checks post-install automatisés
└── evals/
    ├── evals.json             # Cas de test (schéma skill-creator)
    └── trigger_evals.json     # Cas de déclenchement (Description Optimization)
```

### §2.4 Format du rapport de vérification

```markdown
# Rapport correct-work — [Nom du projet/skill]

## Métadonnées
- **Date** : YYYY-MM-DD
- **Mode** : PROJET | CIBLE | DIRECT
- **Version correct-work** : 2.6.0
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
| gen-plan | Invocation à E1 | Plan de vérification (optionnel, autonome sinon), version >= v3.7.0 |
| clone-chat | Vérification Mode CIBLE | §3.5 Context Drift, version >= v2.0.0 |
| fullstack-dev | Vérification | Projets web : structure et dépendances, version >= v1.0.0 |
| knowledge.md | Scan dynamique | Découverte versions et dépendances |

---


### §3.2 Règles de cross-references (décentralisé du SHARED §3.2)

> 📎 Décentralisé depuis `PROMPT-MAITRE-SHARED.md` (corrige-ecosysteme v2.0.0).

Quand un skill A référence un skill B :
1. La référence dans A doit inclure la version minimale requise de B
2. Le fichier de B doit mentionner A dans sa section « Utilisé par » de KNOWLEDGE.md
3. Si A modifie le comportement de B (ex : correct-work modifie clone-chat), la relation doit être documentée dans les deux sens
4. Les mises à jour de version d'un skill doivent déclencher une vérification des dépendances
5. **Plancher de version = version d'intégration validée** : lorsqu'un changement de contrat d'intégration survient (nouveau hook, nouvelle étape, nouveau mode), le plancher de la dépendance concernée est élevé à la version installée validée (ex : correct-work → gen-plan >= v3.7.0, suite au hook « contrôle par phase » E9-E14, 2026-08-30) ; sans changement de contrat, le plancher minimal historique demeure valide. Les arbitres (verify-cross, verify-correct-work) vérifient le plancher déclaré.
6. **Planchers gradués assumés** : un plancher d'option peut demeurer inférieur au plancher d'intégration lorsqu'aucun changement de contrat ne l'affecte — cas assumé du PM correct-work v2.4.0, §A « Options avancées (gen-plan >= v3.6.0) » (options KB de scan antérieures au hook E9-E14), à ne pas confondre avec le plancher d'intégration >= v3.7.0 porté par la matrice des dépendances, le plan de vérification et l'auto-contrôle n°11. Un contrôle automatique de cohérence doit lire cette règle avant de signaler une divergence de plancher entre deux occurrences.

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
| Un FAIL ou une divergence persiste à l'Étape 5 | AVEUGLE |
| Déclencheur explicite `correct-work(aveugle)` | AVEUGLE |

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

## §11 — CONVENTIONS

- Nommage kebab-case, sections préfixées « § », budgets préfixés « #token » (SHARED §1.2)
- Worklog format SHARED §1.4 — une entrée par tâche, verdicts et preuves JSON
- Planchers directionnels plutôt qu'égalité stricte (leçon E21) pour tout critère couplant
  une valeur à un artefact vivant
