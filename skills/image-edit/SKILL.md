---
name: image-edit
version: 1.0.0
category: ecosystem
language: fr
tags:
  - edition-images
  - ia-generative
  - variation
  - transformation
  - z-ai-sdk
  - plateforme
description: >
  Édition et modification d'images par IA via le SDK z-ai-web-dev-sdk (API
  images.generations.edit) et sa CLI : transformer une image existante selon une
  description textuelle, créer des variations, redessiner des assets. Déclencher
  quand l'utilisateur demande de modifier, retoucher, transformer ou décliner une
  image existante à partir d'un texte descriptif.
dependencies:
  - skill: image-generation
    version: ">=1.0.0"
    used_at: "Famille images z-ai-web-dev-sdk — génération depuis texte (canal voisin)"
read_when:
  - Déclencher quand la demande concerne : éditer/retoucher/transformer une image
    existante par description textuelle, créer des variations, redessiner un asset.
  - Déclencher si la demande mentionne : édition d'image, modifier cette photo,
    transformer l'image, créer une variation, z-ai image edit.
  - Ne pas déclencher pour créer une image depuis rien (image-generation), chercher
    des images (image-search) ni analyser une image (vlm) — famille z-ai, un canal
    par skill (convention protocole, Task 28).
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

# IMAGE-EDIT v1.0.0 — Édition d'images par IA (z-ai-web-dev-sdk)

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
(archive R4 — source exhaustive : CLI, base64 local, gestion d'erreurs).

## §1 — Spécification fonctionnelle

Modifier, transformer et décliner des images existantes selon une description
textuelle : refonte d'assets, variations, amélioration de contenu visuel. Le SDK
s'utilise en **backend uniquement, jamais en code client**. Source : URL distante
ou image locale encodée en base64 (data URL). Résultat : image éditée encodée base64.

## §2 — Spécification technique

### Emplacement

`{{SKILLS_ROOT}}image-edit/` — script de référence : `scripts/image-edit.ts`.

### SDK — méthode d'API

```javascript
await zai.images.generations.edit({
  prompt: string,              // Requis : description de l'édition à appliquer
  images: [{ url: string }],   // Requis : tableau d'objets avec propriété url
  size?: string,               // Optionnel : taille de sortie (défaut '1024x1024')
  model?: string               // Optionnel : nom du modèle
})
```

Point d'entrée : `POST /images/generations/edit`. ATTENTION : le paramètre `images`
est un **tableau d'objets** `{ url }`, jamais une chaîne simple.

### Exemple minimal

```javascript
import ZAI from 'z-ai-web-dev-sdk';
import fs from 'fs';

async function editImage(imageSource, editPrompt, outputPath, size = '1024x1024') {
  const zai = await ZAI.create();
  const response = await zai.images.generations.edit({
    prompt: editPrompt,
    images: [{ url: imageSource }],
    size: size
  });
  fs.writeFileSync(outputPath, Buffer.from(response.data[0].base64, 'base64'));
}

await editImage(
  'https://example.com/landscape.jpg',
  'Transform this landscape into a night scene with stars and moon',
  './landscape_night.png'
);
```

Une CLI d'édition rapide est incluse — invocation détaillée dans
`references/plateforme-original.md` (même famille de tailles que image-generation).

## §3 — Relations

| Avec | Nature | Détails |
|------|--------|---------|
| image-generation | Canal voisin | Génération depuis texte ; le présent skill édite une image source |
| image-search | Frontière | Recherche d'images réelles — pas d'édition générative |
| vlm | aval | Contrôle qualité du résultat édité |

---

## HISTORIQUE DES VERSIONS

| Version | Date | Changements |
|---------|------|-------------|
| 1.0.0 | 2026-11-22 | Task 113 — import aux normes skill-creator : frontmatter écosystème (semver, category, language, tags, read_when triptyque), §0 Contexte Système, corps français ; original anglais archivé byte-identité references/plateforme-original.md (R4) |
