#!/usr/bin/env python3
"""analyser-zip-mk2.py v1.2.0 — Pipeline complet d'analyse d'un ZIP/dossier de mapping S4 MK2
ET de TOUS ses fichiers liés (non-TSI compris), adaptatif par type, avec cohérence croisée.

Skill : analyse-doc-s4mk2 (famille TSI, orchestré par agent-TSI).

v1.2.0 (directive propriétaire, traces 1a1989725d74c901 + 1a1989862dd46e61) :
COHÉRENCE CROISÉE (étape E7, module coherence-non-tsi-mk2.py) — les données
extraites des non-TSI sont confrontées aux TSI (SOURCES DE VÉRITÉ) : mentions
numérotées (hotcue/fx/deck/slot/slice/mod) vérifiées contre l'univers S4 MK2
et les noms/conditions du TSI (HORS_UNIVERS / NON_CÂBLÉE = écarts forts,
SUPPORTÉE / INDETERMINABLE = honnêteté), couverture lexicale des contrôles,
illustrés via la table P1b. Verdict FAIL si écarts de cohérence forts.

v1.1.0 (directive propriétaire, règle d'or écosystème) : l'analyseur s'ADAPTE
AUTOMATIQUEMENT au type de chaque fichier — routeur ext→analyseur (table
ROUTEUR), et pour tout type inconnu une analyse par signature magique (stdlib).
Aucun fichier non-TSI lié au mapping ne reste « autre » muet : PDF analysés en
profondeur (texte, pages, polices, mots-clés — module analyser-pdf-mk2.py),
images (dimensions + rôle), textes (.txt/.md), inconnus (signature + taille).

Recherche écosystème consignée (règle d'or, CLAUDE.md Règle 3) : registre KB
(KNOWLEDGE-repo/skills/KNOWLEDGE.md), skills plateforme pdf/pdf-llm = chaînes
ReportLab/Playwright/SDK-qwen non embarquables dans un arbitre stdlib, 153
scripts sans extracteur PDF, inter-scripts = communication multi-langages.
Décision : module stdlib propre (analyser-pdf-mk2.py), sémantique alignée sur
le skill pdf plateforme, consommable inter-scripts par canal one-shot JSON.

Pipeline :
  E1. Inventaire exhaustif (ZIP ou dossier : tous membres, tailles, arborescence
      y compris SOUS-DOSSIERS — l'échantillon DJTT v2.1.0 porte Extra/) ;
  E2. Classification de chaque .tsi : MAPPING (Entry DeviceIO.Config.Controller)
      vs PRÉFÉRENCES-FX (Audio.FX.Selection / Status.4 FX Units) vs
      PRÉFÉRENCES-LAYOUTS (Gui.Layouts2 / Status.Select Layout) vs
      PRÉFÉRENCES-GÉNÉRIQUES vs ILLISIBLE ;
  E3. Analyse du/des mappings via le moteur analyser-tsi-mk2 (comptes +
      conformité référentiel G2 si échantillon de référence reconnu) ;
  E4. Résumé des compagnons de préférences (Entries, clés structurantes) ;
  E5. Fichiers liés NON-TSI, adaptatif : PDF (analyser-pdf-mk2 : texte, pages,
      polices, mots-clés mapping), illustrés jpg/png (dimensions + rôle),
      textes txt/md, types inconnus (signature magique stdlib) ;
  E6. Vérification mécanique de la table de correspondance visuels↔contrôles
      (references/correspondance-visuels.md) sur les noms DCBM définis ;
  E7. COHÉRENCE CROISÉE TSI (source de vérité) ↔ non-TSI : mentions numérotées
      des documents vérifiées contre l'univers S4 MK2 et les noms/conditions du
      mapping, couverture lexicale, illustrés via table P1b (v1.2.0) ;
      VERDICT final : PASS ssi (a) au moins 1 mapping analysé, (b) conformité
      G2 s'il s'agit de l'échantillon de référence, (c) les noms de contrôles
      de la table P1b existent dans les noms définis, (d) aucun .tsi non classé,
      (e) aucun PDF rejeté (illisible), (f) aucun écart de cohérence fort
      (HORS_UNIVERS / NON_CÂBLÉE) dans les documents non-TSI.

Usage :
  analyser-zip-mk2.py <zip-ou-dossier> [--json OUT.json]
Exit code : 0 ssi VERDICT PASS ; 1 écart/échec ; 2 usage/chemin.
Stdlib uniquement. Lecture seule. Sortie déterministe (membres triés).
"""
import argparse
import importlib.util
import io
import json
import os
import sys
import xml.etree.ElementTree as ET
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyser_tsi_mk2 import RejetPropre, analyser, verifier_g2, ENTRY  # noqa: E402

