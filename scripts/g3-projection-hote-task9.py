#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.6)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

# -*- coding: utf-8 -*-
"""Task 9 / G3-pré + G4 — Projection hôte (byte-identité) — périmètre Task 9.

DÉCOUVERTE G3 : PURGE PLATEFORME de l'arbre hôte entre les sessions — 15 fichiers
projetés Task 8 disparus de /home/z/my-project/skills/ (@mon-ecosysteme/ ×7,
@historique/ ×6, KNOWLEDGE.md, gen-plan/SKILL.md, correct-work/SKILL.md — les
dossiers gen-plan/ et correct-work/ hôtes sont VIDÉS). Finding S2 (précédent
Task 4 F4 : « skills/ hôte = arbre réellement chargé par la plateforme »).

Périmètre = UNION de :
  (a) git status skills/ (modifications + nouveautés de la session Task 9) ;
  (b) les 127 chemins du manifeste Task 8 (remédiation purge + idempotence) ;
  (c) nouveautés non suivies sous skills/ (PM REFACTOR-GUARD v1.7.0).

Exclusions permanentes R2 : version-management (homonymie confirmée Task 6 G8 —
JAMAIS écraser). Manifeste : /home/z/my-project/scripts/projection-hote-task9-manifest.json
"""
import hashlib
import json
import os
import subprocess

SRC = "/home/z/my-project/KNOWLEDGE/skills"
DST = "/home/z/my-project/skills"
EXCLUSIONS_PERMANENTES = {"version-management"}  # R2 — homonymie réelle (Task 6 G8)
MANIFEST = "/home/z/my-project/scripts/projection-hote-task9-manifest.json"
MANIFEST_T8 = "/home/z/my-project/scripts/projection-hote-task8-manifest.json"


def sha256(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main():
    paths = set()

    # (a) git status — modifications de session
    r = subprocess.run(["git", "status", "--porcelain"], cwd="/home/z/my-project/KNOWLEDGE",
                       capture_output=True, text=True)
    for line in r.stdout.splitlines():
        code, path = line[:2], line[3:].strip()
        if not path.startswith("skills/"):
            continue
        if code.startswith("??") and path.endswith("/"):
            base = path.rstrip("/")
            out = subprocess.run(["git", "ls-files", "--others", "--exclude-standard", base],
                                 cwd="/home/z/my-project/KNOWLEDGE", capture_output=True, text=True)
            for f in out.stdout.splitlines():
                paths.add(f[len("skills/"):])
            continue
        if path.endswith("/"):
            continue
        rel = path[len("skills/"):]
        if rel.split("/")[0] in EXCLUSIONS_PERMANENTES:
            print("  [EXCLU-R2] %s (homonymie — jamais écraser)" % rel)
            continue
        paths.add(rel)

    # (b) remédiation purge — chemins du manifeste Task 8
    try:
        with open(MANIFEST_T8, encoding="utf-8") as f:
            for e in json.load(f).get("fichiers", []):
                rel = e.get("path")
                if rel and rel.split("/")[0] not in EXCLUSIONS_PERMANENTES:
                    paths.add(rel)
    except FileNotFoundError:
        print("  [WARN] manifeste Task 8 absent — remédiation purge limitée")

    paths = sorted(paths)
    print("Périmètre : %d fichier(s)" % len(paths))
    entries, copied, synced, absent = [], 0, 0, 0
    for rel in paths:
        s, d = os.path.join(SRC, rel), os.path.join(DST, rel)
        if not os.path.isfile(s):
            absent += 1
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

    # Post-checks ×2 : re-vérification byte-identité complète
    ok2 = 0
    for e in entries:
        if sha256(os.path.join(SRC, e["path"])) == sha256(os.path.join(DST, e["path"])):
            ok2 += 1
    manifest = {"task": "Task 9 — projection hôte (remédiation purge plateforme + session G-RES-1/G-RES-2)",
                "exclusions": sorted(EXCLUSIONS_PERMANENTES),
                "fichiers": entries,
                "post_checks": {"perimetre": len(paths), "copies": copied, "identiques": synced,
                                "absents_canonique": absent, "byte_identite_pass2": ok2}}
    with open(MANIFEST, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print("Copies : %d | Identiques : %d | Absents canonique : %d | Post-check ×2 : %d/%d"
          % (copied, synced, absent, ok2, len(entries)))
    purge = [e["path"] for e in entries
             if not os.path.exists(os.path.join(os.path.dirname(MANIFEST_T8), "..", "skills", e["path"]))]
    print("Manifeste : %s" % MANIFEST)
    if ok2 != len(entries):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
