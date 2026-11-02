#!/usr/bin/env python3
"""Couverture multi-couches — matrice contrôles × couches.

Convergence avec la méthode du skill multi-shift-architect : chaque
contrôle physique est couvert sur chaque couche logique (BASE, SHIFT
gauche, SHIFT droit, sous-couches), aucune couche morte. Les couches
sont dérivées des conditions de modifiers (M1-M4) : un état de
modifiers distinct = une couche.
"""
from __future__ import annotations

from collections import defaultdict

MODS = ("M1", "M2", "M3", "M4")


def couches_de(mappings: list[dict]) -> list[str]:
    """Enumère les couches réellement référencées (états modifiers)."""
    vues = set()
    for m in mappings:
        etats = m.get("modifier") or {}
        cle = tuple(etats.get(k, 0) for k in MODS)
        vues.add(cle)
    def nom(cle):
        actifs = [f"{k}={v}" for k, v in zip(MODS, cle) if v]
        return "BASE" if not actifs else "+".join(actifs)
    return [nom(c) for c in sorted(vues)]


def matrice(mappings: list[dict]) -> dict:
    """Matrice contrôle × couche : entrées couvertes."""
    par_controle = defaultdict(set)
    for m in mappings:
        midi = m.get("midi")
        if not midi:
            continue
        etats = m.get("modifier") or {}
        cle = tuple(etats.get(k, 0) for k in MODS)
        actifs = [f"{k}={v}" for k, v in zip(MODS, cle) if v]
        couche = "BASE" if not actifs else "+".join(actifs)
        # contrôle physique approximé par l'événement MIDI (canal/message/n°)
        par_controle[(midi["canal"], midi["message"], midi["numero"])].add(couche)
    return {"controles": {f"{k[0]}/{k[1]}/{k[2]}": sorted(v)
                          for k, v in sorted(par_controle.items())},
            "couches": couches_de(mappings)}


def auditer(mappings: list[dict]) -> dict:
    """Audit de couverture : couches mortes et contrôles non couverts."""
    m = matrice(mappings)
    couches_utilisees = set()
    for couvertes in m["controles"].values():
        couches_utilisees.update(couvertes)
    couverture = {c: (c in couches_utilisees) for c in m["couches"]}
    mortes = [c for c, u in couverture.items() if not u]
    # un contrôle n'est couvert que sur ses couches actives ; signaler
    # les contrôles mono-couche (candidats à l'extension SHIFT)
    mono = [c for c, couches in m["controles"].items() if len(couches) == 1]
    return {"matrice": m, "couches_mortes": mortes,
            "controles_mono_couche": mono,
            "verdict": "PASS" if not mortes else "FAIL"}
