# Plan Task 48 — Directive propriétaire multi-étapes (session web-38713acd, suite — 2026-10-21)

> gen-plan v3.23.1 mode **(step)** — plan persisté AVANT action (règle 3) ; version YAML intégrale : `scripts/task48-plan-directive.yaml`. Profil : NORMAL (G-RES niveau 0). Source : clone certifié `tmp/KNOWLEDGE-repo` @ HEAD e62f354 (poussé — GitHub à jour). Préalable exécuté : **étape 1 installation écosystème profil local COMPLET** (réinstallation post-wipe PM-INSTALL §3.4 + recalibrage KO-L004 ECO_SKILLS 35→36 + bidirectionnalité skill-creator↔iphone19 + rescellage archive v2.3 + **certification 6/6 arbitres PASS** — `download/rapport-installation-ecosysteme-task48.json`).

## Routage normatif de session (citation des skills dédiés)

| Type d'artefact produit par cette session | Skill dédié cité |
|---|---|
| Planification de la tâche (ce plan, groupes G1-G6) | **gen-plan** v3.23.1 mode (step) |
| Prompts maîtres @photos bumpés (iphone17 v2.1, iphone18 v1.1, iphone19 v0.10.0/v0.11.0 — artefacts de prompt : PM) | **agent-creator** |
| Skills métier bumpés (skills/iphone17, iphone18, iphone19 — SKILL.md + evals) | **skill-creator** |
| Scripts de session (task48-*.py, task48-*.mjs — conventions structurelles, tests mécaniques, idempotence) | **script-creator** |
| Déploiement des artefacts dans l'arbre (projections, KB, @historique, archive) | **script-mon-ecosysteme-infrastructure** |
| Vérification par groupe + projet (CW CIBLE après chaque groupe, CW PROJET en S6) | **correct-work** v2.7.0 |
| Leçons de session (worklog, échecs documentés) | **knowledge-observer** |
| Archivage final de la discussion (S7) | **clone-chat** v2.0.1 |

## Directives (ordre propriétaire)

| ID | Action | État |
|---|---|---|
| S1 | Vérifier que iphone19 émule le pixel binning (frandroid, iPhone 19 Pro 200 Mpx, binning 16-en-1 → 12,5 MP) ; si non-émulé → bump v0.10.0 [ANTICIPÉE] avec R19 sourcée (statut [RUMEUR] conservé) | ⏳ |
| S2 | Même comparaison enrichie du rendu 19 pour « Les Potos » (réponse §9 : « sans modification, ni retouches ») — campagne PA-20261021-006 | ⏳ |
| S3 | Rendre iphone17/iphone18/iphone19 fonctionnels et optimisés pour les photos de 1944 (bumps v1.1.0 / v1.1.0 / v0.11.0, archivage R4, KB, re-certification) | ⏳ |
| S4 | Test robuste des 3 skills sur « libération après guerre » (réponse §9 : « sans modification, ni retouches ») — campagne PA-20261021-007 | ⏳ |
| S5 | Même comparaison enrichie des rendus 17/18/19 pour « libération après guerre » | ⏳ |
| S6 | correct-work (projet) | ⏳ |
| S7 | clone-chat | ⏳ |
| D010 | Clôture dépôt : commit + PUSH GitHub (PAT éphémère — précédent propriétaire D1/D6 Task 47) | ⏳ |

## Answer key (E1 — synthèse ; détail dans le YAML)

| ID | Décision | Vérification exécutable | Priorité |
|---|---|---|---|
| D001 | S1 : vérification pixel binning vs article frandroid ; constat attendu = NON émulé (200 MP exclu Task 47 §4.4) → corrective bump v0.10.0 + R19 | grep binning/200 MP fonctionnels PM v0.10.0 + auto-audit A1-A8 + diff documenté | S1 |
| D002 | S2 : rendu 19 potos RÉGÉNÉRÉ avec v0.10.0 (PA-TEST-005-2 = v0.9.0, périmé pour la comparaison) ; zéro retouche (§9 pré-décidée) | sha256 P0 avant/après + QC 12 critères + candidats versionnés | S1 |
| D003 | S2 : comparaison enrichie = format D7 Task 47 (5 versions + guide de lecture + rapport 8 QC) | composite PIL pur, sha256 5 sources intacts, 6/6 panneaux valides | S1 |
| D004 | S3 : renforcement chirurgical 1944 des 3 PMs (N&B argentique, grain, rayures, fidélité historique — G1-G7/B6 intacts) + bumps MINOR ×3 + archivage R4 | auto-audits blocs intangibles byte-identiques + KB/ECO_SKILLS/archive recalibrés + certification 6/6 | S1 |
| D005 | S4 : 1 traitement par skill sur libération (17→18→19), zéro retouche, rendu conservateur d'emblée (leçon PA-TEST-005) | QC 11/12/12 critères + P0 intacts + budget itération 2/2 respecté | S1 |
| D006 | S5 : comparaison enrichie libération (P0, P1-P6 [campagne 19], 17_max, 18_max, 19_max + guide adapté 1944) | composite PIL pur + sha256 + rapport format copines | S1 |
| D007 | S6 : correct-work Mode PROJET (C01-C20 pattern task47 adapté) | verdict PASS requis (max 2 rounds de correction) | S1 |
| D008 | S7 : clone-chat v2.0.1 (7+1 étapes, étape 3.5 Context Drift) | clone scellé, idempotent, 8 checks S1-S8 | S1 |
| D009 | Transversal : remède SSE (createVision + thinking disabled ; jamais de stream parsé) | zéro erreur SSE « Unexpected token 'd' » | S2 |
| D010 | Clôture : commit + push GitHub (PAT éphémère non persisté) | push rc=0, dépôt GitHub à jour | S3 |
| D011 | Invariants : R2/R4, G1-G7/B6, P0 intacts, statut ANTICIPÉE visible, honnêteté 1944 | vérifiés par CW(CIBLE) par groupe + CW(projet) | S1 |

## Invariants

- R2 : jamais éditer les sources certifiées en place — bumps = nouveau contenu versionné + archivage @historique R4 (byte-identité) ; projections régénérées VERBATIM (mécanique task45c).
- G1-G7 + inventaire B6 intacts dans les 3 PMs bumpés ; originaux `upload/` jamais modifiés (sha256 avant/après).
- Statut ANTICIPÉE iphone19 visible partout ; v1.0.0 réservé à la génération confirmée.
- Honnêteté 1944 : aucune colorisation inventée, aucun élément ajouté — fidélité historique stricte.
- PAT : éphémère (env), jamais persisté, jamais committé.
