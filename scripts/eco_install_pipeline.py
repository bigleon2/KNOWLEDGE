#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.7)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.

Pipeline d'installation PM-INSTALL v1.7.1 (§2) — réinstallation hôte post-wipe
(§3.4 : wipe inter-sessions = cas documenté, ré-exécution depuis l'étape 2).
Source : clone local du dépôt bigleon2/KNOWLEDGE @ b944a27 (règle d'or n°4).
Task 8 (2026-10-17) : pin descendant-tolérant (merge-base --is-ancestor — jamais
un état antérieur au pin, évolution forward du dépôt tolérée) ; dessin-technique
v1.0.0 ancré au socle (sync union + garde R2) après réinscription KB (entrée
perdue lors des wipes — Task 7).

Étapes couvertes par ce script :
  1  Corpus   : sync skills/@mon-ecosysteme/ (9 PMs) + garde R2 anti-rétrogradation
  3-6 Formes  : sync skills/{gen-plan,correct-work,clone-chat,refactor-guard,disciplines}
  7  Registre : sync skills/KNOWLEDGE.md
  8  Outillage: sync scripts/ (arbitres + bootstrap), purge des reconstitutions
               provisoires non canoniques (config.json, verify-correct-work.py)
  2  Archive  : rescellement download/mon-ecosysteme_archive.zip (task21-f2)

Le dépôt et l'hôte partagent le même lignage (projection hôte 109 fichiers) :
union-merge sans --delete, fichiers dépôt = source de vérité au commit épinglé.
Les skills plateforme hors dépôt et les scripts de session sont conservés.
"""
import json
import os
import re
import shutil
import subprocess
import sys

REPO = "/home/z/my-project/tmp/KNOWLEDGE-repo"
HOST = "/home/z/my-project"
PIN = "b944a275c244c801206284bc359f55b400f22375"
NON_CANONIQUES = ["config.json", "scripts/verify-correct-work.py"]


def semver_of(skill_md):
    try:
        head = open(skill_md, encoding="utf-8", errors="replace").read(3000)
    except OSError:
        return None
    m = re.search(r"^version:\s*[\"']?(\d+\.\d+\.\d+)", head, re.M)
    return m.group(1) if m else None


def vtuple(v):
    return tuple(int(x) for x in v.split(".")) if v else (0, 0, 0)


def main():
    report = {"pin": PIN[:7], "etapes": {}, "garde_R2": [], "purges": []}

    # Préflight : commit épinglé (descendant-tolérant — Task 8 : le pin est une
    # garde anti-rétrogradation, pas un verrou d'égalité ; l'évolution forward
    # du dépôt est légitime, un état ANTÉRIEUR au pin reste interdit)
    cur = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO,
                         capture_output=True, text=True).stdout.strip()
    anc = subprocess.run(["git", "merge-base", "--is-ancestor", PIN, cur], cwd=REPO,
                         capture_output=True, text=True)
    if anc.returncode != 0:
        print(f"FAIL commit dépôt {cur[:7]} n'est pas un descendant du pin {PIN[:7]}")
        sys.exit(2)
    report["etapes"]["preflight"] = f"commit {cur[:7]} OK (pin {PIN[:7]} ancêtre — descendant-tolérant)"

    # Garde R2 anti-rétrogradation sur les familles + disciplines
    familles = ["gen-plan", "correct-work", "clone-chat", "refactor-guard",
                "refactoring-engineering", "refactoring-test",
                "prompt-engineering", "knowledge-observer", "audit-provenance",
                "skills-inventory", "script-creator", "script-reviewer",
                "agent-creator", "context-engineering", "loop-engineering",
                "graph-engineering", "harness-engineering", "resource-monitor",
                "fleet-engineering", "memory-engineering",
                "spec-driven-development", "script-mon-ecosysteme-infrastructure",
                "dessin-technique"]
    downgrades = []
    for s in familles:
        v_repo = semver_of(os.path.join(REPO, "skills", s, "SKILL.md"))
        v_host = semver_of(os.path.join(HOST, "skills", s, "SKILL.md"))
        if v_host and v_repo and vtuple(v_host) > vtuple(v_repo):
            downgrades.append(f"{s}: host {v_host} > repo {v_repo}")
    if downgrades:
        print("FAIL garde R2 (host > repo) :", downgrades)
        sys.exit(2)
    report["garde_R2"] = "0 rétrogradation — host ≤ repo partout"

    def sync(rel, delete=False):
        src = os.path.join(REPO, rel)
        dst = os.path.join(HOST, rel)
        if not os.path.exists(src):
            report["etapes"][rel] = "absent du dépôt (ignoré)"
            return
        if os.path.isfile(src):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
            report["etapes"][rel] = "fichier sync"
            return
        if delete and os.path.isdir(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst, dirs_exist_ok=True)
        n = sum(len(f) for _, _, f in os.walk(dst))
        report["etapes"][rel] = f"{n} fichiers"

    # Étape 1 — Corpus canonique
    sync("skills/@mon-ecosysteme", delete=True)
    # Étape 7 — Registre KB
    sync("skills/KNOWLEDGE.md")
    # Étapes 3-6 — Formes installées (familles)
    for s in ["gen-plan", "correct-work"]:
        sync(f"skills/{s}", delete=True)
    # Sync union des autres skills éco (clone-chat, refactor-guard, disciplines)
    for s in ["clone-chat", "refactor-guard", "refactoring-engineering",
              "refactoring-test", "prompt-engineering", "knowledge-observer",
              "audit-provenance", "skills-inventory", "script-creator",
              "script-reviewer", "agent-creator", "context-engineering",
              "loop-engineering", "graph-engineering", "harness-engineering",
              "resource-monitor", "fleet-engineering", "memory-engineering",
              "spec-driven-development", "script-mon-ecosysteme-infrastructure",
              "dessin-technique"]:
        sync(f"skills/{s}")
    # @historique (archive documentaire R4)
    sync("skills/@historique")

    # Étape 8 — Outillage (union : scripts de session conservés)
    sync("scripts")

    # Purge des reconstitutions provisoires non canoniques
    for rel in NON_CANONIQUES:
        p = os.path.join(HOST, rel)
        if os.path.exists(p):
            os.remove(p)
            report["purges"].append(rel)

    # Étape 2 — Rescellement archive d'intégrité (round-trip v2.2)
    r = subprocess.run([sys.executable,
                        os.path.join(HOST, "scripts", "task21-f2-rebuild-archive.py")],
                       capture_output=True, text=True)
    report["etapes"]["2_archive"] = (r.stdout.strip() or r.stderr.strip())[-400:]

    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
