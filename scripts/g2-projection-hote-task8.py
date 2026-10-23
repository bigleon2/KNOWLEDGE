#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.10)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

# -*- coding: utf-8 -*-
"""Task 8 G2-a — Projection hôte (byte-identité) du périmètre cascade v3.23.1.

Politique Task 4/7 : périmètre = fichiers skills/ modifiés côté canonique (git status)
; exclusions permanentes R2 : version-management (homonymie confirmée Task 6 G8 —
JAMAIS écraser), frontière vendeur/plateforme hors git.
"""
import hashlib
import json
import os
import subprocess

SRC = "/home/z/my-project/KNOWLEDGE/skills"
DST = "/home/z/my-project/skills"
EXCLUSIONS_PERMANENTES = {"version-management"}  # R2 — homonymie réelle (Task 6 G8)
MANIFEST = "/home/z/my-project/scripts/projection-hote-task8-manifest.json"


def sha256(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main():
    r = subprocess.run(["git", "status", "--porcelain"], cwd="/home/z/my-project/KNOWLEDGE",
                       capture_output=True, text=True)
    paths = []
    for line in r.stdout.splitlines():
        code, path = line[:2], line[3:].strip()
        if not path.startswith("skills/"):
            continue
        if code.startswith("??") and path.endswith("/"):
            # dossier non suivi (refactor-guard/) : prendre tous ses fichiers
            base = path.rstrip("/")
            out = subprocess.run(["git", "ls-files", "--others", "--exclude-standard", base],
                                 cwd="/home/z/my-project/KNOWLEDGE", capture_output=True, text=True)
            for f in out.stdout.splitlines():
                paths.append(f[len("skills/"):])
            continue
        if path.endswith("/"):
            continue
        rel = path[len("skills/"):]
        top = rel.split("/")[0]
        if top in EXCLUSIONS_PERMANENTES:
            print("  [EXCLU-R2] %s (homonymie — jamais écraser)" % top)
            continue
        if code.strip() == "D" or code.startswith("D"):
            # retrait : supprimer côté hôte si présent
            dst = os.path.join(DST, rel)
            if os.path.isfile(dst):
                os.remove(dst)
                print("  [RETRAIT] %s" % rel)
            continue
        paths.append(rel)
    paths = sorted(set(paths))
    print("Périmètre : %d fichier(s)" % len(paths))
    entries, copied, synced = [], 0, 0
    for rel in paths:
        s, d = os.path.join(SRC, rel), os.path.join(DST, rel)
        if not os.path.isfile(s):
            print("  [SKIP] %s (absent canonique)" % rel)
            continue
        os.makedirs(os.path.dirname(d), exist_ok=True)
        hs, hd = sha256(s), (sha256(d) if os.path.isfile(d) else None)
        if hs == hd:
            synced += 1
            status = "IDENTIQUE"
        else:
            with open(s, "rb") as fi, open(d, "wb") as fo:
                fo.write(fi.read())
            copied += 1
            status = "COPIE" if hd else "NOUVEAU"
        entries.append({"path": rel, "status": status, "sha256": hs})
    with open(MANIFEST, "w", encoding="utf-8") as f:
        json.dump({"task": "8", "cascade": "gen-plan v3.23.1 (fusion 468a4c26 + correction outil n°55)",
                   "exclusions": sorted(EXCLUSIONS_PERMANENTES),
                   "fichiers": entries}, f, ensure_ascii=False, indent=1)
    print("Projection : %d copies/nouveaux, %d déjà identiques — manifeste %s" % (copied, synced, MANIFEST))
    # Post-checks hôte
    print("— Post-checks hôte")
    checks = [
        ("gen-plan hôte v3.23.1", "gen-plan/SKILL.md", "version: 3.23.1"),
        ("ref-test hôte = outil v1.0.1", "refactoring-test/SKILL.md", "Skill outil refactoring test"),
        ("ref-eng hôte v1.0.1", "refactoring-engineering/SKILL.md", "version: 1.0.1"),
        ("ref-guard hôte v1.7.0", "refactor-guard/SKILL.md", "version: 1.7.0"),
        ("KB hôte 32 entrées", "KNOWLEDGE.md", "## refactor-guard v1.7.0"),
        ("corpus hôte PM v3.23.1", "@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.23.1.md", "v3.23.1"),
        ("SHARED hôte v1.7.4", "@mon-ecosysteme/PROMPT-MAITRE-SHARED.md", "**Version** : 1.7.4"),
        ("SYNC hôte v1.4.7", "@mon-ecosysteme/SYNC-CONTEXT.md", "> **Version** : 1.4.7"),
        ("fullstack-dev hôte déquoté", "fullstack-dev/SKILL.md", "version: 1.0.0"),
        ("§0 v1.7.4 propagé (ref-eng)", "refactoring-engineering/SKILL.md", "SHARED v1.7.4"),
        ("historique par-skill ref-guard", "@historique/historiques-par-skill/refactor-guard.md", "CONVERGENCE de la lignée externe"),
        ("corpus hôte 8 fichiers", "@mon-ecosysteme/README.md", "Révision v2.1.5"),
    ]
    ok = 0
    for label, rel, needle in checks:
        p = os.path.join(DST, rel)
        found = os.path.isfile(p) and needle in open(p, encoding="utf-8").read()
        print("  [%s] %s" % ("PASS" if found else "FAIL", label))
        ok += found
    print("Post-checks : %d/%d" % (ok, len(checks)))
    if ok != len(checks):
        raise SystemExit("POST-CHECKS INCOMPLETS")
    print("=== Projection hôte OK ===")


if __name__ == "__main__":
    main()
