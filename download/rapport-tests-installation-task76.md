# Rapport final — Task 76 : Tests fonctionnels et performances des systèmes d'installation — PM-INSTALL · ENSURE-INSTALL

**Horodatage : 2026-11-08T07:10:00Z** · Session : web-ecef7f80 · Trace directive : 1a1b9d4c74daee71 · Plan : download/plan-task76-tests-installation-pm-install-ensure-install.md (14 décisions) · Prérequis : Task 75 CLOSE

## 1. Résumé exécutif

| Cible | PRE | POST | Non-régression |
|---|---|---|---|
| **C1 — PM-INSTALL** (corpus v1.9.11 + exécutants canoniques : eco_install_pipeline.py, install-ecosysteme-local.sh, task21-f2-rebuild-archive.py) | **FAIL** (7 PASS · 1 RÉSERVES · 4 FAIL — 109,9 ms) | **PASS** 12/12 (104,6 ms) | ✓ 4 failles résorbées + 1 adjudication close |
| **C2 — ENSURE-INSTALL** (garde É1-INSTALL ensure-installed.py + shim racine) | **PASS** 11/11 (521,0 ms) | **PASS** 11/11 (521,2 ms) | ✓ stable |
| **Global (pire des cibles)** | **FAIL** | **PASS** | **TRUE (0 dégradation test à test)** |

**5 failles détectées et corrigées $FACON** sur la couche installation — 4 en PRE (F1/F2/F3/F5) + 1 adjudication close (F4) — dont **2 majeures révélées par un événement réel** : un appel `--help` au pipeline a exécuté une installation complète pendant l'exploration E2 (F1), et l'archive d'intégrité vivait en **deux véhicules concurrents** contraires à la spécification (F4). La garde ENSURE-INSTALL est saine d'entrée (11/11 aux deux phases, auto-réparation prouvée en bac à sable **et** en réel).

## 2. Directive et alias

« fais $FACON un tests $FACON2 fonctionnels et de performances des systèmes d'installation de mon écosystème (PM-INSTALL et ENSURE-INSTALL) dans l'objectif de corriger $FACON leurs failles et de les optimiser $FACON. / correct-work (projet) --bloc. / fais $FACON les correctifs des différés consignés et des autres erreurs (même non bloquantes). / correct-work (projet) --bloc. » — $FACON = « de façon cohérente, optimisée et fonctionnelle » · $FACON2 = « (cohérent, optimisé et fonctionnel) ».

## 3. Méthodologie (protocole $FACON2)

- **Protocole** : download/protocole-tests-installation-task76.json — 2 cibles, **23 tests** (C1 ×12 · C2 ×11), échelle PASS < RÉSERVES < FAIL, agrégation pire-des-verdicts, phases PRE (capture sans correction) / POST, non-régression stricte test à test, tolérances documentées (WARN B1 hérité · F4 adjudication mécanique · auto-réparation C2 = comportement nominal de la cible).
- **Outillage** : scripts/task76-campagne-tests.py — orchestration **R4** des arbitres existants (integrity délégué ; zéro duplication de logique de verdict), durées ms par test, modes --phase/--cible/--synthese/--protocole/--selftest, **selftest 8/8**, AUCUNE écriture corrective en PRE.
- **Livrables JSON** : download/rapport-campagne-task76-{pre,post}-{C1,C2}.json + synthèse comparative (…-post-synthese.json).

## 4. C1 — PM-INSTALL : FAIL → PASS 12/12

