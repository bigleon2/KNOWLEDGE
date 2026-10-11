#!/usr/bin/env python3
"""rollout.py - H08 rollout progressif des refactorisations (Sprint 5).

Modes verbatim Qwen (l.5789-5795) : disabled -> shadow -> recommend_only ->
sandbox_only -> human_approved -> canary -> enabled. Gate de non-regression
exécutable verbatim (l.6822-6836) et regle de passage de niveau (6 conditions,
l.6400-6405). canary_percentage par defaut 0 (config N0).

Usage:
    python3 rollout.py --self-test
"""

import json
import sys

MODES = ("disabled", "shadow", "recommend_only", "sandbox_only", "human_approved", "canary", "enabled")
CONDITIONS_PASSAGE = (
    "niveau_precedent_stable",
    "tests_verts",
    "metriques_conformes",
    "aucun_incident",
    "rollback_teste",
    "decision_documentee",
)


def can_apply_change(baseline, current):
    """Gate verbatim Qwen : aucune application si un critere de non-regression echoue."""
    if current["tests_failed"] > 0:
        return False
    if current["error_rate"] > baseline["error_rate"]:
        return False
    latency_increase = (
        (current["avg_latency_ms"] - baseline["avg_latency_ms"]) / baseline["avg_latency_ms"] * 100
    )
    if latency_increase > 2.0:
        return False
    if current["new_dependency_cycles"] > 0:
        return False
    if not current["rollback_verified"]:
        return False
    return True


def next_mode(current, conditions):
    """Autorise un passage au mode suivant uniquement si les 6 conditions tiennent."""
    if current not in MODES or current == "enabled":
        return current
    if set(conditions) != set(CONDITIONS_PASSAGE):
        return current
    return MODES[MODES.index(current) + 1]


PLANS = {
    "disabled": {"apply": False, "observe": False},
    "shadow": {"apply": False, "observe": True},
    "recommend_only": {"apply": False, "observe": True, "recommend": True},
    "sandbox_only": {"apply": False, "observe": True, "recommend": True, "sandbox": True},
    "human_approved": {"apply": True, "observe": True, "require_human_approval": True},
    "canary": {"apply": True, "observe": True, "canary_percentage": 0},
    "enabled": {"apply": True, "observe": True},
}


def plan_rollout(mode, canary_percentage=0):
    """Retourne le plan d'application autorise pour un mode donne.

    Optimisation v2 (Qwen T13) : plans precalcules au niveau module (hoisting),
    copie unique pour canary (le seul plan parametre).
    """
    plan = dict(PLANS[mode])
    plan["mode"] = mode
    if mode == "canary":
        plan["canary_percentage"] = max(0, min(100, canary_percentage))
    return plan


def main():
    """Auto-test : gate verbatim, progression 6 conditions, plans, cas limites."""
    if "--self-test" not in sys.argv:
        print("usage : python3 rollout.py --self-test", file=sys.stderr)
        return 2
    checks = []
    baseline = {"error_rate": 0.0, "avg_latency_ms": 100.0}
    good = {
        "tests_failed": 0,
        "error_rate": 0.0,
        "avg_latency_ms": 101.5,
        "new_dependency_cycles": 0,
        "rollback_verified": True,
    }
    checks.append(("gate PASS +1.5%", can_apply_change(baseline, good)))
    # Latence +2.1% -> FAIL (seuil strict 2.0)
    late = dict(good, avg_latency_ms=102.1)
    checks.append(("gate FAIL +2.1%", not can_apply_change(baseline, late)))
    # Chaque critere echoue un par un
    for field, mutation in (
        ("tests", {"tests_failed": 1}),
        ("erreur", {"error_rate": 0.1}),
        ("cycle", {"new_dependency_cycles": 1}),
        ("rollback", {"rollback_verified": False}),
    ):
        checks.append(("gate FAIL %s" % field, not can_apply_change(baseline, dict(good, **mutation))))
    # Progression : 6 conditions requises, sinon statu quo
    all_conditions = set(CONDITIONS_PASSAGE)
    checks.append(("progression disabled->shadow", next_mode("disabled", all_conditions) == "shadow"))
    checks.append(("progression bloquee 5/6", next_mode("shadow", all_conditions - {"rollback_teste"}) == "shadow"))
    checks.append(("enabled termine", next_mode("enabled", all_conditions) == "enabled"))
    checks.append(("mode inconnu statu quo", next_mode("bogus", all_conditions) == "bogus"))
    # Plans : N0 shadow n'applique rien ; canary plafonne 0-100
    checks.append(("shadow sans application", plan_rollout("shadow")["apply"] is False))
    checks.append(("canary plafond", plan_rollout("canary", 150)["canary_percentage"] == 100))
    checks.append(("canary defaut 0", plan_rollout("canary")["canary_percentage"] == 0))
    checks.append(("determinisme", json.dumps(plan_rollout("canary", 5), sort_keys=True) == json.dumps(plan_rollout("canary", 5), sort_keys=True)))
    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print("%s: %s" % (name, "PASS" if ok else "FAIL"))
    print("SELF-TEST : %s (%d/%d)" % ("PASS" if passed == len(checks) else "FAIL", passed, len(checks)))
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
