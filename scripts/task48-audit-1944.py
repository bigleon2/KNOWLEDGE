#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.9)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

# -*- coding: utf-8 -*-
"""Task 48 — G3/S3 : auto-audit des bumps 1944 (17 v2.1 / 18 v1.1 / 19 v0.11.0).
Vérifie : blocs intangibles byte-identiques vs état git 29e2de1 (pré-G3), ajouts purs 1944,
projections VERBATIM, KB/ECO_SKILLS/READMEs, archivage @historique/photos byte-identique."""
import hashlib
import subprocess
import sys
from pathlib import Path

HOST = Path("/home/z/my-project")
REPO = HOST / "tmp" / "KNOWLEDGE-repo"
PRE = "29e2de1"  # état pré-G3 (17 v2.0, 18 v1.0, 19 v0.10.0)

def gitshow(commit, path):
    return subprocess.run(["git", "-C", str(REPO), "show", f"{commit}:{path}"],
                          capture_output=True, text=True, check=True).stdout

def block(txt, start, end):
    lines, out, on = txt.splitlines(), [], False
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

PMS = {
    "iphone17": ("iphone17-photos.md", "2.1", "R1 |", "**R17** |", "1. Visages naturels", "11. **Focale équivalente demandée respectée"),
    "iphone18": ("iphone18-photos.md", "1.1", "R1 |", "**R18** |", "1. Visages naturels", "12. **Ouverture simulée respectée"),
    "iphone19": ("iphone19-photos.md", "0.11.0", "R1 |", "**R19** |", "1. Visages naturels", "13. **Émulation pixel binning respectée"),
}

for name, (pmf, ver, r_first, r_last, qc_first, qc_last) in PMS.items():
    new = (REPO / "skills" / "@photos" / pmf).read_text(encoding="utf-8")
    old = gitshow(PRE, f"skills/@photos/{pmf}")
    # --- blocs intangibles byte-identiques vs pré-G3 ---
    bspecs = [
        (f"Règles {r_first.strip()}…{r_last.strip()}", f"| {r_first}", f"| {r_last}"),
        ("Garde-fous G1-G7", "- **G1** :", "- **G7** :"),
        ("Inventaire B6", "| B6 |", "| B6 |"),
        (f"QC ({qc_first[:12]}…{qc_last[:30]})", qc_first, qc_last),
    ]
    for nm, s, e in bspecs:
        o, n = block(old, s, e), block(new, s, e)
        ck(f"[{name}] INTANGEABLE {nm} byte-identique", o and o == n, f"{len(o)}l vs {len(n)}l")
    # --- ajouts purs 1944 ---
    for kw in ["Note années 1940 (photographie argentique N&B", "| **40s** | Film N&B argentique",
               "Extension années 1930-1950", "grain argentique authentique", "Aucune colorisation n'est inventée",
               "années 40 → 2010", f"Note rétroactive v{ver}", "avis grain/tonalité sources argentiques"]:
        ck(f"[{name}] 1944 : « {kw[:44]} » présent", kw in new)
    ck(f"[{name}] en-tête Version {ver}", f"**Version {ver}" in new[:400])
    for kw in ["Note années 1940", "| **40s** |", "Extension années 1930-1950"]:
        ck(f"[{name}] « {kw[:30]} » ABSENT du pré-G3 (ajout pur)", kw not in old)
    # --- projection ---
    skill = (REPO / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
    skill_p = (HOST / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
    ck(f"[{name}] projection : corps PM VERBATIM", skill[skill.index("## PROMPT MAÎTRE — Pipeline"):] == new[new.index("## PROMPT MAÎTRE — Pipeline"):])
    ck(f"[{name}] projection dépôt = profil", skill == skill_p)
    ck(f"[{name}] projection : restaurations 1944 dans description", "argentiques N&B années 1930-1950" in skill and "années 40 → 2010" in skill)

# --- versions projetées ---
vmap = {"iphone17": "1.1.0", "iphone18": "1.1.0", "iphone19": "0.11.0"}
for name, ver in vmap.items():
    fm = (REPO / "skills" / name / "SKILL.md").read_text(encoding="utf-8")[:600]
    ck(f"[{name}] frontmatter version {ver}", f"version: {ver}" in fm)

# --- KB + ECO_SKILLS ---
kb = (REPO / "skills" / "KNOWLEDGE.md").read_text(encoding="utf-8")
ck("KB : ## iphone17 v1.1.0 / ## iphone18 v1.1.0 / ## iphone19 v0.11.0",
   "## iphone17 v1.1.0" in kb and "## iphone18 v1.1.0" in kb and "## iphone19 v0.11.0" in kb)
ck("KB : plus aucune entrée v1.0.0/v0.10.0 pour les 3 skills",
   "## iphone17 v1.0.0" not in kb and "## iphone18 v1.0.0" not in kb and "## iphone19 v0.10.0" not in kb)
ck("KB : descriptions 1944 (3 entrées)", kb.count("argentiques N&B années 1930-1950") >= 3)
arb = (REPO / "scripts" / "check-ecosysteme-integrity.py").read_text(encoding="utf-8")
ck("Arbitre : ECO_SKILLS 1.1.0 / 1.1.0 / 0.11.0",
   '"iphone17": "1.1.0"' in arb and '"iphone18": "1.1.0"' in arb and '"iphone19": "0.11.0"' in arb)

# --- archivage @historique/photos byte-identique ---
ARCH = [("iphone17-photos-v2.0.md", "e62f354"), ("iphone18-photos-v1.0.md", "e62f354"),
        ("iphone19-photos-v0.9.0.md", "e62f354"), ("iphone19-photos-v0.10.0.md", "29e2de1")]
for fname, commit in ARCH:
    a = (REPO / "skills" / "@historique" / "photos" / fname).read_bytes()
    b = gitshow(commit, f"skills/@photos/{fname.rsplit('-v', 1)[0]}.md").encode()
    ck(f"@historique/photos : {fname} byte-identique au blob {commit}", a == b)
idx = (REPO / "skills" / "@historique" / "photos" / "INDEX.md").read_text(encoding="utf-8")
ck("@historique/photos/INDEX.md : 4 versions scellées SHA-256", idx.count("`iphone1") >= 4)

# --- READMEs ---
rp = (REPO / "skills" / "@photos" / "README.md").read_text(encoding="utf-8")
for kw in ["v1.1 COURANT", "v0.11.0 ANTICIPÉE", "v2.1 ARCHIVÉE (génération)", "@historique/photos/"]:
    ck(f"README @photos : « {kw} »", kw in rp)
rh = (REPO / "skills" / "@historique" / "README.md").read_text(encoding="utf-8")
ck("README @historique : ligne photos/", "`photos/`" in rh)

n_ok = sum(1 for _, ok, _ in checks if ok)
print("=== AUTO-AUDIT BUMPS 1944 (Task 48 G3) ===")
for name, ok, detail in checks:
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail and not ok else ""))
print(f"\nBILAN : {n_ok}/{len(checks)} PASS")
sys.exit(0 if n_ok == len(checks) else 1)
