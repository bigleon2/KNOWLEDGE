---
name: gen-plan
version: 3.19.0
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
  Graph Diamond E9-E14, knowledge-observer E15),
  déclencheur verbatim « intègre dans le plan d'actions » (E13 — règle d'or n°3)
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
  - Déclencher si la demande mentionne : planification, adaptation, answer
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

## §0 — Contexte Système (SHARED v1.6.4)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (exception)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.
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
| **Graph Diamond** | **E9-E14** | Parallélisation exceptionnelle des actions indépendantes (défaut : série, philosophie #4) — tracée au worklog | `references/graph-diamond-pattern.md` |
| **Observer** | **E15** | Invoque knowledge-observer en modes M1-M2 (observation + analyse post-session) ; les modes M3-M4 exigent un verdict correct-work | `references/observation-patterns.md` |

<!-- FIN-PATTERN:GEN-PLAN-HOOKS-PATTERNS-v1.0.0 -->

<!-- PATTERN:GEN-PLAN-HOOKS-E1-RES-v1.0.0 -->

**Hook E1-RES — ouverture de session (n67-1, reconstitué post-wipe — v3.17.0, N28)** : l'étape E1 ouvre par trois vérifications préalables, AVANT toute analyse : (1) **lecture seule préalable B-11** (règle D008 — état du worklog, du plan et des arbitres fait foi) ; (2) **collecte G-RES** via `skills/resource-monitor/scripts/monitor.py --state-file tmp/resource-monitor-state.json` (fonction de surveillance permanente §1.14 — verdict OK/PRESSION/CRITIQUE → mode d'exécution, décision journalisée) ; (3) **contrôle de fraîcheur du plan** (règle L005/D012 — si gen-plan a été modifiée et jugée valide depuis la génération du plan courant, le plan est re-généré AVANT toute reprise). Provenance : le hook n67-1 de la session B12 est PERDU au wipe inter-sessions (constat d'honnêteté Task 44) ; cette reconstitution est tracée comme telle (B13-r6, N28 — aucun faux lignage).

<!-- FIN-PATTERN:GEN-PLAN-HOOKS-E1-RES-v1.0.0 -->

### §1.3 Normes

- **N1 — Tagging #token** : chaque étape et skill reçoit un tag `#token` avec le coût estimé. Grille auto-calibrée après exécutions.
- **N2 — Snippets** : snippets de code réutilisables générés pendant l'exécution, tagués et versionnés.
- **N3 — Python uniquement** : tous les scripts générés doivent être en Python (aucun bash/sh/powershell).

### §1.4 Philosophie clés

1. **Read before planning** — Toujours lire le projet avant de planifier.
2. **Performance-driven sélection** — Le choix skill/agent est dicté par le gain de performance.
3. **Skills can launch specialized agents** — Modèle à deux couches : Skill → Agent Spécialisé.
4. **Serial exécution by DEFAULT** — Tâches UNE À LA UNE. Parallélisme INTERDIT sauf demande explicite.
5. **Visible progress** — L'utilisateur sait toujours où on en est.
6. **CoT + Chaining avec auto-correction** — Raisonnement structuré avant chaque action.
7. **Lecture bloc par bloc** — Fichiers > 500 lignes : lire par blocs successifs (limit/offset), produire une synthèse intermédiaire entre chaque bloc. Ne jamais lire un fichier > 500 lignes d'un seul coup. Voir `references/profils-ressource.md` (VIEUX PC règle 4 : troncature 500 lignes).
8. **Downgrade irréversible** — Le profil ressource ne remonte jamais automatiquement.

### §1.5 Règles d'or (PM v3.7.0 §1.8)

**Règle d'or n°1 — Adaptation autonome** : tout blocage (timeout répété, ressource épuisée, fichier absent, wipe inter-sessions, dépendance indisponible, sortie d'outil perdue) est traité comme un signal d'adaptation, jamais comme un arrêt implicite. Le contournement reste conforme aux conventions (SHARED §1) et à la philosophie §1.4 ; chaque adaptation est journalisée au worklog (cause, solution retenue, coût #token) ; l'objectif final ne change pas, seuls les moyens s'ajustent — si l'objectif devient inatteignable, la pause est explicite et motivée.


