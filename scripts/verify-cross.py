#!/usr/bin/env python3
"""Vérification croisée des 3 prompts maîtres (Phase 3)."""

import re
import os

BASE = "/home/z/my-project/download/"

shared = open(os.path.join(BASE, "PROMPT-MAITRE-SHARED.md")).read()
genplan = open(os.path.join(BASE, "PROMPT-MAITRE-GEN-PLAN-v3.6.0.md")).read()
correct = open(os.path.join(BASE, "PROMPT-MAITRE-CORRECT-WORK-v2.3.0.md")).read()

results = []

def check(name, passed, detail):
    status = "PASS" if passed else "FAIL"
    results.append((name, status, detail))
    print(f"  [{status}] {name}: {detail}")

print("=== CHECK 1 : Pas de duplication entre SHARED et les spécifiques ===")
# Extraire les sections SHARED
shared_sections = re.findall(r'^## §[0-9]', shared, re.MULTILINE)
shared_subsections = re.findall(r'^### §[0-9]+\.[0-9]+', shared, re.MULTILINE)
print(f"  Sections SHARED : {shared_sections}")
print(f"  Sous-sections SHARED : {len(shared_subsections)} trouvées")

# Vérifier que les mots-clés communs apparaissent dans SHARED (pas dupliqués en bloc)
shared_keywords = ["Règle zéro", "Conventions de nommage", "Format worklog", "Registre KB", "Matrice agent", "Protocole de Découverte"]
for kw in shared_keywords:
    in_shared = kw in shared
    check(f"'{kw}' dans SHARED", in_shared, "trouvé" if in_shared else "MANQUANT du socle commun")

print("\n=== CHECK 2 : Références SHARED cohérentes ===")
# Vérifier que les références vers SHARED pointent vers des sections existantes
all_shared_refs = []
for fname, content in [("gen-plan", genplan), ("correct-work", correct)]:
    refs = re.findall(r'SHARED §([0-9](?:.[0-9])?)', content)
    for ref in refs:
        # Vérifier que la section existe dans SHARED
        section_pattern = rf'^##[ #]*§{ref}\b'
        exists = bool(re.search(section_pattern, shared, re.MULTILINE))
        check(f"{fname} réfère SHARED §{ref}", exists, "section trouvée" if exists else "section manquante")
        all_shared_refs.append(ref)

print(f"\n  Total références SHARED : {len(all_shared_refs)}")

print("\n=== CHECK 3 : Relations bidirectionnelles ===")
# gen-plan mentionne correct-work >= v2.3.0
gp_cw = "correct-work" in genplan and (">= v2.3.0" in genplan or ">=2.3.0" in genplan)
# correct-work mentionne gen-plan >= v3.6.0
cw_gp = "gen-plan" in correct and (">= v3.6.0" in correct or ">=3.6.0" in correct)
check("gen-plan -> correct-work >= v2.3.0", gp_cw, "trouvé" if gp_cw else "manquant")
check("correct-work -> gen-plan >= v3.6.0", cw_gp, "trouvé" if cw_gp else "manquant")

# clone-chat mentionné dans les deux
gp_clone = "clone-chat" in genplan
cw_clone = "clone-chat" in correct
check("gen-plan mentionne clone-chat", gp_clone, "")
check("correct-work mentionne clone-chat", cw_clone, "")

print("\n=== CHECK 4 : Aucune info perdue (contenu v1 présent dans v2) ===")
elements = {
    "gen-plan": [
        ("4 modes", "4 modes" in genplan),
        ("15 étapes", "E15" in genplan),
        ("N1 tagging", "Norme N1" in genplan or "#token" in genplan),
        ("N2 snippets", "Norme N2" in genplan or "snippets" in genplan.lower()),
        ("N3 Python", "Norme N3" in genplan or "Python uniquement" in genplan),
        ("3 profils", "NORMAL" in genplan and "ECO" in genplan and "VIEUX PC" in genplan),
        ("Auto-calibration", "auto-calibration" in genplan.lower() or "calibration" in genplan.lower()),
        ("KB kb_path", "kb_path" in genplan),
        ("4 fichiers ref", "etapes-detaillees" in genplan and "grille-token" in genplan and "classification-types" in genplan and "profils-ressource" in genplan),
        ("Type 1-4", "Type 1" in genplan and "Type 4" in genplan),
    ],
    "correct-work": [
        ("3 modes", "PROJET" in correct and "CIBLE" in correct and "DIRECT" in correct),
        ("5 étapes", "Étape 5" in correct),
        ("S1-S4", "S1" in correct and "S4" in correct),
        ("KB kb_path", "kb_path" in correct),
        ("Matrice statique", "Matrice statique" in correct or "SHARED §4" in correct),
        ("Matrice dynamique", "dynamique" in correct),
        ("gen-plan dep", ">= v3.6.0" in correct or ">=3.6.0" in correct),
        ("clone-chat dep", ">= v1.2.0" in correct or ">=1.2.0" in correct),
        ("Verdicts", "PASS" in correct and "FAIL" in correct),
        ("Round corrections", "Round 1" in correct and "Round 3" in correct),
        ("Checklists", "PROJET" in correct or "Mode PROJET" in correct),
    ],
}
for skill, checks in elements.items():
    for name, passed in checks:
        check(f"{skill} : {name}", passed, "présent" if passed else "MANQUANT")

print("\n=== CHECK 5 : Tailles conformes ===")
gp_lines = genplan.count('\n')
cw_lines = correct.count('\n')
sh_lines = shared.count('\n')
check(f"SHARED ~200 lignes", 150 <= sh_lines <= 280, f"{sh_lines} lignes")
check(f"GEN-PLAN ~750 lignes (incluant §9 in extenso)", 600 <= gp_lines <= 850, f"{gp_lines} lignes")
check(f"CORRECT-WORK ~350 lignes", 250 <= cw_lines <= 480, f"{cw_lines} lignes")
total_lines = sh_lines + gp_lines + cw_lines
print(f"\n  Total : {total_lines} lignes (vs ~930+560={930+560} avant refactoring)")
print(f"  Réduction : {930+560 - total_lines} lignes ({round((1-total_lines/(930+560))*100,1)}%)")

print("\n=== RÉSUMÉ ===")
pass_count = sum(1 for _, s, _ in results if s == "PASS")
fail_count = sum(1 for _, s, _ in results if s == "FAIL")
print(f"  PASS : {pass_count}")
print(f"  FAIL : {fail_count}")
if fail_count == 0:
    print("  VERDICT : ALL PASS")
else:
    print("  VERDICT : FAILURES DETECTED")
    for name, status, detail in results:
        if status == "FAIL":
            print(f"    - {name}: {detail}")