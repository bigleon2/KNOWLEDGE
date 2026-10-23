#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.11)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

# PROVENANCE: Task 24 (2026-10-23, session web-fdf5963c) — résolution des 4 conflits
# de rebase publication-task24 sur origin/main (session photos web-38713acd).
# Règles : KB = union (entrées iphone amont + alias-eco local, statuts réattribués) ;
# README @historique = union (lignes photos/ + @Alias/) ; worklog = corps compacté amont
# + entrées locales Task 18/20/22 ré-appendées ; manifeste = côté local (régénéré par
# l'arbitre au run vert). Garde : 0 marqueur résiduel, assertions d'intégrité.
import json
import sys
from pathlib import Path

BASE = Path("/home/z/my-project/KNOWLEDGE-repo")


def resolve(path, mode):
    """mode: union | ours | theirs | kb_union | worklog"""
    p = BASE / path
    lines = p.read_text(encoding="utf-8").splitlines(keepends=True)
    out, i, n, regions = [], 0, len(lines), 0
    while i < n:
        ln = lines[i]
        if ln.rstrip("\r\n").startswith("<<<<<<<"):
            regions += 1
            i += 1
            head = []
            while lines[i].rstrip("\r\n") != "=======":
                head.append(lines[i]); i += 1
            i += 1
            theirs = []
            while not lines[i].rstrip("\r\n").startswith(">>>>>>>"):
                theirs.append(lines[i]); i += 1
            i += 1  # saute le marqueur de fin
            if mode == "union":
                out.extend(head + theirs)
            elif mode == "ours":
                out.extend(head)
            elif mode == "theirs":
                out.extend(theirs)
            elif mode == "kb_union":
                # iphone17 (côté amont) reçoit son Statut, puis l'entrée alias-eco locale ;
                # la ligne commune « - **Statut** : stable » qui suit devient celle d'alias-eco.
                assert head and "à suivre)" in head[-1], "KB: queue inattendue du côté amont"
                out.extend(head + ["- **Statut** : stable\n", "\n"] + theirs)
            elif mode == "worklog":
                # corps compacté amont + bloc local à partir de « Task ID: 18 » (--- inclus)
                idx = next(k for k, l in enumerate(theirs)
                           if l.strip() == "Task ID: 18")
                start = idx - 1 if idx > 0 and theirs[idx - 1].strip() == "---" else idx
                bloc = theirs[start:]
                if bloc[0].strip() != "---":
                    bloc = ["---\n"] + bloc
                out.extend(head + ["\n"] + bloc)
        else:
            out.append(ln); i += 1
    p.write_text("".join(out), encoding="utf-8")
    return regions


def main():
    total = 0
    total += resolve("skills/KNOWLEDGE.md", "kb_union")
    total += resolve("skills/@historique/README.md", "union")
    total += resolve("worklog.md", "worklog")
    total += resolve("scripts/ecosysteme-integrity.json", "theirs")

    # Garde 1 : plus aucun marqueur de conflit
    for f in ("skills/KNOWLEDGE.md", "skills/@historique/README.md",
              "worklog.md", "scripts/ecosysteme-integrity.json"):
        t = (BASE / f).read_text(encoding="utf-8")
        assert "<<<<<<<" not in t and ">>>>>>>" not in t, f"{f}: marqueur résiduel"
        assert "\n=======\n" not in t, f"{f}: séparateur résiduel"

    # Garde 2 : KB — les deux côtés présents, uniques
    kb = (BASE / "skills/KNOWLEDGE.md").read_text(encoding="utf-8")
    for h in ("## iphone19 v0.11.0", "## iphone18 v1.1.0", "## iphone17 v1.1.0",
              "## alias-eco v1.0.0"):
        assert kb.count(h) == 1, f"KB: {h} x{kb.count(h)} (attendu 1)"
    # Statuts réattribués : iphone17 ... à suivre)\n- **Statut** : stable\n\n## alias-eco
    assert "à suivre)\n- **Statut** : stable\n\n## alias-eco v1.0.0" in kb, \
        "KB: statut iphone17 mal réattribué"

    # Garde 3 : worklog — amont compacté + entrées locales 18/20/22
    wl = (BASE / "worklog.md").read_text(encoding="utf-8")
    assert "- MISSION TASK 48 TERMINÉE." in wl, "worklog: fin amont perdue"
    for t in ("Task ID: 18", "Task ID: 20", "Task ID: 22"):
        assert t in wl, f"worklog: entrée {t} perdue"
    assert wl.count("Task ID: 18") == 1, "worklog: Task 18 dupliqué"

    # Garde 4 : manifeste JSON valide (régénéré par l'arbitre au run vert)
    json.loads((BASE / "scripts/ecosysteme-integrity.json").read_text(encoding="utf-8"))

    print(f"Conflits résolus : {total} régions (KB kb_union, README union, worklog, manifeste theirs)")
    print("Gardes : 0 marqueur résiduel ; KB iphone×3 + alias-eco ; worklog amont+18/20/22 ; JSON valide.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
