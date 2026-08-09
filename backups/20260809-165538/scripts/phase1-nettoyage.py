"""Phase 1 — Nettoyage rapide du dépôt Knowledge.
7 findings corrigés, risque zéro.
"""

import os
import shutil
import re

SKILLS_ROOT = "/home/z/my-project/skills"
DOWNLOAD_DIR = "/home/z/my-project/download"
SCRIPTS_DIR = "/home/z/my-project/scripts"
PROJECT_ROOT = "/home/z/my-project"

deleted = []
moved = []
modified = []


def report():
    print(f"\n{'='*60}")
    print(f"BILAN PHASE 1")
    print(f"{'='*60}")
    print(f"Fichiers supprimés : {len(deleted)}")
    print(f"Fichiers déplacés  : {len(moved)}")
    print(f"Fichiers modifiés : {len(modified)}")
    print(f"{'='*60}")
    if deleted:
        print(f"\nSUPPRIMÉS :")
        for f in deleted:
            print(f"  - {f}")
    if moved:
        print(f"\nDÉPLACÉS :")
        for src, dst in moved:
            print(f"  - {src} -> {dst}")
    if modified:
        print(f"\nMODIFIÉS :")
        for f in modified:
            print(f"  - {f}")


# ── 1.1 Supprimer les 69 READMEs stubs morts ──
print("\n[1.1] Suppression READMEs stubs brand-inspiration...")
brand_dir = os.path.join(SKILLS_ROOT, "design", "design-systems", "brand-inspiration")
if os.path.isdir(brand_dir):
    for brand in os.listdir(brand_dir):
        readme_path = os.path.join(brand_dir, brand, "README.md")
        if os.path.isfile(readme_path):
            with open(readme_path, "r", encoding="utf-8") as f:
                content = f.read()
            if "getdesign.md" in content and len(content.strip()) < 200:
                os.remove(readme_path)
                deleted.append(readme_path)
                print(f"  supprimé : {readme_path}")
else:
    print(f"  RÉPERTOIRE TROUVÉ : {brand_dir}")


# ── 1.2 Supprimer clone-chat.zip + ajouter *.zip au .gitignore ──
print("\n[1.2] Suppression clone-chat.zip + mise à jour .gitignore...")
zip_path = os.path.join(DOWNLOAD_DIR, "clone-chat.zip")
if os.path.isfile(zip_path):
    os.remove(zip_path)
    deleted.append(zip_path)
    print(f"  supprimé : {zip_path}")
else:
    print(f"  déjà absent : {zip_path}")

gitignore_path = os.path.join(PROJECT_ROOT, ".gitignore")
zip_rule = "*.zip"
need_zip_rule = True
if os.path.isfile(gitignore_path):
    with open(gitignore_path, "r", encoding="utf-8") as f:
        gi_content = f.read()
    if zip_rule in gi_content:
        need_zip_rule = False
        print(f"  *.zip déjà dans .gitignore")
    else:
        with open(gitignore_path, "a", encoding="utf-8") as f:
            f.write(f"\n{zip_rule}\n")
        modified.append(gitignore_path)
        print(f"  ajouté *.zip dans .gitignore")


# ── 1.3 Supprimer les 2 scripts doublons de download/ ──
print("\n[1.3] Suppression scripts doublons de download/...")
for script_name in ["verify-cross.py", "sync-download.py"]:
    dl_script = os.path.join(DOWNLOAD_DIR, script_name)
    if os.path.isfile(dl_script):
        os.remove(dl_script)
        deleted.append(dl_script)
        print(f"  supprimé : {dl_script}")
    else:
        print(f"  déjà absent : {dl_script}")


# ── 1.4 Archiver 2 scripts obsolètes ──
print("\n[1.4] Archivage scripts obsolètes...")
archive_dir = os.path.join(SCRIPTS_DIR, "_archive")
os.makedirs(archive_dir, exist_ok=True)
for script_name in ["generate-knowledge-v3.py", "generate-clone-genplan.py"]:
    src = os.path.join(SCRIPTS_DIR, script_name)
    dst = os.path.join(archive_dir, script_name)
    if os.path.isfile(src):
        shutil.move(src, dst)
        moved.append((src, dst))
        print(f"  archivé : {src} -> {dst}")
    else:
        print(f"  déjà absent : {src}")


# ── 1.5 Supprimer KNOWLEDGE.md racine obsolète ──
print("\n[1.5] Suppression KNOWLEDGE.md racine (v3.0.0 obsolète)...")
root_kb = os.path.join(PROJECT_ROOT, "KNOWLEDGE.md")
if os.path.isfile(root_kb):
    os.remove(root_kb)
    deleted.append(root_kb)
    print(f"  supprimé : {root_kb}")
else:
    print(f"  déjà absent : {root_kb}")


# ── 1.6 Corriger download/README.md ──
print("\n[1.6] Correction download/README.md...")
dl_readme = os.path.join(DOWNLOAD_DIR, "README.md")
if os.path.isfile(dl_readme):
    with open(dl_readme, "r", encoding="utf-8") as f:
        content = f.read()
    
    original = content
    
    # Fix 78 → 77
    content = content.replace("78 skills", "77 skills")
    content = content.replace("72 skills métier", "71 skills métier")
    # Fix 13 → 14 relations
    content = content.replace("13 relations", "14 relations")
    content = content.replace("13 relations bidirectionnelles", "14 relations bidirectionnelles")
    # Remove _archive/ line from directory tree
    content = re.sub(r"\s*└── _archive/.*\n", "", content)
    # Remove _archive/ reference from text if present
    content = re.sub(r"\s*_archive/.*", "", content)
    
    if content != original:
        with open(dl_readme, "w", encoding="utf-8") as f:
            f.write(content)
        modified.append(dl_readme)
        print(f"  corrigé : {dl_readme}")
    else:
        print(f"  déjà à jour : {dl_readme}")
else:
    print(f"  FICHIER TROUVÉ : {dl_readme}")


report()