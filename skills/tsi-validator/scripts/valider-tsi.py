#!/usr/bin/env python3
"""valider-tsi.py — Arbitre mécanique de validation des fichiers TSI.

Skill : tsi-validator v1.1.0 (Projet TSI/Traktor — S4 MK2 / Traktor Pro 3.11)
Schéma de référence : download/spec-projet-tsi-traktor.md §5 (règles R1-R8,
catégories d'erreur E1-E8). PROVENANCE : reverse-engineering public IvanZ 2014
+ articles NI Controller Manager + mappings TSI tiers documentés, cible actuelle S4 MK2 (R-1 :
extension déclarative en cas d'écart avec un TSI réel — interface stable).

Usage :
  valider-tsi.py <fichier.tsi> [<fichier2.tsi> ...] [--json]
  valider-tsi.py --self-test
Exit code : 0 ssi tous les fichiers verdict PASS ; 1 sinon ; 2 usage invalide.
Python stdlib uniquement (N3). Ne modifie jamais les fichiers validés.
"""
import argparse
import json
import os
import sys
import xml.etree.ElementTree as ET

ICI = os.path.dirname(os.path.abspath(__file__))
GROUPES = {"Deck A", "Deck B", "Deck C", "Deck D", "Focus", "Mixer", "Master", "Global"}
MESSAGES = {"NOTE", "CC", "PB", "PC"}
MODES = {"Direct", "Toggle", "Inverse", "Increment", "Decrement", "Reset"}


def _int(v):
    try:
        return int(str(v).strip())
    except (TypeError, ValueError):
        return None


def valider_fichier(path):
    """Valide un TSI contre les règles R1-R8 → rapport dict (erreurs E1-E8)."""
    rapport = {"fichier": path, "verdict": "FAIL", "erreurs": [], "stats": {}}
    err = lambda cat, det: rapport["erreurs"].append({"categorie": cat, "detail": det})
    try:
        arbre = ET.parse(path)
    except ET.ParseError as e:
        err("E1-structure", f"XML mal formé : {e}")
        return rapport
    racine = arbre.getroot()
    if racine.tag != "NISYSTEM":
        err("E1-structure", f"racine attendue NISYSTEM, trouvée {racine.tag!r}")
    if _int(racine.get("VERSION")) is None:
        err("E1-structure", "attribut VERSION manquant ou non entier sur NISYSTEM")
    devices = racine.findall("DEVICE")
    if len(devices) != 1:
        err("E1-structure", f"{len(devices)} éléments DEVICE (attendu 1)")
        return rapport
    dev = devices[0]
    for att in ("NAME", "TYPE", "IN_PORT", "OUT_PORT", "DECK_TARGET"):
        if not (dev.get(att) or "").strip():
            err("E1-structure", f"attribut {att} manquant/vide sur DEVICE")
    blocs = racine.findall("DEVICE/MAPPINGS")
    if len(blocs) != 1:
        err("E2-comptage", f"{len(blocs)} blocs MAPPINGS (attendu 1)")
        return rapport
    mappings = blocs[0].findall("MAPPING")
    count = _int(blocs[0].get("COUNT"))
    if count != len(mappings):
        err("E2-comptage", f"COUNT={count} mais {len(mappings)} MAPPING enfants")
    vus_noms, vus_in, sources_mod, conditions = {}, [], set(), set()
    for m in mappings:
        nom = (m.get("NAME") or "").strip()
        if not nom:
            err("E3-attributs", "MAPPING sans NAME")
        elif nom in vus_noms:
            err("E3-attributs", f"NAME dupliqué : {nom!r}")
        vus_noms[nom] = vus_noms.get(nom, 0) + 1
        typ = (m.get("TYPE") or "").strip()
        if typ not in ("IN", "OUT"):
            err("E3-attributs", f"{nom!r} : TYPE invalide {typ!r} (attendu IN|OUT)")
        groupe = (m.get("GROUP") or "").strip()
        if groupe not in GROUPES:
            err("E3-attributs", f"{nom!r} : GROUP invalide {groupe!r}")
        if not (m.get("CONTROL") or "").strip():
            err("E3-attributs", f"{nom!r} : CONTROL manquant/vide")
        cond = {}
        mod = m.find("MODIFIER")
        if mod is not None:
            for k, v in mod.attrib.items():
                if not (k.startswith("M") and k[1:].isdigit() and 1 <= int(k[1:]) <= 8):
                    err("E8-modifier", f"{nom!r} : attribut modifier invalide {k!r}")
                    continue
                if _int(v) not in (0, 1):
                    err("E8-modifier", f"{nom!r} : {k}={v!r} (binaire 0/1 attendu)")
                else:
                    cond[f"Modifier {k[1:]}"] = _int(v)
        for k, v in cond.items():
            conditions.add(k)
        if typ == "IN":
            midi = m.findall("MIDI")
            if len(midi) != 1:
                err("E4-plages", f"{nom!r} : {len(midi)} éléments MIDI (attendu 1)")
            else:
                at = midi[0]
                ch, ms = _int(at.get("CHANNEL")), (at.get("MESSAGE") or "").strip()
                no, mo = _int(at.get("NUMBER")), (at.get("MODE") or "").strip()
                if ch is None or not 0 <= ch <= 15:
                    err("E4-plages", f"{nom!r} : CHANNEL={at.get('CHANNEL')!r} (0-15 attendu)")
                if ms not in MESSAGES:
                    err("E4-plages", f"{nom!r} : MESSAGE={ms!r} ({'|'.join(sorted(MESSAGES))} attendu)")
                if ms in ("NOTE", "CC") and (no is None or not 0 <= no <= 127):
                    err("E4-plages", f"{nom!r} : NUMBER={at.get('NUMBER')!r} (0-127 attendu pour {ms})")
                if mo not in MODES:
                    err("E4-plages", f"{nom!r} : MODE={mo!r} ({'|'.join(sorted(MODES))} attendu)")
                cle = (ch, ms, no, tuple(sorted(cond.items())))
                vus_in.append((cle, nom))
        for led in m.findall("LED"):
            if typ != "OUT":
                err("E6-led", f"{nom!r} : LED dans un MAPPING TYPE=IN (OUT uniquement)")
            if led.get("MODE") != "Output":
                err("E6-led", f"{nom!r} : LED MODE={led.get('MODE')!r} (Output attendu)")
            if _int(led.get("NUMBER")) is None or not 0 <= _int(led.get("NUMBER")) <= 127:
                err("E6-led", f"{nom!r} : LED NUMBER={led.get('NUMBER')!r} (0-127 attendu)")
            for att in ("ON", "OFF"):
                if _int(led.get(att)) is None or not 0 <= _int(led.get(att)) <= 127:
                    err("E6-led", f"{nom!r} : LED {att}={led.get(att)!r} (0-127 attendu)")
    vus = {}
    for cle, nom in vus_in:
        if cle in vus:
            err("E5-doublon", f"{nom!r} : MIDI {cle[1]} {cle[2]} ch{cle[0]} déjà alloué à {vus[cle]!r} (mêmes conditions)")
        vus[cle] = nom
    for m in mappings:
        if (m.get("CONTROL") or "").strip().startswith("Modifier "):
            sources_mod.add(m.get("CONTROL").strip())
    for manque in sorted(conditions - sources_mod):
        err("E7-multishift", f"couche morte : condition {manque} sans mapping source ({manque} absent des CONTROL)")
    rapport["stats"] = {"mappings": len(mappings), "in": len(vus_in),
                        "out": len(mappings) - len(vus_in), "couches_logiques": sorted(sources_mod)}
    rapport["verdict"] = "PASS" if not rapport["erreurs"] else "FAIL"
    return rapport


