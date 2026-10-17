#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.7)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.

dessin-technique — F4 mesure de filetage (v1.1.0) : photo d'une tige/vis
filetée de profil (+ pièce de centime comme référence d'échelle) → pas du
filet, diamètre majeur, désignation ISO 261 (candidats).

Usage :
  mesurer_filet.py <photo> --coin 1c|2c|5c|10c|20c|50c|1e|2e
                   [--zone x0,y0,x1,y1] [--axe horizontal|vertical]
                   [--diametre-mm X] [-o out.json]
  mesurer_filet.py --selftest

Méthode : profil de luminance moyen perpendiculairement aux stries →
détendance (moyenne glissante) → autocorrélation normalisée → pic dominant
(interpolation parabolique) → pas en px → pas en mm via l'échelle monnaie.
Désignation : table ISO 261 (miroir de references/filets-normaux.md),
candidats à Ø ±5 % ET pas ±max(10 %, 0,15 mm).
"""
import argparse
import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from capture_forme import PIECES_EURO_MM, segments, circularite  # v1.0.0 — import seul, zéro modification

ANALYSE_MAX = 760
BASE = os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))  # my-project (scripts → skill → skills → racine)

# Table ISO 261 — miroir exact de references/filets-normaux.md
TABLE_ISO = [
    ("M6x1", 6, 1.0),
    ("M8x1.25", 8, 1.25), ("M8x1", 8, 1.0),
    ("M10x1.5", 10, 1.5), ("M10x1.25", 10, 1.25), ("M10x1", 10, 1.0),
    ("M12x1.75", 12, 1.75), ("M12x1.5", 12, 1.5), ("M12x1.25", 12, 1.25),
    ("M14x2", 14, 2.0), ("M14x1.5", 14, 1.5),
    ("M16x2", 16, 2.0), ("M16x1.5", 16, 1.5),
    ("M18x2.5", 18, 2.5), ("M18x2", 18, 2.0), ("M18x1.5", 18, 1.5),
    ("M20x2.5", 20, 2.5), ("M20x2", 20, 2.0), ("M20x1.5", 20, 1.5),
    ("M22x2.5", 22, 2.5), ("M22x2", 22, 2.0), ("M22x1.5", 22, 1.5),
    ("M24x3", 24, 3.0), ("M24x2", 24, 2.0),
    ("M26x1.5", 26, 1.5),
    ("M27x3", 27, 3.0), ("M27x2", 27, 2.0),
    ("M30x3.5", 30, 3.5), ("M30x2", 30, 2.0),
]


def echelle_depuis_photo(img, coin, diametre_mm):
    """Ø de la monnaie détectée → px/mm (espace ANALYSE_MAX, jamais d'upscale —
    l'interpolation LANCZOS à l'agrandissement pollue les masques). Primitives v1.0.0."""
    W0, H0 = img.size
    sc = min(1.0, ANALYSE_MAX / max(W0, H0))
    small = img.resize((max(1, int(W0 * sc)), max(1, int(H0 * sc))),
                       Image.LANCZOS) if sc < 1.0 else img
    a = np.asarray(small).astype(np.int16)
    L = 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]
    mask_obj = L < 235
    lab, tailles = segments(mask_obj)
    if not tailles:
        raise SystemExit("ABANDON : aucun objet segmenté (fond uniforme ?)")
    ordres = sorted(tailles, key=lambda k: -tailles[k])
    # Discrimination par remplissage de bbox : cercle vu de face ≈ π/4 ≈ 0,785 ;
    # tige/objet plein de profil ≈ 1,0 — indépendant des tailles relatives.
    cands, rod_bbox = [], None
    for k in ordres:
        if tailles[k] < 120:
            continue  # specks/artéfacts (une monnaie fait ≥ ~12 px de Ø)
        ys, xs = np.nonzero(lab == k)
        bx0, by0, bx1, by1 = xs.min(), ys.min(), xs.max(), ys.max()
        bw, bh = bx1 - bx0 + 1, by1 - by0 + 1
        c = circularite(tailles[k], bw, bh)
        fill_bbox = tailles[k] / float(bw * bh)
        if c >= 0.60 and fill_bbox < 0.85:
            cands.append({"w": bw, "h": bh, "circ": c, "fill_bbox": round(fill_bbox, 3)})
        if fill_bbox > 0.90 and rod_bbox is None:
            rod_bbox = (int(bx0), int(by0), int(bx1), int(by1))
    if not cands:
        raise SystemExit(
            "ABANDON : aucune pièce de monnaie circulaire détectée — "
            "améliorez la photo ou fournissez --diametre-mm")
    m = max(cands, key=lambda c: c["circ"])
    if diametre_mm is not None:
        ref = {"type": "objet_fourni", "diametre_mm": diametre_mm}
        px_mm = m["w"] / diametre_mm
    else:
        d_mm = PIECES_EURO_MM[coin]
        d_px = (m["w"] + m["h"]) / 2
        px_mm = d_px / d_mm
        ref = {"type": "piece_euro", "denomination": coin,
               "diametre_mm": d_mm, "diametre_px": round(d_px, 1),
               "circularite": round(m["circ"], 3)}
    return px_mm, sc, ref, a, L, lab, tailles, rod_bbox


def profil_filet(L, zone, axe):
    """Profil 1D moyenné sur les lignes (axe horizontal) ou colonnes (vertical) objet."""
    x0, y0, x1, y1 = zone
    z = L[y0:y1, x0:x1]
    if axe == "horizontal":
        couv = (z < 200).mean(axis=1)
        lignes = couv > 0.5
        if lignes.sum() < 8:
            raise SystemExit("ABANDON : tige non couverte dans la zone (< 8 lignes objet)")
        idx = np.flatnonzero(couv > 0.3)
        perp = int(idx.max() - idx.min() + 1) if idx.size else 0
        return z[lignes].mean(axis=0).astype(float), perp
    couv = (z < 200).mean(axis=0)
    cols = couv > 0.5
    if cols.sum() < 8:
        raise SystemExit("ABANDON : tige non couverte dans la zone (< 8 colonnes objet)")
    idx = np.flatnonzero(couv > 0.3)
    return z[:, cols].mean(axis=0).astype(float), int(idx.max() - idx.min() + 1)


def detendre(p, fenetre=19):
    """Moyenne glissante normalisée aux bords (fenêtre effective locale) —
    évite les bosses d'extrémité qui auto-corrèlent (faux positifs de pas)."""
    w = np.ones(fenetre)
    num = np.convolve(p, w, mode="same")
    den = np.convolve(np.ones_like(p), w, mode="same")
    den[den == 0] = 1.0
    return p - num / den


def periode_autocorr(p):
    n = len(p)
    s = p - p.mean()
    ac = np.correlate(s, s, mode="full")[n - 1:]
    if ac[0] <= 0:
        raise SystemExit("ABANDON : profil constant (aucune strie)")
    ac = ac / ac[0]
    lag_max = max(4, n // 4)
    if lag_max <= 3:
        raise SystemExit("ABANDON : zone trop courte pour mesurer une périodicité")
    lags = np.arange(3, lag_max)
    vals = ac[3:lag_max]
    i = int(np.argmax(vals))
    if vals[i] < 0.25:
        raise SystemExit(f"ABANDON : aucune périodicité de filet détectée "
                         f"(pic {vals[i]:.2f} < 0,25 — la zone contient-elle du filetage ?)")
    lag = float(lags[i])
    if 0 < i < len(vals) - 1:
        y0, y1, y2 = vals[i - 1], vals[i], vals[i + 1]
        den = y0 - 2 * y1 + y2
        if den != 0:
            lag += 0.5 * (y0 - y2) / den
    return lag, float(vals[i])


def candidats_iso(d_mm, pas_mm):
    out = []
    for des, dn, pn in TABLE_ISO:
        e_d = abs(d_mm - dn) / dn
        e_p = abs(pas_mm - pn)
        if e_d <= 0.05 and e_p <= max(0.10 * pn, 0.15):
            out.append({"designation": des, "ecart_diametre_pct": round(e_d * 100, 2),
                        "ecart_pas_mm": round(e_p, 3),
                        "score": round(e_d + e_p / pn, 4)})
    out.sort(key=lambda c: c["score"])
    return out


def mesurer(chemin, coin=None, zone=None, axe="horizontal", diametre_mm=None):
    img = Image.open(chemin).convert("RGB")
    px_mm, sc, ref, a, L, lab, tailles, rod_bbox = echelle_depuis_photo(img, coin, diametre_mm)
    if zone is None:
        if rod_bbox is None:
            raise SystemExit("ABANDON : tige (objet allongé plein) non identifiée — "
                             "fournissez --zone x0,y0,x1,y1")
        bx0, by0, bx1, by1 = rod_bbox
        mx = int(0.10 * (bx1 - bx0))
        zone = (bx0 + mx, by0, bx1 - mx, by1)
    else:
        # la zone utilisateur est en pixels de l'image ORIGINALE → espace d'analyse
        zone = tuple(int(round(v * sc)) for v in zone)
    profil, perp_px = profil_filet(L, zone, axe)
    lag, pic = periode_autocorr(detendre(profil))
    pas_mm = lag / px_mm
    d_majeur_mm = perp_px / px_mm
    cands = candidats_iso(d_majeur_mm, pas_mm)
    return {
        "fichier": chemin,
        "echelle_px_mm": round(px_mm / sc, 4),  # espace de l'image originale
        "reference_echelle": ref,
        "filet": {
            "axe": axe,
            "pas_mm": round(pas_mm, 3),
            "pas_px_analyse": round(lag, 2),
            "pic_autocorrelation": round(pic, 3),
            "diametre_majeur_mm": round(d_majeur_mm, 2),
        },
        "designation_candidats": cands,
        "meilleur": cands[0]["designation"] if cands else None,
        "erreurs_estimees": {
            "pas": "≤ 10 % (netteté photo ; ≤ 5 % scène synthétique)",
            "diametre_majeur": "≤ 5 %",
            "limites": "vue de profil requise ; le profil du filet (angle, relief) "
                       "n'est pas mesurable sur photo simple",
        },
    }


def selftest():
    """T5 : tige M22x1,5 synthétique à 4 px/mm (Ø 88 px, pas 6 px) → ≤ 5 %."""
    S = 4.0
    img = Image.new("RGB", (640, 480), "#f5f5f5")
    d = ImageDraw.Draw(img)
    x0, y0 = 60, 200                      # tige 160x88 px, stries 2 px / 6 px
    d.rectangle([x0, y0, x0 + 160, y0 + 88], fill="#8a8a8a")
    for x in range(x0, x0 + 160, 6):
        d.line([x, y0, x, y0 + 88], fill="#505050", width=2)
    r = 16.25 * S / 2                     # pièce 1c Ø16,25 mm → 65 px
    d.ellipse([430 - r, 120 - r, 430 + r, 120 + r],
              fill="#c9c9c9", outline="#8a8a8a", width=2)
    p = os.path.join(BASE, "tmp", "selftest-filet.png")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    img.save(p)
    res = mesurer(p, coin="1c")
    pas, dia, best = res["filet"]["pas_mm"], res["filet"]["diametre_majeur_mm"], res["meilleur"]
    errs = {"pas": abs(pas - 1.5) / 1.5, "diametre": abs(dia - 22.0) / 22.0}
    ok = all(e <= 0.05 for e in errs.values()) and best == "M22x1.5"
    print(json.dumps({"selftest": "T5", "verdict": "PASS" if ok else "FAIL",
                      "erreurs": {k: round(v * 100, 2) for k, v in errs.items()},
                      "mesures": {"pas_mm": pas, "diametre_majeur_mm": dia,
                                  "meilleur": best,
                                  "candidats": [c["designation"] for c in res["designation_candidats"]]}},
                     ensure_ascii=False))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("photo", nargs="?")
    ap.add_argument("--coin", choices=list(PIECES_EURO_MM))
    ap.add_argument("--zone", help="x0,y0,x1,y1 (espace image originale)")
    ap.add_argument("--axe", default="horizontal", choices=["horizontal", "vertical"])
    ap.add_argument("--diametre-mm", type=float, dest="diametre_mm")
    ap.add_argument("-o", "--out")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        sys.exit(selftest())
    if not args.photo or (not args.coin and not args.diametre_mm):
        ap.error("photo + (--coin DENOM | --diametre-mm X) requis")
    zone = tuple(int(v) for v in args.zone.split(",")) if args.zone else None
    res = mesurer(args.photo, args.coin, zone, args.axe, args.diametre_mm)
    out = json.dumps(res, ensure_ascii=False, indent=2)
    if args.out:
        open(args.out, "w", encoding="utf-8").write(out)
    print(out)


if __name__ == "__main__":
    main()
