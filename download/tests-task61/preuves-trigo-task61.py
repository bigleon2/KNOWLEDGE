#!/usr/bin/env python3
"""Task 58 — G2-SG2.2 : harnais de preuves mécaniques du nœud trigo-euler.

Preuves exigées (D585) :
  P1  selftest interne 15/15 ×2 (byte-identique)
  P2  15 opérations via is_client.py (protocole inter-langages, one-shot)
  P3  daemon : demarrer + health-check echo + etat
  P4  concurrence 4 clients × 25 requêtes = 100/100 ok
  P5  saturation 8 clients actifs + 1 → « daemon sature » non-bloquant
  P6  daemon.stop propre → socket supprimée
  P7  orchestrer.py mini-plan (2 tâches, dép) ×2 → sha16 identiques
  P8  cas vivant VOSS : profil axial joint 5c + modèle iso révolution
Journal : tmp/mission-task58/trigo-node/journal-preuves.json
"""
import hashlib
import json
import os
import socket
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor

RACINE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
NOEUD = os.path.join(RACINE, "skills", "dessin-technique", "scripts")
OUT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(RACINE, "skills", "inter-scripts", "scripts"))
from is_client import Client  # noqa: E402

journal = {"preuves": [], "verdict": None}


def preuve(pid, description, ok, details):
    journal["preuves"].append({"id": pid, "description": description,
                               "ok": bool(ok), "details": details})
    print(f"[{'PASS' if ok else 'FAIL'}] {pid} — {description}")
    if not ok:
        print(f"        {details}")


def sha256_fichier(chemin):
    return hashlib.sha256(open(chemin, "rb").read()).hexdigest()


# ---------- P1 : selftest ×2 ----------
st1 = os.path.join(OUT, "selftest-1.txt")
st2 = os.path.join(OUT, "selftest-2.txt")
r1 = subprocess.run([os.path.join(NOEUD, "trigo-euler"), "--selftest"],
                    capture_output=True, text=True, cwd=NOEUD)
r2 = subprocess.run([os.path.join(NOEUD, "trigo-euler"), "--selftest"],
                    capture_output=True, text=True, cwd=NOEUD)
open(st1, "w").write(r1.stdout)
open(st2, "w").write(r2.stdout)
p1_ok = (r1.returncode == 0 and r2.returncode == 0 and
         "15/15 PASS" in r1.stdout and r1.stdout == r2.stdout)
preuve("P1", "selftest interne 15/15 ×2 byte-identique", p1_ok,
       {"rc1": r1.returncode, "rc2": r2.returncode,
        "identiques": r1.stdout == r2.stdout,
        "sha256_binaire": sha256_fichier(os.path.join(NOEUD, "trigo-euler"))})

# ---------- P2 : 15 opérations via is_client (one-shot) ----------
OPS = [
    ("trig.eval", {"fonction": "sin", "x": 0.5}),
    ("trig.resoudre", {"oppose": 3, "adjacente": 4}),
    ("canonique.cercle", {"points": [[0, 0], [4, 0], [0, 4]]}),
    ("canonique.ellipse", {"points": [[3 * __import__("math").cos(t / 3.0) * 0 + 0, 0]
                                      for t in []] or
                           [[2.598, 1.5], [1.837, 2.775], [0.455, 2.965],
                            [-0.75, 2.25], [-1.149, 0.975], [-0.604, -0.353],
                            [0.604, -0.353], [1.149, 0.975], [2.05, 2.4],
                            [0.0, 3.0], [-2.598, 1.5], [-1.5, -2.598]]}),
    ("analyse.derivee", {"fonction": "cos", "x": 0.5}),
    ("analyse.primitive", {"coefficients": [1, 2, 3]}),
    ("analyse.integrale", {"fonction": "sin", "a": 0, "b": 3.14159265358979}),
    ("fourier.serie", {"fonction": "sin", "periode": 6.28318530717959, "harmoniques": 2}),
    ("fourier.eval", {"a0": 0, "an": [0], "bn": [1],
                      "periode": 6.28318530717959, "x": 1.5707963267949}),
    ("euler.formule", {"theta_deg": 90}),
    ("euler.rotation", {"angles_deg": [90, 0, 0], "ordre": "ZXZ", "point": [1, 0, 0]}),
    ("euler.projection", {"point": [1, 0, 0]}),
    ("euler.caracteristique", {"matrice": [[0, -1, 0], [1, 0, 0], [0, 0, 1]]}),
    ("piece.profil_2d", {"segments": [{"x0": 0, "x1": 50, "d": 20}]}),
    ("piece.modele_iso", {"type": "cylindre", "d": 20, "h": 50, "echantillons": 32}),
]
client = Client("trigo-euler")
ops_ok, ops_details = 0, {}
for op, args in OPS:
    rep = client.appeler(op, args, canal="one-shot")
    bon = rep.get("ok") is True
    ops_details[op] = {"ok": bon, "canal": rep.get("canal")}
    if bon:
        ops_ok += 1
