#!/usr/bin/env python3
"""audit_ledger.py - H09 journal d'audit et tracabilite complete (Sprint 1).

Premiere pierre du socle C-SAFE-1 (Qwen T14 Sprint 1) : chaque refactorisation
est tracee avec les champs prescrits T9 - declencheur, analyse, score de
risque, specification, resultat sandbox, decision, rollback eventuel, auteur.
Ecriture bufferisee en JSONL append-only, jamais de modification d'entree.

Usage:
    python3 audit_ledger.py --self-test
"""

import json
import os
import sys
import time

REQUIRED_FIELDS = (
    "trigger",
    "analysis",
    "risk_score",
    "specification",
    "sandbox_result",
    "decision",
    "rollback",
    "author",
)


class AuditLedger:
    """Journal d'audit append-only avec buffer d'ecriture (Qwen T12)."""

    def __init__(self, path, flush_threshold=8):
        self.path = path
        self.buffer = []
        self.flush_threshold = flush_threshold

    def record(self, entry):
        """Ajoute une entree complete ; leve ValueError si champ manquant."""
        missing = [field for field in REQUIRED_FIELDS if field not in entry]
        if missing:
            raise ValueError("champs obligatoires absents : %s" % ", ".join(missing))
        complete = dict(entry)
        complete.setdefault("timestamp", time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
        self.buffer.append(complete)
        if len(self.buffer) >= self.flush_threshold:
            self.flush()
        return complete

    def flush(self):
        """Ecrit le buffer en append JSONL (idempotent par flush vide)."""
        if not self.buffer:
            return 0
        directory = os.path.dirname(os.path.abspath(self.path))
        if directory and not os.path.isdir(directory):
            os.makedirs(directory)
        with open(self.path, "a", encoding="utf-8") as handle:
            for entry in self.buffer:
                handle.write(json.dumps(entry, ensure_ascii=False, sort_keys=True) + "\n")
        count = len(self.buffer)
        self.buffer = []
        return count

    def entries(self):
        """Relit le journal complet (lecture seule)."""
        if not os.path.isfile(self.path):
            return []
        with open(self.path, "r", encoding="utf-8") as handle:
            return [json.loads(line) for line in handle if line.strip()]


def main():
    """Auto-test : completude, buffer/flush, append-only, cas limites."""
    if "--self-test" not in sys.argv:
        print("usage : python3 audit_ledger.py --self-test", file=sys.stderr)
        return 2
    checks = []
    test_path = "/tmp/rg-audit-selftest.jsonl"
    if os.path.isfile(test_path):
        os.remove(test_path)
    ledger = AuditLedger(test_path, flush_threshold=2)
    base = {
        "trigger": "manual",
        "analysis": "test",
        "risk_score": 3,
        "specification": {"goal": "x"},
        "sandbox_result": {"real_change_applied": False},
        "decision": "RECOMMEND_ONLY",
        "rollback": "none",
        "author": "self-test",
    }
    first = ledger.record(base)
    checks.append(("champs par defaut timestamp", "timestamp" in first))
    # Cas limite : entree incomplete refusee
    try:
        ledger.record({"trigger": "x"})
        checks.append(("entree incomplete refusee", False))
    except ValueError:
        checks.append(("entree incomplete refusee", True))
    ledger.record(base)
    checks.append(("buffer auto-flush 2", os.path.isfile(test_path) and len(ledger.entries()) == 2))
    ledger.record(base)
    ledger.flush()
    checks.append(("flush residu", len(ledger.entries()) == 3))
    checks.append(("flush vide inoffensif", ledger.flush() == 0))
    # Idempotence : rejeu de lecture a l'identique
    snapshot = json.dumps(ledger.entries(), sort_keys=True)
    checks.append(("rejeu lecture identique", snapshot == json.dumps(ledger.entries(), sort_keys=True)))
    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print("%s: %s" % (name, "PASS" if ok else "FAIL"))
    print("SELF-TEST : %s (%d/%d)" % ("PASS" if passed == len(checks) else "FAIL", passed, len(checks)))
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
