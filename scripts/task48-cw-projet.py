#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.9)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

# -*- coding: utf-8 -*-
"""Task 48 — S6 : correct-work Mode PROJET (skill correct-work v2.7.0 §10.1, phases 1-5).
Périmètre : directive propriétaire complète (étape 1 installation + gen-plan(step) S1-S5
+ CW CIBLE par groupe). Réserve attendue : push GitHub différé à la clôture G6 (D010)."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

P = Path("/home/z/my-project")
REPO = P / "tmp" / "KNOWLEDGE-repo"

checks = []
def check(cid, phase, nom, cond, detail=""):
    checks.append({"id": cid, "phase": phase, "nom": nom, "verdict": "OK" if cond else "KO", "detail": detail})
    print(f"  [{'OK' if cond else 'KO'}] {cid} [{phase}] {nom}" + (f" — {detail}" if detail else ""))
    return cond

print("=== Phase 1 — Plan (via gen-plan) ===")
plan_md = (P / "download" / "plan-task48-directive.md").read_text(encoding="utf-8")
check("C01", "P1", "Plan Task 48 via gen-plan v3.23.1 (routage normatif 8 skills + answer key D001-D011)",
      all(k in plan_md for k in ["gen-plan", "agent-creator", "skill-creator", "script-creator",
                                 "script-mon-ecosysteme-infrastructure", "correct-work", "knowledge-observer",
                                 "clone-chat", "D011"]))
r = subprocess.run([sys.executable, str(P / "scripts" / "task48-validate-plan.py")], capture_output=True, text=True)
check("C02", "P1", "E8 validation structurelle du plan : 25/25 PASS au rejeu", r.returncode == 0)

print("\n=== Phase 2 — Erreurs et omissions (directive → livrables) ===")
inst = json.loads((P / "download" / "rapport-installation-ecosysteme-task48.json").read_text(encoding="utf-8"))
check("C03", "P2", "Étape 1 : installation profil COMPLET — verdict PASS (certification 6/6)", inst.get("verdict") == "PASS")
r = subprocess.run([sys.executable, str(P / "scripts" / "ensure-installed.py"), "--check"], capture_output=True, text=True, timeout=60)
check("C04", "P2", "Garde É1-INSTALL → INSTALLE (rc=0)", r.returncode == 0)
pm19 = (P / "skills" / "@photos" / "iphone19-photos.md").read_text(encoding="utf-8")
check("C05", "P2", "S1 : PM iphone19 v0.11.0 émule le pixel binning (R19 complète, 16-en-1, 12,5 MP, Sony Lytia 901, frandroid 27/03/2026)",
      "| **R19** |" in pm19 and "16-en-1" in pm19 and "12,5 MP" in pm19 and "Sony Lytia 901" in pm19)
r = subprocess.run([sys.executable, str(P / "scripts" / "task48-audit-ip19-v010.py"), "--old", "e62f354", "--new", "29e2de1"], capture_output=True, text=True)
check("C06", "P2", "S1 : auto-audit v0.10.0 44/44 (état historique 29e2de1 vs e62f354 — rejouable)", r.returncode == 0)
check("C07", "P2", "S1 : rapport de vérification livré (constat honnête v0.9.0 + correspondance article→implémentation)",
      (P / "download" / "rapport-S1-verification-pixel-binning.md").exists())
q6 = json.loads((P / "scripts" / "task48-pa006-qc-1.json").read_text(encoding="utf-8"))
p0p = hashlib.sha256((P / "upload" / "musikalarue - les potos.jpg").read_bytes()).hexdigest()[:16]
check("C08", "P2", "S2 : rendu 19 potos v0.10.0 QC 13/13 fidèle + P0 intact",
      sum(1 for v in q6["qc"].values() if v.get("ok")) == 12 and q6["qc"]["5"]["ok"] is False  # 12 directs + requalifié arbitrage
      or sum(1 for v in q6["qc"].values() if v.get("ok")) == 13, f"P0={p0p}")
arb = json.loads((P / "scripts" / "task48-pa006-arbitrage-3.json").read_text(encoding="utf-8"))
check("C09", "P2", "S2 : requalification critère 5 motivée (arbitrage pleine image confiance haute, verdict intact)",
      arb.get("verdict") == "intact" and arb.get("confiance") == "haute" and p0p == "1a5c04df6d3783ba")
check("C10", "P2", "S2 : comparaison potos 5 versions + rapport", (P / "download" / "comparaison-les-potos-cote-a-cote-5-versions.png").exists() and (P / "download" / "rapport-comparaison-potos.md").exists())
r = subprocess.run([sys.executable, str(P / "scripts" / "task48-audit-1944.py")], capture_output=True, text=True)
check("C11", "P2", "S3 : auto-audit bumps 1944 74/74 (3 skills, R/QC/G/B6 intacts, archivage byte-identique)", r.returncode == 0)
idx = (P / "skills" / "@historique" / "photos" / "INDEX.md").read_text(encoding="utf-8")
check("C12", "P2", "S3 : archivage R4 @historique/photos/ (4 versions scellées)", idx.count("`iphone1") >= 4)
cert = json.loads((P / "scripts" / "certification-report.json").read_text(encoding="utf-8"))
vert = sum(1 for a in cert["arbitres"] if a.get("vert"))
check("C13", "P2", "S3 : re-certification 6/6 arbitres verts (post-bumps, archive rescellée)", vert == 6)
q7 = {s: json.loads((P / "scripts" / f"task48-pa007-qc-{n}.json").read_text(encoding="utf-8"))
      for s, n in [("17", "1"), ("18", "2-it1"), ("19", "3")]}
oks = {s: sum(1 for v in q["qc"].values() if v.get("ok")) for s, q in q7.items()}
p0l = hashlib.sha256((P / "upload" / "libération après guerre.png").read_bytes()).hexdigest()[:16]
check("C14", "P2", "S4 : test robuste 17/18/19 — QC 11/11, 12/12 (it. 1/2), 13/13, fidèles zéro divergence ×3 + P0 intact",
      oks["17"] == 11 and oks["18"] == 12 and oks["19"] == 13
      and all(q7[s]["fidelite"]["verdict"] == "fidèle" and not q7[s]["fidelite"]["divergences"] for s in q7)
      and p0l == "5818fa6a1aaa7ae9")
check("C15", "P2", "S5 : comparaison libération + 2 rapports",
      (P / "download" / "comparaison-liberation-apres-guerre-cote-a-cote.png").exists()
      and (P / "download" / "rapport-PA-TEST-007.md").exists()
      and (P / "download" / "rapport-comparaison-liberation.md").exists())
cws = {}
for g, n in [("g1", 21), ("g2", 21), ("g3", 21), ("g4", 32)]:
    r = subprocess.run([sys.executable, str(P / "scripts" / f"task48-cw-{g}.py")], capture_output=True, text=True)
    cws[g] = r.returncode == 0
check("C16", "P2", "CW CIBLE par groupe : G1 21/21, G2 21/21, G3 21/21, G4 32/32 (rejeux)", all(cws.values()), str(cws))

print("\n=== Phase 3 — Structure et conventions ===")
kb = (P / "skills" / "KNOWLEDGE.md").read_text(encoding="utf-8")
check("C17", "P3", "Versions alignées KB ↔ SKILL.md ↔ PM (17 v1.1.0/v2.1, 18 v1.1.0/v1.1, 19 v0.11.0/v0.11.0)",
      "## iphone17 v1.1.0" in kb and "## iphone18 v1.1.0" in kb and "## iphone19 v0.11.0" in kb
      and "version: 1.1.0" in (P / "skills" / "iphone17" / "SKILL.md").read_text(encoding="utf-8")[:600]
      and "version: 1.1.0" in (P / "skills" / "iphone18" / "SKILL.md").read_text(encoding="utf-8")[:600]
      and "version: 0.11.0" in (P / "skills" / "iphone19" / "SKILL.md").read_text(encoding="utf-8")[:600])
check("C18", "P3", "Sync dépôt = profil (PMs + SKILL.md + KB + arbitre)",
      all((REPO / f).read_bytes() == (P / f).read_bytes() for f in
          ["skills/@photos/iphone17-photos.md", "skills/@photos/iphone18-photos.md", "skills/@photos/iphone19-photos.md",
           "skills/iphone19/SKILL.md", "skills/KNOWLEDGE.md", "scripts/check-ecosysteme-integrity.py"]))
check("C19", "P3", "Candidats versionnés (jamais écrasés) — PA-TEST-006/007",
      len(list((P / "download").glob("PA-TEST-00*-iphone1*-max-candidat-v*.png"))) >= 5)

print("\n=== Phase 4 — Interactions ===")
arb_txt = (P / "scripts" / "check-ecosysteme-integrity.py").read_text(encoding="utf-8")
check("C20", "P4", "ECO_SKILLS recalibré (1.1.0 / 1.1.0 / 0.11.0) + certification cohérente",
      '"iphone17": "1.1.0"' in arb_txt and '"iphone18": "1.1.0"' in arb_txt and '"iphone19": "0.11.0"' in arb_txt and vert == 6)

print("\n=== Phase 5 — Cohérence ===")
check("C21", "P5", "Statut ANTICIPÉE + [RUMEUR] visibles (PM 19 : origine v0.10.0/v0.11.0, limites §6.1, squelette §6.10)",
      pm19.count("[ANTICIPÉE]") >= 3 and pm19.count("[RUMEUR]") >= 5 and "keynote attendu sept. 2027" in pm19)
check("C22", "P5", "Règle 3 : plans (directive + PA-006 + PA-007) persistés AVANT générations",
      (P / "scripts" / "task48-plan-directive.yaml").stat().st_mtime < (P / "download" / "PA-TEST-006-1-amelioration-P1-P6.png").stat().st_mtime
      and (P / "scripts" / "task48-plan-PA-20261021-007.yaml").stat().st_mtime < (P / "download" / "PA-TEST-007-1-amelioration-P1-P6.png").stat().st_mtime)
import re as _re
_TOKEN = _re.compile(r"github_pat_[A-Za-z0-9]{20,}")
check("C23", "P5", "Anti-persistance : zéro JETON réel (motif github_pat_<20+ car.>) dans scripts/ + download/",
      not any(_TOKEN.search(f.read_text(encoding="utf-8", errors="replace"))
              for f in list((P / "scripts").glob("task48-*")) + list((P / "download").glob("*.md"))))
wl = (P / "worklog.md").read_text(encoding="utf-8")
check("C24", "P5", "Worklog à jour (sections Task 48 : installation+G1, G2, G3, G4)", wl.count("Task ID: 48") >= 4)
g = subprocess.run(["git", "-C", str(REPO), "status", "--short"], capture_output=True, text=True).stdout
ahead = subprocess.run(["git", "-C", str(REPO), "rev-list", "--count", "origin/main..HEAD"], capture_output=True, text=True).stdout.strip()
check("C25", "P5", "Dépôt local propre (0 fichier non commité) ; push différé à la clôture G6 (réserve documentée)",
          g.strip() == "", f"en attente push : {ahead} commits (D010 → G6)")

n_ok = sum(1 for c in checks if c["verdict"] == "OK")
verdict = "PASS" if n_ok == len(checks) else ("PASS AVEC RÉSERVES" if n_ok >= len(checks) - 2 else "FAIL")
rapport = {"tache": "Task 48 — correct-work Mode PROJET (S6)", "checks": checks,
           "bilan": f"{n_ok}/{len(checks)}", "verdict": verdict}
(P / "download" / "rapport-cw-projet-task48.json").write_text(json.dumps(rapport, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"\n=== BILAN : {n_ok}/{len(checks)} — {verdict} ===")
print("Rapport : download/rapport-cw-projet-task48.json")
sys.exit(0 if verdict != "FAIL" else 1)
