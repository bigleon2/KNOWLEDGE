#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.11)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

# -*- coding: utf-8 -*-
"""Task 9 / G-RES-2b — Description Optimization refactoring-engineering v1.0.1→v1.1.0.

Protocole SHARED §7 (baseline A2 — dérive constatée → Description Optimization
OBLIGATOIRE) : la baseline A2 (scripts/task9-baseline-a2-n55.py) a détecté 1
dérive voie M sur le cas négatif « Renforce le harnais : profils ressource,
signaux de pression, gardes-fous. » — collision lexicale (`gard`+`fous` ↔
« Garde-fous mobilisés » de la description ; voie L 3/3 NON = conforme).

Reformulation (sémantique inchangée — refactor-guard demeure le garde-fou déclaré) :
  « Garde-fous mobilisés pendant les opérations : refactor-guard (...) »
  → « Sécurisation des opérations assurée par le skill refactor-guard (...) »

Éditions verrouillées (count==1) :
  1. skills/refactoring-engineering/SKILL.md  — phrase + version 1.1.0
  2. skills/KNOWLEDGE.md                      — heading + calibration Task 9
  3. scripts/check-ecosysteme-integrity.py    — ECO_SKILLS 1.1.0
  4. skills/@historique/historiques-par-skill/refactoring-engineering.md — ligne v1.1.0

Usage : python3 scripts/g2b-description-optimization.py [--dry-run]
"""
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRY = "--dry-run" in sys.argv


def abandon(msg, code=2):
    print("ABANDON : %s" % msg)
    sys.exit(code)


def apply(path_rel, edits):
    path = os.path.join(BASE, path_rel)
    with open(path, encoding="utf-8") as f:
        t = f.read()
    for old, new, n, label in edits:
        c = t.count(old)
        if c != n:
            abandon("[%s] motif [%s] trouvé %d fois (attendu %d) : %r"
                    % (path_rel, label, c, n, old[:70]))
        t = t.replace(old, new)
    if DRY:
        print("[DRY-RUN] %s : %d édition(s) OK" % (path_rel, len(edits)))
        return
    with open(path, "w", encoding="utf-8") as f:
        f.write(t)
    print("[OK] %s : %d édition(s)" % (path_rel, len(edits)))


OLD_PHRASE = ("Garde-fous mobilisés pendant les opérations : refactor-guard "
              "(score de risque H01-H15, sandbox, échelle rollout — fusion "
              "discussion 468a4c26, lignée externe v1.7.0).")
NEW_PHRASE = ("Sécurisation des opérations assurée par le skill refactor-guard "
              "(score de risque H01-H15, sandbox, échelle rollout — fusion "
              "discussion 468a4c26, lignée externe v1.7.0).")

apply("skills/refactoring-engineering/SKILL.md", [
    (OLD_PHRASE, NEW_PHRASE, 1, "description A2"),
    ("version: 1.0.1", "version: 1.1.0", 1, "version frontmatter"),
])

apply("skills/KNOWLEDGE.md", [
    ("## refactoring-engineering v1.0.1", "## refactoring-engineering v1.1.0", 1, "heading"),
    ("précédente : v1.0.0 (Task 7 — matérialisation n°55, recherche web approfondie, baseline A2 en attente QUOTA_OK)",
     "précédente : v1.0.0 (Task 7 — matérialisation n°55, recherche web approfondie) ; Task 9 (2026-10-12, session web-b4d7dd19 — gen-plan(step), QUOTA_OK levé) : baselines A2 MESURÉES (scripts/task9-baseline-a2-n55.py, méthode SHARED §7 v2 — voie M mécanique + voie L 3 runs) : voie L 7/7 conforme (3/3 unanimes par cas), voie M 6/7 — 1 dérive sur le cas négatif « Renforce le harnais… gardes-fous » (collision lexicale gard+fous ↔ description) → Description Optimization v1.1.0 (protocole SHARED §7) : « Garde-fous mobilisés pendant les opérations » → « Sécurisation des opérations assurée par le skill refactor-guard » (sémantique inchangée) ; re-mesure voie M 7/7 — 0 dérive ×2 voies",
     1, "calibration"),
])

apply("scripts/check-ecosysteme-integrity.py", [
    ('    "refactoring-engineering": "1.0.1",  # n°55 (session web-b4d7dd19, 2026-10-12) : Task 8 — seule discipline de refactoring, outil refactoring-test, garde-fous refactor-guard',
     '    "refactoring-engineering": "1.1.0",  # n°55 — Task 9 (2026-10-12) : Description Optimization A2 (dérive voie M résorbée, re-mesure 7/7) ; Task 8 : seule discipline de refactoring, outil refactoring-test',
     1, "ECO_SKILLS"),
])

apply("skills/@historique/historiques-par-skill/refactoring-engineering.md", [
    ("| v1.0.1 | 2026-10-12 | Task 8 (gen-plan(step), session web-b4d7dd19, fusion discussion externe 468a4c26)",
     "| v1.1.0 | 2026-10-12 | Task 9 (gen-plan(step), session web-b4d7dd19 — QUOTA_OK levé) : Description Optimization A2 (protocole SHARED §7 — dérive voie M constatée → optimisation obligatoire) : baselines A2 mesurées (scripts/task9-baseline-a2-n55.py) — voie L 7/7 (3 runs unanimes), voie M 6/7 (1 dérive, cas négatif « gardes-fous » : collision lexicale gard+fous) ; reformulation description « Garde-fous mobilisés pendant les opérations » → « Sécurisation des opérations assurée par le skill refactor-guard » (sémantique inchangée) ; re-mesure voie M 7/7 — 0 dérive ×2 voies |\n"
     "| v1.0.1 | 2026-10-12 | Task 8 (gen-plan(step), session web-b4d7dd19, fusion discussion externe 468a4c26)",
     1, "ligne v1.1.0"),
])

print("\nDescription Optimization v1.1.0 %s." % ("validée (dry-run)" if DRY else "écrite"))
