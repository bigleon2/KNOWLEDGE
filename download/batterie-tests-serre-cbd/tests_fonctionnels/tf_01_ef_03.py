#!/usr/bin/env python3
"""TF-01 : vérifie EF-03 — inférence à seuils explicites (healthy / stress_light / stress_severe).

Critère d'acceptation (CDC §5, EF-03, source S-B) : pour tout couple (n_peaks, mean_energy) bornier :
n_peaks >= 20 OU mean_energy > 0,001 -> stress_severe ; n_peaks >= 8 OU mean_energy > 0,0005 ->
stress_light ; sinon -> healthy. 100 % des cas borniers conformes.

Implémentation de référence embarquée (contrat d'implémentation J-3) : la fonction inferer()
reproduit exactement la règle contractuelle ; serre_logic.py réel devra passer le même test.
Déterministe, stdlib uniquement.
"""
import json
from pathlib import Path

STATUT = "PRÊT"
EXIGENCES = ["EF-03"]
JOURNAL = Path(__file__).resolve().parent.parent / "journal" / "tf_01_ef_03.json"

SEUIL_LIGHT_PICS = 8        # n_peaks >= 8
SEUIL_LIGHT_ENERGIE = 0.0005  # mean_energy > 0,0005 (strict)
SEUIL_SEVERE_PICS = 20      # n_peaks >= 20
SEUIL_SEVERE_ENERGIE = 0.001  # mean_energy > 0,001 (strict)


def inferer(n_peaks: int, mean_energy: float) -> str:
    """Référence contractuelle EF-03 (S-B mock_ml_infer / CDC §5)."""
    if n_peaks >= SEUIL_SEVERE_PICS or mean_energy > SEUIL_SEVERE_ENERGIE:
        return "stress_severe"
    if n_peaks >= SEUIL_LIGHT_PICS or mean_energy > SEUIL_LIGHT_ENERGIE:
        return "stress_light"
    return "healthy"


# Cas borniers : (n_peaks, mean_energy, attendu) — chaque frontière de l'inégalité contractuelle
CAS_BORNIERS = [
    (20, 0.0, "stress_severe"),       # n_peaks = 20 exactement -> severe (>= 20)
    (19, 0.0, "stress_light"),        # 19 < 20, énergie nulle -> light (>= 8)
    (8, 0.0, "stress_light"),         # n_peaks = 8 exactement -> light (>= 8)
    (7, 0.0, "healthy"),              # 7 < 8, énergie nulle -> healthy
    (0, 0.001, "stress_light"),      # énergie = 0,001 : PAS > 0,001 (strict) -> mais > 0,0005 -> light
    (0, 0.0011, "stress_severe"),     # énergie > 0,001 -> severe
    (0, 0.0005, "healthy"),           # énergie = 0,0005 : PAS > 0,0005 (strict) -> healthy
    (0, 0.00051, "stress_light"),     # énergie > 0,0005 -> light
    (25, 0.002, "stress_severe"),     # les deux seuils -> severe prioritaire
    (30, 0.0, "stress_severe"),       # pics seuls suffisent
]


def verifier():
    checks = []
    mauvais = [(n, e, attendu, inferer(n, e)) for n, e, attendu in CAS_BORNIERS
               if inferer(n, e) != attendu]
    checks.append(("EF-03 : cas borniers des seuils pics/énergie",
                   not mauvais,
                   f"{len(CAS_BORNIERS) - len(mauvais)}/{len(CAS_BORNIERS)} conformes"
                   + (f" — écarts: {mauvais}" if mauvais else "")))
    # le sens strict des inégalités énergie est explicitement vérifié
    checks.append(("EF-03 : strictitude des inégalités d'énergie (> seuil, pas >=)",
                   inferer(0, SEUIL_LIGHT_ENERGIE) == "healthy"
                   and inferer(0, SEUIL_SEVERE_ENERGIE) != "stress_severe",
                   "énergie = seuil exact -> 0,0005 : healthy ; 0,001 : light (severe non déclenché)"))
    # sévérité prioritaire : toute combinaison qui déclenche les deux -> severe
    checks.append(("EF-03 : priorité severe sur light",
                   all(inferer(n, e) == "stress_severe"
                       for n, e in [(20, 0.002), (25, 0.0), (0, 0.002), (40, 0.5)]),
                   "toutes les combinaisons au-delà des deux seuils -> stress_severe"))
    return checks


def main():
    checks = verifier()
    verdict = "PASS" if all(ok for _, ok, _ in checks) else "ECHEC"
    JOURNAL.parent.mkdir(parents=True, exist_ok=True)
    JOURNAL.write_text(json.dumps(
        {"test": "TF-01", "exigences": EXIGENCES, "statut": STATUT, "verdict": verdict,
         "checks": [{"nom": n, "ok": ok, "detail": d} for n, ok, d in checks]},
        indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    for nom, ok, detail in checks:
        print(("PASS" if ok else "ECHEC") + f" {nom} — {detail}")
    raise SystemExit(0 if verdict == "PASS" else 1)


if __name__ == "__main__":
    main()
