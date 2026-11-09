# Rapport Task 15 — traitement des décisions restantes (S3 dormants, 64 enveloppes, tmp/, rétro-sync)

## Métadonnées
- **Date** : 2026-10-10 (session web-b93f42fa)
- **Directive propriétaire** : « traite les décisions restantes : 11 harnais dormants (S3), 64 enveloppes, disposance, rétro-sync repo. "tmp/" »
- **Plan** : `download/plan-task15-decisions-restantes.md` (gen-plan v3.21.0, hook É1-INSTALL rc0 INSTALLE — head b36f177, kb 28)
- **Answer key** : D001-D006 — `scripts/task15-answer-key-check.py` (16 checks mécaniques)
- **Règle d'or n°2** : 0 commit, 0 push pendant l'exécution — HEAD b36f177 constant (check D006)

## D002 — re-scellement archive 28→27 (préalable)
- Cause : suppression propriétaire `d72226a` (clone-discussion-2026-09-27-…-b13-r7-f.md, UI web, couche 14-push) → round-trip rompu (integrity 58/60, coherence FAIL, zip=28 vs corpus=27).
- `scripts/task21-f2-rebuild-archive.py` évolué : `RETRAITS_SANCTIONNES` (retrait tracé avec provenance commit + décision) — la protection anti-perte reste intégrale pour tout autre extra (test : tout extra non sanctionné échoue toujours).
- `scripts/check-ecosysteme-integrity.py` : `CORPUS_ATTENDU` 28→27 (recalibrage commenté, pattern « recalibré L004 Task 56 ») ; libellé N27.
- Re-scellement exécuté : nouvelle archive **27 entrées**, divergents —, extras —, round-trip vérifié. Manifeste `ecosysteme-integrity.json` **régénéré par l'arbitre** (archive=27, corpus=27, pin download mis à jour automatiquement).
- Résultat : **integrity 60/60 rc0 · coherence PASS AVEC RÉSERVES (48/3/0)** — baseline restaurée.

## D001 — normalisation des 64 enveloppes (schéma canonique)
- État pré-exécution (git HEAD) : 64 `skills/*/evals/trigger_evals.json` hors schéma — enveloppe homogène `{_calibration, _provenance, evals, skill_name}`, 512 cas (8/skill), 0 anomalie de forme.
- Transformation (`scripts/task15-normalize-evals.py`, harnais session) : bare-liste canonique, **512 cas verbatim** (0 réécriture, 0 réordonnancement), format `json.dumps(indent=2, ensure_ascii=False) + '\n'` (miroir du précédent C006 skill-finder-cn).
- **Métadonnées préservées hors données** (provenance historique) : `_provenance: "auto-v1-t27"` (génération mécanique Task 27) ; `_calibration: "requise avant mesure voie L (prompts dérivés mécaniquement du frontmatter — pas de baseline R3)"` — ces 2 caveats valaient pour les 64 enveloppes ; leur suppression des données est couverte par le présent rapport (precedent D005 Task 14 : enveloppe « absente », information vivante au journal).
- Re-jeu du replay (`check-triggers-replay.py`, md5 intact — 0 fix instrument) : **n_skills=93 (29+64), ignores=0, skills_ok=78, dérives=15, verdict FAIL (informatif)**.
- Dérives 15 : agent-browser, agent-creator, ai-news-collectors, audio-metadata, gaokao-recommend-schools, jd-resume-tailor, pdf-llm, prompt-engineering, qingyan-research, script-mon-ecosysteme-infrastructure, script-reviewer, skills-inventory, ui-ux-pro-max, version-management, vue-upload — les 9 héritées + 6 dérives latentes désormais **visibles** (observabilité accrue, non dégradation ; remédiation = re-mesure voie L, restant propriétaire).

## D003 — archivage des 11 dormants (finding S3)
- Périmètre = critère calibré 14-CW reproduit à HEAD (chaîne `my-project/ecosystem` présente, hors 9 instruments VIVANTS ; `stale_live`=AUCUN) : task17 ×3, task18 ×1, task21 ×5 (f3-status-mesure, p2b-pass2, p2b-kb-decision, p2b-kb-sync, p4b-pass2), task23 ×2.
- `git mv` ×11 → `scripts/_archive/` (précédent task40-cw-projet.py ; `_archive/` = 16 entrées après opération) — zéro correctif de masse, zéro churn sur scripts one-shots historiques.
- `task21-f2-rebuild-archive.py` NON archivé (instrument VIVANT — liste LIVE 14-CW, mobilisé par D002).
- Les 5 instruments stables md5 inchangés (test-coherence-interactions, generer-pm-skill, verify-correct-work, verify-registry-sync, answer-key-checker).

