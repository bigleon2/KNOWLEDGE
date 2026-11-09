#!/usr/bin/env python3
"""Configuration refactor-guard (Sprint 1, Qwen T14 - hypothesis H09 socle).

Charge et valide la configuration du systeme de refactoring.
Defauts conformes C-SAFE-1 : mode N0 (shadow, lecture seule), allow_push=False,
garde de performance Qwen (latence<2%, CPU<5%, memoire<5%), budget token 20000.

Usage:
    python3 config.py                 # imprime la configuration JSON
    python3 config.py --self-test     # auto-test deterministe (cas limites)
"""

import json
import os
import sys

DEFAULT_CONFIG = {
    "version": "1.0.0",
    "mode": "N0",
    "allow_push": False,
    "shadow_mode": True,
    "recommend_only": True,
    "sandbox_required": True,
    "tests_required": True,
    "policy_gate": True,
    "human_approval_required": True,
    "rollback_required": True,
    "audit_required": True,
    "canary_percentage": 0,
    "performance_guard": {
        "max_added_latency_percent": 2,
        "max_added_latency_p95_percent": 5,
        "max_added_cpu_percent": 5,
        "max_added_memory_percent": 5,
    },
    "limits": {
        "max_token_budget": 20000,
        "max_cpu_percent": 10,
        "max_memory_mb": 300,
    },
    "realtime_guard": {
        "max_cpu_percent": 5,
        "max_memory_mb": 200,
        "low_priority": True,
        "pause_analysis_during_live": True,
    },
}

REQUIRED_SECTIONS = ("performance_guard", "limits", "realtime_guard")


def load_config(path=None):
    """Retourne la configuration par defaut fusionnee avec un fichier optionnel.

    Un fichier JSON partiel ne peut que raffiner les defauts ; les sections
    obligatoires restent garanties presentes dans le resultat.
    """
    config = json.loads(json.dumps(DEFAULT_CONFIG))
    if path:
        if not os.path.isfile(path):
            raise FileNotFoundError(path)
        with open(path, "r", encoding="utf-8") as handle:
            overrides = json.load(handle)
        if not isinstance(overrides, dict):
            raise ValueError("config racine doit etre un objet JSON")
        for key, value in overrides.items():
            if isinstance(value, dict) and isinstance(config.get(key), dict):
                config[key].update(value)
            else:
                config[key] = value
    for section in REQUIRED_SECTIONS:
        if section not in config:
            raise ValueError("section obligatoire absente : %s" % section)
    return config


def main():
    """Point d'entree : impression JSON deterministe ou auto-test."""
    if "--self-test" in sys.argv:
        checks = []
        base = load_config()
        checks.append(("defaut N0", base["mode"] == "N0"))
        checks.append(("allow_push False", base["allow_push"] is False))
        checks.append(("seuil latence 2", base["performance_guard"]["max_added_latency_percent"] == 2))
        checks.append(("budget token 20000", base["limits"]["max_token_budget"] == 20000))
        # Cas limite : override partiel ne supprime pas les sections obligatoires
        with open("/tmp/rg-config-test.json", "w", encoding="utf-8") as handle:
            json.dump({"mode": "N2"}, handle)
        merged = load_config("/tmp/rg-config-test.json")
        checks.append(("merge partiel", merged["mode"] == "N2" and "limits" in merged))
        # Cas limite : fichier absent leve bien une erreur
        try:
            load_config("/tmp/rg-config-inexistant.json")
            checks.append(("fichier absent", False))
        except FileNotFoundError:
            checks.append(("fichier absent", True))
        passed = sum(1 for _, ok in checks if ok)
        for name, ok in checks:
            print("%s: %s" % (name, "PASS" if ok else "FAIL"))
        print("SELF-TEST : %s (%d/%d)" % ("PASS" if passed == len(checks) else "FAIL", passed, len(checks)))
        return 0 if passed == len(checks) else 1
    print(json.dumps(load_config(), indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
