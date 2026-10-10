#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.6.8)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

"""R4 — Orchestration par dépendances (Task 36, vague 2).
Planification multi-skills avec task_id / dépendances / priorité (pattern
manus-agent) : tri topologique + détection de cycles + priorité dans l'ensemble
prêt + journal dimensionné (truncature 200 car.). Idempotent, sortie JSON.
Usage : r4-task-orchestrator.py --file <plan.json> | --demo
"""
import json, os, sys, time

OUT = "/home/z/my-project/work_knowledge/tmp/r4-orchestration.json"

DEMO = [
    {"id": "T1", "titre": "extraction specs", "deps": [], "priorite": 1},
    {"id": "T2", "titre": "baseline perf", "deps": [], "priorite": 2},
    {"id": "T3", "titre": "vague 1", "deps": ["T1", "T2"], "priorite": 1},
    {"id": "T4", "titre": "tests intermédiaires", "deps": ["T3"], "priorite": 2},
    {"id": "T5", "titre": "vague 2", "deps": ["T4"], "priorite": 1},
    {"id": "T6", "titre": "vérification finale", "deps": ["T5"], "priorite": 1},
]

def orchestre(tasks):
    ids = [t["id"] for t in tasks]
    if len(set(ids)) != len(ids):
        return {"erreur": "task_id dupliqués"}
    known = set(ids)
    for t in tasks:
        if any(d not in known for d in t.get("deps", [])):
            return {"erreur": f"dépendance inconnue dans {t['id']}"}
    pret, ordre, journal = {t["id"]: t for t in tasks if not t.get("deps")}, [], []
    fait, degres = set(), {t["id"]: len(t.get("deps", [])) for t in tasks}
    restants = {t["id"]: t for t in tasks}
    while restants:
        prets = [tid for tid, t in restants.items() if all(d in fait for d in t.get("deps", []))]
        if not prets:
            return {"erreur": f"cycle détecté parmi {sorted(restants)}", "verdict": "FAIL"}
        prets.sort(key=lambda x: restants[x].get("priorite", 9))
        for tid in prets:
            t = restants.pop(tid)
            ligne = f"{tid}:{t.get('titre', '')} (deps={t.get('deps', [])}, prio={t.get('priorite', 9)})"
            journal.append(ligne[:200])
            ordre.append(tid)
            fait.add(tid)
    return {"ordre": ordre, "journal": journal, "verdict": "PASS", "cycles": "aucun"}

def main():
    if "--file" in sys.argv:
        src = sys.argv[sys.argv.index("--file") + 1]
        tasks = json.load(open(src, encoding="utf-8"))
    else:
        tasks = DEMO
    res = orchestre(tasks)
    out = {
        "regle": "R4 — orchestration par dépendances : task_id/dépendances/priorité, tri topologique, journal dimensionné (≤200 car./entrée)",
        "ts": time.strftime("%Y-%m-%d %H:%M:%S"),
        "taches": len(tasks),
        **res,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"R4 : {len(tasks)} tâches → ordre {' → '.join(res.get('ordre', ['—']))} "
          f"({res.get('verdict')})")
    return 0 if res.get("verdict") == "PASS" else 1

if __name__ == "__main__":
    sys.exit(main())
