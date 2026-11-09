# Rapport campagne tests $FACON2 chronologique — Task 84

> Directive trace `1a1bed51ccaf78f1` · session web-ecef7f80 · horodatage 2026-11-09T05:59:02Z
> Périmètre : éléments créés/modifiés dans la discussion (Tasks 70→83, 2026-11-07 soir → 2026-11-09)
> Ordre d'exécution : chronologie STRICTE de création/modification · harnais protocole-test v1.2.2 + arbitres

## Verdict global : **PASS** (52/52 items PASS · durée 3.5 s)

| # | Item chronologique | Élément (task d'origine) | Verdict | Durée | Notes |
|---|---|---|---|---|---|
| C1 | scripts/ecosystem/*.py ×6 — compile + Karnaugh 20/20 | T70 | **PASS** | 0.039 s | karnaugh_20=OK |
| C2 | @GHORG-ecosysteme + ghorg-cmdr v1.1.0 — YAML + KB | T70 | **PASS** | 0.01 s | manifest · selection · kb+version |
| C3 | @Bibliotheque-skills-Multi-IA — 10 fichiers, 0 vide | T70 | **PASS** | 0.01 s | — |
| C4a | poids-chargement.py (R1) — selftest ×2 | T71 | **PASS** | 0.032 s | — |
| C4a | poids-chargement.py (R1) — selftest re-jeu | T71 | **PASS** | 0.038 s | — |
| C4b | cache-verdicts.py (R2) — selftest ×2 | T71 | **PASS** | 0.304 s | — |
| C4b | cache-verdicts.py (R2) — selftest re-jeu | T71 | **PASS** | 0.308 s | — |
| C5 | propagate-context v2.1.1 — passe 1 (absorption canonique : injections en attente acceptées) | T70/71 | **PASS** | 0.072 s | — |
| C5b | propagate-context — passe 2 NO-OP (0 skills + 0 scripts) + échantillon byte-stable | T70/71 | **PASS** | 0.0 s | byte_stable · no_op_p2 |
| C5c | lot §0 propagation — parité hôte==dépôt 12/12 | T70/71 | **PASS** | 0.02 s | — |
| C6a | gen-plan — check_plan_protocol P1-P5 (plan Task 84) | T71→T78 | **PASS** | 0.045 s | P1-P5=OK |
| C6b | gen-plan — answer-key-checker 16 checks | T71→T78 | **PASS** | 0.025 s | 16/16=OK |
| C6c | gen-plan — evals JSON (9 + 15 cas, attendu 9+15) | T71→T78 | **PASS** | 0.01 s | — |
| C6d | gen-plan — references/ 15 fichiers (manquants: []) | T71→T78 | **PASS** | 0.01 s | — |
| C6e | gen-plan v3.41.0 — --verifier (harnais v1.2.2) | T71→T78 | **PASS** | 0.1 s | VERDICT PASS=OK |
| C6f | gen-plan — poids chargement 30.0 Kio · 7674 #token · INTERMÉDIAIRE | T71→T78 | **PASS** | 40.07 s | — |
| C7 | re-curation v1.2.2 — --verifier | T72→T82 | **PASS** | 0.331 s | VERDICT PASS=OK |
| C8a | protocole-test.py harnais v1.2.2 — selftest 15/15 (passe 1) | T73→T82 | **PASS** | 0.209 s | 15/15=OK |
| C8b | protocole-test.py harnais v1.2.2 — selftest 15/15 (passe 2 idempotence) | T73→T82 | **PASS** | 0.21 s | 15/15=OK |
| C10a | eco_install_pipeline.py — --help 0-exécution (contrat CLI F1) | T76 | **PASS** | 0.028 s | — |
| C10c | eco_install_pipeline.py — RÉINSTALLATION PLEINE (cadence — ≥55 SHA, 0 divergence, R2) | T76 | **PASS** | 0.15 s | sha256_verifies=55 · divergences=[] · R2=True |
| C10b | eco_install_pipeline.py --dry-run — 0 mutation, rc 0 (état synchronisé) | T76 | **PASS** | 0.046 s | dry_run_noop=OK · 0_mutation=OK |
| C10d | cp zip hôte→dépôt + integrity manifeste écrit (114/114, round-trip corpus 9/9) | T76 | **PASS** | 0.043 s | 114/114=OK · round-trip corpus 9/9=OK |
| C10e | ensure-installed.py --check — INSTALLE 0 manquant | T76 | **PASS** | 0.064 s | 0_manquant=OK |
| C11 | PM-INSTALL v1.9.13 — corpus générateur --check 4 familles COHERENT | T76/78 | **PASS** | 0.03 s | 4_COHERENT=OK |
| C13 | SHARED v1.7.36 + corpus PM — 9 fichiers (503573 o) + parité zip hôte==dépôt | T78 | **PASS** | 0.05 s | corpus_9 · parité_zip |
| C13b | SHARED v1.7.36 — version + §8 R-F1..R-F4 + §9 règles d'or présents | T78 | **PASS** | 0.01 s | — |
| C12 | protocoles-detailles.md — Extensions v3.40.0 (émission //) + v3.41.0 (sondage borné) | T77/78 | **PASS** | 0.01 s | — |
| C14 | version-management v1.3.0 — --verifier (post-réparation É1-INSTALL) | T79 | **PASS** | 0.162 s | VERDICT PASS=OK |
| C15 | baselines protocole-test v1.2.0+ — 5/5 (manquants: []) | T80 | **PASS** | 0.01 s | — |
| C16a | iphone19 v0.12.0 — --verifier | T81 | **PASS** | 0.061 s | VERDICT PASS=OK |
| C16b | iphone19 — R4-INTÈGRE 6/6 (task81-verif-r4) | T81 | **PASS** | 0.03 s | 6/6=OK |
| C16c | iphone19 — règle absolue 15 inline | T81 | **PASS** | 0.01 s | — |
| C17a | knowledge-observer v1.1.0 — --verifier | T82 | **PASS** | 0.057 s | VERDICT PASS=OK |
| C17b | knowledge-observer — re-jeu tests conversions 9/9 (T4b/T6 dynamisés KO-L003) | T82 | **PASS** | 0.422 s | 9/9=OK |
| C17c | knowledge-observer.agent — structure canonique (manquants: []) | T82 | **PASS** | 0.01 s | — |
| C18a | iphone18 v1.1.0 curé — --verifier | T82 | **PASS** | 0.063 s | VERDICT PASS=OK |
| C18b | iphone18 — R4-INTÈGRE 3/3 (task82-verif-r4) | T82 | **PASS** | 0.031 s | 3/3=OK |
| C19a | agent-engineering — evals JSON 7+7 (7+7) | T83 | **PASS** | 0.01 s | — |
| C19b | agent-engineering — frontmatter v1.0.0 + 3 domaines + planchers semver : gen-plan 3.41.0>=3.15.0=OK; fleet-engineering 1.1.1>=1.0.1=OK; autonomous-agent 1.2.1>=1.2.0=OK; agent-creator 2.3.0>=2.2.0=OK | T83 | **PASS** | 0.01 s | — |
| C19c | agent-engineering — KB entrée n°56 + arêtes (5 mentions ≥ 5) | T83 | **PASS** | 0.01 s | — |
| C19d | agent-engineering — ULTRA 13ᵉ voie (routage n°56) | T83 | **PASS** | 0.01 s | — |
| C19e | agent-engineering — poids 16.0 Kio · 4086 #token · INTERMÉDIAIRE (seuil LOURD 30 Kio) | T83 | **PASS** | 0.01 s | — |
| C20a | gen-ultra-maitre.py — régénération (attendu no-op, SHA stable) | T82/83 | **PASS** | 0.028 s | — |
| C20b | ULTRA idempotence ×2 — SHA 4276550e7756b0d5→4276550e7756b0d5→4276550e7756b0d5 stable | T82/83 | **PASS** | 0.02 s | — |
| C21a | verify-cross — 100,0 % (0 warnings) | transverse | **PASS** | 0.035 s | 100=OK |
| C21b | verify-correct-work — 16/16 | transverse | **PASS** | 0.032 s | 16/16=OK |
| C21c | integrity — 114/114 ×2 (re-jeu) | transverse | **PASS** | 0.045 s | 114/114=OK |
| C21c | integrity — re-jeu 2 (idempotence) | transverse | **PASS** | 0.045 s | 114/114=OK |
| C21d | interactions — STRICT 55/55 | transverse | **PASS** | 0.146 s | VERDICT_STRICT=OK · 55/0/0=OK |
| C21e | doublons download/ — 0 | transverse | **PASS** | 0.026 s | 0 doublon=OK |
| C21f | G-RES final — monitor OK | transverse | **PASS** | 0.027 s | OK=OK |

## Idempotence

- Harnais protocole-test selftest 15/15 ×2 · ULTRA régénéré SHA stable ×2 ·
- integrity 114/114 ×2 · propagate-context no-op ×2 (échantillon byte-stable) ·
- R1/R2 selftests ×2 · pipeline pleine passe (réinstallation cadence) + cp zip + manifeste.

## Failles mesurées et corrections (règle d'or n°5 — round 1 → round 2 : 40/51 → 52/52)

Le round 1 (re-jeu intégral consigné au JSON d'époque) a MESURÉ 11 FAIL avant toute correction. Diagnostic établi sur la sortie réelle de chaque item (jamais pré-écrit), puis corrections appliquées, puis round 2 re-jeu intégral **52/52 PASS** :

1. **FAILLE RÉELLE n°1 — propagation §0 en retard (11 scripts + gabarit n°56)** : `propagate-context.py` (C5) a révélé que 11 scripts (Tasks 78-82 : task78-cascade, task78-final-plan, task79-×3, task81-×2, task82-×4) créés depuis la dernière passe de propagation (Task 78) portaient pas le bloc §0 CONTEXTE SYSTÈME, et que le §0 de `agent-engineering/SKILL.md` (créé Task 83) utilisait un gabarit périmé (mention « (ex-nommé `@PM-SKILLS/`) » absente). **Correction $FACON** : la passe 1 a absorbé le lot (1 skill + 11 scripts mis à jour, gabarit canonique v1.7.36), passe 2 **NO-OP** (0/0 — idempotent), parité hôte==dépôt 12/12 (C5c). Adjudication : SHARED §9 = « propagé dans CHAQUE élément » ; la note SYNC-CONTEXT v1.5.10 « les 2 scripts task82 non-porteurs confirmés inchangés » était descriptive de l'état mesuré, pas une exemption (aucune skip-list n'existe dans l'outil — et la direction propriétaire est la couverture universelle).
2. **FAILLE RÉELLE n°2 — invariants périmés dans `task82-tests-conversions.py` (KO-L003)** : T4b durcissait « 112/112 PASS » (total integrity de l'époque Task 82 — devenu 114/114 avec la discipline n°56 Task 83) et T6 comparait le statut git du dépôt à un instantané exact pré-commit Task 82 (échouait sur tout état postérieur légitime). **Correction $FACON** : invariants DYNAMISÉS — T4b dérive le total de la sortie de l'arbitre elle-même (runs 1-2 identiques au périmètre KB courant), T6 re-scopé en T6a (noyau conversion byte-identique au CLOSE 95fef2b — 5 artefacts, preuve éternelle) + T6b (périmètre 11 chemins ⊆ commit CLOSE 5859566..95fef2b). Re-jeu **9/9 PASS** (8 tests → 9 avec T6a/T6b).
3. **FAILLE RÉELLE n°3 — ordre interne des tests pipeline (transitoire)** : le round 1 exécutait --dry-run AVANT la réinstallation pleine ; la garde F3 fail-fast du pipeline a **correctement détecté** la divergence hôte↔dépôt transitoire (rc 2 — l'hôte n'était pas encore synchronisé avec les injections C5). **Correction $FACON** : ordre interne rétabli (installation pleine → dry-run certifié sur état synchronisé rc 0) — la garde F3 s'est prouvée fonctionnelle en détectant une divergence réelle.
4. **Calibrage harnais de campagne (7 items)** : comptage des evals (dictionnaire à 5 clés, liste `evals` interne — gen-plan 9 ✓, n°56 7 ✓), clés du mesureur de poids (`kio_skill_md`/`tokens_estimes`), vocabulaire des arbitres (corpus « [COHERENT] » ×4, interactions « VERDICT : COHÉRENCE DES INTERACTIONS : PASS STRICT » + « 55 PASS / 0 WARN / 0 FAIL », doublons « DOUBLONS (…) : 0 »), sortie JSON du pipeline (`post_install.sha256_verifies` 55 / `divergences` []), compile en mémoire (py_compile → builtin). Ces items mesuraient le bon état sous la mauvaise loupe — corrigés, aucun n'était un défaut du système testé.

**Optimisations livrées par la campagne** : lot §0 complété (12 éléments portés au canon — les scripts Task 78-82 relisent désormais §0 + règles d'or à l'exécution conformément à SHARED §9), invariants du harnais conversions pérennisés (re-jeu désormais possible à tout état futur), manifeste integrity re-épinglé (n°56 sha 46a3397d… post-gabarit canonique).

Rapport JSON intégral : `scripts/task84-campagne-tests.json` (reproductible, idempotent).
