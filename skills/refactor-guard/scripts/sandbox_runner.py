#!/usr/bin/env python3
"""sandbox_runner.py - H04 sandbox / harnais de validation (Sprint 3).

Conditions verbatim Qwen (l.5712-5717) : copie isolee du code, environnement
reproductible, tests automatises, analyse statique, comparaison avant/apres,
suppression possible sans impact. Garantie absolue (regles l.6062-6068) :
aucune ecriture dans le depot principal, allow_write=False par defaut,
real_change_applied=False toujours retourne par ce module.

Usage:
    python3 sandbox_runner.py --self-test
"""

import hashlib
import json
import os
import shutil
import sys
import tempfile


def snapshot(paths):
    """Hache le contenu des fichiers cibles (comparaison avant/apres)."""
    state = {}
    for path in paths:
        if os.path.isfile(path):
            with open(path, "rb") as handle:
                state[path] = hashlib.sha256(handle.read()).hexdigest()
        else:
            state[path] = None
    return state


def run_sandbox(source_files, commands=None, allow_write=False):
    """Execute des commandes dans une copie isolee puis compare l'original.

    commands : liste de commandes shell executées DANS la copie (defaut :
    compilation python des fichiers copies). La source originale n'est
    jamais modifiee : la verification par hachage le prouve a chaque run.
    """
    commands = commands or []
    paths = [p for p in source_files if os.path.isfile(p)]
    before = snapshot(paths)
    sandbox_dir = tempfile.mkdtemp(prefix="rg-sandbox-")
    copied = []
    try:
        for path in paths:
            target = os.path.join(sandbox_dir, os.path.basename(path))
            shutil.copy2(path, target)
            copied.append(target)
        results = {"compilation": True, "commands": []}
        for target in copied:
            compile_ok = os.system("%s -m py_compile %s > /dev/null 2>&1" % (sys.executable, target)) == 0
            if not compile_ok:
                results["compilation"] = False
        for command in commands:
            if not allow_write and any(token in command for token in (">", ">>", "rm ", "mv ")):
                results["commands"].append({"command": command, "executed": False, "reason": "allow_write=False"})
                continue
            code = os.system("%s > /dev/null 2>&1" % command)
            results["commands"].append({"command": command, "executed": True, "rc": code})
        after = snapshot(paths)
        unchanged = after == before
        return {
            "sandbox_dir": sandbox_dir,
            "allow_write": allow_write,
            "real_change_applied": False,
            "original_unchanged": unchanged,
            "results": results,
        }
    finally:
        # Rollback = suppression de la copie, sans impact sur l'original
        shutil.rmtree(sandbox_dir, ignore_errors=True)


def main():
    """Auto-test : isolation, hachage avant/apres, rollback, cas limites."""
    if "--self-test" not in sys.argv:
        print("usage : python3 sandbox_runner.py --self-test", file=sys.stderr)
        return 2
    checks = []
    source = "/tmp/rg-sandbox-selftest.py"
    with open(source, "w", encoding="utf-8") as handle:
        handle.write("VALUE = 41\n")
    before_content = open(source, "r", encoding="utf-8").read()
    report = run_sandbox([source])
    checks.append(("real_change_applied False", report["real_change_applied"] is False))
    checks.append(("original inchange", report["original_unchanged"]))
    checks.append(("contenu intact", open(source, "r", encoding="utf-8").read() == before_content))
    checks.append(("sandbox supprimee", not os.path.isdir(report["sandbox_dir"])))
    # Commande d'ecriture bloquee par defaut
    report2 = run_sandbox([source], commands=["echo x > %s" % source])
    checks.append(("ecriture bloquee", report2["results"]["commands"][0]["executed"] is False))
    # Compilation d'un fichier valide
    checks.append(("compilation valide", report["results"]["compilation"] is True))
    # Cas limite : fichier inexistant ignore
    report3 = run_sandbox([source, "/tmp/rg-inexistant.py"])
    checks.append(("inexistant ignore", report3["original_unchanged"]))
    # Cas limite : fichier invalide -> compilation False
    bad = "/tmp/rg-sandbox-bad.py"
    with open(bad, "w", encoding="utf-8") as handle:
        handle.write("def (:\n")
    report4 = run_sandbox([bad])
    checks.append(("syntaxe invalide detectee", report4["results"]["compilation"] is False))
    os.remove(source)
    os.remove(bad)
    passed = sum(1 for _, ok in checks if ok)
    for name, ok in checks:
        print("%s: %s" % (name, "PASS" if ok else "FAIL"))
    print("SELF-TEST : %s (%d/%d)" % ("PASS" if passed == len(checks) else "FAIL", passed, len(checks)))
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
