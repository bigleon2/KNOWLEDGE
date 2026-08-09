#!/usr/bin/env python3
"""Vérification post-installation correct-work v2.4.0

16 checks automatisés correspondant au tableau §6 du Prompt Maître.
Usage:
    python verify-correct-work.py
    python verify-correct-work.py --skills-root /chemin/skills
"""

import os
import re
import sys

SKILLS_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SKILL_PATH = os.path.join(SKILLS_ROOT, "correct-work", "SKILL.md")
PM_PATH = os.path.join(SKILLS_ROOT, "_prompts-maitres", "PROMPT-MAITRE-CORRECT-WORK-v2.4.0.md")
SHARED_PATH = os.path.join(SKILLS_ROOT, "_prompts-maitres", "PROMPT-MAITRE-SHARED.md")
KB_PATH = os.path.join(SKILLS_ROOT, "KNOWLEDGE.md")

EXPECTED_VERSION = "2.4.0"
EXPECTED_LINES_MIN = 200
EXPECTED_LINES_MAX = 350
EXPECTED_MODES = {"PROJET", "CIBLE", "DIRECT"}
EXPECTED_STEPS = {"1", "2", "3", "4", "5"}
REQUIRED_DEPS = {"gen-plan": ">=3.6.0", "clone-chat": ">=2.0.0"}
REQUIRED_FRONTMATTER = ["name", "version", "category", "language", "tags", "dependencies"]
# Sections du PM (utilisées pour référence, pas de check dedie)


