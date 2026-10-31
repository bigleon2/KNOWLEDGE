---
name: traduction-zh-fr
version: 1.1.0
category: ecosystem
language: fr
tags:
  - traduction
  - chinois
  - francais
  - localisation
  - pdf
  - markdown
description: >
  Agent spécialisé dans la traduction du chinois vers le français, intégré à
  l'écosystème (directive propriétaire 2026-11-01). Deux moteurs complémentaires :
  (1) PDFMathTranslate (pdf2zh, 38,1 k étoiles GitHub, EMNLP 2025, AGPL-3.0) —
  application open source de référence pour la traduction de PDF avec préservation
  de la mise en page, installée en local (pip) ; successeur pdf2zh-next 2.0/BabelDOC
  identifié (recherche G5) ; (2) script Python stdlib traduire-md-zh-fr.py —
  traduction des fichiers .md (skills écrits en chinois) via une chaîne de backends
  (z-ai LLM glm de l'écosystème → googletrans → endpoint gtx → MyMemory), cache
  persistant anti-quota, verdict d'identité P2 (re-jeux byte-stables), garde de ratio
  CJK 8 % (segments déjà francisés conservés), débit contrôlé, politique P1/P2 du
  chantier P2 (traduire la prose, conserver les données fonctionnelles : blocs de
  code, code en ligne, URLs, valeurs API, spécimens). Cas d'usage direct : chantier
  P2 francisation (Lots 2-3). Test réel G4 : 5 skills volumineux — traductions réelles
  réussies via zai (design 4 471→689 CJK) + idempotence byte-stable ×2 passes.
dependencies:
  - skill: script-creator
    version: ">=1.0.0"
    used_at: "Conventions du script traduire-md-zh-fr.py (N3 stdlib, idempotence ×2)"
  - skill: audit-provenance
    version: ">=1.0.0"
    used_at: "Audit d'adoption de pdf2zh (G1 — rapport download/audit-provenance-pdf2zh.md)"
read_when:
  - Déclencher quand la demande concerne : traduction chinois→français, francisation, traduire un PDF chinois, traduire un fichier .md chinois
  - Déclencher si la demande mentionne : traduction-zh-fr, pdf2zh, googletrans, P2 francisation
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

# Traduction ZH→FR — agent spécialisé de l'écosystème

## §0 — Contexte Système (SHARED v1.7.16)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case | semver | #token | {{VARIABLE}} | @mon-ecosysteme/ | @historique/
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité.

## Provenance (audit-provenance — G1, 2026-11-01)

| Point | Verdict |
|---|---|
| Provenance | GitHub PDFMathTranslate/PDFMathTranslate (38,1 k étoiles, 3 199 commits, actif oct. 2026) — PyPI pdf2zh 1.9.11 |
| Licence | AGPL-3.0 — usage interne écosystème OK ; toute distribution modifiée sous forme de service réseau impose l'ouverture du code |
| Permissions | CLI pip local, aucun daemon, aucun jeton requis (backends gratuits) |
| Contenu dangereux | Aucun — entrypoints inspectés, appels réseau = backends de traduction uniquement |
| Réserves | Test réseau réel ZH→FR EN ATTENTE : l'IP de sortie du bac à sable est throttée (HTTP 429) par Google, MyMemory et Bing — validation à effectuer sur la machine du propriétaire |

## Moteur 1 — PDF chinois (pdf2zh)

```bash
pdf2zh document.pdf -lo fr        # sortie : document-mono.pdf (FR) + document-dual.pdf (bilingue)
pdf2zh document.pdf -lo fr -s bing  # backend alternatif
```

Installation : `pip install pdf2zh` (1.9.11 ; pins compatibles relevés : tencentcloud-sdk-python-tmt==3.0.1300, bitstring==4.2.3).

## Moteur 2 — fichiers .md (script stdlib traduire-md-zh-fr.py)

```bash
# Rapport sans écriture (fichiers > 20 CJK)
python3 skills/traduction-zh-fr/scripts/traduire-md-zh-fr.py --dry --fichier <fichiers.md>

# Traduction effective + journal p2-etat.json (schéma compatible chantier P2)
python3 skills/traduction-zh-fr/scripts/traduire-md-zh-fr.py --exec --fichier <fichiers.md> \
    --racine /home/z/my-project --journal KNOWLEDGE-repo/scripts/p2-etat.json

# Auto-test hors-ligne (logique prouvée sans réseau — 8/8 ×2 idempotent)
python3 skills/traduction-zh-fr/scripts/traduire-md-zh-fr.py --selftest
```

**Politique P1/P2** (héritée du chantier P2 — examen par fichier, jamais de traduction aveugle) :
- **P1 traduit** : prose, instructions, descriptions, explications ;
- **P2 conservé** : blocs de code, code en ligne, URLs, valeurs API, spécimens chinois, vocabulaire de référentiel, frontmatter YAML (structure).

**Architecture du script (v1.1.0)** : chaîne de backends (`zai` CLI LLM glm de l'écosystème → `googletrans` → endpoint gtx Google → MyMemory, avec retries/backoff 2-5-12 s) ; **verdict d'identité** du LLM de confiance (segment inchangé = rien à traduire/P2 → conservé sans échec) ; **garde de ratio CJK 8 %** (segment déjà francisé → conservé sans appel) ; cache persistant JSON (clé sha256 segment — anti-quota, idempotence byte-stable ×2) ; fusion de segments ≤ 3 000 car/requête ; masquage URLs/inline-code/balises avant traduction (jetons \u2063N\u2063) et restauration après ; seuil CJK 20 par fichier (fichier déjà traduit sauté) ; journal append-only compatible `p2-etat.json`.

**Constat d'époque (2026-11-01, après test réel G4)** : backend `zai` OPÉRATIONNEL (traductions réelles réussies — design chinese-typography 4 471→689 CJK en 4 requêtes ; keywords 412→0 ; fortune 694→291 ; verdicts P2 corrects sur jd/gaokao) ; idempotence byte-stable prouvée (passage 3 : 0 requête, sha256 identiques) ; `googletrans` 4.0.2 dysfonctionnel (détecté par la garde) ; endpoints gtx/mymemory/Bing throttlés 429 depuis le bac à sable (repli fonctionnel) ; `--selftest` (8/8 ×2) ; preuves complètes : download/test-traduction-5-skills-rapport.md.

## Optimisations v1.1.0 (recherche G5 — 2026-11-01)

Sources : download/recherche-alternatives-traduction-zh-fr.md.

| Option | Verdict | Action |
|---|---|---|
| LLM écosystème (z-ai chat, glm-4-plus) | **retenu** — qualité > MT pur (LionBridge/LLM study), sans 429 | backend `zai` en tête de chaîne (implémenté) |
| pdf2zh-next 2.0 (BabelDOC) | successeur officiel de pdf2zh 1.9 — WebUI, + de services | upgrade PDF recommandé (machine propriétaire) |
| Argos Translate (Apache, hors-ligne, pivot ZH→EN→FR natif) | retenu pour la machine propriétaire (bac à sable : disque insuffisant pour torch) | recommandation hors-ligne |
| Hunyuan-MT-7B (Tencent, WMT2025 : 1er sur 30/31 langues) | référence qualité ; 7B = GPU requis | veille (machine propriétaire GPU) |
| NLLB-200 / OPUS-MT (Helsinki) | pivot ZH→EN→FR viable (opus-mt-zh-en, opus-mt-en-fr) | documenté (licence NLLB = CC-BY-NC : usage interne OK) |

## Relations

| Avec | Nature |
|---|---|
| gen-plan | Cas d'usage direct du chantier P2 francisation (Lots 2-3) — routing §1.16 : découverte par skill-finder-cn (ClawHub) puis sonde web GitHub |
| correct-work | Contrôle CIBLE post-traduction (comptage CJK, sha256, statuts journal) |
| knowledge-observer | Journal p2-etat.json enrichi de la clé `traduction-zh-fr` |
