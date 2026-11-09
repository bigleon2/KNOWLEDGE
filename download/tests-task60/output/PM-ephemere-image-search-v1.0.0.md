# PROMPT MAÎTRE ÉPHÉMÈRE — image-search v1.0.0

> **Skill source** : `skills/image-search/SKILL.md` (forme installée — référence canonique)
> **Version source** : 1.0.0 · **Généré le** : 2026-11-07
> **SHA-256 source** : `c74da9d8ffbdfe9419d2aadf54d704396b5bb15aa6fcadf65224ee2d99f08fbd`
> **Nature** : projection éphémère auto-portante — le Contexte Système est embarqué,
> **aucune lecture externe n'est requise** (SHARED §6.2). Régénérable à volonté :
> `PM-skill(image-search)` reproduit ce fichier à l'identique (déterminisme même jour).

## MODE D'EMPLOI — IA EXTERNE

1. Copier l'intégralité du présent fichier.
2. Le coller comme **prompt système** (ou premier message) dans l'IA de votre choix.
3. Invoquer le skill par ses déclencheurs (section dédiée ci-dessous).
   Le contenu ci-dessous est la spécification exécutable du skill, auto-contenue.

## MISSION — description du skill (frontmatter source, verbatim)

(description absente du frontmatter source — voir spécification ci-dessous)

---


