#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Shim de compatibilité (Task 29 D001) : le script maître est intégré au skill gen-plan
(skills/gen-plan/scripts/ensure-installed.py — Task 23 D006 + Task 29 D001-D004).
Ce fichier délègue tous les arguments à la version du skill. Ne rien éditer ici."""
import os
import subprocess
import sys

SKILL_SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "..", "skills", "gen-plan", "scripts", "ensure-installed.py")
r = subprocess.run([sys.executable, os.path.abspath(SKILL_SCRIPT)] + sys.argv[1:])
sys.exit(r.returncode)
