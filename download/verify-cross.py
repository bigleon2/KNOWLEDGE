#!/usr/bin/env python3
"""vérification croisée des prompts maîtres + sync download/.

Checks 1-5 : validation du contenu des PMs (source = download/).
Check 6   : rappel de synchronisation download/ vs skills/_prompts-maitres/.
--mode correct-work : 8 checks supplementaires (scan KB dynamique).
"""

import re
import os
import sys
import filecmp


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(BASE_DIR, "download") + "/"
SKILLS_DIR = os.path.join(BASE_DIR, "skills")
KB_PATH = os.path.join(SKILLS_DIR, "KNOWLEDGE.md")

MODE = "default"
if "--mode" in sys.argv and "correct-work" in sys.argv:
    MODE = "correct-work"

S = chr(0xa7)  # signe section
results = []


def check(name, passed, détail):
    status = "PASS" if passed else "FAIL"
    results.append((name, status, détail))
    print(f"  [{status}] {name}: {détail}")


def read_file(path):
    if not os.path.isfile(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# === Chargement des fichiers ===
shared = read_file(os.path.join(BASE, "PROMPT-MAITRE-SHARED.md"))
genplan = read_file(os.path.join(BASE, "PROMPT-MAITRE-GEN-PLAN-v3.6.1.md"))
correct = read_file(os.path.join(BASE, "PROMPT-MAITRE-CORRECT-WORK-v2.4.0.md"))

if not shared or not genplan or not correct:
    print("ERREUR : fichiers PM manquants dans download/")
    sys.exit(1)

# ==========================================================================
# CHECKS 1-6 (mode par defaut)
# ==========================================================================

print("=== CHECK 1 : Pas de duplication entre SHARED et les spécifiques ===")
shared_sections = re.findall(rf'^## {S}[0-9]', shared, re.MULTILINE)
shared_subsections = re.findall(rf'^### {S}[0-9]+\.[0-9]+', shared, re.MULTILINE)
print(f"  Sections SHARED : {shared_sections}")
print(f"  Sous-sections SHARED : {len(shared_subsections)} trouvées")

shared_keywords = ["R\u00e8gle z\u00e9ro", "Conventions de nommage", "Format worklog", "Registre KB", "Matrice agent", "Protocole de D\u00e9couverte"]
for kw in shared_keywords:
    in_shared = kw in shared
    check(f"'{kw}' dans SHARED", in_shared, "trouve" if in_shared else "MANQUANT du socle commun")

print("\n=== CHECK 2 : références SHARED cohérentes ===")
all_shared_refs = []
for fname, content in [("gen-plan", genplan), ("correct-work", correct)]:
    refs = re.findall(rf'SHARED {S}([0-9](?:.[0-9])?)', content)
    for ref in refs:
        section_pattern = rf'^##[ #]*{S}{ref}\b'
        exists = bool(re.search(section_pattern, shared, re.MULTILINE))
        check(f"{fname} refere SHARED {S}{ref}", exists, "section trouvée" if exists else "section manquante")
        all_shared_refs.append(ref)

print(f"\n  Total références SHARED : {len(all_shared_refs)}")

print("\n=== CHECK 3 : Relations bidirectionnelles ===")
gp_cw = "correct-work" in genplan and (">= v2.3.0" in genplan or ">=2.3.0" in genplan or ">= v2.4.0" in genplan)
cw_gp = "gen-plan" in correct and (">= v3.6.0" in correct or ">=3.6.0" in correct)
check("gen-plan -> correct-work >= v2.3.0 (or v2.4.0)", gp_cw, "trouve" if gp_cw else "manquant")
check("correct-work -> gen-plan >= v3.6.0", cw_gp, "trouve" if cw_gp else "manquant")

gp_clone = "clone-chat" in genplan
cw_clone = "clone-chat" in correct
check("gen-plan mentionne clone-chat", gp_clone, "")
check("correct-work mentionne clone-chat", cw_clone, "")

print("\n=== CHECK 4 : Aucune info perdue (contenu v1 dans v2) ===")
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
        ("Matrice statique", "Matrice statique" in correct or "SHARED" in correct),
        ("Matrice dynamique", "dynamique" in correct),
        ("gen-plan dep", ">= v3.6.0" in correct or ">=3.6.0" in correct),
        ("clone-chat dep", ">= v2.0.0" in correct or ">=2.0.0" in correct),
        ("Verdicts", "PASS" in correct and "FAIL" in correct),
        ("Round corrections", "Round 1" in correct and "Round 3" in correct),
        ("Checklists", "PROJET" in correct or "Mode PROJET" in correct),
    ],
}
for skill, checks in elements.items():
    for name, passed in checks:
        check(f"{skill} : {name}", passed, "present" if passed else "MANQUANT")

print("\n=== CHECK 5 : Tailles conformes ===")
gp_lines = genplan.count('\n')
cw_lines = correct.count('\n')
sh_lines = shared.count('\n')
check(f"SHARED ~200 lignes", 150 <= sh_lines <= 280, f"{sh_lines} lignes")
check(f"GEN-PLAN ~937 lignes (incluant {S}9 in extenso enrichi)", 750 <= gp_lines <= 1000, f"{gp_lines} lignes")
check(f"CORRECT-WORK ~500 lignes (incluant checklists)", 400 <= cw_lines <= 600, f"{cw_lines} lignes")
total_lines = sh_lines + gp_lines + cw_lines
print(f"\n  Total : {total_lines} lignes (vs ~930+560={930+560} avant refactoring)")
print(f"  Reduction : {930+560 - total_lines} lignes ({round((1-total_lines/(930+560))*100,1)}%)")

