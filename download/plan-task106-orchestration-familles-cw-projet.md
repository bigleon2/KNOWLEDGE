# Plan Task 106 — Orchestrateurs par famille : analyse → verdict → carte des familles → correct-work (projet)

> gen-plan mode **step** (v3.43.0 — enchaînement autonome des groupes séquentiels, CW(groupe) après chaque groupe, CW(projet) en fin de chaîne) · Directive propriétaire trace `1a1efc61db496e75` (« continue + gen-plan (step) ») : « Peut-on regrouper par famille (ou groupe) certains de mes skills, agents, les scripts ou autres éléments de mon écosystème dans l'objectif de créer des agents qui orchestreraient chaque famille (ou groupe). Est-ce une bonne idée pour optimiser mon écosystème ? Si oui, génère $FACON et exécute un plan d'actions $FACON2 pour faire cela. » + item B « correct-work (projet). »

## G0 — État de départ (vérifié ce tour, session en cours)

Écosystème installé et certifié ce tour même (Task 105 G0 : pipeline rc=0, certification ALL PASS 6/6, É1-INSTALL INSTALLE — aucune réinstallation requise, le préflight Task 106 est l'état Task 105 : 0 porcelain dépôt, HEAD `fe85dba6`, pendance PUSH 2 commits consignée).

## G1 — Analyse et VERDICT (réponse à la question) — ~3000 #token

- **Lecture intégrale des sources (KO-L003)** : `orchestrateur-tsi` v1.1.2 (le pattern PROUVÉ : tandem 2 couches skill-méthode + agent exécution, pipeline P1-P6, micro-spécs, non-substitution, décision de forme directive 2026-11-01) · `agent-engineering` v1.1.1 (doctrine : règle 1 « simple d'abord », **gate anti-flotte** [Cognition 2025 / Anthropic 06/2025 — ratio ≈ 15×], n°56 = CADRE/ROUTE — ne remplace aucun détenteur, précédent « refus d'agentisation pipeline » Tasks 102-103) · registre KB (55 entrées) · graphe de dépendances.
- **Inventaire mécanique** `scripts/task106-inventaire-familles.py` (selftest 4/4) → `download/inventaire-familles-task106.json` : 7 familles mesurées — F1 TSI 6 membres/**13 arêtes intra** (la plus dense, orchestrateur sur disque) · F2 socle gouvernance 7/12 (gen-plan hub **24 dépendances inverses**) · F3 méta-artefacts 10/8 (routée par la table N2 de l'arbitre tool-routing) · F4 disciplines 15/10 (SHARED §7 méthode-mère + n°56) · F5 photo 4/**0 arête intra** (générations parallèles) · F6 diffusion 3/1 · F7 solo/composite 10/2.
- **VERDICT (tranché sur mesure, pas sur intuition)** : **OUI au regroupement par famille — c'est une bonne idée ET elle est déjà capturée là où elle paie** (TSI = orchestrateur dédié preuve vivante ; socle/méta/disciplines = orchestrés par la gouvernance existante gen-plan + correct-work + n°56 + table N2 + inter-scripts ; scripts = inter-scripts). **NON à la création de nouveaux agents orchestrateurs par famille** : les familles restantes sont à missions mono-membre (F5 photo : 0 arête intra — le routage est trivial) ou auto-portantes (F6/F7) — un orchestrateur par famille y violerait la règle 1 « simple d'abord » et la gate anti-flotte (coût ≈ 15× non justifié), dupliquerait la gouvernance (R4) et dégraderait le goulot réel mesuré (budget #token — étude Task 70 + campagne Task 105 : bootstrap mesuré à 6 tours agent, consolidé à 1 tour). La condition « si oui » est donc satisfaite sous sa forme utile : **formaliser ce qui existe** (la carte des familles fait défaut — personne ne peut voir d'un coup d'œil quelle famille est orchestrée par quoi), pas proliférer des agents. CW(groupe) G1 : D001-D002 vérifiés.

## G2 — Formalisation : la carte des familles — ~2500 #token

`download/carte-familles-ecosysteme.md` : les 7 familles avec membres réels, couplages MESURÉS (arêtes intra/inter), **statut d'orchestration par famille** (détenteur + artefact), **matrice de routage consolidée** (quelle demande → quel membre/quel détenteur), la réponse motivée à la question (doctrine + mesures citées), et la décision explicite de non-création d'agents avec ses gardes (règle 1, gate anti-flotte ≈ 15×, R4, goulot #token Task 70/105) + la voie de révision (quand un futur orchestrateur deviendrait justifié : les critères mesurables du précédent TSI). CW(groupe) G2 : D003-D004 vérifiés.

## G3 — correct-work (projet) — ~2500 #token

Item B de la directive + fin de chaîne mode step : rapport CW (projet) `download/rapport-cw-task106-projet.md` — Étapes 1-5 sur l'ensemble du tour (plan + inventaire + carte + décisions), answer key D001-D008 re-jouée, verdict agrégé. CW(groupe) G3 : D005 vérifié.

## G4 — Clôture — ~2500 #token

worklog suite 152 (hôte↔dépôt parité md5, marqueur PLAN-AFFICHE) + arbitres pré-commit (verify-correct-work 16/16 · certification-complete ALL PASS 6/6 · triggers-replay 0 dérive · doublons 0) + E8 (answer-key-checker 16/16 ×2 byte-identiques · check_plan_protocol P1-P5) + miroirs hôte→dépôt (plan + inventaire JSON + carte + rapport CW + script) + COMMIT LOCAL SANS PUSH « Task 106 CLOSE » (0 PAT fourni — 0 exposition, E15 inchangé 31, **pendance PUSH 3 commits** consignée). D006-D008 vérifiés.

## Answer key (schéma E1 — vérifications Python N3 re-jouables)

- D001 :
    criterion: "Inventaire mécanique des familles produit : scripts/task106-inventaire-familles.py (selftest 4/4, mesure seule, R4) + download/inventaire-familles-task106.json (7 familles, couplages arêtes intra/inter mesurés, agents .agent, orchestrateurs sur disque)"
    verification: "python3 scripts/task106-inventaire-familles.py --selftest && python3 scripts/task106-inventaire-familles.py && python3 -c \"import json; d=json.load(open('download/inventaire-familles-task106.json')); assert len(d['familles'])==7 and d['kb_entrees']>=50 and any(f['id']=='F1' and f['aretes_intra_famille']>=10 for f in d['familles'])\""
    source: "directive trace 1a1efc61db496e75 (question familles/orchestrateurs) ; règle d'or n°5 KO-L003 (verdict dérivé du disque)"
    priority: "S1"
    status: "verified"
- D002 :
    criterion: "Verdict rendu dans le plan : OUI qualifié au regroupement (déjà capturé : TSI orchestrateur dédié, socle/méta/disciplines orchestrés par la gouvernance) + NON motivé à la création de nouveaux agents orchestrateurs (règle 1 simple d'abord, gate anti-flotte ≈ 15×, R4, goulot #token mesuré Task 70/105)"
    verification: "python3 -c \"c=open('download/plan-task106-orchestration-familles-cw-projet.md',encoding='utf-8').read(); assert 'OUI au regroupement' in c and 'NON à la création' in c and 'gate anti-flotte' in c and 'règle 1' in c\""
    source: "directive (est-ce une bonne idée ?) ; agent-engineering §1.4 ; orchestrateur-tsi §1.1 décision de forme"
    priority: "S1"
    status: "verified"
- D003 :
    criterion: "Carte des familles livrée : download/carte-familles-ecosysteme.md — 7 familles avec membres réels, couplages mesurés (chiffres de l'inventaire JSON), statut d'orchestration par famille, matrice de routage consolidée"
    verification: "python3 -c \"c=open('download/carte-familles-ecosysteme.md',encoding='utf-8').read(); assert all(f'F{i}' in c for i in range(1,8)) and 'matrice de routage' in c.lower() and 'orchestration' in c and len(c)>3000\""
    source: "directive (regrouper par famille — la formalisation utile manquante) ; inventaire mécanique D001"
    priority: "S1"
    status: "verified"
- D004 :
    criterion: "Décision de non-création d'agents documentée avec gardes et voie de révision : la carte cite la gate anti-flotte (≈ 15×), la règle 1, le R4, le goulot #token mesuré (Task 70 + campagne Task 105), ET les critères mesurables qui justifieraient un futur orchestrateur (précédent TSI)"
    verification: "python3 -c \"c=open('download/carte-familles-ecosysteme.md',encoding='utf-8').read(); assert '15×' in c and 'R4' in c and 'Task 105' in c and 'critères' in c.lower()\""
    source: "agent-engineering §1.4 règles 1-2 ; refus d'agentisation pipeline Tasks 102-103 ; mesures Task 105 (goulot tours agent)"
    priority: "S2"
    status: "verified"
- D005 :
    criterion: "Rapport correct-work (projet) livré (item B + fin de chaîne mode step) : Étapes 1-5 couvrant l'ensemble du tour, answer key D001-D008 re-jouée, verdict agrégé PASS"
    verification: "python3 -c \"c=open('download/rapport-cw-task106-projet.md',encoding='utf-8').read(); assert 'Étape 5' in c and 'PASS' in c and 'D008' in c\""
    source: "directive item B (correct-work (projet)) ; PM-INSTALL étape 9(b)"
    priority: "S2"
    status: "verified"
- D006 :
    criterion: "Worklog suite 152 en parité byte hôte↔dépôt (md5 identiques)"
    verification: "python3 -c \"import hashlib; a=hashlib.md5(open('worklog.md','rb').read()).hexdigest(); b=hashlib.md5(open('KNOWLEDGE-repo/worklog.md','rb').read()).hexdigest(); assert a==b\""
    source: "SHARED §1.4 journalisation — parité hôte/dépôt"
    priority: "S2"
    status: "verified"
- D007 :
    criterion: "Arbitres pré-commit ALL PASS + commit local « Task 106 CLOSE » (exactement 3 commits en avance sur origin/main, aucun push — 0 PAT fourni, E15 inchangé 31)"
    verification: "python3 scripts/certification-complete.py && python3 -c \"import subprocess; r=subprocess.run(['git','-C','KNOWLEDGE-repo','rev-list','--count','origin/main..HEAD'],capture_output=True,text=True); assert int(r.stdout.strip())==3, r.stdout\""
    source: "PM-INSTALL étape 9 ; KO-L009 ; leçon Task 98/101 (pendance PUSH consignée)"
    priority: "S2"
    status: "verified"
- D008 :
    criterion: "Chaîne E7-DISP complète : plan écrit + answer key + verdict E8 aux horodatages couplés + worklog R5 PLAN-AFFICHE + bloc récapitulatif au chat + fenêtre native TodoWrite (check_plan_protocol P1-P5 PASS)"
    verification: "python3 skills/gen-plan/scripts/check_plan_protocol.py --plan download/plan-task106-orchestration-familles-cw-projet.md --worklog worklog.md"
    source: "gen-plan §1.2bis E7-DISP — garde bloquante"
    priority: "S2"
    status: "verified"

## Estimation #token (E4) et routage (E5)

- Total estimé : ~10 500 #token (G1 3000 déjà consommé · G2 2500 · G3 2500 · G4 2500). Profil NORMAL (0 signal pression — la session a déjà exécuté Task 105 complète sans pression).
- Routage : [gen-plan · correct-work · script-creator · correct-py · resource-monitor · agent-engineering (cadre n°56 mobilisé comme CADRE — la tâche est une décision ABE/MASE tranchée par ses règles)] · couches : scripts/ + download/ + worklog (0 skill KB / agent / registre KB modifié — AUCUN nouvel agent ni skill créé, décision D002) · règle d'or n°6 (français exclusif) · KO-L009 (0 jeton).

Horodatage plan : 2026-11-18T18:18:18Z (final — 8/8 décisions verified)

Verdict E8 : PASS (answer-key-checker 16/16 ALL PASS ×2 — idempotence, sorties byte-identiques ; check_plan_protocol P1-P5 PASS — Horodatage vérifié : 2026-11-18T18:18:18Z)