**Règle d'or n°2 — Régénération du plan après installation d'un écosystème** (PM v3.11.0 §1.8) : dès qu'un nouvel écosystème est installé, le plan d'actions actuel est régénéré de façon cohérente via le nouveau skill gen-plan — modes, étapes, règles d'or et hooks réalignés sur la version installée, tags #token recalculés si la grille a évolué, régénération journalisée au worklog ; l'objectif final est inchangé (non-régression R2 des étapes terminées).

<!-- PATTERN:KO-L005-v1.0.0 -->

**Règle KO-L005 — Généralisation de la règle d'or n°2 : re-génération à chaque version de gen-plan modifiée et jugée valide** (leçon L005, validée — v3.17.0, N23-b/N28) : chaque fois que gen-plan est modifié et jugé valide par arbitres mécaniques AVANT toute action (jamais par présomption — L003), le plan d'actions actuel est re-généré via la nouvelle version ; la boucle complète est : arbitres → montée de version → recalibrage croisé (L004) → re-certification → re-génération du plan via la nouvelle version → re-validation E8. Première application : plan B13-r5 via v3.16.0 (directive trace `1a0dfe43940ae0c5`) ; matérialisation : ce bloc (montée v3.17.0, session B13-r6).

<!-- FIN-PATTERN:KO-L005-v1.0.0 -->

**Règle d'or n°3 — Mise à jour du plan à chaque nouvelle demande** (PM v3.11.0 §1.8) : toute nouvelle demande utilisateur pendant l'exécution d'un plan déclenche la mise à jour cohérente du plan d'actions actuel via gen-plan (E13) — demandes intégrées comme étapes/priorités, ré-estimation #token des étapes affectées, re-validation E8 si le périmètre change matériellement, journalisation au worklog ; extension du plan, jamais réécriture destructrice (R2). **Déclencheur verbatim (v3.17.2, directive propriétaire 2026-10-02)** : la formulation « intègre dans le plan d'actions » (et variantes directes : « intègre ça au plan », « ajoute au plan d'actions ») déclenche ce mode E13 sans ambiguïté.

### §1.6 Disciplines d'ingénierie de prompts (PM v3.12.0 §1.9)

| Discipline | Mécanisme gen-plan |
|------------|--------------------|
| **Context engineering** | Socle SHARED lu en premier ; lecture bloc par bloc avec synthèses intermédiaires |
| **Loop engineering** | Boucle E10-E13 (exécution → surveillance → écart → ajustement) ; auto-calibration E15 |
| **Graph engineering** | Registre KB = graphe de relations bidirectionnelles versionnées ; matrice agent × skill |
| **Harness engineering** | Profils ressource + signaux de pression ; hook E8 correct-work + contrôle par phase (E9-E14) ; worklog structuré |

**Table de mobilisation E1-E8 (v3.12.0)** — disciplines mobilisées par étape de planification (audit N5-a : interprétation PEK E1-E3 conforme, génération E4-E8 explicitée) :

