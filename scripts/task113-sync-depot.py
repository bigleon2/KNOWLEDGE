#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 113 — Synchronisation dépôt canonique : les 16 réécritures plateforme.

Répercute dans KNOWLEDGE-repo/skills/ les réécritures faites dans skills/ :
  1. git mv des dossiers majuscules vers kebab-case (ASR->asr, LLM->llm, TTS->tts, VLM->vlm)
  2. copie du SKILL.md réécrit (sha256 vérifié == installation locale)
  3. copie de l'archive R4 references/plateforme-original.md (sha256 vérifié)

Idempotent : second passage = aucun changement (comparaison sha256 avant copie).
Sortie : download/rapport-task113-sync-depot.json
"""

# ⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.46)
# SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
# Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
# Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
# Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
# Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
# Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).

import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

RACINE = Path("/home/z/my-project")
LOCAL = RACINE / "skills"
DEPOT = RACINE / "KNOWLEDGE-repo"
REPO_SKILLS = DEPOT / "skills"
RAPPORT = RACINE / "download" / "rapport-task113-sync-depot.json"

# nom kebab-case (local) -> nom actuel dans le dépôt
CIBLES = {
    "asr": "ASR", "llm": "LLM", "tts": "TTS", "vlm": "VLM",
    "charts": "charts", "docx": "docx", "gif-animator": "gif-animator",
    "gif-animator-pro": "gif-animator-pro", "image-edit": "image-edit",
    "image-generation": "image-generation", "image-search": "image-search",
    "pdf": "pdf", "pptx": "pptx", "task-review": "task-review",
    "video-understand": "video-understand", "xlsx": "xlsx",
}


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def git(cwd: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, timeout=30)


def traiter(kebab: str, nom_depot: str) -> dict:
    entree = {"kebab": kebab, "dossier_depot_avant": nom_depot}
    src_skill = LOCAL / kebab / "SKILL.md"
    src_arch = LOCAL / kebab / "references" / "plateforme-original.md"

    # 1. Renommage éventuel dans le dépôt (git mv pour traçabilité)
    dst_dir = REPO_SKILLS / kebab
    if nom_depot != kebab:
        ancien = REPO_SKILLS / nom_depot
        if ancien.exists() and not dst_dir.exists():
            r = git(DEPOT, "mv", f"skills/{nom_depot}", f"skills/{kebab}")
            if r.returncode != 0 or not dst_dir.exists():
                # repli : les fichiers du dépôt sont suivis, mv + git add
                ancien.rename(dst_dir)
                r2 = git(DEPOT, "add", f"skills/{kebab}", f"skills/{nom_depot}")
                if r2.returncode != 0:
                    entree.update({"statut": "ECHEC_RENOMMAGE",
                                   "detail": (r.stderr or r2.stderr).strip()[:120]})
                    return entree
            entree["renommage"] = "git mv"
        elif dst_dir.exists() and not ancien.exists():
            entree["renommage"] = "DEJA_RENOMME"
        else:
            entree["renommage"] = "NON_REQUIS"
    else:
        entree["renommage"] = "NON_REQUIS"

    # 2. SKILL.md réécrit
    dst_skill = dst_dir / "SKILL.md"
    if not dst_dir.exists():
        entree.update({"statut": "DOSSIER_ABSENT"})
        return entree
    if dst_skill.exists() and sha256(dst_skill) == sha256(src_skill):
        entree["skill_md"] = "DEJA_SYNCHRO"
    else:
        dst_skill.write_bytes(src_skill.read_bytes())
        entree["skill_md"] = "SYNCHRO" if sha256(dst_skill) == sha256(src_skill) else "SHA_DIFFERENT"

    # 3. Archive R4
    dst_refs = dst_dir / "references"
    dst_arch = dst_refs / "plateforme-original.md"
    if dst_arch.exists() and sha256(dst_arch) == sha256(src_arch):
        entree["archive"] = "DEJA_SYNCHRO"
    else:
        dst_refs.mkdir(parents=True, exist_ok=True)
        dst_arch.write_bytes(src_arch.read_bytes())
        entree["archive"] = "SYNCHRO" if sha256(dst_arch) == sha256(src_arch) else "SHA_DIFFERENT"

    entree["statut"] = "OK" if "DIFFERENT" not in f"{entree.get('skill_md')}{entree.get('archive')}" else "SHA_DIFFERENT"
    return entree


def main() -> int:
    resultats = [traiter(k, n) for k, n in CIBLES.items()]

    # git add des modifications (le dépôt exige un add explicite des nouveaux fichiers)
    git(DEPOT, "add", "skills/")

    rapport = {
        "tache": "Task 113 — synchronisation dépôt canonique (16 réécritures plateforme)",
        "horodatage": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "resultats": resultats,
        "synthese": {
            "ok": sum(1 for r in resultats if r["statut"] == "OK"),
            "problemes": [r for r in resultats if r["statut"] != "OK"],
        },
    }
    RAPPORT.write_text(json.dumps(rapport, ensure_ascii=False, indent=2), encoding="utf-8")

    for r in resultats:
        print(f"  {r['statut']:14s} {r['kebab']:20s} renommage={r.get('renommage', '—'):12s} "
              f"skill={r.get('skill_md', '—'):12s} archive={r.get('archive', '—')}")
    print(f"RAPPORT : {RAPPORT}")
    return 1 if rapport["synthese"]["problemes"] else 0


if __name__ == "__main__":
    sys.exit(main())
