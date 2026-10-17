#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.7)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.

dessin-technique — F1 capture de forme : photo d'une pièce (+ pièce de
centime comme référence d'échelle) → formes et cotes déduites (JSON).

Usage :
  capture_forme.py <photo> [--coin 1c|2c|5c|10c|20c|50c|1e|2e]
                    [--mode metal|sombre] [--diametre-mm X] [-o out.json]
  capture_forme.py --selftest
"""
import argparse
import json
import math
import sys
from collections import deque

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ANALYSE_MAX = 760
PIECES_EURO_MM = {
    "1c": 16.25, "2c": 18.75, "5c": 21.25, "10c": 19.75,
    "20c": 22.25, "50c": 24.25, "1e": 23.25, "2e": 25.75,
}


def segments(mask):
    """Composantes connexes 4-connexité → liste (label array, tailles)."""
    h, w = mask.shape
    lab = np.zeros((h, w), dtype=np.int32)
    tailles = {}
    cur = 0
    for sy in range(h):
        for sx in np.flatnonzero(mask[sy] & (lab[sy] == 0)):
            if lab[sy, sx]:
                continue
            cur += 1
            q = deque([(sy, sx)])
            lab[sy, sx] = cur
            n = 0
            while q:
                y, x = q.popleft()
                n += 1
                for ny, nx in ((y-1, x), (y+1, x), (y, x-1), (y, x+1)):
                    if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not lab[ny, nx]:
                        lab[ny, nx] = cur
                        q.append((ny, nx))
            tailles[cur] = n
    return lab, tailles


def fill_holes(cc):
    h, w = cc.shape
    outside = np.zeros((h, w), dtype=bool)
    q = deque()
    for x in range(w):
        for y in (0, h-1):
            if not cc[y, x] and not outside[y, x]:
                outside[y, x] = True; q.append((y, x))
    for y in range(h):
        for x in (0, w-1):
            if not cc[y, x] and not outside[y, x]:
                outside[y, x] = True; q.append((y, x))
    while q:
        y, x = q.popleft()
        for ny, nx in ((y-1, x), (y+1, x), (y, x-1), (y, x+1)):
            if 0 <= ny < h and 0 <= nx < w and not cc[ny, nx] and not outside[ny, nx]:
                outside[ny, nx] = True; q.append((ny, nx))
    return cc | (~cc & ~outside)


def masque_piece(a, mode):
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    L = 0.299*R + 0.587*G + 0.114*B
    gx = np.abs(np.diff(L, axis=1, prepend=L[:, :1]))
    gy = np.abs(np.diff(L, axis=0, prepend=L[:1, :]))
    grad = gx + gy
    if mode == "sombre":
        return L < 78
    return (L < 178) & (grad > 7)          # metal : texturé sur fond lisse


def circularite(npx, w, h):
    if max(w, h) == 0:
        return 0.0
    d_eff = 2 * math.sqrt(npx / math.pi)
    fill = npx / (math.pi * (d_eff / 2) ** 2)
    aspect = min(w, h) / max(w, h)
    return fill * aspect


def analyser(chemin, coin=None, mode="metal", diametre_mm=None):
    img = Image.open(chemin).convert("RGB")
    W0, H0 = img.size
    sc = ANALYSE_MAX / max(W0, H0)
    small = img.resize((int(W0*sc), int(H0*sc)), Image.LANCZOS)
    a = np.asarray(small).astype(np.int16)
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    L = 0.299*R + 0.587*G + 0.114*B
    gx = np.abs(np.diff(L, axis=1, prepend=L[:, :1]))
    gy = np.abs(np.diff(L, axis=0, prepend=L[:1, :]))
    grad = gx + gy

    # masque pièces (mode spécifique) et masque objets (détection monnaie)
    if mode == "sombre":
        mask_piece = L < 78
    else:
        mask_piece = (L < 178) & (grad > 7)
    mask_obj = L < 235                    # tout ce qui n'est pas le fond

    lab_p, tailles_p = segments(mask_piece)
    if not tailles_p:
        raise SystemExit("ABANDON : aucun objet segmenté (fond uniforme ?)")
    ordres_p = sorted(tailles_p, key=lambda k: -tailles_p[k])
    principal_label = ordres_p[0]
    ys, xs = np.nonzero(lab_p == principal_label)
    pw, ph = xs.max()-xs.min()+1, ys.max()-ys.min()+1
    bbox = (xs.min(), ys.min(), xs.max(), ys.max())

    # pièce de monnaie : candidat circulaire du masque objets, distinct de la
    # pièce principale et SITUÉ HORS de sa bbox (les cavités internes sont
    # exclues — KO-L003 : dérivation de l'état réel du masque)
    monnaie = None
    if diametre_mm is None and coin is not None:
        lab_o, tailles_o = segments(mask_obj)
        ordres_o = sorted(tailles_o, key=lambda k: -tailles_o[k])
        taille_max_o = tailles_o[ordres_o[0]]
        pool = []
        for k in ordres_o:
            if tailles_o[k] >= 0.5 * taille_max_o:
                continue
            yo, xo = np.nonzero(lab_o == k)
            bx0, bx1 = xo.min(), xo.max()
            by0, by1 = yo.min(), yo.max()
            # exclusion des composantes internes à la bbox pièce (marge 10 px)
            if (bx0 >= bbox[0]-10 and bx1 <= bbox[2]+10
                    and by0 >= bbox[1]-10 and by1 <= bbox[3]+10):
                continue
            bw, bh = bx1-bx0+1, by1-by0+1
            c = circularite(tailles_o[k], bw, bh)
            if c >= 0.60:
                pool.append({"w": bw, "h": bh, "circ": c, "n": tailles_o[k]})
        if not pool:
            raise SystemExit(
                "ABANDON : aucune pièce de monnaie circulaire détectée — "
                "améliorez la photo (pièce bien visible, séparée) ou fournissez "
                "--diametre-mm <Ø réel de l'objet de référence>")
        m = max(pool, key=lambda c: c["circ"])
        monnaie = m

    if diametre_mm is not None and monnaie is not None:
        px_mm = monnaie["w"] / diametre_mm
        ref = {"type": "objet_fourni", "diametre_mm": diametre_mm}
    elif monnaie is not None:
        d_mm = PIECES_EURO_MM[coin]
        d_px = (monnaie["w"] + monnaie["h"]) / 2
        px_mm = d_px / d_mm
        ref = {"type": "piece_euro", "denomination": coin,
               "diametre_mm": d_mm, "diametre_px": round(d_px, 1),
               "circularite": round(monnaie["circ"], 3)}
    else:
        raise SystemExit("ABANDON : ni --coin ni --diametre-mm fourni")

    # trous internes : cavités RELATIVEMENT sombres à l'intérieur du remplissage
    cc = fill_holes(lab_p == principal_label)
    Lmoy = L[cc].mean()
    trous_mask = cc & (L < Lmoy - 25)
    tl, tt = segments(trous_mask)
    trous = []
    for k, n in tt.items():
        if n < 40:
            continue
        ys2, xs2 = np.nonzero(tl == k)
        bw, bh = xs2.max()-xs2.min()+1, ys2.max()-ys2.min()+1
        if circularite(n, bw, bh) >= 0.55:
            trous.append(round(2 * (n / math.pi) ** 0.5 / px_mm, 1))
    trous.sort(reverse=True)

    return {
        "fichier": chemin,
        "echelle_px_mm": round(px_mm / sc, 4),  # espace de l'image originale
        "reference_echelle": ref,
        "piece": {
            "largeur_mm": round(pw / px_mm, 1),
            "hauteur_mm": round(ph / px_mm, 1),
            "trous_diametres_mm": trous[:4],
        },
        "erreurs_estimees": {
            "cotes": "≤ 5 % (photo conforme protocole) ; profondeurs/filets non mesurables",
            "echelle": "±1 px de détection du Ø de référence",
        },
    }


def selftest():
    """Scène synthétique aux cotes connues (4 px/mm) → vérification ≤ 5 %."""
    S = 4.0  # px/mm
    img = Image.new("RGB", (480, 380), "#f5f5f5")
    d = ImageDraw.Draw(img)
    # plaque 100x60 mm sombre avec trou Ø20 mm plus sombre (mode sombre)
    d.rectangle([16, 100, 16+400, 100+240], fill="#303030")
    d.ellipse([16+200-40, 100+120-40, 16+200+40, 100+120+40], fill="#101010")
    # pièce 1 centime Ø16,25 mm claire, séparée de la plaque (masque objets)
    r = 16.25*S/2
    cx, cy = 446, 40
    d.ellipse([cx-r, cy-r, cx+r, cy+r], fill="#c9c9c9", outline="#8a8a8a", width=2)
    import os
    os.makedirs("/tmp", exist_ok=True)
    p = "/tmp/mission-voss-selftest-capture.png"
    img.save(p)
    res = analyser(p, coin="1c", mode="sombre")
    lw, lh = res["piece"]["largeur_mm"], res["piece"]["hauteur_mm"]
    trou = res["piece"]["trous_diametres_mm"][0] if res["piece"]["trous_diametres_mm"] else None
    errs = {
        "largeur": abs(lw-100)/100, "hauteur": abs(lh-60)/60,
        "echelle": abs(res["echelle_px_mm"]-S)/S,
        "trou": abs(trou-20)/20 if trou else 1.0,
    }
    ok = all(e <= 0.05 for e in errs.values())
    print(json.dumps({"selftest": "T1", "verdict": "PASS" if ok else "FAIL",
                      "erreurs": {k: round(v*100, 2) for k, v in errs.items()},
                      "mesures": {"largeur_mm": lw, "hauteur_mm": lh, "trou_mm": trou}},
                     ensure_ascii=False))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("photo", nargs="?")
    ap.add_argument("--coin", choices=list(PIECES_EURO_MM))
    ap.add_argument("--mode", default="metal", choices=["metal", "sombre"])
    ap.add_argument("--diametre-mm", type=float, dest="diametre_mm")
    ap.add_argument("-o", "--out")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        sys.exit(selftest())
    if not args.photo or (not args.coin and not args.diametre_mm):
        ap.error("photo + (--coin DENOM | --diametre-mm X) requis")
    res = analyser(args.photo, args.coin, args.mode, args.diametre_mm)
    out = json.dumps(res, ensure_ascii=False, indent=2)
    if args.out:
        open(args.out, "w", encoding="utf-8").write(out)
    print(out)


if __name__ == "__main__":
    main()
