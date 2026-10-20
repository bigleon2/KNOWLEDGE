---
name: refactoring-engineering
version: 1.1.1
category: ecosystem
language: fr
tags:
  - refactoring-engineering
  - refactoring
  - zero-regression
  - transformations-preservant-le-comportement
  - cascade
  - gouvernance
  - archivage-r4
description: >-
  Skill discipline refactoring engineering : déclarer, planifier et exécuter les OPÉRATIONS DE REFACTORING de l'écosystème (skills, corpus PM, scripts, agents, documents) par une série de petites transformations préservant le comportement observable — où « comportement observable » = verdicts d'arbitres inchangés, semver strict, invariants R2 (non-régression)/R4 (archivage byte-identité), idempotence ×2. Discipline n°55 (comme graph-engineering) : déclare le système de refactoring effectif de l'écosystème (correct-work modes CIBLE/DIRECT + procédures cascade PM + arbitres mécaniques + @historique R4) et l'organise : pré-checks verrouillés = golden master AVANT toute modification, éditions chirurgicales assert count==1, dry-run puis réel, recalibrage croisé KO-L004, archivage @historique, re-certification. Se sert de refactoring-test comme d'un OUTIL d'évaluation indépendante (pré-vol/post-vol — anti-auto-certification ; refactoring-test est l'outil de la présente discipline, non une discipline — correction directive propriétaire Task 8) ; vérification par correct-work et les arbitres. Appelé par gen-plan (conception de plan E4/E7 + situations de refactoring détectées en E9-E14) et mobilisable par tout élément. Sécurisation des opérations assurée par le skill refactor-guard (score de risque H01-H15, sandbox, échelle rollout — fusion discussion 468a4c26, lignée externe v1.7.0). Spécialise la discipline refactoring engineering n°55 (source de vérité : SHARED §7). Fondements documentés : references/fondements-academiques.md.
dependencies:
  - skill: gen-plan
    version: ">=3.15.0"
    used_at: "détenteur principal — conception des opérations à E4/E7 + situations E9-E14 (§8)"
  - skill: refactoring-test
    version: ">=1.0.1"
    used_at: "pré-vol (M2 évaluation + M3 graphe/blast radius AVANT l'opération) et post-vol (M4 re-scan) — OBLIGATOIRE, anti-auto-certification"
  - skill: correct-work
    version: ">=2.7.0"
    used_at: "vérification post-opératoire — correct-work(groupe) après chaque groupe d'opérations, correct-work(projet) en fin de chaîne"
  - skill: refactor-guard
    version: ">=1.7.0"
    used_at: "garde-fous des opérations D3/D4 — score de risque H01-H15, sandbox obligatoire, échelle rollout, maker-checker (fusion discussion 468a4c26)"
read_when:
  - Déclencher quand la demande concerne : déclarer, planifier ou exécuter une opération de refactoring — transformations préservant le comportement, zéro-régression, cascade versionnée, archivage.
  - Déclencher si la demande mentionne : refactoring, restructuration, opération de refactoring, migration progressive, zéro-régression, refactorer un skill/corpus/script, pré-checks verrouillés, archivage @historique.
  - Ne pas déclencher pour la DÉTECTION/ÉVALUATION seule (refactoring-test) ni pour la vérification post-hoc générique (correct-work).
---

## §0 — Contexte Système (SHARED v1.7.7)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.

## §0 — RÈGLE ZÉRO (résumé de SHARED §0)

1. **Auto-contenu** : ce skill porte tout ce dont il a besoin ; pas de référence hors écosystème hors `references/`.
2. **Versionné semver** : toute modification majeure de comportement → bump MINOR/MAJOR + KB synchronisé.
3. **KB source de vérité** : la description et la version du présent SKILL.md sont répliquées dans `{{KB_PATH}}`.
4. **Dépendances déclarées** : YAML `dependencies` uniquement ; pas d'import implicite.

## §1 — SPÉCIFICATION FONCTIONNELLE

### §1.1 Mission
Déclarer et gouverner les OPÉRATIONS DE REFACTORING de l'écosystème comme un processus d'ingénierie — pas un bricolage opportun : toute opération est DÉCLARÉE (cible, objectif, invariants, preuves attendues), ÉVALUÉE par refactoring-test (indépendance obligatoire), EXÉCUTÉE par petites transformations préservant le comportement observable, puis RE-CERTIFIÉE (arbitres + correct-work). Le « comportement observable » d'un élément documentaire (skill, corpus, PM) = ses verdicts d'arbitres, son semver, ses invariants R2/R4 et ses contrats de cross-references : un refactoring réussi change la STRUCTURE sans changer ces observables.

### §1.2 Modes
- **D1 DÉCLARER** — fiche d'opération : cible(s), situation (verdict refactoring-test joint), objectif, invariants intangibles, stratégie, preuves attendues (arbitres + verdicts), plan de retour arrière (archives @historique = point de restauration byte-identité).
- **D2 PRÉPARER (préparatoire)** — « rendre le changement facile, puis faire le changement facilement » : pré-checks verrouillés AVANT modification (= golden master de l'écosystème : verify-cross, integrity, interactions, answer-key verts — l'état d'avant est la référence de non-régression), scripts d'édition chirurgicale écrits et prouvés (assert count==1), dry-run systématique.
- **D3 EXÉCUTER** — transformations incrémentales avec re-vérification après chaque étape mécanisable ; max 2 rounds de correction par groupe (SHARED §4.4) ; idempotence ×2 prouvée à chaque maillon ; journalisation worklog par Task ID.
- **D4 MIGRER (progressif)** — stratégies à périmètre décroissant pour les gros chantiers : remplacement sanctionné par étapes (style strangler fig), double-écriture temporaire (ancien+ nouveau coexistants avec garde de byte-identité), commutation par périmètre (corpus → KB → arbitres → hôte) ; l'ancien n'est JAMAIS détruit sans archivage R4 préalable (RETRAITS_SANCTIONNES).

### §1.3 Gouvernance (niveaux de risque → exigences de preuve)
| Niveau | Situation | Exigences |
|--------|-----------|-----------|
| G0 | Refactoring cosmétique (renommage interne, commentaires, réorganisation sans sémantique) | Arbitres verts après ; worklog |
| G1 | Refactoring d'un skill/mode mineur | Verdict refactoring-test pré-vol ; arbitres verts ; semver PATCH ; baseline si evals touchés |
| G2 | Refactoring de corpus/PM ou d'arbitres | Verdict refactoring-test pré-vol (M3 blast radius) ; scripts verrouillés count==1 ; dry-run ; archivage R4 ; recalibrage croisé KO-L004 ; idempotence ×2 ; correct-work(groupe) |
| G3 | Refactoring systémique (source de vérité SHARED, conventions transverses) | Tout G2 + validation propriétaire explicite AVANT exécution (règle d'or n°4 pour la publication) + correct-work(projet) en fin de chaîne |

### §1.4 Invariants zéro-régression (constitution non amendable par opération)
1. **R2** : aucune modification n'altère un comportement validé sans preuve, isolation, version et observation ; jamais de rétrogradation de version.
2. **R4** : toute version remplacée est archivée @historique en byte-identité (git mv, SHA-256 scellé à l'index) — l'archive n'est jamais source d'installation (KO-L003).
3. **Arbitres verts aux 2 bornes** : l'état d'avant (golden master) ET l'état d'après passent les mêmes arbitres ; un arbitre rouge après opération = retour arrière ou correction, jamais un contournement.
4. **Idempotence ×2** : chaque mécanisme (scripts, propagation, rescellement) rejoué ne change rien la 2e fois.
5. **Évaluation indépendante** : refactoring-test pré-vol/post-vol obligatoire dès G1 — l'exécutant ne s'auto-évalue pas.
6. **Traçabilité** : worklog par Task ID + answer key pour les décisions E1 ; aucune fabrication de preuve (R3).

### §1.5 Mécanismes écosystème
Le système de refactoring EFFECTIF de l'écosystème — correct-work (4 modes, 5 étapes, verdicts S1-S3), procédures cascade PM (générateur verrouillé, recalibrage croisé, propagation §0, rescellement), arbitres mécaniques (verify-cross, integrity, interactions, answer-key, scan-doublons), @historique R4 — est DÉCLARÉ par la présente discipline et organisé par elle ; refactoring-engineering ne le REDÉFINIT pas (source de vérité : SHARED §7 n°55 ; R4 : une information une source).

### §1.6 Fondements (n°55, 2026-10-12)
Transformations préservant le comportement (Fowler — refactoring.com) ; préparatory refactoring (« make the change easy » — Fowler/Beck) ; characterization tests/golden master avant transformation (Feathers) ; migrations progressives (strangler fig, branch by abstraction — Humble/Fowler) ; fitness functions automatisées comme post-conditions (evolutionary architecture) ; inefficacité des revues seules sur les régressions (janéa systems 2026) → arbitres mécaniques + évaluateur indépendant. Détail et sources : `references/fondements-academiques.md`.

## §2 — SPÉCIFICATION TECHNIQUE
Artefacts par opération : fiche D1 (worklog ou plan), scripts d'édition verrouillés (assert count==1 — persistés sous scripts/), rapports d'arbitres avant/après, verdicts refactoring-test (JSON), manifeste d'archivage R4 (SHA-256), preuves d'idempotence ×2. Outillage existant mobilisé : generer-pm-skill.py (--check/--generate/--delta/--dry-run), propagate-context.py, task21-f2-rebuild-archive.py, gen-ultra-maitre.py, suite d'arbitres. Idempotence : relancer une opération déclarée sur un état déjà transformé = no-op prouvé.

## §3 — RELATIONS (extrait de SHARED §3.1)
- `gen-plan` — détenteur principal : conception des opérations à E4/E7 ; situations détectées en E9-E14 routent vers D1.
- `refactoring-test` — évaluateur indépendant OBLIGATOIRE (pré-vol M2/M3, post-vol M4) ; refactoring-engineering consomme ses verdicts, jamais l'inverse.
- `correct-work` — bras de vérification (correct-work(groupe)/projet) ; correct-work vérifie post-hoc, refactoring-engineering transforme — complémentaires, non fusionnés.
- `refactor-guard` — garde-fous des opérations : score de risque (H01-H15), sandbox obligatoire, échelle de déploiement, maker-checker ; mobilisé pendant D3/D4 pour les opérations à risque ; triangulation avec refactoring-test (évaluation) et correct-work (vérification).
- `spec-driven-development` — la fiche D1 est une micro-spécification (invariants = constitution, preuves = critères d'acceptation mécaniques).
- `harness-engineering` — les arbitres et gardes du harnais sont les post-conditions exécutées de toute opération.
- `graph-engineering` — le graphe KB (arêtes versionnées) est la matière première du blast radius (consommé via refactoring-test).
- `memory-engineering` — worklog append-only + answer key = État Long des opérations ; reprise post-warp depuis la lignée.
- `loop-engineering` — max 2 rounds de correction par groupe (SHARED §4.4) ; boucle externe à chaque dérive prouvée.

## §4 — CONVENTIONS
Kebab-case ; semver strict (PATCH = recalibrage, MINOR = nouvelle capacité, MAJOR = rupture de contrat) ; journalisation worklog obligatoire par Task ID ; scripts d'opération persistés sous scripts/ (jamais inline) ; aucune fabrication de preuve (R3) ; toute publication (push) reste conditionnée à la validation explicite du propriétaire (règle d'or n°4).

## §5 — ÉVALUATIONS ET DÉCLENCHEURS
`evals/trigger_evals.json` : 7 requêtes (5 positives, 2 contrôles négatifs — voisins correct-work et harness-engineering) ; déclenchement attendu sur les requêtes d'exécution/planification de refactoring explicites ; seuil de routage 0.5. Baseline A2 : MESURÉE 7/7 les 2 voies (Task 9/G-RES-2, 2026-10-12 — méthode SHARED §7 v2, voie M + confirm voie L 3 runs, seuil 0.5, ×3 confirmations, 0 dérive, 0 vote null ; rapport `scripts/baseline-a2-n55-report.json`).

## §6 — TRAÇABILITÉ
- v1.1.1 (Task 12, 2026-10-12, session web-b4d7dd19 — gen-plan(step), directive propriétaire « appliquer les corrections ») : résorption F1/F3/F4 (Task 11, consignés) — §5 baseline A2 actualisée (MESURÉE 7/7 les 2 voies — Task 9/G-RES-2) ; plancher frontmatter refactoring-test porté >=1.0.1 (alignement KB) ; l'entrée v1.1.0 est complétée rétrospectivement ci-après (elle n'avait pas de ligne §6 — constat F3).
- v1.1.0 (Task 9, 2026-10-12, session web-b4d7dd19 — gen-plan(step), QUOTA_OK levé) : Description Optimization (protocole SHARED §7) — voie M 6/7 (1 dérive cas négatif, collision lexicale gard+fous) → phrase « Garde-fous mobilisés pendant les opérations » remplacée par « Sécurisation des opérations assurée par le skill refactor-guard » (sémantique inchangée) ; re-mesure 7/7 — 0 dérive ×2 voies.
- v1.0.1 (2026-10-12, session web-b4d7dd19 Task 8 — gen-plan(step), fusion discussion externe 468a4c26) : calibration de déclaration — « refactoring-engineering se sert de refactoring-test comme un outil » (seule discipline n°55) ; dependencies += refactor-guard >=1.7.0 (garde-fous) ; §3/§8 triangulation évaluateur/garde-fous/vérificateur.
- v1.0.0 (n°55, 2026-10-12, session web-b4d7dd19 Task 7 — gen-plan(step) G3/G4) : matérialisation de la discipline refactoring engineering (directive propriétaire : le système de refactoring de l'écosystème déclaré et tagué comme discipline d'engineering, dédié aux opérations de refactoring, appelé par gen-plan à la conception et en situation) ; le système déclaré = correct-work v2.7.0 + procédures cascade PM + arbitres + @historique R4 (prouvé par les cascades v3.22.0/v3.22.1 — Tasks 3/6) ; sources : recherche web approfondie (rapport Task 7) ; baseline A2 en attente QUOTA.

## §7 — RÉFÉRENCES
- `references/fondements-academiques.md` — sources vérifiées (behavior-preserving, préparatoire, golden master, migrations progressives, fitness functions).
- SHARED §7 (PROMPT-MAITRE-SHARED.md, corpus) — source de vérité des disciplines.
- gen-plan v3.23.1 (SKILL.md) §1.6 bloc n°55 — orchestration E4/E7/E9-E14.
- correct-work v2.7.0 (SKILL.md) §1.2/§10 — modes de vérification déclarés.
- `scripts/refactoring-test-graph.py` — bras mécanique de l'évaluateur indépendant.

## §8 — Registre d'assignation des disciplines (décentralisé du SHARED §7)
| Discipline | Détenteur principal | Fonction héritée |
|------------|--------------------|------------------|
| refactoring engineering | gen-plan (E4/E7 conception + situations E9-E14) | correct-work (vérification post-opératoire), refactoring-test (OUTIL — évaluation indépendante obligatoire), refactor-guard (garde-fous des opérations), tout élément transformateur supervisé |
