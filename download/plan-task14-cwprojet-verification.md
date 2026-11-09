# Plan Task 14-CW — correct-work PROJET : vérification de la couche Task 14 (KO-L004 + C006)

## Métadonnées
- **Date** : 2026-10-10 (session web-b93f42fa)
- **Directive propriétaire** : « correct-work(projet) sur le projet actuel » (précision 2026-10-10, avant continuation)
- **gen-plan** : v3.21.0 (frontmatter installé `skills/gen-plan/SKILL.md` — source de vérité, contrat §1.5 correct-work) ; hook É1-INSTALL frais rc0 INSTALLE (head 2992bae, kb_entrees=28)
- **correct-work** : v2.7.0, mode PROJET (couplage Étape 1 OBLIGATOIRE — §1.5) ; déclencheur §A « correct-work(projet) »
- **PM du projet** : `skills/@mon-ecosysteme/PROMPT-MAITRE-CORRECT-WORK-v2.7.0.md` — disponible et lisible (726 L, md5 e64e85ce)
- **Profil** : NORMAL (hook E1-RES : worklog lu — entrées 12 → 14-S0 présentes)
- **Estimation #token** : ~10 000 (grille §4)
- **Règle d'or n°2** : 0 commit, 0 push — HEAD 2992bae ; vérification en lecture seule (livrables nouveaux limités à : plan + rapport + entrée worklog)

## E1 — Livrables + critères de succès
1. **Étapes 1-5** correct-work PROJET sur la couche Task 14 (périmètre : 6 fichiers M + plan-task14 + rapport-task14 + tmp/) — chaque claim du rapport Task 14 re-prouvé par mesure byte-level indépendante (KO-L003 : un verdict non reproduit n'est pas une preuve).
2. **Rapport** `download/rapport-correct-work-projet-task14.md` (format §2.4 — Étapes 1-5 + Résumé verdict §10.5).
3. **Worklog** entrée 14-CW (format §2.6 — « Agent: correct-work v2.7.0 »).
4. **Proposition commit/push** (GO propriétaire requis — couche Task 14 + artefacts correct-work PROJET).

## E2 — Ressources (mesuré)
- Couche Task 14 en arbre : 6 M (PM v2.7.0, sfc trigger_evals, check-triggers-replay, task21-f2-rebuild-archive, ecosystem-integrity.json, triggers-replay-report.json) + 2 nouveaux download/ (plan + rapport Task 14) + tmp/ (13 éléments, hors suivi).
- Baseline arbitres au rapport Task 14 (reproduite en session 14-S0) : vcw 16/16 (shim) · integrity 60/60 · coherence 48/3/0 · verify-cross 84/84 · generer-pm 3/3 · answer-key-checker 16/16 rc0.
- Claims à re-prouver (Étape 2) : PM greps ×4 + md5 e64e85ce ; sfc bare-liste 8 cas verbatim md5 24df0227 ; verify-cross.py 0 diff (D004) ; archive re-scelée round-trip 28 entrées 0 divergent.

## E3 — Type 2 (ingénierie écosystème — protocole de vérification ; rapport .md secondaire)

## E5 — Skills mobilisés
gen-plan (plan de vérification — §1.5) · correct-work v2.7.0 PROJET (étapes 2-5) · arbitres : verify-correct-work (shim → canonique), check-ecosysteme-integrity, test-coherence-interactions, verify-cross, generer-pm-skill, answer-key-checker · leçons KO-L003/L004 appliquées en continu.

## E7 — Séquence (série par défaut — philosophie #4)
| Phase | Contenu | #token |
|---|---|---|
| A | Plan + answer-key-checker 16/16 (E8) | 1 500 |
| B | Étape 2 : byte-proof claims PM/sfc/D004/archive + re-run indépendant des 5 arbitres | 3 000 |
| C | Étapes 3-4 : structure/conventions + interactions/dépendances | 2 000 |
| D | Étape 5 : cohérence des raisonnements → verdict §10.5 (AVEUGLE si divergence persistante) | 1 500 |
| E | Rapport §2.4 + worklog 14-CW + proposition commit | 2 000 |

## Answer key (hook E1 — décisions D001-D006)
| ID | Décision | Vérification exécutable | Source | Priorité | Statut |
|---|---|---|---|---|---|
| D001 | Re-mesure byte-level de chaque claim (la lecture d'un rapport = hypothèse, jamais une preuve) | greps PM ×4 ; md5 PM e64e85ce + sfc 24df0227 ; re-run 5 arbitres (rc + verdicts) | KO-L003 + §10.7 | S1 | pending |
| D002 | Périmètre = couche Task 14 vs baseline 2992bae (6 M + 2 nouveaux + tmp/) | git status --porcelain avant/après identique (hors plan/rapport/worklog CW) | directive | S2 | pending |
| D003 | Vérification en lecture seule — aucune correction fichier pendant les étapes 2-5 | git diff --stat stable après phase B | protocole vérificateur | S1 | pending |
| D004 | AVEUGLE seulement si divergence persistante à l'É5 (condition §1.3) | hook §1.3 consigné au rapport | SKILL.md §1.3 | S2 | pending |
| D005 | Verdict mécanique §10.5 (0 S1-S2 → PASS ; 0 S1 et ≥1 S2 ou ≥2 S3 → PASS AVEC RÉSERVES ; ≥1 S1 → FAIL) | tableau Résumé du rapport | §10.5 | S2 | pending |
| D006 | 0 commit / 0 push sans GO propriétaire | git rev-parse HEAD avant/après = 2992bae | règle d'or n°2 | S1 | pending |

## E8 — Validation du plan
answer-key-checker.py exécuté (verdict consigné) ; fallback honnête journalisé (règle d'or n°1) si l'arbitre est inopérant dans la layout courante.

## R2 — Baselines (couche Task 14 — rapport + reproduction 14-S0)
vcw 16/16 · integrity 60/60 · coherence PASS AVEC RÉSERVES 48/3/0 · verify-cross 84/84 (C006 close) · generer-pm 3/3 · hook rc0 INSTALLE kb 28. Non-régression exigée à l'issue de la vérification (lecture seule).
