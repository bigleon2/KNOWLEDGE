#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.11)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

# -*- coding: utf-8 -*-
"""Task 9 / G-RES-1 — Recalibrage KO-L004 du harnais task17 (guidé arbitre, 3 FAIL).

C01/C04 : SHARED v1.7.4 → v1.7.5 (bump D009) — C12 : corpus 8 → 9 (PM REFACTOR-GUARD).
Substitutions verrouillées (count==1) — idempotent (re-exécution = NO-OP).
"""
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(BASE, "scripts", "task17-answer-key-check.py")
DRY = "--dry-run" in sys.argv

EDITS = [
    ('check("C01 SHARED v1.7.4 — §1.2 codifie @historique (R4, git mv, KO-L004)",\n'
     '          "**Version** : 1.7.4" in shared',
     'check("C01 SHARED v1.7.5 — §1.2 codifie @historique (R4, git mv, KO-L004)",\n'
     '          "**Version** : 1.7.5" in shared', 1, "C01"),
    ('"Idempotence v2" in prop and "SHARED v1.7.4" in prop and "@historique/" in prop)',
     '"Idempotence v2" in prop and "SHARED v1.7.5" in prop and "@historique/" in prop)',
     1, "C04"),
    ('check("C12 integrity : corpus 8/8 SHA vives alignées sur le manifeste",\n'
     '          len(integ["corpus"]) == 8 and not divergents, str(divergents))',
     'check("C12 integrity : corpus 9/9 SHA vives alignées sur le manifeste",\n'
     '          len(integ["corpus"]) == 9 and not divergents, str(divergents))',
     1, "C12"),
]


def abandon(msg, code=2):
    print("ABANDON : %s" % msg)
    sys.exit(code)


with open(PATH, encoding="utf-8") as f:
    t = f.read()
for old, new, n, label in EDITS:
    c = t.count(old)
    if c != n:
        abandon("motif [%s] trouvé %d fois (attendu %d)" % (label, c, n))
    t = t.replace(old, new)
if DRY:
    print("[DRY-RUN] 3 recalibrages validés")
else:
    with open(PATH, "w", encoding="utf-8") as f:
        f.write(t)
    print("[OK] task17 recalibré (C01/C04 v1.7.5, C12 corpus 9)")
