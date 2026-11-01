#!/usr/bin/env python3
"""run_all.py v1.2.0 — Batterie de tests $FACON2 du skill analyse-doc-s4mk2.

$FACON2 = « cohérent, optimisé et fonctionnel » (alias-eco v1.3.0, grammaire B).
La batterie vérifie FONCTIONNELLEMENT chaque capacité du skill sur l'échantillon
de référence réel (ZIP DJTT Kontrol S4 MK2 v2.1.0) et ROBUSTESSEMENT les rejets
propres (entrée non-mapping, blob corrompu, cible absente), l'idempotence ×2 et
le self-test du moteur. v1.1.0 (directive propriétaire, règle d'or écosystème) :
vérifie aussi l'ADAPTATION AUTOMATIQUE aux types — PDF compagnons analysés en
profondeur (échantillon secondaire DREW : 3 PDF + 2 PNG + 1 TSI), aucun fichier
non-TSI muet, rejet propre d'un PDF invalide. v1.2.0 (directive propriétaire,
traces 1a1989725d74c901 + 1a1989862dd46e61) : vérifie la COHÉRENCE CROISÉE
TSI (source de vérité) ↔ non-TSI — TF-09 attestations positives DREW (fx/knob/
button/deck SUPPORTÉES, mods INDETERMINABLES honnêtes) et TF-10 DÉTECTION
d'un écart injecté (PDF fantôme « Hotcue 9 FX 5 Deck H Slice 12 » → 4
HORS_UNIVERS → verdict de section ÉCARTS_DÉTECTÉS + FAIL pipeline).
Verdict mécanique : PASS ssi tous les tests passent ; journal JSON individuel
par test (tests/journal/) + synthèse (synthese.json). Le skill ne ment jamais :
échantillon introuvable = FAIL explicite.

Usage :
  python3 skills/analyse-doc-s4mk2/tests/run_all.py [--zip CHEMIN_ZIP] [--dir CHEMIN_DOSSIER] [--pdf-dir CHEMIN_DREW]
Exit code : 0 ssi BATTERIE PASS ; 1 sinon ; 2 usage.
Stdlib uniquement. Lecture seule (les échantillons ne sont jamais modifiés).
"""
import argparse
import base64
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import xml.etree.ElementTree as ET
import zipfile

ICI = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(ICI)
SCRIPTS = os.path.join(SKILL, "scripts")
JOURNAL = os.path.join(ICI, "journal")

PIPELINE = os.path.join(SCRIPTS, "analyser-zip-mk2.py")
MOTEUR = os.path.join(SCRIPTS, "analyser_tsi_mk2.py")
MODPDF = os.path.join(SCRIPTS, "analyser-pdf-mk2.py")

DEFAUT_ZIP = "/home/z/my-project/upload/DJTT Kontrol S4 MK2 Custom Mapping v2.1.0.zip"
DEFAUT_DIR = "/home/z/my-project/scripts/zip-tsi/extracted/DJTT Kontrol S4 MK2 Custom Mapping v2.1.0"
# Échantillon secondaire DREW (mapping tiers avec PDF compagnons) — v1.1.0
DEFAUT_PDF_DIR = "/home/z/my-project/scripts/zip-tsi/extracted-drew/Kontrol S4  [DREW's MAPPING] - FX4(JogWheel ) + Mode Freeze + Etc"
PDFS_DREW = ("Drew's Assignment List.pdf", "Mapping Speech.pdf", "Mapping Speech-fr.pdf")
TSI_DREW = "Drew's S4 User Controller Maping.tsi"
GHOST_TEXTE = "Hotcue 9 FX 5 Deck H Slice 12 Assignment"

