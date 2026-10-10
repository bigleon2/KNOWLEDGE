#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 16 — harnais answer-key-checker (16 checks mécaniques, lecture seule).

Vérifie la couche Task 16 contre l'answer key D001-D008 du plan
download/plan-task16-corpus-pms-historique-reinstallation.md :
@historique byte-proof, corpus 8, réinstallation profil, recalibrage KO-L004,
arbitres verts, 0 persistance de jeton.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path("/home/z/my-project/work_knowledge")
CORPUS = ROOT / "skills" / "@mon-ecosysteme"
HIST = ROOT / "skills" / "@historique"
PROFIL = Path("/home/z/my-project/skills")
TOKEN_MARK = "11AJST" + "JXQ0"  # préfixe VALEUR du PAT — reconstruit à l'exécution (jamais stocké littéral : 0 occurrence dans l'arbre, y compris ce harnais)

results = []

def check(name, passed, detail=""):
    results.append((name, bool(passed), detail))
    print(f"  [{'PASS' if passed else 'FAIL'}] {name}{(' — ' + detail) if detail else ''}")

def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()

def blob_b36f177(path):
    r = subprocess.run(["git", "show", f"b36f177:{path}"], cwd=ROOT, capture_output=True)
    return r.stdout if r.returncode == 0 else None

def run(cmd):
    return subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)

OLD_GENS = ["v3.6.1", "v3.7.0", "v3.8.0", "v3.8.1", "v3.9.0", "v3.10.0", "v3.11.0",
            "v3.12.0", "v3.13.0", "v3.16.0", "v3.17.0", "v3.17.1", "v3.17.2", "v3.18.0", "v3.19.0"]
OLD_CWS = ["v2.4.0", "v2.5.0", "v2.5.1", "v2.6.0"]

# --- D002 : plan + inventaire ---
plan = ROOT / "download" / "plan-task16-corpus-pms-historique-reinstallation.md"
plan_txt = plan.read_text(encoding="utf-8") if plan.exists() else ""
ids = [f"D00{i}" for i in range(1, 9)]
check("C01 plan Task 16 présent, answer key D001-D008", plan.exists() and all(i in plan_txt for i in ids),
      f"{len(plan_txt)} o")

# --- D004 : @historique structure + byte-proof ---
gp = sorted((HIST / "prompts-maitres" / "gen-plan").glob("*.md"))
cw = sorted((HIST / "prompts-maitres" / "correct-work").glob("*.md"))
readme_h = (HIST / "README.md").exists()
dist = HIST / "historique-versions-prompts-maitres.md"
check("C02 @historique : README + distillation + 15 gen-plan + 4 correct-work",
      readme_h and dist.exists() and len(gp) == 15 and len(cw) == 4,
      f"{len(gp)}+{len(cw)} fichiers")

bad = []
for fam, vs in (("gen-plan", OLD_GENS), ("correct-work", OLD_CWS)):
    for v in vs:
        name = f"PROMPT-MAITRE-{'GEN-PLAN' if fam == 'gen-plan' else 'CORRECT-WORK'}-{v}.md"
        p = HIST / "prompts-maitres" / fam / name
        ref = blob_b36f177(f"skills/@mon-ecosysteme/{name}")
        if ref is None or not p.exists() or sha_bytes(p.read_bytes()) != sha_bytes(ref):
            bad.append(name)
check("C03 byte-identité 19 PMs archivés = blobs b36f177 (SHA-256)", not bad, f"divergents: {bad or 'aucun'}")

# --- D005 : corpus 8 + PMs de famille intacts (contrainte propriétaire) ; INSTALL = révision documentaire légitime (C16) ---
corpus_files = sorted(p.name for p in CORPUS.iterdir() if p.is_file())
attendu = {"PROMPT-MAITRE-GEN-PLAN-v3.21.0.md", "PROMPT-MAITRE-CORRECT-WORK-v2.7.0.md",
           "PROMPT-MAITRE-CLONE-CHAT-v2.0.0.md", "PROMPT-MAITRE-SHARED.md",
           "PROMPT-MAITRE-INSTALL-ECOSYSTEME.md", "PROMPT-ULTRA-MAITRE-ORCHESTRATION.md",
           "README.md", "SYNC-CONTEXT.md"}