# module PDF (nom à tirets → import par chemin, stdlib)
_spec = importlib.util.spec_from_file_location(
    "analyser-pdf-mk2", os.path.join(os.path.dirname(os.path.abspath(__file__)), "analyser-pdf-mk2.py")
)
_pdf = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_pdf)
analyser_pdf = _pdf.analyser_pdf
RejetProprePDF = _pdf.RejetPropre

# module COHÉRENCE croisée TSI↔non-TSI (étape E7, v1.2.0)
_spec_c = importlib.util.spec_from_file_location(
    "coherence-non-tsi-mk2", os.path.join(os.path.dirname(os.path.abspath(__file__)), "coherence-non-tsi-mk2.py")
)
_coherence = importlib.util.module_from_spec(_spec_c)
_spec_c.loader.exec_module(_coherence)
coherence_croisee = _coherence.coherence

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
    "description": "description du mapping (illustré compagnon)",
}

ROLES_PDF = (
    ("assignment", "liste d'assignations contrôles→fonctions (compagnon du mapping)"),
    ("speech", "description du fonctionnement du mapping (script narratif)"),
)

SIGNATURES = (
    (b"%PDF", "PDF"),
    (b"PK\x03\x04", "archive ZIP (Office/ODF/jar)"),
    (b"\x89PNG", "PNG"),
    (b"\xff\xd8\xff", "JPEG"),
    (b"GIF8", "GIF"),
    (b"BM", "BMP"),
    (b"ID3", "MP3 (tag ID3)"),
    (b"RIFF", "conteneur RIFF (WAV/AVI)"),
    (b"OggS", "OGG"),
    (b"fLaC", "FLAC"),
    (b"MZ", "exécutable Windows"),
    (b"\x7fELF", "exécutable ELF"),
    (b"\x1f\x8b", "gzip"),
    (b"7z\xbc\xaf\x27\x1c", "7-Zip"),
    (b"Rar!", "RAR"),
    (b"ftyp", "conteneur ISO-BMFF (MP4/MOV)"),
    (b"<?xml", "XML"),
    (b"{\\rtf", "RTF"),
    (b"SQLite", "base SQLite"),
)


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


def dims_png(buf):
    """Dimensions PNG (IHDR) — stdlib, avec validation de signature."""
    if buf[:8] != b"\x89PNG\r\n\x1a\n" or buf[12:16] != b"IHDR":
        return None
    return {"largeur": int.from_bytes(buf[16:20], "big"), "hauteur": int.from_bytes(buf[20:24], "big")}


def signature(buf):
    """Signature magique d'un flux inconnu — stdlib, jamais muet."""
    for magie, nom in SIGNATURES:
        if buf.startswith(magie) or (magie == b"ftyp" and buf[4:8] == b"ftyp"):
            return nom
    return "inconnue"


def lire_tous_membres(chemin):
    """Rend {chemin_relatif: bytes} pour un ZIP ou un dossier, dossiers inclus (triés)."""
    membres = {}
    if os.path.isfile(chemin) and chemin.lower().endswith(".zip"):
        with zipfile.ZipFile(chemin) as z:
            for info in z.infolist():
                if info.filename.endswith("/"):
                    membres[info.filename] = None  # dossier
                else:
                    membres[info.filename] = z.read(info)
        return dict(sorted(membres.items()))
    if os.path.isdir(chemin):
        for rac, dossiers, fichiers in os.walk(chemin):
            base = os.path.basename(rac) if rac != chemin else os.path.basename(os.path.abspath(chemin))
            for d in dossiers:
                membres[f"{base}/{d}/"] = None
            for f in fichiers:
                rel = f"{base}/{f}" if rac != chemin else f
                with open(os.path.join(rac, f), "rb") as fh:
                    membres[rel] = fh.read()
        return dict(sorted(membres.items()))
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


