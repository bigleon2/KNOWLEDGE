---
name: gen-plan
version: 3.39.0
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
  progressive disclosure R1 (v3.39.0) : résumés inline, intégraux en references/ à la demande
dependencies:
  - skill: correct-work
    version: ">=2.4.0"
    used_at: "E1, E8 hook, contrôle par phase"
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
- `gen-plan(step) : <instructions>` — enchaînement autonome des groupes séquentiels du plan d'actions, correct-work(groupe) après chaque groupe (max 2 rounds de correction), correct-work(projet) en fin de chaîne (v3.22.0) ; à l'ouverture de chaque groupe : vue d'évolution PLAN-AFFICHE (E7-DISP v3.36.0 — tous modes)
- `gen-plan(step-ok) : <instructions>` — identique au mode step avec demande de confirmation du propriétaire avant chaque groupe (nom canonique v3.22.1) ; alias `step-confirm` (v3.22.0) et `step-confim` normalisés en `step-ok` (R4) ; **clause mode NULL** — toute invocation sans `<mode>` explicite (`gen-plan : <instructions>`, ex. « gen-plan : continue ») conserve le comportement antérieur à l'introduction des modes step/step-ok (v3.21.0) : intégration E13 ou exécution classique, sans portes de confirmation (directive propriétaire 2026-10-11) ; tout autre mode → clarification demandée, jamais d'invention de mode (R2)
- `orchestre` — orchestration multi-agents
- Toute demande impliquant plusieurs étapes séquentielles avec des livrables
- `gen-plan:generate(<description>)` — génération d'un plan auto-exécutable

