#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 21 — F2 : régénération de l'archive d'intégrité (véhicule v2.2) après édition du corpus.
Processus établi (Tasks 16/18) : l'archive = copie byte-identique du corpus @mon-ecosysteme
+ homologues/ v2.1 (famille créateur/relecture). Idempotent : re-exécution = archive équivalente."""
import shutil
import zipfile
from pathlib import Path

BASE = Path("/home/z/my-project/work_knowledge")
CORPUS = BASE / "skills" / "@mon-ecosysteme"
ARCHIVE = BASE / "download" / "mon-ecosysteme_archive.zip"
BAK = ARCHIVE.with_suffix(".zip.bak")

corpus_files = sorted(p.name for p in CORPUS.glob("*.md"))
print(f"corpus : {len(corpus_files)} fichiers .md")

shutil.copy2(ARCHIVE, BAK)
with zipfile.ZipFile(BAK) as z:
    old_names = z.namelist()
    old_bytes = {n: z.read(n) for n in old_names if not n.endswith("/")}
print(f"ancienne archive : {len(old_bytes)} entrées")

with zipfile.ZipFile(ARCHIVE, "w", zipfile.ZIP_DEFLATED) as z:
    for name in old_names:
        if name.endswith("/"):
            continue
        short = name.split("@mon-ecosysteme/")[-1]
        if short in set(corpus_files):
            data = (CORPUS / short).read_bytes()
        else:
            data = old_bytes[name]
        z.writestr(name, data)

# auto-vérification : corpus ⊆ archive byte-identique, extras seulement homologues/
with zipfile.ZipFile(ARCHIVE) as z:
    znames = [n for n in z.namelist() if not n.endswith("/")]
    divergent = [n for n in corpus_files
                 if not any(m.split("@mon-ecosysteme/")[-1] == n and z.read(m) == (CORPUS / n).read_bytes()
                            for m in znames)]
    extras = [n for n in znames
              if (n.split("@mon-ecosysteme/")[-1] if "@mon-ecosysteme/" in n else n) not in set(corpus_files)
              and not n.startswith("homologues/")]
print(f"nouvelle archive : {len(znames)} entrées ; divergents : {divergent or '—'} ; "
      f"extras hors homologues : {extras or '—'}")
if divergent or extras:
    shutil.copy2(BAK, ARCHIVE)
    print("ÉCHEC — archive restaurée depuis la sauvegarde")
    raise SystemExit(1)
BAK.unlink()
print("Archive régénérée et round-trip vérifié (véhicule v2.2).")
