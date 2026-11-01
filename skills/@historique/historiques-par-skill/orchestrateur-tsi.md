# Historique par skill — orchestrateur-tsi

> **Version** : 1.0.0 — **Date** : 2026-11-01 (Task 32, session web-4f989063, trace 1a1977ef5718a28d — directive propriétaire : création d'un orchestrateur des skills/agents TSI, TRAKTOR et KONTROL S4 ; forme et niveau de prompt laissés au choix de l'agent)
> **Version vivante (corpus)** : v1.0.0 — `skills/orchestrateur-tsi/SKILL.md` (sa spécification fait foi)
> **Versions archivées** : 0 (point de départ)
> **Provenance** : créé directement au canon (bloc §0 SHARED v1.7.17, pattern tandem 2 couches hérité de tsi-architect) et inscrit simultanément hôte + dépôt (contrairement au trio TSI inscrit a posteriori Task 31 — lignage propre dès la création)

## Famille ORCHESTRATEUR-TSI — 1 version (skill : orchestrateur-tsi)

**Particularité durable du skill** : orchestrateur du domaine TSI/Traktor — coordonne tsi-architect, tsi-validator, multi-shift-architect et midi-doc-expert par micro-spécifications auto-contenues (niveau prompt méta maître) ; ne remplace aucun membre, ne duplique pas la gouvernance d'écosystème (gen-plan/correct-work) ; garde PASS tsi-validator obligatoire avant documentation/livraison ; checkpoints GO propriétaire (push = propriétaire, KO-L009 point 5) ; périmètre matériel ancré S4 MK3, mentions MK2 = calibration préalable (jamais d'invention).

| Version | Date | Améliorations implantées | Avantage par rapport à la version précédente |
|---------|------|--------------------------|----------------------------------------------|
| v1.0.0 | 2026-11-01 | Version initiale : matrice de routage §1.3 (mono-membre → redirection directe, multi-membres → pipeline P1-P6), tandem skill + `orchestrateur-tsi.agent` (mémoire État Court/État Long, pipeline A-H, formats micro_spec/bilan), gardes §1.4 (PASS obligatoire, anti-collision, non-substitution, référentiels non matérialisés jamais routés), trigger_evals 8 cas (5 positifs / 3 négatifs vetos croisés cohérents Task 30), KB + réciproques ×4 (tsi-architect, tsi-validator, midi-doc-expert, gen-plan), pin ECO_SKILLS 47e entrée | Le domaine TSI dispose d'un point d'entrée d'orchestration : les missions de bout en bout (concevoir → valider → documenter) sont routées, spécifiées et arbitrées en une méthode unique — **VERSION VIVANTE (corpus)** |

Décisions de forme consignées (directive propriétaire, choix délégué à l'agent) : (1) **PAS un agent pleinement autonome** — gouvernance déjà détenue (R4 jamais dupliquer, règle d'or n°5 anti-aspirant) et checkpoints obligatoires (PASS, GO push) ; (2) **PAS un simple skill mono-tâche** — pipeline multi-skills ; (3) **tandem 2 couches** (pattern écosystème) ; (4) **niveau prompt méta maître** (compose des micro-prompts auto-contenus par mission ; ultra maître surdimensionné et en conflit de gouvernance).

Fichiers archivés de la famille : néant (0 fichier).
