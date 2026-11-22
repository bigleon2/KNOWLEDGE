---
name: image-generation
version: 1.0.0
category: ecosystem
language: fr
tags:
  - generation-images
  - ia-generative
  - prompt-image
  - z-ai-sdk
  - plateforme
description: >
  Génération d'images par IA via le SDK z-ai-web-dev-sdk (API images.generations.create)
  et sa CLI : créer des images depuis une description textuelle, sept tailles supportées
  (carré, portrait, paysage), résultat encodé base64. Déclencher quand l'utilisateur
  demande de créer une image, un visuel, une illustration ou une œuvre depuis un texte,
  ou d'intégrer une fonctionnalité de génération d'images à une application.
dependencies:
  - skill: image-edit
    version: ">=1.0.0"
    used_at: "Famille images z-ai-web-dev-sdk — édition d'images existantes (canal voisin)"
read_when:
  - Déclencher quand la demande concerne : créer une image depuis un texte (prompt),
    générer un visuel, une illustration, un artwork, des assets de design.
  - Déclencher si la demande mentionne : génération d'images, text-to-image, prompt
    image, créer un visuel/une illustration, z-ai image.
  - Ne pas déclencher pour éditer une image existante (image-edit), chercher des
    images réelles sur le web (image-search) ni analyser une image (vlm) — famille
    z-ai, un canal par skill (convention protocole, Task 28).
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

# IMAGE-GENERATION v1.0.0 — Génération d'images par IA (z-ai-web-dev-sdk)

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
(archive R4 — source exhaustive : CLI, gestion d'erreurs, exemples avancés).

## §1 — Spécification fonctionnelle

Créer des images de qualité depuis une description textuelle (prompt) : illustrations,
artworks, assets de design, workflows créatifs. Le SDK s'utilise en **backend
uniquement, jamais en code client**. Le résultat est retourné encodé en base64
(`response.data[0].base64`) puis écrit sur disque en binaire.

## §2 — Spécification technique

### Emplacement

`{{SKILLS_ROOT}}image-generation/` — script de référence : `scripts/image-generation.ts`.

### Tailles supportées

`1024x1024` (carré) | `768x1344` et `864x1152` (portrait) | `1344x768` et `1152x864`
(paysage) | `1440x720` (paysage large) | `720x1440` (portrait allongé).

### SDK — modèle d'appel

```javascript
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

async function generateImage(prompt, outputPath) {
  const zai = await ZAI.create();
  const response = await zai.images.generations.create({
    prompt: prompt,
    size: '1024x1024'
  });
  const buffer = Buffer.from(response.data[0].base64, 'base64');
  fs.writeFileSync(outputPath, buffer);
}

await generateImage('A cute cat playing in the garden', './cat_image.png');
```

Toute taille hors liste supportée doit être rejetée avant l'appel (validation en
amont). Une CLI de génération rapide est incluse — invocation détaillée dans
`references/plateforme-original.md`.

## §3 — Relations

| Avec | Nature | Détails |
|------|--------|---------|
| image-edit | Canal voisin | Édition d'images existantes (variations, transformations) |
| image-search | Frontière | Images réelles du web (OSS) — pas de génération |
| vlm | aval | Analyse/contrôle qualité de l'image générée |

---

## HISTORIQUE DES VERSIONS

| Version | Date | Changements |
|---------|------|-------------|
| 1.0.0 | 2026-11-22 | Task 113 — import aux normes skill-creator : frontmatter écosystème (semver, category, language, tags, read_when triptyque), §0 Contexte Système, corps français ; original anglais archivé byte-identité references/plateforme-original.md (R4) |
