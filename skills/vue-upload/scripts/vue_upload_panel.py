#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""vue-upload v1.4.0 — PANEL RAPIDE + BOÎTE À OUTILS d'accès aux livrables.

v1.1.0 (Task 36) : voie CHAUDE < 1 s (portail déjà vivant, zéro démarrage),
voie FROIDE in-process < 2 s (thread daemon, import du Handler — zéro subprocess,
zéro setsid), --hold N (session d'accès deux temps, edge :81 → :3000), --json.

v1.2.0 (Task 39 — approfondissement) : ce qui était MANUEL devient une commande :
  share <fichier>  → repli externe AUTOMATISÉ : filebin.net (rétention ≈ 6 jours)
                     + tmpfiles.org (≈ 60 min), VÉRIFICATION sha256 intégrée
                     (re-téléchargement + comparaison) — un lien n'est annoncé
                     VÉRIFIÉ qu'après preuve d'intégrité ; rc 4 si aucun lien vérifié.
  push <source>    → inscription d'un fichier dans download/ (ou upload/) avec les
                     MÊMES règles que le serveur (assainissement des noms, cachés
                     refusés, 200 Mo max) ; no-op honnête si contenu identique ;
                     --force requis pour écraser un contenu différent (rc 5 sinon).
  doctor           → diagnostic < 1 s (racine, dossiers, port, edge :81, disque)
                     + VOIE RECOMMANDÉE — répond à « pourquoi ça ne fonctionne pas ».

v1.4.0 (2026-10-30, directive propriétaire — discussion partagée du 2026-10-25) :
  featured <fichier> → épingle le LIVRABLE COURANT (marker .featured-vue-upload.json)
                       lu par le serveur à chaque requête : bannière ★ + entrée en
                       tête du portail — le propriétaire voit immédiatement quel
                       fichier télécharger, même parmi des dénominations proches.
                       Douleur constatée le 2026-10-25 : 2 mauvais fichiers pris
                       sur 3 au nom proche. --off retire l'épingle (no-op honnête) ;
                       sans argument = affichage de l'épinglé courant.
  --featured <fichier> (drapeau panel) : épinglage + fenêtre d'accès en un appel.
  Journal des téléchargements (.journal-vue-upload.jsonl, tenu par le serveur sur
  chaque /get/ réussi) — le panel expose `featured` + `derniers_telechargements` :
  vérification après la fenêtre d'accès que le bon fichier a été téléchargé.

Recherche z.ai (D036-06, Task 36) : AUCUNE commande/fonction plateforme pour un
panneau de livrables (API storage = jeton absent) — mécanisme réel = preview
edge :81 → :3000. share/push/doctor = voies fiables indépendantes du preview.

Codes retour : 0 OK · 2 bind impossible · 3 portail mort · 4 share/push sans
vérification possible · 5 push destination existante (sans --force) · 6 source ou
nom invalide (y compris featured : fichier introuvable). Options globales (--json,
--port, --root, --sort, --filter, --featured) peuvent précéder OU suivre la
sous-commande.
"""
import argparse, hashlib, http.server, importlib.util, json, os, re, secrets, shutil, socket, sys, threading, time
import urllib.parse, urllib.request

SERVER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vue_upload_server.py")
VERSION = "1.4.0"
MAX_TAILLE = 200 * 1024 * 1024  # même garde que le serveur
UA = {"User-Agent": "vue-upload/%s" % VERSION}
MARKER = ".featured-vue-upload.json"   # marker d'épinglage (racine — lu par le serveur)
JOURNAL = ".journal-vue-upload.jsonl"  # journal des téléchargements (tenu par le serveur)


# ────────────────────────── noyau panel (v1.1.0) ──────────────────────────

def port_alive(port, timeout=0.3):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        return s.connect_ex(("127.0.0.1", port)) == 0
    finally:
        s.close()


def edge_alive(timeout=0.4):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        return s.connect_ex(("127.0.0.1", 81)) == 0
    finally:
        s.close()


def start_inprocess(port, root):
    spec = importlib.util.spec_from_file_location("vue_upload_server", SERVER_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    Handler = mod.Handler
    Handler.root = os.path.realpath(root)
    for d in mod.DIRS:
        os.makedirs(os.path.join(Handler.root, d), exist_ok=True)

    class DualStack(http.server.ThreadingHTTPServer):
        address_family = socket.AF_INET6
        daemon_threads = True

        def server_bind(self):
            try:
                self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
            except OSError:
                pass
            super().server_bind()

    try:
        srv = DualStack(("::", port), Handler)
        mode_bind = "dual-stack [::]"
    except OSError:
        http.server.ThreadingHTTPServer.address_family = socket.AF_INET
        srv = http.server.ThreadingHTTPServer(("0.0.0.0", port), Handler)
        mode_bind = "IPv4 0.0.0.0"
    threading.Thread(target=srv.serve_forever, kwargs={"poll_interval": 0.05},
                     daemon=True).start()
    return srv, mode_bind


def listing(root, filtre=None, tri="nom"):
    out = {}
    for d in ("download", "upload"):
        p = os.path.join(root, d)
        files = []
        if os.path.isdir(p):
            for f in sorted(os.listdir(p)):
                fp = os.path.join(p, f)
                if os.path.isfile(fp):
                    st = os.stat(fp)
                    files.append({
                        "fichier": f,
                        "octets": st.st_size,
                        "mtime": time.strftime("%Y-%m-%d %H:%M", time.localtime(st.st_mtime)),
                    })
        if filtre:
            q = filtre.lower()
            files = [x for x in files if q in x["fichier"].lower()]
        cle = {
            "nom": lambda x: x["fichier"].lower(),
            "taille": lambda x: x["octets"],
            "date": lambda x: x["mtime"],
        }.get(tri, lambda x: x["fichier"].lower())
        files.sort(key=cle, reverse=(tri in ("taille", "date")))
        out[d] = files
    return out


def cmd_panel(a):
    # épinglage préalable si --featured (un seul appel : épingler + fenêtre d'accès)
    if getattr(a, "featured", None):
        nom = sanitize_name(a.featured)
        dossier = None
        for d in ("download", "upload"):
            if nom and os.path.isfile(os.path.join(a.root, d, nom)):
                dossier = d
                break
        if dossier is None:
            return _fin(a.json, "panel", "--featured : fichier introuvable dans download/ ni upload/ : %s" % a.featured, 6)
        with open(os.path.join(a.root, MARKER), "w", encoding="utf-8") as f:
            json.dump({"fichier": nom, "dossier": dossier,
                       "horodatage": time.strftime("%Y-%m-%dT%H:%M:%S%z")}, f, ensure_ascii=False, indent=1)
    t0 = time.perf_counter()
    voie = "CHAUDE (portail déjà vivant)" if port_alive(a.port, 0.15) else "FROIDE (démarrage in-process)"
    bind_mode = "préexistant"
    if voie.startswith("FROIDE"):
        try:
            _, bind_mode = start_inprocess(a.port, a.root)
        except OSError as e:
            print(json.dumps({"erreur": "bind impossible :%d — %s" % (a.port, e)}, ensure_ascii=False))
            return 2
        for _ in range(30):  # attente vivant max ~1,5 s
            if port_alive(a.port, 0.1):
                break
            time.sleep(0.05)
    duree = time.perf_counter() - t0
    vivant = port_alive(a.port, 0.3)
    fl = listing(a.root, a.filter, a.sort)
    feat = lit_featured(a.root)
    panel = {
        "skill": "vue-upload",
        "version": VERSION,
        "voie": voie,
        "bind": bind_mode,
        "portail_vivant": vivant,
        "duree_s": round(duree, 3),
        "url_locale": "http://127.0.0.1:%d/" % a.port,
        "routage_preview": ("edge :81 vivant → proxifie vers :%d (KB Task 34 — cliquer le bouton "
                            "preview de la session pendant --hold)" % a.port) if edge_alive()
                           else "edge :81 absent — voie locale seulement",
        "filtre": a.filter,
        "tri": a.sort,
        "featured": feat,
        "derniers_telechargements": lit_journal(a.root, 5),
        "download": fl["download"],
        "upload": fl["upload"],
        "limites": ("processus éphémère (sandbox fauche les démons entre les appels) — session "
                    "d'accès = --hold ≤ 540 s pendant le clic preview ; repli = share (liens "
                    "externes vérifiés) ; livrable ciblé = featured/--featured (★ en tête du portail)"),
    }
    if a.hold > 0:
        panel["hold_s"] = a.hold
        if a.json:
            print(json.dumps(panel, ensure_ascii=False, indent=2), flush=True)
        else:
            print_panel(panel)
        time.sleep(a.hold)
        # après la fenêtre : les téléchargements survenus sont dans le journal
        panel["derniers_telechargements"] = lit_journal(a.root, 5)
        if a.json:
            print(json.dumps({"commande": "panel", "apres_fenetre": True,
                              "derniers_telechargements": panel["derniers_telechargements"]},
                             ensure_ascii=False, indent=2))
        else:
            print("[panel] après la fenêtre — derniers téléchargements : %s"
                  % (json.dumps(panel["derniers_telechargements"], ensure_ascii=False) or "aucun"))
        return 0
    if a.json:
        print(json.dumps(panel, ensure_ascii=False, indent=2))
    else:
        print_panel(panel)
    return 0 if vivant else 3


def print_panel(p):
    print("╔═ vue-upload v%s — PANEL LIVRABLES ═ voie %s" % (p["version"], p["voie"]))
    print("║ durée totale : %s s · bind %s · portail vivant : %s" % (p["duree_s"], p["bind"], p["portail_vivant"]))
    print("║ URL locale   : %s" % p["url_locale"])
    print("║ preview      : %s" % p["routage_preview"])
    feat = p.get("featured")
    if feat:
        print("║ ★ LIVRABLE COURANT (épinglé) : %s/%s — c'est CE fichier que le propriétaire doit cliquer"
              % (feat["dossier"], feat["fichier"]))
    else:
        print("║ ★ aucun livrable épinglé (featured <fichier> pour cibler une livraison)")
    for d in ("download", "upload"):
        print("╠═ %s/ (%d fichier(s)%s)" % (d, len(p[d]),
              ", filtre « %s »" % p["filtre"] if p.get("filtre") else ""))
        feat_nom = feat["fichier"] if feat and feat["dossier"] == d else None
        lignes = list(p[d][:40])
        if feat_nom:
            # l'épinglé passe en tête de l'affichage, marqueur ★ (le serveur fait de même côté UI)
            lignes.sort(key=lambda x: (x["fichier"] != feat_nom,))
        for f in lignes:
            marque = "★ " if f["fichier"] == feat_nom else "  "
            print("║ %s· %s — %s — modifié %s" % (marque, f["fichier"], human(f["octets"]), f["mtime"]))
        if len(p[d]) > 40:
            print("║   … +%d fichier(s) non affiché(s)" % (len(p[d]) - 40))
    dl = p.get("derniers_telechargements") or []
    print("╠═ derniers téléchargements (journal) : %s" % ("aucun" if not dl else ""))
    for e in dl:
        print("║   · %s — %s/%s — %s" % (e.get("instant", "?"), e.get("dossier", "?"),
                                        e.get("fichier", "?"), human(e.get("octets", 0))))
    print("║ note : %s" % p["limites"])
    print("╚═" + "═" * 60)


# ────────────────────────── featured (épinglage livrable courant, v1.4.0) ──────────────────────────

def lit_featured(root):
    """Lit le marker d'épinglage (None si absent/corrompu — dégradation honnête)."""
    p = os.path.join(root, MARKER)
    try:
        with open(p, encoding="utf-8") as f:
            j = json.load(f)
        if isinstance(j, dict) and j.get("fichier") and j.get("dossier") in ("download", "upload"):
            return j
    except Exception:
        pass
    return None


def lit_journal(root, n=5):
    """Lit les n dernières entrées du journal des téléchargements (best-effort)."""
    p = os.path.join(root, JOURNAL)
    try:
        with open(p, encoding="utf-8") as f:
            lignes = [l.strip() for l in f if l.strip()]
        out = []
        for l in reversed(lignes[-200:]):  # borne de lecture : 200 dernières lignes
            try:
                out.append(json.loads(l))
            except Exception:
                continue
            if len(out) >= n:
                break
        return out
    except Exception:
        return []


def cmd_featured(a):
    t0 = time.perf_counter()
    root = os.path.realpath(a.root)
    marker_path = os.path.join(root, MARKER)
    if a.off:
        # retrait de l'épingle — no-op honnête si absente
        present = os.path.exists(marker_path)
        if present:
            os.remove(marker_path)
        res = {"commande": "featured", "skill": "vue-upload", "version": VERSION,
               "action": "retire", "retire": present, "featured": None,
               "duree_s": round(time.perf_counter() - t0, 3),
               "note": "épingle retirée" if present else "aucune épingle présente (no-op honnête)"}
        print(json.dumps(res, ensure_ascii=False, indent=2) if a.json else
              "[featured] %s" % res["note"])
        return 0
    if not a.fichier:
        # affichage de l'épinglé courant
        j = lit_featured(root)
        if j and os.path.isfile(os.path.join(root, j["dossier"], j["fichier"])):
            msg = "épinglé actuel : %s/%s (posé %s)" % (j["dossier"], j["fichier"], j.get("horodatage", "?"))
        elif j:
            msg = "épinglé actuel : %s/%s — ATTENTION fichier absent du dossier" % (j["dossier"], j["fichier"])
        else:
            msg = "aucune épingle posée (featured <fichier> pour épingler)"
        print(json.dumps({"commande": "featured", "featured": j, "message": msg},
                         ensure_ascii=False, indent=2) if a.json else "[featured] %s" % msg)
        return 0
    nom = sanitize_name(a.fichier)
    if not nom:
        return _fin(a.json, "featured", "nom refusé (caché ou vide après assainissement)", 6)
    dossier = None
    for d in ("download", "upload"):
        if os.path.isfile(os.path.join(root, d, nom)):
            dossier = d
            break
    if dossier is None:
        return _fin(a.json, "featured", "fichier introuvable dans download/ ni upload/ : %s "
                    "(poussez-le d'abord : push <source>)" % nom, 6)
    ent = {"fichier": nom, "dossier": dossier,
           "horodatage": time.strftime("%Y-%m-%dT%H:%M:%S%z")}
    with open(marker_path, "w", encoding="utf-8") as f:
        json.dump(ent, f, ensure_ascii=False, indent=1)
    st = os.stat(os.path.join(root, dossier, nom))
    res = {"commande": "featured", "skill": "vue-upload", "version": VERSION,
           "action": "epingle", "featured": ent, "octets": st.st_size,
           "taille": human(st.st_size), "duree_s": round(time.perf_counter() - t0, 3),
           "note": ("le portail affiche désormais ce fichier en tête avec marqueur ★ "
                    "(bannière LIVRABLE COURANT) — ouvrez/rafraîchissez la fenêtre d'accès")}
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print("╔═ vue-upload v%s — FEATURED (épinglage livrable courant)" % VERSION)
        print("║ ★ %s/%s — %s — posé %s" % (dossier, nom, human(st.st_size), ent["horodatage"]))
        print("║ %s" % res["note"])
        print("╚═" + "═" * 60)
    return 0


# ────────────────────────── utilitaires communs ──────────────────────────

def human(n):
    n = float(n)
    if n < 1024:
        return "%d o" % n
    if n < 1048576:
        return "%.1f Ko" % (n / 1024)
    if n < 1073741824:
        return "%.1f Mo" % (n / 1048576)
    return "%.2f Go" % (n / 1073741824)


def sha256_file(path, _buf=1048576):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(_buf):
            h.update(chunk)
    return h.hexdigest()


def sanitize_name(name):
    """Mêmes règles que le serveur : basename, assainissement, cachés refusés."""
    name = os.path.basename(name or "")
    name = re.sub(r'[\\/:*?"<>|]', "_", name).strip()
    if not name or name.startswith("."):
        return None
    return name


def _http_req(url, data=None, method=None, headers=None, timeout=60):
    h = dict(UA)
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, data=data, method=method, headers=h)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read()


