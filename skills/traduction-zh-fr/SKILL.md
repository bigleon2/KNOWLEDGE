---
name: traduction-zh-fr
version: 1.0.0
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
  de la mise en page, installée en local (pip) ; (2) script Python stdlib
  traduire-md-zh-fr.py — traduction des fichiers .md (skills écrits en chinois)
  via une chaîne de backends gratuits (googletrans → endpoint gtx → MyMemory),
  cache persistant anti-quota, débit contrôlé ≤ 4 req/s, politique P1/P2 du
  chantier P2 (traduire la prose, conserver les données fonctionnelles : blocs de
  code, code en ligne, URLs, valeurs API, spécimens). Cas d'usage direct : chantier
  P2 francisation (Lots 2-3, ~31 000 CJK restants).
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

**Architecture du script** : chaîne de backends gratuits (`googletrans` → endpoint gtx Google → MyMemory, avec retries/backoff 2-5-12 s) ; cache persistant JSON (clé sha256 segment — anti-quota, idempotence ×2) ; fusion de segments ≤ 3 000 car/requête ; masquage URLs/inline-code/balises avant traduction (jetons \u2063N\u2063) et restauration après ; seuil CJK 20 (fichier déjà traduit sauté) ; journal append-only compatible `p2-etat.json`.

**Constat d'époque (2026-11-01)** : le paquet `googletrans` 4.0.2 est dysfonctionnel (texte source renvoyé inchangé — le script le détecte et bascule) ; les endpoints gratuits répondent 429 depuis le bac à sable (IP partagée) — le script est fonctionnel sur une IP normale (machine du propriétaire) ; `--selftest` (8/8 ×2) prouve la cohérence du traitement hors-ligne.

## Relations

| Avec | Nature |
|---|---|
| gen-plan | Cas d'usage direct du chantier P2 francisation (Lots 2-3) — routing §1.16 : découverte par skill-finder-cn (ClawHub) puis sonde web GitHub |
| correct-work | Contrôle CIBLE post-traduction (comptage CJK, sha256, statuts journal) |
| knowledge-observer | Journal p2-etat.json enrichi de la clé `traduction-zh-fr` |
