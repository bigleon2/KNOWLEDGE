#!/usr/bin/env python3
"""E13 (session B5) — Réparation de la sérialisation YAML de la Phase 2.

fix-frontmatter.py (dépôt a8ffb5f, byte-identique) complète correctement les
champs frontmatter des skills métier, mais son sérialiseur manuel (to_yaml)
écrit les scalaires SANS quotage : 9 skills dont la description contient
« : » suivi d'un espace (ex. docx « for: (1) ») produisent un frontmatter
YAML invalide (CHECK 8 : YAML_PARSE_ERROR, 67/76).

Ce script (boucle E12-E13 de gen-plan) :
  1. détecte les skills métier dont le frontmatter courant ne parse pas ;
  2. restaure leur frontmatter ORIGINAL depuis le backup pré-Phase-2
     (tool-results/backup-skills-pre-phase2.tar.gz) ;
  3. re-applique la complétion (règles identiques : version 1.0.0,
     category metier, language fr, tags [], dependencies []) ;
  4. sérialise avec yaml.safe_dump (quotage automatique — divergence
     documentée vs le sérialiseur manuel du dépôt).

Garde-fous : le corps de chaque fichier doit être byte-identique entre
l'original (backup) et l'état courant, sinon ABORT sans écriture ;
chaque fichier réparé est re-parsé et re-vérifié avant écriture.

Usage : python3 scripts/repair-frontmatter-yaml.py
"""

import os
import sys
import tarfile

import yaml

BASE = "/home/z/my-project"
SKILLS_ROOT = os.path.join(BASE, "skills")
BACKUP = os.path.join(BASE, "tool-results", "backup-skills-pre-phase2.tar.gz")
ECOSYSTEM = {"gen-plan", "correct-work", "clone-chat", "skills-inventory",
             "skill-creator", "autonomous-agent"}
REQUIRED = ("version", "category", "language", "tags", "dependencies")
ORDER = ("name", "version", "category", "language", "description",
         "tags", "dependencies")


def split_fm(content):
    """(frontmatter_brute, corps) — None si pas de frontmatter."""
    if not content.startswith("---"):
        return None, content
    try:
        end = content.index("---", 3)
    except ValueError:
        return None, content
    return content[3:end].strip(), content[end + 3:].lstrip("\n")


def ordered(fm):
    """Ordre canonique (celui de to_yaml) puis clés restantes."""
    out = {k: fm[k] for k in ORDER if k in fm}
    for k, v in fm.items():
        if k not in out:
            out[k] = v
    return out


def complete(fm, dir_name):
    """Complétion — règles identiques à fix-frontmatter.py."""
    fm.setdefault("name", dir_name)
    fm.setdefault("version", "1.0.0")
    fm.setdefault("category", "metier")
    fm.setdefault("language", "fr")
    fm.setdefault("tags", [])
    fm.setdefault("dependencies", [])
    return fm


def dump_fm(fm):
    return yaml.safe_dump(ordered(fm), sort_keys=False, allow_unicode=True,
                          width=10 ** 6, default_flow_style=False).rstrip("\n")


def main():
    tar = tarfile.open(BACKUP, "r:gz")
    broken, repaired, errors = [], [], []
    for d in sorted(os.listdir(SKILLS_ROOT)):
        if d.startswith("_") or d in ECOSYSTEM or d == "KNOWLEDGE.md":
            continue
        if not os.path.isdir(os.path.join(SKILLS_ROOT, d)):
            continue
        path = os.path.join(SKILLS_ROOT, d, "SKILL.md")
        if not os.path.isfile(path):
            continue
        with open(path, encoding="utf-8") as f:
            current = f.read()
        fm_raw, body = split_fm(current)
        try:
            fm = yaml.safe_load(fm_raw) if fm_raw else None
            parse_ok = isinstance(fm, dict)
        except yaml.YAMLError:
            parse_ok = False
        if parse_ok:
            continue  # frontmatter sain
        broken.append(d)
        member = tar.extractfile(f"skills/{d}/SKILL.md")
        if member is None:
            errors.append(f"{d}: introuvable dans le backup")
            continue
        original = member.read().decode("utf-8")
        ofm_raw, obody = split_fm(original)
        if ofm_raw is None:
            errors.append(f"{d}: original sans frontmatter — non géré")
            continue
        ofm = yaml.safe_load(ofm_raw)
        if not isinstance(ofm, dict):
            errors.append(f"{d}: original non dict — non géré")
            continue
        if obody != body:
            errors.append(f"{d}: corps divergent — ABORT (aucune écriture)")
            continue
        content = "---\n" + dump_fm(complete(ofm, d)) + "\n---\n\n" + body
        chk_raw, _ = split_fm(content)
        chk = yaml.safe_load(chk_raw)
        if not (isinstance(chk, dict) and all(fld in chk for fld in REQUIRED)):
            errors.append(f"{d}: re-vérification post-sérialisation échouée")
            continue
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        repaired.append(d)
    tar.close()
    print(f"Frontmatter YAML invalides détectés : {len(broken)} → {broken}")
    print(f"Réparés (yaml.safe_dump, quotage automatique) : {len(repaired)}")
    if errors:
        print(f"ERREURS (fichiers NON modifiés) : {errors}")
    print("Corps byte-identiques vérifiés pour chaque fichier réparé.")
    return 0 if not errors and len(repaired) == len(broken) else 1


if __name__ == "__main__":
    sys.exit(main())
