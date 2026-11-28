#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verifier-task20-all.py — Vérification mécanique INDÉPENDANTE de l'exécution
`clone-chat (ALL)` (fenêtre 16 — trace 1a221dc7539d4351).

Relit les 8 livrables DU DISQUE (pas la mémoire du générateur) :
  V1 présence ×2 conformité gabarit par clone (sections obligatoires)
  V2 check 9 indépendant par clone (slug au nom, §0bis, preuves ≥2,
     aucun slug voisin en §1-§3 hors pointeurs de fichiers)
  V3 index cohérent (7 thèmes, 8 fichiers listés, garde anti-slug inconnu,
     canonique cité, idempotence mentionnée)
  V4 batterie préalable (rapport 30/30) + produits consignés (JSON)
  V5 no-collision : 8 noms uniques, aucun clone antérieur écrasé (les 11
     clones de la lignée toujours présents)
Idempotent ×2.
"""
import hashlib
import json
import os
import re
import sys
from pathlib import Path

DL = Path("/home/z/my-project/download")
HOST = Path("/home/z/my-project")
SUJET = "clone-session-web-220878ed"
DATE = "20261128"
SLUGS = ["kps-conversion", "ecosysteme-gif-photo", "installation-ecosysteme",
         "gen-plan-optimisation", "git-pendances", "clone-chat-archivage", "caches-semantiques"]
CANONIQUE = f"{SUJET}-20261128-task19-caches-semantiques-cloture.md"
CHECKS = []


def check(nom: str, cond: bool, detail: str = "") -> None:
    CHECKS.append((nom, bool(cond)))
    print(f"  [{'PASS' if cond else 'FAIL'}] {nom}" + (f" — {detail[:120]}" if detail and not cond else ""))


def main() -> int:
    # V1 + V2 — par clone
    for slug in SLUGS:
        p = DL / f"{SUJET}-clone-theme-{slug}-{DATE}.md"
        if not p.is_file():
            check(f"V1 clone {slug} présent", False)
            continue
        t = p.read_text(encoding="utf-8")
        check(f"V1 {slug} : sections gabarit (§0bis/§1.2/§2.3/§3.5/§4 état+étape/§5)",
              all(s in t for s in ("### §0bis — Exclusions", "### §1.2 Table des sessions", "### §2.3 Artefacts produits",
                                   "### §3.5 Évolutions de contexte", "### État courant du sous-projet",
                                   "### Prochaine étape exécutable", "## §5 — AUTO-CLONAGE THÉMATIQUE")))
        check(f"V1 {slug} : en-tête mode ALL + canonique cité", "(ALL)" in t and CANONIQUE in t and "v2.2.0" in t)
        # check 9 indépendant
        fails = []
        if slug not in p.name:
            fails.append("(c) slug hors nom")
        i0, i4 = t.find("## §1 —"), t.find("## §4 —")
        corps = re.sub(r"clone-session-web-220878ed-\S+", " ", t[i0:i4])
        voisins = [s for s in SLUGS if s != slug]
        hors = [a for a in voisins if a in corps]
        if hors:
            fails.append(f"(a) hors-thème : {hors}")
        if "## §0bis" not in t:
            fails.append("(b) §0bis absente")
        excl_tbl = t[t.find("## §0bis"):t.find("## §1 —")]
        if excl_tbl.count("| ") < 2 * len(voisins) // 2 or len(re.findall(r"^\| \d+ \|", excl_tbl, re.M)) < 3:
            fails.append("(b) table exclusions insuffisante")
        if "Preuves du périmètre (≥2)" not in t:
            fails.append("(d) preuves absentes")
        check(f"V2 {slug} : check 9 indépendant — 9/9", not fails, str(fails))

    # V3 — index
    idx = DL / f"{SUJET}-clone-themes-index-{DATE}.md"
    ti = idx.read_text(encoding="utf-8") if idx.is_file() else ""
    check("V3 index présent", idx.is_file())
    check("V3 index : 7 slugs de la table", all(f"`{s}`" in ti for s in SLUGS))
    check("V3 index : 8 fichiers produits listés", ti.count("clone-theme-") >= 7 and "clone-themes-index" in ti)
    check("V3 index : garde + canonique + idempotence", "thème non reconnu" in ti and CANONIQUE in ti and "écrasement à l'identique" in ti)

    # V4 — preuves du test préalable
    rep = json.loads((HOST / "scripts" / "task20-clone-all-report.json").read_text(encoding="utf-8"))
    check("V4 batterie préalable 30/30 PASS", rep.get("ok") == rep.get("total") == 30)
    prod = json.loads((HOST / "scripts" / "task20-clone-all-products.json").read_text(encoding="utf-8"))
    check("V4 produits consignés (7 clones 9/9)", prod.get("themes") == 7 and all(p["verdict"] == "9/9 PASS" for p in prod.get("produits", [])))

    # V5 — collision + lignée intacte
    noms = sorted(f for f in os.listdir(DL) if f.startswith(SUJET))
    check("V5 aucun doublon de nom dans download/", len(noms) == len(set(noms)))
    lignee = [f for f in os.listdir(DL) if re.match(r"clone-session-web-220878ed-2026\d{4}", f) and "clone-theme-" not in f and "clone-themes-index" not in f]
    check("V5 lignée des 11 clones antérieurs intacte", len(lignee) >= 11, f"{len(lignee)} trouvés")

    ok = sum(1 for _, c in CHECKS if c)
    total = len(CHECKS)
    print(f"\nVÉRIFICATION (ALL) : {ok}/{total} PASS")
    return 0 if ok == total else 1


if __name__ == "__main__":
    sys.exit(main())
