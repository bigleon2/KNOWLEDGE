#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 48 — G1/S1 : auto-audit du bump iphone19 v0.9.0 → v0.10.0 (émulation pixel binning R19).
Vérifie : blocs intangibles byte-identiques vs v0.9.0 (git HEAD), ajouts purs R19/QC13,
propagations, cohérence projection/evals/KB/ECO_SKILLS, coquille §6.9 résorbée."""
import re
import subprocess
import sys
from pathlib import Path

HOST = Path("/home/z/my-project")
REPO = HOST / "tmp" / "KNOWLEDGE-repo"

def git_v090():
    r = subprocess.run(["git", "-C", str(REPO), "show", "HEAD:skills/@photos/iphone19-photos.md"],
                       capture_output=True, text=True, check=True)
    return r.stdout

old = git_v090()
new = (REPO / "skills" / "@photos" / "iphone19-photos.md").read_text(encoding="utf-8")
skill = (REPO / "skills" / "iphone19" / "SKILL.md").read_text(encoding="utf-8")
skill_p = (HOST / "skills" / "iphone19" / "SKILL.md").read_text(encoding="utf-8")
kb = (REPO / "skills" / "KNOWLEDGE.md").read_text(encoding="utf-8")
arb = (REPO / "scripts" / "check-ecosysteme-integrity.py").read_text(encoding="utf-8")
evals = (REPO / "skills" / "iphone19" / "evals" / "evals.json").read_text(encoding="utf-8")

def block(txt, start, end):
    """extrait les lignes de start (incluse) à end (incluse)"""
    lines = txt.splitlines()
    out, on = [], False
    for l in lines:
        if not on and l.startswith(start):
            on = True
        if on:
            out.append(l)
            if l.startswith(end):
                break
    return "\n".join(out)

checks = []
def ck(name, ok, detail=""):
    checks.append((name, bool(ok), detail))

# --- 1. Blocs intangibles byte-identiques v0.9.0 → v0.10.0 ---
b_names = [
    ("Règles R1-R17 (lignes tableau)", "| R1 |", "| R17 |"),
    ("Règle R18", "| **R18** |", "| **R18** |"),
    ("Garde-fous G1-G7", "- **G1** :", "- **G7** :"),
    ("Inventaire B6", "| B6 |", "| B6 |"),
    ("QC 1-11", "1. Visages naturels", "11. **Focale équivalente demandée respectée"),
    ("QC 12", "12. **Ouverture simulée respectée", "12. **Ouverture simulée respectée"),
]
for nm, s, e in b_names:
    o, n = block(old, s, e), block(new, s, e)
    ck(f"INTANGEABLE {nm} byte-identique", o and o == n, f"{len(o)}l vs {len(n)}l")

# --- 2. R19 : ajout pur présent et fonctionnel ---
r19 = block(new, "| **R19** |", "| **R19** |")
ck("R19 présente (ajout pur)", bool(r19))
for kw in ["pixel binning 16-en-1", "200 MP", "12,5 MP", "1/1,12", "crop sauvage", "SNR",
           "Digital Chat Station via Frandroid, 27/03/2026", "JAMAIS une altération des sujets"]:
    ck(f"R19 contient « {kw} »", kw in r19)
ck("R19 absente de v0.9.0 (ajout pur, pas préexistence)", "| **R19** |" not in old)

# --- 3. QC 13 : ajout pur ---
qc13 = block(new, "13. **Émulation pixel binning respectée", "13. **Émulation pixel binning respectée")
ck("QC 13 présente (ajout pur)", bool(qc13) and "R19" in qc13 and "G4" in qc13)
ck("QC 13 absente de v0.9.0", "13. **Émulation pixel binning" not in old)

# --- 4. Propagations ---
ck("§3 regles_declenchees → R19", "regles_declenchees: [R1, ..., R19]" in new)
ck("§8 rapport → R1–R19", "règles déclenchées (R1–R19)" in new)
ck("§8 rapport → binning (13)", "ouverture (12), binning (13)" in new)
ck("§7 expression R19", "Expression de R19 (pixel binning émulé)" in new)
ck("§0 capacités : émulation pixel binning", "une **émulation de pixel binning** (capteur 200 MP, fusion 16-en-1" in new)
ck("§6.1 baseline : capteur 200 MP Lytia", "capteur 200 MP Sony Lytia 901 à pixel binning 16-en-1" in new)
ck("§6.10 : re-ancrage R19 à la confirmation", "re-ancrage de la règle R19" in new)

# --- 5. Ancrage article Frandroid ---
ck("Origine v0.10.0 (bloc Frandroid)", "Origine v0.10.0 (émulation pixel binning" in new and "27/03/2026" in new)
ck("Changelog v0.9.0 → v0.10.0", "Changelog `iphone19-photos.md` v0.9.0 → v0.10.0" in new)
ck("Note rétroactive v0.10.0", "Note rétroactive v0.10.0" in new)
ck("Statut [RUMEUR] conservé", new.count("[RUMEUR]") >= 5)

# --- 6. Coquille §6.9 résorbée ---
ck("En-tête §6.9 unique (coquille doublon corrigée)", new.count("### 6.9 `frontal_center_stage`") == 1,
   f"occurrences: {new.count('### 6.9 `frontal_center_stage`')} (v0.9.0: {old.count('### 6.9 `frontal_center_stage`')})")

# --- 7. Versions et états ---
ck("En-tête PM v0.10.0", "**Version 0.10.0 [ANTICIPÉE] — Langue" in new and "**Version 0.9.0 [ANTICIPÉE] — Langue" not in new)
ck("§12 livrable v0.10.0", "(**v0.10.0 [ANTICIPÉE]**" in new)

# --- 8. Projection SKILL.md ---
ck("Projection : frontmatter version 0.10.0", "version: 0.10.0" in skill)
ck("Projection : description R1-R19 + QC 13", "R1-R19" in skill and "13 critères" in skill)
ck("Projection : tag #r19-pixel-binning", "#r19-pixel-binning" in skill)
ck("Projection : lignage v0.10.0", "v0.10.0 [ANTICIPÉE]" in skill and "pixel binning R19" in skill)
body_new = new[new.index("## PROMPT MAÎTRE — Pipeline"):]
body_skill = skill[skill.index("## PROMPT MAÎTRE — Pipeline"):]
ck("Projection : corps PM VERBATIM", body_new == body_skill)
ck("Projection : dépôt = profil (byte-identiques)", skill == skill_p)

# --- 9. KB + ECO_SKILLS + evals ---
ck("KB : entrée ## iphone19 v0.10.0", "## iphone19 v0.10.0" in kb and "## iphone19 v0.9.0" not in kb)
ck("KB : description R1-R19 + QC 13", "moteur R1-R19" in kb.split("## iphone19 v1.0.0")[0].split("## iphone19 v0.10.0")[1][:3000])
ck("KB : calibration v0.10.0 Task 48", "bump v0.10.0 (Task 48" in kb)
ck("Arbitre ECO_SKILLS : iphone19 0.10.0", '"iphone19": "0.10.0"' in arb)
ck("Evals : moteur R1-R19", "moteur R1-R19" in evals)

# --- 10. Sources intangibles (17/18 non touchées) ---
r = subprocess.run(["git", "-C", str(REPO), "status", "--short", "skills/@photos/"],
                   capture_output=True, text=True)
ck("PMs iphone17/iphone18 non modifiés (R2)",
   "iphone17-photos.md" not in r.stdout and "iphone18-photos.md" not in r.stdout, r.stdout.strip())

n_ok = sum(1 for _, ok, _ in checks if ok)
print("=== AUTO-AUDIT BUMP iphone19 v0.9.0 → v0.10.0 (Task 48 G1) ===")
for name, ok, detail in checks:
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail and not ok else ""))
print(f"\nBILAN : {n_ok}/{len(checks)} PASS")
sys.exit(0 if n_ok == len(checks) else 1)
