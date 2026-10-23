#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.11)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

# -*- coding: utf-8 -*-
"""Task 9 / G-RES-1 — Extensions verrouillées de la décision D009 (gen-plan step).

Décision propriétaire D009 (2026-10-12, session web-b4d7dd19) :
  (a) les PMs de la lignée externe refactor-guard (v1.3.0→v1.7.0, discussion
      468a4c26) sont ACCEPTÉS non portés (non verbatim — provenance R4) ;
  (b) extension `scripts/generer-pm-skill.py` 3→4 familles (refactor-guard) ;
  (c) PM canonique PROMPT-MAITRE-REFACTOR-GUARD-v1.7.0 au corpus (bootstrap —
      script g1-bootstrap-pm-refactor-guard.py, à exécuter AVANT le présent
      script pour l'ordre de dépendance narratif ; les deux sont indépendants).

Éditions verrouillées (méthode B1 — ABANDON sans écriture si count != n) :
  1. generer-pm-skill.py      — docstring + FAMILLES (4e famille)
  2. PROMPT-MAITRE-INSTALL    — note §1, §2quater 3→4, §2ter +1 ligne + note,
                                Version 1.6.4→1.6.5, historique v1.6.5
  3. PROMPT-MAITRE-SHARED     — Version 1.7.4→1.7.5, Révision v1.7.5, §6.1
                                (+1 ligne REFACTOR-GUARD, GEN-PLAN v3.23.1,
                                PM-INSTALL 4 familles + v1.6.5)
  4. KNOWLEDGE.md             — calibration refactor-guard (D009 levée)
  5. @historique/refactor-guard.md — section PM canonique
  6. check-ecosysteme-integrity.py — CORPUS_ATTENDU 8→9 (+commentaire)
  7. task8-tests-n55-fusion.py     — T2.10 « 3 familles »→« 4 familles »
  8. README @mon-ecosysteme   — arbre +1 PM, v1.6.3→v1.6.5, 5→6 fichiers
  9. propagate-context.py     — constantes SHARED v1.7.4→v1.7.5 (×4)

Usage : python3 scripts/g1-extensions-d009.py [--dry-run]
Code retour : 0 = ok ; 2 = ABANDON (état préservé) ; 3 = usage.
"""

import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRY = "--dry-run" in sys.argv


def abandon(msg, code=2):
    print("ABANDON : %s" % msg)
    sys.exit(code)


def apply(path_rel, edits):
    """Applique des substitutions verrouillées sur un fichier."""
    path = os.path.join(BASE, path_rel)
    if not os.path.isfile(path):
        abandon("fichier introuvable : %s" % path)
    with open(path, encoding="utf-8") as f:
        t = f.read()
    for old, new, n, label in edits:
        c = t.count(old)
        if c != n:
            abandon("[%s] motif [%s] trouvé %d fois (attendu %d) : %r"
                    % (path_rel, label, c, n, old[:70]))
        t = t.replace(old, new)
    if DRY:
        print("[DRY-RUN] %s : %d édition(s) verrouillée(s) OK" % (path_rel, len(edits)))
        return
    with open(path, "w", encoding="utf-8") as f:
        f.write(t)
    print("[OK] %s : %d édition(s) écrite(s)" % (path_rel, len(edits)))


# ── 1. generer-pm-skill.py — 4e famille ──────────────────────────────────────
apply("scripts/generer-pm-skill.py", [
    ("utilisateur 2026-10-09) : toute montée de version d'un skill des 3 familles\n"
     "(gen-plan, correct-work, clone-chat) déclenche, AVANT la certification :",
     "utilisateur 2026-10-09) : toute montée de version d'un skill des 4 familles\n"
     "(gen-plan, correct-work, clone-chat, refactor-guard — décision propriétaire\n"
     "D009, 2026-10-12 : PMs de la lignée externe ACCEPTÉS non portés — non\n"
     "verbatim R4 ; le PM canonique démarre à v1.7.0) déclenche, AVANT la "
     "certification :", 1, "docstring KO-L004"),
    ('    "clone-chat": "PROMPT-MAITRE-CLONE-CHAT",\n}',
     '    "clone-chat": "PROMPT-MAITRE-CLONE-CHAT",\n'
     '    # 4e famille — décision propriétaire D009 (2026-10-12, session web-b4d7dd19) :\n'
     '    # PMs externes ACCEPTÉS non portés (non verbatim, R4) ; PM canonique v1.7.0 bootstrap.\n'
     '    "refactor-guard": "PROMPT-MAITRE-REFACTOR-GUARD",\n}', 1, "FAMILLES"),
])

