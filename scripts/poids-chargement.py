#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.33)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).
"""

# -*- coding: utf-8 -*-
"""poids-chargement.py — Arbitre de poids de chargement (R1 — progressive disclosure).

Recommandation R1 de l'étude de faisabilité Task 70 (directive propriétaire
2026-11-08, Task 71 G3) : le goulot réel de l'écosystème est le budget #token,
pas les entrées-sorties fichiers. Cet arbitre mesure, pour chaque skill, le
poids de chargement (SKILL.md + references/) et rend un verdict mécanique :

  OK        : SKILL.md < 12 Kio        — lecture intégrale sans précaution
  LOURD     : 30 Kio <= SKILL.md < 60 Kio — lecture ciblée conseillée (§0 d'abord)
  CRITIQUE  : SKILL.md >= 60 Kio       — lecture ciblée OBLIGATOIRE (§0 + sommaire,
                                          references/ chargées à la demande uniquement)

Estimation #token : caractères / 4 (heuristique standard des токenizers BPE
pour le texte latin/UTF-8 français — l'étude Task 70 §3 l'utilise comme borne).

Usage :
    python3 scripts/poids-chargement.py                 # mesure + verdict + table
    python3 scripts/poids-chargement.py --json          # sortie JSON seule
    python3 scripts/poids-chargement.py --top N         # top N seulement (déf. 10)
    python3 scripts/poids-chargement.py --selftest      # 10 checks mécaniques (fixture temporaire)

