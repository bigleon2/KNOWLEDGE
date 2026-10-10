#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 21 — F3 : statuts « MESURÉ » §5 pour les skills effectivement mesurés 2 voies (P3 + F3).
Idempotent : n'ajoute la ligne que si absente. Les skills encore non mesurés (quota 429)
ne sont PAS marqués — KO-L007 : jamais de statut sans fait de matérialisation."""
import json
from pathlib import Path

BASE = Path("/home/z/my-project/ecosystem")
REP = BASE / "scripts" / "baseline-a2-all-report.json"

measured = json.loads(REP.read_text(encoding="utf-8")).get("skills", {})
print(f"skills mesurés (fait matériel) : {len(measured)} -> {sorted(measured)}")

TEMPLATE = ("\n> **Baseline A2 (Task 21 P3/F3, 2026-10-03)** : MESURÉE 2 voies (voie mécanique "
            "SHARED §7 v2 + voie L 3 runs réels) — score baseline {score} (nulls : {nulls}) ; "
            "détail par cas : `scripts/baseline-a2-all-report.json` ; cas structurels consignés au "
            "registre KB (décision Task 21) ; re-mesure idempotente `--skip-done` armée pour les "
            "nulls 429 restants.\n")

done = []
for name, info in measured.items():
    smd = BASE / "skills" / name / "SKILL.md"
    if not smd.exists():
        print(f"[KO] {name} : SKILL.md absent"); continue
    t = smd.read_text(encoding="utf-8")
    if "Baseline A2 (Task 21 P3/F3" in t:
        done.append(f"[DÉJÀ] {name}")
        continue
    line = TEMPLATE.format(score=info.get("score_baseline"), nulls=info.get("votes_null", 0))
    if "## §5" in t and "## §6 — TRAÇABILITÉ" in t:
        t = t.replace("## §6 — TRAÇABILITÉ", line.rstrip("\n") + "\n\n## §6 — TRAÇABILITÉ", 1)
    else:
        # skills hors-template : section dédiée en fin de fichier
        t = t.rstrip("\n") + ("\n\n---\n\n## Baseline A2 — statut de mesure\n"
                              + line.replace("\n> ", "> ", 1))
    smd.write_text(t, encoding="utf-8")
    done.append(f"[OK] {name} statut MESURÉ ({info.get('score_baseline')})")

print("\n".join(done))
