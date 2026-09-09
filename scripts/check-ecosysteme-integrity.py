#!/usr/bin/env python3
"""Intégrité de l'écosystème Knowledge installé dans ce projet.

Vérifications (pipeline PM-INSTALL étapes 1-2, 8) :
  1. SHA-256 des 14 fichiers du corpus canonique skills/@mon-ecosysteme/
  2. Byte-identité du miroir skills/_prompts-maitres/ (14 fichiers)
  3. Synchronisation download/ (6 fichiers du SYNC_MAP — extension B3 : PM v3.11.0)
  4. Structure des 11 skills écosystème + 3 skills métier installés
  5. Cohérence versions SKILL.md ↔ registre KNOWLEDGE.md

Usage :
    python3 scripts/check-ecosysteme-integrity.py            # vérification + manifeste
    python3 scripts/check-ecosysteme-integrity.py --check    # vérification seule
"""

import hashlib
import json
import os
import re
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPUS = os.path.join(BASE_DIR, "skills", "@mon-ecosysteme")
MIRROR = os.path.join(BASE_DIR, "skills", "_prompts-maitres")
DOWNLOAD = os.path.join(BASE_DIR, "download")
SKILLS = os.path.join(BASE_DIR, "skills")
KB = os.path.join(SKILLS, "KNOWLEDGE.md")
MANIFEST = os.path.join(BASE_DIR, "scripts", "ecosysteme-integrity.json")

ECO_SKILLS = {
    "gen-plan": "3.11.0",
    "correct-work": "2.5.1",
    "clone-chat": "2.0.0",
    "skills-inventory": "1.0.0",
    "skill-creator": "1.0.0",
    "autonomous-agent": "1.0.0",
    "agent-prompt-engineering": "1.0.1",
    "context-engineering": "1.0.1",
    "loop-engineering": "1.0.1",
    "graph-engineering": "1.0.1",
    "harness-engineering": "1.0.1",
}
# Skills dont la version est déclarée uniquement dans le registre KB
# (skill-creator = forme plateforme adoptée par l'écosystème, byte-identique au dépôt)
KB_ONLY_VERSION = {"skill-creator"}
METIER_SKILLS = ["audio-metadata", "cpp-analysis", "pdf-llm"]
SYNC_MAP = [
    "PROMPT-MAITRE-SHARED.md",
    "PROMPT-MAITRE-GEN-PLAN-v3.6.1.md",
    "PROMPT-MAITRE-GEN-PLAN-v3.11.0.md",
    "PROMPT-MAITRE-CORRECT-WORK-v2.4.0.md",
    "PROMPT-MAITRE-CLONE-CHAT-v2.0.0.md",
    "README.md",
]

results = []


def check(name, passed, detail=""):
    results.append((name, bool(passed), detail))
    print(f"  [{'PASS' if passed else 'FAIL'}] {name}{(' — ' + detail) if detail else ''}")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    write_manifest = "--check" not in sys.argv
    manifest = {"corpus": {}, "mirror": {}, "download": {}, "skills": {}}

    print("=== 1. Corpus canonique @mon-ecosysteme (SHA-256) ===")
    corpus_files = sorted(os.listdir(CORPUS)) if os.path.isdir(CORPUS) else []
    check("15 fichiers présents", len(corpus_files) == 15, f"{len(corpus_files)} fichiers")
    for fname in corpus_files:
        digest = sha256(os.path.join(CORPUS, fname))
        manifest["corpus"][fname] = digest

    print("\n=== 2. Miroir _prompts-maitres (byte-identité) ===")
    ok = True
    for fname in corpus_files:
        m = os.path.join(MIRROR, fname)
        if not os.path.isfile(m):
            ok = False
            break
        manifest["mirror"][fname] = sha256(m)
        if manifest["mirror"][fname] != manifest["corpus"][fname]:
            ok = False
    check("Miroir byte-identique", ok, f"{len(manifest['mirror'])}/{len(corpus_files)}")

    print("\n=== 3. Synchronisation download/ ===")
    for fname in SYNC_MAP:
        d = os.path.join(DOWNLOAD, fname)
        c = os.path.join(CORPUS, fname)
        if os.path.isfile(d) and os.path.isfile(c):
            digest = sha256(d)
            manifest["download"][fname] = digest
            check(f"sync {fname}", digest == manifest["corpus"].get(fname))
        else:
            check(f"sync {fname}", False, "fichier manquant")

    print("\n=== 4. Skills écosystème installés ===")
    for skill, expected_ver in ECO_SKILLS.items():
        sp = os.path.join(SKILLS, skill, "SKILL.md")
        if not os.path.isfile(sp):
            check(f"{skill}", False, "SKILL.md manquant")
            continue
        with open(sp, encoding="utf-8") as f:
            content = f.read()
        m = re.search(r"^version:\s*[\"']?([\d.]+)", content, re.MULTILINE)
        ver = m.group(1) if m else None
        manifest["skills"][skill] = {"version": ver or "KB", "sha256": sha256(sp)}
        if skill in KB_ONLY_VERSION:
            check(f"{skill} (version KB-only)", ver is None, "forme plateforme adoptée")
        else:
            check(f"{skill} v{ver}", ver == expected_ver, f"attendu v{expected_ver}")

    print("\n=== 4bis. Skills métier installés ===")
    for skill in METIER_SKILLS:
        sp = os.path.join(SKILLS, skill, "SKILL.md")
        check(f"{skill}", os.path.isfile(sp))

    print("\n=== 5. Cohérence registre KNOWLEDGE.md ===")
    if os.path.isfile(KB):
        with open(KB, encoding="utf-8") as f:
            kb = f.read()
        entries = re.findall(r"^## ([\w-]+) v([\d.]+)", kb, re.MULTILINE)
        check("11 entrées KB", len(entries) == 11, f"{len(entries)} entrées")
        for skill, expected_ver in ECO_SKILLS.items():
            match = [e for e in entries if e[0] == skill]
            check(f"KB {skill}", bool(match) and match[0][1] == expected_ver,
                  f"KB={match[0][1] if match else 'absent'} / attendu={expected_ver}")
    else:
        check("Registre KB", False, "KNOWLEDGE.md manquant")

    n_pass = sum(1 for _, p, _ in results if p)
    n_fail = len(results) - n_pass
    print(f"\n=== RESUME : {n_pass}/{len(results)} PASS, {n_fail} FAIL ===")

    if write_manifest and n_fail == 0:
        with open(MANIFEST, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False, sort_keys=True)
        print(f"Manifeste écrit : {MANIFEST}")
    elif write_manifest:
        print("Manifeste NON écrit (échecs détectés)")

    sys.exit(1 if n_fail else 0)


if __name__ == "__main__":
    main()
