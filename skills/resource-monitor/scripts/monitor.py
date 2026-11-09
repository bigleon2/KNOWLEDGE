#!/usr/bin/env python3
"""
resource-monitor v1.0.0 — Collecteur de surveillance permanente (F1-F4).
stdlib uniquement. Sortie JSON stdout ; code retour 0=OK, 1=PRESSION, 2=CRITIQUE.

Usage :
  python -m skills.resource-monitor.scripts.monitor \
    --budget-tokens 3500 --used-tokens 900 \
    --state-file /tmp/resource-monitor-state.json
"""
import argparse
import json
import os
import sys
import time


def read_free_disk_bytes() -> int:
    usage = os.statvfs("/home/z/my-project")
    return usage.f_bavail * usage.f_frsize


def read_mem_available_bytes() -> int:
    try:
        with open("/proc/meminfo", "r", encoding="utf-8") as fh:
            for line in fh:
                if line.startswith("MemAvailable:"):
                    return int(line.split()[1]) * 1024
    except OSError:
        pass
    return -1


def read_loadavg() -> float:
    try:
        with open("/proc/loadavg", "r", encoding="utf-8") as fh:
            return float(fh.read().split()[0])
    except (OSError, ValueError, IndexError):
        return -1.0


def read_state(path: str) -> dict:
    vide = {"timeouts_consecutifs": 0, "erreurs_429": 0,
            "derniere_progression_epoch": 0, "tache_courante": ""}
    if not path:
        return vide
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        return {**vide, **{k: v for k, v in data.items() if k in vide}}
    except (OSError, ValueError):
        return vide


def main() -> int:
    ap = argparse.ArgumentParser(description="Collecteur resource-monitor v1.0.0")
    ap.add_argument("--budget-tokens", type=int, default=0)
    ap.add_argument("--used-tokens", type=int, default=0)
    ap.add_argument("--state-file", type=str, default="")
    args = ap.parse_args()

    state = read_state(args.state_file)
    disque = read_free_disk_bytes()
    memoire = read_mem_available_bytes()
    charge = read_loadavg()
    now = time.time()

    indicateurs = {}
    causes = []
    score = 0  # 0=OK, 1=PRESSION, 2=CRITIQUE (max)

    def franchise(nom, valeur, seuil_p, seuil_c, unite):
        nonlocal score
        if valeur is None:
            return
        niv = 2 if (seuil_c is not None and valeur <= seuil_c) else (
            1 if (seuil_p is not None and valeur <= seuil_p) else 0)
        indicateurs[nom] = {"valeur": round(valeur, 2), "unite": unite, "niveau": niv}
        if niv:
            causes.append(f"{nom}={'%.2f' % valeur}{unite} niveau {'CRITIQUE' if niv==2 else 'PRESSION'}")
            score = max(score, niv)

    def limite_haute(nom, valeur, seuil_p, seuil_c):
        nonlocal score
        if valeur is None:
            return
        niv = 2 if (seuil_c is not None and valeur >= seuil_c) else (
            1 if (seuil_p is not None and valeur >= seuil_p) else 0)
        indicateurs[nom] = {"valeur": round(valeur, 2), "unite": "", "niveau": niv}
        if niv:
            causes.append(f"{nom}={valeur:.2f} niveau {'CRITIQUE' if niv==2 else 'PRESSION'}")
            score = max(score, niv)

    franchise("disque_libre", disque, 5 * 1024**3, 3 * 1024**3, "octets")
    if memoire >= 0:
        franchise("memoire_disponible", memoire, 1536 * 1024**2, 700 * 1024**2, "octets")
    if charge >= 0:
        limite_haute("charge_systeme", charge, 4.0, 8.0)

    if args.budget_tokens > 0:
        pct = 100.0 * args.used_tokens / args.budget_tokens
        limite_haute("budget_tokens_pct", pct, 80.0, 95.0)

    tos = int(state["timeouts_consecutifs"])
    if tos:
        limite_haute("timeouts_consecutifs", tos, 2, 4)
    e429 = int(state["erreurs_429"])
    if e429:
        limite_haute("erreurs_429", e429, 1, 2)

    dpe = float(state["derniere_progression_epoch"])
    if dpe > 0 and state["tache_courante"]:
        stagnation_min = (now - dpe) / 60.0
        limite_haute("stagnation_min", stagnation_min, 15.0, 40.0)

    n_pression = sum(1 for i in indicateurs.values() if i["niveau"] == 1)
    if score == 2 or n_pression >= 2:
        verdict, code = "CRITIQUE", 2
        mode = "SERIE"
    elif score == 1:
        verdict, code = "PRESSION", 1
        mode = "PARALLELE_REDUIT"
    else:
        verdict, code = "OK", 0
        mode = "PARALLELE"

    print(json.dumps({"verdict": verdict, "mode_recommande": mode,
                      "causes": causes, "indicateurs": indicateurs,
                      "ts_epoch": round(now, 3)}, ensure_ascii=False, indent=2))
    return code


if __name__ == "__main__":
    sys.exit(main())
