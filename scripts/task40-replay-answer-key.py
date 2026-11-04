#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.21)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

"""task40-replay-answer-key.py — Re-jeu mécanique de l'answer key du plan Task 40 (D001-D016).

correct-work(projet) jalons G5/G8 : chaque décision est vérifiée par SA commande
exécutable extraite du plan. Les formulations « cmd >= N » sont converties en
[ $(cmd) -ge N ] ; D012 (PUSH) et D011 (rapport final G8) sont différés tant que
non produits. Statuts dérivés du disque — KO-L003.
"""
import re
import subprocess
from pathlib import Path

RACINE = "/home/z/my-project"
PLAN = Path(f"{RACINE}/download/plan-task40-mission-leon-studio-react.md")
DEPOT = f"{RACINE}/work/knowledge-clone-fddbe94"
DIFFERES = {"D012": "PUSH = G7 (contrôles pré-push à l'exécution)",
            "D011": "rapport final = G8"}

texte = PLAN.read_text(encoding="utf-8")
bloc = re.search(r"```yaml\ndecisions:\n(.*?)```", texte, re.S)
decisions = re.findall(
    r'- id: "(D\d+)"\s*\n\s*criterion: "(.*?)"\s*\n\s*verification: "(.*?)"', bloc.group(1), re.S)

ok_total, ko_total, attente = 0, [], 0
for did, crit, verif in decisions:
    if did in DIFFERES and did == "D012":
        print(f"[ATTENTE] {did} — {DIFFERES[did]}")
        attente += 1
        continue
    if did == "D011" and not Path(f"{RACINE}/download/rapport-final-task40.md").exists():
        print(f"[ATTENTE] {did} — {DIFFERES[did]} (fichier absent à ce stade)")
        attente += 1
        continue
    cmd = verif
    # 1) règles génériques de chemins (les règles worklog ensuite — jamais l'inverse)
    cmd = cmd.replace("download/", f"{RACINE}/download/")
    cmd = cmd.replace("work/", f"{RACINE}/work/")
    cmd = cmd.replace("scripts/check-ecosysteme-integrity.py",
                      f"{RACINE}/scripts/check-ecosysteme-integrity.py")
    cmd = cmd.replace("ls work/drew-fixtures/*.tsi", f"ls {RACINE}/work/drew-fixtures/*.tsi")
    # 2) worklog du dépôt
    cmd = cmd.replace("worklog.md", f"{DEPOT}/worklog.md")
    cmd = cmd.replace(r"grep -c 'PARALLELE\\|∥' ", "grep -cE 'PARALLELE|∥' ")
    cmd = cmd.replace(r"'PERF\\|ms'", "'PERF|ms'")
    cmd = cmd.replace(r"'correctif\\|CORRECTIF'", "'correctif|CORRECTIF'")
    cmd = cmd.replace(r"'résidu\\|RÉSIDU'", "'résidu|RÉSIDU'")
    # 3) « cmd >= N » → [ $(cmd) -ge N ]
    cmd = re.sub(r"^(.*?\S)\s*>=\s*(\d+)\s*$", r"[ $( \1 ) -ge \2 ]", cmd)
    p = subprocess.run(["bash", "-c", cmd], capture_output=True, text=True, cwd=RACINE)
    sortie = (p.stdout + p.stderr).strip().replace("\n", " | ")[:110]
    if p.returncode == 0:
        ok_total += 1
        print(f"[{'PASS':6}] {did} — {sortie}")
    else:
        ko_total.append(did)
        print(f"[{'FAIL':6}] {did} — {sortie}")

print(f"\nREPLAY : {ok_total} PASS / {len(ko_total)} FAIL / {attente} différé(s)")
import sys
sys.exit(1 if ko_total else 0)
