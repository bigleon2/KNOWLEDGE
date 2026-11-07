# Disciplines d'ingénierie de prompts — tables de mobilisation intégrales

> Résumé opérationnel dans le SKILL.md §1.6 ; tables complètes E1-E15, matérialisations n°54/n°55, mobilisation par déclencheur et hook continu ci-dessous.


<!-- BLOC-DEPLACÉ:disciplines:v3.38.0:bbc8280573179ab2 -->

> **Provenance (R4 byte-identité — re-curation R1 v3.39.0, Task 72 G1, 2026-11-08, directive propriétaire « Chantier R1 prioritaire : re-curation progressive disclosure de gen-plan »)** : contenu déplacé VERBATIM depuis le SKILL.md gen-plan v3.38.0 — jamais réédité, jamais dupliqué (le SKILL.md ne conserve qu'un résumé opérationnel NOUVEAU + le présent pointeur, lecture à la demande — progressive disclosure, étude Task 70 R1). SHA-256 du bloc d'origine : `bbc8280573179ab25b43c7b3cfe2ab06b7276f393cabf5bf8e39f4a9486e7361`.

### §1.6 Disciplines d'ingénierie de prompts (PM v3.12.0 §1.9)

| Discipline | Mécanisme gen-plan |
|------------|--------------------|
| **Context engineering** | Socle SHARED lu en premier ; lecture bloc par bloc avec synthèses intermédiaires |
| **Loop engineering** | Boucle E10-E13 (exécution → surveillance → écart → ajustement) ; auto-calibration E15 |
| **Graph engineering** | Registre KB = graphe de relations bidirectionnelles versionnées ; matrice agent × skill |
| **Harness engineering** | Profils ressource + signaux de pression ; hook E8 correct-work + contrôle par phase (E9-E14) ; worklog structuré |
| **Refactoring engineering** | Discipline n°55 : déclaration/planification/exécution des opérations de refactoring (petites transformations préservant le comportement observable — arbitres, semver, R2/R4) ; se sert de refactoring-test comme d'un outil ; garde-fous : refactor-guard (fusion 468a4c26) ; bloc PATTERN:GEN-PLAN-REFACTORING-v1.0.0 |
| **Refactoring test** | Outil de la discipline n°55 (non discipline — Task 8) : détection/évaluation des situations de refactoring + graphe d'interactions (blast radius) ; verdict machine OK/PRESSION/CRITIQUE |

**Table de mobilisation E1-E8 (v3.12.0)** — disciplines mobilisées par étape de planification (audit N5-a : interprétation PEK E1-E3 conforme, génération E4-E8 explicitée) :

| Étape | Disciplines mobilisées | Mécanisme |
|--------|------------------------|-----------|
| E1 | prompt-engineering (PEK) ; context-engineering | Interprétation CoT/Chaining/Hybride (E1-E3) ; lecture SHARED/KB préalable |
| E2 | context-engineering ; graph-engineering | Lecture bloc par bloc + synthèses intermédiaires ; Protocole de Découverte KB |
| E3 | prompt-engineering (PEK) | Blocs de sortie adaptatifs A-J mappés sur les Types 1-4 |
| E4 | harness-engineering | Grille #token, budgets, filtrage par profil |
| E5 | graph-engineering ; context-engineering | Graphe KB (matrice agent × skill) ; scan du registre |
| E6 | harness-engineering ; resource-monitor | Profils NORMAL/ECO/VIEUX PC, signaux de pression ; verdict G-RES (OK/PRESSION/CRITIQUE) → profil — v3.31.0, alignement sur la déclaration du provider |
| E7 | loop-engineering ; context-engineering ; harness-engineering | Boucles R3 prédéfinies (règle d'or n°1) ; plan auto-suffisant ; hooks par phase E9-E14 |
| E8 | harness-engineering ; prompt-engineering (PEK) | Hook correct-work (3 verdicts) ; 12 checks PEK (scoring 22/25) |

**Mobilisation E15 (v3.31.0 — complétion de couverture E1-E15, rapport de vérification des disciplines C1)** : loop-engineering (auto-calibration §2.3 — écart estimé vs réel → recalibrage) ; graph-engineering (enrichissement KB §2.5) ; memory-engineering (écriture État Long du bilan — worklog R5 + calibration) ; refactoring-test (re-scan post-session si une situation de refactoring a été constatée en vol) ; resource-monitor (verdict G-RES de clôture consigné au bilan).

L'optimisation fine des prompts complexes est déléguée au skill `prompt-engineering` (SHARED §3.1).

**Méthode prompt-engineering (méthode-mère)** : gen-plan est le détenteur principal de la méthode prompt-engineering (définitions : SHARED §7 ; orchestration : PM v3.12.0 §1.9) ; les autres skills de l'écosystème la détiennent en tant que **fonction héritée** (registre d'assignation : SHARED §7).

**Méthode de raisonnement adaptative PEK (v3.11.0, PM §1.9)** : gen-plan mobilise le Prompt Engineering Kit v4.1 (méthode pure) comme couche de raisonnement opérationnelle — 3 modes d'exécution (CoT 7 étapes / Chaining 4 étapes / Hybride à bascule automatique selon la complexité E1-E3) alignés sur la philosophie §1.4 #6 et calibrés par les profils §2.4 ; blocs de sortie adaptatifs A-J mappés sur les Types 1-4 (E3) ; 9 règles critiques + 12 checks de validation (scoring 25 pts, seuil 22/25) intégrés aux hooks correct-work par phase (E9-E14). Contenu opérationnel : `references/prompt-engineering-kit.md`.

**Matérialisation des disciplines (état A12, mise à jour session A13)** : les 4 disciplines d'exécution sont matérialisées en skills complets à déclenchement automatique (`context-engineering`, `loop-engineering`, `graph-engineering`, `harness-engineering` — SKILL.md + evals + trigger_evals ; les matérialisations agent intermédiaires `_disciplines/` A11 et `gen-plan.agent` A9 sont retirées, SHA prouvés) et la discipline prompt-engineering en skill (`prompt-engineering`). Source de vérité des disciplines : SHARED §7 ; orchestration : PM v3.12.0 §1.9.

<!-- PATTERN:GEN-PLAN-DISCIPLINES-ETENDUES-v2.0.0 -->

**Matérialisations n°54 — disciplines d'ingénierie étendues (v3.22.0, cascade KO-L004/§2quater — discussion parente 5ef6176f recalibrée sur l'état réel N34, Tasks 16-18)** : les 3 disciplines n°54 sont matérialisées en skills complets à déclenchement automatique (`spec-driven-development`, `memory-engineering`, `fleet-engineering` — SKILL.md + evals + trigger_evals, baselines mesurées 7/7 voie mécanique + 42/42 votes LLM) et sont orchestrées par gen-plan **au même titre** que les 4 disciplines A12 :

