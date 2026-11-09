#!/usr/bin/env python3
"""ghorg-install.py — D4 du PM ghorg-to-ecosysteme.md v1.1 : GHORG local, idempotent.

Étapes (relevé d'état AVANT chaque action — Karnaugh appliqué aux autres étapes, PM §7) :
  1. Source : fork bigleon2/ghorg s'il existe, sinon source gabrie30/ghorg (repli documenté).
  2. Clone ~/GitHub/_outils/ghorg : absent → clone ; présent et propre → fetch + pull --ff-only ;
     présent et sale → ALERTE, aucune modification.
  3. Remote upstream = gabrie30/ghorg (ajouté ou corrigé).
  4. Build conditionnel : seulement si le binaire est absent ou si .ghorg-commit != SHA courant.
  5. PATH utilisateur : ajout de ~/GitHub/_outils/bin à ~/.bashrc (une seule fois, sans doublon).

Sortie : JSON {action, source_utilisee, sha, build, path_ajoute}. Exit 0 idempotent.
"""

import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _commun import (  # noqa: E402
    GHORG_BIN, GHORG_FORK, GHORG_MARQUEUR, GHORG_SOURCE, GHORG_SRC,
    branche_courante, depot_existant, git, horodatage, maj_etat, porcelain_vide, run,
)

URL_FORK = f"https://github.com/{GHORG_FORK}.git"
URL_SOURCE = f"https://github.com/{GHORG_SOURCE}.git"
LIGNE_PATH = 'export PATH="$HOME/GitHub/_outils/bin:$PATH"\n'


def trouver_go():
    """Localise l'exécutable go (PATH, puis tarball officiel ~/go/bin/go)."""
    chemin = shutil.which("go")
    if chemin:
        return chemin, {}
    tarball = Path.home() / "go" / "bin" / "go"
    if tarball.exists():
        # GOROOT/GOPATH explicites : évite le conflit GOPATH==GOROOT du tarball officiel.
        return str(tarball), {
            "GOROOT": str(Path.home() / "go"),
            "GOPATH": str(Path.home() / "gopath"),
        }
    return None, {}


def main():
    rapport = {"horodatage": horodatage(), "action": [], "erreurs": []}

    # 1. Source : fork si présent, sinon source (repli §4 documenté).
    fork_present = depot_existant(URL_FORK)
    url = URL_FORK if fork_present else URL_SOURCE
    rapport["source_utilisee"] = GHORG_FORK if fork_present else GHORG_SOURCE
    if not fork_present:
        rapport["action"].append(
            f"REPLI : fork {GHORG_FORK} ABSENT — clone depuis la source {GHORG_SOURCE} "
            "(origin à re-pointer vers le fork quand il existera)"
        )

    # 2. Clone local.
    if (GHORG_SRC / ".git").exists():
        if porcelain_vide(GHORG_SRC):
            git(["fetch", "origin", "--prune"], cwd=GHORG_SRC)
            branche = branche_courante(GHORG_SRC) or "master"
            code, sortie = git(["pull", "--ff-only"], cwd=GHORG_SRC)
            rapport["action"].append(
                "déjà à jour" if code == 0 and "Already up to date" in sortie
                else f"mise à jour pull --ff-only ({branche})"
            )
            if code != 0:
                rapport["erreurs"].append(f"pull --ff-only : {sortie}")
        else:
            rapport["erreurs"].append(
                "clone ghorg local SALE — aucune modification (relever l'état avant action, PM §7)"
            )
    else:
        GHORG_SRC.parent.mkdir(parents=True, exist_ok=True)
        code, sortie = git(["clone", url, str(GHORG_SRC)])
        if code != 0:
            rapport["erreurs"].append(f"clone : {sortie}")
            print(json.dumps(rapport, ensure_ascii=False, indent=2))
            return 1
        rapport["action"].append(f"clone {rapport['source_utilisee']}")

    # 3. Remote upstream.
    code, url_up = git(["remote", "get-url", "upstream"], cwd=GHORG_SRC)
    if code != 0:
        git(["remote", "add", "upstream", URL_SOURCE], cwd=GHORG_SRC)
        rapport["action"].append("remote upstream ajouté")
    elif url_up.strip() != URL_SOURCE:
        git(["remote", "set-url", "upstream", URL_SOURCE], cwd=GHORG_SRC)
        rapport["action"].append("remote upstream corrigé")

    # 4. SHA courant + build conditionnel.
    _, sha = git(["rev-parse", "HEAD"], cwd=GHORG_SRC)
    sha = sha.strip()
    marqueur = GHORG_MARQUEUR.read_text(encoding="utf-8").strip() if GHORG_MARQUEUR.exists() else ""
    if GHORG_BIN.exists() and marqueur == sha:
        rapport["build"] = "déjà à jour (binaire == SHA du clone)"
    else:
        go, env_go = trouver_go()
        if go is None:
            rapport["build"] = "NON VÉRIFIÉ (go ABSENT — PM §4 : ne pas contourner)"
            rapport["erreurs"].append("go introuvable")
        else:
            GHORG_BIN.parent.mkdir(parents=True, exist_ok=True)
            code, sortie = run([go, "build", "-o", str(GHORG_BIN), "."], cwd=GHORG_SRC, env_extra=env_go, timeout=900)
            if code == 0:
                GHORG_MARQUEUR.write_text(sha + "\n", encoding="utf-8")
                rapport["build"] = f"compilé ({sha[:12]})"
                rapport["action"].append("go build exécuté")
            else:
                rapport["build"] = "ÉCHEC"
                rapport["erreurs"].append(sortie[-500:])
    rapport["sha"] = sha

    # 5. PATH utilisateur (~/.bashrc, une seule fois).
    bashrc = Path.home() / ".bashrc"
    contenu = bashrc.read_text(encoding="utf-8") if bashrc.exists() else ""
    if "GitHub/_outils/bin" not in contenu:
        with open(bashrc, "a", encoding="utf-8") as f:
            f.write("\n# ghorg (écosystème — PM ghorg-to-ecosysteme.md)\n" + LIGNE_PATH)
        rapport["path_ajoute"] = True
    else:
        rapport["path_ajoute"] = False

    maj_etat("D4_ghorg_local", "terminé", sha)
    print(json.dumps(rapport, ensure_ascii=False, indent=2))
    return 0 if not rapport["erreurs"] else 2


if __name__ == "__main__":
    sys.exit(main())