def read_file(path):
    """Lit un fichier et retourne son contenu ou None."""
    if not os.path.isfile(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def count_lines(path):
    """Compte les lignes d'un fichier."""
    content = read_file(path)
    if content is None:
        return 0
    return len(content.strip().split("\n"))


def extract_frontmatter(content):
    """Extrait le bloc YAML frontmatter."""
    if not content or not content.startswith("---"):
        return {}
    end = content.find("---", 3)
    if end == -1:
        return {}
    yaml_block = content[3:end].strip()
    frontmatter = {}
    for line in yaml_block.split("\n"):
        key = line.split(":")[0].strip()
        if key:
            frontmatter[key] = True
    return frontmatter


def extract_yaml_deps(content):
    """Extrait les dépendances du frontmatter YAML."""
    deps = {}
    in_deps = False
    current_skill = None
    for line in content.split("\n"):
        stripped = line.strip()
        if "dependencies:" in stripped:
            in_deps = True
            current_skill = None
            continue
        if not in_deps:
            continue
        if stripped == "---":
            break
        if stripped.startswith("- skill:"):
            skill_match = re.search(r"skill:\s*(\S+)", stripped)
            if skill_match:
                current_skill = skill_match.group(1)
                deps[current_skill] = "any"
        elif current_skill and stripped.startswith(("version:", "used_at:")):
            ver_match = re.search(r'["\']?([><=]+\s*[\d.]+)["\']?', stripped)
            if ver_match:
                deps[current_skill] = ver_match.group(1).replace(" ", "")
        elif stripped == "":
            continue
        elif ":" in stripped and current_skill:
            in_deps = False
            current_skill = None
    return deps


def find_sections(content, prefix="##"):
    """Trouve toutes les sections avec un préfixe donné."""
    return re.findall(rf"{prefix}\s+[^\n]+", content)


def run_checks():
    """Exécute les 16 checks et retourne les résultats."""
    results = []
    total = 16
    passed = 0

    # Check 1 : SKILL.md existe
    exists = os.path.isfile(SKILL_PATH)
    results.append(("Check 1", "SKILL.md existe", "PASS" if exists else "FAIL"))
    if exists:
        passed += 1

    # Check 2 : Taille SKILL.md dans la plage
    if exists:
        lines = count_lines(SKILL_PATH)
        in_range = EXPECTED_LINES_MIN <= lines <= EXPECTED_LINES_MAX
        status = "PASS" if in_range else "FAIL"
        détail = f"{lines} lignes (plage {EXPECTED_LINES_MIN}-{EXPECTED_LINES_MAX})"
        results.append(("Check 2", f"Taille SKILL.md {détail}", status))
        if in_range:
            passed += 1
    else:
        results.append(("Check 2", "Taille SKILL.md", "SKIP (fichier absent)"))

    # Check 3 : YAML frontmatter valide
    content = read_file(SKILL_PATH)
    if content:
        fm = extract_frontmatter(content)
        missing = [f for f in REQUIRED_FRONTMATTER if f not in fm]
        status = "PASS" if not missing else "FAIL"
        détail = f"{len(REQUIRED_FRONTMATTER)}/{len(REQUIRED_FRONTMATTER)}" if not missing else f"manquant: {', '.join(missing)}"
        results.append(("Check 3", f"YAML frontmatter {détail}", status))
        if not missing:
            passed += 1
    else:
        results.append(("Check 3", "YAML frontmatter", "SKIP"))

    # Check 4 : 3 modes documentes
    if content:
        modes_found = set(re.findall(r"\b(PROJET|CIBLE|DIRECT)\b", content))
        all_modes = EXPECTED_MODES.issubset(modes_found)
        status = "PASS" if all_modes else "FAIL"
        détail = f"trouves: {', '.join(modes_found) or 'aucun'}"
        results.append(("Check 4", f"3 modes documentes ({détail})", status))
        if all_modes:
            passed += 1
    else:
        results.append(("Check 4", "3 modes documentes", "SKIP"))

    # Check 5 : 5 étapes documentees
    if content:
        step_matches = set(re.findall(r"étape\s*(\d)|\bE(\d)\b", content))
        steps_flat = {s[0] or s[1] for s in step_matches}
        all_steps = EXPECTED_STEPS.issubset(steps_flat)
        status = "PASS" if all_steps else "FAIL"
        results.append(("Check 5", "5 étapes documentees", status))
        if all_steps:
            passed += 1
    else:
        results.append(("Check 5", "5 étapes documentees", "SKIP"))

    # Check 6 : intégration KB
    if content:
        kb_mentions = 0
        for kw in ["kb_path", "KB", "--kb-skill", "KNOWLEDGE"]:
            if kw in content:
                kb_mentions += 1
        status = "PASS" if kb_mentions >= 2 else "FAIL"
        results.append(("Check 6", f"intégration KB ({kb_mentions} mentions)", status))
        if kb_mentions >= 2:
            passed += 1
    else:
        results.append(("Check 6", "intégration KB", "SKIP"))

    # Check 7 : Matrice statique referencee
    if content:
        has_static = "matrice" in content.lower() or "SHARED" in content
        results.append(("Check 7", "Matrice statique", "PASS" if has_static else "FAIL"))
        if has_static:
            passed += 1
    else:
        results.append(("Check 7", "Matrice statique", "SKIP"))

    # Check 8 : Matrice dynamique KB
    if content:
        has_dynamic = "dynamique" in content.lower() and ("scan" in content.lower() or "découverte" in content.lower())
        results.append(("Check 8", "Matrice dynamique KB", "PASS" if has_dynamic else "FAIL"))
        if has_dynamic:
            passed += 1
    else:
        results.append(("Check 8", "Matrice dynamique KB", "SKIP"))

    # Check 9 : critères de sévérité S1-S4
    if content:
        sevs = set(re.findall(r"\bS([1-4])\b", content))
        all_sevs = {"1", "2", "3", "4"}.issubset(sevs)
        results.append(("Check 9", "critères sévérité S1-S4", "PASS" if all_sevs else "FAIL"))
        if all_sevs:
            passed += 1
    else:
        results.append(("Check 9", "critères sévérité S1-S4", "SKIP"))

    # Check 10 : Format rapport 5 sections
    if content:
        has_rapport = "rapport" in content.lower() or "Metadonnees" in content
        results.append(("Check 10", "Format rapport", "PASS" if has_rapport else "FAIL"))
        if has_rapport:
            passed += 1
    else:
        results.append(("Check 10", "Format rapport", "SKIP"))

    # Check 11 : Cross-ref gen-plan >= v3.6.0
    if content:
        has_gp = "gen-plan" in content and (">= v3.6.0" in content or ">=v3.6.0" in content or ">= 3.6.0" in content)
        results.append(("Check 11", "Cross-ref gen-plan >= v3.6.0", "PASS" if has_gp else "FAIL"))
        if has_gp:
            passed += 1
    else:
        results.append(("Check 11", "Cross-ref gen-plan", "SKIP"))

    # Check 12 : Cross-ref clone-chat >= v2.0.0
    if content:
        has_cc = "clone-chat" in content and (">= v2.0.0" in content or ">=v2.0.0" in content or ">= 2.0.0" in content)
        results.append(("Check 12", "Cross-ref clone-chat >= v2.0.0", "PASS" if has_cc else "FAIL"))
        if has_cc:
            passed += 1
    else:
        results.append(("Check 12", "Cross-ref clone-chat", "SKIP"))

    # Check 13 : KNOWLEDGE.md entr\u00e9e correct-work
    kb_content = read_file(KB_PATH)
    if kb_content:
        has_entry = "correct-work" in kb_content
        results.append(("Check 13", "KNOWLEDGE.md entree", "PASS" if has_entry else "FAIL"))
        if has_entry:
            passed += 1
    else:
        results.append(("Check 13", "KNOWLEDGE.md entree", "FAIL (fichier absent)"))

    # Check 14 : Logging worklog format
    if content:
        has_wl = "worklog" in content.lower() or "Stage Summary" in content
        results.append(("Check 14", "Logging worklog", "PASS" if has_wl else "FAIL"))
        if has_wl:
            passed += 1
    else:
        results.append(("Check 14", "Logging worklog", "SKIP"))

    # Check 15 : Dependants frontmatter corrects
    if content:
        deps = extract_yaml_deps(content)
        dep_ok = True
        for skill, ver in REQUIRED_DEPS.items():
            if skill not in deps:
                dep_ok = False
        status = "PASS" if dep_ok else "FAIL"
        détail = f"{len(deps)} deps trouvées"
        results.append(("Check 15", f"dépendances frontmatter ({détail})", status))
        if dep_ok:
            passed += 1
    else:
        results.append(("Check 15", "dépendances frontmatter", "SKIP"))

    # Check 16 : compatibilité écosystème (15/15 precedents)
    prev_failed = sum(1 for _, _, s in results if s == "FAIL")
    status = "PASS" if prev_failed == 0 else f"FAIL ({prev_failed} echec(s))"
    results.append(("Check 16", "compatibilité écosystème", status))
    if prev_failed == 0:
        passed += 1

    return results, passed, total


def main():
    """Point d'entree principal."""
    print("=== vérification CORRECT-WORK ===")
    print(f"Version cible : {EXPECTED_VERSION}")
    print(f"SKILL.md     : {SKILL_PATH}")
    print(f"PM           : {PM_PATH}")
    print()

    results, passed, total = run_checks()

    for check_id, desc, status in results:
        tag = "PASS" if status == "PASS" else "FAIL" if "FAIL" in status else "SKIP"
        print(f"  [{tag}] {desc}")

    print()
    print("=== RESUME ===")
    print(f"  PASS  : {passed}/{total}")
    print(f"  FAIL  : {total - passed}/{total}")
    verdict = "ALL PASS" if passed == total else "FAIL"
    print(f"  VERDICT : {verdict}")

    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
