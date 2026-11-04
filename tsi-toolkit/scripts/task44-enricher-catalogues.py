#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""task44-enricher-catalogues.py — Enrichit le catalogue toolkit de commandes Traktor
avec la référence Interaktiv Audio « Every Traktor MIDI command » (CC BY 4.0).

Source d'entrée : work/zip-setting-431/traktor-commands.json (524 commandes TP 4.5.1,
24 MIDI Controls IDs 850-873, asOf 2026-09-08/09, traktor3 3.11.1).

Sortie (idempotent ×2 — re-jeu byte-identique) :
  - tsi-toolkit/data/commandes-traktor.json : nouvelle clé 'catalogue_interaktiv'
    (non-régression : comptes/controles/commandes/conditions_declarees DJTT inchangés)

ÉCRIVAIN UNIQUE (correctif F-08 Task 44) : le fichier app src/data/commands.json est
écrit EXCLUSIVEMENT par scripts/task40-generer-catalogue-app.py (qui dérive
lui-même catalogue_interaktiv depuis ce fichier toolkit) — un seul écrivain par
artefact, zéro double source d'écriture (convention R4 / anti-conflit de formats).

Contrat : rc=0 si OK, rc=3 si usage/faute irrécupérable.
"""
import json
import sys
from pathlib import Path

SRC = Path("/home/z/my-project/work/zip-setting-431/traktor-commands.json")
PROJ = Path("/home/z/my-project/work/knowledge-clone-fddbe94")

META = {
    "source": "Interaktiv Audio — Every Traktor MIDI command (https://interaktivaudio.com/traktor-commands)",
    "json_source": "https://interaktivaudio.com/traktor-commands.json",
    "licence": "CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/) — le contenu propre d'Interaktiv Audio (vérification, table, légende, kinds, notes) est réutilisé avec attribution ; les noms, chemins de menu, listes de valeurs et ids sont des faits Traktor",
    "attribution": "Interaktiv Audio, https://interaktivaudio.com/traktor-commands",
    "version_traktor": "Pro 4.5.1",
    "asOf": "2026-09-08/09",
    "traktor3": "3.11.1",
    "note_traktor3": "Traktor 3.11.1 = sous-ensemble strict de TP 4.5.1 : 28 commandes Pro-4-only (Pattern Player complet et autres) ; renames : Show In Explorer -> Show Track In Finder, Load Selected x1 -> x4",
    "champs_provenance": "Task 44 (session web-6058b3ba, 2026-11-04) — intégration directive propriétaire (analyse ZIP setting TRAKTOR 3.11.1.17 + captures Controller Manager)",
}


def charger():
    if not SRC.exists():
        raise SystemExit(3)
    d = json.loads(SRC.read_text(encoding="utf-8"))
    cmds = d.get("commands") or []
    if len(cmds) != 524:
        raise SystemExit(3)
    champ = [
        "name", "id", "section", "direction", "kind", "target",
        "addIn", "addOut", "modes", "types", "range", "pro4Only",
    ]
    norm = [{k: c.get(k) for k in champ if c.get(k) is not None} for c in cmds]
    norm.sort(key=lambda x: x.get("id", -1))
    return d, norm


def enrichir_toolkit(norm, counts):
    p = PROJ / "tsi-toolkit" / "data" / "commandes-traktor.json"
    base = json.loads(p.read_text(encoding="utf-8"))
    mc = [c for c in norm if str(c.get("name", "")).startswith("MIDI ")]
    base["catalogue_interaktiv"] = {
        "meta": META,
        "comptes": {
            "commandes": len(norm),
            "sections": counts.get("sections"),
            "in_and_out": counts.get("inAndOut"),
            "in_only": counts.get("inOnly"),
            "out_only": counts.get("outOnly"),
            "pro4_only": counts.get("pro4Only"),
            "midi_controls": len(mc),
            "midi_controls_ids": [c["id"] for c in mc],
        },
        "commandes": norm,
    }
    p.write_text(json.dumps(base, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return p


def enrichir_app(norm, counts):
    # Correctif F-08 : NO-OP (écrivain unique = générateur Task 40) — définition
    # conservée en tête pour lisibilité ; l'ancien corps écrivain est retiré (R2).
    p = PROJ / "src" / "data" / "commands.json"
    return p


def main():
    d, norm = charger()
    counts = d.get("counts") or {}
    p1 = enrichir_toolkit(norm, counts)
    p2 = enrichir_app(norm, counts)
    t1 = json.loads(p1.read_text(encoding="utf-8"))
    t2 = json.loads(p2.read_text(encoding="utf-8"))
    assert t1["comptes"]["commandes"] == 393, "régression comptes DJTT toolkit"
    assert t2["comptes"]["commandes"] == 455, "régression comptes app"
    assert len(t1["catalogue_interaktiv"]["commandes"]) == 524
    assert len(t2["catalogue_interaktiv"]["commandes"]) == 524
    mc_ids = t1["catalogue_interaktiv"]["comptes"]["midi_controls_ids"]
    assert mc_ids == list(range(850, 874)), "IDs MIDI Controls inattendus"
    print(f"CATALOGUE ENRICHIS : {p1.name} (524 cmd, MIDI Controls {mc_ids[0]}-{mc_ids[-1]}, DJTT 393 intact) ; app {p2.name} = écrivain unique générateur (F-08)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
