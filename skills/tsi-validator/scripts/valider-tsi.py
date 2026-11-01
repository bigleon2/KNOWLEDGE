#!/usr/bin/env python3
"""valider-tsi.py — Arbitre mécanique de validation des fichiers TSI (BI-RACINE).

Skill : tsi-validator v1.2.0 (Projet TSI/Traktor — S4 MK2/MK3 / Traktor Pro 3.11)
Schéma de référence : download/spec-projet-tsi-traktor.md §5 (règles R1-R8,
catégories d'erreur E1-E8). PROVENANCE : reverse-engineering public IvanZ 2014
+ articles NI Controller Manager + mappings TSI tiers S4 MK3 documentés (R-1 :
extension déclarative en cas d'écart avec un TSI réel — interface stable).

v1.2.0 (2026-11-02, directive propriétaire — pendante Task 33 n°1) : évolution
BI-RACINE. Deux formats acceptés en E1 :
  - NISYSTEM (déclaratif) : chemins E1-E8 historiques inchangés (non-régression
    sur les golden samples) ;
  - NIXML (réel Traktor Pro 3.11 — constats Task 33 : DJTT v2.1.0 et DREW) :
    validation structurelle du blob DIOM embarqué (Entry
    DeviceIO.Config.Controller@Value en base64) : magique DIOM, hiérarchie
    DEVS→DEVI→DDAT→DDDC→DDCB→CMAS→CMAI/CMAD + DCBM, cohérence des comptes
    déclarés/lus (E2), device lisible (E3). La sémantique E4-E8 du contenu
    binaire (plages MIDI, doublons, LED, couches mortes, modificateurs) reste
    du ressort du moteur analyse-doc-s4mk2 (R4 jamais dupliquer — délégation
    documentée, pas de substitution).

Usage :
  valider-tsi.py <fichier.tsi> [<fichier2.tsi> ...] [--json]
  valider-tsi.py --self-test
Exit code : 0 ssi tous les fichiers verdict PASS ; 1 sinon ; 2 usage invalide.
Python stdlib uniquement (N3). Ne modifie jamais les fichiers validés.
"""
import argparse
import base64
import json
import os
import struct
import sys
import tempfile
import xml.etree.ElementTree as ET

ICI = os.path.dirname(os.path.abspath(__file__))
GROUPES = {"Deck A", "Deck B", "Deck C", "Deck D", "Focus", "Mixer", "Master", "Global"}
RACINES = {"NISYSTEM": "déclaratif", "NIXML": "réel"}
ENTRY_CTRL = "DeviceIO.Config.Controller"
MESSAGES = {"NOTE", "CC", "PB", "PC"}
MODES = {"Direct", "Toggle", "Inverse", "Increment", "Decrement", "Reset"}


def _int(v):
    try:
        return int(str(v).strip())
    except (TypeError, ValueError):
        return None


def _u32(buf, off):
    return struct.unpack_from(">I", buf, off)[0]


def _trames(buf, deb, fin):
    """Itère (fourcc, d, f) les trames FourCC+u32 taille dans [deb, fin)."""
    off = deb
    while off + 8 <= fin:
        fcc = buf[off:off + 4].decode("latin-1")
        taille = _u32(buf, off + 4)
        d, f = off + 8, off + 8 + taille
        if f > fin:
            raise ValueError(f"trame {fcc} déborde (off={off}, taille={taille}, fin={fin})")
        yield fcc, d, f
        off = f


def _utf16_at(buf, off):
    """Chaîne UTF-16-BE [u32 n][n × 2 o] à l'offset donné."""
    n = _u32(buf, off)
    return buf[off + 4:off + 4 + 2 * n].decode("utf-16-be", errors="replace")


