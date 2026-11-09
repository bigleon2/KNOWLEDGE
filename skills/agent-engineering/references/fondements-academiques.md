# Fondements académiques et veille — agent engineering (n°56 — discipline englobante ABE/AE/MASE)

> Task 83 (2026-11-09, session web-ecef7f80, directive 1a1beaee032b5aa5) — veille : sonde unique KO-L001
> (State of Agent Engineering 2026, ABSE, MASE) + sources N31/N34 déjà vérifiées (preuves tmp/n31-recherche/).

## 1. Sources vérifiées

### 1.1 Domaine « Agent Engineering » (AE)

- **State of Agent Engineering** (LangChain, 2026 — langchain.com/state-of-agent-engineering) : « agent engineering = processus itératif consistant à transformer des LLMs en systèmes fiables » — les agents étant non-déterministes, l'ingénierie exige itération rapide, évaluation systématique, observabilité du comportement et durcissement vers la production ; rapport 1300+ praticiens (57 % ont des agents en production — la fiabilité, pas le coût, est le premier frein). La discipline AE couvre le cycle prototype → production : outillage, évaluation, observabilité, contrôle des coûts.
- **Building Effective Agents** (Anthropic, déc. 2024) : commencer simple (workflow composé), ne complexifier en agent autonome que sur preuve de besoin ; les blocs de base (prompting, tool use, retrieval) avant les patterns sophistiqués — fondement du principisme « simple d'abord » de la discipline.
- **State of Agent Engineering** (LangChain/aiagentsdirectory, janv. 2026) : la coordination d'agents mûrit en discipline d'ingénierie testable et déployable — pont assumé entre AE et MASE.

### 1.2 Domaine « Agent-Based Engineering » (ABE)

- **Agent-Based Software Engineering** (ABSE — paradigme académique, Scribd/Lec « Introduction to Agent-Based Software Engineering ») : construire les systèmes où l'agent est le bloc constitutif premier (agents-as-building-blocks) ; méthodologies (Tropos et lignées i*) : modéliser en société d'agents — rôles, intentions, interactions, environnement — AVANT toute implémentation ; l'ABE est le domaine de MODÉLISATION (le « quoi » structurel), distinct de l'orchestration opérationnelle (MASE).
- **AI-Driven Development / Agentic Engineering** (Ventum Consulting, oct. 2026 ; lignée « vibe coding vs agentic engineering » 2026) : dans une installation productive d'ingénierie basée agents, chaque agent porte une tâche spécialisée du cycle — le modèle agents-as-first-class-citizens du développement.

### 1.3 Domaine « Multi-Agent Systems Engineering » (MASE)

- **How we built our multi-agent research system** (Anthropic, 13 juin 2025) : orchestrateur + sous-agents, citation obligatoire, leçons d'ingénierie — échecs de handoff (perte de contexte inter-agents), ratio de coût multi-agents ≈ 15× vs chat.
- **Don't Build Multi-Agents** (Cognition, 2025, reconfirmé 04/2026) : garde anti-flotte — une architecture multi-agents est interdite si les tâches sont séquentielles à écritures entrelacées ; les sous-tâches doivent partager le contexte via des artefacts de stockage, pas la mémoire vive des agents.
- **Patterns and Problems in Emerging Multi-Agent Systems** (Anthropic, août 2026) : échecs de coordination, collusion, sabotage documentés — journaliser qui-a-décidé-quoi PAR agent ; quotas stricts.
- **Scaling Managed Agents / Agent Teams** (Anthropic, avr. 2026 ; code.claude.com) : découplage cerveau/exécution pour scaler ; team lead assigne et fusionne.
- **Multi-Agent Orchestration: 5 Patterns That Work in 2026** (digitalapplied, mai 2026) : fan-out, pipeline, debate, supervisor, swarm — best-fit explicite par usage (détenu opérationnellement par fleet-engineering n°54).

## 2. Frontière de la discipline (anti-duplication R4)

L'agent-engineering (n°56) est la discipline **englobante** des trois domaines : elle CADRE (classe la tâche dans le bon domaine), ROUTE (vers le détenteur écosystème compétent), OUTILLE (critère vérifiable par tâche) et VEILLE (fondements + signaux). Elle ne détient AUCUNE méthode opérationnelle déjà possédée : patterns de flottes → fleet-engineering (n°54) ; mémoire → memory-engineering ; gardes-fous → harness-engineering ; contrats → spec-driven-development ; format .agent → autonomous-agent ; fabrique → agent-creator/skill-creator ; planification → gen-plan. Source transverse : State of Agent Engineering 2026 — l'ingénierie d'agents est transversale par nature, sa valeur locale est le ROUTAGE rigoureux.

## 3. Signaux de veille

La fiabilité remplace le coût comme frein n°1 (LangChain 2026) ; montée des plateformes d'évaluation/déploiement agents (LangSmith et homologues) ; l'ABSE académique converge avec l'agentique LLM (agents-as-building-blocks) ; durcissement des gardes multi-agents (collusion/sabotage — 08/2026) ; spécialisation croisée platform/ML/skill engineering.

## 4. Lecture professionnelle

Commencer par State of Agent Engineering 2026 (le cadre itératif fiabilisation), puis Building Effective Agents (simplicité d'abord), puis les gardes MASE (Cognition 2025, Anthropic 08/2026), enfin ABSE/Tropos pour la modélisation structurelle.

## 5. Interactions entre disciplines (n°56)

(1) **agent-engineering ↔ fleet-engineering** — n°56 cadre et route les tâches multi-agents VERS n°54 qui détient les patterns M1-M5 et les bornes de flotte ; jamais l'inverse. (2) **agent-engineering ↔ harness-engineering** — chaque tâche d'agents cadrée par n°56 reçoit un critère vérifiable exécutable (arbitre) avant exécution. (3) **agent-engineering ↔ memory-engineering** — l'État Long d'un système d'agents est collectif (worklog, KB), jamais dans la mémoire d'un agent. (4) **agent-engineering ↔ spec-driven-development** — les systèmes multi-agents dérivent aux handoffs ; la micro-spéc par sous-tâche est la parade (Anthropic 06/2025). (5) **agent-engineering ↔ autonomous-agent** — le format .agent et le cycle A-H (États Court/Long) sont le gabarit local d'un agent autonome ; knowledge-observer.agent (v1.1.0, Task 82) en est la matérialisation vivante. (6) **agent-engineering ↔ gen-plan** — la planification E-série décide QUAND mobiliser la discipline (E5) ; n°56 nourrit l'answer key des décisions d'agents.
