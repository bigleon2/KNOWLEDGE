# Plan Task 47 — correct-work (projet) — Phase 1 via gen-plan (§1.5 — obligatoire)

> Vérification du travail Task 47 (directive propriétaire multi-étapes D1→D6, session web-38713acd). gen-plan v3.23.1 installé (D2) — le présent plan en est le produit. Estimation #token : ~6k (15 checks mécaniques + rapport).

## Pré-vérification
- Prompt maître de référence : directive propriétaire D1→D6 (message session) + PM `iphone-photos-migration.md` v1.0 + PM install v1.7.1 — disponibles et lus ✓
- Livrables attendus (listés au plan directeur `download/plan-task47-directive.md`) :
  - D1 : push GitHub `bigleon2/KNOWLEDGE` — skills iphone17 + iphone18 + rapport Task 45 (commits 5ea3548 + 3fa587d)
  - D2 : écosystème installé profil COMPLET + certification 6 arbitres + marqueur
  - D3 : PM `skills/@photos/iphone19-photos.md` v0.9.0 [ANTICIPÉE] + skill `skills/iphone19/` complet + entrée KB + auto-audit PASS
  - D4 : campagne PA-TEST-005 — 2 finals + 2 intermédiaires + QC 12/12 ×2 + rapport unifié + P0 intacts
  - (D5 : le présent correct-work ; D6 : push iphone19 — en aval, vérifié par son propre push rc=0)

## Phase 2 — Erreurs et omissions (checks C01-C13)
Chaque directive vs son livrable : C01-C02 (D1 push + contenu), C03-C05 (D2 installation + certification + garde), C06-C10 (D3 PM/skill/audit/KB/R2), C11-C13 (D4 livrables/QC/P0). Classification S1-S4 de tout écart.

## Phase 3 — Structure et conflits (checks C14 + conventions)
C14 : SÉCURITÉ — PAT propriétaire ABSENT de tout fichier (grep récursif) ; conventions : kebab-case, semver 0.9.0, nommage PA-TEST-005-*, format d'entrée KB, cross-refs frontmatter ↔ KB ↔ PM cohérentes.

## Phase 4 — Interactions
Dépendances déclarées du skill iphone19 (skill-creator, VLM, image-edit ≥ v1.0.0) présentes dans l'arbre ; versions minimales respectées ; script embarqué editer-image.mjs identique à l'éprouvé (diff vs iphone18).

## Phase 5 — Cohérence
Statut ANTICIPÉ cohérent sur toute la chaîne (frontmatter, PM en-tête/§0/§6.1/§6.10, KB, rapport) ; candidats versionnés (v1-v3 potos — jamais d'écrasement) ; décisions documentées (déviation §6-1, aucune règle R19, squelette iphone20) alignées avec les actions.

## Post-vérification
Rapport `download/rapport-cw-projet-task47.md` + verdict (PASS / PASS AVEC RÉSERVES / FAIL) + worklog mis à jour.
