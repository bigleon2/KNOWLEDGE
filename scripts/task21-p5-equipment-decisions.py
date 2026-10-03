#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Task 21 — campagne P5 : décisions d'équipement V0 (trigger_evals) pour les 67 skills
non équipés. La phase ne crée PAS les fichiers trigger_evals (lots à armer) : elle
CONSIGNE la décision skill par skill (gate P5 du plan d'extension), selon une règle
de routage documentée :

- ÉQUIPER-P1 : capacités PLATEFORME génériques (supports/verbes transverses : documents,
  médias, web, code) — collisions de routage probables, équipement prioritaire.
- ÉQUIPER-P2 : compétences MÉTIER à vocabulaire discriminant propre (auto-déclenchement
  déjà fiable) — équipement de normalisation, second lot.
- NON-APPLICABLE : COLLECTEURS/PIPELINES épinglés à une source ou à un workflow scripté
  (aminer-*, gaokao-*, ai-news-collectors, trackers, recherche guidée) — déclenchement
  assuré par l'orchestration gen-plan E5, pas par la description.
"""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
SKILLS = BASE / "skills"

P1_PLATFORM = {
    "ASR", "TTS", "LLM", "VLM", "agent-browser", "charts", "coding-agent", "docx", "pdf",
    "pptx", "xlsx", "web-search", "web-reader", "image-edit", "image-generation",
    "image-search", "image-understand", "video-generation", "video-understand",
    "fullstack-dev", "ui-ux-pro-max", "visual-design-foundations", "design",
}
NON_APPLICABLE = {
    "ai-news-collectors", "aminer-academic-search", "aminer-daily-paper",
    "aminer-deep-search", "aminer-free-academic", "gaokao-collect-student-info",
    "gaokao-fetch-volunteers", "gaokao-generate-report", "gaokao-recommend-majors",
    "gaokao-recommend-schools", "qingyan-research", "auto-target-tracker",
    "job-intent-tracker", "multi-search-engine", "skill-finder-cn",
}
MOTIFS = {
    "collector": "collecteur/pipeline épinglé à une source — déclenchement par orchestration gen-plan E5",
}


def decide(name):
    if name in P1_PLATFORM:
        return "ÉQUIPER-P1", "capacité plateforme transverse — collisions de routage probables"
    if name in NON_APPLICABLE:
        return "NON-APPLICABLE", MOTIFS["collector"]
    return "ÉQUIPER-P2", "compétence métier à vocabulaire discriminant propre — normalisation"


def main():
    rows = []
    for sdir in sorted(SKILLS.iterdir()):
        if not sdir.is_dir() or sdir.name.startswith(("_", ".")) or sdir.name == "@mon-ecosysteme":
            continue
        if (sdir / "evals" / "trigger_evals.json").exists():
            continue
        status, motif = decide(sdir.name)
        rows.append({"skill": sdir.name, "decision": status, "motif": motif,
                     "skil_md_present": (sdir / "SKILL.md").exists()})

    counts = {}
    for r in rows:
        counts[r["decision"]] = counts.get(r["decision"], 0) + 1
    out = BASE / "scripts" / "task21-p5-equipment-decisions.json"
    out.write_text(json.dumps({
        "date": "2026-10-03",
        "task": "Task 21 — campagne P5 : décisions d'équipement V0 consignées (gate P5)",
        "regle": "P1 plateforme / P2 métier / NON-APPLICABLE collecteurs (motifs en ligne)",
        "n_decisions": len(rows),
        "compte": counts,
        "decisions": rows,
    }, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Décisions consignées : {len(rows)} — {counts}")
    print(f"JSON : {out}")


if __name__ == "__main__":
    main()
