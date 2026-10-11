#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.3)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

"""refactoring-test — bras mécanique M3 (graphe d'interactions + blast radius).

Parse le registre KB (skills/KNOWLEDGE.md — arêtes **Dépend de**/**Utilisé
par**, même convention que l'arbitre test-coherence-interactions.py), construit
le graphe dirigé des dépendances (A -> B = A dépend de B) et quantifie le
blast radius d'une cible :
  - backward  : ensemble des éléments qui dépendent de la cible (directement
                ou transitivement) — impact d'une modification de la cible ;
  - forward   : ensemble des éléments dont la cible dépend — risque amont.

Verdict machine-à-machine (SKILL.md refactoring-test §1.3) :
  OK si fan-out backward < 4 ; PRESSION si 4-7 ; CRITIQUE si >= 8.

Usage :
    python3 scripts/refactoring-test-graph.py --target gen-plan [--json]
    python3 scripts/refactoring-test-graph.py --graph [--json]

Idempotent x2 : même état = même sortie (déterminisme — SKILL.md §1.5.4).
Stdlib uniquement. Lecture seule : ne modifie aucun fichier écosystème.
"""
import argparse
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KB = os.path.join(BASE, "skills", "KNOWLEDGE.md")
SKILLS = os.path.join(BASE, "skills")
REPORT = os.path.join(BASE, "scripts", "refactoring-test-report.json")


def known_skills():
    names = set()
    if os.path.isdir(SKILLS):
        for d in os.listdir(SKILLS):
            if os.path.isfile(os.path.join(SKILLS, d, "SKILL.md")):
                names.add(d)
    return names


def parse_kb(names):
    """Retourne {skill: {"depends_on": [...], "used_by": [...]}} — seuls les
    noms de skills connus (dossiers avec SKILL.md) forment des nœuds."""
    edges = {}
    if not os.path.isfile(KB):
        return edges
    text = open(KB, encoding="utf-8", errors="replace").read()
    blocks = re.split(r"^##\s+", text, flags=re.M)
    for b in blocks:
        m = re.match(r"([a-zA-Z0-9_-]+)\s+v?(\d+\.\d+\.\d+)", b)
        if not m:
            continue
        skill = m.group(1)
        if skill not in names:
            continue
        d = edges.setdefault(skill, {"depends_on": [], "used_by": []})
        for label, key in (("Dépend de", "depends_on"), ("Utilisé par", "used_by")):
            mm = re.search(r"\*\*" + label + r"\*\*\s*:(.+)", b)
            if not mm:
                continue
            for cand in re.findall(r"[a-zA-Z0-9_-]+", mm.group(1)):
                if cand in names and cand != skill and cand not in d[key]:
                    d[key].append(cand)
    return edges


def reach(edges, start, key):
    """Reachabilité transitive depuis start via le champ key (BFS déterministe)."""
    seen, stack = [], [start]
    while stack:
        cur = stack.pop()
        for nxt in edges.get(cur, {}).get(key, []):
            if nxt not in seen and nxt != start:
                seen.append(nxt)
                stack.append(nxt)
    return sorted(seen)


def verdict(n_backward):
    if n_backward >= 8:
        return "CRITIQUE"
    if n_backward >= 4:
        return "PRESSION"
    return "OK"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--target", help="skill cible (M3 — blast radius)")
    ap.add_argument("--graph", action="store_true", help="export complet du graphe")
    ap.add_argument("--json", action="store_true", help="sortie machine + rapport JSON")
    args = ap.parse_args()

    names = known_skills()
    edges = parse_kb(names)
    if not edges:
        print("ABANDON : KB introuvable ou vide (%s)" % KB)
        sys.exit(2)

    result = {"kb": os.path.relpath(KB, BASE), "nodes": len(edges), "edges": sum(len(v["depends_on"]) for v in edges.values())}

    if args.graph:
        result["graphe"] = {k: v for k, v in sorted(edges.items())}
        print("GRAPHE : %d nœuds / %d arêtes 'Dépend de'" % (result["nodes"], result["edges"]))
        for k in sorted(edges):
            if edges[k]["depends_on"] or edges[k]["used_by"]:
                print("  %-28s depend de %s | utilise par %s" % (k, edges[k]["depends_on"], edges[k]["used_by"]))
    elif args.target:
        t = args.target
        if t not in edges:
            print("ABANDON : cible inconnue du registre KB (%s)" % t)
            sys.exit(2)
        back = reach(edges, t, "used_by")  # qui liste t dans Utilisé par = dépend (direct)
        # backward transitif : X dépend de Y qui dépend de t
        for y in list(back):
            for z in reach(edges, y, "used_by"):
                if z != t and z not in back:
                    back.append(z)
        back = sorted(set(back))
        fwd = reach(edges, t, "depends_on")
        v = verdict(len(back))
        result.update({"target": t, "backward": back, "forward": fwd,
                       "blast_radius": len(back), "verdict": v})
        print("CIBLE : %s — blast radius (backward) = %d éléments, forward = %d" % (t, len(back), len(fwd)))
        print("BACKWARD : %s" % ", ".join(back) if back else "BACKWARD : (aucun)")
        print("FORWARD  : %s" % ", ".join(fwd) if fwd else "FORWARD  : (aucun)")
        print("VERDICT : %s (seuils : <4 OK / 4-7 PRESSION / >=8 CRITIQUE)" % v)
    else:
        ap.print_help()
        sys.exit(3)

    if args.json:
        with open(REPORT, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print("RAPPORT : %s" % os.path.relpath(REPORT, BASE))
    sys.exit(0)


if __name__ == "__main__":
    main()
