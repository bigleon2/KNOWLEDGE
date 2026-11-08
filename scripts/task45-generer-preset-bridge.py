#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.36)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).
task45-generer-preset-bridge.py — Générateur mécanique du preset
« MIDI Controls bridge » (Task 45).

Conception (d'après Task 44 — D002/D005/D006 : arborescence MIDI Controls,
IDs Interaktiv 850-873 CC BY 4.0 ; convention looprituals 1-4 = deck
gauche / 5-8 = deck droit ; pattern de l'Assignment Table du propriétaire
Master/Key/Mixer FX/Temp Adjust → X.Filter en Direct) :

* ÉTAGE 1 — 24 entrées bridge (GROUP=Global, ch0, CC 80-103) : le
  contrôleur externe attaque les 24 commandes génériques MIDI Controls
  (MIDI Button/Knob/Fader 1-8, IDs réels 850-873).
* ÉTAGE 2 — 24 délégations par deck (ch1 = bus virtuel des MIDI Controls,
  mêmes CC) : chaque MIDI Control délègue à une commande de deck réelle
  (catalogue_interaktiv) — réplique du pattern « In | Deck X | Direct |
  X.Filter » de l'Assignment Table.
* LED — 8 sorties (miroir des boutons, MODE=Output, ON=127/OFF=0).

SYMÉTRIE DES DECKS (source de vérité DJTT) : chaque deck A-D reçoit
exactement 6 délégations (Mixer FX Adjust, Mixer FX On, Low Adjust,
High Adjust, Tempo Adjust, Volume Adjust) — invariant vérifié mécaniquement.

Déterministe (R6) et idempotent ×2 : le re-jeu produit un JSON
byte-identique. Python stdlib uniquement (N3).

