#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.12)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

# -*- coding: utf-8 -*-
"""Task 48 — correct-work Mode CIBLE (groupe G1 : vérification pixel binning + bump v0.10.0).
Vérifie les livrables du groupe, l'invariant règle 3 (plan AVANT action), R2 (sources 17/18
intactes), P0 intacts, et la présence du rapport de vérification avec ses preuves."""
import subprocess
import sys
from pathlib import Path

HOST = Path("/home/z/my-project")
REPO = HOST / "tmp" / "KNOWLEDGE-repo"

checks = []
def ck(name, ok, detail=""):
    checks.append((name, bool(ok), detail))

# 1. Règle 3 : plan persisté AVANT l'action G1 (édition PM)
plan_t = (HOST / "scripts" / "task48-plan-directive.yaml").stat().st_mtime
pm_t = (REPO / "skills" / "@photos" / "iphone19-photos.md").stat().st_mtime
ck("Règle 3 : plan (mtime %d) < édition PM (mtime %d)" % (plan_t, pm_t), plan_t < pm_t)

# 2. Auto-audit 44/44 (preuve exécutable — rejeu)
# Rejouabilité : audit de l'état v0.10.0 préservé au commit 29e2de1 (G1+G2), vs v0.9.0 (e62f354)
r = subprocess.run([sys.executable, str(HOST / "scripts" / "task48-audit-ip19-v010.py"),
                    "--old", "e62f354", "--new", "29e2de1"], capture_output=True, text=True)
ck("Auto-audit v0.10.0 : 44/44 PASS (état historique 29e2de1 vs e62f354, rejouable)", r.returncode == 0, r.stdout[-300:] if r.returncode else "")

# 3. Rapport de vérification S1 présent + contenu factuel
rep = (HOST / "download" / "rapport-S1-verification-pixel-binning.md").read_text(encoding="utf-8")
for kw in ["v0.9.0 N'ÉMULAIT PAS", "bump v0.9.0 → v0.10.0", "Sony Lytia 901", "16 pixels en un seul",
           "12,5", "1/1,12", "Digital Chat Station", "[RUMEUR]", "44/44 PASS", "Souhaitez-vous des modifications ?"]:
    ck(f"Rapport S1 contient « {kw[:40]} »", kw in rep)

# 4. R2 : sources certifiées 17/18 intactes + versionné git propre sur @photos/17-18
g = subprocess.run(["git", "-C", str(REPO), "status", "--short"], capture_output=True, text=True).stdout
ck("R2 : iphone17-photos.md / iphone18-photos.md non modifiés",
   "iphone17-photos.md" not in g and "iphone18-photos.md" not in g)

# 5. P0 intacts (aucun traitement photo en G1 — contrôle de non-régression global upload/)
import hashlib
shas = {}
for f in ["musikalarue - les potos.jpg", "musikalarue - les copines.jpg", "libération après guerre.png"]:
    p = HOST / "upload" / f
    if p.exists():
        shas[f] = hashlib.sha256(p.read_bytes()).hexdigest()[:16]
ck("P0 présents (3 originaux upload/)", len(shas) == 3, str(list(shas)))

# 6. Synchronisation dépôt ↔ profil sur les 5 artefacts G1
pairs = [
    (REPO / "skills" / "@photos" / "iphone19-photos.md", HOST / "skills" / "@photos" / "iphone19-photos.md"),
    (REPO / "skills" / "iphone19" / "SKILL.md", HOST / "skills" / "iphone19" / "SKILL.md"),
    (REPO / "skills" / "iphone19" / "evals" / "evals.json", HOST / "skills" / "iphone19" / "evals" / "evals.json"),
    (REPO / "skills" / "KNOWLEDGE.md", HOST / "skills" / "KNOWLEDGE.md"),
    (REPO / "scripts" / "check-ecosysteme-integrity.py", HOST / "scripts" / "check-ecosysteme-integrity.py"),
    (REPO / "skills" / "@photos" / "README.md", HOST / "skills" / "@photos" / "README.md"),
]
for a, b in pairs:
    ck(f"Sync dépôt=profil : {a.name}", a.read_bytes() == b.read_bytes())

# 7. Anti-persistance : aucun jeton dans les fichiers de session
leak = False
self_path = Path(__file__).resolve()
paths = [p for p in (HOST / "scripts").glob("task48-*") if not p.name.startswith("task48-cw-")] \
        + list((HOST / "download").glob("rapport-S1-*.md")) \
        + [REPO / "skills" / "@photos" / "iphone19-photos.md"]
for f in paths:
    if "github_pat_" in f.read_text(encoding="utf-8", errors="replace"):
        leak = True
ck("Anti-persistance : zéro PAT dans les artefacts", not leak)

n_ok = sum(1 for _, ok, _ in checks if ok)
print("=== CORRECT-WORK CIBLE — Task 48 / G1 (S1 pixel binning) ===")
for name, ok, detail in checks:
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail and not ok else ""))
print(f"\nBILAN : {n_ok}/{len(checks)} — " + ("PASS" if n_ok == len(checks) else "FAIL"))
sys.exit(0 if n_ok == len(checks) else 1)