# Attentes mécaniques de l'échantillon de référence (référentiel G2 + erratum Task 33)
ATTENDU = {
    "membres_zip": 8,          # 6 fichiers + 2 dossiers
    "dossiers": 2,
    "tailles": {
        "DJTT Kontrol S4 MK2 Custom Mapping v2.1.0/DJTT Kontrol S4 MK2 Custom Mapping v2.1.0.tsi": 1810459,
        "DJTT Kontrol S4 MK2 Custom Mapping v2.1.0/QuickGuide v2.1.0.jpg": 3241567,
        "DJTT Kontrol S4 MK2 Custom Mapping v2.1.0/Freeze Mode Help v2.1.0.jpg": 136924,
        "DJTT Kontrol S4 MK2 Custom Mapping v2.1.0/Extra/FX Settings.tsi": 7517,
        "DJTT Kontrol S4 MK2 Custom Mapping v2.1.0/Extra/Layouts.tsi": 5923,
        "DJTT Kontrol S4 MK2 Custom Mapping v2.1.0/Extra/Manual.jpg": 978634,
    },
    "classification": {"MAPPING": 1, "PRÉFÉRENCES-FX": 1, "PRÉFÉRENCES-LAYOUTS": 1},
    "entries": {"FX Settings.tsi": 96, "Layouts.tsi": 39},
    "comptes_g2": {"CMAI": 5626, "CMAD_lus": 5626, "DCBM": 5626, "DCDT_in": 125, "DCDT_out": 220,
                   "DCDT_total": 345, "controles_distincts": 163, "commandes_distinctes": 393,
                   "refs_resolues": 5136, "refs_non_resolues": 490},
    "baseline": {"lisibles": 4960, "illisibles": 666, "sollicites": 49},
    "table_p1b": 22,
    "illustres": {"QuickGuide v2.1.0.jpg": (4000, 2500), "Freeze Mode Help v2.1.0.jpg": (858, 892),
                  "Manual.jpg": (2149, 2753)},
}


class Batterie:
    def __init__(self):
        self.resultats = []

    def test(self, tid, nom, fn):
        t0 = time.monotonic()
        try:
            detail = fn()
            ok = True
            if isinstance(detail, tuple):
                ok, detail = detail
        except Exception as e:  # noqa: BLE001 — journalisation contrôlée
            ok, detail = False, f"EXCEPTION : {type(e).__name__}: {e}"
        res = {"id": tid, "nom": nom, "ok": ok, "detail": detail, "duree_ms": int((time.monotonic() - t0) * 1000)}
        self.resultats.append(res)
        print(f"  [{'PASS' if ok else 'FAIL'}] {tid} {nom} — {detail} ({res['duree_ms']} ms)")
        with open(os.path.join(JOURNAL, f"{tid.lower().replace('-', '_')}.json"), "w", encoding="utf-8") as fh:
            json.dump(res, fh, ensure_ascii=False, indent=2)
        return ok

    def synthese(self, echantillon):
        passes = sum(1 for r in self.resultats if r["ok"])
        verdict = "PASS" if passes == len(self.resultats) else "FAIL"
        synth = {"skill": "analyse-doc-s4mk2", "batterie_version": "1.2.0", "grammaire": "$FACON2",
                 "echantillon": echantillon, "total": len(self.resultats), "passes": passes,
                 "fails": len(self.resultats) - passes, "verdict": verdict, "tests": self.resultats}
        with open(os.path.join(JOURNAL, "synthese.json"), "w", encoding="utf-8") as fh:
            json.dump(synth, fh, ensure_ascii=False, indent=2)
        return synth


def lancer(cmd):
    """Lance un sous-processus, rend (rc, stdout, stderr)."""
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    return p.returncode, p.stdout, p.stderr


def extraire_si_besoin(zip_path, dir_path):
    """Rend le dossier extrait : réutilise --dir si présent, sinon extrait le ZIP."""
    if dir_path and os.path.isdir(dir_path):
        return dir_path
    tmp = tempfile.mkdtemp(prefix="analyse-doc-s4mk2-tests-")
    with zipfile.ZipFile(zip_path) as z:
        z.extractall(tmp)
    racine = os.path.join(tmp, os.path.basename(zip_path).removesuffix(".zip"))
    if not os.path.isdir(racine):
        racine = tmp
    return racine


