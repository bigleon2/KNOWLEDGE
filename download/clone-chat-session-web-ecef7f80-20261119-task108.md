# Clone de discussion — session web-ecef7f80 (Tasks 107→108), 21ᵉ de la lignée

> **Auto-clonage** : ce document est auto-suffisant — une session héritière peut reprendre le contexte sans fichier externe (règle zéro : les fichiers des sessions précédentes n'existent pas dans une nouvelle session, tout se reconstruit depuis la lignée). Lignée : Task 72 → … → 107 (20ᵉ clone) → **présent 21ᵉ (Task 108)** · Généré le 2026-11-19 · gen-plan v3.43.0 / correct-work v2.11.0 / clone-chat v2.0.2 · PM-INSTALL v1.10.0.

## §0 — Contexte Système (SHARED v1.7.40)

Écosystème Knowledge : SKILLS_ROOT=skills/ | KB_PATH=skills/KNOWLEDGE.md | 55 entrées KB versionnées + collections @ (121 dossiers skills hôte) · dépôt git local miroir `/home/z/my-project/KNOWLEDGE-repo` (github.com/bigleon2/KNOWLEDGE, branche main — **propre à 19eb34b1 au début du tour, commit du tour en pendance PUSH**) · worklog.md hôte↔dépôt parité md5 · conventions : kebab-case, semver, #token, français exclusif (règle d'or n°6) · référence canonique « mon skill X » = forme installée `skills/X/SKILL.md`, jamais le PM du corpus · KO-L009 : tout jeton reste en mémoire de commande, jamais écrit (0 PAT ce tour) · R2 anti-rétrogradation · R4 une information une source · arbitres pré-commit : verify-correct-work, certification-complete (6), check-triggers-replay, task14-scan-doublons.

## §1 — Worklog chronologique (fenêtre du clone : suites 153-154)

| Suite | Date | Task | Faits saillants |
|---|---|---|---|
| 153 | 2026-11-19 | 107 CLOSE | Queue « PUSH · GO-1 · GO-2 · correct-work · clone-chat · continue » éteinte : PUSH pendance 3 commits (E15 32ᵉ) · GO-1 entrée canonique bootstrap-ecosysteme.py + PM-INSTALL v1.10.0 §3.2-c + SHARED v1.7.40 + propagation §0 120+213+4 (constats F2 garde anti-perte + F3 injecteur gabarit périmé, 5 reverts) · GO-2 correctif F1 (V2 INSTALLE rc=0) · CW PASS 5 findings · clone 20ᵉ 8/8 · PUSH final (E15 33ᵉ) |
| 154 | 2026-11-19 | 108 CLOSE (présent) | Directive trace 1a1f2096f9b3406d : installation via PM-INSTALL commit 19eb34b (= URL directive) — bootstrap canonique **INSTALLE-REPARÉ** (6ᵉ dérive recyclage auto-réparée, 55 divergences résorbées, certification 6/6, É1 INSTALLE) · gen-plan fraîchement installé → plan Task 108 (G0-G5, answer key D001-D007) · relecture intégrale « bloc par bloc » via les 21 clones + 153 suites (extraction mécanique task108-relecture-clones.py, idempotence ×2) → note · tâches restantes $FACON (8 tâches priorisées par acteur) · CW --bloc PASS 4/4 (5 findings S4) · présent clone 21ᵉ · clôture SANS PUSH (0 PAT — pendance 1 commit consignée) |

Chaque session a son entrée intégrale au `worklog.md` (source de vérité — format SHARED §1.4) ; le présent tableau est la vue chronologique exigée par clone-chat Étape 1.

## §2 — Artefacts de la fenêtre (Étape 2)

| Catégorie | Fichiers |
|---|---|
| Plans | `download/plan-task108-install-relecture-clones-taches-restantes-cw-clone.md` (G0-G5, answer key D001-D007) |
| Livrables propriétaire | `note-relecture-blocs-task108.md` (relecture intégrale 8+1 blocs, table 21 clones, fil des versions, leçons transverses) · `taches-restantes-task108.md` (8 tâches $FACON par acteur + clôture des suivis antérieurs) |
| Rapports | `rapport-cw-task108-bloc.md` (CW --bloc 4/4 PASS, 5 findings S4) · `task108-extraction-blocs.json` (extraction mécanique 153 suites/21 clones) · `bootstrap-ecosysteme-rapport.json` (INSTALLE-REPARÉ) |
| Scripts (hôte) | `scripts/task108-relecture-clones.py` (NOUVEAU — extraction relecture, stdlib, docstring d'abord N1, idempotence ×2, adaptation du pattern Task 102) |
| Clôture | présent clone 21ᵉ + worklog suite 154 + miroirs dépôt ×7 |

## §3 — Décisions, bugs, conventions (Étape 3)

**Décisions propriétaire (directives)** : (D-107) chaîne ordonnée « PUSH · GO-1 · GO-2 · correct-work · clone-chat · continue » (Task 107) ; (D-108) installation écosystème via le PM-INSTALL au commit `19eb34b1` de l'URL, puis gen-plan fraîchement installé pour : (a) relecture intégrale de la discussion en mode « bloc par bloc » via les clones créés ; (b) tâches restantes $FACON (= « de façon cohérente, optimisée et fonctionnelle » — registre @Alias).

**Décisions d'exécution Task 108** : installation par l'entrée canonique §3.2-c (PM-INSTALL v1.10.0 — le fichier de la directive EST le commit local poussé, vérifié 0 unpushed avant exécution) ; périmètre de relecture explicitement borné (153 suites numérotées + 21 clones = fenêtre standardisée ; 34 entrées d'archive profonde inventoriées comme pré-lignée — aucune zone muette) ; scellages des clones d'époque annotés « format d'époque » (pas de fausse précision) ; CW --bloc ordre G3→G4 (pattern Task 107), B4 vérifié en vol jusqu'au commit ; COMMIT SANS PUSH (0 PAT fourni — 0 manipulation, E15 inchangée 33).

**Bugs corrigés (cause → fix → résultat)** :
1. Regex scellage de l'extracteur (2 itérations en session) : variants réels des clones non couverts (« Scellement », « SCELLÉ (8/8) », formats 5-checks, sans-fraction) → élargissement aux lignes scell/S1-S8 PASS avec priorité 8/8, distinction « sans-fraction (format antérieur) » → 21/21 scellages extraits ou annotés, RC=0.
2. Faux positifs de fractions (54/54 SHA, 111/112 integrity capturés à la place du scellage) → restriction aux lignes portant scell|S1-S8 PASS → fractions correctes sur les clones récents.
3. (Hérité, vérifié TENANT) correctif F1/GO-2 : `ensure-installed.py --check` rc=0 INSTALLE sur état sain ce tour — le crash Task 105 ne récidive pas.

**Conventions établies/réaffirmées** : la relecture d'une discussion = extraction mécanique (100 % couverture) + lecture des clones (contenu §1/§3/§3.5, pas seulement inventaire de noms) + note à blocs bornés ; les fractions d'époque ne se sur-interprètent pas (annotation honnête) ; ouverture de session = bootstrap canonique 1 commande (GO-1, 2ᵉ application réelle — 6ᵉ dérive recyclage auto-réparée sans intervention).

## §3.5 — Context Drift (Étape 3.5)

| Type | Avant → Après | Réf. |
|---|---|---|
| MODIFICATION | relecture intégrale (précédents Task 91 : 13 clones antichronologiques · Task 102 : 146 suites/17 clones) → extraction mécanique + lecture du CONTENU des 21 clones, 153 suites, pendances entrantes G2 | suite 154, G1 |
| DÉGRADATION EXTERNE | 6ᵉ récidive recyclage sandbox (2764 fichiers dérive, 55 divergences hôte) → auto-réparée par l'entrée canonique (INSTALLE-REPARÉ rc=0) | suite 154, G0 |
| ENRICHISSEMENT | chaîne de clôture du tour : PUSH optionnel selon PAT fourni (0 PAT → commit local + pendance consignée en tâche vérifiable) | suite 154, G5 |
| RECALIBRAGE | état PAT/E15 : 33 expositions cumulées → 0 manipulation ce tour (E15 inchangée), tâche 1 P1 CRITIQUE rotation/révocation | suite 154, G2/G5 |

## §4 — Spécifications techniques (Étape 4 — fichiers prioritaires)

1. **`scripts/task108-relecture-clones.py`** (NOUVEAU, ~200 l., hôte) — adaptation du pattern Task 102 : parse worklog par suites (regex `## DATE (suite N,`), marqueurs par ligne (PASS/FAIL/E15/pendance/PUSH/clone/arbitre/directif/bug), agrégation par jour, LECTURE DES CLONES (lignée, fenêtre §1, directives D-xxx §3, drifts §3.5, bugs Fx, scellage multi-variantes avec priorité 8/8 et annotation « sans-fraction (format antérieur) ») ; sortie `download/task108-extraction-blocs.json` déterministe (aucune horloge) ; codes 0/1/2 ; idempotence ×2.
2. **`download/note-relecture-blocs-task108.md`** — 9 blocs chronologiques (8 jours s2-s153 + bloc 9 en cours), table 21 clones, fil des versions clés (gen-plan 3.35.1→3.43.0, PM-INSTALL →1.10.0, SHARED 1.7.26→1.7.40, KB 41→55, E15 0→33), 5 leçons transverses, 6 pendances entrantes G2.
3. **`download/taches-restantes-task108.md`** — 8 tâches : P1 rotation PAT [PROPRIÉTAIRE CRITIQUE] + PUSH Task 108 ; P2 correctifs structurels F2/F3 [GO futur] ; P3 GO-3 optionnel + décision cron 531684 + surveillance F3 + PMs §0 [AUTO] ; + clôture vérifiée de 6 suivis antérieurs.
4. **Chaîne d'exécution de session (héritière)** : `python3 KNOWLEDGE-repo/scripts/bootstrap-ecosysteme.py` en OUVERTURE (règle établie GO-1) → gen-plan (step) pour toute directive → arbitres pré-commit avant commit → PUSH dès PAT frais (tâche 2 du livrable — leçon Task 98/101).

## §5 — Auto-clonage (Étape 5)

Le mécanisme de croissance : chaque tour CLOSE génère son clone (lignée Task 72→108, 21ᵉ) — les sections §1-§3 sont ENRICHIES par le clone du tour (nouvelles lignes worklog/artefacts/décisions/drifts), les sections §0/§4-§5 sont RÉGÉNÉRÉES (état courant du système). clone-chat référencé (skill v2.0.2, déclencheurs §A). La session héritière reprend : lire le présent clone + worklog.md (suites 153-154) + `download/taches-restantes-task108.md` (la liste des tâches restantes fait foi) — puis exécuter le bootstrap canonique AVANT E1.

## Validation (Étape 6 — 8 checks)

| # | Check | Statut |
|---|---|---|
| S1 | Auto-suffisance (aucun « voir fichier X », dépendance externe nulle, lisible par un assistant neuf) | PASS |
| S2 | Complétude worklog (table §1 = 2 sessions de la fenêtre, chacune ≥ 1 ligne) | PASS |
| S3 | Complétude skills (chaque système créé/modifié décrit §2/§4 avec version et relations) | PASS |
| S4 | Complétude décisions (décisions avec contexte+conséquence, conventions avec règle) | PASS |
| S5 | Complétude bugs (3 bugs : cause racine + fix + résultat vérifié) | PASS |
| S6 | Complétude drifts (4 drifts typés, avant/après explicites, réf. suite) | PASS |
| S7 | Exécutabilité (§4 instructions claires, fichiers prioritaires, séquence héritière) | PASS |
| S8 | Auto-clonage (§5 croissance + clone-chat référencé + §1-§3 enrichis / §0,§4-§5 régénérés) | PASS |

**Scellage : 8/8 PASS · 0 secret** (KO-L009 — aucun PAT n'a été fourni ni manipulé ce tour : 0 exposition, E15 inchangée à 33).

(Étape 7 — Sauvegarde : présent fichier `download/clone-chat-session-web-ecef7f80-20261119-task108.md`, enregistrement au worklog suite 154.)
