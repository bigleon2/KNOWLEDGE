#!/usr/bin/env python3
"""shadow_run.py - Execution N1 shadow de refactor-guard + calibration grille #token (E15).

Realise le pipeline R1-R8 en mode shadow (observation passive, AUCUNE ecriture
sur la cible) sur un repertoire reel de l'ecosysteme, mesure le cout #token de
chaque phase (heuristique E15 : 3,5 caracteres/token, mix francais/code) et
compare aux plages initiales SKILL.md §2.5 (v1.0.0) pour la recalibration E15.

Gouvernance : refuse tout mode dont plan_rollout(mode)["apply"] est vrai
(N1 shadow = observe seulement) ; ABANDON sans ecriture sinon. La seule
ecriture autorisee est le journal d'audit (H09) et le rapport de calibration,
hors de la cible.

Usage:
    python3 shadow_run.py --target <repertoire> --ledger <audit.jsonl> [--report <calibration.json>]
    python3 shadow_run.py --self-test

Codes retour : 0 = ok ; 1 = garde gouvernance ; 2 = usage/cible invalide ; 3 = self-test echoue.
"""

import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import config as rg_config
import graph_scan
import risk_score
import spec_builder
import human_gate
import rollout
from audit_ledger import AuditLedger

PLAGES_INITIALES = {  # SKILL.md §2.5 v1.0.0 (plages initiales)
    "R1-R3": (500, 1200),
    "R4-R6": (2000, 6000),
    "R7-R8": (3000, 8000),
}
CHARS_PAR_TOKEN = 3.5  # heuristique E15 (mix francais/code) — documentee, estimation
MODES_OBSERVATION = ("disabled", "shadow", "recommend_only", "sandbox_only")


def estime_tokens(texte):
    """Heuristique E15 : nombre de tokens estime d'une charge utile texte/JSON."""
    return max(1, int(math.ceil(len(texte) / CHARS_PAR_TOKEN)))


def garde_gouvernance(mode):
    """Autorise uniquement les modes d'observation (apply False). Retourne (ok, plan)."""
    plan = rollout.plan_rollout(mode)
    return (plan["apply"] is False and mode in MODES_OBSERVATION), plan


def construit_trigger(target, reason="calibration E15 - premiere execution N1 shadow"):
    """R1 : trigger JSON au format SKILL.md §2.4."""
    return {
        "trigger": "explicit",
        "target": target,
        "reason": reason,
        "severity": "low",
        "metrics": {"cyclomatic_complexity": 0, "coupling": 0, "cohesion": 1.0, "test_coverage": 0.0},
        "constraints": ["aucun push sans validation", "N1 shadow : aucune ecriture"],
    }


def agrege_metriques(scan):
    """R2->R3 : agregats conservateurs depuis le scan (max complexite/couplage, couverture inconnue = 0.0)."""
    metriques = scan.get("metriques", {})
    max_complexite = max((m.get("cyclomatic_complexity", 0) for m in metriques.values()), default=0)
    max_couplage = max((m.get("coupling", 0) for m in metriques.values()), default=0)
    return {
        "cyclomatic_complexity": max_complexite,
        "coupling": max_couplage,
        "cohesion": 1.0 if not metriques else 0.8,
        "test_coverage": 0.0,  # inconnue en shadow — hypothese conservatrice documentee
    }


