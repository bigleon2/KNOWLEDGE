#!/usr/bin/env python3
"""Task 10 G1 — Découpe des illustrations du standard non-KPS source.

Entrée : upload/IMG_20261127_131943.jpg (2479x1723, photo du document MO-MF-013-F).
Sorties :
  - assets_tmp/task10-crops/*.png      (crops nommés, ratio préservé)
  - assets_tmp/task10-crops/contact-sheet.png (planche de contrôle visuel)
  - download/source-standard-non-KPS-MO-MF-013-F.jpg (copie d'archive — garde du standard non-KPS)
  - assets_tmp/task10-crops/rapport-crops.json (dimensions + DPI effectif à l'affichage cible)

Idempotent : ré-exécution = mêmes fichiers régénérés à l'identique.
"""
import hashlib
import json
import os
import shutil
from PIL import Image, ImageDraw, ImageFont

SRC = "/home/z/my-project/upload/IMG_20261127_131943.jpg"
OUT = "/home/z/my-project/assets_tmp/task10-crops"
ARCHIVE = "/home/z/my-project/download/source-standard-non-KPS-MO-MF-013-F.jpg"
FONT = "/usr/share/fonts/truetype/chinese/NotoSansSC-Regular.ttf"

# (nom, x0, y0, x1, y1, largeur d'affichage cible en px pour le calcul DPI)
# Coordonnées en fractions de la photo (mesurées sur la vue de contrôle).
CROPS = [
    ("cartouche-source",      0.018, 0.012, 0.985, 0.240, 660),
    ("photo1-valve-bolt",     0.020, 0.238, 0.305, 0.392, 340),
    ("outillage-visses",      0.020, 0.392, 0.305, 0.555, 340),
    ("photo5-screw-m5",       0.178, 0.422, 0.310, 0.530, 260),
    ("localisation-tank",     0.318, 0.250, 0.545, 0.552, 340),
    ("photo2-hose-clamp",     0.598, 0.262, 0.798, 0.380, 300),
    ("photo4-jointpipe",      0.598, 0.418, 0.798, 0.542, 300),
    ("photo3-clamp-detail",   0.812, 0.252, 0.980, 0.532, 300),
    ("tableau-operations",    0.018, 0.568, 0.985, 0.992, 660),
]

os.makedirs(OUT, exist_ok=True)
im = Image.open(SRC)
W, H = im.size
rapport = {"source": SRC, "dimensions_source": [W, H], "crops": []}

for nom, fx0, fy0, fx1, fy1, disp_w in CROPS:
    box = (int(fx0 * W), int(fy0 * H), int(fx1 * W), int(fy1 * H))
    crop = im.crop(box)
    chemin = os.path.join(OUT, f"{nom}.png")
    crop.save(chemin)
    cw, ch = crop.size
    # Sur-échantillonnage = px source / px d'affichage cible (≥ 2 requis pour une
    # impression nette ~150 DPI : cf. mise-en-page, maths-integration §3).
    sur_echantillonnage = round(cw / disp_w, 2)
    rapport["crops"].append({
        "nom": nom, "boite_fraction": [fx0, fy0, fx1, fy1],
        "boite_px": list(box), "taille_px": [cw, ch],
        "affichage_cible_px": disp_w, "sur_echantillonnage_x": sur_echantillonnage,
        "dpi_impression_si_8cm": round(cw * 2.54 / 8),
    })
    print(f"{nom:24s} boîte px {box}  taille {cw}x{ch}  (x{sur_echantillonnage} vs affichage {disp_w}px)")

# --- copie d'archive du standard non-KPS (garde) ---
shutil.copy2(SRC, ARCHIVE)
sha = hashlib.sha256(open(ARCHIVE, "rb").read()).hexdigest()
rapport["archive_non_kps"] = {"chemin": ARCHIVE, "sha256": sha,
                              "taille_octets": os.path.getsize(ARCHIVE)}
print("archive :", ARCHIVE, "sha256", sha[:16], "...")

# --- planche de contact pour contrôle visuel ---
cols, vign_w = 3, 420
vigns = []
for nom, *_ in CROPS:
    c = Image.open(os.path.join(OUT, f"{nom}.png"))
    r = vign_w / c.width
    vigns.append((nom, c.resize((vign_w, max(1, int(c.height * r))), Image.LANCZOS)))
rows = (len(vigns) + cols - 1) // cols
cell_h = max(v.height for _, v in vigns) + 34
sheet = Image.new("RGB", (cols * (vign_w + 12) + 12, rows * (cell_h + 12) + 12), "#f1f5f9")
draw = ImageDraw.Draw(sheet)
font = ImageFont.truetype(FONT, 17)
for i, (nom, v) in enumerate(vigns):
    x = 12 + (i % cols) * (vign_w + 12)
    y = 12 + (i // cols) * (cell_h + 12)
    sheet.paste(v, (x, y + 26))
    draw.text((x, y + 2), nom, fill="#0f172a", font=font)
sheet_path = os.path.join(OUT, "contact-sheet.png")
sheet.save(sheet_path)
rapport["contact_sheet"] = sheet_path

with open(os.path.join(OUT, "rapport-crops.json"), "w", encoding="utf-8") as f:
    json.dump(rapport, f, ensure_ascii=False, indent=2)
print("planche :", sheet_path)
