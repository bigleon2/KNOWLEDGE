#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.12)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

# -*- coding: utf-8 -*-
"""Task 48 — G2/S2 : comparaison côte à côte enrichie des 5 versions de « les potos » + guide de
lecture (grille 2×3, composite PIL pur — zéro appel générationnel, zéro modification des sources).
Adapté à la photo originale potos : légendes B6 (cercle atypique, tête inversée, inscription)."""
import hashlib

from PIL import Image, ImageDraw, ImageFont

BASE = "/home/z/my-project"
CELL_W, CELL_H, CAPTION = 720, 540, 44
M = 12
COLS, ROWS = 3, 2

PANES = [
    ("ORIGINAL — soirée intérieure, lumière dure · 604×453 (P0)",
     f"{BASE}/upload/musikalarue - les potos.jpg"),
    ("AMÉLIORATION QUALITÉ SEULE — P1-P6 v0.10.0 + binning R19 (PA-TEST-006-1)",
     f"{BASE}/download/PA-TEST-006-1-amelioration-P1-P6.png"),
    ("RENDU iPhone 17 Pro Max — d'époque (PA-TEST-004-1, QC arbitré)",
     f"{BASE}/download/PA-TEST-004-1-iphone17-max.png"),
    ("RENDU iPhone 18 Pro Max — confirmée (PA-TEST-002-2, QC 12/12)",
     f"{BASE}/download/PA-TEST-002-2-iphone18-max.png"),
    ("RENDU iPhone 19 Pro Max v0.10.0 — ANTICIPÉ + pixel binning (PA-TEST-006-1, QC 13)",
     f"{BASE}/download/PA-TEST-006-1-iphone19-max.png"),
    ("GUIDE DE LECTURE", None),
]

# --- pré-vol : empreintes des sources (le composite est en lecture seule) ---
empreintes = {}
for _, chemin in PANES:
    if chemin:
        empreintes[chemin] = hashlib.sha256(open(chemin, "rb").read()).hexdigest()[:12]

W = M + COLS * (CELL_W + M)
H = M + ROWS * (CELL_H + CAPTION + M)
canvas = Image.new("RGB", (W, H), (24, 24, 28))
draw = ImageDraw.Draw(canvas)
font_b = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 19)
font_guide_t = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 26)
font_guide = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 19)
font_guide_s = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)

for i, (titre, chemin) in enumerate(PANES):
    r, c = divmod(i, COLS)
    x = M + c * (CELL_W + M)
    y = M + r * (CELL_H + CAPTION + M)

    if chemin is None:
        # ---- panneau guide de lecture (adapté aux potos) ----
        draw.rectangle([x, y, x + CELL_W, y + CELL_H], fill=(32, 32, 38))
        tx = x + 28
        draw.text((tx, y + 24), "GUIDE DE LECTURE — « les potos »", fill=(120, 220, 170), font=font_guide_t)
        lignes = [
            ("1.  Original → P1-P6 : gain technique pur (exposition +0,7 EV,", font_guide),
            ("     débruitage, déblocage JPEG, netteté ×1,9, binning R19 — aucun style).", font_guide),
            ("2.  P1-P6 → 17 / 18 / 19 : chaque génération ajoute son traitement", font_guide),
            ("     soirée Apple — 17 d'époque → 18 confirmée → 19 anticipée + binning.", font_guide),
            ("3.  Repères potos à suivre d'un panneau à l'autre :", font_guide),
            ("     • la tête INVERSÉE au centre (sourire large, anneau au septum)", font_guide),
            ("     • le chevauchement de visages/cheveux (conservé tel quel)", font_guide),
            ("     • la casquette noire à l'envers, les 3 piercings,", font_guide),
            ("       l'inscription rose/violette du t-shirt gris (haut gauche)", font_guide),
            ("", font_guide),
            ("17_max = périmètre d'époque (QC arbitré)   ·   18_max = génération", font_guide),
            ("confirmée, calibrée labo (QC 12/12)   ·   19_max v0.10.0 = ANTICIPÉE", font_guide),
            ("2027 + émulation pixel binning R19 16-en-1 (QC 13/13) — v1.0 à la", font_guide),
            ("confirmation officielle Apple (keynote attendu sept. 2027).", font_guide),
        ]
        yy = y + 78
        for texte, f in lignes:
            draw.text((tx, yy), texte, fill=(225, 225, 230), font=f)
            yy += 31
        draw.text((tx, y + CELL_H - 40),
                  "Pleine résolution : download/PA-TEST-00{2,4,6}-*-*.png · rendu 19 v0.9.0 dispo (PA-TEST-005-2)",
                  fill=(150, 150, 160), font=font_guide_s)
    else:
        im = Image.open(chemin).convert("RGB").resize((CELL_W, CELL_H), Image.LANCZOS)
        canvas.paste(im, (x, y))

    # bandeau légende sous la cellule
    draw.rectangle([x, y + CELL_H, x + CELL_W, y + CELL_H + CAPTION], fill=(40, 40, 46))
    bbox = draw.textbbox((0, 0), titre, font=font_b)
    tw = bbox[2] - bbox[0]
    if tw > CELL_W - 16:  # légende trop longue → police réduite
        font_tmp = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
        bbox = draw.textbbox((0, 0), titre, font=font_tmp)
        tw = bbox[2] - bbox[0]
        draw.text((x + (CELL_W - tw) // 2, y + CELL_H + 13), titre, fill=(240, 240, 240), font=font_tmp)
    else:
        draw.text((x + (CELL_W - tw) // 2, y + CELL_H + 11), titre, fill=(240, 240, 240), font=font_b)

# --- post-vérification : sources inchangées ---
for chemin, h in empreintes.items():
    assert hashlib.sha256(open(chemin, "rb").read()).hexdigest()[:12] == h, f"SOURCE MODIFIÉE : {chemin}"

out = f"{BASE}/download/comparaison-les-potos-cote-a-cote-5-versions.png"
canvas.save(out, optimize=True)
print(f"comparaison OK : {out} — {canvas.size[0]}×{canvas.size[1]}, 5 panneaux 720×540 + guide + légendes")
print("sources intacts :", ", ".join(f"{h}" for h in empreintes.values()))
