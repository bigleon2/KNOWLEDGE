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
"""Task 72 → Task 76 — Shim de délégation : le re-scellement de l'archive
d'intégrité DÉLÈGUE désormais au scelleur canonique v2.2
(`scripts/task21-f2-rebuild-archive.py`).

Task 76 (faille F4, 2026-11-08, session web-ecef7f80 — directive « tests des
systèmes d'installation ») : ce script (voie ré-écrite Task 72 sur la convention
task42) scellait un véhicule v2.3 « corpus + piliers » CONTRAIRE à la
spécification PM-INSTALL, qui désigne le véhicule d'intégrité v2.2 corpus-seul
(5 mentions : §A.1, table §2 étape 2, §2bis, §2ter, §7 — scelleur désigné :
task21-f2-rebuild-archive.py, étapes 2 et 10). Résultat constaté mécaniquement :
DEUX formes d'archive concurrentes — hôte v2.2 (9 entrées, produite par chaque
run du pipeline) vs dépôt v2.3 (15 entrées, produite par les cascades) —
divergence hôte/dépôt systématique (membres corpus identiques, 6 piliers en
plus côté dépôt). Correction : UNE SEULE logique de scellement (R4 — jamais
dupliquer) : toutes les voies (pipeline, cascade) rescellent via le canonique
v2.2 ; le contenu des piliers vit dans l'arbre (retrait sanctionné dans
RETRAITS_SANCTIONNES du canonique — aucune perte). Ce fichier ne contient plus
aucune logique de scellement : ne rien éditer ici."""
import os
import subprocess
import sys

CIBLE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "task21-f2-rebuild-archive.py")
r = subprocess.run([sys.executable, os.path.abspath(CIBLE)])
sys.exit(r.returncode)
