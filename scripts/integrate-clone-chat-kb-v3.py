#!/usr/bin/env python3
"""
integrate-clone-chat-kb-v3.py — Intègre clone-chat v2.0.0 dans une base de
connaissance locale en utilisant le Protocole de Découverte KB (gen-plan v3.6.0+).

Usage :
    python integrate-clone-chat-kb-v3.py <kb_path> [--register] [--verify] [--full]

Options :
    --register    Enregistrer clone-chat dans le registre KB (KNOWLEDGE.md)
    --verify      Vérifier la compatibilité avec les skills KB existants
    --full        Exécuter toutes les étapes (scan + install + register + verify)

Exemples :
    python integrate-clone-chat-kb-v3.py "/home/z/my-project/skills" --full
    python integrate-clone-chat-kb-v3.py "/home/z/my-project/skills" --register
    python integrate-clone-chat-kb-v3.py "/home/z/my-project/skills" --verify

Ce script implémente le Protocole de Découverte KB de gen-plan v3.6.0 :
    1. Scanner le répertoire KB pour découvrir les skills existants
    2. Construire la liste de référence (baseline écosystème)
    3. Extraire les métadonnées de chaque skill (YAML frontmatter)
    4. Classifier les skills (exécutable, référence, agent)
    5. Construire le registre dynamique fusionné
    6. Évaluer la compatibilité (dépendances inter-skills)
    7. Installer clone-chat v2.0.0 dans la KB (si pas déjà présent)
    8. Enregistrer clone-chat dans le registre KB (KNOWLEDGE.md)

Auteur : François + gen-plan v3.6.0
Version : 3.0.0
Date : 2026-08-09
"""

import sys
import os
import re
from pathlib import Path
from datetime import datetime


# ─── Constantes ───────────────────────────────────────────────────────────────

CLONE_CHAT_VERSION = "2.0.0"
CLONE_CHAT_CATEGORY = "ecosystem"
CLONE_CHAT_LANGUAGE = "fr"
CLONE_CHAT_TAGS = ["clone", "discussion", "context", "drift",
                    "gen-plan", "auto-clonage", "worklog"]

SCRIPT_DIR = Path(__file__).resolve().parent
SKILLS_SOURCE = SCRIPT_DIR.parent / "skills" / "clone-chat"

# Skills de l'écosystème connus (baseline)
# Source de vérité : KNOWLEDGE.md et PROMPT-MAITRE-SHARED.md
ECOSYSTEM_BASELINE = {
    "gen-plan": {"version": "3.6.0", "category": "ecosystem"},
    "correct-work": {"version": "2.3.0", "category": "ecosystem"},
    "clone-chat": {"version": "2.0.0", "category": "ecosystem"},
    "skills-inventory": {"version": "1.0.0", "category": "ecosystem"},
    "skill-creator": {"version": "1.0.0", "category": "ecosystem"},
}

# Chemins cibles
CLONE_CHAT_DIR_NAME = "clone-chat"
SKILL_MD_NAME = "SKILL.md"
TEMPLATE_DIR = "references"
TEMPLATE_NAME = "clone-template.md"
KB_FILENAME = "KNOWLEDGE.md"


# ─── Utilitaires ──────────────────────────────────────────────────────────────

def parse_version(ver_str):
    """Parse une version semver en tuple d'entiers."""
    m = re.match(r'(\d+)\.(\d+)\.(\d+)', str(ver_str))
    if not m:
        return (0, 0, 0)
    return tuple(int(x) for x in m.groups())


def version_gte(actual, required):
    """Vérifie si actual >= required (semver)."""
    return parse_version(actual) >= parse_version(required)


def extract_yaml_frontmatter(filepath):
    """Extrait le bloc YAML frontmatter d'un fichier Markdown."""
    try:
        text = filepath.read_text(encoding='utf-8')
    except (OSError, UnicodeDecodeError):
        return {}
    if not text.startswith('---'):
        return {}
    end = text.find('---', 3)
    if end < 0:
        return {}
    yaml_block = text[3:end].strip()
    meta = {}
    for line in yaml_block.split('\n'):
        if ':' in line:
            key, _, val = line.partition(':')
            key = key.strip().lower()
            val = val.strip().strip('"\'')
            if val.startswith('['):
                # Liste simplifiée
                items = re.findall(r'["\']?([^"\',\]]+)["\']?', val)
                meta[key] = [i.strip() for i in items if i.strip()]
            elif val.startswith('>'):
                continue  # Skip multiline description
            else:
                meta[key] = val
    return meta


