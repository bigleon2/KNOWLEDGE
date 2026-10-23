#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.12)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

# -*- coding: utf-8 -*-
"""Task 48 — G3/S3 : régénération des projections skills/iphone17|18|19/SKILL.md depuis les
PMs @photos bumpés 1944 (mécanique task45c : frontmatter + §0 Contexte Système + lignage +
corps PM VERBATIM). Versions : 17 v1.1.0 (PM v2.1), 18 v1.1.0 (PM v1.1), 19 v0.11.0 (PM v0.11.0).
Idempotent par reconstruction. Écrit dépôt + profil (byte-identiques)."""
from pathlib import Path

HOST = Path("/home/z/my-project")
REPO = HOST / "tmp" / "KNOWLEDGE-repo"
CTX = """## §0 — Contexte Système (SHARED v1.7.7)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.
"""

DEPS = """dependencies:
  - skill: skill-creator
    version: ">=1.0.0"
    used_at: "conventions structurelles (frontmatter, evals)"
  - skill: VLM
    version: ">=1.0.0"
    used_at: "analyse §1 (vision) + QC §5 comparatif original↔sortie"
  - skill: image-edit
    version: ">=1.0.0"
    used_at: "exécution §4 P1-P7 — contournement SDK base64 scripts/editer-image.mjs (CLI z-ai erreur 1210)"
"""

ADD_1944 = "restauration de photos anciennes (scans, tirages, photographies argentiques N&B années 1930-1950 — grain préservé, aucune colorisation inventée)"

FM17 = f"""---
name: iphone17
version: 1.1.0
category: metier
language: fr
tags:
  - "#photo"
  - "#amelioration-photo"
  - "#iphone17-pro-max"
  - "#preset-iphone17-max"
  - "#r17-focales-equivalentes"
  - "#restauration-argentique-1944"
  - "#mode-serie"
description: >
  Pipeline d'amélioration photo « iPhone 17 Pro Max, qualité max » (CPE — Computational
  Photo Engine) — PÉRIMÈTRE D'ÉPOQUE (génération 17, supersédée par le skill iphone18
  depuis l'activation de la règle §6.10 du PM source : keynote Apple 9/9/2026 — le
  pipeline reste opérationnel pour un rendu génération 17 demandé explicitement).
  Analyse complète par grille ANALYSE-v2 (A1-A10, B1-B6 dont inventaire B6 verrouillé,
  C1-C3), moteur de décision R1-R17 (R17 : focales équivalentes 13-200 mm — sans R18 :
  l'ouverture est celle de l'appareil source), plan d'actions YAML affiché AVANT toute
  exécution, pipeline P0-P8 dans l'ordre strict, contrôle qualité 11 critères avec
  itération contrôlée (max 2), presets de rendu §6 (défaut iphone17_max — ancrage
  A19 Pro / Photonic Engine nouvelle génération), rendus d'époque (années 40 → 2010),
  {ADD_1944}, mode poster/print A4 300 DPI, mode série
  multi-sorties, rapport final en français + question utilisateur obligatoire.
  Garde-fous photo G1-G7 : fidélité stricte des visages, zéro élément ajouté, original
  non-destructif. Pensez à utiliser ce skill dès que l'utilisateur demande
  explicitement le rendu « iPhone 17 Pro Max », le preset iphone17_max, ou la
  restauration d'une photographie ancienne (argentique N&B, ex. 1944) au rendu 17.
{DEPS}read_when:
  - Déclencher quand la demande concerne : rendu « iPhone 17 Pro Max qualité max » demandé explicitement, preset iphone17_max, focale équivalente 13-200 mm, rendu d'époque génération 17, restauration (dont photographies argentiques N&B années 1930-1950 — ex. 1944), poster/print, mode série
  - Déclencher si la demande mentionne : iphone17, preset iphone17_max, focale équivalente, CPE génération 17, photo de 1944
  - Ne pas déclencher pour : périmètre iPhone 18 (→ skill iphone18 — génération courante), dessin technique coté (→ dessin-technique), génération d'image sans photo source (→ image-generation), vidéo (hors périmètre)
---
"""

