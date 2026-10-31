---
name: traduction-zh-fr
version: 1.2.0
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
  v1.2.0 (candidats du rapport G5 livrés, E13 n°5) : glossaire FR (--glossaire —
  terminologie fixée garantie), export TMX 1.4b de la mémoire de traduction (--tmx),
  axes explicites --src/--dest (ZH→FR défaut, ZH→EN, EN→FR).
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

# v1.2.0 — glossaire FR (terminologie fixée garantie) + export TMX de la mémoire de traduction
python3 skills/traduction-zh-fr/scripts/traduire-md-zh-fr.py --exec --fichier <fichiers.md> \
    --glossaire glossaire.tsv --tmx memoire.tmx

# v1.2.0 — axes explicites (backend zai langue-agnostique : ZH→EN, EN→FR)
python3 skills/traduction-zh-fr/scripts/traduire-md-zh-fr.py --exec --fichier doc-en.md --src en --dest fr

# Auto-test hors-ligne (logique prouvée sans réseau — 14/14 ×2 idempotent)
python3 skills/traduction-zh-fr/scripts/traduire-md-zh-fr.py --selftest
```

**Politique P1/P2** (héritée du chantier P2 — examen par fichier, jamais de traduction aveugle) :
- **P1 traduit** : prose, instructions, descriptions, explications ;
- **P2 conservé** : blocs de code, code en ligne, URLs, valeurs API, spécimens chinois, vocabulaire de référentiel, frontmatter YAML (structure).

**Architecture du script (v1.2.0)** : chaîne de backends (`zai` CLI LLM glm de l'écosystème → `googletrans` → endpoint gtx Google → MyMemory, avec retries/backoff 2-5-12 s) ; **verdict d'identité** du LLM de confiance (segment inchangé = rien à traduire/P2 → conservé sans échec) ; **garde de ratio CJK 8 %** (segment déjà francisé → conservé sans appel) ; cache persistant JSON (clé sha256 `src|dest|segment` — anti-quota, idempotence byte-stable ×2, entrées enrichies src/dst/langues depuis v1.2.0) ; fusion de segments ≤ 3 000 car/requête ; masquage URLs/inline-code/balises avant traduction (jetons \u2063N\u2063) et restauration après ; seuil CJK 20 par fichier (fichier déjà traduit sauté) ; journal append-only compatible `p2-etat.json` (statut TRADUIT/INCHANGÉ, axe).

**Constat d'époque (2026-11-01, après test réel G10 — v1.2.0)** : glossaire FR + export TMX + axes --src/--dest LIVRÉS et testés réellement (design chinese-typography 4 471→663 CJK en 4 requêtes + 1 équilibrage, 157 remplacements glossaire, 15/15 termes fixés vérifiés ; idempotence ×2 prouvée : P4+P5 = 0 requête réseau, sha256 byte-identiques, point fixe mécanique par marqueurs de blocs) ; TMX 1.4b exporté (8 unités zh-CN→fr, tri déterministe) ; axe EN→FR opérationnel (sonde réelle 1 requête, re-jeu no-op) ; selftest étendu 20/20 ×2 (hôte + dépôt). Preuves : download/test-traduction-v1.2-skill-rapport.md.

## Optimisations v1.1.0 (recherche G5 — 2026-11-01)

Sources : download/recherche-alternatives-traduction-zh-fr.md.

| Option | Verdict | Action |
|---|---|---|
| LLM écosystème (z-ai chat, glm-4-plus) | **retenu** — qualité > MT pur (LionBridge/LLM study), sans 429 | backend `zai` en tête de chaîne (implémenté) |
| pdf2zh-next 2.0 (BabelDOC) | successeur officiel de pdf2zh 1.9 — WebUI, + de services | upgrade PDF recommandé (machine propriétaire) |
| Argos Translate (Apache, hors-ligne, pivot ZH→EN→FR natif) | retenu pour la machine propriétaire (bac à sable : disque insuffisant pour torch) | recommandation hors-ligne |
| Hunyuan-MT-7B (Tencent, WMT2025 : 1er sur 30/31 langues) | référence qualité ; 7B = GPU requis | veille (machine propriétaire GPU) |
| NLLB-200 / OPUS-MT (Helsinki) | pivot ZH→EN→FR viable (opus-mt-zh-en, opus-mt-en-fr) | documenté (licence NLLB = CC-BY-NC : usage interne OK) |

## Améliorations v1.2.0 (candidats du rapport G5 LIVRÉS — E13 n°5, trace 1a1936e781a223a9)

| Candidat (§ Recommandations futures du rapport G5) | Option CLI | Mécanisme | Preuve mécanique |
|---|---|---|---|
| **Glossaire FR** | `--glossaire glossaire.tsv` | TSV terme source → terme FR ; **substitution visible AVANT traduction** (termes fixés en langue cible, conservés nativement par le traducteur) + **passe d'application déterministe APRÈS** (tout terme resté chinois dans la sortie est remplacé mécaniquement) — appariement le plus long d'abord ; itérations honnêtes G10 : masquage par jetons ABANDONNÉ (qualité dégradée), phrase prompt « conserve EXACTEMENT » ABANDONNÉE (refus induits) | selftest « glossaire-avant/après » (20/20) + test réel G10 (157 remplacements, 15/15 termes vérifiés) |
| **Export TMX** | `--tmx memoire.tmx` | mémoire de traduction (cache) exportée en TMX 1.4b inter-outils (tu/tuv/seg, xml:lang) ; seules les entrées complètes (src+dst+langues — enrichies depuis v1.2.0) partent ; tri déterministe par clé sha256 | selftest « tmx-valide » + « tmx-deterministe » + export réel G10 |
| **Flag `--src`/`--dest`** | `--src en --dest fr` (etc.) | axes explicites ZH→FR (défaut, clés de cache inchangées v1.1.0), ZH→EN, EN→FR — prompt système + clés de cache paramétrés ; garde « mots vides » par morceau pour sources latines (segment déjà en langue cible = conservé — idempotence des re-jeux) | selftest « axes-cles-distinctes », « axes-prompt », « axe-enfr-garde » + sonde réelle G10 (1 requête, re-jeu 0 requête) |

**Mécanismes de robustesse v1.2.0** (issus du test réel G10) : **garde anti-refus du verdict d'identité** — un segment renvoyé inchangé alors qu'il est en langue SOURCE est un refus (traité comme échec en mode glossaire / source latine ; sans glossaire, sémantique P2 v1.1.0 conservée) ; **écho-conservation 20 %** — un écho sur un segment majoritairement en langue cible (CJK < 20 %) = conservation de données P2 (les refus réels observés portent sur la prose, ratio 0,29-0,55) ; **repli paragraphes** — morceau en échec re-découpé en paragraphes individuels ; **marqueur de bloc stabilisé (point fixe)** — chaque bloc traduit est enregistré (clé sha256 contenu + axe + glossaire) : les re-jeux sont des **no-op byte-stables sans réseau, par construction** (pour forcer une re-traduction : changer le glossaire — les clés changent — ou supprimer les entrées `bloc:` du cache).

## Relations

| Avec | Nature |
|---|---|
| gen-plan | Cas d'usage direct du chantier P2 francisation (Lots 2-3) — routing §1.16 : découverte par skill-finder-cn (ClawHub) puis sonde web GitHub |
| correct-work | Contrôle CIBLE post-traduction (comptage CJK, sha256, statuts journal) |
| knowledge-observer | Journal p2-etat.json enrichi de la clé `traduction-zh-fr` |
