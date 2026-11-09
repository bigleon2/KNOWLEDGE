#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 8 G1 — ajout des evals VU-7 (hygiène versions) et VU-8 (push archivage)
à skills/vue-upload/evals/evals.json. Idempotent : re-jeu = aucun doublon."""

import json

P = "/home/z/my-project/skills/vue-upload/evals/evals.json"

VU11 = {
    "id": "VU-11",
    "objectif": ("hygiène des versions (v1.5.0) — la sous-commande versions détecte les "
                 "familles multi-versions (radical purgé des motifs _vN/V1/final/nouvelle/"
                 "copie/(N)), les suspects au nom proche (1er token commun) et le contenu "
                 "des dossiers download/archive/ et upload/archive/"),
    "verdict": "PASS (test-vue-upload-v150.py, 2026-10-31)",
}

VU12 = {
    "id": "VU-12",
    "objectif": ("push avec archivage automatique (v1.5.0) — au push d'une nouvelle version, "
                 "les supersédées (même radical) sont déplacées vers <dir>/archive/ (une seule "
                 "version reste en listing), no-op honnête si aucune, --no-archive désactive, "
                 "l'épinglé ★ est conservé et signalé, suspects au nom proche listés sans "
                 "archivage, codes retour inchangés"),
    "verdict": "PASS (test-vue-upload-v150.py, 2026-10-31)",
}


def main():
    with open(P, encoding="utf-8") as f:
        j = json.load(f)
    ids = {e["id"] for e in j["evals"]}
    ajoutes = []
    for e in (VU11, VU12):
        if e["id"] not in ids:
            j["evals"].append(e)
            ajoutes.append(e["id"])
    with open(P, "w", encoding="utf-8") as f:
        json.dump(j, f, ensure_ascii=False, indent=1)
    print("evals actuels :", [e["id"] for e in j["evals"]])
    print("ajoutés :", ajoutes if ajoutes else "aucun (idempotent)")


if __name__ == "__main__":
    main()