FM18 = f"""---
name: iphone18
version: 1.1.0
category: metier
language: fr
tags:
  - "#photo"
  - "#amelioration-photo"
  - "#iphone18-pro-max"
  - "#preset-iphone18-max"
  - "#r18-ouverture-variable"
  - "#restauration-argentique-1944"
  - "#mode-serie"
description: >
  Pipeline d'amélioration photo « iPhone 18 Pro Max, qualité max » (CPE — Computational
  Photo Engine) : analyse complète par grille ANALYSE-v2 (A1-A10, B1-B6 dont inventaire
  B6 verrouillé, C1-C3), moteur de décision R1-R18 (R18 : ouverture variable simulée
  ƒ/1.48-ƒ/4.0), plan d'actions YAML affiché AVANT toute exécution, pipeline P0-P8 dans
  l'ordre strict, contrôle qualité 12 critères avec itération contrôlée (max 2), presets
  de rendu §6 (défaut iphone18_max — ancrage A20 Pro / Dual Neural Engine 32 cœurs),
  rendus d'époque (années 40 → 2010), {ADD_1944},
  mode poster/print A4 300 DPI, mode série multi-sorties, rapport final en français +
  question utilisateur obligatoire. Garde-fous photo G1-G7 : fidélité stricte des
  visages (expressions, orientation des têtes), zéro élément ajouté, original
  non-destructif. Pensez à utiliser ce skill dès que l'utilisateur veut améliorer,
  retoucher ou restaurer une photo (y compris photographies anciennes N&B, ex. 1944),
  demande le preset iphone18_max, une ouverture ƒ/…, un rendu d'époque ou un poster —
  même sans mentionner « iPhone ».
{DEPS}read_when:
  - Déclencher quand la demande concerne : améliorer/retoucher/restaurer une photo (y compris photographies argentiques N&B années 1930-1950, ex. 1944), rendu « iPhone 18 Pro Max qualité max », preset iphone18_max, ouverture variable ƒ/1.48-ƒ/4.0, rendus d'époque, poster/print A4 300 DPI, mode série multi-photos
  - Déclencher si la demande mentionne : iphone18, photo qualité max, CPE, preset photo, ouverture ƒ, photo de 1944 à améliorer/restaurer, photo de concert/fête/famille à améliorer
  - Ne pas déclencher pour : périmètre iPhone 17 (→ skill iphone17), dessin technique coté (→ dessin-technique), génération d'image sans photo source (→ image-generation), vidéo (hors périmètre)
---
"""

FM19 = f"""---
name: iphone19
version: 0.11.0
category: metier
language: fr
tags:
  - "#photo"
  - "#amelioration-photo"
  - "#iphone19-pro-max"
  - "#preset-iphone19-max"
  - "#generation-anticipee-2027"
  - "#r19-pixel-binning"
  - "#restauration-argentique-1944"
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
  d'époque (années 40 → 2010), {ADD_1944},
  mode poster/print A4 300 DPI, mode série multi-sorties, rapport final en français +
  question utilisateur obligatoire. Garde-fous photo G1-G7 : fidélité stricte des visages
  (expressions, orientation des têtes), zéro élément ajouté, original non-destructif.
  Pensez à utiliser ce skill dès que l'utilisateur demande explicitement le rendu
  « iPhone 19 » ou la génération suivante, le preset iphone19_max, l'émulation pixel
  binning (R19), ou la restauration d'une photographie ancienne (argentique N&B,
  ex. 1944) au rendu 19 — pour la génération CONFIRMÉE courante (iPhone 18), préférer
  le skill iphone18.
{DEPS}read_when:
  - Déclencher quand la demande concerne : rendu « iPhone 19 Pro Max qualité max » (génération ANTICIPÉE 2027), preset iphone19_max, traitement « génération suivante » demandé explicitement, émulation pixel binning (R19), restauration (dont photographies argentiques N&B années 1930-1950 — ex. 1944)
  - Déclencher si la demande mentionne : iphone19, preset iphone19_max, génération suivante iPhone, pixel binning, photo de 1944
  - Ne pas déclencher pour : génération CONFIRMÉE courante iPhone 18 (→ skill iphone18), périmètre iPhone 17 (→ skill iphone17), dessin technique coté (→ dessin-technique), génération d'image sans photo source (→ image-generation), vidéo (hors périmètre)
---
"""

