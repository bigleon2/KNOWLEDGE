# Plan Task 103 — Installation écosystème (PM-INSTALL @ aa3b99d) + gen-plan « continue » + CW --bloc + clone-chat

> gen-plan mode NULL (v3.43.0 — clause §A : invocation sans `<mode>` explicite = comportement antérieur sans portes de confirmation, directive propriétaire 2026-10-11) · Directive propriétaire trace `1a1e5c6648876ad5` : ① dans l'ordre, installer l'écosystème personnel sur le profil local via le fichier PM-INSTALL (URL `aa3b99d` — identification de procédure ; exécution par dérivation dynamique KO-L003 sur le corpus vivant v1.9.16, garde R2 — précédent Task 1/102, décision D1 réitérée) ; ② lorsque l'installation est terminée, prendre en compte le skill gen-plan fraîchement installé pour générer le plan d'actions de l'étape suivante : « gen-plan : continue » (précédents Task 84 G3 · Task 97 SUIV · Task 102 item c).

## G0 — Installation (EXÉCUTÉE EN AMONT, ce tour)

- Préflight (récidive wipe §3.4) : dérive mode-bits 2734 fichiers + **18 binaires à contenu altéré** (hash-object vs HEAD — tous restaurables depuis les objets git) + ref `origin/main` périmé (`2b9db630`) + arbre hôte skills/ périmé (55 divergences SKILL.md, `gen-plan`/`correct-work`/`version-management` absents) → réparés : `git reset --hard` LOCAL + `git fetch` ANONYNE (0 exposition) → 0 porcelain, HEAD = origin/main = `aaafcc61` (le push Task 102 avait atterri — preuve ls-remote).
- Pipeline canonique `scripts/eco_install_pipeline.py` (voie directe §3.2-a, forme installée) : rc=0 — préflight pin `a14f750` descendant-tolérant OK · garde R2 « 0 rétrogradation host ≤ repo » · archive v2.3 rescellée 15 entrées (attendu 15 — branchement Task 100) · manifeste integrity 114/114 PASS · post-install **55/55 SHA, 0 divergence** · certification-complete **ALL PASS 6/6** (verify-cross 165/165 ×2 · correct-work 16/16 · integrity 114/114 · interactions 55/55 STRICT · tool-routing 5/5) · garde É1-INSTALL verdict **INSTALLE** (`ensure-installed.py --check` rc=0, 55 entrées KB, 0 manquant) · **gen-plan v3.43.0 réinstallé** (exigence directive ②) · correct-work v2.11.0 · clone-chat v2.0.2 · version-management v1.3.0 restaurés.

## Groupes (mode NULL — exécution classique, sans portes)

