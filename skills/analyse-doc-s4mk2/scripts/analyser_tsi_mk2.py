#!/usr/bin/env python3
"""analyser-tsi-mk2.py v1.0.0 — Moteur d'analyse d'un TSI de mapping S4 MK2 (format réel DIOM).

Skill : analyse-doc-s4mk2 (famille TSI). Base : analyse-djtt-mk2.py v1.1.0
(session Task 33, self-test PASS — re-jeu ×2 byte-stable, référentiel G2 10/10).

Format (référentiel G2 §2.2, cf. references/referentiel-g2.md) : NIXML → Entry
DeviceIO.Config.Controller (attribut Value, Base64) → blob DIOM ; trames
FourCC + u32 taille, big-endian intégral, chaînes UTF-16-BE [u32 n][n × 2 o].
Trame CMAD EMBARQUÉE dans CMAI (FourCC @+12, taille @+16, payload @+20) ;
nom de commande localisé mécaniquement (scan 4-aligné) ; contrôles distincts
comptés par NOMS (163) et non par ids DCBM (5626).

Robustesse : rejet propre (exit 2 usage/chemin, exit 1 écart, message sans
traceback) pour : fichier absent, XML non-TSI, Entry absente (préférences
Traktor), blob non-DIOM, trame débordante. Ne modifie jamais le fichier analysé.

Usage :
  analyser-tsi-mk2.py <fichier.tsi> [--json OUT.json]
  analyser-tsi-mk2.py <fichier.tsi> --self-test
Exit code : 0 ssi conformité au référentiel G2 (échantillon DJTT v2.1.0) ;
1 écart/écart de conformité ; 2 usage/chemin/structure non-mapping.
Python stdlib uniquement.
"""
import argparse
import base64
import json
import os
import struct
import sys
import xml.etree.ElementTree as ET

ENTRY = "DeviceIO.Config.Controller"

# Référentiel Task 7 G2 (comptes publiés, vérifiables mécaniquement).
# ERRATUM Task 33 (diag-cmad2/diag-illisibles, motifs BE/LE + scan tous offsets) :
# les 666 CMAD de taille 120 n'ont AUCUN champ nom (payload purement numérique,
# vérifié à tous les offsets) → noms lisibles 4960 (88,17 %) et 393 commandes
# distinctes. Les 4970/394 publiés en G2 incluaient un artefact du décodeur
# d'origine (perdu) — +10 assignations / +1 commande non reproductibles.
REFERENTIEL_G2 = {
    "CMAI": 5626, "CMAD_lus": 5626, "DCBM": 5626,
    "DCDT_in": 125, "DCDT_out": 220, "DCDT_total": 345,
    "controles_distincts": 163, "commandes_distinctes": 393,
    "refs_resolues": 5136, "refs_non_resolues": 490,
}
# Valeurs strictes attendues par le self-test (baseline locale reproductible)
BASELINE_STRICTE = {"noms_commandes_lisibles": 4960, "CMAD_illisibles": 666}


class RejetPropre(Exception):
    """Erreur contrôlée : message propre sans traceback, avec code de retour dédié (1 écart, 2 usage)."""

    def __init__(self, message, rc=1):
        super().__init__(message)
        self.rc = rc


def u32(buf, off):
    return struct.unpack_from(">I", buf, off)[0]


def utf16(buf, off):
    """Lit une chaîne UTF-16-BE [u32 n][n × 2 o] → (texte, nouvel offset)."""
    n = u32(buf, off)
    off += 4
    txt = buf[off:off + 2 * n].decode("utf-16-be", errors="replace")
    return txt, off + 2 * n


def frames(buf, start, end):
    """Itère les trames FourCC+u32 taille dans [start, end)."""
    off = start
    while off + 8 <= end:
        fcc = buf[off:off + 4].decode("latin-1")
        taille = u32(buf, off + 4)
        corps_deb, corps_fin = off + 8, off + 8 + taille
        if corps_fin > end:
            raise RejetPropre(f"ABANDON : trame {fcc} déborde (off={off}, taille={taille}, fin={end}) — blob tronqué ou corrompu")
        yield fcc, corps_deb, corps_fin
        off = corps_fin


def lisible(txt):
    return bool(txt) and "\x00" not in txt and any(c.isprintable() and not c.isspace() for c in txt)


def nom_cmad(buf, deb, fin):
    """Localise mécaniquement le nom de commande dans un payload CMAD (scan 4-aligné)."""
    off = deb + 16
    while off + 8 <= fin:
        n = u32(buf, off)
        if 0 < n <= 200 and off + 4 + 2 * n <= fin:
            brut = buf[off + 4:off + 4 + 2 * n]
            try:
                txt = brut.decode("utf-16-be")
            except UnicodeDecodeError:
                txt = ""
            if lisible(txt) and all(ord(c) >= 32 or c in "\t" for c in txt):
                return txt, off
        off += 4
    return "", None


