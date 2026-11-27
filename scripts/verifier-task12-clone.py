#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 12 — validation S1-S8 du 7ᵉ clone (clone-chat v2.0.2) → JSON de preuve."""
# ⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.47)
# Langue : FRANÇAIS exclusif (règle d'or n°6 gen-plan).

import json
import re
import subprocess
from pathlib import Path

PROJ = Path("/home/z/my-project")
REPO = PROJ / "KNOWLEDGE-repo"
CLONE = PROJ / "download/clone-session-web-220878ed-20261128-task12-optimisation-gen-plan.md"
OUT = PROJ / "scripts/task12-clone-report.json"

checks = []


def check(sid, nom, ok, preuve):
    checks.append({"id": sid, "nom": nom, "verdict": "PASS" if ok else "FAIL", "preuve": preuve})


t = CLONE.read_text(encoding="utf-8")

check("S1", "§0 Règle zéro + contexte matériel (origin/main 5acd9911, gen-plan v3.49.0, KO-L009, KPS Kubota)",
      all(k in t for k in ("RÈGLE ZÉRO", "5acd9911", "gen-plan v3.49.0", "KO-L009", "Kubota")),
      "contexte de reprise complet")
check("S2", "§1 chronologie complète (héritage 6 clones + fenêtre Task 12 + drifts 2 compressions)",
      "chaîne de clonage (6 clones" in t and "Task 12" in t and "2 compressions de contexte" in t,
      "héritage + fenêtre + drifts typés")
check("S3", "§2 inventaire des livrables (table non vide)",
      t.count("| `") >= 10 and "INVENTAIRE DES LIVRABLES" in t, "table ≥ 10 livrables")
check("S4", "§3 décisions tracées (D001-D011, 11 décisions)",
      len(re.findall(r"\| D0\d{2} \|", t)) == 11, "11 décisions numérotées")
check("S5", "§4 pendances/différés (table + CRITIQUE révocation PAT)",
      "PENDANCES PROPRIÉTAIRE" in t and "RÉVOCATION IMMÉDIATE" in t and "CRITIQUE" in t,
      "5 pendances + écarts consignés")
check("S5b", "§5 lignage (7ᵉ clone, drifts typés, auto-clonage)",
      "7ᵉ clone" in t and "auto-clonage" in t.lower() and "clone-chat" in t,
      "lignage + reprise recommandée")
motif = re.compile(r"github_pat_[A-Za-z0-9_]{20,}|ghp_[A-Za-z0-9]{20,}")
check("S7", "0 secret : aucun jeton (motif github_pat_/ghp_) dans le clone",
      not motif.search(t), "scan négatif")
check("S8", "Fichier non vide et structure clone-chat complète (§0-§5)",
      len(t) > 4000 and all(s in t for s in ("§0", "§1", "§2", "§3", "§4", "§5")),
      "6 sections présentes")
r = subprocess.run(["git", "-C", str(REPO), "log", "--oneline", "-3"], capture_output=True, text=True)
check("S6", "Commit miroir suite 168 présent au dépôt local (worklog Task 12)",
      "suite 168" in r.stdout, r.stdout.strip().splitlines()[0][:80] if r.stdout else "vide")

verdict = "PASS" if all(c["verdict"] == "PASS" for c in checks) else "FAIL"
rapport = {"tache": 12, "clone": "7ᵉ génération", "verdict": verdict,
           "total": "%d/%d PASS" % (sum(c["verdict"] == "PASS" for c in checks), len(checks)),
           "checks": checks}
OUT.write_text(json.dumps(rapport, ensure_ascii=False, indent=2), encoding="utf-8")
print("VERDICT CLONE S1-S8 : %s — %s" % (rapport["total"], verdict))
for c in checks:
    print("  [%s] %s %s" % (c["verdict"], c["id"], c["nom"]))
raise SystemExit(0 if verdict == "PASS" else 1)
