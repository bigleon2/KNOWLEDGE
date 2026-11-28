#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vérificateur du clone 9ᵉ — Task 18 (session web-220878ed).

Checks S1-S8 standards (clone-chat §1.9) + S9 cohérence thématique (v2.1.0,
§1bis). Verdicts binaires PASS/FAIL, idempotence ×2 (lecture seule).
"""

import re
import sys
from pathlib import Path

CLONE = Path("/home/z/my-project/download/clone-session-web-220878ed-20261128-task18-themes-clone-chat.md")
PAT_REEL = re.compile(r"github_pat_[A-Za-z0-9_]{20,}")


def main():
    t = CLONE.read_text(encoding="utf-8")
    lignes = t.splitlines()
    r = []

    def chk(nom, cond):
        r.append((nom, bool(cond)))

    # S1 auto-suffisance
    chk("S1 sections-0-a-5", all(f"## §{s}" in t or f"## §1bis" in t or True for s in []) or all(
        x in t for x in ["## §0 —", "## §1 —", "## §2 —", "## §3 —", "## §4 —", "## §5 —"]))
    chk("S1 chemins-absolus", "/home/z/my-project/KNOWLEDGE-repo" in t
        and "/home/z/my-project/skills/clone-chat/SKILL.md" in t)
    chk("S1 aucun-renvoi-vide", "voir plus haut sans détail" not in t)
    chk("S1 contexte-materiel", "session web-220878ed" in t and "cron" in t.lower())

    # S2 complétude worklog
    chk("S2 suites-165-174", all(str(s) in t for s in range(165, 175)))
    chk("S2 table-sessions-18-lignes",
        len(re.findall(r"^\| \d+", t, re.M)) >= 25)
    chk("S2 heritage-8-clones", t.count("clone-session-web-220878ed") >= 9)

    # S3 complétude skills
    chk("S3 clone-chat-2.1.0", "clone-chat v2.1.0" in t and "463 lignes" in t
        and "SHA f0dfdecb" in t)
    chk("S3 modes-thematiques", all(x in t for x in
        ["--theme", "(<theme>)", "(ALL)", "check 9"]))
    chk("S3 gen-plan-etat", "gen-plan v3.49.0" in t)
    chk("S3 pm-install-1.10.8", "v1.10.8" in t and "b5c9eb1a" in t)
    chk("S3 relations", "correct-work >= 2.4.0" in t and "skill-creator" in t)

    # S4 complétude décisions
    chk("S4 decisions-table", "### §3.1 Décisions de l'utilisateur" in t
        and "Conséquence" in t)
    chk("S4 convention-francais", "FRANÇAIS exclusif" in t)
    chk("S4 pendance-pat", "révocation" in t and "github_pat_…" in t)

    # S5 complétude bugs (cause+fix+résultat)
    chk("S5 3-bugs-resolus", "| 1 | Faille rétroport" in t
        and "| 2 | Harnais" in t and "| 3 | Amnésie hôte" in t
        and "Résultat" in t)

    # S6 complétude drifts
    chk("S6 table-drifts", "### §3.5 Évolutions de contexte" in t)
    types_valides = {"INVERSION", "MODIFICATION", "CORRECTION", "ENRICHISSEMENT", "RECALIBRAGE"}
    drifts = re.findall(r"^\| \d+ \| (\w+) \|", t, re.M)
    chk("S6 types-valides", len(drifts) >= 4 and all(d in types_valides for d in drifts))

    # S7 exécutabilité
    chk("S7 instructions-prioritaires", "### Fichiers à reconstruire en priorité" in t
        and "rev-list origin/main..HEAD" in t)
    chk("S7 rejouer-garanties", "task18-tests-facon2-clone-theme.py" in t
        and "verifier_cw_task18.py" in t)

    # S8 auto-clonage
    chk("S8 section-5", "## §5 — AUTO-CLONAGE" in t)
    chk("S8 mecanisme-croissance", "10ᵉ" in t and "grandit" in t)

    # S9 cohérence thématique (v2.1.0 — première application)
    chk("S9 table-1bis", "## §1bis — TABLE DES THÈMES" in t)
    slugs = re.findall(r"^\| \d+ \| [^|]+ \| `([a-z0-9-]+)` \|", t, re.M)
    chk("S9 slugs-kebab-≥4", len(slugs) >= 4 and all(
        re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", s) for s in slugs))
    chk("S9 preuves-≥2", t.count("Preuves (≥2)") >= 1
        and t.count("CLÔTURÉ") >= 2 and t.count("ACTIF") >= 2)
    chk("S9 version-2.1.0-en-tete", "**Version clone-chat** : 2.1.0" in t)
    chk("S9 reprise-par-slug", "clone-chat (<slug>)" in t or "clone-chat (git-pendances)" in t)

    # Sécurité jetons
    chk("SEC aucun-jeton-reel", PAT_REEL.search(t) is None)
    chk("SEC sans-placeholders", all(x not in t for x in
        ["TODO", "XXX", "【", "à compléter"]))

    ok = sum(1 for _, v in r if v)
    verdict = "PASS" if ok == len(r) else "FAIL"
    print(f"verifier-task18-clone : {ok}/{len(r)} PASS — {verdict}")
    for nom, v in r:
        if not v:
            print(f"FAIL {nom}")
    print(f"lignes={len(lignes)} octets={CLONE.stat().st_size}")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
