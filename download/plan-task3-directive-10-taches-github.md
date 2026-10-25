# Plan Task 3 — Directive 10 tâches (déclencheurs, Prompt Maitre, #token, arbitrage, tests) + intégration GitHub (push sauvegarde)

> **Session** : web-eb6c8580 (suite) · 2026-10-25 · **Directive propriétaire** : « continue mais avant exécute gen-plan : "prend en compte que te donne ma clé GITHUB […] si tu trouves nécessaire d'envoyer les modifications que tu as faites sur mon dépôt avant d'effectue certaines taches. met à jour le plan d'actions pour faire cela" » — sur la directive antérieure à 10 tâches (déclencheurs §A, Prompt Maitre par skill + francisation idempotente, recalibration #token ×3-4 [conseil → application → test], arbitrage des 4 propositions [correctif bug §6 + drifts a/b/d/f], test robuste, correct-work projet, clone-chat)
> **gen-plan** : **v3.23.1 installée** (règle d'or n°2 — l'environnement d'exécution local reste la version certifiée 6/6) · **Leçon E15 audit appliquée** : estimations #token recalibrées ×3-4 (profil frais local — coût de découverte du corpus documenté au worklog Task 5)
> **Hook E1-RES** : (1) lecture B-11 ✓ — worklog Tasks 1-5 (installation, plan d'audit, exécution audit 7 drifts + bug diagnostiqué, correct-work, clone) + restauration post-reset (archive v2.3 + MODE CLONE + S3 + corrections (e)/(g) ré-appliquées, arbitre @historique ALL PASS 24/24, certification 6/6 re-vérifiée ce jour) ; (2) G-RES ✓ — verdict OK, profil NORMAL ; (3) fraîcheur du plan ✓ — aucune phase de la directive encore exécutée ; le reset plateforme a invalidé l'exécution locale, l'état certifié est restauré
> **Garde É1-INSTALL** : ensure-installed.py --check → INSTALLE (33 entrées KB) ✓ ; certification-complete.py → 6/6 PASS AVEC RÉSERVES ✓ (re-vérifiée en tête de session)
> **Type (E3)** : Type 2 — modification/vérification écosystème skills + infrastructure publication (correct-work §10.6) · **Profil (E6)** : NORMAL (G-RES OK)
> **Statut du plan** : PRÊT — planification M1 (E1-E8) complète ; exécution M2 (E9+) lancée sur directive propriétaire « continue »

## Découverte structurante (E2) — divergence dépôt GitHub vs état local

Diagnostic git effectué en tête de planification (ls-remote + fetch + show) :

- **Distant `bigleon2/KNOWLEDGE` (origin/main = `dc6e81e`, 2026-10-24 20:10)** : lignée **gen-plan v3.27.0** — le bug v3.24.0 y est **déjà analysé (RC1-RC4)** et **corrigé** (commit 26d9846 : hook E7-DISP + table §1.2bis + arbitre `scripts/check_plan_protocol.py` + trigger_evals 12→13 cas ; commit 2bb9beb : PM v3.27.0 régénéré, SHARED v1.7.9 / PM-INSTALL v1.7.3). Autres avancées : cahier-des-charges v2.0.1, serre-cbd CDC v1.2.0. Conventions distantes : `skills/` + `scripts/` + `download/` (livrables) + `worklog.md` (racine) ; publication = commits de contenu puis **commit de journalisation en tip** ; vérification **ls-remote** ; **audit anti-persistance 5 zones** du jeton (remote URL / arborescence / git log -S / ~/.git-credentials / historiques shell) ; re-projection du miroir hôte après publication.
- **Local `/home/z/my-project`** : écosystème restauré du tarball « fork local » (gen-plan **v3.23.1**), certifié 6/6 ce jour + corrections session (e)/(g) @historique + arbitres + rapports. Le repo git local du tarball (5 commits UUID, HEAD `3d593a3`) et le distant sont **sans ancêtre commun** (histoires indépendantes).
- **@historique distant PLUS RICHE** : index §5 distant = 33 entrées (vs 24 locales corrigées) — la lignée y est déjà intégrée au-delà de nos corrections (e)/(g) → **ces corrections ne sont PAS poussables** (elles régresseraient le distant).
- **SKILL.md gen-plan distant (v3.27.0, 409 L)** : **aucune section DÉCLENCHEURS** → la tâche 1 (déclencheurs §A) reste pertinente sur la lignée distante.

**Conséquence (D001/D002 ci-dessous)** : toute poussée de l'état local des skills vers main = **RÉGRESSION interdite** (v3.27.0 → v3.23.1). Les tâches de contenu ciblent la **lignée distante** ; l'état local certifié reste l'**environnement d'exécution** (méthode gen-plan/correct-work + arbitres + certification).

## Answer Key (E1 — hook obligatoire, spec de session — spec-driven n°54)

| ID | Décision (criterion) | Vérification exécutable | Source | Priorité | Statut |
|----|----------------------|------------------------|--------|----------|--------|
| D001 | **Stratégie push additive anti-régression** : jamais d'écrasement d'un fichier distant plus récent ; jamais force-push ; commits forward-only sur origin/main ; `ls-remote` consigné après chaque push ; diff préalable obligatoire avant chaque fichier poussé | `git ls-remote` SHA consigné au worklog ; `git log --oneline origin/main..HEAD` = commits forward-only ; 0 fichier distant supprimé (`git diff --stat origin/main..HEAD` : additions only) | directive propriétaire PAT + découverte divergence (E2) | S1 | pending |
| D002 | **Architecture double-piste** : ENVIRONNEMENT = écosystème local certifié v3.23.1 (méthode, arbitres, certification 6/6 — non re-projeté en cours de session) ; CIBLE DE PUBLICATION = worktree lignée distante v3.27.0 (branche de publication depuis `dc6e81e`) | worktree/branche de publication créée depuis origin/main ; `python3 scripts/certification-complete.py` local → exit 0 à chaque phase locale | découverte divergence + convention « dépôt = source R4 » | S1 | pending |
| D003 | **P0 — push sauvegarde AVANT les tâches lourdes** (directive propriétaire) : pousser le NET-NEW de la session uniquement — rapports/plans/clones `download/` (convention distante) + arbitres absents du distant + append worklog — **@historique local exclu** (distant plus riche, 33 vs 24) | commit P0 présent sur main distant (`ls-remote`) ; liste de fichiers = additions only ; grep PAT dans le commit → 0 | directive propriétaire (PAT) | S1 | pending |
| D004 | **Tâche 6 / correctif bug §6 → OBSOLÈTE** : la lignée distante a corrigé le bug via v3.27.0 (E7-DISP + check_plan_protocol.py, causes RC1-RC4) — arbitrage : ADOPTER la correction distante, consigner notre diagnostic sandbox (C3 diff intégral : canal canonique exonéré, 6 points de substitution seulement ; H1/H2/H3 réfutées) comme **complément d'analyse** au dossier RC1-RC4 | rapport d'arbitrage : statut OBSOLÈTE documenté + renvoi commits distants 26d9846/2bb9beb + section complément d'analyse | rapport-test-bug §6 + git show distant | S1 | pending |
| D005 | **Drifts a/b/d/f ré-arbitrés contre l'état distant** avant toute correction (peuvent être obsolètes sur la lignée v3.27.0 : PM_PATH, --mode correct-work, worklog B1, dérives voie M) — chaque drift reçoit un statut : CORRIGÉ / JOURNALISÉ / OBSOLÈTE (résolu côté distant) | tableau drifts 4/4 statuts non vides dans le rapport consolidé | rapport-audit §5 + correct-work Mode PROJET | S2 | pending |
| D006 | **Hygiène PAT** : URL one-shot uniquement (aucun remote persistant dans .git/config), zéro commit du PAT, audit **anti-persistance 5 zones** après la dernière poussée (remote URL 0 · arborescence 0 · `git log -S` 0 · ~/.git-credentials absent · historiques shell absents), **rotation/révocation du PAT recommandée au propriétaire en clôture** (précédent distant : « RÉVOQUER le jeton transmis ») | grep -r "github_pat" download/ scripts/ skills/ worklog.md → 0 ; git log -S "github_pat" --all → 0 ; audit 5/5 zones VERT | convention distante anti-persistance | S1 | pending |
| D007 | **Zéro-régression locale** : certification 6/6 re-vérifiée après chaque phase touchant l'état local ; archive v2.3 + golden masters intacts ; SHAs `skills/@mon-ecosysteme/` inchangés pendant P1-P6 (environnement stable) | `sha256sum` avant/après par phase ; certification exit 0 | refactoring-engineering R2/R4 | S1 | pending |
| D008 | **#token recalibrés ×3-4** (leçon E15 audit : réel 45-60 k vs estimé 12,2 k — coût de découverte du corpus sur profil frais) + exécution par **lots resumables** (push + worklog à fin de chaque lot/phase — aucune perte au reset/interruption) | présentes estimations ×3-4 dans la table E9-E15 ; worklog append par phase | worklog Task 5 (bilan E15) | S2 | appliqué |
| D009 | **Reprise E1-RES** : tout déclencheur (reprise après interruption/reset) → état dérivé du disque : worklog + `git log` branche publication + `ls-remote` — jamais depuis la mémoire seule | section reprise à jour au worklog à chaque phase | gen-plan v3.23.1 §E1-RES | S1 | pending |
| D010 | **Tâche 2 — garde anti-lecture** : chaque dossier « Prompt Maitre » porte un marqueur d'exclusion (« ce dossier n'est PAS lu par l'orchestration — usage autonome hors écosystème »), n'est PAS indexé au registre KB, et ne casse AUCUN arbitre (certification re-jeu après le dernier lot) | grep marqueur 100 % des dossiers créés ; certification-complete.py exit 0 post-P2 | directive propriétaire (tâche 2) | S1 | pending |
| D011 | **Environnement local NON re-projeté en cours de session** (stabilité de la méthode v3.23.1 + de la certification) ; re-projection du miroir hôte depuis le dépôt = décision propriétaire en clôture (convention distante documentée au rapport final) | SHAs @mon-ecosysteme inchangés P1→P6 ; section « re-projection » du rapport final | D002 + stabilité environnement | S2 | pending |
| D012 | **Traçabilité** : worklog append par phase (≥ 8 sections Task 6+) + clone-chat final (tâche 9) + bilan E15 (écart estimé/réel sur les phases exécutées) | worklog sections ≥ 8 ; clone-chat livré download/ | gen-plan §1.2bis + SHARED | S1 | pending |

## Inventaire (E2) — état de départ

- **Local (environnement)** : 33 skills écosystème + plateforme ; corpus 9 PMs (gen-plan v3.23.1, correct-work v2.7.0, clone-chat v2.0.1, refactor-guard v1.7.0, PM-INSTALL v1.7.1, SHARED v1.7.7, SYNC-CONTEXT v1.4.8, README v2.1.7) ; @historique corrigé (e)/(g) — arbitre ALL PASS 24/24 ; certification 6/6 PASS AVEC RÉSERVES (résidu : avertissement worklog B1 connu) ; archive v2.3 scellée ; 100+ scripts dont arbitres session (audit-phaseA-historique.py, audit-e15-lessons.py, answer-key-checker.py 16/16).
- **Distant (cible)** : origin/main dc6e81e — gen-plan v3.27.0 (SKILL 409 L sans §A DÉCLENCHEURS ; PM 1477 L), SHARED v1.7.9, PM-INSTALL v1.7.3, cahier-des-charges v2.0.1, check_plan_protocol.py (selftest 7/7), PR #1 existante, worklog.md racine (sessions web-f90062ce, web-dd290b0d…), download/ (livrables).
- **Divergence** : aucun ancêtre commun (repo tarball = 5 commits UUID « fork local » vs lignée distante continue) ; @historique distant 33 entrées §5 > local 24.
- **Directive à 10 tâches** : 1 déclencheurs §A → skill.md gen-plan (+ vérif autres familles) ; 2 francisation idempotente + dossier « Prompt Maitre » par skill ; 3 conseil recalibration #token ; 4 application ; 5 test/optimisation ; 6 arbitrage 4 propositions ; 7 test robuste ; 8 correct-work projet ; 9 clone-chat ; (+0 push GitHub intégré en P0 — directive PAT).

## Étapes (E1-E15) — #token recalibrés ×3-4 (leçon E15 — D008)

| Étape | Action | #token (recal.) | Statut |
|-------|--------|--------|--------|
| E1 | Analyse directive + answer key D001-D012 + hook E1-RES + garde É1-INSTALL | 900 | ✓ (ce plan) |
| E2 | Inventaire + **diagnostic divergence GitHub** (ls-remote, fetch, show, diffs @historique/SKILL/PM distants) | 4 000 | ✓ (réel, dépasse la grille — 2e point de données recalibration) |
| E3 | Type 2 (modification/vérification écosystème + infrastructure publication) | 100 | ✓ |
| E4 | Estimation #token recalibrée ×3-4 + cadrage spec-first + État Long (plan + worklog + dépôt git distant = points de reprise) | 200 | ✓ |
| E5 | Skills : gen-plan v3.23.1 (méthode), correct-work v2.7.0 (CIBLE par phase + PROJET), refactoring-engineering v1.1.1 (zéro-régression), refactor-guard v1.7.0 (garde-fous publication), knowledge-observer v1.0.0 (E15), resource-monitor v1.0.0 (G-RES), clone-chat v2.0.1 (clôture), skills-inventory v1.1.0 (découverte) | 300 | ✓ |
| E6 | Profil NORMAL (G-RES OK) | 50 | ✓ |
| E7 | Création du présent plan + re-validation spec (answer key 12/12 vérifiables) | 700 | ✓ |
| E8 | Validation : `python3 scripts/answer-key-checker.py` (16 checks PASS requis) + correct-work(livrable=présent plan, mode=CIBLE) → verdict consigné | 500 | ✓ (worklog Task 6) |
| E9 | **Phase P0 — Push sauvegarde session** (D003) : P0.1 diff net-new (rapports download/, arbitres scripts/, worklog) vs distant (`git show` par fichier candidat) → P0.2 branche publication depuis dc6e81e → P0.3 copie additions + append worklog session → P0.4 commit de contenu + **commit de journalisation en tip** (précédent distant) + push one-shot URL → P0.5 `ls-remote` consigné + audit anti-persistance (zones visibles) + worklog | 8 000 | exécution |
| E10 | **Phase P1 — Tâche 1 Déclencheurs** : extraction §A DÉCLENCHEURS du PM GEN-PLAN (corpus distant v3.27.0) → intégration au SKILL.md distant (v3.27.0 → bump MINOR v3.28.0) + vérification « mêmes erreurs » sur les autres familles (corps SKILL vs §A des PMs — échantillon local + distant) → régénération PM via canal canonique distant (`generer-pm-skill.py`) → commit/push + worklog | 25 000 | à venir |
| E11 | **Phase P2 — Tâche 2 Francisation + Prompt Maitre** (lots de ~10 skills, resumables — D008/D010) : par skill distant : vérif français idempotente (zh→fr si trouvé) + création dossier « Prompt Maitre » (prompt autonome hors écosystème + marqueur d'exclusion anti-lecture orchestration) ; re-jeu certification locale après le dernier lot (garde D010) ; commit/push par lot + worklog | 45 000 | à venir |
| E12 | **Phase P3 — Tâches 3-5 Recalibration #token** : conseil (grilles §2.3/§4 gen-plan distant : multiplicateur « profil frais local ×3-4 » + guidance parallélisation UNIX/PYTHON) → application (SKILL.md distant + PM régénéré) → test (re-jeu estimation vs réel sur la présente session — 2 points de données E2/E9) ; commit/push + worklog | 20 000 | à venir |
| E12bis | **Phase P4 — Tâche 6 Arbitrage 4 propositions** (D004/D005) : correctif bug §6 → OBSOLÈTE (adoption distante documentée + complément d'analyse sandbox) ; drifts a/b/d/f → ré-arbitrage contre distant (CORRIGÉ/JOURNALISÉ/OBSOLÈTE) ; rapport consolidé ; commit/push + worklog | 15 000 | à venir |
| E13 | **Phase P5 — Tâche 7 Test robuste** : re-jeu intégral local (certification 6/6, arbitre @historique, answer-key-checker, py_compile, trigger_evals) + vérifications distantes post-publication (ls-remote, diff --stat additive-only, selftest check_plan_protocol.py si applicable) ; worklog | 12 000 | à venir |
| E14 | **Phase P6 — Tâche 8 correct-work(projet)** fin de chaîne (max 2 rounds) + push final + audit anti-persistance 5 zones complet (D006) + recommandation révocabilité PAT + section re-projection miroir (D011) | 15 000 | à venir |
| E15 | **Phase P7 — Tâche 9 clone-chat** (clôture étape 11) + bilan E15 (écarts estimé/réel des phases exécutées — 3e point de données recalibration) | 10 000 | à venir |

Total exécution estimé (recalibré) : ~150 k #token — **échelle multi-session assumée** (D008) : chaque phase est autonome (push + worklog en fin de phase), la reprise se fait depuis l'état disque/git (D009), jamais depuis la mémoire seule.

## Hooks par phase (E9-E14 — correct-work §5.4)

correct-work(livrables de la phase, mode=CIBLE) après CHAQUE phase : P0 (push sauvegarde) → P1 (déclencheurs) → P2 (francisation+PM, par lot puis phase) → P3 (#token) → P4 (arbitrage) → P5 (test robuste) → P6 (correct-work PROJET final). PASS → phase suivante ; PASS AVEC RÉSERVES → réserves loggées, exécution continue ; FAIL → pause + correction + re-vérification. Graph Diamond : INTERDIT par défaut — série stricte P0→P7 (la directive impose l'ordre ; chaque phase dépend de l'état git de la précédente). Sauvegarde durable en fin de chaque phase = push + worklog (anti-reset).

## Routage N2 (traçabilité d'usage — check-tool-routing Task 22 D006)

- skill → **skill-creator** (conventions structurelles SKILL.md modifiés en P1/P3)
- agent/PM → **agent-creator** (format §6.1 worklog ; PM v3.28.0 régénéré via canal canonique)
- script → **script-creator** (conventions scripts si arbitre ajouté)
- registre KB → **skills-inventory** (découverte — les dossiers « Prompt Maitre » ne doivent PAS y être indexés, D010)
- infrastructure → **script-mon-ecosysteme-infrastructure** (INFRA-1..3 — déploiement des livrables publiés)

## Hygiène PAT & sécurité (D006 — protocole distant anti-persistance)

1. URL one-shot uniquement : `git push https://<PAT>@github.com/bigleon2/KNOWLEDGE.git` — AUCUN `git remote add` persistant, AUCune écriture du PAT dans .git/config, les fichiers, le worklog ou les commits.
2. Audit anti-persistance 5 zones après la dernière poussée : (1) `git config --get-regexp url` → vide ; (2) `grep -ri "github_pat" download/ scripts/ skills/ worklog.md` → 0 ; (3) `git log -S "github_pat" --all` → 0 ; (4) `~/.git-credentials` absent ; (5) historiques shell nettoyés.
3. Clôture : rappel propriétaire — **RÉVOQUER/ROTATION du PAT** (le jeton a circulé en clair dans le chat ; précédent distant : « RÉVOQUER le jeton transmis (office rempli) »).

## Reprise après interruption (E1-RES — D009)

En cas de reset plateforme / coupure de contexte / interruption (« context canceled » — précédent v3.27.0 RC3/RC4) : la reprise dérive l'état du DISQUE uniquement — (1) `tail worklog.md` (dernière phase clôturée + Task ID suivant) ; (2) `git -C KNOWLEDGE-repo log --oneline -5` + `git status` (branche publication, commits en attente de push) ; (3) `git ls-remote` (état réel du distant). Le plan présent reste la spec ; les phases non clôturées reprennent depuis leur dernier lot poussé. Aucune dépendance à la mémoire de session.