Codes retour : 0 = mesure rendue ; 1 = selftest FAIL ; 3 = usage invalide.
Python stdlib uniquement — idempotent (re-jeu = sortie identique).
"""

import json
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
SKILLS = BASE / "skills"

SEUIL_OK_KIO = 12.0
SEUIL_LOURD_KIO = 30.0
SEUIL_CRITIQUE_KIO = 60.0

VERSION = "1.0.0"


def kio(n: float) -> float:
    return round(n / 1024.0, 1)


def mesure_skill(dossier: Path) -> dict | None:
    """Mesure un dossier skill : SKILL.md + references/ récursif."""
    skill_md = dossier / "SKILL.md"
    if not skill_md.is_file():
        return None
    octets_md = skill_md.stat().st_size
    refs = dossier / "references"
    octets_refs = 0
    n_refs = 0
    if refs.is_dir():
        for f in sorted(refs.rglob("*")):
            if f.is_file():
                octets_refs += f.stat().st_size
                n_refs += 1
    if octets_md >= SEUIL_CRITIQUE_KIO * 1024:
        verdict = "CRITIQUE"
    elif octets_md >= SEUIL_LOURD_KIO * 1024:
        verdict = "LOURD"
    elif octets_md < SEUIL_OK_KIO * 1024:
        verdict = "OK"
    else:
        verdict = "INTERMÉDIAIRE"  # 12-30 Kio : ni OK strict, ni LOURD — non bloquant
    return {
        "skill": dossier.name,
        "kio_skill_md": kio(octets_md),
        "tokens_estimes": octets_md // 4,
        "kio_references": kio(octets_refs),
        "fichiers_references": n_refs,
        "kio_total": kio(octets_md + octets_refs),
        "verdict": verdict,
    }


def mesurer(racine: Path) -> list:
    res = []
    for dossier in sorted(racine.iterdir()):
        if not dossier.is_dir() or dossier.name.startswith("@"):
            continue
        m = mesure_skill(dossier)
        if m:
            res.append(m)
    res.sort(key=lambda r: (-r["kio_skill_md"], r["skill"]))
    return res


def table_md(mesures: list, top: int | None = None) -> str:
    lignes = ["| Rang | Skill | SKILL.md (Kio) | #token estimés | references/ (Kio, nb) | Total (Kio) | Verdict |",
              "|---|---|---|---|---|---|---|"]
    for i, m in enumerate(mesures[: (top or len(mesures))], 1):
        lignes.append("| %d | %s | %s | %s | %s / %d | %s | %s |" % (
            i, m["skill"], m["kio_skill_md"], m["tokens_estimes"],
            m["kio_references"], m["fichiers_references"], m["kio_total"], m["verdict"]))
    return "\n".join(lignes)


def selftest() -> int:
    """10 checks mécaniques sur fixture temporaire (jamais sur l'écosystème réel)."""
    tmp = Path(tempfile.mkdtemp(prefix="poids-chargement-selftest-"))
    ok = 0
    total = 0

    def check(nom: str, cond: bool):
        nonlocal ok, total
        total += 1
        print("  [%s] %s" % ("PASS" if cond else "FAIL", nom))
        if cond:
            ok += 1

    try:
        # fixture : 4 skills couvrant les 4 verdicts
        (tmp / "ok-skill").mkdir()
        (tmp / "ok-skill/SKILL.md").write_text("x" * 2048, encoding="utf-8")
        (tmp / "inter-skill").mkdir()
        (tmp / "inter-skill/SKILL.md").write_text("x" * (20 * 1024), encoding="utf-8")
        (tmp / "lourd-skill").mkdir()
        (tmp / "lourd-skill/SKILL.md").write_text("x" * (45 * 1024), encoding="utf-8")
        (tmp / "critique-skill").mkdir()
        (tmp / "critique-skill/SKILL.md").write_text("x" * (100 * 1024), encoding="utf-8")
        (tmp / "critique-skill/references").mkdir()
        (tmp / "critique-skill/references/a.md").write_text("y" * 5000, encoding="utf-8")
        (tmp / "critique-skill/references/sub").mkdir()
        (tmp / "critique-skill/references/sub/b.md").write_text("y" * 3000, encoding="utf-8")
        (tmp / "@archive").mkdir()          # dossier @ ignoré
        (tmp / "@archive/SKILL.md").write_text("z" * 999999, encoding="utf-8")
        (tmp / "sans-skill-md").mkdir()      # pas de SKILL.md → exclu

        ms = {m["skill"]: m for m in mesurer(tmp)}
        check("T1 : 4 skills mesurés (dossiers @ et sans SKILL.md exclus)", len(ms) == 4)
        check("T2 : verdict OK < 12 Kio", ms["ok-skill"]["verdict"] == "OK")
        check("T3 : verdict INTERMÉDIAIRE 12-30 Kio", ms["inter-skill"]["verdict"] == "INTERMÉDIAIRE")
        check("T4 : verdict LOURD 30-60 Kio", ms["lourd-skill"]["verdict"] == "LOURD")
        check("T5 : verdict CRITIQUE >= 60 Kio", ms["critique-skill"]["verdict"] == "CRITIQUE")
        check("T6 : #token estimés = caractères / 4", ms["ok-skill"]["tokens_estimes"] == 512)
        check("T7 : references/ récursif (2 fichiers, 8000 octets ≈ 7,8 Kio)",
              ms["critique-skill"]["fichiers_references"] == 2 and ms["critique-skill"]["kio_references"] == 7.8)
        check("T8 : total = SKILL.md + references",
              ms["critique-skill"]["kio_total"] == kio(100 * 1024 + 8000))
        # tri décroissant sur SKILL.md
        tri = [m["skill"] for m in mesurer(tmp)]
        check("T9 : tri décroissant du poids SKILL.md", tri[0] == "critique-skill" and tri[-1] == "ok-skill")
        # idempotence : 2 mesures successives identiques
        check("T10 : idempotence (2 exécutions → mesures identiques)", mesurer(tmp) == mesurer(tmp))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("SELFTEST : %d/%d PASS" % (ok, total))
    return 0 if ok == total else 1


def main() -> int:
    args = sys.argv[1:]
    if "--selftest" in args:
        return selftest()
    if "--help" in args or "-h" in args:
        print(__doc__)
        return 0
    top = None
    if "--top" in args:
        i = args.index("--top")
        top = int(args[i + 1]) if i + 1 < len(args) else 10
    mesures = mesurer(SKILLS)
    stats = {
        "nb_skills": len(mesures),
        "critique": sum(1 for m in mesures if m["verdict"] == "CRITIQUE"),
        "lourd": sum(1 for m in mesures if m["verdict"] == "LOURD"),
        "intermediaire": sum(1 for m in mesures if m["verdict"] == "INTERMÉDIAIRE"),
        "ok": sum(1 for m in mesures if m["verdict"] == "OK"),
    }
    if "--json" in args:
        print(json.dumps({"version": VERSION, "stats": stats, "mesures": mesures},
                         ensure_ascii=False, indent=2))
    else:
        print("Arbitre de poids de chargement v%s (R1 — progressive disclosure, étude Task 70)" % VERSION)
        print("Seuils : OK < 12 Kio · LOURD >= 30 Kio · CRITIQUE >= 60 Kio · #token ≈ caractères/4\n")
        print("Bilan : %d skills — %d OK · %d intermédiaires · %d LOURD · %d CRITIQUE\n"
              % (stats["nb_skills"], stats["ok"], stats["intermediaire"], stats["lourd"], stats["critique"]))
        print(table_md(mesures, top))
    return 0


if __name__ == "__main__":
    sys.exit(main())