print("\n=== CHECK 6 : Synchronisation download/ ===")
SOURCE_DIR = os.path.join(BASE_DIR, "skills", "_prompts-maitres") + "/"
SYNC_FILES = [
    "PROMPT-MAITRE-SHARED.md",
    "PROMPT-MAITRE-GEN-PLAN-v3.6.1.md",
    "PROMPT-MAITRE-CORRECT-WORK-v2.4.0.md",
    "PROMPT-MAITRE-CLONE-CHAT-v2.0.0.md",
    "README.md",
]
for fname in SYNC_FILES:
    src = os.path.join(SOURCE_DIR, fname)
    dst = os.path.join(BASE, fname)
    if not os.path.exists(src):
        check(f"sync {fname}", False, "source manquante")
        continue
    if not os.path.exists(dst):
        check(f"sync {fname}", False, "absent de download/")
        continue
    if filecmp.cmp(src, dst, shallow=False):
        check(f"sync {fname}", True, "identique")
    else:
        check(f"sync {fname}", False, "EN écart")

# ==========================================================================
# CHECK 7 : Mode correct-work (scan KB dynamique)
# ==========================================================================

if MODE == "correct-work":
    print("\n=== CHECK 7 : Scan KB dynamique (correct-work) ===")

    kb_content = read_file(KB_PATH)
    cw_skill = read_file(os.path.join(SKILLS_DIR, "correct-work", "SKILL.md"))

    # 7.1 : KB accessible
    check("KB accessible", kb_content is not None, f"{KB_PATH}")

    # 7.2 : correct-work dans KB
    if kb_content:
        cw_in_kb = "correct-work" in kb_content
        check("correct-work dans KB", cw_in_kb, "entree presente" if cw_in_kb else "MANQUANTE")

        # 7.3 : Version KB cohérente avec SKILL.md
        if cw_skill and cw_in_kb:
            fm_ver = re.search(r'^version:\s*([\d.]+)', cw_skill, re.MULTILINE)
            kb_ver = re.search(r'correct-work v([\d.]+)', kb_content)
            fm_v = fm_ver.group(1) if fm_ver else "?"
            kb_v = kb_ver.group(1) if kb_ver else "?"
            ver_ok = fm_v == kb_v
            check(f"Version cohérente (SKILL={fm_v}, KB={kb_v})", ver_ok, "" if ver_ok else "écart")

        # 7.4 : Toutes les deps correct-work existent dans KB
        if cw_skill and kb_content:
            deps = re.findall(r'skill:\s*(\S+)', cw_skill)
            for dep in deps:
                in_kb = dep in kb_content
                check(f"Dep '{dep}' dans KB", in_kb, "present" if in_kb else "MANQUANT")

        # 7.5 : Utilise par cohérent (gen-plan, autonomous-agent)
        if kb_content:
            cw_entry = re.search(r'## correct-work.*?---', kb_content, re.DOTALL)
            if cw_entry:
                used_by = cw_entry.group(0)
                has_gp = "gen-plan" in used_by
                has_aa = "autonomous-agent" in used_by
                check("'Utilise par' mentionne gen-plan", has_gp, "" if has_gp else "manquant")
                check("'Utilise par' mentionne autonomous-agent", has_aa, "" if has_aa else "manquant")

        # 7.6 : Relations bidirectionnelles dans KB
        if kb_content:
            rels = re.findall(r'correct-work.*?\|.*?\|', kb_content)
            check(f"Relations dans KB ({len(rels)}/{len(rels)})", len(rels) >= 3, f"{len(rels)} relations trouvées")

        # 7.7 : verify-correct-work.py existe et fonctionne
        vcw_path = os.path.join(SKILLS_DIR, "correct-work", "scripts", "verify-correct-work.py")
        vcw_exists = os.path.isfile(vcw_path)
        check("verify-correct-work.py existe", vcw_exists, vcw_path if vcw_exists else "MANQUANT")

        # 7.8 : Skills écosystème tous dans KB
        if kb_content:
            eco_skills = ["gen-plan", "correct-work", "clone-chat", "skills-inventory", "skill-creator", "autonomous-agent"]
            for sk in eco_skills:
                in_kb = sk in kb_content
                check(f"écosystème '{sk}' dans KB", in_kb, "" if in_kb else "MANQUANT")

    print(f"\n  Mode : correct-work ({MODE})")

# ==========================================================================
# RESUME
# ==========================================================================

print("\n=== RESUME ===")
pass_count = sum(1 for _, s, _ in results if s == "PASS")
fail_count = sum(1 for _, s, _ in results if s == "FAIL")
print(f"  PASS : {pass_count}")
print(f"  FAIL : {fail_count}")
if fail_count == 0:
    print("  VERDICT : ALL PASS")
else:
    print("  VERDICT : FAILURES DETECTED")
    for name, status, détail in results:
        if status == "FAIL":
            print(f"    - {name}: {détail}")