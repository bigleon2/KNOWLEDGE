---
name: llm
version: 1.0.0
category: ecosystem
language: fr
tags:
  - llm
  - chat-completions
  - generation-texte
  - assistant
  - z-ai-sdk
  - plateforme
description: >
  Complétions de chat par grand modèle de langage (LLM) via le SDK z-ai-web-dev-sdk
  et la CLI z-ai chat : conversations multi-tours, prompts système, raisonnement
  chaîne-de-pensée (thinking), streaming. Déclencher quand l'utilisateur demande de
  construire un chatbot, un assistant IA, une fonctionnalité de génération de texte,
  ou d'interroger le LLM en ligne de commande.
dependencies:
  - skill: asr
    version: ">=1.0.0"
    used_at: "Famille z-ai-web-dev-sdk — même runtime CLI/SDK, backend uniquement"
read_when:
  - Déclencher quand la demande concerne : complétion de chat LLM, chatbot, assistant
    IA, génération de texte par modèle, prompts système multi-tours, streaming de
    réponses.
  - Déclencher si la demande mentionne : LLM, chat completions, z-ai chat, assistant
    conversationnel, prompt système, thinking/chaîne de pensée.
  - Ne pas déclencher pour la vision (VLM), l'audio (ASR/TTS), les images
    (image-generation/image-edit) ni l'analyse vidéo (video-understand) — famille
    z-ai, un canal par skill (convention protocole, Task 28).
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

# LLM v1.0.0 — Complétions de chat (z-ai-web-dev-sdk)

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
(archive R4 — source exhaustive des exemples SDK multi-tours). Ancien dossier « LLM »
renommé kebab-case « llm » (SHARED §1.2).

## §1 — Spécification fonctionnelle

Complétions de chat par LLM : conversations multi-tours avec gestion du contexte,
prompts système pour cadrer le comportement, raisonnement chaîne-de-pensée (thinking)
pour les problèmes complexes, streaming temps réel. Le SDK s'utilise en **backend
uniquement, jamais en code client**. Deux voies d'entrée :

- **CLI** (`z-ai chat`) : questions ponctuelles, tests, scripts d'automatisation ;
- **SDK** (`import ZAI from 'z-ai-web-dev-sdk'`) : applications conversationnelles,
  gestion de l'historique — exemple complet : `scripts/chat.ts`.

## §2 — Spécification technique

### Emplacement

`{{SKILLS_ROOT}}llm/` — script de référence : `scripts/chat.ts`.

### CLI

```bash
# Question simple
z-ai chat --prompt "What is the capital of France?"

# Réponse sauvegardée en JSON
z-ai chat -p "Explain quantum computing" -o response.json

# Streaming de la réponse
z-ai chat -p "Write a short poem" --stream

# Prompt système personnalisé
z-ai chat \
  --prompt "Review this code: function add(a,b) { return a+b; }" \
  --system "You are an expert code reviewer" \
  -o review.json

# Raisonnement chaîne-de-pensée
z-ai chat -p "Solve this math problem..." --thinking -o solution.json
```

Paramètres : `--prompt, -p <texte>` (requis) | `--system, -s <texte>` | `--thinking, -t`
| `--output, -o <chemin>` (JSON) | `--stream`.

### SDK — gestion multi-tours

L'historique de conversation se construit en tableau de messages (rôles system/user/
assistant) passé à chaque appel — modèle de code intégral dans
`references/plateforme-original.md` (sections SDK Usage, Multi-Turn Conversation et
Error Handling).

## §3 — Relations

| Avec | Nature | Détails |
|------|--------|---------|
| asr / tts / vlm | Famille | Même runtime z-ai-web-dev-sdk, autres canaux (audio, vision) |
| agent-prompt-engineering | Amont | Rédaction des prompts système durables des assistants construits sur ce canal |

---

## HISTORIQUE DES VERSIONS

| Version | Date | Changements |
|---------|------|-------------|
| 1.0.0 | 2026-11-22 | Task 113 — import aux normes skill-creator : frontmatter écosystème (semver, category, language, tags, read_when triptyque), §0 Contexte Système, corps français, dossier renommé LLM → llm (kebab-case SHARED §1.2) ; original anglais archivé byte-identité references/plateforme-original.md (R4) |