## D004 — disposition tmp/ (13 artefacts, sources de régénération)
Supprimé (`rm -rf tmp/`, non suivi git) — inventaire exhaustif et reproducible :
- `t12-vcw-canon.txt`, `t12-vcw-canon2.txt`, `t12-vcw-canon-seed.txt`, `t12-vcw-shim.txt`, `t12-vcw-shim-seed.txt` — captures arbitre vcw Task 12 ; régénération : re-run `verify-correct-work.py` (+ variante PYTHONHASHSEED).
- `t12-integrity.txt`, `t12-coherence.txt`, `t12-vcross.txt`, `t12-genpm.txt`, `t12-genpm-check.txt`, `t12-hook-root.txt` — captures arbitres Task 12 ; régénération : re-run des instruments respectifs.
- `r5-token-dashboard.json` — sortie `scripts/r5-token-dashboard.py` (déjà présent au dépôt).
- `vrs-full.json` — sortie `scripts/scan-versions-reelles.py` (homologue tracké `versions-reelles-report.json`).
- Références vérifiées avant suppression : 0 référence vivante au contenu de `tmp/` (les occurrences « tmp/ » du dépôt = `/tmp` système + docstring `phase2-nettoyage.py` + véhicule historique b13-r5).

## D005 — rétro-sync worklog du dépôt
- Port **verbatim** de 19 entrées de campagne (Tasks 0, 1, 2, 3, 4 ×2, 5, 6, 7, P3, 8, 11, 12, 13, 13-commit, 13-push, 14, 14-S0, 14-CW — 55 046 o) depuis le worklog de session, préambule de désambiguïsation inclus (`scripts/task15-retrosync.py`).
- Task IDs du dépôt : 24 → 44 (+20 = 19 + 1 préambule) ; byte-fidélité du bloc porté vérifiée ; homonymes ancienne campagne (web-8a7e5653) intacts ; Task 14-push non re-porté (déjà présent).

## D006 — règle d'or n°2 + recalibration harnais session
- HEAD b36f177 constant pendant toute l'exécution (0 commit, 0 push).
- Harnais `task14-cw-etape2-proof.py` (session) dynamisé : attente HEAD b36f177 (couche publiée), exclusion du report daté du check d'arbre (collatéral documenté), replay 93/0, archive 27. Re-run : **24/24 PASS**.

## Sweep R2 (5 arbitres, état final)
vcw 16/16 ALL PASS (shim) · integrity **60/60** rc0 · coherence **PASS AVEC RÉSERVES** 48/3/0 · verify-cross **100,0 %** · generer-pm **3/3** COHERENT · replay 93 skills / 0 ignore (dérives 15 documentées) · hook rc0 INSTALLE kb 28.

## Calibration d'instruments (pattern KO-L003 — 6 artefacts corrigés sans ajustement de réalité)
Checker Task 15, tour 1 : 10/16 → 6 FAIL tous artefacts d'instrument, corrigés : (1-2) `IGNORES_AVANT` lu dans le report régénéré (= vide) → liste pré-exécution codée depuis git HEAD ; (3) libellé verdict coherence (« COHÉRENCE DES INTERACTIONS : PASS ») ; (4) auto-référence du checker au scan stale (exclue) ; (5) ordre rapport/checker (rapport écrit avant re-run) ; (6) marqueur préambule (« du worklog du dépôt »). Écho d'affichage « Review the changes… » ré-apparu (3e occurrence) : 0 occurrence réelle aux fichiers (grep -c ×4) — anomalie 2 re-confirmée.

## Résumé
- **Problèmes trouvés** : 2 recalibrations réelles (integrity/coherence — suppression d72226a), 1 collision de collatéral daté (harnais), 6 artefacts d'instrument (checker) ; 0 défaut de fond sur les 4 décisions.
- **Corrections appliquées** : D001 (64 fichiers, 512 cas verbatim) · D002 (F2 évolué + CORPUS_ATTENDU 27 + re-scellement) · D003 (git mv ×11) · D004 (rm tmp/) · D005 (port verbatim +20) · D006 (harnais ×4 attentes).
- **Collatéral documenté** : `generer-pm-report.json` (champ date 2026-10-10, régénéré par --check — artefact de génération automatique, sanctionné).
- **Restant propriétaire** : (1) GO commit + push de la couche Task 15 (règle d'or n°2) ; (2) re-mesure voie L des 15 dérives replay (QUOTA_OK — caveats _calibration documentés ci-dessus) ; (3) révocation/régénération du PAT (exposé au canal, consigné 14-push).