| Étape | Disciplines mobilisées | Mécanisme |
|--------|------------------------|-----------|
| E1 | prompt-engineering (PEK) ; context-engineering | Interprétation CoT/Chaining/Hybride (E1-E3) ; lecture SHARED/KB préalable |
| E2 | context-engineering ; graph-engineering | Lecture bloc par bloc + synthèses intermédiaires ; Protocole de Découverte KB |
| E3 | prompt-engineering (PEK) | Blocs de sortie adaptatifs A-J mappés sur les Types 1-4 |
| E4 | harness-engineering | Grille #token, budgets, filtrage par profil |
| E5 | graph-engineering ; context-engineering | Graphe KB (matrice agent × skill) ; scan du registre |
| E6 | harness-engineering | Profils NORMAL/ECO/VIEUX PC, signaux de pression |
| E7 | loop-engineering ; context-engineering ; harness-engineering | Boucles R3 prédéfinies (règle d'or n°1) ; plan auto-suffisant ; hooks par phase E9-E14 |
| E8 | harness-engineering ; prompt-engineering (PEK) | Hook correct-work (3 verdicts) ; 12 checks PEK (scoring 22/25) |

L'optimisation fine des prompts complexes est déléguée au skill `prompt-engineering` (SHARED §3.1).

**Méthode prompt-engineering (méthode-mère)** : gen-plan est le détenteur principal de la méthode prompt-engineering (définitions : SHARED §7 ; orchestration : PM v3.12.0 §1.9) ; les autres skills de l'écosystème la détiennent en tant que **fonction héritée** (registre d'assignation : SHARED §7).

**Méthode de raisonnement adaptative PEK (v3.11.0, PM §1.9)** : gen-plan mobilise le Prompt Engineering Kit v4.1 (méthode pure) comme couche de raisonnement opérationnelle — 3 modes d'exécution (CoT 7 étapes / Chaining 4 étapes / Hybride à bascule automatique selon la complexité E1-E3) alignés sur la philosophie §1.4 #6 et calibrés par les profils §2.4 ; blocs de sortie adaptatifs A-J mappés sur les Types 1-4 (E3) ; 9 règles critiques + 12 checks de validation (scoring 25 pts, seuil 22/25) intégrés aux hooks correct-work par phase (E9-E14). Contenu opérationnel : `references/prompt-engineering-kit.md`.

**Matérialisation des disciplines (état A12, mise à jour session A13)** : les 4 disciplines d'exécution sont matérialisées en skills complets à déclenchement automatique (`context-engineering`, `loop-engineering`, `graph-engineering`, `harness-engineering` — SKILL.md + evals + trigger_evals ; les matérialisations agent intermédiaires `_disciplines/` A11 et `gen-plan.agent` A9 sont retirées, SHA prouvés) et la discipline prompt-engineering en skill (`prompt-engineering`). Source de vérité des disciplines : SHARED §7 ; orchestration : PM v3.12.0 §1.9.

---

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

### §1.14 Leçons knowledge-observer — économie API et arbitres (re-curation B13, modes M3-M4)

> **Note de numérotation (Task 21, résorption A7)** : le saut §1.8 → §1.14 est intentionnel — les sections §1.14/§1.15 portent leurs numéros d'origine du PM (re-curation B13) afin de préserver la traçabilité des références croisées (KB, changelogs PM) ; les sections PM intermédiaires (§1.9-§1.13) ne sont pas miroitées ici — leurs contenus figurent en §1.6-§1.8, chaque en-tête citant sa source PM.

<!-- PATTERN:KO-L001-v1.0.0 -->

**Règle KO-L001 — Économie API face à un quota 429 persistant** (leçon L001, appliquée) : en cas de blocage 429 persistant, ne jamais marteler l'API — une seule sonde par message utilisateur (R3-A11), travail local 100 % entre les sondes, armement automatique des suites à QUOTA_OK (flag + pré-checks + runner 429-aware `--skip-done`), fenêtres candidates documentées. Toute boucle d'attente en-tour est interdite : les démons d'arrière-plan de session sont fauchés entre les appels d'outils (constat expérimental R3-A17-bis — le mécanisme honnête reste la sonde immédiate à chaque tour, ré-armement best-effort seulement).

<!-- FIN-PATTERN:KO-L001-v1.0.0 -->

<!-- PATTERN:KO-L003-v1.0.0 -->

