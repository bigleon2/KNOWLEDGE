#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.22)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

"""task40-perf-comparatif.py — Tests $FACON $FACON2 de performances comparatifs (Task 40, D004).

Compare les éléments de traitement TSI des deux côtés :
- CÔTÉ DÉPÔT GitHub (clone fddbe94, poussé) : arbitre tsi-validator v1.2.0
  (valider-tsi.py, bi-racine) + pipeline analyse-doc-s4mk2 v1.2.0 (analyser-zip-mk2.py).
- CÔTÉ DISCUSSION/Task 39 (toolkit local, non poussé) : tsi_toolkit v1.0.0 —
  nixml (réel DIOM), validateur interne, generateur, presets, studio, convertisseurs.

Méthode $FACON2 : 3 exécutions par cible, médiane rapportée, seuils du CDC
(10 s arbitre / 5 s unitaire), verdict mécanique PASS/FAIL, JSON persisté.
Stdlib uniquement. Lecture seule.
"""
import json
import statistics
import subprocess
import sys
import time

PY = sys.executable
RACINE = "/home/z/my-project"
DREW_TSI = f"{RACINE}/work/drew-fixtures/Drew's S4 User Controller Maping.tsi"
DJTT_ZIP = f"{RACINE}/upload/DJTT Kontrol S4 MK2 Custom Mapping v2.1.0.zip"
DREW_ZIP = f"{RACINE}/upload/Kontrol S4  [DREW's MAPPING].zip"
VALIDEUR_DEPOT = f"{RACINE}/skills/tsi-validator/scripts/valider-tsi.py"
PIPELINE_DEPOT = f"{RACINE}/skills/analyse-doc-s4mk2/scripts/analyser-zip-mk2.py"
TOOLKIT = f"{RACINE}/work/KNOWLEDGE-main/tsi-toolkit"

CIBLES = [
    # (famille, nom, cmd, seuil_s, rc_attendu) — tsi-validator v1.2.0 bi-racine :
    # PASS [réel NIXML] rc=0 attendu (Task 34) ; analyse-doc ZIP DREW rc=1 = verdict
    # FAIL mécaniquement correct pour un mapping tiers hors référence (§6.7 SKILL.md)
    ("depot", "tsi-validator v1.2.0 bi-racine — TSI DREW réel (623 Ko, NIXML)",
     [PY, VALIDEUR_DEPOT, DREW_TSI], 10.0, 0),
    ("depot", "analyse-doc-s4mk2 pipeline — ZIP DJTT référence (1,8 Mo)",
     [PY, PIPELINE_DEPOT, DJTT_ZIP, "--json", "/tmp/p40-djtt.json"], 10.0, 0),
    ("depot", "analyse-doc-s4mk2 pipeline — ZIP DREW (1,3 Mo)",
     [PY, PIPELINE_DEPOT, DREW_ZIP, "--json", "/tmp/p40-drew.json"], 10.0, 1),
    ("toolkit", "tsi_toolkit nixml — TSI DREW réel (pont DIOM)",
     [PY, "-m", "tsi_toolkit.nixml", DREW_TSI], 5.0, 0),
    ("toolkit", "tsi_toolkit convertisseurs — TSI DREW → JSON",
     [PY, "-m", "tsi_toolkit.convertisseurs", DREW_TSI, "--json", "/tmp/p40-conv.json"], 5.0, 0),
    ("toolkit", "tsi_toolkit studio — scénario DSL complet (génère + audit)",
     [PY, "-m", "tsi_toolkit.studio", "/tmp/p40-scenario.tsi"], 5.0, 0),
]


def mesurer(cmd, seuil, rc_attendu, n=3):
    durees, rcs = [], []
    for _ in range(n):
        t0 = time.monotonic()
        p = subprocess.run(cmd, capture_output=True, text=True, cwd=TOOLKIT if "tsi_toolkit" in str(cmd) else None, timeout=120)
        durees.append(time.monotonic() - t0)
        rcs.append(p.returncode)
    med = statistics.median(durees)
    return {
        "medianes_s": round(med, 4), "runs_s": [round(d, 4) for d in durees],
        "rc": rcs, "rc_stable": len(set(rcs)) == 1, "rc0": rc_attendu in rcs,
        "rc_attendu": rc_attendu,
        "seuil_s": seuil, "verdict": "PASS" if med <= seuil else "FAIL",
    }


def main():
    rapport = {"task": "Task 40 — tests $FACON $FACON2 de performances comparatifs (D004)",
               "methode": "3 runs par cible, médiane, seuils CDC 10 s (arbitre) / 5 s (unitaire)",
               "cibles": []}
    print(rapport["task"])
    tout_pass = True
    for famille, nom, cmd, seuil, rc_attendu in CIBLES:
        r = mesurer(cmd, seuil, rc_attendu)
        r = {"famille": famille, "nom": nom, **r}
        rapport["cibles"].append(r)
        tout_pass = tout_pass and r["verdict"] == "PASS" and r["rc0"]
        print(f"  [{r['verdict']}] {famille:8} {nom[:66]:66} médiane {r['medianes_s']:.3f} s (rc {r['rc']})")
    rapport["verdict"] = "PASS" if tout_pass else "FAIL"
    print(f"VERDICT : {rapport['verdict']}")
    with open(f"{RACINE}/work/task40-perf-comparatif.json", "w", encoding="utf-8") as f:
        json.dump(rapport, f, ensure_ascii=False, indent=2)
    return 0 if tout_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
