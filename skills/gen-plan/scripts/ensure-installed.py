#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Task 23 (D006) + Task 29 (D001-D004) — Garde É1-INSTALL : auto-réinstallation de l'écosystème.
Hook gen-plan v3.20.0 §1.16 — exécuter AVANT E1, EN PREMIER (préemption).

  --check      rc=0 écosystème installé / rc=1 absent ou dérivé (lecture seule)
  --reinstall  si ABSENT : clone (jeton éphémère env GITHUB_TOKEN, jamais persisté)
               puis vérification pipeline (Phase A) ; si déjà installé : no-op (idempotence)
               si présent mais DÉRIVÉ : diagnostic + rc=2 (aucune action destructive)
  --preempt    garde de PRÉEMPTION (Task 29 D002) : INSTALLE → PRIORITE-NONE (rc 0) ;
               ROOT absent → réinstallation IMMÉDIATE (PRIORITE-REINSTALL-OK, rc 0) ;
               dérivé → PRIORITE-REINSTALL-REQUISE + diagnostic (rc 2, non destructif)

Comportement agent (SKILL.md §1.16, Task 29 D003) : le hook s'exécute EN PREMIER — si une
réinstallation est requise, l'agent SUSPEND toute tâche (y compris en cours d'exécution),
l'exécute, PUIS met à jour le plan d'actions en cours (directive générée automatiquement
par maj_plan_apres_reinstall → download/plan-post-reinstall-<ts>.json, Task 29 D004)
avant de reprendre l'exécution.
"""
import hashlib, json, os, re, subprocess, sys, time
from pathlib import Path

ROOT = Path("/home/z/my-project/work_knowledge")
ORIGIN = "https://github.com/bigleon2/KNOWLEDGE.git"
MP = Path("/home/z/my-project")

FICHIERS_CLES = [
    "skills/KNOWLEDGE.md",
    "skills/gen-plan/SKILL.md",
    "skills/correct-work/SKILL.md",
    "skills/skills-inventory/SKILL.md",
    "skills/@mon-ecosysteme/PROMPT-MAITRE-SHARED.md",
    "skills/@mon-ecosysteme/PROMPT-ULTRA-MAITRE-ORCHESTRATION.md",
    "skills/@mon-ecosysteme/SYNC-CONTEXT.md",
    "scripts/certification-complete.py",
    "scripts/ensure-installed.py",
]


def sh(cmd, cwd=None, env=None):
    return subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True, env=env)


def etat() -> dict:
    e = {"root_present": ROOT.exists(), "git_repo": False, "head": None,
         "fichiers_manquants": [], "kb_entrees": 0}
    if e["root_present"]:
        r = sh("git rev-parse --short HEAD", cwd=ROOT)
        e["git_repo"] = r.returncode == 0
        if e["git_repo"]:
            e["head"] = r.stdout.strip()
        for f in FICHIERS_CLES:
            if not (ROOT / f).exists():
                e["fichiers_manquants"].append(f)
        kb = ROOT / "skills/KNOWLEDGE.md"
        if kb.exists():
            # S2-ε (Task 12, réconciliation 28/29 — KO-L003) : invariant dynamisé —
            # comptage STRICT au format d'entrée « ## <skill> v<semver> ». La section
            # « Décisions d'architecture (corrige-ecosysteme v2.0.0) » n'est PAS une
            # entrée KB (le filtre lache " v" in l la sur-comptait → 29 au lieu de 28).
            e["kb_entrees"] = len([l for l in kb.read_text(encoding="utf-8", errors="replace").splitlines()
                                   if re.match(r"^## [a-z0-9-]+ v\d+\.\d+\.\d+$", l.rstrip())])
    return e


def installe(e: dict) -> bool:
    return (e["root_present"] and e["git_repo"] and not e["fichiers_manquants"]
            and e["kb_entrees"] >= 14)


def maj_plan_apres_reinstall(head_avant, e2) -> str:
    """Task 29 D004 — directive de mise à jour du plan d'actions en cours.
    Détecte le plan le plus récent (download/plan-task*.md) et produit un appendice
    JSON d'instructions de re-calage cohérent et optimisé, à intégrer par l'agent."""
    plans = sorted(MP.glob("download/plan-task*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    plan_en_cours = str(plans[0]) if plans else None
    ts = time.strftime("%Y%m%d-%H%M%S")
    out = MP / ("download/plan-post-reinstall-" + ts + ".json")
    directive = {
        "verdict": "REINSTALLE-OK",
        "head_avant": head_avant, "head_apres": e2.get("head"),
        "plan_en_cours": plan_en_cours,
        "genere_le": ts,
        "instructions": [
            "Re-exécuter le hook É1-INSTALL --check (rc 0 attendu) avant de reprendre.",
            "Re-lire le plan en cours et marquer chaque étape interrompue par la réinstallation : statut 'INTERRUPT-REINSTALL'.",
            "Re-calage cohérent et optimisé : les étapes idempotentes (KO-L001 skip-done) reprennent là où elles étaient ; les étapes à état perdu en mémoire de session sont re-qualifiées avant reprise.",
            "Re-valider les décisions sensibles par leurs arbitres (answer-key-checker E7/E8) avant de considérer le plan à jour.",
            "Journaliser la mise à jour au worklog (Task ID en cours, motif : réinstallation).",
        ],
    }
    out.write_text(json.dumps(directive, ensure_ascii=False, indent=1), encoding="utf-8")
    return str(out)


def do_reinstall(e, preempt=False):
    """ABSENT → clone éphémère (jeton jamais persisté) ; DÉRIVÉ → diagnostic non destructif."""
    if e["root_present"] and (not e["git_repo"] or e["fichiers_manquants"]):
        print(json.dumps({"verdict": "DERIVE", "diagnostic": e,
                          "action": "aucune action destructive automatique — "
                                    "réparation manuelle ou --force requise"},
                         ensure_ascii=False))
        sys.exit(2)
    head_avant = e.get("head")
    env = dict(os.environ)
    tok = env.pop("GITHUB_TOKEN", None)
    url = (f"https://x-access-token:{tok}@github.com/bigleon2/KNOWLEDGE.git"
           if tok else ORIGIN)
    r = sh(f"git clone --quiet {url} {ROOT}")
    if r.returncode != 0:
        print(f"ECHEC clone (rc={r.returncode}) : {r.stderr.strip()[-300:]}")
        sys.exit(3)
    e2 = etat()
    ok = installe(e2)
    tag = "PRIORITE-REINSTALL-OK" if preempt else "REINSTALLE-OK"
    print(json.dumps({"verdict": tag if ok else ("PRIORITE-REINSTALL-DERIVE" if preempt else "REINSTALLE-DERIVE"),
                      **e2}, ensure_ascii=False))
    try:
        chemin_directive = maj_plan_apres_reinstall(head_avant, e2)
        print("Directive de mise à jour du plan : " + chemin_directive)
        wl = MP / "worklog.md"
        with open(wl, "a", encoding="utf-8") as f:
            f.write(f"\n> É1-INSTALL : réinstallation automatique exécutée (HEAD {e2.get('head')}) "
                    f"— jeton non persisté — directive de plan : {chemin_directive}\n")
    except Exception as exc:  # la réinstallation reste le résultat principal
        print("Directive de plan non générée :", exc)
    sys.exit(0 if ok else 4)


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "--check"
    e = etat()
    if mode == "--check":
        ok = installe(e)
        print(json.dumps({"verdict": "INSTALLE" if ok else "ABSENT-DERIVE", **e},
                         ensure_ascii=False))
        sys.exit(0 if ok else 1)

    if mode == "--reinstall":
        if installe(e):
            print("Déjà installé (HEAD %s) — no-op (idempotence D006)." % e["head"])
            sys.exit(0)
        do_reinstall(e, preempt=False)

    if mode == "--preempt":
        if installe(e):
            print(json.dumps({"verdict": "PRIORITE-NONE", **e}, ensure_ascii=False))
            sys.exit(0)
        if not e["root_present"]:
            do_reinstall(e, preempt=True)  # réinstallation IMMÉDIATE — préemption
        # dérivé : la priorité est d'ALERTER, sans action destructive
        print(json.dumps({"verdict": "PRIORITE-REINSTALL-REQUISE", "diagnostic": e,
                          "action": "suspendre les tâches en cours — réparation manuelle requise"},
                         ensure_ascii=False))
        sys.exit(2)

    print(__doc__)
    sys.exit(64)


if __name__ == "__main__":
    main()
