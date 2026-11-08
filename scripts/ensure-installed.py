#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.36)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).
"""

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
