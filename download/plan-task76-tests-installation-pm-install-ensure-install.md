# Plan Task 76 — Tests fonctionnels et performances des systèmes d'installation (PM-INSTALL + ENSURE-INSTALL) → corrections + optimisation → correct-work --bloc → correctifs des différés → correct-work --bloc

**Horodatage plan : 2026-11-08T07:25:00Z (final — 14/14 décisions verified)** · Mode : gen-plan(step) · Session : web-ecef7f80 · Trace directive : 1a1b9d4c74daee71 · Prérequis vérifié : Task 75 CLOSE (E8 final PASS 2026-11-08T05:49:43Z, answer key 14/14) · Task 74 EN VOL au GO propriétaire — INTACTE (R2, hors périmètre)

## Contexte et périmètre

Directive propriétaire (2026-11-08, trace 1a1b9d4c74daee71), 4 items dans l'ordre :
1. « fais $FACON un tests $FACON2 fonctionnels et de performances des systèmes d'installation de mon écosystème (PM-INSTALL et ENSURE-INSTALL) dans l'objectif de corriger $FACON leurs failles et de les optimiser $FACON. »
2. « correct-work (projet) --bloc. »
3. « fais $FACON les correctifs des différés consignés et des autres erreurs (même non bloquantes). »
4. « correct-work (projet) --bloc. »

Alias résolus (registre @Alias) : **$FACON = « de façon cohérente, optimisée et fonctionnelle » · $FACON2 = « (cohérent, optimisé et fonctionnel) »**.