def fabriquer_tsi_corrompu(zip_path, destination):
    """Copie le TSI de référence avec l'attribut Value (base64) tronqué au milieu."""
    with zipfile.ZipFile(zip_path) as z:
        nom = next(n for n in z.namelist() if n.endswith(".tsi"))
        brut = z.read(nom).decode("utf-8")
    racine = ET.fromstring(brut)
    for entry in racine.iter("Entry"):
        if entry.get("Name") == "DeviceIO.Config.Controller":
            val = entry.get("Value")
            moitie = len(val) // 2
            entry.set("Value", val[moitie:moitie + 40000] + val[-4000:])  # base64 valide mais blob corrompu
    with open(destination, "wb") as fh:
        fh.write(b'<?xml version="1.0" encoding="UTF-8" standalone="no" ?>\n' + ET.tostring(racine))
    return destination


def fabriquer_pdf_fantome(destination, texte=GHOST_TEXTE):
    """PDF minimal valide (texte littéral cp1252, 5 objets) pour la détection d'écart."""
    corps = (
        b"1 0 obj\n<</Type/Catalog/Pages 2 0 R>>\nendobj\n"
        b"2 0 obj\n<</Type/Pages/Kids[3 0 R]/Count 1>>\nendobj\n"
        b"3 0 obj\n<</Type/Page/Parent 2 0 R/MediaBox[0 0 612 792]/Contents 4 0 R/"
        b"Resources<</Font<</F1 5 0 R>>>>>>\nendobj\n"
        b"4 0 obj\n<</Length " + str(len(texte) + 42).encode() + b">>\nstream\n"
        b"BT /F1 12 Tf 72 720 Td (" + texte.encode("cp1252") + b") Tj ET\n"
        b"endstream\nendobj\n"
        b"5 0 obj\n<</Type/Font/Subtype/Type1/BaseFont/Helvetica>>\nendobj\n"
        b"trailer\n<</Root 1 0 R/Size 6>>\n%%EOF\n"
    )
    with open(destination, "wb") as fh:
        fh.write(b"%PDF-1.4\n" + corps)
    return destination


