#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.12)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

# -*- coding: utf-8 -*-
"""
Task 48 — Rescellage de l'archive d'intégrité (véhicule v2.3 — corpus + piliers).

Contexte : la KB (pilier) a changé en Task 47 D3 (inscription iphone19, 35->36 entrées)
sans rescellage ; le recalibrage KO-L004 Task 48 (ECO_SKILLS += iphone19) modifie un
second pilier (check-ecosysteme-integrity.py). L'archive scellée divergente fait échouer
le round-trip (check-ecosysteme-integrity 72/74). Rescelage conforme au processus établi
(F5 Task 8 2026-10-17, v2.3) : l'archive = copie byte-identique du corpus (9 fichiers
@mon-ecosysteme) + des 6 piliers critiques + des éventuels extras homologues/ conservés.

Idempotent : re-exécution = archive équivalente. Garde anti-perte : sauvegarde .bak,
restauration en cas d'échec de l'auto-vérification round-trip.
"""
import shutil
import zipfile
from pathlib import Path

BASE = Path("/home/z/my-project")
CORPUS = BASE / "skills" / "@mon-ecosysteme"
ARCHIVE = BASE / "download" / "mon-ecosysteme_archive.zip"
BAK = ARCHIVE.with_suffix(".zip.bak")

# 6 piliers critiques (définition check-ecosysteme-integrity.py v2.3, F5 Task 8)
PILIERS = {
    "piliers/skills/gen-plan/SKILL.md": BASE / "skills" / "gen-plan" / "SKILL.md",
    "piliers/skills/correct-work/SKILL.md": BASE / "skills" / "correct-work" / "SKILL.md",
    "piliers/skills/KNOWLEDGE.md": BASE / "skills" / "KNOWLEDGE.md",
    "piliers/scripts/certification-complete.py": BASE / "scripts" / "certification-complete.py",
    "piliers/scripts/check-ecosysteme-integrity.py": BASE / "scripts" / "check-ecosysteme-integrity.py",
    "piliers/scripts/install-ecosysteme-local.sh": BASE / "scripts" / "install-ecosysteme-local.sh",
}

corpus_files = sorted(p.name for p in CORPUS.glob("*.md"))
print(f"corpus : {len(corpus_files)} fichiers .md")
assert len(corpus_files) == 9, f"corpus attendu 9 fichiers, trouvé {len(corpus_files)}"

# extras homologues/ de l'ancienne archive (famille créateur/relecture) — conservés
if ARCHIVE.exists():
    shutil.copy2(ARCHIVE, BAK)
    with zipfile.ZipFile(BAK) as z:
        old_names = [n for n in z.namelist() if not n.endswith("/")]
        homologues = [(n, z.read(n)) for n in old_names if n.startswith("homologues/")]
else:
    homologues = []
print(f"ancienne archive : sauvegardée ; extras homologues/ conservés : {len(homologues)}")

with zipfile.ZipFile(ARCHIVE, "w", zipfile.ZIP_DEFLATED) as z:
    for f in corpus_files:
        z.writestr(f"@mon-ecosysteme/{f}", (CORPUS / f).read_bytes())
    for name, src in PILIERS.items():
        z.writestr(name, src.read_bytes())
    for name, data in homologues:
        z.writestr(name, data)

# auto-vérification round-trip : corpus + piliers byte-identiques, extras = homologues/ seulement
with zipfile.ZipFile(ARCHIVE) as z:
    znames = [n for n in z.namelist() if not n.endswith("/")]
    zmap = {n: z.read(n) for n in znames}
corpus_ok = all(zmap.get(f"@mon-ecosysteme/{f}") == (CORPUS / f).read_bytes() for f in corpus_files)
piliers_ok = all(zmap.get(n) == src.read_bytes() for n, src in PILIERS.items())
extras = [n for n in znames if not n.startswith("@mon-ecosysteme/")
          and not n.startswith("piliers/") and not n.startswith("homologues/")]
print(f"nouvelle archive : {len(znames)} entrées ; corpus byte-identique : {corpus_ok} ; "
      f"piliers byte-identiques : {piliers_ok} ; extras hors homologues : {extras or '—'}")
if not (corpus_ok and piliers_ok and not extras):
    shutil.copy2(BAK, ARCHIVE)
    print("ÉCHEC — archive restaurée depuis la sauvegarde")
    raise SystemExit(1)
BAK.unlink()
print("Archive rescellée et round-trip vérifié (véhicule v2.3 — corpus + piliers).")