## §0 — Contexte Système (SHARED v1.7.34)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.
> Langue : FRANÇAIS exclusif pour tous les échanges avec le propriétaire (règle d'or n°6 gen-plan — directive 2026-10-31, renforcée 2026-11-06) : dès le PREMIER mot de toute session ou reprise, la langue d'un message, d'un résumé de continuation ou d'un canal ne dérive JAMAIS la réponse ; toute dérive est corrigée immédiatement.
> Règles d'or & lecture SHARED à l'exécution (directive propriétaire 2026-11-06 — SHARED §9) : tout skill/agent/script exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or de l'écosystème (résumé §9 — canonique gen-plan §1.5).
> Référence canonique skill/agent (directive propriétaire 2026-11-07 — SHARED §0/§1.2) : toute référence à « mon skill X »/« mon agent X » désigne la forme installée à la racine `skills/X/SKILL.md`, JAMAIS le prompt maître du corpus `@mon-ecosysteme/` (ex-nommé `@PM-SKILLS/`) — les PMs sont des spécifications générées mécaniquement (KO-L004), les skills installés sont les formes exécutables.

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
| **Graph Diamond** | **E9-E14** | Parallélisation PAR DÉFAUT des tâches ET commandes prouvées indépendantes (le série est l'exception justifiée — philosophie #4 v3.24.0, extension aux commandes v3.32.0) — tracée au worklog | `references/graph-diamond-pattern.md` |
| **Observer** | **E15** | Invoque knowledge-observer en modes M1-M2 (observation + analyse post-session) ; les modes M3-M4 exigent un verdict correct-work | `references/observation-patterns.md` |
| **E5-POIDS — arbitre de poids de chargement** | **E5** (v3.38.0) | À la sélection des skills (E5), l'arbitre `scripts/poids-chargement.py` (recommandation R1 de l'étude de faisabilité Task 70 — le goulot réel de l'écosystème est le budget #token) mesure le poids de chargement (Kio + #token estimés = caractères/4) ; un skill CRITIQUE (≥ 60 Kio) ou LOURD (≥ 30 Kio) déclenche la voie lecture ciblée : §0 Contexte Système + sommaire d'abord, sections dédiées ensuite, `references/` chargées à la demande — JAMAIS de lecture intégrale par défaut pour un skill LOURD/CRITIQUE | `scripts/poids-chargement.py` |
| **R2-CACHE — cache de verdicts** | **E9-E14** (v3.38.0) | Les graders coûteux (arbitres, harnais, batteries) ré-exécutés à entrées inchangées passent par `scripts/cache-verdicts.py` (recommandation R2 de l'étude Task 70) : verdict figé une fois (rc + stdout + durée), re-jeu sans ré-appel (démo mesurée : gain 440×), invalidation automatique par état des fichiers cibles (taille/mtime), `--force` pour re-vérification réelle — un verdict figé n'est JAMAIS une preuve en soi, la re-exécution reste disponible à la demande | `scripts/cache-verdicts.py` |

<!-- FIN-PATTERN:GEN-PLAN-HOOKS-PATTERNS-v1.0.0 -->

<!-- RÉSUMÉ v3.39.0 — intégraux : references/protocoles-detailles.md -->

**Hook E1-RES — ouverture de session (4 vérifications AVANT analyse)** : (1) lecture seule préalable B-11 (worklog/plan/arbitres) ; (2) collecte G-RES (`monitor.py` : OK/PRESSION/CRITIQUE, journalisé) ; (3) fraîcheur du plan (modifiée et valide → re-généré avant reprise) ; (4) garde post-coupure (règle d'or n°9 : piliers + integrity → rétablissement auto). **Reprise (v3.27.0)** : message pendant un plan en vol → worklog + fraîcheur + E13 + E8 + R5 + affichage ; état « en vol » dérivé du DISQUE (RC3).

**Hook E7-DISP — affichage obligatoire (6 points, garde bloquante)** : (1) plan écrit `download/` ; (2) answer key >= 1 décision ; (3) E8 aux horodatages COUPLÉS (toute écriture = re-validation) ; (4) worklog R5 + marqueur `PLAN-AFFICHE` ; (5) bloc récapitulatif AU chat. Garde `check_plan_protocol.py` (P1-P5) ; affichage REJOUABLE ; ouverture d'étape (v3.36.0, tous modes) : PLAN-AFFICHE d'évolution au début de chaque groupe G<k> (statuts du disque ; step-ok : après confirmation). **(6) Fenêtre native (v3.39.0 — directive 1a1b7fe1c7238e8d)** : fenêtre des étapes du plan via le mécanisme NATIF de l'agent dédié à ce rôle (Z.ai : liste de tâches `TodoWrite`/`TodoRead`) — affichée au DÉBUT de l'exécution du plan d'actions, MISE À JOUR à chaque FIN d'étape ; intégral : `references/protocoles-detailles.md` (point 6).

### §1.3 Normes

- **N1 — Tagging #token** : chaque étape et skill reçoit un tag `#token` avec le coût estimé. Grille auto-calibrée après exécutions.
- **N2 — Snippets** : snippets de code réutilisables générés pendant l'exécution, tagués et versionnés.
- **N3 — Python uniquement** : tous les scripts générés doivent être en Python (aucun bash/sh/powershell).

### §1.4 Philosophie clés

1. **Read before planning** — Toujours lire le projet avant de planifier.
2. **Performance-driven sélection** — Le choix skill/agent est dicté par le gain de performance.
3. **Skills can launch specialized agents** — Modèle à deux couches : Skill → Agent Spécialisé.
4. **Parallélisation par défaut des tâches ET des commandes sur preuve d'indépendance** (v3.24.0/v3.32.0) — vagues indépendantes prouvées en PARALLÈLE : Graph Diamond automatique (E9-E14), série = exception tracée ; dégradation gracieuse 429 — intégral : `references/protocoles-detailles.md` (#4).
5. **Visible progress** — L'utilisateur sait toujours où on en est.
6. **CoT + Chaining avec auto-correction** — Raisonnement structuré avant chaque action.
7. **Lecture bloc par bloc** — Fichiers > 500 lignes : lire par blocs successifs (limit/offset), produire une synthèse intermédiaire entre chaque bloc. Ne jamais lire un fichier > 500 lignes d'un seul coup. Voir `references/profils-ressource.md` (VIEUX PC règle 4 : troncature 500 lignes).
8. **Downgrade irréversible** — Le profil ressource ne remonte jamais automatiquement.

### §1.5 Règles d'or (résumé opérationnel — intégral : `references/regles-or.md` ; miroir SHARED §9)

| N° | Règle | Portée |
|----|-------|--------|
| 1 | **Adaptation autonome** | Blocage = adaptation journalisée, jamais d'arrêt implicite ; pause explicite si inatteignable. |
| 2 | **Régénération post-installation** | Écosystème installé → plan re-généré via le gen-plan installé (R2). |
| 3 | **Mise à jour à chaque demande** | E13 (extension, jamais réécriture) ; « intègre dans le plan d'actions » = extension en place ; « met à jour » = NOUVEAU plan consolidé $FACON2. |
| — | **Modes** | `step` : chaîne par groupes ; `step-ok` : + confirmation ; NULL : comportement antérieur ; autre mode → clarification (R2). |
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

- **Mobilisation** : tables E1-E8, n°54-55, E15, par déclencheur × modes — intégrales : `references/disciplines-mobilisation.md` ; socle commun (context/loop/graph/harness + PEK) à tout déclencheur du §A. **Hook continu E9-E14** : G-RES à chaque checkpoint E11 et entre vagues ; PRESSION → ECO, CRITIQUE → série/PAUSE. gen-plan = détenteur principal de la méthode prompt-engineering (SHARED §7 ; PEK v4.1).
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

### §1.15 Leçons knowledge-observer — recalibrage croisé (résumé — intégral : `references/regles-or.md`)

- **KO-L004 — Recalibrage croisé + génération PM** : toute montée de version → AVANT certification : recalibrage des outils dépendants (arbitres, pre-checks, skills-meta, run-order, SYNC_MAP, miroir, archive) + génération mécanique du PM (`scripts/generer-pm-skill.py`, substitutions verrouillées, R2).
- **KO-L007 — Matérialisation d'abord** : `git sparse-checkout list` + test d'existence AVANT toute écriture et tout verdict naïf ; « non matérialisé » ≠ « échec ».

> Saut §1.8 → §1.14 intentionnel (Task 21 A7).
### §1.16 Routage de découverte des skills + garde d'installation (résumé — intégral : `references/protocoles-detailles.md`)

- **É1-INSTALL — garde avec PRÉEMPTION** : à l'ouverture de session, AVANT E1 : `ensure-installed.py --check` (chemin canonique). rc=0 → no-op ; rc≠0 → suspension de toute tâche + `--reinstall` (pipeline PM-INSTALL, clone éphémère) AVANT toute autre étape ; directive post-réinstallation intégrée au plan ; idempotente. **v3.35.2** : contrôle du SKILL.md de toutes les entrées KB ; manquants → AUTO-RÉPARÉS depuis le miroir (INSTALLE-REPARÉ, rc=0, trace worklog).
- **Routage (E5)** : skills-inventory en PRIORITÉ (`generate_skills_md.py --json`/`--search`/`--category`, comparaison mémorisée au KB) ; skill-finder-cn en FALLBACK si échec — contrôle `audit-provenance` AVANT adoption ; bascule unidirectionnelle.
## §2 — Spécification technique

### §2.1 Stack

- **Langage** : Python (scripts), Markdown (documentation), YAML (frontmatter)
- **Environnement** : `skills/gen-plan/`
- **Pas de dépendance externe** (sauf intégration KB si activée)

### §2.2 Structure

```
skills/gen-plan/
├── SKILL.md                          # < 30 Kio — progressive disclosure (v3.39.0)
├── scripts/
│   ├── ensure-installed.py           # É1-INSTALL — préemption (v3.35.2)
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
| knowledge-observer | Invocation à E15 (§1.2bis) | Observation post-session (modes M1-M2) ; les modes M3-M4 exigent un verdict correct-work — version >= v1.0.0 |
| resource-monitor | Mobilisation hook E1-RES (§1.2bis) + E6 (profilage) + hook continu E9-E14 (checkpoint E11 et entre vagues — v3.31.0) | Collecte G-RES — verdict OK/PRESSION/CRITIQUE → mode d'exécution/profil/bascule, version >= v1.0.0 |
| answer-key | Arbitrage E7/E8 (§1.2bis) | Décisions E1 vérifiables mécaniquement — arbitre answer-key-checker.py (16 checks) |
| knowledge.md | Enrichissement à E15 | Mise à jour registre et calibration |

---

## §4 — Grille #token

Résumé des plages clés (voir `references/grille-token.md` pour la grille complète) :

- **Planification E1-E2** : 800-1500 #token
- **Exécution simple (1 skill)** : 2000-5000 #token
- **Exécution complexe (4+ skills)** : 10000-20000 #token
- **Coefficients** : 0.8x (faible) → 1.5x (critique), ECO 0.7x, VIEUX PC 0.5x
- **Coefficients de contingence (détail et preuves : `references/grille-token.md`)** : **profil frais local ×3-4** (première exécution sur profil restauré — coût de DÉCOUVERTE hors grilles calibrées, v3.28.1) ; **appels API en masse ×2-3** (429/backoff — ThreadPool 2-4 workers, throttle 1-2 s, reprise par lots, petits d'abord) ; **récupération externe bloquée ×3-4** (WAF/SPA/rate-limit — escalade WebFetch → curl → agent-browser → z-ai `page_reader`, budget propre AVANT l'étape requérante, v3.28.2).

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

### §5.4 Hook correct-work par phase (E9-E14)

Dès qu'une phase du plan d'actions se termine, lancer `correct-work(livrables de la phase, mode=CIBLE)` AVANT la phase suivante : PASS → suivante ; PASS AVEC RÉSERVES → réserves au worklog, exécution continue ; FAIL → pause, correction, re-vérification. Le hook E8 reste la vérification finale.

### §5.5 Mode step — structure hiérarchique et état d'avancement (résumé — intégral : `references/protocoles-detailles.md`)

**Couche d'organisation transverse (v3.25.0, tous modes depuis v3.36.0 — seule différence : les portes de confirmation)** : **groupe `G<k>`** (unité de vérification — correct-work(groupe)) → **sous-groupes `SG<k>.<j>`** (lot cohérent 2-5 tâches) → **tâches `T<k>.<j>.<i>`** (unité élémentaire, tag #token). **Statuts dérivés de l'état vérifiable** (KO-L003) : `[À FAIRE]` · `[EN COURS]` · `[TERMINÉ]` · `[BLOQUÉ]` · `[REPORTÉ]` ; compteurs n/m. **Cadence** : début d'exécution → fenêtre native complète (E7-DISP point 6 — Z.ai : `TodoWrite`) ; ouverture de groupe → PLAN-AFFICHE d'évolution puis tableau du groupe (step-ok : après confirmation) ; fin de tâche → ligne + compteurs ; fin de sous-groupe → rappel ; fin de groupe → fenêtre native mise à jour ; clôture → tableau final + verdict correct-work(groupe). **Orthogonal à l'exécution** : couche de LECTURE ; Graph Diamond automatique dès preuve d'indépendance (sous-groupes inclus, série = exception tracée) ; groupes plats normalisés à l'ouverture (R6/R2).
### §5.6 Journal des versions (entrée courante — archive intégrale et mécanique de migration : `references/journal-versions.md`)

- **v3.39.0 (2026-11-08, web-ecef7f80 — Task 72 G1, directives « Chantier R1 : re-curation progressive disclosure de gen-plan » + complémentaires 1a1b7b297b4975 [skill re-curation par script] et 1a1b7fe1c7238e8d [fenêtre native AFFICHE-PLAN])** : 9 blocs déplacés R4 byte-identité vers `references/` + append contingences (grille-token.md) — résumés NOUVEAUX inline, zéro duplication ; contrats baseline golden master + vérif POST (T1.1.0) ; lecture ciblée = état par défaut (E5-POIDS) ; **E7-DISP point 6 « fenêtre native »** (Z.ai : liste de tâches `TodoWrite`/`TodoRead` — début d'exécution + chaque fin d'étape) : intégral `references/protocoles-detailles.md`. MINOR. Cascade KO-L004 : SG1.4 (worklog Task 72).
