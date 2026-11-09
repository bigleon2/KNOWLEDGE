#!/usr/bin/env python3
"""bootstrap.py — PM ghorg-to-ecosysteme.md v1.1 : enchaîne D4 → D5 → D6, re-scelle le manifeste. Idempotent.

Étapes :
  0. Journal d'état §10 lu au démarrage (reprise : ne pas refaire ce qui est terminé).
  1. ghorg-install.py (D4 : GHORG local compilé, marqueur .ghorg-commit).
  2. cmdr-clone.py (D5 : Karnaugh F/L/S/B — clone/mise à jour de CMDR).
  3. cmdr-overlay-sync.py (D6 : superposition famille TSI, SHA-256, SOURCE.md).
  4. Manifeste skills/@GHORG-ecosysteme/manifest.yaml RÉÉCRIT avec les valeurs réelles du jour
     (git rev-parse / git ls-remote — jamais de mémoire) ; réécriture seulement
     si le contenu diffère (idempotence : la 2e exécution ne produit aucun changement git).

Sortie : JSON récapitulatif. Exit 0 si tout « déjà à jour » ou réussi, code d'erreur sinon.
"""

import json
import subprocess
import sys
from pathlib import Path

ICI = Path(__file__).parent
sys.path.insert(0, str(ICI))
from _commun import (  # noqa: E402
    CMDR, CMDR_SOURCE, GHORG_FORK, GHORG_SOURCE, GHORG_SRC, KNOWLEDGE,
    depot_existant, git, horodatage, maj_etat, run,
)

# Task 70 G3 : le dossier GHORG du dépôt vit désormais sous skills/@GHORG-ecosysteme/
# (git mv R4 — directive propriétaire) ; la branche overlay CMDR et le dossier
# cmdr/ecosystem/ (cible de superposition) restent INCHANGÉS.
MANIFESTE = KNOWLEDGE / "skills" / "@GHORG-ecosysteme" / "manifest.yaml"
URL_GHORG_SOURCE = f"https://github.com/{GHORG_SOURCE}.git"
URL_CMDR_SOURCE = f"https://github.com/{CMDR_SOURCE}.git"


def executer(script):
    """Exécute un script sibling, renvoie (code, json_sortie ou texte)."""
    proc = subprocess.run(
        [sys.executable, str(ICI / script)], capture_output=True, text=True, timeout=1800
    )
    try:
        donnees = json.loads(proc.stdout)
    except json.JSONDecodeError:
        donnees = {"sortie": (proc.stdout + proc.stderr)[-500:]}
    return proc.returncode, donnees


def sha_ls_remote(url):
    """SHA HEAD distant (canal git natif anonyme — règle d'or n°4) ou ABSENT."""
    code, sortie = git(["ls-remote", url, "HEAD"])
    return sortie.split()[0] if code == 0 and sortie else "ABSENT"


