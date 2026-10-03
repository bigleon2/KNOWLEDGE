# Rapport correct-work — script-creator (N25-a, mode CIBLE) + N25

## Métadonnées
- **Date** : 2026-09-27 | **Mode** : CIBLE (round 1) | **Version correct-work** : 2.6.0
- **Cible** : `skills/script-creator/` (SKILL.md v1.0.0, 126 L, evals 4+7)
- **Directive** : trace `1a0def365a639149` — « script-creator (désormais présent sur disque), correct-work(script-creator), test simple, champ version skill-creator, 4 evals + 7 trigger_evals en base réelle »

## Étape 1 — Plan d'actions (autonome, mode CIBLE)
Pré-vérification (cible identifiée, specs chargées via KB/skill-creator, version 1.0.0) → vérification ciblée 5 étapes → post-vérification.

## Étape 2 — Erreurs et omissions
| # | Sévérité | Description | Emplacement | Correction |
|---|----------|-------------|-------------|------------|
| — | — | Faits vérifiés : 7 étapes §1.2, 6 garde-fous §1.3 (GF-1 à GF-6), dépendances installées (skill-creator 1.0.0, correct-work 2.6.0, correct-py 1.0.0), evals 4 evals + 7 triggers au schéma officiel skill-creator (id, prompt, expected_output, files, expectations ; query/should_trigger), champ `version: 1.0.0` présent dans skill-creator (N25-c constaté) | SKILL.md + evals/ | aucune requise |

## Étape 3 — Structure et conflits
Structure conforme (frontmatter YAML complet, kebab-case, sections §, non-duplication §4 respectée) ; aucun conflit de noms ni doublon.

## Étape 4 — Interactions
| # | Type | Description | Statut |
|---|------|-------------|--------|
| F1 | S3 | script-creator **absent du registre KB** (famille script-* : script-creator, script-reviewer non enregistrées ; agent-creator seule enregistrée v2.0.0) — l'ajout exigerait le recalibrage croisé L004 des arbitres calibrés à 13 entrées fixes (integrity check 5, interactions) | Réserves — différée (liste L004 tracée au worklog) |
| F2 | S4 | Réciprocité « Utilisé par » non établie (dépend de F1) | idem |
| — | — | Dépendances versionnées vérifiées installées : toutes conformes | PASS |

## Étape 5 — Cohérence des raisonnements
Chaîne cohérente : mission ↔ 7 étapes ↔ garde-fous ↔ relations §3 ↔ frontmatter deps ; evals note (« processus 7 étapes §1.2, garde-fous §1.3 ») conforme au contenu réel ; GF-6 (correct-py) cohérent avec §2 (délégation des normes) ; pas de contradiction inter-fichiers.

## N25-b — Test simple (processus script-creator §1.2, 7 étapes exécutées)
Arbitre de session `scripts/n25-verif-marqueurs-pm3160.py` créé via le processus complet :
critères (marqueurs PATTERN des 3 emplacements PM v3.16.0 + byte-identité) → brouillon persisté → critères mécaniques → test (FAIL 0/8 : invariant figé de l'auteur — 2 marqueurs réels au PM vs 4 supposés, chemin racine erroné) → **itération par édition ciblée** (L003 appliquée : invariants dérivés de l'état courant, PM = 2 blocs PM-* par conception B1) → **re-test 10/10 ALL PASS** → idempotence ×2 (sorties cmp identiques) → traçabilité worklog.
Post-traitement correct-py (GF-6) : py_compile PASS ; shebang, docstring module + fonctions, snake_case, code de retour explicite — conformes ; 6 lignes > 79 c. (S4 cosmétique, PEP 8 W504 tolérance).

## Résumé
- **Problèmes trouvés** : 2 (F1 S3, F2 S4) | **Corrections appliquées** : 0 requise (réserves tracées) | **Verdict : PASS**
- N25-d (evals en base réelle) : PASS — 4 evals + 7 triggers validés mécaniquement contre `skill-creator/references/schemas.md` (1 faux FAIL de vérificateur corrigé contre le schéma source).
- N25-c (champ version skill-creator) : constaté présent (`version: 1.0.0`), cohérent avec la dépendance `script-creator → skill-creator >= 1.0.0`.
