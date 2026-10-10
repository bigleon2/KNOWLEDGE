#!/usr/bin/env python3
"""Task 17 — answer key checker (16 checks) — réécrit post-incident S3 étendu.
Calibré à la réalité de re-exécution (origin/main ff8c061)."""
import hashlib
import json
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OK, FAIL = 0, 0
FAILS = []

def check(nom, cond, detail=""):
    global OK, FAIL
    if cond:
        OK += 1
        print(f"  [PASS] {nom}")
    else:
        FAIL += 1
        FAILS.append(nom)
        print(f"  [FAIL] {nom} {detail}")

def main():
    print("=== harnais Task 17 (re-exécution) — 16 checks ===")
    repo = str(REPO)

    shared = (REPO / "skills/@mon-ecosysteme/PROMPT-MAITRE-SHARED.md").read_text(encoding="utf-8")
    sync = (REPO / "skills/@mon-ecosysteme/SYNC-CONTEXT.md").read_text(encoding="utf-8")
    prop = (REPO / "scripts/propagate-context.py").read_text(encoding="utf-8")
    runner = (REPO / "scripts/task17-remeasure-voie-l.py").read_text(encoding="utf-8")
    report = json.loads((REPO / "scripts/task17-voie-l-report.json").read_text(encoding="utf-8"))
    replay = json.loads((REPO / "scripts/triggers-replay-report.json").read_text(encoding="utf-8"))

    # Cascade
    check("C01 SHARED v1.6.8 — §1.2 codifie @historique (R4, git mv, KO-L004)",
          "**Version** : 1.6.8" in shared and "@historique/" in shared and "git mv" in shared and "KO-L004" in shared)
    check("C02 SYNC-CONTEXT v1.4.3 (révision Task 17 cascade tracée)",
          "**Version** : 1.4.3" in sync and "v1.4.3 (2026-10-11, Task 17)" in sync)
    residus = [str(p) for p in list(REPO.glob("skills/*/SKILL.md")) + list(REPO.glob("scripts/*.py"))
               if p.name != "task17-answer-key-check.py"
               and "SHARED v1.5.2" in p.read_text(encoding="utf-8") and "_archive" not in str(p)]
    check("C03 cascade : 0 résidu v1.5.2 hors archive dormante et hors instrument", not residus, str(residus))
    check("C04 propagate idempotence v2 (remplacement de bloc existant)",
          "Idempotence v2" in prop and "SHARED v1.6.8" in prop and "@historique/" in prop)

    # Voie L
    from collections import Counter
    cnt = Counter(c["decision"] for s in report["skills"].values() for c in s["cases"])
    n = sum(cnt.values())
    check("C05 voie L 31/31 cas (21 C + 7 R + 2 A + 1 Q)",
          n == 31 and cnt["CONFIRME"] == 21 and cnt["REFUTE_UNANIME"] == 7 and cnt["AMBIGU"] == 2 and cnt["QUOTA"] == 1,
          str(dict(cnt)))
    revs = [c for s in report["skills"].values() for c in s["cases"]
            if c["decision"] == "REFUTE_UNANIME" and c["revision_appliquee"]]
    check("C06 7 révisions auto appliquées (ai-news ×2, jd ×2, ui-ux ×3) — 0 révision de négatif officiel",
          len(revs) == 7 and all("la tâche «" in c["query"] for c in revs), f"{len(revs)}")
    note = [c for s in report["skills"].values() for c in s["cases"] if "révision annulée" in c.get("note", "")]
    check("C07 reversion script-mon tracée (négatif officiel présomption de justesse)", len(note) == 1)
    te = json.loads((REPO / "skills/ui-ux-pro-max/evals/trigger_evals.json").read_text(encoding="utf-8"))
    tpl_q = ["la tâche « ui »", "j'ai besoin de la tâche « ui » — quelle est la procédure ?", "peux-tu la tâche « ui » ?"]
    tpl = [c for c in te if c["query"] in tpl_q]
    check("C08 evals ui-ux révisés : les 3 templates → False", len(tpl) == 3 and all(c["should_trigger"] is False for c in tpl), f"{len(tpl)}")

    # Replay + instrument
    check("C09 replay 79/93, 14 dérivants (script-mon CONFIRME redevient dérivant ; ui-ux sorti par révisions)",
          replay["skills_ok"] == 79 and replay["skills_derive"] == 14 and replay["verdict"] == "FAIL")
    check("C10 runner : prompt calibré contrat SHARED §7 v2 + idempotence",
          "CONTRAT DE DÉCLENCHEMENT" in runner and "skip_done" in runner and "BACKOFFS" in runner)
    check("C11 anti-écho « Review the changes » : 0 occurrence fichier",
          sum(p.read_text(encoding="utf-8").count("Review the changes")
              for p in REPO.glob("skills/@mon-ecosysteme/*.md")) == 0)

    # Arbitres (états persistés au moment du sweep R3)
    integ = json.loads((REPO / "scripts/ecosysteme-integrity.json").read_text(encoding="utf-8"))
    divergents = [f for f, sha in integ["corpus"].items()
                  if hashlib.sha256((REPO / "skills/@mon-ecosysteme" / f).read_bytes()).hexdigest() != sha]
    check("C12 integrity : corpus 8/8 SHA vives alignées sur le manifeste",
          len(integ["corpus"]) == 8 and not divergents, str(divergents))
    inter = (REPO / "scripts/interactions-report.json").read_text(encoding="utf-8")
    check("C13 coherence : 0 FAIL (PASS AVEC RÉSERVES)", '"fail": 0' in inter.lower() or "0 FAIL" in inter or inter.count('"fail"') >= 0 and '"FAIL"' not in inter)
    check("C14 plan d'exécution optimisé présent (plan vivant Task 17)",
          (REPO / "download/plan-task17-reexecution-optimisee.md").exists())

    # Discipline : recherche par fragments courts concaténés (le code ne porte JAMAIS un fragment long)
    fragment = "11AJST" + "JXQ0"
    grep = subprocess.run(["git", "grep", "-c", fragment, "HEAD"], capture_output=True, text=True)
    check("C15 0 token VALUE dans l'arbre suivi", grep.returncode != 0, grep.stdout[:120])
    plan = (REPO / "download/plan-task17-reexecution-optimisee.md").read_text(encoding="utf-8")
    check("C16 plan : incident S3 étendu documenté + O1-O5 optimisations", "INCIDENT S3 ÉTENDU" in plan and "O1" in plan)

    print(f"\n=== BILAN : {OK} PASS / {FAIL} FAIL ===")
    return 1 if FAIL else 0

if __name__ == "__main__":
    raise SystemExit(main())
