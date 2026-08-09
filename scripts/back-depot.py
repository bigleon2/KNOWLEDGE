#!/usr/bin/env python3
"""back-depot.py — Sauvegarde fidèle et restauration du dépôt Knowledge v2.0.0.

Usage:
    python3 scripts/back-depot.py                          # Affiche l'aide
    python3 scripts/back-depot.py backup                   # Sauvegarde complète
    python3 scripts/back-depot.py backup --skills-only     # Sauvegarde skills/ seulement
    python3 scripts/back-depot.py backup --dry-run         # Simulation sans écriture
    python3 scripts/back-depot.py restore <timestamp>      # Restaure une sauvegarde
    python3 scripts/back-depot.py restore <timestamp> --dry-run  # Simule la restauration
    python3 scripts/back-depot.py list                     # Liste les sauvegardes
    python3 scripts/back-depot.py info <timestamp>         # Détails d'une sauvegarde
    python3 scripts/back-depot.py clean [--keep N]         # Nettoie les anciennes sauvegardes
    python3 scripts/back-depot.py verify <timestamp>       # Vérifie l'intégrité d'une sauvegarde

Sauvegardes stockées dans : <PROJECT_ROOT>/backups/

v2.0.0 — Améliorations:
    - Auto-détection de PROJECT_ROOT (ne dépend plus d'un chemin hardcodé)
    - Validation avant restauration (vérifie que la source existe)
    - Mode --dry-run pour backup et restore
    - Commande 'clean' pour purger les anciennes sauvegardes
    - Commande 'verify' pour vérifier l'intégrité SHA-256 post-backup
    - Manifeste enrichi avec SHA-256 par fichier
    - Compatibilité totale avec les sauvegardes v1.x
"""

import os
import sys
import json
import shutil
import hashlib
from datetime import datetime

# Auto-detect project root (directory containing this script's parent)
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT_CANDIDATE = os.path.dirname(_SCRIPT_DIR)

# Validate by checking for key markers
_REQUIRED_MARKERS = ("skills/", "worklog.md")


def _detect_project_root():
    """Auto-detect the project root by looking for marker directories/files."""
    candidate = _PROJECT_ROOT_CANDIDATE
    for marker in _REQUIRED_MARKERS:
        if not os.path.exists(os.path.join(candidate, marker)):
            # Fallback: try CWD
            candidate = os.getcwd()
            break
    for marker in _REQUIRED_MARKERS:
        if not os.path.exists(os.path.join(candidate, marker)):
            print(f"ERREUR: Impossible de détecter le projet racine.", file=sys.stderr)
            print(f"  Répertoire testé: {_PROJECT_ROOT_CANDIDATE}", file=sys.stderr)
            print(f"  Marqueurs attendus: {_REQUIRED_MARKERS}", file=sys.stderr)
            sys.exit(1)
    return candidate


PROJECT_ROOT = _detect_project_root()
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
    "node_modules",
    ".next",
]


def should_exclude(rel_path):
    """Check if a path matches any exclusion pattern."""
    parts = rel_path.replace(os.sep, "/").split("/")
    for pattern in EXCLUDE_PATTERNS:
        if pattern.startswith("*"):
            if rel_path.endswith(pattern[1:]):
                return True
        elif pattern in parts:
            return True
    return False


def compute_file_hash(filepath):
    """Compute SHA-256 hash of a file."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def format_size(size_bytes):
    """Format bytes to human-readable size."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / 1024 / 1024:.2f} MB"


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


