#!/usr/bin/env python3
"""Synchronisation download/ depuis skills/_prompts-maitres/ (source de vérité).

Usage:
    python3 scripts/sync-download.py              # mode CHECK (dry-run, affiche les écarts)
    python3 scripts/sync-download.py --sync        # mode SYNC (copie effective)
    python3 scripts/sync-download.py --sync --force # mode SYNC sans confirmation
"""

import os
import sys
import filecmp

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_DIR = os.path.join(BASE_DIR, "skills", "_prompts-maitres")
DEST_DIR = os.path.join(BASE_DIR, "download")

# Mapping source → destination (fichiers à synchroniser)
# Le script integrate-clone-chat-kb-v3.py est EXCLU : c'est un doublon
# de scripts/ qui ne relève pas des prompts maîtres.
SYNC_MAP = [
    ("PROMPT-MAITRE-SHARED.md",              "PROMPT-MAITRE-SHARED.md"),
    ("PROMPT-MAITRE-GEN-PLAN-v3.6.1.md",     "PROMPT-MAITRE-GEN-PLAN-v3.6.1.md"),
    ("PROMPT-MAITRE-CORRECT-WORK-v2.4.0.md", "PROMPT-MAITRE-CORRECT-WORK-v2.4.0.md"),
    ("PROMPT-MAITRE-CLONE-CHAT-v2.0.0.md",   "PROMPT-MAITRE-CLONE-CHAT-v2.0.0.md"),
    ("README.md",                             "README.md"),
]

# Fichiers attendus dans download/ mais HORS sync (à surveiller séparément)
EXCLUDED_FROM_SYNC = ["integrate-clone-chat-kb-v3.py"]


def line_count(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return sum(1 for _ in f)


def check_sync():
    """Mode CHECK : compare source et dest, affiche un rapport."""
    print("=== SYNC CHECK : download/ vs skills/_prompts-maitres/ ===\n")

    all_ok = True
    diffs = []

    for src_name, dst_name in SYNC_MAP:
        src_path = os.path.join(SOURCE_DIR, src_name)
        dst_path = os.path.join(DEST_DIR, dst_name)

        if not os.path.exists(src_path):
            print(f"  [ERREUR] Source manquante : {src_path}")
            all_ok = False
            continue

        if not os.path.exists(dst_path):
            print(f"  [MANQUANT] {dst_name} — absent de download/")
            diffs.append((dst_name, "absent", None, None))
            all_ok = False
            continue

        if filecmp.cmp(src_path, dst_path, shallow=False):
            src_lines = line_count(src_path)
            print(f"  [OK] {dst_name} ({src_lines} lignes)")
        else:
            all_ok = False
            src_lines = line_count(src_path)
            dst_lines = line_count(dst_path)
            delta = src_lines - dst_lines
            sign = "+" if delta > 0 else ""
            diffs.append((dst_name, "divergent", src_lines, dst_lines))
            print(f"  [ÉCART] {dst_name} : source={src_lines}L, download={dst_lines}L (delta={sign}{delta})")

    # Vérifier les fichiers exclus
    print(f"\n  Fichiers exclus du sync : {EXCLUDED_FROM_SYNC}")
    for excl in EXCLUDED_FROM_SYNC:
        excl_path = os.path.join(DEST_DIR, excl)
        if os.path.exists(excl_path):
            scripts_path = os.path.join(BASE_DIR, "scripts", excl)
            if os.path.exists(scripts_path):
                if filecmp.cmp(excl_path, scripts_path, shallow=False):
                    print(f"  [INFO] {excl} : doublon identique de scripts/ (non syncisé)")
                else:
                    print(f"  [AVERTISSEMENT] {excl} : DIFFÈRE de scripts/ — supprimer ou syncer manuellement")
            else:
                print(f"  [INFO] {excl} : pas de contrepartie dans scripts/")

    print(f"\n=== RÉSUMÉ ===")
    if all_ok:
        print("  VERDICT : SYNC OK — download/ est à jour")
    else:
        print(f"  VERDICT : SYNC NÉCESSAIRE — {len(diffs)} fichier(s) en écart")
        for name, status, src_l, dst_l in diffs:
            if status == "absent":
                print(f"    - {name} : à créer")
            else:
                print(f"    - {name} : source={src_l}L, download={dst_l}L")
        print(f"\n  → Lancez : python3 scripts/sync-download.py --sync")

    return 0 if all_ok else 1


def do_sync(force=False):
    """Mode SYNC : copie les fichiers source vers download/."""
    print("=== SYNC : skills/_prompts-maitres/ → download/ ===\n")

    # D'abord, afficher l'état
    needs_sync = False
    for src_name, dst_name in SYNC_MAP:
        src_path = os.path.join(SOURCE_DIR, src_name)
        dst_path = os.path.join(DEST_DIR, dst_name)
        if os.path.exists(src_path) and os.path.exists(dst_path):
            if not filecmp.cmp(src_path, dst_path, shallow=False):
                needs_sync = True
                break
        elif os.path.exists(src_path):
            needs_sync = True
            break

    if not needs_sync:
        print("  download/ est déjà à jour. Rien à faire.")
        return 0

    # Confirmation (sauf --force)
    if not force:
        print("  Fichiers qui seront écrasés/mis à jour :")
        for src_name, dst_name in SYNC_MAP:
            src_path = os.path.join(SOURCE_DIR, src_name)
            dst_path = os.path.join(DEST_DIR, dst_name)
            if os.path.exists(src_path):
                if os.path.exists(dst_path) and not filecmp.cmp(src_path, dst_path, shallow=False):
                    print(f"    - {dst_name} (mis à jour)")
                elif not os.path.exists(dst_path):
                    print(f"    - {dst_name} (créé)")
        print()
        try:
            resp = input("  Confirmer la synchronisation ? [o/N] ").strip().lower()
            if resp != "o":
                print("  Annulé.")
                return 1
        except (EOFError, KeyboardInterrupt):
            print("  Annulé.")
            return 1

    # Exécuter la copie (uniquement les fichiers différents)
    copied = 0
    skipped = 0
    for src_name, dst_name in SYNC_MAP:
        src_path = os.path.join(SOURCE_DIR, src_name)
        dst_path = os.path.join(DEST_DIR, dst_name)
        if not os.path.exists(src_path):
            print(f"  [ERREUR] Source manquante : {src_name}")
            continue
        if os.path.exists(dst_path) and filecmp.cmp(src_path, dst_path, shallow=False):
            skipped += 1
            continue
        with open(src_path, "r", encoding="utf-8") as f:
            content = f.read()
        with open(dst_path, "w", encoding="utf-8") as f:
            f.write(content)
        lines = content.count("\n") + 1
        print(f"  [SYNC] {dst_name} → {lines} lignes")
        copied += 1

    if skipped > 0:
        print(f"  {skipped} fichier(s) déjà à jour (ignorés).")
    print(f"  {copied} fichier(s) synchronisé(s).")
    return 0


def main():
    args = sys.argv[1:]
    if "--sync" in args:
        force = "--force" in args
        return do_sync(force=force)
    else:
        return check_sync()


if __name__ == "__main__":
    sys.exit(main())
