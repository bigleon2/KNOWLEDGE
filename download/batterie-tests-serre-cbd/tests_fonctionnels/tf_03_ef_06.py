#!/usr/bin/env python3
"""TF-03 : vérifie EF-06 — conversion StressDecision -> PLCCommand (mapping, priorité, unicité).

Critère (CDC §5, EF-06, source S-B + HYP-05) : chaque décision non-healthy génère EXACTEMENT UNE
PLCCommand (target, action, parameters, duration_s, priority) ; stress_severe -> priorité
supérieure à stress_light ; healthy -> aucune commande. Implémentation de référence embarquée
(mapper contractuel pour SS-05).
"""
import json
from pathlib import Path

STATUT = "PRÊT"
EXIGENCES = ["EF-06"]
JOURNAL = Path(__file__).resolve().parent.parent / "journal" / "tf_03_ef_06.json"

PRIORITES = {"stress_light": 5, "stress_severe": 1}  # 1 = plus haute priorité
ACTIONS = {"stress_light": {"target": "irrigation_zone", "action": "arrosage",
                            "parameters": {"volume_l_m2": 1.5}, "duration_s": 600},
           "stress_severe": {"target": "irrigation_zone", "action": "arrosage_soutenu",
                             "parameters": {"volume_l_m2": 3.0}, "duration_s": 1200}}


def mapper(decision: dict):
    """Référence contractuelle EF-06 : 0 ou 1 PLCCommand selon le label de la décision."""
    label = decision.get("label")
    if label == "healthy":
        return None
    spec = ACTIONS[label]
    return {"command_id": f"cmd-{decision['decision_id']}",
            "target": spec["target"], "action": spec["action"],
            "parameters": spec["parameters"], "duration_s": spec["duration_s"],
            "priority": PRIORITES[label], "timestamp": decision["timestamp"]}


def decision(dec_id, label):
    return {"decision_id": dec_id, "label": label, "score": 0.9, "confidence": 0.87,
            "model_id": "serre-seuils-v1", "timestamp": "2026-10-25T10:00:00Z"}


def verifier():
    checks = []
    # unicité et complétude pour chaque décision non-healthy
    cmds = {lbl: mapper(decision(f"d-{lbl}", lbl))
            for lbl in ["stress_light", "stress_severe"]}
    complet = all(c is not None and all(k in c for k in
                  ["command_id", "target", "action", "parameters", "duration_s", "priority"])
                  for c in cmds.values())
    checks.append(("EF-06 : chaque décision non-healthy -> exactement 1 PLCCommand complète",
                   complet, f"champs complets pour stress_light et stress_severe"))
    # healthy -> aucune commande
    checks.append(("EF-06 : décision healthy -> 0 commande",
                   mapper(decision("d-h", "healthy")) is None, "aucune commande générée"))
    # priorité : severe strictement supérieure (valeur numérique inférieure = plus haute)
    checks.append(("EF-06 : stress_severe prioritaire sur stress_light",
                   cmds["stress_severe"]["priority"] < cmds["stress_light"]["priority"],
                   f"priority severe={cmds['stress_severe']['priority']} < "
                   f"light={cmds['stress_light']['priority']}"))
    # idempotence du mapping (même décision -> même commande)
    checks.append(("EF-06 : mapping déterministe (idempotence)",
                   mapper(decision("d-x", "stress_light")) == mapper(decision("d-x", "stress_light")),
                   "même décision -> même commande, à l'identique"))
    return checks


def main():
    checks = verifier()
    verdict = "PASS" if all(ok for _, ok, _ in checks) else "ECHEC"
    JOURNAL.parent.mkdir(parents=True, exist_ok=True)
    JOURNAL.write_text(json.dumps(
        {"test": "TF-03", "exigences": EXIGENCES, "statut": STATUT, "verdict": verdict,
         "checks": [{"nom": n, "ok": ok, "detail": d} for n, ok, d in checks]},
        indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    for nom, ok, detail in checks:
        print(("PASS" if ok else "ECHEC") + f" {nom} — {detail}")
    raise SystemExit(0 if verdict == "PASS" else 1)


if __name__ == "__main__":
    main()
