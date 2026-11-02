#!/usr/bin/env python3
"""CLI tsi-toolkit — inspect / generate / validate / convert / coverage /
presets / studio.

Usage : python3 -m tsi_toolkit <commande> [options]
Aide intégrale : python3 -m tsi_toolkit --help (français).
"""
from __future__ import annotations

import argparse
import json
import os
import sys

from . import __version__
from . import convertisseurs
from . import couverture
from . import generateur
from . import nixml
from . import studio as studio_mod
from . import validateur


def _cmd_inspect(args):
    if not os.path.isfile(args.tsi):
        print(f"❌ Fichier introuvable : {args.tsi}", file=sys.stderr)
        return 2
    resultat = nixml.inspecter(args.tsi, pont=True)
    print(json.dumps(resultat, ensure_ascii=False, indent=1))
    return 0 if resultat["format"]["famille"] != "INCONNU" else 2


def _cmd_generate(args):
    sortie = generateur.generer(args.preset, args.sortie,
                                verifier_conflits=not args.force)
    print(f"✅ Généré : {sortie} "
          f"({os.path.getsize(sortie)} octets — anti-conflits "
          f"{'désactivé (--force)' if args.force else 'actif'})")
    return 0


def _cmd_validate(args):
    resultat = validateur.valider(args.tsi, pont=not args.sans_pont)
    print(json.dumps(resultat, ensure_ascii=False, indent=1))
    return 0 if resultat.get("verdict") == "PASS" else 1


def _cmd_convert(args):
    if args.sens == "tsi-json":
        sortie = convertisseurs.tsi_vers_json(args.entree, args.sortie)
    elif args.sens == "json-tsi":
        sortie = convertisseurs.json_vers_tsi(args.entree, args.sortie)
    else:  # csv-tsi
        sortie = convertisseurs.csv_vers_tsi(args.entree, args.sortie)
    print(f"✅ Converti ({args.sens}) : {sortie}")
    return 0


def _cmd_coverage(args):
    modele = nixml.lire_canonique(args.tsi)
    audit = couverture.auditer(modele["mappings"])
    print(json.dumps(audit, ensure_ascii=False, indent=1))
    return 0 if audit["verdict"] == "PASS" else 1


def _cmd_presets(args):
    racine = os.path.join(os.path.dirname(__file__), "..", "examples")
    if args.lister:
        print("Presets d'exemple :")
        for f in sorted(os.listdir(racine)):
            if f.endswith(".json"):
                p = json.load(open(os.path.join(racine, f), encoding="utf-8"))
                print(f"  - {f} : {p.get('meta', {}).get('nom', '?')} "
                      f"({len(p.get('mappings', []))} mappings)")
    return 0


def _cmd_studio(args):
    repertoire = os.path.dirname(args.sortie) or "."
    os.makedirs(repertoire, exist_ok=True)
    journal = os.path.join(repertoire, "audit_log.md")
    resultat = studio_mod.scenario_demo(args.sortie, journal)
    print(f"✅ Studio : {resultat['mappings']} mappings → {resultat['tsi']} ; "
          f"audit → {resultat['audit_log']} "
          f"(conflits : {len(resultat['conflits'])})")
    return 0


def construire_parseur() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="tsi_toolkit",
        description="Toolchain TSI Traktor Pro 3.11 / Kontrol S4 MK2 "
                    f"(v{__version__}) — convergence $facon des outils "
                    "des discussions QWEN avec la famille TSI écosystème.")
    sub = p.add_subparsers(dest="commande", required=True)

    sp = sub.add_parser("inspect", help="Inspection multi-format d'un .tsi "
                        "(canonique, réel DIOM, réglages)")
    sp.add_argument("tsi")
    sp.set_params = None
    sp.set_defaults(func=_cmd_inspect)

    sp = sub.add_parser("generate", help="Génère un .tsi depuis un preset JSON")
    sp.add_argument("preset")
    sp.add_argument("sortie")
    sp.add_argument("--force", action="store_true",
                    help="désactive le contrôle anti-conflits (déconseillé)")
    sp.set_defaults(func=_cmd_generate)

    sp = sub.add_parser("validate", help="Valide un .tsi (interne + pont "
                        "arbitre tsi-validator)")
    sp.add_argument("tsi")
    sp.add_argument("--sans-pont", action="store_true",
                    help="validation interne autonome uniquement")
    sp.set_defaults(func=_cmd_validate)

    sp = sub.add_parser("convert", help="Convertisseurs TSI/JSON/CSV")
    sp.add_argument("sens", choices=["tsi-json", "json-tsi", "csv-tsi"])
    sp.add_argument("entree")
    sp.add_argument("sortie")
    sp.set_defaults(func=_cmd_convert)

    sp = sub.add_parser("coverage", help="Matrice de couverture multi-couches "
                        "(aucune couche morte)")
    sp.add_argument("tsi")
    sp.set_defaults(func=_cmd_coverage)

    sp = sub.add_parser("presets", help="Liste les presets d'exemple")
    sp.add_argument("--lister", action="store_true", default=True)
    sp.set_defaults(func=_cmd_presets)

    sp = sub.add_parser("studio", help="Scénario studio : DSL → TSI + "
                        "audit_log.md auto-évolutif")
    sp.add_argument("sortie")
    sp.set_defaults(func=_cmd_studio)
    return p


def main(argv=None):
    parseur = construire_parseur()
    args = parseur.parse_args(argv)
    try:
        return args.func(args)
    except FileNotFoundError as exc:
        print(f"❌ Fichier introuvable : {exc.filename or exc}", file=sys.stderr)
        return 2
    except (ValueError, OSError) as exc:
        print(f"❌ {exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # noqa: BLE001 — rejet contrôlé, pas de traceback
        print(f"❌ Entrée rejetée : {exc!r}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
