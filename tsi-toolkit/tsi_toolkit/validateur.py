#!/usr/bin/env python3
"""Validateur TSI — contrôles internes + pont vers l'arbitre écosystème.

Deux niveaux :
  * INTERNE (toujours disponible, autonome — ENF-07) : structure, plages,
    LED, modifiers (sous-ensemble des règles E1-E8 de tsi-validator) ;
  * PONT (quand l'écosystème est présent) : délègue le verdict complet à
    ``skills/tsi-validator/scripts/valider-tsi.py`` (R4 — jamais de
    duplication de l'arbitre) et fusionne.

L'inspection des TSI réels (blob DIOM) délègue de la même façon à
``skills/analyse-doc-s4mk2/scripts/analyser_tsi_mk2.py``.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

RACINES_EXPLORATION = [
    os.path.join(os.path.dirname(__file__), "..", "..", "skills"),
    os.path.join(os.path.dirname(__file__), "..", "skills"),
    "skills",
]


def _chemin_ecosysteme(relatif: str) -> str | None:
    for base in RACINES_EXPLORATION:
        chemin = os.path.normpath(os.path.join(base, relatif))
        if os.path.isfile(chemin):
            return chemin
    return None


def pont_analyseur(chemin_tsi: str) -> dict | None:
    """Décode un TSI réel via l'analyseur écosystème (R4 — pont)."""
    script = _chemin_ecosysteme(
        "analyse-doc-s4mk2/scripts/analyser_tsi_mk2.py")
    if script is None:
        return None
    sortie_json = chemin_tsi + ".analyse.json"
    try:
        subprocess.run(
            [sys.executable, script, chemin_tsi, "--json", sortie_json],
            capture_output=True, text=True, timeout=120, check=True)
        with open(sortie_json, encoding="utf-8") as f:
            detail = json.load(f)
        return {k: detail.get(k) for k in (
            "device", "ddic", "comptes", "noms_commandes_lisibles")}
    except Exception as exc:  # noqa: BLE001
        return {"erreur": repr(exc)}
    finally:
        if os.path.exists(sortie_json):
            os.remove(sortie_json)


def pont_validateur(chemin_tsi: str) -> dict | None:
    """Verdict complet via l'arbitre tsi-validator (R4 — pont)."""
    script = _chemin_ecosysteme("tsi-validator/scripts/valider-tsi.py")
    if script is None:
        return None
    try:
        r = subprocess.run([sys.executable, script, chemin_tsi],
                           capture_output=True, text=True, timeout=120)
        return {"code_retour": r.returncode, "sortie": r.stdout[-2000:]}
    except Exception as exc:  # noqa: BLE001
        return {"erreur": repr(exc)}


def valider_interne(chemin_tsi: str) -> dict:
    """Contrôles internes autonomes (sous-ensemble E1-E8)."""
    from . import nixml
    problems = []
    fmt = nixml.detecter_format(chemin_tsi)
    if fmt["famille"] != "CANONIQUE":
        return {"famille": fmt["famille"], "verdict": "HORS_CANONIQUE",
                "problemes": [f"format {fmt['famille']} — utiliser le pont"]}
    try:
        modele = nixml.lire_canonique(chemin_tsi)
    except Exception as exc:  # noqa: BLE001
        return {"famille": "CANONIQUE", "verdict": "FAIL",
                "problemes": [f"lecture impossible : {exc!r}"]}
    mappings = modele["mappings"]
    if not mappings:
        problems.append("aucun mapping")
    # Karnaugh = contrôle consultatif (plus strict que l'arbitre E5 :
    # même événement + états CHEVAUCHANTS) — signalé sans bloquer,
    # l'arbitre écosystème reste la source de vérité du verdict.
    from . import karnaugh
    avertissements = [f"{c['type']}: {c['detail']}"
                      for c in karnaugh.detecter(mappings)]
    for i, m in enumerate(mappings):
        midi = m.get("midi")
        if midi:
            if not 0 <= midi["canal"] <= 15:
                problems.append(f"mapping[{i}] canal {midi['canal']} hors [0,15]")
            if not 0 <= midi["numero"] <= 127:
                problems.append(f"mapping[{i}] numéro {midi['numero']} hors [0,127]")
            if midi["message"] not in ("NOTE", "CC"):
                problems.append(f"mapping[{i}] message {midi['message']} inconnu")
    return {
        "famille": "CANONIQUE", "nb_mappings": len(mappings),
        "verdict": "PASS" if not problems else "FAIL",
        "problemes": problems,
        "avertissements": avertissements,
    }


def valider(chemin_tsi: str, pont: bool = True) -> dict:
    """Validation complète : interne + pont écosystème (verdict final =
    pire des verdicts disponibles)."""
    resultat = valider_interne(chemin_tsi)
    if pont:
        arbitre = pont_validateur(chemin_tsi)
        if arbitre is not None:
            resultat["arbitre_ecosysteme"] = arbitre
            if arbitre.get("code_retour") not in (0, None):
                resultat["verdict"] = "FAIL"
    return resultat
