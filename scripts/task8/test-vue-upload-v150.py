#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Test mécanique vue-upload v1.5.0 (D002 — plan Task 8, G1 : hygiène des versions).

Chaîne vérifiée sur un bac à sable jetable (ports éphémères, nettoyage intégral) :
  1. radical_livrable          → purge _vN/final/(N), garde anti-faux positif (années)
  2. detect_versions           → famille exacte « rapport » + suspects nom proche « mouton »
  3. push rapport_v3           → supersédées (v1 + final) ARCHIVÉES vers download/archive/,
                                 listing = 1 seule version, res.archives == 2
  4. push mouton_rasta_…_v3    → V1 archivée (famille exacte), suspect nom proche SIGNALÉ
                                 mais JAMAIS archivé (garde anti-faux positif)
  5. no-op honnête             → re-push identique : aucune action d'hygiène
  6. --no-archive              → push sans archivage (coexistence volontaire conservée)
  7. versions (cmd)            → familles_exactes + versions_archivees exposés
  8. épinglé ★ conservé        → featured NON archivé au push (note explicite)
  9. serveur                   → /files expose versions_archivees ; archive NON téléchargeable
                                 via /get (anti-mauvais-clic) ; UI porte la section repliée
 10. codes retour préservés    → push contenu différent sans --force = rc 5 (R2)
