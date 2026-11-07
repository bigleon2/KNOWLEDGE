# Clone de discussion — 2026-11-08 — Task 72 : Chantier R1 re-curation gen-plan + fenêtre native AFFICHE-PLAN + adéquation + liste priorisée + skill re-curation + tests + correct-work --bloc + clone-chat (session web-ecef7f80, continuation Task 71)

## §0 — Métadonnées et héritage

- **Session** : web-ecef7f80 (2026-11-08) — continuation de Task 71 (CLOSE, archive download/clone-chat-session-web-ecef7f80-20261108.md) et Task 70.
- **Directives exécutées** : 7 items trace 1a1b79af6dcff4c5 (« Chantier R1 : re-curation progressive disclosure de gen-plan » + adéquation + liste priorisée + skill re-curation + tests $FACON + correct-work --bloc + clone-chat) ; **directive complémentaire 1** trace 1a1b7b297b7b4975 (skill re-curation IMPLÉMENTÉ d'un script — tests avant re-curation, maintien de l'optimisation, comparaison de méthodes) ; **directive complémentaire 2** trace 1a1b7fe1c7238e8d (fenêtre native d'affichage du plan via le mécanisme natif Z.ai — début d'exécution + chaque fin d'étape — intégrée à AFFICHE-PLAN/E7-DISP).
- **Plan** : download/plan-task72-recuration-genplan-adequation-liste-skill-recuration.md — rév. 3, 15 décisions (D001-D015), E8 FINAL PASS 23:59:00Z, answer-key-checker 16/16.
- **Commits dépôt** : 5646e96 (G1), d3ee6e6 (G4+G5), + commit de clôture G6/G7 (worklog suite 41) — PUSH = propriétaire (KO-L009/D013).

## §1 — Contexte et décisions (résumé auto-suffisant)

1. **G1 — Chantier R1 CLOSE** : gen-plan v3.38.0→v3.39.0 — re-curation progressive disclosure : 9 blocs déplacés R4 byte-identité vers references/ (journal-versions 33,3 Ko · regles-or 26,0 [+ leçons KO] · disciplines-mobilisation 12,2 · protocoles-detailles 20,3) + append contingences grille-token.md ; résumés NOUVEAUX inline ; **SKILL.md 104,0 → 29,9 Kio (−71,2 % #token ≈ 26 616→7 667, CRITIQUE → INTERMÉDIAIRE rang 10, 0 CRITIQUE dans l'écosystème)** ; contrats baseline golden master D001-D005 PASS (task72-baseline-verifier.py, harnais v2 : étiquette SHARED du §0 normalisée — preuve modulo-étiquette SHA bb8fe775…) ; cascade KO-L004 complète : PM v3.39.0 (211 Ko/1 770 L, delta verrouillé delta-genplan-v3390.json — 11 subs, intégraux in extenso §9.7-§9.10, AUCUNE duplication intra-PM), SHARED v1.7.34 / PM-INSTALL v1.9.10, PM v3.38.0 archivé R4 (sceau 4c05a74e…, 50 PMs), pin/KB/historiques (lags v3.37.1/v3.35.2 résorbés), README corpus v2.1.19, ULTRA ×2, propagation §0 (69+173+2, contenu stable), sweep 9 skills, arbitres 110→112/110 · 54/1/0 · 16/16 · 100 % (recalibrage 3ᵉ éd. KO-L003 plage PM 1200-1900 L), archive re-scellée v2.3 ×2, version-management 6ᵉ disparition auto-réparée INSTALLE-REPARÉ, sync 0 divergence.
2. **SG1.3bis — fenêtre native AFFICHE-PLAN (directive complémentaire 2)** : E7-DISP point 6 — la fenêtre des étapes du plan s'affiche via le **mécanisme natif de l'agent dédié à ce rôle (Z.ai : liste de tâches — TodoWrite/TodoRead)** au DÉBUT de l'exécution du plan d'actions + MISE À JOUR à chaque FIN d'étape ; canal SUPPLÉMENTAIRE (bloc chat + marqueur worklog PLAN-AFFICHE + garde P1-P5 inchangés) ; intégral references/protocoles-detailles.md (section extension, hors blocs R4) ; SKILL.md 29,95 Kio < 30 maintenu par compensation (résumés non verrouillés compactés) ; **preuve vivante : fenêtre native affichée à l'ouverture et mise à jour à chaque fin de groupe G1→G6**.
3. **G2 — adéquation** : 4 arbitres 0 FAIL (integrity 112/112 · coherence 54/1/0 PASS AVEC RÉSERVES [WARN B1 légitime] · vcw 16/16 · cross 100 %) + 4 selftests (7/7 · 10/10 · 12/12 · rc=0) + evals 9+15 byte-identiques + couverture PM complète (classe WARN §1.13 résorbée par construction) — D007.
4. **G3 — liste priorisée** : 7 LOURD écosystème classés (version-management → iphone19 → iphone18 → skill-creator [noyau 12 dépendants, protocole renforcé] → web-reader → cahier-des-charges → iphone17) + pdf/pptx PLATEFORME (hors gouvernance — décision propriétaire) ; cartographie sèche version-management (~23,1 Kio déplaçables, contrainte miroir documentée) — D008.
5. **G4 — skill re-curation v1.0.0** : IMPLÉMENTÉ du script principal scripts/protocole-test.py (--pre : protocole ADAPTÉ généré [nature détectée] + baseline golden master + GO/NO-GO · --post : MAINTIEN DE L'OPTIMISATION [cohérent/fonctionnel/optimisé] · --verifier C1-C4 · --compare : R4-compliantes seules éligibles) + mesure-sections.py + check-recuration.py (selftests 5/5 · 3/3 · 4/4) + méthode P0-P7 + evals 6+12 + cascade légère (KB + réciprocités + pin + historiques + §0 canonique + ULTRA + arbitres + re-scellement) — D009.
6. **G5 — tests $FACON réels** : PRE version-management GO (baseline cible n°1 capturée) + paire PRE/POST gen-plan → MAINTIEN DE L'OPTIMISATION + VÉRIFICATION gen-plan C1-C4 PASS ×2 (validation rétroactive G1) + --compare réel (moves-r4-pur, suppression disqualifiée) + idempotence ×2 (SHA b66f338a stable) — D010.
7. **G6/G7** : correct-work --bloc — verdicts par groupe G1-G5 PASS (0 S1 · 0 S2 ; S3-class résorbés documentés : recalibrage KO-L003, harnais v2 baseline, harnais mesure +1/section, §0 canonique, lags en-têtes) + answer-key-checker 16/16 + E8 final 15/15 verified ; clone-chat (présente archive) — D011, D012.

## §2 — Artefacts produits (vérifiables sur disque)

- Plan : download/plan-task72-recuration-genplan-adequation-liste-skill-recuration.md (rév. 3 final, 15/15 verified)
- Skill : skills/re-curation/ (SKILL.md + scripts/protocole-test.py + mesure-sections.py + check-recuration.py + evals ×2) ; @historique/historiques-par-skill/re-curation.md
- gen-plan v3.39.0 : skills/gen-plan/SKILL.md (29,9 Kio) + 15 fichiers references/ + PM skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.39.0.md + PM v3.38.0 archivé @historique
- Scripts de passe : scripts/task72-{amendement-affiche-plan,delta-v3390,cascade,cascade2,resceller-archive}.py + delta-genplan-v3390.json + task72-baseline-verifier.py (harnais v2)
- Rapports : download/rapport-adequation-genplan-task72.md · download/liste-recuration-priorisee-task72.md · download/rapport-tests-recuration-task72.md · download/rapport-final-task72.md · download/task72-verif-recuration.json · download/protocole-test-{gen-plan,version-management}.json · download/task72-baseline-genplan.json
- Worklog : suites 36-41 (hôte + miroir — source R4 des états)

## §3 — État de sortie et reprise mécanique

- **Task 72 CLOSE** — 7/7 items + 2 directives complémentaires exécutés ; plan 15/15 verified, E8 final PASS.
- **Pendance unique** : PUSH des commits (Task 70 : cea7d12, 886604d ; Task 71 : 1f80594, 8acc8c1, 2daaa9b, 011d342 ; Task 72 : 5646e96, d3ee6e6 + commit de clôture) PAR LE PROPRIÉTAIRE uniquement, APRÈS révocation du PAT exposé au chat (KO-L009 — jamais utilisé ni stocké par l'agent).
- **Reprise éventuelle** : la prochaine re-curation (version-management, cible n°1) démarre par `python3 skills/re-curation/scripts/protocole-test.py --post version-management` après la passe de re-curation — la baseline PRE est déjà capturée (download/protocole-test-version-management.json, GO).

## §4 — Leçons session (propositions knowledge-observer)

- **L-72-a** : les baselines golden master qui verrouillent des étiquettes de version transverses (SHARED) deviennent fausses au premier bump écosystème — normaliser les étiquettes à la comparaison (harnais v2), jamais ré-écrire la baseline.
- **L-72-b** : les arbitres à invariants chiffrés figés (plage de lignes PM) divergent quand la réalité change légitimement (in extenso) — recalibrer l'arbitre avec la divergence documentée dans son commentaire (KO-L003), jamais ajuster la réalité.
- **L-72-c** : un amendement pré-publication (version non encore cascadée) est R2-propre et économise une cascade entière — la fenêtre entre « version installée hôte » et « version publiée dépôt » est la fenêtre d'amendement.
- **L-72-d** : le re-scellement du véhicule d'intégrité (zip) doit être la DERNIÈRE écriture d'une cascade (toute écriture postérieure sur corpus/piliers/ULTRA/KB le périme — 2 re-scellements nécessaires cette session).
- **L-72-e** : la fenêtre native d'affichage (TodoWrite) est un canal d'affichage agent-side sans trace disque — la preuve journalisable reste le marqueur worklog ; consigner les mises à jour de fenêtre dans la même entrée.

## §5 — Worklog (extrait — forme conforme SHARED §1.4, dépôt = source R4)

Suites 36-41 du worklog.md (hôte + miroir synchronisés) — entrées complises : G1 (cascade + correct-work groupe), G2 (adéquation), G3 (liste), G4+G5 (skill + tests), G6/G7 (finalisation). Verdicts mécaniques : baseline-verifier PASS ×2 · poids INTERMÉDIAIRE rang 10 · integrity 112/112 ×2 · coherence 54/1/0 ×2 · vcw 16/16 · cross 100 % · answer-key-checker 16/16 · check_plan_protocol P1-P5 · selftests 12/12 · idempotence ×2 multiple.
