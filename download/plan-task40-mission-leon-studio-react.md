# PLAN D'ACTIONS — Task 40 : Mission gen-plan(step) « Réinstallation PM-INSTALL + LEON TSI EDITEUR ↔ dépôt GitHub + Extension React studio v11 + PUSH »

> **Mode** : gen-plan(step) — enchaînement autonome des groupes séquentiels, correct-work(groupe, mode=CIBLE) aux barrières du diamant (max 2 rounds), correct-work(projet) aux jalons G5/G8 (v3.32.0/v2.8.0).
> **Session** : web-6058b3ba · **gen-plan** : v3.32.0 (parallélisation par défaut des tâches ET commandes) · **Date** : 2026-11-02
> **Pré-acquis phase A** : réinstallation PM-INSTALL TERMINÉE (clone certifié `fddbe94` = origin/main ; MODE CLONE 11 étapes + garde R2 v3.32.0 bundle + pilier restauré archive v2.3 + 2 correctifs N1 syntaxe + doublon README résorbé ; certification 5/6, N2 résorbé par le présent plan).
> **Routage normatif N2 (arbitre check-tool-routing)** — skills dédiés cités par type d'artefact touché : **skill** → skill-creator (aucune modification de skill prévue — garde KO-L009 skills inchangés sauf cascade) ; **agent/PM** → agent-creator (corpus PM @mon-ecosysteme : montée v3.32.0 déjà produite Task 38, intégration dépôt ici) ; **script** → script-creator (scripts de test/performance $FACON2, scripts d'extraction discussion) ; **infrastructure** → script-mon-ecosysteme-infrastructure (déploiement des livrables dans l'arbre du dépôt, conventions INFRA-1..3).
Horodatage plan : 2026-11-02T22:10:00+01:00

## Answer key (E1) — forme exécutable

```yaml
decisions:
  - id: "D001"
    criterion: "Discussion b6170b8b « LEON TSI EDITEUR » analysée à nouveau — extraction complète persistée (3e voie agent-browser SUCCÈS après WAF ; journal des voies consigné)"
    verification: "test -s work/disc-b6170b8b/discussion-complete.txt && grep -c 'LEON TSI EDITEUR' work/disc-b6170b8b/discussion-complete.txt >= 1"
    source: "Directive « analyse à nouveau la discussion » + contingence v3.28.2 (voies 1-2 bloquées : WebFetch 0 ligne, API curl 403 ; voie 3 agent-browser RENDUE)"
    priority: "S1"
    status: "pending"
  - id: "D002"
    criterion: "Rapport d'analyse de la discussion produit — éléments générés inventoriés (app fullstack, catalogue 388 commandes, contrôles 125 in/220 out, scripts, correctifs, itérations 1-3)"
    verification: "test -s download/rapport-analyse-discussion-b6170b8b.md && grep -c 'Modes & Modules' download/rapport-analyse-discussion-b6170b8b.md >= 1"
    source: "Directive + extraction agent-browser (715+ fragments, 8 positions de scroll)"
    priority: "S1"
    status: "pending"
  - id: "D003"
    criterion: "Comparaison mécanique éléments-discussion ↔ dépôt GitHub (clone fddbe94) — tableau de couverture élément par élément, constat 0/N présent"
    verification: "test -s download/rapport-comparaison-discussion-depot.md && grep -c 'ABSENT' download/rapport-comparaison-discussion-depot.md >= 1"
    source: "Directive « comparer les éléments générés dans cette discussion avec ceux qui existent déjà dans mon dépôt GITHUB »"
    priority: "S1"
    status: "pending"
  - id: "D004"
    criterion: "Tests $FACON $FACON2 de performances exécutés sur les éléments comparables des deux côtés (arbitres dépôt : tsi-validator/analyse-doc-s4mk2 sur fixtures DREW+DJTT ; toolkit Task 39 : suite 20/20 + timings ; harnais discussion documenté) — verdicts + timings consignés"
    verification: "grep -c 'PERF\\|ms' download/rapport-comparaison-discussion-depot.md >= 3"
    source: "Directive « effectue $FACON des tests $FACON2 de performances »"
    priority: "S1"
    status: "pending"
  - id: "D005"
    criterion: "Fixtures DREW réimportées (ZIP uploadé 6 membres, sha256 08d46db8…) — batterie analyse-doc-s4mk2 re-certifiée sur fixtures réelles (pendance Task 39 n°4 résorbée)"
    verification: "test -d work/drew-fixtures && ls work/drew-fixtures/*.tsi >/dev/null 2>&1 && echo OK"
    source: "Upload propriétaire « Kontrol S4 [DREW's MAPPING].zip » + pendance Task 39"
    priority: "S1"
    status: "pending"
  - id: "D006"
    criterion: "Versions cohérentes/optimisées/fonctionnelles générées pour chaque différence — (a) livrables Task 39 intégrés au dépôt (tsi-toolkit, tsi-agent.md, construire-zip-tsi.py, bibliotheque-skills-ia, data/commandes-traktor.json, architecture studio v11) ; (b) corpus gen-plan v3.32.0 intégré (PM + SKILL.md + pin KB + historique) ; (c) catalogue commandes réconcilié (discussion 388 ↔ toolkit 393) ; (d) app LEON (voir D007)"
    verification: "test -d work/knowledge-clone-fddbe94/tsi-toolkit && test -f work/knowledge-clone-fddbe94/skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.32.0.md && echo OK"
    source: "Directive « s'il y a des différences alors toujours générer $FACON une version la plus cohérente, optimisée et fonctionnelle possible » + règle R4 (réutilisation toolchain, jamais duplication)"
    priority: "S1"
    status: "pending"
  - id: "D007"
    criterion: "Extension React du studio v11 = LEON TSI EDITEUR v11 régénéré $FACON dans l'app Next.js du dépôt — vues Contrôleur (In/Modules/LED), Web MIDI (handlePortMessage), catalogue scellé, API projets, mass-edit, préservation correctifs itération 3, consommation du studio v11 (presets/DSL/audit) comme moteur"
    verification: "test -f work/knowledge-clone-fddbe94/src/components/leon/controller-view.tsx && test -f work/knowledge-clone-fddbe94/src/lib/tsi/format.ts && echo OK"
    source: "Directive « Extension React du studio v11 » + architecture-mapping-studio-v11.md §Extension React + discussion b6170b8b (itérations 1-3)"
    priority: "S1"
    status: "pending"
  - id: "D008"
    criterion: "Batterie tests $FACON $FACON2 fonctionnels + performances exécutée sur l'ensemble (app : idempotence/API/ESLint/tsc/navigateur ; toolkit : 20/20 ; arbitres : integrity/verify-cross/valider-tsi DREW+DJTT ; DREW : batterie 16/16) avec timings"
    verification: "test -s download/rapport-tests-task40.md && grep -c 'PASS' download/rapport-tests-task40.md >= 10"
    source: "Directive « effectue $FACON la batterie de tests $FACON2 fonctionnels et de performances »"
    priority: "S1"
    status: "pending"
  - id: "D009"
    criterion: "Correctifs les plus appropriés appliqués aux échecs/réserves des tests (max 2 rounds par cible, re-test après chaque correctif)"
    verification: "grep -c 'correctif\\|CORRECTIF' download/rapport-tests-task40.md >= 1 || echo AUCUN_BESOIN"
    source: "Directive « puis fais les correctifs les plus appropriés »"
    priority: "S1"
    status: "pending"
  - id: "D010"
    criterion: "correct-work(groupe) aux barrières G2/G4/G7 + correct-work(projet) aux jalons G5/G8 — verdicts consignés worklog"
    verification: "grep -c 'Task 40' worklog.md >= 8"
    source: "Directive (5 occurrences correct-work) + protocole diamant"
    priority: "S1"
    status: "pending"
  - id: "D011"
    criterion: "Tous les correctifs exécutés (résidus des correct-work et des tests — boucle jusqu'à résorption ou qualification honnête)"
    verification: "grep -c 'résidu\\|RÉSIDU' download/rapport-final-task40.md >= 0 && test -s download/rapport-final-task40.md"
    source: "Directive « effectue tous les correctifs »"
    priority: "S1"
    status: "pending"
  - id: "D012"
    criterion: "PUSH exécuté sur directive propriétaire explicite (délégation KO-L009 point 5) — commits pathspec, contrôles pré-push 4/4 (divergence fast-forward, commits certifiés, volumétrie, scan secrets 0 github_pat_), PAT en usage transitoire unique jamais persisté"
    verification: "git -C work/knowledge-clone-fddbe94 ls-remote origin main == HEAD local && echo PUSHED"
    source: "Directive « PUSH avec ma clé … » + gouvernance Task 37 (même procédure)"
    priority: "S1"
    status: "pending"
  - id: "D013"
    criterion: "Rotation du PAT guidance réitérée (3e exposition canal — consignée sans la valeur du secret)"
    verification: "grep -c 'rotation' worklog.md >= 1 (entrée Task 40)"
    source: "KO-L009 sécurité + consignations Tasks 32/37"
    priority: "S2"
    status: "pending"
  - id: "D014"
    criterion: "Worklog alimenté par groupe + plan persisté + marqueur PLAN-AFFICHE (garde C5)"
    verification: "grep -c 'PLAN-AFFICHE' worklog.md >= 1 && test -s download/plan-task40-mission-leon-studio-react.md"
    source: "Garde-plan-genplan C1-C5 + KO-L003"
    priority: "S1"
    status: "pending"
  - id: "D015"
    criterion: "Aucune rétrogradation (R2) : skills hôte inchangés vs état certifié v3.32.0 ; intégration dépôt = additions + montée v3.32.0 uniquement"
    verification: "python3 scripts/check-ecosysteme-integrity.py --check 2>&1 | tail -1 | grep -q '0 FAIL' && echo OK"
    source: "Garde R2 + KO-L004"
    priority: "S1"
    status: "pending"
  - id: "D016"
    criterion: "Parallélisation par défaut v3.32.0 — vagues parallèles tracées au worklog avec preuve d'indépendance (SG indépendants, un seul message multi-outils par vague)"
    verification: "grep -c 'PARALLELE\\|∥' worklog.md >= 2 (entrées Task 40)"
    source: "Philosophie #4 v3.32.0 + profilage E6 (OK/PARALLELE)"
    priority: "S1"
    status: "pending"
```

### Lecture rapide

| # | Résumé | Prio |
|---|---|---|
| D001 | Discussion b6170b8b extraite (agent-browser, 3e voie) | S1 |
| D002 | Rapport d'analyse discussion | S1 |
| D003 | Comparaison mécanique discussion ↔ dépôt | S1 |
| D004 | Tests $FACON $FACON2 de performances comparatifs | S1 |
| D005 | Fixtures DREW réimportées + re-certification | S1 |
| D006 | Versions cohérentes des différences (toolkit, v3.32.0, catalogue) | S1 |
| D007 | Extension React studio v11 = LEON TSI EDITEUR régénéré | S1 |
| D008 | Batterie tests fonctionnels + performances | S1 |
| D009 | Correctifs appropriés (max 2 rounds/cible) | S1 |
| D010 | correct-work ×5 (3 groupe + 2 projet) | S1 |
| D011 | Tous les correctifs | S1 |
| D012 | PUSH délégué (contrôles 4/4, PAT transitoire) | S1 |
| D013 | Guidance rotation PAT (3e exposition) | S2 |
| D014 | Worklog + PLAN-AFFICHE | S1 |
| D015 | Garde R2 (aucune rétrogradation) | S1 |
| D016 | Parallélisation par défaut tracée | S1 |

## Vue d'ensemble (ouvre la chaîne — §5.5)

| Groupe | Contenu | correct-work | Statut |
|---|---|---|---|
| **G1** | Analyse discussion b6170b8b + comparaison dépôt + tests perf + fixtures DREW | (groupe) à l'issue de G2 | 0/3 SG |
| **G2** | Génération $FACON des versions cohérentes (toolkit + v3.32.0 + catalogue) | **(groupe) barrière directive n°3** | 0/2 SG |
| **G3** | Extension React du studio v11 — LEON TSI EDITEUR (fullstack-dev) | **(groupe) barrière directive n°5** | 0/3 SG |
| **G4** | Batterie tests $FACON $FACON2 + correctifs appropriés | (dans le groupe) | 0/2 SG |
| **G5** | correct-work (projet) — jalon post-tests | **(projet) directive n°7** | 0/1 SG |
| **G6** | Tous les correctifs (résidus) | **(groupe) barrière directive n°9** | 0/1 SG |
| **G7** | PUSH (commits pathspec + PAT transitoire + contrôles 4/4) | — | 0/1 SG |
| **G8** | correct-work (projet) final + rapport final + clôture | **(projet) directive n°11** | 0/1 SG |

---

## Groupe G1 — Analyse + comparaison + tests de performances — 3 SG #token 14000

> **Indépendances prouvées** : SG1.1 (rapport d'analyse — sortie extraction déjà faite en cadrage), SG1.2 (fixtures DREW + batteries dépôt), SG1.3 (tests perf toolkit Task 39) — livrables et écritures disjoints → **SG1.1 ∥ SG1.2 ∥ SG1.3** (vague 1).

### SG1.1 Analyse de la discussion — 2/2
| Tâche | Description | #token |
|---|---|---|
| T1.1.1 | Journal des voies de récupération (WebFetch 0 ligne [BLOQUÉ], API curl 403 [BLOQUÉ], agent-browser [SUCCÈS] — 8 positions de scroll, 715→1160 fragments, fusion dédupliquée 882) + persistance `work/disc-b6170b8b/discussion-complete.txt` (D001) | 1500 |
| T1.1.2 | Rapport d'analyse `download/rapport-analyse-discussion-b6170b8b.md` : directive originale, itérations 1-3, éléments générés (fichiers/structure), catalogue scellé, correctifs (dont onMessage dupliqué), harnais de tests, tableau CC consolidé, documented performance (D002) | 3000 |

### SG1.2 Fixtures DREW + batteries du dépôt — 2/2
| Tâche | Description | #token |
|---|---|---|
| T1.2.1 | Extraction ZIP DREW → `work/drew-fixtures/` (6 membres : TSI 623 Ko + 2 PDF + 2 PNG) + sha256 (D005) | 1000 |
| T1.2.2 | Re-certification batterie analyse-doc-s4mk2 sur fixtures DREW réelles (16/16 attendu — les 4 tests non exécutables Task 39 deviennent exécutables) + arbitre tsi-validator sur TSI DREW (D005) | 2500 |

### SG1.3 Tests de performances comparatifs — 2/2
| Tâche | Description | #token |
|---|---|---|
| T1.3.1 | Comparatif mécanique élément-par-élément discussion ↔ dépôt (clone fddbe94) — inventaire des présences/absences (app, catalogue, scripts, data, docs) → `download/rapport-comparaison-discussion-depot.md` (D003) | 2000 |
| T1.3.2 | Timings $FACON2 : arbitres dépôt (tsi-validator DREW+DJTT, analyse-zip DREW+DJTT) × toolkit Task 39 (nixml/validateur/presets/generateur) — 3 runs médians, seuils CDC (D004) | 2500 |

---

## Groupe G2 — Génération $FACON des versions cohérentes — 2 SG #token 12000

> Dépend de G1 (constats de comparaison). SG2.1 ∥ SG2.2 (arborescences disjointes : tsi-toolkit/ + racine vs skills/@mon-ecosysteme + KNOWLEDGE.md).

### SG2.1 Intégration des livrables Task 39 au dépôt — 1/1
| Tâche | Description | #token |
|---|---|---|
| T2.1.1 | Copie byte-identique hôte→dépôt : `tsi-toolkit/` (9 modules + tests + data + examples), `tsi-agent.md`, `construire-zip-tsi.py`, `bibliotheque-skills-ia/`, `data/commandes-traktor.json` (via toolkit), `download/architecture-mapping-studio-v11.md` + rapports Task 39 pertinents ; re-jeu suite 20/20 dans l'arbre dépôt (D006a) | 4000 |

### SG2.2 Montée corpus v3.32.0 + réconciliation catalogue — 2/2
| Tâche | Description | #token |
|---|---|---|
| T2.2.1 | Corpus gen-plan v3.32.0 → dépôt : `PROMPT-MAITRE-GEN-PLAN-v3.32.0.md` (retrait v3.31.0), SKILL.md gen-plan v3.32.0, pin KNOWLEDGE.md, @historique/historiques-par-skill/gen-plan.md, delta-genplan-v3320.json (D006b) — cascade KO-L004 déjà certifiée Task 38, intégration uniquement | 3000 |
| T2.2.2 | Réconciliation catalogue : discussion (388 commandes/39 catégories/62 enums + s4mk2-controls 125/220) ↔ toolkit (163 contrôles + 393 commandes + 345 conditions) — analyse des écarts, extension $FACON de data/commandes-traktor.json si cohérent (source : extraction discussion, zéro valeur inventée) (D006c) | 3000 |

**Barrière G2 (convergence)** : correct-work(groupe, CIBLE) sur G1+G2 — **directive n°3**.

---

## Groupe G3 — Extension React du studio v11 (LEON TSI EDITEUR) — 3 SG #token 45000

> Dépend de G2 (toolkit intégré = moteur). SG3.1 → SG3.2 → SG3.3 en série (fondations → couches → intégration studio v11 — dépendances d'ordre prouvées : chaque couche consomme la précédente). Skill **fullstack-dev** chargé avant toute génération (règle plateforme).

### SG3.1 Fondations lib + data — 1/1
| Tâche | Description | #token |
|---|---|---|
| T3.1.1 | `src/lib/tsi/` (binary, format, types, midi, edit, catalog) + `src/lib/midi/midi-access.ts` (singleton, learn, moniteur, **handlePortMessage** — correctif critique itération 3 préservé) + `src/data/*.json` (catalogue scellé reconstruit depuis toolkit + discussion, zéro valeur inventée) + prisma/schema.prisma (projets) (D007) | 12000 |

### SG3.2 API + composants LEON — 1/1
| Tâche | Description | #token |
|---|---|---|
| T3.2.1 | API routes `src/app/api/projects/*` (CRUD, export .tsi, verify byte-exact) + `src/components/leon/` : controller-view (3 vues In/Modes & Modules/LED — 8 modules, 73 chips), add-mapping-dialog (prefillCommand), orchestrateur page.tsx (mass-edit, Ctrl+L) (D007) | 18000 |

### SG3.3 Intégration studio v11 (moteur partagé, R4) — 1/1
| Tâche | Description | #token |
|---|---|---|
| T3.3.1 | Pont studio v11 ↔ app : presets du toolkit exposés/consommés (source de vérité partagée), DSL éditeur, audit_log auto-évolutif, génération validée par l'arbitre (valider-tsi) — conforme architecture-mapping-studio-v11.md §Extension React (D007) | 10000 |

**Barrière G3** : correct-work(groupe, CIBLE) — **directive n°5**.

---

## Groupe G4 — Batterie tests $FACON $FACON2 + correctifs — 2 SG #token 20000

> **Indépendances prouvées** : SG4.1 (app) et SG4.2 (toolchain + arbitres) — cibles disjointes → **SG4.1 ∥ SG4.2**.

### SG4.1 Harnais app full-stack — 2/2
| Tâche | Description | #token |
|---|---|---|
| T4.1.1 | Tests app : idempotence TSI (round-trips), API fonctionnelle (15 points), ESLint 0/0, tsc --noEmit (src/), navigateur interactif (vues, chips, pré-remplissage, persistance), restauration propre de l'état projet (D008) | 8000 |
| T4.1.2 | Correctifs les plus appropriés sur échecs/réserves (max 2 rounds par cible, re-test) (D009) | 4000 |

### SG4.2 Toolchain + arbitres + DREW — 1/1
| Tâche | Description | #token |
|---|---|---|
| T4.2.1 | Suite toolkit 20/20 (dans l'arbre dépôt), arbitres écosystème (integrity 98/98, verify-cross, coherence, tool-routing N1+N2 — N2 résorbé par le présent plan), batterie DREW 16/16, timings médians (seuils CDC 10 s/5 s) (D008) | 6000 |

**G5 — correct-work (projet) jalon** : **directive n°7** (inclut re-jeu answer key D001-D016).

---

## Groupe G6 — Tous les correctifs — 1 SG #token 8000
| Tâche | Description | #token |
|---|---|---|
| T6.1.1 | Résorption de TOUS les résidus (correct-work, tests, verify-cross warnings ciblés, dérives d'arbitres — qualification honnête des légitimes, 0 régression R2) (D011) | 8000 |

**Barrière G6** : correct-work(groupe, CIBLE) — **directive n°9**.

---

## Groupe G7 — PUSH — 1 SG #token 5000
| Tâche | Description | #token |
|---|---|---|
| T7.1.1 | Contrôles pré-push 4/4 (divergence fast-forward vs origin/main fddbe94, commits certifiés pathspec, volumétrie, scan secrets 0 github_pat_/ghp_ dans le diff) → `git push origin main` avec PAT **usage transitoire unique** (env, jamais fichier/config/URL/sortie — procédure Task 37) → vérification post-push ls-remote == HEAD (D012, D013) | 5000 |

---

## Groupe G8 — correct-work (projet) final + clôture — 1 SG #token 8000
| Tâche | Description | #token |
|---|---|---|
| T8.1.1 | correct-work(projet) final : answer key D001-D016 re-jouée, état écosystème, cohérence session (D010) | 4000 |
| T8.1.2 | Rapport final `download/rapport-final-task40.md` (vue fermée, couverture, pendances) + worklog par groupe (D014) | 4000 |

---

## Invariants

- Originaux `upload/` jamais modifiés (P0) ; arbre de travail dépôt = `work/knowledge-clone-fddbe94/` (clone certifié fddbe94) ; livrables session `download/` (hôte) ;
- **PUSH = directive propriétaire explicite (délégation KO-L009 point 5, procédure Task 37)** — PAT transitoire, jamais persisté, guidance rotation consignée (3e exposition) ;
- Garde R2 : aucune rétrogradation skills ; intégration dépôt = additions + montée v3.32.0 ; cascade KO-L004 déjà certifiée Task 38 (aucune re-cascade requise — intégration byte-identique) ;
- Graph Diamond v1.0.0 byte-identique — jamais édité ; preuve d'indépendance pour chaque vague parallèle ;
- Zéro valeur inventée : catalogue et CC issus des sources scellées (discussion extraite + toolkit + arbitre) ; mode MIDI = SHIFT+PREVIEW (manuel NI §6.10.2) ;
- Skills hôte inchangés (sauf vérification correct-work) ; tout script nouveau = conventions script-creator (stdlib Python ou TS du harnais existant, idempotent ×2) ; toute infrastructure déployée = conventions script-mon-ecosysteme-infrastructure (INFRA-1..3) ; tout agent/PM manipulé via les formes agent-creator existantes ; toute modification de skill passerait par skill-creator + cascade KO-L004 (non prévu hors intégration v3.32.0 certifiée) ;
- Max 2 rounds de correction correct-work par groupe ; verdict global = pire des verdicts ; statuts dérivés du disque (KO-L003) ;
- Budget #token estimé ≈ 132 000 — surveillance resource-monitor entre les vagues (hook C2).

## Verdict E8

Verdict E8 : PASS (answer key 16 décisions vérifiables, structure G/SG/T conforme §5.5, barrières alignées sur la directive à 11 étapes, routage normatif N2 cité, invariants Graph Diamond/R2/KO-L009 respectés. Horodatage vérifié : 2026-11-02T22:10:00+01:00)
