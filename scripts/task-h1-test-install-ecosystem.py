#!/usr/bin/env python3
# PROVENANCE: session web-f90062ce (2026-10-24) — tâche H1, preuve du PATCH
# install-ecosystem.py v2.0.1 (garde idempotence P2 append .gitignore).
# MÉTHODE : test SANDBOX — import du module (main() protégé par __main__),
# monkeypatch de REPO_DIR vers un tmp sous my-project (JAMAIS la cible réelle :
# la P2 du script purge download/ — l'exécution directe sur le dépôt est
# interdite). Rejeu ×3 de phase_p2_purge + assertions. Test lui-même idempotent
# (tmp recréé à l'identique à chaque exécution, verdicts déterministes).
"""H1 — test sandbox rejeu ×N : garde idempotence install-ecosystem v2.0.1."""
import importlib.util
import shutil
import sys
from pathlib import Path

REPO = Path("/home/z/my-project/KNOWLEDGE-repo")
SANDBOX = Path("/home/z/my-project/tmp/h1-test-install-ecosystem")


def charger_module():
    spec = importlib.util.spec_from_file_location("install_ecosystem",
                                                  REPO / "scripts" / "install-ecosystem.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # n'exécute PAS main() (garde __main__)
    return mod


def preparer_sandbox():
    """Sandbox déterministe : recréé à l'identique à chaque exécution du test."""
    if SANDBOX.exists():
        shutil.rmtree(SANDBOX)
    (SANDBOX / "download").mkdir(parents=True)
    (SANDBOX / "download" / "fichier-livrable.txt").write_text("livrable", encoding="utf-8")
    (SANDBOX / "skills" / "_prompts-maitres").mkdir(parents=True)
    (SANDBOX / "skills" / "_prompts-maitres" / "ancien.txt").write_text("obsolète", encoding="utf-8")
    (SANDBOX / ".gitignore").write_text("# existant\nnode_modules/\n", encoding="utf-8")
    return SANDBOX


def main():
    mod = charger_module()
    preparer_sandbox()
    mod.REPO_DIR = SANDBOX  # monkeypatch — la cible réelle n'est JAMAIS touchée

    verrous = []

    # Rejeu 1 : append réel (bloc absent) + purge des cibles
    mod.phase_p2_purge()
    gi1 = (SANDBOX / ".gitignore").read_text(encoding="utf-8")
    n1 = gi1.count("# Caches locaux écosystème")
    verrous.append(("rejeu 1 : bloc ajouté exactement une fois", n1 == 1, f"occurrences={n1}"))
    verrous.append(("rejeu 1 : .gitignore existant préservé", "node_modules/" in gi1, ""))
    verrous.append(("rejeu 1 : download/ purgé", not (SANDBOX / "download").exists(), ""))
    verrous.append(("rejeu 1 : _prompts-maitres purgé",
                    not (SANDBOX / "skills" / "_prompts-maitres").exists(), ""))
    etat_apres_rejeu1 = gi1

    # Rejeus 2 et 3 : no-op attendu (garde v2.0.1 — avant le patch, le bloc se
    # dupliquait à chaque rejeu : n2/n3 auraient été 2/3 → FAIL)
    for i in (2, 3):
        mod.phase_p2_purge()
        gi = (SANDBOX / ".gitignore").read_text(encoding="utf-8")
        n = gi.count("# Caches locaux écosystème")
        verrous.append((f"rejeu {i} : bloc NON dupliqué (garde no-op)", n == 1, f"occurrences={n}"))
        verrous.append((f"rejeu {i} : .gitignore byte-stable vs rejeu 1", gi == etat_apres_rejeu1, ""))

    ok = all(v[1] for v in verrous)
    print("H1 — test sandbox install-ecosystem.py v2.0.1 (rejeu ×3)")
    for nom, passe, info in verrous:
        print(f"  [{'PASS' if passe else 'FAIL'}] {nom} {info}")
    print(f"\nVERDICT : {'PASS — garde idempotence PROUVÉE (rejeu = no-op byte-stable)' if ok else 'FAIL'}")

    # nettoyage : le sandbox est retiré (le test le recrée déterministe au rejeu)
    shutil.rmtree(SANDBOX)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
