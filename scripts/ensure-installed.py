#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.47)
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
Ce fichier délègue tous les arguments à la version du skill.

REPLI AMNÉSIE (PM-INSTALL §3.2-d, v1.10.7 — Task 12, session web-220878ed) : si le
script du skill est ABSENT (skills/gen-plan/ effacé du profil — réinjection plateforme
ou wipe), le shim NE CRASHE PLUS : il délègue au bootstrap canonique
(scripts/bootstrap-ecosysteme.py — pipeline PM-INSTALL §3.2-c) qui réinstalle les
formes certifiées, PUIS la garde redevient opérationnelle (fin de l'œuf-et-la-poule :
la garde ne peut pas vivre uniquement dans le skill qu'elle garde). Garde
anti-récursion : le repli pose ECO_REPLI_ACTIF=1 ; si le shim est rappelé dans cet
état avec le skill toujours absent, il rend AMNESIE-PERSISTANTE (rc 2) au lieu de
boucler. ECO_SIMULER=1 : annonce le repli sans l'exécuter (mode test)."""
import os
import subprocess
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
SKILL_SCRIPT = os.path.abspath(os.path.join(ICI, "..", "skills", "gen-plan",
                                            "scripts", "ensure-installed.py"))
BOOTSTRAP = os.path.abspath(os.path.join(ICI, "bootstrap-ecosysteme.py"))

if os.path.exists(SKILL_SCRIPT):
    r = subprocess.run([sys.executable, SKILL_SCRIPT] + sys.argv[1:])
    sys.exit(r.returncode)

# — skill gen-plan absent : amnésie détectée —
print("AMNESIE-DETECTEE : skills/gen-plan/scripts/ensure-installed.py absent du profil — "
      "garde É1-INSTALL non amorçable depuis le skill (réinjection plateforme ou wipe).")
if os.environ.get("ECO_SIMULER") == "1":
    print("REPLI (simulé) : bootstrap canonique scripts/bootstrap-ecosysteme.py "
          "(pipeline PM-INSTALL §3.2-c) serait exécuté maintenant.")
    sys.exit(0)
if os.environ.get("ECO_REPLI_ACTIF") == "1":
    print("AMNESIE-PERSISTANTE : le repli bootstrap n'a PAS réinstallé skills/gen-plan/ — "
          "exécuter le pipeline PM-INSTALL §3.2 manuellement (installation directe §3.2-a).")
    sys.exit(2)
if os.path.exists(BOOTSTRAP):
    print("REPLI : exécution du bootstrap canonique (PM-INSTALL §3.2-c)…")
    env = dict(os.environ)
    env["ECO_REPLI_ACTIF"] = "1"
    r = subprocess.run([sys.executable, BOOTSTRAP], env=env)
    sys.exit(r.returncode)
print("AMNESIE-DETECTEE et bootstrap introuvable — exécuter le pipeline PM-INSTALL "
      "§3.2 manuellement (installation directe §3.2-a).")
sys.exit(1)
