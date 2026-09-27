# CLONE DISCUSSION — Écosystème Knowledge, lignée B12→B13-r7 (2026-09-27)

> **Généré par** : clone-chat v2.0.0 (7+1 étapes, 8 checks) | **Session source** : B13-r7 | **Directive** : trace `1a0dffd2ae120851` — « génère un clone de l'intégralité de cette discussion via mon skill "clone-chat" » | **Pré-clone** : audit de provenance exécuté (L006 — N27, 25 artefacts documentés) ; correct-work(projet) : **PASS** (rapport `tmp/b13r5-install/rapport-correct-work-projet-b13-r7.md`).
> **Auto-suffisance** : ce fichier capture l'intégralité du contexte de la discussion — un assistant neuf peut le lire et reprendre le travail sans perte.

## §0 — Règle zéro (contexte perdu)

> Écosystème **Knowledge** : {{SKILLS_ROOT}}=`skills/` | {{KB_PATH}}=`skills/KNOWLEDGE.md` (16 entrées versionnées + 6 décisions d'architecture) | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | contenu FR, noms de fichiers/fonctions NON traduits
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.

**État au moment du clone** : gen-plan **v3.17.0** certifiée (n60b 12/12 ×2 ; certification complète **5/5 ALL PASS ×2** : verify-cross 56/56 ×2 modes, verify-correct-work 16/16, integrity 49/49, interactions 43/3/0) ; **plan courant** `download/plan-b13-r7.md` (re-généré via v3.17.0 — boucle L005 complète) ; worklog Tasks 1-45 ; journal knowledge-observer **6 leçons** (L001-L006) ; **G-RES active** (garde transversale surveillance ressources + adaptation autonome — skill resource-monitor v1.0.0, gen-plan §1.14) ; hook **E1-RES** en place (n67-1 reconstitué post-wipe : B-11 + collecte G-RES + fraîcheur du plan).

**Reprise d'une nouvelle session** : exécuter le hook E1-RES (1 : lecture seule B-11 — worklog et arbitres fait foi ; 2 : `python skills/resource-monitor/scripts/monitor.py --state-file tmp/resource-monitor/state.json` ; 3 : fraîcheur du plan — re-générer si gen-plan re-modifiée et jugée valide, règle L005), puis suivre le **bloc REPRISE** en fin de `download/plan-b13-r7.md` : N29 (ce clone) → N30 (installation selon `INSTALL-ECOSYSTEME.md`).

## §1 — Chronologie de la discussion

> Mitigation discussion longue (> 15 sessions) : sessions anciennes résumées en 1 ligne ; 5 dernières détaillées. Source de vérité : `worklog.md` (format SHARED §1.4).

### §1.2 Table chronologique

| Task | Lignée | Tâche (1 ligne) |
|------|--------|-----------------|
| 1-11 | B7 | Installation initiale de l'écosystème : création des skills fondateurs (gen-plan, correct-work, clone-chat), pipeline Z0-Z6, KB v1, certifications initiales |
| 1-4 (×4 cycles) | B8-B9 | corrige-ecosysteme Architecture v2.0 : SYNC_MAP, round-trip archive, baselines, restauration clone B9 |
| 3-a/3-b/3-d, 2-9 | B9-B10 | Réinstallation corrigée, miroir _prompts-maitres, harness disciplines, données de calibration |
| 8-explore-1 | B10 | Exploration proactive du projet (inventaire initial) |
| 21-29 | B11-B12 | Renommages semver assumés (bump majeurs), prompts maîtres assemblés (méthode B1), règles d'or, PEK v4.1, disciplines matérialisées (A11-A12) |
| 30-33 | B12-r36-r38 | correct-work(projet) passages 1-2, synthèses, automatisation cadence (R3-A17 : démons fauchés entre appels — constat expérimental) |
| 34 | B12-r39 | correct-work MODE CIBLE 3e passage (PASS, F4 corrigée en vol) |
| 35 | B12-r39 | Sonde 429 + re-arm démon best-effort (R3-A17-bis : automatisation impossible au sandbox) |
| 36 | B12-r39 | correct-work(projet) 3e passage PASS — synthèse n°31 produite (F4) |
| 37 | B12-r40 | Incident B-17 : download/ vidé + skills/ amputés → restauration N18 (clone B9 + archive + 3 contre-ordres diagnostiqués R3-C1/C2/C3) ; extraction propositions-qwen.md (agent-browser, 271 Ko, adaptation R3 §0 reconstitué) ; intégration N19 (5 patterns avancés, registre answer-key-b12 D001-D010) |
| 38 | B12-r41 | N20 montée v3.13.0 : hooks obligatoires (E1 answer key, E7/E8 arbitre 16 checks, E9-E14 Graph Diamond, E15 knowledge-observer), correct-work v2.6.0 (mode AVEUGLE), prompt-engineering v2.1.0 (M5), skill knowledge-observer v1.0.0, SHARED §8 (4 règles fondamentales), arbitre answer-key-checker 16/16, PM v3.13.0 |
| 42 | B13 | Confirmation protocole reprise (sonde R3-A11, démon actif) |
| 43 | B13-r5 | Voir §1.3 — validité gen-plan v3.16.0, re-génération du plan (règle d'or n°2), leçon L005, cycle M1-M2 |
| 44 | B13-r6 | Voir §1.3 — garde G-RES intégrée, N25 (script-creator), N26 (homologues + RÉVERDICT) |
| 45 | B13-r6/r7 | Voir §1.3 — N27 (audit-provenance + L006), N28 (v3.17.0 + boucle L005 complète + plan B13-r7) |

### §1.3 Détail des 5 dernières sessions

**Task 42 (B13)** — confirmation du protocole de reprise par le propriétaire : au QUOTA_OK → séquence r24 immédiate + validation réelle N27 (15 appels) ; 39e sonde 429 persistant ; 13e démon ré-armé. Aucune édition d'écosystème.

**Task 43 (B13-r5, directive `1a0dfe43940ae0c5`)** — validité gen-plan v3.16.0 établie mécaniquement AVANT action (n60-genplan-3160 10/10 ×2 + certification 5/5 ×3) ; plan re-généré via v3.16.0 → `download/plan-b13-r5.md` (E1-E8, registre answer-key-b13 D011-D017, checker 16/16, clé 7/7 verified) ; **règle permanente L005** (toute version de gen-plan modifiée et jugée valide déclenche la re-génération du plan) appendée au journal ; cycle M1-M2 knowledge-observer (9 observations, 5 patterns, 3 propositions M3).

**Task 44 (B13-r6, traces `1a0e00386fa15d9d`/`1a0e00502015eec1`/`1a0e00ed957ff2d1`)** — **garde transversale G-RES intégrée au plan** (révision B13-r6, R-RES1 à R-RES5 ancrées resource-monitor v1.0.0 §1.14, maintenance E13 R2, B-14 8/8) et appliquée en réel (collectes monitor.py OK/PARALLELE) ; **N25** : verdict correct-work(script-creator) mode CIBLE round 1 (PASS AVEC RÉSERVES : 1 S2 KB + 3 S3 cross-refs), test simple de bout en bout (micro-arbitre `tmp/test-script-creator/kb-entry-count.py`, idempotence ×2 sha16 db409d44…), corrections des réserves (KB 13 → 15 entrées : script-creator + script-reviewer + réciproques skill-creator/correct-work + décision N25/N26), recalibrage croisé L004 (integrity 46/46 ×2, interactions 43/3/0 ×2, verify-cross 53/53) ; **N26** : homologues archive v2.1 re-prouvés (clone épinglé `d9ff9fb`, PROVENANCE-homologues.md), correct-work(projet) reporté post-N28 (résolution de pile — directive la plus récente), RÉVERDICT Global **certification 5/5 ALL PASS ×2**.

**Task 45 (B13-r6 → r7, directives `1a0df36f356c3add`/`1a0df4d7831e4f49`)** — **N27** : skill **audit-provenance v1.0.0** matérialisé (SKILL.md §0-§4 + evals 4+7 + collecteur `scripts/audit-provenance.py`) ; adaptation R-RES3 en cascade (périmètre débordant 1057 → écosystème strict 214, ECO_SKILLS dérivé dynamiquement de integrity) ; réécriture idempotente : **25 scripts documentés** (en-tête `PROVENANCE:` syntaxe-safe, no-op au 2e passage — sha16 ded19f62… ×2, ast.parse vérifié) ; 33 orphelins résiduels assumés v1.0.0 ; **leçon L006** (journal 6 leçons, statut appliqué, occurrences 3) ; KB 16 entrées + réciproques + décision N27 ; certification 5/5 ×2 (verify-cross 56/56). **N28** : montée **gen-plan v3.17.0** (§1.5 bloc PATTERN:KO-L005-v1.0.0 ; §1.2bis hook **E1-RES** — n67-1 reconstitué post-wipe, provenance tracée sans faux lignage) ; arbitre **n60b 12/12 ALL PASS ×2** ; **PM v3.17.0 assemblé 1348 → 1362 L déployé ×3** (méthode B1, `scripts/n28-assemble-pm-gen-plan-3170.py`) ; corpus **20 fichiers** (archive 30) ; SYNC_MAP +v3.17.0 ; CORPUS_ATTENDU = 20 (invariant dérivé L003) ; KB gen-plan v3.17.0 ; **boucle L005 complète exécutée** → plan `download/plan-b13-r7.md` (E8 16/16) ; convergences : conventions langage + correct-py constatées, provenance script-creator/correct-work tracée.

## §2 — Écosystème de skills (fichiers, scripts, artefacts)

### §2.1 Skills écosystème ({{KB_ENABLED}}=true — descriptions du registre KB)

| Skill | Version | Rôle |
|-------|---------|------|
| gen-plan | 3.17.0 | Planification : 4 modes, 15 étapes E1-E15, règles d'or §1.5 (+ KO-L005), PEK v4.1, hooks §1.2bis (answer key E1, arbitre E7/E8, Graph Diamond E9-E14, Observer E15), hook E1-RES (n67-1), leçons KO §1.14/§1.15 |
| correct-work | 2.6.0 | Vérification/correction des livrables — 4 modes (PROJET/CIBLE/DIRECT/AVEUGLE), 5 étapes, checklists §10, hook 2nd opinion |
| clone-chat | 2.0.0 | Clonage de discussion en Markdown auto-suffisant (7+1 étapes, 8 checks) — produit ce fichier |
| skills-inventory | 1.0.0 | Scan et rapport d'inventaire des skills |
| skill-creator | 1.0.0 | Création/gestion de skills (conventions structurelles, schéma d'evals) |
| agent-creator | 2.0.0 | Agent autonome à mémoire interne (tâches longues) |
| script-creator | 1.0.0 | Création/modification des scripts écosystème — §1.2 en 7 étapes, 6 garde-fous (R9, N3, idempotence ×2, P2, correct-work CIBLE, correct-py GF-6) |
| script-reviewer | 1.0.0 | Relecture/validation des scripts — grille G1-G8, sévérités S1-S4 |
| audit-provenance | 1.0.0 | Audit de provenance des artefacts (lignage wipes/restaurations), réécriture idempotente — matérialise L006 |
| prompt-engineering | 2.1.0 | Optimisation fine des prompts (M1-M5 dont IDÉATION) — spécialise la méthode (SHARED §7) |
| context-engineering | 1.1.0 | Curation de contexte, compaction, budget d'attention |
| loop-engineering | 1.0.1 | Boucle d'exécution + boucle de vérification (graders) |
| graph-engineering | 1.0.1 | Graphe de connaissances, relations bidirectionnelles versionnées |
| harness-engineering | 1.0.1 | Harnais d'exécution, gardes-fous, profils ressource |
| script-mon-ecosysteme-infrastructure | 1.1.0 | Infrastructure de génération de fichiers (règles INFRA-1..3) |
| knowledge-observer | 1.0.0 | Observation automatique des sessions (cycle A-H, modes M1-M4), journal lessons-learned — hook E15 |

### §2.2 Skills métier (hors registre écosystème)

audio-metadata 1.0.0 | cpp-analysis | pdf-llm — + skills plateforme tiers (exclus du périmètre écosystème : ASR, LLM, TTS, VLM, charts, docx, xlsx, pdf, pptx, web-search…).

### §2.3 Scripts et arbitres (`scripts/`)

| Script | Rôle | Verdict au clone |
|--------|------|------------------|
| `certification-complete.py` | Certification consolidée 5/5 (verify-cross ×2 modes, verify-correct-work, integrity, interactions) | **5/5 ALL PASS ×2** |
| `verify-cross.py` | Cross-references dynamiques (56 checks) | 56/56 ×2 modes |
| `verify-correct-work.py` | 16 checks correct-work (EXPECTED 2.6.0) | 16/16 |
| `check-ecosysteme-integrity.py` | 49 checks : corpus 20 (SHA), round-trip archive v2.1, SYNC_MAP 11, ECO_SKILLS 16, KB 16 entrées | 49/49 ×2 |
| `test-coherence-interactions.py` | 46 checks (round-trip v2.1, bidirectionnalité KB, contracts semver, compilation) | 43 PASS/3 WARN/0 FAIL |
| `answer-key-checker.py` | 16 checks registre answer key | 16/16 ×2 |
| `n60b-genplan-3170.py` | 12 checks non-régression gen-plan v3.17.0 (adaptation L004 de n60-genplan-3160.py conservé) | 12/12 ×2 |
| `audit-provenance.py` | Collecteur audit de provenance (heuristique déclarative, --fix idempotent, écosystème strict) | 214 scannés / 189 tracés / 25 fixés |
| `n28-assemble-pm-gen-plan-3170.py` | Assemblage PM v3.17.0 (méthode B1, base v3.16.0 R2) | 1362 L, ×3 déployé |
| `monitor.py` (skills/resource-monitor) | Collecte G-RES F1-F4 → verdict OK/PRESSION/CRITIQUE + mode | OK/PARALLELE ×4 |
| `kb-entry-count.py` (tmp/test-script-creator) | Micro-arbitre de test N25-b (script-creator §1.2) | idempotence ×2 prouvée |
| `n22b-append-l005.py`, `n27-append-l006.py` | Appends idempotents leçons au journal | APPEND + NO-OP |
| `sync-download.py`, `restore-miroir.py`, `propagate-context.py` | Canal download/ + miroir + propagation (en-têtes PROVENANCE ajoutés N27) | PASS (integrity check 3) |

### §2.4 Historique des interactions (KB — relations bidirectionnelles)

- gen-plan → correct-work (hooks E9-E14), knowledge-observer (E15), clone-chat (E4/E15), skills-inventory (E5), prompt-engineering + 4 disciplines (§1.6), resource-monitor (E1-RES/E6/§1.14)
- correct-work ← gen-plan, clone-chat, knowledge-observer, script-creator (GF-5), script-reviewer (S1-S4), audit-provenance (GF-4)
- script-creator ↔ script-reviewer (création/relecture) ; audit-provenance → knowledge-observer (L006), script-creator (conventions)
- skill-creator ← clone-chat, prompt-engineering, script-mon-ecosysteme-infrastructure, knowledge-observer, script-creator, script-reviewer
- Agent-creator : gen-plan + clone-chat (persistance) ; agent-creator ∥ famille script-creator (homologue)

### §2.5 Artefacts produits (download/, corpus, tmp)

| Artefact | Taille | Rôle |
|----------|--------|------|
| `download/plan-b13-r7.md` | 101 L | **PLAN COURANT** (re-généré via v3.17.0) — E1-E8 + bloc REPRISE (N29 → N30) |
| `download/plan-b13-r5.md` | 135 L | Plan B13-r6 historisé (N22-N28 avec statuts ✅ détaillés) |
| `download/mon-ecosysteme_archive.zip` | 30 fichiers | Véhicule d'intégrité v2.1 : 20 corpus + 10 homologues (clone épinglé `d9ff9fb`) + PROVENANCE-homologues.md |
| `download/PROMPT-MAITRE-GEN-PLAN-v3.17.0.md` (+ v3.6.1→v3.16.0, v3.12/v3.13) | 1362 L | PM courant + historique versions — ×3 (corpus, miroir, download) |
| `download/INSTALL-ECOSYSTEME.md` + `PROMPT-MAITRE-INSTALL-ECOSYSTEME.md` | ~14 Ko | Protocoles d'installation (N30) |
| `download/propositions-qwen.md` | 25 260 o | Patterns avancés Qwen (source N19/N20) |
| `download/synthese-b12-r39.md`, rapports correct-work B12 | ~15 Ko | Historique vérifications B12 |
| `skills/@mon-ecosysteme/` | 20 fichiers | Corpus canonique (PM ×10 versions, SHARED, INSTALL, README, SYNC-CONTEXT) |
| `tmp/b13r5-install/` | ~9 fichiers | answer-key-b13.md (D011-D017), rapports (n60, n60b, correct-work script-creator + projet, M1-M2, audit-provenance ×3) |
| `tmp/resource-monitor/state.json`, `tmp/test-script-creator/` | < 1 Ko | État G-RES + micro-arbitre de test |
| `worklog.md` | 1171 L | Source de vérité — 68 entrées Task (Tasks 1-45, lignées B7→B13-r7) |

### §2.6 Spécifications techniques des fichiers principaux

**gen-plan/SKILL.md (~470 L — résumé structuré, > 500 lignes seuil ajusté)** : frontmatter (name/version 3.17.0/deps [correct-work, clone-chat, skills-inventory, prompt-engineering, 4 disciplines, knowledge-observer]) ; §1.2 15 étapes E1-E15 (table mode × étape) ; §1.2bis hooks patterns avancés (4 hooks + bloc E1-RES) ; §1.3 normes N1-N3 ; §1.4 philosophie clés 1-8 ; §1.5 règles d'or n°1-3 + bloc KO-L005 ; §1.6 disciplines (table mobilisation E1-E8, PEK v4.1) ; §1.7 pipeline Z0-Z6 ; §1.8 idempotence R1-R6 ; §1.14/§1.15 leçons KO-L001/L003/L004 (blocs PATTERN) ; §2 stack ; §3 relations.

**KNOWLEDGE.md (~175 L — in extenso condensé)** : 16 entrées versionnées format SHARED §2.2 (Category/Description/Dépend de/Utilisé par/Dernière calibration/Note/Statut) + section « Décisions d'architecture » (G9, G8, N19, N20, N25/N26, N27).

**Plan B13-r7 (101 L — in extenso référencé)** : voir le fichier lui-même (auto-portant) — hook E1-RES appliqué, E1 objets (a)-(d) avec D018, E2 inventaire, E4 estimations N29/N30, E7 phases N29 (clone) / N30 (installation), E8 validation, bloc REPRISE.

**Journal lessons-learned.json (6 leçons)** : L001 (429 économie API, 29 occ, appliqué) ; L002 (snapshot avant montage, 2 occ, proposé) ; L003 (arbitres à invariants dynamiques, 3 occ, appliqué) ; L004 (recalibrage croisé, 2 occ, appliqué) ; L005 (re-génération du plan, 2 occ, **validé** — matérialisée v3.17.0) ; L006 (provenance des artefacts, 3 occ, **appliqué** — audit-provenance).

## §3 — Décisions clés

### §3.1 Décisions de l'utilisateur (avec contexte et conséquences)

| # | Décision | Contexte | Conséquence | Trace |
|---|----------|----------|-------------|-------|
| D-1 | Objectif maître : RECONSTRUIRE puis INSTALLER la dernière version de l'écosystème (générée avant la perte de mémoire) ; ordre : construction → correct-work(projet) → clone-chat → installation ; repli : relecture bloc par bloc | Perte de mémoire inter-sessions (wipe) | Lignée B13-r1→r7 ; objectif intangible (R-RES5) | `1a0dffd2ae120851` |
| D-2 | Validité des versions exigée par arbitres AVANT toute action (jamais la présomption) | Directive v3.16.0 (Task 43) | Leçon L003 institutionnalisée ; n60/n60b avant toute montée | `1a0dfe43940ae0c5` |
| D-3 | Règle permanente : re-générer le plan à chaque version de gen-plan modifiée et jugée valide | Directive Task 43 → leçon L005 | Boucle L005 exécutée intégralement (v3.17.0 → plan B13-r7) | `1a0dfe43940ae0c5` |
| D-4 | Pile N25→N26→N27→N28 (durcissement script-creator, homologues + RÉVERDICT ×2, audit de provenance, convergences) | Directives N25-N28 | Toutes exécutées (Tasks 44-45) | `1a0def365a639149`, `1a0df0297431ea3d`, `1a0df36f356c3add`, `1a0df4d7831e4f49` |
| D-5 | Garde de surveillance des ressources + adaptation autonome intégrée au plan (mise à jour optimisée via gen-plan si nécessaire) | Demande G-RES | G-RES R-RES1 à R-RES5 (plan B13-r6), ancrée resource-monitor v1.0.0 §1.14 ; appliquée en réel | `1a0e00ed957ff2d1` |
| D-6 | Gen-plan v3.16.0 fonctionnel → régénérer le plan (B13-r5) ; idem à chaque version valide | Directive Task 43 | 1re application de la règle L005 | `1a0dfe43940ae0c5` |
| D-7 | Décisions E1 vérifiables (answer key) : D011-D017 (b13) puis D018 (boucle L005 exécutée) | Hook E1 obligatoire (v3.13.0) | 7/7 puis 8/8 verified — checker 16/16 ×2 | registres tmp/b13r5-install/answer-key-b13.md |

### §3.2 Bugs corrigés (cause → fix → résultat)

| Bug | Cause racine | Fix | Résultat |
|-----|--------------|-----|----------|
| 429 persistant ~16 h (B12) | Quota API épuisé | Sonde 1/message (R3-A11), travail local, armement à QUOTA_OK (L001) | Session poursuivie sans coût API superflu |
| Incident B-17 : download/ vidé + skills/ amputés (B12-r40) | Wipe destructeur | Restauration N18 (clone B9 + archive + 3 contre-ordres diagnostiqués R3-C1/C2/C3) | Certification 5/5, SHA restabilisée |
| Wipe inter-sessions (B13) | Perte de mémoire de session | Reconstitution T1-T4 post-wipe (PM v3.16.0 assemblé 1348 L ×3, L001-L004 restituées) — provenances tracées « reconstitué post-wipe » | Écosystème restauré certifié |
| Bijection stricte integrity bloque les homologues (B13-r6) | Check 2 codé `n_ident == corpus == znames` | Recalibrage v2.1 : corpus ⊆ archive + extras sous `homologues/` (L004) | 42/42 → 49/49 PASS |
| FAIL interactions ok6 (corpus 19 codé) après corpus 20 (B13-r7) | Invariant figé (violation L003) | ok6 recalibré `== 20` + CORPUS_ATTENDU canonique lu par regex | 43/3/0 PASS ×2 |
| Périmètre audit-provenance débordant (1057 artefacts, 796 faux orphelins) | collect_paths scannait les skills plateforme tiers | Adaptation R-RES3 (cascade (a)) : périmètre écosystème strict, ECO_SKILLS dérivé dynamiquement | 214 scannés / 58 orphelins réels |
| n67-1 perdu au wipe (hook E1 absent) | Wipe inter-sessions | Reconstitution tracée « reconstitué post-wipe » (bloc GEN-PLAN-HOOKS-E1-RES-v1.0.0, v3.17.0) | Hook E1-RES opérationnel, aucun faux lignage |
| Asymétries cross-refs famille script (S3 ×3) | Réciproques non déclarées | KB bidirectionnelle complétée + §3 script-creator + réciproque correct-work | Vérifications PASS (round 2 CIBLE) |

### §3.3 Conventions établies (règle + exemple)

1. **Idempotence ×2** (D017) : toute écriture est rejouée à l'identique — ex. kb-entry-count sha16 `db409d44…` ×2, fix audit-provenance no-op au 2e passage (sha16 `ded19f62…`).
2. **Arbitres AVANT action** (L003) : jamais de montée de version sans verdict mécanique préalable — ex. n60b 12/12 ×2 avant la boucle L005.
3. **Recalibrage croisé AVANT certification** (L004) : toute écriture déclenche la mise à jour des arbitres dépendants — ex. KB 15 → integrity + interactions recalibrés puis certification.
4. **Additivité R2** : ne jamais réécrire destructivement — historiques conservés (plans B13-r5/r6, PM par version, n60 conservé).
5. **Worklog source de vérité** (R3) : chaque Task appendée, format SHARED §1.4 — ex. constats d'honnêteté (travail interrompu N26 sans append : détecté, re-prouvé, tracé Task 44).
6. **Persistance avant exécution** (R9) : scripts > 10 L écrits sous `scripts/` avant exécution — ex. n27-append-l006.py, n28-assemble-pm-gen-plan-3170.py.
7. **Contenu FR, identifiants non traduits** : docstrings/messages FR, noms de fichiers/fonctions conservés.
8. **Correct-py post-traitement** (GF-6 script-creator) : PEP 8/257 contrôlés à chaque script produit.

### §3.4 Données de calibration

- Grille #token (plan B13-r7) : N29 clone 12 000, N30 installation 10 000, maintenance 500/tour.
- Lignage SHA : dac07388… (B12 stable ×1226) → 4a2a43f6… → 4317a0f4… → f62359f6… ×1238 (B12-r41) → lignée B13 (post-wipe, snapshot 43 Mo) — constaté par arbitres.
- Volumétrie : PM v3.17.0 = 1362 L (plage arbitre 1200-1400) ; corpus 20 fichiers ; archive 30 ; KB 16 entrées + 6 décisions ; journal 6 leçons ; worklog 1171 L / 68 Tasks.
- Verdicts de référence : certification 5/5 ×6 passages sur B13-r6/r7 ; n60b 12/12 ×3 ; checker 16/16 ×3.

## §3.5 — Évolutions de contexte (Context Drift)

| # | Type | Avant | Après | Session | Ligne worklog | Raison |
|---|------|-------|-------|---------|---------------|--------|
| 1 | MODIFICATION | correct-work(projet) armé en N26.3 (directive `1a0df0297431ea3d`) | REPORTÉ post-N28 (après construction complète) | B13-r6 | Task 44 | Directive la plus récente `1a0dffd2ae120851` fait foi (résolution de pile) |
| 2 | ENRICHISSEMENT | Plan sans garde de ressources | Garde transversale G-RES (R-RES1 à R-RES5) intégrée (B13-r6) | B13-r6 | Task 44 | Demande propriétaire `1a0e00ed957ff2d1` |
| 3 | ENRICHISSEMENT | N23-b et N28 en deux cycles de version | FUSIONNÉES en un seul cycle v3.17.0 | B13-r6 | Task 44 (plan) | Optimisation G-RES-R4 — éviter deux re-certifications |
| 4 | CORRECTION | integrity check 2 bijection stricte (19==zip) | v2.1 : corpus ⊆ archive + extras sous homologues/ | B13-r5/r6 | Task 44 | Ajout des homologues `d9ff9fb` (N26) |
| 5 | RECALIBRAGE | integrity 42 checks/13 entrées/corpus 19 | 49 checks/16 entrées/corpus 20 ; verify-cross 47→56 | B13-r6/r7 | Tasks 44-45 | Ajouts KB (script-creator, script-reviewer, audit-provenance) + corpus 20 (PM v3.17.0) |
| 6 | CORRECTION | Périmètre audit 1057 artefacts (796 faux orphelins) | Périmètre écosystème strict 214 artefacts | B13-r6 | Task 45 | Adaptation R-RES3 en cascade — spec §1.2 déborder par le code |

## §4 — Instructions d'utilisation (reprise d'une nouvelle session)

1. **Hook E1-RES obligatoire** (n67-1 — PATTERN:GEN-PLAN-HOOKS-E1-RES-v1.0.0) : (1) lecture seule B-11 de `worklog.md` (fin = Tasks 43-45, fait foi) ; (2) `python skills/resource-monitor/scripts/monitor.py --state-file tmp/resource-monitor/state.json` → verdict → mode ; (3) fraîcheur du plan : si gen-plan re-modifiée et jugée valide (arbitres) → boucle L005 (re-certification + re-génération du plan via la nouvelle version).
2. **Plan courant** : `download/plan-b13-r7.md` — lire le bloc REPRISE en fin (ordre N29 → N30).
3. **Fichiers prioritaires** : `download/plan-b13-r7.md` (101 L) → `skills/KNOWLEDGE.md` (registre) → `skills/gen-plan/SKILL.md` §1.5/§1.2bis → `worklog.md` (fin) → `skills/correct-work/SKILL.md` §10.
4. **Arbitres à exécuter avant toute écriture** : `python scripts/certification-complete.py` (5/5 attendu) ; après écriture : ×2 + arbitres ciblés (L004).
5. **G-RES en continu** : collecte à l'ouverture/fermeture de chaque phase et à chaque signal (R-RES1) ; adaptation en cascade au blocage (R-RES3 : contourner → simplifier → décomposer → checkpoint) ; objectif final intangible (R-RES5).
6. **N30 installation** : suivre `download/INSTALL-ECOSYSTEME.md` — préalables : collecte G-RES + snapshot de sécurité (L002) + audit de provenance (L006) ; postérieurs : integrity ×2 + certification ×2 + audit post-installation.
7. **Conventions d'écriture** : FR pour les contenus, noms non traduits ; idempotence ×2 sur chaque écriture ; worklog à chaque Task (R3).

## §5 — Auto-clonage

- **Mécanisme** : à chaque nouvelle session significative, (a) ENRICHIR §1 (nouvelle ligne Task + détail si parmi les 5 dernières), §2 (artefacts nouveaux/modifiés), §3 (décisions, bugs, conventions, calibration) et §3.5 (drifts) ; (b) RÉGÉNÉRER §0 (état courant), §4 (instructions à jour), §5 (ce paragraphe).
- **Outil** : exécuter `skills/clone-chat/` v2.0.0 (7+1 étapes, 8 checks — auto-suffisance, complétude worklog/skills/décisions/bugs/drifts, exécutabilité, auto-clonage) ; sauvegarde `download/` avec nom descriptif daté.
- **Cible suivante** : après N30 (installation), régénérer ce clone avec l'état post-installation (ECO_SKILLS 16 installés + preuves ×2).
- **Références** : gen-plan v3.17.0 (règle L005), correct-work v2.6.0 (verdicts), knowledge-observer (journal L001-L006), audit-provenance v1.0.0 (pré-clone — L006 : l'audit de provenance est exécuté AVANT tout clone).

