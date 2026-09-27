# Reference — Patterns avancés (propositions-qwen.md, intégration N19)

> **Origine** : `download/propositions-qwen.md` (proposition Qwen v1.0.0, 2026-09-12,
> extraite demande n°33, session B12-r40) — intégration idempotente et additive (R2).
> **Portée** : gen-plan v3.12.0 — utilisation optionnelle à E1/E5/E9-E14 ; montée
> v3.13.0 (hooks obligatoires + arbitres) ARMÉE phase N20, non déployée (R2 : pas de rétrogradation).

## §1.1 — Answer Key Pattern (spécifications formelles)

Enregistrement structuré (JSON/YAML) des décisions E1 de gen-plan, rendant chaque
critère de succès **vérifiable mécaniquement** :

```yaml
answer_key:
  metadata:
    created: "<date>"
    source_skill: "gen-plan"
    source_version: "<version>"
    decisions_count: N
  decisions:
    - id: "D00N"
      criterion: "Critère de succès mesurable"
      verification: "Méthode de vérification concrète et exécutable"
      source: "E1 décision #N ou justification"
      priority: "S1|S2|S3|S4"      # sévérité correct-work
      status: "pending|verified|failed"
```

Règles opérationnelles :
1. Chaque décision E1 de gen-plan doit avoir une entrée dans l'answer key
2. La vérification doit être exécutable (pas de critère subjectif)
3. La source doit être traçable (étape + numéro de décision)
4. La priorité correspond à la sévérité S1-S4 de correct-work
5. L'answer key est immuable après validation E8 (R2 : ne jamais rétrograder)

Intégration correct-work : E2 vérifie chaque critère ; E5 vérifie la couverture des
décisions ; verdict PASS uniquement si tous les critères S1/S2 sont vérifiés.

Premier registre réel : `answer-key-b12.md` (lignée B12, même dossier).

## §1.2 — Graph Diamond Pattern (parallélisation)

Orchestration parallèle de sous-tâches indépendantes avec synthèse et vérification
centralisées (adapté du Gauntlet Loop — Matt Shumer — et de Graph Engineering, Anthropic 2026) :

```
        [Planificateur]
              |
    +---------+---------+
    |         |         |
[Agent 1] [Agent 2] [Agent 3]
    |         |         |
    +---------+---------+
              |
      [Synthétiseur]
              |
      [Vérificateur]
```

Phases : (1) décomposition en tâches indépendantes → (2) exécution parallèle →
(3) synthèse → (4) vérification centralisée. Applicable à E9-E14 quand les actions
sont sans dépendance d'ordre (ex : propagation multi-porteurs N14-b). Anti-pattern :
paralléliser des actions à effets de bord partagés (KB, canal, miroir).

## §1.3 — Tree of Thought (idéation créative)

Idéation multi-agents avec **isolation de contexte** : chaque agent génère ses idées
dans sa propre perspective (pollution de contexte interdite), puis un arbitre note
chaque idée (Novelty/Viability/Fit, 1-10) et la shortlist retient N+V+F >= 20.

Anti-patterns : ne pas lancer le ToT pour des problèmes fermés ; ne pas partager le
contexte entre agents ; ne pas s'arrêter aux 3 premières réponses.
Intégration : mode M5 Idéation (agent-prompt-engineering), déclencheurs
« génère des idées », « brainstorm », « explore les options ».

## §1.4 — Second Opinion (vérification aveugle)

Vérifier un livrable avec un agent **sans le contexte de construction** — élimine le
biais de confirmation (l'auteur voit ce qu'il s'attend à voir). Protocole :
(1) livrable finalisé + critères de vérification remis au vérificateur isolé ;
(2) vérification à l'aveugle ; (3) comparaison des verdicts ; (4) divergence =
arbitrage par un 3e agent ou un arbitre mécanique.
Analogie écosystème : les arbitres (verify-cross, integrity, interactions) sont
déjà des Second Opinions mécaniques ; le pattern étend la pratique aux verdicts
agent-driven (correct-work E5, clone-chat §3.5 Context Drift).

## §1.5 — Task Observer (apprentissage continu)

Observation automatique des sessions pour détecter les patterns d'erreur récurrents
et proposer des améliorations (adapté de rebelytics — Task Observer) :

| Étape | Action | Sortie |
|-------|--------|--------|
| A | Observation passive (M1) | journal de session |
| B | Détection erreurs/patterns récurrents | liste de patterns |
| C | Enregistrement | `data/lessons-learned.json` |
| D | Analyse post-session (M2, E15 gen-plan) | rapport d'analyse |
| E | Proposition de mises à jour (M3) | propositions idempotentes |
| F | Validation correct-work | verdict |
| G | Application si validé (M4) | correctifs appliqués |
| H | Mise à jour KB | entrée + Décisions |

Convergence écosystème : le worklog + les boucles R3 (A1-A17) + KNOWLEDGE.md
Décisions remplissent déjà A-H de manière agent-driven ; le pattern industrialise
le cycle (détection mécanique des récurrences).

## §2 — Méthode d'intégration (idempotente, appliquée N19)

1. Références additives dans `skills/gen-plan/references/` (ce fichier + answer-key)
2. Registre answer key réel alimenté depuis les décisions documentées (worklog)
3. Entrée KB (Décisions) traçant l'intégration
4. Vérification : arbitres intacts (verify-cross, integrity, interactions) + certification 5/5
5. Hooks obligatoires (E1 answer key, arbitre answer-key-checker, mode M5) : **N20 ARMÉE** —
   montée v3.13.0 complète avec propagation ×3 voies + re-calibrage + certification

## §3 — Bénéfices attendus (mesurables)

| Pattern | Bénéfice | Métrique cible |
|---------|----------|----------------|
| Answer Key | décisions vérifiables mécaniquement | 100 % des décisions E1 couvertes |
| Graph Diamond | temps d'exécution réduit | -30 % sur propagations multi-porteurs |
| Tree of Thought | qualité d'idéation | shortlist N+V+F >= 20 |
| Second Opinion | biais de confirmation éliminé | divergences détectées/arbitrées |
| Task Observer | apprentissage continu | récurrences détectées avant incident |
