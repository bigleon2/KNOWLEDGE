# Clone de discussion — session web-f492e049 (Task 114 : routage décisionnel + rappel langue), 28ᵉ de la lignée

> Session : web-f492e049 · chat 17b8e0d9-d141-4dda-b86b-8b152e773f70 · canal zai-web · traces directives 1a2025197d2a0e9d + 1a2025ce4a6ed095. Généré le 2026-11-22T08:49:31Z par clone-chat v2.0.2 (7+1 étapes). Fenêtre du clone : automatisation des appels skills/agents via gen-plan (déclencheurs intégrés en corps + forcés + script décisionnel pour les agents complexes) et correction de la dérive de langue (chinois → rappel permanent français dans gen-plan). Chaîne G1-G14 du plan-2026-11-21 préalablement close (worklog suites 155-160), Task 114 exécutée en E13d (D015).

## §0 — Contexte Système (SHARED v1.7.45)

> Écosystème Knowledge : skills/ = racine (73 SKILL.md + 4 .agent) | KB = skills/KNOWLEDGE.md | @mon-ecosysteme/ (corpus) | @historique/ (archive R4). Conventions kebab-case/semver/#token. Règle d'or n°6 : FRANÇAIS exclusif dès le premier mot — rappel permanent §0 gen-plan v3.47.0 (dérive chinois corrigée). Référence canonique : « mon skill X » = forme installée skills/X/SKILL.md. État certification : ALL PASS 6/6 (verify-cross 168/168 · correct-work 16/16 · integrity 116/116 · interactions PASS STRICT 59/59 · tool-routing 7/7) · audit 73/73 skills + 4/4 agents CONFORMES · gen-plan v3.47.0 · correct-work v2.12.1 · clone-chat v2.0.2 · SHARED v1.7.45 · pin ECO_SKILLS ×2 arbres.

## §1 — Worklog chronologique (fenêtre du clone : suite 162)

| Suite | Date | Contenu (résumé exécutable) |
|---|---|---|
| 162 | 2026-11-22 | T1 état : récidive réinjection plateforme (17 SKILL.md écrasés + 4 majuscules recréés) → bootstrap INSTALLE-RÉPARÉ + réparation Task 114 (13+4, garde archive R4 byte-identité, idempotence ×2) + audit 73/73 + 4/4 · T2 dérive langue chinois → correction immédiate + worklog + durcissement · T3 routage-skills-agents.py v1.0.0 (selftest 9/9 ×2, 44 ms, porte agents) · T4 gen-plan v3.46.0→v3.47.0 (§0 RAPPEL PERMANENT LANGUE + É5-ROUTAGE + §1.17, 10 patchs verrouillés) + ensure-installed.py garde réinjection (testé INSTALLE-RÉPARÉ → INSTALLE ×2) · T5 cascade KO-L004 complète (PM v3.47.0 + dédup R4 + KB + pin ×2 + evals + 9 citations vives + propagation §0 v1.7.45 ×2 + rescellement ×2) → certification ALL PASS 6/6 · T6 livrables : analyse (139,1 Kio rejeté → OPTIMISE) + tests F+P 32/32 + CW --bloc PASS 5/5 + plan E13d/D015 (P1-P5 PASS) + PUSH (clé du tour) |

## §2 — Artefacts de la fenêtre (Étape 2)

