#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.6.8)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

"""Collecteur d'audit de provenance (skill audit-provenance v1.0.0 — N27).

Scan les artefacts de l'ecosysteme (skills, scripts, corpus, rapports, plans),
deduit leur provenance par heuristique declarative (§2 SKILL.md), et liste les
orphelins. En mode --fix, insere un en-tete `# PROVENANCE: ...` dans les scripts
Python orphelins (garde par marqueur — idempotent x2, GF-2).

Sortie JSON deterministe sur stdout ; code retour 0 (succes), 2 (erreur).
Rapport persiste sous tmp/b13r5-install/ (R9 — session B13-r6, directive
trace 1a0df36f356c3add).
"""
import argparse
import hashlib
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(BASE, "skills")
SCRIPTS = os.path.join(BASE, "scripts")
CORPUS = os.path.join(SKILLS, "@mon-ecosysteme")
DOWNLOAD = os.path.join(BASE, "download")
REPORT = os.path.join(BASE, "tmp", "b13r5-install", "rapport-audit-provenance.json")

PROVENANCE_LINE = (
    "# PROVENANCE: session B13-r6 (N27) — audit-provenance v1.0.0, "
    "directive trace 1a0df36f356c3add ; artefact orphelin documente idempotemment"
)

MARKERS = [
    "Provenance", "provenance", "PROVENANCE:", "PATTERN:", "SYNC-CONTEXT",
    "reconstitu", "restaur", "assembl", "calibr", "pingl", "wip", "wipe",
    "directive", "trace", "session B1", "B13", "B12", "B11", "N2", "N1",
]


def scan_file(path):
    """Retourne True si le fichier contient au moins un marqueur de provenance."""
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            content = f.read()
    except OSError:
        return False
    return any(m in content for m in MARKERS)


def ecosystem_skills():
    """Extrait dynamiquement la liste des skills ecosysteme (ECO_SKILLS de integrity)."""
    cei = os.path.join(SCRIPTS, "check-ecosysteme-integrity.py")
    try:
        with open(cei, encoding="utf-8") as f:
            src = f.read()
    except OSError:
        return []
    m = re.search(r"ECO_SKILLS\s*=\s*\{(.*?)\}", src, re.S)
    if not m:
        return []
    return re.findall(r'"([a-z0-9-]+)":\s*"[\d.]+"', m.group(1))


def collect_paths():
    """Delimite le perimetre d'audit (etape 1 §1.2) — perimetre ECOSYSTEME strict.

    Couvre : KB, corpus, prompts maitres, artefacts des skills ecosysteme
    (SKILL.md, evals/, references/, data/), scripts top-level (.py/.sh),
    plans et rapports download/*.md. Les skills plateforme tiers (hors
    ECO_SKILLS) sont exclus — hors de l'ecosysteme Knowledge.
    """
    paths = []
    eco = ecosystem_skills()
    for skill in eco:
        base = os.path.join(SKILLS, skill)
        if not os.path.isdir(base):
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            if os.path.basename(dirpath) in ("_archive", "__pycache__"):
                dirnames[:] = []
                continue
            for fn in filenames:
                if fn.endswith((".md", ".py", ".json")):
                    paths.append(os.path.join(dirpath, fn))
    for extra in (os.path.join(SKILLS, "KNOWLEDGE.md"),):
        paths.append(extra)
    for root in (CORPUS,):
        if os.path.isdir(root):
            for dirpath, _d, filenames in os.walk(root):
                for fn in filenames:
                    if fn.endswith((".md", ".json")):
                        paths.append(os.path.join(dirpath, fn))
    for fn in sorted(os.listdir(SCRIPTS)):
        if fn.endswith((".py", ".sh")):
            p = os.path.join(SCRIPTS, fn)
            if os.path.isfile(p):
                paths.append(p)
    if os.path.isdir(DOWNLOAD):
        for fn in sorted(os.listdir(DOWNLOAD)):
            if fn.endswith(".md"):
                paths.append(os.path.join(DOWNLOAD, fn))
    return sorted(set(paths))


def fix_python(path):
    """Insere l'en-tete PROVENANCE dans un script Python orphelin (syntaxe-safe).

    Retourne True si le fichier a ete modifie (garde par marqueur — idempotent).
    """
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()
    if any("PROVENANCE:" in line for line in lines[:20]):
        return False
    insert_at = 1 if lines and lines[0].startswith("#!") else 0
    lines.insert(insert_at, PROVENANCE_LINE + "\n")
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    return True


def main():
    """Point d'entree : audit (et correction optionnelle) de provenance."""
    parser = argparse.ArgumentParser(description="Audit de provenance")
    parser.add_argument("--fix", action="store_true",
                        help="insere les en-tetes manquants (scripts Python)")
    parser.add_argument("--report", default=REPORT, help="chemin du rapport JSON")
    args = parser.parse_args()

    paths = collect_paths()
    with_prov, orphans, fixed = [], [], []
    for path in paths:
        rel = os.path.relpath(path, BASE)
        if scan_file(path):
            with_prov.append(rel)
        else:
            orphans.append(rel)
            if args.fix and path.endswith(".py") and fix_python(path):
                fixed.append(rel)
    post_fix_orphans = [os.path.relpath(p, BASE) for p in paths
                        if not scan_file(p)]
    payload = {
        "n_scanned": len(paths),
        "with_provenance": len(with_prov),
        "orphans": post_fix_orphans,
        "n_fixed_this_run": len(fixed),
        "fixed_files": fixed,
        "markers_used": MARKERS,
        "mode": "fix" if args.fix else "audit",
        "sha16": hashlib.sha256(
            json.dumps(post_fix_orphans, ensure_ascii=False).encode("utf-8")
        ).hexdigest()[:16],
    }
    os.makedirs(os.path.dirname(args.report), exist_ok=True)
    with open(args.report, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
