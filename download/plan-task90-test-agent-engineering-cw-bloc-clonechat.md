# Plan d'actions — Task 90 : Test $FACON « agent-engineering » (écosystème en entrée — corriger failles + optimiser) + correct-work (projet) --bloc + clone-chat

> **Directive** : trace `1a1c1dde3f6d0021` (canal zai-web, session web-ecef7f80, chat 891cbdaf-5243-420e-9c3a-50feb93ef417) — « installe mon écosystème personnel via PROMPT-MAITRE-INSTALL-ECOSYSTEME.md [SHA aa3b99d…] ; puis prend en compte mon skill gen-plan fraîchement installé pour générer le plan d'actions des étapes suivantes : gen-plan (step) : { teste $FACON "agent-engineering" avec mon écosystème comme entrée (corriger failles + optimiser $FACON) ; correct-work (projet) --bloc ; clone-chat } »
> **Mode** : gen-plan **step** (structure hiérarchique + état d'avancement + affichages protocolaires E7-DISP/ouverture de groupe — SANS portes de confirmation)
> **Date** : 2026-11-09T20:00Z ≈ 2026-11-10 04:00 +08:00 (Europe/Paris : 2026-11-09 21:00) — **gen-plan v3.42.0** · SHARED v1.7.37 · PM-INSTALL v1.9.14
> **Installation préalable (item 1 directive — FAIT)** : SHA `aa3b99d…` localisé (commit Task 63 ancien, ancêtre de HEAD) → dérivation dynamique « PM le plus récent » (KO-L003) + garde anti-rétrogradation R2 ⇒ **PM-INSTALL v1.9.14** (vs v1.9.7 au SHA — écart consigné) ; voie directe §3.2-a : pipeline RC=0 **55/55 SHA-256, divergences [], R2 0 rétrogradation, round-trip v2.2**, hygiène mode-bits idempotent, dépôt propre ; certification 9(a) verify-cross **100,0 %** + 9(c) integrity **114/114** ; 9(b) correct-work PROJET = G2 ci-dessous ; gen-plan fraîchement installé **v3.42.0** vérifié.
> **Contexte disque (B-11, règle d'or n°5)** : HEAD `4a2981e` (Task 89, poussé, 0 unpushed, arbre propre) ; worklog dernière entrée suite 112 ; pendances cadence TOUTES ÉTEINTES (file re-curation 7/7 · socle n°56 fermé · baseline A2 n°56 mesurée Task 86 : **6/7**, 21/21 votes réels, écart structurel cas 6 voie M consigné hors cadence) ; écart SHA URL vs doctrine consigné D001.

## Items de la directive (ordre d'exécution)

1. **[FAIT]** Installer l'écosystème personnel sur le profil local via PM-INSTALL (voie directe — certifié ci-dessus).
2. Générer le plan d'actions des étapes suivantes via gen-plan fraîchement installé (mode **step** — présent plan).
3. Exécuter dans l'ordre : (a) test $FACON « agent-engineering » avec l'écosystème comme entrée — corriger failles + optimiser $FACON ; (b) correct-work (projet) --bloc ; (c) clone-chat.

## Groupes d'exécution

### G1 — Test $FACON « agent-engineering » (écosystème en entrée) : audit → mesure → corrections → cascade → $FACON2 (#token ≈ 8 500)

- **T1.1.1** E1-RES : B-11 worklog tail (suite 112) ✓ · G-RES OK ✓ · fraîcheur plan (aucun plan en vol — Task 84 clos) ✓ · É1-INSTALL : installation fraîche ce tour (PM-INSTALL v1.9.14 voie directe, 55/55 SHA, 9a/9c au vert) ✓ — consigné worklog. #token 300
- **T1.1.2** **Audit documentaire** (failles pré-identifiées à la lecture — à confirmer mécaniquement, règle d'or n°5 zéro faille pré-écrite) : **F1** SKILL.md §5 stale — « Baseline A2 : EN ATTENTE DE MESURE (v1.0.0) » alors que mesurée Task 86 (6/7, 21/21 votes réels) — viole KO-L003/R5 (statuts dérivés du disque) ; **F2** §6 Traçabilité — entrée v1.1.0 (Task 86, Description Optimization A10/A14) absente ; **F3** evals.json champ `version: 1.0.0` stale ; **F4** description frontmatter — doublon « la discipline agent engineering la discipline agent engineering » (coquille, présente 2 arbres SKILL.md, absente KB = dérive miroir R4) ; **F5** §2 formulation « Pas de script propre en v1.0.0 » à recaler. #token 600
- **T1.1.3** **Test fonctionnel — écosystème comme entrée** : (a) re-mesure voie mécanique arbitre V6.1 `check-triggers-replay.py` (attendu `[DÉRIVE] agent-engineering 6/7` — écart structurel cas 6 voie M connu et consigné) ; (b) **cycle 6 étapes §1.6 appliqué à la présente mission** : Cadrer (mission = 3 tâches directives ; classification ABE/AE/MASE ; ex. test du skill = AE/évaluation), Router (test→n°56 lui-même, validation→correct-work, archivage→clone-chat, planification→gen-plan — routage réel observé), Outiller (arbitres V6.1, integrity, interactions armés AVANT), Surveiller (verdicts mécaniques G1-G3), Consolider (statuts dérivés du disque), Se retirer (0 état résiduel §1.5). #token 900
- **T1.2.1** **Simulation M-safe préalable** (pattern Task 86) : suppression du doublon F4 = aucun radical stemmer ajouté/retiré (mêmes mots) → voie M inchangée par construction — preuve consignée AVANT édition. #token 400
- **T1.2.2** **Corrections chirurgicales** (harnais `scripts/task90-corriger-agent-engineering.py` — stdlib, ancres count==1, all-or-nothing, idempotence ×2) : F1 §5 → « baseline A2 MESURÉE (voie M + confirm 3 runs LLM, 21/21 votes réels) : 6/7 post-optimisation v1.1.0 — écart structurel cas 6 voie M consigné (radical agent ∈ strong arbitre V6) » ; F2 §6 += entrées v1.1.0 (Task 86) + v1.1.1 (ce task) ; F3 evals.json version → 1.1.1 ; F4 description doublon supprimé (sémantique intacte) ; F5 §2 recalé versionné ; frontmatter **1.1.0 → 1.1.1 (PATCH — corrections de contenu sans changement de comportement, routage M-safe prouvé T1.2.1)**. #token 1 200
- **T1.2.3** **Cascade KO-L004** (pattern Task 86 `task86-cascade-reseal-v110.py`) : KB agent-engineering v1.1.1 (en-tête + Description miroir corrigée F4 + Dernière calibration) + pin ECO_SKILLS `check-ecosysteme-integrity.py` 1.1.0 → 1.1.1 (garde en action : FAIL attendu puis PASS) + `historiques-par-skill/agent-engineering.md` ligne v1.1.1 + miroir hôte→dépôt ciblé. #token 800
- **T1.3.1** **$FACON2 éléments modifiés (AVANT commit — ordre chronologique)** : fonctionnel — arbitre V6.1 re-mesure post-correction (attendu 6/7 IDENTIQUE, 0 nouveau faux positif/négatif — preuve T1.2.1 tenue) + cohérence frontmatter/KB/evals ×2 arbres ; interactions — `test-coherence-interactions.py` 55/55 PASS STRICT ; idempotence ×2 — harnais NO-OP ×2 + re-mesure stable ×2 ; performance — durées mesurées. #token 1 000
- **T1.3.2** **Arbitres écosystème post-cascade** : integrity **114/114** (après recalibrage pin) · verify-cross **100,0 %** · doublons 0 · pipeline re-run (55/55, R2, divergences []) idempotent. #token 800
- **T1.4.1** correct-work(groupe G1) : PASS requis (0 S1/S2). #token 800

### G2 — correct-work (projet) --bloc = certification installation étape 9(b) (#token ≈ 3 000)

- **T2.1.1** SKILL.md correct-work v2.11.0 relu (mode PROJET, option --bloc) → **exécution sur l'écosystème (profil + dépôt)** — verdict consigné ; tout S1/S2 résorbé (max 2 rounds, garde anti-boucle) ; rapport download/. Double rôle : exigence directive + **étape 9(b) de la certification PM-INSTALL**. #token 2 500
- **T2.1.2** correct-work(groupe G2) : PASS requis. #token 500

### G3 — clone-chat = clôture installation étape 11 + consignation + PUSH (#token ≈ 2 500)

- **T3.1.1** Skill clone-chat exécuté (§0-§5, 8 checks S1-S8) → archive MD auto-suffisante `download/clone-chat-session-web-ecef7f80-20261110-task90.md` — **étape 11 PM-INSTALL** (clôture installation), scellée, idempotente. #token 1 500
- **T3.2.1** Worklog suite 113 (Directive + G1-G3 + E15 **17ᵉ exposition**) + miroir hôte→dépôt + commit Task 90 + **PUSH PAT** (KO-L009 zéro-persistance stricte — jeton inline uniquement, 0 git config, 0 fichier) + fetch réconciliation + E8 FINAL re-validé (horodatage couplé) + tableau final. #token 1 000

## Answer key

- **D001** — Écart SHA URL vs doctrine. criterion : SHA `aa3b99d…` = commit Task 63 (PM-INSTALL v1.9.7, ancêtre de HEAD) ; la dérivation dynamique « PM le plus récent » (KO-L003) + garde R2 imposent v1.9.14 — écart consigné honnêtement, installation à l'état certifié courant. verification : `grep -m1 "Version" PROMPT-MAITRE-INSTALL-ECOSYSTEME.md` == 1.9.14 + rapport réinstallation 55/55. **Source** : directive item 1 + PM-INSTALL §3.2. **Priorité S2** · statut : verified.
- **D002** — Bump PATCH v1.1.0 → v1.1.1. criterion : corrections F1-F5 = contenu/consistance SANS changement de comportement (routage M-safe prouvé par simulation préalable) ⇒ PATCH sémantique strict. verification : frontmatter `version: 1.1.1` + pin ECO_SKILLS recalibré → `check-ecosysteme-integrity.py` **114/114 PASS**. **Source** : Règle Zéro n°2 + semver. **Priorité S1** · statut : verified.
- **D003** — Correction F4 description (doublon). criterion : doublon « la discipline agent engineering la discipline » supprimé, sémantique intacte, miroir KB resynchronisé (R4). verification : `grep -c "la discipline agent engineering la discipline"` == **0** sur hôte + dépôt + arbitre V6.1 re-mesure **6/7 identique**. **Source** : audit T1.1.2. **Priorité S1** · statut : verified.
- **D004** — F1 §5 + F2 §6 staleness. criterion : statuts dérivés de l'état vérifiable du disque (KO-L003/R5) — §5 documente la baseline MESURÉE (6/7) ; §6 documente v1.1.0 (Task 86) ET v1.1.1 (Task 90). verification : §5 contient « MESURÉE » + « 6/7 » ; §6 contient « v1.1.0 » + « v1.1.1 ». **Source** : audit T1.1.2. **Priorité S1** · statut : verified.
- **D005** — F3 evals.json version. criterion : champ version aligné sur la version courante du skill. verification : `python3 -c "import json; print(json.load(open('skills/agent-engineering/evals/evals.json'))['version'])"` == 1.1.1. **Source** : audit T1.1.2. **Priorité S2** · statut : verified.
- **D006** — $FACON2 AVANT commit (ordre chronologique). criterion : fonctionnel + performance + interactions + idempotence ×2 sur TOUS les éléments modifiés (SKILL.md, evals.json, KB, pin, lignage, harnais). verification : verdicts consignés worklog G1/G3 + harnais NO-OP ×2 + arbitres 5/5. **Source** : instruction permanente discussion. **Priorité S1** · statut : verified.
- **D007** — correct-work (projet) --bloc PASS. criterion : mode PROJET option --bloc exécuté profil+dépôt, verdict consigné, 0 S1/S2 résiduel. verification : rapport download/ + entrée worklog G2. **Source** : directive item 3b + PM-INSTALL étape 9(b). **Priorité S1** · statut : verified.
- **D008** — clone-chat scellé (étape 11). criterion : §0-§5 + 8 checks S1-S8 PASS, 0 secret, idempotent. verification : `download/clone-chat-session-web-ecef7f80-20261110-task90.md` présent + checks consignés. **Source** : directive item 3c + PM-INSTALL étape 11. **Priorité S2** · statut : verified.
- **D009** — PUSH PAT KO-L009 + E15. criterion : jeton inline en mémoire de commande uniquement (0 git config, 0 fichier), fast-forward pur, distant == HEAD, **E15 17ᵉ exposition consignée + rotation recommandée**. verification : `git remote get-url origin` sans jeton + `git log @{u}..HEAD` vide + worklog E15. **Source** : instruction permanente. **Priorité S1** · statut : verified.
- **D010** — Pendances honnêtes R5. criterion : écart structurel cas 6 voie M demeure hors cadence (proposition future — changement d'arbitre requis) ; rotation PAT [propriétaire] ; aucun faux TERMINÉ. verification : §4 clone-chat + bilan worklog. **Source** : R5. **Priorité S2** · statut : verified.

#token estimé total : ≈ 14 000 (G1 8 500 · G2 3 000 · G3 2 500)

## Hooks de validation (E8)

Horodatage plan : 2026-11-09T20:45:00Z

Verdict E8 : PASS — FINAL (answer key 10/10 décisions criterion/verification VERIFIED [D001-D007 mécaniques · D008 clone 8/8 · D009 PUSH KO-L009/E15 17ᵉ · D010 pendances R5] · G1 9/9 [5 failles corrigées v1.1.1, M-safe prouvée] · G2 CW --bloc 4/4 PASS 0 S1/S2 · G3 clone scellé 8/8 + PUSH · 13/13 tâches TERMINÉES — Horodatage vérifié : 2026-11-09T20:45:00Z)
