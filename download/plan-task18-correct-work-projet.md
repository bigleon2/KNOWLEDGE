# Plan Task 18 — directive gen-plan « correct-work(projet) + boucle QUOTA + baselines hors périmètre (c) »

> **Session** : web-bbbeab47 · 2026-10-03 · **Directive propriétaire** : `gen-plan : { exécute "gen-plan:correct-work(projet)" ; FAIS TANT QUE (QUOTA_OK==FALSE) {...} ; Puis LORSQUE (confirm LLM levé) → session gen-plan pour matérialiser les baselines de (hors périmètre de la suggestion (c)) }`
> **Hook E1-RES** : lecture préalable B-11 worklog ✓ (Tasks 0, 1-3) · collecte G-RES ✓ (monitor.py — verdict OK, niveaux 0) · fraîcheur plan ✓ (nouvelle directive → plan neuf)
> **Type (E3)** : Type 2 — analyse/vérification écosystème skills (correct-work §10.6 « Écosystème skills ») · **Profil (E6)** : NORMAL (aucun signal de pression)

## Answer Key (E1 — hook obligatoire)

| ID | Décision | Vérification exécutable | Source | Priorité | Statut |
|----|----------|------------------------|--------|----------|--------|
| D001 | Mode correct-work = **PROJET** (cible = projet écosystème complet via PM orchestration) | SKILL.md §A ligne « correct-work(projet) » + §1.2 tableau mode PROJET | correct-work/SKILL.md | S1 | PASS |
| D002 | Couplage gen-plan OBLIGATOIRE à Étape 1 — version installée = **v3.18.0** (frontmatter = source de vérité) ≥ plancher v3.7.0 | `version: 3.18.0` frontmatter gen-plan/SKILL.md | correct-work §1.5 | S1 | PASS |
| D003 | Boucle QUOTA conforme KO-L001 : **une seule sonde par tour**, zéro boucle d'attente en-tour ; sonde du 2026-10-03 → **QUOTA_OK = TRUE** (2 tokens complétés) | sortie z-ai CLI avec `"content"` parsable | SKILL gen-plan §1.14 | S1 | PASS |
| D004 | Levée du confirm LLM = re-exécution **idempotente** `scripts/task17-baseline-a2.py` (voie M déterministe rejouée à l'identique, voie L votera réellement) | script présent, cwd z-ai valide, parsing `"content"` vérifié sur sonde | rapport n54 §4 | S1 | PASS |
| D005 | « Baselines hors périmètre (c) » = **memory-engineering v1.0.0** — seule discipline n°54 demeurée EN ATTENTE ((c) cite fleet+spec uniquement) | memory-engineering/SKILL.md §5 « EN ATTENTE » + §7c rapport analyse | §7c + SKILL §5 | S1 | PASS |
| D006 | `baseline-pending-n34.json` **absent du clone** → statut « non matérialisé » consigné (KO-L007 — distinct d'un échec) ; référence résorbée à la matérialisation | glob **/baseline-pending* = 0 résultat | worklog Task 17 | S2 | PASS |
| D007 | Publication finale selon **protocole Task 7/14** (PAT utilisateur éphémère, origin sans jeton, audit anti-persistance 0 occurrence) | audit `git log -p` post-push | worklog Tasks 1-3 | S2 | PASS |
| D008 | Dérive éventuelle voie L → **Description Optimization obligatoire** (protocole A10/A14) ; aucune fabrication de résultats (R3) | colonnes voie L du rapport JSON = votes réels | rapport n54 §1 | S1 | PASS |

## Étapes (E1-E15) — #token

| Étape | Action | #token |
|-------|--------|--------|
| E1 | Analyse directive + answer key ci-dessus + hook E1-RES | 400 |
| E2 | Inventaire : worklog, KB, arbitres, rapports Task 17, état git | 500 |
| E3 | Classification Type 2 (vérification écosystème) | 100 |
| E4 | Estimation #token : totale ~5300 (vérification ~2800 + levée confirm ~900 + matérialisation ~1600) | 100 |
| E5 | Skills : correct-work v2.7.0 (PROJET), gen-plan v3.18.0, knowledge-observer (E15), resource-monitor (E1-RES ✓), arbitres scripts | 200 |
| E6 | Profil NORMAL | 50 |
| E7 | Création du présent plan | 300 |
| E8 | Validation : arbitre answer-key-checker (16 checks) + verify-cross + verify-correct-work + check-ecosysteme-integrity + test-coherence-interactions — verdict PASS requis | 400 |
| E9 | Lancement exécution — correct-work PROJET Étape 1 = présent plan (couplage respecté) | 100 |
| E10 | correct-work Étapes 2-3 : erreurs/omissions (données factuelles Task 17 : baselines, confirm LLM armé, SKILL §5, KB) + structure/conflits (état git, conventions, cross-refs) | 900 |
| E11 | correct-work Étape 4 : interactions (deps YAML bidirectionnelles, couplage correct-work↔gen-plan, KB 26 entrées) | 400 |
| E12 | correct-work Étape 5 : cohérence des raisonnements (verdicts vs fichiers, chronologie Task 17, réserves honnêtes) | 400 |
| E13 | Ajustement (si écart détecté) + rapport `download/rapport-correct-work-projet-task18.md` + verdict | 500 |
| E14 | Boucle QUOTA : re-exécution task17-baseline-a2.py (sonde unique KO-L001) → **levée confirm LLM** ; 429 persistant → pause motivée « réessaie dans 30 min » | 400 |
| E15 | Session gen-plan n°2 : matérialisation baselines hors périmètre (c) — memory-engineering voie M+L (`scripts/task18-baseline-a2-memory.py`), consignation confirm LLM fleet/spec, KB, worklog, push Task 7/14 | 700 |

## Hooks phase E9-E14

PASS CIBLE après chaque phase (correct-work §5.4 gen-plan) ; E15 knowledge-observer modes M1-M2.
