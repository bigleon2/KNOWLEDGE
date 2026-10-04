#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Task 23 (D006) — Garde É1-INSTALL : auto-réinstallation de l'écosystème.
Hook gen-plan v3.19.0 §1.16 — exécuter AVANT E1.

  --check      rc=0 écosystème installé / rc=1 absent ou dérivé (lecture seule)
  --reinstall  si ABSENT : clone (jeton éphémère env GITHUB_TOKEN, jamais persisté)
               puis vérification pipeline (Phase A) ; si déjà installé : no-op (idempotence)
               si présent mais DÉRIVÉ : diagnostic + rc=2 (aucune action destructive)
"""
import hashlib, json, os, subprocess, sys
from pathlib import Path

ROOT = Path("/home/z/my-project/ecosystem")
ORIGIN = "https://github.com/bigleon2/KNOWLEDGE.git"
MP = Path("/home/z/my-project")

FICHIERS_CLES = [
    "skills/KNOWLEDGE.md",
    "skills/gen-plan/SKILL.md",
    "skills/correct-work/SKILL.md",
    "skills/skills-inventory/SKILL.md",
    "skills/@mon-ecosysteme/PROMPT-MAITRE-SHARED.md",
    "skills/@mon-ecosysteme/PROMPT-ULTRA-MAITRE-ORCHESTRATION.md",
    "skills/@mon-ecosysteme/SYNC-CONTEXT.md",
    "scripts/certification-complete.py",
    "scripts/ensure-installed.py",
]


def sh(cmd, cwd=None, env=None):
    return subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True, env=env)


def etat() -> dict:
    e = {"root_present": ROOT.exists(), "git_repo": False, "head": None,
         "fichiers_manquants": [], "kb_entrees": 0}
    if e["root_present"]:
        r = sh("git rev-parse --short HEAD", cwd=ROOT)
        e["git_repo"] = r.returncode == 0
        if e["git_repo"]:
            e["head"] = r.stdout.strip()
        for f in FICHIERS_CLES:
            if not (ROOT / f).exists():
                e["fichiers_manquants"].append(f)
        kb = ROOT / "skills/KNOWLEDGE.md"
        if kb.exists():
            e["kb_entrees"] = len([l for l in kb.read_text(encoding="utf-8", errors="replace").splitlines()
                                   if l.startswith("## ") and " v" in l])
    return e


def installe(e: dict) -> bool:
    return (e["root_present"] and e["git_repo"] and not e["fichiers_manquants"]
            and e["kb_entrees"] >= 14)


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "--check"
    e = etat()
    if mode == "--check":
        ok = installe(e)
        print(json.dumps({"verdict": "INSTALLE" if ok else "ABSENT-DERIVE", **e},
                         ensure_ascii=False))
        sys.exit(0 if ok else 1)

    if mode == "--reinstall":
        if installe(e):
            print("Déjà installé (HEAD %s) — no-op (idempotence D006)." % e["head"])
            sys.exit(0)
        if e["root_present"] and (not e["git_repo"] or e["fichiers_manquants"]):
            print(json.dumps({"verdict": "DERIVE", "diagnostic": e,
                              "action": "aucune action destructive automatique — "
                                        "réparation manuelle ou --force requise"},
                             ensure_ascii=False))
            sys.exit(2)
        # ABSENT → clone éphémère (jeton jamais persisté)
        env = dict(os.environ)
        tok = env.pop("GITHUB_TOKEN", None)
        url = (f"https://x-access-token:{tok}@github.com/bigleon2/KNOWLEDGE.git"
               if tok else ORIGIN)
        r = sh(f"git clone --quiet {url} {ROOT}")
        if r.returncode != 0:
            print(f"ECHEC clone (rc={r.returncode}) : {r.stderr.strip()[-300:]}")
            sys.exit(3)
        e2 = etat()
        ok = installe(e2)
        print(json.dumps({"verdict": "REINSTALLE-OK" if ok else "REINSTALLE-DERIVE", **e2},
                         ensure_ascii=False))
        try:
            wl = MP / "worklog.md"
            with open(wl, "a", encoding="utf-8") as f:
                f.write(f"\n> É1-INSTALL : réinstallation automatique exécutée (HEAD {e2.get('head')}) "
                        f"— jeton non persisté.\n")
        except Exception:
            pass
        sys.exit(0 if ok else 4)

    print(__doc__)
    sys.exit(64)


if __name__ == "__main__":
    main()
