#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 21 — F1 : inscription de la décision de campagne au registre KB (C006 + structurels).
Idempotent : saute si l'entrée « Task 21 — » existe déjà."""
from pathlib import Path

KB = Path("/home/z/my-project/ecosystem/skills/KNOWLEDGE.md")
text = KB.read_text(encoding="utf-8")
if "Task 21 — campagne d'extension V0-V6" in text:
    print("Entrée Task 21 déjà présente — idempotent, aucune action.")
    raise SystemExit(0)

ANCHOR = "## Décisions d'architecture (corrige-ecosysteme v2.0.0)\n"
ENTRY = (
    "\n- **Task 21 — campagne d'extension V0-V6 (fin P2 : Description Optimization pass 2 + "
    "statut des cas structurels + décision C006)** : suite campagne interrompue 2026-10-02 "
    "(P0 arbitre V6 créé, P2 12/17, P4 partiel, P5 67/67, P3 9/26 votes réels) — pass 2 "
    "zéro-API (protocole A10/A14, R2) : correct-work 7/7 (radical 'plan' issu de « gen-plan » "
    "éliminé — genplan), script-creator 7/7 (« nouveau » et « évals » retirés de la description), "
    "prompt-engineering 6/7 (itération/trigger_evals retirés de desc + tag 'iteration' retiré — "
    "les tags injectent des radicaux ; montée 2.1.0→2.2.0 ; script-creator 1.0.0→1.1.0 ; "
    "correct-work PM-couplé sans bump) ; re-jeu V6 : 18/26 max. **Cas structurels consignés "
    "(radical du NOM du skill, inréparables par description — réserve 1 Task 19, désambiguïsation "
    "déléguée voie L, plan §6)** : agent-creator ('agent'), audio-metadata ('audio'), pdf-llm "
    "('pdf' ×3), prompt-engineering ('prompt'), script-mon-ecosysteme-infrastructure ('ecosystem', "
    "cas ambigu voie L 0.667 → révision du cas renvoyée au propriétaire), script-reviewer "
    "('script'), skills-inventory ('skill' ×2). **C006 (version-management, zh)** : décision (b) "
    "appliquée par défaut — voie L seule assumée et consignée (voie M structurellement aveugle "
    "au chinois, stemmer français ; voie L réelle P3 : positifs OUI 3/3, négatifs 0.0) ; "
    "réversible vers (a) evals français additionnels sur directive du propriétaire. "
    "KO-L004 recalibré (integrity 2.2.0/1.1.0) ; KB Description = miroir frontmatter ×3.\n"
)

lines = text.splitlines(keepends=True)
idx = lines.index(ANCHOR)
lines.insert(idx + 1, ENTRY)
KB.write_text("".join(lines), encoding="utf-8")
print("Décision Task 21 inscrite au registre KB (C006 + structurels).")
