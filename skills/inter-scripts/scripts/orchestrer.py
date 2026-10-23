#!/usr/bin/env python3
"""⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.7)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.

inter-scripts — orchestrateur multi-projets (v1.0.0).

Graph engineering : chaque plan d'actions (un par projet) est un graphe de
tâches (nœuds = appels de scripts, arêtes = dépendances sortie->entrée) ;
tri topologique de Kahn, détection de cycles, niveaux d'exécution (diamond).

Fleet engineering : exécution niveau par niveau (pipeline M3 entre niveaux),
tâches d'un niveau lancées simultanément en ThreadPool (fan-out M2), Task IDs
préfixés par projet, agrégation unique + re-vérification, journal JSON.

Canaux ADAPTÉS À L'ÉVOLUTION DE CHAQUE PLAN : à chaque exécution, l'état
restant de TOUS les plans est relu ; si >= 2 tâches restantes visent un même
nœud concurrent (même niveau ou projets distincts) -> canal daemon-socket
(démarré/vérifié) ; tâche isolée -> one-shot ; sortie->entrée -> fichier-typé.
La décision et sa rationale sont consignées au journal.

Usage :
  orchestrer.py --plans p1.json p2.json [--executer] [--out-dir DIR]
  orchestrer.py --plans p-cycle.json --verifier   (graphe + canaux, sans exécuter)
Format plan :
  {"projet": "alpha", "taches": [
    {"id": "T1", "script": "trigo-euler", "op": "trig.eval",
     "args": {...}, "out": "T1.json", "deps": []} ]}
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from collections import deque
from concurrent.futures import ThreadPoolExecutor

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.dirname(SKILL))
sys.path.insert(0, os.path.join(SKILL, "scripts"))
from is_client import Client, charger_registre  # noqa: E402


def charger_plans(chemins):
    plans = []
    for c in chemins:
        with open(c, encoding="utf-8") as f:
            p = json.load(f)
        p["_chemin"] = c
        plans.append(p)
    return plans


def niveau_kahn(plans):
    """Graph engineering : niveaux topologiques multi-projets + détection cycles."""
    noeuds = {}
    for p in plans:
        for t in p["taches"]:
            tid = f'{p["projet"]}/{t["id"]}'
            if tid in noeuds:
                raise ValueError(f"Task ID dupliqué : {tid}")
            noeuds[tid] = {"projet": p["projet"], "tache": t,
                           "deps": [f'{p["projet"]}/{d}' for d in t.get("deps", [])]}
    for tid, n in noeuds.items():
        for d in n["deps"]:
            if d not in noeuds:
                raise ValueError(f"dépendance inconnue : {d} (de {tid})")
    deg = {tid: len(n["deps"]) for tid, n in noeuds.items()}
    succ = {tid: [] for tid in noeuds}
    for tid, n in noeuds.items():
        for d in n["deps"]:
            succ[d].append(tid)
    niveau = 0
    libre = sorted([tid for tid, dg in deg.items() if dg == 0])
    ordre, niveaux = [], []
    vus = 0
    while libre:
        niveaux.append(sorted(libre))
        ordre.extend(sorted(libre))
        vus += len(libre)
        suivant = []
        for tid in libre:
            for s in succ[tid]:
                deg[s] -= 1
                if deg[s] == 0:
                    suivant.append(s)
        libre = sorted(set(suivant))
        niveau += 1
    if vus != len(noeuds):
        cycles = sorted([tid for tid, dg in deg.items() if dg > 0])
        return None, noeuds, cycles
    return niveaux, noeuds, []


def decider_canaux(niveaux, noeuds, registre):
    """Choix de canal par tâche, adapté à l'état restant de TOUS les plans."""
    # comptage des tâches restantes par script (toutes tasks du graphe = restantes)
    par_script = {}
    for tid, n in noeuds.items():
        par_script.setdefault(n["tache"]["script"], []).append(tid)
    decisions = {}
    for niv in niveaux or []:
        for tid in niv:
            n = noeuds[tid]
            script = n["tache"]["script"]
            concurrent = registre["scripts"].get(script, {}).get("concurrent", False)
            nb = len(par_script.get(script, []))
            if concurrent and nb >= 2:
                canal, why = "daemon-socket", (
                    f"{nb} tâches restantes visent '{script}' (projets : "
                    f"{sorted(set(noeuds[x]['projet'] for x in par_script[script]))}) "
                    "-> binaire rémanent partagé")
            elif len(n.get("consomme_par", [])) > 0 or n["tache"].get("deps"):
                canal, why = "fichier-typé", (
                    "sortie->entrée chaînée (deps : "
                    f"{n['tache'].get('deps', [])}) — handoff JSON typé")
            else:
                canal, why = "one-shot", "tâche isolée, aucune contention"
            decisions[tid] = {"canal": canal, "rationale": why}
    return decisions


