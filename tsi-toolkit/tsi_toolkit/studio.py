#!/usr/bin/env python3
"""Studio TSI — presets applicables, DSL minimal, audit auto-évolutif.

Réalisation $facon outillée du « Mapping Studio v11 » (L9) : la vision
React/DSL/presets/auto-audit est portée en module toolchain autonome
(l'UI web complète reste une extension documentée — CDC §4 Exclus).

  * Presets applicables : bloc/deck/paramètre → mappings générés ;
  * DSL minimal : ``contrôle -> fonction [couche]`` ;
  * ``audit_log.md`` : journal des écarts/ajustements de chaque
    exécution (mécanisme auto-évolutif de la v11).
"""
from __future__ import annotations

import os
import re
from datetime import datetime, timezone

from . import karnaugh
from . import nixml
from . import presets as presets_mod

LIGNE_DSL = re.compile(
    r"^\s*(?P<controle>[^\s>;]+)\s*->\s*(?P<fonction>[^\[\];]+?)"
    r"\s*(?:\[(?P<couche>[^\]]*)\])?\s*$")


def compiler_dsl(lignes: list[str], device: dict | None = None) -> dict:
    """Compile des lignes DSL ``controle -> fonction [couche]`` en modèle."""
    mappings = []
    couches_connues = {"BASE": {}, "M1=1": {"M1": 1}, "M2=1": {"M2": 1},
                       "M3=1": {"M3": 1}, "M4=1": {"M4": 1}}
    for n, ligne in enumerate(lignes, start=1):
        brute = ligne.split("#", 1)[0]
        if not brute.strip():
            continue
        m = LIGNE_DSL.match(brute)
        if not m:
            raise ValueError(f"DSL ligne {n} invalide : {ligne!r}")
        couche = (m.group("couche") or "BASE").strip()
        if couche not in couches_connues:
            raise ValueError(f"DSL ligne {n} : couche {couche!r} inconnue "
                             f"(attendues : {sorted(couches_connues)})")
        numero = 36 + (len(mappings) % 90)
        mapping = {
            "nom": f"{m.group('controle')} — {m.group('fonction').strip()}",
            "type": "IN", "groupe": "Deck A",
            "controle": m.group("fonction").strip(),
            "midi": {"canal": 0, "message": "NOTE", "numero": numero,
                     "mode": "Direct"},
        }
        if couches_connues[couche]:
            mapping["modifier"] = dict(couches_connues[couche])
        mappings.append(mapping)
    return {"device": device or {
        "name": "Traktor Kontrol S4 MK2", "type": "MIDI",
        "in_port": "Traktor Kontrol S4 MK2 In",
        "out_port": "Traktor Kontrol S4 MK2 Out",
        "deck_target": "Focus"}, "mappings": mappings}


def appliquer_preset(preset: dict, deck: str = "Deck A") -> list[dict]:
    """Applique un preset (liste de mappings paramétrés) à un deck donné."""
    mappings = []
    for m in preset.get("mappings", []):
        copie = dict(m)
        copie["groupe"] = deck
        copie["nom"] = f"{m['nom'].split(' — ')[0]} — {deck}"
        mappings.append(copie)
    return mappings


def journaliser_audit(chemin_journal: str, entree: dict) -> str:
    """Ajoute une entrée datée à audit_log.md (auto-évolutif v11)."""
    horodatage = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
    lignes = [f"- **{horodatage}** — {entree.get('action', '')}"]
    for k, v in entree.items():
        if k != "action":
            lignes.append(f"  - {k} : {v}")
    lignes.append("")
    existe = os.path.isfile(chemin_journal)
    with open(chemin_journal, "a", encoding="utf-8") as f:
        if not existe:
            f.write("# Audit log — Studio TSI (mécanisme auto-évolutif v11)\n\n")
        f.write("\n".join(lignes) + "\n")
    return chemin_journal


def scenario_demo(chemin_tsi: str, chemin_journal: str) -> dict:
    """Scénario documenté EF-13 : DSL → TSI validé + audit_log créé."""
    lignes_dsl = [
        "# Scénario studio — bloc transport Deck A",
        "play -> Play/Pause",
        "sync -> Sync [M1=1]",
        "cue -> Cue/Set",
        "loop_in -> Loop Set [M2=1]",
        "flux -> Flux Mode",
    ]
    modele = compiler_dsl(lignes_dsl)
    erreurs = presets_mod.valider(modele)
    if erreurs:
        raise ValueError("modèle DSL invalide : " + " ; ".join(erreurs))
    conflits = karnaugh.detecter(modele["mappings"])
    nixml.ecrire(modele, chemin_tsi)
    journaliser_audit(chemin_journal, {
        "action": "scénario studio appliqué (DSL → TSI)",
        "lignes_dsl": len([l for l in lignes_dsl if not l.strip().startswith("#")]),
        "mappings_produits": len(modele["mappings"]),
        "conflits_detectes": len(conflits),
        "sortie": os.path.basename(chemin_tsi),
    })
    return {"mappings": len(modele["mappings"]), "conflits": conflits,
            "tsi": chemin_tsi, "audit_log": chemin_journal}