**Règle KO-L003 — Arbitres à invariants dynamisés** (leçon L003, appliquée) : tout arbitre mécanique dérive ses invariants de l'état courant (frontmatter installé = source de vérité, registre KB, comptage réel), jamais d'un état figé. Un invariant figé produit des faux verdicts (faux négatif `@mon-ecosysteme` classé PLATEFORME hors set CORE, faux positif `pgrep -f` par auto-match de la ligne de commande, état « uniformément v3.11.0 » figé). Toute divergence arbitre ↔ réalité se corrige en dynamisant l'arbitre, avec re-verdict honnête obligatoire après correction — jamais en ajustant la réalité pour coller au verdict.

<!-- FIN-PATTERN:KO-L003-v1.0.0 -->

### §1.15 Leçons knowledge-observer — recalibrage croisé (re-curation B13, modes M3-M4)

<!-- PATTERN:KO-L004-v1.0.0 -->

**Règle KO-L004 — Recalibrage croisé** (leçon L004, appliquée) : toute montée de version d'un skill de l'écosystème déclenche le recalibrage mécanique des outils dépendants AVANT la certification : arbitres (`verify-cross.py`, `verify-correct-work.py`, `test-coherence-interactions.py`, `check-ecosysteme-integrity.py`, `answer-key-checker.py`), pre-checks (`n8-a-precheck-a2.py`), `skills-meta.json`, run-order, SYNC_MAP, miroir et archive. Un outil non recalibré valide l'état précédent — verdict inopérant. L'application M4 de toute leçon knowledge-observer intègre donc d'office la liste des outils à recalibrer (garde post-édition).

<!-- FIN-PATTERN:KO-L004-v1.0.0 -->

<!-- PATTERN:KO-L007-v1.0.0 -->

**Règle KO-L007 — Matérialisation d'abord sur clone sparse** (leçon L007, appliquée — v3.18.0, verdict correct-work étape F PASS 2026-10-02, cycle fusion installateurs) : tout travail sur un clone sparse commence par l'établissement des faits de matérialisation — `git sparse-checkout list` + test d'existence des fichiers cibles AVANT toute écriture (`git add` / `git rm`) et AVANT tout verdict d'arbitre naïf ; un audit dérive de l'état matérielisé réel (L003) et consigne « non matérialisé » comme statut distinct de « échec ». 4 occurrences documentées (Tasks 4/6/7/E15 v3.17.1) avant application.

<!-- FIN-PATTERN:KO-L007-v1.0.0 -->

> Provenance : règles KO-L001/L003/L004 issues des leçons L001-L004 du journal `knowledge-observer` (sessions B13), reconstituées post-wipe (B13-r4, complété B13-r5) d'après les marqueurs et le lignage documentés — installées dans gen-plan v3.16.0 ; KO-L007 installée dans gen-plan v3.18.0 (leçon L007, verdict correct-work étape F PASS — cycle fusion installateurs 2026-10-02) ; les contenus exacts de v3.14.0/v3.15.0, non documentés, restent perdus au wipe inter-sessions.

---

### §1.16 Routage de découverte des skills + garde d'installation (v3.19.0, Task 23)

