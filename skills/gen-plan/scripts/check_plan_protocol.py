#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hook E7-DISP (gen-plan v3.24.0, §1.2bis) — arbitre du protocole de finalisation de plan.

Ferme le bug « plan d'actions non affiché / protocole court-circuité » (3 occurrences,
session web-dd290b0d) : un plan écrit mais non validé / non journalisé / non affiché
devient mécaniquement détectable — KO-L003 (invariants dérivés de l'état courant).

Usage :
  check_plan_protocol.py --plan <fichier-plan.md> --worklog <worklog.md> [--json]
  check_plan_protocol.py --selftest

Checks (P1-P5) :
  P1  plan existe et non vide
  P2  answer key présente dans le plan (section « Answer key » avec ≥ 1 décision
      portant un champ verification exécutable)
  P3  worklog journalise le plan (R5 — le nom de fichier du plan est cité)
  P4  preuve d'affichage : marqueur PLAN-AFFICHE cité dans la MÊME entrée worklog
      que le plan (R5 + hook E7-DISP)
  P5  verdict E8 consigné dans le plan (ligne « Verdict E8 : »)

Verdict : PASS (rc 0) si 5/5 — sinon FAIL (rc 1) avec la liste des échecs.
--json : rapport machine. --selftest : auto-vérification (sait échouer).
Idempotent ×2 (lecture seule sur les fichiers audités ; le selftest nettoie son bac à sable).
"""
import argparse
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path


def check_p1(plan: Path) -> tuple:
    if not plan.exists():
        return False, "plan inexistant"
    content = plan.read_text(encoding="utf-8", errors="replace")
    if not content.strip():
        return False, "plan vide"
    return True, f"plan présent ({len(content)} caractères)"


def check_p2(plan: Path) -> tuple:
    content = plan.read_text(encoding="utf-8", errors="replace")
    if not re.search(r"^#{1,3}\s.*Answer key", content, re.MULTILINE | re.IGNORECASE):
        return False, "section « Answer key » absente du plan"
    # au moins une décision avec un champ verification exécutable
    verifs = re.findall(r"verification\s*:", content)
    criteres = re.findall(r"criterion\s*:", content)
    if not verifs or not criteres:
        return False, "answer key sans décision vérifiable (criterion/verification)"
    return True, f"answer key présente ({len(criteres)} décisions, {len(verifs)} vérifications)"


def _worklog_entries(content: str):
    """Découpe le worklog en entrées (séparées par '---' seuls)."""
    blocks = re.split(r"^---\s*$", content, flags=re.MULTILINE)
    return [b for b in blocks if b.strip()]


def check_p3(plan: Path, worklog: Path) -> tuple:
    if not worklog.exists():
        return False, "worklog inexistant"
    content = worklog.read_text(encoding="utf-8", errors="replace")
    nom = plan.name
    if nom not in content:
        return False, f"plan « {nom} » jamais journalisé au worklog (R5 violée)"
    return True, f"plan journalisé au worklog (nom cité : {nom})"


def check_p4(plan: Path, worklog: Path) -> tuple:
    content = worklog.read_text(encoding="utf-8", errors="replace")
    nom = plan.name
    for entry in _worklog_entries(content):
        if "PLAN-AFFICHE" in entry and nom in entry:
            return True, "marqueur PLAN-AFFICHE présent dans l'entrée worklog du plan"
    if "PLAN-AFFICHE" not in content:
        return False, "marqueur PLAN-AFFICHE absent du worklog (affichage non prouvé — hook E7-DISP)"
    return False, "PLAN-AFFICHE présent mais hors de l'entrée worklog du plan"


def check_p5(plan: Path) -> tuple:
    content = plan.read_text(encoding="utf-8", errors="replace")
    m = re.search(r"Verdict E8\s*:\s*(.+)", content)
    if not m:
        return False, "verdict E8 non consigné dans le plan (ligne « Verdict E8 : » attendue)"
    suite = m.group(1).strip()
    # garde anti-verdict-périmé (KO-L003) : l'horodatage du verdict doit matcher
    # l'horodatage du plan — toute écriture E7/E13/re-génération exige la re-validation
    mh = re.search(r"Horodatage plan\s*:\s*([A-Za-z0-9T:.\-+]+)", content)
    if not mh:
        return False, "ligne « Horodatage plan : » absente (convention E7-DISP — anti-verdict-périmé)"
    hv = re.search(r"Horodatage vérifié\s*:\s*([A-Za-z0-9T:.\-+]+)", suite)
    if not hv:
        return False, "verdict E8 sans « Horodatage vérifié : » (anti-verdict-périmé — re-validation requise à chaque écriture du plan)"
    if mh.group(1) != hv.group(1):
        return False, (f"verdict E8 PÉRIMÉ : horodatage plan {mh.group(1)} ≠ horodatage vérifié "
                       f"{hv.group(1)} — le plan a été modifié après validation, re-validation E8 requise")
    return True, f"verdict E8 consigné et frais (horodatage {mh.group(1)} : {suite[:55]})"


def run_checks(plan: Path, worklog: Path) -> dict:
    checks = {}
    ok1, _ = check_p1(plan)
    checks["P1_plan_present"] = (ok1, _)
    if ok1:
        checks["P2_answer_key"] = check_p2(plan)
        checks["P5_verdict_E8"] = check_p5(plan)
    else:
        checks["P2_answer_key"] = (False, "non exécuté — plan absent ou vide")
        checks["P5_verdict_E8"] = (False, "non exécuté — plan absent ou vide")
    checks["P3_worklog_R5"] = check_p3(plan, worklog)
    checks["P4_affichage"] = check_p4(plan, worklog)
    fails = [k for k, (ok, _) in checks.items() if not ok]
    return {
        "verdict": "PASS" if not fails else "FAIL",
        "plan": str(plan),
        "worklog": str(worklog),
        "checks": {k: {"statut": "PASS" if ok else "FAIL", "detail": d} for k, (ok, d) in checks.items()},
        "echecs": fails,
    }


# ---------------------------------------------------------------- selftest

def _plan_valide(nom: str = "plan-factice.md") -> str:
    return (
        f"# Plan factice — {nom}\n\n## Groupes\n\n### G1 — Tâche — #token 100\n\n"
        "## Answer key (hook E1)\n\n```yaml\ndecisions:\n  - id: \"D001\"\n"
        "    criterion: \"Le livrable existe\"\n"
        f"    verification: \"test -s {nom}\"\n"
        "    source: \"directive test\"\n    priority: \"S2\"\n    status: \"pending\"\n```\n\n"
        "## Hooks de validation (E8)\n\nHorodatage plan : 2026-10-25T18:00:00Z\n"
        "Verdict E8 : PASS (answer-key-checker 16/16, test — Horodatage vérifié : 2026-10-25T18:00:00Z)\n"
    )


def _worklog_valide(nom: str) -> str:
    return (
        "---\nTask ID: 99\nAgent: test\nTask: génération du plan factice\n\n"
        f"Work Log:\n- Plan {nom} généré ; verdict E8 : PASS ; bloc récapitulatif affiché.\n"
        f"- PLAN-AFFICHE ({nom}) — titre, groupes, #token, verdict E8, chemin.\n\n"
        "Stage Summary:\n- Plan factice livré.\n"
    )


def selftest() -> int:
    """5 vérifications : PASS sur état complet, FAIL sur chacun des manques clés."""
    results = []
    tmp = Path(tempfile.mkdtemp(prefix="check-plan-protocol-"))
    try:
        # 1. état complet -> PASS
        plan = tmp / "plan-ok.md"
        plan.write_text(_plan_valide(plan.name), encoding="utf-8")
        wl = tmp / "worklog.md"
        wl.write_text(_worklog_valide(plan.name), encoding="utf-8")
        r = run_checks(plan, wl)
        results.append(("état complet -> PASS", r["verdict"] == "PASS", r["echecs"]))

        # 2. plan jamais journalisé -> P3/P4 FAIL
        wl2 = tmp / "worklog-vide.md"
        wl2.write_text("---\nTask ID: 1\nAgent: test\nTask: autre chose\n\nWork Log:\n- rien à voir\n", encoding="utf-8")
        r2 = run_checks(plan, wl2)
        results.append(("plan non journalisé -> FAIL (P3,P4)",
                        r2["verdict"] == "FAIL" and "P3_worklog_R5" in r2["echecs"] and "P4_affichage" in r2["echecs"],
                        r2["echecs"]))

        # 3. journalisé mais non affiché -> P4 seul FAIL
        wl3 = tmp / "worklog-sans-affiche.md"
        wl3.write_text(f"---\nTask ID: 98\nAgent: test\nTask: plan\n\nWork Log:\n- Plan {plan.name} généré.\n",
                       encoding="utf-8")
        r3 = run_checks(plan, wl3)
        results.append(("journalisé non affiché -> FAIL (P4 seul)",
                        r3["verdict"] == "FAIL" and r3["echecs"] == ["P4_affichage"], r3["echecs"]))

        # 4. plan sans verdict E8 -> P5 seul FAIL
        plan4 = tmp / "plan-sans-e8.md"
        plan4.write_text(_plan_valide(plan4.name).replace(
            "Horodatage plan : 2026-10-25T18:00:00Z\n"
            "Verdict E8 : PASS (answer-key-checker 16/16, test — Horodatage vérifié : 2026-10-25T18:00:00Z)\n", ""),
            encoding="utf-8")
        wl4 = tmp / "worklog-e8.md"
        wl4.write_text(_worklog_valide(plan4.name), encoding="utf-8")
        r4 = run_checks(plan4, wl4)
        results.append(("plan sans verdict E8 -> FAIL (P5 seul)",
                        r4["verdict"] == "FAIL" and r4["echecs"] == ["P5_verdict_E8"], r4["echecs"]))

        # 4bis. verdict E8 PÉRIMÉ (E13 sans re-validation — scénario interruption) -> P5 FAIL
        plan4b = tmp / "plan-perime.md"
        plan4b.write_text(_plan_valide(plan4b.name).replace(
            "Horodatage plan : 2026-10-25T18:00:00Z", "Horodatage plan : 2026-10-25T19:30:00Z"),
            encoding="utf-8")
        wl4b = tmp / "worklog-perime.md"
        wl4b.write_text(_worklog_valide(plan4b.name), encoding="utf-8")
        r4b = run_checks(plan4b, wl4b)
        results.append(("verdict E8 périmé (E13 sans re-validation) -> FAIL (P5 seul)",
                        r4b["verdict"] == "FAIL" and r4b["echecs"] == ["P5_verdict_E8"], r4b["echecs"]))

        # 5. plan inexistant -> P1 FAIL
        r5 = run_checks(tmp / "absent.md", wl)
        results.append(("plan inexistant -> FAIL (P1)", r5["verdict"] == "FAIL" and "P1_plan_present" in r5["echecs"], r5["echecs"]))

        # idempotence : re-exécution de l'état complet -> même verdict
        r6 = run_checks(plan, wl)
        results.append(("idempotence ×2 -> PASS stable", r6["verdict"] == r["verdict"] == "PASS", r6["echecs"]))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print("SELFTEST check_plan_protocol (hook E7-DISP) :")
    ok_all = True
    for label, ok, extra in results:
        print(f"  [{'PASS' if ok else 'FAIL'}] {label}" + ("" if ok else f" — detail: {extra}"))
        ok_all = ok_all and ok
    print(f"  RESUME : {'OK (7/7)' if ok_all else 'ECHEC'}")
    return 0 if ok_all else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Arbitre du protocole de finalisation de plan (hook E7-DISP)")
    ap.add_argument("--plan", type=Path, help="fichier du plan d'actions (.md)")
    ap.add_argument("--worklog", type=Path, help="worklog partagé (worklog.md)")
    ap.add_argument("--json", action="store_true", help="sortie machine JSON")
    ap.add_argument("--selftest", action="store_true", help="auto-vérification intégrée")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    if not args.plan or not args.worklog:
        ap.error("--plan et --worklog sont requis (ou --selftest)")
    rapport = run_checks(args.plan, args.worklog)
    if args.json:
        print(json.dumps(rapport, ensure_ascii=False, indent=2))
    else:
        print("=== Arbitre E7-DISP — protocole de finalisation de plan ===")
        for k, v in rapport["checks"].items():
            print(f"  [{v['statut']}] {k} — {v['detail']}")
        print(f"  VERDICT : {rapport['verdict']}" + (f" — échecs: {', '.join(rapport['echecs'])}" if rapport["echecs"] else ""))
    return 0 if rapport["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
