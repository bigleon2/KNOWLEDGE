---
name: agent-engineering
version: 1.0.0
category: ecosystem
language: fr
tags:
  - agent-engineering
  - agent-based-engineering
  - multi-agent-systems
  - agents
  - orchestration
  - disciplines
  - ecosystem
description: >-
  Skill discipline agent engineering : orchestration cohérente, optimisée et fonctionnelle — et autonome —
  des tâches d'Agent-Based Engineering, d'Agent Engineering et de Multi-Agent Systems Engineering au sein de
  l'écosystème : discipline englobante (n°56) qui CADRE chaque tâche relevant des trois domaines (conception,
  construction, outillage, évaluation, observabilité, sûreté des agents et des systèmes multi-agents), ROUTE
  vers le détenteur spécialisé compétent (fleet-engineering pour les patterns de flottes et la coordination,
  memory-engineering pour la mémoire, harness-engineering pour les gardes-fous, spec-driven-development pour
  les contrats, autonomous-agent pour le format .agent, agent-creator/skill-creator pour la fabrique,
  gen-plan pour la planification), OUTILLE chaque tâche d'un critère vérifiable exécutable et VEILLE sur les
  fondements 2026. Spécialise la discipline agent engineering (registre décentralisé : §8 local + registre
  KB). Opérationnalisation 2026 : State of Agent Engineering (LangChain, 2026 — prototype→production),
  Agent-Based Software Engineering (ABSE/Tropos — agents-as-building-blocks), Multi-Agent Systems
  (Anthropic 06/2025, Cognition 2025, Anthropic 08/2026). Fondements documentés :
  references/fondements-academiques.md.
dependencies:
  - skill: gen-plan
    version: ">=3.15.0"
    used_at: "détenteur principal de l'orchestration — décide de la mobilisation à E5/E7 ; n°56 cadre et route les tâches d'agents (§8)"
  - skill: fleet-engineering
    version: ">=1.0.1"
    used_at: "détenteur des patterns de coordination de flottes M1-M5 — route des tâches multi-agents opérationnelles (§1.3)"
  - skill: autonomous-agent
    version: ">=1.2.0"
    used_at: "détenteur du format .agent et du modèle agent autonome (cycle A-H, États Court/Long)"
  - skill: agent-creator
    version: ">=2.2.0"
    used_at: "détenteur de la fabrique d'agents réutilisables (workflow F1-F5)"
read_when:
  - Déclencher quand la demande concerne : l'ingénierie des agents et systèmes d'agents — conception, construction, outillage, évaluation, observabilité ou sûreté d'un agent ou d'un système multi-agents (trois domaines : Agent-Based Engineering, Agent Engineering, Multi-Agent Systems Engineering) — et l'orchestration de ces tâches au sein de l'écosystème.
  - Déclencher si la demande mentionne : agent engineering, ingénierie d'agents, agent-based engineering, agent-based software engineering, multi-agent systems engineering, systèmes multi-agents, concevoir/construire/évaluer un agent, observabilité des agents, sûreté des agents, fiabiliser un agent en production, orchestration des tâches d'agents, société d'agents, Tropos.
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28) — les demandes de coordination opérationnelle d'une flotte relèvent de fleet-engineering ; la fabrique concrète d'un skill/agent de agent-creator/skill-creator ; le format .agent de autonomous-agent ; la planification de tâches de gen-plan.
---