def construire_manifeste():
    """Régénère le contenu du manifeste avec les valeurs réelles relevées par commande.

    cmdr.commit_epingle épingle la BRANCHE PAR DÉFAUT (master) du clone — l'état
    amont suivi — et NON le HEAD courant : la procédure elle-même fait bouger le HEAD
    (commits de superposition sur la branche overlay), épingle qui serait alors
    auto-invalide à chaque exécution (faille de couplage découverte au contrat §8).
    """
    _, sha_ghorg = git(["rev-parse", "HEAD"], cwd=GHORG_SRC)
    sha_ghorg = sha_ghorg.strip() if (GHORG_SRC / ".git").exists() else "ABSENT"
    _, sha_cmdr = git(["rev-parse", "master"], cwd=CMDR)
    sha_cmdr = sha_cmdr.strip() if (CMDR / ".git").exists() else "ABSENT"
    licence = "ABSENT"
    for nom in ("LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING"):
        p = CMDR / nom
        if p.exists():
            licence = f"{nom} (voir dépôt — aucune conclusion juridique)"
            break
    fork_ghorg = "présent" if depot_existant(f"https://github.com/{GHORG_FORK}.git") else "ABSENT (ls-remote anonyme — création différée au propriétaire)"
    fork_cmdr = "présent" if depot_existant("https://github.com/bigleon2/cmdr.git") else "ABSENT (ls-remote anonyme — création différée au propriétaire)"
    return (
        "version: 1\n"
        "proprietaire: bigleon2\n"
        "note: \"Fichier réécrit mécaniquement par scripts/ecosystem/bootstrap.py — SHA relevés "
        "par commande (git rev-parse / git ls-remote), jamais écrits de mémoire. L'horodatage "
        "n'est réécrit QUE si le contenu stable diffère (idempotence — faille du §8 résorbée).\"\n"
        f"genere_le: {horodatage()}\n"
        "outils:\n"
        "  ghorg:\n"
        f"    source: {GHORG_SOURCE}\n"
        f"    fork: {GHORG_FORK}\n"
        f"    fork_existant: {fork_ghorg}\n"
        "    clone_local: ~/GitHub/_outils/ghorg\n"
        f"    commit_epingle: {sha_ghorg}\n"
        f"    commit_source_distant: {sha_ls_remote(URL_GHORG_SOURCE)}\n"
        "applications:\n"
        "  cmdr:\n"
        f"    source: {CMDR_SOURCE}\n"
        "    fork: bigleon2/cmdr\n"
        f"    fork_existant: {fork_cmdr}\n"
        "    clone_local: ~/GitHub/bigleon2/cmdr\n"
        "    origin_actuel: cmdr-editor/cmdr (repli documenté — re-pointer vers le fork quand il existera)\n"
        "    branche_par_defaut: master\n"
        "    branche_superposition: ecosystem/tsi-traktor-s4mk2\n"
        f"    commit_epingle: {sha_cmdr}\n"
        f"    commit_source_distant: {sha_ls_remote(URL_CMDR_SOURCE)}\n"
        f"    licence: {licence}\n"
        "disposition_locale:\n"
        "  racine: ~/GitHub\n"
        "  dossier_outils: _outils\n"
        "recloner:\n"
        "  nom_entree: cmdr-editor-fork\n"
        "superposition:\n"
        "  dossier_cible_dans_cmdr: ecosystem\n"
        "  fichier_selection: skills/@GHORG-ecosysteme/selection-tsi.yaml\n"
    )


def manifeste_stable(contenu):
    """Retire la ligne volatile genere_le (comparaison de contenu stable)."""
    return "\n".join(l for l in contenu.splitlines() if not l.startswith("genere_le:"))


def main():
    resume = {"horodatage": horodatage(), "etapes": []}
    for nom, script in (("D4", "ghorg-install.py"), ("D5", "cmdr-clone.py"), ("D6", "cmdr-overlay-sync.py")):
        code, donnees = executer(script)
        resume["etapes"].append({"bloc": nom, "script": script, "exit": code, "resume": donnees})
        if code not in (0,) and not (nom == "D5" and code == 3):
            resume["erreurs"] = True
            print(json.dumps(resume, ensure_ascii=False, indent=2))
            return 1

    # Manifeste : réécriture seulement si le CONTENU STABLE diffère (idempotence —
    # la ligne genere_le volatile ne déclenche jamais une réécriture seule).
    contenu = construire_manifeste()
    actuel = MANIFESTE.read_text(encoding="utf-8") if MANIFESTE.exists() else ""
    if actuel and manifeste_stable(actuel) == manifeste_stable(contenu):
        resume["manifeste"] = "déjà à jour (contenu stable identique — aucun changement git)"
    else:
        MANIFESTE.parent.mkdir(parents=True, exist_ok=True)
        MANIFESTE.write_text(contenu, encoding="utf-8")
        resume["manifeste"] = "réécrit (SHA réels du jour)"
    maj_etat("phase_E_verification", "a_faire")
    print(json.dumps(resume, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
