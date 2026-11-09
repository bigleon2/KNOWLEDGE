# Plan Task 17-RE — re-exécution optimisée post-incident (mise à jour consolidée du plan d'actions)

## Métadonnées

- **Skill** : gen-plan v3.21.0 — mise à jour demandée par le propriétaire (« continue mais avant optimise le plan d'actions actuel en le mettant à jour », 2026-10-11)
- **Remplace** : `plan-task17-b-historique-par-skill.md` (perdu au snapshot) et `plan-task17-reprise-optimisee.md` (perdu) — le présent plan est le SEUL plan vivant de la Task 17
- **GO** : accordé par le propriétaire (« GO avec PAT… » — commit/push autorisés, discipline jeton URL seule)

## État réel re-mesuré (faits byte-level, 2026-10-11)

1. **INCIDENT S3 ÉTENDU (documenté au commit 2df7429)** : le répertoire `work_knowledge/` ENTIER (working tree + `.git`) a été restauré depuis un snapshot au 2026-10-10 20:48 (mtimes et reflog alignés) — la couche Task 17 originelle (codification, cascade, voie L 31/31, harnais 16/16, rapports, plans) ET le plan Task 17-B ont été PERDUS hors contexte de session ; aucune récupération possible (0 blob Task 17 dans l'ODB, miroir profil stalé, origin inchangée).
2. **Riposte en couches commitées/poussées** (fenêtre de vulnérabilité minimale — origin/main = seule zone survivante) : R1 PUBLIÉE (2df7429 : SHARED v1.6.8 §1.2 @historique/ + cascade 145 porteurs + SYNC v1.4.3 + propagate idempotence v2 + fix 4 blocs divergents ; arbitres verts : integrity 60/60, coherence 48/3/0, verify-cross 100 %).
3. **Voie L en cours** : runner réécrit (`scripts/task17-remeasure-voie-l.py`, crash-safe par cas, idempotent) — **20/31 cas** (6 CONFIRME, 9 REFUTE_UNANIME, 5 AMBIGU) au moment de la présente mise à jour.
4. **DÉCALIBRAGE détecté et corrigé** : les votes du premier prompt (sans contrat de déclenchement) ont produit des REFUTE faux sur des cas négatifs officiels (pdf-llm ×3 « Produis un rapport PDF » = création ≠ analyse → false CORRECT ; agent-creator « plutôt qu'avec X » ; script-reviewer ; script-mon ; skills-inventory) — biais « usage général » corrigé par prompt calibré au contrat SHARED §7 v2 (périmètre précis, anti-faux-positif, négatifs explicites) + description frontmatter complète (bloc YAML multi-lignes).
5. **BUG révision corrigé** : `reviser_trigger_evals` ne gérait que le sens True→False — 5 REFUTE avec `revision_appliquee: False` ; fonction désormais bidirectionnelle.
6. **R4 partiellement exécuté** (artefacts sur disque, non commités) : D001 migration verbatim OK (historiques-par-skill ×3 : 22/10/4 lignes), D002 `historique-autres-elements.md` OK, D004 README @historique v1.1.0 OK.

## Optimisations adoptées (par rapport au plan initial)

| # | Optimisation | Justification |
|---|--------------|---------------|
| O1 | Couches R1→R5 commitées+poussées IMMÉDIATEMENT après chaque couche | L'écraseur local frappe sans trace — origin/main = seule protection ; fin du « staging long » |
| O2 | Runner voie L en runs foreground séquentiels de ~9 min (idempotent --skip-done implicite) | Le sandbox tue les processus d'arrière-plan à la fin de chaque commande (nohup/setsid inefficaces) ; le crash-safe par cas rend les reprises gratuites |
| O3 | Prompt de vote calibré au contrat SHARED §7 v2 + descriptions complètes | Élimine les REFUTE faux (biais usage vs contrat) — les re-votes remplacent les décisions suspectes |
| O4 | Re-vote ciblé UNIQUEMENT des cas suspects (5 REFUTE négatifs-officiels + 5 AMBIGU), les 6 CONFIRME + 2 REFUTE ai-news-collectors sont conservés | Économie ~70 % des appels vs re-mesure totale |
| O5 | Révisions bidirectionnelles + `_calibration` trace dans le report (jamais dans les bare-listes — precedent D001 Task 15) | Cohérence schéma canonique |

## E7 — Séquence restante (série par défaut)

1. **R2-fin** : reset des 10 cas suspects → re-votes prompt calibré → 31/31 → re-jouer replay (replay attendu : skills révisés quittent les dérives) → **commit+push couche R2** (runner + report + evals révisés + replay report).
2. **R3** : sweep 9 arbitres (integrity, coherence, verify-cross, vcw, generer-pm, doublons, registry-sync, replay, harnais task16) ; harnais `task17-answer-key-check.py` réécrit (16 checks recalibrés à la réalité de re-exécution) ; correct-work PROJET (§1.5 — verdict sur l'ensemble) ; plans/rapports réécrits (présent plan + rapport Task 17 + rapport correct-work) ; worklog dépôt — **commit+push couche R3**.
3. **R4** : D003 `git rm` distillation globale (migration verbatim déjà prouvée) + maj références croisées (PM-INSTALL ×2, README écosystème, harnais task16 C02) ; D005 SYNC-CONTEXT ligne descriptive ; D006 harnais `task17-b-answer-key-check.py` (16 checks : verbatim migration, 0 homonyme R4, pointeurs valides, périmètre scellé intouché) + sweep — **commit+push couche R4**.
4. **R5** : journal dépôt + worklog racine (incident complet) — **commit+push couche R5** + audit anti-persistance canonique (token VALUE : arbre suivi / working tree / git config = 0/0/0 ; fragments courts = proses d'audit sanctionnées) + update-ref après chaque push.

## Answer key (critères de succès mécaniques)

- Voie L : 31/31 cas décidés, 0 QUOTA ; les REFUTE résiduels portent `revision_appliquee: True` ; les cas négatifs officiels ne sont révisés QUE si le vote calibré le confirme unanime.
- Replay : re-joué après révisions — md5 arbitre `d4563d6f` intact (0 fix instrument) ; les skills révisés quittent les dérives (attendu ~80+/93).
- R4 : 3 fichiers `historiques-par-skill/` + `historique-autres-elements.md` + README v1.1.0 + index SHA-256 intact ; distillation retirée ; 0 homonyme ; harnais task17-b 16/16 rc0.
- Arbitres finaux : integrity 60/60, coherence PASS AVEC RÉSERVES, verify-cross 100 %, vcw 16/16, generer-pm 3/3, doublons 0.
- origin/main : 5 couches poussées (R2→R5), 0 token VALUE persisté.

## R2 — Baselines (au moment de la mise à jour)

| Référence | Valeur |
|-----------|--------|
| origin/main | 2df7429 (R1 publiée) |
| Voie L | 20/31 (6 C / 9 R / 5 A) — 10 cas suspects à re-voter, 11 à mesurer |
| R4 disque | D001 ✓ D002 ✓ D004 ✓ — D003/D005/D006 à faire |
| Harnais task17 original | PERDU (à réécrire R3) |
| GO | actif (PAT fournie — commit/push chaque couche) |
