#!/usr/bin/env python3
"""analyser-zip-mk2.py v1.0.0 — Pipeline complet d'analyse d'un ZIP/dossier de mapping S4 MK2
ET de ses documents illustrés liés.

Skill : analyse-doc-s4mk2 (famille TSI, orchestré par agent-TSI).

Pipeline (6 étapes) :
  E1. Inventaire exhaustif (ZIP ou dossier : tous membres, tailles, arborescence
      y compris SOUS-DOSSIERS — l'échantillon DJTT v2.1.0 porte Extra/) ;
  E2. Classification de chaque .tsi : MAPPING (Entry DeviceIO.Config.Controller)
      vs PRÉFÉRENCES-FX (Audio.FX.Selection / Status.4 FX Units) vs
      PRÉFÉRENCES-LAYOUTS (Gui.Layouts2 / Status.Select Layout) vs
      PRÉFÉRENCES-GÉNÉRIQUES vs ILLISIBLE ;
  E3. Analyse du/des mappings via le moteur analyser-tsi-mk2 (comptes +
      conformité référentiel G2 si échantillon de référence reconnu) ;
  E4. Résumé des compagnons de préférences (Entries, clés structurantes) ;
  E5. Documents illustrés (jpg/png : dimensions stdlib, rôle attendu si nom
      reconnu : QuickGuide/vue complète, Manual/manuel+vignettes, Freeze Help) ;
  E6. Vérification mécanique de la table de correspondance visuels↔contrôles
      (references/correspondance-visuels.md) sur les noms DCBM définis ;
      VERDICT final : PASS ssi (a) au moins 1 mapping analysé, (b) conformité
      G2 s'il s'agit de l'échantillon de référence, (c) les noms de contrôles
      de la table P1b existent dans les noms définis, (d) aucun .tsi non classé.

Usage :
  analyser-zip-mk2.py <zip-ou-dossier> [--json OUT.json]
Exit code : 0 ssi VERDICT PASS ; 1 écart/échec ; 2 usage/chemin.
Stdlib uniquement. Lecture seule.
"""
import argparse
import io
import json
import os
import sys
import xml.etree.ElementTree as ET
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyser_tsi_mk2 import RejetPropre, analyser, verifier_g2, ENTRY  # noqa: E402

# Membres attendus de l'échantillon de référence DJTT v2.1.0 (2 dossiers, 6 fichiers)
REFERENCE_DJTT = {
    "dossiers": {"DJTT Kontrol S4 MK2 Custom Mapping v2.1.0/", "DJTT Kontrol S4 MK2 Custom Mapping v2.1.0/Extra/"},
    "fichiers": {
        "DJTT Kontrol S4 MK2 Custom Mapping v2.1.0/DJTT Kontrol S4 MK2 Custom Mapping v2.1.0.tsi": 1810459,
        "DJTT Kontrol S4 MK2 Custom Mapping v2.1.0/QuickGuide v2.1.0.jpg": 3241567,
        "DJTT Kontrol S4 MK2 Custom Mapping v2.1.0/Freeze Mode Help v2.1.0.jpg": 136924,
        "DJTT Kontrol S4 MK2 Custom Mapping v2.1.0/Extra/FX Settings.tsi": 7517,
        "DJTT Kontrol S4 MK2 Custom Mapping v2.1.0/Extra/Layouts.tsi": 5923,
        "DJTT Kontrol S4 MK2 Custom Mapping v2.1.0/Extra/Manual.jpg": 978634,
    },
}

# Table de correspondance visuels ↔ contrôles (references/correspondance-visuels.md)
# nom de contrôle → nb de définitions cid attendues (échantillon de référence)
TABLE_P1B = {
    "Left.FX.Dry/Wet": 16, "Left.FX.Knob 1": 17, "Left.FX.Knob 2": 17, "Left.FX.Knob 3": 17,
    "Left.FX.Button 1": 113, "Left.FX.Button 2": 111, "Left.FX.Button 3": 111,
    "Left.FX.On": 78, "Left.FX.Mode": 71,
    "Right.FX.Dry/Wet": 17, "Right.FX.Knob 1": 17, "Right.FX.Knob 2": 16, "Right.FX.Knob 3": 17,
    "Right.FX.Button 1": 110, "Right.FX.Button 2": 111, "Right.FX.Button 3": 110,
    "Right.FX.On": 80, "Right.FX.Mode": 70,
    "Left.Jog.Encoder": 166, "Right.Jog.Encoder": 161,
    "Left.Jog.Touch": 105, "Right.Jog.Touch": 111,
}

ROLES_ILLUSTRES = {
    "quickguide": "vue complète du contrôleur (référence de correspondance)",
    "manual": "manuel DJTT : fonctionnement + vignettes d'éléments (vues partielles)",
    "freeze": "aide dédiée du mode Freeze (8 slices, Shift+Loop In)",
}


