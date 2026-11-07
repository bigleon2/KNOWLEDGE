#!/usr/bin/env python3
"""Task 47 (e) — scan + réparation systématique de la collision §0 / from __future__.

Constat (G4, boucle E12-E13) : l'injection du bloc §0 CONTEXTE SYSTÈME (propagation
v1.7.18 puis re-propagations) a inséré un docstring AVANT le docstring descriptif de
scripts dont l'import `from __future__ import annotations` suivait — rendant ces
imports illégaux (SyntaxError). Cas trouvés et corrigés : garde-plan-genplan.py,
sync-instructions-ecosysteme.py (repo) ; task45-generer-preset-bridge.py (hôte,
masqué car TB-04 exécutait la copie saine du clone fddbe94).
Correctif élément (le test n'est PAS touché) : fusion des deux docstrings en UNE
docstring de module — l'import __future__ redevient légal (précédé de la seule
docstring). + recalage §0 v1.7.19 → v1.7.20 des fichiers réparés (cohérence corpus).
Scan : hôte scripts/ + repo scripts/ + tsi-toolkit/scripts + skills/*/scripts (2 arbres).
Idempotent : re-jeu = NO-OP (compile OK partout).
"""
import os
import sys

CIBLES = [
    "/home/z/my-project/scripts",
    "/home/z/my-project/work/KNOWLEDGE-b75a620/scripts",
    "/home/z/my-project/work/KNOWLEDGE-b75a620/tsi-toolkit/scripts",
    "/home/z/my-project/work/KNOWLEDGE-b75a620/skills",
    "/home/z/my-project/skills",
]

MARQUEUR = 'Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.\n"""\n\n"""'
REMPLACEMENT = 'Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.\n'


def liste_py(racine):
    if not os.path.isdir(racine):
        return []
    if racine.rstrip("/").endswith("/scripts") or racine.rstrip("/").endswith("tsi-toolkit/scripts"):
        return [os.path.join(racine, f) for f in sorted(os.listdir(racine)) if f.endswith(".py")]
    out = []
    for d in sorted(os.listdir(racine)):
        sd = os.path.join(racine, d, "scripts")
        if os.path.isdir(sd):
            out += [os.path.join(sd, f) for f in sorted(os.listdir(sd)) if f.endswith(".py")]
    return out


def casse_par_future(path):
    """True si le fichier ne compile pas à cause d'un import __future__ mal placé."""
    try:
        with open(path, encoding="utf-8") as f:
            compile(f.read(), path, "exec")
        return False
    except SyntaxError as e:
        return "from __future__" in str(e)


def main():
    vus, reparés = 0, []
    for racine in CIBLES:
        for p in liste_py(racine):
            vus += 1
            if not casse_par_future(p):
                continue
            with open(p, encoding="utf-8") as f:
                t = f.read()
            if MARQUEUR not in t:
                print("[ÉCHEC] %s — casse __future__ SANS marqueur de fusion — inspection manuelle" % p)
                sys.exit(1)
            t = t.replace(MARQUEUR, REMPLACEMENT, 1)
            t = t.replace("⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.19)",
                          "⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.20)", 1)
            with open(p, "w", encoding="utf-8") as f:
                f.write(t)
            with open(p, encoding="utf-8") as f:
                compile(f.read(), p, "exec")
            print("[RÉPARÉ] %s" % p)
            reparés.append(p)
    print("SCAN : %d fichiers .py — %d réparés" % (vus, len(reparés)))
    for p in reparés:
        if "/work/KNOWLEDGE-b75a620/" not in p:
            miroir = p.replace("/home/z/my-project/", "/home/z/my-project/work/KNOWLEDGE-b75a620/")
            if os.path.isfile(miroir) or "/scripts/" in p:
                os.makedirs(os.path.dirname(miroir), exist_ok=True)
                with open(p, "rb") as f:
                    data = f.read()
                if os.path.isfile(miroir):
                    with open(miroir, "rb") as f:
                        if f.read() == data:
                            continue
                with open(miroir, "wb") as f:
                    f.write(data)
                print("[MIROIR] hôte → dépôt : %s" % miroir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
