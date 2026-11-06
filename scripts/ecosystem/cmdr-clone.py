#!/usr/bin/env python3
"""cmdr-clone.py — D5 du PM ghorg-to-ecosysteme.md v1.1 : clone de CMDR selon la table de Karnaugh F/L/S/B.

Les 4 variables sont relevées AVANT toute action (PM §7) :
  F = fork bigleon2/cmdr existe sur GitHub (ls-remote anonyme) ;
  L = clone local ~/GitHub/bigleon2/cmdr existe ;
  S = clone local sale (git status --porcelain non vide) — testé seulement si L=1 ;
  B = branche courante == ecosystem/tsi-traktor-s4mk2 — testé seulement si L=1.

Règles (PM §7, tableau 4x4 — GHORG n'est autorisé QUE règles 1, 2 et 5) :
  1. L=0, F=0 → créer le fork puis cloner. Sans jeton : REPLI §4 documenté —
     clonage depuis la source cmdr-editor/cmdr (origin à re-pointer vers le fork plus tard).
  2. L=0, F=1 → cloner (ghorg si disponible et jeton présent, sinon git clone).
  3. L=1, F=0 → STOP P0 (clone orphelin), SAUF si origin pointe déjà vers la source
     (état repli documenté : origin résoluble ≠ orphelin — raffinement Task 51).
  4. L=1, F=1, S=1 → NE_RIEN_MODIFIER + ALERTE (quelle que soit B).
  5. L=1, F=1, S=0, B=0 → reclone ghorg puis checkout de la branche overlay si elle existe.
  6. L=1, F=1, S=0, B=1 → mise à jour ciblée git uniquement (fetch + pull --ff-only overlay,
     JAMAIS de reclone ghorg) ; branche par défaut rafraîchie par fetch sans checkout.

Après tout clonage : remote upstream = cmdr-editor/cmdr (ajouté ou corrigé), fetch --prune.

Sortie : JSON {F, L, S, B, action, origin, notes}. Exit 0 idempotent, 3 sur P0.
"""

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _commun import (  # noqa: E402
    BRANCHE_SUPERPOSITION, CMDR, CMDR_FORK, CMDR_SOURCE, GHORG_BIN,
    branche_courante, depot_existant, git, horodatage, maj_etat, porcelain_vide,
)

URL_FORK = f"https://github.com/{CMDR_FORK}.git"
URL_SOURCE = f"https://github.com/{CMDR_SOURCE}.git"

# Entrée reclone.yaml (D5 — raccourci ghorg reclone cmdr-editor-fork) — UTF-8 sans BOM.
ENTREE_RECLONE = (
    "cmdr-editor-fork:\n"
    "  cmd: ghorg clone bigleon2 --scm=github --clone-type=user "
    "--path=$HOME/GitHub --output-dir=bigleon2 "
    "--target-repos-path=$HOME/GitHub/_outils/cmdr-cibles.txt "
    "--no-clean --concurrency=1\n"
    "  description: Clone du fork bigleon2/cmdr (CMDR EDITOR) via ghorg — idempotent, "
    "sans git clean (Karnaugh F/L/S/B : reclone réservé aux clones propres sur la branche par défaut)\n"
    "  token_cmd: gh auth token\n"
)


def ecrire_entree_reclone(rapport):
    """Fusionne l'entrée cmdr-editor-fork dans ~/.config/ghorg/reclone.yaml (XDG respecté).

    Idempotent : entrée déjà présente et identique → aucun changement. Les autres
    entrées existantes ne sont jamais touchées. Chemin avec espace → avertir, ne pas écrire.
    """
    racine_cfg = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    reclone = racine_cfg / "ghorg" / "reclone.yaml"
    if " " in str(reclone):
        rapport["notes"].append(
            f"reclone.yaml NON écrit : le chemin contient un espace ({reclone}) — avertir, ne pas écrire"
        )
        return
    existant = reclone.read_text(encoding="utf-8") if reclone.exists() else ""
    if "cmdr-editor-fork:" in existant:
        rapport["notes"].append("reclone.yaml : entrée cmdr-editor-fork déjà présente (inchangée)")
        return
    reclone.parent.mkdir(parents=True, exist_ok=True)
    separateur = "" if (not existant or existant.endswith("\n\n")) else "\n"
    reclone.write_text(existant + separateur + ENTREE_RECLONE, encoding="utf-8")
    rapport["notes"].append(f"reclone.yaml : entrée cmdr-editor-fork ajoutée ({reclone})")


