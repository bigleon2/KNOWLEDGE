---
name: gen-plan
version: 3.49.0
category: ecosystem
language: fr
tags:
  - planning
  - task-management
  - token-estimation
  - auto-calibration
  - ecosystem
description: >
  Skill de planification de tâches pour assistant IA.
  4 modes (Planification, Exécution, Surveillance, Adaptation),
  15 étapes (E1-E15), classification Type 1-4 (documents, analyse, développement web, data), 3 profils ressource (NORMAL/ECO/VIEUX PC),
  tagging #token, snippets, scripts Python uniquement,
  règles d'or d'adaptation autonome, disciplines d'ingénierie de prompts,
  hooks patterns avancés (answer key E1, arbitre answer-key-checker E7/E8,
  Graph Diamond E9-E14 — parallélisation par défaut sur preuve d'indépendance, knowledge-observer E15),
  déclencheurs verbatim « intègre dans le plan d'actions » (E13 — extension du plan courant, règle d'or n°3)
  et « met à jour » (re-génération $FACON d'un nouveau plan d'actions $FACON2 — v3.37.0),
  glossaire alias-eco inline $FACON/$FACON2 (§A — auto-contenu, v3.37.0)
  progressive disclosure R1 (v3.39.0) : résumés inline, intégraux en references/ à la demande,
  chaîne de vérification par étape terminée en mode NULL — correct-work(CIBLE) AVANT l'étape suivante (v3.44.0),
  mode step sans AUCUNE validation du propriétaire pour passer aux étapes suivantes — seul le mode step-ok en demande (v3.45.0),
  pré-traitement PROMPT-GATEWAY : agent-prompt-engineering v1.2.0 invoqué en tête de chaîne (É1-PROMPT-GATEWAY §1.16, v3.46.0) — réécriture des demandes complexes AVANT l'analyse E1,
  règle FAIL-CLOSE §1.18 (v3.48.0) : correction des FAILS même non bloquants avant fermeture d'étape + journal journal-fails.md,
  routage décisionnel É5-ROUTAGE (v3.47.0) : script routage-skills-agents.py — recommandation de skills depuis les frontmatters installés (source unique R4) + verdict de complexité 5 critères + porte COMPLEXE >= 2/5 pour la délégation d'agents (§1.17),
  rappel permanent langue française (règle d'or n°6 durcie — §0, v3.47.0),
  garde É1-INSTALL à TOUTE invocation — chaque nouvelle requête (v3.49.0) : détection d'amnésie
  via point d'entrée AMORÇABLE (shim → repli bootstrap canonique, PM-INSTALL §3.2-d) et
  réinstallation des éléments INDISPENSABLES adaptés à l'exécution du plan (fermeture MINIMALE
  + skills routés É5-ROUTAGE — jamais l'arbre complet sauf directive, verdict INSTALLE-POUR-PLAN),
  hook É5-DISCIPLINES (v3.49.0) : routage-disciplines.py (skill orchestration-disciplines v1.0.0)
  — section « Orchestration des disciplines » du plan + protocole d'évolution (re-injection des
  résultats vérifiés des tâches parallèles aux checkpoints E11 et frontières de groupes)
dependencies:
  - skill: correct-work
    version: ">=2.4.0"
    used_at: "E1, E8 hook, contrôle par phase ; par étape terminée en mode NULL (v3.44.0)"
  - skill: clone-chat
    version: ">=2.0.0"
    used_at: "E4, E15"
    optional: true
  - skill: skills-inventory
    version: ">=1.0.0"
    used_at: "E5"
  - skill: knowledge-observer
    version: ">=1.0.0"
    used_at: "E15 (analyse post-session, modes M1-M2)"
  - skill: resource-monitor
    version: ">=1.0.0"
    used_at: "Hook E1-RES (collecte G-RES, ouverture de session)"
  - skill: agent-prompt-engineering
    version: ">=1.2.0"
    used_at: "É1-PROMPT-GATEWAY (pré-traitement de la demande, §1.16) + délégation §1.6/§1.9"
  - skill: orchestration-disciplines
    version: ">=1.0.0"
    used_at: "É5-DISCIPLINES (mobilisation des disciplines + protocole d'évolution du plan, §1.16)"
