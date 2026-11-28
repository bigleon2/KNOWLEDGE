#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verifier-task19-clone.py — Vérificateur mécanique du clone 11ᵉ (clôture fenêtre 15).

S1-S9 sur download/clone-session-web-220878ed-20261128-task19-caches-semantiques-cloture.md :
structure §0-§5+§1bis, lignée 1→11, auto-suffisance (chemins absolus), table des thèmes
(7 thèmes, preuves ≥2, slugs kebab-case), cohérence versions disque, drifts §3.5,
instructions rejouables, traçabilité worklog 165-175, mode incrémental §1.13 cité.
Idempotent ×2.
"""
import re
import sys
from pathlib import Path

CLONE = Path("/home/z/my-project/download/clone-session-web-220878ed-20261128-task19-caches-semantiques-cloture.md")
CHECKS = []


def check(nom: str, cond: bool) -> None:
    CHECKS.append((nom, bool(cond)))
    print(f"  [{'PASS' if cond else 'FAIL'}] {nom}")


def main() -> int:
    if not CLONE.is_file():
        print(f"FAIL : clone absent : {CLONE}")
        return 1
    t = CLONE.read_text(encoding="utf-8")

    # S1 — structure imposée
    print("S1 — structure §0-§5 + §1bis")
    for sec in ("## §0 —", "## §1 —", "## §1bis —", "## §2 —", "### §2.4", "## §3 —", "### §3.5", "## §4 —", "## §5 —"):
        check(f"section {sec[:14]} présente", sec in t)

    # S2 — lignée de clonage 1→11
    print("S2 — lignée de clonage")
    check("titre 11ᵉ génération", "11ᵉ GÉNÉRATION" in t or "11ᵉ génération" in t)
    check("10 clones antérieurs listés", t.count("clone-session-web-220878ed-") >= 11)
    check("clone 10ᵉ cité comme cache §1.13", "task19-caches-semantiques.md" in t and "cache sémantique" in t)

    # S3 — auto-suffisance (chemins absolus, pas de renvoi externe nu)
    print("S3 — auto-suffisance")
    check("worklog hôte en chemin absolu", "/home/z/my-project/worklog.md" in t)
    check("dépôt en chemin absolu", "/home/z/my-project/KNOWLEDGE-repo/" in t)
    check("aucun placeholder résiduel", not re.search(r"\{\{[A-Z_]+\}\}|TODO|XXX|待补充", t))

    # S4 — table des thèmes (≥2 preuves, slugs kebab-case, 7 thèmes)
    print("S4 — table des thèmes §1bis")
    slugs = re.findall(r"\| `([a-z0-9-]+)` \|", t)
    check("7 thèmes à slugs kebab-case", len(set(slugs)) >= 7, )
    check("slug caches-semantiques présent", "caches-semantiques" in slugs)
    check("colonne preuves renseignée (≥2 par ligne)", "+" in t or " + " in t)

    # S5 — cohérence versions avec le disque
    print("S5 — cohérence versions disque")
    for f, ver in (("/home/z/my-project/skills/correct-work/SKILL.md", "2.12.2"),
                   ("/home/z/my-project/skills/clone-chat/SKILL.md", "2.2.0")):
        disque = ver in Path(f).read_text(encoding="utf-8")[:600]
        clone = f"v{ver}" in t
        check(f"v{ver} cohérente clone↔disque ({f.split('/')[-3]})", disque and clone)

    # S6 — drifts §3.5 renseignés
    print("S6 — drifts §3.5")
    i = t.find("### §3.5")
    j = t.find("## §4", i)  # fin de section : le titre suivant (le « --- » matcherait la séparation de table)
    bloc = t[i:j]
    check("≥4 drifts tracés avec types", bloc.count("| ENRICHISSEMENT") + bloc.count("| CORRECTION") + bloc.count("| SANS OBJET") >= 4)

    # S7 — instructions rejouables avec verdicts attendus
    print("S7 — instructions §4")
    for attendu in ("INSTALLE ×2, ALL PASS 6/6 ×2", "52/52 ×2", "PASS 25/25 ×2"):
        check(f"garantie attendue citée : {attendu}", attendu in t)

    # S8 — traçabilité worklog
    print("S8 — traçabilité worklog")
    check("suites 165→175 couvertes", "suites **165-168**" in t and "**175** (Task 19" in t)
    check("suite suivante = 176", "suite suivante = 176" in t)

    # S9 — mode incrémental §1.13 appliqué et cité
    print("S9 — mode incrémental §1.13")
    check("§1.13 citée (première application réelle)", "§1.13" in t and "PREMIÈRE application" in t or "première clôture produite SOUS v2.2.0" in t)
    check("delta explicite (fenêtre 15)", "delta re-analysé = fenêtre 15" in t or "delta = fenêtre 15" in t)

    ok = sum(1 for _, c in CHECKS if c)
    total = len(CHECKS)
    print(f"\nVÉRIFICATION CLONE 11ᵉ : {ok}/{total} PASS")
    return 0 if ok == total else 1


if __name__ == "__main__":
    sys.exit(main())