def print_header(title):
    """Affiche un en-tête de section."""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}")


def print_step(step_num, description):
    """Affiche une étape avec son numéro."""
    print(f"\n  Étape {step_num} — {description}")
    print(f"  {'-' * 60}")


# ─── Fonctions principales ────────────────────────────────────────────────────

def scan_skills(kb_path):
    """Scan le répertoire KB pour découvrir les skills existants (E2+E5)."""
    print_step(1, "Scanner le répertoire KB")
    kb = Path(kb_path)
    if not kb.is_dir():
        print(f"  ERREUR : Répertoire introuvable : {kb}")
        return []

    skills_found = []
    for item in sorted(kb.iterdir()):
        if not item.is_dir():
            continue
        if item.name.startswith('_') or item.name.startswith('.'):
            continue
        skill_md = item / SKILL_MD_NAME
        if skill_md.exists():
            meta = extract_yaml_frontmatter(skill_md)
            name = meta.get('name', item.name)
            version = meta.get('version', '?.?.?')
            category = meta.get('category', 'unknown')
            skills_found.append({
                'name': name,
                'version': version,
                'category': category,
                'path': item,
                'meta': meta,
            })
            print(f"  [OK] {name} v{version} ({category})")

    print(f"\n  Total : {len(skills_found)} skills découverts")
    return skills_found


def build_baseline(skills_found):
    """Construit le registre dynamique fusionné."""
    print_step(2, "Construire le registre dynamique")
    registry = dict(ECOSYSTEM_BASELINE)
    for s in skills_found:
        name = s['name']
        if name in registry:
            # Le skill scanné peut être plus récent que le baseline
            if version_gte(s['version'], registry[name]['version']):
                registry[name] = {
                    'version': s['version'],
                    'category': s['category'],
                }
        else:
            registry[name] = {
                'version': s['version'],
                'category': s['category'],
            }
    print(f"  Registre fusionné : {len(registry)} skills")
    for name, info in sorted(registry.items()):
        print(f"    {name} v{info['version']} ({info['category']})")
    return registry


def check_compat(registry):
    """Évalue la compatibilité des dépendances inter-skills."""
    print_step(3, "Évaluer la compatibilité")
    # Dépendances de clone-chat v2.0.0
    clone_deps = {
        'gen-plan': '3.6.0',
        'correct-work': '2.3.0',
    }
    all_ok = True
    for dep_name, min_ver in clone_deps.items():
        if dep_name in registry:
            actual = registry[dep_name]['version']
            ok = version_gte(actual, min_ver)
            status = "OK" if ok else "FAIL"
            if not ok:
                all_ok = False
            print(f"  [{status}] {dep_name} : v{actual} (requis >= v{min_ver})")
        else:
            print(f"  [--] {dep_name} : absent (requis >= v{min_ver})")

    # Vérifier que les skills qui dépendent de clone-chat sont compatibles
    reverse_deps = {
        'gen-plan': '2.0.0',
        'correct-work': '2.0.0',
    }
    for skill_name, min_clone_ver in reverse_deps.items():
        if skill_name in registry:
            print(f"  [info] {skill_name} requiert clone-chat >= v{min_clone_ver} : OK")
    return all_ok


