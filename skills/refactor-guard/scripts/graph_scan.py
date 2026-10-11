#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
graph_scan.py — Scan de graphe d'imports et de complexité (H02) — refactor-guard v1.0.0.

Analyse statique Python via `ast` (stdlib uniquement — N3, aucun networkx requis) :
  - nœuds : fichiers .py d'un répertoire cible
  - arêtes : imports internes (module -> module, résolu par nom de fichier)
  - métriques par fichier : lignes, fonctions/classes, complexité cyclomatique
    approximée (1 + nb points de branchement if/for/while/and/or/except/assert/with),
    couplage (nb d'imports internes sortants + entrants)
  - cycles : détection par DFS (Tarjan simplifié — composantes fortement connexes)
  - scores de centralité : degré entrant (fan-in) / sortant (fan-out)

Sortie JSON compatible avec le format d'entrée de risk_score.py (métriques par
fichier -> cyclomatic_complexity / coupling). Self-test intégré (--self-test).
Usage :
    python3 graph_scan.py <repertoire_cible> [--json] [--self-test]
"""
import ast
import json
import os
import sys
from collections import defaultdict

BRANCHEMENTS = (ast.If, ast.For, ast.While, ast.ExceptHandler, ast.Assert, ast.IfExp)

def complexite_fichier(arbre: ast.AST) -> int:
    """Complexité cyclomatique approximée : 1 + nb de branchements (+ booléens)."""
    c = 1
    for noeud in ast.walk(arbre):
        if isinstance(noeud, BRANCHEMENTS):
            c += 1
        elif isinstance(noeud, ast.BoolOp):
            c += len(noeud.values) - 1
    return c

def scanner(repertoire: str) -> dict:
    repertoire = os.path.abspath(repertoire)
    fichiers, imports, metriques = {}, defaultdict(set), {}
    for racine, _dirs, noms in os.walk(repertoire):
        _dirs[:] = [d for d in _dirs if d not in (".git", "__pycache__", "node_modules", "backups")]
        for nom in noms:
            if nom.endswith(".py"):
                chemin = os.path.join(racine, nom)
                fichiers[nom[:-3]] = chemin
    for mod, chemin in fichiers.items():
        try:
            with open(chemin, encoding="utf-8", errors="replace") as f:
                arbre = ast.parse(f.read())
        except SyntaxError as exc:
            metriques[mod] = {"erreur": f"syntaxe invalide : {exc.msg}"}
            continue
        nb_lignes = sum(1 for _ in open(chemin, encoding="utf-8", errors="replace"))
        n_fonctions = sum(isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) for n in ast.walk(arbre))
        n_classes = sum(isinstance(n, ast.ClassDef) for n in ast.walk(arbre))
        for noeud in ast.walk(arbre):
            if isinstance(noeud, ast.Import):
                for alias in noeud.names:
                    base = alias.name.split(".")[0]
                    if base in fichiers and base != mod:
                        imports[mod].add(base)
            elif isinstance(noeud, ast.ImportFrom) and noeud.module:
                base = noeud.module.split(".")[0]
                if base in fichiers and base != mod:
                    imports[mod].add(base)
        metriques[mod] = {
            "lignes": nb_lignes,
            "fonctions": n_fonctions,
            "classes": n_classes,
            "cyclomatic_complexity": complexite_fichier(arbre),
        }
    for mod, cibles in imports.items():
        metriques.setdefault(mod, {})["fan_out"] = len(cibles)
        for cible in cibles:
            metriques.setdefault(cible, {})["fan_in"] = \
                metriques.setdefault(cible, {}).get("fan_in", 0) + 1
    for mod, m in metriques.items():
        m.setdefault("fan_in", 0)
        m.setdefault("fan_out", 0)
        m["coupling"] = m["fan_in"] + m["fan_out"]
    # cycles par DFS (composantes fortement connexes — Tarjan simplifié)
    cycles = trouver_cycles(imports)
    return {"repertoire": repertoire, "nb_fichiers": len(fichiers),
            "aretes": {m: sorted(s) for m, s in sorted(imports.items())},
            "cycles": cycles, "metriques": metriques}

def trouver_cycles(graphe: dict) -> list:
    """Composantes fortement connexes de taille > 1 (Tarjan itératif léger)."""
    index, bas, pile, sur_pile, cycles, compteur = {}, {}, [], set(), [], [0]
    for depart in graphe:
        if depart in index:
            continue
        travail = [(depart, iter(graphe[depart]))]
        index[depart] = bas[depart] = compteur[0] ; compteur[0] += 1
        pile.append(depart) ; sur_pile.add(depart)
        while travail:
            noeud, voisins = travail[-1]
            avance = False
            for v in voisins:
                if v not in graphe:
                    continue
                if v not in index:
                    index[v] = bas[v] = compteur[0] ; compteur[0] += 1
                    pile.append(v) ; sur_pile.add(v)
                    travail.append((v, iter(graphe.get(v, ()))))
                    avance = True
                    break
                elif v in sur_pile:
                    bas[noeud] = min(bas[noeud], index[v])
            if avance:
                continue
            if bas[noeud] == index[noeud]:
                composante = []
                while True:
                    w = pile.pop() ; sur_pile.discard(w) ; composante.append(w)
                    if w == noeud:
                        break
                if len(composante) > 1:
                    cycles.append(sorted(composante))
            travail.pop()
            if travail:
                parent = travail[-1][0]
                bas[parent] = min(bas[parent], bas[noeud])
    return cycles

def _self_test() -> int:
    import shutil
    import tempfile
    base = tempfile.mkdtemp(prefix="graph-scan-test-")
    try:
        # a.py -> b.py -> c.py -> a.py (cycle) ; sain.py isolé
        open(os.path.join(base, "a.py"), "w").write("import b\n\ndef f():\n    if True:\n        return 1\n")
        open(os.path.join(base, "b.py"), "w").write("import c\n\ndef g():\n    return 2\n")
        open(os.path.join(base, "c.py"), "w").write("import a\n\ndef h():\n    return 3\n")
        open(os.path.join(base, "sain.py"), "w").write("def ok():\n    return 0\n")
        res = scanner(base)
        tests = [
            ("T1 nb_fichiers", res["nb_fichiers"] == 4),
            ("T2 cycle détecté", len(res["cycles"]) == 1 and set(res["cycles"][0]) == {"a", "b", "c"}),
            ("T3 fan-out a", res["metriques"]["a"]["fan_out"] == 1),
            ("T4 fan-in a", res["metriques"]["a"]["fan_in"] == 1),
            ("T5 complexité a", res["metriques"]["a"]["cyclomatic_complexity"] == 2),
            ("T6 sain sans cycle", res["metriques"]["sain"]["coupling"] == 0
             and all("sain" not in c for c in res["cycles"])),
            ("T7 déterminisme", scanner(base)["metriques"] == res["metriques"]),
        ]
        ok = True
        for nom, bon in tests:
            print(f"{nom}: [{'PASS' if bon else 'FAIL'}]")
            ok = ok and bon
        print("SELF-TEST :", "PASS (7/7)" if ok else "FAIL")
        return 0 if ok else 1
    finally:
        shutil.rmtree(base, ignore_errors=True)

def main() -> int:
    argv = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--self-test" in sys.argv:
        return _self_test()
    if not argv or not os.path.isdir(argv[0]):
        print(__doc__)
        return 64
    res = scanner(argv[0])
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    sys.exit(main())
