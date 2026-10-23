#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.12)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

"""Arbitre Task 20 — validation du plan et de l'answer key (E8, hook §1.12 gen-plan v3.23.2).

Plan cible : download/plan-task20-test-installation-performante.md
Pattern : task14/15/16/17-answer-key-check.py (16 checks, code retour 0 si et
seulement si 16/16 PASS).

Checks 1-15 : structure du plan (answer key, seuils, groupes, gardes, clôture).
Check 16 : faits vivants (registre alias ECO-LEON, exécuteur canonique, gen-plan hôte).
"""
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLAN = os.path.join(BASE, "download", "plan-task20-test-installation-performante.md")
HOST = "/home/z/my-project"

results = []


def check(num, label, ok, detail=""):
    results.append((num, label, ok, detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] Check {num} : {label}" + (f" — {detail}" if detail else ""))


plan = open(PLAN, encoding="utf-8").read() if os.path.isfile(PLAN) else ""

# 1 — Présence et nommage canonique
check(1, "Plan présent, nommage kebab-case canonique",
      os.path.isfile(PLAN) and re.match(r"^plan-task20-test-installation-performante\.md$", os.path.basename(PLAN)) is not None,
      os.path.basename(PLAN) if plan else "ABSENT")

# 2 — Answer key : bloc decisions YAML avec >= 12 décisions
m = re.search(r"```yaml\s*\ndecisions:\s*\n(.*?)```", plan, re.S)
dec_block = m.group(1) if m else ""
ids = re.findall(r'- id: "(D\d+)"', dec_block)
check(2, "Answer key YAML présente (>= 12 décisions)", len(ids) >= 12, f"{len(ids)} décisions : {ids[0]}..{ids[-1]}")

# 3 — Champs requis par décision
req = ["criterion:", "verification:", "source:", "priority:", "status:"]
missing = [f for f in req if dec_block.count(f) < len(ids)]
check(3, "Champs criterion/verification/source/priority/status sur chaque décision",
      len(ids) > 0 and not missing,
      "complets" if not missing else f"manquants: {missing}")

# 4 — Priorités valides
prios = re.findall(r'priority: "?(S[1-4])"?', dec_block)
check(4, "Priorités S1/S2 valides", all(p in ("S1", "S2", "S3", "S4") for p in prios) and len(prios) == len(ids),
      f"{len(prios)} priorités")

# 5 — Statuts initiaux pending
stats = re.findall(r'status: "?(\w+)"?', dec_block)
check(5, "Statuts initiaux 'pending' (aucun pré-marqué verified)",
      len(stats) == len(ids) and all(s == "pending" for s in stats),
      f"{stats.count('pending')}/{len(stats)} pending")

# 6 — Identifiants séquentiels D001..D0nn sans doublon
expected = [f"D{n:03d}" for n in range(1, len(ids) + 1)]
check(6, "Identifiants séquentiels sans doublon", ids == expected, f"{ids[0]}..{ids[-1]}")

# 7 — Seuils de verdict §5
ok7 = all(v in plan for v in ["PERFORMANT", "PARTIELLEMENT PERFORMANT", "NON PERFORMANT"]) and "## §5 — Seuils de verdict" in plan
check(7, "Seuils de verdict explicites (3 niveaux, §5)", ok7)

# 8 — Définition opérationnelle 5 axes (§2)
axes = ["Complétude", "Intégrité", "Fonctionnalité", "Performance", "Idempotence"]
check(8, "Définition opérationnelle 5 axes (§2)", all(a in plan for a in axes), " · ".join(axes))

# 9 — Groupes séquentiels G1-G5 avec #token
grp = [g for g in ["G1 —", "G2 —", "G3 —", "G4 —", "G5 —"] if g in plan]
tok = re.search(r"\*\*Total estimé\*\* : ~(\d+) k #token", plan)
check(9, "Groupes séquentiels G1-G5 + budget #token", len(grp) == 5 and tok is not None,
      f"{len(grp)}/5 groupes · total ~{tok.group(1) if tok else '?'} k")

# 10 — Exécuteur canonique + pin
ok10 = "eco_install_pipeline.py" in plan and "b75a620" in plan
check(10, "Exécuteur canonique eco_install_pipeline.py + pin b75a620 référencés", ok10)

# 11 — Règle d'or n°2
ok11 = "0 commit, 0 push" in plan and "règle d'or n°2" in plan.lower()
check(11, "Garde règle d'or n°2 (aucun commit/push sans GO)", ok11)

# 12 — Délégation alias-eco §10.1 (D012)
ok12 = "§10.1" in plan and "alias-eco" in plan and "D012" in plan
check(12, "Clôture : délégation alias-eco §10.1 + D012", ok12)

# 13 — Expansion $ECO-LEON documentée (G2 plan Task 19)
ok13 = "$ECO-LEON" in plan and "mon écosystème personnel" in plan and "Expansion alias" in plan
check(13, "Expansion $ECO-LEON documentée dans l'en-tête", ok13)

# 14 — Hooks correct-work par phase (E9-E14, §6)
ok14 = "E9-E14" in plan and "correct-work" in plan
check(14, "Hooks correct-work par phase (E9-E14) prévus §6", ok14)

# 15 — Harnais de tests + snapshots SHA-256
ok15 = "task20-tests-installation.py" in plan and "SHA-256" in plan
check(15, "Harnais de tests désigné + snapshots SHA-256 (idempotence)", ok15)

# 16 — Faits vivants : registre ECO-LEON + exécuteur + gen-plan hôte
reg_path = os.path.join(HOST, "skills", "@historique", "@Alias", "aliases.json")
eco_ok = exe_ok = gp_ok = False
detail = []
if os.path.isfile(reg_path):
    reg = json.load(open(reg_path, encoding="utf-8"))
    hits = [p for p in reg.get("phrases", []) if p.get("alias") == "ECO-LEON"]
    eco_ok = any(p.get("phrase") == "mon écosystème personnel" for p in hits)
    detail.append(f"registre ECO-LEON {'OK' if eco_ok else 'SANS ENTRÉE'}")
else:
    detail.append("registre ABSENT")
exe_ok = os.path.isfile(os.path.join(BASE, "scripts", "eco_install_pipeline.py"))
detail.append(f"exécuteur canonique {'OK' if exe_ok else 'ABSENT'}")
gp = os.path.join(HOST, "skills", "gen-plan", "SKILL.md")
if os.path.isfile(gp):
    head = open(gp, encoding="utf-8", errors="replace").read(3000)
    gp_ok = re.search(r"^version:\s*[\"']?3\.23\.2", head, re.M) is not None
    detail.append(f"gen-plan hôte {'v3.23.2' if gp_ok else 'VERSION INATTENDUE'}")
else:
    detail.append("gen-plan hôte ABSENT")
check(16, "Faits vivants : ECO-LEON au registre + exécuteur + gen-plan hôte v3.23.2",
      eco_ok and exe_ok and gp_ok, " · ".join(detail))

n_pass = sum(1 for _, _, ok, _ in results if ok)
print("\n=== RESUME ===")
print(f"  PASS  : {n_pass}/{len(results)}")
print(f"  FAIL  : {len(results) - n_pass}/{len(results)}")
sys.exit(0 if n_pass == len(results) else 1)
