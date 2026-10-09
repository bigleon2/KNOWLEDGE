---
name: script-reviewer
version: 1.0.0
category: ecosystem
language: fr
description: >
  Relire et valider les scripts de l'écosystème (arbitres, collecteurs, outils stdlib)
  avant adoption : grille de relecture en 8 checks mécaniques (G1-G8), sévérités S1-S4
  alignées correct-work, verdict PASS / PASS AVEC RÉSERVES / FAIL, preuve d'idempotence
  ×2. Utiliser lorsqu'un script vient d'être créé ou modifié (par script-creator ou
  manuellement) et doit être certifié avant livraison, lorsqu'un script existant doit
  être audité (idempotence, traçabilité, stdlib-only), ou lorsqu'une relecture de
  convergence doit être exécutée avant correct-work. Structure, éléments et conventions
  hérités de skill-creator ; pendant « relecture » de script-creator ; homologue de la
  famille agent-creator. Non concerné : création de skills (skill-creator),
  planification (gen-plan), création de scripts (script-creator).
dependencies:
  - skill: script-creator
    version: ">=1.0.0"
    used_at: "Scripts entrants du processus de création (§1.1, §3)"
  - skill: correct-work
    version: ">=2.6.0"
    used_at: "Sévérités S1-S4, escalade mode CIBLE (§1.3)"
  - skill: skill-creator
    version: ">=1.0.0"
    used_at: "Conventions de description, d'évals et de frontmatter (§1.4)"
tags: [script, creator, être]
read_when:
  - Déclencher quand la demande concerne : relire et valider les scripts de l'écosystème (arbitres, collecteurs, outils stdlib) avant adoption : grille d…
  - Déclencher si la demande mentionne : creator, script, être
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

# Relecteur de scripts

Un skill pour relire, auditer et certifier les scripts de l'écosystème de manière
mécanique, idempotente et traçable — le pendant « relecture » de script-creator.

## §0 — Contexte Système (SHARED v1.6.7)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.

## §1 — SPÉCIFICATION FONCTIONNELLE

### §1.1 Mission