def executer_tache(tid, n, decision, out_dir, client_cache, registre):
    """Exécute une tâche selon son canal — retourne l'entrée de journal."""
    t = n["tache"]
    script = t["script"]
    entree = {"id": tid, "script": script, "op": t.get("op"),
              "canal": decision["canal"], "projet": n["projet"]}
    t0 = time.perf_counter()
    try:
        out_f = os.path.join(out_dir, f'{n["projet"]}_{t["id"]}.json')
        if registre["scripts"].get(script, {}).get("binaire"):
            # script JSON-protocole (binaire ou python + requête/réponse fichiers)
            cli = client_cache.get(script)
            if cli is None:
                cli = client_cache[script] = Client(script)
            rep = cli.appeler(t["op"], t.get("args", {}),
                              canal="daemon-socket" if decision["canal"] == "daemon-socket" else None)
            if not rep.get("ok"):
                entree["statut"] = "ECHEC"
                entree["erreur"] = rep.get("erreur", "?")
            else:
                rep = {k: v for k, v in rep.items() if k != "canal"}
                with open(out_f, "w", encoding="utf-8") as f:
                    json.dump(rep, f, ensure_ascii=False, indent=1)
                entree["statut"] = "OK"
                entree["out"] = out_f
        else:
            # script CLI fichiers : commande déclarée dans la tâche
            cmd = [os.path.join(ROOT, t["cmd"][0])] + t["cmd"][1:]
            if cmd[0].endswith(".py"):
                cmd = [sys.executable] + cmd   # exécutable non +x -> via interpréteur
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=300, cwd=ROOT)
            entree["statut"] = "OK" if r.returncode == 0 else "ECHEC"
            entree["rc"] = r.returncode
            if r.returncode != 0:
                entree["erreur"] = r.stderr[-300:]
            if t.get("out"):
                entree["out"] = os.path.join(out_dir, t["out"])
        if entree.get("out") and os.path.exists(entree["out"]):
            h = hashlib.sha256(open(entree["out"], "rb").read()).hexdigest()[:16]
            entree["sha16"] = h
    except Exception as e:  # noqa: BLE001
        entree["statut"] = "ECHEC"
        entree["erreur"] = str(e)[:300]
    entree["duree_ms"] = round((time.perf_counter() - t0) * 1000, 2)
    return entree


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plans", nargs="+", required=True)
    ap.add_argument("--executer", action="store_true")
    ap.add_argument("--verifier", action="store_true")
    ap.add_argument("--out-dir", default="tmp/inter-scripts-journal")
    a = ap.parse_args()
    registre = charger_registre()
    try:
        plans = charger_plans(a.plans)
        niveaux, noeuds, cycles = niveau_kahn(plans)
    except ValueError as e:
        print(json.dumps({"verdict": "REJET", "erreur": str(e)}, ensure_ascii=False))
        return 2
    if cycles:
        print(json.dumps({"verdict": "CYCLE_DETECTE", "cycles": cycles,
                          "nb_noeuds": len(noeuds)}, ensure_ascii=False))
        return 1
    decisions = decider_canaux(niveaux, noeuds, registre)
    graphe = {
        "noeuds": sorted(noeuds),
        "niveaux": niveaux,
        "aretes": [{"de": d, "vers": tid}
                   for tid, n in noeuds.items() for d in n["deps"]],
        "canaux": decisions,
    }
    if a.verifier or not a.executer:
        print(json.dumps({"verdict": "PLAN_VALIDE", "graphe": graphe,
                          "nb_noeuds": len(noeuds)}, ensure_ascii=False, indent=1))
        return 0
    # ---- exécution flotte : pipeline de niveaux, fan-out intra-niveau
    os.makedirs(a.out_dir, exist_ok=True)
    journal = {"date_debut": time.strftime("%Y-%m-%dT%H:%M:%S"),
               "plans": [p["projet"] for p in plans],
               "graphe": graphe, "taches": [], "verdict": None}
    client_cache = {}
    ok_all = True
    for niv in niveaux:
        avec_deps = [tid for tid in niv if noeuds[tid]["tache"].get("deps")]
        sans_deps = [tid for tid in niv if tid not in avec_deps]
        for tid in sans_deps:   # canaux déclarés même sans exécution parallèle
            noeuds[tid]["consomme_par"] = []
        resultats = []
        with ThreadPoolExecutor(max_workers=max(1, len(niv))) as pool:
            futs = {pool.submit(executer_tache, tid, noeuds[tid], decisions[tid],
                                a.out_dir, client_cache, registre): tid for tid in niv}
            for fut in futs:
                resultats.append(fut.result())
        resultats.sort(key=lambda r: r["id"])
        journal["taches"].extend(resultats)
        ok_all = ok_all and all(r["statut"] == "OK" for r in resultats)
    echecs = [r["id"] for r in journal["taches"] if r["statut"] != "OK"]
    journal["verdict"] = "PASS" if ok_all else f"ECHEC ({', '.join(echecs)})"
    journal["date_fin"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    chem_journal = os.path.join(a.out_dir, "journal.json")
    with open(chem_journal, "w", encoding="utf-8") as f:
        json.dump(journal, f, ensure_ascii=False, indent=1)
    print(json.dumps({"verdict": journal["verdict"], "taches": len(journal["taches"]),
                      "canaux_utilises": sorted(set(d["canal"] for d in decisions.values())),
                      "journal": chem_journal}, ensure_ascii=False, indent=1))
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main())
