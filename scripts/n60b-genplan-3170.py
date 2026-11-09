#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.6.0)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL

Arbitre n60b — Non-régression gen-plan v3.17.0 (N23-b/N28, session B13-r6,
directives traces 1a0dff290e1cef55 / 1a0df36f356c3add / 1a0df4d7831e4f49).

Leçon L003 appliquée : les invariants cibles (version 3.17.0) sont dérivés du
frontmatter installé (source de vérité) ; adaptation de n60-genplan-3160.py
(R2 — l'original n60 reste en place pour l'historique v3.16.0).

12 checks : frontmatter 3.17.0, blocs KO L001/L003/L004/L005, appariement
PATTERN global, hooks §1.2bis, hook E1-RES (n67-1 reconstitué), dépendance
knowledge-observer, 15 étapes E1-E15, observation-patterns.md, sections
§1.14/§1.15 + provenance.
"""
import json
import re
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent / "skills" / "gen-plan" / "SKILL.md"
RAPPORT_DIR = Path(__file__).resolve().parent.parent / "tmp" / "b13r5-install"
CIBLE_VERSION = "3.17.0"
KO_LECONS = ("L001", "L003", "L004", "L005")


def main():
    """Point d'entree : 12 checks non-regression gen-plan v3.17.0."""
    texte = SKILL.read_text(encoding="utf-8")
    checks = []

    def record(nom, ok, detail=""):
        checks.append({"check": nom, "verdict": "PASS" if ok else "FAIL",
                       "detail": detail})

    # 1. Version frontmatter (dérivée dynamiquement)
    m = re.search(r"^version:\s*([\d.]+)", texte, re.M)
    v = m.group(1) if m else "?"
    record("1. frontmatter version == 3.17.0 (cible N23-b/N28)",
           v == CIBLE_VERSION, f"version={v}")

    # 2-5. Blocs PATTERN KO ouverts ET fermés
    for lid in KO_LECONS:
        ouvre = f"<!-- PATTERN:KO-{lid}-v1.0.0 -->" in texte
        ferme = f"<!-- FIN-PATTERN:KO-{lid}-v1.0.0 -->" in texte
        record(f"{2 + len(checks)}. bloc PATTERN:KO-{lid} ouvert+fermé",
               ouvre and ferme)

    # 6. Appariement global des marqueurs PATTERN
    ouverts = re.findall(r"<!-- PATTERN:([A-Z0-9-]+)-v[\d.]+ -->", texte)
    fermes = re.findall(r"<!-- FIN-PATTERN:([A-Z0-9-]+)-v[\d.]+ -->", texte)
    apparies = sorted(ouverts) == sorted(fermes)
    record("6. marqueurs PATTERN appariés (ouvert == fermé)", apparies,
           f"{len(ouverts)} ouverts / {len(fermes)} fermés")

    # 7. Hooks patterns avancés §1.2bis
    record("7. hooks patterns §1.2bis (GEN-PLAN-HOOKS-PATTERNS)",
           "PATTERN:GEN-PLAN-HOOKS-PATTERNS-v1.0.0" in texte)

    # 8. Hook E1-RES (n67-1 reconstitué — N28)
    record("8. hook E1-RES (GEN-PLAN-HOOKS-E1-RES — n67-1 reconstitué)",
           "PATTERN:GEN-PLAN-HOOKS-E1-RES-v1.0.0" in texte
           and "n67-1" in texte and "resource-monitor" in texte)

    # 9. Dépendance knowledge-observer >= 1.0.0
    dep_ok = bool(re.search(r"skill:\s*knowledge-observer", texte)) and \
             bool(re.search(r"knowledge-observer[\s\S]{0,120}>=\s*1\.0\.0", texte))
    record("9. dépendance knowledge-observer >= 1.0.0 (E15)", dep_ok)

    # 10. 15 étapes E1-E15
    etapes = len(set(re.findall(r"\| E(\d+) \|", texte))
                 & set(str(i) for i in range(1, 16)))
    record("10. 15 étapes E1-E15 (§1.2)", etapes == 15, f"{etapes}/15")

    # 11. Référence observation-patterns.md mobilisée (hook E15)
    record("11. référence observation-patterns.md (hook E15)",
           "observation-patterns.md" in texte)

    # 12. Sections leçons §1.14/§1.15 + note de provenance
    record("12. sections §1.14/§1.15 + provenance B13",
           "§1.14" in texte and "§1.15" in texte
           and "reconstituées post-wipe" in texte)

    n_pass = sum(1 for c in checks if c["verdict"] == "PASS")
    verdict = "ALL PASS" if n_pass == len(checks) else "FAIL"
    rapport = {
        "arbitre": "n60b-genplan-3170",
        "session": "B13-r6",
        "traces": ["1a0df36f356c3add", "1a0df4d7831e4f49", "1a0dff290e1cef55"],
        "cible": CIBLE_VERSION,
        "checks": checks,
        "synthese": {"pass": n_pass, "total": len(checks), "verdict": verdict},
    }
    RAPPORT_DIR.mkdir(parents=True, exist_ok=True)
    (RAPPORT_DIR / "rapport-n60b.json").write_text(
        json.dumps(rapport, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"n60b-genplan-3170 : {n_pass}/{len(checks)} — {verdict}")
    for c in checks:
        if c["verdict"] == "FAIL":
            print(f"  FAIL: {c['check']} ({c['detail']})")
    return 0 if verdict == "ALL PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