script-reviewer industrialise la **relecture des scripts** de l'écosystème : aucun
script n'est déclaré fiable tant qu'il n'a pas passé la grille de relecture G1-G8
(§1.2). Il travaille en binôme avec script-creator (qui produit) et correct-work
(qui valide les livrables d'écosystème au sens large) : script-reviewer est
l'arbitrage LOCAL d'abord (P1, gen-plan §1.14) — rapide, exécutable, sans API —
avant toute escalade. Sa connaissance des leçons de session (knowledge-observer
L003 — faux verdicts d'arbitres sur cas limites) fait partie intégrante de sa
mission : un relecteur qui se trompe est plus dangereux qu'un script fautif.

### §1.2 La grille de relecture en 8 checks

| Check | Action | Preuve mécanique |
|-------|--------|------------------|
| G1 | Syntaxe Python valide | `py_compile` sans erreur |
| G2 | Stdlib uniquement (N3) | scan des imports — 0 dépendance externe non justifiée |
| G3 | Docstring d'intention + sortie JSON déterministe | en-tête présent, `ensure_ascii=False` |
| G4 | Code de retour explicite | `sys.exit(code)` présent (0 = succès) |
| G5 | Idempotence ×2 | deux exécutions consécutives → sorties identiques |
| G6 | Persistance R9 + nommage | fichier sous `scripts/`, nom kebab-case |
| G7 | Traçabilité | entrée worklog correspondante (règle d'or n°1) |
| G8 | Auto-test des cas limites (P2) | cas limites embarqués pour les arbitres génériques |

Un check non applicable (ex. G8 pour un outil one-shot) est marqué `n/a — justifié`,
jamais silencieusement omis.

Les checks s'appliquent aux normes du langage cible du script relu : pour Python, la
conformité fine PEP 8 (style, nommage snake_case, indentation) et PEP 257 (docstrings,
commentaires) est déléguée au post-traitement `correct-py` (exécuté après chaque
utilisation de script-creator) — la grille G1-G8 en retient les critères mécaniques
(G1 syntaxe, G3 docstring + sortie déterministe) et converge avec le rapport de
correct-py avant toute adoption.

### §1.3 Sévérités et escalade

- **S1** (bloquant) : syntaxe invalide, dépendance externe non justifiée, non-idempotence
  d'un arbitre de vérification → correction avant toute adoption.
- **S2** (majeur) : sortie non déterministe, code de retour implicite, traçabilité absente.
- **S3** (mineur) : nommage impropre, docstring incomplète, cas limite non couvert.
- **S4** (informatif) : suggestion d'amélioration, factorisation possible.
- Verdicts : PASS (0 S1/S2) / PASS AVEC RÉSERVES (S3/S4 listées) / FAIL (≥ 1 S1/S2).
- Escalade : un FAIL ou une réserve non résoluble localement est escaladé à
  correct-work (mode CIBLE) — jamais étouffé ; le relecteur ne réécrit jamais le
  script lui-même (frontière avec script-creator, étape 5).

### §1.4 Déclencheurs et conventions héritées

- Manuel : « relis ce script », « audite cet arbitre avant adoption », « vérifie
  l'idempotence de cet outil », « relecture de convergence avant livraison ».
- De skill-creator, script-reviewer hérite : frontmatter avec dépendances versionnées,
  schéma d'evals (`evals/evals.json` + `evals/trigger_evals.json`), discipline de
  description (déclencheurs explicites, cas négatifs), itération par évaluation.
- De agent-creator, il reprend la structure documentaire en sections §0-§4 et la
  référence `references/` (grille détaillée + modèle de rapport de relecture).

## §2 — SPÉCIFICATION TECHNIQUE

- **Mode d'emploi** : la relecture s'exécute via un arbitre de session persisté sous
  `scripts/` (R9) qui implémente G1-G8 et émet un JSON déterministe (`verdict`,
  `checks`, `severites`) ; le relecteur humain/agent consigne le verdict au worklog.
- **Lecture seule** : un arbitre de relecture ne modifie AUCUN artefact audité —
  l'idempotence ×2 est une preuve systématique (deux passes, même verdict).
- **Localisation** : `{{SKILLS_ROOT}}script-reviewer/` pour le skill ; rapports de
  relecture sous `tmp/` (artefacts de session) ou consignés au worklog.
- **Convergence** : avant une certification globale, la relecture de convergence
  relit les scripts modifiés depuis la dernière certification (delta = worklog).

## §3 — RELATIONS

| Avec | Nature | Détails |
|------|--------|---------|
| script-creator | binôme | produit (creator) ↔ valide localement (reviewer) — frontière étape 5 / §1.2 |
| correct-work | escalade | sévérités S1-S4 partagées ; mode CIBLE au-delà de l'arbitrage local (>= 2.6.0) |
| skill-creator | hérite de | Conventions de description, d'évals et de frontmatter (>= 1.0.0) |
| knowledge-observer | applique | Lesson L003 (faux verdicts d'arbitres → auto-test cas limites) |
| correct-py | convergence | Conformité fine du langage (PEP 8/PEP 257) déléguée au post-traitement de script-creator (>= 1.0.0) |
| gen-plan | servi par | P1 arbitrage local d'abord (§1.14), hooks de validation par phase |

## §4 — CONVENTIONS

- Nommage kebab-case (SHARED §1.2) ; worklog SHARED §1.4 ; idempotence R1-R6 (gen-plan §1.11).
- Toute relecture est tracée au worklog (règle d'or n°1) — jamais de verdict silencieux.
- Non-duplication (SHARED §6.3) : script-reviewer ne redéfinit ni la création de scripts
  (script-creator), ni la validation d'écosystème au sens large (correct-work), ni la
  création de skills (skill-creator) — il couvre uniquement la relecture des scripts.
- Un relecteur est lui-même un script : il passe sa propre grille (G1-G8) avant adoption
  (autoréférence, esprit L003).

## HISTORIQUE DES VERSIONS

- v1.0.0 (2026-09-27, session B13-r5) : matérialisation initiale — homologue de
  script-creator (pendant relecture), structure et éléments similaires à skill-creator
  et agent-creator (en-tête, description, frontmatter, evals, references) ; grille
  G1-G8 ; sévérités alignées correct-work v2.6.0.
