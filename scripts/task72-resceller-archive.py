#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.34)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).
"""

"""task72-resceller-archive.py — Re-scellement du véhicule d'intégrité v2.3
(download/mon-ecosysteme_archive.zip) après la cascade KO-L004 gen-plan v3.39.0.

Convention task42-resceller-archive.py (le script Task 42 pointait vers un clone
périmé work/knowledge-clone-fddbe94 disparu — voie ré-écrite sur l'arbre vivant) :
  - 9 fichiers corpus skills/@mon-ecosysteme/* (entrées « @mon-ecosysteme/<nom> ») ;
  - 6 piliers sous le préfixe « piliers/ » (byte-identité exigée au round-trip) :
    skills/gen-plan/SKILL.md, skills/correct-work/SKILL.md, skills/KNOWLEDGE.md,
    scripts/certification-complete.py, scripts/check-ecosysteme-integrity.py,
    scripts/install-ecosysteme-local.sh ;
  - zéro extra ; entrées triées ; date_time FIGÉE (2026-11-08 23:30:00) —
    re-jeu ×2 byte-identique ;
  - vérification interne : round-trip SHA-256 de chaque entrée contre le fichier
    vivant, verdict PASS/FAIL + exit code.

Python stdlib uniquement, idempotence ×2, verdict mécanique (script-creator).
"""
import hashlib
import sys
import zipfile
from pathlib import Path

RACINE = Path("/home/z/my-project")
ARCHIVE = RACINE / "download" / "mon-ecosysteme_archive.zip"
CORPUS = RACINE / "skills" / "@mon-ecosysteme"
DATE_FIGEE = (2026, 11, 8, 23, 30, 0)

PILIERS = [
    ("piliers/skills/gen-plan/SKILL.md", "skills/gen-plan/SKILL.md"),
    ("piliers/skills/correct-work/SKILL.md", "skills/correct-work/SKILL.md"),
    ("piliers/skills/KNOWLEDGE.md", "skills/KNOWLEDGE.md"),
    ("piliers/scripts/certification-complete.py", "scripts/certification-complete.py"),
    ("piliers/scripts/check-ecosysteme-integrity.py", "scripts/check-ecosysteme-integrity.py"),
    ("piliers/scripts/install-ecosysteme-local.sh", "scripts/install-ecosysteme-local.sh"),
]


def main() -> int:
    corpus_files = sorted(p for p in CORPUS.iterdir() if p.is_file())
    if len(corpus_files) != 9:
        print(f"ABANDON : corpus à {len(corpus_files)} fichiers (attendu 9)")
        return 2

    entrees = [("@mon-ecosysteme/" + p.name, p) for p in corpus_files]
    for nom_zip, chemin in PILIERS:
        src = RACINE / chemin
        if not src.exists():
            print(f"ABANDON : pilier manquant {chemin}")
            return 2
        entrees.append((nom_zip, src))

    avant = hashlib.sha256(ARCHIVE.read_bytes()).hexdigest() if ARCHIVE.exists() else None

    with zipfile.ZipFile(ARCHIVE, "w", zipfile.ZIP_DEFLATED) as z:
        for nom, chemin in entrees:
            info = zipfile.ZipInfo(nom, date_time=DATE_FIGEE)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, chemin.read_bytes())

    apres = hashlib.sha256(ARCHIVE.read_bytes()).hexdigest()

    # Round-trip : chaque entrée == fichier vivant
    ok = True
    with zipfile.ZipFile(ARCHIVE) as z:
        noms = z.namelist()
        if len(noms) != len(entrees):
            print(f"ABANDON : {len(noms)} entrées écrites (attendu {len(entrees)})")
            return 2
        for nom, chemin in entrees:
            sha_zip = hashlib.sha256(z.read(nom)).hexdigest()
            sha_vif = hashlib.sha256(chemin.read_bytes()).hexdigest()
            match = sha_zip == sha_vif
            ok = ok and match
            print(f"  [{'PASS' if match else 'FAIL'}] {nom} ({sha_vif and len(chemin.read_bytes())} o)")

    print(f"Archive re-scellée : {ARCHIVE}")
    print(f"  SHA-256 archive : {apres}")
    if avant == apres:
        print("  IDEMPOTENCE : SHA identique au passage précédent (byte-identique).")
    else:
        print(f"  SHA précédent  : {avant or '(aucun)'} — archive mise à jour.")
    print(f"VERDICT round-trip : {'PASS (corpus 9/9 + piliers 6/6 byte-identiques)' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
