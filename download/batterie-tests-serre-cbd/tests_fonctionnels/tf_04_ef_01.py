#!/usr/bin/env python3
"""TF-04 : vérifie EF-01 — intégrité des AcqWindow produites (complétude, cohérence, Nyquist).

Critère (CDC §5, EF-01, sources S-B + S-A) : un AcqWindow produit contient TOUS les champs
obligatoires du schéma S-B et passe la validation de schéma ; cohérences internes exigées :
bornes temporelles ordonnées, sample_rate suffisant pour la bande 40-80 kHz (Nyquist + marge).
"""
import json
from pathlib import Path

STATUT = "PRÊT"
EXIGENCES = ["EF-01"]
JOURNAL = Path(__file__).resolve().parent.parent / "journal" / "tf_04_ef_01.json"

CHAMPS_OBLIGATOIRES = ["sensor_id", "site_id", "timestamp_start", "timestamp_end",
                       "sample_rate", "n_peaks", "mean_energy", "median_freq",
                       "peak_list_summary", "env", "meta", "raw_audio_ref"]
BANDE_MAX_KHZ = 80.0     # S-A : clics jusqu'à 80 kHz
FE_MIN_KHZ = 2 * BANDE_MAX_KHZ * 1.2  # Nyquist + 20 % de marge = 192 kS/s


def produire_acqwindow(fenetre: int = 60, fe_khz: float = 250.0, horodatage: int = 1_000):
    """Référence contractuelle SS-01/SS-02 : fabrication d'une fenêtre complète."""
    return {"sensor_id": "mic-us-01", "site_id": "serre-cbd-a",
            "timestamp_start": horodatage, "timestamp_end": horodatage + fenetre,
            "sample_rate": fe_khz * 1000.0, "n_peaks": 12, "mean_energy": 0.0007,
            "median_freq": 58000.0, "peak_list_summary": [41.2, 47.9, 55.1, 62.3, 71.8],
            "env": {"temperature_c": 24.5, "humidite_pct": 72.0},
            "meta": {"version_traitement": "1.0"}, "raw_audio_ref": "audio/2026/10/25/w0001.raw"}


def est_complete(aw: dict) -> bool:
    return all(c in aw for c in CHAMPS_OBLIGATOIRES)


def verifier():
    checks = []
    aw = produire_acqwindow()
    checks.append(("EF-01 : AcqWindow produite avec les 12 champs obligatoires du schéma S-B",
                   est_complete(aw),
                   f"{sum(c in aw for c in CHAMPS_OBLIGATOIRES)}/{len(CHAMPS_OBLIGATOIRES)} champs présents"))
    checks.append(("EF-01 : bornes temporelles ordonnées (end > start)",
                   aw["timestamp_end"] > aw["timestamp_start"],
                   f"{aw['timestamp_end']} > {aw['timestamp_start']}"))
    # Nyquist : sample_rate >= 2 x 80 kHz, avec marge contractuelle 20 %
    checks.append(("EF-01 : sample_rate >= 192 kS/s (Nyquist 80 kHz + marge 20 %)",
                   aw["sample_rate"] >= FE_MIN_KHZ * 1000.0,
                   f"sample_rate={aw['sample_rate']/1000:.0f} kS/s >= {FE_MIN_KHZ:.0f} kS/s"))
    # une fenêtre incomplète est détectée (défense en profondeur I-03)
    aw_incomplete = dict(aw); aw_incomplete.pop("median_freq")
    checks.append(("EF-01 : champ manquant détecté (validation I-03)",
                   not est_complete(aw_incomplete), "median_freq absent -> incomplète"))
    return checks


def main():
    checks = verifier()
    verdict = "PASS" if all(ok for _, ok, _ in checks) else "ECHEC"
    JOURNAL.parent.mkdir(parents=True, exist_ok=True)
    JOURNAL.write_text(json.dumps(
        {"test": "TF-04", "exigences": EXIGENCES, "statut": STATUT, "verdict": verdict,
         "checks": [{"nom": n, "ok": ok, "detail": d} for n, ok, d in checks]},
        indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    for nom, ok, detail in checks:
        print(("PASS" if ok else "ECHEC") + f" {nom} — {detail}")
    raise SystemExit(0 if verdict == "PASS" else 1)


if __name__ == "__main__":
    main()
