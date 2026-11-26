---
name: tts
version: 1.0.0
category: ecosystem
language: fr
tags:
  - tts
  - text-to-speech
  - synthese-vocale
  - audio
  - z-ai-sdk
  - plateforme
description: >
  Synthèse vocale (TTS — Text to Speech) via le SDK z-ai-web-dev-sdk et la CLI
  z-ai tts : convertir du texte en parole naturelle avec voix multiples, vitesse
  réglable (0,5 à 2,0) et formats WAV/PCM/MP3. Déclencher quand l'utilisateur
  demande de générer un fichier audio parlé, de créer du contenu audio, de doter
  une application de sortie vocale ou de produire une voix off.
dependencies:
  - skill: asr
    version: ">=1.0.0"
    used_at: "Famille z-ai-web-dev-sdk — même runtime CLI/SDK, backend uniquement"
read_when:
  - Déclencher quand la demande concerne : convertir du texte en audio parlé, générer
    une voix off, produire un fichier audio depuis un script, construire une
    application à sortie vocale.
  - Déclencher si la demande mentionne : TTS, text-to-speech, synthèse vocale, voix
    de lecture, audio généré, z-ai tts, voix off.
  - Ne pas déclencher pour la transcription (ASR), la vision (VLM) ni la génération
    de texte (LLM) — famille z-ai, un canal par skill (convention protocole, Task 28).
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

# TTS v1.0.0 — Synthèse vocale texte vers parole (z-ai-web-dev-sdk)

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
(archive R4 — source exhaustive : voix disponibles, exemples SDK, découpage de textes
longs). Ancien dossier « TTS » renommé kebab-case « tts » (SHARED §1.2).

## §1 — Spécification fonctionnelle

Convertir du texte en parole naturelle : voix multiples, vitesse et volume réglables,
sortie WAV/PCM/MP3. Le SDK s'utilise en **backend uniquement, jamais en code client**.
Deux voies d'entrée :

- **CLI** (`z-ai tts`) : génération rapide, tests de voix, automatisation simple ;
- **SDK** (`import ZAI from 'z-ai-web-dev-sdk'`) : intégration applicative — exemple
  complet : `scripts/tts.ts` et `tts.ts` à la racine du skill.

### Contraintes d'API (à connaître AVANT implémentation)

| Contrainte | Valeur | Conséquence |
|------------|--------|-------------|
| Longueur du texte | 1024 caractères max par requête | Texte long → découper en morceaux (fonction `splitTextIntoChunks` dans l'archive R4) |
| Vitesse (`speed`) | 0,5 à 2,0 (défaut 1,0) | 0,5 = ralenti de moitié, 2,0 = accéléré double |
| Volume | supérieur à 0, jusqu'à 10 (défaut 1,0) | Valeur strictement positive |
| Streaming | uniquement format `pcm` | `stream: true` → PCM seul ; hors flux : wav, pcm, mp3 |
| Fréquence d'échantillonnage | 24000 Hz recommandée | — |

## §2 — Spécification technique

### Emplacement

`{{SKILLS_ROOT}}tts/` — scripts de référence : `scripts/tts.ts` et `tts.ts`.

### CLI

```bash
# Texte vers parole (WAV par défaut)
z-ai tts --input "Bonjour le monde" --output ./bonjour.wav

# Options courtes
z-ai tts -i "Bonjour le monde" -o ./bonjour.wav
```

Paramètres : `--input, -i <texte>` (requis) | `--output, -o <chemin>` | options de
voix/vitesse détaillées dans `references/plateforme-original.md`.

### Textes longs

Au-delà de 1024 caractères, découper par phrases (le modèle `splitTextIntoChunks`
de l'archive R4 regroupe les phrases jusqu'à la limite) puis synthétiser chaque
morceau et concaténer les sorties audio.

## §3 — Relations

| Avec | Nature | Détails |
|------|--------|---------|
| asr | Inverse | ASR transcrit l'audio en texte ; tts produit l'audio depuis le texte |
| llm / vlm | Famille | Même runtime z-ai-web-dev-sdk, autres canaux |

---

## HISTORIQUE DES VERSIONS

| Version | Date | Changements |
|---------|------|-------------|
| 1.0.0 | 2026-11-22 | Task 113 — import aux normes skill-creator : frontmatter écosystème (semver, category, language, tags, read_when triptyque), §0 Contexte Système, corps français, dossier renommé TTS → tts (kebab-case SHARED §1.2) ; original anglais archivé byte-identité references/plateforme-original.md (R4) |
