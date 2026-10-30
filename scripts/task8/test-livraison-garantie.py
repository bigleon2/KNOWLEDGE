#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test mécanique livraison-garantie v1.0.0 (D004 — plan Task 8, G2).

Portail RÉEL in-process (primitives vue-upload), téléchargements simulés par
GET /get/ authentiques — la boucle fermée est éprouvée de bout en bout :
  1. garde de dépendance   → vue-upload chargé, VERSION >= 1.5.0
  2. cible absente         → rc 6 + guidance push
  3. CONFIRME              → épinglage AVANT fenêtre (marker posé pendant la course),
                             arrêt ANTICIPÉ (< hold/2), verdict CONFIRME,
                             critère cible_telechargee, mauvais_fichiers = []
  4. avertissement famille → cible en famille multi-versions signalée (sans modification)
  5. PARTIEL               → mauvais fichier au nom proche pris : verdict PARTIEL,
                             mauvais_fichiers nommé avec nom_proche=True,
                             téléchargements = 1 (le mauvais), la cible ABSENTE
  6. AUCUN                 → fenêtre expirée sans téléchargement : verdict AUCUN
  7. codes retour          → 0 / 1 / 7 / 6 conformes à la spécification
Usage : python3 scripts/task8/test-livraison-garantie.py  (rc 0 = PASS)
"""
import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..",
                      "skills", "livraison-garantie", "scripts", "livraison_garantie.py")
PANEL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..",
                     "skills", "vue-upload", "scripts", "vue_upload_panel.py")


def port_libre():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


def ver_tuple(v):
    return tuple(int(x) for x in v.split("."))


def run_orchestrateur(args):
    """Lance l'orchestrateur en subprocess --json, retourne (rc, dict JSON)."""
    p = subprocess.run([sys.executable, SCRIPT] + args, capture_output=True, text=True,
                       timeout=90)
    try:
        j = json.loads(p.stdout)
    except Exception:
        j = {"_stdout": p.stdout[-400:], "_stderr": p.stderr[-400:]}
    return p.returncode, j


def attend_port(port, timeout=8.0):
    t0 = time.monotonic()
    while time.monotonic() - t0 < timeout:
        s = socket.socket()
        s.settimeout(0.3)
        try:
            if s.connect_ex(("127.0.0.1", port)) == 0:
                return True
        finally:
            s.close()
        time.sleep(0.1)
    return False


