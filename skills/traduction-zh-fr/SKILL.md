---
name: traduction-zh-fr
version: 1.3.1
category: ecosystem
language: fr
tags:
  - traduction
  - chinois
  - francais
  - localisation
  - pdf
  - markdown
  - anglais
  - documentation
  - referentiel
description: >
  Agent spécialisé dans la traduction du chinois vers le français, intégré à
  l'écosystème (directive propriétaire 2026-11-01). Deux moteurs complémentaires :
  (1) PDF — pdf2zh-next 2.9.0/BabelDOC (successeur officiel de pdf2zh 1.9.11,
  rapport G5 — installé en local pip, v1.3.0) piloté par traduire-pdf-zh-fr.py,
  avec adaptateur TraducteurZai câblant le LLM glm de l'écosystème dans le
  pipeline BabelDOC (moteurs gratuits Google/Bing throttlés — constat D703) ;
  (2) fichiers .md — script Python stdlib traduire-md-zh-fr.py via une chaîne de
  5 backends (z-ai LLM glm → Argos Translate hors-ligne [v1.3.0 — pivot
  ZH→EN→FR intégré, zéro quota, détection dynamique] → googletrans → endpoint
  gtx → MyMemory), cache persistant anti-quota, verdict d'identité P2 (re-jeux
  byte-stables), garde de ratio CJK 8 %, politique P1/P2 du chantier P2.
  v1.2.0 : glossaire FR (--glossaire — terminologie fixée garantie), export TMX
  1.4b (--tmx), axes explicites --src/--dest (ZH→FR défaut, ZH→EN, EN→FR).
  Tests réels : G4 (5 skills volumineux), G10 (v1.2), G13 (v1.3 — 5 skills +
  idempotence ×2 + PDF D703 clos). Cas d'usage direct : chantier P2 francisation
  (Lots 2-3).
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

