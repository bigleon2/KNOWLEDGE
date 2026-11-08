# Plan Task 75 — Vérification d'idempotence de l'écosystème post-re-curation vs version précédente

**Horodatage plan : 2026-11-08T05:49:43Z** (rév. 2 — état final, statuts dérivés du disque) · Mode : gen-plan v3.39.0 **NULL** (exécution classique, sans portes de confirmation) · Session : web-ecef7f80 · Trace directive : 1a1b9955a1f207ed · Prérequis : Task 72 CLOSE (re-curation gen-plan v3.39.0 + skill re-curation v1.0.0) · Task 73 CLOSE (tests 3 cibles, non-régression True) · **Task 74 EN VOL** (G1 clone-chat / G2 correct-work --bloc / G3 GO — 0/7 · 0/7 · 0/5, exécution suspendue au GO propriétaire)

## Contexte et périmètre

Directive propriétaire (2026-11-08, trace 1a1b9955a1f207ed, canal zai-web) : « gen-plan : "vérifie que mon écosystème après re-curation reste idempotent à sa version précédente". »

**Interprétation formalisée (E1 — la propriété demandée décomposée en 3 propriétés vérifiables mécaniquement)** :
- **P1 — Équivalence de contenu (vs version précédente)** : la version post-re-curation préserve TOUT le contenu de la version précédente — 9 blocs déplacés byte-identiques en `references/` (R4), contrats verbatim intacts (§A, §0, read_when, evals ×2), zéro perte, zéro duplication ;
- **P2 — Idempotence opérationnelle (re-jeu = no-op)** : re-appliquer les opérations de la re-curation sur l'état courant ne change RIEN — `protocole-test.py --post` ×2 → MAINTIEN DE L'OPTIMISATION stable, `check-recuration.py` ×2 → C1-C4 PASS, `poids-chargement.py` ×2 → byte-identiques, `ensure-installed.py --check` → rc=0 no-op ;
- **P3 — Intégrité vérifiable (écarts justifiés)** : tout écart entre la baseline pré-re-curation et l'état courant est un changement versionné documenté — 0 écart orphelin ; arbitres écosystème PASS en exécution réelle.

**Baseline « version précédente »** = commit git **`011d342`** (Task 71 G5+G6 CLOSE — parent prouvé de `5646e96` re-curation ; `git log -1 --format='%P' 5646e96` → `011d342860e…`). Chaîne documentée post-baseline : `5646e96` (Task 72 G1 re-curation) → `d3ee6e6` (G4+G5 skill re-curation) → `4439592` (G6+G7 CLOSE) → `a790d04` (Task 73 tests) → `a14f750` (Task 73 CLOSE) + resync non-commité Task 74 (installation certifiée post-wipe, worklog suite 50 — commit prévu au G3 GO de la Task 74).

**Trois couches de périmètre** : (a) **gen-plan v3.39.0** (cible directe de la re-curation — équivalence P1 + idempotence P2) ; (b) **skill re-curation v1.0.0** (créé pendant le chantier — présent, fonctionnel, réutilisé comme outil de vérification) ; (c) **écosystème entier** (54 entrées KB — fidélité hôte↔dépôt, écarts justifiés P3, arbitres globaux).

**Position dans le workflow** : la présente vérification s'exécute AVANT la clôture Task 74 (G1-G3 au GO propriétaire) — son rapport sera couvert par le correct-work (projet) --bloc de Task 74 G2 et archivé par le clone-chat Task 74 G1. Le plan Task 74 reste INTACT (R2 — jamais réécrit) ; la présente Task 75 est un plan distinct, référence d'exécution courante.