def run_shadow(target, ledger_path, report_path=None):
    """Pipeline R1-R8 shadow + mesure #token par phase. Retourne le rapport (dict)."""
    if not os.path.isdir(target):
        print("ABANDON : cible introuvable : %s" % target)
        sys.exit(2)
    cfg = rg_config.load_config()
    cfg["mode"] = "N1"
    ok, plan = garde_gouvernance("shadow")
    if not ok:
        print("ABANDON : mode d'application refuse en shadow")
        sys.exit(1)
    phases = {}
    # R1 - reception du signal
    trigger = construit_trigger(target)
    phases["R1"] = estime_tokens(json.dumps(trigger, ensure_ascii=False, sort_keys=True))
    # R2 - scan et analyse (H02)
    scan = graph_scan.scanner(target)
    phases["R2"] = estime_tokens(json.dumps(scan, ensure_ascii=False, sort_keys=True))
    # R3 - score de risque (H14)
    metrics = agrege_metriques(scan)
    risque = risk_score.compute_risk(metrics, critique=False)
    phases["R3"] = estime_tokens(json.dumps(risque, ensure_ascii=False, sort_keys=True))
    # R4 - specification (H07) : contrat 9 sections, en memoire uniquement
    spec, spec_verdict, spec_missing = spec_builder.build_spec(
        goal="observation shadow de %s (calibration E15)" % target,
        scope=target,
        files=sorted(scan.get("metriques", {}).keys()),
        preserve=["comportement observable", "interfaces publiques", "performances"],
        tests=["self-tests modules", "arbitres ecosysteme"],
        constraints=["N1 shadow : aucune ecriture", "allow_push: false"],
        criteria=["0 S1/S2", "latence < 2 %", "CPU < 5 %", "memoire < 5 %"],
        plan=["R1-R3 observation", "R4-R6 specification/plan", "R7-R8 gates"],
        rollback=["snapshot tar anti-R2", "git status avant/apres"],
    )
    spec_valide = (spec_verdict == "VALIDE")
    phases["R4"] = estime_tokens(json.dumps(spec, ensure_ascii=False, sort_keys=True))
    # R5 - sandbox (H04) : en shadow, aucune execution — represente par le contrat seul
    sandbox_contrat = {"sandbox": "shadow_skip", "real_change_applied": False,
                       "isolation": "copies uniquement (N3 requis pour execution)",
                       "hash_avant": None, "hash_apres": None}
    phases["R5"] = estime_tokens(json.dumps(sandbox_contrat, ensure_ascii=False, sort_keys=True))
    # R6 - plan d'actions (gen-plan, N2+) : en shadow, le plan de la spec fait foi
    phases["R6"] = estime_tokens(json.dumps(spec.get("plan_propose", []), ensure_ascii=False, sort_keys=True))
    # R7 - maker-checker / human gate (H05/H15)
    gate = human_gate.decide(risque["risk_level"], metrics["test_coverage"], sensitive_zones=False)
    phases["R7"] = estime_tokens(json.dumps(gate, ensure_ascii=False, sort_keys=True))
    # R8 - rollout + validation finale (H08) : gate verbatim evalue a sec (baseline == courant)
    baseline = {"error_rate": 0.0, "avg_latency_ms": 100.0}
    courant = {"tests_failed": 0, "error_rate": 0.0, "avg_latency_ms": 100.0,
               "new_dependency_cycles": len(scan.get("cycles", [])), "rollback_verified": True}
    gate_verbatim = rollout.can_apply_change(baseline, courant)
    phases["R8"] = estime_tokens(json.dumps({"plan": plan, "can_apply_change_sec": gate_verbatim},
                                            ensure_ascii=False, sort_keys=True))
    # Groupes SKILL.md §2.5
    groupes = {
        "R1-R3": phases["R1"] + phases["R2"] + phases["R3"],
        "R4-R6": phases["R4"] + phases["R5"] + phases["R6"],
        "R7-R8": phases["R7"] + phases["R8"],
    }
    comparaison = {}
    for g, (bas, haut) in PLAGES_INITIALES.items():
        mesure = groupes[g]
        comparaison[g] = {"mesure": mesure, "plage_initiale": [bas, haut],
                          "dans_plage": bas <= mesure <= haut,
                          "ecart": mesure - haut if mesure > haut else (mesure - bas if mesure < bas else 0)}
    rapport = {
        "type": "shadow-run-calibration",
        "mode": cfg["mode"],
        "target": target,
        "nb_fichiers": scan.get("nb_fichiers", 0),
        "cycles_detectes": len(scan.get("cycles", [])),
        "risk": {"score": risque["risk_score"], "niveau": risque["risk_level"], "decision": risque["decision"]},
        "spec_valide": bool(spec_valide),
        "apply_autorise": plan["apply"],
        "tokens_par_phase": phases,
        "groupes_tokens": groupes,
        "comparaison_plages": comparaison,
        "estimation_note": "heuristique E15 : %.1f chars/token (mix FR/code) — estimation, pas un comptage tokenizer" % CHARS_PAR_TOKEN,
    }
    # Journal d'audit (H09) — seule ecriture, hors cible
    ledger = AuditLedger(ledger_path)
    ledger.record({
        "trigger": trigger,
        "analysis": {"nb_fichiers": scan.get("nb_fichiers", 0), "cycles": len(scan.get("cycles", []))},
        "risk_score": risque["risk_score"],
        "specification": {"valide": bool(spec_valide), "verdict": spec_verdict, "manquants": spec_missing},
        "sandbox_result": sandbox_contrat,
        "decision": "shadow-observation (aucune application)",
        "rollback": "n/a (aucune modification)",
        "author": "shadow_run.py N1",
    })
    ledger.flush()
    if report_path:
        with open(report_path, "w", encoding="utf-8") as handle:
            json.dump(rapport, handle, indent=2, ensure_ascii=False, sort_keys=True)
    return rapport