def valider_nixml(path, err):
    """Voie réelle NIXML : validation structurelle du blob DIOM embarqué.

    Vérifie E1 (Entry contrôleur, base64, magique DIOM, hiérarchie de trames),
    E2 (comptes déclarés == lus : DDCI/DDCO, CMAI/CMAD, DCBM) et E3 (device).
    Retourne un dict stats (format, device, comptes). Les règles E4-E8 du
    contenu binaire relèvent du moteur analyse-doc-s4mk2 (délégation R4).
    """
    stats = {"format": "réel NIXML"}
    try:
        arbre = ET.parse(path)
    except ET.ParseError as e:
        err("E1-structure", f"XML mal formé : {e}")
        return stats
    racine = arbre.getroot()
    if racine.tag != "NIXML":
        err("E1-structure", f"racine NIXML attendue, trouvée {racine.tag!r}")
        return stats
    ctrl = next((e for e in racine.iter("Entry") if e.get("Name") == ENTRY_CTRL), None)
    if ctrl is None:
        err("E1-structure", f"Entry {ENTRY_CTRL!r} absente — TSI de préférences (pas un mapping)")
        return stats
    try:
        blob = base64.b64decode((ctrl.get("Value") or ctrl.text or "").strip())
    except Exception as e:
        err("E1-structure", f"blob base64 illisible : {e}")
        return stats
    if not blob.startswith(b"DIOM"):
        err("E1-structure", "magique DIOM absent du blob décodé")
        return stats
    try:
        diom = next(_trames(blob, 0, len(blob)))
        devs = next(t for t in _trames(blob, diom[1], diom[2]) if t[0] == "DEVS")
        nb_dev = _u32(blob, devs[1])
        if nb_dev != 1:
            err("E3-attributs", f"DEVS déclare {nb_dev} devices (attendu 1)")
        devi = next(_trames(blob, devs[1] + 4, devs[2]))
        n_nom = _u32(blob, devi[1])
        nom_dev = _utf16_at(blob, devi[1])
        if not nom_dev.strip():
            err("E3-attributs", "device DEVI sans nom lisible")
        ddat = next(t for t in _trames(blob, devi[1] + 4 + 2 * n_nom, devi[2]) if t[0] == "DDAT")
        dmap = {f: (d, f2) for f, d, f2 in _trames(blob, ddat[1], ddat[2])}
        for req in ("DDDC", "DDCB"):
            if req not in dmap:
                err("E2-comptage", f"bloc {req} absent de DDAT")
                return stats
        dmap2 = {f: (d, f2) for f, d, f2 in _trames(blob, dmap["DDDC"][0], dmap["DDDC"][1])}
        for fcc, lab in (("DDCI", "in"), ("DDCO", "out")):
            if fcc not in dmap2:
                err("E2-comptage", f"{fcc} absent de DDDC")
                continue
            d, f2 = dmap2[fcc]
            nb = _u32(blob, d)
            lus = sum(1 for t in _trames(blob, d + 4, f2) if t[0] == "DCDT")
            if lus != nb:
                err("E2-comptage", f"{fcc} : déclaré {nb}, lues {lus}")
        dmap3 = {f: (d, f2) for f, d, f2 in _trames(blob, dmap["DDCB"][0], dmap["DDCB"][1])}
        cmad_lus, cmai_lus, dcbm_lus = 0, 0, 0
        if "CMAS" in dmap3:
            d, f2 = dmap3["CMAS"]
            nb_cmai = _u32(blob, d)
            for fcc2, d2, f22 in _trames(blob, d + 4, f2):
                if fcc2 != "CMAI":
                    continue
                cmai_lus += 1
                fcc_c = blob[d2 + 12:d2 + 16].decode("latin-1")
                taille_c = _u32(blob, d2 + 16)
                if fcc_c == "CMAD" and d2 + 20 + taille_c <= f22:
                    cmad_lus += 1
            if cmai_lus != nb_cmai:
                err("E2-comptage", f"CMAS : {nb_cmai} CMAI déclarés, {cmai_lus} lus")
        else:
            err("E2-comptage", "CMAS absent de DDCB")
        if "DCBM" in dmap3:
            d, f2 = dmap3["DCBM"]
            nb_dcbm = _u32(blob, d)
            dcbm_lus = sum(1 for t in _trames(blob, d + 4, f2) if t[0] == "DCBM")
            if dcbm_lus != nb_dcbm:
                err("E2-comptage", f"DCBM : déclaré {nb_dcbm}, lus {dcbm_lus}")
        else:
            err("E2-comptage", "DCBM absent de DDCB")
        if cmai_lus and cmad_lus and cmai_lus != cmad_lus:
            err("E2-comptage", f"CMAD embarqués {cmad_lus} ≠ CMAI lus {cmai_lus}")
        stats.update({"device": nom_dev, "cmai": cmai_lus, "dcbm": dcbm_lus})
    except (StopIteration, ValueError, struct.error) as e:
        err("E1-structure", f"trame DIOM illisible : {e}")
    return stats


def valider_fichier(path):
    """Valide un TSI (bi-racine) contre les règles → rapport dict (erreurs E1-E8)."""
    rapport = {"fichier": path, "verdict": "FAIL", "erreurs": [], "stats": {}}
    err = lambda cat, det: rapport["erreurs"].append({"categorie": cat, "detail": det})
    try:
        arbre = ET.parse(path)
    except ET.ParseError as e:
        err("E1-structure", f"XML mal formé : {e}")
        return rapport
    racine = arbre.getroot()
    if racine.tag == "NIXML":
        rapport["stats"].update(valider_nixml(path, err))
        rapport["verdict"] = "PASS" if not rapport["erreurs"] else "FAIL"
        return rapport
    if racine.tag != "NISYSTEM":
        err("E1-structure", f"racine attendue {' ou '.join(sorted(RACINES))}, trouvée {racine.tag!r}")
    rapport["stats"]["format"] = "déclaratif NISYSTEM"
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


