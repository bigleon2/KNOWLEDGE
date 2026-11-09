# Rapport correct-work (projet) --bloc — Task 90

> **Mode PROJET** (option « bloc par bloc » §1.7, v2.9.0) · correct-work v2.11.0 · session web-ecef7f80 · 2026-11-09/10 · directive trace `1a1c1dde3f6d0021`
> Périmètre : installation PM-INSTALL (item 1 directive) + test $FACON « agent-engineering » écosystème en entrée (G1, corrections v1.1.1) + présent rapport (G2) — G3 (clone-chat + PUSH) suit immédiatement, consigné worklog
> Blocs : unités vérifiables explicites (étapes de la directive + groupes du plan) · Agrégation : pire-des-verdicts · garde anti-boucle 2 rounds (SHARED §4.4) — **0 round consommé**

## B1 — Installation écosystème (item 1 directive) : **PASS**

- Référence SHA `aa3b99d583429efb0b2ccb40690c84b389076693` élucidée : commit **Task 63** (ancien, ancêtre de HEAD — PM-INSTALL **v1.9.7** à l'époque) ; la dérivation dynamique « PM le plus récent » (KO-L003, §3.2) + garde anti-rétrogradation R2 imposent **PM-INSTALL v1.9.14** (HEAD) — écart consigné honnêtement (answer key D001, S2 aucune : doctrine explicite du PM-INSTALL).
- Voie directe §3.2-a (exécutant canonique `scripts/eco_install_pipeline.py`) : RC=0 · **55/55 SHA-256 certifiés** · divergences `[]` · **garde R2 : 0 rétrogradation (host ≤ repo partout)** · archive round-trip corpus 9/9 (véhicule v2.2) · purges `[]` — passes multiples dans le tour (installation initiale + re-runs $FACON2), toutes conformes.
- Hygiène mode-bits racinaire (`scripts/eco-hygiene-mode-bits.py`) : idempotent ×3 runs dans le tour (drift 2684 fichiers 100644→100755, 0 octet de contenu — racine connue cp hôte→dépôt, Task 85 G1) → dépôt propre à chaque frontière.
- **Certification §3/étape 9 du PM-INSTALL** : 9(a) verify-cross **100,0 % (0 W/0 E)** ✓ · 9(b) correct-work mode PROJET = **présent rapport** ✓ · 9(c) check-ecosysteme-integrity **114/114 PASS** ✓ — gén-plan fraîchement installé **v3.42.0** vérifié (frontmatter) pour l'item 2 directive (plan d'actions mode step).
- Étape 10 (publication) et étape 11 (clôture clone-chat) = G3, suivies immédiatement après ce rapport.

## B2 — Test $FACON « agent-engineering » (écosystème en entrée) — G1 : **PASS**

