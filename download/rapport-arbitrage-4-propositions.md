# Rapport d'arbitrage — 4 propositions en attente (Phase P4, tâche 6)

> **Session** : web-eb6c8580 · 2026-10-26 · **Directive propriétaire** : tâche 6 de la directive à 10 tâches — arbitrage des 4 propositions consignées à l'audit (Task 5, Phase B/C) contre l'état réel de la lignée distante
> **Référentiel d'arbitrage** : worktree publication (b2d4e5b + commits P0-P3) — la lignée distante est la cible de publication (D002) ; les drifts locaux de l'état fork v3.23.1 sont ré-arbitrés contre elle
> **Statuts** : CORRIGÉ / JOURNALISÉ / OBSOLÈTE (résolu côté distant) — conformément D005 du plan task3

## Table d'arbitrage (4/4 statutés)

| Proposition (audit Task 5) | Statut | Fondement vérifiable |
|---------------------------|--------|----------------------|
| **Correctif bug §6** (rapport-test-bug-genplan-v3240.md — gate exit 4, --check PM-SHELL, --complete, arbitre de complétude, propagation) | **OBSOLÈTE-PARTIEL** | La lignée distante a corrigé la cause par une voie supérieure : commit `26d9846` (v3.27.0 — fusion des lignées) : hook E7-DISP (table §1.2bis + affichage REJOUABLE + garde anti-verdict-périmé), extension E1-RES, evals 13 cas, causes racines RC1-RC4 (`download/analyse-causes-racines-gen-plan.md`). **Résidu documenté** : l'arbitre mécanique `scripts/check_plan_protocol.py` reste **reporté** (absent du dépôt — mention explicite au commit) — notre diagnostic sandbox (C3 : canal canonique exonéré par diff intégral, 6 points de substitution seulement ; faille « complétion agent » L009 : WARN sans gate + aucun arbitre ne contrôle la complétude sémantique) constitue le **complément d'analyse** directement exploitable pour implémenter l'arbitre reporté. |
| **(a) PM_PATH référence v2.5.1** (verify-correct-work local pointait un PM antérieur au corpus v2.7.0) | **OBSOLÈTE** | `scripts/verify-correct-work.py` distant ne porte AUCUNE constante PM_PATH (rg 0 occurrence) — la lignée distante a réécrit l'arbitre ; le drift n'existe pas sur la cible de publication. |
| **(b) `--mode correct-work` non implémenté** (certification-complete local acceptait l'option sans l'implémenter) | **JOURNALISÉ** | Vérifié : le verify-correct-work distant n'expose pas davantage `--mode` (aucun `add_argument` de mode). La proposition locale n'est PAS applicable à la lignée distante (correct-work v2.8.0 distant a sa propre mécanique de modes). Le need reste valide (proposition conservée pour la lignée locale fork v3.23.1 — environnent d'exécution, non re-projeté D011). |
| **(d) worklog B1** (WARN 47/48 — avertissement résiduel de la restauration locale) | **OBSOLÈTE** | Le worklog distant porte son propre historique (sessions web-f90062ce, web-dd290b0d — conventions propres) ; l'avertissement B1 est un artefact de la restauration locale (profil fork), sans portée sur la cible de publication. |
| **(f) dérives voie M** (check-triggers-replay local : 26/43, 17 dérives sur le fork) | **OBSOLÈTE** | Les trigger_evals distants sont ré-équilibrés (13 cas — v3.27.0 : +2 cas interruption/reprise) et `scripts/check-triggers-replay.py` distant est le test de référence ; le re-jeu distant est exécuté en P5 (test robuste). Les 17 dérives locales portent sur des triggers du fork jamais publiés. |

## Décisions d'arbitrage

1. **ADOPTER la correction distante** (D004) : le correctif bug §6 est porté par la v3.27.0 fusionnée — aucune re-application. Le diagnostic sandbox est conservé comme **complément d'analyse** (le présent rapport fait foi).
2. **Recommandation résiduelle** : implémenter `scripts/check_plan_protocol.py` (reporté depuis v3.27.0) — les 5 points du diagnostic C6 (gate exit 4, --check PM-SHELL, --complete, arbitre de complétude, propagation §2quater/§1.15) en fournissent la spécification. Tracé comme proposition ouverte au propriétaire.
3. **Zéro-régression** : aucun fichier distant modifié par le présent arbitrage (rapport ajouté uniquement — additions only D001).

## Traçabilité

- Source des propositions : `download/rapport-audit-ecosysteme-2026-10-25.md` §5 (drifts a/b/d/f) + `download/rapport-test-bug-genplan-v3240.md` §6 (correctif 5 points)
- Vérifications exécutées : `ls scripts/check_plan_protocol.py` (absent) ; `rg PM_PATH scripts/verify-correct-work.py` (0) ; `rg add_argument scripts/verify-correct-work.py` (0 mode) ; `git log --oneline -15` (commit 26d9846 — mention « arbitre reporté »)
- Hook de phase : correct-work(livrables P4, mode=CIBLE) au bilan de phase (P6 — consolidation)
