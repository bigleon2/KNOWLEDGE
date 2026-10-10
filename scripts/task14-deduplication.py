#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.6.8)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

"""Exécution de la décision d'architecture v2.2 (Task 14 — déduplication).

1. Archive scripts/sync-download.py → scripts/_archive/ (convention du dépôt :
   les scripts retirés du périmètre actif sont conservés sous _archive/).
2. Supprime de download/ tout fichier portant le nom d'un fichier du corpus
   (garde de sécurité : uniquement les collisions de noms corpus ↔ download/).
3. Rescelle download/mon-ecosysteme_archive.zip depuis le corpus (préfixe
   @mon-ecosysteme/, 24 fichiers — véhicule d'intégrité v2.2) puis vérifie le
   round-trip byte-identique.

Idempotent : ré-exécutable sans effet de bord (les suppressions déjà faites
sont des no-ops ; l'archive est rescellée à l'identique).
"""
import os
import shutil
import sys
import zipfile

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPUS = os.path.join(BASE, "skills", "@mon-ecosysteme")
DOWNLOAD = os.path.join(BASE, "download")
ARCHIVE = os.path.join(DOWNLOAD, "mon-ecosysteme_archive.zip")
SCRIPTS = os.path.join(BASE, "scripts")
ARCHIVE_DIR = os.path.join(SCRIPTS, "_archive")


def main():
    # 1. Retrait de sync-download.py → _archive/ (convention)
    src = os.path.join(SCRIPTS, "sync-download.py")
    if os.path.isfile(src):
        os.makedirs(ARCHIVE_DIR, exist_ok=True)
        shutil.move(src, os.path.join(ARCHIVE_DIR, "sync-download.py"))
        print("[1] sync-download.py → scripts/_archive/sync-download.py")
    else:
        print("[1] sync-download.py déjà absent (no-op)")

    # 2. Suppression des doublons download/ (collisions de noms avec le corpus)
    corpus_files = sorted(f for f in os.listdir(CORPUS) if os.path.isfile(os.path.join(CORPUS, f)))
    supprimes = []
    for fname in corpus_files:
        d = os.path.join(DOWNLOAD, fname)
        if os.path.isfile(d):
            os.remove(d)
            supprimes.append(fname)
    print(f"[2] Doublons download/ supprimés : {len(supprimes)}/{len(corpus_files)} corpus "
          + ("" if not supprimes else "(déjà effectuée)" if len(supprimes) == 0 else ""))
    if supprimes:
        for f in supprimes:
            print(f"    - {f}")
    else:
        print("    aucun (no-op)")

    # 3. Rescellage de l'archive (véhicule d'intégrité v2.2)
    os.makedirs(DOWNLOAD, exist_ok=True)
    with zipfile.ZipFile(ARCHIVE, "w", zipfile.ZIP_DEFLATED) as z:
        for fname in corpus_files:
            z.write(os.path.join(CORPUS, fname), f"@mon-ecosysteme/{fname}")
    # Round-trip : byte-identité archive → corpus
    n_ident, n_tot = 0, 0
    with zipfile.ZipFile(ARCHIVE) as z:
        for fname in corpus_files:
            n_tot += 1
            if z.read(f"@mon-ecosysteme/{fname}") == open(os.path.join(CORPUS, fname), "rb").read():
                n_ident += 1
    print(f"[3] Archive rescellée : {n_ident}/{n_tot} round-trip byte-identique "
          f"({len(corpus_files)} fichiers corpus, véhicule v2.2)")
    if n_ident != n_tot:
        print("ÉCHEC round-trip")
        sys.exit(1)
    print("OK — décision v2.2 exécutée (déduplication complète).")


if __name__ == "__main__":
    main()
