#!/usr/bin/env python3
"""⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.12)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

"""Task F5 — scellement archive v2.3 (corpus + piliers) — restauration autonome complète.

Processus (à exécuter sur un état certifié 68/68) :
  1. sauvegarde .bak de l'archive entrante (v2.2 ou v2.3) + garde anti-perte
     (corpus local byte-identique à l'archive scellée, sinon échec)
  2. construction v2.3 = @mon-ecosysteme/* (9 corpus) + piliers/* (6 fichiers critiques)
  3. auto-vérification round-trip complète (15 entrées byte-identiques)
  4. rollback depuis .bak en cas d'échec ; .bak supprimée après succès (convention task21)
Idempotent : re-exécution sur v2.3 = re-scellement équivalent (15 entrées).
Racines dérivées de __file__ (L008 — portabilité des chemins)."""

import hashlib
import shutil
import sys
import zipfile
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
CORPUS = BASE / "skills" / "@mon-ecosysteme"
ARCHIVE = BASE / "download" / "mon-ecosysteme_archive.zip"
BAK = ARCHIVE.with_suffix(".zip.bak")
PILIERS = {
    "piliers/skills/gen-plan/SKILL.md": BASE / "skills" / "gen-plan" / "SKILL.md",
    "piliers/skills/correct-work/SKILL.md": BASE / "skills" / "correct-work" / "SKILL.md",
    "piliers/skills/KNOWLEDGE.md": BASE / "skills" / "KNOWLEDGE.md",
    "piliers/scripts/certification-complete.py": BASE / "scripts" / "certification-complete.py",
    "piliers/scripts/check-ecosysteme-integrity.py": BASE / "scripts" / "check-ecosysteme-integrity.py",
    "piliers/scripts/install-ecosysteme-local.sh": BASE / "scripts" / "install-ecosysteme-local.sh",
}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


corpus_fichiers = sorted(p.name for p in CORPUS.glob("*.md"))
print(f"corpus : {len(corpus_fichiers)} fichiers .md ; piliers à sceller : {len(PILIERS)}")
for arc, src in sorted(PILIERS.items()):
    if not src.exists():
        print(f"ECHEC : pilier absent : {src}")
        sys.exit(2)

old = {}
if ARCHIVE.exists():
    shutil.copy2(ARCHIVE, BAK)
    with zipfile.ZipFile(BAK) as z:
        old = {n: z.read(n) for n in z.namelist() if not n.endswith("/")}
print(f"archive entrante : {len(old)} entrées")

# Garde anti-perte : corpus local byte-identique à l'archive scellée entrante
perdus = [f for f in corpus_fichiers
          if f"@mon-ecosysteme/{f}" in old and old[f"@mon-ecosysteme/{f}"] != (CORPUS / f).read_bytes()]
if perdus:
    print(f"ECHEC anti-perte : corpus local divergent de l'archive scellée : {perdus}")
    sys.exit(2)

with zipfile.ZipFile(ARCHIVE, "w", zipfile.ZIP_DEFLATED) as z:
    for f in corpus_fichiers:
        z.writestr(f"@mon-ecosysteme/{f}", (CORPUS / f).read_bytes())
    for arc, src in sorted(PILIERS.items()):
        z.writestr(arc, src.read_bytes())

with zipfile.ZipFile(ARCHIVE) as z:
    noms = [n for n in z.namelist() if not n.endswith("/")]
    div_corpus = [f for f in corpus_fichiers if z.read(f"@mon-ecosysteme/{f}") != (CORPUS / f).read_bytes()]
    div_piliers = [a for a in PILIERS if z.read(a) != PILIERS[a].read_bytes()]
attendu = len(corpus_fichiers) + len(PILIERS)
print(f"nouvelle archive : {len(noms)} entrées (attendu {attendu}) ; "
      f"divergences : corpus={div_corpus or '—'} piliers={div_piliers or '—'}")
if div_corpus or div_piliers or len(noms) != attendu:
    shutil.copy2(BAK, ARCHIVE)
    print("ÉCHEC — archive restaurée depuis la sauvegarde")
    sys.exit(1)
if BAK.exists():
    BAK.unlink()
print("Archive v2.3 scellée (corpus + piliers) — round-trip vérifié.")
print("Pense-bête : exécuter ensuite l'arbitre en mode COMPLET pour régénérer le manifeste (SHA archive + entrées piliers).")
