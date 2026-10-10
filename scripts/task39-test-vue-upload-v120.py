#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.6.8)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

# -*- coding: utf-8 -*-
"""task39 — TEST du skill vue-upload v1.2.0 (approfondissement).

Couverture :
  T1  compile py_compile des 2 scripts
  T2  --help (rc 0, usage)
  T3  panel voie FROIDE --json (rétrocompat v1.1.0, version 1.2.0, portail vivant)
  T4  listing --filter + --sort taille (tri décroissant, filtre appliqué)
  T5  push nouveau fichier → rc 0, verifie=true
  T6  push identique → no_op=true rc 0
  T7  push contenu différent sans --force → rc 5 ; avec --force → rc 0
  T8  push fichier caché → rc 6 ; fichier > 200 Mo (creux) → rc 6
  T9  doctor sans serveur (< 1 s, verdict, voie recommandée, contrôles ≥ 7)
  T10 doctor AVEC serveur vivant (portail /files 200 reconnu)
  T11 hold VU-6 : panel --hold 1 --json → hold_s=1, voie CHAUDE
  T12 share réseau : filebin + tmpfiles, ≥ 1 lien VÉRIFIÉ sha256, rc 0
  T13 parseur tolérant : drapeaux avant ET après le fichier (share fichier --json)
  T14 régression Task 33 : suite VU-1..6 → 15/15 PASS, 0 FAIL

Le serveur est démarré/arrêté PAR CE SCRIPT (contrainte sandbox, leçon Task 31).
Root de test : tmp/task39-root (le download/ officiel n'est PAS pollué).
Sortie : scripts/task39-test-vue-upload-v120.json + verdict console.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import time

BASE = "/home/z/my-project"
SKILL = os.path.join(BASE, "ecosystem/skills/vue-upload")
PANEL = os.path.join(SKILL, "scripts/vue_upload_panel.py")
SERVER = os.path.join(SKILL, "scripts/vue_upload_server.py")
T33 = os.path.join(BASE, "scripts/task33-test-vue-upload.py")
ROOT = os.path.join(BASE, "tmp/task39-root")
PORT = 3999
results = []


def check(cid, name, ok, detail=""):
    results.append({"id": cid, "name": name, "ok": bool(ok), "detail": str(detail)[:300]})
    print(("[PASS] " if ok else "[FAIL] ") + cid + " " + name + ((" — " + str(detail)[:300]) if detail else ""), flush=True)


def run(args, timeout=180):
    return subprocess.run([sys.executable] + args, capture_output=True, text=True, timeout=timeout)


# ═══ T1 — compile ═══
r1 = subprocess.run([sys.executable, "-m", "py_compile", PANEL, SERVER], capture_output=True, text=True)
check("T1", "py_compile panel+serveur", r1.returncode == 0, r1.stderr[:200])

# ═══ T2 — --help ═══
r2 = run([PANEL, "--help"])
check("T2", "--help rc 0 + usage", r2.returncode == 0 and "share <fichier>" in r2.stdout and "doctor" in r2.stdout,
      "rc=%s" % r2.returncode)

# ═══ préparation root de test ═══
shutil.rmtree(ROOT, ignore_errors=True)
os.makedirs(os.path.join(ROOT, "download"), exist_ok=True)
os.makedirs(os.path.join(ROOT, "upload"), exist_ok=True)
src = os.path.join(ROOT, "src-a.txt")
open(src, "w").write("contenu A " * 10)
os.makedirs(os.path.join(ROOT, "download"), exist_ok=True)
for nom, taille in [("grand.txt", 5000), ("moyen.txt", 500), ("petit-docx-like.txt", 100)]:
    with open(os.path.join(ROOT, "download", nom), "w") as f:
        f.write("x" * taille)

# ═══ T3 — panel voie froide --json (rétrocompat) ═══
r3 = run([PANEL, "--json", "--port", str(PORT), "--root", ROOT])
try:
    j3 = json.loads(r3.stdout)
except Exception:
    j3 = {}
check("T3", "panel voie froide --json v1.2.0 rétrocompat",
      r3.returncode == 0 and j3.get("version") == "1.2.0" and j3.get("portail_vivant") is True
      and j3.get("voie", "").startswith("FROIDE") and isinstance(j3.get("download"), list),
      "voie=%s portail=%s rc=%s" % (j3.get("voie"), j3.get("portail_vivant"), r3.returncode))

# ═══ T4 — filter/sort ═══
r4 = run([PANEL, "--json", "--filter", "txt", "--sort", "taille", "--port", str(PORT), "--root", ROOT])
try:
    j4 = json.loads(r4.stdout)
    dl = j4.get("download", [])
    tailles = [x["octets"] for x in dl]
    check("T4", "listing --filter txt --sort taille (décroissant)",
          r4.returncode == 0 and len(dl) == 3 and tailles == sorted(tailles, reverse=True)
          and j4.get("tri") == "taille" and j4.get("filtre") == "txt",
          "tailles=%s" % tailles)
except Exception as e:
    check("T4", "listing --filter txt --sort taille (décroissant)", False, repr(e))

# ═══ T5 — push nouveau ═══
r5 = run([PANEL, "--root", ROOT, "push", src])
dest5 = os.path.join(ROOT, "download", "src-a.txt")
check("T5", "push nouveau → rc 0 + copie vérifiée",
      r5.returncode == 0 and "copie VÉRIFIÉE" in r5.stdout and os.path.isfile(dest5),
      "rc=%s out=%s" % (r5.returncode, r5.stdout[-160:].replace("\n", " ")))

# ═══ T6 — push identique → no-op ═══
r6 = run([PANEL, "--root", ROOT, "push", src])
check("T6", "push identique → NO-OP rc 0",
      r6.returncode == 0 and "NO-OP (contenu identique)" in r6.stdout, "rc=%s" % r6.returncode)

# ═══ T7 — push différent sans/avec --force ═══
srcb = os.path.join(ROOT, "src-b.txt")
open(srcb, "w").write("contenu B différent")
r7a = run([PANEL, "--root", ROOT, "push", srcb, "--as", "src-a.txt"])
r7b = run([PANEL, "--root", ROOT, "push", srcb, "--as", "src-a.txt", "--force"])
ok7 = r7a.returncode == 5 and "existe déjà" in (r7a.stdout + r7a.stderr) and r7b.returncode == 0 \
      and "copie VÉRIFIÉE" in r7b.stdout
check("T7", "push différent : rc 5 sans --force, rc 0 avec", ok7,
      "rc7a=%s rc7b=%s" % (r7a.returncode, r7b.returncode))

# ═══ T8 — push caché + push > 200 Mo (creux) ═══
cacher = os.path.join(ROOT, ".secret.txt")
open(cacher, "w").write("secret")
r8a = run([PANEL, "--root", ROOT, "push", cacher])
gros = os.path.join(ROOT, "gros.bin")
with open(gros, "wb") as f:
    f.seek(200 * 1024 * 1024 + 1)
    f.write(b"x")
r8b = run([PANEL, "--root", ROOT, "push", gros])
check("T8", "push caché → rc 6 ; push > 200 Mo → rc 6",
      r8a.returncode == 6 and r8b.returncode == 6, "rc8a=%s rc8b=%s" % (r8a.returncode, r8b.returncode))

# ═══ T9 — doctor sans serveur ═══
t9 = time.perf_counter()
r9 = run([PANEL, "--root", ROOT, "--port", str(PORT), "--json", "doctor"])
d9 = time.perf_counter() - t9
try:
    j9 = json.loads(r9.stdout)
except Exception:
    j9 = {}
check("T9", "doctor sans serveur : <1 s, verdict + voie, ≥7 contrôles",
      r9.returncode == 0 and j9.get("duree_s", 1) < 1.0 and j9.get("verdict") in ("a-demarrer", "repli", "local", "pret")
      and len(j9.get("voie_recommandee", "")) > 10 and len(j9.get("controles", [])) >= 7,
      "duree=%.3fs verdict=%s ctrl=%d" % (d9, j9.get("verdict"), len(j9.get("controles", []))))

# ═══ serveur standalone pour T10/T11 ═══
proc = subprocess.Popen([sys.executable, SERVER, "--port", str(PORT), "--root", ROOT],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
import socket as _s
vivantt = False
for _ in range(40):
    s = _s.socket()
    s.settimeout(0.2)
    try:
        vivantt = s.connect_ex(("127.0.0.1", PORT)) == 0
    finally:
        s.close()
    if vivantt:
        break
    time.sleep(0.05)

# ═══ T10 — doctor avec serveur vivant ═══
r10 = run([PANEL, "--root", ROOT, "--port", str(PORT), "--json", "doctor"])
try:
    j10 = json.loads(r10.stdout)
except Exception:
    j10 = {}
port_ok = any(c["controle"] == "port %d" % PORT and c["ok"] for c in j10.get("controles", []))
check("T10", "doctor serveur vivant : portail /files reconnu", vivantt and r10.returncode == 0 and port_ok,
      "vivant=%s ctrl_port_ok=%s verdict=%s" % (vivantt, port_ok, j10.get("verdict")))

# ═══ T11 — hold VU-6 (voie chaude) ═══
t11 = time.perf_counter()
r11 = run([PANEL, "--json", "--hold", "1", "--port", str(PORT), "--root", ROOT], timeout=60)
d11 = time.perf_counter() - t11
try:
    j11 = json.loads(r11.stdout[:r11.stdout.rfind("}") + 1])
except Exception:
    j11 = {}
check("T11", "hold VU-6 : hold_s=1, voie CHAUDE, attente ≥1 s",
      r11.returncode == 0 and j11.get("hold_s") == 1 and j11.get("voie", "").startswith("CHAUDE") and d11 >= 1.0,
      "hold_s=%s voie=%s duree=%.1fs" % (j11.get("hold_s"), j11.get("voie"), d11))

proc.terminate()
try:
    proc.wait(timeout=5)
except Exception:
    proc.kill()

# ═══ T12 — share réseau (liens vérifiés sha256) ═══
petit = os.path.join(ROOT, "download", "petit-docx-like.txt")
t12 = time.perf_counter()
r12 = run([PANEL, "--root", ROOT, "share", petit, "--json"], timeout=240)
d12 = time.perf_counter() - t12
try:
    j12 = json.loads(r12.stdout)
except Exception:
    j12 = {}
cibles = j12.get("cibles", [])
verifies = [c for c in cibles if c.get("verifie")]
detail12 = "; ".join("%s:%s" % (c.get("service"), "VERIFIE" if c.get("verifie")
                                else c.get("erreur", c.get("verification", "?"))[:60]) for c in cibles)
check("T12", "share réseau : ≥1 lien VÉRIFIÉ sha256, rc 0",
      r12.returncode == 0 and len(verifies) >= 1 and j12.get("sha256"),
      "%.1fs rc=%s [%s]" % (d12, r12.returncode, detail12))

# ═══ T13 — parseur tolérant : drapeaux après le fichier ═══
r13 = run([PANEL, "--root", ROOT, "doctor", "--json"])
ok13 = r13.returncode == 0 and '"commande": "doctor"' in r13.stdout
r13b = run([PANEL, "--root", ROOT, "push", src, "--as", "src-task13.txt", "--json"])
ok13 = ok13 and r13b.returncode == 0 and '"verifie": true' in r13b.stdout
check("T13", "drapeaux après sous-commande/fichier acceptés (doctor --json, push f --json)", ok13,
      "rc13=%s rc13b=%s" % (r13.returncode, r13b.returncode))

# ═══ T14 — régression Task 33 ═══
r14 = subprocess.run([sys.executable, T33], capture_output=True, text=True, timeout=300)
npass = r14.stdout.count("[PASS]")
nfail = r14.stdout.count("[FAIL]")
check("T14", "régression suite Task 33 : 15 PASS / 0 FAIL", nfail == 0 and npass == 15,
      "PASS=%d FAIL=%d rc=%s" % (npass, nfail, r14.returncode))

# ═══ résumé ═══
ok_all = all(x["ok"] for x in results)
resume = {"suite": "task39-vue-upload-v1.2.0", "date": time.strftime("%Y-%m-%d %H:%M:%S"),
          "tests": len(results), "pass": sum(1 for x in results if x["ok"]),
          "fail": sum(1 for x in results if not x["ok"]), "verdict": "PASS" if ok_all else "FAIL",
          "details": results}
out = os.path.join(BASE, "scripts/task39-test-vue-upload-v120.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(resume, f, ensure_ascii=False, indent=2)
print("\n═══ TASK39 : %d/%d PASS — verdict %s ═══" % (resume["pass"], resume["tests"], resume["verdict"]))
print("détails : %s" % out)
sys.exit(0 if ok_all else 1)