def _fixture_nixml(path, nb_cmai_decl, nb_cmai_reel=1):
    """Écrit une fixture NIXML (blob DIOM minimal) pour le self-test bi-racine."""
    u = lambda n: n.to_bytes(4, "big")
    t = lambda s: u(len(s)) + s.encode("utf-16-be")
    fr = lambda fcc, p: fcc.encode("latin-1") + u(len(p)) + p
    cmad_p = u(0) + b"\x00" * 16
    cmai = fr("CMAI", u(0) + u(0) + u(101) + b"CMAD" + u(len(cmad_p)) + cmad_p)
    if nb_cmai_reel > 1:
        cmai += fr("CMAI", u(1) + u(0) + u(101) + b"CMAD" + u(len(cmad_p)) + cmad_p)
    cmas = u(nb_cmai_decl) + cmai
    dcbm = fr("DCBM", u(1) + fr("DCBM", u(101) + t("Left.Play")))
    ddat = fr("DDAT", fr("DDIV", t("2.11.0")) + fr("DDIC", t("")) +
              fr("DDDC", fr("DDCI", u(0)) + fr("DDCO", u(0))) +
              fr("DDCB", fr("CMAS", cmas) + dcbm))
    devi = fr("DEVI", t("Traktor.Kontrol S4.Test") + ddat)
    blob = fr("DIOM", fr("DEVS", u(1) + devi))
    import base64 as _b64
    with open(path, "w", encoding="utf-8") as fh:
        fh.write('<NIXML VERSION="3.11.0">\n'
                 f'  <Entry Name="{ENTRY_CTRL}" Value="{_b64.b64encode(blob).decode()}"/>\n'
                 '</NIXML>')


def self_test():
    """Golden samples NISYSTEM (non-régression) + fixtures NIXML (voie réelle)."""
    v = valider_fichier(os.path.join(ICI, "..", "samples", "echantillon-valide.tsi"))
    i = valider_fichier(os.path.join(ICI, "..", "samples", "echantillon-invalide.tsi"))
    cats = {e["categorie"].split("-")[0] for e in i["erreurs"]}
    ok_decl = v["verdict"] == "PASS" and i["verdict"] == "FAIL" and \
        cats >= {"E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8"}
    with tempfile.TemporaryDirectory() as tmp:
        p_ok = os.path.join(tmp, "nixml-valide.tsi")
        p_ko = os.path.join(tmp, "nixml-invalide.tsi")
        _fixture_nixml(p_ok, 1)
        _fixture_nixml(p_ko, 2, nb_cmai_reel=1)  # 2 déclarés, 1 réel → E2
        vr = valider_fichier(p_ok)
        ir = valider_fichier(p_ko)
    ok_reel = vr["verdict"] == "PASS" and ir["verdict"] == "FAIL" and \
        any(e["categorie"].startswith("E2") for e in ir["erreurs"]) and \
        vr["stats"].get("format") == "réel NIXML"
    print(f"self-test tsi-validator v1.2.0 :")
    print(f"  déclaratif NISYSTEM : valide → {v['verdict']} ; invalide → {i['verdict']} ; "
          f"catégories : {sorted(cats)}")
    print(f"  réel NIXML : valide → {vr['verdict']} ({vr['stats'].get('device')}, "
          f"CMAI={vr['stats'].get('cmai')}) ; invalide → {ir['verdict']} "
          f"({[e['detail'] for e in ir['erreurs']]})")
    ok = ok_decl and ok_reel
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
        print(json.dumps(rapports, ensure_ascii=False, indent=2), file=sys.stdout)
        verdict = all(r["verdict"] == "PASS" for r in rapports)
        print(f"VERDICT : {'PASS' if verdict else 'FAIL'}", file=sys.stderr)
        sys.exit(0 if verdict else 1)
    for r in rapports:
        fmt = r["stats"].get("format", "")
        print(f"{r['fichier']} → {r['verdict']} [{fmt}] ({len(r['erreurs'])} erreur(s), "
              f"{r['stats'].get('mappings', 0)} mappings)")
        for e in r["erreurs"]:
            print(f"  [{e['categorie']}] {e['detail']}")
    verdict = all(r["verdict"] == "PASS" for r in rapports)
    print(f"VERDICT : {'PASS' if verdict else 'FAIL'}")
    sys.exit(0 if verdict else 1)


if __name__ == "__main__":
    main()
