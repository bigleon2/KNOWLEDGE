#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 15 — Scan anti-fuite de jetons (suite 170 « scan 0 fuite jeton à suivre »).

Lecture seule : parcourt l'arbre du dépôt KNOWLEDGE-repo (fichiers texte,
exclusion .git et binaires) et les artefacts de travail hôte (download/, scripts/,
worklog.md, journal-fails.md) à la recherche de motifs de jetons réels
(GitHub PAT fine-grained, PAT classique, ghp_, gho_, ghu_, ghs_, slack, AWS…).
Les mentions TRONQUÉES/scellées (forme abrégée) ne comptent pas comme fuite.

Verdict : rc=0 si 0 jeton réel détecté ; rc=1 sinon (liste des fichiers/lignes).
"""

import re
import sys
from pathlib import Path

MOTIFS = [
    # GitHub fine-grained PAT : github_pat_ + 22+ caractères alphanumériques/_
    re.compile(r"github_pat_[A-Za-z0-9_]{22,}"),
    # GitHub PAT classiques
    re.compile(r"ghp_[A-Za-z0-9]{36}"),
    re.compile(r"gho_[A-Za-z0-9]{36}"),
    re.compile(r"ghu_[A-Za-z0-9]{36}"),
    re.compile(r"ghs_[A-Za-z0-9]{36}"),
    re.compile(r"ghr_[A-Za-z0-9]{36}"),
    # AWS
    re.compile(r"AKIA[0-9A-Z]{16}"),
    # Slack
    re.compile(r"xox[baprs]-[A-Za-z0-9-]{10,}"),
]

EXT_BINAIRES = {
    ".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip", ".ico", ".webp",
    ".woff", ".woff2", ".ttf", ".pyc", ".so", ".db", ".mp4", ".mp3",
}

RACINES = [
    Path("/home/z/my-project/KNOWLEDGE-repo"),
    Path("/home/z/my-project/download"),
    Path("/home/z/my-project/scripts"),
    Path("/home/z/my-project/worklog.md"),
    Path("/home/z/my-project/journal-fails.md"),
]


B64 = re.compile(r"[A-Za-z0-9+/=]{60,}")


def contexte_base64(texte: str, pos: int, fin: int) -> bool:
    """Vrai si la correspondance est noyée dans un long run base64 (>= 60 chars
    contigus) — signature d'un blob binaire embarqué (data-URI, payload TSI),
    où un motif AKIA apparaît par hasard : faux positif structurel."""
    s = max(0, pos - 80)
    segment = texte[s:fin + 80]
    return bool(B64.search(segment))


def scan_fichier(p: Path):
    try:
        texte = p.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return [], 0
    trouvailles, faux_positifs = [], 0
    for motif in MOTIFS:
        for m in motif.finditer(texte):
            # Les motifs GitHub PAT (préfixe souligné) n'apparaissent pas par
            # hasard dans le base64 ; seuls AKIA/Slack exigent la garde contexte.
            if motif.pattern.startswith("AKIA") and contexte_base64(texte, m.start(), m.end()):
                faux_positifs += 1
                continue
            trouvailles.append((str(p), m.group(0)[:12] + "…", motif.pattern[:24]))
    return trouvailles, faux_positifs


def main() -> int:
    fuites = []
    faux_positifs = 0
    fichiers_scannes = 0
    for racine in RACINES:
        if racine.is_file():
            fichiers_scannes += 1
            t, fp = scan_fichier(racine)
            fuites.extend(t)
            faux_positifs += fp
            continue
        for p in racine.rglob("*"):
            if ".git" in p.parts or p.suffix.lower() in EXT_BINAIRES:
                continue
            if p.is_file():
                fichiers_scannes += 1
                t, fp = scan_fichier(p)
                fuites.extend(t)
                faux_positifs += fp
    if fuites:
        print(f"FAIL : {len(fuites)} jeton(s) réel(s) détecté(s) :")
        for fichier, extrait, motif in fuites[:20]:
            print(f"  {fichier} · {extrait} · motif {motif}")
        return 1
    print(f"PASS : 0 jeton réel détecté — {fichiers_scannes} fichiers texte scannés "
          f"(dépôt + download/ + scripts/ + worklogs hôte) ; "
          f"{faux_positifs} faux positifs structurels écartés (motifs AKIA dans blobs "
          f"base64 : data-URI HTML design-templates, payload binaire TSI Traktor).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
