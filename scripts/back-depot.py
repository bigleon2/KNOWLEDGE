#!/usr/bin/env python3
"""back-depot.py — Sauvegarde fidèle et restauration du dépôt Knowledge.

Usage:
    python3 scripts/back-depot.py                    # Affiche l'aide
    python3 scripts/back-depot.py backup             # Sauvegarde complète
    python3 scripts/back-depot.py backup --skills-only  # Sauvegarde skills/ seulement
    python3 scripts/back-depot.py list               # Liste les sauvegardes
    python3 scripts/back-depot.py restore <timestamp> # Restaure une sauvegarde
    python3 scripts/back-depot.py info <timestamp>   # Détails d'une sauvegarde

Sauvegardes stockées dans : /home/z/my-project/backups/
"""

import os
import sys
import json
import shutil
import hashlib
from datetime import datetime

PROJECT_ROOT = "/home/z/my-project"
BACKUP_DIR = os.path.join(PROJECT_ROOT, "backups")
METADATA_FILE = os.path.join(BACKUP_DIR, "backups-registry.json")

# Répertoires et fichiers à sauvegarder (fidélité complète)
BACKUP_TARGETS = [
    "skills/",
    "scripts/",
    "download/",
    "mini-services/",
    "worklog.md",
    ".gitignore",
]

# Exclusions (à l'intérieur des répertoires ciblés)
EXCLUDE_PATTERNS = [
    "__pycache__",
    ".DS_Store",
    "*.pyc",
    ".pytest_cache",
    "*.egg-info",
]


def should_exclude(rel_path):
    """Check if a path matches any exclusion pattern."""
    for pattern in EXCLUDE_PATTERNS:
        if pattern.startswith("*"):
            if rel_path.endswith(pattern[1:]):
                return True
        elif pattern in rel_path.split(os.sep):
            return True
    return False


