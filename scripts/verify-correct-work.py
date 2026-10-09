#!/usr/bin/env python3
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