| Test | PRE | POST | Détail |
|---|---|---|---|
| C1-F01 structure (version == table §7 + sections) | PASS | PASS | v1.9.10 → **v1.9.11** (montée correction F5 — cohérence en-tête/table vérifiée dynamiquement) |
| C1-F02 sync corpus hôte↔dépôt | PASS | PASS | SHA identiques deux côtés (v1.9.11) |
| C1-F03 §2ter instantané 4 familles | PASS | PASS | GEN-PLAN v3.39.0 · CORRECT-WORK v2.11.0 · CLONE-CHAT v2.0.2 · REFACTOR-GUARD v1.8.1 == corpus réel |
| C1-F04 étiquette de date §2ter | **FAIL (F5)** | PASS | « au 2026-10-12 » périmée → **« au 2026-11-07 »** (date du dernier recalibrage) |
| C1-F05 critères §3 (≥14 entrées KB + §A.3) | PASS | PASS | 54 entrées · §A.3 → registre |
| C1-F06 registre certifié integrity (R4) | PASS | PASS | 112/112 PASS, 0 FAIL |
| C1-F07 exécutants canoniques compilables | PASS | PASS | pipeline + install-local.sh (bash -n) + rebuild-archive |
| C1-F08 contrat CLI du pipeline | **FAIL (F1)** | PASS | usage/--help sans exécution · argv explicite validé · --dry-run |
| C1-F09 PIN à jour | **FAIL (F2)** | PASS | b75a620 → **a14f750** (dernier commit certifié d'installation) |
| C1-F10 fichiers-refs alignés | **FAIL (F3)** | PASS | copies d'époque aa3b99d → formes canoniques courantes |
| C1-F11 archive intégrité hôte↔dépôt | **RÉSERVES (F4)** | PASS | deux véhicules concurrents → **unifié v2.2**, hôte==dépôt (SHA 1015308d…) |
| C1-P01 poids (référence) | PASS | PASS | 51 212 o = 50,0 Kio ≈ 12 803 #token (chargé à l'installation uniquement) |

## 5. C2 — ENSURE-INSTALL : PASS 11/11 (stable)

| Test | Verdict PRE/POST | Mesure clé |
|---|---|---|
| C2-F01 py_compile garde + shim | PASS / PASS | 230 L + shim délégation |
| C2-F02 --check réel | PASS / PASS | INSTALLE rc=0 · 54 entrées KB · 0 manquant · head miroir 3171c4b |
| C2-F03 idempotence ×2 | PASS / PASS | sorties byte-identiques |
| C2-F04 --preempt | PASS / PASS | PRIORITE-NONE rc=0 |
| C2-F05 --reinstall no-op | PASS / PASS | « Déjà installé » rc=0 (idempotence D006) |
| C2-F06 mode inconnu | PASS / PASS | rc=64 + usage |
| C2-F07 FICHIERS_CLES | PASS / PASS | 9/9 présents |
| C2-F08 KB dynamique | PASS / PASS | garde 54 == décompte strict indépendant 54 |
| C2-F09 **auto-réparation en bac à sable** | PASS / PASS | fake-skill-07 supprimé → INSTALLE-REPARÉ rc=0, restauré depuis miroir factif, trace worklog sandbox ; **contrôle négatif** : skill sans copie miroir → ABSENT-DERIVE rc=1 (aucune fausse réparation) |
| C2-F10 délégation shim racine | PASS / PASS | --check → INSTALLE rc=0 |
| C2-P01 performance --check | PASS / PASS | ~40 ms sur l'écosystème réel |

**Lecture** : la garde É1-INSTALL (Task 23/29/56/69) est **$FACON2 d'entrée** — aucune faille détectée ; l'auto-réparation est prouvée en isolation (bac à sable à contrôle négatif) et en réel (36ᵉ disparition version-management réparée en direct pendant la Task 75).

## 6. Failles → corrections ($FACON)

| Faille | Classe | Détection | Correction (preuve mécanique) | Validation POST |
|---|---|---|---|---|
| **F1** — contrat CLI absent du pipeline : `--help` exécutait une installation complète (constat E2 réel), argv[1] silencieusement repurposé, repli par défaut masquant l'erreur | **S2** | C1-F08 PRE FAIL + run E2 accidentel documenté | usage explicite · `--help`/`-h` n'exécute RIEN (rc=0, **SHA archive inchangé après l'appel**) · chemin explicite invalide → ABANDON rc=1 (aucun repli silencieux) · option inconnue rc=64 · **mode `--dry-run` lecture seule** (rapport complet, **preuve 0 mutation** : 0 fichier modifié, SHA stables) | C1-F08 PASS |
| **F2** — PIN obsolète (b75a620 ; 3 commits certifiés plus récents) | S3 | C1-F09 PRE FAIL | PIN → **a14f750** (dernier commit certifié d'installation, Task 74 run 2 rc=0) + docstring rafraîchi ; preflight re-vérifié descendant-tolérant | C1-F09 PASS |
| **F3** — fichiers-refs d'époque divergents (PM-INSTALL −680 o, shim ancien) | S3 | C1-F10 PRE FAIL | ressync aux formes canoniques (v1.9.11 + shim courant) ; l'état d'époque reste documenté (plan E2 + worklog) | C1-F10 PASS |
| **F4** — deux véhicules d'archive concurrents : hôte v2.2 corpus-seul (9 entrées, chaque run du pipeline) vs dépôt v2.3 corpus+piliers (15 entrées, cascades) — contrairement à la spécification PM-INSTALL (v2.2 désigné en 5 endroits, scelleur = task21-f2, étapes 2/10) | **S2** | C1-F11 PRE RÉSERVES + diagnostic mécanique (membres corpus identiques, 6 piliers en plus côté dépôt ; rescellement byte-déterministe ×2) | **unification v2.2 (R4 — une seule logique)** : task72-resceller-archive.py → shim de délégation vers le canonique ; archive dépôt réalignée (round-trip 0 divergence) ; corpus sync hôte↔dépôt ; le contenu des piliers vit dans l'arbre (retrait sanctionné — aucune perte) | C1-F11 PASS (hôte==dépôt 1015308d…, byte-stable ×2) |
| **F5** — étiquette de date §2ter périmée (« au 2026-10-12 » alors que la table était à jour) | S4 | C1-F04 PRE FAIL | étiquette → « au 2026-11-07 » + **PM-INSTALL v1.9.10 → v1.9.11** (ligne §7) + **cause racine résorbée au générateur** (generer-pm-skill.py rafraîchit l'étiquette à chaque recalibrage, substitution verrouillée) + sweep références vivantes (ULTRA ×2, README — lag v1.9.2 résorbé) | C1-F04 PASS + C1-F01 dynamisé |

## 7. Run E2 accidentel — transparence (règle d'or n°5)

L'exploration initiale a invoqué `python3 scripts/eco_install_pipeline.py --help` : l'argument a été interprété comme chemin de dépôt (inexistant) → repli silencieux sur le miroir local → **exécution complète du pipeline d'installation** (preflight OK, garde R2, sync union, rescellement, F3 post-install 0 divergence). **Conséquences mesurées : 0 changement de contenu** (dépôt numstat vide — seuls les mode-purs Task 74 connus ; hôte integrity 112/112 PASS post-run). Ce run accidentel est (a) une **preuve vivante d'idempotence du pipeline**, (b) la révélation de F1 **en conditions réelles**, (c) le déclencheur du diagnostic F4 (archive re-scellée v2.2 par l'étape 2). Consigné au plan E2 et au worklog dès constat.

## 8. Performances

| Mesure | Valeur |
|---|---|
| Campagne C1 (12 tests) | 109,9 ms (PRE) → 104,6 ms (POST) |
| Campagne C2 (11 tests) | 521,0 ms (PRE) → 521,2 ms (POST) |
| Garde --check seule (écosystème réel, 54 entrées) | ~40 ms |
| Pipeline --dry-run complet (60 étapes projetées + F3 ×54) | < 2 s, **0 mutation** |
| PM-INSTALL (poids de référence) | 51 212 o = 50,0 Kio ≈ 12 803 #token — chargé à l'installation uniquement, jamais par défaut |

## 9. Bugs de harnais corrigés en round (jamais du système testé)

1. Chaîne de test PIN à 39 caractères au lieu de 40 (selftest) ;
2. Assertion de non-régression du selftest mal formulée ;
3. Template plan : ligne Verdict E8 sans « Horodatage vérifié : » (P5) ;
4. C1-F01 version attendue figée « 1.9.10 » alors que la correction F5 montait v1.9.11 → critère **dynamisé** (en-tête == première entrée table §7 — robuste aux montées futures, KO-L003).

## 10. Optimisation et interactions (recommandations)

1. **`--dry-run` = voie canonique de test du pipeline** : toute vérification future de l'installation passe par ce mode (0 mutation, rapport complet) — ne plus jamais exécuter le pipeline en mode réel pour tester.
2. **Recommandation Task 73 §10.1 adjudiquée sans nouveau code** : la garde É1-INSTALL (40 ms, auto-réparation, invoquée à toute session post-coupure — règle d'or n°9) couvre la détection critique ; les arbitres complets restent aux jalons (R4 — aucun doublon du rôle de la garde).
3. **Une seule logique de scellement d'archive** (F4) : toutes les voies — pipeline ET cascades — rescellent via le canonique v2.2 ; la divergence hôte/dépôt ne peut plus reparaître.
4. **Interactions re-certifiées** : corpus v1.9.11 hôte==dépôt, integrity 112/112, ULTRA/README sweepés, garde R2 « 0 rétrogradation », F3 post-install 54/54 SHA 0 divergence.

## 11. Verdicts et answer key

- **Synthèse POST** : verdict global **FAIL → PASS** · non-régression **TRUE** · 4 failles FAIL résorbées + 1 adjudication close — download/rapport-campagne-task76-post-synthese.json.
- correct-work (projet) **--bloc n°1** (blocs G1→G5) : **PASS** (0 S1 · 0 S2 ; 5 constats S3/S4-class résorbés en round — tous bugs de harnais).
- Answer key : D001-D009 verified à ce stade (D010-D014 au G7/G8).
- Fenêtre native AFFICHE-PLAN (E7-DISP point 6) : affichée au début d'exécution et mise à jour à chaque fin de groupe G1→G8.

## 12. Pendance PUSH (KO-L009 — héritage)

Aucun push ni manipulation de jeton par l'agent durant la Task 76. Les commits (Task 70-76) sont à pousser **par le propriétaire uniquement**, après **révocation du PAT exposé** (un jeton collé en conversation doit être considéré compromis : révocation puis rotation recommandées avant tout push). Les 131 mode-purs Task 74 restent en attente de leur commit au G3 GO de la Task 74 (R2 — la Task 76 ne les a pas commités).
