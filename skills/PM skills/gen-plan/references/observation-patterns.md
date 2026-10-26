# observation-patterns.md — Source de vérité du pattern Task Observer

Version : 1.0.0 · Créé : phase N20 (session B12-r41) · Restauré : B13-r5 (trace `1a0dfca3a0ffe13d`, post-wipe inter-sessions — reconstitution d'après la matérialisation installée `skills/knowledge-observer/`, le journal et le worklog ; le contenu exact d'origine, non documenté au-delà des marqueurs, est perdu au wipe).

<!-- PATTERN:OBSERVATION-PATTERNS-v1.0.0 -->

---

## §0 — Contexte Système (SHARED v1.6.0)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case | semver | #token | {{VARIABLE}} | @mon-ecosysteme/ (exception)
> Règle Zéro : skills auto-contenus, registre KB source de vérité, cross-references bidirectionnelles.

## §1 — Le pattern Task Observer

### §1.1 Problème

Un assistant IA opérant sur de longues sessions accumule des **erreurs récurrentes non détectées** : les mêmes blocages (quota API figé, arbitres mal calibrés, wipe inter-sessions, outils non recalibrés) reviennent sans qu'aucun mécanisme ne les généralise en règles. Les leçons restent enfouies dans le worklog, non structurées, non rejouables : le worklog documente, il ne **conclut** pas. L'apprentissage reste agent-driven et subjectif, sans détection mécanique des récurrences.

### §1.2 Solution

**Task Observer** : un observateur de sessions qui industrialise le cycle d'apprentissage continu — détection mécanique des patterns récurrents, journalisation structurée, proposition idempotente de correctifs, application validée. Le worklog + les boucles R3 + le KB Décisions remplissent déjà le cycle de manière agent-driven ; le Task Observer le rend **observé, journalisé et validé**.

### §1.3 Principe directeur

Observation passive par défaut ; jamais d'auto-modification non validée. L'observateur détecte et propose, l'écosystème (correct-work) valide, l'application est idempotente et tracée.

## §2 — Architecture

| Composant | Rôle | Emplacement |
|-----------|------|-------------|
| **Agent observateur** | Exécute le cycle A-H pendant/après la session | matérialisation : `{{SKILLS_ROOT}}knowledge-observer/` |
| **Journal des leçons** | Enregistrement persistant (étape C) | `{{SKILLS_ROOT}}knowledge-observer/data/lessons-learned.json` |
| **Rapport d'analyse** | Sortie de l'analyse post-session (étape D, E15 gen-plan) | worklog + KB |
| **Propositions** | Mises à jour idempotentes marquées (étape E) | blocs `PATTERN:` dans les skills cibles |
| **Validation** | Verdict correct-work (étape F) | verdict PASS requis avant application |

## §3 — Le cycle A-H

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

## §4 — Journal lessons-learned.json (schéma)

Chemin : `{{SKILLS_ROOT}}knowledge-observer/data/lessons-learned.json`. Structure racine : `{"lessons": [...], "schema": "...", "champs": {...}, "note": "..."}`. Champs d'une leçon :

| Champ | Règle | Description |
|-------|-------|-------------|
| `id` | L001, L002, … (séquentiel, **jamais réutilisé**) | identifiant de la leçon |
| `pattern` | description du pattern récurrent | ce qui a été observé |
| `occurrences` | nombre documenté (récurrence à 3, 2 si S1) | preuve de récurrence |
| `proposition` | mise à jour idempotente proposée (marqueur + rejeu sans effet) | correctif candidate |
| `statut` | `proposé \| validé \| appliqué \| rejeté` | état du cycle |
| `session` | identifiant de session (ex. B13-r5) | provenance |
| `verdict_correct_work` | PASS \| PASS AVEC RÉSERVES \| FAIL \| null | validation étape F |

## §5 — Les 4 modes

| Mode | Nom | Étapes | Description |
|------|-----|--------|-------------|
| M1 | **OBSERVATION** | A-B | Journalise et détecte les récurrences, ne modifie rien |
| M2 | **ANALYSE** | C-D | Enregistre les lessons, rapport d'analyse post-session (E15) |
| M3 | **PROPOSITION** | E-F | Propose des mises à jour idempotentes, fait valider par correct-work |
| M4 | **APPLICATION** | G-H | Applique les correctifs validés, met à jour le KB |

Déclenchement : automatique par gen-plan à E15 (modes M1-M2) ; manuel (« observe la session », « lessons learned », « analyse les patterns d'erreur »). Les modes M3-M4 exigent un verdict correct-work.

## §6 — Seuils de détection

- **Récurrence standard** : un pattern devient « récurrent » à **3 occurrences documentées**.
- **Récurrence S1** : à **2 occurrences** si la sévérité est critique (S1 — corruption de données, verdict faux, perte de livrable).
- Sous le seuil : la leçon est journalisée avec son compteur mais reste sans proposition (M3 ne s'ouvre qu'à récurrence atteinte).
- Chaque occurrence doit citer sa source (worklog Task ID, trace de session) — comptage vérifiable, jamais déclaratif.

## §7 — Garde-fous

1. **Observation passive par défaut** : M1 n'écrit que dans `data/lessons-learned.json`.
2. **Aucune auto-modification non validée** : les modes M3-M4 exigent un verdict correct-work (étape F) avant application.
3. **Garde anti-boucle** : max 2 rounds de correction par artefact (SHARED §4.4) — identique pour les lessons.
4. **Idempotence** : toute proposition appliquée porte un marqueur `PATTERN:` et est rejouable sans effet (R1-R6).

## §8 — Intégration écosystème

| Relation | Nature | Détail |
|----------|--------|--------|
| gen-plan | déclencheur | E15 — invoque knowledge-observer en modes M1-M2 (hook §1.2bis) |
| correct-work | validation | étape F — verdict sur les propositions (modes M3-M4) |
| skill-creator | application | conventions d'assemblage des mises à jour de skills |
| KNOWLEDGE.md | enrichissement | étape H — entrée versionnée + Décisions |
| arbitres | garde post-édition | re-certification après application M4 (leçon L004 : recalibrage croisé) |

<!-- FIN-PATTERN:OBSERVATION-PATTERNS-v1.0.0 -->

## §9 — Provenance

- **v1.0.0 — 2026-09-19 (phase N20, session B12-r41)** : création d'après `propositions-qwen.md` §1.5 (pattern Task Observer, cycle A-H).
- **2026-09-26 (B13-r5, trace `1a0dfca3a0ffe13d`)** : restauration post-wipe inter-sessions — reconstitution conforme à la matérialisation installée (knowledge-observer v1.0.0, SKILL.md 100 L) et au schéma du journal ; le fichier d'origine (absent du snapshot pré-N20 et de l'archive) est perdu. R2 : aucune information non dérivée des artefacts présents n'est introduite.