LIGN = {
    "iphone17": "> Skill métier projeté depuis le prompt maître `skills/@photos/iphone17-photos.md` **v2.1** (génération 17 — ARCHIVÉE au plan générationnel, supersédée par iphone18 [règle §6.10 activée, keynote 9/9/2026] ; le pipeline reste opérationnel pour un rendu génération 17 demandé explicitement ; v2.1 : extension 1944 — chemin argentique N&B années 1930-1950, grain préservé, aucune colorisation inventée ; v2.0 archivée @historique/photos/) — fichier du dépôt, **byte-identique, jamais édité (R2)**. Le corps ci-dessous (« ## PROMPT MAÎTRE » → §13) est repris **VERBATIM** de cette source ; dans ce skill, « le document » y désigne le présent SKILL.md, et la discipline §11 (auto-audit) s'exécute à l'occasion d'un bump de version du skill (semver + recalibrage du registre KB). Tests empiriques de référence : PA-TEST-003 (2 photos — sortie 1 QC 11/11) + PA-TEST-004 (nouvelle tentative « les potos » — QC arbitré haute confiance, zéro retouche). P8b (recadrage) : le PM source référence `crop_utils.py` (livrable historique du projet CLUB, non embarqué — un recadrage PIL équivalent est produit à la demande).",
    "iphone18": "> Skill métier projeté depuis le prompt maître `skills/@photos/iphone18-photos.md` **v1.1** (COURANT — génération iPhone 18 CONFIRMÉE ; v1.1 : extension 1944 — chemin argentique N&B années 1930-1950, grain préservé, aucune colorisation inventée ; v1.0 archivée @historique/photos/) — fichier du dépôt, **byte-identique, jamais édité (R2)**. Le corps ci-dessous (« ## PROMPT MAÎTRE » → §13) est repris **VERBATIM** de cette source ; dans ce skill, « le document » y désigne le présent SKILL.md, et la discipline §11 (auto-audit) s'exécute à l'occasion d'un bump de version du skill (semver + recalibrage du registre KB). Tests empiriques de référence : PA-TEST-001 (Task 42, QC 12/12 PASS, validation propriétaire §9 sans réserve) + PA-TEST-002 (2 photos, QC 12/12 ×2, R18 validée). P8b (recadrage) : le PM source référence `crop_utils.py` (livrable historique du projet CLUB, non embarqué — un recadrage PIL équivalent est produit à la demande).",
    "iphone19": "> Skill métier projeté depuis le prompt maître `skills/@photos/iphone19-photos.md` **v0.11.0 [ANTICIPÉE]** (génération iPhone 19 ANTICIPÉE 2027 — calibration extrapolée de rumeurs crédibles 2026, non confirmée ; v0.10.0 : émulation pixel binning R19 — capteur 200 MP Sony Lytia 901, fusion 16-en-1 → 12,5 MP, [RUMEUR] Digital Chat Station via Frandroid 27/03/2026, directive propriétaire 2026-10-21 ; v0.11.0 : extension 1944 — chemin argentique N&B années 1930-1950, grain préservé, aucune colorisation inventée ; v0.9.0 et v0.10.0 archivées @historique/photos/ ; PM génération 18 confirmée : `iphone18-photos.md` v1.1, PM parallèle) — fichier du dépôt, **byte-identique, jamais édité (R2)**. Le corps ci-dessous (« ## PROMPT MAÎTRE » → §13) est repris **VERBATIM** de cette source ; dans ce skill, « le document » y désigne le présent SKILL.md, et la discipline §11 (auto-audit) s'exécute à l'occasion d'un bump de version du skill (semver + recalibrage du registre KB). Tests empiriques de référence : PA-TEST-005 (Task 47, 2 photos, zéro retouche) + PA-TEST-006 (Task 48, rendu 19 v0.10.0 « les potos », QC 13/13, zéro itération). P8b (recadrage) : le PM source référence `crop_utils.py` (livrable historique du projet CLUB, non embarqué — un recadrage PIL équivalent est produit à la demande).",
}

SPECS = [
    ("iphone17", FM17, "iphone17-photos.md", "2.1"),
    ("iphone18", FM18, "iphone18-photos.md", "1.1"),
    ("iphone19", FM19, "iphone19-photos.md", "0.11.0"),
]

for name, fm, pmfile, ver in SPECS:
    pm = (REPO / "skills" / "@photos" / pmfile).read_text(encoding="utf-8")
    assert f"Version {ver}" in pm[:400], f"version PM inattendue pour {name}"
    assert "Note années 1940" in pm and "| **40s** |" in pm, f"extension 1944 absente de {name}"
    body = pm[pm.index("## PROMPT MAÎTRE — Pipeline"):]
    skill = fm + "\n" + CTX + "\n## Lignage — projection skill ← prompt maître source\n\n" + LIGN[name] + "\n\n" + body
    for dst in [REPO / "skills" / name / "SKILL.md", HOST / "skills" / name / "SKILL.md"]:
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(skill, encoding="utf-8")
    print(f"écrit : skills/{name}/SKILL.md ({len(skill.splitlines())} lignes, PM {pmfile} v{ver})")

print("OK — 3 projections régénérées (dépôt + profil).")
