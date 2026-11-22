---
name: vlm
version: 1.0.0
category: ecosystem
language: fr
tags:
  - vlm
  - vision
  - analyse-images
  - multimodal
  - z-ai-sdk
  - plateforme
description: >
  Chat vision par IA (VLM — Vision Language Model) via le SDK z-ai-web-dev-sdk et
  la CLI z-ai vision : analyser des images (URL, base64 ou fichier local), décrire
  du contenu visuel, comparer plusieurs images, combiner compréhension d'image et
  conversation. Déclencher quand l'utilisateur demande d'analyser une image, de
  décrire un contenu visuel, d'extraire des informations d'une photo ou de construire
  une application multimodale image + texte.
dependencies:
  - skill: llm
    version: ">=1.0.0"
    used_at: "Famille z-ai-web-dev-sdk — même runtime CLI/SDK, backend uniquement"
read_when:
  - Déclencher quand la demande concerne : analyser/décrire/comparer des images,
    extraire des informations visuelles, construire un chatbot qui comprend les images.
  - Déclencher si la demande mentionne : VLM, vision chat, analyse d'image, que
    contient cette photo, décrire une image, z-ai vision, multimodal.
  - Ne pas déclencher pour la génération d'images (image-generation), l'édition
    d'images (image-edit), la recherche d'images (image-search), l'audio (asr/tts)
    ni la génération de texte seul (llm) — famille z-ai, un canal par skill
    (convention protocole, Task 28).
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

# VLM v1.0.0 — Chat vision (z-ai-web-dev-sdk)

## §0 — Contexte Système (SHARED v1.7.45)

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
(archive R4 — source exhaustive : base64, multi-images, erreurs). Ancien dossier
« VLM » renommé kebab-case « vlm » (SHARED §1.2).

## §1 — Spécification fonctionnelle

Analyser des images par dialogue : décrire un contenu visuel, répondre à des questions
sur une image, comparer plusieurs images, extraire des informations. Sources supportées :
URL distante, fichier local, image encodée en base64 ; plusieurs images par requête.
Le raisonnement chaîne-de-pensée (`--thinking`) améliore les analyses complexes.
Le SDK s'utilise en **backend uniquement, jamais en code client**.

## §2 — Spécification technique

### Emplacement

`{{SKILLS_ROOT}}vlm/` — script de référence : `scripts/vlm.ts`.

### CLI

```bash
# Décrire une image depuis une URL
z-ai vision --prompt "What's in this image?" --image "https://example.com/photo.jpg"

# Options courtes
z-ai vision -p "Describe this image" -i "https://example.com/image.png"

# Image locale, réponse sauvegardée
z-ai vision -p "Describe the scene" -i "./landscape.png" -o description.json

# Plusieurs images (comparaison)
z-ai vision \
  -p "Compare these two images" \
  -i "./photo1.jpg" \
  -i "./photo2.jpg" \
  -o comparison.json

# Raisonnement chaîne-de-pensée
z-ai vision -p "Count the people and describe their activities" -i "./crowd.jpg" --thinking
```

Paramètres : `--prompt, -p <texte>` (requis) | `--image, -i <url|chemin|b64>` (répétable)
| `--thinking, -t` | `--output, -o <chemin>` (JSON) | `--stream`.

### SDK

Modèle d'appel `zai.chat.completions.create` avec messages contenant des images
(URL ou base64) — code intégral dans `scripts/vlm.ts` et `references/plateforme-original.md`.

## §3 — Relations

| Avec | Nature | Détails |
|------|--------|---------|
| video-understand | Extension | L'analyse vidéo passe par le même canal vision (drapeau --image avec URL vidéo) |
| image-generation / image-edit / image-search | Frontière | Génération, édition et recherche d'images — l'analyse relève du présent skill |
| llm / asr / tts | Famille | Même runtime z-ai-web-dev-sdk, autres canaux |

---

## HISTORIQUE DES VERSIONS

| Version | Date | Changements |
|---------|------|-------------|
| 1.0.0 | 2026-11-22 | Task 113 — import aux normes skill-creator : frontmatter écosystème (semver, category, language, tags, read_when triptyque), §0 Contexte Système, corps français, dossier renommé VLM → vlm (kebab-case SHARED §1.2) ; original anglais archivé byte-identité references/plateforme-original.md (R4) |