# ── 2. PROMPT-MAITRE-INSTALL-ECOSYSTEME.md ───────────────────────────────────
apply("skills/@mon-ecosysteme/PROMPT-MAITRE-INSTALL-ECOSYSTEME.md", [
    ("instantané explicite des dernières versions des PMs sources (GEN-PLAN, "
     "CORRECT-WORK, CLONE-CHAT) et des fichiers indispensables",
     "instantané explicite des dernières versions des PMs sources (GEN-PLAN, "
     "CORRECT-WORK, CLONE-CHAT, REFACTOR-GUARD — 4e famille, décision D009) et "
     "des fichiers indispensables", 1, "référence §1"),
    ("chaque fois qu'un skill des 3 familles (gen-plan, correct-work, clone-chat) "
     "monte en version",
     "chaque fois qu'un skill des 4 familles (gen-plan, correct-work, clone-chat, "
     "refactor-guard — décision D009 du 2026-10-12) monte en version",
     1, "§2quater"),
    ("| clone-chat | `PROMPT-MAITRE-CLONE-CHAT-v2.0.0.md` | clone-chat v2.0.0 | 5 |",
     "| clone-chat | `PROMPT-MAITRE-CLONE-CHAT-v2.0.0.md` | clone-chat v2.0.0 | 5 |\n"
     "| refactor-guard | `PROMPT-MAITRE-REFACTOR-GUARD-v1.7.0.md` | refactor-guard "
     "v1.7.0 | — |", 1, "§2ter +1 ligne"),
    ("\n### Fichiers de socle indispensables (corpus, archive, outillage, registre)",
     "\nrefactor-guard (4e famille — décision D009, bootstrap v1.7.0) : hors pipeline "
     "d'installation 3-5 (garde-fous de refactoring appelé par gen-plan, hook E13) — "
     "l'instantané est tenu à jour au même titre.\n\n"
     "### Fichiers de socle indispensables (corpus, archive, outillage, registre)",
     1, "§2ter note"),
    ("Version : 1.6.4", "Version : 1.6.5", 1, "version PM-INSTALL"),
    ("| v1.6.4 | 2026-10-11 | KO-L004 v1.1.0 — génération mécanique du PM à toute "
     "montée de version (`scripts/generer-pm-skill.py`) : gen-plan v3.23.0→v3.23.1 ; "
     "recalibrage croisé : SHARED v1.7.4 (§6.1), §2ter, §A.3 |",
     "| v1.6.5 | 2026-10-12 | Décision propriétaire D009 (Task 9, session "
     "web-b4d7dd19 — gen-plan(step)) : 4e famille refactor-guard — PM canonique "
     "PROMPT-MAITRE-REFACTOR-GUARD-v1.7.0 au corpus (bootstrap — PMs de la lignée "
     "externe ACCEPTÉS non portés, R4) ; generer-pm-skill.py 3→4 familles ; §2ter "
     "+1 ligne REFACTOR-GUARD, §2quater 3→4 familles, référence §1 alignée |\n"
     "| v1.6.4 | 2026-10-11 | KO-L004 v1.1.0 — génération mécanique du PM à toute "
     "montée de version (`scripts/generer-pm-skill.py`) : gen-plan v3.23.0→v3.23.1 ; "
     "recalibrage croisé : SHARED v1.7.4 (§6.1), §2ter, §A.3 |", 1, "historique v1.6.5"),
])

