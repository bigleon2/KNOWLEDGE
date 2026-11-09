# Plan Task 73 — Tests fonctionnels et performances : gen-plan hôte + écosystème hôte + gen-plan miroir → correction des failles + optimisation

**Horodatage plan : 2026-11-09T01:58:00Z (final — 13/13 décisions verified)** · Mode : gen-plan(step) · Session : web-ecef7f80 · Trace directive : 1a1b853d77f65451 · Prérequis vérifié : Task 72 CLOSE (plan rév. 3 final, 15/15 verified, E8 2026-11-08T23:59:00Z)

## Contexte et périmètre

Directive propriétaire (2026-11-08, trace 1a1b853d77f65451) : « génère $FACON, effectue des tests $FACON2 fonctionnels et performances sur mon skill "gen-plan", mon écosystème hôte et sur le skill "gen-plan" du miroir dans l'objectif de corriger $FACON leurs failles et d'optimiser $FACON leur fonctionnement et leurs interactions au sein de mon écosystème. » — alias résolus (skills/@historique/@Alias/aliases.json) : **$FACON = « de façon cohérente, optimisée et fonctionnelle » · $FACON2 = « (cohérent, optimisé et fonctionnel) »**.

Trois cibles de test :
- **C1 — skill gen-plan hôte** (skills/gen-plan/, v3.39.0 re-curée Task 72, 30 668 o) ;
- **C2 — écosystème hôte** (skills/ — effectif attendu 71 dont version-management, + 4 collections @) ;
- **C3 — skill gen-plan du miroir** (KNOWLEDGE-repo/skills/gen-plan/ + ancrages dépôt : PM @mon-ecosysteme, KB, pin, historiques, ULTRA).

Objectif : campagne de tests **fonctionnels ET de performances** → **corriger les failles** → **optimiser le fonctionnement et les interactions**. Réutilisation R4 stricte des arbitres existants (check-ecosysteme-integrity.py, test-coherence-interactions.py, cache-verdicts.py, verify-cross.py, poids-chargement.py, protocole-test.py + check-recuration.py du skill re-curation, check_plan_protocol.py, generer-pm-skill.py --check) — le script de campagne ORCHESTRE ces arbitres et MESURE les durées, il ne duplique aucune logique de verdict et n'écrit aucune correction (la phase PRE capture l'état défaillant tel quel).

