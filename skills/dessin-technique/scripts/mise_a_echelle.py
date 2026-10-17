#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.7)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.

dessin-technique — F2 mise à l'échelle pièce par pièce : cotes connues →
facteurs d'échelle harmonisés pour un dessin multi-pièces.

Usage :
  mise_a_echelle.py <spec.json> --cible-w W --cible-h H
                    [--echelle-commune] [-o plan.json]
  mise_a_echelle.py --selftest

spec.json : {"pieces":[{"id","dims_mm":{"cote":valeur,...},"poids":1.0}]}
"""
import argparse
import json
import sys


def planifier(spec, cw, ch, commune=False):
    pieces = spec["pieces"]
    n = len(pieces)
    # taille linéaire allouée à chaque pièce (poids normalisés)
    poids = [float(p.get("poids", 1.0)) for p in pieces]
    tot = sum(poids)
    parts = [p / tot for p in poids]
    zone = 0.92 * min(cw, ch)   # marges 8 %

    echelles = []
    if commune:
        # échelle unique : la plus grande pièce doit tenir dans la zone
        s = min(zone / max(p["dims_mm"].values()) for p in pieces)
        echelles = [s] * n
    else:
        for p, part in zip(pieces, parts):
            max_mm = max(p["dims_mm"].values())
            L = zone * part            # part visuelle linéaire de la pièce
            echelles.append(L / max_mm)

    plan = {"cible": {"w": cw, "h": ch}, "mode": "commune" if commune else "par_piece",
            "pieces": []}
    for p, s in zip(pieces, echelles):
        dims_px = {k: round(v * s, 1) for k, v in p["dims_mm"].items()}
        plan["pieces"].append({"id": p["id"], "echelle_px_mm": round(s, 4),
                               "dims_px": dims_px})
    # contrôle de cohérence : dims_px = dims_mm × échelle (tolérance d'arrondi)
    for piece, p in zip(plan["pieces"], pieces):
        s_exact = echelles[pieces.index(p)]
        for k in p["dims_mm"]:
            assert abs(piece["dims_px"][k] - p["dims_mm"][k] * s_exact) <= 0.06, \
                f"ratio {piece['id']}.{k}"
    return plan


def selftest():
    """T2 : 2 pièces de cotes connues → ratios et cohérence."""
    spec = {"pieces": [
        {"id": "uma", "dims_mm": {"hex": 27, "filetage": 22, "longueur": 55}},
        {"id": "coude", "dims_mm": {"ecrou": 26, "stud": 22, "hauteur": 42}},
    ]}
    plan = planifier(spec, 1344, 768)
    p1, p2 = plan["pieces"]
    # pièce 1 poids 1/2 : son échelle doit être plus grande que si elle était seule pleine zone? non :
    # vérifications contractuelles :
    ok = True
    raisons = []
    # 1) ratios px/mm == échelle (déjà asserté dans planifier)
    # 2) à poids égaux, max_dim des deux pièces rend leurs tailles visuelles comparables
    vis1 = max(p1["dims_px"].values())
    vis2 = max(p2["dims_px"].values())
    if not (0.7 < vis1 / vis2 < 1.4):
        ok = False; raisons.append(f"tailles visuelles déséquilibrées {vis1}/{vis2}")
    # 3) mode commune : échelles identiques
    plan2 = planifier(spec, 1344, 768, commune=True)
    s_set = {x["echelle_px_mm"] for x in plan2["pieces"]}
    if len(s_set) != 1:
        ok = False; raisons.append("mode commune : échelles divergentes")
    # 4) cohérence relative des cotes réelles : hex 27 > filetage 22 en px
    if not p1["dims_px"]["hex"] > p1["dims_px"]["filetage"]:
        ok = False; raisons.append("ordre des cotes non conservé")
    print(json.dumps({"selftest": "T2", "verdict": "PASS" if ok else "FAIL",
                      "raisons": raisons,
                      "echelles": [p1["echelle_px_mm"], p2["echelle_px_mm"]]},
                     ensure_ascii=False))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("spec", nargs="?")
    ap.add_argument("--cible-w", type=int, dest="cible_w")
    ap.add_argument("--cible-h", type=int, dest="cible_h")
    ap.add_argument("--echelle-commune", action="store_true", dest="echelle_commune")
    ap.add_argument("-o", "--out")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        sys.exit(selftest())
    if not args.spec or not args.cible_w or not args.cible_h:
        ap.error("spec.json + --cible-w + --cible-h requis")
    spec = json.load(open(args.spec, encoding="utf-8"))
    plan = planifier(spec, args.cible_w, args.cible_h, args.echelle_commune)
    out = json.dumps(plan, ensure_ascii=False, indent=2)
    if args.out:
        open(args.out, "w", encoding="utf-8").write(out)
    print(out)


if __name__ == "__main__":
    main()
