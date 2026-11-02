#!/usr/bin/env python3
"""construire-zip-tsi.py — construit zip-tsi.zip (source de vérité portable) v1.1.0.

v1.1.0 (Task 40, correct-work G2) : entrées à date figée 1980-01-01 — le
zip devient byte-identique au re-jeu indépendamment des mtime (R6). Le
writestr horodatat le manifeste à l'heure courante : source de non-
déterminisme attrapée par le correct-work Task 40 (re-jeus sha divergents
masqués par la granularité 2 s du format zip).


Héritage : generate_zip_tsi.py (discussion L10 « Recherche historique
agents TSI »). Convergence $facon : l'archive embarque la toolchain, le
prompt maître tsi-agent.md, les manifestes des skills TSI de l'écosystème
et les exemples — reconstruite à l'identique (déterministe : sha256 ×2).

Usage : python3 construire-zip-tsi.py [--sortie zip-tsi.zip]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import zipfile

RACINE_DEPOT = os.path.dirname(os.path.abspath(__file__))
RACINE_TOOLKIT = os.path.join(RACINE_DEPOT, "tsi-toolkit")


def ajouter_dossier(zf: zipfile.ZipFile, dossier: str, prefixe: str) -> int:
    n = 0
    for racine, _, fichiers in sorted(os.walk(dossier)):
        for f in sorted(fichiers):
            if f.endswith((".pyc", "__init__.pyc")) or "__pycache__" in racine:
                continue
            chemin = os.path.join(racine, f)
            relatif = os.path.join(
                prefixe, os.path.relpath(chemin, dossier))
            # entrées à date figée (1980-01-01) — zip déterministe
            # byte-identique au re-jeu, indépendant des mtime (R6)
            info = zipfile.ZipInfo(relatif, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, open(chemin, "rb").read())
            n += 1
    return n


def main() -> int:
    parseur = argparse.ArgumentParser(description=__doc__)
    parseur.add_argument("--sortie", default="zip-tsi.zip")
    args = parseur.parse_args()

    manifeste = {
        "nom": "zip-tsi",
        "version": "1.0.0",
        "description": "Source de vérité portable de l'écosystème TSI — "
                       "toolchain + prompt maître + manifestes skills",
        "contenu": {
            "tsi-toolkit/": "toolchain Python stdlib (inspect/generate/"
                            "validate/convert/coverage/studio)",
            "tsi-agent.md": "Ultra Prompt Maître idempotent (exécution Z.ai)",
            "manifestes-skills/": "SKILL.md de la famille TSI écosystème",
        },
    }
    compte = 0
    with zipfile.ZipFile(args.sortie, "w", zipfile.ZIP_DEFLATED) as zf:
        info = zipfile.ZipInfo("zip-tsi/manifeste.json",
                               date_time=(1980, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        zf.writestr(info, json.dumps(manifeste, ensure_ascii=False, indent=1))
        compte += ajouter_dossier(zf, RACINE_TOOLKIT, "zip-tsi/tsi-toolkit")
        agent = os.path.join(RACINE_DEPOT, "tsi-agent.md")
        if os.path.isfile(agent):
            info = zipfile.ZipInfo("zip-tsi/tsi-agent.md",
                                   date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            zf.writestr(info, open(agent, "rb").read())
            compte += 1
        skills = os.path.join(RACINE_DEPOT, "skills")
        for nom in ("tsi-architect", "tsi-validator", "multi-shift-architect",
                    "orchestrateur-tsi", "analyse-doc-s4mk2", "midi-doc-expert"):
            chemin = os.path.join(skills, nom, "SKILL.md")
            if os.path.isfile(chemin):
                cible = f"zip-tsi/manifestes-skills/{nom}-SKILL.md"
                info = zipfile.ZipInfo(cible, date_time=(1980, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                zf.writestr(info, open(chemin, "rb").read())
                compte += 1

    empreinte = hashlib.sha256(open(args.sortie, "rb").read()).hexdigest()
    taille = os.path.getsize(args.sortie)
    print(f"✅ {args.sortie} : {compte} fichiers + manifeste — "
          f"{taille} octets — sha256 {empreinte[:16]}…")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