def _fin(as_json, cmd, msg, code):
    if as_json:
        print(json.dumps({"commande": cmd, "erreur": msg}, ensure_ascii=False))
    else:
        print("[%s] ERREUR : %s" % (cmd, msg))
    return code


# ────────────────────────── share (repli externe vérifié) ──────────────────────────

def _multipart(field, nom, data):
    b = "----vueupload" + secrets.token_hex(8)
    body = (("--%s\r\nContent-Disposition: form-data; name=\"%s\"; filename=\"%s\"\r\n"
             "Content-Type: application/octet-stream\r\n\r\n") % (b, field, nom)).encode("utf-8") \
           + data + ("\r\n--%s--\r\n" % b).encode("utf-8")
    return body, "multipart/form-data; boundary=%s" % b


def _share_filebin(nom, data, bin_name=None):
    bin_name = (bin_name or ("vue-upload-" + secrets.token_hex(10))).strip()
    if len(bin_name) < 16:
        raise ValueError("le bin filebin doit faire ≥ 16 caractères")
    url = "https://filebin.net/%s/%s" % (bin_name, urllib.parse.quote(nom))
    st, _ = _http_req(url, data=data, method="PUT",
                      headers={"Content-Type": "application/octet-stream"}, timeout=120)
    if st not in (200, 201):
        raise RuntimeError("PUT filebin → HTTP %s" % st)
    return {"url": url, "statut_http": st}


