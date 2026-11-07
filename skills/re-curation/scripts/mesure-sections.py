#!/usr/bin/env python3
"""mesure-sections.py — Mesure du poids par section d'un SKILL.md (skill re-curation v1.0.0).

Généralisé depuis scripts/task72-mesure-sections.py (Task 72 E2) : chemin en argument,
sortie JSON optionnelle, selftest embarqué. Règle d'or n°5 : tout chiffre affiché est
mesuré ici. Python stdlib (N3), idempotent (lecture seule).

Usage :
  python3 skills/re-curation/scripts/mesure-sections.py <skill>          # tableau au chat
  python3 skills/re-curation/scripts/mesure-sections.py <skill> --json   # JSON machine
  python3 skills/re-curation/scripts/mesure-sections.py --selftest
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

RACINE = Path("/home/z/my-project")


def mesurer(chemin: Path) -> list[dict]:
    lignes = chemin.read_text(encoding="utf-8").splitlines()
    fm_fin = 0
    vues = 0
    for i, l in enumerate(lignes):
        if l.strip() == "---":
            vues += 1
            if vues == 2:
                fm_fin = i + 1
                break
    bornes = [(0, "(frontmatter)", 1)]
    bornes += [(i, re.sub(r"^#{2,3}\s+", "", l)[:78], i + 1) for i, l in enumerate(lignes)
               if re.match(r"^#{2,3} ", l) and i >= fm_fin]
    secs = []
    for k, (i, titre, num) in enumerate(bornes):
        j = bornes[k + 1][0] if k + 1 < len(bornes) else len(lignes)
        # octets réels : join + le saut de ligne de clôture (somme des sections == fichier)
        secs.append({"section": titre, "ligne_debut": num,
                     "ligne_fin": j,
                     "octets": len("\n".join(lignes[i:j]).encode("utf-8")) + 1})
    return secs


def main() -> int:
    p = argparse.ArgumentParser(description="mesure-sections.py — skill re-curation")
    p.add_argument("skill", nargs="?", help="nom du skill (skills/<nom>/SKILL.md)")
    p.add_argument("--json", action="store_true")
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    if a.selftest:
        # sait échouer : fichier introuvable + mesure correcte d'un gabarit
        import tempfile
        tmp = Path(tempfile.mkdtemp(prefix="mesure-selftest-"))
        gab = tmp / "SKILL.md"
        gab.write_text("---\nname: t\n---\n## A\n\nx\n\n## B\n\ny\n", encoding="utf-8")
        secs = mesurer(gab)
        ok1 = len(secs) == 3 and secs[0]["section"] == "(frontmatter)"
        total = sum(s["octets"] for s in secs)
        ok2 = total == gab.stat().st_size  # couverture exhaustive des octets
        try:
            mesurer(tmp / "ABSENT.md")
            ok3 = False
        except FileNotFoundError:
            ok3 = True
        print(f"  [{'PASS' if ok1 else 'FAIL'}] sections détectées (frontmatter + 2)")
        print(f"  [{'PASS' if ok2 else 'FAIL'}] couverture exhaustive ({total} o == fichier)")
        print(f"  [{'PASS' if ok3 else 'FAIL'}] fichier introuvable → erreur explicite")
        verdict = ok1 and ok2 and ok3
        print(f"SELFTEST : {'PASS' if verdict else 'FAIL'}")
        return 0 if verdict else 1
    if not a.skill:
        p.print_usage()
        return 3
    chemin = RACINE / "skills" / a.skill / "SKILL.md"
    if not chemin.is_file():
        print(f"ABANDON : {chemin} introuvable")
        return 2
    secs = mesurer(chemin)
    total = sum(s["octets"] for s in secs)
    if a.json:
        print(json.dumps({"skill": a.skill, "fichier": str(chemin),
                          "total_octets": total, "sections": secs}, ensure_ascii=False, indent=1))
    else:
        print(f"# Sections — skills/{a.skill}/SKILL.md ({total} o / {total/1024:.1f} Kio / {len(secs)} sections)")
        for s in sorted(secs, key=lambda x: -x["octets"]):
            print(f"  {s['octets']:>7} o  {s['section']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