def role_pdf(nom_base):
    bas = nom_base.lower()
    role = "document PDF compagnon du mapping"
    for cle, r in ROLES_PDF:
        if cle in bas:
            role = r
            break
    if bas.endswith("-fr.pdf") or ".fr." in bas:
        role += " — traduction française"
    return role


def analyser_tsi_membre(nom, buf, rapports):
    """E2+E3 : classification puis analyse moteur du mapping."""
    cls = classifier_tsi(nom, buf)
    rapports["inventaire"][nom] = f"{len(buf)} o — {cls['classe']}"
    rapports["tsi"][nom] = cls
    if cls["classe"] != "MAPPING":
        return
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


def analyser_pdf_membre(nom, buf, rapports):
    """E5 : PDF lié analysé en profondeur (texte COMPLET pour l'étape E7)."""
    base = os.path.basename(nom)
    try:
        r = analyser_pdf(buf, base, max_cars=100000)
    except RejetProprePDF as e:
        rapports["inventaire"][nom] = f"{len(buf)} o — PDF ILLISIBLE ({e})"
        rapports["pdf"].append({"fichier": base, "taille": len(buf), "rejet": str(e)})
        return
    r["role"] = role_pdf(base)
    r["texte_complet"] = r["texte"]["echantillon"]
    statut = r["texte"]["statut"]
    rapports["inventaire"][nom] = f"{len(buf)} o — PDF ({r['pages']} p., texte : {r['texte']['caracteres']} car) — {r['role']}"
    rapports["pdf"].append(r)


def analyser_image_membre(nom, buf, ext, rapports):
    """E5 : illustré jpg/png (dimensions stdlib + rôle)."""
    base = os.path.basename(nom)
    d = dims_png(buf) if ext == ".png" else dims_jpeg(buf)
    rapports["inventaire"][nom] = f"{len(buf)} o — illustré ({d})"
    rapports["illustrés"].append({"nom": base, "taille": len(buf), "dimensions": d, "role": role_illustre(base)})


def analyser_texte_membre(nom, buf, rapports):
    """E5 : texte lié (.txt/.md) — décodage utf-8 puis cp1252."""
    base = os.path.basename(nom)
    try:
        texte = buf.decode("utf-8")
        enc = "utf-8"
    except UnicodeDecodeError:
        texte = buf.decode("cp1252", errors="replace")
        enc = "cp1252"
    mots = [w for w in texte.split() if w]
    rapports["inventaire"][nom] = f"{len(buf)} o — texte ({len(texte)} car, {enc})"
    rapports["textes"].append({
        "nom": base, "taille": len(buf), "encodage": enc,
        "caracteres": len(texte), "mots": len(mots), "echantillon": texte[:300],
        "texte_complet": texte,
    })


def analyser_autre_membre(nom, buf, ext, rapports):
    """E5 : type inconnu → analyse par signature magique (jamais muet)."""
    base = os.path.basename(nom)
    sig = signature(buf)
    rapports["inventaire"][nom] = f"{len(buf)} o — autre ({ext or 'sans extension'}) — signature : {sig}"
    rapports["autres"].append({
        "nom": base, "taille": len(buf), "extension": ext or None, "signature": sig,
        "premiers_octets": buf[:16].hex(),
        "statut": "analysé sommairement (type hors périmètre TSI/illustré/texte/PDF)",
    })


# Routeur adaptatif ext → analyseur (extension de la table = nouvelle capacité)
def _route_tsi(nom, buf, rapports):
    analyser_tsi_membre(nom, buf, rapports)


def _route_pdf(nom, buf, rapports):
    analyser_pdf_membre(nom, buf, rapports)


def _route_image(nom, buf, rapports):
    analyser_image_membre(nom, buf, os.path.splitext(nom)[1].lower(), rapports)


def _route_texte(nom, buf, rapports):
    analyser_texte_membre(nom, buf, rapports)


ROUTEUR = {
    ".tsi": _route_tsi,
    ".pdf": _route_pdf,
    ".jpg": _route_image,
    ".jpeg": _route_image,
    ".png": _route_image,
    ".txt": _route_texte,
    ".md": _route_texte,
}