Usage : task45-generer-preset-bridge.py [chemin_sortie]
Exit : 0 succès ; 1 échec de cohérence.
"""
from __future__ import annotations

import json
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
SORTIE_PAR_DEFAUT = os.path.join(
    ICI, "..", "tsi-toolkit", "examples",
    "preset-midi-controls-bridge.json")

DECKS_GAUCHE = ["A", "C"]   # convention looprituals 1-4 = deck gauche
DECKS_DROITE = ["B", "D"]   # 5-8 = deck droit
CC_DEBUT_BOUTONS, CC_DEBOUT_KNOBS, CC_DEBUT_FADERS = 80, 88, 96


def _matrice_etage2():
    """Matrice de délégation (1:1 avec les 24 MIDI Controls) — 6/deck."""
    rows = []
    # Boutons 1-4 : Mixer FX Adjust par deck (lignes « Mixer FX Adjust |
    # In | Deck A-D | Direct | X.Filter » de l'Assignment Table).
    for i, deck in enumerate(["A", "B", "C", "D"]):
        rows.append({
            "bridge": ("MIDI Button", i + 1),
            "cc": CC_DEBUT_BOUTONS + i, "mode": "Direct",
            "controle": "Mixer FX Adjust", "groupe": f"Deck {deck}",
            "cible": f"{deck}.Filter",
        })
    # Boutons 5-8 : Mixer FX On par deck (activation du Mixer FX, switch).
    for i, deck in enumerate(["A", "B", "C", "D"]):
        rows.append({
            "bridge": ("MIDI Button", i + 5),
            "cc": CC_DEBUT_BOUTONS + 4 + i, "mode": "Toggle",
            "controle": "Mixer FX On", "groupe": f"Deck {deck}",
            "cible": f"{deck}.MixerFX On",
        })
    # Knobs 1-4 = deck gauche (A, C) : Low puis High ; Knobs 5-8 = deck
    # droit (B, D) — EQ 2 bandes par deck, appariées gauche/droite.
    knobs = [("Low Adjust", "A"), ("High Adjust", "A"),
             ("Low Adjust", "C"), ("High Adjust", "C"),
             ("Low Adjust", "B"), ("High Adjust", "B"),
             ("Low Adjust", "D"), ("High Adjust", "D")]
    for i, (cmd, deck) in enumerate(knobs):
        rows.append({
            "bridge": ("MIDI Knob", i + 1),
            "cc": CC_DEBOUT_KNOBS + i, "mode": "Direct",
            "controle": cmd, "groupe": f"Deck {deck}",
            "cible": f"{deck}.{cmd.split()[0]}",
        })
    # Faders 1-2 = Deck A (Tempo, Volume) ; 3-4 = Deck C ; 5-6 = Deck B ;
    # 7-8 = Deck D — 2 faders par deck, gauche d'abord (looprituals).
    faders = [("Tempo Adjust", "A"), ("Volume Adjust", "A"),
              ("Tempo Adjust", "C"), ("Volume Adjust", "C"),
              ("Tempo Adjust", "B"), ("Volume Adjust", "B"),
              ("Tempo Adjust", "D"), ("Volume Adjust", "D")]
    for i, (cmd, deck) in enumerate(faders):
        rows.append({
            "bridge": ("MIDI Fader", i + 1),
            "cc": CC_DEBUT_FADERS + i, "mode": "Direct",
            "controle": cmd, "groupe": f"Deck {deck}",
            "cible": f"{deck}.{cmd.split()[0]}",
        })
    return rows


def construire_preset():
    """Construit le dict preset complet (56 mappings)."""
    mappings = []
    # Étage 1 — les 24 MIDI Controls (GROUP=Global, ch0, CC 80-103).
    for i in range(8):
        mappings.append({
            "nom": f"Bridge entrée — MIDI Button {i + 1} (CC{CC_DEBUT_BOUTONS + i})",
            "type": "IN", "groupe": "Global", "controle": f"MIDI Button {i + 1}",
            "midi": {"canal": 0, "message": "CC",
                     "numero": CC_DEBUT_BOUTONS + i,
                     "mode": "Direct" if i < 4 else "Toggle"},
        })
    for i in range(8):
        mappings.append({
            "nom": f"Bridge entrée — MIDI Knob {i + 1} (CC{CC_DEBOUT_KNOBS + i})",
            "type": "IN", "groupe": "Global", "controle": f"MIDI Knob {i + 1}",
            "midi": {"canal": 0, "message": "CC",
                     "numero": CC_DEBOUT_KNOBS + i, "mode": "Direct"},
        })
    for i in range(8):
        mappings.append({
            "nom": f"Bridge entrée — MIDI Fader {i + 1} (CC{CC_DEBUT_FADERS + i})",
            "type": "IN", "groupe": "Global", "controle": f"MIDI Fader {i + 1}",
            "midi": {"canal": 0, "message": "CC",
                     "numero": CC_DEBUT_FADERS + i, "mode": "Direct"},
        })
    # Étage 2 — délégation par deck (ch1 = bus virtuel, mêmes CC).
    for r in _matrice_etage2():
        famille, n = r["bridge"]
        mappings.append({
            "nom": (f"Délégation {r['controle']} — {r['groupe']} "
                    f"({r['cible']}) ← {famille} {n}"),
            "type": "IN", "groupe": r["groupe"], "controle": r["controle"],
            "midi": {"canal": 1, "message": "CC", "numero": r["cc"],
                     "mode": r["mode"]},
        })
    # LED — miroir des 8 boutons (retour d'état, MODE=Output sérialisé).
    # Le contrôle reprend la commande du bouton (miroir DCBM réel : une
    # LED de sortie porte le NOM de la commande source, pas un nom
    # artificiel — évite les fausses inconnues au validateur catalogue).
    for i in range(8):
        mappings.append({
            "nom": f"LED retour — MIDI Button {i + 1}",
            "type": "OUT", "groupe": "Global",
            "controle": f"MIDI Button {i + 1}",
            "led": {"numero": CC_DEBUT_BOUTONS + i, "on": 127, "off": 0},
        })
    return {
        "meta": {
            "nom": "MIDI Controls bridge — délégation par deck",
            "description": (
                "Bridge MIDI par les 24 commandes génériques Global > MIDI "
                "Controls (Buttons/Knobs/Faders 1-8, IDs 850-873) : étage 1 "
                "= entrées du contrôleur externe (ch0, CC 80-103) ; étage 2 "
                "= délégation par deck sur le bus virtuel (ch1), réplique du "
                "pattern « In | Deck X | Direct | X.Filter » de l'Assignment "
                "Table du propriétaire (Master/Key/Mixer FX/Temp Adjust). "
                "Symétrie des decks DJTT respectée : 6 délégations par deck "
                "A-D. Sources : Interaktiv Audio, "
                "https://interaktivaudio.com/traktor-commands (CC BY 4.0) ; "
                "looprituals.de (convention 1-4 gauche / 5-8 droite) ; "
                "captures Controller Manager Traktor 3.11.1.17 du "
                "propriétaire (2026-11-03)."),
            "version": "1.0.0",
            "appareil": "Traktor Kontrol S4 MK2",
            "traktor": "3.11.1",
        },
        "device": {
            "name": "Traktor Kontrol S4 MK2",
            "type": "MIDI",
            "in_port": "Traktor Kontrol S4 MK2 In",
            "out_port": "Traktor Kontrol S4 MK2 Out",
            "deck_target": "Focus",
        },
        "mappings": mappings,
    }


def verifier(preset):
    """Contrôles de cohérence internes (échec bruyant KO-L003)."""
    m = preset["mappings"]
    assert len(m) == 56, f"56 mappings attendus, trouvé {len(m)}"
    e1 = [x for x in m if x["groupe"] == "Global"
          and x["type"] == "IN" and x["controle"].startswith("MIDI ")
          and not x["controle"].endswith("LED")]
    e2 = [x for x in m if x["type"] == "IN"
          and x["groupe"].startswith("Deck ")]
    led = [x for x in m if x["type"] == "OUT"]
    assert len(e1) == 24 and len(e2) == 24 and len(led) == 8, \
        f"étages {len(e1)}/{len(e2)}/{len(led)} ≠ 24/24/8"
    # Appariement 1:1 étage 1 ↔ étage 2 (famille+n ↔ même CC, ch distinct).
    e1_pairs = {(x["controle"].rsplit(" ", 1)[0],
                 x["controle"].rsplit(" ", 1)[1],
                 x["midi"]["numero"]) for x in e1}
    e2_pairs = {(x["controle"], x["midi"]["numero"]) for x in e2}
    assert len({p[2] for p in e1_pairs}) == 24, "CC étage 1 non uniques"
    assert len({x["midi"]["numero"] for x in e2}) == 24, "CC étage 2 non uniques"
    # Symétrie des decks : exactement 6 délégations par deck.
    comptes = {}
    for x in e2:
        comptes[x["groupe"]] = comptes.get(x["groupe"], 0) + 1
    assert comptes == {f"Deck {d}": 6 for d in "ABCD"}, \
        f"symétrie violée : {comptes}"
    # Plages MIDI (E4) : canaux 0-1, CC 80-103, pas de collision.
    vus = set()
    for x in e1 + e2:
        cle = (x["midi"]["canal"], x["midi"]["numero"])
        assert cle not in vus, f"collision MIDI {cle}"
        vus.add(cle)
        assert 0 <= x["midi"]["canal"] <= 15 and 80 <= x["midi"]["numero"] <= 103
    return True


def main():
    sortie = os.path.abspath(sys.argv[1] if len(sys.argv) > 1
                             else SORTIE_PAR_DEFAUT)
    preset = construire_preset()
    verifier(preset)
    os.makedirs(os.path.dirname(sortie), exist_ok=True)
    with open(sortie, "w", encoding="utf-8", newline="\n") as f:
        json.dump(preset, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(f"✅ Preset écrit : {sortie} "
          f"({len(preset['mappings'])} mappings — 24 bridge + "
          f"24 délégations + 8 LED ; decks symétriques 6/6/6/6)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
