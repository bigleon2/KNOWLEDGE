# Historique par skill — correct-work

> **Version** : 1.0.0 — **Date** : 2026-10-11 (Task 17-B, session web-b93f42fa — directive propriétaire « un historique par skill »)
> **Version vivante (corpus)** : v2.7.0 — `skills/@mon-ecosysteme/PROMPT-MAITRE-CORRECT-WORK-v2.7.0.md` (sa table §7 fait foi)
> **Versions archivées** : 4 PMs (v2.4.0 → v2.6.0) dans `prompts-maitres/correct-work/` — sceau SHA-256 au README §2
> **Provenance** : tables migrées verbatim de `historique-versions-prompts-maitres.md` §3 (fichier retiré après migration — R4 une information, une source ; Task 17-B)

## Famille CORRECT-WORK — 10 versions (skill : correct-work)

**Particularité durable du skill** : vérification et correction de travaux pour assistant IA — 5 étapes, 4 modes (PROJET, CIBLE, AVEUGLE, + rapport), verdicts S1-S4, métriques de performance, checklists opérationnelles, hooks gen-plan (E8 + contrôle par phase E9-E14), arbitre verify-correct-work (16 checks).

| Version | Date | Améliorations implantées (source §7 du PM v2.7.0) | Avantage par rapport à la version précédente |
|---------|------|---------------------------------------------------|----------------------------------------------|
| v1.0.0 | 2026-07-18 | Version initiale, vérification basique | — (point de départ) |
| v2.0.0 | 2026-07-29 | Ajout du Mode CIBLE, amélioration du rapport | Vérification d'un élément précis en plus du projet entier ; rapport plus exploitable |
| v2.1.0 | 2026-07-29 | Intégration gen-plan à l'Étape 1 | Toute vérification s'appuie d'abord sur un plan structuré au lieu d'un balayage ad hoc |
| v2.2.0 | 2026-07-29 | Registre KB (gen-plan >= v3.3.0), kb_path, --kb-skill, matrice dynamique | Les vérifications consultent le registre vivant de l'écosystème (contexte à jour) |
| v2.3.0 | 2026-08-09 | Refactoring du prompt maître : extraction du socle commun SHARED | Déduplication : les informations communes vivent une seule fois dans SHARED (R4) |
| v2.4.0 | 2026-08-09 | Support multi-cibles, découplage gen-plan (mode autonome), métriques de performance, checklists opérationnelles (§4.6-§4.10), scripts/ + evals/, hook gen-plan E8, verify-cross --mode correct-work (8 checks KB) | Vérifications opérables même sans gen-plan présent, instrumentées (scripts + evals) et branchées sur le hook E8 de gen-plan |
| v2.5.0 | 2026-09-06 | Unification du schéma evals (skill-creator) au §5 (evals.json, trigger_evals.json, workspaces) | Evals comparables entre exécutions (with_skill vs baseline) — même référentiel que gen-plan |
| v2.5.1 | 2026-09-06 | Description Optimization (itération-3) : description frontmatter enrichie « erreurs, omissions, incohérences » | Déclenchement du skill 8/8 (au lieu de 6/8) — les cas « correction » et « omissions/incohérences » sont couverts |
| v2.6.0 | 2026-09-19 | 4e mode AVEUGLE (Second Opinion — re-vérification sans accès au premier verdict), hook 2nd opinion agent-driven à l'Étape 5 (inputs filtrés), maximum 2 rounds de correction par artefact | Le biais de confirmation est éliminé (le second verdict ne voit pas le premier) ; la boucle de correction est bornée (SHARED §4.4) |
| v2.7.0 | 2026-10-02 | Couplage gen-plan OBLIGATOIRE à l'Étape 1 (résolution dynamique de la dernière version installée) — fin du mode autonome ; ARRÊT EXPLICITE si gen-plan est indisponible ou corrompu ; §5.4 aligné sur la forme installée certifiée (7 cas trigger_evals) | Cohérence méthodologique garantie : toute vérification est planifiée par gen-plan, jamais improvisée — **VERSION VIVANTE (corpus)** |

Révisions documentaires de la famille (sans changement de version) : session A11 2026-09-06 (§B pointeur disciplines → SHARED §7) ; Task 16 2026-10-02 (v2.6.0 et v2.7.0 RECONSTITUTIONS par diffs chirurgicaux méthode B1 — `scripts/materialise-pm-correct-work.py` — les originaux perdus au wipe, provenance tracée en tête de PM, aucun faux lignage) ; Task 14 2026-10-10 (§2.6/§9.2/§10.1 alignés sur le SKILL.md v2.7.0 certifié, corruption « ode] » réparée, calibration de forme).
Fichiers archivés de la famille : `prompts-maitres/correct-work/` — v2.4.0, v2.5.0, v2.5.1, v2.6.0 (4 fichiers, SHA-256 au §5).