def ghorg_utilisable():
    """GHORG utilisable : binaire présent ET jeton disponible (GHORG_GITHUB_TOKEN ou GH_TOKEN)."""
    jeton = os.environ.get("GHORG_GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    return GHORG_BIN.exists() and bool(jeton), bool(jeton)


def cloner(url, rapport):
    """Clonage initial (git direct — le repli git est documenté ; ghorg réservé au reclone règle 5)."""
    CMDR.parent.mkdir(parents=True, exist_ok=True)
    code, sortie = git(["clone", url, str(CMDR)], timeout=600)
    if code != 0:
        rapport["erreurs"].append(f"clone : {sortie}")
        return False
    rapport["action"] = f"CLONER ({'fork' if url == URL_FORK else 'source ' + CMDR_SOURCE + ' — repli documenté'})"
    return True


def main():
    rapport = {"horodatage": horodatage(), "notes": [], "erreurs": []}

    # --- Relevé des 4 variables AVANT action (PM §7) ---
    f = depot_existant(URL_FORK)
    l = (CMDR / ".git").exists()
    s = (not porcelain_vide(CMDR)) if l else False
    b = (branche_courante(CMDR) == BRANCHE_SUPERPOSITION) if l else False
    origin = ""
    if l:
        _, origin = git(["remote", "get-url", "origin"], cwd=CMDR)
        origin = origin.strip()
    rapport.update({"F": int(f), "L": int(l), "S": int(s), "B": int(b), "origin": origin})

    # --- Karnaugh (règles 1-6) ---
    if not l and not f:
        # Règle 1 : fork à créer (jeton requis) → repli §4 : clonage depuis la source.
        rapport["notes"].append(
            f"règle 1 (F=0, L=0) : fork {CMDR_FORK} à créer par le propriétaire (jeton requis, "
            "KO-L009 point 5) — REPLI documenté : clonage depuis la source"
        )
        ok = cloner(URL_SOURCE, rapport)
        if not ok:
            print(json.dumps(rapport, ensure_ascii=False, indent=2))
            return 1
    elif not l and f:
        # Règle 2 : cloner le fork.
        rapport["notes"].append("règle 2 (F=1, L=0) : clonage du fork")
        ok = cloner(URL_FORK, rapport)
        if not ok:
            print(json.dumps(rapport, ensure_ascii=False, indent=2))
            return 1
    elif l and not f:
        if origin and "cmdr-editor/cmdr" in origin:
            # Raffinement Task 51 : origin résoluble (repli documenté) ≠ orphelin.
            rapport["notes"].append(
                "règle 3 (F=0, L=1) raffinée : origin = source cmdr-editor/cmdr (état repli "
                "documenté, origin résoluble) — mise à jour ciblée, PAS un orphelin"
            )
            if not s:
                git(["fetch", "origin", "--prune"], cwd=CMDR)
                git(["pull", "--ff-only"], cwd=CMDR)
                rapport["action"] = "MISE_À_JOUR_CIBLÉE (repli source)"
            else:
                rapport["action"] = "NE_RIEN_MODIFIER + ALERTE (clone sale)"
        else:
            rapport["action"] = "STOP (P0) — clone local orphelin : origin à vérifier par l'utilisateur"
            rapport["erreurs"].append(
                f"règle 3 (F=0, L=1) : fork absent et origin '{origin}' ne pointe pas vers la source"
            )
            print(json.dumps(rapport, ensure_ascii=False, indent=2))
            return 3
    elif l and f and s:
        # Règle 4 : clone sale — ne rien modifier, quelle que soit la branche.
        rapport["action"] = "NE_RIEN_MODIFIER + ALERTE (modifications locales non commitées)"
        rapport["notes"].append("règle 4 (S=1) : alerter dans le rapport, ne rien modifier")
    elif l and f and not s and not b:
        # Règle 5 : clone propre sur la branche par défaut → reclone ghorg puis checkout overlay.
        dispo, jeton = ghorg_utilisable()
        if dispo:
            rapport["notes"].append("règle 5 (S=0, B=0) : reclone ghorg autorisé")
            rapport["action"] = "GHORG RECLONE (non exécuté ici — voir bootstrap)"
        else:
            rapport["notes"].append(
                "règle 5 (S=0, B=0) : ghorg non utilisable"
                + (" (jeton ABSENT — KO-L009)" if not jeton else " (binaire absent)")
                + " → mise à jour git ciblée (repli documenté)"
            )
            git(["fetch", "origin", "--prune"], cwd=CMDR)
            git(["pull", "--ff-only"], cwd=CMDR)
            rapport["action"] = "MISE_À_JOUR_CIBLÉE (repli git)"
        _, branches = git(["branch", "--list", BRANCHE_SUPERPOSITION], cwd=CMDR)
        if branches.strip():
            git(["checkout", BRANCHE_SUPERPOSITION], cwd=CMDR)
            rapport["notes"].append(f"checkout {BRANCHE_SUPERPOSITION} (branche existante)")
    else:
        # Règle 6 : clone propre sur la branche overlay → git uniquement, JAMAIS reclone ghorg.
        rapport["notes"].append(
            f"règle 6 (S=0, B=1) : mise à jour ciblée git sur {BRANCHE_SUPERPOSITION} — "
            "JAMAIS de reclone ghorg (le pull ghorg cible la branche par défaut)"
        )
        git(["fetch", "origin", "--prune"], cwd=CMDR)
        git(["pull", "--ff-only"], cwd=CMDR)
        # Branche par défaut rafraîchie sans checkout (best effort, master relevé au manifeste).
        git(["fetch", "origin", "master"], cwd=CMDR)
        rapport["action"] = "MISE_À_JOUR_CIBLÉE (git seul, branche overlay)"

    # --- Remote upstream après tout clonage réussi ---
    if (CMDR / ".git").exists():
        code, url_up = git(["remote", "get-url", "upstream"], cwd=CMDR)
        if code != 0:
            git(["remote", "add", "upstream", URL_SOURCE], cwd=CMDR)
            rapport["notes"].append("remote upstream ajouté (cmdr-editor/cmdr)")
        elif url_up.strip() != URL_SOURCE:
            git(["remote", "set-url", "upstream", URL_SOURCE], cwd=CMDR)
            rapport["notes"].append("remote upstream corrigé")
        git(["fetch", "upstream", "--prune"], cwd=CMDR)
        # Raccourci reclone.yaml (D5) — après un clonage réussi uniquement.
        ecrire_entree_reclone(rapport)
        _, sha = git(["rev-parse", "HEAD"], cwd=CMDR)
        maj_etat("D5_clone_cmdr", "terminé", sha.strip())

    print(json.dumps(rapport, ensure_ascii=False, indent=2))
    return 0 if not rapport["erreurs"] else 2


if __name__ == "__main__":
    sys.exit(main())
