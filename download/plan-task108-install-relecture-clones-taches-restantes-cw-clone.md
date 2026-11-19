# Plan Task 108 — Relecture intégrale « bloc par bloc » via les clones + tâches restantes $FACON + CW --bloc + clone-chat

**Directive propriétaire** trace `1a1f2096f9b3406d` : « installe mon écosystème personnel en tant que mon écosystème personnel sur mon profil local grâce à mon fichier "github.com/bigleon2/KNOWLEDGE/blob/19eb34b1…/skills/@mon-ecosysteme/PROMPT-MAITRE-INSTALL-ECOSYSTEME.md" et lorsque l'installation sera terminée, exécute mon skill "gen-plan" fraîchement installé pour générer le plan d'actions des tâches suivantes : (a) relis l'intégralité de cette discussion en mode "bloc par bloc" via ses clones créés ; (b) dis-moi $FACON les tâches restantes à faire. » — $FACON = « de façon cohérente, optimisée et fonctionnelle » (registre @Alias, entrée D-105).
Horodatage plan : 2026-11-19T04:35:00Z · gen-plan v3.43.0 mode step (clause §A, précédents Task 102/107) · profil NORMAL.

## G0 — Installation de l'écosystème (EXÉCUTÉE EN AMONT, ce tour)

- Fichier source vérifié : PM-INSTALL du dépôt local = commit `19eb34b1` (= HEAD = origin/main = le commit de l'URL directive — push Task 107 vérifié `git rev-list --count origin/main..HEAD` = 0).
- Entrée canonique `scripts/bootstrap-ecosysteme.py` (PM-INSTALL v1.10.0 §3.2-c) : **VERDICT INSTALLE-REPARÉ rc=0** — preflight RÉPARÉ (dérive 2764 fichiers, 6ᵉ récidive recyclage sandbox — reset --hard LOCAL) · dry-run DIVERGENCE-HÔTE 55 · installation OK 55 SHA 0 divergence · certification **ALL-PASS-6/6** · garde É1 **INSTALLE** · 1 commande, 1 tour, 2,08 s. gen-plan v3.43.0 + correct-work + clone-chat installés sur le profil local.

## G1 — (item a) Relecture intégrale en mode « bloc par bloc » via les clones

1. **Inventaire mécanique** : `scripts/task108-relecture-clones.py` (NOUVEAU, stdlib — adaptation du précédent Task 102, règle d'or n°5 : fenêtre étendue aux 20 clones + 153 suites, lecture des §1-§3 des clones) → `download/task108-extraction-blocs.json` : découpage du worklog par suite, agrégation en blocs chronologiques (phases), inventaire exhaustif des 20 clones (dates, tasks, scellages S1-S8), stats verdicts/E15/pendances.
2. **Lecture bloc par bloc** : chaque bloc chronologique relu via le clone correspondant (§1 worklog + §2 artefacts + §3 décisions/bugs + §3.5 drifts) — intégralité de la lignée Task 70 → 108.
3. **Note de relecture** : `download/note-relecture-blocs-task108.md` — un bloc par phase (points clés, incidents, leçons, pendances portées), table des 20 clones, synthèse des drifts majeurs, fil des versions clés (gen-plan, correct-work, PM-INSTALL, SHARED).

## G2 — (item b) Tâches restantes à faire $FACON

1. **Extraction des pendances** : scan mécanique du worklog (suites 149-153 + point d'état continue Task 107) + rapports CW Task 105-107 (findings) + feuille de route §8 du rapport Task 105 → liste brute.
2. **Livrable** : `download/taches-restantes-task108.md` — liste priorisée par acteur ([PROPRIÉTAIRE] / [AUTO] / [AUTOMATIQUE]) avec pour chaque tâche : nature, source (suite/rapport), critère d'extinction vérifiable, priorité P1-P3. $FACON : chaque tâche formulée de façon cohérente (ancrée dans sa source), optimisée (regroupements, pas de doublon), fonctionnelle (critère d'extinction mécanique).
3. **Réponse au propriétaire** : la liste est affichée au chat en fin de G2 (le livrable intégral fait foi, le chat donne la vue priorisée).

## G3 — correct-work (projet) --bloc

Rapport `download/rapport-cw-task108-bloc.md` — 4 blocs (B1 installation G0 · B2 relecture G1 · B3 tâches restantes G2 · B4 clôture G4-G5) × Étapes 2-5 (erreurs/omissions avec délégation alias-eco — registre phrases récurrentes · structure/conventions · interactions [verify-cross · tool-routing · interactions] · cohérence) → verdict agrégé = pire bloc, findings S1-S4.

## G4 — clone-chat (21ᵉ clôture)

`download/clone-chat-session-web-ecef7f80-20261119-task108.md` — 7+1 étapes, §0-§5 (§1-§3 enrichis par le tour, §0/§4-§5 régénérés), scellage 8 checks S1-S8, 0 secret (KO-L009), lignée Task 72 → 108.

## G5 — Clôture

Worklog suite 154 (parité md5 hôte↔dépôt, cite le présent plan + marqueur PLAN-AFFICHE — R5/P3-P4) ; miroirs download/ hôte→dépôt (plan + extraction + note + tâches restantes + CW + clone) ; arbitres pré-commit ALL PASS (verify-correct-work · certification-complete · check-triggers-replay · task14-scan-doublons) ; check_plan_protocol P1-P5 ; COMMIT local « Task 108 CLOSE » — **SANS PUSH** (0 PAT fourni ce tour : aucune exposition, KO-L009 — pendance PUSH consignée au worklog et à la liste des tâches restantes, leçon Task 98/101 : PUSH dès PAT frais) ; point d'état (cron : vérification liste plateforme, aucune recréation en boucle — clause anti-boucle).

## Answer key

- **D001** — criterion: écosystème installé sur le profil local depuis le fichier source de la directive (commit 19eb34b). verification: bootstrap canonique rc=0 verdict INSTALLE-REPARÉ ; certification ALL-PASS-6/6 ; garde É1 INSTALLE ; gen-plan/correct-work/clone-chat présents sous `skills/`. source: Bash (G0, ce tour). priority: P1. status: verified.
- **D002** — criterion: relecture intégrale couvrant 100 % de la discussion (153 suites worklog + 20 clones), 0 clone manquant. verification: `download/task108-extraction-blocs.json` — comptes suites/clones = attendus, chaque clone inventorié avec date/task/scellage. source: exécution script G1.1. priority: P1. status: verified.
- **D003** — criterion: note de relecture livrée en mode bloc par bloc (un bloc par phase, points clés + incidents + leçons + pendances, table des 20 clones). verification: `download/note-relecture-blocs-task108.md` présent, sections de blocs = phases extraites, table 20 lignes clones. source: G1.3. priority: P1. status: verified.
- **D004** — criterion: liste des tâches restantes livrée $FACON (par acteur, priorisée, critères d'extinction vérifiables) ET affichée au propriétaire. verification: `download/taches-restantes-task108.md` présent ; chaque entrée a acteur + source + critère + priorité ; vue priorisée rendue au chat en G2.3. source: G2. priority: P1. status: verified.
- **D005** — criterion: correct-work --bloc mené à terme sur les 4 blocs du tour. verification: `download/rapport-cw-task108-bloc.md` — 4 blocs × Étapes 2-5, verdict agrégé assigné, findings classés S1-S4. source: G3. priority: P1. status: verified.
- **D006** — criterion: clone-chat 21ᵉ scellé. verification: clone 8/8 S1-S8, 0 occurrence de jeton (grep mécanique). source: G4. priority: P1. status: verified.
- **D007** — criterion: clôture complète et traçable. verification: worklog suite 154 parité md5 hôte↔dépôt ; arbitres pré-commit ALL PASS ; check_plan_protocol P1-P5 PASS ; commit local créé ; pendance PUSH explicitement consignée (0 PAT ce tour). source: G5. priority: P1. status: verified.

## Garde-fous du tour

- KO-L009 : aucun jeton ce tour (aucun PAT fourni) — aucune credential manipulée, fetch/ls-remote anonymes si utilisés.
- R2/zéro-régression : aucun arbitre, aucun pipeline, aucun SKILL.md modifié — le tour est analytique (lecture seule du système) + livrables documentaires.
- R4 : réutilisation du pattern Task 102 par ADAPTATION (nouveau script task108, étendue 20 clones/153 suites) ; les originaux Task 102 intacts.
- Règle d'or n°6 : français exclusif. Règle d'or n°5 : la relecture n'est pas un re-jeu de Task 91/102 — fenêtre étendue aux 5 clones/suites nouveaux (103→108) et angle nouveau (tâches restantes $FACON).
- #token : G1 ~35 k (extraction + lecture ciblée 20 clones) · G2 ~8 k · G3 ~10 k · G4 ~10 k · G5 ~12 k · total ~75 k (plage E15 estimée 60-90 k).

## Hooks de validation (E8)

Horodatage plan : 2026-11-19T04:35:00Z

Verdict E8 : PASS — Horodatage vérifié : 2026-11-19T04:35:00Z (answer key re-jeu D001-D007 **7/7 verified** — D001 bootstrap rc=0 + certification 6/6 + É1 INSTALLE + re-check rc=0 · D002 153 suites/0 trous/21 clones · D003 note 9 blocs + table 21 clones · D004 8 tâches + vue chat · D005 CW --bloc PASS 4/4 · D006 clone 21ᵉ 8/8 S1-S8 · D007 worklog suite 154 parité md5 + arbitres ALL PASS [vcw 16/16 · certification 6/6 · triggers 101/101 · doublons 0 · answer-key 16/16 ×2] + check_plan_protocol P1-P5 PASS + commit CLOSE local SANS PUSH [0 PAT — pendance 1 commit consignée — aucune auto-référence de SHA] ; E7-DISP chaîne 6 points : plan écrit download/ ✓ · answer key 7 décisions ✓ · E8 horodaté ✓ · worklog R5 ✓ [suite 154] · bloc récapitulatif au chat ✓ · fenêtre native TodoWrite ✓)
