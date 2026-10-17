#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.7)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.

dessin-technique — F5 mesure de profondeur (v1.1.0) : photo d'un trou borgne
CIRCULAIRE à fond visible (+ pièce de centime pour l'échelle) → profondeur,
Ø d'ouverture, inclinaison de vue.

Usage :
  mesurer_profondeur.py <photo> --coin 1c|2c|5c|10c|20c|50c|1e|2e
                        --trou x0,y0,x1,y1 [--diametre-mm X] [-o out.json]
  mesurer_profondeur.py --selftest

Méthode (projection orthographique, fond éclairé) : le contour de la cavité
visible = ellipse d'ouverture (2a, 2b) → inclinaison φ = acos(b/a) ; le fond
(plus clair que la paroi) est tronqué par le bord proche : son extension le
long de l'axe mineur vaut 2b − δ avec δ = profondeur × sin φ × px_mm.
Gardes : vue trop verticale (b/a > 0,97) → ABANDON ; fond non visible → ABANDON.
Limites : ±8 % scène synthétique / ±15 % photo réelle (erreurs_estimees).
"""
import argparse
import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mesurer_filet import echelle_depuis_photo  # réutilise F4 (échelle monnaie)

BASE = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))  # my-project (scripts → skill → skills → racine)


def erode(m, it=2):
    """Érosion binaire 4-connexe (padding False, pas de wrap) — tue les anneaux
    d'interpolation LANCZOS sur le contour."""
    for _ in range(it):
        p = np.pad(m, 1, constant_values=False)
        m = (p[1:-1, 1:-1] & p[:-2, 1:-1] & p[2:, 1:-1]
             & p[1:-1, :-2] & p[1:-1, 2:])
    return m


EROSION_IT = 2


def analyser_zone(L, zone):
    """Ellipse d'ouverture (PCA) + extension du fond visible → (2a, 2b, δ, métriques)."""
    x0, y0, x1, y1 = zone
    z = L[y0:y1, x0:x1]
    p5, p95 = np.percentile(z, 5), np.percentile(z, 95)
    seuil = 0.5 * (p5 + p95)
    interieur = z < seuil
    if interieur.sum() < 80:
        raise SystemExit("ABANDON : intérieur du trou non segmenté "
                         f"({int(interieur.sum())} px < 80 — zone --trou trop petite ?)")
    ys, xs = np.nonzero(interieur)
    pts = np.stack([xs, ys], axis=1).astype(float)
    c = pts.mean(axis=0)
    cov = np.cov((pts - c).T)
    evals, evecs = np.linalg.eigh(cov)
    v_maj = evecs[:, int(np.argmax(evals))]
    v_min = evecs[:, int(np.argmin(evals))]

    def extent(vec, p):
        proj = p @ vec
        return float(proj.max() - proj.min() + 1.0)

    deux_a = extent(v_maj, pts)
    deux_b = extent(v_min, pts)
    b_sur_a = deux_b / deux_a
    if b_sur_a > 0.97:
        raise SystemExit("ABANDON : vue trop verticale (b/a > 0,97) — la profondeur "
                         "n'est pas séparable de l'ellipticité à cette inclinaison")
    phi = math.degrees(math.acos(min(1.0, b_sur_a)))

    Li = z[interieur]
    s_fond = Li.min() + 0.5 * (Li.max() - Li.min())
    fond = erode(interieur, EROSION_IT) & (z > s_fond)
    if fond.sum() < 40:
        raise SystemExit("ABANDON : fond du trou non visible (ou non éclairé) — "
                         "la méthode exige un fond distinguable de la paroi")
    ysf, xsf = np.nonzero(fond)
    pts_f = np.stack([xsf, ysf], axis=1).astype(float)
    ext_fond = extent(v_min, pts_f) + EROSION_IT  # compensation : seul le bord
    # FAR de la lentille confond avec le contour du masque intérieur (érodé) ;
    # le bord proche est interne (paroi/fond) et n'est pas érodé.
    delta = deux_b - ext_fond
    return {"deux_a": deux_a, "deux_b": deux_b, "b_sur_a": float(b_sur_a),
            "phi_deg": phi, "delta_px": float(delta), "ext_fond_px": ext_fond}


def mesurer(chemin, coin, zone, diametre_mm=None):
    img = Image.open(chemin).convert("RGB")
    px_mm, sc, ref, a, L, lab, tailles, rod_bbox = echelle_depuis_photo(img, coin, diametre_mm)
    # la zone utilisateur est en pixels de l'image ORIGINALE → espace d'analyse
    zone_an = tuple(int(round(v * sc)) for v in zone)
    m = analyser_zone(L, zone_an)
    phi = m["phi_deg"]
    if m["delta_px"] <= 1.0:
        prof = 0.0
        note = "trou traversant ou fond au ras (δ ≤ 1 px)"
    else:
        prof = m["delta_px"] / (px_mm * math.sin(math.radians(phi)))
        note = None
    return {
        "fichier": chemin,
        "echelle_px_mm": round(px_mm / sc, 4),  # espace de l'image originale
        "reference_echelle": ref,
        "trou": {
            "diametre_bord_mm": round(m["deux_a"] / px_mm, 2),
            "inclinaison_deg": round(phi, 1),
            "profondeur_mm": round(prof, 2),
            "profondeur_note": note,
            "delta_px": round(m["delta_px"], 2),
            "b_sur_a": round(m["b_sur_a"], 3),
        },
        "erreurs_estimees": {
            "profondeur": "±8 % scène synthétique / ±15 % photo réelle",
            "diametre_bord": "≤ 5 %",
            "limites": "projection orthographique (d ≪ distance caméra), fond éclairé "
                       "et distinguable de la paroi, trou circulaire",
        },
    }


def selftest():
    """T6 : ouverture Ø25 mm (a=50 px), φ=40°, profondeur 15 mm (δ=38,57 px) → ≤ 8 %."""
    S = 4.0
    img = Image.new("RGB", (640, 480), "#f0f0f0")
    d = ImageDraw.Draw(img)
    d.rectangle([60, 130, 580, 440], fill="#d0d0d0")   # plaque claire (sous la pièce)
    cx, cy = 300, 260
    a_px = 25.0 * S / 2                                # 50 px
    phi = math.radians(40.0)
    b_px = a_px * math.cos(phi)                        # 38,3 px
    delta = 15.0 * math.sin(phi) * S                   # 38,57 px
    t = np.linspace(0, 2 * np.pi, 720)
    ell = np.stack([a_px * np.cos(t), b_px * np.sin(t)], axis=1)
    inter = ell + [cx, cy]
    d.polygon([tuple(p) for p in inter], fill="#2a2a2a")            # cavité (paroi)
    fond = ell + [cx, cy + delta]
    # fond visible = intersection fond ∩ ouverture (clip par le polygone d'ouverture)
    from PIL import Image as _I
    mask_f = _I.new("L", img.size, 0)
    ImageDraw.Draw(mask_f).polygon([tuple(p) for p in fond], fill=255)
    mask_o = _I.new("L", img.size, 0)
    ImageDraw.Draw(mask_o).polygon([tuple(p) for p in inter], fill=255)
    clip = (np.asarray(mask_f) > 0) & (np.asarray(mask_o) > 0)
    arr = np.asarray(img).copy()
    arr[clip] = (90, 90, 90)                                        # fond plus clair
    img = _I.fromarray(arr)
    d = ImageDraw.Draw(img)
    d.polygon([tuple(p) for p in inter], outline="#303030", width=2)  # bord d'ouverture
    r = 25.75 * S / 2                     # pièce 2e Ø25,75 mm → 103 px
    d.ellipse([80 - r, 60 - r, 80 + r, 60 + r], fill="#c9c9c9", outline="#8a8a8a", width=2)
    p = os.path.join(BASE, "tmp", "selftest-profondeur.png")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    img.save(p)
    zone = (int(cx - a_px - 6), int(cy - b_px - 6), int(cx + a_px + 6), int(cy + b_px + 6))
    res = mesurer(p, coin="2e", zone=zone)
    tr = res["trou"]
    errs = {"profondeur": abs(tr["profondeur_mm"] - 15.0) / 15.0,
            "diametre": abs(tr["diametre_bord_mm"] - 25.0) / 25.0,
            "inclinaison": abs(tr["inclinaison_deg"] - 40.0) / 40.0}
    ok = errs["profondeur"] <= 0.08 and errs["diametre"] <= 0.05 and errs["inclinaison"] <= 0.075
    print(json.dumps({"selftest": "T6", "verdict": "PASS" if ok else "FAIL",
                      "erreurs": {k: round(v * 100, 2) for k, v in errs.items()},
                      "mesures": {"profondeur_mm": tr["profondeur_mm"],
                                  "diametre_bord_mm": tr["diametre_bord_mm"],
                                  "inclinaison_deg": tr["inclinaison_deg"],
                                  "b_sur_a": tr["b_sur_a"]}},
                     ensure_ascii=False))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("photo", nargs="?")
    ap.add_argument("--coin", choices=["1c", "2c", "5c", "10c", "20c", "50c", "1e", "2e"])
    ap.add_argument("--trou", help="x0,y0,x1,y1 (espace image originale)")
    ap.add_argument("--diametre-mm", type=float, dest="diametre_mm")
    ap.add_argument("-o", "--out")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        sys.exit(selftest())
    if not args.photo or (not args.coin and not args.diametre_mm):
        ap.error("photo + (--coin DENOM | --diametre-mm X) requis")
    if not args.trou:
        ap.error("--trou x0,y0,x1,y1 requis (ou --selftest)")
    zone = tuple(int(v) for v in args.trou.split(","))
    res = mesurer(args.photo, args.coin, zone, args.diametre_mm)
    out = json.dumps(res, ensure_ascii=False, indent=2)
    if args.out:
        open(args.out, "w", encoding="utf-8").write(out)
    print(out)


if __name__ == "__main__":
    main()
