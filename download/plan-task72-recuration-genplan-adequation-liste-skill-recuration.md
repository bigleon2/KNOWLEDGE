# Plan Task 72 — Chantier R1 : re-curation progressive disclosure de gen-plan + adéquation + liste priorisée + skill re-curation

**Horodatage plan : 2026-11-08T23:59:00Z (final — 15/15 décisions verified)** · Mode : gen-plan(step) · Session : web-ecef7f80 · Trace directive : 1a1b79af6dcff4c5 (dédoublonnée des reçus partiels 1a1b75a2…/1a1b75a96…/1a1b78a7…/1a1b7955…) · **Rév. 3 — directive complémentaire 2 trace 1a1b7fe1c7238e8d : fenêtre native d'affichage du plan intégrée à AFFICHE-PLAN/E7-DISP (D015 + SG1.3bis — v3.39.0 amendée PRÉ-publication)** · Rév. 2 : directive complémentaire 1a1b7b297b7b4975 (skill re-curation implémenté d'un script — G4/D009/D010 + T1.1.0) · gen-plan v3.38.0 → v3.39.0 (D001)

## Contexte et périmètre

Directive propriétaire à 7 items : (1) Chantier R1 prioritaire — re-curation progressive disclosure de gen-plan (le plus lourd skill, ~26 k tokens, file complète download/rapport-poids-chargement-task71.md), $FACON et en adéquation avec les règles de l'écosystème ; (2) tester l'adéquation du skill gen-plan avec l'écosystème ; (3) analyser l'écosystème pour générer la liste triée par priorité des prochains éléments à re-curer (progressive disclosure, règles et protocoles respectés, tests pour être sûr) ; (4) créer un skill « re-curation » ayant pour objectif la re-curation progressive disclosure d'éléments de l'écosystème ; (5) tester $FACON le skill re-curation ; (6) correct-work (projet) --bloc ; (7) clone-chat.

**Directive complémentaire 1 (2026-11-08, trace 1a1b7b297b7b4975 — rév. 2 du plan)** : « le skill "re-curation" devra être implémenté d'un script dont l'objectif est de s'assurer $FACON [de façon cohérente, optimisée et fonctionnelle] du maintien de l'optimisation du fonctionnement de mon écosystème pour qu'il soit $FACON2 [(cohérent, optimisé et fonctionnel)] en faisant des tests $FACON2 (génère un protocole de test adapté à mon écosystème) avant d'effectuer les "re-curation progressive disclosure" sur les éléments de mon écosystème pour trouver la méthode la plus optimisée et performante pour effectuer les "re-curation progressive disclosure" sur les éléments de mon écosystème. » — intégration : **G4** (le skill est IMPLÉMENTÉ d'un script principal `scripts/protocole-test.py` : GÉNÈRE un protocole de test adapté à l'élément ciblé, l'exécute en phase PRE AVANT toute re-curation [baseline golden master, GO/NO-GO], le ré-exécute en POST [maintien de l'optimisation : cohérent/optimisé/fonctionnel], arbitre les méthodes candidates en mode `--compare`), **D009/D010** enrichis, et principe « tests avant re-curation » rendu explicite en **G1** (T1.1.0 baseline golden master AVANT tout move).

**Directive complémentaire 2 (2026-11-08, trace 1a1b7fe1c7238e8d — rév. 3 du plan)** : « je veux que la fenêtre qui affiche les étapes du plan d'actions soit affichée via la fonction, le script ou la commande qui est dédiée à ce rôle nativement dans "Z.ai" (ou via la commande à laquelle "Z.ai" fait appel) et cela au début de l'exécution du plan d'actions, ainsi qu'à chaque fois qu'une étape du plan d'actions se terminent. intègre $FACON cette fonction, script ou commande dans "AFFICHE-PLAN" de mon écosystème. » — intégration : **D015 + SG1.3bis** : le mécanisme natif dédié à l'affichage des étapes d'un plan chez Z.ai est la **liste de tâches native** (outil `TodoWrite` en écriture / `TodoRead` en lecture — fenêtre dédiée du client) ; il devient le canal d'affichage de la fenêtre des étapes du plan dans **E7-DISP (point 6 « fenêtre native »)** : affichée au DÉBUT de l'exécution du plan d'actions et MISE À JOUR à chaque FIN d'étape (groupe `G<k>`) — canal SUPPLÉMENTAIRE (le bloc récapitulatif au chat, le marqueur `PLAN-AFFICHE` worklog et la garde `check_plan_protocol.py` P1-P5 restent inchangés) ; amendement de v3.39.0 PRÉ-publication (dépôt encore à v3.38.0 → R2-propre, pas de seconde montée de version, la cascade unique SG1.4 porte la version consolidée).

