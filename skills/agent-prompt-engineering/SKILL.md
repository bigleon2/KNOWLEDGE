---
name: agent-prompt-engineering
version: 1.2.0
category: infrastructure
language: fr
tags:
  - prompt-engineering
  - optimisation
  - evaluation
  - iteration
  - ecosystem
  - gateway
  - complexite
description: >
  Skill d'optimisation fine des prompts complexes : rédaction, restructuration
  (restructure, restructurer), évaluation, itération et validation des
  déclencheurs (trigger_evals) des artefacts de prompts (PMs, SKILL.md, évals).
  Spécialise la méthode prompt-engineering (méthode-mère : gen-plan ; source de vérité : SHARED §7)
  ; matérialisé le 2026-09-06 (recommandation de session, §5.2).
  AUTO-DÉCLENCHEMENT PROMPT-GATEWAY INCONDITIONNEL (directive propriétaire 2026-11-21 Task 112 G1 + précision trace 1a1fc7b1728869e9) :
  s'exécute automatiquement, de façon autonome et à CHAQUE prompt envoyé à
  l'IA — analyse le prompt et évalue sa complexité de façon systématique
  (phases A-B) ; si le prompt s'avère ni court ni simple (≥ 2 critères
  COMPLEXE sur la grille 5 critères) : le retranscrit de façon cohérente,
  optimisée et fonctionnelle et envoie à l'IA une version compréhensible,
  explicite et structurée (objectif, contexte, contraintes, étapes,
  livrables) qui devient l'entrée d'exécution ; si court et simple :
  passage direct sans transformation, verdict journalisé (la profondeur du
  traitement est routée par la complexité, le déclenchement est
  inconditionnel).
dependencies:
  - skill: gen-plan
    version: ">=3.7.0"
    used_at: "Consultation du contexte écosystème (planification E1-E8, méthode-mère §1.9)"
---