| Étape | Disciplines matérialisées n°54 mobilisées | Mécanisme |
|--------|------------------------|-----------|
| E4 | spec-driven-development ; memory-engineering | Cadrage spec-first (answer key E1 = spec de session) ; État Long obligatoire (plan + worklog + KB) |
| E5/E7 | fleet-engineering ; graph-engineering | Choix pattern/bornes de flotte à E5 (Graph Diamond E9-E14) ; re-validation du choix de flotte avec la spec de session à E7 — v3.31.0, alignement §3 (divergence interne résorbée) ; matrice agent × skill |
| E7 | spec-driven-development | Re-validation de la spec de session avant publication du plan |
| E9-E14 | memory-engineering ; fleet-engineering | Compaction + ancres de reprise entre phases ; contrôle de flotte par phase (hook correct-work) |
| E15 | memory-engineering | Écriture État Long du bilan (worklog R5, enrichissement KB, calibration grille #token) |

Source de vérité : SHARED §7 (table de définitions + registre d'assignation — v1.7.0) ; détention orchestrée : registre décentralisé §8 de chaque skill + registre KB ; orchestration : PM v3.12.0 §1.9. Les relations inter-disciplines (fleet ↔ memory ↔ spec) restent en §3 des skills, non versionnées (SHARED §3.2 règle 5).

<!-- FIN-PATTERN:GEN-PLAN-DISCIPLINES-ETENDUES-v2.0.0 -->

<!-- PATTERN:GEN-PLAN-REFACTORING-v1.0.0 -->

**Discipline de refactoring n°55 et son outil (v3.23.1 — Task 8 : correction directive propriétaire « seul refactoring-engineering est une discipline, qui se sert de refactoring-test comme un outil » ; fusion discussion externe 468a4c26 : refactor-guard v1.7.0 déclaré comme garde-fous des opérations)** : le système de refactoring effectif de l'écosystème (correct-work modes CIBLE/DIRECT + procédures cascade PM + arbitres mécaniques + archivage @historique R4) est déclaré comme discipline `refactoring-engineering` ; l'outil `refactoring-test` (producteur d'information, non discipline, ne modifie rien — anti-auto-certification) est appelable par tout élément (gen-plan, agents, disciplines, scripts) ; le garde-fous `refactor-guard` (score de risque H01-H15, sandbox, échelle rollout) est mobilisé par refactoring-engineering pendant les opérations à risque. gen-plan les mobilise :

| Étape | Disciplines n°55 mobilisées | Mécanisme |
|--------|------------------------|-----------|
| E4 | refactoring-test ; refactoring-engineering | Détection/évaluation des situations de refactoring (M1 scan, verdict OK/PRESSION/CRITIQUE) ; conception des opérations dans le plan (fiche D1 — invariants, preuves attendues, pré-checks verrouillés = golden master) |
| E7 | refactoring-test | Re-validation de l'impact avant publication du plan (M3 — graphe d'interactions, blast radius des modifications prévues) |
| E9-E14 | refactoring-test ; refactoring-engineering | Toute situation où un refactoring pourrait se poser route vers refactoring-test (évaluation) puis refactoring-engineering (D1-D4 — zéro-régression) ; re-scan post-opératoire M4 |
| E15 | refactoring-test | Re-scan post-session si une situation de refactoring a été constatée (M1) — verdict OK/PRESSION/CRITIQUE consigné au bilan |

Règle d'anti-auto-certification : l'exécutant (refactoring-engineering) ne s'auto-évalue pas — évaluation indépendante par refactoring-test (pré-vol/post-vol) + arbitres mécaniques + correct-work. Source de vérité : SHARED §7 (n°55) ; détention orchestrée : registre décentralisé §8 de chaque skill + registre KB. Les opérations à risque mobilisent refactor-guard (garde-fous — fusion 468a4c26).

<!-- FIN-PATTERN:GEN-PLAN-REFACTORING-v1.0.0 -->

<!-- PATTERN:GEN-PLAN-DISCIPLINES-MODES-v1.0.0 -->

**Mobilisation par déclencheur — disciplines × modes d'invocation (v3.31.0 — complétion « tous les cas de figure », rapport de vérification des disciplines C4)** : le socle commun (context-engineering, loop-engineering, graph-engineering, harness-engineering + méthode-mère PEK) s'applique à TOUT déclencheur du §A ; les tables E1-E8/n°54/n°55/E15 ci-dessus s'appliquent au chemin nominal. Au-delà du socle :

| Déclencheur | Disciplines mobilisées en sus du socle | Mécanisme |
|-------------|----------------------------------------|-----------|
| `gen-plan : <tâche>` (mode NULL — exécution classique / intégration E13) | Toutes, selon les tables E1-E15 ci-dessus | Chemin nominal — aucune restriction |
| `gen-plan(step)` / `gen-plan(step-ok)` | harness (correct-work(groupe) à chaque groupe, §5.4) ; memory-engineering (statuts dérivés du disque entre groupes, ancres de reprise) | §5.5 |
| `orchestre` | fleet-engineering (choix du pattern M1-M5 et des bornes AVANT lancement) ; graph-engineering (matrice agent × skill) ; memory-engineering (sections worklog par Task ID — lignée de flotte) | SHARED §7 (n°54) |
| `gen-plan:generate(<description>)` | spec-driven-development (answer key = spec exécutable) ; harness (grille #token, arbitre E7/E8) ; PEK (blocs A-J) | §1.2bis, §4 |
| `gen-plan:correct-work(projet\|<cible>)` | harness (arbitres, verdicts) ; refactoring-test (évaluation si écarts de refactoring détectés) puis refactoring-engineering + refactor-guard (opérations) ; memory-engineering (lecture préalable du worklog — B-11) | §3, SHARED §7 (n°55) |
| Reprise E1-RES (toute interruption) | memory-engineering (état dérivé du disque, ancres de reprise) ; harness (re-validation E8, affichage REJOUABLE) ; resource-monitor (collecte G-RES avant reprise) | §1.2bis |

**Hook continu E9-E14 — resource-monitor (v3.31.0, résorption du drift provider)** : le verdict resource-monitor (OK/PRESSION/CRITIQUE) est re-collecté à chaque checkpoint E11 et entre les vagues du Graph Diamond (philosophie #4) ; PRESSION → ECO, CRITIQUE → bascule sérielle/PAUSE — décision journalisée (règle d'or n°1) ; l'avis reste un AVIS structuré : la bascule reste à gen-plan.

<!-- FIN-PATTERN:GEN-PLAN-DISCIPLINES-MODES-v1.0.0 -->

---

<!-- FIN-BLOC-DEPLACÉ:disciplines -->