# ── 3. PROMPT-MAITRE-SHARED.md ───────────────────────────────────────────────
apply("skills/@mon-ecosysteme/PROMPT-MAITRE-SHARED.md", [
    ("> **Version** : 1.7.4", "> **Version** : 1.7.5", 1, "version SHARED"),
    ("> **Révision** : 2026-10-11 (montée gen-plan v3.23.0→v3.23.1, KO-L004 v1.1.0)",
     "> **Révision** : 2026-10-12 (Task 9, session web-b4d7dd19 — décision "
     "propriétaire D009, gen-plan(step)) — **v1.7.5** : §6.1 — PM REFACTOR-GUARD "
     "v1.7.0 ajouté au corpus (4e famille — bootstrap D009, PMs de la lignée "
     "externe ACCEPTÉS non portés/R4) ; lignes GEN-PLAN + PM-INSTALL recalibrées "
     "aux versions vivantes (KO-L004) ; référence PM-INSTALL v1.6.5. "
     "2026-10-11 (montée gen-plan v3.23.0→v3.23.1, KO-L004 v1.1.0)", 1, "révision"),
    ("règle d'or n°4 : récupération du dépôt par clone) | v3.21.0 |",
     "règle d'or n°4 : récupération du dépôt par clone) | v3.23.1 |",
     1, "§6.1 GEN-PLAN version vivante"),
    ("dérivation dynamique 3 familles + garde anti-rétrogradation v1.2.0",
     "dérivation dynamique 4 familles + garde anti-rétrogradation v1.2.0",
     1, "§6.1 PM-INSTALL 4 familles"),
    ("§2quater génération automatique du PM — KO-L004 v1.1.0, v1.6.0) | v1.6.0 |",
     "§2quater génération automatique du PM — KO-L004 v1.1.0, v1.6.0 ; 4e famille "
     "refactor-guard — décision D009 (PM v1.7.0 bootstrap au corpus), v1.6.5) "
     "| v1.6.5 |", 1, "§6.1 PM-INSTALL version vivante"),
    ("| `PROMPT-MAITRE-CLONE-CHAT-v2.0.0.md` | Spécification clone-chat | v2.0.0 |",
     "| `PROMPT-MAITRE-CLONE-CHAT-v2.0.0.md` | Spécification clone-chat | v2.0.0 |\n"
     "| `PROMPT-MAITRE-REFACTOR-GUARD-v1.7.0.md` | Spécification refactor-guard "
     "(4e famille — décision D009 : PMs de la lignée externe ACCEPTÉS non portés, "
     "bootstrap canonique v1.7.0) | v1.7.0 |", 1, "§6.1 +1 ligne PM"),
])

# ── 4. KNOWLEDGE.md — calibration refactor-guard ─────────────────────────────
apply("skills/KNOWLEDGE.md", [
    ("6 PM instance source — non portés, réserve R3/D009) ; arêtes bidirectionnelles ×7",
     "6 PM instance source — ACCEPTÉS non portés, décision D009) ; arêtes "
     "bidirectionnelles ×7 ; Task 9 (2026-10-12, session web-b4d7dd19 — "
     "gen-plan(step)) : décision propriétaire D009 LEVÉE — PM canonique "
     "PROMPT-MAITRE-REFACTOR-GUARD-v1.7.0 au corpus (bootstrap, 4e famille — "
     "generer-pm 3→4 familles), PMs de la lignée externe ACCEPTÉS non portés "
     "(non verbatim, R4)", 1, "calibration refactor-guard"),
])