**État initial mesuré (E2, règle d'or n°5 — mesures réelles de session)** :
- gen-plan hôte == miroir : v3.39.0, SKILL.md 30 668 o (29,95 Kio), `diff -rq` VIDE (15 fichiers references identiques), PM v3.39.0 SHA identique deux côtés (211 054 o, 918bc692…), ULTRA SHA identique (f40ea21e…), KB « montée v3.39.0 » ×1 chaque côté, historiques v3.39.0 ×3 chaque côté ;
- **FAILLE DÉTECTÉE D'ENTRÉE (C2)** : skills/version-management/ ABSENT côté hôte (7ᵉ récidive du jour) — l'arbitre coherence signe « [FAIL] Versions KB <-> SKILL.md — version-management: répertoire absent » ; présent au miroir → restaurable par la garde Task 56 (ensure-installed.py --check → INSTALLE-REPARÉ) ;
- effectifs disque : hôte 70 skills (sans vm) · miroir 119 (dépôt complet, plateforme incluse) · hôte ⊆ miroir (0 skill en trop) · poids global : 0 CRITIQUE, 8 LOURD (vm absente du décompte), 33 intermédiaires, 29 OK ;
- écart arithmétique à élucider en T3.2 (comptages Task 72 mouvants du jour — disparitions/réparations multiples intra-journée) ;
- diagnostic cause racine HÉRITÉ (Task 56, v3.35.2) : volatilité plateforme sandbox × angle mort historique de la garde × détection tardive → récidive structurelle (9 occurrences documentées à l'époque) — la campagne le REVÉRIFIE (aucun script écosystème ne supprime skills/ [grep rmtree/rm -rf], git hôte ne suit pas skills/ [commits plateforme UUID, arbre propre]) ;
- E1-RES : aucun plan en vol (Task 72 CLOSE), ressources OK → PARALLELE ; pendance héritée : PUSH propriétaire (KO-L009).

## Answer key (hook E1) — décisions vérifiables

```yaml
decisions:
  - id: "D001"
    criterion: "Protocole de tests $FACON2 généré et outillé : download/protocole-tests-fonctionnels-performances-task73.json (par cible C1/C2/C3 : tests fonctionnels, tests de performances, critères de verdict, tolérances) produit par scripts/task73-campagne-tests.py --protocole (source unique), script d'orchestration R4 (arbitres existants, zéro duplication de logique de verdict), mesures de durées ms, agrégation pire-des-verdicts, modes --phase pre|post --cible, --selftest, AUCUNE écriture corrective en PRE"
    verification: "python3 -m py_compile scripts/task73-campagne-tests.py && python3 scripts/task73-campagne-tests.py --selftest (PASS) && python3 scripts/task73-campagne-tests.py --protocole && ls download/protocole-tests-fonctionnels-performances-task73.json"
    source: "Directive trace 1a1b853d77f65451 («génère $FACON… effectue des tests $FACON2») ; R4 jamais dupliquer ; précédent protocole-test.py Task 72"
    priority: "S1"
    status: "verified"
  - id: "D002"
    criterion: "Campagne PRE — C1 gen-plan hôte : fonctionnel (frontmatter v3.39.0, taille <= 30 Kio, 15 references + pointeurs cités, contrats verbatim [read_when, $FACON, SHARED, PATTERN:GEN-PLAN-HOOKS-PATTERNS, fenêtre native, TodoWrite], evals 9 cas + trigger_evals 15 cas, selftest check_plan_protocol 7/7, vérification re-curation C1-C4, PM --check COHERENT x4 familles) + performances (29,95 Kio, #token estimes, durees ms par test) — verdict C1 tracé dans download/rapport-campagne-task73-pre-C1.json"
    verification: "python3 scripts/task73-campagne-tests.py --phase pre --cible C1 && python3 -c \"import json; d=json.load(open('download/rapport-campagne-task73-pre-C1.json')); print(d['cible'], d['verdict'], len(d['tests']))\""
    source: "Directive (« mon skill gen-plan ») ; contrats D001-D005/D015 Task 72"
    priority: "S1"
    status: "verified"
  - id: "D003"
    criterion: "Campagne PRE — C2 écosystème hôte : arbitres integrity + coherence + vcw (mécanisme de cache) + cross + poids global (0 CRITIQUE) + effectifs disque vs miroir (hote ⊆ miroir) + entrées KB manquantes (via FAIL coherence) + sweep citations v3.38.0 — FAILLE PRE documentée : version-management absent (7ᵉ récidive, FAIL coherence) + écart arithmétique de comptage élucidé — verdict C2 tracé dans download/rapport-campagne-task73-pre-C2.json"
    verification: "python3 scripts/task73-campagne-tests.py --phase pre --cible C2 && grep -c 'version-management' download/rapport-campagne-task73-pre-C2.json"
    source: "Directive (« mon écosystème hôte ») ; échelle de verdicts des arbitres officiels"
    priority: "S1"
    status: "verified"
  - id: "D004"
    criterion: "Campagne PRE — C3 gen-plan miroir : identité byte hote<->miroir (diff -rq vide sur SKILL.md + 15 references + scripts + evals), frontmatter miroir v3.39.0, PM v3.39.0 SHA identique deux côtés, KB depôt « montée v3.39.0 », historiques v3.39.0, ULTRA SHA identique — verdict C3 tracé dans download/rapport-campagne-task73-pre-C3.json"
    verification: "python3 scripts/task73-campagne-tests.py --phase pre --cible C3 && diff -rq skills/gen-plan KNOWLEDGE-repo/skills/gen-plan (vide)"
    source: "Directive (« le skill gen-plan du miroir ») ; R4 dépôt = source, sync Task 72 SG1.4"
    priority: "S1"
    status: "verified"
  - id: "D005"
    criterion: "Failles corrigées $FACON : version-management restauré côté hote depuis le miroir (garde Task 56 : ensure-installed.py --check → verdict INSTALLE-REPARÉ, rc=0) + diagnostic de récidive formalisé (grep négatif suppressions internes [rmtree/rm -rf ciblant skills/], git hote ne suit pas skills/, conclusion cause environnementale héritée Task 56 + parade en place) + toute autre faille S1/S2 relevée en PRE corrigée avec preuve mécanique et non-régression"
    verification: "ls skills/version-management/SKILL.md && python3 skills/gen-plan/scripts/ensure-installed.py --check (rc=0) && grep 'rmtree\\|rm -rf' scripts/task73-*.py (négatif hors selftest doc)"
    source: "Directive (« corriger $FACON leurs failles ») ; garde É1-INSTALL étendue Task 56 (L54-1/L55-3)"
    priority: "S1"
    status: "verified"
  - id: "D006"
    criterion: "Campagne POST : batterie complète re-exécutée sur les 3 cibles — faille PRE résorbée vérifiée mécaniquement (coherence 0 FAIL, version-management présent) + non-régression stricte (aucun verdict dégradé vs PRE, comparaison test à test) — synthèse globale download/rapport-campagne-task73-post-synthese.json"
    verification: "python3 scripts/task73-campagne-tests.py --phase post --cible all && python3 scripts/task73-campagne-tests.py --synthese post && grep 'non_regression' download/rapport-campagne-task73-post-synthese.json"
    source: "Directive (« dans l'objectif de corriger ») ; règle d'or n°5 ; R2 non-régression"
    priority: "S1"
    status: "verified"
  - id: "D007"
    criterion: "Fonctionnement et interactions optimisés : durées PRE vs POST tracées, poids global maintenu (0 CRITIQUE, vm restaurée comptée LOURD), interactions gen-plan<->écosystème re-certifiées (KB bidirectionnelle, réciprocités « Utilisé par », sweep citations v3.39.0) + recommandations d'optimisation et leçons consignées au rapport final"
    verification: "section « Optimisation et interactions » du rapport final D008 + worklog suite correspondante"
    source: "Directive (« optimiser $FACON leur fonctionnement et leurs interactions »)"
    priority: "S1"
    status: "verified"
  - id: "D008"
    criterion: "Rapport final de campagne : download/rapport-tests-fonctionnels-performances-task73.md (méthodologie, 3 cibles x PRE/POST, failles -> corrections, verdicts, durées, leçons, recommandations, guidance PUSH)"
    verification: "ls -la download/rapport-tests-fonctionnels-performances-task73.md && grep -c 'C1\\|C2\\|C3' download/rapport-tests-fonctionnels-performances-task73.md"
    source: "Directive (objectif global) ; règle francophone durcie (règle d'or n°6)"
    priority: "S1"
    status: "verified"
  - id: "D009"
    criterion: "correct-work (projet) --bloc : PASS (agrégation pire-des-verdicts par groupe G1->G6, findings S1-S4, max 2 rounds) + answer-key-checker 13/13 ALL PASS"
    verification: "verdict consigné au worklog + re-jeu mécanique de l'answer key du présent plan"
    source: "Protocole correct-work ; précédent Task 72 G6"
    priority: "S1"
    status: "verified"
  - id: "D010"
    criterion: "E8 final : answer key 13/13 verified + horodatages croissants G1->G8 au worklog + check_plan_protocol P1-P5 PASS post-finalisation (horodatage plan == horodatage verdict)"
    verification: "python3 skills/gen-plan/scripts/check_plan_protocol.py --plan download/plan-task73-tests-fonctionnels-performances-genplan-ecosysteme-miroir.md --worklog worklog.md (VERDICT : PASS)"
    source: "Hook E7-DISP ; garde KO-L003 (verdict frais)"
    priority: "S1"
    status: "verified"
  - id: "D011"
    criterion: "clone-chat v2.0.2 : archive auto-suffisante de la session Task 73 (§0-§5, décisions, artefacts, reprise, leçons)"
    verification: "fichier download/clone-chat-session-web-ecef7f80-20261108-task73.md conforme au template"
    source: "Protocole clone-chat v2.0.2 ; précédent Task 72 G7"
    priority: "S2"
    status: "verified"
  - id: "D012"
    criterion: "Fenêtre native AFFICHE-PLAN (E7-DISP point 6, héritage D015 Task 72) : liste de tâches native (outil TodoWrite) affichée au DÉBUT de l'exécution du plan et MISE À JOUR à chaque FIN de groupe G1->G8 — preuve vivante : la présente exécution"
    verification: "fenêtre native visible dans la session (statuts G1->G8 tenus) + mentions worklog à chaque fin de groupe"
    source: "Directive complémentaire 2 Task 72 (trace 1a1b7fe1c7238e8d) intégrée à E7-DISP point 6 v3.39.0"
    priority: "S1"
    status: "verified"
  - id: "D013"
    criterion: "Pendance PUSH inchangée (KO-L009) : aucun push ni manipulation de jeton par l'agent ; PUSH = propriétaire uniquement, après révocation du PAT exposé (héritage Task 71/72)"
    verification: "absence de commande push distante dans les journaux de la session + guidance révocation au rapport final"
    source: "KO-L009 points 1-2-5 ; D013 Task 72"
    priority: "S2"
    status: "verified"
```

## Groupes d'exécution (chaîne step : correct-work(groupe) après chaque groupe, max 2 rounds)

### G1 — Protocole de tests $FACON2 + outillage + E8 initial — #token estimé 4-6 k

- **T1.1 Protocole adapté** : download/protocole-tests-fonctionnels-performances-task73.json — par cible, tests fonctionnels (structure, contrats, selftests, arbitres, sync) et de performances (poids #token, durées ms, effectifs) + critères de verdict (pire-des-verdicts, tolérances documentées : WARN B1 hérité toléré, écart v3.38.0 en sweep = WARN à adjudication manuelle).
- **T1.2 Script de campagne** : scripts/task73-campagne-tests.py — orchestration R4 des arbitres existants (aucune duplication de logique de verdict), mesures de durées par test, agrégation, modes `--phase pre|post --cible C1|C2|C3|all`, `--synthese`, `--protocole`, `--selftest` ; AUCUNE écriture corrective (la PRE capture l'état défaillant tel quel — ensure-installed n'est PAS appelé par la campagne).
- **T1.3 Validation et affichage** : py_compile + selftest + export protocole ; plan journalisé au worklog (suite 42 + marqueur PLAN-AFFICHE) ; E8 initial (check_plan_protocol P1-P5) ; **fenêtre native affichée au début de l'exécution** (E7-DISP point 6).

### G2 — Campagne PRE — C1 gen-plan hôte (fonctionnel + performances) — #token estimé 3-4 k

- T2.1 Exécution `--phase pre --cible C1` : 10 tests fonctionnels + poids.
- T2.2 Analyse des résultats, consignation worklog (suite), verdict C1.
- T2.3 correct-work(groupe G2).

### G3 — Campagne PRE — C2 écosystème hôte (fonctionnel + interactions + performances) — #token estimé 4-5 k

- T3.1 Exécution `--phase pre --cible C2` : arbitres ×4 + poids + effectifs + sweep.
- T3.2 Élucidation de l'écart arithmétique de comptage (comptages Task 72 mouvants du jour — disparitions/réparations intra-journée ; l'état mesuré PRE fait foi).
- T3.3 Consignation, verdict C2, liste des failles (dont vm 7ᵉ récidive) ; correct-work(groupe G3).

### G4 — Campagne PRE — C3 gen-plan miroir (sync + fonctionnel + performances) — #token estimé 3-4 k

- T4.1 Exécution `--phase pre --cible C3` : identité byte + ancrages dépôt (PM/KB/historiques/ULTRA).
- T4.2 Consignation, verdict C3 ; correct-work(groupe G4).

### G5 — Corrections $FACON des failles + optimisation — #token estimé 4-6 k

- T5.1 Restauration version-management (garde Task 56 : ensure-installed.py --check → INSTALLE-REPARÉ) + diagnostic de récidive formalisé (grep négatif suppressions internes, git hôte hors skills/, conclusion : cause environnementale héritée Task 56 — parade = garde auto-réparation, jugée adéquate).
- T5.2 Correction de toute autre faille S1/S2 relevée en PRE (le cas échéant) — preuve mécanique par correction, non-régression.
- T5.3 Optimisations retenues + leçons ; correct-work(groupe G5).

### G6 — Campagne POST + comparaison PRE/POST — #token estimé 3-4 k

- T6.1 Re-exécution complète `--phase post --cible all` + `--synthese post`.
- T6.2 Comparaison test à test (non-régression stricte : aucun verdict dégradé ; failles PRE résorbées) ; verdict global POST ; correct-work(groupe G6).

### G7 — correct-work --bloc + E8 final + rapport final + commit + sync — #token estimé 6-9 k

- T7.1 correct-work (projet) --bloc G1→G6 (agrégation pire-des-verdicts, findings S1-S4, 2 rounds max) + answer-key-checker 13/13.
- T7.2 Rapport final download/rapport-tests-fonctionnels-performances-task73.md + statuts verified + E8 final (horodatage frais).
- T7.3 Worklog R5 clôture + sync dépôt↔hôte (scripts/download/worklog, sans --delete [C5]) + commit — PUSH = propriétaire (D013).

### G8 — clone-chat — #token estimé 2-3 k

- T8.1 Archive auto-suffisante download/clone-chat-session-web-ecef7f80-20261108-task73.md (§0-§5, décisions, artefacts, reprise, leçons).

## Estimation #token totale

~29-41 k (G1 outillage 4-6 k · G2-G4 campagnes PRE 10-13 k · G5 corrections 4-6 k · G6 POST 3-4 k · G7 finalisation 6-9 k · G8 clone-chat 2-3 k — grille §4 « exécution complexe » x coefficient multi-groupes ; skills mobilisés : gen-plan [pilotage], re-curation [protocole-test], correct-work, clone-chat).

## Verdict E8

**Verdict E8 : PASS (FINAL — plan exécuté intégralement : G1 ✅ outillage [protocole $FACON2 + campagne R4 selftest 8/8, E8 initial P1-P5] ; G2 ✅ PRE C1 PASS 11/11 [130 ms, contrats intacts] ; G3 ✅ PRE C2 FAIL mono-racine version-management [3 tests concordants, écart arithmétique résolu] ; G4 ✅ PRE C3 PASS 7/7 [identité byte hôte↔dépôt] ; G5 ✅ corrections [vm INSTALLE-REPARÉ rc=0, cause racine environnementale, aucun script coupable] ; G6 ✅ POST [FAIL→PASS AVEC RÉSERVES, non-régression True, 3 failles résorbées] ; G7 ✅ [correct-work --bloc PASS 0 S1 · 0 S2 · 3 S3-class résorbés, answer key 12/13, rapport final, commit a790d04] ; G8 ✅ clone-chat [archive auto-suffisante, D011] ; answer key 13/13 verified [re-jeu mécanique 13/13 PASS] ; fenêtre native D012 maintenue G1→G8 ; pendance PUSH propriétaire D013 [KO-L009]. — Horodatage vérifié : 2026-11-09T01:58:00Z)**
