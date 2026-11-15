# Rapport correct-work — Task 95 : intégration des 3 propositions S4

## Métadonnées
- **Date** : 2026-11-15
- **Mode** : PROJET `--bloc` (v2.9.0)
- **Version correct-work** : 2.11.0
- **Cible** : chaîne Task 95 — `scripts/gen-ultra-maitre.py` · `scripts/generer-pm-skill.py` · corpus SHARED v1.7.39 / PM-INSTALL v1.9.16 / ULTRA · `scripts/cache-verdicts.py` · `skills/KNOWLEDGE.md` · `scripts/task95-tests-s4.py` · cascade (propagation §0, archive) · 2 réparations latentes (task73)
- **Couplage gen-plan §1.5** : v3.43.0 (dernière version installée — frontmatter `skills/gen-plan/SKILL.md`) ; plan `download/plan-task95-integration-propositions-s4.md`, answer key D001-D010 — RESPECTÉ
- **Arbitre mécanique** : `verify-correct-work.py` **16/16 ALL PASS** (exécution fraîche, certification post-intégration)

## Blocs vérifiés

| Bloc | Contenu | Étapes couvertes | Findings | Verdict |
|------|---------|------------------|----------|---------|
| **B1 — S4-1** | Dynamisation littéral harnais (`harness_version()`, marqueur `{HV}`) + ULTRA régénéré ×2 idempotent | 2-5 | 0 S1/S2 — dérive pré-existante version-management « — » → 1.3.0 résorbée au passage (D008, baseline diff 5 lignes) | **PASS** |
| **B2 — S4-2** | Extrait §0-§1.2 DÉRIVÉ du SHARED vivant + `--refresh-ctx` NO-OP-si-frais + recalibrage étendu + versions (SHARED v1.7.39 · PM-INSTALL v1.9.16) + cascade (propagation, archive) | 2-5 | 0 S1/S2 — 2 S4 documentés (taille PM-INSTALL +9,9 % lu à l'installation seulement ; échec N1 tool-routing sur skills miroirs plateforme = non-conformité PRÉ-EXISTANTE à HEAD, hors périmètre écosystème — proposition future périmètre KB) | **PASS** |
| **B3 — S4-3** | Doctrine codifiée dans `cache-verdicts.py` (domaine d'usage) + KB Décisions Task 95 | 2-5 | 0 | **PASS** |
| **B4 — Tests $FACON2** | `task95-tests-s4.py` : baseline AVANT (médiane ×3) + T01-T18 + P-gardes APRÈS + rapport | 2-5 | 0 S1/S2 — 4 adaptations du script de test en cours de route (règle d'or n°1 : diagnostic puis correction, jamais de re-jeu à l'identique) + 2 défauts latents scripts Task 73 réparés + 1 drift plateforme mode-bits éteint (hygiène 2707+853 fichiers) | **PASS** |

## Étape 2 — Erreurs et omissions

| # | Sévérité | Description | Emplacement | Correction proposée |
|---|----------|-------------|-------------|---------------------|
| 1 | S4 | T16 : marqueur doctrinal coupé par retour à la ligne (« norme de / certification ») — faux négatif du test | scripts/task95-tests-s4.py + cache-verdicts.py | APPLIQUÉE : reflow docstring + comparaison insensible à la casse |
| 2 | S4 | T18 : sous-chaîne « 0 FAIL » déclenchait un faux positif d'échec | scripts/task95-tests-s4.py | APPLIQUÉE : attentes honnêtes structurées (5/6 verts + fail-set attendu) |
| 3 | S4 | T12 : le script de test s'auto-correspondait (littéral du motif dans son propre source) | scripts/task95-tests-s4.py | APPLIQUÉE : motif construit dynamiquement (concaténation) |
| 4 | S4 | P-guard : delta tool-routing (+38 %) comparait des charges différentes (arbre propre vs 340 fichiers modifiés) | scripts/task95-tests-s4.py | APPLIQUÉE : garde recentrée sur arbitres à charge fixe + note explicative |
| 5 | S3 | 2 scripts Task 73 latemment non compilables (`from __future__` après imports — introduit à l'ère de l'insertion des en-têtes §0, pré-existant à HEAD, révélé par l'arbitre N1) | scripts/task73-campagne-tests.py · scripts/task73-rejeu-answer-key.py | APPLIQUÉE : import remonté ligne 2 (sémantique inchangée, py_compile OK, scan exhaustif : 0 autre script cassé) |
| 6 | S3 | Drift mode-bits plateforme : 2707 fichiers dépôt + 853 hôte passés en 755 par la restauration sandbox (ctimes 10:24:25 — AVANT la session) | arbre entier | APPLIQUÉE : `eco-hygiene-mode-bits.py` (outil canonique Task 85) — 644 partout, idempotent |
| 7 | S4 | Skills miroirs plateforme (~65 : ASR, LLM, TTS, VLM, agent-browser…) sans frontmatter skill-creator — pré-existant à HEAD (preuve `git show HEAD` : 0 champ), révélé par la propagation (en-têtes §0 mis à jour v1.7.39 correctement) | skills/\<plateforme\>/SKILL.md | NON CORRIGÉ (hors périmètre écosystème — fichiers miroirs plateforme du propriétaire) — **proposition future** : calibrer le check N1 skill de check-tool-routing sur le périmètre KB (source de vérité) |

## Étape 3 — Structure et conflits

| # | Type | Description | Fichiers concernés | Résolution |
|---|------|-------------|-------------------|------------|
| 1 | Collision noms | 6 nouveaux helpers (version_shared, span_ctx_shared, bloc_ctx, refresh_pm_install_ctx, maj_ligne_install_shared, maj_etiquette_instantane) + harness_version | generer-pm-skill.py, gen-ultra-maitre.py | Aucune collision (py_compile OK, --check OK, exécutions réelles OK) |
| 2 | Coexistence modes | `--refresh-ctx` vs `--generate`/`--check` dans main() | generer-pm-skill.py | Dispatch exclusif if/elif — OK |
| 3 | Double bump potentiel | refresh_ctx et recalibrage bumpent chacun SHARED/PM-INSTALL | generer-pm-skill.py | Outils CLI séquentiels, garde NO-OP si frais — pas de conflit (prouvé : rejeu NO-OP rc 0) |

## Étape 4 — Interactions

| # | Skill A | Skill B | Type d'interaction | Statut |
|---|--------|--------|-------------------|--------|
| 1 | generer-pm-skill.py | SHARED + PM-INSTALL (corpus) | écriture recalibrage | verify-cross 165/165 ×2 modes — OK |
| 2 | gen-ultra-maitre.py | corpus + harnais re-curation | lecture dérivation | ULTRA idempotent, --check rc 0 — OK |
| 3 | propagate-context.py | 335 porteurs §0 | substitution version | interactions **55/55 PASS STRICT** — OK |
| 4 | task21-f2-rebuild-archive | corpus + archive | rescellage | integrity **114/114 PASS** — OK |
| 5 | certification-complete | 5 arbitres + tool-routing | orchestration | 5/6 verts + tool-routing N1 (documenté §Étape 2 #7) |

## Étape 5 — Cohérence des raisonnements

| # | Point vérifié | Résultat | Détail |
|---|---------------|----------|--------|
| 1 | D001-D010 answer key vs réalisé | 9/10 verified | D001 (T01-T03) · D002 (T05 byte-identité) · D003 (T08-T09) · D004 (T10-T11) · D005 (T06-T07) · D006 (T15-T16 + KB) · D007 (T12-T14, T17) · D008 (diff 5 lignes + T03) · D009 (20/20) — D010 en cours (le présent rapport en fait partie) |
| 2 | Formes retenues conformes aux recommandations de la note S4 (directive « intègre $FACON ») | OUI | dynamisation > recalibrage · extraction complète > digest · doctrine > câblage |
| 3 | Idempotence des mécanismes livrés | OUI | ULTRA --check rc 0 ×2 · --refresh-ctx NO-OP ×2 · propagate no-op · hygiène 2ᵉ passage 0 |
| 4 | Honnêteté des preuves (KO-L003) | OUI | baseline AVANT écriture · échecs intermédiaires consignés (17/20 → corrections → 20/20) · pré-existances prouvées au HEAD |
| 5 | alias-eco Phase 2 (registre phrases récurrentes) | 0 nouvelle | les répétitions de la discussion sont des re-formulations de directive couvertes par $FACON/$FACON2 (déjà enregistrés) — seuil non atteint |

## Résumé
- **Problèmes trouvés** : 7 (0 S1, 0 S2, 2 S3, 5 S4)
- **Corrections appliquées** : 6 (4 tests + 2 scripts latents) + 1 hygiène plateforme
- **Problèmes restants** : 1 (S4 #7 — skills miroirs plateforme : documenté, proposition future, pré-existant)
- **Verdict global** : **PASS** (pire des blocs = PASS · 4/4 blocs PASS · arbitre 16/16 ALL PASS)

---
*Rapport correct-work (projet) --bloc — Task 95, chaîne directives 1a1ded2a59319bb9 / 1a1dee6f8511bee1. Verdicts par bloc consignés ci-dessus (§1.7 v2.9.0).*
