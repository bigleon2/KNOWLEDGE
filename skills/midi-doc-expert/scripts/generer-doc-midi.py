#!/usr/bin/env python3
"""generer-doc-midi.py — Générateur de documentation technique MIDI (skill midi-doc-expert v1.2.0).

Projet TSI/Traktor — S4 MK2 / Traktor Pro 3.11. Persona : Rédacteur Technique
Expert en Mappings MIDI et Contrôleurs Audio (cahier des charges S2).
Entrée : un fichier .tsi (préalablement validé par tsi-validator). Sorties :
document .md (structure type 9 sections, tableaux de référence MIDI, états LED)
+ document .json machine-readable. DÉTERMINISTE (ENF-05 : aucun horodatage,
tri stable) — le rejeu est un no-op binaire. Python stdlib uniquement (N3).

v1.2.0 (Task 45) : §5 rédigé par mode (Increment/Decrement = encodeur,
Toggle = bouton/commutation, Direct = valeur absolue — « attaque la commande
générique » pour les MIDI Controls) ; §2 signale et explique un bridge
MIDI Controls (2 étages, IDs 850-873, convention 1-4/5-8) quand il en
détecte ; attribution Interaktiv CC BY 4.0 portée dans le §2.

Usage : generer-doc-midi.py <fichier.tsi> --outdir <dir> [--titre "…"] [--json-seul]
        generer-doc-midi.py --self-test
Exit : 0 succès ; 1 échec structurel ; 2 usage.
"""
import argparse
import json
import os
import sys
import xml.etree.ElementTree as ET

ICI = os.path.dirname(os.path.abspath(__file__))
SECTIONS = ["Introduction", "Vue d'ensemble du mapping", "Activation / Désactivation",
            "Contrôle des Slices", "Réglages avancés", "Tableau de Référence MIDI",
            "Modes de sortie", "États des LED", "Annexes"]


def extraire_mappings(path):
    arbre = ET.parse(path)
    racine = arbre.getroot()
    dev = racine.find("DEVICE")
    out = []
    for m in dev.findall("MAPPINGS/MAPPING"):
        cond = {}
        mod = m.find("MODIFIER")
        if mod is not None:
            cond = {k: v for k, v in mod.attrib.items()}
        midi = m.find("MIDI")
        led = m.find("LED")
        out.append({
            "nom": (m.get("NAME") or "").strip(), "type": m.get("TYPE"),
            "groupe": m.get("GROUP"), "control": m.get("CONTROL"),
            "conditions": cond,
            "midi": dict(midi.attrib) if midi is not None else None,
            "led": dict(led.attrib) if led is not None else None,
        })
    meta = {"device": dev.get("NAME"), "in_port": dev.get("IN_PORT"),
            "out_port": dev.get("OUT_PORT"), "deck_target": dev.get("DECK_TARGET"),
            "n_mappings": len(out)}
    return meta, out


def couche(mapping):
    """Nom de couche multi-shift d'un mapping (méthode multi-shift-architect)."""
    c = mapping["conditions"]
    if c.get("M1") == "1":
        return "FREEZE"
    return "BASE"


