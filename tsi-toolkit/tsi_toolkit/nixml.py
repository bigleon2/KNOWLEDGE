#!/usr/bin/env python3
"""Parser/sérialiseur TSI — 3 familles de formats réels.

1. Format CANONIQUE écosystème (génération) : racine NISYSTEM ou NIXML,
   DEVICE/MAPPINGS/MAPPING[/MODIFIER]/MIDI[/LED] — format validé par
   l'arbitre tsi-validator (bi-racine).
2. Format RÉEL Traktor (mapping contrôleur) : NIXML > TraktorSettings >
   Entry[@Name='DeviceIO.Config.Controller'] avec blob DIOM base64.
3. Format RÉEL réglages complets : NIXML > TraktorSettings > centaines
   d'Entry (le mapping contrôleur est une Entry parmi les autres).

Python stdlib uniquement. Aucune duplication du décodage DIOM (R4) :
l'inspection des blobs délègue à l'analyseur écosystème quand il est
présent (pont), sinon se limite au relevé textuel.
"""
from __future__ import annotations

import base64
import os
import re
import xml.etree.ElementTree as ET

RACINES_CANONIQUES = {"NISYSTEM", "NIXML"}
ENTREE_CONTROLEUR = "DeviceIO.Config.Controller"


def _texte(elem) -> str:  # noqa: ANN001 - ElementTree
    return (elem.text or "").strip() if elem is not None else ""


def detecter_format(chemin: str) -> dict:
    """Identifie la famille de format d'un fichier .tsi."""
    with open(chemin, "rb") as f:
        debut = f.read(4096)
    racine_txt = re.search(rb"<(\w+)", debut)
    racine = racine_txt.group(1).decode("ascii", "replace") if racine_txt else "?"
    if racine not in RACINES_CANONIQUES:
        return {"famille": "INCONNU", "racine": racine}
    with open(chemin, "rb") as f:
        contenu = f.read()
    if b"<TraktorSettings" in contenu[:4096] or b"TraktorSettings" in debut:
        # réel : réglages (avec ou sans mapping contrôleur embarqué)
        a_controleur = ENTREE_CONTROLEUR.encode() in contenu
        return {"famille": "REGLAGES" if not a_controleur else "REEL_DDIOM",
                "racine": racine, "controleur": a_controleur}
    return {"famille": "CANONIQUE", "racine": racine}


def _mapping_vers_dict(mp) -> dict:  # noqa: ANN001
    entree = {
        "nom": mp.get("NAME", ""),
        "type": mp.get("TYPE", "IN"),
        "groupe": mp.get("GROUP", ""),
        "controle": mp.get("CONTROL", ""),
    }
    mod = mp.find("MODIFIER")
    if mod is not None:
        entree["modifier"] = {k: int(v) for k, v in mod.attrib.items()}
    midi = mp.find("MIDI")
    if midi is not None:
        entree["midi"] = {
            "canal": int(midi.get("CHANNEL", "0")),
            "message": midi.get("MESSAGE", "NOTE"),
            "numero": int(midi.get("NUMBER", "0")),
            "mode": midi.get("MODE", "Direct"),
        }
    led = mp.find("LED")
    if led is not None:
        entree["led"] = {
            "numero": int(led.get("NUMBER", "0")),
            "on": int(led.get("ON", "127")),
            "off": int(led.get("OFF", "0")),
        }
    return entree


def lire_canonique(chemin: str) -> dict:
    """Lit un TSI canonique → modèle {device, mappings}."""
    racine = ET.parse(chemin).getroot()
    device = racine.find("DEVICE")
    if device is None:
        raise ValueError("Pas d'élément DEVICE dans le TSI canonique")
    mappings = [_mapping_vers_dict(mp)
                for mp in device.findall("MAPPINGS/MAPPING")]
    return {
        "device": {
            "name": device.get("NAME", ""),
            "type": device.get("TYPE", "MIDI"),
            "in_port": device.get("IN_PORT", ""),
            "out_port": device.get("OUT_PORT", ""),
            "deck_target": device.get("DECK_TARGET", "Focus"),
        },
        "mappings": mappings,
    }