# ── 5. @historique/historiques-par-skill/refactor-guard.md ───────────────────
apply("skills/@historique/historiques-par-skill/refactor-guard.md", [
    ("| v1.0.0 | 2026-10-10 | Matérialisation initiale (projet « Skill Refactorisation "
     "Plan » — discussion Qwen T1-T46 : conception C05/C-SAFE-1, zéro-régression, "
     "gouvernance N0-N5) |",
     "| v1.0.0 | 2026-10-10 | Matérialisation initiale (projet « Skill Refactorisation "
     "Plan » — discussion Qwen T1-T46 : conception C05/C-SAFE-1, zéro-régression, "
     "gouvernance N0-N5) |\n"
     "\n### PM canonique (2026-10-12 — décision D009)\n\n"
     "Le PM refactor-guard entre au corpus sous décision propriétaire D009 (Task 9, "
     "session web-b4d7dd19 — gen-plan(step)) : `PROMPT-MAITRE-REFACTOR-GUARD-v1.7.0.md` "
     "(bootstrap — sections SKILL.md portées verbatim, ancres `generer-pm-skill.py` "
     "alignées, famille n°4). Les 6 PMs de la lignée externe (v1.2.0→v1.7.0, discussion "
     "468a4c26) sont ACCEPTÉS non portés (non verbatim — provenance R4) ; les futures "
     "montées génèrent leur PM mécaniquement (extension generer-pm 3→4 familles, "
     "§2quater PM-INSTALL v1.6.5).", 1, "section PM canonique"),
])

# ── 6. check-ecosysteme-integrity.py — CORPUS_ATTENDU 8→9 ────────────────────
apply("scripts/check-ecosysteme-integrity.py", [
    ("# (SHARED, INSTALL, ULTRA, README, SYNC-CONTEXT), re-scellement archive "
     "aligné (F2).\nCORPUS_ATTENDU = 8",
     "# (SHARED, INSTALL, ULTRA, README, SYNC-CONTEXT), re-scellement archive "
     "aligné (F2).\n# Recalibrage Task 9 (session web-b4d7dd19, 2026-10-12) : 8 → 9 — "
     "PM REFACTOR-GUARD\n# v1.7.0 au corpus (décision D009 — 4e famille, bootstrap "
     "canonique).\nCORPUS_ATTENDU = 9", 1, "CORPUS_ATTENDU"),
])

# ── 7. task8-tests-n55-fusion.py — T2.10 recalibré ───────────────────────────
apply("scripts/task8-tests-n55-fusion.py", [
    ('check("T2.10 generer-pm --check : 3 familles COHERENT après cascade", '
     '"COHERENT" in r.stdout and r.returncode == 0)',
     'check("T2.10 generer-pm --check : 4 familles COHERENT après cascade (D009)", '
     '"COHERENT" in r.stdout and r.returncode == 0)', 1, "T2.10"),
])

# ── 8. README @mon-ecosysteme ────────────────────────────────────────────────
apply("skills/@mon-ecosysteme/README.md", [
    ("│   ├── PROMPT-MAITRE-CLONE-CHAT-v2.0.0.md\n"
     "│   ├── PROMPT-MAITRE-INSTALL-ECOSYSTEME.md  ← Installation (source unique v1.6.3)",
     "│   ├── PROMPT-MAITRE-CLONE-CHAT-v2.0.0.md\n"
     "│   ├── PROMPT-MAITRE-REFACTOR-GUARD-v1.7.0.md  ← 4e famille (décision D009)\n"
     "│   ├── PROMPT-MAITRE-INSTALL-ECOSYSTEME.md  ← Installation (source unique v1.6.5)",
     1, "arbre corpus"),
    ("- **Cibles** : 5 fichiers `PROMPT-MAITRE-*.md`",
     "- **Cibles** : 6 fichiers `PROMPT-MAITRE-*.md`", 1, "cibles"),
])

# ── 9. propagate-context.py — constantes SHARED v1.7.4→v1.7.5 ────────────────
apply("scripts/propagate-context.py", [
    ("SHARED v1.7.4", "SHARED v1.7.5", 4, "constantes propagateur"),
])

if DRY:
    print("\n[DRY-RUN] aucune écriture — 9 fichiers validés.")
else:
    print("\nExtensions D009 écrites (9 fichiers, substitutions verrouillées).")
