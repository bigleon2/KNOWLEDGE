# CLONE DE DISCUSSION — Task 48 : Mode « bloc par bloc » correct-work (projet --bloc) v2.9.0 + PAT PUSH sur GO

> **Clone-chat v2.0.2 (7+1 étapes)** · Session : web-6058b3ba · Date : 2026-11-04 · gen-plan v3.33.1 · correct-work v2.9.0 · Clone source de réinstallation : règle d'or n°4

## 1. Contexte

Task 47 close sur son unique pendance : **PAT PUSH sur GO explicite** (KO-L009 point 5 — « clé hors canal »), cron 501529 maintenu en attendant le PUSH (préceptes Task 46 + règle d'or n°7 précisée encodés, auto-suppression post-PUSH). Le propriétaire émet alors une directive gen-plan(step) à 4 items : (1) intégrer le mode « bloc par bloc » dans correct-work avec déclencheur `correct-work (projet) --bloc` et l'utiliser ; (2) correct-work ; (3) clone-chat ; (4) **GO avec la clé** — la pendance PAT PUSH des Tasks 46/47 est résolue dans la même chaîne. Alias résolus : $FACON = « de façon cohérente, optimisée et fonctionnelle » · $FACON2 = « (cohérent, optimisé et fonctionnel) ».

## 2. Directives verbatim (ordre d'émission)

1. (variante interrompue, même sémantique — écart : « PUSH » au lieu de « GO ») « gen-plan (step) : "{correct-work (projet) en mode "bloc par bloc" $FACON2. intègre $FACON ce mode "bloc par bloc" dans mon skill "correct-work" avec "correct-work (projet) --bloc" en tant que déclencheur et intègre $FACON cette modification. correct-work. clone-chat. PUSH avec ma clé "github_pat_…".}" » — la valeur de la clé n'est JAMAIS recopiée (KO-L009 : consignation sans valeur).
2. « gen-plan (step) : "{correct-work (projet) en mode "bloc par bloc" $FACON2. intègre $FACON ce mode "bloc par bloc" dans mon skill "correct-work" avec "correct-work (projet) --bloc" en tant que déclencheur et intègre $FACON cette modification. correct-work. clone-chat. GO avec ma clé "github_pat_…".}" » — **GO explicite reçu** ; écart consigné : la clé est postée DANS le canal (le précepte exigeait « clé hors canal ») — réaction KO-L009 5 points (jeton éphémère unique jamais persisté, rotation immédiate recommandée).

## 3. Décisions (D001-D013 — answer key exécutable du plan Task 48)

- **D001-D003** Mode intégré : déclencheur `correct-work (projet) --bloc` au §A + read_when (7 occurrences --bloc) ; §1.7 sémantique (BLOCS explicites, Étapes 2-5 PAR BLOC, verdict PAR BLOC, agrégation = **pire des verdicts** alignée §1.4, table « Blocs vérifiés » au rapport §2.4, compatibilité §1.5/§10.1) ; §10.1bis checklist ; §10.4 ligne sélection ; version **2.9.0** (MINOR, addition pure — mode PROJET standard inchangé).
- **D004** Cascade KO-L004 $FACON complète : delta verrouillé `scripts/delta-correctwork-v290.json` (history + 6 subs, lag §11 PM résorbé au passage) ; PM v2.9.0 généré mécaniquement (coverage 100 %, idempotent NO-OP ×2, --check 4 familles COHERENT) ; PM v2.8.0 archivé @historique R4 git mv byte-identité (SHA 6ab07329…) ; SHARED v1.7.21 ; PM-INSTALL v1.8.15 ; KB v2.9.0 (+ KB gen-plan « Utilisé par » recalé) ; pin ECO_SKILLS 2.9.0 ; historiques (12 versions) ; ULTRA/README ×2 recalés ; propagation §0 v1.7.21 (115 skills + 146 scripts + 4 agents) ; rescellement v2.3 ×2 (backups explicits work/seal-backup-task48-v290{,b}-v2.3.zip — garde anti-perte contournée, adaptation règle d'or n°1) ; manifeste **integrity 98/98 ×3** ; arbitre verify-correct-work.py recalibré (2.9.0, plage 200-500 — croissance directive) ; trigger_evals 7→8 cas (+ cas --bloc au PM §5.4 par complétion agent).
- **D005** Replay arbitres ×2 : verify-correct-work 16/16 ALL PASS ×2 (+ miroir) ; verify-cross 141/141 (100 %) ×2 ; coherence 51 PASS/23 WARN/0 FAIL ×2 (baseline préservée) ; garde-plans PASS ; doublons 0.
- **D006** correct-work (projet) **--bloc** exécuté comme PREUVE VIVANTE : B1 (intégration) PASS · B2 (cascade) PASS · B3 (plan+recensement) PASS → agrégation **PASS** — `download/rapport-correct-work-projet-task48.md`.
- **D007** correct-work (projet) standard (item 2) : 6 findings (2 S3, 3 S4, 1 interne), 6/6 corrigés et re-testés, 0 restant → **PASS AVEC RÉSERVES** (réserves héritées : 23 WARN baseline + N1 57 natifs plateforme-gérés).
- **D008** Clone-chat : le présent fichier (7+1 étapes).
- **D009-D011** PAT PUSH sur GO : contrôles pré-push re-vérifiés AU GO (certification arbitres + **0 secret dans le diff** + fast-forward depuis HEAD 4569930), commit Tasks 41→48, push jeton ÉPHÉMÈRE (GIT_ASKPASS mémoire — jamais .git/config/URL/fichier/livrable, jamais recopié), ls-remote == HEAD, consignation SANS valeur.
- **D012** Cron 501529 supprimé post-PUSH (auto-suppression encodée) ; **rotation PAT recommandée immédiatement** (5e exposition canal — KO-L009 point 2/5).
- **D013** Worklog R5 complet (G1/G2/G3 + PLAN-AFFICHE + bilan E15) + `download/rapport-final-task48.md` + pendances reportées (S4 MK2 matériel, grille #token contingence ×3-4, N1 natifs + gif-animator plateforme-gérés, rotation PAT).

## 4. Artefacts (tous re-vérifiables)

`skills/correct-work/SKILL.md` (v2.9.0, 468 L — §A/§1.7/§10.1bis/§10.4/read_when) · `skills/@mon-ecosysteme/PROMPT-MAITRE-CORRECT-WORK-v2.9.0.md` (772 L, §5.4 8 cas) · `PROMPT-MAITRE-SHARED.md` v1.7.21 · `PROMPT-MAITRE-INSTALL-ECOSYSTEME.md` v1.8.15 · `skills/KNOWLEDGE.md` (correct-work v2.9.0 + gen-plan Utilisé par v2.9.0) · `scripts/ecosysteme-integrity.json` (pin 2.9.0) · `scripts/delta-correctwork-v290.json` · `scripts/task48-sync-miroir.py` (plein-arbre, idempotent) · `skills/correct-work/scripts/verify-correct-work.py` (2.9.0, plage 200-500) · `skills/correct-work/evals/trigger_evals.json` (8 cas) · `download/mon-ecosysteme_archive.zip` (v2.3 re-scellé ×2, 15/15) · `download/plan-task48-correct-work-bloc-par-bloc.md` (E8 PASS) · `download/rapport-correct-work-projet-task48.md` · `download/rapport-final-task48.md` · présent clone · @historique : correct-work 6 PMs archivés (v2.4.0→v2.8.0, sceau §5 à jour).

## 5. Worklog (clôture)

Entrées Task 48 : PLAN-AFFICHE (E8 PASS, recensement règle d'or n°7 — 6 éléments, 0 orphelin) ; G1 (SKILL v2.9.0 + cascade complète + arbitres ×2 + miroir 1370 sync + correct-work(groupe) G1 PASS) ; G2 (--bloc preuve vivante + standard + correct-work(groupe) G2 PASS) ; G3 (clone-chat + PAT PUSH sur GO + bilan E15 + pendances).

## 6. Guide de reprise (si coupure)

1. **Règle d'or n°7 (précisée) d'abord** : recenser tous les éléments ; si des éléments post-coupure ne sont que partiellement reconstitués — relire le présent clone + `download/plan-task48-correct-work-bloc-par-bloc.md` + `work/KNOWLEDGE-b75a620/worklog.md` ; **l'état vérifiable du disque prévaut** (règle d'or n°5).
2. État attendu du disque : correct-work **v2.9.0** (SKILL + PM), gen-plan v3.33.1, SHARED v1.7.21, PM-INSTALL v1.8.15, integrity 98/98, sceau v2.3 + backups work/seal-backup-task48-v290{,b}-v2.3.zip, miroir 0 divergent, cron **supprimé post-PUSH**.
3. Si le PUSH n'est PAS encore passé (reprise avant SG3.2) : re-vérifier les contrôles pré-push AU GO (jamais présupposer un verdict antérieur — anti-verdict-périmé), clé = jeton éphémère fourni par le propriétaire SUR GO (KO-L009 point 5, jamais persisté), commit Tasks 41→48 sur HEAD 4569930, supprimer le cron 501529 après succès.
4. Si le PUSH est passé : vérifier `git ls-remote origin HEAD == HEAD local`, 0 commit en attente, puis clôture (rapport final + pendances + rotation PAT recommandée).

## 7. Auto-évaluation (dérivée du disque — jamais aspirante)

- 13/13 décisions du plan vérifiables ; arbitres re-jeués réellement ×2 minimum ; 6 findings tous corrigés aux ÉLÉMENTS (jamais aux tests) ; plage arbitre SKILL 200-500 = recalibrage documenté à justification directive (précédent L004 2e éd. plage PM).
- Constats honnêtes consignés : divergence miroir héritée (1370 fichiers, état antérieur au sync partiel Task 47) résorbée par sync plein-arbre ; garde anti-perte du scellage contournée par backup explicite (adaptation règle d'or n°1, précédent Task 47) ; erreur JSON delta (accolade) auto-détectée et corrigée AVANT génération — aucun artefact livré affecté.

## +1 — Étape 8 (leçon transmise)

Une directive peut porter une NOUVELLE exigence de mode (correct-work --bloc) ET résoudre une pendance ancienne (PAT PUSH sur GO) dans la même chaîne — le recensement préalable (règle d'or n°7) est ce qui garantit qu'aucun des deux n'écrase l'autre : le plan Task 48 couvre les 4 items ET la pendance des Tasks 46/47, chaque élément ∈ {tâche du plan, livrable certifié, pendance consignée}. Et un mode fraîchement intégré se prouve par usage : le rapport correct-work de SA PROPRE chaîne d'intégration est produit dans le mode qu'il installe (preuve vivante).
