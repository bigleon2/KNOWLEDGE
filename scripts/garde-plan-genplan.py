#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.30)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).
garde-plan-genplan.py — Garde mécanique « plans d'actions générés par gen-plan ».

Directive propriétaire 2026-11-01 (trace 1a1932155da4969d) : 100 % des plans d'actions
doivent être produits par le skill gen-plan, dans toutes les situations. Cette garde
détecte mécaniquement (R-F2/R-F3 — le filesystem fait foi) tout plan de download/plan-*.md
hors protocole, à chaque ouverture de session :

  C1  « Verdict E8 » consigné (validation par l'arbitre check_plan_protocol.py)
  C2  « Horodatage plan » présent (couplage verdict/horodatage E7-DISP)
  C3  answer key YAML « decisions: » avec « verification: » exécutable (≥ 1)
  C4  référence au protocole gen-plan (gen-plan / E13 / règle d'or / PLAN-AFFICHE)
  C5  worklog : marqueur PLAN-AFFICHE citant le fichier plan

Par défaut : plan le plus récent uniquement (--tout pour tous). Verdict PASS/FAIL + JSON.
Conventions script-creator : stdlib (N3), idempotent ×2, --selftest sait échouer.

Usage :
    garde-plan-genplan.py [--racine DIR] [--tout] [--json] [--selftest]
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MARQUEURS_PROTOCOLE = ("gen-plan", "E13", "règle d'or", "PLAN-AFFICHE", "E8", "answer key")


def plans(racine: Path, tout: bool) -> list[Path]:
    trouves = sorted((racine / "download").glob("plan-*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    return trouves if tout else trouves[:1]


def verifier_plan(plan: Path, racine: Path) -> dict:
    texte = plan.read_text(encoding="utf-8", errors="replace")
    echecs = []
    if not re.search(r"Verdict E8\s*:\s*(PASS|FAIL)", texte):
        echecs.append("C1-verdict-E8-absent")
    if not re.search(r"Horodatage plan\s*:", texte):
        echecs.append("C2-horodatage-absent")
    if not (re.search(r"^decisions:\s*$", texte, re.M) and "verification:" in texte):
        echecs.append("C3-answer-key-absente")
    if not any(m.lower() in texte.lower() for m in MARQUEURS_PROTOCOLE):
        echecs.append("C4-protocole-gen-plan-non-referencé")
    worklog = racine / "worklog.md"
    if worklog.exists():
        if plan.name not in worklog.read_text(encoding="utf-8", errors="replace"):
            echecs.append("C5-worklog-ne-cite-pas-le-plan")
    else:
        echecs.append("C5-worklog-absent")
    return {"plan": plan.name, "verdict": "PASS" if not echecs else "FAIL", "echecs": echecs}


def selftest() -> int:
    import tempfile
    bon = ("# Plan test\n\n## Answer key\n\n```yaml\ndecisions:\n  - id: \"D001\"\n    criterion: x\n"
           "    verification: \"test -s f\"\n```\n\nHorodatage plan : 2026-01-01T00:00:00+00:00\n\n"
           "Verdict E8 : PASS (check_plan_protocol P1-P5)\n")
    mauvais = "# Plan improvisé sans protocole\n\nJuste des étapes.\n"
    with tempfile.TemporaryDirectory() as tmp:
        racine = Path(tmp)
        (racine / "download").mkdir()
        (racine / "worklog.md").write_text("Task 1 — PLAN-AFFICHE (plan : plan-test.md)\n", encoding="utf-8")
        (racine / "download/plan-test.md").write_text(bon, encoding="utf-8")
        r1 = verifier_plan(racine / "download/plan-test.md", racine)
        (racine / "download/plan-autre.md").write_text(mauvais, encoding="utf-8")
        r2 = verifier_plan(racine / "download/plan-autre.md", racine)
    echecs = []
    if r1["verdict"] != "PASS":
        echecs.append("plan-conforme-rejete:" + str(r1["echecs"]))
    if r2["verdict"] != "FAIL" or len(r2["echecs"]) < 3:
        echecs.append("plan-hors-protocole-accepte:" + str(r2["echecs"]))
    print("SELFTEST FAIL : " + str(echecs) if echecs else "SELFTEST PASS (2/2 — conforme accepté, hors protocole rejeté)")
    return 1 if echecs else 0


def main() -> int:
    if "--selftest" in sys.argv:
        return selftest()
    racine = Path(sys.argv[sys.argv.index("--racine") + 1]) if "--racine" in sys.argv else Path(__file__).resolve().parents[2]
    tout = "--tout" in sys.argv
    liste = plans(racine, tout)
    if not liste:
        rapport = {"verdict": "PASS", "note": "aucun plan-*.md — rien à contrôler", "plans": []}
    else:
        resultats = [verifier_plan(p, racine) for p in liste]
        rapport = {"verdict": "PASS" if all(r["verdict"] == "PASS" for r in resultats) else "FAIL",
                   "plans": resultats, "perimetre": "tous" if tout else "plus-récent"}
    if "--json" in sys.argv:
        print(json.dumps(rapport, ensure_ascii=False, indent=1))
    else:
        print(f"  GARDE-PLANS {rapport['verdict']} ({rapport.get('perimetre', 'plus-récent')}) — " +
              "; ".join(f"{r['plan']}:{r['verdict']}" + (f" [{','.join(r['echecs'])}]" if r["echecs"] else "") for r in rapport["plans"]))
    return 0 if rapport["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
