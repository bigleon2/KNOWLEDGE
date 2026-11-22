# RAPPORT correct-work (projet) --bloc — Task 114

**Trace** : 1a2025197d2a0e9d + 1a2025ce4a6ed095 (session web-f492e049) · **Date** : 2026-11-22 · **Mode** : PROJET « bloc par bloc » (v2.12.1 — `--bloc` synonyme explicite)
**Périmètre vérifié** : modifications et créations de la demande Task 114 — script de routage décisionnel, gen-plan v3.47.0 (rappel permanent langue + É5-ROUTAGE + §1.17), garde réinjection plateforme (ensure-installed.py), cascade KO-L004, livrables et tests.

## Blocs vérifiés

| Bloc | Étapes couvertes | Findings | Verdict |
|------|------------------|----------|---------|
| **B1 — Mécanique du script de routage** | selftest ×2 arbres (9/9 ×2) · parité byte hôte↔dépôt · scénarios F3/F4/F5 (traduction top-3, porte SIMPLE, COMPLEXE 3/5 + agents) · idempotence ×2 | F1 : attente d'idempotence byte-à-byte fausse (champ volatile `duree_ms` = métadonnée de mesure par conception) → test corrigé en comparaison sémantique hors durée (KO-L003, arbitre corrigé — la réalité inchangée) · 1 round | **PASS** |
| **B2 — gen-plan v3.46.0→v3.47.0** | 7 ancres (frontmatter, §0 rappel langue, §1.16 É5-ROUTAGE, §1.17, §2.2, §3, §4) · poids 39 788 o (38,9 Kio < 60 Kio CRITIQUE) · journal §5.6 v3.47.0 + migration R4 v3.46.0 vers references/journal-versions.md · description + clauses | aucun | **PASS** |
| **B3 — Garde réinjection plateforme (ensure-installed.py)** | code présent (SKILLS_REINJETES, signature_native, reparer_reinjection, MAJUSCULES_STALE) · test RÉEL en conditions réelles : simulation réinjection → INSTALLE-RÉPARÉ (13 restaurations + 4 suppressions stale sous garde archive R4 byte-identité) → INSTALLE idempotent ×2 · état stable final rc=0 | aucun | **PASS** |
| **B4 — Cascade KO-L004 (recalibrage croisé)** | PM v3.47.0 généré mécaniquement (delta verrouillé) + PM v3.46.0 dédup @historique R4 · KB (titre + Description + Dernière calibration) · pin ECO_SKILLS 3.47.0 ×2 arbres · evals sync 3.46.0→3.47.0 · propagation §0 SHARED v1.7.45 ×2 arbres (121 skills dépôt + 17 skills hôte résiduels) · archive v2.5 rescellée ×2 arbres · manifeste 116/116 | F2 : 9 citations vives gen-plan v3.46.0 (5 flaggées + 4 de même nature bullet) → recalibrées v3.47.0 (addition pure, précédent Task 113) · F3 : archive périmée après PM v3.47.0 (KeyError interactions) → rescellement ×2 arbres · F4 : propagation §0 exécutée dépôt puis hôte · 2 rounds max | **PASS** |
| **B5 — Livrables, tests et langue** | tests F+P 32/32 PASS (rapport download/rapport-task114-tests-fp.json) · livrable analyse avec mesures (download/analyse-routage-decisionnel-task114.md) · audit conformité 73/73 skills + 4/4 agents · dérive langue chinois journalisée au worklog + corrigée + durcissement intégré (§0 gen-plan) · arbitres non-régression (triggers 55/55, verify-cross 168/168, interactions PASS STRICT 59/59, poids non-CRITIQUE) · certification ALL PASS 6/6 · bootstrap VERDICT GLOBAL INSTALLE(-RÉPARÉ) | aucun | **PASS** |

## Corrections appliquées pendant la vérification (traçage §1.7)

1. **B1/F1** — `scripts/task114-tests-fp.py` F6 : attente idempotence reformulée (comparaison sémantique hors `duree_ms`) — KO-L003 : le champ de durée est une métadonnée de mesure, jamais un verdict ; la réalité (scores de routage) est restée identique ×2.
2. **B4/F2** — recalibrage croisé KO-L004 des 9 citations vives gen-plan (références de version, addition pure non-régression — précédent Task 113 « même patch de session »).
3. **B4/F3-F4** — rescellement archive v2.5 ×2 arbres + propagation §0 hôte — ordre cascade corrigé (propagation → rescellement → manifeste → arbitres).

Rounds consommés : 2 (B4) / 1 (B1) — garde anti-boucle SHARED §4.4 respectée (max 2 par bloc).

## VERDICT GLOBAL

**PASS** — 5/5 blocs PASS, 0 FAIL, 0 PASS AVEC RÉSERVES. Findings corrigés en séance avec preuves mécaniques (tests re-jeu 32/32, certification ALL PASS 6/6, bootstrap INSTALLE, audit 73/73 + 4/4 CONFORMES).

*Preuves d'exécution : selftests ×2 arbres 9/9 · tests F+P download/rapport-task114-tests-fp.json (32/32) · certification scripts/certification-report.json (6/6) · rapport bootstrap download/bootstrap-ecosysteme-rapport.json (INSTALLE) · audit download/rapport-audit-conformite-task113.json (73/73 + 4/4).*
