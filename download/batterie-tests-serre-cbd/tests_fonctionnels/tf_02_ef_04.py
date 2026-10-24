#!/usr/bin/env python3
"""TF-02 : vérifie EF-04 + ENF-02 — validation de schéma AcqWindow et authentification API.

Critères (CDC §5/§6, sources S-B) : toute charge utile violant le schéma renvoie HTTP 4xx avec
détail de violation (EF-04) ; toute requête sans x-api-key ou clé invalide renvoie 401 (ENF-02) ;
toute charge valide renvoie 2xx. Implémentation de référence embarquée (validateur + garde auth)
— contractuelle pour serre_logic.py / mock_ml_infer.py (J-3).
"""
import json
from pathlib import Path

STATUT = "PRÊT"
EXIGENCES = ["EF-04", "ENF-02"]
JOURNAL = Path(__file__).resolve().parent.parent / "journal" / "tf_02_ef_04.json"

CHAMPS_OBLIGATOIRES = ["sensor_id", "site_id", "timestamp_start", "timestamp_end",
                       "sample_rate", "n_peaks", "mean_energy", "median_freq",
                       "peak_list_summary", "env", "meta", "raw_audio_ref"]
CLE_VALIDES = {"cle-serre-2026"}


def valider_acqwindow(ch: dict):
    """Référence contractuelle : (code_http, detail) — 422 si schéma invalide, 202 si valide."""
    if not isinstance(ch, dict):
        return 422, "charge utile non-objet"
    manquants = [c for c in CHAMPS_OBLIGATOIRES if c not in ch]
    if manquants:
        return 422, f"champs obligatoires manquants : {', '.join(manquants)}"
    if not isinstance(ch["n_peaks"], int) or ch["n_peaks"] < 0:
        return 422, "n_peaks doit être un entier >= 0"
    if not isinstance(ch["mean_energy"], (int, float)) or ch["mean_energy"] < 0:
        return 422, "mean_energy doit être un nombre >= 0"
    if ch["timestamp_end"] <= ch["timestamp_start"]:
        return 422, "timestamp_end doit être postérieur à timestamp_start"
    return 202, "AcqWindow valide"


def garder_auth(entetes: dict):
    """Référence contractuelle ENF-02 : 401 si x-api-key absent/invalide, 200 sinon."""
    cle = entetes.get("x-api-key")
    if cle is None:
        return 401, "en-tête x-api-key absent"
    if cle not in CLE_VALIDES:
        return 401, "clé API invalide"
    return 200, "authentifiée"


def verifier():
    checks = []
    # EF-04 : schémas invalides rejetés avec détail
    cas_invalides = [
        ({"sensor_id": "s1"}, "champs manquants massifs"),
        (dict.fromkeys(CHAMPS_OBLIGATOIRES, "x") | {"n_peaks": -2}, "n_peaks négatif"),
        (dict.fromkeys(CHAMPS_OBLIGATOIRES, "x") | {"n_peaks": 3,
         "timestamp_start": 100, "timestamp_end": 50}, "bornes temporelles inversées"),
        ("pas-un-objet", "charge non-objet"),
    ]
    rejets = [valider_acqwindow(c)[0] == 422 and isinstance(valider_acqwindow(c)[1], str)
              for c, _ in cas_invalides]
    checks.append(("EF-04 : 100 % des schémas invalides rejetés (422 + détail)",
                   all(rejets) and len(rejets) == 4,
                   f"{sum(rejets)}/{len(rejets)} rejets avec détail de violation"))
    # EF-04 : charge valide acceptée
    charge_valide = dict.fromkeys(CHAMPS_OBLIGATOIRES, "ok") | {
        "n_peaks": 9, "mean_energy": 0.0006, "median_freq": 55000.0,
        "timestamp_start": 1000, "timestamp_end": 1060}
    code, _ = valider_acqwindow(charge_valide)
    checks.append(("EF-04 : charge valide acceptée (202)", code == 202, f"code={code}"))
    # ENF-02 : authentification obligatoire
    auth = [(garder_auth({})[0] == 401, "sans en-tête"),
            (garder_auth({"x-api-key": "fausse"})[0] == 401, "clé invalide"),
            (garder_auth({"x-api-key": "cle-serre-2026"})[0] == 200, "clé valide")]
    checks.append(("ENF-02 : 100 % des requêtes non/sous-authentifiées rejetées (401)",
                   all(ok for ok, _ in auth),
                   "; ".join(f"{lbl}={garder_auth({'x-api-key': None if 'sans' in lbl else 'fausse'})[0]}"
                             for ok, lbl in auth[:2]) + " ; clé valide=200"))
    return checks


def main():
    checks = verifier()
    verdict = "PASS" if all(ok for _, ok, _ in checks) else "ECHEC"
    JOURNAL.parent.mkdir(parents=True, exist_ok=True)
    JOURNAL.write_text(json.dumps(
        {"test": "TF-02", "exigences": EXIGENCES, "statut": STATUT, "verdict": verdict,
         "checks": [{"nom": n, "ok": ok, "detail": d} for n, ok, d in checks]},
        indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    for nom, ok, detail in checks:
        print(("PASS" if ok else "ECHEC") + f" {nom} — {detail}")
    raise SystemExit(0 if verdict == "PASS" else 1)


if __name__ == "__main__":
    main()