## §0 — Contexte Système (SHARED v1.7.44)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.
> Langue : FRANÇAIS exclusif pour tous les échanges avec le propriétaire (règle d'or n°6 gen-plan — directive 2026-10-31, renforcée 2026-11-06) : dès le PREMIER mot de toute session ou reprise, la langue d'un message, d'un résumé de continuation ou d'un canal ne dérive JAMAIS la réponse ; toute dérive est corrigée immédiatement.
> Règles d'or & lecture SHARED à l'exécution (directive propriétaire 2026-11-06 — SHARED §9) : tout skill/agent/script exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or de l'écosystème (résumé §9 — canonique gen-plan §1.5).
> Référence canonique skill/agent (directive propriétaire 2026-11-07 — SHARED §0/§1.2) : toute référence à « mon skill X »/« mon agent X » désigne la forme installée à la racine `skills/X/SKILL.md`, JAMAIS le prompt maître du corpus `@mon-ecosysteme/` (ex-nommé `@PM-SKILLS/`) — les PMs sont des spécifications générées mécaniquement (KO-L004), les skills installés sont les formes exécutables.



## §0 — RÈGLE ZÉRO (résumé de SHARED §0)

Les fichiers des sessions précédentes n'existent pas dans une nouvelle session : tout est
à reconstruire à partir des documents de la lignée. Ne jamais utiliser le verbe « conserver ».
Voir `PROMPT-MAITRE-SHARED.md §0` pour la règle complète.

## §A — DÉCLENCHEURS (v1.2.0 — Task 112 G1 + E13 précision propriétaire trace 1a1fc7b1728869e9)

> **Glossaire alias-eco inline** : **`$FACON` = « de façon cohérente, optimisée et fonctionnelle »** (adverbe modal : la manière d'exécuter) · **`$FACON2` = « (cohérent, optimisé et fonctionnel) »** (qualificatif : la propriété attendue du livrable). Source canonique : registre alias-eco `@historique/@Alias/aliases.json` ; en cas d'écart, le présent glossaire fait foi pour la lecture du skill.

- **AUTO-DÉCLENCHEMENT — PROMPT-GATEWAY INCONDITIONNEL (voie royale — directive 2026-11-21 + précision propriétaire trace 1a1fc7b1728869e9 : « à CHAQUE fois que j'envoie un prompt à mon IA »)** : le skill s'exécute automatiquement et de façon autonome sur **CHAQUE prompt envoyé à l'IA** — phases A (analyse) et B (évaluation de complexité) **systématiques** sur tout prompt ; si verdict COMPLEXE (≥ 2 critères sur la grille §1.6) : phases C-D — retranscription $FACON puis envoi à l'IA de la version compréhensible, explicite et structurée qui devient l'entrée d'exécution ; si verdict COURT/SIMPLE : passage direct sans transformation (verdict journalisé worklog). Le déclenchement est INCONDITIONNEL — seule la PROFONDEUR du traitement dépend de la complexité (workflow 4 phases §1.6 ; intégral : `references/prompt-gateway.md`).
- `optimise ce prompt maître` / `optimise ce prompt, il contient des duplications` — optimisation fine d'un artefact de prompt
- `restructure ce prompt / cette section §N` (restructure, restructurer) — réorganisation sans perte sémantique
- `évalue ce SKILL.md / ce prompt selon la grille` — notation 5 axes sans modification
- `valide les déclencheurs (trigger_evals) de ce skill` — Description Optimization M4
- Délégation gen-plan §1.9 (SHARED §3.1) — artefacts de prompts exigeant un travail spécialisé

## §1 — SPÉCIFICATION FONCTIONNELLE

### §1.1 Mission

agent-prompt-engineering est le skill d'**optimisation fine des prompts complexes** de l'écosystème. Il reçoit en délégation (gen-plan §1.9, SHARED §3.1) les artefacts de prompts exigeant un travail spécialisé : rédaction, restructuration, évaluation et itération. Il ne redéfinit JAMAIS la méthode prompt-engineering (source de vérité : SHARED §7 ; registre d'assignation : SHARED §7 ; orchestration gen-plan : PM gen-plan §1.9) — il la spécialise sur les artefacts de haut niveau (Prompts Maîtres, SKILL.md, evals, rapports de vérification).

### §1.2 Les 4 opérations

| Opération | Description | Artefacts typiques |
|-----------|-------------|--------------------|
| **Rédaction** | Production d'un prompt nouveau à partir d'une intention (objectif, contraintes, formats de sortie) | PM, SKILL.md, evals |
| **Restructuration** | Réorganisation d'un prompt existant (sections, hiérarchie, tableaux, suppression de duplication) | PM, SKILL.md |
| **Évaluation** | Notation d'un prompt selon la grille (§1.4) : clarté, précision, structure, économie, robustesse | Tout artefact de prompt |
| **Itération** | Boucle évaluer → ajuster → re-évaluer jusqu'au seuil de qualité (loop engineering) | Tout artefact de prompt |

### §1.3 Modes

| Mode | Nom | Description |
|------|-----|-------------|
| M1 | **CIBLE** | Optimisation d'un artefact unique (un SKILL.md, une section de PM) |
| M2 | **PROJET** | Optimisation d'un ensemble cohérent (les §5 de plusieurs PMs, un corpus) |
| M3 | **ÉVALUATION** | Notation seule, sans modification (rapport + recommandations) |
| M4 | **DÉCLENCHEURS** | Validation Description Optimization : trigger_evals (true/false) sur le frontmatter d'un skill |
| M5 | **PROMPT-GATEWAY** | Auto-déclenchement INCONDITIONNEL à chaque prompt envoyé à l'IA : phases A-B systématiques (analyse + évaluation de complexité) ; si COMPLEXE : retranscription $FACON + envoi à l'IA de la version compréhensible, explicite et structurée ; si COURT/SIMPLE : passage direct journalisé (v1.2.0, §1.6) |

### §1.4 Grille d'évaluation (5 axes)

| Axe | Question | Seuil PASS |
|-----|----------|------------|
| Clarté | Chaque instruction a-t-elle une seule lecture possible ? | 0 ambiguïté S1/S2 |
| Précision | Les critères sont-ils mesurables (seuils, formats, versions) ? | Critères vérifiables |
| Structure | Les sections suivent-elles les conventions (SHARED §5) ? | Conformes |
| Économie | Le prompt évite-t-il duplication et verbiage (SHARED §6.3) ? | 0 duplication détectée |
| Robustesse | Le prompt survit-il aux cas limites (blocage, wipe, ressource) ? | Règle d'or n°1 couverte |

Détail d'usage : `references/grille-evaluation-prompt.md`.

### §1.5 Boucle d'itération

1. Évaluation initiale (grille §1.4) — rapport M3.
2. Ajustements proposés (un par axe sous seuil), classés par impact.
3. Re-évaluation après application. L'itération s'arrête quand tous les axes PASS, ou après 3 itérations (dérive documentée au worklog, décision utilisateur).

### §1.6 Mode PROMPT-GATEWAY — auto-déclenchement inconditionnel à chaque prompt (v1.2.0)

**Objet (directive propriétaire 2026-11-21, Task 112 G1 + précision trace 1a1fc7b1728869e9)** : l'écosystème exécute ce skill AUTOMATIQUEMENT, de façon autonome et **à CHAQUE prompt envoyé à l'IA** — sans exception. Le skill est la porte d'entrée systématique des prompts : il analyse et évalue la complexité de tout prompt, puis route la profondeur du traitement.

**Règle de routage (E13 — le déclenchement est inconditionnel, la profondeur est conditionnelle)** : phases A-B sur TOUT prompt ; phases C-D (retranscription + envoi structuré) uniquement si verdict COMPLEXE (≥ 2 critères sur la grille) ; verdict COURT/SIMPLE → passage direct sans transformation, verdict journalisé worklog.

**Workflow — 4 phases strictement ordonnées** (intégral, exemples et gabarit de sortie : `references/prompt-gateway.md`) :

| Phase | Action | Sortie |
|-------|--------|-------|
| **A — Analyse** | **SYSTÉMATIQUE (tout prompt)** — décomposition : longueur, structure, verbes d'action, étapes explicites/implicites, dépendances entre étapes, livrables attendus, ambiguïtés, implicites, contexte cité | Fiche d'analyse (points saillants + risques d'exécution) |
| **B — Évaluation de complexité** | **SYSTÉMATIQUE (tout prompt)** — grille ci-dessous : verdict COURT/SIMPLE (→ passage direct sans transformation, AUCUNE retranscription, verdict journalisé) ou COMPLEXE (→ phases C-D) | Verdict GO/NO-GO motivé sur critères |
| **C — Retranscription $FACON** | Reformulation complète en version compréhensible, explicite et structurée : objectif · contexte · contraintes · étapes ordonnées · dépendances · livrables · critères d'acceptation. Zéro perte sémantique — tout détail, nom, URL, chiffre ou contrainte de l'original est préservé | Prompt retranscrit $FACON2 |
| **D — Envoi à l'IA** | La version structurée devient l'entrée d'exécution de l'IA ; l'original est cité en provenance ; le bloc « prompt retranscrit » est affiché au propriétaire en français (règle d'or n°6) AVANT exécution | Exécution lancée sur la version structurée |

**Grille de complexité (phase B — 5 critères, GO si ≥ 2 critères COMPLEXE)** :

| Critère | COURT/SIMPLE | COMPLEXE |
|---------|--------------|----------|
| Longueur | ≤ ~20 mots | > ~20 mots ou multi-paragraphes |
| Étapes | 0-1 action unique | ≥ 2 actions, imbrication ou ordre contraignant |
| Ambiguïté | Références univoques | Pronoms/imprécisions à désambiguïser (« fais de même », « la même chose ») |
| Livrables | Réponse immédiate, sans fichier | Livrables nommés, multiples, ou avec format contraint |
| Contexte | Autosuffisant | Dépend de sessions/fichiers/URLs cités |

**Gardes-fous** : (1) jamais de perte sémantique — la retranscription est vérifiée contre l'original point par point avant envoi (phase C) ; (2) les prompts courts et simples ne sont JAMAIS transformés (phases A-B exécutées, retranscription omise — verdict journalisé, garde anti-bruit) ; (3) en cas d'indécision sur un critère, le critère compte COMPLEXE (prudence — mieux vaut structurer à tort que rater une exécution) ; (4) la retranscription ne modifie jamais l'intention du propriétaire — elle l'explicite ; (5) journalisation worklog R5 de CHAQUE passage gateway (verdict de complexité, #token du prompt original/retranscrit) ; (6) les prompts relevant du périmètre réservé d'un autre skill (déclencheurs verbatim d'un autre skill, corpus trigger_evals croisé — doctrine « périmètre » V6.1/V6.2 de l'arbitre check-triggers-replay) sont transmis à ce skill : la gateway analyse et journalise mais ne détourne JAMAIS le routage d'exécution.

## §2 — SPÉCIFICATION TECHNIQUE

- **Langage** : Markdown (rapports), Python (scripts de mesure), YAML (frontmatter)
- **Environnement** : `{{SKILLS_ROOT}}agent-prompt-engineering/`
- **Arbitres mobilisés** : verify-cross.py (cohérence PM ↔ formes), spell-check.py, verify-correct-work.py, check-triggers-replay.py (déclencheurs — 0 dérive attendue à toute évolution du présent skill)
- **Sorties** : rapport d'évaluation (grille §1.4), prompt restructuré (diff documenté), trigger_evals.json (M4), prompt retranscrit structuré (M5 — gabarit `references/prompt-gateway.md`)

## §3 — RELATIONS (extrait de SHARED §3.1)

| Avec | Nature | Détails |
|------|--------|---------|
| gen-plan | consulte | Contexte écosystème, planification E1-E8, méthode-mère (SHARED §7), version >= v3.7.0 |
| gen-plan | délégué par | Optimisation fine des prompts complexes (SHARED §3.1) |
| install-ecosystem | utilisé par | Bootstrap P6-P7 (INSTALL-ECOSYSTEME §9.1) |
| correct-work | vérifié par | Conformité des artefacts produits, version >= v2.5.0 |

## §4 — CONVENTIONS

- Nommage kebab-case (SHARED §1.2) ; worklog SHARED §1.4 ; Python uniquement (N3).
- Non-duplication (SHARED §6.3) : la définition des disciplines reste dans SHARED §7 (source de vérité, session A11) ; l'orchestration gen-plan dans PM gen-plan §1.9 ; le présent skill enregistre uniquement ses opérations et sa grille.
- Toute optimisation d'un artefact PM-gouverné passe par une révision de prompt (modèle de toilettage, SHARED en-tête) — jamais d'édition silencieuse.
