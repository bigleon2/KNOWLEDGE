#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.37)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).
"""

# -*- coding: utf-8 -*-
"""Task 79 G2 — Finalisation du plan : D005/D006 verified + G2 TERMINÉ."""
import sys
from pathlib import Path

R = Path("/home/z/my-project/KNOWLEDGE-repo")
PLAN = R / "download/plan-task79-recuration-vm-task74-go-cw-bloc-push.md"

t = PLAN.read_text(encoding="utf-8")


def sub(old, new, label, n=1):
    global t
    c = t.count(old)
    if c != n:
        print("ABANDON : [%s] trouvé %d fois" % (label, c))
        sys.exit(2)
    t = t.replace(old, new)


for did in ("D005", "D006"):
    anchor = '  - id: "%s"\n' % did
    idx = t.find(anchor)
    if idx < 0:
        print("ABANDON : %s introuvable" % did)
        sys.exit(2)
    end = t.find('  - id: "D', idx + 10)
    bloc = t[idx:end]
    if 'status: "pending"' not in bloc:
        print("ABANDON : %s sans pending" % did)
        sys.exit(2)
    t = t[:idx] + bloc.replace('status: "pending"', 'status: "verified"') + t[end:]

sub("## G2 — Re-curation version-management (protocole P0-P7) `[À FAIRE]` (0/3)",
    "## G2 — Re-curation version-management (protocole P0-P7) `[TERMINÉ]` (3/3)", "G2")
sub("**G1 Task 78 sondage borné `[À FAIRE]` 0/3 · G2 re-curation version-management `[À FAIRE]` 0/3",
    "**G1 Task 78 sondage borné ✅ 3/3 · G2 re-curation version-management ✅ 3/3",
    "PLAN-AFFICHE compteurs")

PLAN.write_text(t, encoding="utf-8")
print("Plan Task 79 : D005 + D006 verified, G2 TERMINÉ")