def compute_file_hash(filepath):
    """Compute SHA-256 hash of a file."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def scan_target(target_rel, base):
    """Scan a target directory/file. Returns (files_list, total_size)."""
    files = []
    total_size = 0
    full_path = os.path.join(base, target_rel.rstrip("/"))

    if os.path.isfile(full_path):
        size = os.path.getsize(full_path)
        fhash = compute_file_hash(full_path)
        files.append({
            "rel": target_rel,
            "size": size,
            "sha256": fhash,
        })
        return files, size

    if not os.path.isdir(full_path):
        return files, 0

    for root, dirs, filenames in os.walk(full_path):
        # Filter excluded dirs in-place
        dirs[:] = [d for d in dirs if not should_exclude(d)]
        for fname in filenames:
            if should_exclude(fname):
                continue
            fpath = os.path.join(root, fname)
            rel = os.path.relpath(fpath, base)
            size = os.path.getsize(fpath)
            fhash = compute_file_hash(fpath)
            files.append({
                "rel": rel,
                "size": size,
                "sha256": fhash,
            })
            total_size += size

    return files, total_size


def do_backup(skills_only=False):
    """Create a timestamped backup."""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_path = os.path.join(BACKUP_DIR, timestamp)
    os.makedirs(backup_path, exist_ok=True)

    targets = ["skills/"] if skills_only else BACKUP_TARGETS
    all_files = []
    total_size = 0
    total_files = 0

    print(f"Sauvegarde: {timestamp}")
    print(f"Cible: {PROJECT_ROOT}")
    print(f"Destination: {backup_path}")
    print()

    for target in targets:
        files, size = scan_target(target, PROJECT_ROOT)
        all_files.extend(files)
        total_size += size

        # Copy files preserving structure
        for finfo in files:
            src = os.path.join(PROJECT_ROOT, finfo["rel"])
            dst = os.path.join(backup_path, finfo["rel"])
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)

        print(f"  {target:30s} {len(files):4d} fichiers  {size/1024/1024:8.2f} MB")

    total_files = len(all_files)

    # Save manifest
    manifest = {
        "timestamp": timestamp,
        "date": datetime.now().isoformat(),
        "mode": "skills-only" if skills_only else "full",
        "total_files": total_files,
        "total_size": total_size,
        "targets": targets,
        "files": all_files,
    }
    manifest_path = os.path.join(backup_path, "MANIFEST.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    # Update registry
    registry = load_registry()
    registry[timestamp] = {
        "date": datetime.now().isoformat(),
        "mode": manifest["mode"],
        "total_files": total_files,
        "total_size": total_size,
    }
    save_registry(registry)

    print(f"\n  TOTAL: {total_files} fichiers  {total_size/1024/1024:.2f} MB")
    print(f"  Manifeste: {manifest_path}")
    print(f"  VERDICT: SAUVEGARDE TERMINEE")
    return timestamp


def do_restore(timestamp):
    """Restore from a backup."""
    backup_path = os.path.join(BACKUP_DIR, timestamp)
    manifest_path = os.path.join(backup_path, "MANIFEST.json")

    if not os.path.isfile(manifest_path):
        print(f"ERREUR: sauvegarde '{timestamp}' non trouvée")
        print(f"Chemins essayés: {backup_path}")
        return False

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    print(f"Restauration: {timestamp}")
    print(f"Source: {backup_path}")
    print(f"Destination: {PROJECT_ROOT}")
    print(f"Fichiers: {manifest['total_files']}")
    print()

    restored = 0
    verified = 0
    failed = []

    for finfo in manifest["files"]:
        src = os.path.join(backup_path, finfo["rel"])
        dst = os.path.join(PROJECT_ROOT, finfo["rel"])

        if not os.path.isfile(src):
            failed.append((finfo["rel"], "source manquante"))
            continue

        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        restored += 1

        # Verify hash
        actual_hash = compute_file_hash(dst)
        if actual_hash == finfo["sha256"]:
            verified += 1
        else:
            failed.append((finfo["rel"], f"hash mismatch: attendu {finfo['sha256'][:12]}... obtenu {actual_hash[:12]}..."))

    print(f"  Restaures : {restored}/{manifest['total_files']}")
    print(f"  Verifies (SHA-256): {verified}/{restored}")
    if failed:
        print(f"\n  ERREURS ({len(failed)}):")
        for path, reason in failed:
            print(f"    - {path}: {reason}")
        print(f"  VERDICT: ECHEC PARTIEL")
        return False
    else:
        print(f"  VERDICT: RESTAURATION REUSSIE")
        return True


def do_list():
    """List all backups."""
    registry = load_registry()
    if not registry:
        print("Aucune sauvegarde trouvee.")
        return

    print(f"Sauvegardes dans: {BACKUP_DIR}")
    print(f"{'Timestamp':20s} {'Mode':12s} {'Fichiers':>8s} {'Taille':>10s}  Date")
    print("-" * 70)
    for ts in sorted(registry.keys(), reverse=True):
        info = registry[ts]
        size_mb = info["total_size"] / 1024 / 1024
        print(f"{ts:20s} {info['mode']:12s} {info['total_files']:>8d} {size_mb:>9.2f}MB  {info['date']}")
    print(f"\nTotal: {len(registry)} sauvegarde(s)")


def do_info(timestamp):
    """Show details of a specific backup."""
    manifest_path = os.path.join(BACKUP_DIR, timestamp, "MANIFEST.json")
    if not os.path.isfile(manifest_path):
        print(f"ERREUR: sauvegarde '{timestamp}' non trouvée")
        return

    with open(manifest_path, "r", encoding="utf-8") as f:
        m = json.load(f)

    print(f"Sauvegarde: {m['timestamp']}")
    print(f"Date: {m['date']}")
    print(f"Mode: {m['mode']}")
    print(f"Fichiers: {m['total_files']}")
    print(f"Taille: {m['total_size']/1024/1024:.2f} MB")
    print(f"Cibles: {', '.join(m['targets'])}")
    print(f"\nContenu:")

    # Group by top-level directory
    by_dir = {}
    for finfo in m["files"]:
        top = finfo["rel"].split(os.sep)[0]
        if top not in by_dir:
            by_dir[top] = {"count": 0, "size": 0}
        by_dir[top]["count"] += 1
        by_dir[top]["size"] += finfo["size"]

    for d in sorted(by_dir.keys()):
        info = by_dir[d]
        print(f"  {d + '/':35s} {info['count']:>5d} fichiers  {info['size']/1024/1024:>8.2f} MB")


def load_registry():
    """Load the backups registry."""
    if os.path.isfile(METADATA_FILE):
        with open(METADATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_registry(registry):
    """Save the backups registry."""
    os.makedirs(BACKUP_DIR, exist_ok=True)
    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help", "help"):
        print(__doc__)
        return 0

    cmd = sys.argv[1]

    if cmd == "backup":
        skills_only = "--skills-only" in sys.argv
        do_backup(skills_only=skills_only)
    elif cmd == "restore":
        if len(sys.argv) < 3:
            print("Usage: back-depot.py restore <timestamp>")
            print("Utilisez 'list' pour voir les sauvegardes disponibles.")
            return 1
        do_restore(sys.argv[2])
    elif cmd == "list":
        do_list()
    elif cmd == "info":
        if len(sys.argv) < 3:
            print("Usage: back-depot.py info <timestamp>")
            return 1
        do_info(sys.argv[2])
    else:
        print(f"Commande inconnue: {cmd}")
        print("Commandes disponibles: backup, restore, list, info")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