- **Audit (failles mesurées, règle d'or n°5 — zéro faille pré-écrite)** : F1 §5 stale (« baseline EN ATTENTE DE MESURE » vs MESURÉE Task 86 6/7 — KO-L003/R5) · F2 §6 traçabilité v1.1.0 absente · F3 evals.json version 1.0.0 stale · F4 doublon description (2 arbres SKILL.md, absente KB = dérive miroir R4) · F5 §2 version figée périmée.
- **Test fonctionnel** : re-mesure arbitre V6.1 `[DÉRIVE] agent-engineering 6/7` — conforme à l'attendu (écart structurel cas 6 voie M consigné Task 86, radical « agent » ∈ strong) · cycle 6 étapes §1.6 exécuté sur la mission réelle (Cadrer/Router/Outiller/Surveiller/Consolider/Se retirer — routage réel observé : test→n°56, validation→correct-work, archivage→clone-chat, planification→gen-plan).
- **Corrections v1.1.0 → v1.1.1 (PATCH)** : harnais `scripts/task90-corriger-agent-engineering.py` (réplique stemmer V6, **simulation M-safe PRÉALABLE** : ensembles de radicaux identiques + verdicts 7 cas identiques [True×5 · True cas 6 structurel · False cas 7] — abort sans écriture si écart ; ancres count==1 ×11, all-or-nothing, pré/post-asserts) — SHA SKILL.md 5c65a8a7… → 9316ec5c….
- **Cascade KO-L004** : KB v1.1.1 (en-tête + Description miroir **resynchronisée** — divergence KB↔SKILL résorbée + calibration) + pin ECO_SKILLS `check-ecosysteme-integrity.py` ligne 113 + lignage `historiques-par-skill/agent-engineering.md` v1.1.1 + miroirs hôte→dépôt ×5.
- **$FACON2 AVANT commit** : fonctionnel — V6.1 post-correction **6/7 IDENTIQUE** (M-safe tenue, 0 nouveau faux positif/négatif) · doublon **0/2 arbres** ; interactions — **55/55 PASS STRICT · 0 WARN · 0 FAIL** ; idempotence ×2 — harnais **NO-OP ×2** (SHA stable 9316ec5c…) + pipeline re-run 55/55 divergences [] + hygiène idempotent ; performance — harnais < 1 s, arbitres < 5 s.
- **Arbitres post-cascade** : integrity **114/114 PASS** (agent-engineering v1.1.1 attendu v1.1.1 · KB 1.1.1) · verify-cross **100,0 %** · doublons **0** (79 uniques, +1 = plan Task 90) — arbitres 5/5 au vert.

## B3 — Plan d'actions Task 90 + livrables : **PASS**

- Plan `download/plan-task90-test-agent-engineering-cw-bloc-clonechat.md` : mode step gen-plan v3.42.0, structure hiérarchique G/SG/T conforme §5.5, answer key **D001-D010** (criterion/verification exécutables), garde E8 `check_plan_protocol.py` **PASS 5/5** (P1 plan 11 251 caractères · P2 10 décisions/10 vérifications · P3 worklog R5 · P4 PLAN-AFFICHE même entrée · P5 verdict frais), horodatage 2026-11-09T20:05:00Z, #token ≈ 14 000, fenêtre native + bloc récapitulatif affichés, ouverture de groupe G1/G2 affichée (E7-DISP v3.36.0).
- **Answer key — vérification à date** : D001 ✓ (PM-INSTALL 1.9.14 + rapport 55/55) · D002 ✓ (v1.1.1 + integrity 114/114) · D003 ✓ (doublon 0/2 + V6.1 6/7 identique) · D004 ✓ (§5 « MESURÉE » + « 6/7 » ; §6 v1.1.0+v1.1.1) · D005 ✓ (evals.json 1.1.1) · D006 ✓ ($FACON2 consignée) · **D007 ✓ (présent rapport — 0 S1/S2)** · D008-D010 = G3 (clone + PUSH + pendances) — statuts dérivés du disque, G3 suit immédiatement.
- Harnais `scripts/task90-corriger-agent-engineering.py` : livrable G1 permanent (réutilisable, self-contained, réplique stemmer V6 documentée).

## B4 — État écosystème + pendances honnêtes R5 : **PASS**

- Dépôt git : HEAD `4a2981e` poussé (0 unpushed en début de tour) · **6 fichiers M = cibles exactes du tour** (skills/agent-engineering/SKILL.md, evals/evals.json, skills/KNOWLEDGE.md, scripts/check-ecosysteme-integrity.py, @historique lignage, worklog.md) — commit + PUSH en G3 (après clone-chat, $FACON2 déjà consommée AVANT commit conformément à l'instruction permanente).
- G-RES : OK (ressources niveau 0 — harnais et arbitres < 5 s chacun).
- **Pendances honnêtes R5** : écart structurel cas 6 voie M agent-engineering = **proposition future HORS cadence** (extinction requiert changement d'arbitre V6 — consigné Tasks 81/82/85/86/90) · **rotation PAT** [propriétaire — récidive structurelle, chaque PUSH expose le jeton] · G3 (clone-chat + commit + PUSH) en cours immédiat.
- E15 : PAT sera utilisé au PUSH G3 (instruction permanente — KO-L009 zéro-persistance stricte, **17ᵉ exposition à consigner**, rotation recommandée).

## Table « Blocs vérifiés » (format §2.4 étendu §1.7)

| Bloc | Contenu | Étapes couvertes | Findings | Verdict |
|---|---|---|---|---|
| B1 | Installation PM-INSTALL v1.9.14 + certification 9a/9c | Installation, réinstallation ×N, hygiène ×3 | 0 S1 · 0 S2 (écart SHA élucidé D001, doctrine) | **PASS** |
| B2 | Test $FACON agent-engineering + corrections v1.1.1 + cascade + $FACON2 | Audit, simulation M-safe, corrections, arbitres | 0 S1 · 0 S2 (5 failles corrigées, 0 régression) | **PASS** |
| B3 | Plan Task 90 E8 + answer key + harnais | E7-DISP, E8 P1-P5, vérifications D001-D007 | 0 S1 · 0 S2 (D008-D010 = G3, statuts disque) | **PASS** |
| B4 | État écosystème + pendances R5 | Arbitres 5/5, dépôt, G-RES | 0 S1 · 0 S2 (pendances consignées honnêtement) | **PASS** |

## Verdict agrégé : **PASS** (4/4 blocs · 0 S1 · 0 S2 · 0 round consommé)

Agrégation pire-des-verdicts : B1 PASS · B2 PASS · B3 PASS · B4 PASS → **CHAÎNE TASK 90 (G1+G2) : PASS**. Conformité worklog ↔ disque vérifiée (suites 113-114, marqueur PLAN-AFFICHÉ, statuts dérivés des verdicts réels). G3 (clone-chat + commit + PUSH PAT) suit immédiatement — consigné au worklog suite 115.
