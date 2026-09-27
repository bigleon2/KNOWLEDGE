# Fondements académiques et veille — memory engineering (N34, r56 — n°54)

## 1. Sources vérifiées (preuves tmp/n31-recherche/ : cand-x3)

- **Agentic Memory: Learning Unified Long-Term and Short-Term… (AgeMem)** (Y. Yu et al., arXiv 2026, 110+ citations) : les opérations mémoire sont exposées comme outils — l'agent décide de façon autonome quoi/quand stocker, récupérer, mettre à jour.
- **Memory in the Age of AI Agents: A Survey** (github.com) : taxonomie de la mémoire conversationnelle long terme (baselines simples mais fortes, MemoryLLM étendu, court vs long terme).
- **Build AI agents with short-term & long-term memory** (Redis × LangGraph, 1er juil. 2026) : checkpointing d'état et mémoire vectorielle pour la persistance et le retrieval.
- **The 6 Best AI Agent Memory Frameworks** (machinelearningmastery, 2 avr. 2026) : panorama frameworks — mémoire long terme, retrieval, gestion de contexte.

## 2. Signaux de veille

L'agent qui gouverne sa mémoire (AgeMem : opérations en outils) déplace le problème de « tout stocker » vers « décider » ; le budget d'attention fini devient le critère de conception ; les frameworks convergent vers checkpointing + retrieval hybride ; vigilance : la mémoire non ancrée hallucine (croisement avec graph-engineering).

## 3. Lecture professionnelle

Commencer par le survey (carte du territoire), puis AgeMem (mécanique des opérations mémoire comme outils), puis Redis/LangGraph (implémentation concrète du checkpointing) ; le panorama de frameworks sert de comparatif rapide.

## 4. Interactions entre disciplines (n°54, r56)

(1) **memory ↔ context** — les deux disciplines partagent le même budget fini : la mémoire décrit ce qui persiste, le contexte ce qui est lu maintenant ; compaction (SHARED §7) est leur frontière opérationnelle ; (2) **memory ↔ graph** — le registre KB versionné EST la mémoire relationnelle de l'écosystème : requêtes ancrées = retrieval anti-hallucination ; (3) **memory ↔ loop** — les boucles longues exigent compaction paramétrable + reprise mécanique (REPRISE, --skip-done) ; (4) **memory ↔ fleet** — l'État Long de flotte est collectif et append-only (worklog par Task ID). Source transverse : AgeMem — « décider quoi stocker » est exactement la règle §1.4-1 du SKILL.md (écrire est une décision d'ingénierie).
