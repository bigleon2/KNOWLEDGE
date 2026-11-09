#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Hygiène mode-bits racinaire écosystème (Task 85 G1).

Normalise les permissions des FICHIERS de l'écosystème (hôte + dépôt) à la
convention canonique 0o644 (établie Task 83 G1 : dépôt 100644 partout),
éteignant à la SOURCE le drift récurrent 100755 transporté par les cp
hôte->dépôt (miroirs livrables, syncs worklog/plan/rapport).

- Répertoires : intacts (755).
- .git/ : exclu (intégrité git interne).
- Idempotent : un 2e passage = 0 normalisation.
- stdlib uniquement, aucun réseau, zéro contenu modifié (chmod seul).

Sortie : rapport JSON (stdout) + exit 0.
"""

import json
import os
import sys

HOTE = "/home/z/my-project"
DEPOT = "/home/z/my-project/KNOWLEDGE-repo"

ZONES_HOTE = ["scripts", "download", "skills", "upload"]
ZONES_DEPOT = ["skills", "scripts", "download"]

EXCLUSIONS = {".git", "__pycache__", "node_modules"}


def normaliser(racine, zones):
    """chmod 0o644 tous les fichiers des zones, retourne la liste des changements."""
    changes = []
    for zone in zones:
        base = os.path.join(racine, zone)
        if not os.path.isdir(base):
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [d for d in dirnames if d not in EXCLUSIONS]
            for name in filenames:
                chemin = os.path.join(dirpath, name)
                try:
                    mode = os.lstat(chemin).st_mode
                except OSError:
                    continue
                if os.path.islink(chemin):
                    continue
                if mode & 0o111:
                    os.chmod(chemin, 0o644)
                    changes.append(os.path.relpath(chemin, racine))
    return changes


def main():
    ch_hote = normaliser(HOTE, ZONES_HOTE)
    ch_depot = normaliser(DEPOT, ZONES_DEPOT)
    rapport = {
        "script": "eco-hygiene-mode-bits",
        "convention": "0o644 fichiers (Task 83 G1, récurrence éteinte à la source)",
        "hote_normalises": len(ch_hote),
        "depot_normalises": len(ch_depot),
        "echantillon_hote": sorted(ch_hote)[:12],
        "echantillon_depot": sorted(ch_depot)[:12],
        "idempotent": True,
    }
    print(json.dumps(rapport, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
