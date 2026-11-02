#!/usr/bin/env python3
"""Karnaugh anti-conflits — collisions MIDI et incohérences de modifiers.

Héritage des discussions (L4 : validator/karnaugh.py) converge avec la
règle E5 de tsi-validator (doublons d'allocation). Deux mappings entrent
en conflit si :
  (a) CONFLIT_MIDI — même événement (canal, message, numéro) ET états de
      modifiers COMPATIBLES (aucune contradiction sur M1-M4) ;
  (b) MODIFIER_ETAT — un mapping exige Mx=1 alors qu'aucun mapping
      d'activation ne produit Mx=1 (état injoignable) ;
  (c) LED_SANS_SORTIE — un LED IN associé à un message non déclaré OUT.
"""
from __future__ import annotations

from collections import defaultdict


def _etats(m: dict) -> dict:
    return m.get("modifier") or {}


def _compatibles(e1: dict, e2: dict) -> bool:
    """Deux conditions de modifiers sont compatibles si aucune clé
    commune n'exige des valeurs différentes."""
    for k, v in e1.items():
        if k in e2 and e2[k] != v:
            return False
    return True


def _evenement(m: dict) -> tuple | None:
    midi = m.get("midi")
    if not midi:
        return None
    return (midi["canal"], midi["message"], midi["numero"])


def detecter(mappings: list[dict]) -> list[dict]:
    """Retourne la liste des conflits (vide = sain)."""
    conflits = []
    # (a) collisions MIDI avec états compatibles
    par_evenement = defaultdict(list)
    for i, m in enumerate(mappings):
        ev = _evenement(m)
        if ev is not None and m.get("type", "IN") == "IN":
            par_evenement[ev].append(i)
    for ev, idxs in sorted(par_evenement.items()):
        for a in range(len(idxs)):
            for b in range(a + 1, len(idxs)):
                ma, mb = mappings[idxs[a]], mappings[idxs[b]]
                if _compatibles(_etats(ma), _etats(mb)):
                    conflits.append({
                        "type": "CONFLIT_MIDI",
                        "detail": (f"{ma['nom']!r} et {mb['nom']!r} sur "
                                   f"canal {ev[0]} {ev[1]} n°{ev[2]} "
                                   f"(états modifiers compatibles)"),
                        "indexes": [idxs[a], idxs[b]],
                    })
    # (b) états de modifiers injoignables
    produits: dict[str, set[int]] = defaultdict(set)
    for m in mappings:
        if m.get("controle", "").startswith("Modifier "):
            midi = m.get("midi")
            if midi and m.get("type", "IN") == "IN":
                numero = "".join(ch for ch in m["controle"] if ch.isdigit())
                if numero:
                    produits[f"M{numero}"].add(1)
    for m in mappings:
        for k, v in _etats(m).items():
            if int(v) == 1 and k not in produits:
                conflits.append({
                    "type": "MODIFIER_ETAT",
                    "detail": (f"{m['nom']!r} exige {k}={v} mais aucun "
                               f"mapping n'active {k}"),
                    "indexes": [],
                })
    # (c) LED sans sortie déclarée
    sorties = {(_evenement(m)) for m in mappings if m.get("type") == "OUT"}
    for i, m in enumerate(mappings):
        led = m.get("led")
        if led is not None and m.get("type", "IN") == "IN":
            midi = m.get("midi")
            cle = (midi["canal"], midi["message"], led["numero"]) if midi else None
            if cle and cle not in sorties:
                conflits.append({
                    "type": "LED_SANS_SORTIE",
                    "detail": (f"{m['nom']!r} porte un LED n°{led['numero']} "
                               f"sans mapping OUT correspondant"),
                    "indexes": [i],
                })
    return conflits
