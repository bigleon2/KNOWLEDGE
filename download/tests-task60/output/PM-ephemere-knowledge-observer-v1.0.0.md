# PROMPT MAÎTRE ÉPHÉMÈRE — knowledge-observer v1.0.0

> **Skill source** : `skills/knowledge-observer/SKILL.md` (forme installée — référence canonique)
> **Version source** : 1.0.0 · **Généré le** : 2026-11-07
> **SHA-256 source** : `7b5e3a450bf028eba30186cb20101d13ea03a95799a15e78571909bcb557ee11`
> **Nature** : projection éphémère auto-portante — le Contexte Système est embarqué,
> **aucune lecture externe n'est requise** (SHARED §6.2). Régénérable à volonté :
> `PM-skill(knowledge-observer)` reproduit ce fichier à l'identique (déterminisme même jour).

## MODE D'EMPLOI — IA EXTERNE

1. Copier l'intégralité du présent fichier.
2. Le coller comme **prompt système** (ou premier message) dans l'IA de votre choix.
3. Invoquer le skill par ses déclencheurs (section dédiée ci-dessous).
   Le contenu ci-dessous est la spécification exécutable du skill, auto-contenue.

## MISSION — description du skill (frontmatter source, verbatim)

Skill d'observation automatique des sessions pour détecter les patterns d'erreur et améliorer les skills de l'écosystème. Cycle A-H (Task Observer), 4 modes M1-M4 (observation, analyse, proposition, application), journal lessons-learned, propositions idempotentes validées par correct-work.

---


## §0 — Contexte Système (SHARED v1.7.27)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.
> Langue : FRANÇAIS exclusif pour tous les échanges avec le propriétaire (règle d'or n°6 gen-plan — directive 2026-10-31, renforcée 2026-11-06) : dès le PREMIER mot de toute session ou reprise, la langue d'un message, d'un résumé de continuation ou d'un canal ne dérive JAMAIS la réponse ; toute dérive est corrigée immédiatement.
> Règles d'or & lecture SHARED à l'exécution (directive propriétaire 2026-11-06 — SHARED §9) : tout skill/agent/script exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or de l'écosystème (résumé §9 — canonique gen-plan §1.5).
> Référence canonique skill/agent (directive propriétaire 2026-11-07 — SHARED §0/§1.2) : toute référence à « mon skill X »/« mon agent X » désigne la forme installée à la racine `skills/X/SKILL.md`, JAMAIS le prompt maître du corpus `@mon-ecosysteme/` (ex-nommé `@PM-SKILLS/`) — les PMs sont des spécifications générées mécaniquement (KO-L004), les skills installés sont les formes exécutables.

## §1 — SPÉCIFICATION FONCTIONNELLE

### §1.1 Mission

knowledge-observer matérialise le pattern **Task Observer** (propositions-qwen.md §1.5,
intégré phase N20) : industrialiser le cycle d'apprentissage continu de l'écosystème en
détection mécanique des récurrences. Le worklog + les boucles R3 + KB Décisions remplissent
déjà le cycle de manière agent-driven ; ce skill le rend **observé, journalisé et validé**.
Source de vérité du pattern : `{{SKILLS_ROOT}}gen-plan/references/observation-patterns.md`.

### §1.2 Le cycle A-H

| Étape | Action | Sortie |
|-------|--------|--------|
| A | Observation passive (M1) | journal de session |
| B | Détection erreurs/patterns récurrents | liste de patterns |
| C | Enregistrement | `data/lessons-learned.json` |
| D | Analyse post-session (M2, E15 gen-plan) | rapport d'analyse |
| E | Proposition de mises à jour (M3) | propositions idempotentes |
| F | Validation correct-work | verdict |
| G | Application si validé (M4) | correctifs appliqués |
| H | Mise à jour KB | entrée + Décisions |

### §1.3 Les 4 modes

| Mode | Nom | Étapes | Description |
|------|-----|--------|-------------|
| M1 | **OBSERVATION** | A-B | Journalise et détecte les récurrences, ne modifie rien |
| M2 | **ANALYSE** | C-D | Enregistre les lessons, rapport d'analyse post-session (E15) |
| M3 | **PROPOSITION** | E-F | Propose des mises à jour idempotentes, fait valider par correct-work |
| M4 | **APPLICATION** | G-H | Applique les correctifs validés, met à jour le KB |

### §1.4 Garde-fous

1. **Observation passive par défaut** : M1 n'écrit que dans `data/lessons-learned.json`.
2. **Aucune auto-modification non validée** : les modes M3-M4 exigent un verdict correct-work (étape F) avant application.
3. **Garde anti-boucle** : max 2 rounds de correction par artefact (SHARED §4.4) — identique pour les lessons.
4. **Idempotence** : toute proposition appliquée porte un marqueur et est rejouable sans effet (R1-R6).

### §1.5 Déclencheurs

- Automatique : invoqué par gen-plan à **E15** (bilan et auto-calibration) en modes M1-M2.
- Manuel : « observe la session », « lessons learned », « analyse les patterns d'erreur ».

## §2 — SPÉCIFICATION TECHNIQUE

- **Langage** : Markdown (rapports), JSON (données), YAML (frontmatter)
- **Environnement** : `{{SKILLS_ROOT}}knowledge-observer/`
- **Données** : `data/lessons-learned.json` (journal des lessons — schéma §4 de la référence)
- **Seuil de récurrence** : un pattern est « récurrent » à 3 occurrences documentées (2 si S1).
- **Arbitres mobilisés** : verify-cross.py (cohérence KB), answer-key-checker.py (décisions), certification-complete.py (5/5 après application M4).

## §3 — RELATIONS

| Avec | Nature | Détails |
|------|--------|---------|
| gen-plan | invoqué par | E15 (analyse post-session, modes M1-M2), version >= v3.13.0 |
| correct-work | valide | Étape F du cycle A-H (validation des lessons, modes M3-M4), version >= v2.6.0 |
| skill-creator | applique via | Application des mises à jour de skills (conventions), version >= v1.0.0 |
| KNOWLEDGE.md | enrichit | Étape H (entrée + Décisions) |

## §4 — CONVENTIONS

- Nommage kebab-case (SHARED §1.2) ; worklog SHARED §1.4 ; idempotence R1-R6 (gen-plan §1.8).
- Non-duplication (SHARED §6.3) : la définition du pattern Task Observer reste dans
  `gen-plan/references/observation-patterns.md` ; le présent skill enregistre uniquement
  son cycle, ses modes et son journal.
- Toute lesson appliquée est tracée au worklog et au KB (étape H) — jamais d'édition silencieuse.

---

## RELATIONS — dépendances déclarées (frontmatter source, verbatim)

- **gen-plan** >=3.13.0 — E15 (analyse post-session)
- **correct-work** >=2.6.0 — Validation des lessons learned (étape F)
- **skill-creator** >=1.0.0 — Application des mises à jour

> Ces dépendances sont des relations ÉCOSYSTÈME (traçabilité). En usage IA externe,
> la spécification embarquée ci-dessus suffit à l'exécution de la mission.
