#!/usr/bin/env python3
"""⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.7)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.

inter-scripts — client générique de communication inter-langages (v1.0.0).

Canaux gérés pour un nœud du registre :
- "one-shot"       : subprocess, requête/réponse en fichiers JSON (défaut)
- "stdin-pipe"     : JSON sur stdin -> stdout
- "daemon-socket"  : socket UNIX NDJSON ; démarrage paresseux si absent,
                     health-check, réutilisé par plusieurs tâches simultanées

Usage bibliothèque :
    from is_client import Client
    c = Client("trigo-euler")
    rep = c.appeler("trig.eval", {"fonction": "sin", "x": 0.5})

Usage CLI :
    is_client.py --script trigo-euler --op trig.eval --args '{"x":0.5}'
    is_client.py --script trigo-euler --daemon demarrer|arreter|etat
"""
import argparse
import json
import os
import socket
import subprocess
import sys
import time

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(SKILL))
REGISTRE = os.path.join(SKILL, "scripts", "registre.json")


def charger_registre(chemin=None):
    with open(chemin or REGISTRE, encoding="utf-8") as f:
        return json.load(f)


class Client:
    """Client d'un nœud du registre — choix de canal transparent."""

    def __init__(self, script, registre=None):
        reg = registre or charger_registre()
        if script not in reg["scripts"]:
            raise ValueError(f"script inconnu au registre : {script}")
        self.script = script
        self.noeud = reg["scripts"][script]
        self.registre_path = REGISTRE

    # ---------- canal daemon-socket ----------
    def socket_path(self):
        return self.noeud.get("daemon", {}).get("socket", f"/tmp/{self.script}.sock")

    def ready_path(self):
        return self.noeud.get("daemon", {}).get("ready_file", f"/tmp/{self.script}.ready")

    def daemon_vivant(self):
        sp = self.socket_path()
        if not os.path.exists(sp):
            return False
        try:
            rep = self._socket_call({"op": "echo", "args": {"ping": True}}, timeout=3)
            return bool(rep.get("ok"))
        except Exception:
            return False

    def daemon_demarrer(self, attendre=10.0):
        if self.daemon_vivant():
            return {"ok": True, "deja_actif": True}
        d = self.noeud["daemon"]
        cmd = [self.binaire(), "--daemon", "--socket", d["socket"],
               "--ready-file", d.get("ready_file", ""),
               "--pid-file", d.get("pid_file", ""),
               "--max-clients", str(d.get("max_clients", 8))]
        proc = subprocess.Popen(cmd, stderr=subprocess.DEVNULL, cwd=ROOT)
        t0 = time.time()
        while time.time() - t0 < attendre:
            if os.path.exists(d.get("ready_file", "")) and self.daemon_vivant():
                return {"ok": True, "pid": proc.pid, "demarre": True}
            if proc.poll() is not None:
                return {"ok": False, "erreur": f"daemon exit {proc.returncode}"}
            time.sleep(0.05)
        return {"ok": False, "erreur": "timeout attente ready-file"}

    def daemon_arreter(self):
        try:
            self._socket_call({"op": "daemon.stop", "args": {}}, timeout=5)
        except Exception:
            pass
        t0 = time.time()
        while time.time() - t0 < 5 and os.path.exists(self.socket_path()):
            time.sleep(0.05)
        return {"ok": not os.path.exists(self.socket_path())}

    def binaire(self):
        b = self.noeud.get("binaire") or self.noeud.get("script")
        return b if os.path.isabs(b) else os.path.join(ROOT, b)

    # ---------- transport ----------
    def _socket_call(self, requete, timeout=30):
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect(self.socket_path())
        f = s.makefile("rwb")
        f.write((json.dumps(requete) + "\n").encode())
        f.flush()
        rep = json.loads(f.readline().decode())
        f.close()
        s.close()
        return rep

    def appeler(self, op, args=None, canal=None, timeout=60, cwd=None):
        """Appelle une op — canal auto : daemon si actif/demandé, sinon one-shot."""
        requete = {"op": op, "args": args or {}}
        wants_daemon = canal == "daemon-socket" or (
            canal is None and self.noeud.get("daemon") and self.daemon_vivant())
        if wants_daemon:
            # le canal daemon est exigé : démarrage paresseux si nécessaire
            if not self.daemon_vivant():
                d = self.daemon_demarrer()
                if not d.get("ok"):
                    raise RuntimeError(f"daemon indisponible : {d.get('erreur')}")
            rep = self._socket_call(requete, timeout=timeout)
            return dict(rep, canal="daemon-socket")
        if self.noeud.get("daemon"):
            # le nœud SUPPORTE le daemon : démarrage paresseux
            d = self.daemon_demarrer()
            if d.get("ok"):
                rep = self._socket_call(requete, timeout=timeout)
                return dict(rep, canal="daemon-socket", daemon_demarre=not d.get("deja_actif"))
        # one-shot fichiers
        req_f = f"/tmp/is-client-{self.script}-{os.getpid()}-{time.time_ns()}.req.json"
        out_f = req_f.replace(".req.json", ".rep.json")
        with open(req_f, "w", encoding="utf-8") as f:
            json.dump(requete, f, ensure_ascii=False)
        proc = subprocess.run([self.binaire(), "--request", req_f, "--out", out_f],
                              capture_output=True, text=True, timeout=timeout,
                              cwd=cwd or ROOT)
        try:
            os.remove(req_f)
        except OSError:
            pass
        if not os.path.exists(out_f):
            raise RuntimeError(f"{self.script} : pas de réponse (rc={proc.returncode}) "
                               f"{proc.stderr[-200:]}")
        with open(out_f, encoding="utf-8") as f:
            rep = json.load(f)
        os.remove(out_f)
        return dict(rep, canal="one-shot", rc=proc.returncode)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--script", required=True)
    ap.add_argument("--op")
    ap.add_argument("--args", default="{}")
    ap.add_argument("--daemon", choices=["demarrer", "arreter", "etat"])
    ap.add_argument("--canal", choices=["auto", "daemon-socket", "one-shot"], default="auto")
    a = ap.parse_args()
    c = Client(a.script)
    if a.daemon == "demarrer":
        print(json.dumps(c.daemon_demarrer(), ensure_ascii=False))
        return 0
    if a.daemon == "arreter":
        print(json.dumps(c.daemon_arreter(), ensure_ascii=False))
        return 0
    if a.daemon == "etat":
        print(json.dumps({"script": a.script, "vivant": c.daemon_vivant(),
                          "socket": c.socket_path()}, ensure_ascii=False))
        return 0
    if not a.op:
        ap.error("--op requis (ou --daemon)")
    canal = None if a.canal == "auto" else a.canal
    rep = c.appeler(a.op, json.loads(a.args), canal=canal)
    print(json.dumps(rep, ensure_ascii=False, indent=1))
    return 0 if rep.get("ok") else 1


if __name__ == "__main__":
    sys.exit(main())
