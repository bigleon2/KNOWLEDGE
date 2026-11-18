# Plan Task 107 — GO-1 (entrée canonique consolidée) + GO-2 (correctif F1) + correct-work + clone-chat

**Directive propriétaire** trace `1a1efebf27dcbafd` (gen-plan mode step) : « PUSH [clé du tour] · GO-1 · GO-2 · correct-work · clone-chat · continue. » — GO-1/GO-2 réfèrent à la feuille de route §8 du rapport Task 105 (`download/rapport-tests-efficacite-task105.md`) : GO-1 = promotion de la voie consolidée en entrée canonique (S1) ; GO-2 = correctif F1 (S2) + test de non-régression dédié (la voie V2 doit rendre INSTALLE sur état sain).
Horodatage plan : 2026-11-19 · gen-plan v3.43.0 mode step (clause §A, précédents Task 84/97/102/103/105/106) · profil NORMAL.

## G0 — PUSH : extinction de la pendance (3 commits Tasks 104-106)

État constaté : HEAD = 0473e8f4 (Task 106 CLOSE), origin/main = 6b79009f, 3 commits locaux sans push (24441ed2, fe85dba6, 0473e8f4), arbre propre.
Action : push `HEAD:main` avec la clé fraîche du tour (KO-L009 — mémoire de commande uniquement, sortie masquée, RC mesuré sans pipe — leçon F2 Task 103). Vérification atterrissage : `git ls-remote` anonyme (0 exposition) → parité HEAD = origin/main, 0 unpushed. E15 : 32ᵉ exposition.

## G1 — GO-1 : promotion de la voie consolidée en ENTRÉE CANONIQUE (S1)

