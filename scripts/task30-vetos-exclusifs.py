#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.13)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

# -*- coding: utf-8 -*-
"""
Task 30 (GO propriétaire) — Option A : application des vetos exclusifs (champ
optionnel `exclusifs` par cas dans trigger_evals.json — termes réservés d'AUTRES
skills/générations, doctrine « périmètre » des SKILL.md encodée comme donnée).

Chaque veto est tracé avec sa doctrine (arbitrage Task 25 §4 + discussion
PM INSTALL scripts/discussion-64c90144.txt). Idempotent : ré-appliquer le même
veto est un no-op (le champ existant identique n'est pas réécrit).

Usage : python scripts/task30-vetos-exclusifs.py [--dry-run]
"""
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
SKILLS = BASE / "skills"
DRY = "--dry-run" in sys.argv

# Vetos exclusifs — (skill, sous-chaîne exacte de la query du cas, [termes réservés],
#                    doctrine) — la sous-chaîne identifie le cas sans ambiguïté.
VETOS = [
    ("iphone17", "rendu iPhone 18 Pro Max", ["iphone 18"],
     "Périmètre d'époque : iphone17 supersédée par iphone18 (SKILL.md v1.1.0) — arbitrage Task 25 D1 CONFIRME"),
    ("iphone18", "rendu iPhone 17 Pro Max", ["iphone 17"],
     "Périmètre d'époque : le rendu 17 appartient à iphone17 — arbitrage Task 25 D2 CONFIRME"),
    ("iphone19", "rendu iPhone 18 Pro Max", ["iphone 18"],
     "Génération confirmée courante = iphone18 (SKILL.md iphone19 : « préférer le skill iphone18 ») — arbitrage Task 25 D3 CONFIRME"),
    ("agent-creator", "Zapier", ["zapier"],
     "Automatisation SaaS tierce (Zapier) hors périmètre agent-creator (agents autonomes .agent)"),
    ("audio-metadata", "Transcris le contenu parlé", ["transcris"],
     "Transcription parole→texte = domaine ASR (speech-to-text), pas métadonnées audio"),
    ("prompt-engineering", "nouveau skill à partir de ce prompt", ["nouveau skill"],
     "Création de skill = domaine skill-creator, pas optimisation de prompt"),
    ("script-reviewer", "Crée un nouveau script", ["nouveau script"],
     "Création de script = domaine script-creator ; script-reviewer = relecture/évaluation"),
    ("script-mon-ecosysteme-infrastructure", "installation complète", ["installation complète"],
     "Installation profil = domaine PM-INSTALL ; script-mon-ecosysteme-infrastructure = génération de fichiers"),
    ("skills-inventory", "hub ClawHub", ["clawhub"],
     "Recherche/installation depuis un hub tiers = domaine skill-finder-cn ; skills-inventory = inventaire local"),
    ("skills-inventory", "Cherche et installe de nouveaux skills", ["et installe"],
     "Installation de skills = domaine skill-finder-cn ; « installe » seul entrerait en collision avec les cas positifs (« skills installés »)"),
    ("pdf-llm", "Produis un rapport PDF", ["produis un rapport"],
     "Création de PDF = domaine pdf (production line Report) ; pdf-llm = extraction documentaire"),
    ("pdf-llm", "Génère un nouveau PDF", ["génère un nouveau pdf"],
     "Création de PDF = domaine pdf ; pdf-llm = extraction/RAG"),
    ("pdf-llm", "Fusionne ces 5 PDF", ["fusionne"],
     "Manipulation de PDF existants = domaine pdf (Process) ; pdf-llm = extraction"),
    ("vue-upload", "Vérifie le travail réalisé", ["vérifie le travail"],
     "Relecture/vérification de livrables = domaine script-reviewer/correct-work ; vue-upload = portail de fichiers"),
]


def main():
    applied, noop, missing = 0, 0, []
    for skill, anchor, termes, doctrine in VETOS:
        path = SKILLS / skill / "evals" / "trigger_evals.json"
        cases = json.loads(path.read_text(encoding="utf-8"))
        hits = [c for c in cases if anchor in c["query"]]
        if not hits:
            missing.append(f"{skill}::{anchor[:40]}")
            continue
        for c in hits:
            existants = c.get("exclusifs")
            if existants == termes:
                noop += 1
                continue
            c["exclusifs"] = termes
            applied += 1
            if not DRY:
                path.write_text(json.dumps(cases, ensure_ascii=False, indent=1) + "\n",
                                encoding="utf-8")
            print(f"VETO {skill:<38} {termes} — {doctrine}")
    print(f"\nBILAN : {applied} veto(s) appliqué(s), {noop} déjà en place (no-op), "
          f"{len(missing)} cas introuvable(s) : {missing or 'aucun'}")
    sys.exit(1 if missing else 0)


if __name__ == "__main__":
    main()
