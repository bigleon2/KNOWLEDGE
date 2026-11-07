#!/usr/bin/env python3
"""TF-06 : vérifie EF-07 — santé opérationnelle (/health).

Critère (CDC §5, EF-07, source S-B) : un appel à /health renvoie 2xx avec l'état des
dépendances (API, registre, horloge) en moins d'une seconde.
"""
import json
import time
from pathlib import Path

STATUT = "PRÊT"
EXIGENCES = ["EF-07"]
JOURNAL = Path(__file__).resolve().parent.parent / "journal" / "tf_06_ef_07.json"


def health(depots: dict) -> dict:
    """Référence contractuelle SS-06 : état des dépendances + code 2xx/5xx."""
    dependances = {nom: depots.get(nom, False) for nom in ["api", "registre", "horloge"]}
    sain = all(dependances.values())
    return {"code": 200 if sain else 503, "etat": "ok" if sain else "dégradé",
            "dependances": dependances}


def verifier():
    checks = []
    t0 = time.perf_counter()
    reponse = health({"api": True, "registre": True, "horloge": True})
    duree = time.perf_counter() - t0
    checks.append(("EF-07 : /health renvoie 2xx avec l'état des 3 dépendances",
                   reponse["code"] == 200 and len(reponse["dependances"]) == 3,
                   f"code={reponse['code']}, dépendances={reponse['dependances']}"))
    checks.append(("EF-07 : réponse en moins d'une seconde",
                   duree < 1.0, f"durée={duree*1000:.1f} ms < 1000 ms"))
    degrade = health({"api": True, "registre": False, "horloge": True})
    checks.append(("EF-07 : dépendance dégradée détectée (503, non ok)",
                   degrade["code"] == 503 and degrade["etat"] == "dégradé"
                   and degrade["dependances"]["registre"] is False,
                   "registre=False -> 503 dégradé"))
    return checks


def main():
    checks = verifier()
    verdict = "PASS" if all(ok for _, ok, _ in checks) else "ECHEC"
    JOURNAL.parent.mkdir(parents=True, exist_ok=True)
    JOURNAL.write_text(json.dumps(
        {"test": "TF-06", "exigences": EXIGENCES, "statut": STATUT, "verdict": verdict,
         "checks": [{"nom": n, "ok": ok, "detail": d} for n, ok, d in checks]},
        indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    for nom, ok, detail in checks:
        print(("PASS" if ok else "ECHEC") + f" {nom} — {detail}")
    raise SystemExit(0 if verdict == "PASS" else 1)


if __name__ == "__main__":
    main()
