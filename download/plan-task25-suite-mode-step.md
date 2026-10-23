# Plan d'actions — Task 25 (SUITE, mode step)

> **Session** : web-fdf5963c · **Date** : 2026-10-23 (révision 2026-10-24 : G2 armé) · **gen-plan** : v3.23.2 (mode step) · généré à E15/F1 de la Task 24 (mécanisme permanent).
> **État d'entrée** : origin/main = 08c956c (couches 18/20/22 + intégration amont + Task 24 publiées, certification 6/6, hôte 78/78) ; règle d'or n°2 réarmée (0 commit/push sans GO).

## §1 — Groupes séquentiels (mode step)

| Groupe | Tâches | Prérequis | #token |
|--------|--------|-----------|--------|
| **G1 — Rotation du PAT** | révocation/régénération du jeton GitHub fourni en Task 24 (procédure propriétaire) | côté propriétaire | ~1 k |
| **G2 — Arbitrage des 3 dérives replay iphone** (ARMÉE 2026-10-24) | re-mesure replay (idempotence) ; arbitrage des **6 cas négatifs échoués** hérités de l'amont photos — iphone17 v1.1.0 ×1 (rendu « iPhone 18 » attendu false), iphone18 v1.1.0 ×1 (rendu « iPhone 17 » attendu false), iphone19 v0.11.0 ×4 (générique / rendu 18 / restauration / poster, attendus false) — verdict CONFIRME/révision par dérive ; si révision : correctif eval/SKILL + recalibrage KO-L004 ; rapport `download/arbitrage-derives-replay-iphone-task25.md` | armée par directive propriétaire | ~6 k |
| **G3 — Plan actif Task 19 (restants)** | G2 alias opérationnel (tenue au fil des sessions) ; G4 restants documentaires : PM-INSTALL v1.8.3 si documentation F1/F3 voulue au §3.2 (décision propriétaire) ; baselines A2 des 16 éléments bumpés si Description Optimization future (descriptions inchangées → non requise) | demande propriétaire | ~4 k |
| **G4 — Veille §1.9bis** | à la prochaine campagne disciplines : re-veille 2026+ et révision incrémentale des §1.9bis (format Task 24 : apport → application locale) | prochaine directive | ~20 k |

## §2 — Answer key (extraits)

```yaml
decisions:
  - id: "D001"
    criterion: "PAT Task 24 révoquée/régénérée (côté propriétaire)"
    verification: "constat propriétaire"
    source: "plan-task23 G3 + audit anti-persistance Task 24"
    priority: "S1"
    status: "pending"
  - id: "D002"
    criterion: "Dérives iphone arbitragées voie L si armées (0 dérive non arbitrée persistante) — ARMÉE : 6 cas négatifs arbitragés, verdict par dérive tracé dans le rapport, 0 dérive iphone restante non arbitrée"
    verification: "replay check-triggers-replay.py idempotent + rapport arbitrage (constat == Task 24)"
    source: "leçon Task 17 + replay Task 24 + directive propriétaire 2026-10-24"
    priority: "S3"
    status: "executed"
```

## §3 — Exécution
G1 (propriétaire) → G2/G3 à la demande → correct-work(projet) en fin de chaîne. E15 : bilan + plan suivant via gen-plan.
