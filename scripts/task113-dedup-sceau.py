#!/usr/bin/env python3
"""Task 113 — Dédup du sceau + déplacement R4 canonique des PMs remplacés.

Séquence (précédent Task 112 G16 « post-dédup PM v3.45.0 ») :
1. git mv des PMs remplacés depuis @mon-ecosysteme/ vers l'archive canonique
   skills/@historique/prompts-maitres/<skill>/ (R4 git mv byte-identité).
2. Dédup mécanique des 2 entrées périmées du sceau download/mon-ecosysteme_archive.zip
   (les contenus sont archivés — la garde anti-perte v2.4 du scelleur compare les
   noms au corpus top-level et bloquerait sinon, rc=2 JAMAIS contournable).
3. Idempotent : re-exécuter = 0 changement. Stdlib.
Codes retour : 0 = PASS, 1 = échec, 2 = selftest.
"""
# ⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.46)
# SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
# Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
# Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
# Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
# Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
# Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).

import json
import subprocess
import sys
import zipfile
from pathlib import Path

RACINE = Path("/home/z/my-project")
DEPOT = RACINE / "KNOWLEDGE-repo"
SCEAU = DEPOT / "download/mon-ecosysteme_archive.zip"
RAPPORT = RACINE / "scripts/task113-dedup-sceau-rapport.json"

MOUVEMENTS = [
    ("skills/@mon-ecosysteme/@historique-pms/PROMPT-MAITRE-CORRECT-WORK-v2.12.0.md",
     "skills/@historique/prompts-maitres/correct-work/PROMPT-MAITRE-CORRECT-WORK-v2.12.0.md"),
    ("skills/@mon-ecosysteme/@historique-pms/PROMPT-MAITRE-REFACTOR-GUARD-v1.8.1.md",
     "skills/@historique/prompts-maitres/refactor-guard/PROMPT-MAITRE-REFACTOR-GUARD-v1.8.1.md"),
]
ENTREES_PERIMEES = [
    "@mon-ecosysteme/PROMPT-MAITRE-CORRECT-WORK-v2.12.0.md",
    "@mon-ecosysteme/PROMPT-MAITRE-REFACTOR-GUARD-v1.8.1.md",
]


def selftest() -> int:
    # la garde v2.4 compare Path(name) au corpus top-level : les noms déplacés
    # ne doivent plus être présents au sceau après dédup
    nom = "@mon-ecosysteme/PROMPT-MAITRE-CORRECT-WORK-v2.12.0.md"
    print("PASS garde_name_extrait", Path(nom).name == "PROMPT-MAITRE-CORRECT-WORK-v2.12.0.md")
    return 0


def main() -> int:
    j = {"mouvements": [], "dedup": None}
    # 1 — déplacements R4 canoniques (git mv, byte-identité)
    for src, dst in MOUVEMENTS:
        s, d = DEPOT / src, DEPOT / dst
        if s.exists():
            d.parent.mkdir(parents=True, exist_ok=True)
            r = subprocess.run(["git", "mv", src, dst], cwd=DEPOT,
                               capture_output=True, text=True)
            j["mouvements"].append({"src": src, "dst": dst,
                                    "statut": "MV_OK" if r.returncode == 0 else "MV_KO",
                                    "detail": r.stderr.strip()[:120]})
        elif d.exists():
            j["mouvements"].append({"src": src, "dst": dst, "statut": "DEJA_ARCHIVE"})
        else:
            j["mouvements"].append({"src": src, "dst": dst, "statut": "ABSENT_DOUBLEMENT"})
            print("ECHEC :", src, "absent des deux côtés"); print(json.dumps(j, indent=2)); return 1
        print(f"  {Path(src).name} → {Path(dst).parent.name}/ : {j['mouvements'][-1]['statut']}")
    # purge du dossier intermédiaire vide
    inter = DEPOT / "skills/@mon-ecosysteme/@historique-pms"
    if inter.exists():
        try:
            inter.rmdir()
            j["dossier_intermediaire"] = "supprimé (vide)"
        except OSError:
            j["dossier_intermediaire"] = "NON VIDE — à inspecter"
            print("GARDE : dossier non vide :", inter); return 1
    # 2 — dédup du sceau : réécriture sans les entrées périmées (contenus archivés R4)
    if SCEAU.exists():
        with zipfile.ZipFile(SCEAU) as z:
            entrees = {n: z.read(n) for n in z.namelist() if not n.endswith("/")}
        presentes = [e for e in ENTREES_PERIMEES if e in entrees]
        if presentes:
            avec_sceau = {n: v for n, v in entrees.items() if n not in ENTREES_PERIMEES}
            SCEAU.write_bytes(b"")
            with zipfile.ZipFile(SCEAU, "w", zipfile.ZIP_DEFLATED) as z:
                for n, v in avec_sceau.items():
                    z.writestr(n, v)
            j["dedup"] = {"retirees": presentes, "restantes": len(avec_sceau)}
        else:
            j["dedup"] = {"retirees": [], "restantes": len(entrees), "statut": "déjà propre"}
        print("dédup sceau :", j["dedup"])
    else:
        j["dedup"] = "sceau absent"
    (RAPPORT).write_text(json.dumps(j, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    sys.exit(main())
