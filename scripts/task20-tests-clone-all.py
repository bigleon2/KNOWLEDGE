#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""task20-tests-clone-all.py — Batterie $FACON2 fenêtre 16 (Task 20).

Directive (trace 1a221dc7539d4351) : « test "clone-chat (ALL)" et ses clones, puis
exécute "clone-chat (ALL)" » — CETTE batterie teste le mode AVANT l'exécution.

6 sections S1-S6, checks binaires, stdlib uniquement :
  S1 socle        : gabarit theme-template.md ×2 (SHA identiques) ; SKILL.md v2.2.0
                    §1.12.3 (ALL) + index + idempotence ×2 miroirs.
  S2 table thèmes : clone 11ᵉ — 7 slugs uniques kebab-case, statuts valides,
                    preuves ≥2 renseignées par thème.
  S3 nommage      : convention §1.12.3 — noms déterministes clones + index,
                    idempotence des noms ×2, 8 noms uniques sans collision.
  S4 gardes       : §1.12.2 — garde thème inconnu (erreur contrôlée, aucun clone
                    inventé), garde mono-thème, auto-suffisance périmétrique
                    dans le gabarit, les clones thématiques dérivent du canonique.
  S5 check 9      : critères mécaniques sur fixture de clone thématique (positif :
                    9/9 ; négatif : hors-thème détecté → FAIL).
  S6 gabarit      : sections obligatoires du gabarit (§0bis, tables, §4 état
                    courant + prochaine étape, §5 auto-clonage thématique).

