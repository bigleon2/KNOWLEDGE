#!/usr/bin/env python3
"""vue-upload v1.1.0 — PANEL RAPIDE d'accès aux livrables (Task 36, D036-06).
Douleur traitée : exécution longue + fiabilité irrégulière de l'ancien démarrage.
Conception performante :
  - voie CHAude  : portail déjà vivant → rapport immédiat (< 1 s), zéro démarrage ;
  - voie FROIDE  : serveur démarré IN-PROCESS (thread daemon, import du Handler
    existant — zéro subprocess, zéro setsid) → vivant en < 2 s ;
  - --hold N     : maintient le portail N secondes pendant l'appel d'outil
    (session d'accès deux temps, KB Task 34 — edge :81 → :3000 prouvé) ;
  - stdlib uniquement, aucun appel réseau externe, sortie humaine ou --json.
Recherche z.ai (D036-06) : AUCUNE commande/fonction documentée pour un panneau
de livrables (4 requêtes web, 17 résultats, aucun pertinent ; API storage =
jeton absent) — le mécanisme réel de la plateforme = preview edge :81 → :3000.
"""
import argparse, http.server, importlib.util, json, os, socket, sys, threading, time

SERVER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vue_upload_server.py")
VERSION = "1.1.0"

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

def listing(root):
    out = {}
    for d in ("download", "upload"):
        p = os.path.join(root, d)
        files = []
        if os.path.isdir(p):
            for f in sorted(os.listdir(p)):
                fp = os.path.join(p, f)
                if os.path.isfile(fp):
                    files.append({"fichier": f, "octets": os.path.getsize(fp)})
        out[d] = files
    return out

def main():
    ap = argparse.ArgumentParser(description="vue-upload v1.1.0 — panneau rapide des livrables")
    ap.add_argument("--port", type=int, default=3000)
    ap.add_argument("--root", default="/home/z/my-project")
    ap.add_argument("--hold", type=int, default=0, help="maintient le portail N secondes (session d'accès deux temps)")
    ap.add_argument("--json", action="store_true", help="sortie JSON machine-readable")
    a = ap.parse_args()
    t0 = time.perf_counter()
    voie = "CHAUDE (portail déjà vivant)" if port_alive(a.port, 0.15) else "FROIDE (démarrage in-process)"
    bind_mode = "préexistant"
    if voie.startswith("FROIDE"):
        try:
            _, bind_mode = start_inprocess(a.port, a.root)
        except OSError as e:
            print(json.dumps({"erreur": f"bind impossible :{a.port} — {e}"}, ensure_ascii=False))
            return 2
        for _ in range(30):  # attente vivant max ~1,5 s
            if port_alive(a.port, 0.1):
                break
            time.sleep(0.05)
    duree = time.perf_counter() - t0
    vivant = port_alive(a.port, 0.3)
    fl = listing(a.root)
    panel = {
        "skill": "vue-upload",
        "version": VERSION,
        "voie": voie,
        "bind": bind_mode,
        "portail_vivant": vivant,
        "duree_s": round(duree, 3),
        "url_locale": f"http://127.0.0.1:{a.port}/",
        "routage_preview": "edge :81 vivant → proxifie vers :%d (KB Task 34 — cliquer le bouton preview de la session pendant --hold)" % a.port if edge_alive() else "edge :81 absent — voie locale seulement",
        "download": fl["download"],
        "upload": fl["upload"],
        "limites": "processus éphémère (sandbox fauche les démons entre les appels) — session d'accès = --hold ≤ 540 s pendant le clic preview ; repli = hébergement externe vérifié",
    }
    if a.hold > 0:
        panel["hold_s"] = a.hold
        if a.json:
            print(json.dumps(panel, ensure_ascii=False, indent=2), flush=True)
        else:
            print_panel(panel)
        time.sleep(a.hold)
        return 0
    if a.json:
        print(json.dumps(panel, ensure_ascii=False, indent=2))
    else:
        print_panel(panel)
    return 0 if vivant else 3

def print_panel(p):
    print(f"╔═ vue-upload v{p['version']} — PANEL LIVRABLES ═ voie {p['voie']}")
    print(f"║ durée totale : {p['duree_s']} s · bind {p['bind']} · portail vivant : {p['portail_vivant']}")
    print(f"║ URL locale   : {p['url_locale']}")
    print(f"║ preview      : {p['routage_preview']}")
    for d in ("download", "upload"):
        print(f"╠═ {d}/ ({len(p[d])} fichier(s))")
        for f in p[d][:40]:
            print(f"║   · {f['fichier']} ({f['octets']:,} o)".replace(",", " "))
    print(f"║ note : {p['limites']}")
    print("╚═" + "═" * 60)

if __name__ == "__main__":
    sys.exit(main())