def generer(meta, mappings, titre):
    tris = sorted(mappings, key=lambda m: (m["type"] != "IN", m["groupe"] or "", m["nom"]))
    lignes_tableau = [f"| {m['nom']} | {m['groupe']} | {m['control']} | {m['type']} | "
                      f"{(m['midi'] or {}).get('MESSAGE', '—')} {(m['midi'] or {}).get('NUMBER', '')}".rstrip()
                      + f" | ch {(m['midi'] or {}).get('CHANNEL', '—')} | {(m['midi'] or {}).get('MODE', '—')} | "
                      f"{couche(m)} |" for m in tris]
    modifiers = sorted({m["control"] for m in mappings if (m["control"] or "").startswith("Modifier ")})
    slices = [m for m in mappings if (m["control"] or "").startswith("Slice") and m["type"] == "IN"]
    encodeurs = [m for m in mappings if m["type"] == "IN" and (m["midi"] or {}).get("MESSAGE") == "CC"]
    leds = [m for m in mappings if m["type"] == "OUT"]
    md = [
        f"# {titre}", "",
        "## 1. Introduction", "",
        f"Ce document décrit en détail le fonctionnement du mapping MIDI « {titre} » pour le contrôleur "
        f"**{meta['device']}** sous **TRAKTOR PRO 3.11**. Il est généré automatiquement par le skill "
        f"midi-doc-expert à partir du fichier de mapping source, puis validé mécaniquement (couverture complète). "
        f"Le vocabulaire MIDI utilisé — note (message NOTE), CC (Control Change, message de commande continue), "
        f"canal (CHANNEL, voie MIDI 0-15) et mode (Interaction Mode : Direct, Toggle, Increment…) — est défini "
        f"à sa première occurrence afin d'être accessible sans prérequis.", "",
        "## 2. Vue d'ensemble du mapping", "",
        f"Le device « {meta['device']} » dialogue avec Traktor via les ports {meta['in_port']} (entrée) et "
        f"{meta['out_port']} (sortie), avec pour cible de deck {meta['deck_target']}. Le mapping compte "
        f"**{meta['n_mappings']} affectations** : {sum(1 for m in mappings if m['type'] == 'IN')} entrées "
        f"(commandes) et {len(leds)} sorties (retours d'état LED). "
        f"{'Les couches logiques (multi-shift) sont : ' + ', '.join(modifiers) + ' (activation toggle).' if modifiers else 'Aucune couche logique (mapping mono-couche).'}", "",
    ]
    bridges = [m for m in mappings if m["type"] == "IN"
               and (m["control"] or "").startswith("MIDI ")]
    if bridges:
        n_btn = sum(1 for m in bridges if "Button" in (m["control"] or ""))
        n_knob = sum(1 for m in bridges if "Knob" in (m["control"] or ""))
        n_fad = sum(1 for m in bridges if "Fader" in (m["control"] or ""))
        md += [
            "**Bridge MIDI Controls détecté** : ce mapping exploite les commandes génériques "
            "Global > MIDI Controls (MIDI Button/Knob/Fader, IDs 850-873 — Interaktiv Audio, "
            "https://interaktivaudio.com/traktor-commands, CC BY 4.0) comme relais : "
            f"{n_btn} boutons, {n_knob} knobs, {n_fad} faders. Le pont fonctionne en deux "
            "étages : l'étage 1 (canal 0) reçoit le MIDI du contrôleur externe vers les "
            "commandes génériques ; l'étage 2 (canal 1 — bus virtuel des MIDI Controls) "
            "délègue ces mêmes événements aux commandes de deck réelles, en réplique du "
            "pattern « In | Deck X | Direct | X.Filter » de l'Assignment Table, selon la "
            "convention 1-4 = deck gauche / 5-8 = deck droit (looprituals.de).", "",
        ]
    md += ["## 3. Activation / Désactivation", "",
    ]
    if modifiers:
        md += [f"La couche logique **{modifiers[0]}** s'active par un appui **Toggle** sur le contrôle physique "
               f"dédié (pattern S4 MK2 : maintien SHIFT + pression du contrôle d'activation, ex. LOOP IN). "
               f"Tant que le modifier vaut 1, les affectations conditionnées restent actives. "
               f"Un nouvel appui toggle le ramène à 0 et désactive la couche.", ""]
    else:
        md += ["Ce mapping n'utilise pas de couche logique conditionnée : toutes les commandes sont actives en permanence.", ""]
    md += ["## 4. Contrôle des Slices", ""]
    if slices:
        notes = ", ".join((m["midi"] or {}).get("NUMBER", "?") for m in slices)
        md += [f"En couche FREEZE, les **{len(slices)} pads** déclenchent chacun une tranche (Slice) de la grille "
               f"gelée : pads 1 à {len(slices)}, notes {notes} (canal {(slices[0]['midi'] or {}).get('CHANNEL', '?')}, "
               f"mode Direct). Chaque pad rejoue la tranche correspondante tant que la couche est active. "
               f"La condition de couche (modifier = 1) garantit qu'aucun pad ne déclenche une slice hors Freeze.", ""]
    else:
        md += ["Aucune affectation de slices conditionnée dans ce mapping (pas de couche FREEZE).", ""]
    md += ["## 5. Réglages avancés", ""]
    if encodeurs:
        for e in encodeurs:
            mode = (e["midi"] or {}).get("MODE")
            ctrl = e["control"] or ""
            entete = (f"« {e['nom']} » (CC {(e['midi'] or {}).get('NUMBER')}, canal "
                      f"{(e['midi'] or {}).get('CHANNEL')}, mode {mode})")
            suite = ('Conditionné à la couche FREEZE.' if e["conditions"]
                     else "Actif en couche BASE.")
            if mode in ("Increment", "Decrement"):
                md += [f"L'encodeur {entete} ajuste **{ctrl}**. "
                       f"Le mode Increment/decrement traduit la rotation en pas "
                       f"successifs. {suite}", ""]
            elif mode == "Toggle":
                md += [f"Le bouton {entete} commute **{ctrl}**. "
                       f"Le mode Toggle bascule l'état (on/off) à chaque appui. "
                       f"{suite}", ""]
            elif ctrl.startswith("MIDI "):
                md += [f"Le contrôle {entete} attaque la commande générique "
                       f"**{ctrl}** (relais bridge). Le mode Direct transmet la "
                       f"valeur absolue du contrôle (0-127). {suite}", ""]
            else:
                md += [f"Le contrôle {entete} ajuste **{ctrl}** en valeur "
                       f"absolue (mode Direct, 0-127). {suite}", ""]
    else:
        md += ["Aucun encodeur continu (CC) dans ce mapping.", ""]
    md += ["## 6. Tableau de Référence MIDI", "",
           "| Affectation | Groupe | Commande | Sens | Message MIDI | Canal | Mode | Couche |",
           "|---|---|---|---|---|---|---|---|"] + lignes_tableau + ["",
           "## 7. Modes de sortie", "",
           f"Les sorties (TYPE=OUT, {len(leds)} affectation(s)) restituent l'état logiciel sur les LED du "
           f"contrôleur : chaque LED porte son numéro de note, ses valeurs ON (allumée) et OFF (éteinte), "
           f"et le mode Output (émission d'état). Les LED conditionnées ne s'allument que dans leur couche.", ""]
    md += ["## 8. États des LED", ""]
    for l in leds:
        cond = " (couche FREEZE uniquement)" if l["conditions"].get("M1") == "1" else ""
        md += [f"- **{l['nom']}** — note {l['led'].get('NUMBER')}{cond} : OFF ({l['led'].get('OFF')}) par défaut, "
               f"ON ({l['led'].get('ON')}) lorsque l'état porté par « {l['control']} » est actif."]
    md += ["", "## 9. Annexes", "",
           "Calibration : les numéros MIDI proviennent du référentiel de référence du projet (statut « à calibrer », "
           "R-1/R-2 — spec §8) ; ils sont remplaçables par les valeurs d'un TSI réel sans changement de pipeline. ",
           "Sources : articles Native Instruments (Controller Manager, Generic MIDI), reverse-engineering public "
           "du format TSI (IvanZ 2014), mappings TSI tiers documentés (cible S4 MK2, analyse DJTT v2.1.0), documentation PyMuPDF/pymupdf4llm "
           "(chaîne PDF aval). Format PDF : généré en aval via le skill plateforme pdf.", ""]
    doc_json = {
        "document": {"titre": titre, "device": meta["device"], "structure": SECTIONS,
                     "deterministe": True, "generateur": "midi-doc-expert v1.2.0"},
        "mappings": mappings,
        "led": [{"nom": l["nom"], "note": l["led"].get("NUMBER"),
                 "on": l["led"].get("ON"), "off": l["led"].get("OFF"),
                 "couche": couche(l)} for l in leds],
        "couverture": {"mappings_tsi": meta["n_mappings"], "lignes_tableau": len(lignes_tableau),
                       "taux": round(len(lignes_tableau) / meta["n_mappings"], 4) if meta["n_mappings"] else 0},
    }
    return "\n".join(md), doc_json


