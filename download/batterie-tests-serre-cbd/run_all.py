#!/usr/bin/env python3
"""run_all.py — harnais d'exécution de la batterie batterie-tests-serre-cbd.

Généré par scaffold_tests.py v2.0.0 (skill cahier-des-charges). stdlib uniquement.

Protocole STATUT (en-tête de chaque test) :
  - STATUT = "NON_IMPLÉMENTÉ" -> test NON exécuté (squelette : un squelette ne prouve rien, R3) ;
  - STATUT = "PRÊT" ou absent (patron references/simulation-materielle.md) -> exécution en
    sous-processus, verdict = code retour (0 = PASS, sinon ECHEC).

Verdict global : PASS si >= 1 test et tous PASS ; ECHEC si >= 1 ECHEC ; NON_IMPLÉMENTÉ si des
squelettes restent à adapter ; AUCUN_TEST si la batterie est vide.
Code sortie : 0 tout PASS ; 1 au moins un ECHEC ; 2 au moins un NON_IMPLÉMENTÉ (sans ECHEC) ;
3 aucun test.
"""
import json
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

RACINE = Path(__file__).resolve().parent
PROJET = "serre-cbd"
TIMEOUT_S = 300
RE_STATUT = re.compile(r'^STATUT\s*=\s*"([^"]+)"', re.M)
RE_ID = re.compile(r"^(tf|th)_(\d+)", re.I)
JOURNAL = RACINE / "journal" / "synthese.json"


def statut_du_test(chemin):
    m = RE_STATUT.search(chemin.read_text(encoding="utf-8"))
    return m.group(1) if m else "PRÊT"


def id_du_test(chemin):
    m = RE_ID.match(chemin.stem)
    if m:
        return f"{m.group(1).upper()}-{int(m.group(2)):02d}"
    return chemin.stem.upper()


def decouvrir():
    tests = []
    for sous_dossier, motif in (("tests_fonctionnels", "tf_*.py"), ("tests_materiel", "th_*.py")):
        dossier = RACINE / sous_dossier
        if dossier.is_dir():
            tests.extend(sorted(dossier.glob(motif)))
    return tests


def main():
    resultats = []
    for chemin in decouvrir():
        statut = statut_du_test(chemin)
        if statut == "NON_IMPLÉMENTÉ":
            resultats.append({"id": id_du_test(chemin), "test": chemin.name, "statut": statut,
                              "verdict": "NON_IMPLÉMENTÉ", "code_retour": None, "duree_s": 0.0,
                              "sortie": "squelette non exécuté — à adapter puis STATUT=PRÊT"})
            continue
        debut = time.monotonic()
        try:
            proc = subprocess.run([sys.executable, str(chemin)], capture_output=True,
                                  text=True, timeout=TIMEOUT_S, cwd=str(RACINE))
            code = proc.returncode
            sortie = ((proc.stdout or "") + (proc.stderr or "")).strip()
        except subprocess.TimeoutExpired:
            code, sortie = 1, f"ECHEC — TIMEOUT > {TIMEOUT_S} s"
        resultats.append({"id": id_du_test(chemin), "test": chemin.name, "statut": statut,
                          "verdict": "PASS" if code == 0 else "ECHEC", "code_retour": code,
                          "duree_s": round(time.monotonic() - debut, 3), "sortie": sortie[-2000:]})
    verdicts = [r["verdict"] for r in resultats]
    if not resultats:
        verdict_global, code_sortie = "AUCUN_TEST", 3
    elif "ECHEC" in verdicts:
        verdict_global, code_sortie = "ECHEC", 1
    elif "NON_IMPLÉMENTÉ" in verdicts:
        verdict_global, code_sortie = "NON_IMPLÉMENTÉ", 2
    else:
        verdict_global, code_sortie = "PASS", 0
    synthese = {
        "projet": PROJET,
        "horodatage": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "verdict_global": verdict_global,
        "total": len(resultats),
        "passes": verdicts.count("PASS"),
        "echecs": verdicts.count("ECHEC"),
        "non_implementes": verdicts.count("NON_IMPLÉMENTÉ"),
        "tests": resultats,
    }
    JOURNAL.parent.mkdir(parents=True, exist_ok=True)
    JOURNAL.write_text(json.dumps(synthese, indent=2, ensure_ascii=False), encoding="utf-8")
    for r in resultats:
        derniere = r["sortie"].splitlines()[-1] if r["sortie"] else ""
        print(f"{r['verdict']:<16} {r['id']} ({r['test']}) {derniere}")
    print(f"VERDICT GLOBAL : {verdict_global} — {synthese['passes']} PASS / "
          f"{synthese['echecs']} ECHEC / {synthese['non_implementes']} NON_IMPLÉMENTÉ "
          f"(journal : journal/synthese.json)")
    raise SystemExit(code_sortie)


if __name__ == "__main__":
    main()
