# Rapport correct-work Mode PROJET — Task 22 (installation → idempotence → push conditionnel)

**Date** : 2026-10-03 · **Skill** : correct-work v2.7.0 (gen-plan v3.18.0 session, plan `download/plan-task22-idempotence-skills-agents.md` — answer key D001-D008) · **Périmètre** : état local du dépôt bigleon2/KNOWLEDGE après corrections Task 22.

## Étape 2 — Découverte et invariants

- Couche locale = HEAD `4328d66` + couche Task 21 non commitée (36 fichiers contenu-modifiés + 18 nouveaux) + corrections Task 22.
- D001 vérifié : périmètre sémantique = contenu-modifié (hors `.next/` et hors 291 drifts de mode 100644→100755 S4, documentés Task 18/20).

## Étape 3 — Findings (constats)

| ID | Constat | Sévérité | Correctif appliqué (Task 22) |
|----|---------|----------|------------------------------|
| F22-1 | Orchestrateur ULTRA hors point-fixe (KO-L004) : montées Task 18/21 non propagées (memory-engineering 1.1.0, prompt-engineering 2.2.0, script-creator 1.1.0, skills-inventory 1.1.0, agent-creator 2.1.0 absentes du §3) | S2 | `gen-ultra-maitre.py` régénéré (SHA `c435a2f3`, `--check` no-op), archive rescellée round-trip 26/26, intégrité re-verdict 56/56 |
| F22-2 | 5 SKILL.md sans `tags:` frontmatter (audit-provenance, correct-py, script-creator, script-reviewer, skill-creator) — écart conformité skill-creator §2 | S3 | tags neutres insérés (radicaux du nom — zéro dérive de calibration, preuve : V6 re-verdict 18 OK / 8 dérivants identiques) |
| F22-3 | Agrégateur `certification-complete.py` : entrée verify-correct-work invoquée sans chemin de rapport (crash IndexError) — agrégateur inopérant | S2 | dérivation dynamique du dernier rapport correct-work (KO-L003) — agrégateur réparé et étendu 5→6 arbitres |
| F22-4 | Routage des outils dédiés non tracé explicitement (audit historique Tasks 18-21 : 4/9 explicites — gen-plan, correct-work, prompt-engineering, knowledge-observer ; 5/9 conformité implicite via arbitres) — directive propriétaire : enforcement automatique | S2 (directive) | **nouvel arbitre `check-tool-routing.py`** (N1 preuves mécaniques par artefact + N2 routage normatif par session), branché dans l'agrégateur (6ᵉ arbitre), décision KB consignée — le routage est désormais automatique à chaque certification |
| F22-5 | Hérités : S3 frontière plateforme correct-work→fullstack-dev (WARN, hérité Task 19) ; 8 dérivants V6 consignés (cas structurels radical-du-nom + C006, décision Task 21) ; drift S4 mode + artefacts `.next/dev` (S4, D007 Task 18) | S3/S4 | aucun — réserves héritées, documentées |

## Étape 4 — Vérifications mécaniques

- Idempotence f(f(x))=f(x) : installation double-exécutée (empreinte `f2f1f382` ×2), arbitres ×2 déterministes, ULTRA `--check` no-op.
- Arbitres : verify-cross 78/78 (×2 modes), check-ecosysteme-integrity 56/56, test-coherence-interactions 48 PASS/1 WARN hérité/0 FAIL, answer-key-checker ALL PASS, V6 18/26 (8 consignés, zéro régression), check-tool-routing 10/10.
- Certification consolidée (agrégateur 6 arbitres) : **PASS AVEC RÉSERVES (0 échec, 1 avertissement hérité)**.
- Harnais triggers voie M (Task 19) : rc=0, stable.
- KB : 26 entrées versionnées intactes + décision Task 22 consignée (§Décisions).

## Étape 5 — Verdict

**PASS AVEC RÉSERVES** — 0 échec nouveau ; 5 constats, tous corrigés dans la couche Task 22 (F22-1 à F22-4) ou hérités documentés (F22-5). Les réserves subsistantes sont intégralement héritées des Tasks 19-21 (S3 plateforme, 8 dérivants consignés, S4 cosmétique). L'objectif D007 (push conditionné à l'idempotence) est levé : le verdict d'idempotence est PASS.
