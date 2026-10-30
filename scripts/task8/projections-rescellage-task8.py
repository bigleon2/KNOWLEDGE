#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 8 — Projections hôte↔worktree + rescellage des archives d'intégrité v2.3 ×2 arbres.

Projections (le worktree = vérité de publication — convention Task 7) :
  - skills/KNOWLEDGE.md (bump vue-upload v1.5.0 + entrée livraison-garantie v1.0.0 + réciproques)
  - scripts/check-ecosysteme-integrity.py (ECO_SKILLS vue-upload 1.5.0 + livraison-garantie 1.0.0)
  - skills/livraison-garantie/*, skills/gif-animator-pro/*, skills/vue-upload/* (déjà projetés G1-G3,
    re-projetés par sûreté — byte-identité idempotente)
  - scripts/task8/* (tests + ajout evals)
Rescellage archive (canon F5 v2.3 / Task 48) : corpus 9 @mon-ecosysteme/ + 6 piliers
byte-identiques + extras homologues/ conservés, sauvegarde .bak, round-trip auto-vérifié.
Idempotent : re-exécution = état équivalent.
"""
import hashlib
import shutil
import zipfile
from pathlib import Path

HOST = Path("/home/z/my-project")
WT = HOST / ".staging" / "KNOWLEDGE-publish"

PILIERS = {
    "piliers/skills/gen-plan/SKILL.md": "skills/gen-plan/SKILL.md",
    "piliers/skills/correct-work/SKILL.md": "skills/correct-work/SKILL.md",
    "piliers/skills/KNOWLEDGE.md": "skills/KNOWLEDGE.md",
    "piliers/scripts/certification-complete.py": "scripts/certification-complete.py",
    "piliers/scripts/check-ecosysteme-integrity.py": "scripts/check-ecosysteme-integrity.py",
    "piliers/scripts/install-ecosysteme-local.sh": "scripts/install-ecosysteme-local.sh",
}

FICHIERS = [
    "skills/KNOWLEDGE.md",
    "scripts/check-ecosysteme-integrity.py",
    "skills/vue-upload/SKILL.md",
    "skills/vue-upload/scripts/vue_upload_panel.py",
    "skills/vue-upload/scripts/vue_upload_server.py",
    "skills/vue-upload/evals/evals.json",
    "skills/livraison-garantie/SKILL.md",
    "skills/livraison-garantie/scripts/livraison_garantie.py",
    "skills/livraison-garantie/evals/evals.json",
    "skills/livraison-garantie/evals/trigger_evals.json",
    "skills/gif-animator-pro/SKILL.md",
    "skills/gif-animator-pro/scripts/qa_animation.py",
    "scripts/task8/test-vue-upload-v150.py",
    "scripts/task8/test-livraison-garantie.py",
    "scripts/task8/test-qa-animation.py",
    "scripts/task8/ajout-evals-vue-upload.py",
]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def projette(rel: str) -> bool:
    src, dst = HOST / rel, WT / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    if not src.is_file():
        raise SystemExit("source absente : %s" % src)
    avant = sha(dst) if dst.is_file() else None
    shutil.copy2(src, dst)
    apres = sha(dst)
    change = avant != apres
    print("  %s %s" % ("=" if not change else "->", rel))
    return change


def rescellage(base: Path):
    corpus = base / "skills" / "@mon-ecosysteme"
    archive = base / "download" / "mon-ecosysteme_archive.zip"
    bak = archive.with_suffix(".zip.bak")
    corpus_files = sorted(p.name for p in corpus.glob("*.md"))
    entrees = {}
    for f in corpus_files:
        entrees["skills/@mon-ecosysteme/" + f] = (corpus / f).read_bytes()
    for arc, rel in PILIERS.items():
        entrees[arc] = (base / rel).read_bytes()
    # conserve les extras homologues/ existants
    extras = {}
    if archive.is_file():
        with zipfile.ZipFile(archive) as z:
            for n in z.namelist():
                if not n.endswith("/") and n not in entrees and n.startswith("homologues/"):
                    extras[n] = z.read(n)
    if bak.exists():
        bak.unlink()
    shutil.copy2(archive, bak)
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as z:
        for n in sorted(entrees):
            z.writestr(n, entrees[n])
        for n in sorted(extras):
            z.writestr(n, extras[n])
    # round-trip auto-vérifié
    with zipfile.ZipFile(archive) as z:
        for n, data in entrees.items():
            assert z.read(n) == data, "round-trip KO : %s" % n
        for n, data in extras.items():
            assert z.read(n) == data, "round-trip KO (extra) : %s" % n
    print("  rescellage %s : %d corpus + %d piliers + %d homologues — round-trip OK"
          % (base.name, len(corpus_files), len(PILIERS), len(extras)))


def main():
    print("— Projections hôte → worktree —")
    n = sum(1 for f in FICHIERS if projette(f))
    print("  (%d fichier(s) modifié(s))" % n)
    print("— Rescellage ×2 arbres —")
    rescellage(HOST)
    rescellage(WT)
    print("OK")


if __name__ == "__main__":
    main()