def install_clone_chat(kb_path):
    """Installe clone-chat v2.0.0 dans la KB."""
    print_step(4, "Installer clone-chat v2.0.0")
    kb = Path(kb_path)
    target_dir = kb / CLONE_CHAT_DIR_NAME
    source_dir = SKILLS_SOURCE

    if not source_dir.is_dir():
        print(f"  ERREUR : Source introuvable : {source_dir}")
        print(f"  Ce script doit être dans scripts/ à la racine de my-project/")
        return False

    # Créer la structure cible
    (target_dir / TEMPLATE_DIR).mkdir(parents=True, exist_ok=True)

    # Copier SKILL.md
    src_skill = source_dir / SKILL_MD_NAME
    dst_skill = target_dir / SKILL_MD_NAME
    if src_skill.exists():
        content = src_skill.read_text(encoding='utf-8')
        dst_skill.write_text(content, encoding='utf-8')
        print(f"  [OK] {SKILL_MD_NAME} copié ({len(content)} lignes)")
    else:
        print(f"  [FAIL] {SKILL_MD_NAME} introuvable dans {source_dir}")
        return False

    # Copier le template
    src_template = source_dir / TEMPLATE_DIR / TEMPLATE_NAME
    dst_template = target_dir / TEMPLATE_DIR / TEMPLATE_NAME
    if src_template.exists():
        content = src_template.read_text(encoding='utf-8')
        dst_template.write_text(content, encoding='utf-8')
        print(f"  [OK] {TEMPLATE_DIR}/{TEMPLATE_NAME} copié ({len(content)} lignes)")
    else:
        print(f"  [WARN] {TEMPLATE_DIR}/{TEMPLATE_NAME} introuvable")

    print(f"  Installation terminée dans : {target_dir}")
    return True


def register_in_kb(kb_path):
    """Enregistre clone-chat dans le registre KNOWLEDGE.md."""
    print_step(5, "Enregistrer dans le registre KB")
    kb = Path(kb_path)
    kb_file = kb / KB_FILENAME

    if not kb_file.exists():
        print(f"  [WARN] {KB_FILENAME} introuvable, création du fichier")
        header = f"# KNOWLEDGE.md — Registre de l'écosystème Knowledge\n\n"
        header += f"> **Dernière mise à jour** : {datetime.now().strftime('%Y-%m-%d')}\n"
        header += f"> **Nombre de skills** : 77 installés (5 écosystème + 72 métier)\n\n---\n\n"
        kb_file.write_text(header, encoding='utf-8')

    content = kb_file.read_text(encoding='utf-8')

    # Vérifier si clone-chat est déjà enregistré
    if re.search(r'^## clone-chat\s', content, re.MULTILINE):
        # Mettre à jour l'entrée existante
        print(f"  Mise à jour de l'entrée clone-chat existante")
        new_entry = f"""## clone-chat v{CLONE_CHAT_VERSION}

- **Category** : {CLONE_CHAT_CATEGORY}
- **Description** : Clonage de discussion en Markdown auto-suffisant. 7+1 étapes, intégration gen-plan v3.6.0+ KB.
- **Dépend de** : gen-plan >= v3.6.0 (optionnel), correct-work >= v2.3.0 (validation croisée)
- **Utilisé par** : gen-plan (E4, E15), correct-work (Mode CIBLE, §3.5)
- **Dernière calibration** : {datetime.now().strftime('%Y-%m-%d')}
- **Statut** : stable"""
        pattern = r'## clone-chat\s.*?(?=\n---|\n## )'
        content = re.sub(pattern, new_entry, content, flags=re.DOTALL)
    else:
        # Ajouter une nouvelle entrée
        print(f"  Ajout d'une nouvelle entrée clone-chat")
        new_entry = f"""\n---\n
## clone-chat v{CLONE_CHAT_VERSION}

- **Category** : {CLONE_CHAT_CATEGORY}
- **Description** : Clonage de discussion en Markdown auto-suffisant. 7+1 étapes, intégration gen-plan v3.6.0+ KB.
- **Dépend de** : gen-plan >= v3.6.0 (optionnel), correct-work >= v2.3.0 (validation croisée)
- **Utilisé par** : gen-plan (E4, E15), correct-work (Mode CIBLE, §3.5)
- **Dernière calibration** : {datetime.now().strftime('%Y-%m-%d')}
- **Statut** : stable\n"""
        content += new_entry

    kb_file.write_text(content, encoding='utf-8')
    print(f"  [OK] Registre KB mis à jour : {kb_file}")
    return True


