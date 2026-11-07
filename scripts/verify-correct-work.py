#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.31)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).
"""

# -*- coding: utf-8 -*-
"""Shim de compatibilité (S2-α — Task 12, matérialisation de la décision Task 10,
re-validée propriétaire 2026-10-10) : délègue à l'arbitre canonique du skill
correct-work — source de vérité unique (résorption du double divergent, finding ④).

  - sans argument          → 16 checks canoniques (délégation pure, sortie identique)
  - <rapport.md> / args    → REFUS EXPLICITE rc=64 : la validation de rapport §2.4
    n'est PAS déléguée par le canonique — refus explicite, jamais d'avalage
    silencieux (finding S3, Second Opinion Task 10).

Ne rien éditer ici — éditer skills/correct-work/scripts/verify-correct-work.py.
"""
import os
import runpy
import sys

CANONICAL = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "..", "skills", "correct-work", "scripts", "verify-correct-work.py")

if len(sys.argv) > 1:
    sys.stderr.write(
        "ERREUR (S2-a) : mode '<rapport.md>' non delegue — l'arbitre canonique "
        "n'implemente que les 16 checks post-install (finding S3, Second Opinion "
        "Task 10 ; refus explicite, pas d'avalage silencieux).\n")
    sys.exit(64)

if not os.path.isfile(CANONICAL):
    sys.stderr.write("ERREUR (S2-a) : arbitre canonique absent : %s\n" % CANONICAL)
    sys.exit(2)

sys.argv[0] = CANONICAL
runpy.run_path(CANONICAL, run_name="__main__")
