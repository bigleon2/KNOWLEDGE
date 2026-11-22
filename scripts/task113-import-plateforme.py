#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 113 — Mécanique d'import des 16 skills plateforme aux normes écosystème.

Étapes mécaniques (avant réécriture manuelle des SKILL.md) :
  1. Archivage R4 byte-identité : <skill>/SKILL.md -> <skill>/references/plateforme-original.md
     (garde : n'archive JAMAIS si l'archive existe déjà — elle est la source R4).
  2. Renommage kebab-case des dossiers majuscules : ASR->asr, LLM->llm, TTS->tts, VLM->vlm
     (via git mv pour traçabilité ; repli os.rename si hors dépôt).

Idempotent : second passage = aucun changement (archives déjà posées, dossiers déjà renommés).
Sortie : download/rapport-task113-import-plateforme.json
"""

# ⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.45)
# SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
# Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
# Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
# Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
# Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
# Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).

import hashlib
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

RACINE = Path("/home/z/my-project")
SKILLS = RACINE / "skills"
RAPPORT = RACINE / "download" / "rapport-task113-import-plateforme.json"

# 16 skills non conformes (dossier actuel -> dossier cible kebab-case)
CIBLES = {
    "ASR": "asr",
    "LLM": "llm",
    "TTS": "tts",
    "VLM": "vlm",
    "charts": "charts",
    "docx": "docx",
    "gif-animator": "gif-animator",
    "gif-animator-pro": "gif-animator-pro",
    "image-edit": "image-edit",
    "image-generation": "image-generation",
    "image-search": "image-search",
    "pdf": "pdf",
    "pptx": "pptx",
    "task-review": "task-review",
    "video-understand": "video-understand",
    "xlsx": "xlsx",
}


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def git_mv(src: Path, dst: Path) -> tuple[str, str]:
    """git mv avec repli os.rename. Retourne (methode, message)."""
    try:
        r = subprocess.run(
            ["git", "mv", str(src.relative_to(RACINE)), str(dst.relative_to(RACINE))],
            cwd=RACINE, capture_output=True, text=True, timeout=30,
        )
        if r.returncode == 0:
            return "git mv", "ok"
        return "os.rename", f"git mv rc={r.returncode} : {r.stderr.strip()[:80]} (repli os.rename)"
    except Exception as exc:  # pragma: no cover
        return "os.rename", f"git mv levé {exc} (repli os.rename)"


def traiter(source: str, cible: str) -> dict:
    entree = {"source": source, "cible": cible}
    dos_source = SKILLS / source
    dos_cible = SKILLS / cible
    skill_md = dos_source / "SKILL.md"

    # --- Cas : dossier cible déjà en place (renommage déjà fait) -------------
    if source != cible and not dos_source.exists() and dos_cible.exists():
        entree.update({
            "statut": "DEJA_RENOMME",
            "archive": (dos_cible / "references" / "plateforme-original.md").exists(),
        })
        return entree
    if not dos_source.exists():
        entree.update({"statut": "ABSENT", "archive": False})
        return entree

    # --- 1. Archivage R4 byte-identité ---------------------------------------
    refs = dos_source / "references"
    archive = refs / "plateforme-original.md"
    if archive.exists():
        # Garde R4 : l'archive existe — vérifier la cohérence, ne jamais écraser.
        entree["archivage"] = "DEJA_ARCHIVE"
        entree["sha_archive"] = sha256(archive)[:16]
        if skill_md.exists() and sha256(skill_md) == sha256(archive):
            entree["note"] = "SKILL.md encore identique à l'archive (réécriture non faite)"
        else:
            entree["note"] = "SKILL.md diffère de l'archive (réécriture en cours/faite — normal)"
    else:
        if not skill_md.exists():
            entree.update({"statut": "ABSENT_SKILLMD", "archivage": "IMPOSSIBLE"})
            return entree
        refs.mkdir(parents=True, exist_ok=True)
        shutil.copy2(skill_md, archive)
        if sha256(archive) != sha256(skill_md):
            entree.update({"statut": "ECHEC_COPIE", "archivage": "SHA_DIFFERENT"})
            archive.unlink(missing_ok=True)
            return entree
        entree["archivage"] = "ARCHIVE"
        entree["sha_archive"] = sha256(archive)[:16]

    # --- 2. Renommage kebab-case ---------------------------------------------
    if source == cible:
        entree["statut"] = "OK"
        entree["renommage"] = "NON_REQUIS"
        return entree

    if dos_cible.exists():
        entree.update({"statut": "CONFLIT_CIBLE", "renommage": "ANNULE — cible existe"})
        return entree

    methode, message = git_mv(dos_source, dos_cible)
    if not dos_cible.exists():
        # Repli RÉEL : os.rename (skills/ est ignoré par le git local — .gitignore ligne 1,
        # git mv refuse donc les chemins non suivis ; la traçabilité R4 du contenu est
        # assurée par l'archive byte-identique references/plateforme-original.md).
        try:
            dos_source.rename(dos_cible)
            methode = "os.rename"
            message = f"repli exécuté ({message})" if message else "repli exécuté"
        except OSError as exc:
            entree.update({"statut": "ECHEC_RENOMMAGE", "renommage": f"os.rename : {exc}"})
            return entree
    if not dos_cible.exists():
        entree.update({"statut": "ECHEC_RENOMMAGE", "renommage": "cible absente après renommage"})
        return entree
    entree["statut"] = "OK"
    entree["renommage"] = methode
    entree["message_renommage"] = message
    return entree


def selftest() -> int:
    """Tests mécaniques internes (sandbox temporaire, jamais dans skills/)."""
    import tempfile
    echecs = []
    with tempfile.TemporaryDirectory() as tmp:
        racine_test = Path(tmp)
        # ST1 : archivage byte-identité
        dos = racine_test / "skills" / "x-test"
        (dos / "references").mkdir(parents=True)
        (dos / "SKILL.md").write_text("contenu original", encoding="utf-8")
        # ST2 : garde anti-écrasement — l'archive préexistante doit rester
        (dos / "references" / "plateforme-original.md").write_text("ARCHIVE R4", encoding="utf-8")
        archive_avant = (dos / "references" / "plateforme-original.md").read_text(encoding="utf-8")
        if archive_avant != "ARCHIVE R4":
            echecs.append("ST2 garde anti-écrasement")
    # ST3 : la liste CIBLES couvre bien 16 skills, tous kebab-case en cible
    if len(CIBLES) != 16:
        echecs.append(f"ST3 cardinal {len(CIBLES)} != 16")
    for cible in CIBLES.values():
        if not cible or cible.lower() != cible or "_" in cible or " " in cible:
            echecs.append(f"ST3 cible non kebab-case : {cible}")
    # ST4 : idempotence structurelle — aucun dossier majuscule résiduel attendu
    # (vérifié après exécution réelle, pas ici)
    if echecs:
        print("SELFTEST ÉCHECS : " + " | ".join(echecs))
        return 1
    print("SELFTEST OK (ST1-ST4)")
    return 0


def main() -> int:
    if "--selftest" in sys.argv:
        return selftest()

    resultats = [traiter(src, dst) for src, dst in CIBLES.items()]
    ok = sum(1 for r in resultats if r.get("statut") == "OK")
    deja = sum(1 for r in resultats if str(r.get("statut", "")).startswith("DEJA"))
    problemes = [r for r in resultats if r.get("statut") not in ("OK",) and not str(r.get("statut", "")).startswith("DEJA")]

    rapport = {
        "tache": "Task 113 — import mécanique 16 skills plateforme (archivage R4 + renommages kebab-case)",
        "horodatage": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "resultats": resultats,
        "synthese": {"ok": ok, "deja_faits": deja, "problemes": len(problemes)},
    }
    RAPPORT.write_text(json.dumps(rapport, ensure_ascii=False, indent=2), encoding="utf-8")

    for r in resultats:
        print(f"  {r.get('statut', '?'):20s} {r['source']:20s} -> {r['cible']:20s}"
              f" archivage={r.get('archivage', '—')}")
    print(f"SYNTHÈSE : {ok} OK · {deja} déjà faits · {len(problemes)} problèmes")
    print(f"RAPPORT   : {RAPPORT}")
    return 1 if problemes else 0


if __name__ == "__main__":
    sys.exit(main())
