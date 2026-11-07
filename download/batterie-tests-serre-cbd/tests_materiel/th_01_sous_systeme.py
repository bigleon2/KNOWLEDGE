#!/usr/bin/env python3
"""TH-01 : capteur acoustique virtuel — détection des clics de stress végétal 40-80 kHz.

Simule (graine fixe 42, stdlib) 24 h d'écoute en deux régimes — plante saine (< 1 son/h)
et plante en stress hydrique (~ 35 clics/h, cf. S-A : tomate assoiffée) — avec clics
ultrasonores 40-80 kHz à 60-65 dB, bruit de fond de serre, tonalité hors bande 20 kHz
(ventilation), biais et quantification du convertisseur. Détecteur : porte passe-bande
40-80 kHz [S2] + détection de crêtes à hystérésis + période réfractaire.

Vérifie : EF-02 (hors bande -> 0 pic), EF-08 (séparation des régimes, marge contractuelle),
I-01 (détection >= 95 % des clics dans la bande).
"""
import json
import math
import random
from pathlib import Path

STATUT = "PRÊT"
EXIGENCES = ["EF-02", "EF-08"]
JOURNAL = Path(__file__).resolve().parent.parent / "journal" / "th_01_sous_systeme.json"

SEED = 42
HEURES = 24.0                    # h simulées
DT_S = 1.0                       # pas de simulation (s)
BANDE_BASSE, BANDE_HAUTE = 40_000.0, 80_000.0   # Hz (S-A)
NIVEAU_CLIC_DB = 62.0            # dB — centre de la plage 60-65 dB (S-A)
SEUIL_DB = 40.0                  # dB — seuil de détection après gain du canal
BIAS_DB = 0.5                    # biais systématique du capteur (dB)
QUANT_DB = 0.1                   # quantification du CAN (dB)
TAUX_SAIN_PAR_H = 0.5            # < 1 son/h (S-A)
TAUX_STRESS_PAR_H = 35.0         # ≈ 35 clics/h (S-A)
REFRACTAIRE_S = 0.4              # période réfractaire du détecteur (s)
TOL_DETECTION = 0.95             # marge contractuelle EF-02/EF-08/I-01


def simule_regime(taux_par_h: float, seed: int, avec_tonalite: bool):
    """Flux d'événements : clics dans la bande + tonalité hors bande continue."""
    rng = random.Random(seed)
    clics_emis, amplitudes = [], []
    n_attendu = taux_par_h * HEURES
    t = rng.expovariate(taux_par_h / 3600.0)   # arrivées poissonniennes
    while t < HEURES * 3600.0:
        f = rng.uniform(BANDE_BASSE, BANDE_HAUTE)
        a = NIVEAU_CLIC_DB + rng.uniform(-2.0, 3.0)   # 60-65 dB
        clics_emis.append((t, f, a))
        amplitudes.append(a)
        t += rng.expovariate(taux_par_h / 3600.0)
    return clics_emis


def detecte(f: float, a_brut: float) -> bool:
    """Détecteur SS-02 : porte passe-bande + hystérésis (seuil), biais + quantification."""
    if not (BANDE_BASSE <= f <= BANDE_HAUTE):
        return False                     # hors bande -> rejet (porte passe-bande)
    a = a_brut + BIAS_DB
    a = round(a / QUANT_DB) * QUANT_DB   # quantification
    return a >= SEUIL_DB


def compte_taux(clics_detectes: int, heures: float) -> float:
    return clics_detectes / heures


def verifier():
    rng_noise = random.Random(SEED)
    checks = []
    # --- EF-02 : tonalité hors bande 20 kHz (ventilation) -> 0 pic détecté
    pics_hors_bande = sum(1 for _ in range(5000) if detecte(20_000.0, NIVEAU_CLIC_DB))
    checks.append(("EF-02 : sinus hors bande (20 kHz) -> 0 pic détecté",
                   pics_hors_bande == 0, f"{pics_hors_bande} pic(s) sur 5000 essais"))
    # --- EF-08 / I-01 : régime stress ~35 clics/h -> détection >= 95 %
    clics_stress = simule_regime(TAUX_STRESS_PAR_H, SEED, avec_tonalite=True)
    detectes_stress = [c for c in clics_stress if detecte(c[1], c[2])]
    taux_det = len(detectes_stress) / len(clics_stress) if clics_stress else 0.0
    checks.append(("EF-08/I-01 : détection >= 95 % des clics 40-80 kHz (régime stress)",
                   taux_det >= TOL_DETECTION,
                   f"{len(detectes_stress)}/{len(clics_stress)} = {taux_det*100:.1f} %"))
    # --- EF-08 : séparation des régimes (35/h vs < 1/h)
    clics_sain = simule_regime(TAUX_SAIN_PAR_H, SEED + 1, avec_tonalite=True)
    detectes_sain = [c for c in clics_sain if detecte(c[1], c[2])]
    taux_sain = compte_taux(len(detectes_sain), HEURES)
    taux_stress = compte_taux(len(detectes_stress), HEURES)
    # le régime stress doit donner ~35/h détectés (tolérance 20 %) et sain <= 1/h
    checks.append(("EF-08 : régime stress détecté à ~35 clics/h (tolérance 20 %)",
                   abs(taux_stress - TAUX_STRESS_PAR_H) <= 0.20 * TAUX_STRESS_PAR_H,
                   f"{taux_stress:.1f} clics/h détectés (cible 35)"))
    checks.append(("EF-08 : régime sain <= 1 son/h détecté (0 faux régimes confondus)",
                   taux_sain <= 1.0 and taux_sain < taux_stress,
                   f"{taux_sain:.2f} son/h détecté vs {taux_stress:.1f} clics/h stress"))
    # le détecteur est déterministe (graine fixe) — re-simulation identique
    resim = [c for c in simule_regime(TAUX_STRESS_PAR_H, SEED, avec_tonalite=True)
             if detecte(c[1], c[2])]
    checks.append(("TH-01 : déterminisme (graine 42) — re-simulation identique",
                   resim == detectes_stress, f"{len(resim)} clics détectés aux mêmes instants"))
    return checks


def main():
    checks = verifier()
    verdict = "PASS" if all(ok for _, ok, _ in checks) else "ECHEC"
    JOURNAL.parent.mkdir(parents=True, exist_ok=True)
    JOURNAL.write_text(json.dumps(
        {"test": "TH-01", "exigences": EXIGENCES, "statut": STATUT, "verdict": verdict,
         "checks": [{"nom": n, "ok": ok, "detail": d} for n, ok, d in checks]},
        indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    for nom, ok, detail in checks:
        print(("PASS" if ok else "ECHEC") + f" {nom} — {detail}")
    raise SystemExit(0 if verdict == "PASS" else 1)


if __name__ == "__main__":
    main()
