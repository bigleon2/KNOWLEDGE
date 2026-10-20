# Plan Task 47 — Directive propriétaire multi-étapes (session web-38713acd)

> gen-plan — plan persisté AVANT action (règle 3) ; version YAML intégrale : `scripts/task47-plan-directive.yaml`. Profil : NORMAL. Source : clone certifié `tmp/KNOWLEDGE-repo` @ HEAD 3fa587d (poussé en D1).

## Routage normatif de session (citation des skills dédiés)

| Type d'artefact produit par cette session | Skill dédié cité |
|---|---|
| Planification de la tâche (ce plan, phases P0-P8) | **gen-plan** v3.23.1 |
| Scripts de session (`task47-install-ecosysteme.py`, `task47-audit-iphone19.py`, `task47-*.mjs`) — conventions structurelles, tests mécaniques, idempotence | **script-creator** |
| Prompt maître `iphone19-photos.md` v0.9.0 (artefact de prompt : PM) | **agent-creator** |
| Skill métier `skills/iphone19/` (SKILL.md + frontmatter, evals/evals.json + trigger_evals.json — conventions structurelles) | **skill-creator** |
| Déploiement des artefacts dans l'arbre (injection Contexte Système 3 niveaux, gardes INFRA-1..INFRA-3, conventions de déploiement) | **script-mon-ecosysteme-infrastructure** |
| Vérification du travail de session (D5, après D3+D4) | **correct-work** v2.7.0 (Mode PROJET) |
| Leçons de session (worklog, échecs documentés) | **knowledge-observer** |

## Directives (ordre propriétaire)

| ID | Action | État |
|---|---|---|
| D1 | PUSH skills iphone17 + iphone18 → GitHub `bigleon2/KNOWLEDGE` (dossier skills/) — PAT éphémère non persisté | ✅ FAIT — push `1020518..3fa587d main`, rc=0 |
| D2 | Installer l'écosystème personnel sur le profil local (PM install v1.7.1, profil COMPLET) | 🔄 EN COURS — sync fait, certification 5/6 |
| D3 | Créer le skill iphone19 (migration ANTICIPÉE autonome, v0.9.0, fonctionnelle/cohérente/optimisée) | ⏳ |
| D4 | Tester iphone19 sur « les copines » + « les potos » (PA-TEST-005, série §10, 1 traitement/photo, zéro modification/retouche, G1-G7 stricts) | ⏳ |
| D5 | correct-work (projet) | ⏳ |
| D6 | PUSH skill iphone19 → GitHub (avec KB, @photos, rapports, worklog) | ⏳ |
| D7 | (repris après gen-plan) Comparaison côte à côte « les copines » ADAPTÉE à la photo originale — 5 versions (P0, P1-P6, 17_max, 18_max, 19_max), composite PIL pur | ⏳ |
| D8 | (transversal) Remède erreur SSE : appels SDK via `createVision` + `thinking: disabled` / `images.generations.edit` — jamais de flux stream parsé en JSON | appliqué |

## Invariants

- R2 : jamais éditer les sources certifiées — iphone19 = NOUVEAU document.
- G1-G7 + inventaire B6 intacts dans `iphone19-photos.md` v0.9.0 ; originaux `upload/` jamais modifiés (sha256 vérifiés avant/après).
- PAT propriétaire : usage éphémère (env), jamais persisté, jamais committé.
- Honnêteté : statut [ANTICIPÉE]/[SPÉCULATIF-RUMEUR] visible (frontmatter, description, §0, §6.10-analog, limites) ; versionnement v0.9.0 (v1.0.0 réservé à la génération confirmée — même mécanique que le squelette §6.10, activée sur arbitrage propriétaire explicite).
