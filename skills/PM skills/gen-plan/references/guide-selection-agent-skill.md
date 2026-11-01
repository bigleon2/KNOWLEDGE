# Guide de Sélection Agent/Skill — gen-plan E5/E7

> Complété Task 22 (2026-10-23, session web-fdf5963c — directive « disciplines/techniques »,
> recherches web ciblées 2025-2026) : le fichier ne portait qu'un arbre vide
> (5 lignes, fence non fermée — défaut documenté au rapport Task 22).

## Arbre de décision (ordre de routage E5/E7)

```markdown
Tâche à router ?
├── (a) SÉQUENTIELLE à décisions entrelacées / écritures volatiles
│     → 1 agent autonome (autonomous-agent, pipeline A-H + G2 re-planification)
├── (b) PARALLÉLISABLE / sous-tâches indépendantes (lecture seule ou écritures disjointes)
│     → flotte (fleet-engineering M1-M5) — gate anti-flotte §1.9bis :
│         interdite si ratio ~15× tokens non justifié par un périmètre large
├── (c) NŒUDS SCRIPTS / BINAIRES inter-langages à dépendances de données
│     → inter-scripts (registre de nœuds, Kahn, one-shot/daemon/handoff)
└── (d) CRÉATION d'agents réutilisables
      → agent-creator (fabrique F1-F5) ; l'exécution ensuite → autonomous-agent
```

## Règles transverses (veille 2025-2026)

1. **Gate anti-flotte** (Cognition 2025/2026, reconfirmé 04/2026) : le mono-agent
   + context engineering surpasse la flotte sur les tâches séquentielles à
   écritures entrelacées ; la flotte se justifie par un périmètre large
   parallélisable (ratio ~15× tokens, Anthropic 06/2025).
2. **Task IDs globaux** : tout travail délégué porte un Task ID reflétant
   l'ordre global et le parallélisme (ex. `2-a`, `2-b`) + worklog partagé
   `/home/z/my-project/worklog.md` (format SHARED §1.4).
3. **Prompts auto-contenus** : les sous-agents ne voient PAS le contexte de
   session — la tâche déléguée est auto-suffisante (provenance, entrées,
   sorties attendues, artefacts à produire).
4. **Micro-spéc par sous-tâche** (liaison spec-driven-development) : la majorité
   des échecs multi-agents sont des échecs de handoff — la spécification
   complète de la sous-tâche est la parade citée.
5. **Agrégation unique re-vérifiée** : une seule agrégation des résultats de
   flotte, re-vérifiée mécaniquement (arbitres) avant intégration au plan.