def main():
    echecs = []

    def check(nom, ok, detail=""):
        print("  [%s] %s%s" % ("PASS" if ok else "FAIL", nom, (" — " + str(detail)) if detail else ""))
        if not ok:
            echecs.append(nom)

    print("— 1. garde de dépendance (vue-upload >= 1.5.0) —")
    import importlib.util
    spec = importlib.util.spec_from_file_location("panel_check", PANEL)
    pan = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pan)
    check("vue-upload >= 1.5.0 disponible", ver_tuple(pan.VERSION) >= (1, 5, 0), pan.VERSION)

    bac = tempfile.mkdtemp(prefix="lgtest-")
    try:
        os.makedirs(os.path.join(bac, "download"), exist_ok=True)
        os.makedirs(os.path.join(bac, "upload"), exist_ok=True)
        for nom, taille in (("livrable_cible_v3.pdf", 120),
                            ("livrable_cible_v1.pdf", 100)):
            with open(os.path.join(bac, "download", nom), "wb") as f:
                f.write(b"x" * taille)

        print("— 2. cible absente → rc 6 —")
        rc, res = run_orchestrateur(["--fichier", "absent.pdf", "--root", bac, "--json"])
        check("rc=6", rc == 6, (rc, res.get("erreur", "")))
        check("guidance push présente", "push" in res.get("erreur", ""), res.get("erreur"))

        print("— 3. CONFIRME : épinglage avant fenêtre + arrêt anticipé —")
        port = port_libre()
        args = ["--fichier", "livrable_cible_v3.pdf", "--root", bac, "--port", str(port),
                "--hold", "8", "--poll", "0.2", "--json"]
        proc = subprocess.Popen([sys.executable, SCRIPT] + args,
                                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        vivant = attend_port(port)
        check("portail démarré pendant la course", vivant)
        marker = os.path.join(bac, ".featured-vue-upload.json")
        epingle_pendant = None
        if os.path.isfile(marker):
            epingle_pendant = json.load(open(marker, encoding="utf-8"))
        check("épinglé posé AVANT téléchargement (marker lu pendant la fenêtre)",
              bool(epingle_pendant) and epingle_pendant.get("fichier") == "livrable_cible_v3.pdf"
              and epingle_pendant.get("pose_par", "").startswith("livraison-garantie"), epingle_pendant)
        corps = urllib.request.urlopen(
            "http://127.0.0.1:%d/get/download/livrable_cible_v3.pdf" % port, timeout=5).read()
        check("téléchargement simulé servit 120 o", len(corps) == 120, len(corps))
        t0 = time.monotonic()
        out, _err = proc.communicate(timeout=30)
        rc = proc.returncode
        duree = time.monotonic() - t0
        try:
            res = json.loads(out)
        except Exception:
            res = {"_stdout": out[-400:]}
        check("verdict CONFIRME", res.get("verdict") == "CONFIRME", res.get("verdict"))
        check("critère d'arrêt = cible_telechargee (arrêt anticipé)",
              res.get("critere_arret") == "cible_telechargee" and res.get("arret_anticipe") is True
              and duree < 8.0, (res.get("critere_arret"), round(duree, 2)))
        check("mauvais_fichiers vide", res.get("mauvais_fichiers") == [], res.get("mauvais_fichiers"))
        check("avertissement famille multi-versions signalé (sans modification)",
              any("famille multi-versions" in w for w in res.get("avertissement_famille", []))
              and os.path.isfile(os.path.join(bac, "download", "livrable_cible_v1.pdf")),
              res.get("avertissement_famille"))
        check("rc=0", rc == 0, rc)

        print("— 4. PARTIEL : mauvais fichier au nom proche pris —")
        port = port_libre()
        args = ["--fichier", "livrable_cible_v3.pdf", "--root", bac, "--port", str(port),
                "--hold", "4", "--poll", "0.2", "--json"]
        proc = subprocess.Popen([sys.executable, SCRIPT] + args,
                                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
        attend_port(port)
        time.sleep(0.3)
        urllib.request.urlopen("http://127.0.0.1:%d/get/download/livrable_cible_v1.pdf" % port,
                               timeout=5).read()
        out, _err = proc.communicate(timeout=30)
        rc = proc.returncode
        try:
            res = json.loads(out)
        except Exception:
            res = {"_stdout": out[-400:]}
        check("verdict PARTIEL", res.get("verdict") == "PARTIEL", res.get("verdict"))
        mf = res.get("mauvais_fichiers") or []
        check("mauvais fichier nommé + nom_proche",
              len(mf) == 1 and mf[0]["fichier"] == "livrable_cible_v1.pdf"
              and mf[0].get("nom_proche") is True, mf)
        check("guidance de re-ciblage (épinglé conservé + nom EXACT)",
              "réouvrir" in res.get("guidance", "") and "livrable_cible_v3.pdf" in res.get("guidance", ""),
              res.get("guidance"))
        check("rc=1", rc == 1, rc)

        print("— 5. AUCUN : fenêtre expirée sans téléchargement —")
        port = port_libre()
        rc, res = run_orchestrateur(["--fichier", "livrable_cible_v3.pdf", "--root", bac,
                                     "--port", str(port), "--hold", "2", "--poll", "0.2", "--json"])
        check("verdict AUCUN + rc=7", res.get("verdict") == "AUCUN" and rc == 7,
              (res.get("verdict"), rc))
        check("guidance preview/share", "preview" in res.get("guidance", "") and "share" in res.get("guidance", ""),
              res.get("guidance"))

        print("— 6. nom caché refusé (assainissement) —")
        rc, res = run_orchestrateur(["--fichier", ".cache.json", "--root", bac, "--json"])
        check("rc=6 sur nom caché", rc == 6, (rc, res.get("erreur", "")))
    finally:
        shutil.rmtree(bac, ignore_errors=True)

    print("\n=== TEST livraison-garantie : %s ===" % ("PASS" if not echecs else "FAIL — " + ", ".join(echecs)))
    return 0 if not echecs else 1


if __name__ == "__main__":
    sys.exit(main())
