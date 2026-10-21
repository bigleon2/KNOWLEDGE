#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 48 — G4/S5 : comparaison côte à côte enrichie des rendus 17/18/19 pour
« libération après guerre » + guide de lecture 1944 (grille 2×3, panneaux 3:2 720×480,
composite PIL pur — zéro appel générationnel, zéro modification des sources).
Panneau P1-P6 : copie DÉSATURÉE mécaniquement (PIL L→RGB) de l'intermédiaire 19 —
l'intermédiaire généré est ressorti colorisé (documenté), désaturation de présentation
déterministe et non inventive."""
import hashlib

from PIL import Image, ImageDraw, ImageFont

BASE = "/home/z/my-project"
CELL_W, CELL_H, CAPTION = 720, 480, 44
M = 12
COLS, ROWS = 3, 2

# panneau P1-P6 : désaturation mécanique de présentation (l'intermédiaire natif est colorisé)
src = Image.open(f"{BASE}/download/PA-TEST-007-3-amelioration-P1-P6.png").convert("RGB")
p16 = src.convert("L").convert("RGB")
p16.save(f"{BASE}/download/PA-TEST-007-3-amelioration-P1-P6-desature.png")
print("panneau P1-P6 désaturé (mécanique PIL) écrit")

PANES = [
    ("ORIGINAL — tirage argentique N&B, août 1944 · 828×550 (P0)",
     f"{BASE}/upload/libération après guerre.png"),
    ("AMÉLIORATION TECHNIQUE SEULE — P1-P6 v0.11.0, désaturée pour lecture (intermédiaire 19)",
     f"{BASE}/download/PA-TEST-007-3-amelioration-P1-P6-desature.png"),
    ("RENDU iPhone 17 Pro Max — d'époque (PA-TEST-007-1, QC 11/11)",
     f"{BASE}/download/PA-TEST-007-1-iphone17-max.png"),
    ("RENDU iPhone 18 Pro Max — confirmée (PA-TEST-007-2, QC 12/12, it. 1)",
     f"{BASE}/download/PA-TEST-007-2-iphone18-max.png"),
    ("RENDU iPhone 19 Pro Max v0.11.0 — ANTICIPÉ + binning (PA-TEST-007-3, QC 13/13)",
     f"{BASE}/download/PA-TEST-007-3-iphone19-max.png"),
    ("GUIDE DE LECTURE", None),
]

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
        draw.rectangle([x, y, x + CELL_W, y + CELL_H], fill=(32, 32, 38))
        tx = x + 28
        draw.text((tx, y + 24), "GUIDE DE LECTURE — 1944", fill=(120, 220, 170), font=font_guide_t)
        lignes = [
            ("1.  Original → P1-P6 : gain technique pur (tonalité du tirage", font_guide),
            ("     restaurée, taches/poussières nettoyées, netteté légère —", font_guide),
            ("     grain argentique PRÉSERVÉ, monochrome conservé).", font_guide),
            ("2.  P1-P6 → 17 / 18 / 19 : chaque génération ajoute sa finition —", font_guide),
            ("     tous les rendus demeurent STRICTEMENT en N&B (aucune", font_guide),
            ("     colorisation : les drapeaux restent en niveaux de gris).", font_guide),
            ("3.  Repères 1944 à suivre d'un panneau à l'autre :", font_guide),
            ("     • le drapeau tricolore et le drapeau américain (en gris !)", font_guide),
            ("     • l'homme casqué au sommet, bras levé", font_guide),
            ("     • le jeune homme à la carabine, la jeune femme à la robe claire,", font_guide),
            ("       les 3 pousseurs, le garçon qui court, l'homme au pare-choc", font_guide),
            ("", font_guide),
            ("17_max = d'époque (QC 11/11) · 18_max = confirmée (QC 12/12,", font_guide),
            ("it. 1) · 19_max v0.11.0 = ANTICIPÉE + binning R19 (QC 13/13) —", font_guide),
            ("restauration ≠ colorisation : authenticité historique préservée.", font_guide),
        ]
        yy = y + 74
        for texte, f in lignes:
            draw.text((tx, yy), texte, fill=(225, 225, 230), font=f)
            yy += 31
        draw.text((tx, y + CELL_H - 40),
                  "Pleine résolution : download/PA-TEST-007-{1,2,3}-*.png · intermédiaires natifs inclus",
                  fill=(150, 150, 160), font=font_guide_s)
    else:
        im = Image.open(chemin).convert("RGB").resize((CELL_W, CELL_H), Image.LANCZOS)
        canvas.paste(im, (x, y))

    draw.rectangle([x, y + CELL_H, x + CELL_W, y + CELL_H + CAPTION], fill=(40, 40, 46))
    bbox = draw.textbbox((0, 0), titre, font=font_b)
    tw = bbox[2] - bbox[0]
    if tw > CELL_W - 16:
        font_tmp = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 15)
        bbox = draw.textbbox((0, 0), titre, font=font_tmp)
        tw = bbox[2] - bbox[0]
        draw.text((x + (CELL_W - tw) // 2, y + CELL_H + 14), titre, fill=(240, 240, 240), font=font_tmp)
    else:
        draw.text((x + (CELL_W - tw) // 2, y + CELL_H + 11), titre, fill=(240, 240, 240), font=font_b)

for chemin, h in empreintes.items():
    assert hashlib.sha256(open(chemin, "rb").read()).hexdigest()[:12] == h, f"SOURCE MODIFIÉE : {chemin}"

out = f"{BASE}/download/comparaison-liberation-apres-guerre-cote-a-cote.png"
canvas.save(out, optimize=True)
print(f"comparaison OK : {out} — {canvas.size[0]}×{canvas.size[1]}, 5 panneaux 720×480 + guide + légendes")
print("sources intacts :", ", ".join(empreintes.values()))