def lire_reel(chemin: str) -> dict:
    """Lit un TSI réel (TraktorSettings) → relevé textuel + métadonnées blob.

    Le décodage DIOM (DCBM/CMAD) N'EST PAS dupliqué (R4) : cette fonction
    relève les Entry DeviceIO.Config.* (nom device, taille blob décodée)
    et délègue le détail à l'analyseur écosystème via le pont
    ``validateur.pont_analyseur``.
    """
    racine = ET.parse(chemin).getroot()
    entrees = racine.findall(".//Entry")
    releve = {"famille": "REEL", "entrees": len(entrees), "controleurs": []}
    for e in entrees:
        nom = e.get("Name", "")
        if nom.startswith("DeviceIO.Config.") and e.get("Type") == "3":
            valeur = e.get("Value", "")
            try:
                blob = base64.b64decode(valeur)
                taille = len(blob)
                # le nom du device est en UTF-16LE dans le blob (structure DIOM)
                apercu = ""
                m = re.search(rb"(?:[\x20-\x7e]\x00){6,}", blob)
                if m:
                    apercu = m.group(0).decode("utf-16-le", "replace")
            except Exception:  # noqa: BLE001
                taille, apercu = 0, ""
            releve["controleurs"].append({
                "entree": nom, "blob_octets": taille, "device_aperçu": apercu,
            })
    return releve


def inspecter(chemin: str, pont: bool = True) -> dict:
    """Inspection multi-format : détection + lecture adaptée."""
    fmt = detecter_format(chemin)
    resultat = {"fichier": chemin, "format": fmt}
    if fmt["famille"] == "CANONIQUE":
        modele = lire_canonique(chemin)
        resultat.update(modele)
        resultat["nb_mappings"] = len(modele["mappings"])
    elif fmt["famille"] in ("REEL_DDIOM", "REGLAGES"):
        resultat.update(lire_reel(chemin))
    if pont and fmt["famille"] in ("REEL_DDIOM", "REGLAGES"):
        from .validateur import pont_analyseur
        detail = pont_analyseur(chemin)
        if detail is not None:
            resultat["analyseur_ecosysteme"] = detail
    return resultat


def serialiser(modele: dict) -> str:
    """Sérialise {device, mappings} → XML canonique (déterministe)."""
    lignes = ['<?xml version="1.0" encoding="UTF-8"?>',
              "<NISYSTEM VERSION=\"1\">"]
    dev = modele["device"]
    attributs = [f'NAME="{dev["name"]}"', f'TYPE="{dev.get("type", "MIDI")}"',
                 f'IN_PORT="{dev.get("in_port", "")}"',
                 f'OUT_PORT="{dev.get("out_port", "")}"']
    if dev.get("deck_target"):
        attributs.append(f'DECK_TARGET="{dev["deck_target"]}"')
    lignes.append("  <DEVICE " + " ".join(attributs) + ">")
    mappings = modele["mappings"]
    lignes.append(f'    <MAPPINGS COUNT="{len(mappings)}">')
    for m in mappings:
        attrs = (f'NAME="{m["nom"]}" TYPE="{m.get("type", "IN")}" '
                 f'GROUP="{m["groupe"]}" CONTROL="{m["controle"]}"')
        corps = []
        if "modifier" in m:
            mods = " ".join(f'{k}="{v}"' for k, v in sorted(m["modifier"].items()))
            corps.append(f"      <MODIFIER {mods}/>")
        if "midi" in m:
            mid = m["midi"]
            corps.append(
                "      <MIDI CHANNEL=\"{canal}\" MESSAGE=\"{message}\" "
                "NUMBER=\"{numero}\" MODE=\"{mode}\"/>".format(**mid))
        if "led" in m:
            led = m["led"]
            corps.append(
                "      <LED NUMBER=\"{numero}\" ON=\"{on}\" OFF=\"{off}\" "
                "MODE=\"Output\"/>".format(**led))
        if corps:
            lignes.append(f"    <MAPPING {attrs}>")
            lignes.extend(corps)
            lignes.append("    </MAPPING>")
        else:
            lignes.append(f"    <MAPPING {attrs}/>")
    lignes.append("    </MAPPINGS>")
    lignes.append("  </DEVICE>")
    lignes.append("</NISYSTEM>")
    return "\n".join(lignes) + "\n"


def ecrire(modele: dict, chemin: str) -> str:
    """Écrit le modèle dans un fichier TSI canonique (déterministe)."""
    with open(chemin, "w", encoding="utf-8", newline="\n") as f:
        f.write(serialiser(modele))
    return chemin
