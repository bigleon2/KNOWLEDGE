# PROMPT MAÎTRE ÉPHÉMÈRE — script-mon-ecosysteme-infrastructure v1.1.0

> **Skill source** : `skills/script-mon-ecosysteme-infrastructure/SKILL.md` (forme installée — référence canonique)
> **Version source** : 1.1.0 · **Généré le** : 2026-11-07
> **SHA-256 source** : `e01a0faebdcc7290012517f3630852c5980574d18591d6d1c0234e7b8f88faf1`
> **Nature** : projection éphémère auto-portante — le Contexte Système est embarqué,
> **aucune lecture externe n'est requise** (SHARED §6.2). Régénérable à volonté :
> `PM-skill(script-mon-ecosysteme-infrastructure)` reproduit ce fichier à l'identique (déterminisme même jour).

## MODE D'EMPLOI — IA EXTERNE

1. Copier l'intégralité du présent fichier.
2. Le coller comme **prompt système** (ou premier message) dans l'IA de votre choix.
3. Invoquer le skill par ses déclencheurs (section dédiée ci-dessous).
   Le contenu ci-dessous est la spécification exécutable du skill, auto-contenue.

## MISSION — description du skill (frontmatter source, verbatim)

Skill d'infrastructure de génération de fichiers de l'écosystème Knowledge. Injection automatique du Contexte Système à 3 niveaux, gardes d'intégrité et conventions de déploiement des artefacts (règles INFRA-1..INFRA-3).

---


## §0 — Contexte Système (SHARED v1.7.27)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.
> Langue : FRANÇAIS exclusif pour tous les échanges avec le propriétaire (règle d'or n°6 gen-plan — directive 2026-10-31, renforcée 2026-11-06) : dès le PREMIER mot de toute session ou reprise, la langue d'un message, d'un résumé de continuation ou d'un canal ne dérive JAMAIS la réponse ; toute dérive est corrigée immédiatement.
> Règles d'or & lecture SHARED à l'exécution (directive propriétaire 2026-11-06 — SHARED §9) : tout skill/agent/script exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or de l'écosystème (résumé §9 — canonique gen-plan §1.5).
> Référence canonique skill/agent (directive propriétaire 2026-11-07 — SHARED §0/§1.2) : toute référence à « mon skill X »/« mon agent X » désigne la forme installée à la racine `skills/X/SKILL.md`, JAMAIS le prompt maître du corpus `@mon-ecosysteme/` (ex-nommé `@PM-SKILLS/`) — les PMs sont des spécifications générées mécaniquement (KO-L004), les skills installés sont les formes exécutables.

## §1 — Spécification fonctionnelle

Skill d'infrastructure (pas un skill métier) : il génère et déploie les fichiers de l'écosystème (scripts d'arbitres, blocs de Contexte Système, artefacts d'installation) en appliquant l'injection automatique des 3 niveaux de Contexte Système.

### INFRA-1 (injection systématique)
Tout fichier généré par l'infrastructure embarque le Contexte Système à son niveau :
- **Niveau 1** — prompts maîtres (`skills/@mon-ecosysteme/PROMPT-MAITRE-*.md`) : bloc complet après l'en-tête ;
- **Niveau 2** — SKILL.md et fichiers `.agent` : bloc §0 compact après le frontmatter/titre ;
- **Niveau 3** — scripts Python (`scripts/*.py`) : docstring après le shebang.

### INFRA-2 (intégrité et idempotence)
La génération est idempotente (R1 : vérifier présence avant insertion ; R4 : ne jamais dupliquer) ; les remplacements passent par `scripts/sync-context-block.py`, les propagations par `scripts/propagate-context.py` ; toute divergence est détectée par `scripts/verify-cross.py --check-context`.

### INFRA-3 (enregistrement et traçabilité)
Tout artefact généré est enregistré dans `KNOWLEDGE.md` (template : `skills-inventory` §2.1), journalisé au worklog (format : `agent-creator` §6.1) et couvert par au moins un arbitre (gardes anti-boucle : SHARED §4.4).

## §2 — Spécification technique

- Stack : Python 3 (scripts), Markdown, YAML
- Emplacements : `scripts/` (arbitres et bootstrap), `skills/@mon-ecosysteme/` (prompts maîtres), `config.json` (configuration centralisée)
- Validation : `verify-cross.py --check-context` (score 100 %), `verify-correct-work.py` (16 checks)

## §3 — Relations

| Avec | Nature | Détails |
|------|--------|---------|
| install-ecosystem | utilise cette infrastructure | Phases P6-P7 du bootstrap (SHARED §3.1) |
| skill-creator | conventions | Conventions structurelles, >= v1.0.0 |
| correct-work | vérifié par | Conformité des artefacts générés, >= v2.4.0 |
| knowledge.md | enregistrement | Toute matérialisation est inscrite au registre |

## §4 — Conventions

Nommage kebab-case, versions semver, tags `#token`, variables `{{VARIABLE}}` (SHARED §1.2 — pointeur décentralisé : `skill-creator` §2).

---

## Baseline A2 — statut de mesure
> **Baseline A2 (Task 21 P3/F3, 2026-10-03)** : MESURÉE 2 voies (voie mécanique SHARED §7 v2 + voie L 3 runs réels) — score baseline 6/7 (nulls : 2) ; détail par cas : `scripts/baseline-a2-all-report.json` ; cas structurels consignés au registre KB (décision Task 21) ; re-mesure idempotente `--skip-done` armée pour les nulls 429 restants.

---

## RELATIONS — dépendances déclarées (frontmatter source, verbatim)

- **skill-creator** >=1.0.0 — conventions structurelles

> Ces dépendances sont des relations ÉCOSYSTÈME (traçabilité). En usage IA externe,
> la spécification embarquée ci-dessus suffit à l'exécution de la mission.