def _self_test():
    """Auto-test deterministe : pipeline shadow complet, garde N4 refusee, idempotence x2."""
    import tempfile
    checks = []
    d = tempfile.mkdtemp(prefix="rg-shadow-")
    with open(os.path.join(d, "a.py"), "w", encoding="utf-8") as h:
        h.write("import os\nimport json\ndef f(x):\n    if x > 0:\n        return 1\n    return 0\n")
    ledger1 = os.path.join(d, "audit1.jsonl")
    r1 = run_shadow(d, ledger1)
    checks.append(("apply False", r1["apply_autorise"] is False))
    checks.append(("tokens positifs", all(v > 0 for v in r1["tokens_par_phase"].values())))
    checks.append(("3 groupes", set(r1["groupes_tokens"]) == set(PLAGES_INITIALES)))
    checks.append(("comparaison complete", set(r1["comparaison_plages"]) == set(PLAGES_INITIALES)))
    checks.append(("spec validee", r1["spec_valide"] is True))
    checks.append(("ledger ecrit", os.path.isfile(ledger1) and os.path.getsize(ledger1) > 0))
    cible_vide = not [n for n in os.listdir(d) if n not in ("a.py", "audit1.jsonl")]
    checks.append(("aucune ecriture sur cible", cible_vide))
    # Idempotence x2 : meme run -> memes comptages
    ledger2 = os.path.join(d, "audit2.jsonl")
    r2 = run_shadow(d, ledger2)
    checks.append(("idempotence x2", r1["tokens_par_phase"] == r2["tokens_par_phase"]))
    # Garde gouvernance : mode d'application refuse
    ok_n4, _ = garde_gouvernance("human_approved")
    checks.append(("garde refuse N4", ok_n4 is False))
    ok_sh, _ = garde_gouvernance("shadow")
    checks.append(("garde autorise shadow", ok_sh is True))
    # Heuristique bornee
    checks.append(("estime_tokens 0", estime_tokens("") == 1))
    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print("%s: %s" % (name, "PASS" if ok else "FAIL"))
    print("SELF-TEST : %s (%d/%d)" % ("PASS" if passed == len(checks) else "FAIL", passed, len(checks)))
    return 0 if passed == len(checks) else 3


def main():
    """Point d'entree CLI."""
    args = sys.argv[1:]
    if "--self-test" in args:
        return _self_test()
    if "--target" not in args or "--ledger" not in args:
        print(__doc__)
        return 2
    target = args[args.index("--target") + 1]
    ledger = args[args.index("--ledger") + 1]
    report = args[args.index("--report") + 1] if "--report" in args else None
    rapport = run_shadow(target, ledger, report)
    print(json.dumps(rapport, indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