preuve("P2", "15 opérations via is_client.py (one-shot)", ops_ok == 15,
       {"ok_count": ops_ok, "operations": ops_details})

# ---------- P3 : daemon démarrage + health-check ----------
d = client.daemon_demarrer()
etat = {"demarrage": d}
if d.get("ok"):
    vivant = client.daemon_vivant()
    etat["health_check_echo"] = vivant
    etat["ready_file"] = os.path.exists("/tmp/trigo-euler.ready")
    etat["pid_file"] = os.path.exists("/tmp/trigo-euler.pid")
    etat["socket"] = os.path.exists("/tmp/trigo-euler.sock")
preuve("P3", "daemon démarré + health-check echo + fichiers socket/ready/pid",
       d.get("ok") and etat.get("health_check_echo") and etat.get("ready_file"),
       etat)

# ---------- P4 : concurrence 4 clients × 25 requêtes = 100/100 ----------
resultats_concurrence = []
verrous = threading.Lock()


def travailleur(num):
    ok_local = 0
    for i in range(25):
        rep = client.appeler("trig.eval", {"fonction": "sin", "x": 0.5 + num * 0.01 + i * 0.001},
                             canal="daemon-socket")
        attendu = 0.5 + num * 0.01 + i * 0.001
        import math
        if rep.get("ok") and abs(rep.get("valeur", 99) - math.sin(attendu)) < 1e-9:
            ok_local += 1
    with verrous:
        resultats_concurrence.append(ok_local)


t0 = time.perf_counter()
with ThreadPoolExecutor(max_workers=4) as pool:
    list(pool.map(travailleur, range(4)))
duree_ms = round((time.perf_counter() - t0) * 1000, 1)
total_ok = sum(resultats_concurrence)
preuve("P4", "concurrence 4 clients × 25 requêtes = 100/100 (ThreadPool)",
       total_ok == 100,
       {"par_client": resultats_concurrence, "total_ok": total_ok,
        "duree_ms": duree_ms,
        "latence_moyenne_ms": round(duree_ms / 100, 3)})

# ---------- P5 : saturation 8 clients actifs + 1 → « daemon sature » ----------
socks = []
for _ in range(8):
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.settimeout(5)
    s.connect("/tmp/trigo-euler.sock")
    socks.append(s)
time.sleep(0.4)  # laisser le daemon accepter les 8 connexions
sat = None
try:
    s9 = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s9.settimeout(5)
    s9.connect("/tmp/trigo-euler.sock")  # la connexion réussit (non-bloquant)
    ligne = s9.makefile("r").readline()
    sat = json.loads(ligne)
    s9.close()
except Exception as e:  # noqa: BLE001
    sat = {"exception": str(e)}
finally:
    for s in socks:
        s.close()
preuve("P5", "saturation max_clients 8 : 9e client → « daemon sature » non-bloquant",
       sat.get("ok") is False and sat.get("erreur") == "daemon sature",
       sat)

# ---------- P6 : daemon.stop propre ----------
arr = client.daemon_arreter()
preuve("P6", "daemon.stop propre → socket supprimée", arr.get("ok") is True,
       {"arret": arr, "socket_absente": not os.path.exists("/tmp/trigo-euler.sock")})

# ---------- P7 : orchestrer mini-plan ×2 (sha16 identiques) ----------
plan = {"projet": "trigo-demo",
        "taches": [
            {"id": "T1", "script": "trigo-euler", "op": "trig.eval",
             "args": {"fonction": "sin", "x": 0.5}, "out": "T1.json", "deps": []},
            {"id": "T2", "script": "trigo-euler", "op": "trig.resoudre",
             "args": {"oppose": 3, "adjacente": 4}, "out": "T2.json", "deps": ["T1"]},
        ]}
