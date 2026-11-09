# CLONE DE DISCUSSION — Task 47 : Règle d'or n°7 (mémoire complète — PRÉCISÉE) + plan re-généré en mode STEP

> **Clone-chat v2.0.2 (7+1 étapes)** · Session : web-6058b3ba · Date : 2026-11-04 · gen-plan v3.33.1 · Clone source de réinstallation : règle d'or n°4

## 1. Contexte

Chaîne propriétaire Tasks 38→46 terminée et certifiée (recensement §des clones). Task 46 close sur son unique pendance : PAT PUSH (GO propriétaire). Le propriétaire émet alors trois directives : (1) règle d'or « se rappeler précisément de TOUS les éléments de la discussion à traiter dans les tâches du plan ; si oubli dû à une coupure → relire les clones et les sauvegardes », devant devenir une **règle d'or** ; (2) « recommence en utilisant le mode STEP » ; (3) précision sémantique : « ce que tu as oublié » = « les éléments oubliés à cause d'une coupure et que tu as partiellement réussi à reconstituer » — à prendre en compte **avant gen-plan**.

## 2. Directives verbatim (ordre d'émission)

1. « je précise que tu dois te rappeler précisément de tous les éléments de la discussion que tu dois traiter dans tes taches du plan d'actions et pour cela si tu as oublié quelque chose à cause d'une coupure alors tu dois relire les clones et les sauvegardes de la discussion pour prendre en compte les parties que tu as oubliées. recommence la génération de ton plan d'actions en prenant compte de cette directive qui doit devenir une règle d'or »
2. « recommence en utilisant le mode STEP de mon skill "gen-plan" »
3. « continue mais avant gen-plan : "prend en compte que lorsque je précise que lorsque je disais "ce que tu as oublié" alors je voulais dire "les éléments oubliés à cause d'une coupure et que tu as partiellement réussi à reconstituer"." »

## 3. Décisions (D001-D017 — answer key exécutable)

- **D001** Recensement mécanique des 11 directives (relecture : 3 clones + rapports task46 + worklog intégral) — AUCUN ÉLÉMENT ORPHELIN.
- **D002-D007** Règle d'or n°7 installée (v3.33.0 : SKILL §1.5 + PM + cascade KO-L004 ×2 arbres + KB + pin + historiques + lignes vives + propagation + rescellement + miroir + re-génération du plan) puis **PRÉCISÉE** (v3.33.1 : même cascade).
- **D008/D017** Cron recréé ×2 (501373 → 501446 → **501529**) — payload : règle précisée + préceptes Task 46 + PAT PUSH sur GO.
- **D009/D010/D016** Re-certification RÉELLE : integrity 98/98 ×3, verify-cross 141/141, coherence 51/23W/0F (plage L004 2e éd.), N2 5/5, garde-plan PASS (réparé), doublons 0, batterie task45 20/20 ×2 (re-pointée sur le clone vivant), tsi-validator self-test + task46 rc=0.
- **D011** correct-work (projet) : PASS AVEC RÉSERVES, 0 finding ouvert (7 constats corrigés aux ÉLÉMENTS, jamais aux tests).
- **D012/D013** Bilan E15 (G-RES OK, leçons ×4, contingence grille ×3-4) + rapport final + présent clone.
- **D014** Worklog R5 complet (rattrapage G1-G3 dérivé du disque + G4-G6 + PLAN-AFFICHE) + pendances.
- **D015** Précision sémantique v3.33.1 : l'« oubli » = éléments post-coupure partiellement reconstitués ; reconstitution partielle ≠ mémoire complète ; état disque prévaut. **Preuve vivante** : le résumé post-compression affirmait « règle non persistée / plan non commencé » alors que le disque portait v3.33.0 + plan + recensement.

## 4. Artefacts (tous re-vérifiables)