**Garde E1-RES (ouverture)** : B-11 worklog lu (suite 50 — Task 74 installation certifiée) · G-RES **OK** (disque 12 % / 8,3 Go libres, 0 timeout, budget #token session chaude) · **É1-INSTALL exécutée AVANT E1** : `ensure-installed.py --check` → **rc=0 INSTALLE-REPARÉ** (version-management : 35ᵉ disparition environnementale connue — neutralisation résiliente Task 69 v1.3.0 — auto-réparée depuis le miroir, journalisée ; preuve vivante que la machinerie d'idempotence/réparation fonctionne) · fraîcheur : plan Task 74 valide EN VOL (GO propriétaire en attente — suspension de sa séquence, pas une dérive) · garde post-coupure : acquise (installation certifiée suite 50).

**Arbitrage de voie (règle d'or n°3, journalisé)** : invocation `gen-plan : <tâche>` sans mode explicite → clause mode NULL (§A) : « intégration E13 ou exécution classique ». Choix : **exécution classique en plan distinct (Task 75)** — la demande est une vérification autonome à exécuter immédiatement, antérieure logiquement à la clôture Task 74 ; l'extension E13 en place du plan Task 74 aurait dénaturé son périmètre (clôture) ou imposé une renumérotation destructrice (R2). La Task 74 reprend intacte au GO propriétaire.

**Classification (E3)** : Type 2 (analyse/vérification — livrables documentaires Markdown + JSON). **Profil (E6)** : **NORMAL** (G-RES OK, aucun signal de pression).

**Estimation #token (E4 — grille v3.39.0, contingence re-jeus arbitres)** : G1 ≈ 3 500 · G2 ≈ 3 500 · G3 ≈ 6 000 · G4 ≈ 4 000 · G5 ≈ 3 500 · réserve E13 ≈ 2 000 — **total ≈ 22 500 #token** (bornes 16 000-33 000).

**Sélection skills (E5 — E5-POIDS respecté, lectures ciblées)** : gen-plan v3.39.0 (29,9 Kio INTERMÉDIAIRE — SKILL.md lu intégralement, 337 L ; references/ à la demande) · re-curation v1.0.0 (léger — SKILL.md 104 L lu intégralement ; scripts exécutés) · arbitres `scripts/*.py` (exécutés, jamais chargés intégralement). Disciplines socle mobilisées : loop-engineering (boucle de vérification P0-P7), harness-engineering (arbitres mécaniques = juges), context-engineering (lecture ciblée par blocs).

## Answer key (hook E1) — décisions vérifiables

```yaml
decisions:
  - id: "D001"
    criterion: "Interprétation formalisée P1/P2/P3 documentée au plan ET couverte au rapport final (une section verdict par propriété, chacune appuyée sur des preuves disque)"
    verification: "rg -c 'P1 — Équivalence de contenu|P2 — Idempotence opérationnelle|P3 — Intégrité vérifiable' download/plan-task75-verif-idempotence-ecosysteme-post-recuration.md download/rapport-verif-idempotence-task75.md"
    source: "Directive trace 1a1b9955a1f207ed ; gen-plan v3.39.0 E1 (answer key obligatoire)"
    priority: "S2"
    status: "verified"
  - id: "D002"
    criterion: "Baseline « version précédente » identifiée et prouvée : commit 011d342 = parent de 5646e96 (re-curation) ; intégrité croisée baseline JSON Task 72 ↔ git 011d342 (SKILL.md v3.38.0 sha256 identique modulo étiquette §0, 9 blocs sha256 identiques)"
    verification: "git -C KNOWLEDGE-repo log -1 --format='%P' 5646e96 | rg -c '^011d342' && python3 scripts/task75-verif-idempotence.py --check baseline && echo BASELINE_OK"
    source: "git log miroir ; download/task72-baseline-genplan.json (golden master) ; leçon harnais v2 Task 72 (étiquette §0 normalisée)"
    priority: "S1"
    status: "verified"
  - id: "D003"
    criterion: "Fidélité hôte↔dépôt : skills/ hôte byte-identique à KNOWLEDGE-repo/skills/ (0 divergence hors __pycache__) — l'écosystème installé (Task 74) == état certifié du dépôt"
    verification: "python3 scripts/task75-verif-idempotence.py --check fidelite && echo FIDELITE_OK"
    source: "Task 74 suite 50 (post-install F3 : 54/54 SHA-256, 0 divergence) ; règle d'or n°5 (état vérifiable du disque)"
    priority: "S1"
    status: "verified"
  - id: "D004"
    criterion: "Idempotence P2 noyau : protocole-test.py --post gen-plan exécuté ×2 → verdict MAINTIEN DE L'OPTIMISATION aux DEUX passages, verdict sha-stable (cohérent + fonctionnel + optimisé : contrats == baseline, pointeurs, non-duplication, poids sous seuil)"
    verification: "rg -c 'MAINTIEN' download/protocole-test-gen-plan.json && rg -c 'MAINTIEN DE L.OPTIMISATION.*×2|MAINTIEN.*×2' worklog.md"
    source: "Skill re-curation v1.0.0 §2 P5 ; protocole-test.py --post ; directive (idempotence post-re-curation)"
    priority: "S1"
    status: "verified"
  - id: "D005"
    criterion: "Équivalence P1 noyau : task72-baseline-verifier.py --verifier → PASS sur l'état courant — 9/9 blocs déplacés byte-identiques baseline ↔ references/, contrats verbatim intacts (§A/§0/read_when/evals ×2/comptages), non-duplication 1024 o"
    verification: "python3 scripts/task72-baseline-verifier.py --verifier 2>&1 | rg -c 'PASS' && rg -c '\"verdict\": \"PASS\"' download/task72-verif-recuration.json"
    source: "Harnais T1.1.0 Task 72 (R4 — jamais dupliquer) ; baseline golden master v3.38.0"
    priority: "S1"
    status: "verified"
  - id: "D006"
    criterion: "Arbitre C1-C4 du skill re-curation : check-recuration.py gen-plan ×2 → PASS aux deux passages (C1 pointeurs, C2 non-duplication, C3 marqueurs, C4 seuils)"
    verification: "python3 skills/re-curation/scripts/check-recuration.py gen-plan && python3 skills/re-curation/scripts/check-recuration.py gen-plan && rg -c 'C1-C4.*PASS.*×2' worklog.md"
    source: "Skill re-curation v1.0.0 §2 P7 ; arbitre check-recuration.py"
    priority: "S1"
    status: "verified"
  - id: "D007"
    criterion: "Mesures stables : poids-chargement.py --json ×2 → sorties byte-identiques (cmp OK) ; gen-plan demeure ≤ 30 Kio (maintien de l'optimisation poids)"
    verification: "rg -c 'byte-identiques' worklog.md && python3 skills/gen-plan/scripts/poids-chargement.py --json 2>/dev/null | rg -c 'gen-plan' || rg -c 'poids.*×2' worklog.md"
    source: "Hook E5-POIDS v3.38.0 ; précédent Task 72 T3.1 (poids ×2 idempotent)"
    priority: "S2"
    status: "verified"
  - id: "D008"
    criterion: "Idempotence installation : ensure-installed.py --check → rc=0 no-op (l'état installé est stable ; la réparation version-management horodatée journalisée = preuve de la machinerie, pas une régression)"
    verification: "python3 skills/gen-plan/scripts/ensure-installed.py --check > /dev/null && echo E1_INSTALL_RC0"
    source: "É1-INSTALL v3.35.2 ; neutralisation résiliente version-management v1.3.0 (Task 69)"
    priority: "S2"
    status: "verified"
  - id: "D009"
    criterion: "Écarts justifiés P3 : commit range 011d342..a14f750 == exactement les 5 commits documentés (5646e96, d3ee6e6, 4439592, a790d04, a14f750) ; fichiers non-commités ⊆ classes resync Task 74 (download/, @historique/, @mon-ecosysteme/, KB, scripts/, worklog) — 0 orphelin"
    verification: "python3 scripts/task75-verif-idempotence.py --check diffs && echo DIFFS_JUSTIFIES"
    source: "git log miroir ; worklog suite 50 (resync installation Task 74 — 131 fichiers M en attente du commit Task 74 G3)"
    priority: "S1"
    status: "verified"
  - id: "D010"
    criterion: "Arbitres écosystème PASS en exécution réelle (fresh, hors cache R2) : verify-cross 162/162 · verify-correct-work 16/16 · check-ecosysteme-integrity 112/112 · task14-scan-doublons 0 doublon"
    verification: "python3 scripts/verify-cross.py > /dev/null && python3 scripts/verify-correct-work.py > /dev/null && python3 scripts/check-ecosysteme-integrity.py > /dev/null && python3 scripts/task14-scan-doublons.py 2>&1 | rg -c 'DOUBLONS.*: 0' && echo ARBITRES_PASS"
    source: "Certification Task 74 suite 50 (mêmes arbitres — re-preuve sur état courant)"
    priority: "S1"
    status: "verified"
  - id: "D011"
    criterion: "Rapport final download/rapport-verif-idempotence-task75.md : verdict global mécanique (PASS / PASS AVEC RÉSERVES / FAIL) + une section par propriété P1/P2/P3 avec preuves disque horodatées + tableau des écarts justifiés"
    verification: "ls download/rapport-verif-idempotence-task75.md && rg -c 'VERDICT' download/rapport-verif-idempotence-task75.md && rg -c 'P1|P2|P3' download/rapport-verif-idempotence-task75.md"
    source: "Directive ; règle d'or n°5 (état vérifiable) ; format rapports Task 72/73"
    priority: "S2"
    status: "verified"
  - id: "D012"
    criterion: "Fenêtre native E7-DISP point 6 (TodoWrite) affichée au DÉBUT de l'exécution (G1-G5) et MISE À JOUR à chaque fin de groupe + PLAN-AFFICHE au chat + worklog R5"
    verification: "rg -c 'fenêtre native' worklog.md && rg -c 'PLAN-AFFICHE \\(Task 75' worklog.md"
    source: "Directive complémentaire 2 trace 1a1b7fe1c7238e8d ; gen-plan v3.39.0 E7-DISP point 6"
    priority: "S2"
    status: "verified"
  - id: "D013"
    criterion: "E8 final : answer key 14/14 verified, horodatages couplés plan↔verdict (KO-L003), check_plan_protocol P1-P5 PASS sur le plan révisé"
    verification: "python3 skills/gen-plan/scripts/check_plan_protocol.py --plan download/plan-task75-verif-idempotence-ecosysteme-post-recuration.md --worklog worklog.md && rg -c '14/14 verified' worklog.md"
    source: "gen-plan v3.39.0 E7-DISP point 3 (horodatages couplés) ; précédent Task 73 G8"
    priority: "S2"
    status: "verified"
  - id: "D014"
    criterion: "Sync dépôt ciblée Task 75 (rapport + plan + worklog + scripts du harnais + JSON protocole enrichi) + commit dédié — SANS toucher aux 131 fichiers resync Task 74 en attente (leur commit = Task 74 G3) ; PUSH distant = propriétaire uniquement (KO-L009/D013)"
    verification: "git -C KNOWLEDGE-repo log --oneline -1 | rg -c 'Task 75' && git -C KNOWLEDGE-repo status --short | wc -l | rg -v '^0$' && echo SYNC_CIBLEE"
    source: "KO-L009/D013 (leçons Task 63/71) ; worklog Task 74 (commit G3 en attente)"
    priority: "S3"
    status: "verified"
```

## Groupes d'exécution (structure §5.5)

### G1 — Matériaux de comparaison et fidélité `[TERMINÉ] 6/6` · #token ≈ 3 500

- **SG1.1 Baseline git** `[TERMINÉ] 2/2`
  - T1.1.1 Extraction byte-exacte de la baseline : `git show 011d342:skills/gen-plan/SKILL.md` + `evals/evals.json` + `evals/trigger_evals.json` → `tmp/verif-task75/baseline/` (sha256 consignés) · #token 800
  - T1.1.2 Harnais `scripts/task75-verif-idempotence.py` écrit (N3 Python stdlib, selftest embarqué) — checks : `baseline` (intégrité croisée baseline JSON ↔ git, modulo étiquette §0), `fidelite` (hôte↔dépôt skills/), `diffs` (commit range + classification non-commité), `evals` (identité byte evals baseline↔courant) · #token 1 200
- **SG1.2 Artefacts de référence chargés** `[TERMINÉ] 2/2`
  - T1.2.1 Golden master Task 72 : `download/task72-baseline-genplan.json` (SKILL.md v3.38.0 : 106 465 o, 489 L, sha256 3e71ea45… + 9 blocs + contrats) + `task72-verif-recuration.json` (verdict PASS D001-D005) · #token 300
  - T1.2.2 Protocole généré : `download/protocole-test-gen-plan.json` (nature détectée v3.39.0, tests PRE/POST, verdict POST à enrichir au re-jeu G2) · #token 300
- **SG1.3 Fidélité hôte↔dépôt** `[TERMINÉ] 2/2`
  - T1.3.1 Byte-compare complet `skills/` hôte ↔ `KNOWLEDGE-repo/skills/` (exclusion `__pycache__`) → 0 divergence attendue (D003) · #token 500
  - T1.3.2 État non-commité dépôt inventorié : 131 fichiers M → classes resync Task 74 (périmètre G3 T3.3) · #token 400

### G2 — Idempotence opérationnelle (re-jeu ×2 = no-op) `[TERMINÉ] 4/4` · #token ≈ 3 500  — **PARALLÉLISABLE avec G3 (vague unique après G1 — preuve d'indépendance : écritures/lectures disque disjointes ; G2 écrit `download/protocole-test-gen-plan.json` + sorties stdout, G3 lit `tmp/verif-task75/baseline/` + git + `references/`)**

- T2.1 `protocole-test.py --post gen-plan` **×2** → MAINTIEN DE L'OPTIMISATION aux deux passages, verdict sha-stable (D004) · #token 1 000
- T2.2 `check-recuration.py gen-plan` **×2** → C1-C4 PASS ×2 (D006) · #token 800
- T2.3 `poids-chargement.py --json` **×2** → sorties byte-identiques (cmp) + gen-plan ≤ 30 Kio (D007) · #token 800
- T2.4 `ensure-installed.py --check` → rc=0 no-op (D008) · #token 400

### G3 — Équivalence à la version précédente (P1) `[TERMINÉ] 4/4` · #token ≈ 6 000

- T3.1 `task72-baseline-verifier.py --verifier` → PASS frais : 9/9 blocs byte-identiques baseline ↔ `references/`, contrats verbatim, non-duplication (D005) · #token 1 500
- T3.2 Intégrité croisée baseline : golden master JSON ↔ git 011d342 (sha256 SKILL.md modulo étiquette §0 + 9 blocs + evals ×2) (D002) · #token 1 200
- T3.3 Écarts justifiés écosystème : commit range 011d342..a14f750 == 5 commits documentés exactement + non-commité ⊆ classes resync Task 74 → 0 orphelin (D009) · #token 2 000
- T3.4 Synthèse P1 : zéro perte (chaque bloc v3.38.0 vit UNE fois en `references/` byte-identique), zéro duplication (fenêtres 1024 o), résumés inline NOUVEAUX (pas des copies) · #token 1 300

### G4 — Arbitres globaux et synthèse `[TERMINÉ] 3/3` · #token ≈ 4 000 — **série (dépend de G2+G3 : synthèse)**

- T4.1 Arbitres écosystème en exécution réelle : `verify-cross.py` · `verify-correct-work.py` · `check-ecosysteme-integrity.py` · `task14-scan-doublons.py` (D010) · #token 1 500
- T4.2 Synthèse du verdict global : agrégation P1 (D002/D003/D005) + P2 (D004/D006/D007/D008) + P3 (D009/D010) — pire-des-verdicts, réserves éventuelles qualifiées · #token 1 000
- T4.3 Rapport final `download/rapport-verif-idempotence-task75.md` (D011) · #token 1 500

### G5 — Journalisation, E8 final et clôture `[TERMINÉ] 4/4` · #token ≈ 3 500 — **série (dépend de G4)**

- T5.1 Worklog R5 : entrée Task 75 (suite 51) + PLAN-AFFICHE final + verdicts par groupe (correct-work(groupe) mode CIBLE : livrables vs answer key, arbitres = juges mécaniques — hook §5.4) (D012) · #token 800
- T5.2 Sync dépôt ciblée + commit dédié Task 75 — fichiers Task 75 uniquement, les 131 resync Task 74 restent en attente de leur commit G3 (D014) · #token 1 000
- T5.3 E8 final : answer key 14/14 verified + horodatages couplés + `check_plan_protocol.py` P1-P5 (D013) · #token 900
- T5.4 Clôture : marqueur TASK 75 CLOSE + bilan E15 (auto-calibration grille, leçons) + rappel position Task 74 (G1-G3 au GO propriétaire) · #token 800

## Séquence et parallélisation (Graph Diamond — philosophie #4)

**G1 → {G2 ∥ G3} → G4 → G5**. Série G1→{G2,G3} justifiée : G2/G3 consomment les matériaux extraits par G1 (baseline git + harnais). Parallélisation G2∥G3 : vagues indépendantes prouvées (fichiers disjunts — voir note G2). Série G4/G5 : la synthèse et la clôture dépendent des verdicts de G2+G3. Dégradation gracieuse : tout FAIL → pause, correction, re-vérification (règle d'or n°1 — adaptation journalisée, jamais d'arrêt implicite).

## E8 — Validation du plan (horodatage couplé)

- Arbitre `scripts/answer-key-checker.py` ×2 → **16/16 ALL PASS, sha16 stable** (`3a4a549a6c916174` ×2)
- Arbitre `skills/gen-plan/scripts/check_plan_protocol.py --plan <présent> --worklog worklog.md` → **P1-P5 PASS**

Verdict E8 : PASS (answer-key-checker 16/16 ALL PASS ×2 idempotent + check_plan_protocol P1-P5 PASS — Horodatage vérifié : 2026-11-08T05:49:43Z) · **E8 FINAL : answer key 14/14 verified · P1-P5 re-validés sur rév. 2 · verdict global Task 75 : PASS** (rapport download/rapport-verif-idempotence-task75.md)

*Langue : français intégral (règle d'or n°6). PUSH distant : propriétaire uniquement (KO-L009/D013).*
