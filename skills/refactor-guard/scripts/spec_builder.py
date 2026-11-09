#!/usr/bin/env python3
"""spec_builder.py - H07 specification formelle de refactorisation (Sprint 4).

Contenu minimal prescrit Qwen T9 (l.5661-5679) : objectif, perimetre, fichiers
concernes, comportement a preserver, tests requis, contraintes, criteres de
validation, plan propose, rollback prevu. Une specification incomplete est
rejetee (verdict REJET, jamais de spec approximative).

Usage:
    python3 spec_builder.py --self-test
"""

import json
import sys

REQUIRED_SECTIONS = (
    "objectif",
    "perimetre",
    "fichiers",
    "comportement_preserve",
    "tests_requis",
    "contraintes",
    "criteres_validation",
    "plan_propose",
    "rollback_prevu",
)


def build_spec(goal, scope, files, preserve, tests, constraints, criteria, plan, rollback):
    """Assemble une specification ; refuse toute section vide (honestete)."""
    spec = {
        "objectif": goal,
        "perimetre": scope,
        "fichiers": files,
        "comportement_preserve": preserve,
        "tests_requis": tests,
        "contraintes": constraints,
        "criteres_validation": criteria,
        "plan_propose": plan,
        "rollback_prevu": rollback,
    }
    verdict, missing = validate_spec(spec)
    if verdict != "VALIDE":
        return spec, verdict, missing
    return spec, verdict, []


def validate_spec(spec):
    """Verifie completude et non-vacuite de chaque section obligatoire."""
    missing = [key for key in REQUIRED_SECTIONS if key not in spec]
    empty = [
        key
        for key in REQUIRED_SECTIONS
        if key in spec and (spec[key] is None or (hasattr(spec[key], "__len__") and len(spec[key]) == 0))
    ]
    missing.extend(empty)
    return ("VALIDE" if not missing else "REJET"), missing


def to_recommend_only(spec):
    """Format JSON recommend_only Qwen (l.5981-5997) : spec.goal/preserve/acceptance."""
    return {
        "mode": "recommend_only",
        "spec": {
            "goal": spec.get("objectif"),
            "preserve": spec.get("comportement_preserve"),
            "acceptance_criteria": spec.get("criteres_validation"),
        },
    }


def main():
    """Auto-test : completude, rejet des sections vides, format recommend_only."""
    if "--self-test" not in sys.argv:
        print("usage : python3 spec_builder.py --self-test", file=sys.stderr)
        return 2
    checks = []
    spec, verdict, missing = build_spec(
        "extraire module X",
        "core/",
        ["core/x.py"],
        ["API publique inchangee"],
        ["tests/test_x.py"],
        ["pas de nouvelle dependance"],
        ["tests verts", "0 cycle"],
        ["etape 1", "etape 2"],
        ["git revert"],
    )
    checks.append(("spec complete VALIDE", verdict == "VALIDE" and missing == []))
    # Cas limite : section vide -> REJET (perimetre non vide : 8 sections manquantes)
    spec_vide, verdict_vide, missing_vide = build_spec(
        "", "core/", [], None, [], [], [], [], "")
    attendus = set(REQUIRED_SECTIONS) - {"perimetre"}
    checks.append(("spec vide REJET 8", verdict_vide == "REJET" and set(missing_vide) == attendus))
    # Cas limite : spec partielle -> REJET avec liste precise
    partiel = {"objectif": "x", "perimetre": "core/"}
    verdict_p, missing_p = validate_spec(partiel)
    checks.append(("spec partielle 7 manquants", verdict_p == "REJET" and len(missing_p) == 7))
    reco = to_recommend_only(spec)
    checks.append(("format recommend_only", reco["mode"] == "recommend_only" and reco["spec"]["goal"] == "extraire module X"))
    # Idempotence : meme entree -> meme sortie
    spec2, verdict2, _ = build_spec(
        "extraire module X", "core/", ["core/x.py"], ["API publique inchangee"],
        ["tests/test_x.py"], ["pas de nouvelle dependance"], ["tests verts", "0 cycle"],
        ["etape 1", "etape 2"], ["git revert"])
    checks.append(("determinisme", json.dumps(spec, sort_keys=True) == json.dumps(spec2, sort_keys=True) and verdict2 == "VALIDE"))
    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print("%s: %s" % (name, "PASS" if ok else "FAIL"))
    print("SELF-TEST : %s (%d/%d)" % ("PASS" if passed == len(checks) else "FAIL", passed, len(checks)))
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