`skills/gen-plan/SKILL.md` (v3.33.1, n°7 précisée) · `skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.33.1.md` (point 2 précisé + point 5) · `PROMPT-MAITRE-SHARED.md` v1.7.20 · `PROMPT-MAITRE-INSTALL-ECOSYSTEME.md` v1.8.14 · `skills/KNOWLEDGE.md` (calibration 3.33.1) · `scripts/ecosysteme-integrity.json` (pin 3.33.1) · `scripts/delta-genplan-v333{0,1}.json` · `scripts/task47-regle-or-7-edits.py`, `scripts/task47-b-precision-v3331-edits.py`, `scripts/task47-c-correctifs-arbitres.py`, `scripts/task47-e-scan-fix-future.py` (idempotents ×2) · `download/mon-ecosysteme_archive.zip` (v2.3 re-scellé, 15/15) + `work/seal-backup-task46-v2.3.zip` + `work/seal-backup-task47-v3330-v2.3.zip` · `download/plan-task47-regle-or-7-mode-step.md` · `download/rapport-recensement-discussion-task47.md` · `download/rapport-correct-work-projet-task47.md` · `download/rapport-final-task47.md` · @historique : 33 PMs gen-plan (v3.6.1→v3.33.0) + sceaux §5 à jour.

## 5. Worklog (rattrapage + clôture)

Entrée Task 47 (E7-DISP, plan affiché) préexistante ; la clôture journalise : reprise E1-RES post-coupure (audit disque : G1-G3 terminés par artefacts, T2.4.2/G5/G6 restants), cascade v3.33.1 complète, G3 cron 501529, G4 re-certification réelle + 3 correctifs éléments (docstrings §0/__future__ ×10, plage PM L004 2e éd., miroir complété + batterie re-pointée), G5 correct-work projet PASS AVEC RÉSERVES, G6 clôture — marqueur **PLAN-AFFICHE**.

## 6. Guide de reprise (si coupure)

1. **Règle d'or n°7 d'abord, forme précisée** : recenser tous les éléments ; si des éléments ont été oubliés à cause d'une coupure — les éléments **partiellement reconstitués** — relire les clones/sauvegardes (les plus récents `download/clone-discussion-*.md` + `download/rapport-recensement-discussion-task47.md` + `work/KNOWLEDGE-b75a620/worklog.md`) pour les COMPLÉTER ; une reconstitution partielle (résumé de session) n'est PAS une mémoire complète ; **l'état vérifiable du disque prévaut**.
2. État attendu du disque : gen-plan **v3.33.1** (SKILL + PM), cron **501529** actif, plan `download/plan-task47-regle-or-7-mode-step.md` (E8 PASS), rapports final + CW + recensement + clone présents, sceau v2.3 + backups, miroir 0 divergent, integrity 98/98.
3. Reste à faire : **PAT PUSH uniquement** (GO propriétaire + clé hors canal — KO-L009 point 5 ; commit Tasks 41→47 à créer sur HEAD 4569930 ; contrôles pré-push 4/4 au GO ; supprimer le cron après PUSH).

## 7. Auto-évaluation (dérivée du disque — jamais aspirante)

- 17/17 décisions traitées ; arbitres re-jeués réellement ×2 minimum ; 7 constats d'éléments corrigés ; 0 test retouché pour masquer (la plage PM L004 2e éd. est un recalibrage documenté à justification directive, précédent L004 2026-10-09).
- Constat honnête consigné : la revendication « replay arbitres ×2 » de v3.33.0 (pré-coupure) était aspirante — détectée par la re-certification réelle, corrigée, jamais masquée (règle d'or n°5).

## +1 — Étape 8 (leçon transmise)

Les coupures de contexte sont le risque n°1 de la lignée ; une reconstitution partielle peut être **partiellement fausse**. La règle d'or n°7 (v3.33.1) l'institutionnalise : la relecture des clones/sauvegardes COMPLÈTE les éléments partiellement reconstitués AVANT toute génération/reprise, et l'état vérifiable du disque prévaut sur toute reconstruction mémorielle.