Usage : python3 scripts/task8/test-vue-upload-v150.py  (rc 0 = PASS)
"""
import argparse
import importlib.util
import io
import contextlib
import json
import os
import shutil
import socket
import sys
import tempfile
import threading
import time
import urllib.request
import urllib.error

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


def main():
    echecs = []

    def check(nom, ok, detail=""):
        print("  [%s] %s%s" % ("PASS" if ok else "FAIL", nom, (" — " + str(detail)) if detail else ""))
        if not ok:
            echecs.append(nom)

    bac = tempfile.mkdtemp(prefix="vutest150-")
    racine = bac
    try:
        os.makedirs(os.path.join(racine, "download"), exist_ok=True)
        os.makedirs(os.path.join(racine, "upload"), exist_ok=True)
        os.makedirs(os.path.join(racine, "src"), exist_ok=True)
        # reproduction de la douleur : 2 versions d'un rapport + 2 fichiers au nom proche
        for nom, taille in (("rapport_v1.docx", 100), ("rapport_final.docx", 110),
                            ("mouton_sauts_photo.gif", 90),
                            ("mouton_rasta_sauts_photo.gif", 95)):
            with open(os.path.join(racine, "download", nom), "wb") as f:
                f.write(b"x" * taille)
        # sources des "nouvelles versions" (hors dossiers servis)
        for nom, taille in (("rapport_v3.docx", 120), ("rapport_v4.docx", 130),
                            ("rapport_v5.docx", 140),
                            ("mouton_rasta_sauts_photo_v3.gif", 120)):
            with open(os.path.join(racine, "src", nom), "wb") as f:
                f.write(b"y" * taille)

        pan = charge_module(PANEL, "panel_v150")
        srv = charge_module(SERVER, "server_v150")

        print("— 1. marqueurs v1.5.0 + radical_livrable —")
        check("VERSION panel 1.5.0", pan.VERSION == "1.5.0", pan.VERSION)
        cas = {"rapport_v3.docx": "rapport", "rapport_final.docx": "rapport",
               "Rapport.docx": "rapport", "rapport_v3_final.docx": "rapport",
               "cv_2024.docx": "cv_2024", "rapport-corrige.docx": "rapport-corrige"}
        for brut, attendu in cas.items():
            check("radical %s → %s" % (brut, attendu),
                  pan.radical_livrable(brut) == attendu, pan.radical_livrable(brut))

        print("— 2. détection pré-push (detect_versions) —")
        det = pan.detect_versions(racine)
        fam = [e for e in det["exactes"] if e["radical"] == "rapport" and e["dossier"] == "download"]
        check("famille exacte « rapport » (2 versions)", len(fam) == 1 and len(fam[0]["fichiers"]) == 2, det["exactes"])
        sus = [s for s in det["suspects"] if s["token"] == "mouton" and s["dossier"] == "download"]
        check("suspect nom proche « mouton » (hors famille exacte)",
              len(sus) == 1 and "mouton_sauts_photo.gif" in sus[0]["hors_famille_exacte"], det["suspects"])

        def ns_push(src, nom=None, force=False, no_archive=False):
            return argparse.Namespace(source=os.path.join(racine, "src", src),
                                      as_name=nom, dir="download", force=force,
                                      no_archive=no_archive, root=racine, json=True)

        def capture_rc_ns(fn, ns):
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = fn(ns)
            try:
                res = json.loads(buf.getvalue())
            except Exception:
                res = {}
            return rc, res

        print("— 3. push rapport_v3 : archivage automatique des supersédées —")
        rc, res = capture_rc_ns(pan.cmd_push, ns_push("rapport_v3.docx", "rapport_v3.docx"))
        check("push rc=0", rc == 0, (rc, res))
        check("res.archives == 2 (v1 + final)",
              len(res.get("archives", [])) == 2
              and {a["fichier"] for a in res["archives"]} == {"rapport_v1.docx", "rapport_final.docx"},
              res.get("archives"))
        dl = sorted(os.listdir(os.path.join(racine, "download")))
        check("listing download sans les supersédées",
              "rapport_v3.docx" in dl and "rapport_v1.docx" not in dl
              and "rapport_final.docx" not in dl, dl)
        arc = sorted(os.listdir(os.path.join(racine, "download", "archive")))
        check("download/archive/ contient les 2 supersédées", arc == ["rapport_final.docx", "rapport_v1.docx"], arc)

        print("— 4. push mouton_rasta_sauts_photo_v3 : V1 archivée, suspect signalé —")
        rc, res = capture_rc_ns(pan.cmd_push, ns_push("mouton_rasta_sauts_photo_v3.gif",
                                                      "mouton_rasta_sauts_photo_v3.gif"))
        check("push rc=0", rc == 0, (rc, res))
        check("V1 archivée (famille exacte)",
              len(res.get("archives", [])) == 1 and res["archives"][0]["fichier"] == "mouton_rasta_sauts_photo.gif",
              res.get("archives"))
        check("suspect nom proche signalé (mouton)",
              any(s.get("token") == "mouton" for s in res.get("suspects_nom_proche", [])),
              res.get("suspects_nom_proche"))
        dl = sorted(os.listdir(os.path.join(racine, "download")))
        check("suspect NON archivé (toujours en listing)",
              "mouton_sauts_photo.gif" in dl and "mouton_rasta_sauts_photo_v3.gif" in dl, dl)

        print("— 5. no-op honnête : re-push identique —")
        rc, res = capture_rc_ns(pan.cmd_push, ns_push("mouton_rasta_sauts_photo_v3.gif",
                                                      "mouton_rasta_sauts_photo_v3.gif"))
        check("no-op rc=0", rc == 0 and res.get("no_op") is True, (rc, res.get("no_op")))
        check("no-op = aucune action d'hygiène",
              res.get("archives") == [] and res.get("suspects_nom_proche") == [], res)

        print("— 6. --no-archive : coexistence volontaire —")
        rc, res = capture_rc_ns(pan.cmd_push, ns_push("rapport_v4.docx", "rapport_v4.docx",
                                                      no_archive=True))
        check("push --no-archive rc=0", rc == 0, (rc, res))
        dl = sorted(os.listdir(os.path.join(racine, "download")))
        check("v3 ET v4 coexistent (archivage désactivé)",
              "rapport_v3.docx" in dl and "rapport_v4.docx" in dl, dl)
        check("archive inchangée (3 fichiers)",
              len(os.listdir(os.path.join(racine, "download", "archive"))) == 3)

        print("— 7. versions : familles + archive exposées —")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = pan.cmd_versions(argparse.Namespace(root=racine, json=True))
        vres = json.loads(buf.getvalue())
        check("versions rc=0", rc == 0, rc)
        fam = [e for e in vres["familles_exactes"] if e["radical"] == "rapport"]
        check("famille « rapport » = [v3, v4]", len(fam) == 1 and set(fam[0]["fichiers"]) == {"rapport_v3.docx", "rapport_v4.docx"}, vres["familles_exactes"])
        check("total_archive == 3", vres.get("total_archive") == 3, vres.get("total_archive"))
        check("archive téléchargeable listée par dossier",
              len(vres["versions_archivees"]["download"]) == 3
              and vres["versions_archivees"]["upload"] == [], vres["versions_archivees"])

        print("— 8. épinglé ★ conservé au push —")
        rc, _ = capture_rc_ns(pan.cmd_featured, argparse.Namespace(root=racine, json=True,
                                                                   fichier="rapport_v4.docx", off=False))
        check("featured rapport_v4 posé", rc == 0, rc)
        rc, res = capture_rc_ns(pan.cmd_push, ns_push("rapport_v5.docx", "rapport_v5.docx"))
        check("push v5 rc=0 avec épinglé présent", rc == 0, (rc, res))
        dl = sorted(os.listdir(os.path.join(racine, "download")))
        check("épinglé v4 NON archivé (v3 archivée)",
              "rapport_v4.docx" in dl and len(os.listdir(os.path.join(racine, "download", "archive"))) == 4
              and any("conservé" in n for n in res.get("notes_hygiene", [])), (dl, res.get("notes_hygiene")))

        print("— 9. serveur : /files versions_archivees + archive NON téléchargeable + UI repliée —")
        port = port_libre()
        Handler = srv.Handler
        Handler.root = os.path.realpath(racine)
        httpd = srv.ThreadingHTTPServer(("127.0.0.1", port), Handler)
        threading.Thread(target=httpd.serve_forever, daemon=True).start()
        time.sleep(0.2)
        base = "http://127.0.0.1:%d" % port
        r = json.loads(urllib.request.urlopen(base + "/files", timeout=5).read().decode("utf-8"))
        check("serveur version 1.5.0", Handler.server_version == "vue-upload/1.5.0", Handler.server_version)
        arch_srv = r.get("versions_archivees", {}).get("download", [])
        check("/files expose versions_archivees (4)",
              len(arch_srv) == 4 and {a["name"] for a in arch_srv} >= {"rapport_v1.docx", "rapport_final.docx"},
              arch_srv)
        dl_srv = {f["name"] for f in r.get("download", [])}
        check("listing principal sans les archivées",
              "rapport_v1.docx" not in dl_srv and "rapport_v5.docx" in dl_srv, dl_srv)
        try:
            urllib.request.urlopen(base + "/get/download/archive/rapport_v1.docx", timeout=5)
            code_arch = 200
        except urllib.error.HTTPError as e:
            code_arch = e.code
        check("archive NON téléchargeable via /get (anti-mauvais-clic)", code_arch in (400, 404), code_arch)
        page = urllib.request.urlopen(base + "/", timeout=5).read().decode("utf-8")
        check("UI porte la section repliée « versions archivées »",
              "details" in page and "Versions archivées" in page and "archbox" in page)

        print("— 10. panel --json : versions + versions_archivees exposés —")
        buf = io.StringIO()
        pa = argparse.Namespace(port=port_libre(), root=racine, hold=0, json=True,
                                sort="nom", filter=None, featured=None)
        with contextlib.redirect_stdout(buf):
            pan.cmd_panel(pa)
        pres = json.loads(buf.getvalue())
        check("panel expose versions (compteurs)",
              pres.get("versions", {}).get("familles_exactes", 0) >= 1, pres.get("versions"))
        check("panel expose versions_archivees",
              len(pres.get("versions_archivees", {}).get("download", [])) == 4, pres.get("versions_archivees"))
        check("panel version 1.5.0", pres.get("version") == "1.5.0", pres.get("version"))

        print("— 11. codes retour préservés (R2) : conflit sans --force = rc 5 —")
        with open(os.path.join(racine, "src", "rapport_v5.docx"), "wb") as f:
            f.write(b"z" * 999)
        rc, _ = capture_rc_ns(pan.cmd_push, ns_push("rapport_v5.docx", "rapport_v5.docx"))
        check("push conflit rc=5 (inchangé)", rc == 5, rc)

        httpd.shutdown()
    finally:
        shutil.rmtree(bac, ignore_errors=True)

    print("\n=== TEST vue-upload v1.5.0 : %s ===" % ("PASS" if not echecs else "FAIL — " + ", ".join(echecs)))
    return 0 if not echecs else 1


if __name__ == "__main__":
    sys.exit(main())
