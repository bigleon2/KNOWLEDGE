#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.47)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).
"""

"""Task 114 — Réparation de la réinjection plateforme (trace 1a2025197d2a0e9d).

Constat (Task 113 → Task 114, récidive documentée) : la plateforme RÉINJECTE ses
skills natifs au démarrage de session — les 17 SKILL.md français posés par Task 113
sont écrasés par les versions natives anglaises (agent-browser clawdbot, charts, docx,
pdf, pptx, xlsx, image-*, video-understand, gif-animator*, task-review) et les 4
dossiers majuscules ASR/LLM/TTS/VLM sont RECRÉÉS (renommés kebab-case dans le dépôt).

Réparation canonique (règle d'or n°4 — source de vérité = miroir KNOWLEDGE-repo) :
  1. Restauration des 13 SKILL.md français depuis le miroir (garde : la version
     miroir doit porter le §0 SHARED — jamais restaurer une version non conforme).
  2. Suppression des 4 dossiers majuscules réinjectés (garde préalable : l'archive
     R4 references/plateforme-original.md du dossier réinjecté doit être
     byte-identique à celle du jumeau kebab-case du miroir — preuve que le contenu
     réinjecté = contenu d'origine déjà archivé ; sinon REPROTÉ, jamais détruit).
Idempotent ×2 : second passage = aucun changement (0 restauration, 0 suppression).
Sortie : download/rapport-task114-reparation-reinjection.json
"""
import hashlib
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

RACINE = Path("/home/z/my-project")
SKILLS = RACINE / "skills"
MIROIR = RACINE / "KNOWLEDGE-repo" / "skills"
RAPPORT = RACINE / "download" / "rapport-task114-reparation-reinjection.json"

# 13 skills réinjectés dont le dossier est kebab-case (même nom hôte et miroir)
RESTAURER = [
    "agent-browser", "charts", "docx", "gif-animator", "gif-animator-pro",
    "image-edit", "image-generation", "image-search", "pdf", "pptx",
    "task-review", "video-understand", "xlsx",
]
# 4 dossiers majuscules réinjectés — jumeau kebab-case dans le miroir
MAJUSCULES = {"ASR": "asr", "LLM": "llm", "TTS": "tts", "VLM": "vlm"}

GARDE_SHARED = "Contexte Système"


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    resultats = {"restaurations": [], "suppressions": [], "reportes": [],
                 "deja_faits": []}

    for nom in RESTAURER:
        src, dst = MIROIR / nom / "SKILL.md", SKILLS / nom / "SKILL.md"
        if not src.exists():
            resultats["reportes"].append({"skill": nom, "motif": "miroir absent"})
            continue
        texte_src = src.read_text(encoding="utf-8", errors="replace")
        if GARDE_SHARED not in texte_src:
            resultats["reportes"].append(
                {"skill": nom, "motif": "version miroir sans §0 SHARED — garde anti-régression"})
            continue
        if dst.exists() and dst.read_text(encoding="utf-8", errors="replace") == texte_src:
            resultats["deja_faits"].append(nom)
            continue
        dst.write_text(texte_src, encoding="utf-8")
        resultats["restaurations"].append(
            {"skill": nom, "sha_restauré": sha256(dst)[:16]})

    for maj, kebab in MAJUSCULES.items():
        dossier = SKILLS / maj
        if not dossier.exists():
            resultats["deja_faits"].append(maj + " (absent)")
            continue
        # Garde anti-perte : l'archive R4 du dossier réinjecté doit être
        # byte-identique à celle du jumeau kebab-case du miroir.
        arc_hote = dossier / "references" / "plateforme-original.md"
        arc_miroir = MIROIR / kebab / "references" / "plateforme-original.md"
        if not (arc_hote.exists() and arc_miroir.exists()
                and sha256(arc_hote) == sha256(arc_miroir)):
            resultats["reportes"].append(
                {"skill": maj, "motif": "archive R4 absente ou divergente — REPORTÉ, jamais détruit"})
            continue
        shutil.rmtree(dossier)
        resultats["suppressions"].append({"skill": maj, "jumeau": kebab})

    rapport = {
        "tache": "Task 114 réparation réinjection plateforme",
        "trace": "1a2025197d2a0e9d",
        "horodatage": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "synthese": {"restaurés": len(resultats["restaurations"]),
                     "supprimés": len(resultats["suppressions"]),
                     "déjà_faits": len(resultats["deja_faits"]),
                     "reportés": len(resultats["reportes"])},
        "resultats": resultats,
    }
    RAPPORT.parent.mkdir(parents=True, exist_ok=True)
    RAPPORT.write_text(json.dumps(rapport, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(rapport["synthese"], ensure_ascii=False))
    if resultats["reportes"]:
        print("REPORTÉS :", json.dumps(resultats["reportes"], ensure_ascii=False))
    print("RAPPORT :", RAPPORT)
    return 0


if __name__ == "__main__":
    sys.exit(main())