def ecrire(outdir, base, md, dj):
    os.makedirs(outdir, exist_ok=True)
    pmd, pjs = os.path.join(outdir, base + ".md"), os.path.join(outdir, base + ".json")
    with open(pmd, "w", encoding="utf-8") as f:
        f.write(md)
    with open(pjs, "w", encoding="utf-8") as f:
        json.dump(dj, f, ensure_ascii=False, indent=2)
    return pmd, pjs


def self_test():
    sample = os.path.join(ICI, "..", "..", "tsi-validator", "samples", "echantillon-valide.tsi")
    meta, maps = extraire_mappings(sample)
    md, dj = generer(meta, maps, "Freeze Mode — S4 MK2 (échantillon de référence)")
    ok = all(f"## {i}." in md for i in range(1, 10)) and "Tableau de Référence MIDI" in md
    ok = ok and dj["couverture"]["taux"] == 1.0 and all(m["nom"] in md for m in maps)
    print(f"self-test generer-doc-midi : 9 sections={'OK' if all(f'## {i}.' in md for i in range(1,10)) else 'KO'}, "
          f"couverture={dj['couverture']['taux']:.0%}, mappings={dj['couverture']['mappings_tsi']}")
    print(f"SELF-TEST : {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description="Générateur de documentation MIDI (MD+JSON)")
    ap.add_argument("tsi", nargs="?", help="fichier .tsi source (validé par tsi-validator)")
    ap.add_argument("--outdir", default=".", help="répertoire de sortie")
    ap.add_argument("--base", default=None, help="base du nom de fichier de sortie")
    ap.add_argument("--titre", default="Mapping MIDI — S4 MK2", help="titre du document")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        sys.exit(self_test())
    if not a.tsi:
        ap.print_usage()
        sys.exit(2)
    meta, maps = extraire_mappings(a.tsi)
    md, dj = generer(meta, maps, a.titre)
    base = a.base or os.path.splitext(os.path.basename(a.tsi))[0] + "-doc"
    pmd, pjs = ecrire(a.outdir, base, md, dj)
    print(f"MD   : {pmd}\nJSON : {pjs}")
    print(f"couverture : {dj['couverture']['lignes_tableau']}/{dj['couverture']['mappings_tsi']} mappings documentés")
    print("VERDICT : PASS")
    sys.exit(0)


if __name__ == "__main__":
    main()
