# Clone-chat — Session web-ecef7f80 · Task 73 — Tests fonctionnels et performances (gen-plan hôte · écosystème hôte · gen-plan miroir)

Archive auto-suffisante générée par clone-chat v2.0.2 — 2026-11-09T01:58:00Z.

## §0 — Métadonnées et héritage

- **Session** : web-ecef7f80-814d-46ee-a19e-86b14a019531 · **Chat** : 891cbdaf-5243-420e-9c3a-50feb93ef417 · **Canal** : zai-web · **Trace directive** : 1a1b853d77f65451.
- **Directive clôturée** : « génère $FACON, effectue des tests $FACON2 fonctionnels et performances sur mon skill "gen-plan", mon écosystème hôte et sur le skill "gen-plan" du miroir dans l'objectif de corriger $FACON leurs failles et d'optimiser $FACON leur fonctionnement et leurs interactions au sein de mon écosystème. » ($FACON = « de façon cohérente, optimisée et fonctionnelle » · $FACON2 = « (cohérent, optimisé et fonctionnel) » — registre skills/@historique/@Alias/aliases.json).
- **Héritage** : Task 70 (intégration ghorg, CLOSE) · Task 71 (plan step 7 items + R1/R2 + durcissement francophone, CLOSE) · Task 72 (re-curation gen-plan v3.39.0 + fenêtre native AFFICHE-PLAN + skill re-curation v1.0.0, CLOSE 15/15).
- **Commits dépôt** : a790d04 (Task 73 — campagne + rapports + worklog suites 42-48) · précédents : 4439592 (Task 72 CLOSE), 5646e96, d3ee6e6.
- **Pendance inter-taskes** : PUSH des commits Task 70+71+72+73 PAR LE PROPRIÉTAIRE uniquement, après révocation du PAT exposé (KO-L009 — jamais utilisé ni stocké par l'agent).

## §1 — Contexte et décisions (auto-suffisant)

1. **Mission** : campagne de tests FONCTIONNELS et de PERFORMANCES sur trois cibles — C1 skill gen-plan hôte (skills/gen-plan/ v3.39.0), C2 écosystème hôte (skills/), C3 skill gen-plan du miroir (KNOWLEDGE-repo/skills/gen-plan/ + ancrages dépôt) — objectif : corriger les failles + optimiser fonctionnement et interactions.
2. **Protocole $FACON2** (download/protocole-tests-fonctionnels-performances-task73.json) : 26 tests (17 fonctionnels, 7 performances/méta, 2 hybrides), échelle PASS < PASS AVEC RÉSERVES < FAIL, agrégation pire-des-verdicts, phases PRE (capture SANS correction) / POST, non-régression stricte test à test ; tolérances documentées (WARN B1 légitime hérité ; sweep v3.38.0 = WARN à adjudication).
3. **Outillage R4** : scripts/task73-campagne-tests.py orchestre 9 arbitres existants (zéro duplication de logique de verdict), mesure les durées, AUCUNE écriture corrective (ensure-installed volontairement non appelé en PRE) ; selftest 8/8 ; modes --phase/--cible/--synthese/--protocole/--selftest.
4. **Résultats PRE** : C1 **PASS 11/11** (contrats verbatim intacts, evals 9+15, selftests 7/7, re-curation C1-C4 PASS, PM --check ×4 COHERENT, 29,95 Kio ≤ 30 Kio, 130 ms) · C2 **FAIL** — racine unique : version-management absente hôte (7ᵉ récidive du jour), confirmée par 3 tests indépendants (integrity « SKILL.md manquant », coherence « répertoire absent » + 2 WARN conséquences, effectifs KB manquants [vm]) · C3 **PASS 7/7** (identité byte hôte↔dépôt, PM SHA 918bc692…, KB/historiques v3.39.0, ULTRA f40ea21e…, 4,7 ms).
5. **Correction $FACON (G5)** : restauration par la garde Task 56 — `ensure-installed.py --check` → **INSTALLE-REPARÉ rc=0** (vm v1.3.0 recopiée du miroir local, aucun jeton) ; cause racine revérifiée : **environnementale** (volatilité sandbox ; aucun script écosystème ne supprime skills/ — tous les rmtree sont tmp/selftest/réparation ; aucun rsync --delete ; git hôte hors skills/) ; parade adéquate = garde auto-réparation, démontrée en réel.
6. **Résultats POST** : C1 PASS 11/11 · C2 **PASS AVEC RÉSERVES** (0 FAIL ; 2 réserves = tolérances adjudiquées légitimes : WARN B1 hérité + auto-références historiques v3.38.0 de la table des hooks gen-plan lignes 116-117) · C3 PASS 7/7 · **verdict global PRE FAIL → POST PASS AVEC RÉSERVES · non-régression True (0 dégradation) · failles résorbées C2-F01/F02/F05** · poids : 71 skills · 0 CRITIQUE (vm comptée LOURD).
7. **Fenêtre native AFFICHE-PLAN** (E7-DISP point 6, héritage D015 Task 72) : liste de tâches native (TodoWrite) affichée au début de l'exécution et mise à jour à chaque fin de groupe G1→G8 — preuve vivante de la présente session.

## §2 — Artefacts vérifiables

| Artefact | Preuve |
|---|---|
| Plan (13 décisions, E8 final) | download/plan-task73-tests-fonctionnels-performances-genplan-ecosysteme-miroir.md |
| Protocole $FACON2 | download/protocole-tests-fonctionnels-performances-task73.json |
| Campagne PRE (gelée) | download/rapport-campagne-task73-pre-{C1,C2,C3}.json |
| Campagne POST | download/rapport-campagne-task73-post-{C1,C2,C3}.json |
| Synthèse comparative | download/rapport-campagne-task73-post-synthese.json |
| Rapport final | download/rapport-tests-fonctionnels-performances-task73.md |
| Script campagne (selftest 8/8) | scripts/task73-campagne-tests.py |
| Re-jeu answer key (12/12 puis 13/13) | scripts/task73-rejeu-answer-key.py |
| Worklog | suites 42-49 (hôte + miroir synchronisés) |
| Commit dépôt | a790d04 |

## §3 — État de sortie et reprise mécanique

- **État écosystème** : 71 skills (vm v1.3.0 restaurée) · 0 CRITIQUE · arbitres integrity 0 FAIL · coherence 0 FAIL (1 WARN B1 légitime) · cross 100 % · vcw fonctionnel · gen-plan hôte == miroir v3.39.0.
- **Reprise post-coupure recommandée** : (1) exécuter `python3 skills/gen-plan/scripts/ensure-installed.py --check` (garde canonical — répare automatiquement toute entrée KB disparue) ; (2) optionnel : `python3 scripts/task73-campagne-tests.py --phase pre --cible C2` (~300 ms) comme détection systématique complémentaire ; (3) la re-curation future de version-management (cible n°1 de la liste Task 72) démarre par `protocole-test.py --post` si l'état a changé depuis la baseline GO capturée (download/protocole-test-version-management.json).
- **Pendance PUSH** : commits Task 70+71+72+73 à pousser par le propriétaire uniquement, après révocation du PAT exposé (un jeton collé en chat doit être considéré compromis : révoquer puis rotation avant tout push).
- **Position** : Task 73 CLOSE — aucune tâche en vol.

## §4 — Leçons (knowledge-observer)

- **L-73-a (harnais vs système)** : ne jamais tester un verdict par l'ABSENCE d'une chaîne (« FAIL ») dans une sortie — les libellés de scénarios contiennent légitimement cette chaîne ; critère = ligne de verdict explicite (« RESUME : OK », « VERDICT : PASS ») + code retour. 2 des 3 bugs de harnais de la campagne venaient de là.
- **L-73-b (CLI sous-documentée)** : le wrapper cache-verdicts.py exige `--cibles` (rc=3 + message explicite) — lire le message d'erreur d'usage AVANT de conclure à une défaillance du mécanisme.
- **L-73-c (mono-racine par conséquences)** : les WARN « evals absents » ont disparu avec la restauration de vm — la disparition des symptômes conséquences confirme mécaniquement la mono-racine d'une faille.
- **L-73-d (PRE gelé)** : la phase PRE ne doit JAMAIS être ré-exécutée après corrections (elle écraserait les preuves) — le re-jeu d'answer key vérifie les artefacts gelés en lecture seule.
- **L-73-e (agrégation par phase)** : un verdict global « POST » ne doit agréger QUE les verdicts POST — inclure les PRE pollue le verdict de sortie (3ᵉ bug de harnais).

## §5 — Worklog

Entrées « ## 2026-11-08 (suite 42 à 49), session web-ecef7f80 » de worklog.md (hôte et dépôt synchronisés — préfixe miroir ⊆ hôte vérifié par copie intégrale post-suite 49), conformes SHARED §1.4 : directive verbatim, preuves mécaniques par groupe, PLAN-AFFICHE à chaque clôture, fenêtre native maintenue de l'ouverture à la clôture.
