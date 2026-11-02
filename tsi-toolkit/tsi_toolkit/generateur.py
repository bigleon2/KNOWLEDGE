#!/usr/bin/env python3
"""Générateur TSI — preset JSON → fichier .tsi canonique.

Déterministe par construction (R6) : un preset donné produit toujours
le même XML byte-identique. Anti-conflits intégré (karnaugh) : option
``verifier_conflits=True`` refuse de générer un mapping en conflit.
"""
from __future__ import annotations

from . import karnaugh
from . import nixml
from . import presets as presets_mod


def generer(chemin_preset: str, chemin_sortie: str,
            verifier_conflits: bool = True) -> str:
    """Génère un .tsi depuis un preset. Retourne le chemin de sortie."""
    preset = presets_mod.charger(chemin_preset)
    modele = {"device": preset["device"], "mappings": preset["mappings"]}
    if verifier_conflits:
        conflits = karnaugh.detecter(modele["mappings"])
        if conflits:
            resume = " ; ".join(
                f"{c['type']}: {c['detail']}" for c in conflits[:5])
            raise ValueError(
                f"{len(conflits)} conflit(s) détecté(s) — génération refusée "
                f"(voir tsi_toolkit.karnaugh) : {resume}")
    return nixml.ecrire(modele, chemin_sortie)
