#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 102 — Extraction mécanique des blocs du worklog (relecture intégrale, item a).

Découpe le worklog par suites (« ## DATE (suite N, ...) — TITRE »), agrège par
blocs chronologiques (par jour), et produit des statistiques : verdicts
PASS/FAIL, expositions E15, pendances, livrables download/, commits.
Sortie JSON déterministe (aucune horloge) + résumé lisible.
"""

# ⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.40)
# SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
# Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
# Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
# Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
# Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
# Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

HOST = Path("/home/z/my-project")
WORKLOG = HOST / "KNOWLEDGE-repo" / "worklog.md"
DOWNLOAD = HOST / "download"

SUITE_RX = re.compile(
    r"^## (?P<date>\d{4}-\d{2}-\d{2}) \(suite (?P<n>\d+),(?P<reste>.*)$"
)


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
                ("PASS", r"\bALL PASS\b|\bPASS STRICT\b|PASS 4/4|PASS\b"),
                ("FAIL", r"\bFAIL\b"),
                ("E15", r"E15\s*:|\dᵉ exposition|exposition consignée"),
                ("pendance", r"[Pp]endance"),
                ("PUSH", r"\bPUSH\b"),
                ("clone", r"clone-chat"),
                ("arbitre", r"certification-complete|verify-correct-work|triggers"),
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
            blocs[d] = {"jour": d, "suites": [], "bornes": None, "taches": []}
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


def stats_globales(suites: list[dict]) -> dict:
    marqueurs = Counter()
    for s in suites:
        for m in set(s["marqueurs"]):
            marqueurs[m] += 1
    e15_nums = []
    for m in re.finditer(r"(\d+)ᵉ exposition", WORKLOG.read_text(encoding="utf-8")):
        e15_nums.append(int(m.group(1)))
    return {
        "nb_suites": len(suites),
        "octets_total": sum(s["octets"] for s in suites),
        "suites_avec_marqueur": dict(marqueurs),
        "e15_max_constatee": max(e15_nums) if e15_nums else 0,
        "premiere_suite": f"{suites[0]['date']} s{suites[0]['suite']}" if suites else "—",
        "derniere_suite": f"{suites[-1]['date']} s{suites[-1]['suite']}" if suites else "—",
    }


def main() -> int:
    suites = parse_suites()
    if not suites:
        print("FAIL worklog illisible")
        return 2
    num = [s["suite"] for s in suites]
    trous = [n for n in range(min(num), max(num) + 1) if n not in num]
    clones = sorted(p.name for p in DOWNLOAD.glob("clone-chat-*.md"))
    rapport = {
        "task": "102-relecture-blocs",
        "stats_globales": stats_globales(suites),
        "continuite_suites": {"min": min(num), "max": max(num),
                              "trous": trous, "nb": len(num)},
        "blocs_par_jour": blocs_par_jour(suites),
        "clones": {"nb": len(clones), "fichiers": clones},
        "details_suites": [
            {"suite": s["suite"], "date": s["date"],
             "titre": s["titre"][:160], "octets": s["octets"]}
            for s in suites
        ],
    }
    out = HOST / "download" / "task102-extraction-blocs.json"
    out.write_text(json.dumps(rapport, ensure_ascii=False, indent=2) + "\n",
                   encoding="utf-8")
    sg = rapport["stats_globales"]
    print(json.dumps({
        "suites": sg["nb_suites"], "trous": trous,
        "e15_max": sg["e15_max_constatee"],
        "premiere": sg["premiere_suite"], "derniere": sg["derniere_suite"],
        "clones": len(clones),
        "blocs_jours": len(rapport["blocs_par_jour"]),
    }, ensure_ascii=False, indent=2))
    print(f"rapport: {out}")
    return 0 if not trous else 1


if __name__ == "__main__":
    sys.exit(main())
