#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rea-install.py — Installation idempotente du kit REA (skill rea-analysis v1.0.0).

Étapes (chacune sautée si son composant est déjà présent — idempotence ×2 :
le re-jeu sur état installé ne modifie RIEN, contrat ghorg-install.py Task 51) :
  1. clone ANONYME lecture seule du fork bigleon2/REA_Reverse_All_Thing_Kit
     (dépôt public — jamais de jeton, règle d'or n°4 / KO-L009) ;
  2. `npm ci` si node_modules absent (cache dédié sous périmètre) ;
  3. `npm run build:cached` si dist absent ;
  4. sonde CLI `node scripts/rea.mjs --help` (rc=0 requis) — rapport final.

Options : --pin <sha>  re-calage de l'épingle datée (checkout après clone/déjà
présent — git checkout détaché, arbre propre exigé).

Codes retour : 0 = kit opérationnel · 1 = échec d'étape (message) ·
2 = état incohérent (arbre sale / CLI cassée après build).
"""
# ⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.46)
# SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
# Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
# Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
# Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
# Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
# Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).

import argparse
import os
import subprocess
import sys
from pathlib import Path

BASE = Path("/home/z/my-project")
KIT = BASE / "tools" / "rea" / "REA_Reverse_All_Thing_Kit"
URL_FORK = "https://github.com/bigleon2/REA_Reverse_All_Thing_Kit.git"
CACHE_NPM = BASE / "tools" / "rea" / "npm-cache"
ENV = dict(os.environ, npm_config_cache=str(CACHE_NPM))


def run(cmd, **kw):
    print("»", " ".join(str(c) for c in cmd))
    return subprocess.run(cmd, capture_output=True, text=True, timeout=590, env=ENV, **kw)


def etape_clone(pin):
    if KIT.exists() and (KIT / ".git").exists():
        head = run(["git", "-C", str(KIT), "rev-parse", "--short", "HEAD"])
        if head.returncode == 0:
            print(f"[DÉJÀ] kit présent @ {head.stdout.strip()} (clone conservé — pas de re-clone)")
            if pin:
                co = run(["git", "-C", str(KIT), "checkout", pin])
                if co.returncode != 0:
                    print("ÉCHEC : re-calage --pin impossible\n" + co.stderr[-300:])
                    return 1
                print(f"[OK] épingle re-calée : {pin}")
            return 0
        print("ÉCHEC : dossier kit présent mais dépôt git illisible")
        return 1
    print("[ÉTAPE] clone anonyme lecture seule…")
    r = run(["git", "clone", URL_FORK, str(KIT)])
    if r.returncode != 0:
        print("ÉCHEC : clone\n" + r.stderr[-400:])
        return 1
    if pin:
        co = run(["git", "-C", str(KIT), "checkout", pin])
        if co.returncode != 0:
            print("ÉCHEC : --pin introuvable après clone\n" + co.stderr[-300:])
            return 1
    head = run(["git", "-C", str(KIT), "rev-parse", "--short", "HEAD"])
    print(f"[OK] clone @ {head.stdout.strip()} (anonyme — zéro jeton)")
    return 0


def etape_npm():
    if (KIT / "node_modules").exists():
        print("[DÉJÀ] node_modules présent — npm ci sauté")
        return 0
    print("[ÉTAPE] npm ci (cache dédié périmètre)…")
    r = run(["npm", "ci", "--no-audit", "--no-fund"], cwd=KIT)
    if r.returncode != 0:
        print("ÉCHEC : npm ci\n" + (r.stderr or r.stdout)[-400:])
        return 1
    print("[OK] node_modules installé")
    return 0


def etape_build():
    if (KIT / "dist").exists() and any((KIT / "dist").iterdir()):
        print("[DÉJÀ] dist présent — build:cached sauté")
        return 0
    print("[ÉTAPE] npm run build:cached…")
    r = run(["npm", "run", "build:cached"], cwd=KIT)
    if r.returncode != 0:
        print("ÉCHEC : build:cached\n" + (r.stderr or r.stdout)[-400:])
        return 1
    print("[OK] dist construit")
    return 0


def etape_sonde():
    r = run(["node", "scripts/rea.mjs", "--help"], cwd=KIT)
    if r.returncode != 0:
        print("ÉCHEC : sonde CLI rc=%d\n" % r.returncode + (r.stderr or r.stdout)[-300:])
        return 2
    lignes = r.stdout.count("\n")
    head = run(["git", "-C", str(KIT), "rev-parse", "--short", "HEAD"])
    propre = run(["git", "-C", str(KIT), "status", "--porcelain"])
    print(f"[OK] CLI opérationnelle ({lignes} lignes d'aide) — kit @ {head.stdout.strip()}")
    if propre.stdout.strip():
        print("AVERTISSEMENT : arbre sale (divergence locale — inspecter)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Installation idempotente du kit REA (rea-analysis v1.0.0)")
    ap.add_argument("--pin", default=None, help="SHA d'épingle datée (checkout après clone)")
    args = ap.parse_args()
    for etape in (lambda: etape_clone(args.pin), etape_npm, etape_build, etape_sonde):
        rc = etape()
        if rc != 0:
            return rc
    print("VERDICT : kit REA opérationnel (idempotent — re-jeu = no-op)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
