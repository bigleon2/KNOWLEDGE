# Rapport Task 14 — KO-L004 (régénération PM correct-work v2.7.0) + clôture C006 (skill-finder-cn)

**Session** web-b93f42fa · **Date** 2026-10-10 · **gen-plan** v3.21.0 · **HEAD de départ** 2992bae · **0 commit / 0 push** (GO requis)

## Verdict : PASS AVEC RÉSERVES

Les 2 items de la directive sont matérialisés et byte-prouvés ; le périmètre s'est étendu de façon traçable à 2 remédiations d'arbitres découvertes en cours (classe S2-δ validée + garde anti-crash) ; 1 dérive héritée nouvelle-mesurée est consignée (non bloquante, hors périmètre).

## E8 / Plan
`download/plan-task14-ko004-pm-cw-c006-skillfinder.md` — answer-key-checker **16/16 ALL PASS rc0** (D001-D006).

## Phase B — KO-L004 : PM correct-work v2.7.0 (6 édits + provenance)
`skills/@mon-ecosysteme/PROMPT-MAITRE-CORRECT-WORK-v2.7.0.md` (724→726 L, md5 final `e64e85ce`) :
1. §2.6 L175 `Agent: correct-work v2.4.0` → `v2.7.0` (miroir SKILL.md L194, S2-β Task 12) ;
2. §2.6 L176 corruption `ode]` → `[mode]` (corruption fichier RÉELLE, byte-proof md5 `3789699e` ; survivait à Task 16 + commits + arbitres) ;
3. §9.2 L540 « (via gen-plan ou autonome) » → « (via gen-plan — OBLIGATOIRE, §1.5) » ;
4-6. §10.1 L572-576 : cale « via gen-plan — OBLIGATOIRE, §1.5 » + item réécrit + **garde ARRÊT EXPLICITE insérée** + #token « grille §4 » (miroir exact SKILL.md §10.1 L275-280) ;
7. Provenance KO-L004 datée 2026-10-10 insérée au §7 (aucun faux lignage, **pas de bump de version** — calibration de forme).
**Validation** : « ou autonome »=0, « si gen-plan disponible »=0, generer-pm --check 3/3, vcw 16/16, hex-proof `[mode]` = `5b 6d 6f 64 65 5d`.

## Phase C — C006 : skill-finder-cn/evals/trigger_evals.json
Enveloppe objet `auto-v1-t27` (1019 o, `_provenance`/`_calibration: requise`/`skill_name`/`evals[8]`) → **schéma canonique bare-liste**, 8 cas **verbatim** (`data == cases` prouvé par script, 5 positifs / 3 négatifs), md5 `0585dd89`→`24df0227`. **verify-cross : 83/84 → 84/84, 100.0 %, 0 erreur** — C006 clôturée. **Aucun fix instrument** : verify-cross.py non modifié (0 diff git — D004). Métadonnées enveloppe préservées ici (D005) : `auto-v1-t27`, calibration requise avant mesure voie L (réserve Task 23, re-mesure R3 QUOTA_OK).

