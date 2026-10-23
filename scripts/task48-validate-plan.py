#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.11)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

# -*- coding: utf-8 -*-
"""Task 48 — E8 : validation structurelle du plan + answer key (pattern task41-validate-answer-key.py,
l'arbitre answer-key-checker.py n'étant pas matérialisé au dépôt — constat Task 41 déjà consigné)."""
import re
import sys
from pathlib import Path

YAML = Path("/home/z/my-project/scripts/task48-plan-directive.yaml").read_text(encoding="utf-8")
MD = Path("/home/z/my-project/download/plan-task48-directive.md").read_text(encoding="utf-8")

checks = []
def ck(name, ok, detail=""):
    checks.append((name, bool(ok), detail))

# 1. YAML : directives S1-S7 + D010 présentes
for d in ["S1:", "S2:", "S3:", "S4:", "S5:", "S6:", "S7:", "D010:"]:
    ck(f"YAML directive {d}", re.search(rf"^\s{{2}}{re.escape(d)}", YAML, re.M), "bloc présent")

# 2. YAML : invariants + ordre + estimation
for k in ["ordre:", "invariants:", "estimation:", "groupes_cw:"]:
    ck(f"YAML section {k}", k in YAML)

# 3. YAML : éléments critiques S1 (pixel binning) et S3 (1944)
ck("S1 mentionne pixel binning + 16-en-1 + 12,5 MP", all(t in YAML for t in ["pixel binning", "16-en-1", "12,5 MP"]))
ck("S1 mentionne frandroid + Digital Chat Station", "frandroid" in YAML and "Digital Chat Station" in YAML)
ck("S3 mentionne 1944 + bumps MINOR + archivage R4", all(t in YAML for t in ["1944", "v1.1.0", "v0.11.0", "archivage @historique R4"]))
ck("S4 mentionne libération après guerre + 3 skills", all(t in YAML for t in ["libération après guerre", "iphone17", "iphone18", "iphone19"]))
ck("S2/S5 mentionnent comparaison enrichie + guide de lecture", YAML.count("GUIDE DE LECTURE") >= 2)
ck("Remède SSE présent (createVision + thinking disabled)", "createVision" in YAML and "thinking disabled" in YAML)

# 4. MD : routage normatif complet (N2 — check-tool-routing)
routing = ["gen-plan", "agent-creator", "skill-creator", "script-creator",
           "script-mon-ecosysteme-infrastructure", "correct-work", "knowledge-observer", "clone-chat"]
ck("MD routage : 8 skills dédiés cités", all(r in MD for r in routing))

# 5. MD : answer key D001-D011
ids = re.findall(r"\| (D0\d\d) \|", MD)
ck("MD answer key D001-D011 (11 entrées)", sorted(set(ids)) == [f"D0{i:02d}" for i in range(1, 12)], f"trouvés: {sorted(set(ids))}")

# 6. MD : directives S1-S7 + D010 avec états
ck("MD table directives S1-S7 + D010", all(f"| {d} " in MD for d in ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "D010"]))

# 7. MD : invariants (R2/R4, G1-G7, ANTICIPÉE, PAT)
ck("MD invariants R2/R4 + G1-G7/B6 + ANTICIPÉE + PAT", all(t in MD for t in ["R2", "R4", "G1-G7", "ANTICIPÉE", "PAT"]))

# 8. Règle 3 : plan YAML et MD existent, MD référence le YAML
ck("MD référence le YAML (règle 3)", "task48-plan-directive.yaml" in MD)

# 9. Cohérence versions : v0.10.0 (S1) puis v0.11.0 (S3) pour iphone19 ; v1.1.0 pour 17/18
ck("Versions cohérentes iphone19 v0.10.0 → v0.11.0", YAML.index("v0.10.0") < YAML.index("v0.11.0"))
ck("Versions iphone17/18 v1.1.0", YAML.count("v1.1.0") >= 2)

n_ok = sum(1 for _, ok, _ in checks if ok)
print(f"=== VALIDATION STRUCTURELLE PLAN TASK 48 ===")
for name, ok, detail in checks:
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f" — {detail}" if detail and not ok else ""))
print(f"\nBILAN : {n_ok}/{len(checks)} PASS")
sys.exit(0 if n_ok == len(checks) else 1)