**État initial mesuré (E2, règle d'or n°5 — scripts/task72-mesure-sections.py, sortie download/task72-poids-sections-genplan.json)** : SKILL.md gen-plan v3.38.0 = 104,0 Kio ≈ 26 616 #token · 489 lignes. Sections dominantes : §5.6 Journal des versions 31,6 Kio · §1.5 Règles d'or 19,0 Kio · §1.6 Disciplines 11,0 Kio · §1.2bis Hooks (blocs PATTERN) 8,7 Kio = 70,3 Kio (68 %). Verdict arbitre poids-chargement.py : CRITIQUE (≥ 60 Kio). E1-RES : garde INSTALLE-REPARÉ rc=0 (version-management 5ᵉ disparition, auto-réparée miroir) · G-RES OK → PARALLELE · aucun plan en vol (Task 71 CLOSE).

## Answer key (hook E1) — décisions vérifiables

```yaml
decisions:
  - id: "D001"
    criterion: "gen-plan v3.39.0 installé des deux côtés (hôte + dépôt) avec cascade complète"
    verification: "grep '^version: 3.39.0' skills/gen-plan/SKILL.md && ls skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.39.0.md"
    source: "Étude Task 70 §6 R1 ; semver (restructuration fonctionnelle à fonctionnalité égale = MINOR)"
    priority: "S1"
    status: "verified"
  - id: "D002"
    criterion: "SKILL.md gen-plan < 30 Kio (verdict INTERMÉDIAIRE ou mieux), réduction >= 60 % des #token de chargement par défaut"
    verification: "python3 scripts/poids-chargement.py --top 3 (gen-plan < 30,0 Kio) — avant 104,0 Kio / 26 616 #token"
    source: "Arbitre poids-chargement.py v1.0.0 (seuils OK < 12 / LOURD >= 30 / CRITIQUE >= 60 Kio)"
    priority: "S1"
    status: "verified"
  - id: "D003"
    criterion: "9 blocs déplacés R4 byte-identiques vers references/ : journal-versions.md (§5.6), regles-or.md (§1.5 règles d'or + leçons §1.14/§1.15), disciplines-mobilisation.md (§1.6), protocoles-detailles.md (PATTERN E1-RES/E7-DISP + §1.16 routage + §5.5 mode step + philosophie #4) + append contingences §4 à grille-token.md (fichier existant)"
    verification: "script de vérification : SHA-256 de chacun des 9 blocs déplacés == SHA-256 de la baseline T1.1.0 == SHA-256 du bloc dans son fichier references/ (9/9)"
    source: "R4 byte-identité ; pattern industrie progressive disclosure (étude Task 70 §7.3)"
    priority: "S1"
    status: "verified"
  - id: "D004"
    criterion: "Aucune duplication : résumés inline = textes nouveaux ; §5.6 inline ne garde que l'entrée courante v3.39.0"
    verification: "vérif mécanique : aucun bloc > 1024 octets identique entre SKILL.md et chaque fichier references/"
    source: "R4 ne jamais dupliquer ; KO-L003"
    priority: "S1"
    status: "verified"
  - id: "D005"
    criterion: "Contrats inline intacts : 15 cas trigger_evals + déclencheurs verbatim §A + commandes canoniques + glossaire $FACON + §0 SHARED — baseline capturée AVANT tout move (T1.1.0, directive complémentaire), comparaison mécanique après"
    verification: "grep après == baseline T1.1.0 sur les motifs de contrat (liste verrouillée au script de vérification)"
    source: "Non-régression triggers (précédent Task 61 F-V1-1)"
    priority: "S1"
    status: "verified"
  - id: "D006"
    criterion: "Cascade KO-L004 complète : delta verrouillé, PM v3.39.0 (subs chirurgicales, PM auto-portant sans duplication intra-PM), PM v3.38.0 archivé R4, pin, KB, historiques, ULTRA x2, sweep 9 skills, arbitres 0 FAIL"
    verification: "python3 scripts/generer-pm-skill.py --check (rc=0) ; integrity 110/110 ; coherence 0 FAIL ; cross 100 % ; vcw ALL PASS"
    source: "KO-L004 v1.1.0 ; précédents v3.37.2/v3.38.0"
    priority: "S1"
    status: "verified"
  - id: "D007"
    criterion: "Adéquation gen-plan <-> écosystème testée par batterie mécanique complète, verdicts tracés, WARN documentés"
    verification: "rapport download/rapport-adequation-genplan-task72.md (4 arbitres + 4 selftests + evals 9+15 + poids + couverture PM)"
    source: "Item 2 directive"
    priority: "S1"
    status: "verified"
  - id: "D008"
    criterion: "Liste priorisée des prochaines re-curations fondée sur critères mécaniques + tests de sûreté (idempotence x2, croisement mesures/disque échantillon 5, cartographie sèche du n°1)"
    verification: "livrable download/liste-recuration-priorisee-task72.md avec tableau trié + preuves de test"
    source: "Item 3 directive ; règle d'or n°5"
    priority: "S1"
    status: "verified"
  - id: "D009"
    criterion: "Skill re-curation v1.0.0 créé, IMPLÉMENTÉ D'UN SCRIPT principal (directive complémentaire) : scripts/protocole-test.py GÉNÈRE un protocole de test adapté à l'élément ciblé, l'exécute AVANT toute re-curation (phase PRE : baseline golden master, GO/NO-GO), vérifie APRÈS le maintien de l'optimisation (phase POST : écosystème cohérent, optimisé, fonctionnel) et arbitre les méthodes candidates (--compare : la plus optimisée et performante) ; méthode P0-P7 (P0 = PRE, P7 = POST), 3 scripts selftestés, evals, cascade légère (KB + pin + historiques + ULTRA + arbitres)"
    verification: "ls skills/re-curation/SKILL.md skills/re-curation/scripts/protocole-test.py && py_compile ×3 && selftests PASS && exécution réelle PRE/POST/--compare tracée && integrity 0 FAIL"
    source: "Item 4 directive + directive complémentaire 2026-11-08 (implémentation par script ; tests avant re-curation ; maintien de l'optimisation ; comparaison de méthodes) ; pattern skill-creator ; précédent cascade légère ghorg-cmdr v1.1.0"
    priority: "S1"
    status: "verified"
  - id: "D010"
    criterion: "Skill re-curation testé $FACON : selftests + protocole de test adapté GÉNÉRÉ puis EXÉCUTÉ (phase PRE sur re-curation témoin — GO/NO-GO ; phase POST — maintien de l'optimisation vérifié) + mode VÉRIFICATION réel sur gen-plan v3.39.0 + comparaison de méthodes tracée + idempotence x2"
    verification: "rapport download/rapport-tests-recuration-task72.md — verdicts PASS tracés (PRE / POST / --compare)"
    source: "Item 5 directive ; R6"
    priority: "S1"
    status: "verified"
  - id: "D011"
    criterion: "correct-work (projet) --bloc : PASS (aggregation pire-des-verdicts, findings S1-S4, max 2 rounds)"
    verification: "verdict consigné au worklog + rapport download/rapport-correct-work-task72.md"
    source: "Item 6 directive"
    priority: "S1"
    status: "verified"
  - id: "D012"
    criterion: "clone-chat v2.0.2 : archive auto-suffisante de la session (§0-§5, décisions, artefacts, reprise, leçons)"
    verification: "fichier download/clone-chat-session-web-ecef7f80-20261108-task72.md conforme au template"
    source: "Item 7 directive"
    priority: "S2"
    status: "verified"
  - id: "D013"
    criterion: "Pendance PUSH inchangée : propriétaire uniquement, après révocation du PAT exposé ; aucun push/jeton par l'agent"
    verification: "absence de commande push distante dans les journaux + guidance révocation au rapport final"
    source: "KO-L009 points 1-2-5 (héritage Task 71)"
    priority: "S2"
    status: "verified"
  - id: "D014"
    criterion: "Ordre chronologique des tests respecté : G1 (certification gen-plan) -> G2 (adéquation) -> G3 (liste) -> G4/G5 (skill) — chaque groupe ne consomme que des artefacts déjà vérifiés"
    verification: "timestamps croissants des groupes dans le worklog"
    source: "Directive Task 71 G4 (ordre chronologique) ; règle d'or n°5"
    priority: "S2"
    status: "verified"
  - id: "D015"
    criterion: "AFFICHE-PLAN natif intégré (directive complémentaire 2, trace 1a1b7fe1c7238e8d) : la fenêtre d'affichage des étapes du plan d'actions passe par le mécanisme NATIF de l'agent dédié à ce rôle (Z.ai : liste de tâches — outil TodoWrite/TodoRead) — affichée au DÉBUT de l'exécution du plan d'actions et MISE À JOUR à chaque FIN d'étape (groupe G<k>) ; intégré dans E7-DISP point 6 « fenêtre native » (SKILL.md §1.2bis table + résumé + §5.5 cadence + intégral references/protocoles-detailles.md, nouvelle section HORS blocs R4), v3.39.0 amendée PRÉ-publication, SKILL.md reste < 30 Kio, contrats D005 intacts, preuve vivante : la présente exécution (fenêtre native affichée en début de session et mise à jour à chaque fin de groupe)"
    verification: "grep 'fenêtre native' skills/gen-plan/SKILL.md (§1.2bis + §5.5) && grep 'point 6' skills/gen-plan/references/protocoles-detailles.md && python3 scripts/task72-baseline-verifier.py --verifier (D001-D005 PASS post-amendement, taille < 30 Kio)"
    source: "Directive complémentaire 2 (2026-11-08, trace 1a1b7fe1c7238e8d) ; hook E7-DISP v3.27.0/v3.36.0 ; mécanisme natif Z.ai = liste de tâches (TodoWrite/TodoRead)"
    priority: "S1"
    status: "verified"
```

## Groupes d'exécution (chaîne step : correct-work(groupe) après chaque groupe, max 2 rounds)

### G1 — Chantier R1 : re-curation progressive disclosure de gen-plan + montée v3.39.0 + cascade KO-L004 (item 1) — #token estimé 18-25 k

- **SG1.1 Moves R4 byte-identiques** (T1.1.0 → T1.1.4) : **T1.1.0 baseline AVANT tout move** (directive complémentaire — tests avant re-curation) : capture golden master dans download/task72-baseline-genplan.json (greps contrat D005 + SHA-256 des 9 blocs + mesure poids) ; puis extraction mécanique par script (task72-extraction-genplan.py, marqueurs uniquement) des 9 blocs (§5.6 journal, §1.5 règles d'or, §1.14+§1.15 leçons, §1.6 disciplines, §1.2bis PATTERN E1-RES+E7-DISP, §1.16 routage, §5.5 mode step, §4 contingences, philosophie #4) vers 4 fichiers references/ (journal-versions.md, regles-or.md [+ leçons], disciplines-mobilisation.md, protocoles-detailles.md) + append contingences à grille-token.md (en-tête de provenance : section d'origine, version, date, SHA-256 du bloc déplacé) ; jamais de réécriture du contenu déplacé.
- **SG1.2 Résumés inline + pointeurs** (T1.2.1 → T1.2.5) : §1.5 table compacte (n° + titre + portée 1 ligne) + pointer `references/regles-or.md` (texte intégral, chargé à la demande — la canonique §1.5 reste le résumé, §0/SHARED §9 inchangés) ; §1.6 table disciplines + mécanismes 1-ligne + pointer ; §1.2bis protocoles compacts E1-RES (4 vérifications en 4 lignes — exécutées à chaque session) et E7-DISP (chaîne 5 points en 5 lignes) + pointer ; §1.16 résumé garde (commande + préemption + réparation auto) + pointer ; §5.6 entrée courante v3.39.0 seule + pointer journal + mécanique de migration ; §2.2 arbre mis à jour (4 nouveaux fichiers) ; frontmatter version 3.39.0 + description (+ mention progressive disclosure) ; §1.2bis table E5-POIDS : la lecture ciblée devient l'état par défaut du skill lui-même.
- **SG1.3 Vérifications fonctionnalité égale** (T1.3.1 → T1.3.3) : grep contrat après == baseline T1.1.0 (D005) ; vérification D003/D004 (SHA blocs == baseline, non-duplication) ; re-mesure (D002) — cible INTERMÉDIAIRE < 30 Kio.
- **SG1.3bis Amendement v3.39.0 pré-publication — fenêtre native AFFICHE-PLAN (rév. 3, directive complémentaire 2 trace 1a1b7fe1c7238e8d)** : E7-DISP point 6 « fenêtre native » — la fenêtre des étapes du plan passe par le mécanisme natif de l'agent dédié à ce rôle (Z.ai : liste de tâches `TodoWrite`/`TodoRead`) : affichée au DÉBUT de l'exécution du plan + MISE À JOUR à chaque FIN d'étape (groupe) ; canaux existants inchangés (bloc chat + marqueur worklog + garde P1-P5) ; éditions chirurgicales SKILL.md §1.2bis (table ligne E7-DISP + résumé) + §5.5 cadence + §5.6 entrée v3.39.0 (mention directive 2) + NOUVELLE section extension dans references/protocoles-detailles.md (HORS blocs déplacés R4 — byte-identité préservée) ; compensation de taille (résumés non verrouillés compactés) pour maintenir < 30 Kio ; re-vérification D001-D005 + E8 avant SG1.4 — la cascade unique porte la version consolidée.
- **SG1.4 Cascade KO-L004** (T1.4.1 → T1.4.6) : delta verrouillé v3.39.0 → génération PM (subs D006) → archive PM v3.38.0 R4 (dépôt + miroir) → pin ECO_SKILLS + KB + historiques-par-skill → ULTRA ×2 → sweep 9 skills citations + arbitres re-certifiés (integrity/coherence/vcw/cross) + sync dépôt↔hôte.

### G2 — Tests d'adéquation gen-plan ↔ écosystème (item 2) — #token estimé 4-6 k

- T2.1 Batterie arbitres (integrity 110/110, coherence 0 FAIL, vcw ALL PASS, cross 100 %) — verdicts tracés.
- T2.2 Selftests scripts gen-plan + écosystème (check_plan_protocol, poids-chargement, cache-verdicts, ensure-installed).
- T2.3 Evals non-régression : 9 evals + 15 trigger_evals (déclencheurs verbatim intacts — D005).
- T2.4 Verdict poids post-re-curation + rapport de couverture PM (WARN classe §1.13 documentés).
- T2.5 Synthèse honnèse + livrable download/rapport-adequation-genplan-task72.md.

### G3 — Analyse écosystème : liste priorisée des prochaines re-curations (item 3) — #token estimé 5-7 k

- T3.1 Re-run complet poids-chargement.py --json ×2 (idempotence) — état post-G1 (gen-plan re-curé mesuré à sa nouvelle valeur).
- T3.2 Vérification croisée mesures vs disque (échantillon 5 skills : tailles réelles vs rapport — règle d'or n°5).
- T3.3 Analyse multicritère (verdict · #token · noyau/périphérie via KB « Utilisé par » · risque) → tableau trié.
- T3.4 Cartographie sèche du candidat n°1 (sections mesurées + faisabilité + gain estimé — sans écriture, test de sûreté).
- T3.5 Livrable download/liste-recuration-priorisee-task72.md (tableau + méthodologie + preuves de test).

### G4 — Création du skill re-curation v1.0.0 (item 4 + directive complémentaire) — #token estimé 9-13 k

- T4.1 SKILL.md (frontmatter complet, méthode P0-P7 — **P0 = protocole de test adapté GÉNÉRÉ puis EXÉCUTÉ avant toute re-curation (directive complémentaire) ; P7 = vérification POST du maintien de l'optimisation : l'écosystème demeure cohérent, optimisé, fonctionnel** —, règles R4/R2/KO-L003, seuils, déclencheurs read_when).
- T4.2 **Script principal `scripts/protocole-test.py` (le skill est IMPLÉMENTÉ par ce script — directive complémentaire)** : GÉNÈRE le protocole de test adapté à l'élément ciblé (nature du skill : contrats triggers verbatim, cascade PM, evals, poids, arbitres écosystème), l'EXÉCUTE en phase PRE avant toute re-curation (baseline golden master → verdict GO/NO-GO), le ré-exécute en POST (verdict de maintien de l'optimisation : cohérent/optimisé/fonctionnel — comparaison PRE/POST), mode `--compare` (mesure des méthodes candidates → la plus optimisée et performante) + scripts/mesure-sections.py (généralisé depuis task72-mesure-sections.py, argument chemin, selftest) + scripts/check-recuration.py (arbitre : pointeurs valides, non-duplication, seuils — selftest embarqué).
- T4.3 evals/ (evals.json + trigger_evals.json).
- T4.4 Cascade légère : KB entrée + pin ECO_SKILLS + historiques-par-skill + ULTRA + arbitres + sync dépôt↔hôte.

### G5 — Tests $FACON du skill re-curation (item 5) — #token estimé 5-7 k

- T5.1 Selftests embarqués (protocole-test + mesure-sections + check-recuration) + py_compile ×3.
- T5.2 Exécution réelle du protocole de test GÉNÉRÉ par le skill : phase PRE (baseline GO/NO-GO) sur un re-curation témoin sandbox + phase POST (maintien de l'optimisation vérifié) + mode VÉRIFICATION sur gen-plan v3.39.0 (validation mécanique de la re-curation G1 par l'arbitre du nouveau skill).
- T5.3 Idempotence ×2 (re-jeu no-op) + mode --compare (gains par section mesurés, méthode la plus optimisée et performante documentée) + livrable download/rapport-tests-recuration-task72.md.

### G6 — correct-work (projet) --bloc + finalisation (item 6) — #token estimé 6-9 k

- T6.1 correct-work (projet) --bloc (Étapes 2-5, bloc par bloc G1→G5, findings S1-S4, 2 rounds max).
- T6.2 E8 final (horodatages couplés) + answer key 15/15 verified + rapport final download/rapport-final-task72.md.
- T6.3 Worklog R5 clôture + commit (message complet, arbre propre) — PUSH = propriétaire (D013).

### G7 — clone-chat (item 7) — #token estimé 2-3 k

- T7.1 Archive auto-suffisante download/clone-chat-session-web-ecef7f80-20261108-task72.md (§0-§5, décisions, artefacts, reprise, leçons).

## Estimation #token totale

~50-73 k (rév. 3 — G1 enrichi de SG1.3bis [amendement fenêtre native + re-vérifications] ; rév. 2 : G4/G5 enrichis par la directive complémentaire 1 ; tâche complexe multi-livrables, 4+ skills mobilisés : gen-plan, correct-work, clone-chat, skill-creator-pattern, knowledge-observer à E15) — grille §4 « exécution complexe 10-20 k » × coefficient multi-groupes avec cascade PM et création de skill.

## Verdict E8

**Verdict E8 : PASS (FINAL — rév. 3 exécutée intégralement : G1 ✅ re-curation gen-plan v3.39.0 [104,0→29,9 Kio, −71,2 %, CRITIQUE→INTERMÉDIAIRE rang 10] + SG1.3bis fenêtre native AFFICHE-PLAN E7-DISP point 6 + SG1.4 cascade KO-L004 complète [commit 5646e96] ; G2 ✅ adéquation PASS AVEC RÉSERVES [4 arbitres 0 FAIL, D007] ; G3 ✅ liste priorisée [7 écosystème + 2 plateforme, cartographie sèche, D008] ; G4 ✅ skill re-curation v1.0.0 IMPLÉMENTÉ de protocole-test.py [cascade légère, D009, commit d3ee6e6] ; G5 ✅ tests $FACON réels [PRE vm GO + PRE/POST gen-plan MAINTENU + VÉRIFICATION C1-C4 ×2 + --compare R4 + idempotence ×2, D010] ; G6 ✅ correct-work --bloc [verdicts par groupe G1-G5 PASS, answer-key-checker 16/16, D011] ; G7 ✅ clone-chat [archive auto-suffisante, D012] ; answer key 15/15 verified ; pendance PUSH propriétaire D013 [KO-L009] ; ordre chronologique D014 respecté. — Horodatage vérifié : 2026-11-08T23:59:00Z)**