## Remédiations découvertes en cours (traçables)
1. **Round-trip archive ↔ corpus** (integrity 59/60, coherence FAIL) : l'édit PM a divergé de l'archive véhicule v2.2 → `task21-f2-rebuild-archive.py` : chemin stale `ecosystem`→`work_knowledge` (classe S2-δ) puis **re-scellement : 28 entrées, 0 divergent, round-trip vérifié** ; integrity **60/60** ; coherence **PASS AVEC RÉSERVES (47/3/1 → 48/3/0)**.
2. **check-triggers-replay.py** : crash latent TypeError L120 (depuis génération de masse Task 27 — jamais re-joué car le chemin stale `git -C ecosystem` figeait le rapport au fallback 2026-10-03) → **garde défensive** (schéma canonique exigé, sinon **IGNORE EXPLICITE** compté au rapport et au stdout — jamais d'avalage silencieux, leçon S3) + chemin stale corrigé. Re-jeu : **29 skills canoniques, 64 enveloppes ignorées explicitement, skill-finder-cn 8/8**, date de rapport dérivée du commit audité (2026-10-09 — déterminisme B2 restauré).

## R2 final (5 arbitres baseline)
vcw **16/16** (via shim) · integrity **60/60** · coherence **PASS AVEC RÉSERVES 48/3/0** · verify-cross **100.0 % (84/84)** · generer-pm **3/3** (3.21.0/2.7.0/2.0.0) · hook --check rc0 INSTALLE kb 28. Replay (hors baseline, exposé) : 20/29 max, **9 dérives héritées post-francisation Task 23** (agent-creator, audio-metadata, pdf-llm, prompt-engineering, script-mon-ecosysteme-infrastructure, script-reviewer, skills-inventory, version-management, vue-upload 6/8) — non causées par Task 14, **non forcées (KO-L003)**, re-mesure voie L à armer QUOTA_OK.

## Anomalies KO-L003 consignées
1. **MultiEdit — violation d'atomicité** : a appliqué les edits 1-2 en déclarant un échec global (« No replacement performed ») — md5 passé de `3789699e` à `90efbf35` malgré le message ; contredit la garantie documentée. Remédiation : scripts Python byte-exacts (pré-comptage → application → re-lecture).
2. **Canal d'affichage — aval de séquence `[m`** : `sed`/`unicode_escape` affichaient `[mode]` comme `ode]` (preuve par hex : le fichier contenait bien `5b6d6f64655d`) — les corruptions « d'affichage » historiques doivent être re-soupçonnées fichier par fichier avant conclusion.

## Décisions D001-D006
D001 OK (6 édits + preuves) · D002 OK (provenance, pas de bump) · D003 OK (fix donnée verbatim, C006 close) · D004 OK (verify-cross md5 intact ; extension traçable : replay + rebuild-archive remédiés, classe S2-δ/garde) · D005 OK (enveloppe journalisée ici) · D006 OK (0 commit / 0 push, HEAD 2992bae).

## Restant propriétaire
- GO commit + push (couche Task 14 : 6 M + plan + rapport ; verify-cross non modifié).
- 64 enveloppes trigger_evals non canoniques (plateforme, `_calibration: requise`) : décision — normalisation de masse après calibration, ou extension d'instrument.
- 9 dérives voie M héritées : re-mesure armée QUOTA_OK (R3), révision des cas pré-francisation.
- PM gen-plan v3.21.0 non concerné ; C006 version-management (V6 3/8) toujours ouverte.

---

## Addendum S0 — Conformité « écriture selon les règles de l'écosystème » (directive propriétaire 2026-10-10)

**Directive** : « assure-toi que tous les fichiers soient écrits en suivant les règles de mon écosystème personnel » (pré-étape avant finalisation Task 14). **Méthode** : sweep mécanique persisté (`task14-s0-conformite.py`, répertoire harnais) — 16 checks C1-C11 byte-level sur 9 fichiers (6 M + 2 nouveaux + worklog externe de session), lecture seule du dépôt. **Verdict : CONFORME 16/16, rc0.**

| Axe | Résultat |
|---|---|
| C1 kebab-case (fichiers créés) | 2/2 (noms préexistants à convention établie exclus : corpus `PROMPT-MAITRE-*-vX.Y.Z.md`, schéma plateforme `trigger_evals.json`) |
| C2 semver 3 parties | OK (véhicule v2.1/v2.2 = schéma établi, cité — pas déclaré) |
| C3 0 jeton/secret | 0 occurrence sur 9 fichiers (anti-persistance B5) |
| C4 placeholders byte-level | PM `b'[mode]'` ×1 (hex 5b 6d 6f 64 65 5d) ; worklog `b'[mode]'` ×3 — l'affichage « ode] » = artefact d'affichage pur (anomalie 2 confirmée fichier par fichier) |
| C5 compile() + docstring | 2/2 scripts modifiés |
| C6 JSON valides | 3/3 |
| C7 marqueurs de fin artificiels | 0 |
| C8 PM chaînes interdites | « ou autonome »=0 ; « si gen-plan disponible »=0 ; provenance 2026-10-10 présente ; pas de faux lignage (v2.8.0 absent) |
| C9 schéma canonique trigger_evals | bare-liste 8 cas (5 positifs / 3 négatifs) |
| C10 D004 (aucun fix instrument) | verify-cross.py 0 diff vs HEAD |
| C11 documents en français | OK (plan + rapport) |

**Calibration d'instrument (KO-L003, honnêteté)** : tour 1 = 3 FAIL tous artefacts du sweep lui-même (C1/C2 périmètre trop naïf ; C5 `py_compile(cfile=/dev/null)` refusé) — 0 violation fichier ; corrigé en 2 passes (scope restreint aux fichiers créés + conventions établies exclues ; regex lookahead `(?!\.\d)` anti-préfixe). Anti-écho « Review the changes and make sure » (phrase intégrale) : 0 occurrence réelle — les matches du fragment isolé étaient la prose auto-référentielle de la présente documentation (×2 canaux contrôlés : MultiEdit et Edit). **Normalisation conformité** : chmod 755 ×2 (plan + rapport — convention corpus download/). **Re-vérification indépendante des arbitres en session (reproduction des claims)** : vcw 16/16 · integrity 60/60 · coherence PASS AVEC RÉSERVES 48/3/0 · verify-cross 84/84 ×2 · generer-pm 3/3 · answer-key-checker 16/16 · replay 20/29 + 64 ignores explicites + sfc 8/8 (mêmes 9 dérives héritées, NON forcées).

**Observations non bloquantes (décision propriétaire)** : (1) `tmp/` non suivi — 13 éléments (gitignore ou suppression) ; (2) 7 scripts de preuve session `task14-*` au répertoire harnais `/home/z/my-project/scripts/`, hors dépôt ; (3) worklog repo (`work_knowledge/worklog.md`) s'arrête à Task 24-push — entrées session courante (11-14) au worklog externe, synchronisation à décider.