def _share_tmpfiles(nom, data):
    body, ctype = _multipart("file", nom, data)
    st, payload = _http_req("https://tmpfiles.org/api/v1/upload", data=body,
                            headers={"Content-Type": ctype}, timeout=120)
    j = json.loads(payload.decode("utf-8", "replace"))
    if str(j.get("status")) != "success":
        raise RuntimeError("tmpfiles réponse inattendue : %s" % (str(j)[:140]))
    u = (j.get("data") or {}).get("url")
    if not u:
        raise RuntimeError("tmpfiles : url absente de la réponse")
    direct = u.replace("tmpfiles.org/", "tmpfiles.org/dl/", 1)
    # sonde : si l'URL directe sert une page HTML (interstitielle), retrouver le lien /dl/ réel
    try:
        _, b2 = _http_req(direct, timeout=30)
        head = b2[:512].lstrip().lower()
        if head.startswith(b"<!doctype") or head.startswith(b"<html"):
            _, page = _http_req(u, timeout=30)
            m = re.search(r'href="([^"]*/dl/[^"]+)"', page.decode("utf-8", "replace"))
            if m:
                lien = m.group(1)
                if lien.startswith("/"):
                    lien = "https://tmpfiles.org" + lien
                direct = lien
    except Exception:
        pass
    return {"url": direct, "page": u, "statut_http": st}


