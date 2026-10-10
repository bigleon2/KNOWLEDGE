# Historique par skill — gen-plan

> **Version** : 1.0.0 — **Date** : 2026-10-11 (Task 17-B, session web-b93f42fa — directive propriétaire « un historique par skill »)
> **Version vivante (corpus)** : v3.21.0 — `skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.21.0.md` (sa table §7 fait foi)
> **Versions archivées** : 15 PMs (v3.6.1 → v3.19.0) dans `prompts-maitres/gen-plan/` — sceau SHA-256 au README §2
> **Provenance** : tables migrées verbatim de `historique-versions-prompts-maitres.md` §2 (fichier retiré après migration — R4 une information, une source ; Task 17-B)

## Famille GEN-PLAN — 22 versions (skill : gen-plan)

**Particularité durable du skill** : planification structurée pour assistant IA — 4 modes (Planification, Exécution, Surveillance, Adaptation), 15 étapes E1-E15, classification Type 1-4, 3 profils ressource (NORMAL/ECO/VIEUX PC), tagging #token, scripts Python uniquement (N3), disciplines d'ingénierie de prompts, hooks patterns avancés, règles d'or §1.8.

| Version | Date | Améliorations implantées (source §7 du PM v3.21.0) | Avantage par rapport à la version précédente |
|---------|------|---------------------------------------------------|----------------------------------------------|
| v2.0.0 | 2026-07-18 | Version initiale (refusée par l'utilisateur) | — (point de départ de la lignée) |
| v3.1.0 | 2026-07-18 | Refactoring complet suite au refus de v2.0.0 | Forme restructurée qui devient la base acceptée de toute la lignée |
| v3.3.0 | 2026-07-29 | Ajout du Registre KB et du Protocole de Découverte | gen-plan découvre les skills via le registre vivant au lieu d'un inventaire figé |
| v3.5.0 | 2026-07-29 | Intégration clone-chat, calibration #token, normes N1-N3 | Coût de chaque étape estimé en tokens ; conventions de nommage et de tagging normées |
| v3.6.0 | 2026-08-09 | Refactoring du prompt maître : extraction du socle commun SHARED | Déduplication : les informations communes vivent une seule fois dans SHARED (R4) |
| v3.6.1 | 2026-08-09 | Méthode lecture bloc par bloc (philosophie #7, E2/E9/E10), correct-work >= v2.4.0 avec hook E8, chemins references/ sans accent, description enrichie | Les fichiers volumineux sont couverts sans surcharge de contexte ; le plan est vérifié par correct-work dès sa création |
| v3.7.0 | 2026-08-30 | Règles d'or (§1.8 : adaptation autonome sur blocage), disciplines d'ingénierie de prompts (§1.9), hook correct-work par phase (E9-E14) | Tout blocage devient un signal d'adaptation au lieu d'un arrêt ; chaque phase exécutée est vérifiée avant la suivante |
| v3.8.0 | 2026-09-06 | Unification du schéma evals (skill-creator) au §5, pipeline d'optimisation Z0-Z6, idempotence R1-R6, matérialisation agent | Evals comparables entre exécutions (with_skill vs baseline) ; toute ré-exécution du pipeline est garantie sans effet de bord |
| v3.8.1 | 2026-09-06 | Description Optimization (itération-3 workspaces) : description frontmatter enrichie « classification Type 1-4 » | Déclenchement du skill 9/9 (au lieu de 8/9) — le cas « classe cette tâche » est couvert |
| v3.9.0 | 2026-09-06 | Réimplantation des disciplines : source de vérité déplacée vers SHARED §7, matérialisation des 4 disciplines d'exécution | Non-duplication (§6.3) : les disciplines sont réutilisables par tous les skills en fonction héritée |
| v3.10.0 | 2026-09-07 | Règle d'or n°2 (régénération du plan après installation d'un écosystème) et n°3 (mise à jour à chaque nouvelle demande) | Le plan suit l'écosystème installé et les demandes de l'utilisateur sans réécriture destructrice (extension R2) |
| v3.11.0 | 2026-09-10 | Intégration du Prompt Engineering Kit v4.1 : 3 modes de raisonnement (CoT/Chaining/Hybride), blocs de sortie A-J, 9 règles critiques, 12 checks + scoring | Couche de raisonnement adaptative calibrée par les profils ressource — la profondeur d'analyse s'ajuste à la complexité détectée |
| v3.12.0 | 2026-09-19 | Mobilisation disciplinaire complète (audit N5-a) : table de mobilisation E1-E8, relations étendues aux 4 disciplines | Chaque étape de planification a ses disciplines assignées explicitement — plus d'angle mort disciplinaire |
| v3.13.0 | 2026-09-19 | Hooks patterns avancés (phase N20) : answer key E1, arbitre answer-key-checker E7/E8 (16 checks), Graph Diamond E9-E14, knowledge-observer E15 | Les décisions de planification deviennent vérifiables mécaniquement ; la parallélisation exceptionnelle est tracée |
| v3.16.0 | 2026-09-26 | Re-curation B13 des leçons knowledge-observer : KO-L001 (économie API 429), KO-L003 (arbitres à invariants dynamisés), KO-L004 (recalibrage croisé) | Les leçons d'économie et d'anti-dérive des arbitres sont institutionalisées dans la méthode |
| v3.17.0 | 2026-09-27 | Règle KO-L005 (généralisation règle d'or n°2), hook E1-RES (lecture B-11 + collecte G-RES + fraîcheur du plan) | Le plan est re-généré à chaque version de gen-plan modifiée et jugée valide ; l'ouverture de session est instrumentée (ressources) |
| v3.17.1 | 2026-10-02 | Propagation du renommage du skill prompt-engineering (ex agent-prompt-engineering ; census 118 refs/32 fichiers) | Références opératives alignées sur le renommage — plus de pointeur mort vers l'ancien nom |
| v3.17.2 | 2026-10-02 | Déclencheur verbatim « intègre dans le plan d'actions » (E13, directive propriétaire), correction E1 vers le pipeline PM-INSTALL v1.1.0, trigger_evals 7 → 8 cas | L'intégration d'une nouvelle demande au plan courant devient sans ambiguïté (déclencheur verbatim) |
| v3.18.0 | 2026-10-02 | Application M4 de la leçon L007 (matérialisation d'abord — pièges sparse-checkout), YAML §4 synchronisé sur le frontmatter installé | Les faits de matérialisation sont établis AVANT toute écriture et tout verdict d'arbitre (anti-faux-verdict) |
| v3.19.0 | 2026-10-03 | Routage de découverte (Task 23) : skills-inventory prioritaire, fallback skill-finder-cn avec contrôle cybersécurité audit-provenance, bascule unidirectionnelle ; garde É1-INSTALL --check à l'ouverture | La découverte des skills est priorisée et comparée au registre ; l'écart d'installation est détecté avant tout travail |
| v3.20.0 | 2026-10-04 | Task 29 : script maître ensure-installed.py intégré au skill, mode --preempt (réinstallation immédiate si ROOT absent), directive post-réinstallation download/plan-post-reinstall-<ts>.json | La réinstallation est garantie idempotente et le plan en cours est mis à jour de façon cohérente après réinstallation |
| v3.21.0 | 2026-10-09 | Règle d'or n°4 : toute utilisation d'un élément du dépôt passe par un clone git local (shallow), jamais une lecture distante API/raw/web ; askpass éphémère, zéro persistance de jeton | Accès au dépôt fiable (rate-limiting API 403 contourné) et discipline de sécurité du jeton institutionnalisée — **VERSION VIVANTE (corpus)** |

Fichiers archivés de la famille : `prompts-maitres/gen-plan/` — v3.6.1, v3.7.0, v3.8.0, v3.8.1, v3.9.0, v3.10.0, v3.11.0, v3.12.0, v3.13.0, v3.16.0, v3.17.0, v3.17.1, v3.17.2, v3.18.0, v3.19.0 (15 fichiers, SHA-256 au §5).