check("C04 corpus = 8 fichiers (noms exacts)", set(corpus_files) == attendu, f"{len(corpus_files)} fichiers")

famille = ["PROMPT-MAITRE-GEN-PLAN-v3.21.0.md", "PROMPT-MAITRE-CORRECT-WORK-v2.7.0.md",
           "PROMPT-MAITRE-CLONE-CHAT-v2.0.0.md"]
vifs_bad = [n for n in famille
            if (blob_b36f177(f"skills/@mon-ecosysteme/{n}") is None
                 or sha_bytes((CORPUS / n).read_bytes()) != sha_bytes(blob_b36f177(f"skills/@mon-ecosysteme/{n}")))]
check("C05 PMs de famille byte-identiques à b36f177 (0 édition — contrainte propriétaire)", not vifs_bad,
      f"divergents: {vifs_bad or 'aucun'}")

# R4 : doublon = même nom ET même octets (critère task14-scan-doublons) — deux README distincts par rôle ne sont pas des doublons
homs = []
for p in CORPUS.glob("*.md"):
    for q in HIST.rglob(p.name):
        if q.is_file() and q.read_bytes() == p.read_bytes():
            homs.append(p.name)
check("C06 0 doublon corpus ↔ @historique (R4 : même nom + même octets)", not homs, f"{homs or 'aucun'}")

# --- D003 : profil réinstallé ---
gpv = ""
gp_skill = PROFIL / "gen-plan" / "SKILL.md"
if gp_skill.exists():
    for line in gp_skill.read_text(encoding="utf-8").splitlines():
        if line.startswith("version:"):
            gpv = line.split(":", 1)[1].strip()
            break
check("C07 gen-plan déployé au profil (v3.21.0)", gpv == "3.21.0", f"version={gpv or 'absent'}")

cwv = ""
cw_skill = PROFIL / "correct-work" / "SKILL.md"
if cw_skill.exists():
    for line in cw_skill.read_text(encoding="utf-8").splitlines():
        if line.startswith("version:"):
            cwv = line.split(":", 1)[1].strip()
            break
check("C08 correct-work déployé au profil (v2.7.0)", cwv == "2.7.0", f"version={cwv or 'absent'}")

kb = PROFIL / "KNOWLEDGE.md"
kb_ok = kb.exists() and kb.read_bytes() == (ROOT / "skills" / "KNOWLEDGE.md").read_bytes()
check("C09 KNOWLEDGE.md déployé au profil (byte-identique au registre KB 28 entrées)", kb_ok)

ALIGNED = ["clone-chat", "context-engineering", "loop-engineering", "graph-engineering",
           "harness-engineering", "skills-inventory", "agent-creator", "prompt-engineering",
           "audit-provenance", "knowledge-observer", "resource-monitor", "script-creator",
           "script-reviewer", "script-mon-ecosysteme-infrastructure"]
div = [s for s in ALIGNED
       if not (PROFIL / s / "SKILL.md").exists()
       or (PROFIL / s / "SKILL.md").read_bytes() != (ROOT / "skills" / s / "SKILL.md").read_bytes()]
check("C14 14 skills écosystème du profil alignés byte-identiques au dépôt", not div, f"divergents: {div or 'aucun'}")

plat = [s for s in ("skill-creator", "version-management", "skill-finder-cn")
        if (PROFIL / s / "SKILL.md").exists()
        and (PROFIL / s / "SKILL.md").read_bytes() != (ROOT / "skills" / s / "SKILL.md").read_bytes()]
check("C15 couche plateforme intouchée (skill-creator, version-management, skill-finder-cn)", len(plat) == 3,
      f"formes plateforme distinctes: {len(plat)}/3")

# --- D006 : recalibrage KO-L004 ---
checker_src = (ROOT / "scripts" / "check-ecosysteme-integrity.py").read_text(encoding="utf-8")
check("C10 CORPUS_ATTENDU = 8 (recalibrage commenté Task 16)",
      "CORPUS_ATTENDU = 8" in checker_src and "Recalibrage Task 16" in checker_src)