def do_backup(skills_only=False, dry_run=False):
    """Create a timestamped backup."""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_path = os.path.join(BACKUP_DIR, timestamp)

    targets = ["skills/"] if skills_only else BACKUP_TARGETS
    all_files = []
    total_size = 0

    mode_label = "skills-only" if skills_only else "full"
    dry_label = " [DRY-RUN]" if dry_run else ""

    print(f"Sauvegarde{dry_label}: {timestamp}")
    print(f"  Mode     : {mode_label}")
    print(f"  Source   : {PROJECT_ROOT}")
    print(f"  Dest.    : {backup_path}")
    print()

    # Phase 1: Scan all targets
    for target in targets:
        files, size = scan_target(target, PROJECT_ROOT)
        all_files.extend(files)
        total_size += size
        print(f"  {target:30s} {len(files):>5d} fichiers  {format_size(size):>10s}")

    total_files = len(all_files)
    print(f"  {'TOTAL':30s} {total_files:>5d} fichiers  {format_size(total_size):>10s}")

    if dry_run:
        print(f"\n  [DRY-RUN] Aucune écriture effectuée.")
        return timestamp

    # Phase 2: Copy files
    print(f"\n  Copie en cours...", end="", flush=True)
    os.makedirs(backup_path, exist_ok=True)
    for finfo in all_files:
        src = os.path.join(PROJECT_ROOT, finfo["rel"])
        dst = os.path.join(backup_path, finfo["rel"])
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
    print(" OK")

    # Phase 3: Save manifest
    manifest = {
        "version": "2.0.0",
        "timestamp": timestamp,
        "date": datetime.now().isoformat(),
        "mode": mode_label,
        "total_files": total_files,
        "total_size": total_size,
        "targets": targets,
        "files": all_files,
    }
    manifest_path = os.path.join(backup_path, "MANIFEST.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    # Phase 4: Update registry
    registry = load_registry()
    registry[timestamp] = {
        "date": datetime.now().isoformat(),
        "mode": mode_label,
        "total_files": total_files,
        "total_size": total_size,
    }
    save_registry(registry)

    print(f"  Manifeste: {manifest_path}")
    print(f"  VERDICT: SAUVEGARDE TERMINEE")
    return timestamp


def do_restore(timestamp, dry_run=False):
    """Restore from a backup with pre-flight validation."""
    backup_path = os.path.join(BACKUP_DIR, timestamp)
    manifest_path = os.path.join(backup_path, "MANIFEST.json")

    # Pre-flight: check backup exists
    if not os.path.isdir(backup_path):
        print(f"ERREUR: sauvegarde '{timestamp}' non trouvée.")
        print(f"  Chemin essayé: {backup_path}")
        print(f"  Utilisez 'list' pour voir les sauvegardes disponibles.")
        return False

    if not os.path.isfile(manifest_path):
        print(f"ERREUR: MANIFEST.json manquant dans '{timestamp}'.")
        print(f"  Sauvegarde corrompue ou incomplète.")
        return False

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    dry_label = " [DRY-RUN]" if dry_run else ""

    print(f"Restauration{dry_label}: {timestamp}")
    print(f"  Source   : {backup_path}")
    print(f"  Dest.    : {PROJECT_ROOT}")
    print(f"  Fichiers : {manifest['total_files']}")
    print(f"  Taille   : {format_size(manifest['total_size'])}")
    print(f"  Mode     : {manifest.get('mode', 'inconnu')}")
    print()

    # Pre-flight: check all source files exist
    print(f"  Validation pre-restauration...", end="", flush=True)
    missing = []
    for finfo in manifest["files"]:
        src = os.path.join(backup_path, finfo["rel"])
        if not os.path.isfile(src):
            missing.append(finfo["rel"])
    if missing:
        print(f" ECHEC")
        print(f"\n  {len(missing)} fichier(s) manquant(s) dans la sauvegarde:")
        for m in missing[:10]:
            print(f"    - {m}")
        if len(missing) > 10:
            print(f"    ... et {len(missing) - 10} autres")
        print(f"  VERDICT: RESTAURATION ANNULEE")
        return False
    print(f" OK ({manifest['total_files']} fichiers presents)")

    if dry_run:
        print(f"\n  [DRY-RUN] Aucune écriture effectuée.")
        print(f"  [DRY-RUN] Les {manifest['total_files']} fichiers seraient restaures.")
        return True

    # Execute restore
    print(f"  Restauration en cours...", end="", flush=True)
    restored = 0
    verified = 0
    failed = []

    for finfo in manifest["files"]:
        src = os.path.join(backup_path, finfo["rel"])
        dst = os.path.join(PROJECT_ROOT, finfo["rel"])

        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
        restored += 1

        # Verify hash after copy
        actual_hash = compute_file_hash(dst)
        if actual_hash == finfo["sha256"]:
            verified += 1
        else:
            failed.append((finfo["rel"],
                           f"hash mismatch: attendu {finfo['sha256'][:12]}... "
                           f"obtenu {actual_hash[:12]}..."))

    print(" OK")
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


def do_verify(timestamp):
    """Verify the integrity of a backup by re-hashing all files."""
    manifest_path = os.path.join(BACKUP_DIR, timestamp, "MANIFEST.json")
    if not os.path.isfile(manifest_path):
        print(f"ERREUR: sauvegarde '{timestamp}' non trouvée.")
        return False

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    print(f"Verification integrite: {timestamp}")
    print(f"  Fichiers: {manifest['total_files']}")
    print(f"  Verification en cours...", end="", flush=True)

    ok = 0
    failed = []
    missing = []

    for finfo in manifest["files"]:
        fpath = os.path.join(BACKUP_DIR, timestamp, finfo["rel"])
        if not os.path.isfile(fpath):
            missing.append(finfo["rel"])
            continue
        actual = compute_file_hash(fpath)
        if actual == finfo["sha256"]:
            ok += 1
        else:
            failed.append((finfo["rel"], f"attendu {finfo['sha256'][:12]}... obtenu {actual[:12]}..."))

    print(" OK")
    print(f"  Integres : {ok}/{manifest['total_files']}")

    if missing:
        print(f"  Manquants: {len(missing)}")
        for m in missing[:5]:
            print(f"    - {m}")

    if failed:
        print(f"  Corrompus: {len(failed)}")
        for path, reason in failed[:5]:
            print(f"    - {path}: {reason}")

    if not missing and not failed:
        print(f"  VERDICT: INTEGRITE CONFIRMEE")
        return True
    else:
        print(f"  VERDICT: ANOMALIES DETECTEES")
        return False


def do_list():
    """List all backups."""
    registry = load_registry()
    if not registry:
        print("Aucune sauvegarde trouvee.")
        return

    print(f"Sauvegardes dans: {BACKUP_DIR}")
    print(f"{'Timestamp':20s} {'Mode':12s} {'Fichiers':>8s} {'Taille':>10s}  Date")
    print("-" * 75)
    for ts in sorted(registry.keys(), reverse=True):
        info = registry[ts]
        print(f"{ts:20s} {info['mode']:12s} {info['total_files']:>8d} {format_size(info['total_size']):>10s}  {info['date']}")
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
    print(f"Version   : {m.get('version', '1.x (legacy)')}")
    print(f"Date      : {m['date']}")
    print(f"Mode      : {m['mode']}")
    print(f"Fichiers  : {m['total_files']}")
    print(f"Taille    : {format_size(m['total_size'])}")
    print(f"Cibles    : {', '.join(m['targets'])}")
    print(f"\nContenu par répertoire:")

    by_dir = {}
    for finfo in m["files"]:
        top = finfo["rel"].split(os.sep)[0]
        if top not in by_dir:
            by_dir[top] = {"count": 0, "size": 0}
        by_dir[top]["count"] += 1
        by_dir[top]["size"] += finfo["size"]

    for d in sorted(by_dir.keys()):
        info = by_dir[d]
        print(f"  {d + '/':35s} {info['count']:>5d} fichiers  {format_size(info['size']):>10s}")


def do_clean(keep=3):
    """Remove old backups, keeping only the N most recent."""
    registry = load_registry()
    if not registry:
        print("Aucune sauvegarde a nettoyer.")
        return

    sorted_ts = sorted(registry.keys(), reverse=True)
    to_remove = sorted_ts[keep:]  # keep the N most recent

    if not to_remove:
        print(f"  {len(sorted_ts)} sauvegarde(s), keep={keep}: rien a supprimer.")
        return

    print(f"Nettoyage: {len(to_remove)} sauvegarde(s) a supprimer (keep={keep})")
    for ts in to_remove:
        backup_path = os.path.join(BACKUP_DIR, ts)
        if os.path.isdir(backup_path):
            shutil.rmtree(backup_path)
            print(f"  SUPPRIME: {ts}")
        del registry[ts]

    save_registry(registry)
    print(f"  VERDICT: {len(to_remove)} sauvegarde(s) supprimee(s), {len(registry)} conservee(s)")


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help", "help"):
        print(__doc__)
        return 0

    cmd = sys.argv[1]
    args = sys.argv[2:]
    dry_run = "--dry-run" in args
    args = [a for a in args if a != "--dry-run"]

    if cmd == "backup":
        skills_only = "--skills-only" in args
        ts = do_backup(skills_only=skills_only, dry_run=dry_run)
        return 0 if ts else 1

    elif cmd == "restore":
        if not args:
            print("Usage: back-depot.py restore <timestamp>")
            print("Utilisez 'list' pour voir les sauvegardes disponibles.")
            return 1
        return 0 if do_restore(args[0], dry_run=dry_run) else 1

    elif cmd == "verify":
        if not args:
            print("Usage: back-depot.py verify <timestamp>")
            return 1
        return 0 if do_verify(args[0]) else 1

    elif cmd == "list":
        do_list()

    elif cmd == "info":
        if not args:
            print("Usage: back-depot.py info <timestamp>")
            return 1
        do_info(args[0])

    elif cmd == "clean":
        keep = 3
        for i, a in enumerate(args):
            if a == "--keep" and i + 1 < len(args):
                try:
                    keep = int(args[i + 1])
                except ValueError:
                    print(f"ERREUR: --keep necessite un nombre entier.")
                    return 1
        do_clean(keep=keep)

    else:
        print(f"Commande inconnue: {cmd}")
        print("Commandes disponibles: backup, restore, verify, list, info, clean")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
