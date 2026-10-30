---
nom: ContentAnalysis
source: skills/contentanalysis/SKILL.md
sha256_source: ca4830e8e349
genere: 2026-10-26 (phase P2 — directive 10 tâches, tâche 2)
usage: AUTONOME hors écosystème (dossier « Prompt Maitre » — non lu par l'orchestration)
---

> ⚠️ **MARQUEUR D'EXCLUSION (garde D010)** — CE DOSSIER N'EST PAS LU PAR L'ORCHESTRATION. Les dossiers « Prompt Maitre » sont des prompts autonomes à usage HORS écosystème : ils ne sont pas indexés au registre KB, ne sont mobilisés par aucun arbitre, et ne remplacent jamais la forme installée `skills/<skill>/` (source de vérité).

# Prompt Maître autonome — ContentAnalysis (version non déclarée)

## Comment utiliser ce prompt (hors écosystème)

Ce document encapsule la compétence sous forme autonome : copiez-le intégralement
dans un assistant IA (ou ouvrez-le en référence directe) — aucune installation,
aucun registre, aucune dépendance à l'écosystème Knowledge d'origine n'est requise.
Les variables de l'écosystème d'origine ont été résolues en valeurs littérales ;
si des ressources `references/` accompagnent ce dossier, elles sont jointes au même
emplacement et le prompt y renvoie par leur chemin relatif. La version d'origine
(source de vérité) vit dans `skills/contentanalysis/SKILL.md` du dépôt KNOWLEDGE.

---

## Le prompt

---
name: ContentAnalysis
description: Content extraction and analysis — wisdom extraction from videos, podcasts, articles, and YouTube. USE WHEN extract wisdom, content analysis, analyze content, insight report, analyze video, analyze podcast, extract insights, key takeaways, what did I miss, extract from YouTube.
---

## §0 — Contexte Système (SHARED v1.7.14)

> Écosystème Knowledge : `skills/`=skills/ | `skills/KNOWLEDGE.md`=skills/KNOWLEDGE.md | `true`=true | `NORMAL`=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.



# ContentAnalysis

Unified skill for content extraction and analysis workflows.

## Workflow Routing

| Request Pattern | Route To |
|---|---|
| Extract wisdom, content analysis, insight report, analyze content | `ExtractWisdom/SKILL.md` |


---

## Ressources locales du dossier

Aucune ressource annexe — ce prompt est auto-suffisant.
