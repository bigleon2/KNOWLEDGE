#!/usr/bin/env python3
"""Convertisseurs — TSI ↔ JSON et CSV Pseudo-TSI → TSI.

Héritage des discussions : tsi_to_json.py (L4), csv_to_tsi_converter v1-v3
(L8). Le CSV Pseudo-TSI (séparateur `;`, encodage UTF-8) est le cahier des
charges tabulaire antérieur à l'implémentation — colonnes :

  Ligne;Phase;Ctrl_Physique;Section_Commande;Type;Interaction;Condition;
  MIDI_Channel;MIDI_Note_CC;MIDI_Type;Commentaire

Les numéros MIDI/CC sont convertis : canal 1-16 → 0-15, valeurs
hexadécimales acceptées (leçon L3 « valeurs CC en hexa »).
"""
from __future__ import annotations

import csv
import json
import re

from . import nixml
from . import presets as presets_mod

COLONNES_CSV = ["Ligne", "Phase", "Ctrl_Physique", "Section_Commande",
                "Type", "Interaction", "Condition", "MIDI_Channel",
                "MIDI_Note_CC", "MIDI_Type", "Commentaire"]

# Canonisation des sections Traktor réelles (Add Assignment) vers la
# taxonomie GROUP du format écosystème (tsi-validator E3) — la section
# d'origine est conservée dans le NOM du mapping (perte d'information nulle).
SECTIONS_CANONIQUES = {
    "Global": "Global", "MIDI Controls": "Global", "Loop Recorder": "Global",
    "Browser": "Global", "FX Unit 1": "Global", "FX Unit 2": "Global",
    "FX Unit 3": "Global", "FX Unit 4": "Global", "Master": "Master",
    "Mixer": "Mixer", "Remix Deck": "Focus", "Deck A": "Deck A",
    "Deck B": "Deck B", "Deck C": "Deck C", "Deck D": "Deck D",
    "Track Deck": "Focus",
}


def _nombre(brut: str) -> int:
    """Convertit '0x2C', '2C', '44' → entier (hexa toléré, leçon L3)."""
    brut = (brut or "").strip()
    if not brut:
        return 0
    if brut.lower().startswith("0x"):
        return int(brut, 16)
    if re.fullmatch(r"[0-9a-fA-F]{1,2}", brut) and any(
            c in "abcdefABCDEF" for c in brut):
        return int(brut, 16)
    return int(brut)


def _canal(brut: str) -> int:
    """Canal MIDI 1-16 → index 0-15."""
    n = _nombre(brut)
    return max(0, n - 1) if n >= 1 else 0


def _conditions(brut: str) -> dict:
    """'M1=1' / 'M3=0,M4=1' / '-' → dictionnaire de modifiers."""
    etats = {}
    for part in re.split(r"[,;]", brut or "-"):
        part = part.strip()
        m = re.fullmatch(r"(M[1-4])\s*=\s*([01])", part)
        if m:
            etats[m.group(1)] = int(m.group(2))
    return etats


def csv_vers_modele(chemin_csv: str, device: dict | None = None) -> dict:
    """Importe un CSV Pseudo-TSI → modèle canonique {device, mappings}."""
    with open(chemin_csv, encoding="utf-8-sig", newline="") as f:
        lignes = list(csv.reader(f, delimiter=";"))
    if not lignes:
        raise ValueError("CSV vide")
    entete = [c.strip() for c in lignes[0]]
    idx = {c: i for i, c in enumerate(entete)}
    for col in ("Ctrl_Physique", "Section_Commande", "Interaction"):
        if col not in idx:
            raise ValueError(f"Colonne CSV requise absente : {col} (entête : {entete})")
    mappings = []
    for n, ligne in enumerate(lignes[1:], start=2):
        if not ligne or not any(c.strip() for c in ligne):
            continue
        def cell(col):
            i = idx.get(col)
            return ligne[i].strip() if i is not None and i < len(ligne) else ""
        commande = cell("Section_Commande")
        # Section > Commande Traktor : 'Global > MIDI Controls > Modifier 1'
        parties = [p.strip() for p in commande.split(">")]
        controle = parties[-1]
        section = parties[0] if parties else "Global"
        groupe = SECTIONS_CANONIQUES.get(section, "Global")
        conditions = _conditions(cell("Condition"))
        suffixe = f" [{cell('Condition')}]" if conditions else ""
        mapping = {
            "nom": f"{cell('Ctrl_Physique')} — {commande}{suffixe}",
            "type": "IN",
            "groupe": groupe,
            "controle": controle,
        }
        if conditions:
            mapping["modifier"] = conditions
        if "MIDI_Channel" in idx and cell("MIDI_Channel") not in ("", "-"):
            mapping["midi"] = {
                "canal": _canal(cell("MIDI_Channel")),
                "message": "CC" if cell("MIDI_Type").upper() == "CC" else "NOTE",
                "numero": _nombre(cell("MIDI_Note_CC")) % 128,
                "mode": {"Hold": "Direct", "Toggle": "Toggle",
                         "Relative": "Increment", "Direct": "Direct"}
                        .get(cell("Interaction"), "Direct"),
            }
        mappings.append(mapping)
    return {
        "device": device or {
            "name": "Traktor Kontrol S4 MK2", "type": "MIDI",
            "in_port": "Traktor Kontrol S4 MK2 In",
            "out_port": "Traktor Kontrol S4 MK2 Out",
            "deck_target": "Focus",
        },
        "mappings": mappings,
    }


def csv_vers_tsi(chemin_csv: str, chemin_sortie: str) -> str:
    """CSV Pseudo-TSI → .tsi canonique (avec validation preset)."""
    modele = csv_vers_modele(chemin_csv)
    erreurs = presets_mod.valider(
        {"device": modele["device"], "mappings": modele["mappings"]})
    if erreurs:
        raise ValueError("CSV importé invalide : " + " ; ".join(erreurs[:5]))
    return nixml.ecrire(modele, chemin_sortie)


def tsi_vers_json(chemin_tsi: str, chemin_sortie: str | None = None) -> str:
    """TSI canonique → JSON (représentation intégrale)."""
    modele = nixml.lire_canonique(chemin_tsi)
    sortie = json.dumps(modele, ensure_ascii=False, indent=1) + "\n"
    if chemin_sortie:
        with open(chemin_sortie, "w", encoding="utf-8", newline="\n") as f:
            f.write(sortie)
        return chemin_sortie
    return sortie


def json_vers_tsi(chemin_json: str, chemin_sortie: str) -> str:
    """JSON → TSI canonique (inverse exact de tsi_vers_json)."""
    with open(chemin_json, encoding="utf-8") as f:
        modele = json.load(f)
    erreurs = presets_mod.valider(modele)
    if erreurs:
        raise ValueError("JSON invalide : " + " ; ".join(erreurs[:5]))
    return nixml.ecrire(modele, chemin_sortie)