## §0 — Contexte Système (SHARED v1.7.27)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.
> Langue : FRANÇAIS exclusif pour tous les échanges avec le propriétaire (règle d'or n°6 gen-plan — directive 2026-10-31, renforcée 2026-11-06) : dès le PREMIER mot de toute session ou reprise, la langue d'un message, d'un résumé de continuation ou d'un canal ne dérive JAMAIS la réponse ; toute dérive est corrigée immédiatement.
> Règles d'or & lecture SHARED à l'exécution (directive propriétaire 2026-11-06 — SHARED §9) : tout skill/agent/script exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or de l'écosystème (résumé §9 — canonique gen-plan §1.5).
> Référence canonique skill/agent (directive propriétaire 2026-11-07 — SHARED §0/§1.2) : toute référence à « mon skill X »/« mon agent X » désigne la forme installée à la racine `skills/X/SKILL.md`, JAMAIS le prompt maître du corpus `@mon-ecosysteme/` (ex-nommé `@PM-SKILLS/`) — les PMs sont des spécifications générées mécaniquement (KO-L004), les skills installés sont les formes exécutables.



# image-search (ZAI in-house, via z-ai SDK)

Searches public web images for a natural-language query, re-hosts each hit on
OSS so the link is embeddable, and (optionally) attaches a short caption. The
backend is **ZAI's own self-developed image search service**.

You **do not call the backend directly**, and you **do not call the gateway
HTTP API directly**. Always go through the `z-ai image-search` subcommand
from the `z-ai-web-dev-sdk` CLI — that's the only supported entry point.

## When to activate

Trigger this skill when the user wants to:

- Find images for an article, slide deck, PPT, blog post, or report.
- Get reference photos / inspiration for a topic.
- Embed pictures into generated documents with stable URLs.
- Caption a set of images in Chinese or English.

Do **not** use this skill for:

- Generating new images from scratch — use `z-ai image` (image generation).
- Reverse image search ("what is this image of?").
- Searching images inside a private corpus — this hits public web sources.

## Prerequisites

**`z-ai-web-dev-sdk` installed**, providing the `z-ai` binary:

```bash
npm install -g z-ai-web-dev-sdk
# or:  bun add -g z-ai-web-dev-sdk
```

## Invocation

```bash
z-ai image-search --query "<natural-language sentence>" [flags]
```

The CLI prints the JSON response (pretty-formatted) to stdout, or writes it
to `--output <path>` if supplied.

### Flags

| Flag                | Default | Notes |
|---------------------|---------|-------|
| `--query`, `-q`     | —       | Required. Natural-language sentence describing what should be in the image. Prefer one coherent concept; avoid mixing unrelated keywords. |
| `--count`, `-c`     | 5       | Number of images to return. Range 1–20. |
| `--gl`              | `cn`    | Region code for localization. Common: `cn`, `us`, `jp`, `kr`. |
| `--no-rank`         | —       | Disable captioning for a faster, caption-less response (default is on). |
| `--output`, `-o`    | —       | Optional: write the full JSON response to this path. |
| `--help`, `-h`      | —       | Show CLI help. |

### Examples

```bash
# Default search (5 images, cn region, captions on).
z-ai image-search -q "a cute orange tabby kitten playing with yarn" --count 5

# US region, no captioning (faster).
z-ai image-search -q "vintage red sports car on a mountain road" --count 5 --gl us --no-rank

# Chinese query — captions come back in Chinese.
z-ai image-search -q "中国传统水墨山水画" --count 5 -o results.json
```

## Choosing parameters

- **`--query`**: use a descriptive sentence, not a keyword list. The service
  is tuned for natural language and returns more on-topic results that way.
  Match the language to the audience: Chinese queries produce Chinese
  captions, English queries produce English captions.
- **`--count`**: default to `5` for most asset-gathering tasks. Drop to
  `1`–`3` when the user only needs one finalist; raise toward `10`–`20`
  when building a moodboard or browsing options. Stay within `1`–`20`.
- **`--no-rank`**: turn captions off for moodboards or when latency matters;
  leave them on when the user will pick images by reading the captions.
- **One concept per call**: for two unrelated subjects, fire two separate
  invocations rather than concatenating keywords.

## Response shape

```json
{
  "success": true,
  "query": "cute orange tabby kitten",
  "count": 5,
  "ranked": true,
  "results": [
    {
      "original_url": "https://sfile.chatglm.cn/images-ppt/<hash>.png",
      "caption": "A cute orange tabby kitten playing with yarn on a rug.",
      "source": "Unsplash",
      "original_width": "750px",
      "original_height": "500px"
    }
  ]
}
```

Failure response (HTTP is still 200; check `success`):

```json
{
  "success": false,
  "query": "...",
  "count": 0,
  "ranked": true,
  "results": [],
  "error": "<human-readable reason>"
}
```

### Field reference

| Field                       | Type    | Notes |
|-----------------------------|---------|-------|
| `success`                   | boolean | Always check this before reading `results`. |
| `query`                     | string  | Echo of the input query. |
| `count`                     | integer | Number of images actually returned. |
| `ranked`                    | boolean | Whether captioning was applied. |
| `results[].original_url`    | string  | OSS-hosted direct image URL. Stable and embeddable. |
| `results[].caption`         | string  | Short caption. Present only when `ranked` is `true`. |
| `results[].source`          | string  | Original source site (e.g. `Unsplash`, `Pinterest`). |
| `results[].original_width`  | string  | Image width as `"NNNpx"`. |
| `results[].original_height` | string  | Image height as `"NNNpx"`. |
| `error`                     | string  | Present only on failure. |

## Operating tips

1. **Always present the OSS `original_url`, not the source site URL.** The
   OSS link is the one that's guaranteed reachable; source pages may be
   paywalled, geo-blocked, or deleted.
2. **Skip captioning for speed.** `--no-rank` typically cuts response time
   by more than half. Use it when you'll caption results yourself.
3. **Be patient with timeouts.** A full call can take 90 seconds or more —
   the upstream does image reachability probes, OSS upload, and captioning
   one after another. Use a client-side timeout of at least 120 seconds.
4. **Region matters.** `gl=cn` biases toward Chinese-language sources;
   `gl=us` toward English. Pick the one that matches the user's audience.

## Error handling

| Symptom | Likely cause | What to do |
|---------|--------------|------------|
| `Unknown command "image-search"` | SDK too old | Upgrade: `npm install -g z-ai-web-dev-sdk@latest`. |
| `API request failed with status 401` / `403` | Auth issue at the gateway | Tell the user — credentials are managed outside this skill. |
| `API request failed with status 502` | Upstream service unreachable | Retry; if it persists the in-house service is down. |
| Empty `results` but `success: true` | Query too narrow or upstream filtered everything | Broaden the query, raise `--count`, or change `--gl`. |

---
