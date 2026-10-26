# Graph Diamond Pattern — parallélisation par défaut sur preuve d'indépendance

Source : propositions-qwen.md §1.2 (pattern Graph Diamond), intégré phase N20 (gen-plan v3.13.0) ; **défaut INVERSÉ v3.24.0** (directive propriétaire 2026-10-24 — le parallèle devient le défaut, le série l'exception tracée, en cohérence avec fleet-engineering n°54 orchestrée par gen-plan à E5/E7).
Hook gen-plan : **E9-E14** (parallélisation par défaut des actions prouvées indépendantes).

<!-- PATTERN:GRAPH-DIAMOND-v1.0.0 -->

## §1 — Principe

Le défaut gen-plan est la **parallélisation des sous-tâches prouvées indépendantes**
(philosophie #4 v3.24.0 : le série est l'exception justifiée). Dès que la preuve
d'indépendance existe (aucune écriture partagée, aucune dépendance d'ordre), le
Graph Diamond s'ouvre AUTOMATIQUEMENT : les sous-tâches se déploient en parallèle
puis convergent — la forme d'un losange (diamond) : 1 nœud d'entrée, N nœuds
parallèles, 1 nœud de synthèse. Exécuter en série des sous-tâches prouvées
indépendantes exige une justification tracée au worklog (dépendance d'ordre
découverte, verdict resource-monitor SERIE/PAUSE, profil ECO/VIEUX PC).

## §2 — Les 4 phases

| Phase | Nom | Rôle |
|-------|-----|------|
| 1 | **Décomposition** | Découper en sous-tâches réellement indépendantes (preuve d'indépendance : aucune écriture partagée, aucune dépendance d'ordre) |
| 2 | **Exécution parallèle** | Lancer les agents/skills en un seul message multi-outils (R4 : DAG parallèle) — re-verdict resource-monitor entre les vagues |
| 3 | **Synthèse** | Fusionner les sorties dans l'ordre du plan, résoudre les collisions de noms/chemins |
| 4 | **Vérification** | Arbitre sur l'ensemble fusionné (pas vagues séparées) : hook correct-work + re-verdict ×2 pour l'idempotence |

## §3 — Conditions d'ouverture

- **Ouverture AUTOMATIQUE dès preuve d'indépendance** (v3.24.0) : aucune justification
  supplémentaire n'est requise pour paralléliser ; c'est le REFUS de paralléliser
  (série) qui exige une justification tracée (dépendance d'ordre, écriture partagée,
  verdict resource-monitor SERIE/PAUSE, profil ECO/VIEUX PC).
- Les sous-tâches sont prouvées indépendantes (aucune écriture dans le même fichier,
  aucune lecture d'une sortie d'une autre sous-tâche).
- Le travail en parallèle est tracé au worklog (Task IDs attribués, pattern `2-a`/`2-b`).
- Le re-verdict des arbitres est rejoué après CHAQUE vague (R4) — un verdict figé est
  inopérant (leçon KO-L003).

## §4 — Anti-patterns

- **Effets de bord partagés** : deux sous-tâches parallèles qui écrivent le même
  fichier ou le même registre (KB, worklog) — interdits ; sérialiser ou partitionner.
- **Dépendance cachée d'ordre** : « 2-b lit ce que 2-a écrit » — c'est une chaîne
  série déguisée ; la parallélisation produirait un livrable au contenu dépendant
  de l'ordonnancement.
- **Parallélisme sans preuve d'indépendance** : ouvrir un diamond SANS la preuve
  (écritures partagées, dépendance d'ordre cachée) — la preuve d'indépendance reste
  le prérequis non négociable de la parallélisation par défaut (v3.24.0).
- **Sériographie par défaut** : exécuter en série des sous-tâches PROUVÉES
  indépendantes sans justification tracée — violation de la philosophie #4 v3.24.0 ;
  l'exception série se justifie, elle ne s'impose plus.
- **Synthèse sans vérification globale** : vérifier chaque branche isolément puis
  fusionner sans arbitre final laisse passer les conflits inter-branches.

<!-- FIN-PATTERN:GRAPH-DIAMOND-v1.0.0 -->

> Provenance : reconstituée post-wipe (B13-r4) d'après les 4 phases et l'anti-pattern
> vérifiés par l'arbitre survivant `scripts/answer-key-checker.py` (N20, check 6) et la
> pratique R4 documentée du worklog — le contenu exact de la version N20 originale
> reste perdu au wipe inter-sessions. Révision v3.24.0 (2026-10-24) : inversion du
> défaut (parallèle par défaut sur preuve, série = exception tracée) — directive
> propriétaire, session web-fdf5963c, Task 26.
