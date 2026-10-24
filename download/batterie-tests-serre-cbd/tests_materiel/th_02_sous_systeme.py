#!/usr/bin/env python3
"""TH-02 : propagation ultrasonore atténuée — portée de détection cible 5 m en air humide.

Simule (graine fixe 42, stdlib) la propagation d'un clic ultrasonore 40-80 kHz émis à 60-65 dB
(S-A) vers un capteur distant, avec les mécanismes de l'ISO 9613-2 [S1] transposés à la bande
ultrasonore (HORS domaine nominal de la norme — simplification empirique assumée, cf. fiche
domaine / HYP-03) : divergence géométrique Adiv = 20·log10(r/r0) et absorption atmosphérique
Aatm = alpha(f, RH)·r, avec alpha croissant en f² et décroissant avec l'humidité relative
(relaxation de l'oxygène — approximation monotone documentée).

Vérifie : ENF-08/[HYP-03] (portée >= 5 m sur la bande cœur 40-60 kHz, marge >= 95 %),
monotonie en distance et en humidité.
"""
import json
import math
import random
from pathlib import Path

STATUT = "PRÊT"
EXIGENCES = ["ENF-08"]
JOURNAL = Path(__file__).resolve().parent.parent / "journal" / "th_02_sous_systeme.json"

SEED = 42
L0_DB = 62.0            # dB — niveau d'émission au point source (plage 60-65 dB de S-A)
SEUIL_CAPTEUR_DB = 35.0  # dB — sensibilité du micro ultrasonique
PORTÉE_CIBLE_M = 5.0     # S-A / Natural History Museum de Londres
BANDE_CŒUR = (40_000.0, 60_000.0)   # Hz — bande cœur la moins atténuée
K_ALPHA = 1.2e-9         # dB/m/Hz² — coefficient d'absorption calibré (ordre de grandeur)


def alpha_db_par_m(f: float, rh_pct: float) -> float:
    """Absorption atmosphérique simplifiée : croissante en f², décroissante en humidité."""
    return K_ALPHA * f * f * (100.0 - rh_pct) / 100.0


def niveau_recu_db(f: float, rh_pct: float, r_m: float) -> float:
    """Niveau au capteur : émission - divergence géométrique - absorption atmosphérique."""
    adiv = 20.0 * math.log10(max(r_m, 0.1) / 1.0)     # divergence (source ponctuelle)
    aatm = alpha_db_par_m(f, rh_pct) * r_m             # absorption
    return L0_DB - adiv - aatm


def taux_detection_bande_coeur(rh_pct: float, r_m: float, n: int = 2000) -> float:
    """Proportion de clics de la bande cœur détectés (bruit de niveau seedé)."""
    rng = random.Random(SEED)
    ok = 0
    for _ in range(n):
        f = rng.uniform(*BANDE_CŒUR)
        niveau = L0_DB + rng.uniform(-2.0, 3.0)        # 60-65 dB
        ok += 1 if (niveau_recu_db(f, rh_pct, r_m) + (niveau - L0_DB)) >= SEUIL_CAPTEUR_DB else 0
    return ok / n


def verifier():
    checks = []
    # portée cible : >= 95 % des clics de la bande cœur détectés à 5 m, air humide 70 %
    taux_5m = taux_detection_bande_coeur(70.0, PORTÉE_CIBLE_M)
    checks.append(("ENF-08/[HYP-03] : >= 95 % des clics 40-60 kHz détectés à 5 m (RH 70 %)",
                   taux_5m >= 0.95, f"taux={taux_5m*100:.1f} % à {PORTÉE_CIBLE_M:.0f} m"))
    # monotonie en distance (plus près = mieux détecté)
    t4, t5, t6 = (taux_detection_bande_coeur(70.0, r) for r in (4.0, 5.0, 6.0))
    checks.append(("TH-02 : monotonie en distance (4 m >= 5 m >= 6 m)",
                   t4 >= t5 >= t6 - 1e-9,
                   f"4 m={t4*100:.1f} % / 5 m={t5*100:.1f} % / 6 m={t6*100:.1f} %"))
    # effet humidité : air plus humide = absorption plus faible (approximation monotone)
    a30 = alpha_db_par_m(50_000.0, 30.0)
    a90 = alpha_db_par_m(50_000.0, 90.0)
    checks.append(("TH-02 : absorption décroissante avec l'humidité (relaxation O2, approx.)",
                   a90 < a30, f"alpha(50 kHz, 30 %)={a30:.2f} dB/m > alpha(90 %)={a90:.2f} dB/m"))
    # haut de bande plus atténué (croissance en f²) — honnêteté sur la bande 80 kHz
    a40 = alpha_db_par_m(40_000.0, 70.0)
    a80 = alpha_db_par_m(80_000.0, 70.0)
    checks.append(("TH-02 : absorption croissante en f² (80 kHz plus atténué que 40 kHz)",
                   a80 > a40, f"alpha(80 kHz)={a80:.2f} > alpha(40 kHz)={a40:.2f} dB/m"))
    # déterminisme (graine fixe)
    checks.append(("TH-02 : déterminisme (graine 42)",
                   taux_5m == taux_detection_bande_coeur(70.0, PORTÉE_CIBLE_M),
                   f"taux stable = {taux_5m*100:.1f} %"))
    return checks


def main():
    checks = verifier()
    verdict = "PASS" if all(ok for _, ok, _ in checks) else "ECHEC"
    JOURNAL.parent.mkdir(parents=True, exist_ok=True)
    JOURNAL.write_text(json.dumps(
        {"test": "TH-02", "exigences": EXIGENCES, "statut": STATUT, "verdict": verdict,
         "checks": [{"nom": n, "ok": ok, "detail": d} for n, ok, d in checks]},
        indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    for nom, ok, detail in checks:
        print(("PASS" if ok else "ECHEC") + f" {nom} — {detail}")
    raise SystemExit(0 if verdict == "PASS" else 1)


if __name__ == "__main__":
    main()
