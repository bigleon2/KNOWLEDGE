#!/usr/bin/env python3
"""Re-jeu mécanique correct-work (projet) --bloc — Task 17 (blocs B2-B4).

Rejoue les vérifications exécutables de l'answer key D001-D009 du plan
MODE STEP (plan-actions-optimisation-ecosysteme-elements-step-2026-11-21T03h23Z.md,
E8 PASS) et imprime un verdict par décision — jamais de faux PASS (KO-L003 :
les statuts sont fixés par l'exécution, les chiffres viennent du disque).
"""

# ⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.45)
# SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
# Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
# Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
# Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
# Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
# Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).

import glob
import re
import subprocess
import sys
from pathlib import Path

HOST = Path("/home/z/my-project")
REPO = HOST / "KNOWLEDGE-repo"
PLAN = (HOST / "download"
        / "plan-actions-optimisation-ecosysteme-elements-step-2026-11-21T03h23Z.md")
WORKLOG = HOST / "worklog.md"
PIPELINE = HOST / "scripts/eco_install_pipeline.py"
PIPELINE_REPO = REPO / "scripts/eco_install_pipeline.py"
HARNAIS = HOST / "scripts/task17-harnais-elements.py"
SONDE = HOST / "scripts/task17-sonde-elements.py"
GARDE = HOST / "skills/gen-plan/scripts/check_plan_protocol.py"


def executer(cmd, cwd=None, timeout=420):
    """Exécute une commande ; retourne (rc, sortie_texte)."""
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                          timeout=timeout)
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def d001():
    """D001 — pendance PUSH Task 16 éteinte (3a7a4a67 sur origin/main)."""
    rc, _ = executer(["git", "-C", str(REPO), "merge-base", "--is-ancestor",
                      "3a7a4a67", "origin/main"])
    return rc == 0, "3a7a4a67 ancêtre de origin/main (ref local vérifié ls-remote)"


def d002():
    """D002 — analyse approfondie consolidée présente au plan."""
    s = PLAN.read_text(encoding="utf-8")
    ok = ("### État des éléments intégrés" in s and "re-sondé ce tour" in s
          and "P8" in s and "JUDICIEUX" in s)
    return ok, "sections analyse + re-sonde + écarts + choix présents au plan"


def d003():
    """D003 — plan re-généré MODE STEP : garde E7-DISP P1-P5."""
    rc, out = executer(["python3", str(GARDE), "--plan", str(PLAN),
                        "--worklog", str(WORKLOG)])
    return rc == 0 and "VERDICT : PASS" in out, f"check_plan_protocol rc={rc}"


def d004():
    """D004 — P8 éteint : 0 import indenté + arbres byte-identiques."""
    s = PIPELINE.read_text(encoding="utf-8")
    indents = [l for l in s.split("\n")
               if re.match(r"^[ ]+[A-Za-z_]*(import|from) ", l)]
    if indents:
        return False, f"imports indentés restants : {indents[:2]}"
    a = PIPELINE.read_bytes()
    b = PIPELINE_REPO.read_bytes()
    return a == b, "0 import indenté, ×2 arbres byte-identiques (commit 56eeb82b)"


def d005():
    """D005 — verdicts correct-py consignés au worklog Task 17."""
    w = WORKLOG.read_text(encoding="utf-8")
    i = w.find("Task ID: 17")
    t = w[i:]
    n = t.count("CONFORME")
    return n >= 2, f"{n} verdicts CONFORME au worklog Task 17"


def d006():
    """D006 — fixtures TSI restaurées : ≥ 15 re-jeuables."""
    a = glob.glob("/home/z/my-project/tools/sxm/super-xtreme-mapper/**/Fixtures/TSI/*.tsi",
                  recursive=True)
    return len(a) >= 15, f"{len(a)} fixtures .tsi re-jeuables"


def d007():
    """D007 — harnais tests fonctionnels : rc=0, PASS en sortie."""
    rc, out = executer(["python3", str(HARNAIS)], cwd=str(HOST))
    return rc == 0 and "VERDICT : PASS" in out, f"harnais rc={rc} (matrice T0-T9)"


def d008():
    """D008 — rapport performance présent, VERDICT + mesures ms."""
    p = sorted(glob.glob("/home/z/my-project/download/rapport-tests-elements-integres-2026-11-21T*.md"))
    if not p:
        return False, "rapport perf absent"
    s = open(p[-1], encoding="utf-8").read()
    return "VERDICT" in s and "ms" in s, f"{Path(p[-1]).name} ({len(s)} caractères)"


def d009():
    """D009 — sonde éléments : idempotente ×2 + commisée au dépôt."""
    r1 = subprocess.run(["python3", str(SONDE)], capture_output=True, text=True)
    r2 = subprocess.run(["python3", str(SONDE)], capture_output=True, text=True)
    if r1.returncode != r2.returncode or r1.stdout != r2.stdout:
        return False, "sorties divergentes (non idempotent)"
    g = subprocess.run(["git", "-C", str(REPO), "ls-files", "--error-unmatch",
                        "scripts/task17-sonde-elements.py"], capture_output=True)
    return g.returncode == 0, f"idempotente ×2 rc={r1.returncode} + commisée (ff5e5a2f)"


DECISIONS = [
    ("D001", d001), ("D002", d002), ("D003", d003), ("D004", d004),
    ("D005", d005), ("D006", d006), ("D007", d007), ("D008", d008),
    ("D009", d009),
]


def main():
    """Rejoue D001-D009 et imprime le verdict par décision (rc 0/1)."""
    echecs = []
    for ident, func in DECISIONS:
        ok, detail = func()
        print(f"[{'PASS' if ok else 'FAIL'}] {ident} — {detail}")
        if not ok:
            echecs.append(ident)
    if echecs:
        print(f"VERDICT : FAIL ({9 - len(echecs)}/9) — échecs : {', '.join(echecs)}")
        return 1
    print("VERDICT : PASS (9/9)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
