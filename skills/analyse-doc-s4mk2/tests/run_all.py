#!/usr/bin/env python3
"""run_all.py v1.0.0 — Batterie de tests $FACON2 du skill analyse-doc-s4mk2.

$FACON2 = « cohérent, optimisé et fonctionnel » (alias-eco v1.3.0, grammaire B).
La batterie vérifie FONCTIONNELLEMENT chaque capacité du skill sur l'échantillon
de référence réel (ZIP DJTT Kontrol S4 MK2 v2.1.0) et ROBUSTESSEMENT les rejets
propres (entrée non-mapping, blob corrompu, cible absente), l'idempotence ×2 et
le self-test du moteur. Verdict mécanique : PASS ssi tous les tests passent ;
journal JSON individuel par test (tests/journal/) + synthèse (synthese.json).
Le skill ne ment jamais : échantillon introuvable = FAIL explicite.

Usage :
  python3 skills/analyse-doc-s4mk2/tests/run_all.py [--zip CHEMIN_ZIP] [--dir CHEMIN_DOSSIER]
Exit code : 0 ssi BATTERIE PASS ; 1 sinon ; 2 usage.
Stdlib uniquement. Lecture seule (l'échantillon n'est jamais modifié).
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

DEFAUT_ZIP = "/home/z/my-project/upload/DJTT Kontrol S4 MK2 Custom Mapping v2.1.0.zip"
DEFAUT_DIR = "/home/z/my-project/scripts/zip-tsi/extracted/DJTT Kontrol S4 MK2 Custom Mapping v2.1.0"

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
        synth = {"skill": "analyse-doc-s4mk2", "batterie_version": "1.0.0", "grammaire": "$FACON2",
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


def batterie(zip_path, dir_path):
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
    a = ap.parse_args()
    return batterie(a.zip, a.dir_path if a.dir_path and os.path.isdir(a.dir_path) else None)


if __name__ == "__main__":
    sys.exit(main())
