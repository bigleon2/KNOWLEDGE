# Rapport final — Task 72 : Chantier R1 re-curation + adéquation + liste priorisée + skill re-curation

**Date : 2026-11-08** · Session : web-ecef7f80 · Plan : download/plan-task72-recuration-genplan-adequation-liste-skill-recuration.md (rév. 3 — **15/15 décisions verified, E8 final PASS 23:59:00Z**) · Directives : 7 items trace 1a1b79af6dcff4c5 + complémentaires 1a1b7b297b7b4975 et 1a1b7fe1c7238e8d.

## Bilan par groupe

| Groupe | Livrable | Verdict |
|---|---|---|
| **G1** Chantier R1 | gen-plan **v3.39.0** : 9 blocs R4 → references/, résumés inline, **104,0 → 29,9 Kio (−71,2 % #token, CRITIQUE → INTERMÉDIAIRE rang 10, 0 CRITIQUE écosystème)** ; fenêtre native AFFICHE-PLAN (E7-DISP point 6) ; cascade KO-L004 complète (PM 211 Ko, archive R4+sceau, pin/KB/histo/README v2.1.19, ULTRA ×2, propagation, sweep 9, arbitres, re-scellement ×2, sync 0 divergence) | **PASS** — D001-D006, D015 (commit 5646e96) |
| **G2** Adéquation | download/rapport-adequation-genplan-task72.md — 4 arbitres 0 FAIL, 4 selftests, evals 9+15 byte-identiques, couverture PM complète | **PASS AVEC RÉSERVES** (WARN B1 légitime) — D007 |
| **G3** Liste priorisée | download/liste-recuration-priorisee-task72.md — 7 écosystème classés + 2 plateforme (décision propriétaire), cartographie sèche n°1 | **PASS** — D008 |
| **G4** Skill re-curation | skills/re-curation v1.0.0 — IMPLÉMENTÉ de protocole-test.py (PRE GO/NO-GO, POST maintien, --compare R4) + 2 outils + evals + cascade légère | **PASS** — D009 (commit d3ee6e6) |
| **G5** Tests $FACON | download/rapport-tests-recuration-task72.md — selftests 12/12, PRE vm GO (baseline cible n°1), PRE/POST gen-plan MAINTENU, VÉRIFICATION C1-C4 ×2, --compare réel, idempotence ×2 | **PASS** — D010 |
| **G6** correct-work --bloc | Verdicts par groupe G1-G5 PASS (0 S1 · 0 S2 ; S3-class résorbés documentés), answer-key-checker 16/16, E8 final | **PASS** — D011, D014 |
| **G7** clone-chat | download/clone-chat-session-web-ecef7f80-20261108-task72.md (§0-§5, reprise mécanique, 5 leçons) | **PASS** — D012 |

## Résultats saillants

1. **Le goulot #token est résorbé à sa source n°1** : gen-plan (le plus lourd skill, 26 616 #token au chargement par défaut) passe à 7 667 #token (−71,2 %) — l'écosystème n'a plus AUCUN skill CRITIQUE (70 skills : 28 OK · 33 intermédiaires · 9 LOURD · 0 CRITIQUE).
2. **AFFICHE-PLAN est maintenant natif** : la fenêtre des étapes du plan s'affiche via le mécanisme natif Z.ai (liste de tâches TodoWrite/TodoRead) au début de l'exécution et à chaque fin d'étape — canal supplémentaire aux canaux existants (bloc chat, marqueur worklog, garde P1-P5), preuve vivante tenue tout au long de la présente exécution.
3. **Le protocole « tests avant re-curation » est outillé** : le skill re-curation (implémenté de protocole-test.py) génère un protocole adapté à chaque cible, capture la baseline golden master (GO/NO-GO), vérifie le maintien de l'optimisation en POST et arbitre les méthodes (R4-compliantes seules). La baseline de la prochaine cible (version-management) est déjà capturée : GO.
4. **Constats S3-class résorbés en cours de route (transparents)** : recalibrage KO-L003 de la plage PM (1 770 L in extenso) ; harnais v2 baseline (étiquette SHARED normalisée) ; harnais mesure (+1/section au lieu de +[j−i] — preuve couverture exhaustive) ; §0 canonique du nouveau skill ; lags d'en-têtes (v3.37.1, v3.35.2) résorbés.

## État git et pendance

- **Commits dépôt (KNOWLEDGE-repo, non poussés)** : Task 70 (cea7d12, 886604d) · Task 71 (1f80594, 8acc8c1, 2daaa9b, 011d342) · **Task 72 (5646e96 G1, d3ee6e6 G4+G5, + commit de clôture)**.
- **Pendance unique — D013/KO-L009** : le PUSH est réservé au PROPRIÉTAIRE. Le PAT collé au chat le 2026-11-08 (déjà circulé le 2026-10-26) doit être **RÉVOQUÉ avant toute manipulation** : GitHub → Settings → Developer settings → Personal access tokens → révoquer. Puis, depuis un environnement authentifié : `git push origin main` (fast-forward attendu). L'agent n'a jamais utilisé ni stocké ce jeton.