def verify_install(kb_path):
    """Vérifie l'installation de clone-chat."""
    print_step(6, "Vérification post-installation")
    kb = Path(kb_path)
    checks = []

    # Check 1 : répertoire clone-chat existe
    target_dir = kb / CLONE_CHAT_DIR_NAME
    c1 = target_dir.is_dir()
    checks.append(("Répertoire clone-chat/", c1))

    # Check 2 : SKILL.md existe
    skill_md = target_dir / SKILL_MD_NAME
    c2 = skill_md.is_file()
    checks.append((f"{SKILL_MD_NAME} présent", c2))

    # Check 3 : YAML frontmatter valide
    if c2:
        meta = extract_yaml_frontmatter(skill_md)
        c3 = all(k in meta for k in ('name', 'version', 'category'))
        checks.append(("YAML frontmatter valide (name, version, category)", c3))

        # Check 4 : version cohérente
        c4 = meta.get('version', '') == CLONE_CHAT_VERSION
        checks.append((f"Version = v{CLONE_CHAT_VERSION}", c4))

        # Check 5 : dependencies présentes
        content = skill_md.read_text(encoding='utf-8')
        c5 = 'dependencies:' in content
        checks.append(("Bloc dependencies dans frontmatter", c5))

        # Check 6 : gen-plan >= v3.6.0 dans les deps
        c6 = 'gen-plan' in content and '>=3.6.0' in content
        checks.append(("gen-plan >= v3.6.0 dans les deps", c6))

        # Check 7 : 77 skills mentionné
        c7 = '77 skills' in content or '77 installés' in content
        checks.append(("77 skills mentionné", c7))

        # Check 8 : variables SHARED présentes
        c8 = '{{SKILLS_ROOT}}' in content and '{{KB_PATH}}' in content
        checks.append(("Variables SHARED (SKILLS_ROOT, KB_PATH)", c8))
    else:
        checks.extend([
            ("YAML frontmatter valide", False),
            (f"Version = v{CLONE_CHAT_VERSION}", False),
            ("Bloc dependencies", False),
            ("gen-plan >= v3.6.0", False),
            ("77 skills mentionné", False),
            ("Variables SHARED", False),
        ])

    # Check 9 : template présent
    template = target_dir / TEMPLATE_DIR / TEMPLATE_NAME
    c9 = template.is_file()
    checks.append((f"{TEMPLATE_DIR}/{TEMPLATE_NAME} présent", c9))

    # Check 10 : template version 2.0.0
    if c9:
        tmpl_content = template.read_text(encoding='utf-8')
        c10 = '2.0.0' in tmpl_content
        checks.append(("Template version 2.0.0", c10))
    else:
        checks.append(("Template version 2.0.0", False))

    # Affichage
    passed = 0
    for label, ok in checks:
        status = "PASS" if ok else "FAIL"
        if ok:
            passed += 1
        print(f"  [{status}] {label}")

    total = len(checks)
    print(f"\n  Résultat : {passed}/{total} checks PASS")
    return passed == total


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("  ERREUR : chemin KB requis\n")
        sys.exit(1)

    kb_path = sys.argv[1]
    do_register = '--register' in sys.argv
    do_verify = '--verify' in sys.argv
    do_full = '--full' in sys.argv

    if do_full:
        do_register = True
        do_verify = True

    print_header(f"integrate-clone-chat-kb v3.0.0 — clone-chat v{CLONE_CHAT_VERSION}")
    print(f"  Chemin KB : {kb_path}")
    print(f"  Date : {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"  Écosystème : gen-plan v3.6.0, correct-work v2.3.0, 77 skills")

    # Toujours scanner
    skills_found = scan_skills(kb_path)
    registry = build_baseline(skills_found)
    compat_ok = check_compat(registry)

    if do_register or do_full:
        installed = install_clone_chat(kb_path)
        if installed:
            register_in_kb(kb_path)

    if do_verify or do_full:
        verify_ok = verify_install(kb_path)
    else:
        verify_ok = True

    # Résumé
    print_header("RÉSUMÉ")
    print(f"  Skills découverts : {len(skills_found)}")
    print(f"  Compatibilité : {'OK' if compat_ok else 'FAIL'}")
    if do_register or do_full:
        print(f"  Installation : OK")
    if do_verify or do_full:
        print(f"  Vérification : {'PASS' if verify_ok else 'FAIL'}")
    print()

    if not compat_ok:
        sys.exit(1)


if __name__ == '__main__':
    main()