def _verifie_url(url, sha_attendu, timeout=90, headers=None):
    try:
        st, body = _http_req(url, timeout=timeout, headers=headers)
    except Exception as e:
        return False, "%s: %s" % (type(e).__name__, str(e)[:140])
    if st != 200:
        return False, "HTTP %s" % st
    ok = hashlib.sha256(body).hexdigest() == sha_attendu
    return ok, "%d octets re-téléchargés — sha256 %s" % (len(body), "IDENTIQUE" if ok else "DIFFÉRENT")


def cmd_share(a):
    t0 = time.perf_counter()
    src = os.path.realpath(os.path.expanduser(a.fichier))
    if not os.path.isfile(src):
        return _fin(a.json, "share", "fichier introuvable : %s" % a.fichier, 6)
    taille = os.path.getsize(src)
    if taille > MAX_TAILLE:
        return _fin(a.json, "share", "taille %s > 200 Mo — utilisez un autre canal" % human(taille), 6)
    nom = sanitize_name(a.as_name or os.path.basename(src))
    if not nom:
        return _fin(a.json, "share", "nom refusé (fichier caché ou vide après assainissement)", 6)
    sha = sha256_file(src)
    with open(src, "rb") as f:
        data = f.read()
    cibles = []
    if not a.no_filebin:
        cibles.append(("filebin.net", "≈ 6 jours", lambda: _share_filebin(nom, data, a.bin_name)))
    if not a.no_tmpfiles:
        cibles.append(("tmpfiles.org", "≈ 60 minutes", lambda: _share_tmpfiles(nom, data)))
    resultats = []
    for service, retention, fn in cibles:
        ent = {"service": service, "retention": retention}
        try:
            ent.update(fn())
            if "url" in ent:
                # filebin négocie le contenu selon l'UA : UA navigateur → page HTML de
                # visualisation, UA curl (usage documenté de leur API) → 302 vers le
                # fichier brut. La VÉRIFICATION doit donc partir avec l'UA curl.
                h = {"User-Agent": "curl/8.5.0"} if service == "filebin.net" else None
                ok, detail = _verifie_url(ent["url"], sha, headers=h)
                ent["verifie"] = ok
                ent["verification"] = detail
        except Exception as e:
            ent["verifie"] = False
            ent["erreur"] = ("%s: %s" % (type(e).__name__, e))[:200]
        resultats.append(ent)
    nv = sum(1 for r in resultats if r.get("verifie"))
    duree = round(time.perf_counter() - t0, 2)
    res = {
        "commande": "share", "skill": "vue-upload", "version": VERSION,
        "fichier": src, "nom": nom, "octets": taille, "taille": human(taille),
        "sha256": sha, "duree_s": duree, "cibles": resultats,
        "liens_verifies": nv,
        "regle": "un lien n'est VÉRIFIÉ qu'après re-téléchargement sha256 identique — ne communiquer que ceux-là",
    }
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print("╔═ vue-upload v%s — SHARE (repli externe vérifié) — %.2f s" % (VERSION, duree))
        print("║ fichier : %s — %s — sha256 %s…" % (src, human(taille), sha[:16]))
        for r in resultats:
            if r.get("verifie"):
                print("║ ✓ %s : %s  (rétention %s — sha256 VÉRIFIÉ)" % (r["service"], r["url"], r["retention"]))
            elif "erreur" in r:
                print("║ ✗ %s : échec — %s" % (r["service"], r["erreur"]))
            else:
                print("║ ✗ %s : lien obtenu mais intégrité NON prouvée — %s" % (r["service"], r.get("verification", "")))
        print("╚═" + "═" * 60)
    return 0 if nv else 4