| Artefact | Rôle | État |
|---|---|---|
| skills/gen-plan/scripts/routage-skills-agents.py | Script décisionnel É5-ROUTAGE (scores frontmatters installés — source unique R4, porte agents COMPLEXE >= 2/5) | CERTIFIÉ ×2 arbres |
| skills/gen-plan/scripts/ensure-installed.py | Garde réinjection plateforme (signature native, réparation miroir, stale majuscules sous garde R4) | CERTIFIÉ ×2 arbres |
| skills/gen-plan/SKILL.md | gen-plan v3.47.0 (§0 rappel langue + §1.16 É5-ROUTAGE + §1.17 + §2.2 + §3 + §4 + journal) | INSTALLED ×2 arbres |
| skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.47.0.md | PM généré mécaniquement (delta verrouillé scripts/delta-genplan-v3470.json) | SCELLÉ |
| download/analyse-routage-decisionnel-task114.md | Analyse mesurée (options A/B/C, verdict OPTIMISE, extension autres éléments) | SCELLÉ |
| download/rapport-task114-tests-fp.json | Tests F+P 32/32 PASS | SCELLÉ |
| download/rapport-cw-task114-projet.md | CW --bloc Task 114 PASS 5/5 | SCELLÉ |
| download/rapport-task114-reparation-reinjection.json | Réparation réinjection 13+4 | SCELLÉ |
| download/rapport-audit-conformite-task113.json | Audit 73/73 skills + 4/4 agents CONFORMES | SCELLÉ |
| download/plan-2026-11-21-optimisation-ecosysteme.md | Plan étendu E13d/D015 (P1-P5 PASS) | SCELLÉ |
| scripts/t114-genplan-v3470.py · scripts/task114-tests-fp.py · scripts/task114-reparation-reinjection.py | Cascade + tests + réparation | CERTIFIÉS |

## §3 — Décisions et leçons de la fenêtre (Étape 3)

| ID | Décision / leçon | Portée |
|---|---|---|
| Option C — routage mécanique | Incruster le catalogue complet des déclencheurs DÉGRADE (139,1 Kio = 2,3× seuil CRITIQUE 60 Kio + violation R4 + cascade KO-L004 ×73 skills) ; routage à l'exécution OPTIMISE (+3,99 Kio une fois, 44 ms/plan, ~300 #token, source unique) | Task 114 |
| Rappel permanent langue | Dérive chinois constatée → correction immédiate + worklog + durcissement : §0 gen-plan rappelle le FRANÇAIS exclusif à CHAQUE exécution (directive 1a2025ce4a6ed095) | Task 114 |
| Garde réinjection durable | La plateforme réinjecte ses skills natifs entre-tours (9ᵉ récidive environnement) → ensure-installed.py étendu : détection signature native (clawdbot/absence §0), réparation miroir, suppression majuscules SOUS garde archive R4 byte-identité (jamais détruire sans preuve) | Task 114 |
| KO-L003 (×2) | F6 : champ volatile duree_ms = métadonnée de mesure, idempotence testée sémantiquement · F2 : propagation §0 = étape de cascade (dépôt PUIS hôte puis rescellement) — arbitres corrigés, réalité inchangée | Task 114 |
| Extension décisionnelle | Système pertinent UNIQUEMENT pour les orchestrateurs : gen-plan modifié, orchestrateur-tsi inchangé (routage de domaine propre — preuve score 13 au test), 4 agents = cibles du routage | Task 114 |

## §4 — État des pendances (Étape 4)

| Pendance | État |
|---|---|
| PUSH des commits du tour (clé du tour — KO-L009 mémoire de commande, sortie masquée) | Exécutée en fin de fenêtre |
| RÉVOCATION PATs antérieurs (Task 107 + Task 112 + tour précédent) | CONSERVÉE — action propriétaire UNIQUE [CRITIQUE] |
| Révocation du PAT fourni après usage | CONSERVÉE — rappel propriétaire [CRITIQUE] |
| Décision cron 531684 (0 job — vérification récurrente) | CONSERVÉE — escalade propriétaire |

## §5 — Lignage et scellage (Étape 5)

Lignée : … → Task 112 (24ᵉ) → Task 113 audit conformité (26ᵉ) → Task 113 SUITE plateforme (27ᵉ) → **Task 114 routage décisionnel (28ᵉ)**. Session web-f492e049, fenêtre suite 162.

Drifts typés de la fenêtre : MODIFICATION gen-plan v3.46.0→v3.47.0 ×2 arbres · CREATION routage-skills-agents.py v1.0.0 ×2 arbres · MODIFICATION ensure-installed.py (garde réinjection) ×2 arbres · CREATION PM v3.47.0 + delta verrouillé · RENOMMAGE R4 PM v3.46.0 → @historique · MODIFICATION KB + pin ×2 + evals + 9 citations vives + propagation §0 ×2 arbres · RESCELLEMENT archive v2.5 ×2 arbres · CREATION livrables download/ ×5 + scripts Task 114 ×3 + clone 28ᵉ.
