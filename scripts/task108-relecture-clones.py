#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 108 — Relecture intégrale « bloc par bloc » via les clones (item a).

Adaptation du précédent Task 102 (règle d'or n°5 — pas de re-jeu à
l'identique) : étendue portée de 17 à 20 clones et 146 à 153 suites, et
LECTURE DU CONTENU DE CHAQUE CLONE (lignée, fenêtre worklog §1, directives §3,
drifts §3.5, scellage validation) — les clones sont la matière première de la
relecture, pas un simple inventaire de noms de fichiers.
Sortie JSON déterministe (aucune horloge) : download/task108-extraction-blocs.json.
Codes retour : 0 = extraction complète (0 trou, 0 clone illisible) · 1 = trous
ou clones illisibles · 2 = worklog illisible.
"""
# ⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.40)
# SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
# Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
# Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6).
# Règle zéro : skills auto-contenus, KB source de vérité, dépendances YAML.

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

HOST = Path("/home/z/my-project")
WORKLOG = HOST / "worklog.md"
DOWNLOAD = HOST / "download"

SUITE_RX = re.compile(
    r"^## (?P<date>\d{4}-\d{2}-\d{2}) \(suite (?P<n>\d+),(?P<reste>.*)$"
)
CLONE_RX = re.compile(r"clone-chat-.*task(\d+)")
LIGNEE_RX = re.compile(r"(\d+)[ᵉe]+(?: de la lignée| clôture| \(|,)")


def parse_suites() -> list[dict]:
    suites: list[dict] = []
    current: dict | None = None
    for line in WORKLOG.read_text(encoding="utf-8").splitlines():
        m = SUITE_RX.match(line)
        if m:
            current = {
                "date": m.group("date"),
                "suite": int(m.group("n")),
                "titre": (m.group("reste") or "").strip(" —").strip(),
                "octets": len(line),
                "marqueurs": [],
            }
            suites.append(current)
        elif current is not None:
            current["octets"] += len(line)
            for tag, rx in (
                ("PASS", r"\bALL PASS\b|\bPASS STRICT\b|PASS 4/4|PASS 8/8|PASS\b"),
                ("FAIL", r"\bFAIL\b"),
                ("E15", r"E15\s*:|\dᵉ exposition|exposition consignée"),
                ("pendance", r"[Pp]endance"),
                ("PUSH", r"\bPUSH\b"),
                ("clone", r"clone-chat"),
                ("arbitre", r"certification-complete|verify-correct-work|triggers"),
                ("directif", r"directive propriétaire|trace `[0-9a-f]{16}`"),
                ("bug", r"\bbug\b|\bF[0-9] \("),
            ):
                if re.search(rx, line):
                    current["marqueurs"].append(tag)
    return suites


def blocs_par_jour(suites: list[dict]) -> list[dict]:
    blocs: dict[str, dict] = {}
    order: list[str] = []
    for s in suites:
        d = s["date"]
        if d not in blocs:
            blocs[d] = {"jour": d, "suites": [], "taches": []}
            order.append(d)
        b = blocs[d]
        b["suites"].append(s["suite"])
        t = re.search(r"Task (\d+)", s["titre"])
        if t:
            b["taches"].append(int(t.group(1)))
    out = []
    for d in order:
        b = blocs[d]
        taches = sorted(set(b["taches"]))
        out.append({
            "jour": d,
            "suites": f"{min(b['suites'])}-{max(b['suites'])}",
            "nb_suites": len(b["suites"]),
            "taches": (f"T{taches[0]}-T{taches[-1]}" if taches else "—"),
            "taches_liste": [f"T{t}" for t in taches],
        })
    return out


def lire_clone(path: Path) -> dict:
    """Extrait le contenu structuré d'un clone (matière première de relecture)."""
    txt = path.read_text(encoding="utf-8")
    mtask = CLONE_RX.search(path.name)
    mdate = re.search(r"-(\d{8})-", path.name)
    # Lignée : « 20ᵉ de la lignée » / « (Tasks 104→107), 20ᵉ » etc.
    mlignee = re.search(r"(\d+)[ᵉ]\s", txt)
    # Fenêtre worklog §1 : lignes « | N | date | Task ... | »
    fenetre = re.findall(r"^\|\s*(\d+)\s*\|", txt, re.M)
    fenetre_uniq = sorted({int(n) for n in fenetre})
    # Drifts §3.5 : « | TYPE | avant → après | réf | »
    drifts = re.findall(
        r"^\|\s*([A-ZÉÈ]+[A-Z ]*)\s*\|([^|]+→[^|]+)\|([^|]+)\|\s*$", txt, re.M
    )
    drifts_types = [d[0].strip() for d in drifts]
    # Directives §3 : lignes « **Décisions propriétaire (directives)** : ... »
    directives = []
    for m in re.finditer(r"\(D-(\d+)\)\s*([^;·]+)", txt):
        directives.append(f"D-{m.group(1)}: {m.group(2).strip()[:120]}")
    # Scellage — variantes réelles : « Scellage : 8/8 PASS », « Scellement :
    # 8/8 S1-S8 PASS », « Verdict clone-chat : 8/8 PASS — scellé », « 8/8
    # checks S1-S8 ». Ne PAS prendre les fractions voisines (54/54 SHA,
    # 111/112 integrity…) : la ligne doit porter scell|S1-S8 PASS ; 8/8 prioritaire.
    # Format antérieur (v2.0.x, ex. task73 : clôture §5 Worklog sans fraction) :
    # « sans-fraction ».
    scellage = "sans-fraction (format antérieur)"
    candidats: list[str] = []
    for line in txt.splitlines():
        if re.search(r"scell", line, re.I) or re.search(r"S1-S8\s+PASS|PASS[^.\n]{0,12}S1-S8|checks S1-S8", line, re.I):
            mfrac = re.search(r"(\d)\s*/\s*(\d)", line)
            if mfrac:
                candidats.append(f"{mfrac.group(1)}/{mfrac.group(2)}")
    for frac in ("8/8", "7/8", "6/8", "5/5", "4/4", "3/3", "2/2", "1/1"):
        if frac in candidats:
            scellage = frac
            break
    if scellage.startswith("sans-fraction") and candidats:
        scellage = candidats[0]
    # Bugs §3 : lignes « N. **Fx ...** »
    bugs = re.findall(r"^\d+\.\s*\*{0,2}(F\d+)[^:]*:\s*([^;]{10,140})", txt, re.M)
    return {
        "fichier": path.name,
        "task_clone": (f"T{mtask.group(1)}" if mtask else "—"),
        "date_nom": (mdate.group(1) if mdate else "—"),
        "position_lignee": (int(mlignee.group(1)) if mlignee else None),
        "fenetre_worklog": (
            f"s{fenetre_uniq[0]}-s{fenetre_uniq[-1]}" if fenetre_uniq else "—"
        ),
        "suites_listees": fenetre_uniq,
        "nb_drifts": len(drifts),
        "drifts_types": drifts_types,
        "directives": directives[:8],
        "bugs": [f"{b[0]}: {b[1].strip()[:110]}" for b in bugs[:6]],
        "scellage": scellage,
        "octets": len(txt.encode("utf-8")),
    }


def stats_globales(suites: list[dict], clones: list[dict]) -> dict:
    marqueurs = Counter()
    for s in suites:
        for m in set(s["marqueurs"]):
            marqueurs[m] += 1
    e15_nums = [
        int(m.group(1))
        for m in re.finditer(r"(\d+)ᵉ exposition", WORKLOG.read_text(encoding="utf-8"))
    ]
    drifts_tous = Counter()
    for c in clones:
        for t in c["drifts_types"]:
            drifts_tous[t.strip()] += 1
    return {
        "nb_suites": len(suites),
        "octets_total": sum(s["octets"] for s in suites),
        "suites_avec_marqueur": dict(marqueurs),
        "e15_max_constatee": max(e15_nums) if e15_nums else 0,
        "premiere_suite": f"{suites[0]['date']} s{suites[0]['suite']}",
        "derniere_suite": f"{suites[-1]['date']} s{suites[-1]['suite']}",
        "clones_lus": len(clones),
        "clones_octets": sum(c["octets"] for c in clones),
        "drifts_par_type": dict(drifts_tous),
        "scellages": {c["fichier"]: c["scellage"] for c in clones},
    }


def main() -> int:
    suites = parse_suites()
    if not suites:
        print("FAIL worklog illisible")
        return 2
    clones_paths = sorted(DOWNLOAD.glob("clone-chat-*.md"))
    clones = [lire_clone(p) for p in clones_paths]
    illisibles = [c["fichier"] for c in clones if c["scellage"] == "?"]
    sans_fraction = [
        c["fichier"] for c in clones
        if c["scellage"].startswith("sans-fraction")
    ]
    num = [s["suite"] for s in suites]
    trous = [n for n in range(min(num), max(num) + 1) if n not in num]
    rapport = {
        "task": "108-relecture-blocs-clones",
        "stats_globales": stats_globales(suites, clones),
        "continuite_suites": {"min": min(num), "max": max(num),
                              "trous": trous, "nb": len(num)},
        "blocs_par_jour": blocs_par_jour(suites),
        "clones": clones,
        "details_suites": [
            {"suite": s["suite"], "date": s["date"],
             "titre": s["titre"][:160], "octets": s["octets"],
             "marqueurs": sorted(set(s["marqueurs"]))}
            for s in suites
        ],
    }
    out = DOWNLOAD / "task108-extraction-blocs.json"
    out.write_text(
        json.dumps(rapport, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    sg = rapport["stats_globales"]
    print(json.dumps({
        "suites": sg["nb_suites"], "trous": trous,
        "e15_max": sg["e15_max_constatee"],
        "premiere": sg["premiere_suite"], "derniere": sg["derniere_suite"],
        "clones_lus": sg["clones_lus"],
        "octets_clones": sg["clones_octets"],
        "blocs_jours": len(rapport["blocs_par_jour"]),
        "clones_scellage_inconnu": illisibles,
        "clones_format_anterieur": sans_fraction,
        "drifts_par_type": sg["drifts_par_type"],
    }, ensure_ascii=False, indent=2))
    print(f"rapport: {out}")
    return 0 if (not trous and not illisibles) else 1


if __name__ == "__main__":
    sys.exit(main())
