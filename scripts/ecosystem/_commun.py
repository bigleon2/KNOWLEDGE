#!/usr/bin/env python3
"""Helpers partagés des scripts ecosystem/ (PM ghorg-to-ecosysteme.md v1.1, Task 51).

Conventions : stdlib uniquement (portabilité poste propriétaire), chemins ancrés
sur la disposition locale du PM §4, sorties JSON déterministes, idempotence.
"""

import json
import os
import subprocess
import time
from pathlib import Path

# --- Disposition locale (PM §4) ---
RACINE_GITHUB = Path.home() / "GitHub"
OUTILS = RACINE_GITHUB / "_outils"
GHORG_SRC = OUTILS / "ghorg"
GHORG_BIN = OUTILS / "bin" / "ghorg"
GHORG_MARQUEUR = OUTILS / "bin" / ".ghorg-commit"
CIBLES_CMDR = OUTILS / "cmdr-cibles.txt"
KNOWLEDGE = RACINE_GITHUB / "bigleon2" / "KNOWLEDGE"
CMDR = RACINE_GITHUB / "bigleon2" / "cmdr"
ETAT_JSON = OUTILS / "etat-ghorg-ecosysteme.json"

# --- Dépôts distants ---
GHORG_SOURCE = "gabrie30/ghorg"
GHORG_FORK = "bigleon2/ghorg"
CMDR_SOURCE = "cmdr-editor/cmdr"
CMDR_FORK = "bigleon2/cmdr"
BRANCHE_SUPERPOSITION = "ecosystem/tsi-traktor-s4mk2"

SECRET_MOTIFS = ("ghp_", "github_pat_", "gho_", "Bearer ")


def run(cmd, cwd=None, env_extra=None, timeout=300):
    """Exécute une commande, renvoie (code, sortie). GIT_TERMINAL_PROMPT=0 : jamais d'invite bloquante."""
    env = dict(os.environ)
    env["GIT_TERMINAL_PROMPT"] = "0"
    env["LC_ALL"] = "C"
    if env_extra:
        env.update(env_extra)
    proc = subprocess.run(
        cmd, cwd=str(cwd) if cwd else None, env=env,
        capture_output=True, text=True, timeout=timeout,
    )
    return proc.returncode, (proc.stdout + proc.stderr).strip()


def git(args, cwd=None, timeout=300):
    """Commande git — renvoie (code, sortie)."""
    return run(["git"] + args, cwd=cwd, timeout=timeout)


def depot_existant(url):
    """Vrai si le dépôt distant public existe (ls-remote anonyme, sans jeton — règle d'or n°4)."""
    code, _ = git(["ls-remote", "--heads", url], timeout=60)
    return code == 0


def sha256_fichier(chemin):
    """SHA-256 d'un fichier (lecture par blocs)."""
    import hashlib
    h = hashlib.sha256()
    with open(chemin, "rb") as f:
        for bloc in iter(lambda: f.read(65536), b""):
            h.update(bloc)
    return h.hexdigest()


def porcelain_vide(cwd):
    """Vrai si l'arbre git local est propre (S=0 du Karnaugh)."""
    code, sortie = git(["status", "--porcelain"], cwd=cwd)
    return code == 0 and sortie == ""


def branche_courante(cwd):
    """Nom de la branche courante (relevé B du Karnaugh) — None si détaché/vide."""
    code, sortie = git(["branch", "--show-current"], cwd=cwd)
    return sortie if code == 0 and sortie else None


def horodatage():
    """Horodatage ISO UTC (traces déterministes par exécution)."""
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def maj_etat(cle, valeur, sha=None):
    """Met à jour le journal d'état §10 (reprise : lire, ne pas refaire ce qui est terminé)."""
    etat = {}
    if ETAT_JSON.exists():
        try:
            etat = json.loads(ETAT_JSON.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            etat = {}
    etat.setdefault("phases", {})[cle] = valeur
    etat["maj"] = horodatage()
    if sha:
        etat["dernier_commit_concerne"] = sha
    ETAT_JSON.parent.mkdir(parents=True, exist_ok=True)
    ETAT_JSON.write_text(
        json.dumps(etat, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def scan_secrets(texte):
    """Vrai si un motif de secret apparaît (garde n°4 du PM — avant commit)."""
    return any(m in texte for m in SECRET_MOTIFS)
