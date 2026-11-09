#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
risk_score.py — Scoring de risque de refactorisation (H14) — refactor-guard v1.0.0.

Design hérité du projet « Skill Refactorisation Plan » (Qwen T7/T9) :
  complexité > 20  -> +3
  couplage   > 10  -> +3
  couverture < 0.5 -> +4
  module critique  -> +5
Niveaux : >= 10 critique | >= 6 moyen | < 6 faible.
Décision : >= 10 block|require_approval ; 6-9 sandbox_then_plan ; < 6 allow_simple.

Stdlib uniquement (N3), déterministe (PYTHONHASHSEED-independent — aucune
itération sur set ordonné), CLI JSON, self-test intégré (--self-test).
Usage :
    echo '{"metrics": {...}}' | python3 risk_score.py
    python3 risk_score.py --input entree.json [--output sortie.json]
    python3 risk_score.py --self-test
"""
import json
import sys

SEUILS = {"complexite": 20, "couplage": 10, "couverture": 0.5}
PONDERATIONS = {"complexite": 3, "couplage": 3, "couverture": 4, "critique": 5}
NIVEAUX = {"critique": 10, "moyen": 6}

def compute_risk(metrics: dict, critique: bool = False) -> dict:
    """Score pondéré déterministe à partir des métriques du trigger (format §2.4)."""
    complexite = float(metrics.get("cyclomatic_complexity", 0) or 0)
    couplage = float(metrics.get("coupling", 0) or 0)
    couverture = float(metrics.get("test_coverage", 1) if metrics.get("test_coverage") is not None else 1)
    score = 0
    facteurs = []
    if complexite > SEUILS["complexite"]:
        score += PONDERATIONS["complexite"]
        facteurs.append(f"complexité {complexite:g} > {SEUILS['complexite']} (+3)")
    if couplage > SEUILS["couplage"]:
        score += PONDERATIONS["couplage"]
        facteurs.append(f"couplage {couplage:g} > {SEUILS['couplage']} (+3)")
    if couverture < SEUILS["couverture"]:
        score += PONDERATIONS["couverture"]
        facteurs.append(f"couverture {couverture:g} < {SEUILS['couverture']} (+4)")
    if critique:
        score += PONDERATIONS["critique"]
        facteurs.append("module critique (+5)")
    niveau = "critique" if score >= NIVEAUX["critique"] else ("moyen" if score >= NIVEAUX["moyen"] else "faible")
    decision = {"critique": "block", "moyen": "sandbox_then_plan", "faible": "allow_simple"}[niveau]
    if critique and decision == "allow_simple":
        # Plancher zéro-régression : un module critique ne JAMAIS en allow_simple
        # (score inchangé — fidèle au design Qwen T7 ; décision relevée, adaptation documentée)
        decision = "sandbox_then_plan"
        facteurs.append("module critique — plancher décision : sandbox_then_plan (zéro-régression)")
    return {
        "risk_score": score,
        "risk_level": niveau,
        "decision": decision,
        "facteurs": facteurs,
        "exigences": {
            "critique": "validation humaine OBLIGATOIRE (N4) — sandbox + spec + maker-checker + rollback testé",
            "moyen": "spec + sandbox + maker-checker (N3), puis N4 pour application",
            "faible": "refactorisation locale simple contrôlée par tests (N2→N3)",
        }[niveau],
    }

def _self_test() -> int:
    """7 vérifications déterministes — rc 0 attendu."""
    cas = [
        # (metrics, critique, score attendu, niveau attendu)
        ({"cyclomatic_complexity": 8, "coupling": 4, "test_coverage": 0.8}, False, 0, "faible", "allow_simple"),
        ({"cyclomatic_complexity": 25, "coupling": 4, "test_coverage": 0.8}, False, 3, "faible", "allow_simple"),
        ({"cyclomatic_complexity": 25, "coupling": 14, "test_coverage": 0.8}, False, 6, "moyen", "sandbox_then_plan"),
        ({"cyclomatic_complexity": 25, "coupling": 14, "test_coverage": 0.3}, False, 10, "critique", "block"),
        ({"cyclomatic_complexity": 8, "coupling": 4, "test_coverage": 0.8}, True, 5, "faible", "sandbox_then_plan"),
        ({"cyclomatic_complexity": 30, "coupling": 20, "test_coverage": 0.1}, True, 15, "critique", "block"),
        ({"cyclomatic_complexity": 20, "coupling": 10, "test_coverage": 0.5}, False, 0, "faible", "allow_simple"),
    ]
    ok = True
    for i, (m, crit, s_att, n_att, d_att) in enumerate(cas, 1):
        r = compute_risk(m, crit)
        bon = r["risk_score"] == s_att and r["risk_level"] == n_att and r["decision"] == d_att
        print(f"T{i}: score={r['risk_score']} niveau={r['risk_level']} decision={r['decision']} "
              f"[{'PASS' if bon else 'FAIL'}] (attendu {s_att}/{n_att}/{d_att})")
        ok = ok and bon
    # T8 : décision critique cohérente avec le niveau critique (test complémentaire)
    r = compute_risk({"cyclomatic_complexity": 30, "coupling": 20, "test_coverage": 0.1}, True)
    bon = r["decision"] == "block" and r["risk_level"] == "critique"
    print(f"T8: decision={r['decision']} [{'PASS' if bon else 'FAIL'}]")
    ok = ok and bon
    print("SELF-TEST :", "PASS (8/8)" if ok else "FAIL")
    return 0 if ok else 1

def main() -> int:
    argv = sys.argv[1:]
    if "--self-test" in argv:
        return _self_test()
    donnee = None
    if "--input" in argv:
        chemin = argv[argv.index("--input") + 1]
        donnee = json.loads(open(chemin, encoding="utf-8").read())
    else:
        donnee = json.loads(sys.stdin.read() or "{}")
    metrics = donnee.get("metrics", {})
    critique = bool(donnee.get("severity") == "critical" or donnee.get("critique"))
    resultat = compute_risk(metrics, critique)
    resultat["target"] = donnee.get("target")
    resultat["trigger"] = donnee.get("trigger")
    sortie = json.dumps(resultat, ensure_ascii=False, indent=2)
    if "--output" in argv:
        open(argv[argv.index("--output") + 1], "w", encoding="utf-8").write(sortie + "\n")
    else:
        print(sortie)
    return 0

if __name__ == "__main__":
    sys.exit(main())
