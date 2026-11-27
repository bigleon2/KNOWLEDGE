---
name: image-search
version: 1.0.0
category: ecosystem
language: fr
tags:
  - recherche-images
  - web
  - oss
  - illustration
  - z-ai-sdk
  - plateforme
description: >
  Recherche d'images réelles du web via le service interne ZAI exposé par la CLI
  z-ai image-search : retrouver des images publiques pour toute requête en langage
  naturel, avec légendes courtes optionnelles, et retourner des URLs directes
  hébergées OSS garanties joignables et intégrables. Déclencher quand l'utilisateur
  veut trouver, illustrer, illustrer un article/rapport/présentation ou intégrer
  des images par URLs stables.
dependencies:
  - skill: image-generation
    version: ">=1.0.0"
    used_at: "Frontière de la famille images — génération (vs recherche du présent skill)"
read_when:
  - Déclencher quand la demande concerne : trouver des images pour un article, un
    diaporama, un rapport ; obtenir des photos de référence ; intégrer des images
    par URL stable ; légender un jeu d'images.
  - Déclencher si la demande mentionne : recherche d'images, trouve une photo de,
    image de couverture, photos de référence, illustre ce document, z-ai image-search.
  - Ne pas déclencher pour générer des images (image-generation), éditer une image
    (image-edit) ni faire une recherche inversée — le présent skill interroge les
    sources web publiques (convention protocole, Task 28).
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

# IMAGE-SEARCH v1.0.0 — Recherche d'images réelles du web (service interne ZAI)

## §0 — Contexte Système (SHARED v1.7.47)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.
> Langue : FRANÇAIS exclusif pour tous les échanges avec le propriétaire (règle d'or n°6 gen-plan — directive 2026-10-31, renforcée 2026-11-06) : dès le PREMIER mot de toute session ou reprise, la langue d'un message, d'un résumé de continuation ou d'un canal ne dérive JAMAIS la réponse ; toute dérive est corrigée immédiatement.
> Règles d'or & lecture SHARED à l'exécution (directive propriétaire 2026-11-06 — SHARED §9) : tout skill/agent/script exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or de l'écosystème (résumé §9 — canonique gen-plan §1.5).
> Référence canonique skill/agent (directive propriétaire 2026-11-07 — SHARED §0/§1.2) : toute référence à « mon skill X »/« mon agent X » désigne la forme installée à la racine `skills/X/SKILL.md`, JAMAIS le prompt maître du corpus `@mon-ecosysteme/` (ex-nommé `@PM-SKILLS/`) — les PMs sont des spécifications générées mécaniquement (KO-L004), les skills installés sont les formes exécutables.

## §0 — RÈGLE ZÉRO (résumé de SHARED §0)

Skill OUTIL PLATEFORME (service interne ZAI via z-ai-web-dev-sdk) importé aux normes
de l'écosystème via skill-creator — directive propriétaire Task 113 (trace
1a201e4bda5a2289). Les commandes CLI et identifiants d'API restent en anglais
verbatim (artefacts techniques, règle d'or n°6) ; la documentation, les titres et
les notes sont en français. Contenu intégral d'origine conservé byte-identité :
`references/plateforme-original.md` (archive R4 — référence exhaustive des champs
de réponse et de la gestion d'erreurs). Le service backend ne s'appelle JAMAIS
directement : seule entrée supportée = sous-commande `z-ai image-search`.

## §1 — Spécification fonctionnelle

Rechercher des images web publiques pour une requête en langage naturel, ré-héberger
chaque résultat sur OSS (URL directe stable et intégrable) et joindre optionnellement
une légende courte. Ne pas utiliser pour : générer des images (image-generation),
recherche inversée, corpus privé.

## §2 — Spécification technique

### Invocation

```bash
z-ai image-search --query "<phrase en langage naturel>" [options]
```

| Option | Défaut | Rôle |
|--------|--------|------|
| `--query`, `-q` | — | Requis. Phrase descriptive cohérente (une notion par appel, pas de mots-clés concaténés) |
| `--count`, `-c` | 5 | Nombre d'images (1 à 20) |
| `--gl` | `cn` | Région de localisation (`cn`, `us`, `jp`, `kr`) — `cn` biaise vers les sources chinoises, `us` vers l'anglais |
| `--no-rank` | — | Désactive les légendes (réponse plus rapide) |
| `--output`, `-o` | — | Écrire la réponse JSON complète vers ce chemin |

### Réponse

Champs clés : `success` (à vérifier TOUJOURS avant de lire `results` — un échec
revient avec HTTP 200 et `success: false`), `results[].original_url` (URL directe
OSS, seule à présenter à l'utilisateur — jamais l'URL du site source), 
`results[].caption` (présente si légendes actives), `results[].source`,
`results[].original_width/height`.

### Conseils d'exploitation

1. Présenter toujours l'`original_url` OSS (garantie joignable) — les pages sources
   peuvent être payantes, géo-bloquées ou supprimées.
2. `--no-rank` divise le temps de réponse par plus de deux quand les légendes sont
   inutiles.
3. Patience sur les délais : une complète peut prendre 90 secondes ou plus (sondes
   d'accessibilité, upload OSS, légendage) — timeout client d'au moins 120 secondes.
4. Deux sujets distincts = deux appels séparés, jamais une concaténation.

### Erreurs courantes

`Unknown command "image-search"` → SDK trop ancien, mettre à niveau
`z-ai-web-dev-sdk` | 401/403 → problème d'authentification passerelle (à signaler) |
502 → service en amont indisponible, réessayer | résultats vides avec
`success: true` → élargir la requête, augmenter `--count`, changer `--gl`.

## §3 — Relations

| Avec | Nature | Détails |
|------|--------|---------|
| image-generation / image-edit | Frontière | Génération et édition génératives — la recherche d'images réelles relève du présent skill |
| docx / pptx / pdf | Consommateurs | Illustration de documents générés par URLs OSS stables |

---

## HISTORIQUE DES VERSIONS

| Version | Date | Changements |
|---------|------|-------------|
| 1.0.0 | 2026-11-22 | Task 113 — import aux normes skill-creator : frontmatter écosystème (semver, category, language, tags, read_when triptyque), §0 Contexte Système, corps français ; original anglais archivé byte-identité references/plateforme-original.md (R4) |
