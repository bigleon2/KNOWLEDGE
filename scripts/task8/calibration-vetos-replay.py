#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 8 G4 — calibration voie M des 2 dérives de replay (contingence D008).

Mécanisme canon Task 30 (Option A — vetos exclusifs) : champ `exclusifs` par cas
de trigger_evals — termes réservés d'AUTRES skills/générations, veto appliqué
AVANT le scoring.

Dérives résorbées :
  1. vue-upload — cas négatif « Réinstalle la dernière version du skill gen-plan. »
     trigger_m=true via le radical « vers » (description v1.5.0 : hygiène des
     VERSIONS — addition pure R2, jamais retirer le cœur de la feature) →
     veto « réinstalle » (terme réservé réinstallation = gen-plan/PM-INSTALL).
  2. livraison-garantie — cas négatif « Ouvre-moi simplement le portail des
     livrables, je vais regarder moi-même. » trigger_m=true via « livr »+« portail »
     (MACRO vue-upload — frontière de déclenchement v1.3.0) →
     veto « portail » (terme réservé portail = vue-upload).

Idempotent : re-jeu = aucun changement (champ déjà présent = inchangé).
"""
import json

CALIBRATIONS = {
    "/home/z/my-project/skills/vue-upload/evals/trigger_evals.json": [
        ("Réinstalle la dernière version du skill gen-plan.", ["réinstalle"]),
    ],
    "/home/z/my-project/skills/livraison-garantie/evals/trigger_evals.json": [
        ("Ouvre-moi simplement le portail des livrables, je vais regarder moi-même.",
         ["portail"]),
    ],
}


def applique(path, regles):
    with open(path, encoding="utf-8") as f:
        cas = json.load(f)
    n = 0
    for query, exclusifs in regles:
        for c in cas:
            if c.get("query") == query:
                if c.get("exclusifs") != exclusifs:
                    c["exclusifs"] = exclusifs
                    n += 1
    with open(path, "w", encoding="utf-8") as f:
        json.dump(cas, f, ensure_ascii=False, indent=1)
    return n


def main():
    total = 0
    for path, regles in CALIBRATIONS.items():
        n = applique(path, regles)
        total += n
        print("  %s — %d cas calibré(s)" % (path.split("skills/")[1], n))
    print("vétos posés :", total, "(idempotent si 0 au re-jeu)")


if __name__ == "__main__":
    main()