def self_test():
    """Valide les golden samples : valide→PASS ; invalide→FAIL avec E1-E8."""
    v = valider_fichier(os.path.join(ICI, "..", "samples", "echantillon-valide.tsi"))
    i = valider_fichier(os.path.join(ICI, "..", "samples", "echantillon-invalide.tsi"))
    cats = {e["categorie"].split("-")[0] for e in i["erreurs"]}
    ok = v["verdict"] == "PASS" and i["verdict"] == "FAIL" and cats >= {"E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8"}
    print(f"self-test tsi-validator : échantillon valide → {v['verdict']} ; "
          f"échantillon invalide → {i['verdict']} ; catégories déclenchées : {sorted(cats)}")
    print(f"SELF-TEST : {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description="Arbitre mécanique de validation TSI (E1-E8)")
    ap.add_argument("fichiers", nargs="*", help="fichiers .tsi à valider")
    ap.add_argument("--json", action="store_true", help="rapport JSON sur stdout")
    ap.add_argument("--self-test", action="store_true", help="golden samples (valide PASS, invalide FAIL)")
    a = ap.parse_args()
    if a.self_test:
        sys.exit(self_test())
    if not a.fichiers:
        ap.print_usage()
        sys.exit(2)
    rapports = [valider_fichier(f) for f in a.fichiers]
    if a.json:
        print(json.dumps(rapports, ensure_ascii=False, indent=2))
    else:
        for r in rapports:
            print(f"{r['fichier']} → {r['verdict']} ({len(r['erreurs'])} erreur(s), "
                  f"{r['stats'].get('mappings', 0)} mappings)")
            for e in r["erreurs"]:
                print(f"  [{e['categorie']}] {e['detail']}")
    verdict = all(r["verdict"] == "PASS" for r in rapports)
    print(f"VERDICT : {'PASS' if verdict else 'FAIL'}")
    sys.exit(0 if verdict else 1)


if __name__ == "__main__":
    main()
