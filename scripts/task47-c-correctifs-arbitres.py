#!/usr/bin/env python3
"""⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.22)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""
"""Task 47 (c) — correctifs aux éléments d'arbitres (G4, boucle E12-E13 — jamais aux tests pour masquer).
1. garde-plan-genplan.py + sync-instructions-ecosysteme.py : fusion des docstrings doublés —
   l'injection §0 (propagation v1.7.18) avait inséré un docstring AVANT le docstring descriptif,
   rendant `from __future__ import annotations` illégal (SyntaxError, casse héritée constatée à
   HEAD — py_compile KO). Correctif : UNE seule docstring fusionnée (§0 + description), import
   __future__ redevient légal (précédé de la seule docstring de module).
2. test-coherence-interactions.py : recalibrage L004 2e édition — plage PM 1200-1500 → 1200-1560
   (croissance directive propriétaire : règle d'or n°7 [v3.33.0, 1511 L] + précision sémantique
   [v3.33.1, 1513 L] ; précédent recalibrage L004 2026-10-09 « croissance directive », PM v3.21.0
   = 1425 L ; la garde anti-dérive est conservée — borne haute 1560).
Substitutions verrouillées count==1 (abandon SANS écriture si dérive). Idempotent : re-jeu = NO-OP.
"""
import sys

BASE = "/home/z/my-project/work/KNOWLEDGE-b75a620"


def abandon(msg, code=1):
    print("[ABANDON] %s" % msg)
    sys.exit(code)


def lire(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def sub(text, motif, remplace, n, label):
    c = text.count(motif)
    if c != n:
        abandon("motif [%s] trouvé %d fois (attendu %d) : %r" % (label, c, n, motif[:70]))
    return text.replace(motif, remplace)


def fusion_docstrings(path):
    """Fusionne docstring §0 + docstring descriptive en UNE docstring de module."""
    t = lire(path)
    marqueur = 'Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.\n"""\n\n"""'
    if marqueur not in t:
        print("[NO-OP] %s — docstrings déjà fusionnées" % path.split("/")[-1])
        return
    t = sub(t, marqueur,
            "Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.\n",
            1, "fusion docstrings %s" % path.split("/")[-1])
    with open(path, "w", encoding="utf-8") as f:
        f.write(t)
    print("[OK] docstrings fusionnées : %s" % path)


def main():
    # --- 1. Fusion docstrings (2 scripts cassés par l'injection §0) ---
    fusion_docstrings(BASE + "/scripts/garde-plan-genplan.py")
    fusion_docstrings(BASE + "/scripts/sync-instructions-ecosysteme.py")

    # --- 2. Recalibrage plage PM (L004 2e édition — croissance directive) ---
    p = BASE + "/scripts/test-coherence-interactions.py"
    t = lire(p)
    old = ("pm_ok = bool(pm_file) and pm_gv in pm_text[:600] and 1200 <= pm_text.count(\"\\n\") + 1 <= 1500"
           "  # recalibrage L004 (web-b93f42fa, 2026-10-09) : PM v3.21.0 = 1425 L"
           " (bloc KO-L004 v1.1.0, croissance directive)")
    new = ("pm_ok = bool(pm_file) and pm_gv in pm_text[:600] and 1200 <= pm_text.count(\"\\n\") + 1 <= 1560"
           "  # recalibrage L004 2e éd. (session web-6058b3ba, 2026-11-04, Task 47) : croissance directive"
           " propriétaire — règle d'or n°7 [v3.33.0, 1511 L] + précision sémantique [v3.33.1, 1513 L] ;"
           " 1er recalibrage L004 (web-b93f42fa, 2026-10-09) : PM v3.21.0 = 1425 L"
           " (bloc KO-L004 v1.1.0, croissance directive)")
    if "1200 <= pm_text.count" not in t:
        abandon("ligne plage PM introuvable dans l'arbitre cohérence")
    if old not in t:
        if new in t:
            print("[NO-OP] plage PM déjà recalibrée 1200-1560")
        else:
            abandon("motif plage PM non conforme (ni ancien ni nouveau)")
    else:
        t = sub(t, old, new, 1, "plage PM L004 2e éd.")
        with open(p, "w", encoding="utf-8") as f:
            f.write(t)
        print("[OK] plage PM recalibrée : 1200-1500 → 1200-1560 (L004 2e éd., croissance directive)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
