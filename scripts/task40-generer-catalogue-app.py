#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.34)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).
"""

"""task40-generer-catalogue-app.py — Génère le catalogue scellé de l'app LEON TSI EDITEUR (Task 40 / G3 / D006c).

Sources de vérité (zéro valeur inventée) :
  1. tsi-toolkit/data/commandes-traktor.json — extraction mécanique du mapping réel
     DJTT S4 MK2 v2.1.0 (393 commandes nommées, 163 contrôles, conditions 125 in / 220 out).
  2. Discussion b6170b8b (extraction Task 40, rapport-analyse §3) — familles de commandes
     documentées avec ids du catalogue CMDR : Global_MidiControls (24 relais 850-873),
     MasterClock_AbletonLink (2811), RemixDeck_StepSequencer (20 : 734-756), AudioRecorder
     (4 : 2056/2055/29/3084), DeckCommon (Flux 2350/874, Advanced Panel 2299/2298,
     Deck Flavor 2302), LoopRecorder (280-287 : 6), contrôles usine LoopRec (cid 47-51),
     Flux (cid 30), Remix Slots (cid 9-12) + tableau CC consolidé (schémas Drive, passes
     VLM concordantes).

Sortie : src/data/commands.json (catégories→commandes, ids, provenance) et
src/data/s4mk2-controls.json (contrôles in/out par zone + table CC documentée).
Conventions script-creator : stdlib, idempotent ×2 (byte-identique, clés triées).
"""
import json
from pathlib import Path

RACINE = Path("/home/z/my-project")
TOOLKIT = RACINE / "work/knowledge-clone-fddbe94/tsi-toolkit/data/commandes-traktor.json"
SORTIE = RACINE / "src/data"

# --- Source 2 : familles documentées de la discussion (ids catalogue CMDR) ---
FAMILLES_DISCUSSION = {
    "Ableton/MIDI (Global MIDI Controls)": {
        "categorie": "Global",
        "commandes": [
            ("Global MIDI Control Button %d" % i, 850 + i - 1) for i in range(1, 9)
        ] + [
            ("Global MIDI Control Knob %d" % i, 858 + i - 1) for i in range(1, 9)
        ] + [
            ("Global MIDI Control Fader %d" % i, 866 + i - 1) for i in range(1, 9)
        ],
    },
    "Deck > Horloge": {
        "categorie": "Global",
        "commandes": [("Ableton Link Reset Downbeat", 2811)],
    },
    "Deck > Remix (Step Sequencer)": {
        "categorie": "Remix",
        "commandes": (
            [("Sequencer On", 734), ("Sequencer Swing", 735),
             ("Sequencer Pattern Length", 736), ("Sequencer Selected Sample", 737)]
            + [("Sequencer Enable Step %d" % i, 738 + i - 1) for i in range(1, 17)]
        ),
    },
    "Deck > Enregistrement (Audio Recorder)": {
        "categorie": "Enregistrement",
        "commandes": [("Audio Recorder Record/Stop", 2056), ("Audio Recorder Record", 2055),
                      ("Broadcasting On", 29), ("Audio Recorder Record and Advance", 3084)],
    },
    "Deck > Flux": {
        "categorie": "Flux",
        "commandes": [("Flux Mode On", 2350), ("Flux Reverse", 874)],
    },
    "Deck > Panneau avancé": {
        "categorie": "Deck",
        "commandes": [("Advanced Panel", 2299), ("Advanced Panel Open/Close", 2298),
                      ("Deck Flavor Selector", 2302)],
    },
    "Deck > Loop Recorder": {
        "categorie": "Boucles",
        "commandes": [("Loop Recorder Record", 280), ("Loop Recorder Play/Pause", 281),
                      ("Loop Recorder Size", 282), ("Loop Recorder Delete", 283),
                      ("Loop Recorder Dry/Wet", 284), ("Loop Recorder Undo/Redo", 285),
                      ("Loop Recorder Capture Source", 286), ("Loop Recorder Advance", 287)],
    },
}

# --- Source 2b : table CC consolidée (schémas Drive + VLM, discussion §3) ---
TABLE_CC = {
    "Deck A": [
        ("Jog Wheel extérieur", 1, "fader"), ("Jog Wheel intérieur", 2, "fader"),
        ("Tempo", 4, "fader"), ("Shift", 5, "bouton"), ("Flux", 6, "bouton"),
        ("Load", 8, "bouton"), ("Deck C (jeu)", 9, "bouton"),
        ("Remix Slot 1", 11, "bouton"), ("Remix Slot 2", 12, "bouton"),
        ("Remix Slot 3", 13, "bouton"), ("FX Mode", 14, "bouton"),
        ("Hotcue 1", 15, "bouton"), ("Hotcue 2", 16, "bouton"),
        ("Hotcue 3", 17, "bouton"), ("Hotcue 4", 18, "bouton"),
        ("Loop Move", 19, "fader"), ("FX Knob 1", 20, "fader"), ("FX Knob 2", 21, "fader"),
        ("FX Knob 3", 22, "fader"), ("FX Bouton 1", 24, "bouton"), ("FX Bouton 2", 25, "bouton"),
        ("FX Bouton 3", 26, "bouton"), ("FX On", 28, "bouton"),
    ],
    "FX droit": [("FX droit %d" % i, 30 + i - 1, "fader" if i <= 4 else "bouton") for i in range(1, 9)],
    "Mixer (tranche)": [
        ("Gain", 60, "fader"), ("Cue", 62, "bouton"), ("FX 1", 63, "bouton"),
        ("EQ High", 64, "fader"), ("EQ Mid", 65, "fader"), ("EQ Low", 66, "fader"),
        ("Filtre", 67, "fader"), ("Volume", 68, "fader"),
    ],
    "Deck B": [("Bouton deck droit %d" % i, 71 + i - 1, "bouton") for i in range(1, 7)],
    "Faders": [("Fader gauche (jeu)", 69, "fader"), ("Fader droit (jeu)", 70, "fader")],
    "Master": [("Master %d" % i, 77 + i - 1, "fader" if i <= 2 else "bouton") for i in range(1, 4)],
    "Loop Recorder (matériel)": [("Loop Recorder %d" % i, 80 + i - 1, "bouton") for i in range(1, 4)],
    "Crossfader": [("Crossfader", 10, "fader")],
}


def main() -> int:
    tk = json.loads(TOOLKIT.read_text(encoding="utf-8"))

    # --- commands.json : fusion triée, ids stables, provenance ---
    commandes, id_suivant = [], 1
    for nom, cat in sorted(tk["commandes"].items()):
        commandes.append({"id": id_suivant, "nom": nom, "categorie": cat,
                           "provenance": "toolkit-djtt-reel"})
        id_suivant += 1
    for famille, bloc in FAMILLES_DISCUSSION.items():
        for nom, cmdr_id in bloc["commandes"]:
            if any(c["nom"].lower() == nom.lower() for c in commandes):
                continue  # doublon nominal → garde la version toolkit (source 1 prioritaire)
            commandes.append({"id": id_suivant, "nom": nom, "categorie": bloc["categorie"],
                               "provenance": "discussion-cmdr", "cmdrId": cmdr_id})
            id_suivant += 1
    categories = {}
    for c in commandes:
        categories.setdefault(c["categorie"], []).append(c["id"])
    out_commands = {
        "meta": {
            "titre": "Catalogue scellé LEON TSI EDITEUR v11",
            "sources": [
                "tsi-toolkit/data/commandes-traktor.json (extraction mécanique DJTT v2.1.0 réel — source de vérité primaire)",
                "discussion b6170b8b §3 (familles CMDR documentées — rapport-analyse-discussion-b6170b8b.md)",
            ],
            "convention": "source 1 prioritaire sur doublons nominaux ; ids stables par ordre lexicographique",
        },
        "comptes": {"commandes": len(commandes), "categories": len(categories)},
        "categories": categories,
        "commandes": {str(c["id"]): {"nom": c["nom"], "categorie": c["categorie"],
                                     "provenance": c["provenance"],
                                     **({"cmdrId": c["cmdrId"]} if "cmdrId" in c else {})}
                      for c in commandes},
    }

    # --- s4mk2-controls.json : conditions in/out réelles + table CC documentée ---
    cond = tk["conditions_declarees"]
    in_par_deck, out_par_deck = {}, {}
    for nom in cond["in"]:
        cle = nom.split(".")[0] if "." in nom else "Global"
        in_par_deck.setdefault(cle, []).append(nom)
    for nom in cond["out"]:
        cle = nom.split(".")[0] if "." in nom else "Global"
        out_par_deck.setdefault(cle, []).append(nom)
    out_controls = {
        "meta": {
            "titre": "Contrôles S4 MK2 scellés — 125 entrées / 220 sorties (DJTT réel) + table CC documentée",
            "sources": out_commands["meta"]["sources"],
        },
        "comptes": {"in": len(cond["in"]), "out": len(cond["out"])},
        "in": {k: sorted(v) for k, v in sorted(in_par_deck.items())},
        "out": {k: sorted(v) for k, v in sorted(out_par_deck.items())},
        "tableCC": {zone: [{"nom": n, "cc": cc, "type": t} for n, cc, t in lst]
                    for zone, lst in TABLE_CC.items()},
        "controlesUsine": {
            "LoopRec": {"cids": [47, 48, 49, 50, 51], "notes": "Record/Play/Size/Delete/DryWet"},
            "Flux": {"cids": [30], "notes": "Left/Right via Flux"},
            "RemixSlots": {"cids": [9, 10, 11, 12], "notes": "8 slots via cid 9-12"},
        },
        "modeMidi": {"combinaison": "SHIFT + PREVIEW", "source": "Manuel NI §6.10.2 (support officiel, croisé DJTT)"},
    }

    SORTIE.mkdir(parents=True, exist_ok=True)
    j1 = json.dumps(out_commands, ensure_ascii=False, indent=1) + "\n"
    j2 = json.dumps(out_controls, ensure_ascii=False, indent=1) + "\n"
    (SORTIE / "commands.json").write_text(j1, encoding="utf-8")
    (SORTIE / "s4mk2-controls.json").write_text(j2, encoding="utf-8")
    print(f"commands.json : {out_commands['comptes']} ({len(j1)} octets)")
    print(f"s4mk2-controls.json : {out_controls['comptes']} ({len(j2)} octets)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
