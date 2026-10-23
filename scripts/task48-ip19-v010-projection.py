#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.9)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

# -*- coding: utf-8 -*-
"""Task 48 — G1/S1 : régénération de la projection skills/iphone19/SKILL.md depuis le PM
@photos/iphone19-photos.md v0.10.0 (mécanique task45c : frontmatter 6 champs + §0 Contexte
Système N2 + note de lignage + corps PM VERBATIM de « ## PROMPT MAÎTRE » à EOF).
Idempotent par reconstruction. Écrit dépôt + profil (byte-identiques)."""
from pathlib import Path

HOST = Path("/home/z/my-project")
REPO = HOST / "tmp" / "KNOWLEDGE-repo"
PM = REPO / "skills" / "@photos" / "iphone19-photos.md"

FRONTMATTER = """---
name: iphone19
version: 0.10.0
category: metier
language: fr
tags:
  - "#photo"
  - "#amelioration-photo"
  - "#iphone19-pro-max"
  - "#preset-iphone19-max"
  - "#generation-anticipee-2027"
  - "#r19-pixel-binning"
  - "#mode-serie"
description: >
  Pipeline d'amélioration photo « iPhone 19 Pro Max, qualité max » (CPE — Computational
  Photo Engine) — génération ANTICIPÉE 2027 (calibration extrapolée des rumeurs crédibles
  2026 : A21 Pro, Photonic Engine NG+, capteur 200 MP Sony Lytia 901 à pixel binning
  16-en-1 — aucune spécification confirmée, bump v1.0.0 prévu à la confirmation officielle
  Apple). Analyse complète par grille ANALYSE-v2 (A1-A10, B1-B6 dont inventaire B6
  verrouillé, C1-C3), moteur de décision R1-R19 (R18 : ouverture variable simulée
  ƒ/1.48-ƒ/4.0 ; R19 : émulation pixel binning 16-en-1 — capteur 200 MP, fusion 16 pixels
  en 1, sortie 12,5 MP équivalente, gains SNR/lumière/crop-zoom), plan d'actions YAML
  affiché AVANT toute exécution, pipeline P0-P8 dans l'ordre strict, contrôle qualité
  13 critères avec itération contrôlée (max 2), presets de rendu §6 (défaut iphone19_max —
  ancrage ANTICIPÉ A21 Pro [RUMEUR] / extrapolation de la baseline confirmée 18), rendus
  d'époque (années 70 → 2010), restauration de photos anciennes (scans, tirages), mode
  poster/print A4 300 DPI, mode série multi-sorties, rapport final en français + question
  utilisateur obligatoire. Garde-fous photo G1-G7 : fidélité stricte des visages
  (expressions, orientation des têtes), zéro élément ajouté, original non-destructif.
  Pensez à utiliser ce skill dès que l'utilisateur demande explicitement le rendu
  « iPhone 19 » ou la génération suivante, ou le preset iphone19_max — pour la génération
  CONFIRMÉE courante (iPhone 18), préférer le skill iphone18.
dependencies:
  - skill: skill-creator
    version: ">=1.0.0"
    used_at: "conventions structurelles (frontmatter, evals)"
  - skill: VLM
    version: ">=1.0.0"
    used_at: "analyse §1 (vision) + QC §5 comparatif original↔sortie"
  - skill: image-edit
    version: ">=1.0.0"
    used_at: "exécution §4 P1-P7 — contournement SDK base64 scripts/editer-image.mjs (CLI z-ai erreur 1210)"
read_when:
  - Déclencher quand la demande concerne : rendu « iPhone 19 Pro Max qualité max » (génération ANTICIPÉE 2027), preset iphone19_max, traitement « génération suivante » demandé explicitement, émulation pixel binning (R19)
  - Déclencher si la demande mentionne : iphone19, preset iphone19_max, génération suivante iPhone, pixel binning
  - Ne pas déclencher pour : génération CONFIRMÉE courante iPhone 18 (→ skill iphone18), périmètre iPhone 17 (→ skill iphone17), dessin technique coté (→ dessin-technique), génération d'image sans photo source (→ image-generation), vidéo (hors périmètre)
---
"""

CTX = """## §0 — Contexte Système (SHARED v1.7.7)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.
"""

LIGNAGE = """## Lignage — projection skill ← prompt maître source

> Skill métier projeté depuis le prompt maître `skills/@photos/iphone19-photos.md` **v0.10.0 [ANTICIPÉE]** (génération iPhone 19 ANTICIPÉE 2027 — calibration extrapolée de rumeurs crédibles 2026, non confirmée ; v0.10.0 : **émulation pixel binning R19** — capteur 200 MP Sony Lytia 901, fusion 16-en-1 → sortie 12,5 MP, [RUMEUR] Digital Chat Station via Frandroid 27/03/2026, directive propriétaire 2026-10-21 ; PM génération 18 confirmée : `iphone18-photos.md` v1.0, PM parallèle) — fichier du dépôt, **byte-identique, jamais édité (R2)**. Le corps ci-dessous (« ## PROMPT MAÎTRE » → §13) est repris **VERBATIM** de cette source ; dans ce skill, « le document » y désigne le présent SKILL.md, et la discipline §11 (auto-audit) s'exécute à l'occasion d'un bump de version du skill (semver + recalibrage du registre KB). Test empirique de référence : PA-TEST-005 (Task 47, campagne série 2 photos — fidélité maximale, zéro retouche demandée par le propriétaire). P8b (recadrage) : le PM source référence `crop_utils.py` (livrable historique du projet CLUB, non embarqué — un recadrage PIL équivalent est produit à la demande).
"""

pm = PM.read_text(encoding="utf-8")
idx = pm.index("## PROMPT MAÎTRE")
body = pm[idx:]
assert "Version 0.10.0" in body[:400], "version PM inattendue"
assert "**R19**" in body and "13. **Émulation pixel binning respectée" in body, "R19/QC13 absents du PM"

skill = FRONTMATTER + "\n" + CTX + "\n" + LIGNAGE + "\n" + body
for dst in [REPO / "skills" / "iphone19" / "SKILL.md", HOST / "skills" / "iphone19" / "SKILL.md"]:
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(skill, encoding="utf-8")
    print(f"écrit : {dst} ({len(skill.splitlines())} lignes)")

# Cohérence evals : description du pipeline R1-R18 → R1-R19
ev = REPO / "skills" / "iphone19" / "evals" / "evals.json"
t = ev.read_text(encoding="utf-8")
n = t.count("moteur R1-R18")
t = t.replace("moteur R1-R18", "moteur R1-R19")
ev.write_text(t, encoding="utf-8")
(HOST / "skills" / "iphone19" / "evals" / "evals.json").write_text(t, encoding="utf-8")
print(f"evals.json : {n} occurrence(s) « moteur R1-R18 » → R1-R19 (dépôt + profil)")
print("OK — projection v0.10.0 régénérée.")