1. **Point d'entrée unique** — `scripts/bootstrap-ecosysteme.py` (dépôt, nouvelle couche outillage) : 1 commande = préflight git dépôt (réparation dérive par `reset --hard LOCAL` + fetch anonyme) → dry-run lecture seule → installation canonique (`eco_install_pipeline.py`, rescellement v2.3 + manifeste inclus) → certification 6 arbitres → garde É1-INSTALL → verdict consolidé compact + rapport JSON. Orchestration R4 (sous-processus des exécutants canoniques, AUCUNE logique de verdict dupliquée, AUCUNE modification du pipeline ni des arbitres — R2/zéro-régression). Convention « docstring d'abord » (S3/F4, N1 tool-routing < 600 octets). `--selftest` sait échouer. Codes retour : 0 = INSTALLE/INSTALLE-REPARÉ · 1 = ECHEC · 64 = usage.
2. **PM-INSTALL v1.9.16 → v1.10.0** : §3.2 ajout clause **(c) entrée consolidée canonique** (point d'entrée unique, gains mesurés campagne Task 105 : −83,3 % tours / −97,6 % octets sans perte de garantie, voies (a)/(b) inchangées, auto-install D727 demeure le self-healing à couverture partielle) ; §2ter +1 ligne socle ; §A.3 étiquette instantané rafraîchie ; en-tête « Complète » complété ; §7 ligne historique v1.10.0.
3. **Recalibrage croisé KO-L004** : SHARED v1.7.39 → v1.7.40 (§6.1 — ligne PM-INSTALL portée v1.9.16→v1.10.0 + note Révision) ; ULTRA régénéré par `scripts/gen-ultra-maitre.py` (install_v/shared_v dérivées dynamiquement — aucun repli manuel).
4. **Exécution de l'entrée canonique** — commit GO-1 D'ABORD (le préflight git de l'entrée consolide répare par `reset --hard` : aucune modification légitime non commitée ne doit être présente), puis bootstrap : verdict attendu vert (INSTALLE), certification ALL PASS 6/6, garde É1 rc=0.
5. **Campagne de non-régression re-jouée** : idempotence ×2 de l'entrée canonique (verdicts normalisés byte-identiques — champs volatils exclus) ; harnais Task 105 `--axe garanties` re-jeu g1-g4 (idempotence prototype ×2 · dry-run 0 mutation preuve mtime · garde R2 0 rétrogradation · arbitres post-campagne 6/6) ; rapports re-jeu copiés au dépôt sous noms `rapport-nonregression-task107-*.json` (les originaux Task 105 du dépôt demeurent intacts — R4, l'historique git fait foi).

## G2 — GO-2 : correctif F1 + test de non-régression dédié (S2)

1. **Correctif chirurgical** (rapport Task 105 §5-F1, 3 lignes) dans `skills/gen-plan/scripts/ensure-installed.py` (copie dépôt) — `etat()` : le contrôle « head miroir » (O-68-1) n'interroge le miroir que si `(ROOT/"KNOWLEDGE-repo"/".git")` existe ; sinon le head pointe ROOT lui-même quand ROOT est le dépôt (le crash `subprocess cwd inexistant` est résorbé — la sémantique O-68-1 « head = source de vérité » est préservée, la copie hôte est inchangée par construction).
2. **Test immédiat** : exécution de la copie dépôt `--check` → rc=0 verdict INSTALLE (l'état Task 105 : crash FileNotFoundError).
3. **Commit GO-2** puis **bootstrap canonique** (la forme gen-plan fixée est projetée à l'hôte par le sync du pipeline — R2) + **test dédié V2** : `scripts/auto-install-ecosysteme.py` (voie D727, exécutée depuis l'hôte, contrôle initial via la copie dépôt) → verdict **INSTALLE** rc=0 sur état sain (l'état Task 105 : ECHEC — preuve mécanique de résorption).
4. **Harnais `--axe flux` re-jeu** : la voie V2 rend INSTALLE (fonctionnel=true) — rapport copié au dépôt `rapport-nonregression-task107-flux.json` ; certification ALL PASS 6/6 + garde É1 post-GO-2.

## G3 — correct-work (projet)

Rapport `download/rapport-cw-task107-projet.md` — mode PROJET (§10.1, couplage gen-plan v3.43.0 Étape 1 = le présent plan) : Phase 1 plan ✓ · Phase 2 erreurs/omissions (délégation alias-eco — registre phrases récurrentes) · Phase 3 structure/conflits · Phase 4 interactions (dépendances inter-skills, versions minimales) · Phase 5 cohérence des raisonnements · verdict (PASS attendu) + findings classés S1-S4 + re-jeu de l'answer key 9/9 verified.

## G4 — clone-chat (20ᵉ, pattern Task 97/99/102/103)

`download/clone-chat-session-web-ecef7f80-20261119-task107.md` — 7+1 étapes (worklog, artefacts, décisions, Context Drift, spécifications, assemblage, validation 8 checks S1-S8, sauvegarde) ; 0 secret (KO-L009 — le PAT du tour n'est JAMAIS écrit) ; drifts du tour ; lignée Task 72→107.

## G5 — Clôture

Worklog suite 153 (parité md5 hôte↔dépôt, cite le présent plan + marqueur PLAN-AFFICHE — R5/P3-P4) ; miroirs download/ hôte→dépôt (plan + rapports GO-1/GO-2 + CW + clone + archive rescellée + manifeste) ; arbitres pré-commit ALL PASS (verify-correct-work · certification-complete · check-triggers-replay · task14-scan-doublons) ; answer-key-checker 16/16 ×2 byte-identiques ; check_plan_protocol P1-P5 ; COMMIT « Task 107 CLOSE » ; PUSH final avec la clé du tour (E15 : 33ᵉ exposition — leçon Task 98/101 : 0 pendance résiduelle) ; ls-remote anonyme de vérification ; point d'état **continue** (cron 531684 — vérification liste plateforme, aucune recréation en boucle · rotation/révocation PAT [PROPRIÉTAIRE] · PMs §0 L2 [AUTO] · G-RES).

## Answer key

- **D001** — criterion: pendance PUSH éteinte (3 commits Tasks 104-106 atterris). verification: `git ls-remote` anonyme → origin/main = HEAD dépôt ; `git rev-list --count origin/main..HEAD` = 0. source: Bash git (G0). priority: P1. status: verified.
- **D002** — criterion: point d'entrée unique créé et sain. verification: `scripts/bootstrap-ecosysteme.py` présent au dépôt ; `--selftest` PASS ; docstring dans les 600 premiers octets (N1) ; aucun exécuteur canonique modifié (`git diff --stat` limité au seul nouveau fichier à G1). source: Bash + git (G1.1). priority: P1. status: verified.
- **D003** — criterion: PM-INSTALL v1.10.0 documente l'entrée canonique (§3.2-c, §2ter, §A.3, §7) et SHARED v1.7.40 recalibré (§6.1 ligne PM-INSTALL + note Révision) + ULTRA régénéré. verification: grep `1.10.0` PM-INSTALL (Version/§3.2/§7/§A.3) ; grep ligne §6.1 SHARED ; diff ULTRA régénéré (install_v dérivée dynamique). source: Bash grep (G1.2). priority: P1. status: verified.
- **D004** — criterion: campagne de non-régression GO-1 au vert. verification: bootstrap canonique verdict INSTALLE rc=0 ; idempotence ×2 verdicts normalisés byte-identiques ; harnais `--axe garanties` g1-g4 PASS 4/4 ; certification ALL PASS 6/6. source: exécutions G1.3 + rapports JSON. priority: P1. status: verified.
- **D005** — criterion: correctif F1 appliqué chirurgicalement (garde d'existence du miroir). verification: diff borné à `etat()` de la copie dépôt ; exécution copie dépôt `--check` → rc=0 INSTALLE (état antérieur : crash). source: git diff + Bash (G2.1). priority: P1. status: verified.
- **D006** — criterion: test de non-régression dédié V2 — la voie D727 rend INSTALLE sur état sain. verification: `auto-install-ecosysteme.py` → JSON verdict INSTALLE rc=0, contrôle initial INSTALLE, 0 critique en défaut ; harnais `--axe flux` voie V2 fonctionnel=true. source: exécutions G2.2-G2.4. priority: P1. status: verified.
- **D007** — criterion: garanties post-GO-2 intactes. verification: bootstrap canonique vert après GO-2 (sync hôte de la forme fixée) ; certification ALL PASS 6/6 ; garde É1 rc=0 ; garde R2 0 rétrogradation. source: exécutions G2.3. priority: P1. status: verified.
- **D008** — criterion: correct-work (projet) mené à terme. verification: rapport CW présent, phases 1-5 exécutées, verdict assigné, findings classés, answer key re-jeu 9/9 verified. source: lecture du rapport (G3). priority: P1. status: verified.
- **D009** — criterion: clone-chat scellé + clôture complète. verification: clone 8/8 S1-S8, 0 secret ; worklog suite 153 parité md5 ; arbitres pré-commit ALL PASS ; answer-key-checker 16/16 ×2 ; P1-P5 PASS ; commit + PUSH final rc=0, 0 unpushed résiduel. source: exécutions G4-G5. priority: P1. status: verified.

## Garde-fous du tour

- KO-L009 : le PAT du tour reste en mémoire de commande uniquement — jamais écrit dans un fichier, un rapport ou le worklog ; sorties masquées ; fetch/ls-remote anonymes.
- R2/zéro-régression : le pipeline, les arbitres et le harnais Task 105 ne sont PAS modifiés (seule l'entrée change — GO-1) ; le correctif F1 restaure le comportement documenté (GO-2), sans changement de spécification ni de version de skill.
- R4 : le prototype V3 du harnais Task 105 demeure une preuve de mesure historique ; son pattern est promu dans le point d'entrée canonique ; les rapports originaux Task 105 du dépôt ne sont pas écrasés (copies re-jeu sous noms task107).
- Commits GO-1 et GO-2 AVANT chaque exécution du bootstrap/harnais (le préflight répare par `reset --hard` — aucune modification légitime non commitée ne doit être présente).

Verdict E8 : PASS — Horodatage vérifié : 2026-11-19 (answer key re-jouée D001-D008 8/8 verified mécaniquement — scripts/task107-rejeu-answer-key.py ; D009 vérifié au push final ; E7-DISP chaîne 6 points : plan écrit download/ ✓ · answer key 9 décisions ✓ · E8 horodaté ✓ · worklog R5 ✓ [suite 153] · bloc récapitulatif au chat ✓ · fenêtre native TodoWrite ✓)