def dims_jpeg(buf):
    """Dimensions JPEG (marqueurs SOF) — stdlib, aucun décodage."""
    if buf[:2] != b"\xff\xd8":
        return None
    i = 2
    while i + 9 < len(buf):
        if buf[i] != 0xFF:
            i += 1
            continue
        marqueur = buf[i + 1]
        if marqueur in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            h, l = int.from_bytes(buf[i + 5:i + 7], "big"), int.from_bytes(buf[i + 7:i + 9], "big")
            return {"hauteur": h, "largeur": l}
        if marqueur in (0xD8, 0x01) or 0xD0 <= marqueur <= 0xD7:
            i += 2
            continue
        taille = int.from_bytes(buf[i + 2:i + 4], "big")
        i += 2 + taille
    return None


def lire_tous_membres(chemin):
    """Rend {chemin_relatif: bytes} pour un ZIP ou un dossier, dossiers inclus."""
    membres = {}
    if os.path.isfile(chemin) and chemin.lower().endswith(".zip"):
        with zipfile.ZipFile(chemin) as z:
            for info in z.infolist():
                if info.filename.endswith("/"):
                    membres[info.filename] = None  # dossier
                else:
                    membres[info.filename] = z.read(info)
        return membres
    if os.path.isdir(chemin):
        for rac, dossiers, fichiers in os.walk(chemin):
            base = os.path.basename(rac) if rac != chemin else os.path.basename(os.path.abspath(chemin))
            for d in dossiers:
                membres[f"{base}/{d}/"] = None
            for f in fichiers:
                rel = f"{base}/{f}" if rac != chemin else f
                with open(os.path.join(rac, f), "rb") as fh:
                    membres[rel] = fh.read()
        return membres
    raise RejetPropre(f"USAGE : ni ZIP ni dossier : {chemin}")


def classifier_tsi(nom, buf):
    """Classifie un TSI : mapping / préférences-FX / préférences-layouts / générique."""
    try:
        racine = ET.parse(io.BytesIO(buf)).getroot()
    except ET.ParseError as e:
        return {"classe": "ILLISIBLE", "detail": f"XML invalide ({e})"}
    entrees = list(racine.iter("Entry"))
    noms = {e.get("Name") for e in entrees}
    if any(n == ENTRY for n in noms):
        return {"classe": "MAPPING", "entries": len(entrees), "deviceio": True}
    cles_fx = {"Audio.FX.Selection", "Status.4 FX Units", "Status.FX Panel Mode"} & noms
    cles_layouts = {"Gui.Layouts2", "Status.Select Layout", "Status.Deck Flavor"} & noms
    if cles_fx:
        return {"classe": "PRÉFÉRENCES-FX", "entries": len(entrees), "cles": sorted(cles_fx)}
    if cles_layouts:
        return {"classe": "PRÉFÉRENCES-LAYOUTS", "entries": len(entrees), "cles": sorted(cles_layouts)}
    return {"classe": "PRÉFÉRENCES-GÉNÉRIQUES", "entries": len(entrees)}


def role_illustre(nom_base):
    bas = nom_base.lower()
    for cle, role in ROLES_ILLUSTRES.items():
        if cle in bas:
            return role
    return "illustré non identifié (rôle à qualifier)"


