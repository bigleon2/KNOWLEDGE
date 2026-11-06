#!/usr/bin/env python3
"""test-karnaugh-f-l-s-b.py — TG4 (Task 51) : simulation mécanique des 16 états du Karnaugh F/L/S/B.

Test de la logique d'état de cmdr-clone.py SANS aucune action distante : les primitives
(depot_existant, git, porcelain_vide, branche_courante) sont remplacées par des doubles
de contrôle, les 4 variables sont imposées case par case, et l'action choisie est
confrontée à l'action attendue par la table du PM ghorg-to-ecosysteme.md v1.1 §7.

Lignes F L × colonnes S B (ordre de Gray 00 01 11 10) — X = cas impossible (S et B
n'ont pas de sens quand L = 0 : le script ne les teste alors pas).
"""

import importlib.util
import io
import json
import sys
import tempfile
from contextlib import redirect_stdout
from pathlib import Path

ICI = Path(__file__).parent
sys.path.insert(0, str(ICI))

# Le script cible est en kebab-case (convention dépôt) : chargement par chemin.
_spec = importlib.util.spec_from_file_location("cmdr_clone", ICI / "cmdr-clone.py")
cmdr_clone = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cmdr_clone)

ATTENDUS = {
    # (F, L, S, B) : (contenu attendu dans "action", code retour attendu)
    # L = 0 → S/B non testés (X) : règle 1 (F=0, repli source) ou règle 2 (F=1, clone fork).
    (0, 0, 0, 0): ("CLONER", 0), (0, 0, 0, 1): ("CLONER", 0),
    (0, 0, 1, 1): ("CLONER", 0), (0, 0, 1, 0): ("CLONER", 0),
    (1, 0, 0, 0): ("CLONER", 0), (1, 0, 0, 1): ("CLONER", 0),
    (1, 0, 1, 1): ("CLONER", 0), (1, 0, 1, 0): ("CLONER", 0),
    # F = 0, L = 1 : orphelin (P0) si origin ≠ source ; repli documenté si origin = source.
    (0, 1, 0, 0): ("MISE_À_JOUR_CIBLÉE", 0),   # origin = source, propre
    (0, 1, 0, 1): ("MISE_À_JOUR_CIBLÉE", 0),   # origin = source, propre, branche overlay
    (0, 1, 1, 1): ("NE_RIEN_MODIFIER", 0),     # origin = source, sale
    (0, 1, 1, 0): ("NE_RIEN_MODIFIER", 0),     # origin = source, sale
    # F = 1, L = 1.
    (1, 1, 1, 0): ("NE_RIEN_MODIFIER", 0),     # règle 4 : sale, quelle que soit B
    (1, 1, 1, 1): ("NE_RIEN_MODIFIER", 0),
    (1, 1, 0, 0): ("MISE_À_JOUR_CIBLÉE", 0),   # règle 5 : ghorg non utilisable (pas de jeton) → repli git
    (1, 1, 0, 1): ("MISE_À_JOUR_CIBLÉE", 0),   # règle 6 : git seul, jamais reclone
}


def simuler(f, l, s, b, origin_source=True):
    """Exécute cmdr_clone.main() avec les 4 variables imposées, renvoie (action, code, rapport)."""
    etiquettes = {"actions_git": []}

    def faux_depot_existant(url):
        return f if "bigleon2/cmdr" in url else True

    def faux_git(args, cwd=None, timeout=300):
        etiquettes["actions_git"].append(args[0])
        if args[:3] == ["remote", "get-url", "origin"]:
            return 0, "https://github.com/cmdr-editor/cmdr.git" if origin_source else "https://exemple/autre.git"
        if args[:2] == ["rev-parse", "HEAD"]:
            return 0, "abc123def456"
        if args[:2] == ["branch", "--list"]:
            return 0, "ecosystem/tsi-traktor-s4mk2" if b else ""
        return 0, "Already up to date"

    def faux_porcelain(cwd):
        return not s

    def faux_branche(cwd):
        return "ecosystem/tsi-traktor-s4mk2" if b else "master"

    def faux_maj_etat(cle, valeur, sha=None):
        pass

    # Basculement des primitives sur les doubles de contrôle.
    cmdr_clone.depot_existant = faux_depot_existant
    cmdr_clone.git = faux_git
    cmdr_clone.porcelain_vide = faux_porcelain
    cmdr_clone.branche_courante = faux_branche
    cmdr_clone.maj_etat = faux_maj_etat
    cmdr_clone.ecrire_entree_reclone = lambda rapport: None

    with tempfile.TemporaryDirectory() as tmp:
        cmdr_clone.CMDR = Path(tmp) / "cmdr"
        if l:
            (cmdr_clone.CMDR / ".git").mkdir(parents=True)  # présence simulée
        tampon = io.StringIO()
        with redirect_stdout(tampon):
            code = cmdr_clone.main()
    try:
        rapport = json.loads(tampon.getvalue())
    except json.JSONDecodeError:
        rapport = {"action": "<illisible>", "sortie": tampon.getvalue()[-200:]}
    return rapport.get("action", ""), code, rapport, etiquettes["actions_git"]


def main():
    resultats, echecs = [], []
    for (f, l, s, b), (attendu, code_attendu) in sorted(ATTENDUS.items()):
        # Les cas F=0 L=1 sont testés avec origin = source (repli) — le variant orphelin
        # (origin ≠ source) est testé séparément ci-dessous.
        action, code, rapport, _ = simuler(f, l, s, b, origin_source=True)
        ok = attendu in action and code == code_attendu
        resultats.append(ok)
        if not ok:
            echecs.append((f, l, s, b, attendu, action, code, code_attendu))

    # Variants complémentaires : clone orphelin (F=0, L=1, origin ≠ source) → STOP P0 (exit 3).
    for s, b in ((0, 0), (0, 1), (1, 0), (1, 1)):
        action, code, _, _ = simuler(0, 1, s, b, origin_source=False)
        ok = "STOP" in action and code == 3
        resultats.append(ok)
        if not ok:
            echecs.append((0, 1, s, b, "STOP", action, code, 3))

    # Règle 6 : JAMAIS de reclone ghorg — vérifié structurellement (ghorg_utilisable()
    # exige un jeton ; sans jeton, aucune commande ghorg n'est émise — le repli est git seul).
    print(f"TG4 — Karnaugh F/L/S/B : {sum(resultats)}/{len(resultats)} états conformes")
    for ligne in echecs:
        print(f"  ÉCHEC : F{ligne[0]} L{ligne[1]} S{ligne[2]} B{ligne[3]} — attendu {ligne[4]!r}, obtenu {ligne[5]!r} (exit {ligne[6]} ≠ {ligne[7]})")
    return 0 if not echecs else 1


if __name__ == "__main__":
    sys.exit(main())
