# PLAN D'ACTIONS — Task 45 : Mission gen-plan(step) « Skills photo pour l'écosystème personnel »

> **Mode** : gen-plan(step) — enchaînement autonome des groupes séquentiels, correct-work(groupe, mode=CIBLE) après chaque groupe (max 2 rounds), correct-work(projet) en fin de chaîne (v3.22.0).
> **Session** : web-38713acd · **gen-plan** : v3.23.1 (hôte réinstallé à jour) · **Date** : 2026-10-20
> **Source** : directive propriétaire verbatim (7 étapes ordonnées) + pré-vol « vérifie que mon écosystème local est à jour » (exécuté PASS — pipeline eco_install_pipeline.py, hôte = dépôt @ 1020518, E1-INSTALL PRIORITE-NONE).

## Answer key (E1)

| # | Décision | Critère / vérification exécutable | Source | Priorité | Statut |
|---|---|---|---|---|---|
| D001 | Mode step autonome (pas de portes de confirmation — ≠ step-ok) | Le présent plan s'exécute groupe après groupe sans porte propriétaire ; correct-work(groupe) consigné après chaque groupe | Invocation `gen-plan(step)` explicite | S1 | PASS |
| D002 | Ordre propriétaire fait foi : clone-chat EN PREMIER (≠ leçon E23 « clonage en dernier ») | Groupe A = clone-chat avant tout le reste ; note au clone : un clonage de clôture pourra être proposé en fin de mission | Liste propriétaire étape 1 | S1 | PASS |
| D003 | Pré-vol écosystème (demande « avant ») | E1-INSTALL PRIORITE-NONE + hôte aux versions dépôt + clone tmp/KNOWLEDGE-repo @ 1020518 = origin/main | Message propriétaire « continue mais avant… » | S1 | PASS (exécuté) |
| D004 | Génération des skills iphone18/iphone17 selon précédent dessin-technique (Task 8 dépôt) : répertoire SKILL.md (frontmatter + §0 Contexte Système N2) + evals + trigger_evals ; contenu pipeline source = PMs `skills/@photos/` (lignage byte-identique) | Structure conforme skill-creator + diff vs précédent ; PMs source intacts (SHA-256) | Étapes 3-4 propriétaire | S1 | pending |
| D005 | Inscription au registre KB (33→35) + cross-references bidirectionnelles + recalibrage KO-L004 (arbitres/compteurs) — ordre explicite propriétaire (« pour mon écosystème personnel »), contrairement à Task 44 où l'inscription avait été écartée unilatéralement | Entrées 6 champs SHARED §2.2 ; verify-cross.py --check-context PASS ; compteurs recalibrés | Étapes 3-4 propriétaire | S1 | pending |
| D006 | Tests robustes = mode SÉRIE §10 de chaque PM : 2 photos × skill, pipeline §1→§9 complet par sortie, QC unitaire, rapport unifié, question unique finale par campagne | 2 sorties PA-TEST-002-* (iphone18) + 2 sorties PA-TEST-003-* (iphone17) ; QC grille complète par sortie ; rapports unifiés | Étapes 6-7 propriétaire | S1 | pending |
| D007 | Traitement d'image via SDK z-ai base64 (.mjs) — contournement CLI défaillant (erreur 1210, Task 42) | Scripts exécutés sans erreur de transmission ; sorties générées | Leçon Task 42 | S2 | pending |
| D008 | Push dépôt en fin de mission (commit + push PAT si valide ; si PAT révoqué → commit local + rapport honnête) | ls-remote montre le nouveau commit OU rapport note l'échec push | Précédent Task 44 | S2 | pending |
| D009 | Les skills générés portent les pipelines complets : iphone17 = v2.0 (archivé, R17/R16 d'époque), iphone18 = v1.0 (R18, preset iphone18_max) — chacun avec son périmètre d'époque honnête | SKILL.md contient §1→§13 opérationnels ; limites documentées | PMs @photos/ | S1 | pending |
| D010 | Plan persisté + worklog mis à jour par groupe (durabilité inter-tours, écraseur local) | Ce fichier existe + entrées worklog par groupe | Leçons Tasks 17/44 | S1 | PASS |

## Groupes séquentiels (mode step)

| Groupe | Étapes propriétaire | Contenu | correct-work(groupe) | Statut |
|---|---|---|---|---|
| **A** | 1 | clone-chat v2.0.1 de la session (7+1 étapes, 8 checks) → `download/` | CIBLE livrable clone | pending |
| **B** | 2 | correct-work(projet) — état écosystème + session (5 étapes, couplage gen-plan v3.23.1) | (est lui-même une vérification) | pending |
| **C** | 3-4 | Génération skills `iphone18` + `iphone17` (skill-creator + KB + KO-L004 + PM) | CIBLE skills générés + KB | pending |
| **D** | 5 | correct-work(projet) — vérification post-génération | (vérification) | pending |
| **E** | 6 | Test robuste iphone18 — 2 photos (copines + potos), série §10 | CIBLE sorties + rapport | pending |
| **F** | 7 | Test robuste iphone17 — 2 photos, série §10 | CIBLE sorties + rapport | pending |
| **Fin de chaîne** | — | correct-work(projet) final + worklog + rapport mission | — | pending |

## Invariants
- PMs `skills/@photos/` jamais édités (byte-identité R2) ; originaux `upload/` jamais modifiés (P0)
- Garde-fous photo G1-G7 + inventaire B6 respectés pendant les tests ; fidélité stricte des visages
- PAT jamais persisté (fichier/config/script) ; révocation rappelée au rapport final
- Max 2 rounds de correction correct-work par groupe ; verdict global = pire des verdicts
