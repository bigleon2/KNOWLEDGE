# Rapport correct-work — alias-eco (mode CIBLE)

## Métadonnées
- **Date** : 2026-10-24
- **Mode** : CIBLE (vérification ciblée — pas de couplage gen-plan requis, correct-work v2.8.0 §1.5)
- **Version correct-work** : 2.8.0
- **Cible** : skill `alias-eco` v1.0.0 (profil local + dépôt KNOWLEDGE-repo) + livrable de session `scripts/alias_trigger_analysis.py`

## Étape 1 — Plan d'actions (mode CIBLE)

1. Intégrité mécanique du skill : py_compile, `--selftest`, frontmatter YAML, structure §2.1.
2. Livrable de session (analyse déclencheur propriétaire) : py_compile, idempotence, cohérence avec les gardes réelles du gestionnaire.
3. Interactions : dépendances correct-work ↔ alias-eco, KB, registre @historique/@Alias (R4).
4. Cohérence des raisonnements : recommandation (grammaire B) vs spécification §1.1/§1.2 ; statut « intégration en attente GO ».

## Étape 2 — Erreurs et omissions

| # | Sévérité | Description | Emplacement | Correction proposée |
|---|----------|-------------|-------------|---------------------|
| 1 | S3 (héritée, documentée) | trigger_evals alias-eco à 5/8 au replay voie M — 3 cas négatifs échoués (hits partagés clon/discuss/sess, inventair/skill, livr/projet avec clone-chat, skills-inventory, correct-work) | evals/trigger_evals.json | Aucune — même nature que les dérives iphone (limite heuristique mots-clés), documentée Task 24 (parmi les 17) |
| 2 | S3 | Registre `@historique/@Alias/aliases.json` absent au profil local (présent au dépôt, 1 865 o) | skills/@historique/@Alias/ (local) | Aucune — cohérent R4 (source unique au dépôt) ; `load_registry` recrée à la volée, et `--resolve` signale explicitement tout alias inconnu (exit 1) |

0 S1, 0 S2.

## Étape 3 — Structure et conflits

| # | Type | Description | Fichiers concernés | Résolution |
|---|------|-------------|-------------------|------------|
| 1 | Contrôle | Structure §2.1 complète (5/5 fichiers) — SKILL.md, format-alias.md, alias-manager.py, evals.json, trigger_evals.json | alias-eco/ | OK |
| 2 | Contrôle | Frontmatter YAML valide — name alias-eco, version 1.0.0, dependencies [], 5 tags ; entrée KB `## alias-eco v1.0.0` cohérente | SKILL.md, KNOWLEDGE.md | OK |
| 3 | Divergence bénigne | `__pycache__/alias-manager.cpython-312.pyc` diffère profil ↔ dépôt (bytecode, non-livrable) | scripts/__pycache__/ | Aucune — couvert par la purge F2 du pipeline |

## Étape 4 — Interactions

| # | Skill A | Skill B | Type d'interaction | Statut |
|---|---------|---------|-------------------|--------|
| 1 | correct-work v2.8.0 | alias-eco | dépendance `>=1.0.0` (mode PROJET, §10.1 tenue du registre) | OK — version satisfaite |
| 2 | alias-eco v1.0.0 | correct-work | relation documentée §3 (« Utilisé par ») + description frontmatter | OK — bidirectionnelle |
| 3 | alias-eco | @historique/ | héberge `@Alias/` (convention `@` SHARED §1.2, R4 source unique) | OK — registre vivant au dépôt |
| 4 | alias-eco | registre KB | entrée `alias-eco v1.0.0` (category ecosystem) | OK |
| 5 | profil local ↔ dépôt | — | livrables identiques ×5 (seul bytecode diffère) | OK |

## Étape 5 — Cohérence des raisonnements

| # | Point vérifié | Résultat | Détail |
|---|---------------|----------|--------|
| 1 | Intégrité mécanique | PASS | py_compile ×2 OK ; `--selftest` **15/15 PASS** (détection, tri, déduplication, résolution, garde format, mode chat) |
| 2 | Livrable d'analyse idempotent | PASS | alias_trigger_analysis.py ré-exécutable, résultats stables (24/29 PASS — les 5 FAIL sont les ambiguïtés **documentées** du format proposé, comportement attendu de l'instrument) |
| 3 | Verdict d'analyse vs gardes réelles | PASS | Conclusions confirmées par le gestionnaire réel : `--add 'façon()'` → rc=2 ABANDON ; `$façon()` laissé intact par `--resolve` (échec silencieux documenté) ; grammaire B 100% PASS (7/7 cas) et cohérente avec §1.1 (regex `^[A-Z0-9][A-Z0-9-]*$`) et §1.2 (trigger existant « ajoute l'alias X pour « … » ») |
| 4 | Statut « en attente GO » respecté | PASS | `git status` sur skills/alias-eco/ : **0 modification de session** — aucune intégration non autorisée (règle d'or n°2) |
| 5 | Cohérence éval/description | PASS | trigger_evals 8 cas (5+, 3-) conformes aux 3 déclencheurs §1.2 ; evals.json 5 cas canoniques |

## Résumé
- **Problèmes trouvés** : 2 (S3) + 1 divergence bénigne (bytecode)
- **Corrections appliquées** : 0 (aucune requise — livrables intègres, session non intruse)
- **Problèmes restants** : 2 réerves S3 documentées (dérive replay héritée ; registre local à amorçage différé)
- **Verdict** : **PASS AVEC RÉSERVES** (0 S1/S2 ; réserves S3 héritées, documentées, hors périmètre de correction de ce mode CIBLE)