f2_src = (ROOT / "scripts" / "task21-f2-rebuild-archive.py").read_text(encoding="utf-8")
check("C11 F2 : 19 retraits sanctionnés + garde anti-perte @historique",
      f2_src.count("PROMPT-MAITRE-") >= 19 and "garde anti-perte" in f2_src)

sync_src = (ROOT / "scripts" / "sync-context-block.py").read_text(encoding="utf-8")
check("C12 sync-context-block recalibré (2 porteurs vivants, v3.11.0/v2.5.1 retirés)",
      "PROMPT-MAITRE-GEN-PLAN-v3.11.0.md" not in sync_src
      and "PROMPT-MAITRE-CORRECT-WORK-v2.5.1.md" not in sync_src
      and "PROMPT-MAITRE-CLONE-CHAT-v2.0.0.md" in sync_src)

ultra = (CORPUS / "PROMPT-ULTRA-MAITRE-ORCHESTRATION.md").read_text(encoding="utf-8")
check("C13 ULTRA régénéré (7 fichiers canoniques + orchestrateur, v3.21.0/v2.7.0/v2.0.0)",
      "7 fichiers canoniques" in ultra and "v3.21.0" in ultra and "3.18.0" not in ultra)

readme_c = (CORPUS / "README.md").read_text(encoding="utf-8")
sync_c = (CORPUS / "SYNC-CONTEXT.md").read_text(encoding="utf-8")
install_c = (CORPUS / "PROMPT-MAITRE-INSTALL-ECOSYSTEME.md").read_text(encoding="utf-8")
check("C16 révisions documentaires (README v2.1.1, SYNC-CONTEXT v1.4.2, PM-INSTALL révision Task 16)",
      "v2.1.1" in readme_c and "v1.4.2" in sync_c
      and "Révision documentaire 2026-10-11 (Task 16" in install_c)

# --- D007 : arbitres (re-vérification compacte) ---
vcw = run(["python3", "scripts/verify-correct-work.py"])
check("C17 arbitre vcw ALL PASS 16/16", "ALL PASS" in vcw.stdout)

integ = run(["python3", "scripts/check-ecosysteme-integrity.py", "--check"])
check("C18 integrity --check 60/60 rc0", integ.returncode == 0 and "60/60 PASS" in integ.stdout)

coh = run(["python3", "scripts/test-coherence-interactions.py"])
check("C19 coherence PASS AVEC RÉSERVES (48/3/0)", "PASS AVEC RÉSERVES" in coh.stdout and "0 FAIL" in coh.stdout)

gpm = run(["python3", "scripts/generer-pm-skill.py", "--check"])
check("C20 generer-pm 3/3 COHERENT rc0", gpm.returncode == 0 and gpm.stdout.count("COHERENT") == 3)

dbl = run(["python3", "scripts/task14-scan-doublons.py"])
check("C21 garde anti-doublons : 0 doublon", "DOUBLONS (même nom + byte-identique) : 0" in dbl.stdout)

# --- D001 : anti-persistance jeton ---
tracked = run(["git", "grep", "-c", TOKEN_MARK, "HEAD"])
work = run(["grep", "-rc", TOKEN_MARK, str(ROOT), "--exclude-dir=.git"])
cfg = run(["git", "config", "--local", "--list"])
tok_hits = [ln for ln in cfg.stdout.splitlines() if TOKEN_MARK in ln.lower()]
check("C22 0 persistance du jeton (arbre suivi + arbre de travail + config locale)",
      tracked.returncode != 0 and work.returncode != 0 and not tok_hits,
      f"suivi rc={tracked.returncode}, travail rc={work.returncode}, config {len(tok_hits)} occurrence(s)")

# --- bilan ---
n_pass = sum(1 for _, ok, _ in results if ok)
n_fail = len(results) - n_pass
print(f"\n=== RESUME : {n_pass}/{len(results)} PASS, {n_fail} FAIL ===")
print("VERDICT : ALL PASS" if n_fail == 0 else "VERDICT : FAIL")
sys.exit(0 if n_fail == 0 else 1)