read_when:
  - Déclencher quand la demande concerne : skill de planification de tâches pour assistant IA
  - Déclencher si la demande mentionne : plan d'actions, planification, adaptation, answer, intègre dans le plan d'actions, met à jour (le plan d'actions), gen-plan(step), gen-plan(step-ok), orchestre
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

## §A — DÉCLENCHEURS (v3.28.0 — intégration du §A du PM GEN-PLAN, tâche 1 directive 10 tâches)

> **Glossaire alias-eco inline (v3.37.0 — directive propriétaire 2026-11-07 : « fais en sorte qu'à la lecture du skill que tu n'aies pas besoin de "alias-eco" pour comprendre $FACON et $FACON2 »)** : les marqueurs alias employés dans ce SKILL.md sont définis ICI pour lecture auto-contenue — **`$FACON` = « de façon cohérente, optimisée et fonctionnelle »** (adverbe modal : la manière d'exécuter) · **`$FACON2` = « (cohérent, optimisé et fonctionnel) »** (qualificatif : la propriété attendue du livrable). Source canonique : registre alias-eco `@historique/@Alias/aliases.json` ; en cas d'écart, le présent glossaire fait foi pour la lecture du skill, le registre pour l'expansion des messages du propriétaire ; toute évolution du registre est recalibrée ici à la montée de version suivante (cascade KO-L004).

- `gen-plan:` suivi d'une description de tâche
- `gen-plan:correct-work(projet)` — vérification et correction d'un projet complet
- `gen-plan:correct-work(<cible>)` — vérification/correction d'un élément spécifique
- `plan d'actions` — demande explicite de planification
- « intègre dans le plan d'actions » — intégration d'une nouvelle demande dans le plan courant (E13, règle d'or n°3 — extension, jamais réécriture destructrice R2 ; déclencheur verbatim v3.17.2, directive propriétaire)
- « met à jour (le plan d'actions) » — re-génération $FACON d'un NOUVEAU plan d'actions $FACON2 : consolidation de l'état vérifiable du plan courant (groupes terminés reportés avec preuves — statuts dérivés du disque : worklog, verdicts d'arbitres, livrables ; règle d'or n°5 — KO-L003) + restes-à-faire re-planifiés + nouvelles demandes (E13 intégrées à la consolidation) + re-estimation #token + answer key re-numérotée ; le NOUVEAU plan (fichier horodaté dans `download/`) devient la référence d'exécution, l'ancien est conservé (R2) ; chaîne E7-DISP complète (answer key, E8 horodatages couplés, R5, PLAN-AFFICHE) — VOIE DISTINCTE de « intègre dans le plan d'actions » (extension E13 du plan courant EN PLACE) (règle d'or n°3 — déclencheur verbatim v3.37.0, directive propriétaire 2026-11-07)
- `gen-plan(step) : <instructions>` — enchaînement autonome des groupes séquentiels du plan d'actions, correct-work(groupe) après chaque groupe (max 2 rounds de correction), correct-work(projet) en fin de chaîne (v3.22.0) ; à l'ouverture de chaque groupe : vue d'évolution PLAN-AFFICHE (E7-DISP v3.36.0 — tous modes) ; **JAMAIS de validation du propriétaire pour passer aux étapes/groupes suivants (v3.45.0 — aucune porte, aucune pause : l'exécution enchaîne intégralement jusqu'à la clôture de la chaîne, seuls les verdicts mécaniques correct-work(groupe)/(projet) jalonnent la progression ; les portes de validation sont l'EXCLUSIVITÉ du mode step-ok)**
- `gen-plan(step-ok) : <instructions>` — identique au mode step avec demande de confirmation du propriétaire avant chaque groupe — **SEUL mode à portes de validation (v3.45.0 : les modes step et NULL n'en demandent JAMAIS — hors step-ok, aucune validation n'est requise pour passer aux étapes suivantes)** (nom canonique v3.22.1) ; alias `step-confirm` (v3.22.0) et `step-confim` normalisés en `step-ok` (R4) ; **clause mode NULL** — toute invocation sans `<mode>` explicite (`gen-plan : <instructions>`, ex. « gen-plan : continue ») conserve le comportement antérieur à l'introduction des modes step/step-ok (v3.21.0) : intégration E13 ou exécution classique, sans portes de confirmation (directive propriétaire 2026-10-11) ; **chaîne de vérification par étape terminée (v3.44.0)** : chaque étape du plan d'actions terminée est vérifiée par `correct-work(livrables de l'étape, mode=CIBLE)` AVANT l'étape suivante — le statut `verified` de l'answer key est subordonné au verdict CIBLE (KO-L003) ; tout autre mode → clarification demandée, jamais d'invention de mode (R2)
- `orchestre` — orchestration multi-agents
- Toute demande impliquant plusieurs étapes séquentielles avec des livrables
- `gen-plan:generate(<description>)` — génération d'un plan auto-exécutable

## §0 — Contexte Système (SHARED v1.7.47)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.
> Langue : FRANÇAIS exclusif pour tous les échanges avec le propriétaire (règle d'or n°6 gen-plan — directive 2026-10-31, renforcée 2026-11-06) : dès le PREMIER mot de toute session ou reprise, la langue d'un message, d'un résumé de continuation ou d'un canal ne dérive JAMAIS la réponse ; toute dérive est corrigée immédiatement.
> Règles d'or & lecture SHARED à l'exécution (directive propriétaire 2026-11-06 — SHARED §9) : tout skill/agent/script exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or de l'écosystème (résumé §9 — canonique gen-plan §1.5).
> Référence canonique skill/agent (directive propriétaire 2026-11-07 — SHARED §0/§1.2) : toute référence à « mon skill X »/« mon agent X » désigne la forme installée à la racine `skills/X/SKILL.md`, JAMAIS le prompt maître du corpus `@mon-ecosysteme/` (ex-nommé `@PM-SKILLS/`) — les PMs sont des spécifications générées mécaniquement (KO-L004), les skills installés sont les formes exécutables.

**RAPPEL PERMANENT — LANGUE DU DIALOGUE (règle d'or n°6 durcie, v3.47.0 — directive propriétaire trace 1a2025ce4a6ed095, rappel à CHAQUE exécution de gen-plan, AVANT tout autre rappel)** : le dialogue avec le propriétaire est en FRANÇAIS exclusif — JAMAIS de chinois, jamais d'anglais, dès le PREMIER mot de tout message, TODO/fenêtre de tâches, résumé de continuation ou livrable ; toute dérive constatée (langue du tour précédent ou en cours) est CORRIGÉE IMMÉDIATEMENT dans le même message et journalisée au worklog (correction + worklog + durcissement) ; artefacts techniques verbatim exceptés (code, CLI, identifiants d'API — règle d'or n°6).

## §1 — Spécification fonctionnelle

### §1.1 Les 4 modes

| Mode | Nom | Description |
|------|-----|-------------|
| M1 | **Planification** | Analyse, classification, estimation, création du plan |
| M2 | **Exécution** | Passage à l'action selon le plan |
| M3 | **Surveillance** | Monitoring temps réel, détection d'écarts |
| M4 | **Adaptation** | Ajustement du plan en cas de dérive |

### §1.2 Les 15 étapes (E1-E15)

| Étape | Nom | Mode |
|-------|------|------|
| E1 | Analyse de la demande | M1 |
| E2 | Inventaire des ressources | M1 |
| E3 | Classification du type de tâche (Type 1-4) | M1 |
| E4 | Estimation #token | M1 |
| E5 | Sélection des skills | M1 |
| E6 | Profilage ressource (NORMAL/ECO/VIEUX PC) | M1 |
| E7 | Création du plan | M1 |
| E8 | Validation du plan | M1 |
| E9 | Lancement de l'exécution | M2 |
| E10 | Suivi d'étape | M2/M3 |
| E11 | Checkpoint intermédiaire | M3 |
| E12 | Détection d'écart | M3 |
| E13 | Ajustement | M4 |
| E14 | Finalisation | M2 |
| E15 | Bilan et auto-calibration | M1/M4 |

> Détail complet de chaque étape : `references/etapes-detaillees.md`

### §1.2bis Hooks patterns avancés (v3.13.0, phase N20)

<!-- PATTERN:GEN-PLAN-HOOKS-PATTERNS-v1.0.0 -->

| Hook | Étape | Mécanisme | Référence |
|------|-------|-----------|-----------|
| **Answer key obligatoire** | **E1** | Chaque décision E1 devient une entrée `D0NN` de l'answer key (criterion, verification exécutable, source, priority S1-S4, status pending) | `references/answer-key-template.md` |
| **Arbitre answer-key-checker** | **E7/E8** | Le plan référence l'answer key ; à E8, l'arbitre mécanique `scripts/answer-key-checker.py` (16 checks) valide structure, fonctionnalité, idempotence et intégration — verdict PASS requis pour S1/S2 | `scripts/answer-key-checker.py` |
| **E7-DISP — Affichage obligatoire du plan** | **E7/E8/E13 + ouverture d'étape (v3.36.0) + fenêtre native début/fin d'étape (v3.39.0)** | Toute écriture du fichier plan (création E7, E13, re-génération KO-L005, reprise) n'est TERMINÉE qu'après la chaîne : plan écrit + answer key + verdict E8 (horodatages couplés) + worklog R5 marqueur `PLAN-AFFICHE` + bloc récapitulatif au chat — verdict mécanique bloquant ; affichage REJOUABLE (v3.27.0) ; à l'ouverture de chaque étape (v3.36.0) : bloc d'évolution du déroulement (groupes + statuts + compteurs + position — tous modes) | `scripts/check_plan_protocol.py` |
| **Graph Diamond** | **E9-E14** | Parallélisation PAR DÉFAUT des tâches ET commandes indépendantes (série = exception justifiée — #4 v3.24.0/v3.32.0/v3.40.0 émission : fan-out bloc + `&`+`wait`) — tracé worklog | `references/graph-diamond-pattern.md` |
| **Sondage borné** | **E9-E14** | Inspection transverse sur l'arbre skills/ TOUJOURS bornée : mode fichiers (-l) d'abord, greps multi-fichiers tronqués + limite de résultats ; §0/contrats jamais affichés en entier | `references/protocoles-detailles.md` |
| **Observer** | **E15** | Invoque knowledge-observer en modes M1-M2 (observation + analyse post-session) ; les modes M3-M4 exigent un verdict correct-work | `references/observation-patterns.md` |
| **E5-POIDS — arbitre de poids de chargement** | **E5** (v3.38.0) | À la sélection des skills (E5), l'arbitre `scripts/poids-chargement.py` (recommandation R1 étude Task 70 — le goulot réel est le budget #token) mesure le poids de chargement (Kio + #token estimés = caractères/4) ; un skill CRITIQUE (≥ 60 Kio) ou LOURD (≥ 30 Kio) déclenche la lecture ciblée : §0 + sommaire d'abord, sections dédiées ensuite, `references/` à la demande — JAMAIS de lecture intégrale par défaut | `scripts/poids-chargement.py` |
| **R2-CACHE — cache de verdicts** | **E9-E14** (v3.38.0) | Les graders coûteux (arbitres, harnais, batteries) ré-exécutés à entrées inchangées passent par `scripts/cache-verdicts.py` (recommandation R2 de l'étude Task 70) : verdict figé une fois (rc + stdout + durée), re-jeu sans ré-appel (gain 440×), invalidation auto par état des cibles (taille/mtime), `--force` pour re-vérification réelle — un verdict figé n'est JAMAIS une preuve en soi, la re-exécution reste disponible à la demande | `scripts/cache-verdicts.py` |
| **É5-DISCIPLINES — orchestration des disciplines** | **E5/E7** (v3.49.0) | À la sélection (E5) et à l'écriture du plan (E7) : `orchestration-disciplines/scripts/routage-disciplines.py --tache "<normalisée>" --declencheur <mode> --complexite <verdict>` → section « Orchestration des disciplines » du plan (mobilisation par étape + protocole d'évolution) ; les disciplines demeurent à déclenchement automatique (SHARED §7) — le hook formalise décision + gestion d'évolution | `skills/orchestration-disciplines/` |

<!-- FIN-PATTERN:GEN-PLAN-HOOKS-PATTERNS-v1.0.0 -->

<!-- RÉSUMÉ v3.39.0 — intégraux : references/protocoles-detailles.md -->

**Hook E1-RES — ouverture de session (4 vérifications AVANT analyse)** : (1) lecture seule préalable B-11 (worklog/plan/arbitres) ; (2) collecte G-RES (`monitor.py` : OK/PRESSION/CRITIQUE, journalisé) ; (3) fraîcheur du plan (modifiée et valide → re-généré avant reprise) ; (4) garde post-coupure (règle d'or n°9 : piliers + integrity → rétablissement auto). **Reprise (v3.27.0)** : message pendant un plan en vol → worklog + fraîcheur + E13 + E8 + R5 + affichage ; état « en vol » dérivé du DISQUE (RC3).

**Hook E7-DISP — affichage obligatoire (6 points, garde bloquante)** : (1) plan écrit `download/` ; (2) answer key >= 1 décision ; (3) E8 aux horodatages COUPLÉS (toute écriture = re-validation) ; (4) worklog R5 + marqueur `PLAN-AFFICHE` ; (5) bloc récapitulatif AU chat. Garde `check_plan_protocol.py` (P1-P5) ; affichage REJOUABLE ; ouverture d'étape (v3.36.0, tous modes) : PLAN-AFFICHE d'évolution au début de chaque groupe G<k> (statuts du disque). **(6) Fenêtre native (v3.39.0 — directive 1a1b7fe1c7238e8d)** : fenêtre des étapes du plan via le mécanisme NATIF de l'agent dédié à ce rôle (Z.ai : liste de tâches `TodoWrite`/`TodoRead`) — affichée au DÉBUT de l'exécution du plan d'actions, MISE À JOUR à chaque FIN d'étape ; intégral : `references/protocoles-detailles.md` (point 6).

### §1.3 Normes

- **N1 — Tagging #token** : chaque étape et skill reçoit un tag `#token` avec le coût estimé. Grille auto-calibrée après exécutions.
- **N2 — Snippets** : snippets de code réutilisables générés pendant l'exécution, tagués et versionnés.
- **N3 — Python uniquement** : tous les scripts générés doivent être en Python (aucun bash/sh/powershell).

### §1.4 Philosophie clés

1. **Read before planning** — Toujours lire le projet avant de planifier.
2. **Performance-driven sélection** — Le choix skill/agent est dicté par le gain de performance.
3. **Skills can launch specialized agents** — Modèle à deux couches : Skill → Agent Spécialisé.
4. **Parallélisation par défaut des tâches ET des commandes sur preuve d'indépendance** (v3.24.0/v3.32.0 + émission v3.40.0 + **sondage borné v3.41.0**) — vagues indépendantes en PARALLÈLE : Graph Diamond (E9-E14), série = exception tracée ; émission : fan-out multi-appels + concurrence `&`+`wait` ; sondage : inspection bornée (§1.2bis) ; dégradation 429 — intégral : `references/protocoles-detailles.md` (#4).
5. **Visible progress** — L'utilisateur sait toujours où on en est.
6. **CoT + Chaining avec auto-correction** — Raisonnement structuré avant chaque action.
7. **Lecture bloc par bloc** — Fichiers > 500 lignes : lire par blocs successifs (limit/offset) avec synthèse intermédiaire — jamais d'un seul coup (détail : `references/profils-ressource.md`).
8. **Downgrade irréversible** — Le profil ressource ne remonte jamais automatiquement.

### §1.5 Règles d'or (résumé opérationnel — intégral : `references/regles-or.md` ; miroir SHARED §9)

| N° | Règle | Portée |
|----|-------|--------|
| 1 | **Adaptation autonome** | Blocage = adaptation journalisée, jamais d'arrêt implicite ; pause explicite si inatteignable. |
| 2 | **Régénération post-installation** | Écosystème installé → plan re-généré via le gen-plan installé (R2). |
| 3 | **Mise à jour à chaque demande** | E13 (extension, jamais réécriture) ; « intègre dans le plan d'actions » = extension en place ; « met à jour » = NOUVEAU plan consolidé $FACON2. |
| — | **Modes** | `step` : chaîne par groupes SANS AUCUNE validation pour passer aux étapes suivantes (v3.45.0) ; `step-ok` : SEUL mode à confirmation ; NULL : comportement antérieur + correct-work(CIBLE) par étape terminée (v3.44.0) ; autre mode → clarification (R2). |
| 4 | **Dépôt par clone** | Clone git local, jamais de lecture distante ; jeton éphémère jamais persisté ; publication = validation propriétaire. |
| 5 | **État vérifiable** | Chiffres et statuts du disque, jamais pré-écrits (KO-L003) ; dépôt = source R4. |
| 6 | **Langue française** | Tout texte de l'agent en français dès le premier mot ; dérive → correction + worklog + durcissement. |
| 7 | **Mémoire complète** | Oubli de coupure → relire clones/sauvegardes avant (re-)génération. |
| 8 | **Formes installées** | PM INSTALL installe `skills/<skill>/` uniquement ; prompts maîtres jamais installés. |
| 9 | **Vérification d'installation** | Garde mécanique à toute invocation ; rétablissement auto puis re-génération du plan. |
| KO | **KO-L005** | gen-plan modifiée et validée → re-génération du plan (arbitres → montée → L004 → E8). |
| KO | **KO-L009** | Secret exposé : jamais utiliser ; révocation immédiate ; push = propriétaire, jamais l'agent. |
### §1.6 Disciplines d'ingénierie de prompts (résumé — tables intégrales : `references/disciplines-mobilisation.md`)

| Discipline | Mécanisme gen-plan |
|------------|--------------------|
| **Context engineering** | Socle SHARED d'abord ; lecture par blocs + synthèses |
| **Loop engineering** | Boucle E10-E13 ; auto-calibration E15 |
| **Graph engineering** | KB = graphe bidirectionnel versionné ; matrice agent × skill |
| **Harness engineering** | Profils + signaux ; hook E8 + contrôle par phase ; worklog |
| **Refactoring engineering** | Discipline n°55 : opérations préservant le comportement observable ; garde-fous refactor-guard |
| **Refactoring test** | Outil n°55 (anti-auto-certification) : évaluation + blast radius, verdict OK/PRESSION/CRITIQUE |
| **Agent engineering** | Discipline n°56 : cadrage/routage/outillage/veille des tâches d'agents (ABE/AE/MASE) — (SHARED §7, registre §8 du skill) |

- **Mobilisation** : tables E1-E8, n°54-55, E15, par déclencheur × modes — intégrales : `references/disciplines-mobilisation.md` ; socle commun (context/loop/graph/harness + PEK) à tout déclencheur du §A. **Hook continu E9-E14** : G-RES à chaque checkpoint E11 et entre vagues ; PRESSION → ECO, CRITIQUE → série/PAUSE. gen-plan = détenteur principal de la méthode prompt-engineering (SHARED §7 ; PEK v4.1). **Couche d'orchestration (v3.49.0)** : la décision de mobilisation et le protocole d'évolution du plan (nouvelles requêtes E13 + re-injection MÉCANIQUE des résultats vérifiés des tâches parallèles aux checkpoints E11 et frontières de groupes — scan du disque KO-L003) sont portés par le skill `orchestration-disciplines` (hook É5-DISCIPLINES, §1.2bis) — les tables demeurent la source unique R4.
### §1.7 Pipeline d'optimisation écosystème Z0-Z6 (PM v3.11.0 §1.10)

| Phase | Nom | Règles clés |
|-------|-----|-------------|
| Z0 | Inventaire | Règle zéro (SHARED §0) |
| Z1 | Normalisation | Frontmatters YAML complets (SHARED §1.3) |
| Z2 | Optimisation par fichier | Règles d'or, disciplines (§1.6), dépendances, cohérence |
| Z3 | Optimisation scripts Python | N3 ; arbitres (verify-cross, spell-check, sync-download) |
| Z4 | Vérifications croisées | SHARED §3.2 ; hooks correct-work |
| Z5 | Journalisation | Worklog (SHARED §1.4) |
| Z6 | Idempotence | R1-R6 (§1.8) |

### §1.8 Règles d'idempotence R1-R6 (PM v3.11.0 §1.11)

R1 vérifier présence avant insertion · R2 ne jamais rétrograder · R3 fusionner les frontmatters ·
R4 ne jamais dupliquer · R5 journaliser · R6 auto-adaptation sans duplication.

### §1.14 Leçons knowledge-observer — économie API et arbitres (résumé — intégral : `references/regles-or.md`)

- **KO-L001 — Économie API (429)** : une seule sonde par message utilisateur, travail local 100 % entre les sondes, suites armées à QUOTA_OK (`--skip-done`) ; pas d'attente en-tour.
- **KO-L003 — Arbitres à invariants dynamisés** : invariants dérivés de l'état courant, jamais figés ; divergence → dynamiser l'arbitre + re-verdict honnête, jamais ajuster la réalité.

### §1.14bis Leçons knowledge-observer — adaptation autonome aux erreurs runtime (résumé — intégral : `references/regles-or.md`)

- **KO-L011 — Assainissement SSE avant JSON.parse** (v3.43.0) : signature `SyntaxError` + `data:` (V8/Node — trame Server-Sent Events soumise à JSON.parse : préfixe de champ, payloads multiples, `[DONE]`, trame partielle) → **jamais de re-jeu à l'identique** (erreur déterministe de format) ; assainir AVANT parse — `scripts/adaptation-json-sse.py` (strip préfixes `data:`/`event:`/`id:`/`retry:`, filtre `[DONE]`/lignes vides, parse par payload, repli extraction bloc `{…}`, rc 0/2) — puis re-jeu ; échec persistant → voie non-streaming/méthode alternée (**max 2 rounds** — SHARED §4.4) ; adaptation journalisée worklog (règle d'or n°1). Instanciation de la règle d'or n°1 pour la classe SSE/JSON — sœur runtime d'`adaptation-syntaxe.py` (fichiers Python source ≠ données runtime).

### §1.15 Leçons knowledge-observer — recalibrage croisé (résumé — intégral : `references/regles-or.md`)

- **KO-L004 — Recalibrage croisé + génération PM** : toute montée de version → AVANT certification : recalibrage des outils dépendants (arbitres, pre-checks, skills-meta, run-order, SYNC_MAP, miroir, archive) + génération mécanique du PM (`scripts/generer-pm-skill.py`, substitutions verrouillées, R2).
- **KO-L007 — Matérialisation d'abord** : `git sparse-checkout list` + test d'existence AVANT toute écriture et tout verdict naïf ; « non matérialisé » ≠ « échec ».

> Saut §1.8 → §1.14 intentionnel (Task 21 A7).
### §1.16 Routage de découverte des skills + garde d'installation (résumé — intégral : `references/protocoles-detailles.md`)

- **É1-INSTALL — garde avec PRÉEMPTION** : à l'ouverture de session, AVANT E1 : `ensure-installed.py --check` (chemin canonique). rc=0 → no-op ; rc≠0 → suspension + `--reinstall` (pipeline PM-INSTALL) AVANT toute autre étape ; directive post-réinstall intégrée au plan ; idempotente. **v3.35.2** : contrôle du SKILL.md de toutes les entrées KB ; manquants → AUTO-RÉPARÉS depuis le miroir (INSTALLE-REPARÉ, rc=0, trace worklog). **v3.49.0 — garde à TOUTE invocation (directive propriétaire 2026-11-28 : chaque nouvelle requête, plus seulement l'ouverture de session)** : le point d'entrée est AMORÇABLE (shim `scripts/ensure-installed.py` → repli bootstrap canonique si `skills/gen-plan/` est absent — PM-INSTALL §3.2-d v1.10.7, fin de l'œuf-et-la-poule) ; en cas d'amnésie (seeds manquants), gen-plan fait appel au PM-INSTALL (bootstrap canonique) pour réinstaller les éléments INDISPENSABLES ADAPTÉS à l'exécution du plan (fermeture du profil MINIMALE + skills routés par É5-ROUTAGE pour le plan courant — jamais l'arbre complet sauf directive) ; verdict INSTALLE-POUR-PLAN consigné ; seeds vérifiés EN PREMIER (SEEDS-FIRST, PM-INSTALL §2bis v1.10.7). **Alignement R4 (audit déduplication — précision propriétaire trace 1a21e38435b96641)** : raffinement de la règle d'or n°9 (v3.35.0 — sources intégrales `references/regles-or.md`) : la voie COMPLÈTE n°9 (rétablissement 4 temps : lecture PM SHARED → réinstallation voie directe → certification → re-génération du plan) demeure quand l'écosystème est ABSENT ou ENDOMMAGÉ ; la fermeture MINIMALE adaptée au plan s'applique quand les piliers sont sains et que seuls les skills nécessaires au plan manquent — n°9 = règle SOURCE, É1-INSTALL = hook d'IMPLÉMENTATION (une seule description du mécanisme, R4).
- **É1-PROMPT-GATEWAY — pré-traitement de la demande (v3.46.0)** : après É1-INSTALL et AVANT l'analyse E1 : si le prompt du propriétaire n'a pas déjà été normalisé par le PROMPT-GATEWAY de agent-prompt-engineering (v1.2.0 — déclenchement inconditionnel : phases A-B systématiques, phases C-D conditionnelles au verdict COMPLEXE >= 2/5), l'agent l'invoque pour réécrire la demande en version compréhensible, explicite et structurée ; la version normalisée alimente l'analyse E1 et l'answer key ; les demandes courtes/simples passent directement (phases C-D by-passées, passage journalisé).
- **É5-ROUTAGE — décision mécanique de routage skills + agents (v3.47.0, Task 114 — directive trace 1a2025197d2a0e9d)** : à E5 (sélection des skills) et à E7 (écriture du plan — section « Routage »), exécuter `python3 skills/gen-plan/scripts/routage-skills-agents.py --tache "<demande normalisée>" --format json` : le script lit les frontmatters INSTALLÉS (description + read_when — source unique, zéro duplication R4, zéro lag KO-L004) et rend une recommandation compacte (skills scorés + verdict de complexité 5 critères) ; les skills recommandés alimentent la sélection E5 (croisement avec le registre KB et l'arbitre poids-chargement) ; les AGENTS ne sont recommandés QUE si le verdict est COMPLEXE (>= 2/5 critères — porte-garde §1.17) ; sortie consignée download/routage-dernier.json ; idempotent, < 1 s.
- **Routage (E5)** : skills-inventory en PRIORITÉ (`generate_skills_md.py --json`/`--search`/`--category`, comparaison mémorisée au KB) ; skill-finder-cn en FALLBACK si échec — contrôle `audit-provenance` AVANT adoption ; bascule unidirectionnelle.
### §1.17 Décision d'agents — porte de complexité et matrice dynamique (v3.47.0, Task 114)

La délégation à un agent (sous-agent = contexte plein — coût #token élevé) est JUSTIFIÉE uniquement dans les cas complexes : verdict COMPLEXE du script de routage (>= 2/5 critères : multi_livrables, multi_domaines >= 3 skills, horizon_long, parallele, integration_externe — grille alignée sur le PROMPT-GATEWAY §1.6). En dessous du seuil : skills directs, aucun agent (motif journalisé par le script — portegardes_agents).

| Agent | Cas justifiés (COMPLEXE requis) | Moteur de recommandation |
|-------|----------------------------------|--------------------------|
| agents écosystème (.agent installés) | Sous-tâches autonomes multi-phases d'un cas complexe — recommandation dérivée À L'EXÉCUTION du score objectif/modes des .agent | `routage-skills-agents.py` (matrice dynamique — R4, jamais de copie statique dans le corps) |

> La matrice des agents est DYNAMIQUE (objectifs .agent lus à l'exécution — source unique) : gen-plan ne duplique JAMAIS les descriptions d'agents dans son corps (R4) ; le verdict COMPLEXE est la PORTE, le score du script est le MOTEUR, la décision finale reste à E5/E7 avec l'arbitre poids-chargement (budget #token).
### §1.18 Règle FAIL-CLOSE — correction obligatoire des FAILS à la fermeture d'étape (v3.48.0 — règle créée v3.41.0 session web-f68de5ac, directive propriétaire 2026-11-08 trace 1a1bb8a4a78f2bfd : « ajoute une règle qui t'obliges à corriger les FAILS (même les non bloquantes) directement après la fermeture de l'étape du plan d'actions où elles ont été découvertes (journalise leur découverte dans un fichier) et intègre cette règle dans mon écosystème » ; renumérotée §1.18 au port v3.48.0 — §1.17 pris par la porte de décision d'agents Task 114)

- **Invariant (anti-report)** : une étape `T<k>.<j>.<i>` (et tout SG/Groupe qui la contient) ne peut PAS passer au statut `[TERMINÉ]` tant qu'elle détient au moins un FAIL ouvert — y compris les FAILS NON BLOQUANTS (avertissements, réserves, FAIL partiels de PASS AVEC RÉSERVES). Aucun report à une étape ultérieure, aucune liste « connu/non gênant » : la correction est IMMÉDIATE et s'achève AVANT la fermeture de l'étape où le FAIL a été découvert.
- **Journal obligatoire** : chaque découverte de FAIL est journalisée en append-only dans `<racine profil>/journal-fails.md` (une ligne par FAIL : horodatage ISO · Task ID · étape · source/arbitre émetteur · sévérité [BLOQUANT|NON-BLOQUANT] · verdict · correctif appliqué · horodatage de correction). L'entrée est FERMÉE à la correction (champs correctif + horodatage remplis) ; une étape ne peut être fermée que si TOUTES ses entrées journal sont fermées. Le journal n'est jamais écrasé ni élagué (R4/R5).
- **Boucle de correction** : FAIL découvert → JOURNALISER (découverte) → corriger → RE-VÉRIFIER par l'arbitre producteur du verdict (KO-L003 — même invariant, jamais ajuster la réalité) → JOURNALISER l'horodatage de correction → fermer l'étape. 2 échecs de correction consécutifs → escalade `[BLOQUÉ]` + diagnostic au worklog — jamais de clôture avec FAIL ouvert.
- **Portée** : tous les verdicts FAIL émis par arbitres mécaniques (answer-key-checker, check_plan_protocol, correct-work, validators, QA de livrables, tests) et contrôles manuels équivalents ; s'applique aussi aux sous-tâches/agents — un FAIL découvert dans une sous-tâche est remonté et journalisé sous le Task ID parent.

## §2 — Spécification technique

### §2.1 Stack

- **Langage** : Python (scripts), Markdown (documentation), YAML (frontmatter)
- **Environnement** : `skills/gen-plan/`
- **Pas de dépendance externe** (sauf intégration KB si activée)

### §2.2 Structure

```
skills/gen-plan/
├── SKILL.md                          # < 30 Kio — progressive disclosure
├── scripts/
│   ├── ensure-installed.py           # É1-INSTALL — préemption (v3.35.2) + garde réinjection plateforme (Task 114)
│   ├── routage-skills-agents.py      # É5-ROUTAGE — décision skills + agents (v3.47.0)
│   └── check_plan_protocol.py        # Arbitre E7-DISP — P1-P5 (v3.27.0)
├── references/
│   ├── etapes-detaillees.md          # 15 étapes + mode step
│   ├── grille-token.md               # Grille #token + contingences (v3.39.0)
│   ├── classification-types.md       # Routage Type 1-4
│   ├── profils-ressource.md          # NORMAL / ECO / VIEUX PC
│   ├── guide-selection-agent-skill.md # Arbre de décision
│   ├── prompt-engineering-kit.md     # PEK v4.1
│   ├── patterns-avances-qwen.md      # 5 patterns (N19)
│   ├── answer-key-b12.md             # Registre réel (N19)
│   ├── answer-key-template.md        # Schéma Answer Key (N20)
│   ├── graph-diamond-pattern.md      # Parallélisation par défaut
│   ├── observation-patterns.md       # Task Observer (N20)
│   ├── regles-or.md                  # Règles d'or + KO — intégraux (v3.39.0)
│   ├── disciplines-mobilisation.md   # Tables de mobilisation (v3.39.0)
│   ├── protocoles-detailles.md       # E1-RES/E7-DISP/§1.16/§5.5/#4 (v3.39.0)
│   └── journal-versions.md           # Journal — archive (v3.39.0)
└── evals/
    ├── evals.json                    # 9 evals
    └── trigger_evals.json            # 15 cas
```

### §2.3 Auto-calibration E15

| Écart estimé vs réel | Action |
|----------------------|--------|
| 0-20% | Aucune action |
| 20-35% | Ajustement de la grille (paramétrage fin) |
| >35% | Recalibration complète |

L'historique de calibration (11 entrées, rows 1-11) est maintenu dans `references/grille-token.md`.

### §2.4 Profils ressource

| Profil | Contexte | Règles clés |
|--------|----------|-------------|
| **NORMAL** | Par défaut | 15 étapes, tous les skills, surveillance complète |
| **ECO** | < 5 sessions, #token < 3500 | Étapes réduites, 1 checkpoint, pas de matrice dynamique KB |
| **VIEUX PC** | Matériel limité | Règles ECO + scripts < 100 lignes, pas de graphiques |

**Signaux de pression** (détectés à E2) :
- Espace disque < 5 Go (critique < 3 Go), Timeout 2+ consécutifs (critique 4+), Budget tokens > 80% (critique > 95%)
- **1 signal pression** → ECO. **2+ signaux** ou **1 critique** → VIEUX PC.

**Filtrage #token par profil** : NORMAL = aucun filtre. ECO = exclut > 8000 #token. VIEUX PC = exclut > 5000 #token.

> Détail complet : `references/profils-ressource.md`

### §2.5 Intégration KB

Si activé : consultation de `{{KB_PATH}}`, scan du registre pour identifier les skills pertinents (Protocole de Découverte SHARED §2.3), enrichissement à E15. Environnement bac à sable : registre minimal `skills/KNOWLEDGE.md` (skills écosystème installés), extensible à chaque matérialisation.

---

## §3 — Relations

| Avec | Nature | Détails |
|------|--------|--------|
| correct-work | Invocation à E1 + hook E8 + contrôle par phase | Validation du plan initial + vérification post-plan et à chaque phase terminée (E9-E14), version >= v2.4.0 |
| clone-chat | Calibration + archivage | E4, E15, optionnel, version >= v2.0.0 |
| skills-inventory | Routage prioritaire de découverte (§1.16) + consultation à E5 | Sélection des skills, version >= v1.1.0 |
| skill-finder-cn | Fallback de découverte (§1.16) | Recherche externe UNIQUEMENT si skills-inventory échoue — contrôle cybersécurité audit-provenance obligatoire avant adoption |
| prompt-engineering | Délégation (§1.6) | Optimisation des prompts complexes, version >= v1.0.0 |
| agent-prompt-engineering | Pré-traitement (É1-PROMPT-GATEWAY §1.16) + délégation (§1.6/§1.9) | PROMPT-GATEWAY inconditionnel v1.2.0 — réécriture des demandes complexes AVANT l'analyse E1 ; optimisation fine des prompts (SHARED §3.1) — version >= v1.2.0 |
| agents écosystème (4 .agent) | Délégation porte-gardée (§1.17) | Recommandation dérivée à l'exécution par routage-skills-agents.py — verdict COMPLEXE >= 2/5 requis ; matrice dynamique R4 |
| context-engineering | Mobilisation (§1.6) | Socle SHARED, Protocole de Découverte KB, lecture bloc par bloc — déclenchement automatique (SHARED §7) |
| loop-engineering | Mobilisation (§1.6) | Boucle E10-E13 + auto-calibration E15 — déclenchement automatique (SHARED §7) |
| graph-engineering | Mobilisation (§1.6) | Registre KB graphe bidirectionnel versionné, matrice agent × skill — déclenchement automatique (SHARED §7) |
| harness-engineering | Mobilisation (§1.6) | Profils ressource, hooks E8 + E9-E14, arbitres, worklog — déclenchement automatique (SHARED §7) |
| spec-driven-development | Détention orchestrée (SHARED §7, registre décentralisé §8 du skill) | Cadrage spec-first à E4, re-validation à E7 — version >= v1.0.0 |
| memory-engineering | Détention orchestrée (SHARED §7, registre décentralisé §8 du skill) | État Long obligatoire aux exécutions longues, compaction/reprise — version >= v1.1.0 |
| fleet-engineering | Détention orchestrée (SHARED §7, registre décentralisé §8 du skill) | Choix du pattern et des bornes à E5/E7, Graph Diamond — version >= v1.0.0 |
| refactoring-engineering | Mobilisation n°55 (SHARED §7, bloc PATTERN:GEN-PLAN-REFACTORING-v1.0.0) | Conception/exécution des opérations de refactoring (E4/E7 + situations E9-E14) — version >= v1.0.1 |
| refactor-guard | Garde-fous de refactoring (fusion discussion 468a4c26 — lignée externe v1.7.0) | Mobilisé par refactoring-engineering pendant les opérations à risque (score H01-H15, sandbox, rollout) ; détection de besoins (hook E13) — version >= v1.7.0 |
| refactoring-test | Outil n°55 (SHARED §7, bloc PATTERN:GEN-PLAN-REFACTORING-v1.0.0) | Détection/évaluation + graphe d'interactions (blast radius) — verdict machine, version >= v1.0.1 |
| agent-engineering | Mobilisation n°56 (SHARED §7, registre décentralisé §8 du skill) | Cadrage/routage des tâches d'agents (ABE/AE/MASE) — version >= v1.0.0 |
| knowledge-observer | Invocation à E15 (§1.2bis) | Observation post-session (modes M1-M2) ; les modes M3-M4 exigent un verdict correct-work — version >= v1.0.0 |
| resource-monitor | Mobilisation hook E1-RES (§1.2bis) + E6 (profilage) + hook continu E9-E14 (checkpoint E11 et entre vagues — v3.31.0) | Collecte G-RES — verdict OK/PRESSION/CRITIQUE → mode d'exécution/profil/bascule, version >= v1.0.0 |
| answer-key | Arbitrage E7/E8 (§1.2bis) | Décisions E1 vérifiables mécaniquement — arbitre answer-key-checker.py (16 checks) |
| knowledge.md | Enrichissement à E15 | Mise à jour registre et calibration |
| orchestration-disciplines | Hook É5-DISCIPLINES (v3.49.0) + protocole d'évolution | Décision de mobilisation des disciplines (routage-disciplines.py — tables sources `references/disciplines-mobilisation.md` R4) + re-injection des résultats vérifiés des tâches parallèles aux checkpoints E11 et frontières de groupes — version >= v1.0.0 |

---

## §4 — Grille #token

Résumé des plages clés (voir `references/grille-token.md` pour la grille complète) :

- **Planification E1-E2** : 800-1500 #token
- **Exécution simple (1 skill)** : 2000-5000 #token
- **Exécution complexe (4+ skills)** : 10000-20000 #token
- **Coefficients** : 0.8x (faible) → 1.5x (critique), ECO 0.7x, VIEUX PC 0.5x
- **Contingences (preuves : `references/grille-token.md`)** : **profil frais local ×3-4** (première exécution sur profil restauré — coût de DÉCOUVERTE hors grilles calibrées, v3.28.1) ; **appels API en masse ×2-3** (429/backoff — ThreadPool 2-4 workers, throttle 1-2 s, reprise par lots, petits d'abord) ; **récupération externe bloquée ×3-4** (WAF/SPA/rate-limit — escalade WebFetch → curl → agent-browser → z-ai `page_reader`, budget propre AVANT l'étape requérante, v3.28.2).
- **Routage É5-ROUTAGE (v3.47.0)** : ~300 #token par plan (exécution script + intégration section Routage) — sortie JSON ~1-2 Kio, < 1 s ; économie nette : le catalogue des déclencheurs N'EST PAS incrusté dans le corps (R4 + poids gen-plan maîtré sous le seuil CRITIQUE 60 Kio).

---

## §5 — Conventions

### §5.1 Nommage

- Répertoires et fichiers : kebab-case (`gen-plan`, `etapes-detaillees.md`)
- Versions : semver (`3.7.0`)
- Tags : préfixe `#` (`#token 3500`)
- Variables : double accolades (`{{SKILLS_ROOT}}`)

### §5.2 Python uniquement (N3)

Tous les scripts générés en Python. Aucun script shell (bash, sh, powershell). Portabilité cross-platform garantie.

### §5.3 Tagging #token (N1)

Chaque étape du plan et chaque skill utilisé reçoit un tag `#token` indiquant le coût estimé. La grille est auto-calibrée à E15.

### §5.4 Hook correct-work par phase ET par étape — mode NULL, granularité étape (v3.44.0)

Dès qu'une phase du plan d'actions se termine, lancer `correct-work(livrables de la phase, mode=CIBLE)` AVANT la phase suivante : PASS → suivante ; PASS AVEC RÉSERVES → réserves au worklog, exécution continue ; FAIL → pause, correction, re-vérification. Le hook E8 reste la vérification finale.

**Mode NULL, granularité étape (v3.44.0)** : lorsqu'une ÉTAPE du plan d'actions est terminée, lancer `correct-work(livrables de l'étape, mode=CIBLE)` AVANT l'étape suivante — le statut `verified` de l'entrée d'answer key correspondante est subordonné au verdict CIBLE (KO-L003 : statuts fixés par l'exécution, jamais à la main).

**Complément FAIL-CLOSE (v3.48.0, §1.18)** : ce hook ne clôt jamais une étape portant un FAIL ouvert — même non bloquant — sans correction immédiate + entrée fermée dans `journal-fails.md`.

### §5.5 Mode step — structure hiérarchique et état d'avancement (résumé — intégral : `references/protocoles-detailles.md`)

**Couche d'organisation transverse (v3.25.0, tous modes depuis v3.36.0 — seule différence : les portes de confirmation, EXCLUSIVES au mode step-ok — v3.45.0 : les modes step et NULL n'en demandent JAMAIS)** : **groupe `G<k>`** (unité de vérification — correct-work(groupe)) → **sous-groupes `SG<k>.<j>`** (lot cohérent 2-5 tâches) → **tâches `T<k>.<j>.<i>`** (unité élémentaire, tag #token). **Statuts dérivés de l'état vérifiable** (KO-L003) : `[À FAIRE]` · `[EN COURS]` · `[TERMINÉ]` · `[BLOQUÉ]` · `[REPORTÉ]` ; compteurs n/m. **Cadence** : début d'exécution → fenêtre native complète (E7-DISP point 6 — Z.ai : `TodoWrite`) ; ouverture de groupe → PLAN-AFFICHE d'évolution puis tableau du groupe (step-ok : après confirmation) ; fin de tâche → ligne + compteurs ; fin de sous-groupe → rappel ; fin de groupe → fenêtre native mise à jour ; clôture → tableau final + verdict correct-work(groupe). **Orthogonal à l'exécution** : couche de LECTURE ; Graph Diamond automatique dès preuve d'indépendance (sous-groupes inclus, série = exception tracée) ; groupes plats normalisés à l'ouverture (R6/R2).
### §5.6 Journal des versions (entrée courante — archive intégrale et mécanique de migration : `references/journal-versions.md`)

- **v3.49.0 (2026-11-28, web-220878ed — Task 12, directive propriétaire trace 1a21e208f489f7f5 : « analyse mon skill gen-plan et son système de réinstallation … qu'il fasse appel à mon fichier PM INSTALL pour ré-installer les éléments de mon écosystème qui sont indispensables et adaptés à l'exécution … du plan d'actions à chaque nouvelle requête » + « génère des skills ou des agents spécialisés … pour que toutes ces disciplines s'exécutent et s'orchestrent »)** : É1-INSTALL étendu — garde à TOUTE invocation (chaque nouvelle requête, plus seulement l'ouverture de session) + point d'entrée AMORÇABLE (shim scripts/ensure-installed.py → repli bootstrap canonique PM-INSTALL §3.2-d v1.10.7 — fin de l'œuf-et-la-poule) + réinstallation des éléments INDISPENSABLES ADAPTÉS au plan (fermeture MINIMALE + skills routés É5-ROUTAGE, jamais l'arbre complet sauf directive — verdict INSTALLE-POUR-PLAN) + SEEDS-FIRST ; hook **É5-DISCIPLINES** : orchestration-disciplines v1.0.0 (routage-disciplines.py → section « Orchestration des disciplines » du plan : mobilisation par étape + protocole d'évolution — nouvelles requêtes E13 règle d'or n°3 + re-injection MÉCANIQUE des résultats vérifiés des tâches parallèles aux checkpoints E11 et frontières de groupes, scan disque KO-L003) ; dependencies += orchestration-disciplines >= 1.0.0 ; §3 relations += orchestration-disciplines ; **précision propriétaire trace 1a21e38435b96641 (E13 en vol — audit de déduplication rôles/objectifs)** : alignement règle d'or n°9 (rétablissement GRADUÉ — fermeture MINIMALE adaptée au plan quand les piliers sont sains, voie complète 4 temps conservée sinon ; n°9 = règle source, É1-INSTALL = implémentation — note de raffinement appendée à references/regles-or.md) + correctif placement de la ligne É5-DISCIPLINES dans le tableau §1.2bis + frontière documentée sweep-entetes-shared.py (RÉPARATION §0 au bootstrap) ↔ sync-context-block.py (INJECTION §0 à la génération — PM-INSTALL §3.2-c v1.10.8) + non-doublons consignés au plan (routage-disciplines ↔ routage-skills-agents : disciplines/tables sources vs skills/frontmatters ; orchestration-disciplines ↔ agent-engineering/fleet-engineering/resource-monitor/orchestrateur-tsi — garde §1.4). MINOR, additions pures (non-régression triggers). Cascade KO-L004 : PM v3.49.0 généré mécaniquement (delta verrouillé scripts/delta-genplan-v3490.json) + KB + v3.48.0 migrée R4 byte-identité references/journal-versions.md + PM v3.48.0 archivé @historique + pin ECO_SKILLS recalibré + certification.