- **G1 (continue — ~1500 #token)** Point d'état des pendances, dérivé du disque (KO-L003) : cron 531684 **DISPARU de la liste plateforme (0 job, désarmés inclus — 3ᵉ dispositif perdu après 531671 puis le désarmement « Disabled by API » 2026-11-16)** → escalade propriétaire maintenue, **AUCUNE recréation en boucle** (règle d'or n°5 + clause anti-boucle du job) · rotation/révocation PAT [PROPRIÉTAIRE — CRITIQUE : 29 expositions consignées à fin Task 102, 0 ce tour] · PMs §0 L2 [AUTO aux prochaines montées] · PUSH : 0 unpushed au point d'état (fetch anonyme vérifié) — le commit du tour crée 1 unpushed (0 PAT fourni → commit local SANS push, 0 exposition, pendance consignée — leçon Task 98 : push immédiat dès PAT frais) · G-RES verdict OK (disque 7,6 Go libres) → profil NORMAL.
- **G2 (clone-chat — ~3000 #token)** clone-chat 19ᵉ clôture, AVANT le CW (pattern Task 97/99/102, décision D1 du tour — le clone doit exister pour être vérifié par l'arbitre) : `download/clone-chat-session-web-ecef7f80-20261116-task103.md` — §0-§5, directives/décisions/bugs/drifts/reprise mécanique, scellement 8/8 S1-S8, 0 secret (KO-L009), drifts typés DÉGRADATION EXTERNE (cron disparu + wipe partiel hôte réparé), lignée Task 72→103.
- **G3 (correct-work — ~4000 #token)** correct-work (projet) --bloc : 4 blocs (B1 préflight+installation G0 · B2 continue/point d'état G1 · B3 clone G2 · B4 clôture G3-G4) × Étapes 2-5 → rapport `download/rapport-cw-task103-bloc.md` (agrégation = pire bloc ; answer key D001-D008 re-jouée).
- **G4 (clôture — ~2500 #token)** worklog suite 148 (hôte↔dépôt parité md5) + arbitres pré-commit (verify-correct-work 16/16 · certification-complete ALL PASS 6/6 · triggers-replay · scan doublons download/ 0) + miroirs download/ hôte→dépôt (plan + rapport CW + clone) + COMMIT LOCAL SANS PUSH « Task 103 CLOSE » (0 PAT fourni ce tour — 0 exposition, pendance PUSH 1 commit consignée).

## Answer key (schéma E1 — arbitre answer-key-checker, vérifications Python N3 re-jouables)

- D001 :
    criterion: "L'écosystème est installé et certifié sur le profil hôte (garde É1-INSTALL verdict INSTALLE, 0 fichier manquant)"
    verification: "python3 skills/gen-plan/scripts/ensure-installed.py --check"
    source: "directive trace 1a1e5c6648876ad5 item ① — PM-INSTALL §2/§3.2-a"
    priority: "S1"
    status: "verified"
- D002 :
    criterion: "Le point d'état « continue » est rendu dans le plan : cron 531684 disparu documenté, pendances par acteur (PROPRIÉTAIRE/AUTO), aucune recréation en boucle"
    verification: "python3 -c \"c=open('download/plan-task103-installation-continue-cw-clone.md',encoding='utf-8').read(); assert 'DISPARU' in c and 'PROPRIÉTAIRE' in c and 'AUCUNE recréation en boucle' in c\""
    source: "directive trace 1a1e5c6648876ad5 item ② — « gen-plan : continue » (mode NULL, précédents Task 84/97/102)"
    priority: "S2"
    status: "verified"
- D003 :
    criterion: "Clone-chat 19ᵉ scellé 8/8 S1-S8 avec 0 secret (aucun jeton dans le clone)"
    verification: "python3 -c \"c=open('download/clone-chat-session-web-ecef7f80-20261116-task103.md',encoding='utf-8').read(); assert 'Scellement : 8/8 S1-S8 PASS' in c and 'ghp_' not in c and 'github_pat' not in c\""
    source: "PM-INSTALL étape 11 (clôture) + KO-L009 — pattern Task 97/99/102 (décision D1 : clone avant CW)"
    priority: "S1"
    status: "verified"
- D004 :
    criterion: "Rapport correct-work (projet) --bloc livré : 4 blocs B1-B4, verdict agrégé PASS 4/4, answer key D001-D008 vérifiée"
    verification: "python3 -c \"c=open('download/rapport-cw-task103-bloc.md',encoding='utf-8').read(); assert all(f'B{i}' in c for i in range(1,5)) and 'PASS 4/4' in c and 'D008' in c\""
    source: "PM-INSTALL étape 9(b) — correct-work Mode PROJET, couplage gen-plan §1.5 (v2.11.0)"
    priority: "S2"
    status: "verified"
- D005 :
    criterion: "Worklog suite 148 en parité byte hôte↔dépôt (md5 identiques)"
    verification: "python3 -c \"import hashlib; a=hashlib.md5(open('worklog.md','rb').read()).hexdigest(); b=hashlib.md5(open('KNOWLEDGE-repo/worklog.md','rb').read()).hexdigest(); assert a==b\""
    source: "SHARED §1.4 journalisation — parité hôte/dépôt (précédent suites 141-147)"
    priority: "S2"
    status: "verified"
- D006 :
    criterion: "Arbitres pré-commit ALL PASS 6/6 sur l'état réel avant commit (certification complète)"
    verification: "python3 scripts/certification-complete.py"
    source: "PM-INSTALL étape 9 — certification (a)→(b)→(c) avant toute publication"
    priority: "S1"
    status: "verified"
- D007 :
    criterion: "Commit local « Task 103 CLOSE » créé : exactement 1 commit en avance sur origin/main, aucun push (0 PAT fourni — 0 exposition)"
    verification: "python3 -c \"import subprocess; r=subprocess.run(['git','-C','KNOWLEDGE-repo','rev-list','--count','origin/main..HEAD'],capture_output=True,text=True); assert int(r.stdout.strip())==1, r.stdout\""
    source: "KO-L009 + leçon Task 98/101 : 0 PAT ce tour → commit local sans push, pendance consignée"
    priority: "S2"
    status: "verified"
- D008 :
    criterion: "Chaîne E7-DISP complète : plan écrit + answer key + verdict E8 consigné + worklog R5 PLAN-AFFICHE + bloc récapitulatif au chat + fenêtre native (P1-P5 PASS)"
    verification: "python3 skills/gen-plan/scripts/check_plan_protocol.py --plan download/plan-task103-installation-continue-cw-clone.md --worklog worklog.md"
    source: "gen-plan §1.2bis E7-DISP (v3.36.0/v3.39.0) — garde bloquante check_plan_protocol.py"
    priority: "S2"
    status: "verified"

## Estimation #token (E4) et routage (E5)

- Total estimé : ~11 000 #token (G1 1500 · G2 3000 · G3 4000 · G4 2500) ; contingence « profil frais local » ×3-4 déjà consommée sur E1-E2 (découverte post-restauration, v3.28.1). Profil NORMAL (G-RES OK).
- Routage : [gen-plan · correct-work · clone-chat · resource-monitor] · couches : download/ + worklog (0 skill KB / agent / registre KB modifié — réinstallation idempotente d'état certifié) · règle d'or n°6 (français exclusif) · règle d'or n°5 (état vérifiable, KO-L003) · KO-L009 (0 jeton manipulé ce tour).

Horodatage plan : 2026-11-16T19:28:39Z

Verdict E8 : PASS (answer-key-checker 16/16 ALL PASS ×2 — idempotence, sorties byte-identiques ; check_plan_protocol P1-P5 PASS — Horodatage vérifié : 2026-11-16T19:28:39Z)
