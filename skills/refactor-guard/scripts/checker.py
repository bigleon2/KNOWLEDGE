#!/usr/bin/env python3
"""checker.py - H05 boucle maker-checker (Sprint 5).

Flux verbatim Qwen (l.5733-5739) : Proposition -> Critique -> Validation
technique -> Rapport. Un agent propose, un autre verifie ; la critique et la
validation technique sont deux etapes distinctes et obligatoires.

Usage:
    python3 checker.py --self-test
"""

import json
import sys

STAGES = ("proposition", "critique", "validation_technique", "rapport")


def run_maker_checker(proposition, critic, technical_validator):
    """Execute la boucle 4 stages.

    critic : fonction(proposition) -> {"approuve": bool, "notes": str}
    technical_validator : fonction(proposition, critique) -> {"approuve": bool, "tests": str}
    La rapport final n'est emis que si critique ET validation approuvent.
    """
    trace = {"stages": [], "approuve": False}
    trace["stages"].append({"stage": "proposition", "contenu": proposition})
    critique = critic(proposition)
    trace["stages"].append({"stage": "critique", **critique})
    if not critique.get("approuve", False):
        trace["rapport"] = "REJETE en critique"
        return trace
    validation = technical_validator(proposition, critique)
    trace["stages"].append({"stage": "validation_technique", **validation})
    if not validation.get("approuve", False):
        trace["rapport"] = "REJETE en validation technique"
        return trace
    trace["approuve"] = True
    trace["rapport"] = "APPROUVE (maker-checker complet)"
    return trace


def lax_checker(proposition):
    """Contre-exemple documente : un checker trop laxiste est un risque Qwen (I3)."""
    return {"approuve": True, "notes": "laxiste (risque documente I3)"}


def main():
    """Auto-test : 4 stages, rejet en critique, rejet en validation, cas limites."""
    if "--self-test" not in sys.argv:
        print("usage : python3 checker.py --self-test", file=sys.stderr)
        return 2
    checks = []

    def critic_strict(prop):
        return {"approuve": "risque" not in prop.get("description", ""), "notes": "verification risque"}

    def validator_strict(prop, critique):
        return {"approuve": prop.get("tests_presents", False), "tests": "py_compile + pytest"}

    ok_prop = {"description": "extraire module", "tests_presents": True}
    trace = run_maker_checker(ok_prop, critic_strict, validator_strict)
    checks.append(("approuve 4 stages", trace["approuve"] and len(trace["stages"]) == 3))
    checks.append(("stages conformes", [s["stage"] for s in trace["stages"]] == list(STAGES[:3])))
    # Rejet en critique
    risky = {"description": "refactor risquee", "tests_presents": True}
    trace2 = run_maker_checker(risky, critic_strict, validator_strict)
    checks.append(("rejet en critique", not trace2["approuve"] and "critique" in trace2["rapport"]))
    # Rejet en validation technique
    notested = {"description": "extraire module", "tests_presents": False}
    trace3 = run_maker_checker(notested, critic_strict, validator_strict)
    checks.append(("rejet en validation", not trace3["approuve"] and "validation" in trace3["rapport"]))
    # Cas limite : checker laxiste + validator technique = le risque I3 documente
    # (la critique laxiste laisse passer le risque ; la validation technique ne
    # porte que sur les tests — d'ou l'exigence des DEUX stages stricts)
    trace4 = run_maker_checker(risky, lax_checker, validator_strict)
    checks.append(("laxiste laisse passer (I3 documente)", trace4["approuve"] is True))
    # Idempotence
    trace5 = run_maker_checker(ok_prop, critic_strict, validator_strict)
    checks.append(("determinisme", json.dumps(trace, sort_keys=True) == json.dumps(trace5, sort_keys=True)))
    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print("%s: %s" % (name, "PASS" if ok else "FAIL"))
    print("SELF-TEST : %s (%d/%d)" % ("PASS" if passed == len(checks) else "FAIL", passed, len(checks)))
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
