#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.46)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).
Référence canonique : « mon skill X » = forme installée skills/X/, JAMAIS le PM.
"""

"""Task 114 — Batterie de tests fonctionnels (F) et de performances (P).

Directive propriétaire trace 1a2025197d2a0e9d (« génère et exécute des tests
fonctionnels et de performances sur ce que tu as modifié ou créé dans cette demande »)
+ trace 1a2025ce4a6ed095 (rappel permanent langue).

Périmètres testés : routage-skills-agents.py (nouveau), gen-plan v3.47.0 (§0 rappel
langue + É5-ROUTAGE + §1.17 + cascade), ensure-installed.py (garde réinjection),
arbitres non-régression, livrable d'analyse.

Sortie : download/rapport-task114-tests-fp.json — codes retour : 0 = PASS, 1 = FAIL.
Idempotent (lecture seule sauf sortie rapport), stdlib uniquement.
"""
import json
import subprocess
import sys
import time
from pathlib import Path

RACINE = Path("/home/z/my-project")
SKILL = RACINE / "skills/gen-plan/SKILL.md"
SCRIPT = RACINE / "skills/gen-plan/scripts/routage-skills-agents.py"
ENSURE = RACINE / "skills/gen-plan/scripts/ensure-installed.py"
KB = RACINE / "skills/KNOWLEDGE.md"
ANALYSE = RACINE / "download/analyse-routage-decisionnel-task114.md"
RAPPORT = RACINE / "download/rapport-task114-tests-fp.json"
WORKLOG = RACINE / "worklog.md"

tests = []


def F(nom, condition, detail=""):
    tests.append({"type": "F", "nom": nom, "verdict": "PASS" if condition else "FAIL",
                  "detail": detail})
    return bool(condition)


def routage(tache, fmt="json"):
    return subprocess.run([sys.executable, str(SCRIPT), "--tache", tache, "--format", fmt],
                          capture_output=True, text=True, timeout=30)


def main():
    # F1 — selftest script ×2 arbres
    for arbre, p in (("hôte", SCRIPT),
                     ("dépôt", RACINE / "KNOWLEDGE-repo/skills/gen-plan/scripts/routage-skills-agents.py")):
        r = subprocess.run([sys.executable, str(p), "--selftest"], capture_output=True, text=True)
        F(f"F1_selftest_{arbre}", "SELFTEST 9/9" in r.stdout, r.stdout.strip().splitlines()[-1] if r.stdout else r.stderr[-120:])
    # F2 — parité byte ×2 arbres
    F("F2_parite_script", SCRIPT.read_bytes() == (RACINE / "KNOWLEDGE-repo/skills/gen-plan/scripts/routage-skills-agents.py").read_bytes())
    # F3 — scénario traduction
    r = routage("traduire le document pdf en français")
    d = json.loads(r.stdout)
    F("F3_traduction_top", any(x["nom"] in ("traduction-zh-fr", "pdf", "pdf-llm") for x in d["skills_recommandes"][:3]),
      ", ".join(x["nom"] for x in d["skills_recommandes"][:3]))
    # F4 — porte agents SIMPLE
    d4 = json.loads(routage("quelle heure est-il ?").stdout)
    F("F4_gate_simple", d4["verdict_complexite"] == "SIMPLE" and d4["agents_recommandes"] == [] and d4["portegardes_agents"],
      d4.get("portegardes_agents") or "")
    # F5 — verdict COMPLEXE + agents
    d5 = json.loads(routage("génère un rapport pdf et une présentation pptx puis pousse sur le dépôt git avec la clé").stdout)
    F("F5_complexe_agents", d5["verdict_complexite"] == "COMPLEXE" and isinstance(d5["agents_recommandes"], list),
      f"{d5['criteres_remplis']}/5 critères, {len(d5['agents_recommandes'])} agent(s)")
    # F6 — idempotence ×2 (sortie sémantiquement identique — hors champ volatile duree_ms)
    a = routage("audit des skills du projet et corrections")
    b = routage("audit des skills du projet et corrections")
    da, db = json.loads(a.stdout), json.loads(b.stdout)
    da["metadonnees"].pop("duree_ms", None)
    db["metadonnees"].pop("duree_ms", None)
    F("F6_idempotence", a.returncode == 0 and da == db)
    # F7 — ancres gen-plan v3.47.0
    t = SKILL.read_text(encoding="utf-8")
    for ancre, lab in (("version: 3.47.0", "frontmatter"),
                       ("RAPPEL PERMANENT — LANGUE DU DIALOGUE", "§0 rappel langue"),
                       ("É5-ROUTAGE — décision mécanique de routage skills + agents", "§1.16 hook"),
                       ("### §1.17 Décision d'agents", "§1.17"),
                       ("routage-skills-agents.py      # É5-ROUTAGE", "§2.2 structure"),
                       ("| agents écosystème (4 .agent) |", "§3 ligne"),
                       ("Routage É5-ROUTAGE (v3.47.0)", "§4 coût")):
        F(f"F7_{lab}", ancre in t)
    # F8 — cascade : KB + pin ×2 + evals + PM
    kb = KB.read_text(encoding="utf-8")
    F("F8_kb_titre", "## gen-plan v3.47.0" in kb)
    F("F8_pin_x2", '"gen-plan": "3.47.0"' in (RACINE / "scripts/check-ecosysteme-integrity.py").read_text(encoding="utf-8")
      and '"gen-plan": "3.47.0"' in (RACINE / "KNOWLEDGE-repo/scripts/check-ecosysteme-integrity.py").read_text(encoding="utf-8"))
    F("F8_evals", json.load(open(RACINE / "skills/gen-plan/evals/evals.json"))["version"] == "3.47.0")
    F("F8_pm_347", (RACINE / "KNOWLEDGE-repo/skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.47.0.md").exists())
    F("F8_pm_346_archive", (RACINE / "KNOWLEDGE-repo/skills/@historique/prompts-maitres/gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.46.0.md").exists())
    F("F8_journal_r4", "v3.46.0 (2026-11-22" in (RACINE / "KNOWLEDGE-repo/skills/gen-plan/references/journal-versions.md").read_text(encoding="utf-8"))
    # F9 — garde réinjection ensure-installed (code présent + état stable)
    e = ENSURE.read_text(encoding="utf-8")
    F("F9_garde_code", all(s in e for s in ("SKILLS_REINJETES", "signature_native", "reparer_reinjection", "MAJUSCULES_STALE")))
    r9 = subprocess.run([sys.executable, str(ENSURE), "--check"], capture_output=True, text=True)
    try:
        d9 = json.loads(r9.stdout.strip().splitlines()[0])
        F("F9_etat_stable", d9.get("verdict") in ("INSTALLE", "INSTALLE-REPARÉ"), d9.get("verdict", "?"))
    except Exception as exc:
        F("F9_etat_stable", False, str(exc)[:120])
    # F10 — audit conformité
    r10 = subprocess.run([sys.executable, str(RACINE / "scripts/task113-audit-conformite.py")], capture_output=True, text=True)
    F("F10_audit", "73/73 CONFORMES" in r10.stdout and "4/4 CONFORMES" in r10.stdout,
      r10.stdout.splitlines()[0] if r10.stdout else "")
    # F11 — arbitres non-régression
    for lab, p, cwd in (("triggers", RACINE / "scripts/check-triggers-replay.py", RACINE),
                        ("verify_cross", RACINE / "KNOWLEDGE-repo/scripts/verify-cross.py", RACINE / "KNOWLEDGE-repo")):
        r11 = subprocess.run([sys.executable, str(p)], cwd=str(cwd), capture_output=True, text=True, timeout=120)
        F(f"F11_{lab}", r11.returncode == 0)
    # F12 — livrable analyse
    a = ANALYSE.read_text(encoding="utf-8")
    F("F12_analyse", all(s in a for s in ("139,1 Kio", "OPTIMISE", "DÉGRADE", "orchestrateur-tsi", "100,2 Kio")))
    # F13 — dérive langue journalisée + rappel permanent
    F("F13_derive_worklog", "DÉRIVE LANGUE constatée + corrigée" in WORKLOG.read_text(encoding="utf-8"))
    F("F13_rappel_genplan", "rappel à CHAQUE exécution de gen-plan" in t)
    # P1 — performance script (< 1 s ×4 tâches, murale subprocess)
    p1max = 0.0
    for tc in ("traduire un pdf chinois en français", "concevoir un site web interactif",
               "quelle heure est-il ?", "audit complet des skills puis correction et push"):
        t0 = time.perf_counter()
        routage(tc)
        p1max = max(p1max, (time.perf_counter() - t0) * 1000)
    F("P1_duree_max", p1max < 1000.0, f"max {p1max:.0f} ms (cible < 1000 ms)")
    # P2 — poids gen-plan sous seuil CRITIQUE
    poids = SKILL.stat().st_size
    F("P2_poids_genplan", poids < 60 * 1024, f"{poids} o ({poids/1024:.1f} Kio < 60 Kio)")
    # P3 — sortie JSON compacte
    sortie = (RACINE / "download/routage-dernier.json").stat().st_size
    F("P3_sortie_json", sortie < 5 * 1024, f"{sortie} o < 5120 o")
    # P4 — arbitre poids-chargement : gen-plan non-CRITIQUE
    r4 = subprocess.run([sys.executable, str(RACINE / "scripts/poids-chargement.py")], capture_output=True, text=True, timeout=60)
    ligne = [l for l in r4.stdout.splitlines() if l.startswith("| 1 ") or "| gen-plan " in l]
    F("P4_poids_arbitre", ("CRITIQUE" not in (ligne[0] if ligne else r4.stdout[:400])), (ligne[0][:120] if ligne else "absent du top — OK"))

    nf = sum(1 for x in tests if x["verdict"] == "FAIL")
    rapport = {"tache": "Task 114 tests F+P", "trace": "1a2025197d2a0e9d + 1a2025ce4a6ed095",
               "synthese": {"total": len(tests), "pass": len(tests) - nf, "fail": nf},
               "tests": tests}
    RAPPORT.write_text(json.dumps(rapport, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for x in tests:
        print(("PASS " if x["verdict"] == "PASS" else "FAIL ") + x["nom"]
              + (" — " + x["detail"] if x["detail"] else ""))
    print(f"VERDICT : {rapport['synthese']['pass']}/{len(tests)} PASS"
          + (" — FAIL détectés" if nf else ""))
    return 0 if nf == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
