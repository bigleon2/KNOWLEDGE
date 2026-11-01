#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""qa-animation v1.0.0 — CONTRÔLES QUALITÉ MÉCANIQUES des livrables animés (GIF).

Task 8 (directive propriétaire 2026-10-31 « crée $facon ces trois skills » —
suggestion D018-3, douleur prouvée du 2026-10-25 : la QA du GIF mouton rasta fut
VISUELLE à chaque itération — 3 versions — alors que chaque critère de rejet était
vérifiable mécaniquement).

Ce que ce contrôle VÉRIFIE mécaniquement (déterministe, PIL uniquement) :
  format       → lisible par PIL, format GIF
  animation    → is_animated + n_frames >= 2
  boucle       → info['loop'] (0 = infinie ; absent = inconnue — déclaré honnête)
  dimensions   → taille (l, h)
  poids        → octets du fichier (+ poids_max_mo du référentiel)
  durees       → durée par frame + uniformité (min/max)
  palette      → couleurs distinctes utilisées (échantillon) + dominantes top 5
  mouvement    → bbox de différence frame 0 ↔ frame médiane (movement réel)
  referentiel  → si fourni (JSON) : frames, dimensions, boucle, poids_max_mo,
                 palette_dominante (tolérance canal ±32), duree_frame_ms, mouvement

Ce que ce contrôle NE VÉRIFIE PAS (subjectif — honnêteté R3, jamais simulé) :
  couleurs perçues (« peau trop verte »), anatomie du sprite (« yeux au menton »,
  « une seule jambe »), fidélité au personnage source, esthétique générale.
Ces critères restent de la responsabilité de la revue VISUELLE — ils sont LISTÉS
dans chaque rapport pour rappeler qu'ils n'ont PAS été vérifiés mécaniquement.

Usage :
    python3 qa_animation.py --gif livrable.gif [--referentiel ref.json] [--json]
