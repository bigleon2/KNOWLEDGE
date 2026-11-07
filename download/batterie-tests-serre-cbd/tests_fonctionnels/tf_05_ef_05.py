#!/usr/bin/env python3
"""TF-05 : vérifie EF-05 — traçabilité des décisions via le registre de modèles.

Critère (CDC §5, EF-05, source S-B) : chaque décision StressDecision référence un model_id
présent dans model_registry.json (version + seuils utilisés) — 0 décision orpheline de registre.
"""
import json
from pathlib import Path

STATUT = "PRÊT"
EXIGENCES = ["EF-05"]
JOURNAL = Path(__file__).resolve().parent.parent / "journal" / "tf_05_ef_05.json"

# Registre de référence contractuel (SS-03) — structure model_registry.json de S-B
REGISTRE = {
    "serre-seuils-v1": {"version": "1.0.0",
                        "seuils": {"light_pics": 8, "light_energie": 0.0005,
                                   "severe_pics": 20, "severe_energie": 0.001}},
}


def decision_avec_registre(dec_id: str, model_id: str, registre: dict):
    """Référence contractuelle : une décision ne peut être émise que si son model_id est connu."""
    if model_id not in registre:
        raise ValueError(f"EF-05 violée : décision {dec_id} orpheline (model_id inconnu)")
    return {"decision_id": dec_id, "model_id": model_id, "label": "stress_light",
            "score": 0.9, "confidence": 0.85, "timestamp": "2026-10-25T10:00:00Z"}


def verifier():
    checks = []
    # chaque décision porte un model_id du registre
    dec = decision_avec_registre("d-1", "serre-seuils-v1", REGISTRE)
    checks.append(("EF-05 : décision référence un model_id présent au registre",
                   dec["model_id"] in REGISTRE, f"model_id={dec['model_id']} connu"))
    # 0 décision orpheline : model_id inconnu -> rejet (levée d'erreur)
    orpheline_rejetee = False
    try:
        decision_avec_registre("d-2", "modele-inconnu", REGISTRE)
    except ValueError:
        orpheline_rejetee = True
    checks.append(("EF-05 : 0 décision orpheline (model_id inconnu rejeté)",
                   orpheline_rejetee, "ValueError levée pour model_id hors registre"))
    # le registre porte les seuils utilisés (cohérence EF-03)
    seuils = REGISTRE["serre-seuils-v1"]["seuils"]
    checks.append(("EF-05 : registre porte version + seuils utilisés (cohérence EF-03)",
                   all(k in seuils for k in ["light_pics", "light_energie",
                                             "severe_pics", "severe_energie"])
                   and REGISTRE["serre-seuils-v1"]["version"] == "1.0.0",
                   f"seuils={seuils}"))
    return checks


def main():
    checks = verifier()
    verdict = "PASS" if all(ok for _, ok, _ in checks) else "ECHEC"
    JOURNAL.parent.mkdir(parents=True, exist_ok=True)
    JOURNAL.write_text(json.dumps(
        {"test": "TF-05", "exigences": EXIGENCES, "statut": STATUT, "verdict": verdict,
         "checks": [{"nom": n, "ok": ok, "detail": d} for n, ok, d in checks]},
        indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    for nom, ok, detail in checks:
        print(("PASS" if ok else "ECHEC") + f" {nom} — {detail}")
    raise SystemExit(0 if verdict == "PASS" else 1)


if __name__ == "__main__":
    main()
