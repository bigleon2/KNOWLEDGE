---
name: ContentAnalysis
version: "1.0.0"
category: "Autres"
tags:
  - contentanalysis
description: Extraction et analyse de contenu — extraction d'insights à partir de vidéos, podcasts, articles et YouTube. USE WHEN extract wisdom, content analysis, analyze content, insight report, analyze video, analyze podcast, extract insights, key takeaways, what did I miss, extract from YouTube.
language: fr

read_when:
  - Déclencher quand la demande concerne : extraction et analyse de contenu — extraction d'insights à partir de vidéos, podcasts, articles et YouTube
  - Déclencher si la demande mentionne : extract, analyze, extraction
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

## §0 — Contexte Système (SHARED v1.6.8)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.



# ContentAnalysis

Skill unifié pour les flux de travail d'extraction et d'analyse de contenu.

## Workflow Routing

| Motif de requête | Router vers |
|---|---|
| Extract wisdom, content analysis, insight report, analyze content | `ExtractWisdom/SKILL.md` |