Codes retour : 0 PASS (tous les contrôles applicables) · 1 FAIL (au moins un échec)
· 6 fichier invalide/illisible.
"""
import argparse
import json
import os
import sys
import time

SKILL = "gif-animator-pro"
FEATURE = "qa-animation"
VERSION = "1.0.0"

CRITERES_SUBJECTIFS = [
    "couleurs perçues (ex. « peau trop verte ») — revue visuelle requise",
    "anatomie du sprite (ex. « yeux au menton », « une seule jambe ») — revue visuelle requise",
    "fidélité au personnage/source fourni — revue visuelle requise",
    "esthétique générale du rendu — revue visuelle requise",
]

TOLERANCE_CANAL = 32  # comparaison de palette dominante (anti-fragile au dithering)


def _hex(rgb):
    return "#%02X%02X%02X" % tuple(rgb[:3])


def _dist_canal(a, b):
    return max(abs(a[i] - b[i]) for i in range(3))


def parse_referentiel(path):
    with open(path, encoding="utf-8") as f:
        j = json.load(f)
    if not isinstance(j, dict):
        raise ValueError("référentiel : objet JSON attendu")
    return j


def analyse(gif_path):
    """Analyse mécanique complète d'un GIF — retourne (mesures, erreurs_lecture)."""
    from PIL import Image, ImageChops
    mesures, erreurs = {}, []
    img = Image.open(gif_path)
    if (img.format or "").upper() != "GIF":
        # format non-GIF = fichier invalide pour ce contrôle (rc 6, pas un échec de contrôle)
        raise ValueError("format %s ≠ GIF" % img.format)
    mesures["format"] = img.format
    n_frames = getattr(img, "n_frames", 1)
    mesures["frames"] = n_frames
    mesures["anime"] = bool(getattr(img, "is_animated", False)) and n_frames >= 2
    loop = img.info.get("loop", None)
    mesures["boucle"] = "infinie" if loop == 0 else ("inconnue" if loop is None else loop)
    mesures["dimensions"] = list(img.size)
    mesures["poids_octets"] = os.path.getsize(gif_path)

    # durées par frame
    durees = []
    for i in range(n_frames):
        img.seek(i)
        durees.append(int(img.info.get("duration", 0) or 0))
    mesures["durees_frame_ms"] = durees
    mesures["duree_uniforme"] = (len(set(durees)) <= 1) if durees else None

    # échantillon de frames (≤ 16 frames balayées, pas × pas régulier)
    idx = sorted(set([0, n_frames // 2, n_frames - 1] +
                     [int(i * (n_frames - 1) / 15) for i in range(16) if n_frames > 1]))
    palette_count = {}
    rgb_frames = {}
    for i in idx:
        img.seek(i)
        f = img.convert("RGB")
        rgb_frames[i] = f
        cols = f.getcolors(maxcolors=1 << 16)
        if cols:
            for cnt, col in cols:
                palette_count[col] = palette_count.get(col, 0) + cnt
    mesures["couleurs_distinctes"] = len(palette_count)
    dominantes = sorted(palette_count.items(), key=lambda kv: -kv[1])[:5]
    mesures["palette_dominante"] = [_hex(col) for col, _ in dominantes]

    # mouvement : bbox de différence frame 0 ↔ frame médiane
    bbox = None
    if n_frames >= 2 and (n_frames // 2) in rgb_frames and 0 in rgb_frames:
        diff = ImageChops.difference(rgb_frames[0], rgb_frames[n_frames // 2])
        bbox = diff.getbbox()
    mesures["mouvement"] = bbox is not None
    mesures["mouvement_bbox"] = list(bbox) if bbox else None
    return mesures, erreurs


def controles(mesures, ref):
    """Compare les mesures au référentiel (ou aux invariants absolus si ref absent)."""
    c = []

    def add(nom, valeur, attendu, ok):
        c.append({"controle": nom, "valeur": valeur, "attendu": attendu, "verdict": "PASS" if ok else "FAIL"})

    add("format GIF", mesures.get("format"), "GIF", mesures.get("format") == "GIF")
    add("animation (frames >= 2)", mesures.get("frames"), ">= 2",
        bool(mesures.get("anime")))
    if ref.get("frames") is not None:
        add("frames (référentiel)", mesures.get("frames"), ref["frames"], mesures.get("frames") == ref["frames"])
    if ref.get("dimensions"):
        add("dimensions (référentiel)", mesures.get("dimensions"), ref["dimensions"],
            list(mesures.get("dimensions") or []) == list(ref["dimensions"]))
    if "boucle" in ref:
        add("boucle (référentiel)", mesures.get("boucle"), ref["boucle"],
            str(mesures.get("boucle")) == str(ref["boucle"]))
    if ref.get("poids_max_mo") is not None:
        add("poids <= %s Mo (référentiel)" % ref["poids_max_mo"], mesures.get("poids_octets"),
            "<= %d octets" % int(ref["poids_max_mo"] * 1048576),
            (mesures.get("poids_octets") or 0) <= int(ref["poids_max_mo"] * 1048576))
    if ref.get("duree_frame_ms") is not None:
        att = ref["duree_frame_ms"]
        durees = mesures.get("durees_frame_ms") or []
        ok = all((min(att) if isinstance(att, list) else att) <= d <=
                 (max(att) if isinstance(att, list) else att) for d in durees if d)
        add("durée/frame ms (référentiel)", durees, att, ok)
    if ref.get("palette_dominante"):
        dom = mesures.get("palette_dominante") or []
        dom_rgb = [tuple(int(dom_hex.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)) for dom_hex in dom]
        detail = {}
        for attendu_hex in ref["palette_dominante"]:
            rgb = tuple(int(attendu_hex.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
            detail[attendu_hex] = any(_dist_canal(rgb, d) <= TOLERANCE_CANAL for d in dom_rgb)
        add("palette dominante (référentiel, tolérance ±%d/canal)" % TOLERANCE_CANAL,
            dom, ref["palette_dominante"], all(detail.values()))
    if "mouvement" in ref:
        add("mouvement (référentiel)", mesures.get("mouvement"), ref["mouvement"],
            bool(mesures.get("mouvement")) == bool(ref["mouvement"]))
    return c


def main():
    ap = argparse.ArgumentParser(
        description="qa-animation — contrôles mécaniques des livrables animés (GIF)")
    ap.add_argument("--gif", required=True, help="GIF livrable à contrôler")
    ap.add_argument("--referentiel", help="JSON optionnel : frames, dimensions, boucle, "
                                          "poids_max_mo, palette_dominante, duree_frame_ms, mouvement")
    ap.add_argument("--json", action="store_true", help="sortie machine-readable")
    a = ap.parse_args()
    t0 = time.perf_counter()
    gif = os.path.realpath(os.path.expanduser(a.gif))
    if not os.path.isfile(gif):
        return _fin(a.json, "fichier introuvable : %s" % a.gif, 6)
    try:
        ref = parse_referentiel(a.referentiel) if a.referentiel else {}
    except Exception as e:
        return _fin(a.json, "référentiel illisible (%s: %s)" % (type(e).__name__, e), 6)
    try:
        mesures, erreurs_lecture = analyse(gif)
    except Exception as e:
        return _fin(a.json, "GIF illisible (%s: %s)" % (type(e).__name__, e), 6)
    c = controles(mesures, ref)
    n_fail = sum(1 for x in c if x["verdict"] == "FAIL")
    verdict = "PASS" if n_fail == 0 and not erreurs_lecture else "FAIL"
    res = {
        "commande": FEATURE, "skill": SKILL, "feature_version": VERSION,
        "fichier": gif, "mesures": mesures, "controles": c,
        "verdict": verdict, "echecs": n_fail,
        "erreurs_lecture": erreurs_lecture,
        "criteres_subjectifs_non_verifies": CRITERES_SUBJECTIFS,
        "duree_s": round(time.perf_counter() - t0, 2),
        "regle": ("verdict mécanique — les critères subjectifs listés restent à la revue "
                  "visuelle (honnêteté R3) : ils ne sont JAMAIS simulés ici"),
    }
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print("╔═ %s/%s v%s — QA MÉCANIQUE — %.2f s — verdict : %s"
              % (SKILL, FEATURE, VERSION, res["duree_s"], verdict))
        print("║ fichier : %s" % gif)
        for x in c:
            print("║ %s %s — valeur %s / attendu %s" % ("✓" if x["verdict"] == "PASS" else "✗",
                                                        x["controle"], x["valeur"], x["attendu"]))
        for e in erreurs_lecture:
            print("║ ⚠ %s" % e)
        print("║ NON vérifié (subjectif — revue visuelle) :")
        for s in CRITERES_SUBJECTIFS:
            print("║   · %s" % s)
        print("╚═" + "═" * 60)
    return 0 if verdict == "PASS" else 1


def _fin(as_json, msg, code):
    res = {"commande": FEATURE, "skill": SKILL, "feature_version": VERSION,
           "verdict": "ERREUR", "erreur": msg}
    if as_json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print("[%s] ERREUR : %s" % (FEATURE, msg))
    return code


if __name__ == "__main__":
    sys.exit(main())
