#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.6.2)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}}
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

"""Scan des doublons download/ ↔ skills/ (Task 14, directive déduplication).

Critère utilisateur : « même nom, même contexte, idempotent » — un fichier de
download/ est un DOUBLON s'il existe dans skills/ un fichier de MÊME NOM au
contenu BYTE-IDENTIQUE (idempotence stricte, pas de heuristique de contenu).

Usage :
    python3 scripts/task14-scan-doublons.py            # scan sandbox (download/ local)
    python3 scripts/task14-scan-doublons.py <dir>      # scan d'un autre dossier download/
"""
import hashlib
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(BASE, "skills")
DEFAULT_DOWNLOAD = os.path.join(BASE, "download")

# L'archive est le véhicule d'intégrité (check 2 round-trip, restore §3.4) —
# nom et format distincts : elle n'est PAS un doublon au sens fichier.
ARCHIVE_NAME = "mon-ecosysteme_archive.zip"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def build_skills_index():
    """Index nom → liste des chemins skills/ (recherche par nom de fichier)."""
    index = {}
    for root, _dirs, files in os.walk(SKILLS):
        if "__pycache__" in root or "/evals/" in root.replace(os.sep, "/"):
            pass  # les evals sont aussi des sources légitimes pour la comparaison
        for fname in files:
            index.setdefault(fname, []).append(os.path.join(root, fname))
    return index


def scan(download_dir):
    index = build_skills_index()
    doublons, uniques = [], []
    if not os.path.isdir(download_dir):
        print(f"ABSENT : {download_dir}")
        return doublons, uniques
    for fname in sorted(os.listdir(download_dir)):
        fpath = os.path.join(download_dir, fname)
        if not os.path.isfile(fpath):
            continue
        if fname == ARCHIVE_NAME:
            uniques.append((fname, "véhicule d'intégrité (check 2 round-trip) — exclu du critère fichier"))
            continue
        candidates = index.get(fname, [])
        match = None
        dsha = sha256(fpath)
        for c in candidates:
            if sha256(c) == dsha:
                match = c
                break
        if match:
            doublons.append((fname, os.path.relpath(match, BASE)))
        else:
            uniques.append((fname, None))
    return doublons, uniques


def main():
    download_dir = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_DOWNLOAD
    print(f"=== Scan doublons : {os.path.relpath(download_dir, BASE)} ↔ skills/ ===")
    doublons, uniques = scan(download_dir)
    print(f"\n-- DOUBLONS (même nom + byte-identique) : {len(doublons)}")
    for fname, src in doublons:
        print(f"  {fname}  ==  {src}")
    print(f"\n-- UNIQUES (pas de doublon skills/) : {len(uniques)}")
    for fname, note in uniques:
        print(f"  {fname}" + (f"  [{note}]" if note else ""))
    # Code retour : 0 si aucun doublon, 1 sinon (exploitable en garde)
    sys.exit(1 if doublons else 0)


if __name__ == "__main__":
    main()