def analyser_zip(chemin):
    membres = lire_tous_membres(chemin)
    rapports = {"cible": chemin, "inventaire": {}, "tsi": {}, "mappings": [], "illustrés": [], "table_p1b": {}, "alertes": []}
    n_dossiers = 0
    for nom, buf in membres.items():
        if buf is None:
            n_dossiers += 1
            rapports["inventaire"][nom] = "dossier"
            continue
        ext = os.path.splitext(nom)[1].lower()
        base = os.path.basename(nom)
        if ext == ".tsi":
            cls = classifier_tsi(nom, buf)
            rapports["inventaire"][nom] = f"{len(buf)} o — {cls['classe']}"
            rapports["tsi"][nom] = cls
            if cls["classe"] == "MAPPING":
                import tempfile
                tmp_dir = tempfile.mkdtemp(prefix="analyse-doc-s4mk2-")
                tmp = os.path.join(tmp_dir, os.path.basename(nom))
                with open(tmp, "wb") as fh:
                    fh.write(buf)
                try:
                    meta = analyser(tmp)
                finally:
                    os.unlink(tmp)
                    os.rmdir(tmp_dir)
                meta["fichier"] = nom  # normalise : pas de chemin temporaire aléatoire (idempotence)
                ecarts, conforme = verifier_g2(meta)
                meta["conforme_g2"] = conforme
                meta["ecarts_g2"] = ecarts
                rapports["mappings"].append(meta)
        elif ext in (".jpg", ".jpeg", ".png"):
            d = dims_jpeg(buf) if ext != ".png" else {"largeur": int.from_bytes(buf[16:20], "big"), "hauteur": int.from_bytes(buf[20:24], "big")}
            rapports["inventaire"][nom] = f"{len(buf)} o — illustré ({d})"
            rapports["illustrés"].append({"nom": base, "taille": len(buf), "dimensions": d, "role": role_illustre(base)})
        else:
            rapports["inventaire"][nom] = f"{len(buf)} o — autre ({ext or 'sans extension'})"
    rapports["comptes_inventaire"] = {"dossiers": n_dossiers, "fichiers": len(membres) - n_dossiers}
    # E6 : table P1b contre le premier mapping analysé
    if rapports["mappings"]:
        defines = rapports["mappings"][0].get("noms_controles_definis", {})
        for nom, nb_attendu in TABLE_P1B.items():
            nb = defines.get(nom)
            rapports["table_p1b"][nom] = {"attendu_cid": nb_attendu, "observe_cid": nb, "ok": nb == nb_attendu}
    # cohérence de référence
    rapports["reference_djtt_v210"] = {
        "membres_identiques": set(membres) == (set(REFERENCE_DJTT["fichiers"]) | REFERENCE_DJTT["dossiers"]),
        "tailles_identiques": all(membres.get(n) is not None and len(membres[n]) == t for n, t in REFERENCE_DJTT["fichiers"].items()),
    }
    return rapports


def verdict(r):
    """Verdict mécanique PASS/FAIL + motifs."""
    motifs = []
    if not r["mappings"]:
        motifs.append("aucun mapping analysé")
    for m in r["mappings"]:
        if not m["conforme_g2"]:
            motifs.append(f"mapping {os.path.basename(m['fichier'])} non conforme G2 : {m['ecarts_g2']}")
    ko_p1b = [k for k, v in r["table_p1b"].items() if not v["ok"]] if r["table_p1b"] else []
    if ko_p1b:
        motifs.append(f"table P1b en écart : {ko_p1b}")
    non_classes = [n for n, c in r["tsi"].items() if c["classe"] == "ILLISIBLE"]
    if non_classes:
        motifs.append(f"TSI illisibles : {non_classes}")
    if r["reference_djtt_v210"]["membres_identiques"] and not r["illustrés"]:
        motifs.append("échantillon de référence sans documents illustrés")
    r["verdict"] = "PASS" if not motifs else "FAIL"
    r["verdict_motifs"] = motifs
    return r


def main():
    ap = argparse.ArgumentParser(description="Pipeline analyse ZIP/dossier mapping S4 MK2 + documents illustrés")
    ap.add_argument("cible")
    ap.add_argument("--json", help="écrire le rapport JSON complet dans ce fichier")
    try:
        a = ap.parse_args()
        if not os.path.exists(a.cible):
            raise RejetPropre(f"USAGE : cible introuvable : {a.cible}", 2)
        r = verdict(analyser_zip(a.cible))
        print(f"cible           : {r['cible']}")
        print(f"inventaire      : {r['comptes_inventaire']['fichiers']} fichiers, {r['comptes_inventaire']['dossiers']} dossiers")
        for nom, cls in r["tsi"].items():
            print(f"TSI classifié   : {os.path.basename(nom)} → {cls['classe']} ({cls.get('entries', '?')} Entry)")
        for m in r["mappings"]:
            print(f"mapping         : {os.path.basename(m['fichier'])} — device {m['device']} — conforme G2 : {m['conforme_g2']}")
        for ill in r["illustrés"]:
            d = ill["dimensions"] or {}
            print(f"illustré        : {ill['nom']} ({d.get('largeur')}×{d.get('hauteur')}) — {ill['role']}")
        if r["table_p1b"]:
            ok = sum(1 for v in r["table_p1b"].values() if v["ok"])
            print(f"table P1b       : {ok}/{len(r['table_p1b'])} noms de contrôles vérifiés")
        ref = r["reference_djtt_v210"]
        print(f"réf. DJTT v2.1.0: membres identiques : {ref['membres_identiques']} — tailles identiques : {ref['tailles_identiques']}")
        if a.json:
            with open(a.json, "w", encoding="utf-8") as fh:
                json.dump(r, fh, ensure_ascii=False, indent=2)
            print(f"JSON → {a.json}")
        print(f"VERDICT : {r['verdict']}" + (f" — motifs : {r['verdict_motifs']}" if r["verdict_motifs"] else ""))
        return 0 if r["verdict"] == "PASS" else 1
    except RejetPropre as e:
        print(f"{e}")
        return e.rc


if __name__ == "__main__":
    sys.exit(main())