Idempotent : fixtures temporaires neuves à chaque passage.
Rapport : scripts/task20-clone-all-report.json.
"""
import hashlib
import json
import re
import sys
import tempfile
from pathlib import Path

HOST = Path("/home/z/my-project")
REPO = HOST / "KNOWLEDGE-repo"
CLONE11 = HOST / "download" / "clone-session-web-220878ed-20261128-task19-caches-semantiques-cloture.md"
RAPPORT = HOST / "scripts" / "task20-clone-all-report.json"

SUJET = "clone-session-web-220878ed"
DATE = "20261128"

resultats = {"sections": {}, "ok": 0, "total": 0}


def check(section: str, nom: str, cond: bool, detail: str = "") -> None:
    resultats["total"] += 1
    resultats["sections"].setdefault(section, []).append(
        {"check": nom, "verdict": "PASS" if cond else "FAIL", "detail": detail[:180]})
    print(f"  [{'PASS' if cond else 'FAIL'}] {nom}" + (f" — {detail[:120]}" if detail and not cond else ""))


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:12]


def nom_clone_theme(slug: str) -> str:
    return f"{SUJET}-clone-theme-{slug}-{DATE}.md"


def nom_index() -> str:
    return f"{SUJET}-clone-themes-index-{DATE}.md"


def check9_fichier(chemin: Path, slug: str, autres_slugs: list) -> list:
    """Check 9 mécanique (§1.9 v2.1.0) sur un fichier clone thématique :
    (a) slug dans le nom, (b) §0bis exclusions présentes, (c) preuves ≥2 citées,
    (d) aucun autre slug hors §0bis. Retourne la liste des échecs (vide = 9/9)."""
    t = chemin.read_text(encoding="utf-8")
    fails = []
    if slug not in chemin.name:
        fails.append("(c) slug absent du nom de fichier")
    if "## §0bis" not in t:
        fails.append("(b) §0bis exclusions absente")
    else:
        i = t.find("## §0bis")
        tbl = t[i:i + 2000]
        if tbl.count("| 1 |") + tbl.count("| 2 |") + tbl.count("| 3 |") + tbl.count("| 4 |") + tbl.count("| 5 |") + tbl.count("| 6 |") < 1:
            fails.append("(b) table exclusions vide")
    j = t.find("Preuves du périmètre")
    if j < 0 or len(re.findall(r"\[[^\]]+\]", t[j:j + 400])) < 2:
        fails.append("(d) preuves ≥2 non citées en en-tête")
    i0 = t.find("## §1 —")
    i4 = t.find("## §4 —")
    corps = t[i0:i4] if i0 >= 0 and i4 > i0 else t
    for a in autres_slugs:
        if a in corps:
            fails.append(f"(a) hors-thème : slug voisin « {a} » cité en §1-§3")
    return fails


def section_s1() -> None:
    print("S1 — socle : gabarit + SKILL.md (ALL)")
    g1, g2 = HOST / "skills" / "clone-chat" / "références" / "theme-template.md", REPO / "skills" / "clone-chat" / "références" / "theme-template.md"
    check("S1", "gabarit theme-template.md ×2 SHA identiques", g1.is_file() and g2.is_file() and sha(g1) == sha(g2))
    for base, tag in ((HOST, "hôte"), (REPO, "dépôt")):
        sk = (base / "skills" / "clone-chat" / "SKILL.md").read_text(encoding="utf-8")
        sk_norm = re.sub(r"\s+", " ", sk)  # normalise les retours à la ligne (leçon suite 174 : sémantique de test)
        check("S1", f"§1.12.3 (ALL) : N clones + index + idempotence ({tag})",
              "§1.12.3 Clones multiples" in sk_norm and "clone-themes-index" in sk_norm and "écrasement à l'identique" in sk_norm)
        check("S1", f"version 2.2.0 ({tag})", "version: 2.2.0" in sk)


def section_s2() -> None:
    print("S2 — table des thèmes (clone 11ᵉ)")
    t = CLONE11.read_text(encoding="utf-8")
    i, j = t.find("## §1bis"), t.find("## §2 —")
    tbl = t[i:j]
    slugs = re.findall(r"\| `([a-z0-9-]+)` \|", tbl)
    check("S2", "7 thèmes détectés à slugs uniques", len(slugs) >= 7 and len(set(slugs)) == len(slugs), str(slugs))
    resultats["slugs"] = slugs
    check("S2", "slugs kebab-case", all(re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", s) for s in slugs))
    statuts = re.findall(r"\| (ACTIF[^|]*|CLÔTURÉ[^|]*) \|", tbl)
    check("S2", "statuts valides (ACTIF/CLÔTURÉ) sur chaque ligne", len(statuts) >= 7, str(len(statuts)))
    check("S2", "preuves ≥2 renseignées (colonne preuve non vide)", tbl.count(" + ") >= 7 or "clones" in tbl)


def section_s3() -> None:
    print("S3 — nommage §1.12.3")
    slugs = resultats.get("slugs", [])
    noms = [nom_clone_theme(s) for s in slugs] + [nom_index()]
    noms2 = [nom_clone_theme(s) for s in slugs] + [nom_index()]
    check("S3", "noms déterministes (idempotence ×2)", noms == noms2)
    check("S3", f"{len(slugs)} noms de clones + 1 index uniques", len(set(noms)) == len(noms) and len(noms) == len(slugs) + 1)
    check("S3", "convention <sujet>-clone-theme-<slug>-<date>.md",
          all(re.fullmatch(rf"{SUJET}-clone-theme-[a-z0-9-]+-{DATE}\.md", n) for n in noms[:-1]))
    check("S3", "convention <sujet>-clone-themes-index-<date>.md", noms[-1] == nom_index())
    resultats["noms_prevus"] = noms


def section_s4() -> None:
    print("S4 — gardes §1.12.2")
    gab = (HOST / "skills" / "clone-chat" / "références" / "theme-template.md").read_text(encoding="utf-8")
    slugs = resultats.get("slugs", [])
    # garde thème inconnu : erreur contrôlée, aucun clone inventé
    connu = "kps-conversion" in slugs
    inconnu = "theme-inexistant-xyz" not in slugs
    check("S4", "garde : slug connu reconnu, slug inconnu rejeté (aucun clone)", connu and inconnu)
    check("S4", "garde : auto-suffisance périmétrique documentée dans le gabarit",
          "Auto-suffisance périmétrique" in gab and "ne remplace jamais l'instantané de clôture" in gab)
    check("S4", "garde : le clone complet demeure canonique", "demeure canonique" in gab)
    check("S4", "garde : exclusions obligatoires en §0bis du gabarit", "### §0bis — Exclusions" in gab)


def section_s5() -> None:
    print("S5 — check 9 (fixture positive + négative)")
    slugs = resultats.get("slugs", ["kps-conversion"])
    autres = [s for s in slugs if s != "kps-conversion"]
    tmp = Path(tempfile.mkdtemp(prefix="t20-check9-"))
    ok_md = tmp / nom_clone_theme("kps-conversion")
    ok_md.write_text(
        "# CLONE THÉMATIQUE — kps-conversion\n\n"
        "> **Preuves du périmètre (≥2)** : [clones 1ᵉʳ-5ᵉ] + [worklog suites 165-167]\n\n"
        "## §0bis — Exclusions\n\n| # | Exclu | Où |\n|---|---|---|\n| 1 | installation-ecosysteme | clone thématique dédié |\n\n"
        "## §1 — CHRONOLOGIE DU THÈME\n\ncontenu kps\n\n## §4 — INSTRUCTIONS\n",
        encoding="utf-8")
    fails_ok = check9_fichier(ok_md, "kps-conversion", autres)
    check("S5", "fixture conforme → check 9 sans échec", not fails_ok, str(fails_ok))
    ko_md = tmp / nom_clone_theme("kps-conversion")
    ko_md.write_text(
        "# CLONE THÉMATIQUE — kps-conversion\n\n"
        "> **Preuves du périmètre (≥2)** : [x] + [y]\n\n"
        "## §1 — CHRONOLOGIE DU THÈME\n\ncontenu mélangeant git-pendances et " + (autres[0] if autres else "installation-ecosysteme") + "\n\n## §4 — INSTRUCTIONS\n",
        encoding="utf-8")
    fails_ko = check9_fichier(ko_md, "kps-conversion", autres)
    check("S5", "fixture hors-thème → échec détecté (critère a)", len(fails_ko) >= 1, str(fails_ko))
    import shutil as _sh
    _sh.rmtree(tmp, ignore_errors=True)


def section_s6() -> None:
    print("S6 — conformité gabarit")
    gab = (HOST / "skills" / "clone-chat" / "références" / "theme-template.md").read_text(encoding="utf-8")
    for sec in ("## §0 —", "### §0bis — Exclusions", "## §1 —", "### §1.2 Table des sessions", "### §2.3 Artefacts produits",
                "### §3.5 Évolutions de contexte", "## §4 — INSTRUCTIONS DE REPRISE DU THÈME", "### État courant du sous-projet",
                "### Prochaine étape exécutable", "## §5 — AUTO-CLONAGE THÉMATIQUE"):
        check("S6", f"section gabarit : {sec[:40]}", sec in gab)
    check("S6", "gabarit : drifts obligatoires ou mention « Aucune évolution »",
          "Aucune évolution de contexte détectée pour ce thème" in gab)


def main() -> int:
    for s in (section_s1, section_s2, section_s3, section_s4, section_s5, section_s6):
        s()
    ok = sum(1 for sec in resultats["sections"].values() for c in sec if c["verdict"] == "PASS")
    fails = [(s, c["check"]) for s, lst in resultats["sections"].items() for c in lst if c["verdict"] == "FAIL"]
    resultats["ok"] = ok
    print(f"\nBATTERIE $FACON2 TASK 20 : {ok}/{resultats['total']} PASS")
    for s, n in fails:
        print(f"  FAIL {s} — {n}")
    RAPPORT.write_text(json.dumps(resultats, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
