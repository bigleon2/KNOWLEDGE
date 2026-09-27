# Fondements académiques et veille — fleet engineering (N34, r56 — n°54)

## 1. Sources vérifiées (preuves tmp/n31-recherche/ : cours-f1, cours-f2, cand-x1)

- **Agent Teams — Orchestrate teams of Claude Code sessions** (code.claude.com) : plusieurs instances coordonnées ; un team lead assigne les tâches, coordonne le travail et fusionne les résultats — le pattern SUPERVISOR industrialisé.
- **Scaling Managed Agents: Decoupling the brain from the execution** (Anthropic, 8 avr. 2026) : découpler la décision (cerveau) de l'exécution pour scaler des agents managés — fondement du découplage pattern/bornes/exécution.
- **Multi-Agent Orchestration: 5 Patterns That Work in 2026** (digitalapplied, 17 mai 2026) : fan-out, pipeline, debate, supervisor, swarm — chacun avec son best-fit explicite ; base des modes M1-M5 du SKILL.md.
- **How we built our multi-agent research system** (Anthropic, 13 juin 2025) : orchestrateur + sous-agents de recherche, citation obligatoire, leçons d'ingénierie (échecs de handoff, coûts de token).
- **2026 will be the Year of Multi-agent Systems / State of Agent Engineering** (LangChain/aiagentsdirectory, janv. 2026) : la coordination multi-agents mûrit en discipline d'ingénierie (test, déploiement) — la flotte s'ingénierie comme un système.

## 2. Signaux de veille

Découplage cerveau/exécution comme réponse au scaling ; montée des plateformes « build vs buy » (augmentcode, mai 2026) ; spécialisation croisée (platform + ML + skill engineering) ; mise en garde transverse : la coordination coûte (tokens, latence) — bornes obligatoires (§1.4 du SKILL.md).

## 3. Lecture professionnelle

Commencer par les 5 patterns (carte mentale), puis Agent Teams (mécanique concrète de lead/workers), puis multi-agent research system (retours d'expérience honnêtes) ; Managed Agents pour la trajectoire de scaling.

## 4. Interactions entre disciplines (n°54, r56)

(1) **fleet ↔ harness** — l'arbitrage mécanique est le critère de sortie de flotte : les livrables agrégés passent les arbitres avant tout statut « validé » (R3) ; (2) **fleet ↔ spec-driven** — chaque sous-tâche porte une micro-spécification avec critère d'acceptation exécutable, sinon l'agent dérive ; (3) **fleet ↔ memory** — l'État Long d'une flotte est collectif (worklog par Task ID, KB), jamais confiné à la mémoire d'un agent mort ; (4) **fleet ↔ loop** — la boucle externe génération-vérification s'applique à la flotte entière : le vérifier arbitre, le générateur re-planifie (D017). Source transverse : Anthropic multi-agent research system — la citation obligatoire des sources est déjà de la memory engineering appliquée à une flotte.