# ────────────────────────── push (inscription livrable) ──────────────────────────

def cmd_push(a):
    src = os.path.realpath(os.path.expanduser(a.source))
    if not os.path.isfile(src):
        return _fin(a.json, "push", "fichier introuvable : %s" % a.source, 6)
    taille = os.path.getsize(src)
    if taille > MAX_TAILLE:
        return _fin(a.json, "push", "taille %s > 200 Mo (garde serveur)" % human(taille), 6)
    nom = sanitize_name(a.as_name or os.path.basename(src))
    if not nom:
        return _fin(a.json, "push", "nom refusé (caché ou vide après assainissement)", 6)
    if a.dir not in ("download", "upload"):
        return _fin(a.json, "push", "--dir doit valoir download ou upload", 6)
    os.makedirs(os.path.join(a.root, a.dir), exist_ok=True)
    dest = os.path.join(a.root, a.dir, nom)
    no_op = False
    if os.path.exists(dest):
        if sha256_file(src) == sha256_file(dest):
            no_op = True
        elif not a.force:
            return _fin(a.json, "push", "%s/%s existe déjà avec un contenu différent — relancez avec --force" % (a.dir, nom), 5)
    if not no_op:
        shutil.copy2(src, dest)
    sha = sha256_file(src)
    verifie = os.path.isfile(dest) and sha256_file(dest) == sha
    res = {
        "commande": "push", "skill": "vue-upload", "version": VERSION,
        "source": src, "destination": dest, "dossier": a.dir, "nom": nom,
        "octets": taille, "taille": human(taille), "sha256": sha,
        "no_op": no_op, "verifie": verifie,
        "note": "le fichier est désormais listé par le panel/serveur (download/ ou upload/)",
    }
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print("╔═ vue-upload v%s — PUSH%s" % (VERSION, " NO-OP (contenu identique)" if no_op else ""))
        print("║ %s → %s — %s" % (src, dest, human(taille)))
        print("║ sha256 %s… — copie %s" % (sha[:16], "VÉRIFIÉE" if verifie else "EN ÉCHEC"))
        print("╚═" + "═" * 60)
    return 0 if verifie else 4


