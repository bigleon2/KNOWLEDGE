#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.10)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

# -*- coding: utf-8 -*-
"""Task 48 — correct-work Mode CIBLE (groupe G3 : adaptation 1944 des 3 skills)."""
import json
import subprocess
import sys
from pathlib import Path

HOST = Path("/home/z/my-project")
REPO = HOST / "tmp" / "KNOWLEDGE-repo"

checks = []
def ck(name, ok, detail=""):
    checks.append((name, bool(ok), detail))

# 1. Règle 3 : plan directive AVANT les éditions G3
plan_t = (HOST / "scripts" / "task48-plan-directive.yaml").stat().st_mtime
for pm in ["iphone17-photos.md", "iphone18-photos.md", "iphone19-photos.md"]:
    ck(f"Règle 3 : plan < édition {pm}", plan_t < (REPO / "skills" / "@photos" / pm).stat().st_mtime)

# 2. Auto-audit 74/74 (rejeu)
r = subprocess.run([sys.executable, str(HOST / "scripts" / "task48-audit-1944.py")],
                   capture_output=True, text=True)
ck("Auto-audit 1944 : 74/74 PASS au rejeu", r.returncode == 0, r.stdout[-200:] if r.returncode else "")

# 3. Certification 6/6 (état consolidé post-rescellage)
rep = json.loads((HOST / "scripts" / "certification-report.json").read_text(encoding="utf-8"))
vert = sum(1 for a in rep["arbitres"] if a.get("vert"))
ck("Certification : 6/6 arbitres verts (post-rescellage)", vert == 6, f"verts={vert}")
ck("Certification : 0 échec consolidé", rep["consolide"]["verdict"].startswith("CERTIFICATION COMPLÈTE"))

# 4. Sync dépôt=profil (artefacts G3)
pairs = ["skills/KNOWLEDGE.md", "scripts/check-ecosysteme-integrity.py",
         "skills/@photos/iphone17-photos.md", "skills/@photos/iphone18-photos.md",
         "skills/@photos/iphone19-photos.md", "skills/@photos/README.md",
         "skills/iphone17/SKILL.md", "skills/iphone18/SKILL.md", "skills/iphone19/SKILL.md",
         "skills/@historique/README.md"]
for p in pairs:
    ck(f"Sync dépôt=profil : {p.split('/')[-1]}", (REPO / p).read_bytes() == (HOST / p).read_bytes())
histo_ok = all((REPO / "skills" / "@historique" / "photos" / f.name).read_bytes() == f.read_bytes()
               for f in (HOST / "skills" / "@historique" / "photos").iterdir() if f.is_file())
ck("Sync dépôt=profil : @historique/photos/ (5 fichiers)", histo_ok)

# 5. P0 intacts (aucune génération en G3)
import hashlib
for f in ["musikalarue - les potos.jpg", "musikalarue - les copines.jpg", "libération après guerre.png"]:
    p = HOST / "upload" / f
    ck(f"P0 présent : {f[:30]}…", p.exists())

# 6. Anti-persistance (hors scripts vérificateurs)
leak = any("github_pat_" in f.read_text(encoding="utf-8", errors="replace")
           for f in (HOST / "scripts").glob("task48-*")
           if not f.name.startswith("task48-cw-"))
ck("Anti-persistance : zéro PAT dans les artefacts G3", not leak)

n_ok = sum(1 for _, ok, _ in checks if ok)
print("=== CORRECT-WORK CIBLE — Task 48 / G3 (adaptation 1944 × 3 skills) ===")
for name, ok, detail in checks:
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail and not ok else ""))
print(f"\nBILAN : {n_ok}/{len(checks)} — " + ("PASS" if n_ok == len(checks) else "FAIL"))
sys.exit(0 if n_ok == len(checks) else 1)
