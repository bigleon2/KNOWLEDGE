#!/usr/bin/env python3
"""Presets TSI — chargement et validation de schéma.

Un preset est un JSON {meta, device, mappings} — source d'entrée du
générateur. Validation stricte : canaux 0-15, numéros 0-127, messages
NOTE/CC, modifiers M1-M4 binaires (limite native Traktor — leçon L8).
"""
from __future__ import annotations

import json

MESSAGES = {"NOTE", "CC"}
MODS_VALIDES = {"M1", "M2", "M3", "M4"}


def charger(chemin: str) -> dict:
    with open(chemin, encoding="utf-8") as f:
        preset = json.load(f)
    erreurs = valider(preset)
    if erreurs:
        raise ValueError("Preset invalide : " + " ; ".join(erreurs))
    return preset


def valider(preset: dict) -> list[str]:
    """Retourne la liste (vide si OK) des violations de schéma."""
    erreurs = []
    for cle in ("device", "mappings"):
        if cle not in preset:
            erreurs.append(f"clé manquante : {cle}")
    if erreurs:
        return erreurs
    dev = preset["device"]
    if not dev.get("name"):
        erreurs.append("device.name requis")
    if not isinstance(preset["mappings"], list) or not preset["mappings"]:
        erreurs.append("mappings : liste non vide requise")
        return erreurs
    for i, m in enumerate(preset["mappings"]):
        p = f"mappings[{i}]"
        if not m.get("nom"):
            erreurs.append(f"{p}.nom requis")
        if m.get("type", "IN") not in {"IN", "OUT"}:
            erreurs.append(f"{p}.type ∈ {{IN, OUT}}")
        if not m.get("controle"):
            erreurs.append(f"{p}.controle requis")
        midi = m.get("midi")
        if midi is not None:
            if midi.get("message") not in MESSAGES:
                erreurs.append(f"{p}.midi.message ∈ {sorted(MESSAGES)}")
            if not 0 <= int(midi.get("canal", 0)) <= 15:
                erreurs.append(f"{p}.midi.canal ∈ [0,15]")
            if not 0 <= int(midi.get("numero", 0)) <= 127:
                erreurs.append(f"{p}.midi.numero ∈ [0,127]")
        for k, v in (m.get("modifier") or {}).items():
            if k not in MODS_VALIDES:
                erreurs.append(f"{p}.modifier.{k} ∈ {sorted(MODS_VALIDES)}")
            if int(v) not in (0, 1):
                erreurs.append(f"{p}.modifier.{k} binaire (0/1)")
        led = m.get("led")
        if led is not None:
            if not 0 <= int(led.get("numero", 0)) <= 127:
                erreurs.append(f"{p}.led.numero ∈ [0,127]")
    return erreurs
