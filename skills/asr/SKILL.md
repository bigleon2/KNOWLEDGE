---
name: asr
version: 1.0.0
category: ecosystem
language: fr
tags:
  - asr
  - speech-to-text
  - transcription
  - audio
  - z-ai-sdk
  - plateforme
description: >
  Transcription automatique de la parole en texte (ASR — Automatic Speech Recognition)
  via le SDK z-ai-web-dev-sdk et la CLI z-ai : transcrire des fichiers audio (WAV, MP3
  et formats courants) en texte, en local ou encodés en base64, avec sortie JSON.
  Déclencher quand l'utilisateur demande de transcrire un enregistrement audio, de
  convertir de la parole en texte, de construire une fonctionnalité de saisie vocale
  ou d'analyser le contenu d'un fichier son.
dependencies:
  - skill: llm
    version: ">=1.0.0"
    used_at: "Famille z-ai-web-dev-sdk — même runtime CLI/SDK, backend uniquement"
read_when:
  - Déclencher quand la demande concerne : transcrire de l'audio en texte (ASR), traiter
    des enregistrements vocaux, construire une saisie vocale, extraire le contenu parole
    d'un fichier WAV/MP3.
  - Déclencher si la demande mentionne : transcription, ASR, speech-to-text, reconnaissance
    vocale, sous-titrage depuis l'audio, z-ai asr.
  - Ne pas déclencher pour la synthèse vocale (TTS), l'analyse d'images (VLM), la
    génération de texte (LLM) ni l'analyse vidéo (video-understand) — famille z-ai,
    un canal par skill (convention protocole, Task 28).
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

# ASR v1.0.0 — Transcription parole vers texte (z-ai-web-dev-sdk)

## §0 — Contexte Système (SHARED v1.7.46)

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
(archive R4 — source exhaustive des exemples SDK). Ancien dossier « ASR » renommé
kebab-case « asr » (SHARED §1.2).

## §1 — Spécification fonctionnelle

Transcrire la parole d'un fichier audio en texte : enregistrements, interviews,
messages vocaux, saisie vocale d'application. Le SDK z-ai-web-dev-sdk s'utilise en
**backend uniquement, jamais en code client**. Deux voies d'entrée :

- **CLI** (`z-ai asr`) : transcription rapide, tests, traitement par lots ;
- **SDK** (`import ZAI from 'z-ai-web-dev-sdk'`) : intégration applicative, flux
  streaming — exemples complets dans `scripts/asr.ts` et l'archive R4.

Formats audio supportés : WAV, MP3 et formats courants.

## §2 — Spécification technique

### Emplacement

`{{SKILLS_ROOT}}asr/` — script de référence : `scripts/asr.ts` (exemple fonctionnel).

### CLI

```bash
# Transcrire un fichier audio
z-ai asr --file ./audio.wav

# Sortie JSON vers fichier
z-ai asr -f ./recording.mp3 -o transcript.json

# Depuis un flux encodé en base64
z-ai asr --base64 "UklGRiQAAABXQVZFZm10..." -o result.json

# Sortie en flux
z-ai asr -f ./audio.wav --stream
```

Paramètres : `--file, -f <chemin>` (requis sauf base64) | `--base64, -b <b64>`
(requis sauf fichier) | `--output, -o <chemin>` (JSON) | `--stream` (sortie en flux).

### Choix CLI vs SDK

- **CLI** : transcription ponctuelle, test de précision, lots simples.
- **SDK** : intégration applicative, streaming, contrôle fin — modèle d'appel complet
  dans `references/plateforme-original.md` (sections SDK Usage et Error Handling).

## §3 — Relations

| Avec | Nature | Détails |
|------|--------|---------|
| llm | Famille | Même runtime z-ai-web-dev-sdk — post-traitement du transcript par chat completions |
| tts | Inverse | TTS produit de l'audio depuis le texte ; asr fait l'opération inverse |
| vlm / video-understand | Famille | Autres canaux multimodaux du même SDK |

---

## HISTORIQUE DES VERSIONS

| Version | Date | Changements |
|---------|------|-------------|
| 1.0.0 | 2026-11-22 | Task 113 — import aux normes skill-creator : frontmatter écosystème (semver, category, language, tags, read_when triptyque), §0 Contexte Système, corps français, dossier renommé ASR → asr (kebab-case SHARED §1.2) ; original anglais archivé byte-identité references/plateforme-original.md (R4) |
