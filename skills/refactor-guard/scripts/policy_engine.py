#!/usr/bin/env python3
"""policy_engine.py - H10 fonctions de fitness architecturales (Sprint 3).

Politiques verbatim Qwen (l.5692-5696) : pas de dependance circulaire, pas de
suppression de tests, pas de changement d'API publique sans validation, pas de
modification directe du coeur sans feature flag, pas de degradation de
performance au-dela du seuil. Le moteur ne bloque jamais seul : il rend un
verdict que le niveau de gouvernance consomme (defaut N0).

Usage:
    python3 policy_engine.py --self-test
"""

import json
import sys

POLICIES = (
    "no_dependency_cycle",
    "no_test_deletion",
    "no_public_api_change_without_validation",
    "no_core_change_without_feature_flag",
    "no_performance_degradation",
)


def check_no_dependency_cycle(graph):
    """Graph {noeud: [deps]} - detecte un cycle par parcours iteratif."""
    color = {node: 0 for node in graph}

    def dfs(node):
        color[node] = 1
        for dep in graph.get(node, []):
            if color.get(dep, 0) == 1:
                return True
            if color.get(dep, 0) == 0 and dfs(dep):
                return True
        color[node] = 2
        return False

    return not any(color[node] == 0 and dfs(node) for node in list(graph))


def evaluate(change, graph=None, baseline_perf=None, current_perf=None):
    """Evalue les 5 politiques sur une demande de changement.

    change : dict(cree_cycle, supprime_tests, api_publique_modifiee,
                  validation_api, fichier, feature_flag, perf_delta_percent)
    Retourne {politique: verdict} avec verdict dans {PASS, FAIL, SKIP}.
    """
    graph = graph or {}
    perf_guard = 2
    verdicts = {}
    verdicts["no_dependency_cycle"] = "PASS" if not change.get("cree_cycle", False) else "FAIL"
    verdicts["no_test_deletion"] = "FAIL" if change.get("supprime_tests", False) else "PASS"
    if change.get("api_publique_modifiee", False):
        verdicts["no_public_api_change_without_validation"] = (
            "PASS" if change.get("validation_api", False) else "FAIL"
        )
    else:
        verdicts["no_public_api_change_without_validation"] = "SKIP"
    is_core = "core" in (change.get("fichier") or "")
    if is_core:
        verdicts["no_core_change_without_feature_flag"] = (
            "PASS" if change.get("feature_flag", False) else "FAIL"
        )
    else:
        verdicts["no_core_change_without_feature_flag"] = "SKIP"
    delta = change.get("perf_delta_percent", 0)
    verdicts["no_performance_degradation"] = "PASS" if delta <= perf_guard else "FAIL"
    if not check_no_dependency_cycle(graph or {}):
        verdicts["no_dependency_cycle"] = "FAIL"
    return verdicts


def gate(verdicts):
    """Verdict global : tout FAIL interdit ; FAIL si une politique echoue."""
    fails = [name for name, verdict in verdicts.items() if verdict == "FAIL"]
    return (False, fails) if fails else (True, [])


def main():
    """Auto-test : 5 politiques, cycle implicite, gate, cas limites."""
    if "--self-test" not in sys.argv:
        print("usage : python3 policy_engine.py --self-test", file=sys.stderr)
        return 2
    checks = []
    clean = evaluate({"fichier": "skills/x.py", "perf_delta_percent": 1})
    ok_clean, _ = gate(clean)
    checks.append(("changement propre PASS", ok_clean))
    # Politique 1 : cycle declare ET cycle dans le graphe
    cycle = evaluate({"cree_cycle": True})
    checks.append(("cycle declare FAIL", cycle["no_dependency_cycle"] == "FAIL"))
    cycle2 = evaluate({}, graph={"a": ["b"], "b": ["a"]})
    checks.append(("cycle graphe FAIL", cycle2["no_dependency_cycle"] == "FAIL"))
    # Politique 2 et 3
    bad = evaluate({"supprime_tests": True, "api_publique_modifiee": True})
    checks.append(("suppression tests FAIL", bad["no_test_deletion"] == "FAIL"))
    checks.append(("API sans validation FAIL", bad["no_public_api_change_without_validation"] == "FAIL"))
    # Politique 4 : coeur sans feature flag
    checks.append(("coeur sans flag FAIL", evaluate({"fichier": "core/main.py"})["no_core_change_without_feature_flag"] == "FAIL"))
    # Politique 5 : seuil perf depasse
    checks.append(("perf > seuil FAIL", evaluate({"perf_delta_percent": 3})["no_performance_degradation"] == "FAIL"))
    # Cas limite : graphe vide
    checks.append(("graphe vide sans cycle", check_no_dependency_cycle({})))
    ok_bad, fails = gate(bad)
    checks.append(("gate refuse et liste", not ok_bad and len(fails) >= 2))
    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print("%s: %s" % (name, "PASS" if ok else "FAIL"))
    print("SELF-TEST : %s (%d/%d)" % ("PASS" if passed == len(checks) else "FAIL", passed, len(checks)))
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