## §0 — Contexte Système (SHARED v1.7.31)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.
> Langue : FRANÇAIS exclusif pour tous les échanges avec le propriétaire (règle d'or n°6 gen-plan — directive 2026-10-31, renforcée 2026-11-06) : dès le PREMIER mot de toute session ou reprise, la langue d'un message, d'un résumé de continuation ou d'un canal ne dérive JAMAIS la réponse ; toute dérive est corrigée immédiatement.
> Règles d'or & lecture SHARED à l'exécution (directive propriétaire 2026-11-06 — SHARED §9) : tout skill/agent/script exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or de l'écosystème (résumé §9 — canonique gen-plan §1.5).
> Référence canonique skill/agent (directive propriétaire 2026-11-07 — SHARED §0/§1.2) : toute référence à « mon skill X »/« mon agent X » désigne la forme installée à la racine `skills/X/SKILL.md`, JAMAIS le prompt maître du corpus `@mon-ecosysteme/` (ex-nommé `@PM-SKILLS/`) — les PMs sont des spécifications générées mécaniquement (KO-L004), les skills installés sont les formes exécutables.

## Provenance (audit-provenance — G1, 2026-11-01)

| Point | Verdict |
|---|---|
| Provenance | GitHub PDFMathTranslate/PDFMathTranslate (38,1 k étoiles, 3 199 commits, actif oct. 2026) — PyPI pdf2zh 1.9.11 |
| Licence | AGPL-3.0 — usage interne écosystème OK ; toute distribution modifiée sous forme de service réseau impose l'ouverture du code |
| Permissions | CLI pip local, aucun daemon, aucun jeton requis (backends gratuits) |
| Contenu dangereux | Aucun — entrypoints inspectés, appels réseau = backends de traduction uniquement |
| Réserves | Test réseau réel ZH→FR : CLOS en 3 temps — (1) backends gratuits Google/MyMemory/Bing throttlés depuis le bac à sable (HTTP 429) ; (2) contournement zai opérationnel (G4/G10/G13 — traductions réelles prouvées) ; (3) PDF clos en v1.3 via pdf2zh-next + adaptateur zai (D703 — download/test-traduction-v1.3-5skills-rapport.md §5) |

## Moteur 1 — PDF chinois (pdf2zh-next 2.9.0/BabelDOC — v1.3.0)

```bash
# Traduction d'un PDF chinois (sortie : <nom>.fr.mono.pdf [traduit] + <nom>.fr.dual.pdf [bilingue])
python3 skills/traduction-zh-fr/scripts/traduire-pdf-zh-fr.py --exec document.pdf --output sortie/

# Rapport sans traduction (pages, CJK, toolchain)
python3 skills/traduction-zh-fr/scripts/traduire-pdf-zh-fr.py --dry document.pdf

# Auto-test (10 contrôles — adaptateur, placeholders, toolchain)
python3 skills/traduction-zh-fr/scripts/traduire-pdf-zh-fr.py --selftest
```

Installation : `pip install pdf2zh-next` (2.9.0 ; babeldoc 0.6.2 — **pin bitstring==4.3.0** : bitstring 5.0.0 a supprimé `BitStream`, requis par babeldoc 0.6.2 ; pymupdf==1.25.2 exigé par pdf2zh-next 2.9.0) + `pip install argostranslate` + `argospm install translate-zh_en translate-en_fr`. Moteur LLM : adaptateur `TraducteurZai` (CLI `z-ai chat` — les moteurs gratuits Google/Bing de BabelDOC sont throttlés depuis la machine d'exécution, constat D703 ; le dual produit = page originale + page traduite).

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

# Auto-test hors-ligne (logique prouvée sans réseau — 24/24 ×2 idempotent)
python3 skills/traduction-zh-fr/scripts/traduire-md-zh-fr.py --selftest
```

**Politique P1/P2** (héritée du chantier P2 — examen par fichier, jamais de traduction aveugle) :
- **P1 traduit** : prose, instructions, descriptions, explications ;
- **P2 conservé** : blocs de code, code en ligne, URLs, valeurs API, spécimens chinois, vocabulaire de référentiel, frontmatter YAML (structure).

**Architecture du script (v1.3.0)** : chaîne de 5 backends (`zai` CLI LLM glm de l'écosystème → `argos` Argos Translate hors-ligne [v1.3.0 — pivot ZH→EN→FR intégré, zéro réseau, détection dynamique] → `googletrans` → endpoint gtx Google → MyMemory, avec retries/backoff 2-5-12 s) ; **verdict d'identité** du LLM de confiance (segment inchangé = rien à traduire/P2 → conservé sans échec) ; **garde de ratio CJK 8 %** (segment déjà francisé → conservé sans appel) ; cache persistant JSON (clé sha256 `src|dest|segment` — anti-quota, idempotence byte-stable ×2, entrées enrichies src/dst/langues depuis v1.2.0) ; fusion de segments ≤ 3 000 car/requête ; masquage URLs/inline-code/balises avant traduction (jetons \u2063N\u2063) et restauration après ; seuil CJK 20 par fichier (fichier déjà traduit sauté) ; journal append-only compatible `p2-etat.json` (statut TRADUIT/INCHANGÉ, axe).

**Constat d'époque (2026-11-01, après test réel G10 — v1.2.0)** : glossaire FR + export TMX + axes --src/--dest LIVRÉS et testés réellement (design chinese-typography 4 471→663 CJK en 4 requêtes + 1 équilibrage, 157 remplacements glossaire, 15/15 termes fixés vérifiés ; idempotence ×2 prouvée : P4+P5 = 0 requête réseau, sha256 byte-identiques, point fixe mécanique par marqueurs de blocs) ; TMX 1.4b exporté (8 unités zh-CN→fr, tri déterministe) ; axe EN→FR opérationnel (sonde réelle 1 requête, re-jeu no-op) ; selftest étendu 20/20 ×2 (hôte + dépôt). Preuves : download/test-traduction-v1.2-skill-rapport.md.

## Optimisations v1.1.0 (recherche G5 — 2026-11-01)

Sources : download/recherche-alternatives-traduction-zh-fr.md.

| Option | Verdict | Action |
|---|---|---|
| LLM écosystème (z-ai chat, glm-4-plus) | **retenu** — qualité > MT pur (LionBridge/LLM study), sans 429 | backend `zai` en tête de chaîne (implémenté) |
| pdf2zh-next 2.0 (BabelDOC) | successeur officiel de pdf2zh 1.9 — WebUI, + de services | **LIVRÉ v1.3.0** — moteur PDF du skill (installé + adaptateur zai + D703 clos) |
| Argos Translate (Apache, hors-ligne, pivot ZH→EN→FR natif) | retenu pour la machine propriétaire (bac à sable : disque insuffisant pour torch) | **LIVRÉ v1.3.0** — 5e backend `argos` installé + sonde réelle (l'obstruction disque d'alors est levée) |
| Hunyuan-MT-7B (Tencent, WMT2025 : 1er sur 30/31 langues) | référence qualité ; 7B = GPU requis | veille (machine propriétaire GPU) |
| NLLB-200 / OPUS-MT (Helsinki) | pivot ZH→EN→FR viable (opus-mt-zh-en, opus-mt-en-fr) | documenté (licence NLLB = CC-BY-NC : usage interne OK) |

## Améliorations v1.2.0 (candidats du rapport G5 LIVRÉS — E13 n°5, trace 1a1936e781a223a9)

| Candidat (§ Recommandations futures du rapport G5) | Option CLI | Mécanisme | Preuve mécanique |
|---|---|---|---|
| **Glossaire FR** | `--glossaire glossaire.tsv` | TSV terme source → terme FR ; **substitution visible AVANT traduction** (termes fixés en langue cible, conservés nativement par le traducteur) + **passe d'application déterministe APRÈS** (tout terme resté chinois dans la sortie est remplacé mécaniquement) — appariement le plus long d'abord ; itérations honnêtes G10 : masquage par jetons ABANDONNÉ (qualité dégradée), phrase prompt « conserve EXACTEMENT » ABANDONNÉE (refus induits) | selftest « glossaire-avant/après » (20/20) + test réel G10 (157 remplacements, 15/15 termes vérifiés) |
| **Export TMX** | `--tmx memoire.tmx` | mémoire de traduction (cache) exportée en TMX 1.4b inter-outils (tu/tuv/seg, xml:lang) ; seules les entrées complètes (src+dst+langues — enrichies depuis v1.2.0) partent ; tri déterministe par clé sha256 | selftest « tmx-valide » + « tmx-deterministe » + export réel G10 |
| **Flag `--src`/`--dest`** | `--src en --dest fr` (etc.) | axes explicites ZH→FR (défaut, clés de cache inchangées v1.1.0), ZH→EN, EN→FR — prompt système + clés de cache paramétrés ; garde « mots vides » par morceau pour sources latines (segment déjà en langue cible = conservé — idempotence des re-jeux) | selftest « axes-cles-distinctes », « axes-prompt », « axe-enfr-garde » + sonde réelle G10 (1 requête, re-jeu 0 requête) |

**Mécanismes de robustesse v1.2.0** (issus du test réel G10) : **garde anti-refus du verdict d'identité** — un segment renvoyé inchangé alors qu'il est en langue SOURCE est un refus (traité comme échec en mode glossaire / source latine ; sans glossaire, sémantique P2 v1.1.0 conservée) ; **écho-conservation 20 %** — un écho sur un segment majoritairement en langue cible (CJK < 20 %) = conservation de données P2 (les refus réels observés portent sur la prose, ratio 0,29-0,55) ; **repli paragraphes** — morceau en échec re-découpé en paragraphes individuels ; **marqueur de bloc stabilisé (point fixe)** — chaque bloc traduit est enregistré (clé sha256 contenu + axe + glossaire) : les re-jeux sont des **no-op byte-stables sans réseau, par construction** (pour forcer une re-traduction : changer le glossaire — les clés changent — ou supprimer les entrées `bloc:` du cache).

## Améliorations v1.3.0 (2 candidats restants du rapport G5 LIVRÉS — E13 n°6, trace 1a1968934958f495)

| Candidat (§ Recommandations futures du rapport G5) | Livrable | Preuve mécanique |
|---|---|---|
| **Upgrade pdf2zh → pdf2zh-next 2.9.0 (BabelDOC)** | moteur PDF du skill passé à pdf2zh-next ; script `traduire-pdf-zh-fr.py` (adaptateur `TraducteurZai` : contrat ILTranslator complet — translate + placeholders + voie LLM désactivée, verrou thread, débit, 3 tentatives) ; pin bitstring==4.3.0 | selftest 10/10 ×2 + **re-test D703 SUCCÈS** : PDF chinois réel (1 page, 68 CJK) traduit en français propre via le pipeline complet (2 appels z-ai, 0 échec) — statut EN ATTENTE CLOS |
| **Argos Translate hors-ligne** (5e backend) | backend `argos` en 2e position de chaîne (zai → argos → googletrans → gtx → mymemory) ; pip argostranslate 1.11.0 + torch 2.15.0+cpu + modèles `translate-zh_en`/`translate-en_fr` ; détection dynamique (paquet absent = sauté proprement, jamais d'échec silencieux) | selftest 24/24 ×2 (4 contrôles argos : ordre de chaîne, saut si absent, repli, enregistrement) + **sonde réelle** ZH→FR (« La disposition est l'art de la communication visuelle… ») et EN→FR via le chemin de code du script |

**Tests réels G13** (download/test-traduction-v1.3-5skills-rapport.md) : 5 skills volumineux — chinese-typography 4 471→693 CJK (4 requêtes), keywords_tech 412→0 (1 requête), fortune/jd/gaokao INCHANGÉS (verdicts P2 corrects — données fonctionnelles, garde de ratio, 0 appel) ; **idempotence ×2** (P2+P3 : 0 requête réseau, sha256 byte-identiques — point fixe) ; originaux intacts.

## Recalibrage v1.3.1 (triggers — correct-work Task 28 F-2, directive propriétaire « GO », trace 1a19749ed0a1575d)

| Défaut constaté (replay Task 28 : 6/8) | Correction | Preuve mécanique |
|---|---|---|
| Faux négatif — « Traduis la documentation chinoise du référentiel en anglais avec le même outil » (axe --src zh --dest en supporté v1.2.0, non routé : stems `chinoise`→`chinois` ≠ radical tags `chinoi`, 0-1 hit) | tags += `anglais`, `documentation`, `referentiel` (keywords_for — ≥ 2 hits) | replay arbitre V6.1 : case 5 → trigger voie-m ✓ |
| Faux positif — « Résume ce vidéo YouTube en chinois sans traduction » (2 hits : chinois + traduction) | veto négatif `exclusifs: ["sans traduction"]` sur le cas (mécanisme V6.1 Task 30 — veto AVANT scoring) | replay arbitre V6.1 : case 7 → source veto-exclusif ✓ |

Non-régression : description frontmatter inchangée (md5) ; cas négatifs 6/8 re-vérifiés au replay ×2 ; zéro changement fonctionnel des scripts (PATCH sémantique).

## Relations

| Avec | Nature |
|---|---|
| gen-plan | Cas d'usage direct du chantier P2 francisation (Lots 2-3) — routing §1.16 : découverte par skill-finder-cn (ClawHub) puis sonde web GitHub |
| correct-work | Contrôle CIBLE post-traduction (comptage CJK, sha256, statuts journal) |
| knowledge-observer | Journal p2-etat.json enrichi de la clé `traduction-zh-fr` |
