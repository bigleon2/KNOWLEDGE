#!/usr/bin/env python3
"""Task 17-B — answer key checker (16 checks) : structure d'historique par skill + autres éléments.
Directive propriétaire : « un historique par skill et un fichier historique pour les autres éléments »."""
import hashlib
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
HIST = REPO / "skills/@historique"
OK, FAIL = 0, 0

def check(nom, cond, detail=""):
    global OK, FAIL
    if cond:
        OK += 1
        print(f"  [PASS] {nom}")
    else:
        FAIL += 1
        print(f"  [FAIL] {nom} {detail}")

def main():
    print("=== harnais Task 17-B — 16 checks ===")

    # D001 — historiques par skill
    par_skill = HIST / "historiques-par-skill"
    check("C01 les 3 historiques par skill présents",
          all((par_skill / f"{s}.md").exists() for s in ("gen-plan", "correct-work", "clone-chat")))
    gp = (par_skill / "gen-plan.md").read_text(encoding="utf-8")
    cw = (par_skill / "correct-work.md").read_text(encoding="utf-8")
    cc = (par_skill / "clone-chat.md").read_text(encoding="utf-8")
    check("C02 tables complètes (22/10/4 lignes de versions)",
          sum(1 for l in gp.splitlines() if l.startswith("| v")) == 22
          and sum(1 for l in cw.splitlines() if l.startswith("| v")) == 10
          and sum(1 for l in cc.splitlines() if l.startswith("| v")) == 4)
    check("C03 migration verbatim : lignes de tables d'origine présentes",
          "| v3.21.0 | 2026-10-09 |" in gp and "| v2.7.0 | 2026-10-02 |" in cw and "| v2.0.0 | 2026-08-09 |" in cc)
    check("C04 en-têtes par skill : version vivante + pointeur prompts-maitres + provenance",
          "v3.21.0" in gp and "prompts-maitres/gen-plan/" in gp and "Task 17-B" in gp
          and "v2.7.0" in cw and "v2.0.0" in cc)

    # D002 — autres éléments
    autres = (HIST / "historique-autres-elements.md").read_text(encoding="utf-8")
    check("C05 historique autres éléments : 6 sections socle",
          all(s in autres for s in ("PROMPT-MAITRE-SHARED", "SYNC-CONTEXT", "README.md",
                                    "ULTRA", "INSTALL-ECOSYSTEME", "Registre KB")))
    check("C06 trajectoires : SHARED jusqu'à v1.6.8, SYNC jusqu'à v1.4.3",
          "| v1.6.8 | 2026-10-11 |" in autres and "| v1.4.3 | 2026-10-11 |" in autres)
    check("C07 instantané KB 28 skills (verbatim registre)",
          autres.count("| v") >= 56 and "vue-upload | v1.2.0" in autres)

    # D003 — distillation retirée + références croisées
    check("C08 distillation globale retirée (R4 une information, une source)",
          not (HIST / "historique-versions-prompts-maitres.md").exists())
    pm = (REPO / "skills/@mon-ecosysteme/PROMPT-MAITRE-INSTALL-ECOSYSTEME.md").read_text(encoding="utf-8")
    rd = (REPO / "skills/@mon-ecosysteme/README.md").read_text(encoding="utf-8")
    check("C09 PM-INSTALL : 0 référence distillation, pointeur historiques-par-skill",
          "historique-versions-prompts-maitres" not in pm and "historiques-par-skill" in pm)
    check("C10 README éco : arborescence recalibrée",
          "historiques-par-skill" in rd and "historique-versions-prompts-maitres" not in rd)

    # D004 — README @historique v1.1.0
    readme = (HIST / "README.md").read_text(encoding="utf-8")
    check("C11 README v1.1.0 : structure par skill documentée",
          "**Version** : 1.1.0" in readme and "historiques-par-skill/gen-plan.md" in readme
          and "historique-autres-elements.md" in readme)
    check("C12 index SHA-256 19 PMs conservé (§5)",
          readme.count("PROMPT-MAITRE-") == 19 and "| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.6.1.md | 6356ae3e" in readme)
    check("C13 procédure §4 étendue (mise à jour des historiques)",
          "historiques-par-skill/<skill>.md" in readme and "historique-autres-elements.md" in readme)

    # Périmètre scellé + D005
    integ = __import__("json").loads((REPO / "scripts/ecosysteme-integrity.json").read_text(encoding="utf-8"))
    divergents = [f for f, sha in integ["corpus"].items()
                  if hashlib.sha256((REPO / "skills/@mon-ecosysteme" / f).read_bytes()).hexdigest() != sha]
    check("C14 périmètre scellé : corpus 8/8 SHA vives alignées", not divergents, str(divergents))
    sync = (REPO / "skills/@mon-ecosysteme/SYNC-CONTEXT.md").read_text(encoding="utf-8")
    check("C15 SYNC-CONTEXT : structure Task 17-B décrite (distillation retirée)",
          "historiques-par-skill/" in sync and "distillation globale retirée" in sync)

    # Discipline
    fragment = "11AJST" + "JXQ0"
    grep = subprocess.run(["git", "grep", "-c", fragment, "HEAD"], capture_output=True, text=True)
    check("C16 0 fragment long de token dans l'arbre suivi (fragments courts concaténés)",
          grep.returncode != 0, grep.stdout[:120])

    print(f"\n=== BILAN : {OK} PASS / {FAIL} FAIL ===")
    return 1 if FAIL else 0

if __name__ == "__main__":
    raise SystemExit(main())
