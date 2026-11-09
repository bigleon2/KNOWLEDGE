#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 21 — F1 : synchronisation KB (miroir descriptions pass 2 + calibration).
Précédent pass 1 : la ligne Description du KB reflète la description frontmatter du SKILL.md,
suivie d'une ligne « Dernière calibration ». Idempotent (échec si motif attendu absent)."""
import re
import sys
from pathlib import Path

KB = Path("/home/z/my-project/ecosystem/skills/KNOWLEDGE.md")

DESCS = {
    "correct-work": (
        "Skill de vérification et correction du travail réalisé (erreurs, omissions, incohérences). "
        "5 étapes, 4 modes (PROJET/CIBLE/DIRECT/AVEUGLE), support multi-cibles, couplage genplan "
        "OBLIGATOIRE (dernière version installée) à l'Étape 1, intégration KB (Registre, kb_path, "
        "--kb-skill), matrice de décision agent/skill (statique + dynamique KB), métriques de "
        "performance. Contrôler la cohérence avant de livrer ce que tu viens de produire."),
    "prompt-engineering": (
        "Skill d'optimisation fine des prompts complexes : rédaction, restructuration (restructure, "
        "restructurer), évaluation et validation des déclencheurs officiels des artefacts de prompts "
        "(PMs, SKILL.md). Spécialise la méthode prompt-engineering (méthode-mère : gen-plan ; source "
        "de vérité : SHARED §7) ; matérialisé le 2026-09-06 (recommandation de session, §5.2)."),
    "script-creator": (
        "Créer et modifier les scripts de l'écosystème (arbitres, collecteurs, outils de vérification "
        "stdlib) avec critères de succès et tests mécaniques intégrés. Utiliser lorsque "
        "l'utilisateur souhaite créer un script, corriger ou améliorer un script existant, rendre un "
        "check certifiable exécutable localement, ou garantir l'idempotence (rejeu ×2 sans effet) "
        "d'un outil. Structure, conventions de description héritées de skill-creator ; objectif "
        "principal : la création ou la modification des scripts (et non des skills)."),
}

CAL = ("Dernière calibration : 2026-10-03 (Task 21 F1 — P2 pass 2 : chirurgies incidents-FP "
       "locaux radicaux-description + tag iteration retiré (prompt-engineering) ; validation "
       "locale zéro-API via arbitre V6 ; cas structurels radical-du-nom consignés réserve 1 ; "
       "montées v2.2.0 (prompt-engineering) et v1.1.0 (script-creator) ; KO-L004 recalibré)")

lines = KB.read_text(encoding="utf-8").splitlines()
headers = {}
for i, l in enumerate(lines):
    m = re.match(r"^## (correct-work|prompt-engineering|script-creator) ", l)
    if m:
        headers[m.group(1)] = i

# versions dans les en-têtes
for i, l in enumerate(lines):
    lines[i] = l.replace("## prompt-engineering v2.1.0", "## prompt-engineering v2.2.0") \
                .replace("## script-creator v1.0.0", "## script-creator v1.1.0")

fail = 0
for skill, desc in DESCS.items():
    if skill not in headers:
        print(f"[KO] section absente : {skill}"); fail = 1; continue
    start = headers[skill]
    end = next((j for j in range(start + 1, len(lines)) if lines[j].startswith("## ")), len(lines))
    desc_idx = next((j for j in range(start, end) if lines[j].startswith("- **Description** :")), None)
    if desc_idx is None:
        print(f"[KO] ligne Description absente : {skill}"); fail = 1; continue
    lines[desc_idx] = f"- **Description** : {desc}"
    cal_idx = next((j for j in range(desc_idx + 1, end)
                    if lines[j].startswith("- **Dernière calibration** :")), None)
    cal_line = f"- **{CAL}**"
    if cal_idx is None:
        lines.insert(desc_idx + 1, cal_line)
    else:
        lines[cal_idx] = cal_line
    print(f"[OK] {skill} : Description miroir + calibration (section l.{start+1})")

if not fail:
    KB.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("KNOWLEDGE.md synchronisé.")
sys.exit(fail)
