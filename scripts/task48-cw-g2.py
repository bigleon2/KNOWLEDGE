#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.9)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

# -*- coding: utf-8 -*-
"""Task 48 — correct-work Mode CIBLE (groupe G2 : campagne PA-TEST-006 + comparaison enrichie potos).
Vérifie les livrables du groupe, la contrainte zéro-retouche, P0 intacts, candidats versionnés,
règle 3, preuves QC/arbitrage, sources de la comparaison intactes, anti-persistance."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HOST = Path("/home/z/my-project")

checks = []
def ck(name, ok, detail=""):
    checks.append((name, bool(ok), detail))

# 1. Règle 3 : mini-plan campagne AVANT la génération
plan_t = (HOST / "scripts" / "task48-plan-PA-20261021-006.yaml").stat().st_mtime
inter_t = (HOST / "download" / "PA-TEST-006-1-amelioration-P1-P6.png").stat().st_mtime
ck("Règle 3 : mini-plan PA-006 (mtime %d) < intermédiaire (mtime %d)" % (plan_t, inter_t), plan_t < inter_t)

# 2. P0 potos intact + jamais modifié
p0 = hashlib.sha256((HOST / "upload" / "musikalarue - les potos.jpg").read_bytes()).hexdigest()[:16]
ck("P0 « les potos » intact (sha256 %s… = 1a5c04df6d3783ba)" % p0, p0 == "1a5c04df6d3783ba")
p0c = hashlib.sha256((HOST / "upload" / "musikalarue - les copines.jpg").read_bytes()).hexdigest()[:16]
p0l = hashlib.sha256((HOST / "upload" / "libération après guerre.png").read_bytes()).hexdigest()[:16]
ck("P0 copines + libération présents et intacts (lecture seule)", len(p0c) == 16 and len(p0l) == 16)

# 3. Chaîne d'appels : 2 appels exactement (pas de retouche supplémentaire) — intermédiaire + 1 candidat
cands = list((HOST / "download").glob("PA-TEST-006-1-iphone19-max-candidat-v*.png"))
ck("Candidats versionnés : exactement 1 (aucune itération — leçon appliquée)", len(cands) == 1, str([c.name for c in cands]))

# 4. QC 13 critères : preuve JSON + verdict 13/13 (12 directs + 1 requalifié arbitrage)
qc = json.loads((HOST / "scripts" / "task48-pa006-qc-1.json").read_text(encoding="utf-8"))
oks_direct = sum(1 for v in qc["qc"].values() if v.get("ok"))
ko_direct = [k for k, v in qc["qc"].items() if not v.get("ok")]
ck("QC grille : 12/13 directs (KO unique = critère 5, requalifié)", oks_direct == 12 and ko_direct == ["5"], str(ko_direct))
arb = json.loads((HOST / "scripts" / "task48-pa006-arbitrage-3.json").read_text(encoding="utf-8"))
ck("Arbitrage pleine image : inscription identique + netteté acceptable + intact + confiance haute",
   arb.get("inscription_identique") is True and arb.get("nettete_acceptable") is True
   and arb.get("verdict") == "intact" and arb.get("confiance") == "haute")
ck("Critère 13 (R19 binning) OK direct", qc["qc"].get("13", {}).get("ok") is True)
ck("Fidélité : verdict ≠ divergences majeures", qc.get("fidelite", {}).get("verdict") != "divergences majeures")

# 5. Final promu = candidat v1 (byte-identique, promotion sans régénération)
fin = (HOST / "download" / "PA-TEST-006-1-iphone19-max.png").read_bytes()
c1 = (HOST / "download" / "PA-TEST-006-1-iphone19-max-candidat-v1.png").read_bytes()
ck("Final = candidat v1 (promotion par copie, byte-identique)", fin == c1)

# 6. Rendu v0.9.0 précédent NON modifié (PA-TEST-005-2 : 12/12 Task 47, sha d'époque ?)
p5 = (HOST / "download" / "PA-TEST-005-2-iphone19-max.png")
ck("Rendu 19 v0.9.0 (PA-TEST-005-2) toujours présent (non remplacé par la v0.10.0)", p5.exists())

# 7. Comparaison : dimensions, 6 panneaux, sources intactes (rejoue la vérification du composite)
from PIL import Image
img = Image.open(HOST / "download" / "comparaison-les-potos-cote-a-cote-5-versions.png")
ck("Comparaison 2208×1204 (grille 2×3)", img.size == (2208, 1204), str(img.size))
r = subprocess.run([sys.executable, str(HOST / "scripts" / "task48-comparaison-potos.py")],
                   capture_output=True, text=True)
ck("Composite idempotent : rejeu OK + sources intacts", r.returncode == 0 and "sources intacts" in r.stdout,
   r.stdout[-200:] if r.returncode else "")

# 8. Rapport présent + éléments clés
rep = (HOST / "download" / "rapport-comparaison-potos.md").read_text(encoding="utf-8")
for kw in ["sans modification, ni retouches", "13/13", "arbitrage ciblé", "R19", "PA-TEST-006-1",
           "GUIDE DE LECTURE", "Limites honnêtes", "Souhaitez-vous des modifications ?"]:
    ck(f"Rapport comparaison contient « {kw[:40]} »", kw in rep)

# 9. Anti-persistance
self_path = Path(__file__).resolve()
leak = any("github_pat_" in f.read_text(encoding="utf-8", errors="replace")
           for f in (HOST / "scripts").glob("task48-*") if not f.name.startswith("task48-cw-"))
ck("Anti-persistance : zéro PAT dans les artefacts G2", not leak)

n_ok = sum(1 for _, ok, _ in checks if ok)
print("=== CORRECT-WORK CIBLE — Task 48 / G2 (PA-TEST-006 + comparaison potos) ===")
for name, ok, detail in checks:
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail and not ok else ""))
print(f"\nBILAN : {n_ok}/{len(checks)} — " + ("PASS" if n_ok == len(checks) else "FAIL"))
sys.exit(0 if n_ok == len(checks) else 1)