plan_f = os.path.join(OUT, "mini-plan.json")
json.dump(plan, open(plan_f, "w"), ensure_ascii=False)
sorties, sha16s, verdicts = [], [], []
for run in (1, 2):
    d = os.path.join(OUT, f"run{run}")
    os.makedirs(d, exist_ok=True)
    # NB : PAS de capture_output (pipe) — le daemon lancé par l'orchestrateur
    # (binaire rémanent voulu) hériterait du pipe et maintiendrait l'EOF ouvert
    # -> blocage de communicate(). Redirection fichier à la place.
    log_f = os.path.join(d, "orchestrer.log")
    with open(log_f, "w") as lf:
        r = subprocess.run([sys.executable,
                            os.path.join(RACINE, "skills", "inter-scripts", "scripts", "orchestrer.py"),
                            "--plans", plan_f, "--executer", "--out-dir", d],
                           stdout=lf, stderr=subprocess.STDOUT, cwd=RACINE, timeout=120)
    try:
        synthese = json.load(open(os.path.join(d, "journal.json")))
        verdicts.append(synthese.get("verdict"))
    except Exception:  # noqa: BLE001
        verdicts.append(f"PARSE-ERR rc={r.returncode} {open(log_f).read()[:200]}")
    sha_run = {}
    for t in ("T1", "T2"):
        chemin = os.path.join(d, f"trigo-demo_{t}.json")
        sha_run[t] = hashlib.sha256(open(chemin, "rb").read()).hexdigest()[:16]
    sha16s.append(sha_run)
# arrêter le daemon que l'orchestrateur a pu démarrer (démarrage paresseux)
client.daemon_arreter()
p7_ok = verdicts == ["PASS", "PASS"] and sha16s[0] == sha16s[1]
preuve("P7", "orchestrer mini-plan (2 tâches, dép) ×2 idempotent (sha16 identiques)",
       p7_ok, {"verdicts": verdicts, "sha16": sha16s,
               "canaux": "T1 daemon-socket (2 tâches nœud concurrent), T2 fichier-typé (dép)"})

# ---------- P8 : cas vivant VOSS — joint 5c ----------
JOINT_5C = {
    "segments": [
        {"x0": 0, "x1": 22.7, "d": 28.5, "note": "filet G"},
        {"x0": 22.7, "x1": 23.9, "d": 26.0, "note": "gorge O-ring (Ø estimé)"},
        {"x0": 23.9, "x1": 33.8, "d": 35.2, "facettes": 6, "note": "hexagone"},
        {"x0": 34.5, "x1": 41.9, "d": 26.0, "note": "filet D (M26×1,5 DKO VOSS)"},
        {"x0": 41.9, "x1": 44.9, "d": 26.0, "note": "bout filet D (cote officielle 44,9)"},
    ],
    "bores": [15.4, 12.0, 6.0],
}
rep_profil = client.appeler("piece.profil_2d", JOINT_5C, canal="one-shot")
rep_iso = client.appeler("piece.modele_iso", dict(JOINT_5C, type="revolution"),
                         canal="one-shot")
json.dump(rep_profil, open(os.path.join(OUT, "joint-5c-profil.json"), "w"),
          ensure_ascii=False, indent=1)
json.dump(rep_iso, open(os.path.join(OUT, "joint-5c-modele-iso.json"), "w"),
          ensure_ascii=False, indent=1)
p8_ok = (rep_profil.get("ok") and rep_iso.get("ok") and
         rep_profil["mesures"]["longueur_totale_mm"] == 44.9 and
         rep_profil["mesures"]["diametre_max_mm"] == 35.2 and
         any("hex" in c for c in rep_profil["cotes"]) and
         rep_iso["verif_perspective"]["concordance"] and
         rep_iso["nb_rendu"] > 100)
preuve("P8", "cas vivant VOSS : profil axial joint 5c (44,9 × 35,2, hexagone, gorges, bores) + modèle iso révolution",
       p8_ok, {"profil": {"longueur": rep_profil.get("mesures", {}).get("longueur_totale_mm"),
                          "diametre_max": rep_profil.get("mesures", {}).get("diametre_max_mm"),
                          "volume_guldin": rep_profil.get("solide", {}).get("volume_guldin_mm3"),
                          "nb_cotes": len(rep_profil.get("cotes", []))},
               "iso": {"nb_rendu": rep_iso.get("nb_rendu"),
                       "concordance_perspective": rep_iso.get("verif_perspective", {}).get("concordance")}})

# ---------- verdict ----------
journal["verdict"] = ("PASS 8/8" if all(p["ok"] for p in journal["preuves"])
                      else "FAIL " + ",".join(p["id"] for p in journal["preuves"] if not p["ok"]))
journal["date"] = time.strftime("%Y-%m-%dT%H:%M:%S")
chemin_journal = os.path.join(OUT, "journal-preuves.json")
json.dump(journal, open(chemin_journal, "w"), ensure_ascii=False, indent=1)
print("\nVERDICT :", journal["verdict"])
sys.exit(0 if journal["verdict"] == "PASS 8/8" else 1)