# ────────────────────────── doctor (diagnostic) ──────────────────────────

def cmd_doctor(a):
    t0 = time.perf_counter()
    c = []

    def add(nom, ok, detail=""):
        c.append({"controle": nom, "ok": bool(ok), "detail": str(detail)[:160]})

    racine = os.path.realpath(a.root)
    add("racine projet", os.path.isdir(racine), racine)
    fl = {}
    for d in ("download", "upload"):
        p = os.path.join(racine, d)
        n = len([x for x in os.listdir(p) if os.path.isfile(os.path.join(p, x))]) if os.path.isdir(p) else -1
        fl[d] = n
        add("dossier %s/" % d, n >= 0, "ABSENT" if n < 0 else "%d fichier(s)" % n)
    vivant = port_alive(a.port, 0.3)
    portal_ok = False
    detail_port = "libre — démarrage possible"
    if vivant:
        try:
            st, body = _http_req("http://127.0.0.1:%d/files" % a.port, timeout=2)
            if st == 200 and b"download" in body:
                portal_ok = True
                detail_port = "portail vue-upload répond /files 200"
            else:
                detail_port = "port occupé (HTTP %s, /files non conforme) — autre service ?" % st
        except Exception as e:
            detail_port = "port occupé, pas un portail vue-upload (%s)" % type(e).__name__
    add("port %d" % a.port, (not vivant) or portal_ok, detail_port)
    edge = edge_alive()
    add("edge preview :81", edge, "routage preview disponible" if edge else "indisponible — preview non cliquable")
    try:
        libre = shutil.disk_usage(racine).free
        add("espace disque", libre > 100 * 1024 * 1024, "%s libres" % human(libre))
    except Exception as e:
        add("espace disque", False, str(e)[:100])
    add("python", sys.version_info >= (3, 10), sys.version.split()[0])
    url_loc = "http://127.0.0.1:%d/" % a.port
    if portal_ok and edge:
        verdict = "pret"
        voie = "preview — cliquer le bouton preview de la session maintenant (ou relancer --hold pour rouvrir une fenêtre)"
    elif portal_ok and not edge:
        verdict = "local"
        voie = "portail vivant mais edge :81 absent — accès local %s seulement ; sinon share <fichier>" % url_loc
    elif edge and not vivant:
        verdict = "a-demarrer"
        voie = "lancer : vue_upload_panel.py --hold 540 --port %d puis cliquer le bouton preview pendant la fenêtre" % a.port
    else:
        verdict = "repli"
        voie = "preview indisponible — utiliser : vue_upload_panel.py share <fichier> (liens externes vérifiés) ou push pour organiser download/"
    duree = round(time.perf_counter() - t0, 3)
    res = {
        "commande": "doctor", "skill": "vue-upload", "version": VERSION,
        "duree_s": duree, "verdict": verdict, "voie_recommandee": voie,
        "controles": c, "portail_vivant": portal_ok, "edge_81": edge, "fichiers": fl,
    }
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print("╔═ vue-upload v%s — DOCTOR — %.3f s — verdict : %s" % (VERSION, duree, verdict))
        for x in c:
            print("║ %s %s — %s" % ("✓" if x["ok"] else "✗", x["controle"], x["detail"]))
        print("║ voie recommandée : %s" % voie)
        print("╚═" + "═" * 60)
    return 0