def extraire_blob(path):
    """Extrait le blob DIOM d'un TSI mapping. Rejets propres sinon."""
    if not os.path.isfile(path):
        raise RejetPropre(f"USAGE : fichier introuvable : {path}")
    try:
        racine = ET.parse(path).getroot()
    except ET.ParseError as e:
        raise RejetPropre(f"REJET PROPRE : XML invalide ({e}) — ce n'est pas un fichier TSI")
    for entry in racine.iter("Entry"):
        if entry.get("Name") == ENTRY:
            val = entry.get("Value") or (entry.text or "")
            try:
                return base64.b64decode(val.strip())
            except Exception as e:  # noqa: BLE001 — rejet contrôlé
                raise RejetPropre(f"REJET PROPRE : base64 du blob corrompu ({e})")
    raise RejetPropre(
        "REJET PROPRE : Entry DeviceIO.Config.Controller absente — fichier de "
        "préférences Traktor (pas un mapping) ; utiliser les TSI de mapping uniquement")


def analyser(path):
    blob = extraire_blob(path)
    meta, alertes = {"fichier": path, "taille_blob": len(blob)}, []
    top = list(frames(blob, 0, len(blob)))
    if not top or top[0][0] != "DIOM":
        raise RejetPropre(f"ABANDON : magique DIOM absent (trames={top[:2]})")
    diom_deb, diom_fin = top[0][1], top[0][2]
    sous = list(frames(blob, diom_deb, diom_fin))
    devs = next((s for s in sous if s[0] == "DEVS"), None)
    if devs is None:
        raise RejetPropre("ABANDON : trame DEVS absente du DIOM")
    nb_dev = u32(blob, devs[1])
    dev = list(frames(blob, devs[1] + 4, devs[2]))[0]  # DEVI
    off = dev[1]
    n_nom = u32(blob, off)
    off += 4
    meta["device"] = blob[off:off + 2 * n_nom].decode("utf-16-be", errors="replace")
    off += 2 * n_nom
    ddat_frame = list(frames(blob, off, dev[2]))[0]
    ddat_map = {f: (d, f2) for f, d, f2 in frames(blob, ddat_frame[1], ddat_frame[2])}
    meta["ddiv"], _ = utf16(blob, ddat_map["DDIV"][0])
    meta["ddic"], _ = utf16(blob, ddat_map["DDIC"][0])
    # DDDC : conditions/modifiers → DDCI (in) + DDCO (out), DCDT × n
    conditions_in, conditions_out = [], []
    dddc_map = {f: (d, f2) for f, d, f2 in frames(blob, ddat_map["DDDC"][0], ddat_map["DDDC"][1])}
    for fcc, cible in (("DDCI", conditions_in), ("DDCO", conditions_out)):
        if fcc not in dddc_map:
            alertes.append(f"{fcc} absent de DDDC")
            continue
        d, f2 = dddc_map[fcc]
        nb = u32(blob, d)
        items = list(frames(blob, d + 4, f2))
        lus = 0
        for i, (fcc2, d2, f22) in enumerate(items):
            if fcc2 != "DCDT":
                continue
            try:
                nom, _ = utf16(blob, d2)
                cible.append(nom)
                lus += 1
            except Exception:
                cible.append(f"<dcdt#{i}:illisible>")
        if lus != nb:
            alertes.append(f"{fcc} : déclaré {nb}, lues {lus}")
    # DDCB : CMAS (CMAI → CMAD embarqué) + DCBM
    ddcb_map = {f: (d, f2) for f, d, f2 in frames(blob, ddat_map["DDCB"][0], ddat_map["DDCB"][1])}
    cm_d, cm_f = ddcb_map["CMAS"]
    nb_cmai = u32(blob, cm_d)
    commandes, cmai_bruts, cmad_illisibles, types_cmad = {}, [], 0, {}
    for fcc, d, f2 in frames(blob, cm_d + 4, cm_f):
        if fcc != "CMAI":
            continue
        ordinal, drapeau, ref = u32(blob, d), u32(blob, d + 4), u32(blob, d + 8)
        fcc_c = blob[d + 12:d + 16].decode("latin-1")
        taille_cmad = u32(blob, d + 16)
        nom = ""
        if fcc_c == "CMAD" and d + 20 + taille_cmad <= f2:
            pc_deb, pc_fin = d + 20, d + 20 + taille_cmad
            types_cmad[u32(blob, pc_deb)] = types_cmad.get(u32(blob, pc_deb), 0) + 1
            nom, _ = nom_cmad(blob, pc_deb, pc_fin)
        if nom:
            commandes[nom] = commandes.get(nom, 0) + 1
        else:
            cmad_illisibles += 1
        cmai_bruts.append({"ordinal": ordinal, "drapeau": drapeau, "ref": ref, "commande": nom})
    db_d, db_f = ddcb_map["DCBM"]
    nb_dcbm = u32(blob, db_d)
    controles = {}
    for fcc, d, f2 in frames(blob, db_d + 4, db_f):
        if fcc != "DCBM":
            continue
        cid = u32(blob, d)
        try:
            nom, _ = utf16(blob, d + 4)
        except Exception:
            nom = f"<dcbm#{cid}:illisible>"
        controles[cid] = nom
    # Résolution des références + sollicitation des contrôles (par NOM)
    resolus, non_resolus, solli = 0, 0, {}
    for a in cmai_bruts:
        nom_c = controles.get(a["ref"])
        if nom_c is None:
            non_resolus += 1
        else:
            resolus += 1
            solli[nom_c] = solli.get(nom_c, 0) + 1
    noms_controles = set(controles.values())
    noms_definis = {}
    for nom in controles.values():
        noms_definis[nom] = noms_definis.get(nom, 0) + 1
    meta.update({
        "comptes": {
            "DEVI": nb_dev, "DCDT_in": len(conditions_in), "DCDT_out": len(conditions_out),
            "DCDT_total": len(conditions_in) + len(conditions_out),
            "CMAI": nb_cmai, "CMAD_lus": len(cmai_bruts), "CMAD_illisibles": cmad_illisibles,
            "DCBM": nb_dcbm, "controles_distincts": len(noms_controles),
            "commandes_distinctes": len(commandes),
            "refs_resolues": resolus, "refs_non_resolues": non_resolus,
        },
        "noms_commandes_lisibles": sum(commandes.values()),
        "types_cmad": dict(sorted(types_cmad.items())),
        "conditions_in": conditions_in, "conditions_out": conditions_out,
        "noms_controles_definis": dict(sorted(noms_definis.items(), key=lambda kv: (-kv[1], kv[0]))),
        "controles_par_sollicitation": dict(sorted(solli.items(), key=lambda kv: -kv[1])),
        "commandes_par_assignations": dict(sorted(commandes.items(), key=lambda kv: -kv[1])),
        "alertes": alertes,
    })
    return meta


