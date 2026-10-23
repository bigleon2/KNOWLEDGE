#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.10)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

# -*- coding: utf-8 -*-
"""Task 48 — PA-TEST-006 : crop côte à côte de la zone inscription (PIL pur) pour arbitrage ciblé.
Zone : homme à gauche au centre, t-shirt gris inscription rose/violette épaule gauche."""
import sys
from PIL import Image

orig, cand, out = sys.argv[1], sys.argv[2], sys.argv[3]
ZONE = (0.00, 0.68, 0.50, 1.00)  # x0, y0, x1, y1 — quadrant bas-gauche (t-shirt + inscription)

def crop(p):
    img = Image.open(p).convert("RGB")
    W, H = img.size
    box = (int(ZONE[0] * W), int(ZONE[1] * H), int(ZONE[2] * W), int(ZONE[3] * H))
    return img.crop(box)

a, b = crop(orig), crop(cand)
h = max(a.height, b.height)
canvas = Image.new("RGB", (a.width + b.width + 12, h), (255, 255, 255))
canvas.paste(a, (0, 0))
canvas.paste(b, (a.width + 12, 0))
canvas.save(out)
print(f"crop arbitrage : {out} ({canvas.width}×{canvas.height}) — gauche original, droite candidat")
