#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.10)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

# -*- coding: utf-8 -*-
"""Task 48 — correct-work Mode CIBLE (groupe G4 : PA-TEST-007 × 3 skills + comparaison libération)."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HOST = Path("/home/z/my-project")

checks = []
def ck(name, ok, detail=""):
    checks.append((name, bool(ok), detail))

def sat(p):
    from PIL import Image
    img = Image.open(p).convert("RGB").resize((256, 170))
    px = list(img.getdata())
    return sum(max(r, g, b) - min(r, g, b) for r, g, b in px) / len(px)

# 1. Règle 3
plan_t = (HOST / "scripts" / "task48-plan-PA-20261021-007.yaml").stat().st_mtime
inter_t = (HOST / "download" / "PA-TEST-007-1-amelioration-P1-P6.png").stat().st_mtime
ck("Règle 3 : mini-plan PA-007 < 1re génération", plan_t < inter_t)

# 2. P0 intacts
p0 = hashlib.sha256((HOST / "upload" / "libération après guerre.png").read_bytes()).hexdigest()[:16]
ck("P0 « libération après guerre » intact (5818fa6a1aaa7ae9)", p0 == "5818fa6a1aaa7ae9")
for f in ["musikalarue - les potos.jpg", "musikalarue - les copines.jpg"]:
    ck(f"P0 intact : {f[:28]}…", (HOST / "upload" / f).exists())

# 3. Finaux + verdicts QC
finals = {"17": ("PA-TEST-007-1-iphone17-max.png", "task48-pa007-qc-1.json", 11),
          "18": ("PA-TEST-007-2-iphone18-max.png", "task48-pa007-qc-2-it1.json", 12),
          "19": ("PA-TEST-007-3-iphone19-max.png", "task48-pa007-qc-3.json", 13)}
for sk, (fin, qcf, n) in finals.items():
    p = HOST / "download" / fin
    ck(f"[{sk}] final présent : {fin}", p.exists())
    q = json.loads((HOST / "scripts" / qcf).read_text(encoding="utf-8"))
    oks = sum(1 for v in q["qc"].values() if v.get("ok"))
    ck(f"[{sk}] QC {n}/{n} — fidèle, zéro divergence",
       oks == n and q["fidelite"]["verdict"] == "fidèle" and q["fidelite"]["divergences"] == [],
       f"oks={oks}, verdict={q['fidelite']['verdict']}")

# 4. Monochrome mécanique des finaux
for sk, (fin, _, _) in finals.items():
    s = sat(HOST / "download" / fin)
    ck(f"[{sk}] final monochrome (saturation {s:.2f} < 1.0)", s < 1.0)

# 5. Itération 18 : budget 1/2, candidats versionnés, v2 promu = final
c1 = (HOST / "download" / "PA-TEST-007-2-iphone18-max-candidat-v1.png").read_bytes()
c2 = (HOST / "download" / "PA-TEST-007-2-iphone18-max-candidat-v2.png").read_bytes()
f18 = (HOST / "download" / "PA-TEST-007-2-iphone18-max.png").read_bytes()
ck("[18] candidat v1 rejeté conservé + final = candidat v2 (byte-identique)", c1 != c2 and f18 == c2)
ck("[17]/[19] zéro itération : exactement 1 candidat chacun",
   len(list((HOST / "download").glob("PA-TEST-007-1-iphone17-max-candidat-v*.png"))) == 1
   and len(list((HOST / "download").glob("PA-TEST-007-3-iphone19-max-candidat-v*.png"))) == 1)

# 6. Comparaison : dimensions + rejeu idempotent + sources intactes
from PIL import Image
img = Image.open(HOST / "download" / "comparaison-liberation-apres-guerre-cote-a-cote.png")
ck("Comparaison 2208×1084 (grille 2×3, panneaux 3:2)", img.size == (2208, 1084), str(img.size))
r = subprocess.run([sys.executable, str(HOST / "scripts" / "task48-comparaison-liberation.py")],
                   capture_output=True, text=True)
ck("Composite idempotent (rejeu OK, sources intacts)", r.returncode == 0 and "sources intacts" in r.stdout,
   r.stdout[-200:] if r.returncode else "")

# 7. Rapports
for rep, kws in [("rapport-PA-TEST-007.md", ["11/11", "12/12", "13/13", "colorisation complète", "itération 1/2",
                                             "sans modification, ni retouches", "grain argentique", "Souhaitez-vous des modifications ?"]),
                 ("rapport-comparaison-liberation.md", ["8/8 OK", "désaturation mécanique", "GUIDE DE LECTURE",
                                                        "niveaux de gris", "restauration ≠ colorisation", "Souhaitez-vous des modifications ?"])]:
    t = (HOST / "download" / rep).read_text(encoding="utf-8")
    for kw in kws:
        ck(f"{rep} contient « {kw[:36]} »", kw in t)

# 8. Anti-persistance
leak = any("github_pat_" in f.read_text(encoding="utf-8", errors="replace")
           for f in (HOST / "scripts").glob("task48-*")
           if not f.name.startswith("task48-cw-"))
ck("Anti-persistance : zéro PAT dans les artefacts G4", not leak)

n_ok = sum(1 for _, ok, _ in checks if ok)
print("=== CORRECT-WORK CIBLE — Task 48 / G4 (PA-TEST-007 + comparaison libération) ===")
for name, ok, detail in checks:
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail and not ok else ""))
print(f"\nBILAN : {n_ok}/{len(checks)} — " + ("PASS" if n_ok == len(checks) else "FAIL"))
sys.exit(0 if n_ok == len(checks) else 1)