# ────────────────────────── CLI ──────────────────────────

def _extrait(args, cmd, drapeaux_valeur, drapeaux_bool, n_positionnels, usage):
    """Parseur tolérant : les drapeaux de sous-commande peuvent suivre le fichier."""
    pos, inconnus, opts, i = [], [], {}, 0
    while i < len(args):
        t = args[i]
        if t in drapeaux_valeur:
            if i + 1 >= len(args):
                raise SystemExit("[%s] valeur manquante pour %s — %s" % (cmd, t, usage))
            opts[t] = args[i + 1]
            i += 2
        elif t in drapeaux_bool:
            opts[t] = True
            i += 1
        elif t.startswith("--"):
            inconnus.append(t)
            i += 1
        else:
            pos.append(t)
            i += 1
    if inconnus:
        raise SystemExit("[%s] options inconnues : %s — %s" % (cmd, ", ".join(inconnus), usage))
    if len(pos) != n_positionnels:
        raise SystemExit("[%s] %d argument(s) attendu(s) — %s" % (cmd, n_positionnels, usage))
    return pos, opts


USAGE = """usage : vue_upload_panel.py [--port N] [--root RACINE] [--hold N] [--json] [--sort nom|taille|date] [--filter MOTIF] [--featured FICHIER] [sous-commande]

Sous-commandes :
  featured <fichier> [--off]
      Épingle le LIVRABLE COURANT (★ bannière + entrée en tête du portail) —
      le propriétaire voit immédiatement quel fichier télécharger, même parmi
      des dénominations proches (douleur constatée 2026-10-25). --off retire
      l'épingle (no-op honnête) ; sans argument = affiche l'épinglé courant.
  share <fichier> [--as NOM] [--bin BIN] [--no-filebin] [--no-tmpfiles]
      Repli externe AUTOMATISÉ : filebin.net (≈ 6 jours) + tmpfiles.org (≈ 60 min),
      vérification sha256 par re-téléchargement — seuls les liens VÉRIFIÉS sont annoncés.
  push <source> [--as NOM] [--dir download|upload] [--force]
      Inscription dans download/ ou upload/ (règles serveur : assainissement, cachés
      refusés, 200 Mo max) ; no-op honnête si identique ; --force pour écraser.
  doctor
      Diagnostic < 1 s + voie recommandée (preview / --hold / share).
Sans sous-commande → PANEL (voie chaude < 1 s, voie froide in-process < 2 s, --hold N,
featured + derniers téléchargements du journal exposés).

Codes retour : 0 OK · 2 bind impossible · 3 portail mort · 4 vérification impossible ·
5 push destination existante (sans --force) · 6 source ou nom invalide (featured y c.
fichier introuvable).

exemples :
  vue_upload_panel.py                                  panel (voie chaude ou froide)
  vue_upload_panel.py --hold 540 --featured rapport_v3.docx
                                                       épingler + fenêtre d'accès 9 min
  vue_upload_panel.py featured mouton_rasta_sauts_photo_v3.gif
                                                       épinglage seul
  vue_upload_panel.py featured --off                   retirer l'épingle
  vue_upload_panel.py --filter docx --sort taille      listing filtré et trié
  vue_upload_panel.py share rapport.docx               liens externes vérifiés sha256
  vue_upload_panel.py push /tmp/notes.md --as notes.md inscription dans download/
  vue_upload_panel.py doctor                           diagnostic + voie recommandée
"""


