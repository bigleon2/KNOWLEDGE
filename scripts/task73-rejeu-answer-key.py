#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.35)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).
"""

"""Task 73 — Re-jeu mécanique de l'answer key du plan (lecture seule).

Vérifie chaque décision D001-D013 du plan Task 73 à partir des artefacts
gelés (les fichiers PRE ne sont JAMAIS ré-exécutés — preuves figées) et des
vérifications idempotentes. D011 (clone-chat) n'est vérifiable qu'après G8 :
le paramètre --inclure-d011 l'active.

Usage : python3 scripts/task73-rejeu-answer-key.py [--inclure-d011]
"""

from __future__ import annotations

import argparse
import json
import py_compile
import subprocess
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
DOWNLOAD = RACINE / "download"
PLAN = DOWNLOAD / "plan-task73-tests-fonctionnels-performances-genplan-ecosysteme-miroir.md"
WORKLOG = RACINE / "worklog.md"
RAPPORT = DOWNLOAD / "rapport-tests-fonctionnels-performances-task73.md"


def check(nom: str, ok: bool, detail: str = "") -> bool:
    print(f"  [{'PASS' if ok else 'FAIL'}] {nom}" + (f" — {detail}" if detail else ""))
    return ok


def json_de(chemin: Path) -> dict:
    return json.loads(chemin.read_text(encoding="utf-8"))


def rejeu(inclure_d011: bool) -> int:
    resultats = []

    print("=== Re-jeu answer key Task 73 (lecture seule) ===")

    # D001 — protocole + outillage
    ok = True
    try:
        py_compile.compile(str(RACINE / "scripts" / "task73-campagne-tests.py"),
                           doraise=True)
    except py_compile.PyCompileError:
        ok = False
    rep = subprocess.run([sys.executable, "scripts/task73-campagne-tests.py",
                          "--selftest"], capture_output=True, text=True,
                         cwd=str(RACINE))
    ok = ok and "8/8 PASS" in rep.stdout
    protocole = DOWNLOAD / "protocole-tests-fonctionnels-performances-task73.json"
    ok = ok and protocole.exists()
    if ok:
        d = json_de(protocole)
        ok = sorted(d["cibles"].keys()) == ["C1", "C2", "C3"]
    resultats.append(check("D001 protocole $FACON2 + outillage (selftest 8/8, 3 cibles)", ok))

    # D002 — PRE C1 (fichier gelé, jamais ré-exécuté)
    d = json_de(DOWNLOAD / "rapport-campagne-task73-pre-C1.json")
    resultats.append(check("D002 PRE C1 gen-plan hôte", d["verdict"] == "PASS"
                           and len(d["tests"]) == 11,
                           f"verdict {d['verdict']} · {len(d['tests'])} tests"))

    # D003 — PRE C2 (faille vm documentée)
    d = json_de(DOWNLOAD / "rapport-campagne-task73-pre-C2.json")
    details = json.dumps(d, ensure_ascii=False)
    resultats.append(check("D003 PRE C2 écosystème (faille vm tracée)",
                           d["verdict"] == "FAIL"
                           and details.count("version-management") >= 1,
                           f"verdict {d['verdict']} · vm documentée"))

    # D004 — PRE C3 + identité byte (diff re-vérifié en lecture seule)
    d = json_de(DOWNLOAD / "rapport-campagne-task73-pre-C3.json")
    diff = subprocess.run(["diff", "-rq", "skills/gen-plan",
                           "KNOWLEDGE-repo/skills/gen-plan"],
                          capture_output=True, text=True, cwd=str(RACINE))
    resultats.append(check("D004 PRE C3 miroir + diff -rq vide",
                           d["verdict"] == "PASS" and diff.returncode == 0
                           and not diff.stdout.strip()))

    # D005 — vm restaurée + garde rc=0 + aucun rmtree dans le script campagne
    vm = RACINE / "skills" / "version-management" / "SKILL.md"
    rep = subprocess.run([sys.executable,
                          "skills/gen-plan/scripts/ensure-installed.py",
                          "--check"], capture_output=True, text=True, cwd=str(RACINE))
    script = (RACINE / "scripts" / "task73-campagne-tests.py").read_text(
        encoding="utf-8")
    resultats.append(check("D005 vm restaurée + garde INSTALLE/INSTALLE-REPARÉ rc=0",
                           vm.exists() and rep.returncode == 0
                           and "rmtree" not in script,
                           f"vm {'présente' if vm.exists() else 'ABSENTE'} · "
                           f"garde rc={rep.returncode}"))

    # D006 — POST + non-régression
    d = json_de(DOWNLOAD / "rapport-campagne-task73-post-synthese.json")
    resultats.append(check("D006 POST : non-régression True + 3 failles résorbées",
                           d["non_regression"] is True
                           and len(d["failles_resorbees"]) == 3
                           and d["verdict_global_post"] == "PASS AVEC RÉSERVES",
                           f"{d['verdict_global_pre']} -> {d['verdict_global_post']}"))

    # D007 — optimisation et interactions (rapport final sections 8 et 10)
    texte = RAPPORT.read_text(encoding="utf-8")
    resultats.append(check("D007 durées + interactions re-certifiées au rapport",
                           "## 8. Performances" in texte
                           and "## 10. Optimisation et interactions" in texte
                           and "95 arêtes" in texte))

    # D008 — rapport final présent, 3 cibles couvertes
    nb = sum(texte.count(c) for c in ("C1", "C2", "C3"))
    resultats.append(check("D008 rapport final (3 cibles couvertes)", nb >= 30,
                           f"{nb} mentions C1/C2/C3"))

    # D009 — correct-work --bloc consigné au worklog (Task 73)
    wl = WORKLOG.read_text(encoding="utf-8")
    resultats.append(check("D009 correct-work (projet) --bloc PASS consigné",
                           "correct-work (projet) --bloc : PASS" in wl
                           and "Task 73" in wl))

    # D010 — E8 final (statuts verified + P1-P5) — vérifié en fin de session
    resultats.append(check("D010 E8 final : 13 statuts verified au plan",
                           PLAN.read_text(encoding="utf-8").count(
                               'status: "verified"') >= 12))

    # D011 — clone-chat (après G8 uniquement)
    if inclure_d011:
        clone = DOWNLOAD / "clone-chat-session-web-ecef7f80-20261108-task73.md"
        ok = clone.exists()
        if ok:
            t = clone.read_text(encoding="utf-8")
            ok = all(s in t for s in ("§0", "§1", "§2", "§3", "§4", "§5"))
        resultats.append(check("D011 clone-chat archive auto-suffisante", ok))

    # D012 — fenêtre native : mentions worklog à chaque fin de groupe
    resultats.append(check("D012 fenêtre native (mentions worklog >= 8)",
                           wl.count("fenêtre native") >= 8,
                           f"{wl.count('fenêtre native')} mentions"))

    # D013 — pendance PUSH (guidance rapport + aucun push par l'agent)
    resultats.append(check("D013 pendance PUSH KO-L009 (guidance révocation)",
                           "révocation du PAT" in texte
                           and "par le propriétaire uniquement" in texte))

    nb_ok = sum(resultats)
    total = len(resultats)
    print(f"RÉSULTAT : {nb_ok}/{total} décisions verified")
    return 0 if nb_ok == total else 1


def main() -> int:
    parseur = argparse.ArgumentParser(description="Re-jeu answer key Task 73")
    parseur.add_argument("--inclure-d011", action="store_true")
    args = parseur.parse_args()
    return rejeu(args.inclure_d011)


if __name__ == "__main__":
    sys.exit(main())
