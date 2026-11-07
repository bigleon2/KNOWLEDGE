# Rapport de tests d'installation — Task 70 G1 (tests $FACON2 : PM INSTALL + ensure-installed.py)

**Horodatage : 2026-11-07T17:27:36Z** · Plan : `download/plan-task70-integration-bibliotheque-ghorg-etude-faisabilite.md` (G1/SG1.2-T1.2.3) · Objectif propriétaire : vérifier que les fichiers qui installent et orchestrent l'écosystème sont **à jour et optimisés**.

## 1. Tests PM INSTALL — pipeline `scripts/eco_install_pipeline.py`

| # | Test | Commande | Résultat | Verdict |
|---|---|---|---|---|
| 1 | Exécution nominale | `python3 scripts/eco_install_pipeline.py` | rc=0 · préflight pin `b75a620` ancêtre de HEAD `0e1e4fb` (descendant-tolérant) · garde R2 « 0 rétrogradation — host ≤ repo partout » · rescellement archive round-trip v2.2 OK (9 entrées, 0 divergent, 0 extra) · post-install **53/53 SHA-256 vérifiés, 0 divergence** | **PASS** |
| 2 | Idempotence (rejeu) | 2ᵉ exécution | rc=0 · verdicts identiques (53 SHA, 0 divergence, **0 purge**) · git status dépôt : seuls artefacts Task 70 (worklog + plan) — aucune action de bord | **PASS** |

## 2. Tests ensure-installed.py (commit `0e1e4fb` — lancé par gen-plan)

| # | Test | Commande | Résultat | Verdict |
|---|---|---|---|---|
| 1 | Garde `--check` | `python3 skills/gen-plan/scripts/ensure-installed.py --check` | `INSTALLE` rc=0 · root_present=true · git_repo=true · head=`0e1e4fb` · fichiers_manquants=[] · kb_entrees=53 · skills_kb_manquants=[] | **PASS** |
| 2 | Préemption `--preempt` | `python3 skills/gen-plan/scripts/ensure-installed.py --preempt` | `PRIORITE-NONE` rc=0 (écosystème à jour → aucune interruption de tâche) | **PASS** |
| 3 | Shim racine (délégation) | `python3 scripts/ensure-installed.py --check` | `INSTALLE` rc=0 — le shim racine délègue correctement au script maître intégré au skill gen-plan (§1.16) | **PASS** |
| 4 | Auto-réparation (garde étendue Task 56) | ouverture de session (avant tests) | `version-management` absent → **INSTALLE-REPARÉ** rc=0 (restauration miroir local, 0 action distante) puis re-jeu `INSTALLE` no-op | **PASS** |
| 5 | Idempotence ×2 | 2 exécutions `--check` consécutives | verdicts byte-identiques (INSTALLE, listes vides) — `IDEMPOTENT-OK` (diff vide) | **PASS** |

## 3. Fraîcheur / optimisation des fichiers d'installation et d'orchestration

| Fichier d'installation/orchestration | Attendu | Constaté | Verdict |
|---|---|---|---|
| PM INSTALL (`@mon-ecosysteme/PROMPT-MAITRE-INSTALL-ECOSYSTEME.md`) | v1.9.7 (cascade Task 61 G3) | **v1.9.7** déclarée · §2ter instantané = gen-plan v3.37.1 (dernier) · mécanisme dual (pipeline = exécutant canonique) opérationnel | **À JOUR** |
| SHARED (`PROMPT-MAITRE-SHARED.md`) | v1.7.31 | **v1.7.31** | **À JOUR** |
| gen-plan installé (`skills/gen-plan/SKILL.md`) | v3.37.1 = fiche KB | **3.37.1** = KB v3.37.1 | **À JOUR** |
| Garde ensure-installed.py | couvre toutes les entrées KB + auto-réparation | 53/53 entrées couvertes, auto-réparation prouvée en conditions réelles (version-management) | **À JOUR + OPTIMISÉ** |
| Arbitre integrity | 110/110 PASS 0 FAIL | **110/110 PASS, 0 FAIL** (re-jeu post-réparation) | **À JOUR** |
| Propagation §0 (`scripts/propagate-context.py`) | tous porteurs d'en-tête §0 à v1.7.31 | **F-70-2 (S3) découvert et résorbé** : gap de périmètre — `skills/*/scripts/*.py` invisibles à la propagation (8 scripts STALE v1.7.17 : alias-eco ×1, inter-scripts ×2, dessin-technique ×5) → extension v2.0.10→**v2.1.0** (mise à jour idempotente des seuls porteurs d'en-tête, jamais d'injection) → 9 scripts mis à jour, rejeu ×2 = 0/0/0, **scan STALE résiduel = 0** (hors @historique figé R2) | **RÉSORBÉ — OPTIMISÉ** |

## 4. Findings qualifiés (règle d'or n°5 — statuts dérivés du disque)

- **F-70-1 (S3 — reporté à la cascade, PAS corrigé à la main)** : les extraits §0 des PMs du corpus (INSTALL v1.7.17, CORRECT-WORK v1.6.4, CLONE-CHAT v2.0.2 v1.6.8, REFACTOR-GUARD v1.8.1 v1.7.17) affichent la version SHARED **à leur date de génération mécanique**, pas la courante v1.7.31. Les PMs sont des artefacts générés (KO-L004) — leur recalibrage appartient à la cascade `generer-pm-skill.py` à la prochaine montée, jamais à une édition manuelle (R2). Recommandation consignée pour E15.
- **F-70-2 (S3 — RÉSORBÉ)** : gap de périmètre propagate-context (ci-dessus). Leçon F-63-1 réappliquée : le périmètre d'une propagation doit être prouvé par grep post-exécution, pas présumé de la liste de cibles.

## 5. Verdict global G1

**PM INSTALL : 2/2 PASS** (nominal + idempotence) · **ensure-installed.py : 5/5 PASS** (check, preempt, shim, auto-réparation, idempotence) · **fraîcheur : 6/6 À JOUR** (dont 1 optimisé en vol : propagate-context v2.1.0) · 1 finding S3 résorbé (F-70-2), 1 finding S3 reporté à la cascade (F-70-1, par conception). **Les fichiers qui installent et orchestrent l'écosystème sont à jour et optimisés — aucune régression (R2), idempotence prouvée partout (R6).**