def verifier_g2(meta):
    """Vérifie les 10 comptes du référentiel G2 → (écarts dict, bool conforme)."""
    c = meta["comptes"]
    ecarts = {k: {"attendu": v, "observe": c.get(k)} for k, v in REFERENTIEL_G2.items() if c.get(k) != v}
    return ecarts, not ecarts


def self_test(chemin):
    """Test de validation complet : analyse + conformité G2 + stabilité ×2."""
    print(f"SELF-TEST analyser-tsi-mk2 (skill analyse-doc-s4mk2) — cible : {chemin}")
    m1 = analyser(chemin)
    j1 = json.dumps(m1, ensure_ascii=False, sort_keys=True)
    m2 = analyser(chemin)
    j2 = json.dumps(m2, ensure_ascii=False, sort_keys=True)
    stable = j1 == j2
    ecarts, conforme = verifier_g2(m1)
    lisibles = m1["noms_commandes_lisibles"]
    ratio = lisibles / m1["comptes"]["CMAI"]
    strict_ok = (lisibles == BASELINE_STRICTE["noms_commandes_lisibles"]
                 and m1["comptes"]["CMAD_illisibles"] == BASELINE_STRICTE["CMAD_illisibles"])
    print(f"  re-jeu ×2 byte-stable        : {'PASS' if stable else 'FAIL'}")
    print(f"  conformité référentiel G2    : {'PASS (10/10)' if conforme else f'FAIL {ecarts}'}")
    print(f"  baseline stricte locale      : {'PASS' if strict_ok else 'FAIL'} (lisibles=4960, illisibles=666)")
    print(f"  noms lisibles {lisibles} ({ratio:.1%})")
    print(f"  device : {m1['device']}")
    print(f"  titre  : {m1['ddic']}")
    verdict = stable and conforme and strict_ok
    print(f"SELF-TEST : {'PASS' if verdict else 'FAIL'}")
    return 0 if verdict else 1


def main():
    ap = argparse.ArgumentParser(description="Analyse un TSI de mapping S4 MK2 (format réel DIOM)")
    ap.add_argument("fichier", nargs="?")
    ap.add_argument("--json", help="écrire le rapport JSON complet dans ce fichier")
    ap.add_argument("--self-test", action="store_true",
                    help="test de validation : re-jeu ×2 + conformité référentiel G2")
    try:
        a = ap.parse_args()
        if not a.fichier:
            ap.print_usage()
            raise RejetPropre("USAGE : fichier .tsi requis", 2)
        if a.self_test:
            sys.exit(self_test(a.fichier))
        meta = analyser(a.fichier)
        c = meta["comptes"]
        print(f"fichier        : {meta['fichier']}")
        print(f"device         : {meta['device']}")
        print(f"titre (DDIC)   : {meta['ddic']}")
        print(f"comptes        : {json.dumps(c, ensure_ascii=False)}")
        if a.json:
            with open(a.json, "w", encoding="utf-8") as fh:
                json.dump(meta, fh, ensure_ascii=False, indent=2)
            print(f"JSON → {a.json}")
        ecarts, conforme = verifier_g2(meta)
        print(f"VERIFICATION REFERENTIEL G2 : {'CONFORME (10/10)' if conforme else f'ECARTS {ecarts}'}")
        return 0 if conforme else 1
    except RejetPropre as e:
        print(f"{e}")
        return e.rc


if __name__ == "__main__":
    sys.exit(main())