Deux cibles de test (systèmes d'installation) :
- **C1 — PM-INSTALL** : `skills/@mon-ecosysteme/PROMPT-MAITRE-INSTALL-ECOSYSTEME.md` **v1.9.10** (51 208 o, unique source d'installation : périmètre §A + ordre §2 + étendue §2bis + instantané §2ter + génération §2quater + critères §3 + mécanisme dual §3.2) **et ses exécutants canoniques** : `scripts/eco_install_pipeline.py` (exécutant canonique §3.2-a), `scripts/install-ecosysteme-local.sh`, `scripts/task21-f2-rebuild-archive.py` (étape 2 rescellement).
- **C2 — ENSURE-INSTALL** : la garde É1-INSTALL `skills/gen-plan/scripts/ensure-installed.py` (Task 23 D006 + Task 29 D001-D004 + Task 56 extension auto-réparation + Task 69 head miroir) + son shim racine `scripts/ensure-installed.py` (délégation Task 29 D001).

Objectif : campagne de tests **fonctionnels ET de performances** → **corriger les failles** → **optimiser le fonctionnement** (items 1) → correct-work --bloc (item 2) → **correctifs des différés consignés + autres erreurs même non bloquantes** (item 3) → correct-work --bloc (item 4). Réutilisation R4 stricte des arbitres existants (check-ecosysteme-integrity.py, test-coherence-interactions.py, verify-cross.py, verify-correct-work.py, poids-chargement.py, generer-pm-skill.py --check, check_plan_protocol.py) — le harnais de campagne ORCHESTRE ces arbitres et MESURE les durées, il ne duplique aucune logique de verdict et n'écrit aucune correction en PRE.

## État initial mesuré (E2, règle d'or n°5 — mesures réelles de session)

- **PM-INSTALL v1.9.10** : corpus hôte == miroir **byte-identiques** (51 208 o, SHA-256 9e19d9047753…) ; §2ter instantané **à jour** sur les 4 familles (GEN-PLAN v3.39.0 · CORRECT-WORK v2.11.0 · CLONE-CHAT v2.0.2 · REFACTOR-GUARD v1.8.1 — conforme au corpus réel) MAIS étiquette de date « au 2026-10-12 » **périmée** (F5) ; registre KB 54 entrées au format strict (57 en-têtes `##` totaux) ; exécutants présents ×3.
- **ENSURE-INSTALL** : 230 L, modes `--check` / `--reinstall` / `--preempt` ; FICHIERS_CLES **9/9 présents** ; état installé rc=0 (54/54 entrées KB — héritage Task 75 P2) ; 36 disparitions environnementales version-management documentées, auto-réparation depuis miroir local démontrée en direct (Task 75 §4 — preuve vivante) ; shim racine fonctionnel (délégation).
- **RUN E2 ACCIDENTEL DOCUMENTÉ (transparence règle d'or n°5)** : l'exploration E2 a invoqué `python3 scripts/eco_install_pipeline.py --help` — l'argument `--help` a été interprété comme CHEMIN DE DÉPÔT (inexistant) → repli silencieux sur le miroir local → **exécution complète du pipeline d'installation** : preflight commit 3171c4b descendant-tolérant OK (pin b75a620 ancêtre) · garde R2 « 0 rétrogradation — host ≤ repo partout » · sync union (corpus 9 PMs + registre + familles + collections + scripts) · rescellement archive · F3 post-install 0 divergence. **Conséquences mesurées : 0 changement de contenu** (dépôt : `diff --numstat` vide — seuls les mode-purs Task 74 connus [129-131, décompte mouvant intra-session, 0 contenu] ; hôte : integrity **112/112 PASS, 0 FAIL** post-run) — preuve vivante d'idempotence du pipeline, ET révélation de la faille F1 en conditions réelles.
- **Failles/constats d'entrée (à confirmer/adjudiquer en campagne PRE)** :
  - **F1 (pipeline — S2)** : aucun contrat CLI — un appel d'aide (`--help`) exécute une installation complète ; argv[1] est silencieusement repurposé en chemin de dépôt, le repli par défaut masque l'erreur utilisateur, aucune confirmation.
  - **F2 (pipeline — S3)** : PIN constant `b75a620` obsolète — 3 commits certifiés plus récents (aa3b99d directive Task 74, a14f750 Task 73 CLOSE/run 2 certifié rc=0, 3171c4b Task 75 CLOSE) ; docstring « @ b75a620 » périmé.
  - **F3 (fichiers de référence — S3)** : `ecosysteme-travail/fichiers-refs/` = 2 copies d'époque aa3b99d (installation Task 74) **divergentes** des formes canoniques courantes : PM-INSTALL.md 50 528 o (a43d5155…, −680 o vs corpus v1.9.10 recalibré Task 72) + ensure-installed.py 1 507 o (shim d'époque ≠ shim courant).
  - **F4 (archive — à adjudiquer)** : après le run E2, archive hôte SHA aa127f04… ≠ copie dépôt a5d911dd… — hypothèse : piliers frais côté hôte (worklog suites postérieures au commit Task 75) ; stabilité byte du rescellement à tester ×2.
  - **F5 (PM-INSTALL — S4 documentation)** : étiquette de date §2ter « au 2026-10-12 » non rafraîchie par le générateur lors des recalibrages v1.9.8→v1.9.10 (les versions, elles, sont à jour).
- **Différés consignés (Task 75 §6 + héritages — item 3 de la directive)** : (a) 131 mode-purs non-commités → **appartiennent au G3 GO de la Task 74** (R2 — NON actionnable par la Task 76) ; (b) **17 skills plate-forme divergents** hôte↔dépôt (copies d'archive dépôt périmées) ; (c) 67 corpus externes dépôt-seuls (règle d'or n°8 — jamais installés par conception) ; (d) conventions de mesure 30 667/30 668 o (self-consistantes) ; (e) ancien S3 Task 55 : plancher inter-scripts→dessin-technique >=1.3.0 — **désormais satisfaisable** (dessin-technique v1.3.0 installé, vérifié E2) ; (f) S4 Task 55 orchestrateur-tsi : déjà résorbé (Task 57 v1.1.1 — vérifié worklog) ; (g) WARN B1 coherence : artefact historique propriétaire, tolérance documentée ; (h) KO-L009 : PUSH = propriétaire uniquement.
- E1-RES : ressources OK ; aucun plan en vol de la présente session ; Task 74 EN VOL intacte → PARALLELE possible G2/G3 (indépendants), série imposée par la directive pour G6→G7→G8.

## Answer key (hook E1) — décisions vérifiables

```yaml
decisions:
  - id: "D001"
    criterion: "Protocole de tests $FACON2 généré et outillé : download/protocole-tests-installation-task76.json (par cible C1 PM-INSTALL / C2 ENSURE-INSTALL : tests fonctionnels, tests de performances, critères de verdict, tolérances) produit par scripts/task76-campagne-tests.py --protocole (source unique), orchestration R4 des arbitres existants (zéro duplication de logique de verdict), mesures de durées ms, agrégation pire-des-verdicts, modes --phase pre|post --cible C1|C2|all, --synthese, --selftest, AUCUNE écriture corrective en PRE"
    verification: "python3 -m py_compile scripts/task76-campagne-tests.py && python3 scripts/task76-campagne-tests.py --selftest (PASS) && python3 scripts/task76-campagne-tests.py --protocole && ls download/protocole-tests-installation-task76.json"
    source: "Directive item 1 (trace 1a1b9d4c74daee71) ; précédents protocoles Task 72/73 ; R4 jamais dupliquer"
    priority: "S1"
    status: "verified"
  - id: "D002"
    criterion: "Campagne PRE — C1 PM-INSTALL : structure (version 1.9.10, sections §A/§2/§2bis/§2ter/§2quater/§3/§3.2/§A.3) + instantané §2ter vs corpus réel (4 familles) + registre §A.3 vs KNOWLEDGE.md (54 entrées) + critères §3 vs arbitres courants + exécutants canoniques présents (pipeline + install-local.sh + rebuild-archive) + sync hôte↔dépôt byte-identité + poids #token + durées — failles F1/F2/F3/F4/F5 documentées en PRE — verdict C1 tracé dans download/rapport-campagne-task76-pre-C1.json"
    verification: "python3 scripts/task76-campagne-tests.py --phase pre --cible C1 && python3 -c \"import json; d=json.load(open('download/rapport-campagne-task76-pre-C1.json')); print(d['cible'], d['verdict'], len(d['tests']))\""
    source: "Directive item 1 (« systèmes d'installation… PM-INSTALL ») ; PM-INSTALL v1.9.10 §2/§2ter/§3/§A.3"
    priority: "S1"
    status: "verified"
  - id: "D003"
    criterion: "Campagne PRE — C2 ENSURE-INSTALL : py_compile + matrice des modes (--check rc=0 INSTALLE · --preempt rc=0 PRIORITE-NONE · --reinstall no-op rc=0 idempotence · mode inconnu rc=64) + idempotence ×2 (sorties byte-identiques) + FICHIERS_CLES 9/9 + détection KB dynamique 54/0 manquant + AUTO-RÉPARATION EN BAC À SABLE (arbre factice isolé sous tmp/ : skill factice supprimé → INSTALLE-REPARÉ rc=0, restauré depuis miroir factice, aucun effet sur l'écosystème réel) + délégation shim racine + durées — verdict C2 tracé dans download/rapport-campagne-task76-pre-C2.json"
    verification: "python3 scripts/task76-campagne-tests.py --phase pre --cible C2 && python3 -c \"import json; d=json.load(open('download/rapport-campagne-task76-pre-C2.json')); print(d['cible'], d['verdict'], len(d['tests']))\""
    source: "Directive item 1 (« ENSURE-INSTALL ») ; garde É1-INSTALL Task 23/29/56/69 ; preuve vivante Task 75 §4"
    priority: "S1"
    status: "verified"
  - id: "D004"
    criterion: "Faille F1 corrigée $FACON : contrat CLI du pipeline — usage explicite (--help/-h affiche l'aide et NE FAIT RIEN), validation de argv[1] (chemin explicite inexistant → ABANDON rc≠0, PLUS JAMAIS de repli silencieux sur argument explicite), mode --dry-run lecture seule (rapport complet sans aucune mutation) ; py_compile + re-test : --help n'exécute plus rien (aucun mtime modifié), --dry-run produit le rapport avec 0 divergence et 0 écriture"
    verification: "python3 scripts/eco_install_pipeline.py --help (rc=0, usage affiché, aucune mutation) && python3 scripts/eco_install_pipeline.py /chemin/inexistant (rc!=0 ABANDON explicite) && python3 scripts/eco_install_pipeline.py --dry-run (rapport, 0 mutation — vérifiée par mtime/SHA stables)"
    source: "Constat E2 réel (run accidentel documenté) ; leçon Task 17 (toute mutation doit échouer si son sous-traitement échoue — symétrique : une demande d'aide ne doit jamais muter)"
    priority: "S1"
    status: "verified"
  - id: "D005"
    criterion: "Faille F2 corrigée : PIN du pipeline actualisé au dernier commit certifié d'installation (a14f750 — Task 74 run 2 rc=0) + docstring rafraîchi ; garde descendant-tolérant re-vérifiée sur HEAD courant (3171c4b descendant de a14f750)"
    verification: "rg -n 'a14f750' scripts/eco_install_pipeline.py && python3 scripts/eco_install_pipeline.py --dry-run (preflight OK — pin a14f750 ancêtre)"
    source: "Constat E2 ; sémantique pin = garde anti-rétrogradation (jamais un verrou d'égalité — Task 8)"
    priority: "S2"
    status: "verified"
  - id: "D006"
    criterion: "Adjudications F3/F4/F5 $FACON : (F3) fichiers-refs resynchronisés aux formes canoniques courantes (PM-INSTALL v1.9.10 corpus + shim courant) avec mention d'époque aa3b99d conservée au worklog (perte d'information nulle) ; (F4) stabilité byte du rescellement testée ×2 (mêmes entrées → mêmes octets ?) + divergence hôte/dépôt EXPLIQUÉE mécaniquement (piliers frais — preuve SHA) et consignée ; (F5) étiquette de date §2ter rafraîchie (« au 2026-11-07 » — date du dernier recalibrage v1.9.10) au corpus hôte + dépôt + fichiers-refs, R2 vérifié (aucun contenu versionné modifié hors documentation de date)"
    verification: "diff ecosysteme-travail/fichiers-refs/PM-INSTALL.md skills/@mon-ecosysteme/PROMPT-MAITRE-INSTALL-ECOSYSTEME.md (identiques) && rg 'au 2026-11-07' skills/@mon-ecosysteme/PROMPT-MAITRE-INSTALL-ECOSYSTEME.md && rapport campagne G5 : test F4-stabilité PASS"
    source: "Constats E2 F3/F4/F5 ; R4 une information une source ; règle d'or n°5 (hypothèse F4 prouvée mécaniquement, jamais affirmée)"
    priority: "S2"
    status: "verified"
  - id: "D007"
    criterion: "Campagne POST + non-régression stricte : batterie C1+C2 re-exécutée complète — failles PRE résorbées vérifiées mécaniquement (F1 : --help sans effet · F2 : pin a14f750 · F3 : fichiers-refs identiques · F4 : stabilité expliquée) + non-régression test à test (aucun verdict dégradé vs PRE) + --dry-run du pipeline = voie de test sans mutation — synthèse download/rapport-campagne-task76-post-synthese.json (verdict_global_post n'agrège que les POST — leçon harnais Task 73)"
    verification: "python3 scripts/task76-campagne-tests.py --phase post --cible all && python3 scripts/task76-campagne-tests.py --synthese post && python3 -c \"import json; d=json.load(open('download/rapport-campagne-task76-post-synthese.json')); print(d['verdict_global_post'], d['non_regression'])\""
    source: "Directive item 1 (« corriger ») ; R2 non-régression ; règle d'or n°5"
    priority: "S1"
    status: "verified"
  - id: "D008"
    criterion: "correct-work (projet) --bloc n°1 (directive item 2) : blocs G1→G5 vérifiés bloc par bloc, verdict par bloc, corrections re-vérifiées (max 2 rounds), agrégation pire-des-verdicts + answer-key-checker — verdict consigné au worklog"
    verification: "worklog suite correspondante : « correct-work (projet) --bloc n°1 : <verdict> » + table des blocs"
    source: "Directive item 2 ; protocole correct-work §1.7 (v2.9.0) ; précédent Task 72 G6"
    priority: "S1"
    status: "verified"
  - id: "D009"
    criterion: "Rapport final : download/rapport-tests-installation-task76.md (méthodologie, 2 cibles × PRE/POST, failles → corrections F1-F5, différés → correctifs/justifications, verdicts, durées, leçons, guidance)"
    verification: "ls -la download/rapport-tests-installation-task76.md && rg -c 'C1|C2' download/rapport-tests-installation-task76.md"
    source: "Directive (objectif global) ; règle francophone (règle d'or n°6)"
    priority: "S1"
    status: "verified"
  - id: "D010"
    criterion: "Correctifs des différés consignés + autres erreurs même non bloquantes (directive item 3) : (a) plancher inter-scripts→dessin-technique >=1.3.0 : SATISFAIT vérifié mécaniquement (v1.3.0 installé + dépendance YAML) et consigné (différé Task 55 auto-résorbé par l'évolution) ; (b) 17 skills plate-forme divergents : ressync hôte→dépôt des 17 copies d'archive (0 divergence `diff -rq` après) ; (c) conventions 30 667/30 668 : note croisée documentée dans les deux mesureurs (aucun comportement modifié) ; (d) non-actionnables justifiés mécaniquement : 131 mode-purs → Task 74 G3 GO (R2 — la Task 76 ne les commit PAS), 67 corpus externes → règle d'or n°8, WARN B1 → tolérance documentée des protocoles, KO-L009 → propriétaire"
    verification: "rg -n 'version: 1.3.0' skills/dessin-technique/SKILL.md && diff -rq skills/pdf KNOWLEDGE-repo/skills/pdf (vide) [×17 automatisé] && rg '30 667|30 668' skills/re-curation/scripts/protocole-test.py scripts/task72-baseline-verifier.py (notes croisées) && git -C KNOWLEDGE-repo status (mode-purs Task 74 NON commités par la Task 76)"
    source: "Directive item 3 ; Task 75 §6 ; S3 Task 55 ; R2 Task 74 intacte"
    priority: "S1"
    status: "verified"
  - id: "D011"
    criterion: "correct-work (projet) --bloc n°2 (directive item 4) : couvre le groupe G7 (correctifs différés) + re-certification globale (integrity · coherence · vcw · cross après les ressync) — verdict par bloc, agrégation pire-des-verdicts"
    verification: "worklog suite correspondante : « correct-work (projet) --bloc n°2 : <verdict> » + arbitres re-certifiés 0 FAIL"
    source: "Directive item 4 ; protocole correct-work §1.7"
    priority: "S1"
    status: "verified"
  - id: "D012"
    criterion: "E8 final : answer key 14/14 verified + horodatages croissants G1→G8 au worklog + check_plan_protocol P1-P5 PASS post-finalisation (horodatage plan == horodatage verdict — KO-L003)"
    verification: "python3 skills/gen-plan/scripts/check_plan_protocol.py --plan download/plan-task76-tests-installation-pm-install-ensure-install.md --worklog worklog.md (VERDICT : PASS)"
    source: "Hook E7-DISP ; garde KO-L003 (verdict frais)"
    priority: "S1"
    status: "verified"
  - id: "D013"
    criterion: "Fenêtre native AFFICHE-PLAN (E7-DISP point 6) : liste de tâches native (TodoWrite) affichée au DÉBUT de l'exécution et MISE À JOUR à chaque fin de groupe G1→G8 — preuve vivante : la présente exécution"
    verification: "fenêtre native visible dans la session (statuts G1→G8 tenus) + mentions worklog à chaque fin de groupe"
    source: "Directive complémentaire 2 Task 72 (trace 1a1b7fe1c7238e8d) intégrée E7-DISP point 6 v3.39.0"
    priority: "S1"
    status: "verified"
  - id: "D014"
    criterion: "KO-L009 + R2 : aucun push ni manipulation de jeton par l'agent ; Task 74 EN VOL intacte (les 131 mode-purs ne sont PAS commités par la Task 76) ; clôture : worklog R5 (suites consignées) + sync dépôt ciblée + commit dédié Task 76 (fichiers Task 76 uniquement — corrections F1/F2/F5 + ressync 17 plateformes + fichiers-refs + livrables)"
    verification: "absence de commande push distante dans la session + git -C KNOWLEDGE-repo log (commit Task 76 ciblé, mode-purs Task 74 toujours en attente) + worklog suites Task 76"
    source: "KO-L009 points 1-2-5 ; R2 ; précédents commits ciblés Task 73/75"
    priority: "S1"
    status: "verified"
```

## Groupes d'exécution (chaîne step : correct-work(groupe) après chaque groupe, max 2 rounds)

### G1 — Protocole de tests $FACON2 + outillage + E8 initial — #token estimé 4-6 k

- **T1.1 Protocole adapté** : download/protocole-tests-installation-task76.json — par cible (C1 PM-INSTALL / C2 ENSURE-INSTALL), tests fonctionnels (structure, contrats, modes, auto-réparation en bac à sable, sync) et de performances (poids #token, durées ms) + critères de verdict (pire-des-verdicts, tolérances documentées : WARN B1 hérité toléré, divergence archive F4 = à adjudication mécanique).
- **T1.2 Script de campagne** : scripts/task76-campagne-tests.py — orchestration R4 (arbitres existants, zéro duplication de logique de verdict), durées par test, agrégation, modes `--phase pre|post --cible C1|C2|all`, `--synthese`, `--protocole`, `--selftest` ; AUCUNE écriture corrective en PRE ; le bac à sable d'auto-réparation vit sous tmp/ (leçon L-75-a : /tmp ne persiste pas).
- **T1.3 Validation et affichage** : py_compile + selftest + export protocole ; plan journalisé au worklog (suite + marqueur PLAN-AFFICHE) ; E8 initial (check_plan_protocol P1-P5) ; **fenêtre native affichée au début de l'exécution** (E7-DISP point 6).

### G2 — Campagne PRE — C1 PM-INSTALL (fonctionnel + performances) — #token estimé 3-4 k

- T2.1 Exécution `--phase pre --cible C1` : structure + §2ter vs corpus + §A.3 vs KB + critères §3 + exécutants ×3 + sync hôte↔dépôt + poids + F1/F2/F3/F4/F5 documentés en PRE.
- T2.2 Analyse des résultats, consignation worklog, verdict C1.
- T2.3 correct-work(groupe G2).

### G3 — Campagne PRE — C2 ENSURE-INSTALL (fonctionnel + performances, //G2) — #token estimé 4-5 k

- T3.1 Exécution `--phase pre --cible C2` : py_compile + matrice des modes ×4 + idempotence ×2 + FICHIERS_CLES + KB dynamique + **bac à sable auto-réparation** (arbre factice isolé tmp/task76-sandbox/ : KB factif ≥14 entrées, skill factif supprimé → INSTALLE-REPARÉ rc=0 depuis miroir factif) + shim racine + durées.
- T3.2 Analyse, consignation, verdict C2.
- T3.3 correct-work(groupe G3).

### G4 — Corrections $FACON des failles F1-F5 + optimisation — #token estimé 5-7 k

- T4.1 **F1** : contrat CLI du pipeline (usage/--help sans effet, validation argv[1] explicite, mode --dry-run lecture seule) + tests de non-régression (mtimes/SHA stables).
- T4.2 **F2** : PIN → a14f750 + docstring ; **F5** : étiquette de date §2ter (corpus hôte + dépôt + fichiers-refs après ressync).
- T4.3 **F3** : ressync fichiers-refs aux formes canoniques (mention d'époque au worklog) ; **F4** : test stabilité rescellement ×2 + explication mécanique de la divergence hôte/dépôt consignée.
- T4.4 Optimisations : mesure des durées avant/après, recommandation Task 73 §10.1 (détection complémentaire C2 à l'ouverture) adjudiquée SANS nouveau code si la garde É1-INSTALL couvre déjà la détection critique (R4).
- T4.5 correct-work(groupe G4).

### G5 — Campagne POST + comparaison PRE/POST — #token estimé 3-4 k

- T5.1 Re-exécution complète `--phase post --cible all` + `--synthese post` (leçon Task 73 : verdict global POST n'agrège que les POST).
- T5.2 Comparaison test à test (non-régression stricte : aucun verdict dégradé ; failles F1-F5 résorbées ou adjudiquées) ; correct-work(groupe G5).

### G6 — correct-work (projet) --bloc n°1 + rapport final (directive item 2) — #token estimé 3-5 k

- T6.1 correct-work (projet) --bloc n°1 : blocs G1→G5 (verdict par bloc, pire-des-verdicts, findings S1-S4, 2 rounds max) + answer-key-checker D001-D007.
- T6.2 Rapport final download/rapport-tests-installation-task76.md + statuts verified D001-D009 (partiels — complétés à G8).

### G7 — Correctifs des différés consignés + autres erreurs même non bloquantes (directive item 3) — #token estimé 4-6 k

- T7.1 Plancher dessin-technique >=1.3.0 : vérification mécanique SATISFAIT (v1.3.0 + dépendance YAML inter-scripts) + consignation (différé Task 55 auto-résorbé).
- T7.2 17 skills plate-forme divergents : ressync hôte→dépôt des copies d'archive + vérification `diff -rq` ×17 (0 divergence).
- T7.3 Conventions 30 667/30 668 : notes croisées dans les deux mesureurs (aucun comportement modifié).
- T7.4 Non-actionnables justifiés mécaniquement (131 mode-purs → Task 74 G3 [R2] · 67 externes → règle d'or n°8 · WARN B1 → tolérance documentée · KO-L009 → propriétaire) ; correct-work(groupe G7).

### G8 — correct-work (projet) --bloc n°2 (directive item 4) + E8 final + clôture — #token estimé 4-6 k

- T8.1 correct-work (projet) --bloc n°2 : blocs G6-G7 + re-certification globale (integrity · coherence · vcw · cross après ressync) — verdict par bloc, agrégation.
- T8.2 E8 final : answer key 14/14 verified + horodatage couplé + check_plan_protocol P1-P5 PASS post-finalisation.
- T8.3 Clôture : worklog R5 + sync dépôt ciblée (fichiers Task 76 uniquement — les 131 mode-purs Task 74 restent en attente de leur commit G3, R2) + commit dédié Task 76 — PUSH = propriétaire (KO-L009).

## Estimation #token totale

~30-43 k (G1 outillage 4-6 k · G2-G3 campagnes PRE 7-9 k · G4 corrections 5-7 k · G5 POST 3-4 k · G6 cw--bloc n°1 + rapport 3-5 k · G7 correctifs différés 4-6 k · G8 cw--bloc n°2 + clôture 4-6 k — grille §4 « exécution complexe » × coefficient multi-groupes ; skills mobilisés : gen-plan [pilotage], correct-work [--bloc ×2], re-curation [protocole-test référence]).

## Verdict E8

**Verdict E8 : PASS (FINAL — plan exécuté intégralement : G1 ✅ outillage [protocole 23 tests + harnais selftest 8/8 + E8 initial P1-P5] ; G2 ✅ PRE C1 FAIL 7 PASS / 1 RÉSERVES / 4 FAIL [failles F1/F2/F3/F5 + F4 à adjudiquer capturées mécaniquement] ; G3 ✅ PRE C2 PASS 11/11 [garde saine, auto-réparation bac à sable + contrôle négatif] ; G4 ✅ corrections F1-F5 [contrat CLI + --dry-run 0 mutation prouvée · PIN a14f750 · PM-INSTALL v1.9.11 + cause racine générateur · véhicule archive unifié v2.2 hôte==dépôt 1015308d… · fichiers-refs alignés · integrity 112/112] ; G5 ✅ POST [C1 12/12 · C2 11/11 · FAIL→PASS · non-régression TRUE] ; G6 ✅ correct-work --bloc n°1 PASS [0 S1 · 0 S2 · 5 harnais résorbés] + rapport final ; G7 ✅ correctifs différés [plancher dessin-technique résorbé v1.3.0 >= v1.3.0 · 17 plateformes ressync 0 divergence · conventions 30 667/30 668 notes croisées · non-actionnables justifiés mécaniquement] ; G8 ✅ correct-work --bloc n°2 PASS [blocs G6-G7 + re-certification : integrity 112/112 · coherence 55/0/0 PASS STRICT · vcw 16/16 · cross 100,0 %] ; answer key 14/14 verified ; fenêtre native D013 maintenue G1→G8 ; pendance PUSH propriétaire D014 [KO-L009 — les 131 mode-purs Task 74 restent au G3 GO, R2]. — Horodatage vérifié : 2026-11-08T07:25:00Z)**
