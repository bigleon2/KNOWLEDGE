#!/usr/bin/env python3
# PROVENANCE: session B13-r6 (N27) — audit-provenance v1.0.0, directive trace 1a0df36f356c3add ; artefact orphelin documente idempotemment
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.5.2)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}}
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.

Arbitre correct-work — 16 checks post-install + validation de rapports
Usage :
  python3 scripts/verify-correct-work.py                 # 16 checks sur le skill correct-work
  python3 scripts/verify-correct-work.py <rapport.md>    # valide un rapport correct-work (§2.4)
Version : 1.0.0 (corrige-ecosysteme v2.0.0, Phase G1)
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CW = ROOT / "skills" / "correct-work"
KB = ROOT / "skills" / "KNOWLEDGE.md"

def run_checks():
    checks, passed = [], 0
    def chk(label, cond):
        checks.append((label, bool(cond)))
        return bool(cond)

    sm = CW / "SKILL.md"
    content = sm.read_text(encoding="utf-8") if sm.exists() else ""
    parts = content.split("---", 2)
    fm = parts[1] if len(parts) >= 3 else ""

    chk("01 SKILL.md présent", content != "")
    chk("02 frontmatter YAML présent", len(parts) >= 3)
    chk("03 champs frontmatter (name/version/category/language/description)",
        all(f in fm for f in ("name:", "version:", "category:", "language:", "description:")))
    kb = KB.read_text(encoding="utf-8") if KB.exists() else ""
    m_kb = re.search(r"## correct-work v([\d.]+)", kb)
    m_fm = re.search(r"version:\s*([\d.]+)", fm)
    chk("04 version KB == version SKILL.md", bool(m_kb and m_fm and m_kb.group(1) == m_fm.group(1)))
    chk("05 §0 Contexte Système / Règle zéro présent",
        ("§0 — Contexte Système" in content) or ("§0 — RÈGLE ZÉRO" in content) or ("§0 — Règle zéro" in content))
    chk("06 3 modes documentés (PROJET/CIBLE/DIRECT)",
        all(m in content for m in ("PROJET", "CIBLE", "DIRECT")))
    chk("07 5 étapes présentes", all(s in content for s in
        ("Plan d'actions", "Erreurs et omissions", "Structure et conflits", "Interactions", "Cohérence")))
    chk("08 format de rapport §2.4 (verdicts)", "Verdict" in content and "PASS AVEC RÉSERVES" in content)
    chk("09 sévérités S1-S4", all(s in content for s in ("S1", "S2", "S3", "S4")))
    chk("10 checklists §10 (Mode PROJET)", "### §10.1 Mode PROJET" in content)
    chk("11 §3.2 cross-references décentralisées", "§3.2 Règles de cross-references" in content)
    chk("12 arbitre auto-référencé (ce script)", (CW / "scripts" / "verify-correct-work.py").exists())
    ev, tr = CW / "evals" / "evals.json", CW / "evals" / "trigger_evals.json"
    ok_ev = ok_tr = False
    try:
        ok_ev = isinstance(json.loads(ev.read_text(encoding="utf-8")), (list, dict))
    except Exception:
        pass
    try:
        d_tr = json.loads(tr.read_text(encoding="utf-8"))
        ok_tr = isinstance(d_tr, list) and all("query" in x and "should_trigger" in x for x in d_tr)
    except Exception:
        pass
    chk("13 evals/evals.json valide", ok_ev)
    chk("14 evals/trigger_evals.json valide", ok_tr)
    chk("15 dépendance gen-plan >= 3.7.0 déclarée", bool(re.search(r"gen-plan\s*\n?\s*version:\s*[\"]?>=?\s*3\.[7-9]", fm) or re.search(r"gen-plan.*?>=\s*v?3\.[7-9]", content, re.S)))
    chk("16 format worklog documenté", "Task ID" in content and "Stage Summary" in content)

    npass = sum(1 for _, ok in checks if ok)
    for label, ok in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}] {label}")
    print(f"\nRésultat : {npass}/{len(checks)} PASS")
    return npass, len(checks)

def check_report(path):
    txt = Path(path).read_text(encoding="utf-8")
    checks = {
        "Métadonnées (Mode/Date/Cible)": all(k in txt for k in ("Mode", "Date", "Cible")),
        "Étape 1 — Plan": "Étape 1" in txt,
        "Étape 2 — Erreurs et omissions": "Étape 2" in txt,
        "Étape 3 — Structure et conflits": "Étape 3" in txt,
        "Étape 4 — Interactions": "Étape 4" in txt,
        "Étape 5 — Cohérence": "Étape 5" in txt,
        "Résumé (problèmes/corrections)": "Résumé" in txt,
        "Verdict explicite": bool(re.search(r"Verdict\*\*\s*:\s*\*{0,2}(PASS|PASS AVEC RÉSERVES|FAIL)", txt)) or bool(re.search(r"Verdict\s*:\s*\*{0,2}(PASS|PASS AVEC RÉSERVES|FAIL)", txt)),
    }
    npass = sum(1 for ok in checks.values() if ok)
    for k, ok in checks.items():
        print(f"  [{'PASS' if ok else 'FAIL'}] {k}")
    print(f"\nRapport : {npass}/{len(checks)} PASS")
    return npass, len(checks)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        npass, total = check_report(sys.argv[1])
    else:
        npass, total = run_checks()
    sys.exit(0 if npass == total else 1)
