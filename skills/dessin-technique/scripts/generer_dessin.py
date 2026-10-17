#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.7)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.

dessin-technique — F3 génération dans le style « dessin technique » :
spec de scène + DNA de style → rendu z-ai + couche d'annotations PIL.

Usage :
  generer_dessin.py --spec scene.json --out img.png [--size 1344x768] [--check]
  generer_dessin.py --check-only --out img.png   (re-contrôle d'un rendu)
"""
import argparse
import colorsys
import json
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DNA = os.path.join(SKILL, "style-dna.json")
FD = "/usr/share/fonts/truetype/dejavu/"


def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def construire_prompt(spec):
    dna = json.load(open(DNA, encoding="utf-8"))
    blocs = [dna["prompt_style_en"]]
    scene = spec.get("scene", "").strip()
    if scene:
        blocs.append("Scene: " + scene)
    for p in spec.get("pieces", []):
        if p.get("forme"):
            blocs.append(f"{p['id']}: {p['forme']}")
    blocs.append("Absolutely no text, no labels, no numbers, no watermark, "
                 "no dimension lines in the generated image (annotations are "
                 "added later), no photo realism.")
    return ". ".join(b + "." for b in blocs)


def postpro(img):
    """Conformité DNA : fond #f8f8f8 + ombres supprimées + palette flat à 5 tons.
    La quantification par bandes de luminance reproduit le rendu CAO flat du
    dessin de référence (lavande dessus / gris flancs / anthracite arêtes)."""
    a = np.asarray(img.convert("RGB")).astype(np.int16)
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    L = 0.299*R + 0.587*G + 0.114*B
    # fond : zones claires connectées aux bords (+ ombres douces collées au sol)
    h, w = L.shape
    from collections import deque
    bg = (L > 205) | ((L > 110) & (np.abs(R-G) < 14) & (np.abs(G-B) < 14) & (B >= R))
    visited = np.zeros((h, w), dtype=bool)
    q = deque()
    for x in range(w):
        for y in (0, h-1):
            if bg[y, x] and not visited[y, x]:
                visited[y, x] = True; q.append((y, x))
    for y in range(h):
        for x in (0, w-1):
            if bg[y, x] and not visited[y, x]:
                visited[y, x] = True; q.append((y, x))
    while q:
        y, x = q.popleft()
        for ny, nx in ((y-1, x), (y+1, x), (y, x-1), (y, x+1)):
            if 0 <= ny < h and 0 <= nx < w and bg[ny, nx] and not visited[ny, nx]:
                visited[ny, nx] = True; q.append((ny, nx))
    out = np.zeros_like(a)
    # palette DNA par bandes de luminance (objets uniquement)
    pal = [(60, (58, 58, 68)), (100, (106, 106, 120)), (140, (160, 160, 174)),
           (200, (184, 184, 196)), (256, (216, 216, 248))]
    Lo = np.clip(L, 0, 255)
    idx = np.digitize(Lo, [p[0] for p in pal[:-1]])
    for i, (_, col) in enumerate(pal):
        m = idx == i
        out[m] = col
    out[visited] = (248, 248, 248)
    return Image.fromarray(out.astype(np.uint8))


def annoter(img, annotations):
    """Couche de cotation PIL suivant le DNA (#4b4b51, flèches pleines)."""
    d = ImageDraw.Draw(img)
    col = hex2rgb("#4b4b51")
    acc = hex2rgb("#226b8f")
    corr = hex2rgb("#d16c4a")
    f_cote = ImageFont.truetype(FD + "DejaVuSans.ttf", 20)
    f_note = ImageFont.truetype(FD + "DejaVuSans-Bold.ttf", 22)
    f_pet = ImageFont.truetype(FD + "DejaVuSans.ttf", 17)
    for an in annotations:
        t = an.get("type", "note")
        x, y = int(an["x_px"]), int(an["y_px"])
        txt = an["texte"]
        if t == "cote":
            d.text((x, y), txt, font=f_cote, fill=col)
        elif t == "couple":
            pad = 10
            tw = d.textlength(txt, font=f_note)
            d.rounded_rectangle([x, y, x + tw + 2*pad, y + 34], 5, fill=corr)
            d.text((x + pad, y + 5), txt, font=f_note, fill="#ffffff")
        elif t == "ligne":
            x2, y2 = int(an["x2_px"]), int(an["y2_px"])
            d.line([x, y, x2, y2], fill=col, width=2)
            if an.get("texte"):
                d.text((x2 + 8, y2 - 10), an["texte"], font=f_pet, fill=col)
        else:
            d.text((x, y), txt, font=f_note if an.get("fort") else f_cote,
                   fill=acc if an.get("accent") else col)
    return img


def check_style(img_path):
    """T3 : conformité palette du rendu vs DNA."""
    dna = json.load(open(DNA, encoding="utf-8"))
    a = np.asarray(Image.open(img_path).convert("RGB")).astype(np.int16)
    L = 0.299*a[..., 0] + 0.587*a[..., 1] + 0.114*a[..., 2]
    tot = L.size
    clair = (L > 235).sum() / tot
    gris = ((L > 140) & (L < 210) &
            (np.abs(a[..., 0] - a[..., 1]) < 30)).sum() / tot
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    lavande = ((b - r > 15) & (b - g > 10) & (L > 170) & (L < 245)).sum() / tot
    sombres = (L < 110).sum() / tot
    crit = {
        "fond_clair_dominant": bool(clair > 0.25),
        "faces_grises_presentes": bool(0.05 < gris < 0.75),
        "lavande_presente": bool(lavande > 0.008),
        "traits_sombres_presents": bool(0.002 < sombres < 0.30),
    }
    verdict = "PASS" if all(crit.values()) else "FAIL"
    return {"check": "T3", "verdict": verdict,
            "mesures": {"fond": round(clair, 3), "gris": round(gris, 3),
                        "lavande": round(lavande, 3), "traits": round(sombres, 3)},
            "criteres": crit}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec")
    ap.add_argument("--out", required=True)
    ap.add_argument("--size", default="1344x768")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--check-only", action="store_true")
    ap.add_argument("--annotate-only", action="store_true",
                    help="applique les annotations de la spec sur le rendu "
                         "_base existant (sans régénérer)")
    args = ap.parse_args()
    if args.check_only:
        print(json.dumps(check_style(args.out), ensure_ascii=False))
        return
    if not args.spec:
        ap.error("--spec requis (ou --check-only)")
    spec = json.load(open(args.spec, encoding="utf-8"))
    if args.annotate_only:
        base = args.out.replace(".png", "_base.png")
        img = postpro(Image.open(base).convert("RGB"))
        img = annoter(img, spec.get("annotations", []))
        img.save(args.out)
        print(json.dumps({"out": args.out, "annotate_only": True,
                          "postpro": True}, ensure_ascii=False))
        return
    prompt = construire_prompt(spec)
    # rendu de base via z-ai CLI
    base = args.out.replace(".png", "_base.png")
    r = subprocess.run(["z-ai", "image", "-p", prompt, "-o", base,
                        "-s", args.size], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"FAIL génération z-ai : {r.stderr[-300:]}")
    img = postpro(Image.open(base).convert("RGB"))
    img = annoter(img, spec.get("annotations", []))
    img.save(args.out)
    rapport = {"out": args.out, "prompt_chars": len(prompt)}
    if args.check:
        rapport["style"] = check_style(args.out)
    print(json.dumps(rapport, ensure_ascii=False))


if __name__ == "__main__":
    main()
