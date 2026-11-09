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
"""
Task 84 G3 — Sweep final de la cascade socle n°56 (2 compléments mesurés par
l'arbitre interactions — 1 WARN asymétrie + 1 FAIL citations vives STALE) :
  1. KB gen-plan « Dépend de » += agent-engineering >= v1.0.0 (mobilisation n°56
     désormais RÉELLE — déclarée à l'inscription socle ; asymétrie Task 83
     résolue dans le sens de la complétion, jamais la suppression).
  2. Sweep citations vives : 5 disciplines citent gen-plan v3.41.0 → v3.42.0
     (context/loop/graph/harness-engineering registre + fleet-engineering ligne).
Garde-fous : assert count==1 par fichier ; idempotence ; ABANDON rc=2 sans écriture.
"""
import sys
from pathlib import Path

R = Path("/home/z/my-project/KNOWLEDGE-repo")
KB = R / "skills/KNOWLEDGE.md"


def sub(text, old, new, label, n=1):
    c = text.count(old)
    if c != n:
        print("ABANDON : [%s] trouvé %d fois (attendu %d) : %r" % (label, c, n, old[:70]))
        sys.exit(2)
    return text.replace(old, new)


def main():
    # 1. KB gen-plan « Dépend de » += agent-engineering (mobilisation déclarée)
    k = KB.read_text(encoding="utf-8")
    if "agent-engineering >= v1.0.0 (mobilisation n°56" in k:
        print("[NO-OP] KB Dépend de gen-plan inclut déjà agent-engineering")
    else:
        k = sub(k, "refactor-guard >= v1.7.0 (garde-fous de refactoring — détection de besoins, hook E13, fusion discussion 468a4c26)",
                "refactor-guard >= v1.7.0 (garde-fous de refactoring — détection de besoins, hook E13, fusion discussion 468a4c26), "
                "agent-engineering >= v1.0.0 (mobilisation n°56 — §1.6/§3, orchestration des tâches ABE/AE/MASE, "
                "déclarée à l'inscription socle Task 84 G3)",
                "KB Dépend de gen-plan += n°56")
        KB.write_text(k, encoding="utf-8")
        print("KB : gen-plan « Dépend de » += agent-engineering >= v1.0.0 (mobilisation n°56)")

    # 2. Sweep citations vives des 5 disciplines (v3.41.0 → v3.42.0)
    cibles = [
        ("context-engineering", "PM gen-plan v3.41.0 §1.9", "PM gen-plan v3.42.0 §1.9"),
        ("loop-engineering", "PM gen-plan v3.41.0 §1.9", "PM gen-plan v3.42.0 §1.9"),
        ("graph-engineering", "PM gen-plan v3.41.0 §1.9", "PM gen-plan v3.42.0 §1.9"),
        ("harness-engineering", "PM gen-plan v3.41.0 §1.9", "PM gen-plan v3.42.0 §1.9"),
        ("fleet-engineering", "- gen-plan v3.41.0 (SKILL.md) §1.9 PM/§1.6",
         "- gen-plan v3.42.0 (SKILL.md) §1.9 PM/§1.6"),
        ("memory-engineering", "- gen-plan v3.41.0 (SKILL.md) §1.9 PM/§1.6",
         "- gen-plan v3.42.0 (SKILL.md) §1.9 PM/§1.6"),
        ("spec-driven-development", "- gen-plan v3.41.0 (SKILL.md) §1.9 PM/§1.6",
         "- gen-plan v3.42.0 (SKILL.md) §1.9 PM/§1.6"),
        ("refactoring-engineering", "- gen-plan v3.41.0 (SKILL.md) §1.6 bloc n°55",
         "- gen-plan v3.42.0 (SKILL.md) §1.6 bloc n°55"),
        ("refactoring-test", "- gen-plan v3.41.0 (SKILL.md) §1.6 bloc n°55",
         "- gen-plan v3.42.0 (SKILL.md) §1.6 bloc n°55"),
    ]
    for skill, old, new in cibles:
        p = R / "skills" / skill / "SKILL.md"
        t = p.read_text(encoding="utf-8")
        if new in t:
            print("[NO-OP] %s cite déjà gen-plan v3.42.0" % skill)
            continue
        t = sub(t, old, new, "citation %s" % skill)
        p.write_text(t, encoding="utf-8")
        print("%s : citation gen-plan v3.41.0 → v3.42.0" % skill)
    return 0


if __name__ == "__main__":
    sys.exit(main())
