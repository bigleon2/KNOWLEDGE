# PROVENANCE: session du 2026-10-01 (C3) — recommandation C3 du rapport de simulation @68ff91d ;
# arbitre cree par script-creator (R9, idempotence x2, GF-3) pour mecaniser le controle
# registre KNOWLEDGE.md <-> repertoires skills/ jusqu'ici dependant de la discipline E15.
#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.6.8)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.

verify-registry-sync.py — Arbitre de synchronisation registre ↔ répertoires (C3).

Compare les entrées du registre KB (skills/KNOWLEDGE.md, format « ## [nom] vX.Y.Z »)
aux répertoires de skills effectivement présents sous skills/ (dotés d'un SKILL.md).
Signale :
  GAPS    — répertoire présent sous skills/ mais absent du registre
            (création non matérialisée : protocole gen-plan E15 non passé) ;
  GHOSTS  — entrée du registre sans répertoire correspondant
            (skill retirée ou checkout partiel — à trancher selon le contexte).

Idempotent ×2 (lecture seule) ; sorties déterministes ; sensibilité à la casse
désactivée pour la comparaison des noms (convention kebab-case SHARED §1.2).

Usage :
    python3 scripts/verify-registry-sync.py
    python3 skills/correct-work/...            # (aucun rapport avec ce script)
    python3 scripts/verify-registry-sync.py --kb-path skills/KNOWLEDGE.md

Sortie : rapport lisible + bloc JSON ; code retour 0 = synchronisé, 1 = écarts, 2 = erreur.
"""
import argparse
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENTRY_RE = re.compile(r"^##\s+([A-Za-z0-9@_.-]+)\s+v(\d+\.\d+\.\d+)\s*$", re.MULTILINE)


def read_registry(kb_path):
    """Retourne {nom_normalise: (nom_source, version)} depuis le registre KB."""
    try:
        with open(kb_path, "r", encoding="utf-8", errors="replace") as fh:
            text = fh.read()
    except OSError:
        return None
    entries = {}
    for m in ENTRY_RE.finditer(text):
        name = m.group(1).strip().lower()
        entries.setdefault(name, (m.group(1), m.group(2)))
    return entries


def scan_skills(skills_root):
    """Retourne la liste triée des répertoires de skills dotés d'un SKILL.md."""
    found = []
    if not os.path.isdir(skills_root):
        return None
    for entry in sorted(os.listdir(skills_root)):
        d = os.path.join(skills_root, entry)
        if os.path.isdir(d) and not os.path.islink(d) and os.path.isfile(os.path.join(d, "SKILL.md")):
            found.append(entry)
    return found


def main():
    parser = argparse.ArgumentParser(description="Arbitre registre KNOWLEDGE.md <-> skills/ (C3)")
    parser.add_argument("--kb-path", default=os.path.join(BASE, "skills", "KNOWLEDGE.md"))
    parser.add_argument("--skills-root", default=os.path.join(BASE, "skills"))
    args = parser.parse_args()

    registry = read_registry(args.kb_path)
    if registry is None:
        print(f"ERREUR : registre introuvable : {args.kb_path}", file=sys.stderr)
        return 2
    skills = scan_skills(args.skills_root)
    if skills is None:
        print(f"ERREUR : racine skills introuvable : {args.skills_root}", file=sys.stderr)
        return 2

    reg_names = set(registry.keys())
    dir_names = {s.strip().lower() for s in skills}

    gaps = sorted(dir_names - reg_names)
    ghosts = sorted(reg_names - dir_names)
    synced = sorted(dir_names & reg_names)

    print("=== Arbitre verify-registry-sync (C3) ===")
    print(f"  Registre KB  : {args.kb_path} ({len(registry)} entrées)")
    print(f"  Racine skills: {args.skills_root} ({len(skills)} répertoires)")
    print(f"  Synchronisés : {len(synced)}")
    if gaps:
        print(f"\n  [GAP] présents sur disque, absents du registre ({len(gaps)}) :")
        for g in gaps:
            print(f"    - {g}")
    if ghosts:
        print(f"\n  [GHOST] au registre, absents du disque ({len(ghosts)}) :")
        for g in ghosts:
            print(f"    - {registry[g][0]} v{registry[g][1]}")
    if not gaps and not ghosts:
        print("\n  ✅ Synchronisation parfaite registre <-> répertoires")

    report = {
        "script": "verify-registry-sync",
        "kb_path": args.kb_path,
        "skills_root": args.skills_root,
        "registre_entrees": len(registry),
        "repertoires_skills": len(skills),
        "synchronises": synced,
        "gaps": gaps,
        "ghosts": sorted(registry[g][0] for g in ghosts),
        "verdict": "SYNC" if not gaps and not ghosts else "ECARTS",
    }
    print("\n" + json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not gaps and not ghosts else 1


if __name__ == "__main__":
    sys.exit(main())