**É1-INSTALL — garde d'installation (décision D006)** : à l'ouverture de session, AVANT E1, exécuter `python3 scripts/ensure-installed.py --check` — rc=0 : écosystème installé (no-op, jamais de réinstallation d'un état à jour) ; rc≠0 : écosystème absent ou dérivé → exécuter `python3 scripts/ensure-installed.py --reinstall` (pipeline PM-INSTALL §2/§2bis ; clone éphémère SANS persistance de jeton — anti-persistance Task 8/14) avant toute autre étape. La garde est idempotente (f(f(x))=f(x)) et journalise toute réinstallation au worklog.

**Routage de découverte (décision D004)** — quand gen-plan doit trouver, sélectionner ou inventorier des skills (E5, §3) :

1. **skills-inventory en PRIORITÉ** : scanner `{{SKILLS_ROOT}}` via son script (`generate_skills_md.py --json` / `--search` / `--category`). Les performances des éléments trouvés sont comparées aux éléments natifs (couverture, fraîcheur, pertinence des métadonnées) et la comparaison est MÉMORISÉE au registre KB (section Décisions d'architecture) — la mémoire évite de re-comparer à chaque session et alimente le choix du routeur.
2. **skill-finder-cn en FALLBACK** : UNIQUEMENT si skills-inventory échoue (script absent, arbre vide, erreur d'exécution). Tout élément trouvé par le fallback passe un **contrôle cybersécurité `audit-provenance`** (provenance, permissions, contenu dangereux) AVANT adoption ; un échec du contrôle disqualifie l'élément et est consigné au KB. La bascule est unidirectionnelle au cours d'une même recherche : pas de retour à skills-inventory après activation du fallback.

---

## §2 — Spécification technique

### §2.1 Stack

- **Langage** : Python (scripts), Markdown (documentation), YAML (frontmatter)
- **Environnement** : `skills/gen-plan/`
- **Pas de dépendance externe** (sauf intégration KB si activée)

### §2.2 Structure

```
skills/gen-plan/
├── SKILL.md                          # Skill opérationnel compact (~300 lignes)
├── references/
│   ├── etapes-detaillees.md          # Détail des 15 étapes
│   ├── grille-token.md               # Grille de calibration #token
│   ├── classification-types.md       # Routage Type 1-4
│   ├── profils-ressource.md          # NORMAL / ECO / VIEUX PC
│   ├── guide-selection-agent-skill.md # Arbre de décision + tableau
│   ├── prompt-engineering-kit.md     # PEK v4.1 — raisonnement adaptatif (CoT/Chaining/Hybride, blocs A-J, 9 règles, 12 checks)
│   ├── patterns-avances-qwen.md      # 5 patterns avancés (N19) — Answer Key, Graph Diamond, ToT, Second Opinion, Task Observer
│   ├── answer-key-b12.md             # Premier registre réel des décisions (N19, D001-D010)
│   ├── answer-key-template.md        # Schéma + règles Answer Key (N20)
│   ├── graph-diamond-pattern.md      # Parallélisation exceptionnelle (N20)
│   └── observation-patterns.md       # Task Observer — cycle A-H (N20)
└── evals/
    ├── evals.json                    # Cas de test d'évaluation (6 evals)
    └── trigger_evals.json            # Description Optimization (8 cas — déclencheur verbatim v3.17.2)
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
| knowledge-observer | Invocation à E15 (§1.2bis) | Observation post-session (modes M1-M2) ; les modes M3-M4 exigent un verdict correct-work — version >= v1.0.0 |
| resource-monitor | Mobilisation hook E1-RES (§1.2bis) | Collecte G-RES à l'ouverture de session — verdict OK/PRESSION/CRITIQUE → mode d'exécution, version >= v1.0.0 |
| answer-key | Arbitrage E7/E8 (§1.2bis) | Décisions E1 vérifiables mécaniquement — arbitre answer-key-checker.py (16 checks) |
| knowledge.md | Enrichissement à E15 | Mise à jour registre et calibration |

---

## §4 — Grille #token

Résumé des plages clés (voir `references/grille-token.md` pour la grille complète) :

- **Planification E1-E2** : 800-1500 #token
- **Exécution simple (1 skill)** : 2000-5000 #token
- **Exécution complexe (4+ skills)** : 10000-20000 #token
- **Coefficients** : 0.8x (faible) → 1.5x (critique), ECO 0.7x, VIEUX PC 0.5x

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

Dès qu'une phase du plan d'actions vient de se terminer, lancer `correct-work(livrables de la phase, mode=CIBLE)` AVANT d'entamer la phase suivante : PASS → phase suivante ; PASS AVEC RÉSERVES → réserves loggées au worklog, exécution continue ; FAIL → pause jusqu'à correction puis re-vérification. Le hook E8 (fin de plan) reste la vérification finale.
