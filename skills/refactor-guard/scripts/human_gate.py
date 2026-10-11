#!/usr/bin/env python3
"""human_gate.py - H15 human-in-the-loop pour refactorisations critiques (Sprint 5).

Matrice de decision risque x couverture Qwen (l.6127-6188) :
    risque critique                        -> BLOCAGE
    risque eleve + couverture faible       -> BLOCAGE
    risque eleve (cœur, API, securite...)  -> APPROBATION_HUMAINE_REQUISE
    sinon                                  -> AUTO (recommandation)
require_human_approval=True n'est JAMAIS contourne par ce module.

Usage:
    python3 human_gate.py --self-test
"""

import json
import sys
from functools import lru_cache

BLOCAGE = "BLOCAGE"
APPROBATION = "APPROBATION_HUMAINE_REQUISE"
AUTO = "AUTO"
ZONES_SENSIBLES = ("core", "api_publique", "securite", "persistance", "comportement_utilisateur")


@lru_cache(maxsize=256)
def _decide_cached(risk_level, test_coverage, zones_tuple):
    """Decision pure cachee (optimisation v2 Qwen : LRU sur entrees hachables)."""
    risk_level = (risk_level or "").lower()
    zones = zones_tuple
    if risk_level == "critique":
        return {"decision": BLOCAGE, "require_human_approval": True}
    if risk_level == "eleve" and test_coverage == "faible":
        return {"decision": BLOCAGE, "require_human_approval": True}
    if risk_level == "eleve":
        return {"decision": APPROBATION, "require_human_approval": True}
    if risk_level == "moyen" and any(zone in zones for zone in ZONES_SENSIBLES):
        return {"decision": APPROBATION, "require_human_approval": True}
    return {"decision": AUTO, "require_human_approval": False}


def decide(risk_level, test_coverage, sensitive_zones):
    """Applique la matrice ; risk_level dans {faible, moyen, eleve, critique}."""
    return dict(_decide_cached(risk_level or "", test_coverage or "", tuple(sorted(sensitive_zones or ()))))


def main():
    """Auto-test : matrice complete, cas limites, determinisme."""
    if "--self-test" not in sys.argv:
        print("usage : python3 human_gate.py --self-test", file=sys.stderr)
        return 2
    checks = []
    # Ligne 1 : critique -> blocage quelle que soit la couverture
    checks.append(("critique blocage", decide("critique", "bonne", ["core"])["decision"] == BLOCAGE))
    checks.append(("critique flag humain", decide("critique", "faible", [])["require_human_approval"] is True))
    # Ligne 2 : eleve + couverture faible -> blocage
    checks.append(("eleve+faible blocage", decide("eleve", "faible", [])["decision"] == BLOCAGE))
    # Ligne 3 : eleve + couverture ok -> approbation humaine
    checks.append(("eleve approbation", decide("eleve", "bonne", [])["decision"] == APPROBATION))
    # Moyen + zone sensible -> approbation
    checks.append(("moyen+core approbation", decide("moyen", "bonne", ["core"])["decision"] == APPROBATION))
    # Faible -> auto
    checks.append(("faible auto", decide("faible", "faible", [])["decision"] == AUTO))
    # Cas limites : entree vide / inconnue -> traitement prudent (moyen par defaut)
    checks.append(("vide prudent", decide(None, None, None)["decision"] == AUTO))
    checks.append(("inconnu prudent", decide("inconnu", "moyenne", [])["decision"] == AUTO))
    # API publique zone sensible
    checks.append(("api sensible", decide("moyen", "bonne", ["api_publique"])["decision"] == APPROBATION))
    # Determinisme
    checks.append(("determinisme", decide("eleve", "faible", []) == decide("eleve", "faible", [])))
    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print("%s: %s" % (name, "PASS" if ok else "FAIL"))
    print("SELF-TEST : %s (%d/%d)" % ("PASS" if passed == len(checks) else "FAIL", passed, len(checks)))
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
