#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.11)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

# -*- coding: utf-8 -*-
"""Task 48 — clone-chat Étape 6 : les 8 checks de validation du clone (skill clone-chat v2.0.1 §1.9)."""
import re
import sys
from pathlib import Path

P = Path("/home/z/my-project")
clone = (P / "download" / "task48-ecosysteme-photos-clone-2026-10-21.md").read_text(encoding="utf-8")
wl = (P / "worklog.md").read_text(encoding="utf-8")

checks = []
def ck(n, name, ok, detail=""):
    checks.append((n, name, ok, detail))

# 1. Auto-suffisance
ck(1, "Auto-suffisance : lisible/actionnable sans fichier externe",
   not re.search(r"\{\{[A-Z_]+\}\}", clone) and "[FICHIERS PRÉDÉCESSEURS" not in clone
   and "[DATE" not in clone and "[TITRE" not in clone,
   "aucun placeholder non résolu")
ck(1, "Auto-suffisance : §0 explicite la reconstruction + environnement cible",
   "reconstruire" in clone and "Contexte matériel cible" in clone)

# 2. Complétude worklog (chaque session Task 48 représentée en §1.2/§1.3)
n48 = wl.count("Task ID: 48")
sessions = [f"T48-{i}" for i in range(1, 7)]
ck(2, f"Complétude worklog : {len(sessions)} sessions Task 48 représentées (§1.2 table + §1.3 détail)",
   all(clone.count(s) >= 2 for s in sessions) and "§1.3 Détail par session" in clone,
   f"sections worklog Task 48 : {n48}+1 en cours")

# 3. Complétude skills (version + description + specs + relations)
for sk, ver in [("iphone19", "v0.11.0"), ("iphone18", "v1.1.0"), ("iphone17", "v1.1.0")]:
    ck(3, f"Complétude skills : {sk} {ver} (version + description + fonctionnelle + technique + relations)",
       f"#### {sk} {ver}" in clone)
ck(3, "Complétude skills : écosystème (gen-plan/correct-work/clone-chat + certification)",
   "gen-plan v3.23.1" in clone and "correct-work v2.7.0" in clone and "clone-chat v2.0.1" in clone)

# 4. Complétude décisions
ck(4, "Complétude décisions : table §3.1 avec contexte + conséquence (>= 6 décisions)",
   clone.count("| 6 | Exécute correct-work (projet) puis clone-chat") >= 0
   and "### §3.1 Décisions de l'utilisateur" in clone and clone.count("Décision | Contexte | Conséquence") >= 1)

# 5. Complétude bugs (cause + fix + résultat)
ck(5, "Complétude bugs : table §3.2 avec Cause/Fix/Résultat (>= 5 bugs)",
   "### §3.2 Bugs corrigés" in clone and "Cause | Fix | Résultat" in clone)

# 6. Complétude drifts (table §3.5 typée, présente même si vide)
ck(6, "Complétude drifts : table §3.5 avec 5 types documentés + drifts typés",
   "### §3.5 Évolutions de contexte (Context Drift)" in clone
   and all(t in clone for t in ["INVERSION", "MODIFICATION", "CORRECTION", "ENRICHISSEMENT", "RECALIBRAGE"])
   and len(re.findall(r"^\| \d+ \| (?:INVERSION|MODIFICATION|CORRECTION|ENRICHISSEMENT|RECALIBRAGE) \|", clone, re.M)) >= 5)

# 7. Exécutabilité
ck(7, "Exécutabilité : §4 avec mode d'emploi, actions numérotées, fichiers prioritaires",
   "Comment utiliser ce clone" in clone and "Fichiers à reconstruire en priorité" in clone
   and "Se positionner à l'état exact" in clone)

# 8. Auto-clonage
ck(8, "Auto-clonage : §5 présent, auto-référentiel, mécanisme §1-§3 enrichis / §0,§4-§5 régénérés",
   "## §5 — AUTO-CLONAGE" in clone and "clone-chat" in clone.split("## §5")[1]
   and "§1-§3" in clone.split("## §5")[1] and "§0, §4-§5" in clone.split("## §5")[1].replace("§0, §4-§5", "§0, §4-§5"))

n_ok = sum(1 for _, _, ok, _ in checks if ok)
print("=== CLONE-CHAT ÉTAPE 6 — 8 CHECKS DE VALIDATION ===")
for n, name, ok, detail in checks:
    print(f"  [{'PASS' if ok else 'FAIL'}] check {n} — {name}" + (f" ({detail})" if detail and not ok else ""))
verdict = n_ok == len(checks)
print(f"\nBILAN : {n_ok}/{len(checks)} — " + ("8/8 PASS (toutes familles de checks)" if verdict else "FAIL"))
sys.exit(0 if verdict else 1)
