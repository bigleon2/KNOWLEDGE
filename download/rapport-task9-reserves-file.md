# Rapport Task 9 — clôture des réserves + file gen-plan(step) (correct-work PROJET)

> **Session** : web-b4d7dd19 · **Mode** : gen-plan(step) sur gen-plan v3.23.1 · **Date** : 2026-10-12
> **Directive propriétaire** : (1) traiter les réserves consignées — « OK » pour PMs refactor-guard externes non verbatim (D009 — extension generer-pm 3→4 familles) + baselines A2 n°55 (QUOTA_OK) ; (2) poursuivre la file : correct-work(projet), conception/exécution des 3 tests complexes sur les deux skills n°55.
> **Commit** : `3475b17` (local — SANS push, règle d'or n°4 ; le push demeure conditionné à la validation explicite).

## 1. G-RES-1 — Réserve D009 CLOSE (4e famille refactor-guard vivante)

**Décision propriétaire D009 appliquée** : les PMs de la lignée externe refactor-guard (v1.2.0→v1.7.0, discussion 468a4c26) sont ACCEPTÉS non portés (non verbatim — provenance R4) ; le corpus démarre le PM refactor-guard à v1.7.0 ; la génération future est mécanique.

- **Bootstrap** : `PROMPT-MAITRE-REFACTOR-GUARD-v1.7.0.md` au corpus (321 lignes — sections SKILL.md portées verbatim §0-§4 + frontmatter YAML, 6/6 ancres `generer-pm-skill.py` vérifiées, idempotent R2) — `scripts/g1-bootstrap-pm-refactor-guard.py`.
- **Extension générateur** : `generer-pm-skill.py` 3→4 familles (FAMILLES + docstring KO-L004) — `scripts/g1-extensions-d009.py` (21 éditions verrouillées count==1 sur 9 fichiers).
- **Recalibrage croisé KO-L004** : SHARED **v1.7.5** (§6.1 +1 ligne PM, GEN-PLAN/PM-INSTALL recalibrés aux versions vivantes), PM-INSTALL **v1.6.5** (§2ter +1 ligne + note hors-pipeline, §2quater 3→4 familles), CORPUS_ATTENDU 8→9, propagation §0 v1.7.5 (98 skills + 60 scripts + 2 agents — idempotent ×2), ULTRA régénéré, re-scellement archive **9 entrées** round-trip OK, KB (D009 LEVÉE consignée), @historique par-skill (+section PM canonique).
- **Preuves** : `--check` **4/4 COHERENT ×2** ; `--generate refactor-guard` = **NO-OP** ; integrity 68/68 ×2.

## 2. G-RES-2 — Baselines A2 n°55 CLOSE (14/14, 0 dérive résiduelle)

**Gate QUOTA_OK levé par directive** (sonde KO-L001 verte préalable) — mesure complète 14 cas × 2 voies (`scripts/task9-baseline-a2-n55.py`, méthode SHARED §7 v2 réplique task18/task21) : **42 appels LLM réels, 0 vote null** (anti-fabrication R3).

| Skill | Voie M (mécanique) | Voie L (3 runs) | Traitement |
|---|---|---|---|
| refactoring-test v1.0.1 | 7/7 dès le 1er passage | 7/7 unanime | aucun requis |
| refactoring-engineering | 6/7 → **1 dérive** | 7/7 unanime | **Description Optimization v1.1.0** (protocole §7) |

- **La dérive** : cas négatif « Renforce le harnais : … gardes-fous » routé à tort par la voie M (collision lexicale `gard`+`fous` ↔ « Garde-fous mobilisés » de la description) — la voie L (3/3 NON) ne confirme jamais.
- **Le traitement** : `scripts/g2b-description-optimization.py` — « Garde-fous mobilisés pendant les opérations » → « **Sécurisation des opérations assurée par le skill refactor-guard** » (sémantique inchangée) ; cascade **v1.0.1→v1.1.0** (SKILL.md, KB heading + calibration, ECO_SKILLS, @historique par-skill) ; **re-mesure (`--remeasure-m`, votes L préservés) : 7/7 — verdict consolidé 14/14, ZÉRO dérive ×2 voies**.
- **R2 respecté** : les evals officielles sont inchangées — c'est la description qui est optimisée.
- Livrables : `download/rapport-baselines-a2-n55.md` + `scripts/baseline-a2-n55-report.json`.

## 3. G3 — Les 3 tests complexes + tests de clôture (tout idempotent ×2)

- **DÉCOUVERTE MAJEURE** : **purge plateforme de l'arbre hôte** entre les sessions — 15 fichiers projetés Task 8 disparus de `skills/` hôte (`@mon-ecosysteme/` ×7, `@historique/` ×6, `KNOWLEDGE.md`, `gen-plan/SKILL.md`, `correct-work/SKILL.md` — dossiers vidés ; 112/127 restants). Finding S2 (précédent Task 4 F4 : l'arbre hôte est celui réellement chargé par la plateforme).
- **Remédiation** : `scripts/g3-projection-hote-task9.py` — périmètre UNION (session + manifeste Task 8) = **128 fichiers, 113 copies, post-check byte-identité 128/128 ×2, idempotent** (exclusion R2 version-management maintenue).
- **3 tests complexes (Task 8)** : recalibrage KO-L004 T2.3 (corpus 9) après T2.10 (4 familles) → **39/39 PASS ×2** (T1 détecter/évaluer/grapher · T2 gouverner zéro-régression · T3 fusion ×2 arbres).
- **Tests de clôture T-RES** (`scripts/task9-tests-reserves.py`) : **26/26 PASS ×2** — T-RES-1 D009 (11 checks), T-RES-2 baselines A2 (9 checks), T-RES-3 remédiation purge (5 checks).

## 4. G4 — correct-work(PROJET) : VERDICT PASS

| # | Arbitre | Résultat |
|---|---|---|
| 1 | verify-cross --check-context | **100 %** (0 erreur) |
| 2 | integrity (manifeste écrit ×2) | **68/68** (corpus 9, archive 9/9 byte-identique, 0 doublon) |
| 3 | interactions (graphe KB) | **47 PASS / 0 WARN / 0 FAIL — PASS STRICT** |
| 4 | task17 / task17b | **16/16** · **16/16** |
| 5 | verify-correct-work | **ALL PASS (16/16)** |
| 6 | generer-pm --check ×2 | **4/4 COHERENT** (4 familles — D009) |
| 7 | propagation §0 v1.7.5 | idempotent ×2 (0/0/0) |
| 8 | re-scellement archive | round-trip **9/9** (véhicule v2.2) |
| 9 | tests (3 complexes + T-RES) | **39/39 + 26/26 — ×2 idempotents** |

**Commit local `3475b17`** (180 fichiers, +2267/−253) — SANS push (règle d'or n°4).

## 5. Réserves et restants

- **Clôturées** : D009 (4e famille vivante) ; baselines A2 n°55 (mesurées, 0 dérive résiduelle).
- **Nouvelle réserve documentée (R-T9-1)** : la purge plateforme de l'arbre hôte est structurelle — chaque session hors hôte exige une re-projection (l'outil `g3-projection-hote-task9.py` est idempotent et réutilisable ; le manifeste Task 9 fait foi).
- **Restant propriétaire (inchangé)** : push du commit (validation explicite — pat one-shot à re-fournir, anti-persistance) ; révocation du PAT affiché en clair en Task 7-G1.