## §0 — Contexte Système (SHARED v1.7.36)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.
> Langue : FRANÇAIS exclusif pour tous les échanges avec le propriétaire (règle d'or n°6 gen-plan — directive 2026-10-31, renforcée 2026-11-06) : dès le PREMIER mot de toute session ou reprise, la langue d'un message, d'un résumé de continuation ou d'un canal ne dérive JAMAIS la réponse ; toute dérive est corrigée immédiatement.
> Règles d'or & lecture SHARED à l'exécution (directive propriétaire 2026-11-06 — SHARED §9) : tout skill/agent/script exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or de l'écosystème (résumé §9 — canonique gen-plan §1.5).
> Référence canonique skill/agent (directive propriétaire 2026-11-07 — SHARED §0/§1.2) : toute référence à « mon skill X »/« mon agent X » désigne la forme installée à la racine `skills/X/SKILL.md`, JAMAIS le prompt maître du corpus `@mon-ecosysteme/` — les PMs sont des spécifications générées mécaniquement (KO-L004), les skills installés sont les formes exécutables.

## §0 — RÈGLE ZÉRO (résumé de SHARED §0)

1. **Auto-contenu** : ce skill porte tout ce dont il a besoin ; pas de référence hors écosystème hors `references/`.
2. **Versionné semver** : toute modification majeure de comportement → bump MINOR/MAJOR + KB synchronisé.
3. **KB source de vérité** : la description et la version du présent SKILL.md sont répliquées dans `{{KB_PATH}}`.
4. **Dépendances déclarées** : YAML `dependencies` uniquement ; pas d'import implicite.

## §1 — SPÉCIFICATION FONCTIONNELLE

### §1.1 Mission
Orchestrer les tâches relevant des trois domaines — **Agent-Based Engineering** (ABE), **Agent Engineering** (AE), **Multi-Agent Systems Engineering** (MASE) — au sein de l'écosystème, de façon cohérente, optimisée, fonctionnelle et autonome. La discipline n°56 est **englobante** : elle CADRE (classe la tâche dans le bon domaine et en dérive les exigences), ROUTE (vers le détenteur écosystème compétent — §1.3), OUTILLE (chaque tâche reçoit un critère vérifiable exécutable avant exécution) et VEILLE (fondements 2026, signaux, garde-fous). Elle ne remplace AUCUN détenteur : sa valeur est le routage rigoureux et les critères de sortie — jamais la duplication de méthode (R4). Une tâche d'agents sans cadrage n°56 dérive vers la complexité prématurée (Building Effective Agents — « simple d'abord ») ; une tâche multi-agents sans garde n°56 viole la gate anti-flotte (Cognition 2025 / Anthropic 06/2025 — ratio ≈ 15×).

### §1.2 Les trois domaines (cadre de classification)
| Domaine | Définition (fondements) | Tâches types |
|---------|------------------------|--------------|
| **ABE** — Agent-Based Engineering | Paradigme où l'agent est le bloc constitutif premier du système (ABSE — agents-as-building-blocks, méthodologies Tropos/i*) | Modéliser un système en société d'agents (rôles, intentions, interactions, environnement) ; décider SI un système doit être agentisé ; structure des rôles et du contexte partagé |
| **AE** — Agent Engineering | Processus itératif de transformation de LLMs en systèmes fiables (State of Agent Engineering, LangChain 2026) | Prototype → production : outillage (tool use), contexte agentique, évaluation, observabilité, contrôle des coûts, durcissement |
| **MASE** — Multi-Agent Systems Engineering | Ingénierie des systèmes multi-agents : orchestration, communication, coordination, émergence, sûreté inter-agents | Orchestration d'une flotte (route vers n°54), handoffs typés, évaluation multi-agents, gardes coordination/collusion/sabotage |

### §1.3 Routage écosystème (fonction première de n°56)
| Tâche cadrée | Détenteur mobilisé | Cadre |
|--------------|--------------------|-------|
| Coordination opérationnelle de plusieurs agents (flotte) | `fleet-engineering` (n°54) | patterns M1-M5, Task IDs, bornes, agrégation arbitrée — gen-plan E5/E7 |
| Mémoire d'un agent / État Court-Long / compaction | `memory-engineering` | piliers write/select/compress/isolate |
| Critères de sortie exécutables, arbitres, gardes | `harness-engineering` | verdicts mécaniques, profils, signaux |
| Contrat/micro-spéc par sous-tâche (anti-handoff) | `spec-driven-development` | spec AVANT code, critères d'acceptation |
| Créer un agent autonome (format, cycle A-H, États) | `autonomous-agent` | gabarit .agent — matérialisation vivante : knowledge-observer.agent v1.1.0 (Task 82) |
| Fabriquer un skill/agent réutilisable | `agent-creator` / `skill-creator` | workflow F1-F5, conventions, evals |
| Planifier la mission, paralléliser, arbitrer | `gen-plan` | E1-E15, Graph Diamond E9-E14, answer key |
| Refactoring d'un système d'agents | `refactoring-engineering` (n°55) + `refactor-guard` | zéro-régression, blast radius (`refactoring-test`) |

**Règle de routage (neutralise les conflits de périmètre)** : (a) tâche séquentielle à écritures entrelacées → UN agent (jamais une flotte — Cognition) ; (b) parallélisable/indépendante → flotte M1-M5 via fleet-engineering (gate anti-flotte : périmètre large + lecture seule/indépendance prouvés) ; (c) nœuds scripts/binaires → inter-scripts ; (d) agent réutilisable à créer → agent-creator ; (e) la n°56 reste mobilisée COMME CADRE tant que la tâche est vivante (elle vérifie que le détenteur tient ses critères, puis se retire).

### §1.4 Règles opérationnelles
1. **Simple d'abord** : pas de système multi-agents tant qu'un agent simple (ou un workflow composé) résout — complexification sur preuve de besoin mesurée.
2. **Gate anti-flotte AVANT routage MASE** : tâches séquentielles/entrelacées → interdit ; ratio de coût (≈ 15×) non justifié par un périmètre parallélisable → interdit.
3. **Critère vérifiable par tâche** : chaque tâche cadrée embarque un arbitre/critère exécutable (harness-engineering) — un livrable non validé est « en attente », jamais « validé » (R3).
4. **États collectifs** : l'État Long d'un système d'agents est collectif (worklog par Task ID, KB), jamais dans la mémoire d'un agent mort.
5. **Journalisation qui-décide-quoi PAR agent** (Anthropic 08/2026) : traçabilité individuelle obligatoire dans tout système multi-agents cadré.
6. **Adaptation autonome** : l'échec d'un routage ou d'un agent est un signal de re-cadrage (domaine, détenteur, bornes), jamais un arrêt implicite.

### §1.5 Mémoire
La discipline ne détient PAS d'état propre (rôle de cadre) : l'État Long est délégué — worklog (sections par Task ID), KB (décisions d'architecture), answer key (décisions E1) — écrits par l'élément coordinateur (gen-plan ou l'agent maître) ; État Court : le contexte de cadrage, mort avec la tâche. Référence croisée : memory-engineering.

### §1.6 Cycle opérationnel
1. **Cadrer** : classifier la tâche (ABE/AE/MASE — §1.2), dériver les exigences, décider si le système doit être agentisé.
2. **Router** : sélectionner le détenteur (§1.3), lui transmettre un cadrage auto-contenu (contexte + critères + bornes — jamais de dépendance au contexte parent).
3. **Outiller** : armer le critère vérifiable (arbitre, baseline, seuil) AVANT l'exécution.
4. **Surveiller** : vérifier que le détenteur tient ses critères (arbitres) ; re-router au besoin sans changer l'objectif.
5. **Consolider** : statuts dérivés du disque (KO-L003), verdicts mécaniques, écarts consignés honnêtement.
6. **Se retirer** : la discipline n°56 ne laisse aucun état résiduel ; le système livré relève de son détenteur.

### §1.7 Fondements académiques et veille (n°56)
Sources vérifiées (veille Task 83 sonde unique + N31/N34) : **State of Agent Engineering** (LangChain 2026 — fiabilité premier frein, 1300+ praticiens) · **Building Effective Agents** (Anthropic 12/2024 — simple d'abord) · **ABSE/Tropos** (agents-as-building-blocks) · **multi-agent research system** (Anthropic 06/2025 — handoffs, ratio 15×) · **Don't Build Multi-Agents** (Cognition 2025 — gate anti-flotte) · **Patterns and problems in emerging multiagent systems** (Anthropic 08/2026 — collusion, sabotage, traçabilité par agent). Détail, frontière anti-duplication et lecture professionnelle : `references/fondements-academiques.md`.

## §2 — SPÉCIFICATION TECHNIQUE
Artefacts : matrice de cadrage (tâche × domaine × détenteur × critère vérifiable × bornes) ; fiche de routage auto-contenue par tâche (contexte, lecture worklog, livrable attendu, arbitre de sortie) ; trace de veille (references/). Pas de script propre en v1.0.0 (discipline de cadrage — les arbitres appartiennent aux détenteurs) ; l'évaluation A2 des déclencheurs suit le protocole SHARED §7 v2 (voie mécanique + confirm 3 runs LLM au QUOTA_OK — KO-L001). Idempotence : re-cadrage d'une même tâche = même route et mêmes critères (décisions dérivées de l'état du disque — KO-L003).

## §3 — RELATIONS (extrait de SHARED §3.1)
- `gen-plan` §1.6/§1.9 — détenteur principal de l'orchestration : mobilise n°56 à E5/E7 quand la demande touche les agents.
- `fleet-engineering` (n°54) — complément R4 : n°56 cadre/route, n°54 détient les patterns de coordination ; arête bidirectionnelle (MASE ↔ cadre).
- `memory-engineering` — États Court/Long des agents cadrés ; `harness-engineering` — critères de sortie exécutables ; `spec-driven-development` — micro-specs anti-handoff ; `loop-engineering` — boucle externe sur les systèmes d'agents.
- `autonomous-agent` — format .agent et cycle A-H (États Court/Long) : gabarit des agents autonomes (matérialisation vivante : knowledge-observer.agent v1.1.0).
- `agent-creator` / `skill-creator` — fabriques en aval du cadrage ; `refactoring-engineering` (n°55) + `refactor-guard` + `refactoring-test` — refactors de systèmes d'agents.

## §4 — CONVENTIONS
Kebab-case pour dossiers/fichiers ; semver strict ; tags `#token` ; `{{VARIABLE}}` pour les variables de contexte ; journalisation au worklog (`Task ID` + preuves) pour toute exécution réelle ; aucune fabrication de résultats (R3) ; langue française exclusive (règle d'or n°6).

## §5 — ÉVALUATIONS ET DÉCLENCHEURS
`evals/trigger_evals.json` : 7 requêtes (5 positives, 2 contrôles négatifs — disciplines voisines fleet/agent-creator) ; déclenchement attendu sur les demandes d'ingénierie d'agents des 3 domaines ; seuil de routage 0.5 (voie mécanique SHARED §7 v2). Baseline A2 : EN ATTENTE DE MESURE (v1.0.0 — protocole voie mécanique + confirm 3 runs LLM à armer à la prochaine fenêtre QUOTA_OK, KO-L001 — consigné honnêtement, aucune baseline pré-écrite R3).

## §6 — TRAÇABILITÉ
- v1.0.0 (Task 83, 2026-11-09, session web-ecef7f80, directive 1a1beaee032b5aa5) : matérialisation de la discipline n°56 (agent engineering) — forme SKILL DISCIPLINE (motifs : directive verbatim « défini en tant que discipline » + pattern disciplines n°54/n°55 ; agent .agent = exécutant spécialisé ; agent autonome = cycle A-H + État Long — knowledge-observer seul cas justifié à ce jour) ; cascade KO-L004 locale (KB + ECO_SKILLS + ULTRA 13ᵉ voie + historiques-par-skill + projection hôte) ; inscription socle SHARED §7 + gen-plan §1.6 = pendance structurée (précédents v1.7.0 n°54 / Task 7-8 n°55 — tâche dédiée).

## §7 — RÉFÉRENCES
- `references/fondements-academiques.md` — sources vérifiées 2026 (AE/ABE/MASE), frontière anti-duplication, signaux de veille, interactions inter-disciplines.
- SHARED §7 (PROMPT-MAITRE-SHARED.md, corpus) — source de vérité des disciplines (inscription n°56 : pendance Task 83).
- `fleet-engineering` SKILL.md §1.9bis — garde anti-flotte et ordre de routage partagés.

## §8 — Registre d'assignation des disciplines (décentralisé du SHARED §7)
| Discipline | Détenteur principal | Fonction héritée |
|------------|--------------------|------------------|
| agent engineering (n°56) | gen-plan (mobilisation E5/E7 — cadrage et routage des tâches d'agents vers les détenteurs §1.3) | fleet-engineering (exécution MASE), autonomous-agent (gabarit .agent), agent-creator (fabrique), memory/harness/spec/loop-engineering (socles), refactoring-engineering (n°55, refactors d'agents) |
