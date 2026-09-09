#!/usr/bin/env python3
"""check-corps-phase2.py — Vérification exhaustive post-Phase 2 (session B5).

Confirme que la standardisation frontmatter (fix-frontmatter.py + E13
repair-frontmatter-yaml.py) n'a touché QUE la zone frontmatter des SKILL.md :
pour chaque skill présent dans le backup pré-Phase-2
(tool-results/backup-skills-pre-phase2.tar.gz), le CORPS du fichier
(contenu après le frontmatter fermant, espacements de tête normalisés)
doit être byte-identique entre backup et état courant.

Usage : python3 scripts/check-corps-phase2.py
"""

import os
import tarfile

BASE = "/home/z/my-project"
BACKUP = os.path.join(BASE, "tool-results", "backup-skills-pre-phase2.tar.gz")


def body(content):
    try:
        return content[content.index("---", 3) + 3:].lstrip("\n")
    except ValueError:
        return content


def main():
    tar = tarfile.open(BACKUP, "r:gz")
    total, divergents = 0, []
    for m in tar.getmembers():
        if not (m.isfile() and m.name.endswith("/SKILL.md")):
            continue
        total += 1
        old = tar.extractfile(m).read().decode("utf-8")
        path = os.path.join(BASE, m.name)
        if not os.path.isfile(path):
            divergents.append(f"{m.name}: absent de l'état courant")
            continue
        with open(path, encoding="utf-8") as f:
            new = f.read()
        if body(old) != body(new):
            divergents.append(m.name)
    tar.close()
    print(f"SKILL.md comparés backup <-> courant : {total}")
    if divergents:
        print(f"CORPS DIVERGENTS ({len(divergents)}) : {divergents}")
        return 1
    print("CORPS : 100 % byte-identiques — la Phase 2 n'a touché que le frontmatter.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