def analyser_zip(chemin):
    membres = lire_tous_membres(chemin)
    rapports = {
        "cible": chemin, "inventaire": {}, "tsi": {}, "mappings": [], "illustrés": [],
        "pdf": [], "textes": [], "autres": [], "table_p1b": {}, "alertes": [],
    }
    n_dossiers = 0
    for nom, buf in membres.items():
        if buf is None:
            n_dossiers += 1
            rapports["inventaire"][nom] = "dossier"
            continue
        ext = os.path.splitext(nom)[1].lower()
        route = ROUTEUR.get(ext)
        if route:
            route(nom, buf, rapports)
        else:
            analyser_autre_membre(nom, buf, ext, rapports)
    rapports["comptes_inventaire"] = {"dossiers": n_dossiers, "fichiers": len(membres) - n_dossiers}
    # E6 : table P1b contre le premier mapping analysé
    if rapports["mappings"]:
        defines = rapports["mappings"][0].get("noms_controles_definis", {})
        for nomc, nb_attendu in TABLE_P1B.items():
            nb = defines.get(nomc)
            rapports["table_p1b"][nomc] = {"attendu_cid": nb_attendu, "observe_cid": nb, "ok": nb == nb_attendu}
        # E7 : cohérence croisée TSI (source de vérité) ↔ non-TSI (v1.2.0)
        p1b_ok = bool(rapports["table_p1b"]) and all(v["ok"] for v in rapports["table_p1b"].values())
        rapports["coherence_non_tsi"] = coherence_croisee(
            rapports["mappings"][0], rapports["pdf"], rapports["textes"],
            len(rapports["illustrés"]), p1b_ok)
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
    pdf_ko = [p["fichier"] for p in r["pdf"] if p.get("rejet")]
    if pdf_ko:
        motifs.append(f"PDF illisibles (rejet) : {pdf_ko}")
    coh = r.get("coherence_non_tsi") or {}
    if coh.get("ecarts"):
        motifs.append(f"cohérence croisée TSI↔non-TSI : {len(coh['ecarts'])} écarts forts {coh['ecarts'][:6]}")
    if r["reference_djtt_v210"]["membres_identiques"] and not r["illustrés"]:
        motifs.append("échantillon de référence sans documents illustrés")
    r["verdict"] = "PASS" if not motifs else "FAIL"
    r["verdict_motifs"] = motifs
    return r


def main():
    ap = argparse.ArgumentParser(description="Pipeline analyse ZIP/dossier mapping S4 MK2 + fichiers liés (adaptatif)")
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
        for p in r["pdf"]:
            if p.get("rejet"):
                print(f"PDF             : {p['fichier']} — REJET : {p['rejet']}")
            else:
                t = p["texte"]
                print(f"PDF             : {p['fichier']} ({p['pages']} p.) — {t['statut']} {t['caracteres']} car / {t['mots']} mots — {p['role']}")
        for ill in r["illustrés"]:
            d = ill["dimensions"] or {}
            print(f"illustré        : {ill['nom']} ({d.get('largeur')}×{d.get('hauteur')}) — {ill['role']}")
        for t in r["textes"]:
            print(f"texte           : {t['nom']} — {t['caracteres']} car ({t['encodage']})")
        for au in r["autres"]:
            print(f"autre           : {au['nom']} — signature : {au['signature']}")
        if r["table_p1b"]:
            ok = sum(1 for v in r["table_p1b"].values() if v["ok"])
            print(f"table P1b       : {ok}/{len(r['table_p1b'])} noms de contrôles vérifiés")
        coh = r.get("coherence_non_tsi")
        if coh:
            print(f"cohérence       : {coh['verdict']} — {len([d for d in coh['documents'] if 'attestations' in d])} documents attestés, {len(coh['ecarts'])} écarts, source : {coh['source_verite']['fichier']}")
        ref = r["reference_djtt_v210"]
        print(f"réf. DJTT v2.1.0: membres identiques : {ref['membres_identiques']} — tailles identiques : {ref['tailles_identiques']}")
        if a.json:
            with open(a.json, "w", encoding="utf-8") as fh:
                json.dump(r, fh, ensure_ascii=False, indent=2)
            print(f"JSON → {a.json}")
        print(f"VERDICT : {r['verdict']}" + (f" — motifs : {r['verdict_motifs']}" if r["verdict_motifs"] else ""))
        return 0 if r["verdict"] == "PASS" else 1
    except RejetPropre as e:
        print(e)
        return e.rc


if __name__ == "__main__":
    sys.exit(main())
