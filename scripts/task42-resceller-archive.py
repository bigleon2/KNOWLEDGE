#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.21)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Task 42 — Re-scellement de l'archive d'intégrité v2.3 (clone écosystème).

Construit download/mon-ecosysteme_archive.zip depuis l'état LIVE du clone :
  - 9 fichiers corpus skills/@mon-ecosysteme/* (entrées « skills/@mon-ecosysteme/<nom> »),
  - 6 piliers sous le préfixe « piliers/ » (byte-identité exigée au round-trip),
  - zéro extra (les homologues/ restent admis mais non produits ici).

Déterminisme : entrées triées, date_time figée (2026-11-03 20:00:00) — re-jeu ×2
byte-identique. Vérification interne : round-trip SHA-256 de chaque entrée contre
le fichier vivant, verdict PASS/FAIL + exit code.

Convention script-creator : stdlib uniquement, idempotence ×2, verdict mécanique.
"""
from __future__ import annotations

import hashlib
import zipfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent / "work" / "knowledge-clone-fddbe94"
CORPUS = BASE_DIR / "skills" / "@mon-ecosysteme"
ARCHIVE = BASE_DIR / "download" / "mon-ecosysteme_archive.zip"
PILIERS = {
    "piliers/skills/gen-plan/SKILL.md": BASE_DIR / "skills" / "gen-plan" / "SKILL.md",
    "piliers/skills/correct-work/SKILL.md": BASE_DIR / "skills" / "correct-work" / "SKILL.md",
    "piliers/skills/KNOWLEDGE.md": BASE_DIR / "skills" / "KNOWLEDGE.md",
    "piliers/scripts/certification-complete.py": BASE_DIR / "scripts" / "certification-complete.py",
    "piliers/scripts/check-ecosysteme-integrity.py": BASE_DIR / "scripts" / "check-ecosysteme-integrity.py",
    "piliers/scripts/install-ecosysteme-local.sh": BASE_DIR / "scripts" / "install-ecosysteme-local.sh",
}
DATE_TIME = (2026, 11, 3, 20, 0, 0)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    corpus_files = sorted(p for p in CORPUS.iterdir() if p.is_file())
    if len(corpus_files) != 9:
        print(f"VERDICT : FAIL — corpus attendu 9 fichiers, trouvé {len(corpus_files)}")
        return 2

    entries: list[tuple[str, Path]] = [
        (f"skills/@mon-ecosysteme/{p.name}", p) for p in corpus_files
    ] + sorted(PILIERS.items(), key=lambda kv: kv[0])

    ARCHIVE.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(ARCHIVE, "w", zipfile.ZIP_DEFLATED) as z:
        for name, path in entries:
            info = zipfile.ZipInfo(name, date_time=DATE_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, path.read_bytes())

    # Round-trip interne : byte-identité de chaque entrée contre le fichier vivant.
    divergents: list[str] = []
    with zipfile.ZipFile(ARCHIVE) as z:
        noms = [n for n in z.namelist() if not n.endswith("/")]
        for name, path in entries:
            if hashlib.sha256(z.read(name)).hexdigest() != sha256(path):
                divergents.append(name)
    if divergents or len(noms) != len(entries):
        print(f"VERDICT : FAIL — divergents={divergents} entrées={len(noms)}/{len(entries)}")
        return 1

    print(f"VERDICT : PASS — archive v2.3 scellée ({len(entries)} entrées : "
          f"corpus {len(corpus_files)}/9 · piliers {len(PILIERS)}/6 · homologues 0)")
    print(f"  chemin : {ARCHIVE}")
    print(f"  sha256 : {sha256(ARCHIVE)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
