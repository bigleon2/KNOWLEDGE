#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.13)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

# PROVENANCE: session web-f90062ce (2026-10-24) — SG7.4 Task B2 : port des références
# vives gen-plan v3.24.0 → v3.25.0 (5 skills — arbitre interactions, boucle E12-E13).
# Idempotent : rejeu = 0 substitution (les motifs v3.25.0 ne matchent plus v3.24.0).
"""Port des références vives gen-plan v3.24.0 → v3.25.0 (5 skills)."""
import sys

BASE = "/home/z/my-project/KNOWLEDGE-repo/skills"
# (skill, old, new) — chaque motif doit apparaître exactement 1 fois
SUBS = [
    ("context-engineering",
     "PM gen-plan v3.24.0 §1.9 (PM corpus antérieur toléré — garde R2)",
     "PM gen-plan v3.25.0 §1.9 (PM corpus antérieur toléré — garde R2)"),
    ("graph-engineering",
     "PM gen-plan v3.24.0 §1.9 (PM corpus antérieur toléré — garde R2)",
     "PM gen-plan v3.25.0 §1.9 (PM corpus antérieur toléré — garde R2)"),
    ("harness-engineering",
     "PM gen-plan v3.24.0 §1.9 (PM corpus antérieur toléré — garde R2)",
     "PM gen-plan v3.25.0 §1.9 (PM corpus antérieur toléré — garde R2)"),
    ("loop-engineering",
     "PM gen-plan v3.24.0 §1.9 (PM corpus antérieur toléré — garde R2)",
     "PM gen-plan v3.25.0 §1.9 (PM corpus antérieur toléré — garde R2)"),
    ("fleet-engineering",
     "- gen-plan v3.24.0 (SKILL.md) §1.9 PM/§1.6 — PM corpus antérieur toléré (garde R2)",
     "- gen-plan v3.25.0 (SKILL.md) §1.9 PM/§1.6 — PM corpus antérieur toléré (garde R2)"),
    ("memory-engineering",
     "- gen-plan v3.24.0 (SKILL.md) §1.9 PM/§1.6",
     "- gen-plan v3.25.0 (SKILL.md) §1.9 PM/§1.6"),
    ("spec-driven-development",
     "- gen-plan v3.24.0 (SKILL.md) §1.9 PM/§1.6",
     "- gen-plan v3.25.0 (SKILL.md) §1.9 PM/§1.6"),
    ("refactoring-engineering",
     "- gen-plan v3.24.0 (SKILL.md) §1.6 bloc n°55",
     "- gen-plan v3.25.0 (SKILL.md) §1.6 bloc n°55"),
    ("refactoring-test",
     "- gen-plan v3.24.0 (SKILL.md) §1.6 bloc n°55",
     "- gen-plan v3.25.0 (SKILL.md) §1.6 bloc n°55"),
]


def main():
    n = 0
    for skill, old, new in SUBS:
        p = f"{BASE}/{skill}/SKILL.md"
        t = open(p, encoding="utf-8").read()
        c = t.count(old)
        if c == 0:
            if t.count(new) >= 1:
                print(f"  [NO-OP] {skill} : déjà v3.25.0")
                continue
            print(f"  ABANDON {skill} : motif introuvable")
            sys.exit(2)
        if c != 1:
            print(f"  ABANDON {skill} : motif trouvé {c} fois (attendu 1)")
            sys.exit(2)
        open(p, "w", encoding="utf-8").write(t.replace(old, new))
        n += 1
        print(f"  [OK] {skill} : référence vive portée v3.25.0")
    print(f"substitutions : {n}")


if __name__ == "__main__":
    main()
