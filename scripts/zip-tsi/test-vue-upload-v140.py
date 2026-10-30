#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test mécanique vue-upload v1.4.0 (D015 — plan Task 7 amendé, G0).

Chaîne vérifiée sur un bac à sable jetable (port éphémère, nettoyage intégral) :
  1. featured <fichier>  → marker écrit + lisible (panel --json expose featured)
  2. serveur jetable      → GET /files expose l'épinglé (dossier+taille)
  3. GET /get/<d>/<f>     → 200 + journal JSONL renseigné (1 entrée exacte)
  4. featured --off       → retrait no-op honnête ×2
  5. panel --json         → derniers_telechargements lus depuis le journal
Usage : python3 scripts/zip-tsi/test-vue-upload-v140.py  (rc 0 = PASS)
"""
import importlib.util
import json
import os
import shutil
import socket
import sys
import tempfile
import threading
import time
import urllib.request

PANEL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..",
                     "skills", "vue-upload", "scripts", "vue_upload_panel.py")
SERVER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..",
                      "skills", "vue-upload", "scripts", "vue_upload_server.py")


def port_libre():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


def charge_module(chemin, nom):
    spec = importlib.util.spec_from_file_location(nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def ver_tuple(v):
    return tuple(int(x) for x in v.split("."))


def main():
    echecs = []

    def check(nom, ok, detail=""):
        print("  [%s] %s%s" % ("PASS" if ok else "FAIL", nom, (" — " + str(detail)) if detail else ""))
        if not ok:
            echecs.append(nom)

    bac = tempfile.mkdtemp(prefix="vutest-")
    racine = bac
    try:
        os.makedirs(os.path.join(racine, "download"), exist_ok=True)
        os.makedirs(os.path.join(racine, "upload"), exist_ok=True)
        # 3 fichiers au nom proche — reproduction exacte de la douleur du 2026-10-25
        for nom, taille in (("mouton_rasta_sauts_photo.gif", 100),
                            ("mouton_sauts_photo.gif", 90),
                            ("mouton_rasta_sauts_photo_v3.gif", 120)):
            with open(os.path.join(racine, "download", nom), "wb") as f:
                f.write(b"x" * taille)

        pan = charge_module(PANEL, "panel_v140")
        srv = charge_module(SERVER, "server_v140")

        print("— 1. épinglage (featured) —")
        import argparse
        a = argparse.Namespace(root=racine, json=True, fichier="mouton_rasta_sauts_photo_v3.gif", off=False)
        rc = pan.cmd_featured(a)
        check("featured rc=0", rc == 0, rc)
        marker = os.path.join(racine, pan.MARKER)
        check("marker écrit", os.path.isfile(marker))
        j = json.load(open(marker, encoding="utf-8"))
        check("marker conforme", j.get("fichier") == "mouton_rasta_sauts_photo_v3.gif"
              and j.get("dossier") == "download", j)
        # garde semver (Task 8) : la version AVANCE par design — le comportement v1.4.0
        # est ce qui est vérifié ici, jamais le littéral (bump v1.5.0 = non-régression OK)
        check("VERSION panel >= 1.4.0", ver_tuple(pan.VERSION) >= (1, 4, 0), pan.VERSION)

        print("— 2. serveur jetable : /files expose l'épinglé —")
        port = port_libre()
        Handler = srv.Handler
        Handler.root = os.path.realpath(racine)
        httpd = srv.ThreadingHTTPServer(("127.0.0.1", port), Handler)
        threading.Thread(target=httpd.serve_forever, daemon=True).start()
        time.sleep(0.2)
        base = "http://127.0.0.1:%d" % port
        r = json.loads(urllib.request.urlopen(base + "/files", timeout=5).read().decode("utf-8"))
        check("/files featured présent", r.get("featured", {}).get("fichier") == "mouton_rasta_sauts_photo_v3.gif"
              if r.get("featured") else False, r.get("featured"))
        check("/files featured taille", r.get("featured", {}).get("octets") == 120,
              r.get("featured", {}).get("octets"))
        page = urllib.request.urlopen(base + "/", timeout=5).read().decode("utf-8")
        check("UI porte la bannière ★", "LIVRABLE COURANT" in page and "featbox" in page)

        print("— 3. téléchargement → journal —")
        jnl = os.path.join(racine, srv.JOURNAL)
        check("journal absent avant téléchargement", not os.path.exists(jnl))
        corps = urllib.request.urlopen(base + "/get/download/mouton_rasta_sauts_photo_v3.gif",
                                       timeout=5).read()
        check("corps téléchargé intact", len(corps) == 120, len(corps))
        # l'append serveur est POST-réponse (best-effort) : poller ≤ 2 s (anti-race client/serveur)
        for _ in range(40):
            if os.path.isfile(jnl) and os.path.getsize(jnl) > 0:
                break
            time.sleep(0.05)
        check("journal créé (non vide)", os.path.isfile(jnl) and os.path.getsize(jnl) > 0)
        ent = [json.loads(l) for l in open(jnl, encoding="utf-8") if l.strip()]
        check("journal 1 entrée exacte", len(ent) == 1, ent)
        check("entrée conforme", ent and ent[0].get("fichier") == "mouton_rasta_sauts_photo_v3.gif"
              and ent[0].get("dossier") == "download" and ent[0].get("octets") == 120, ent)

        print("— 4. retrait de l'épingle (no-op honnête ×2) —")
        a_off = argparse.Namespace(root=racine, json=True, fichier=None, off=True)
        rc1 = pan.cmd_featured(a_off)
        rc2 = pan.cmd_featured(a_off)  # 2e retrait : no-op
        check("featured --off rc=0 ×2", rc1 == 0 and rc2 == 0, (rc1, rc2))
        check("marker retiré", not os.path.exists(marker))
        r2 = json.loads(urllib.request.urlopen(base + "/files", timeout=5).read().decode("utf-8"))
        check("/files featured null après retrait", r2.get("featured") is None, r2.get("featured"))

        print("— 5. panel --json expose featured + derniers téléchargements —")
        # re-épinglage puis panel (voie froide sur un AUTRE port pour ne pas toucher :3000)
        a_on = argparse.Namespace(root=racine, json=True, fichier="mouton_sauts_photo.gif", off=False)
        pan.cmd_featured(a_on)
        out = {}
        import io, contextlib
        buf = io.StringIO()
        import argparse as ap
        pa = ap.Namespace(port=port_libre(), root=racine, hold=0, json=True, sort="nom",
                          filter=None, featured=None)
        with contextlib.redirect_stdout(buf):
            pan.cmd_panel(pa)
        out = json.loads(buf.getvalue())
        check("panel expose featured", out.get("featured", {}).get("fichier") == "mouton_sauts_photo.gif",
              out.get("featured"))
        dl = out.get("derniers_telechargements") or []
        check("panel expose derniers_telechargements", len(dl) == 1
              and dl[0].get("fichier") == "mouton_rasta_sauts_photo_v3.gif", dl)
        check("panel VERSION >= 1.4.0", ver_tuple(out.get("version", "0")) >= (1, 4, 0), out.get("version"))

        print("— 6. garde : featured fichier introuvable → rc 6 —")
        a_ko = argparse.Namespace(root=racine, json=True, fichier="inexistant.gif", off=False)
        buf2 = io.StringIO()
        with contextlib.redirect_stdout(buf2):
            rc_ko = pan.cmd_featured(a_ko)
        check("rc=6 sur introuvable", rc_ko == 6, rc_ko)

        httpd.shutdown()
    finally:
        shutil.rmtree(bac, ignore_errors=True)

    print("\n=== TEST vue-upload v1.4.0 : %s ===" % ("PASS" if not echecs else "FAIL — " + ", ".join(echecs)))
    return 0 if not echecs else 1


if __name__ == "__main__":
    sys.exit(main())