def batterie(zip_path, dir_path, pdf_dir=None):
    print(f"BATTERIE $FACON2 — skill analyse-doc-s4mk2")
    print(f"  échantillon ZIP    : {zip_path}")
    b = Batterie()
    if not os.path.isfile(zip_path):
        b.test("TF-00", "échantillon de référence disponible", (False, f"ZIP introuvable : {zip_path}"))
        synth = b.synthese(zip_path)
        print(f"BATTERIE : {synth['verdict']} ({synth['passes']}/{synth['total']})")
        return 1
    dossier = extraire_si_besoin(zip_path, dir_path)
    try:
        # --- TF-01 : inventaire exhaustif du ZIP (y compris sous-dossiers) ---
        def tf01():
            with zipfile.ZipFile(zip_path) as z:
                membres = z.infolist()
            dossiers = [m for m in membres if m.filename.endswith("/")]
            tailles_ok = all(m.file_size == t for n, t in ATTENDU["tailles"].items()
                             for m in membres if m.filename == n)
            ok = len(membres) == ATTENDU["membres_zip"] and len(dossiers) == ATTENDU["dossiers"] and tailles_ok
            return ok, f"{len(membres)} membres ({len(dossiers)} dossiers), tailles conformes : {tailles_ok}"
        b.test("TF-01", "inventaire exhaustif du ZIP (6 fichiers + 2 dossiers, tailles)", tf01)

        # --- un run pipeline sur le ZIP alimente TF-02..TF-06 ---
        rc, out, err = lancer([sys.executable, PIPELINE, zip_path, "--json", "/tmp/adsm-run-zip.json"])
        def tf02():
            r = json.load(open("/tmp/adsm-run-zip.json", encoding="utf-8"))
            classes = {os.path.basename(n): c["classe"] for n, c in r["tsi"].items()}
            attendu_cl = {os.path.basename(n): v for n, v in ATTENDU["classification"].items()}
            # compte par classe
            cnt = {}
            for c in classes.values():
                cnt[c] = cnt.get(c, 0) + 1
            ents = {os.path.basename(n): c["entries"] for n, c in r["tsi"].items()}
            ok = cnt == ATTENDU["classification"] and ents["FX Settings.tsi"] == ATTENDU["entries"]["FX Settings.tsi"] and ents["Layouts.tsi"] == ATTENDU["entries"]["Layouts.tsi"]
            return ok, f"classes {cnt}, Entry {ents}"
        b.test("TF-02", "classification des 3 TSI (mapping / FX 96 / Layouts 39)", tf02)

        def tf03():
            r = json.load(open("/tmp/adsm-run-zip.json", encoding="utf-8"))
            c = r["mappings"][0]["comptes"]
            ok = all(c[k] == v for k, v in ATTENDU["comptes_g2"].items()) and r["mappings"][0]["conforme_g2"]
            return ok, f"comptes {'égaux' if ok else 'en écart'} : G2 {r['mappings'][0]['conforme_g2']}"
        b.test("TF-03", "comptes du mapping conformes au référentiel G2 (10/10)", tf03)

        def tf04():
            r = json.load(open("/tmp/adsm-run-zip.json", encoding="utf-8"))
            m = r["mappings"][0]
            lisibles = m["noms_commandes_lisibles"]
            illisibles = m["comptes"]["CMAD_illisibles"]
            sollicites = len(m["controles_par_sollicitation"])
            ok = (lisibles == ATTENDU["baseline"]["lisibles"] and illisibles == ATTENDU["baseline"]["illisibles"]
                  and sollicites == ATTENDU["baseline"]["sollicites"])
            return ok, f"lisibles {lisibles}, illisibles {illisibles}, sollicités {sollicites}"
        b.test("TF-04", "baseline stricte (4960 lisibles / 666 illisibles / 49 sollicités)", tf04)

        def tf05():
            r = json.load(open("/tmp/adsm-run-zip.json", encoding="utf-8"))
            t = r["table_p1b"]
            ko = [k for k, v in t.items() if not v["ok"]]
            ok = len(t) == ATTENDU["table_p1b"] and not ko
            return ok, f"{sum(1 for v in t.values() if v['ok'])}/{len(t)} vérifiés" + (f" — écart : {ko}" if ko else "")
        b.test("TF-05", "table de correspondance visuels↔contrôles P1b (22 noms, nb cid exacts)", tf05)

        def tf06():
            r = json.load(open("/tmp/adsm-run-zip.json", encoding="utf-8"))
            vus = {i["nom"]: i["dimensions"] for i in r["illustrés"]}
            roles = {i["nom"]: i["role"] for i in r["illustrés"]}
            dims_ok = all(vus.get(n) and vus[n]["largeur"] == w and vus[n]["hauteur"] == h for n, (w, h) in ATTENDU["illustres"].items())
            roles_ok = all("non identifié" not in roles.get(n, "") for n in ATTENDU["illustres"])
            ok = len(vus) == 3 and dims_ok and roles_ok
            return ok, f"{len(vus)} illustrés, dimensions conformes : {dims_ok}, rôles identifiés : {roles_ok}"
        b.test("TF-06", "documents illustrés identifiés (3 JPG, dimensions et rôles)", tf06)

        # --- TF-07 : PDF compagnons analysés (échantillon secondaire DREW, v1.1.0) ---
        def tf07():
            if not pdf_dir or not os.path.isdir(pdf_dir):
                return False, f"échantillon DREW introuvable ({pdf_dir}) — le skill ne ment jamais"
            details = []
            ok_global = True
            for pdf in PDFS_DREW:
                chemin = os.path.join(pdf_dir, pdf)
                if not os.path.isfile(chemin):
                    return False, f"PDF introuvable : {chemin}"
                j = "/tmp/adsm-tf07.json"
                rc, out, err = lancer([sys.executable, MODPDF, chemin, "--json", j])
                r = json.load(open(j, encoding="utf-8"))
                t = r["texte"]
                ok = rc == 0 and t["statut"] == "TEXTE_EXTRAIT" and t["caracteres"] > 1000 and t["mots"] > 500 and r["mots_cles_mapping"]
                ok_global = ok_global and ok
                details.append(f"{pdf}: {t['caracteres']} car/{t['mots']} mots/{len(r['mots_cles_mapping'])} mc"
                               + ("" if ok else " ÉCART"))
            return ok_global, " ; ".join(details)
        b.test("TF-07", "PDF compagnons analysés en profondeur (3 PDF DREW : texte, mots, mots-clés)", tf07)

        # --- TF-08 : adaptation automatique aux types (aucun non-TSI muet, v1.1.0) ---
        def tf08():
            if not pdf_dir or not os.path.isdir(pdf_dir):
                return False, f"échantillon DREW introuvable ({pdf_dir})"
            j = "/tmp/adsm-tf08.json"
            rc, out, err = lancer([sys.executable, PIPELINE, pdf_dir, "--json", j])
            r = json.load(open(j, encoding="utf-8"))
            n_pdf = len(r["pdf"])
            pdf_ok = n_pdf == 3 and not [p for p in r["pdf"] if p.get("rejet")]
            illus_ok = len(r["illustrés"]) == 2 and all(i["dimensions"] for i in r["illustrés"])
            muets = len(r["autres"])
            n_tsi = len(r["tsi"])
            # adaptation = chaque fichier non-TSI classé dans pdf/illustrés/textes/autres
            couverts = n_pdf + len(r["illustrés"]) + len(r["textes"]) + muets
            ok = pdf_ok and illus_ok and muets == 0 and couverts == r["comptes_inventaire"]["fichiers"] - n_tsi
            return ok, f"{n_tsi} TSI, {n_pdf} PDF analysés, {len(r['illustrés'])} illustrés, {muets} muets, couverture {couverts}/{r['comptes_inventaire']['fichiers'] - n_tsi}"
        b.test("TF-08", "adaptation automatique aux types (DREW : 3 PDF + 2 PNG couverts, 0 muet)", tf08)

        # --- TF-09 : cohérence croisée TSI↔non-TSI positive (v1.2.0) ---
        def tf09():
            r = json.load(open("/tmp/adsm-tf08.json", encoding="utf-8"))
            coh = r.get("coherence_non_tsi")
            if not coh:
                return False, "section coherence_non_tsi absente"
            docs = [d for d in coh["documents"] if "attestations" in d]
            verds = [a["verdict"] for d in docs for a in d["attestations"]]
            ok = (coh["verdict"] == "COHÉRENT" and not coh["ecarts"] and len(docs) == 3
                  and "SUPPORTÉE" in verds and "INDETERMINABLE" in verds
                  and coh["source_verite"]["noms_controles"] == 171
                  and coh["illustrés"]["coherence_via_table_p1b"] is False)
            return ok, (f"verdict {coh['verdict']}, {len(docs)} docs attestés, 0 écart, "
                        f"{verds.count('SUPPORTÉE')} supportées / {verds.count('INDETERMINABLE')} indéterminables (honnêteté)")
        b.test("TF-09", "cohérence croisée TSI↔non-TSI (DREW : attestations positives, mods honnêtes, 0 écart)", tf09)

        # --- TF-10 : détection d'un écart injecté (PDF fantôme, v1.2.0) ---
        def tf10():
            if not pdf_dir or not os.path.isdir(pdf_dir):
                return False, f"échantillon DREW introuvable ({pdf_dir})"
            tsi_src = os.path.join(pdf_dir, TSI_DREW)
            if not os.path.isfile(tsi_src):
                return False, f"TSI DREW introuvable : {tsi_src}"
            tmpd = tempfile.mkdtemp(prefix="adsm-tf10-")
            try:
                shutil.copy(tsi_src, os.path.join(tmpd, TSI_DREW))
                fabriquer_pdf_fantome(os.path.join(tmpd, "Mapping Ghost.pdf"))
                j = "/tmp/adsm-tf10.json"
                rc, out, err = lancer([sys.executable, PIPELINE, tmpd, "--json", j])
                r = json.load(open(j, encoding="utf-8"))
                coh = r.get("coherence_non_tsi") or {}
                familles = sorted((e["famille"], str(e["valeur"])) for e in coh.get("ecarts", []))
                ok = (rc == 1 and coh.get("verdict") == "ÉCARTS_DÉTECTÉS"
                      and len(coh.get("ecarts", [])) == 4
                      and familles == [("deck", "H"), ("fx", "5"), ("hotcue", "9"), ("slice", "12")]
                      and any("cohérence croisée" in m for m in r.get("verdict_motifs", []))
                      and "Traceback" not in err)
                return ok, (f"rc={rc}, verdict {coh.get('verdict')}, écarts {familles}, "
                            f"motif pipeline={'cohérence croisée' in str(r.get('verdict_motifs', []))}, traceback={'Traceback' in err}")
            finally:
                shutil.rmtree(tmpd, ignore_errors=True)
        b.test("TF-10", "détection d'écart injecté : PDF fantôme (Hotcue 9/FX 5/Deck H/Slice 12) → 4 HORS_UNIVERS → FAIL", tf10)

        # --- TR-01 : rejet propre d'un TSI de préférences par le moteur ---
        def tr01():
            fx = os.path.join(dossier, "Extra", "FX Settings.tsi")
            rc, out, err = lancer([sys.executable, MOTEUR, fx])
            ok = rc == 1 and "REJET PROPRE" in out and "Traceback" not in err
            return ok, f"rc={rc}, message={'REJET PROPRE' in out}, traceback={'Traceback' in err}"
        b.test("TR-01", "rejet propre : TSI de préférences (rc=1, message, sans traceback)", tr01)

        # --- TR-02 : rejet propre d'un blob corrompu ---
        def tr02():
            tmp = os.path.join(tempfile.mkdtemp(), "corrompu.tsi")
            fabriquer_tsi_corrompu(zip_path, tmp)
            try:
                rc, out, err = lancer([sys.executable, MOTEUR, tmp])
            finally:
                os.unlink(tmp)
            ok = rc in (1,) and "Traceback" not in err and ("ABANDON" in out or "REJET PROPRE" in out)
            return ok, f"rc={rc}, rejet contrôlé : {'ABANDON' in out or 'REJET PROPRE' in out}, traceback : {'Traceback' in err}"
        b.test("TR-02", "robustesse : blob DIOM corrompu → rejet contrôlé, sans crash", tr02)

        # --- TR-03 : idempotence ×2 (pipeline byte-stable) ---
        def tr03():
            j1, j2 = "/tmp/adsm-idem-1.json", "/tmp/adsm-idem-2.json"
            rc1, _, _ = lancer([sys.executable, PIPELINE, dossier, "--json", j1])
            rc2, _, _ = lancer([sys.executable, PIPELINE, dossier, "--json", j2])
            b1, b2 = open(j1, "rb").read(), open(j2, "rb").read()
            ok = rc1 == 0 and rc2 == 0 and b1 == b2
            return ok, f"rc {rc1}/{rc2}, byte-stable : {b1 == b2}"
        b.test("TR-03", "idempotence ×2 : pipeline byte-stable (re-jeu identique)", tr03)

        # --- TR-04 : cible inexistante → rc=2 propre ---
        def tr04():
            rc, out, err = lancer([sys.executable, PIPELINE, "/tmp/n-existe-pas-xyz.zip"])
            ok = rc == 2 and "USAGE" in out and "Traceback" not in err
            return ok, f"rc={rc}, message USAGE : {'USAGE' in out}"
        b.test("TR-04", "robustesse : cible inexistante → rc=2, message propre", tr04)

        # --- TR-05 : self-test du moteur (stabilité + G2) ---
        def tr05():
            tsi = os.path.join(dossier, "DJTT Kontrol S4 MK2 Custom Mapping v2.1.0.tsi")
            rc, out, err = lancer([sys.executable, MOTEUR, tsi, "--self-test"])
            ok = rc == 0 and "SELF-TEST : PASS" in out
            return ok, f"rc={rc}, self-test={'PASS' in out}"
        b.test("TR-05", "self-test moteur : re-jeu ×2 + conformité G2 + baseline", tr05)

        # --- TR-06 : rejet propre d'un PDF invalide (v1.1.0) ---
        def tr06():
            tmpd = tempfile.mkdtemp()
            garbage = os.path.join(tmpd, "pas-un-pdf.pdf")
            with open(garbage, "wb") as fh:
                fh.write(b"\x00\x01\x02garbage\xff\xfe ceci n'est pas un PDF")
            vide = os.path.join(tmpd, "pdf-sans-texte.pdf")
            with open(vide, "wb") as fh:
                fh.write(b"%PDF-1.4\n1 0 obj\n<</Type/Catalog/Pages 2 0 R>>\nendobj\n2 0 obj\n<</Type/Pages/Kids[]/Count 0>>\nendobj\ntrailer<</Root 1 0 R>>\n%%EOF\n")
            try:
                rc1, out1, err1 = lancer([sys.executable, MODPDF, garbage])
                rc2, out2, err2 = lancer([sys.executable, MODPDF, vide, "--json", "/tmp/adsm-tr06.json"])
            finally:
                shutil.rmtree(tmpd, ignore_errors=True)
            r2 = json.load(open("/tmp/adsm-tr06.json", encoding="utf-8"))
            ok = (rc1 == 1 and "REJET PROPRE" in out1 and "Traceback" not in err1
                  and rc2 == 0 and r2["texte"]["statut"] == "AUCUN_TEXTE_EXTRAIT" and "Traceback" not in err2)
            return ok, f"garbage rc={rc1} rejet={'REJET PROPRE' in out1}, vide rc={rc2} statut={r2['texte']['statut']}, tracebacks : {'Traceback' in err1 or 'Traceback' in err2}"
        b.test("TR-06", "robustesse PDF : signature absente → rc=1 ; PDF sans texte → statut honnête", tr06)
    finally:
        if dir_path is None:
            shutil.rmtree(os.path.dirname(dossier) if dossier != dir_path else dossier, ignore_errors=True)
    synth = b.synthese(zip_path)
    print(f"BATTERIE : {synth['verdict']} ({synth['passes']}/{synth['total']})")
    return 0 if synth["verdict"] == "PASS" else 1


def main():
    ap = argparse.ArgumentParser(description="Batterie de tests $FACON2 du skill analyse-doc-s4mk2")
    ap.add_argument("--zip", default=DEFAUT_ZIP, help="ZIP de l'échantillon de référence")
    ap.add_argument("--dir", dest="dir_path", default=DEFAUT_DIR, help="dossier déjà extrait (optimisation)")
    ap.add_argument("--pdf-dir", dest="pdf_dir", default=DEFAUT_PDF_DIR, help="dossier extrait de l'échantillon secondaire DREW")
    a = ap.parse_args()
    return batterie(a.zip, a.dir_path if a.dir_path and os.path.isdir(a.dir_path) else None,
                    a.pdf_dir if a.pdf_dir and os.path.isdir(a.pdf_dir) else None)


if __name__ == "__main__":
    sys.exit(main())
