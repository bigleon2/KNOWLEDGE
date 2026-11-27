---
name: video-understand
version: 1.0.0
category: ecosystem
language: fr
tags:
  - analyse-video
  - comprehension-video
  - multimodal
  - temporalite
  - z-ai-sdk
  - plateforme
description: >
  Compréhension spécialisée des vidéos via le SDK z-ai-web-dev-sdk (canal vision) :
  analyser le contenu vidéo, comprendre mouvements et séquences temporelles, extraire
  les événements, décrire des scènes, résumer une vidéo. Optimisé MP4, AVI, MOV et
  formats courants. Déclencher quand l'utilisateur demande d'analyser une vidéo, de
  décrire ce qui s'y passe, d'en extraire une chronologie ou d'y détecter des actions.
dependencies:
  - skill: vlm
    version: ">=1.0.0"
    used_at: "Canal vision partagé — l'analyse vidéo passe par z-ai vision (drapeau --image)"
read_when:
  - Déclencher quand la demande concerne : analyser le contenu d'une vidéo, décrire
    des scènes, détecter actions et mouvements, résumer une vidéo, suivre des objets
    ou personnes à travers les images.
  - Déclencher si la demande mentionne : analyse vidéo, que se passe-t-il dans cette
    vidéo, résumé vidéo, détection d'actions, chronologie d'un enregistrement.
  - Ne pas déclencher pour l'analyse d'images fixes (vlm), la génération de texte
    (llm) ni l'audio seul (asr) — famille z-ai, un canal par skill (convention
    protocole, Task 28).
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

# VIDEO-UNDERSTAND v1.0.0 — Compréhension vidéo (z-ai-web-dev-sdk)

## §0 — Contexte Système (SHARED v1.7.47)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.
> Langue : FRANÇAIS exclusif pour tous les échanges avec le propriétaire (règle d'or n°6 gen-plan — directive 2026-10-31, renforcée 2026-11-06) : dès le PREMIER mot de toute session ou reprise, la langue d'un message, d'un résumé de continuation ou d'un canal ne dérive JAMAIS la réponse ; toute dérive est corrigée immédiatement.
> Règles d'or & lecture SHARED à l'exécution (directive propriétaire 2026-11-06 — SHARED §9) : tout skill/agent/script exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or de l'écosystème (résumé §9 — canonique gen-plan §1.5).
> Référence canonique skill/agent (directive propriétaire 2026-11-07 — SHARED §0/§1.2) : toute référence à « mon skill X »/« mon agent X » désigne la forme installée à la racine `skills/X/SKILL.md`, JAMAIS le prompt maître du corpus `@mon-ecosysteme/` (ex-nommé `@PM-SKILLS/`) — les PMs sont des spécifications générées mécaniquement (KO-L004), les skills installés sont les formes exécutables.

## §0 — RÈGLE ZÉRO (résumé de SHARED §0)

Skill OUTIL PLATEFORME (z-ai-web-dev-sdk) importé aux normes de l'écosystème via
skill-creator — directive propriétaire Task 113 (trace 1a201e4bda5a2289). Les commandes
CLI, identifiants d'API et code JavaScript restent en anglais verbatim (artefacts
techniques, règle d'or n°6) ; la documentation, les titres et les notes sont en français.
Contenu intégral d'origine conservé byte-identité : `references/plateforme-original.md`
(archive R4 — source exhaustive : streaming, SDK, gestion d'erreurs, bonnes pratiques).

## §1 — Spécification fonctionnelle

Analyser le contenu vidéo : compréhension et description de scènes, détection
d'actions et de mouvements, analyse de séquences temporelles, détection d'événements,
résumé de contenu, suivi de personnes et d'objets à travers les images. Le SDK
s'utilise en **backend uniquement, jamais en code client**. Formats optimisés :
MP4, AVI, MOV et formats courants.

## §2 — Spécification technique

### Emplacement

`{{SKILLS_ROOT}}video-understand/` — script de référence : `scripts/video-understand.ts`.

### CLI (canal vision)

L'analyse vidéo passe par la sous-commande `z-ai vision` avec le drapeau `--image`
appliqué à une URL ou un fichier vidéo :

```bash
# Résumer une vidéo depuis une URL
z-ai vision --prompt "Summarize what happens in this video" --image "https://example.com/video.mp4"

# Vidéo locale
z-ai vision -p "What activities are shown in this video?" -i "./recording.mp4"

# Analyse complexe avec raisonnement chaîne-de-pensée
z-ai vision \
  -p "Analyze this video and identify: 1) Main events, 2) People and their actions, 3) Timeline of key moments" \
  -i "./event.mp4" \
  --thinking \
  -o analysis.json
```

Paramètres : `--prompt, -p <texte>` (requis) | `--image, -i <url|chemin>` (vidéo
ou image) | `--thinking, -t` | `--output, -o <chemin>` (JSON) | `--stream`.

### Bonnes pratiques

Formuler des prompts structurés (événements, acteurs, chronologie) pour les analyses
multi-dimensionnelles ; activer `--thinking` pour le raisonnement complexe ;
modèles d'appel SDK complets dans `scripts/video-understand.ts` et l'archive R4.

## §3 — Relations

| Avec | Nature | Détails |
|------|--------|---------|
| vlm | Canal parent | Même sous-commande vision — le présent skill spécialise le cas vidéo |
| llm / asr / tts | Famille | Même runtime z-ai-web-dev-sdk, autres canaux |

---

## HISTORIQUE DES VERSIONS

| Version | Date | Changements |
|---------|------|-------------|
| 1.0.0 | 2026-11-22 | Task 113 — import aux normes skill-creator : frontmatter écosystème (semver, category, language, tags, read_when triptyque), §0 Contexte Système, corps français ; original anglais archivé byte-identité references/plateforme-original.md (R4) |