def main():
    # parseur manuel TOLÉRANT À L'ORDRE : les drapeaux globaux (--port/--root/--hold/
    # --json/--sort/--filter) sont reconnus AVANT ou APRÈS la sous-commande — argparse
    # rejetait les drapeaux inconnus placés après le fichier (rc 2, défaut T3 du 1er jeu).
    argv = sys.argv[1:]
    if "-h" in argv or "--help" in argv:
        print(USAGE, end="")
        return 0
    g = {"port": 3000, "root": "/home/z/my-project", "hold": 0, "json": False,
         "sort": "nom", "filter": None, "featured": None}
    drapeaux = {"--port": "port", "--root": "root", "--hold": "hold",
                "--sort": "sort", "--filter": "filter", "--featured": "featured"}
    cmd, rargs, i = None, [], 0
    try:
        while i < len(argv):
            t = argv[i]
            if t in drapeaux:
                g[drapeaux[t]] = argv[i + 1]
                i += 2
            elif t == "--json":
                g["json"] = True
                i += 1
            elif t in ("featured", "share", "push", "doctor") and cmd is None:
                cmd = t
                i += 1
            elif cmd is not None:
                rargs.append(t)
                i += 1
            else:
                raise SystemExit("option ou sous-commande inconnue : %s\n\n%s" % (t, USAGE))
    except IndexError:
        raise SystemExit("valeur manquante après %s\n\n%s" % (argv[-1], USAGE))
    if g["sort"] not in ("nom", "taille", "date"):
        raise SystemExit("--sort doit valoir nom|taille|date\n\n%s" % USAGE)
    try:
        g["port"] = int(g["port"])
        g["hold"] = int(g["hold"])
    except ValueError:
        raise SystemExit("--port/--hold doivent être des entiers\n\n%s" % USAGE)
    a = argparse.Namespace(**g)
    if cmd is None:
        return cmd_panel(a)
    if cmd == "featured":
        pos, o = _extrait(rargs, cmd, set(), {"--off"}, 0 if ("--off" in rargs or not rargs) else 1,
                          "featured <fichier> [--off] (ou sans argument = affichage)")
        a.fichier = pos[0] if pos else None
        a.off = o.get("--off", False)
        return cmd_featured(a)
    if cmd == "share":
        pos, o = _extrait(rargs, cmd, {"--as", "--bin"}, {"--no-filebin", "--no-tmpfiles"}, 1,
                          "share <fichier> [--as NOM] [--bin BIN] [--no-filebin] [--no-tmpfiles]")
        a.fichier, a.as_name, a.bin_name = pos[0], o.get("--as"), o.get("--bin")
        a.no_filebin, a.no_tmpfiles = o.get("--no-filebin", False), o.get("--no-tmpfiles", False)
        return cmd_share(a)
    if cmd == "push":
        pos, o = _extrait(rargs, cmd, {"--as", "--dir"}, {"--force"}, 1,
                          "push <source> [--as NOM] [--dir download|upload] [--force]")
        a.source, a.as_name = pos[0], o.get("--as")
        a.dir = o.get("--dir", "download")
        if a.dir not in ("download", "upload"):
            raise SystemExit("[push] --dir doit valoir download ou upload")
        a.force = o.get("--force", False)
        return cmd_push(a)
    if rargs:
        raise SystemExit("[doctor] ne prend pas d'argument")
    return cmd_doctor(a)


if __name__ == "__main__":
    sys.exit(main())
