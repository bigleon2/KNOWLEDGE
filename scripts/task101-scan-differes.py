#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 101 — Scanner mécanique des différés consignés à corriger ($FACON).

Zones :
  VIVANTE    : worklog (3 dernières suites) · dernier plan · dernier rapport CW.
  HISTORIQUE : clones-chat scellés + plans/rapports antérieurs (R6 — non éditables,
               mentions = enregistrements datés).
  CODE       : scripts/*.py + skills/*/SKILL.md (marqueurs TODO/FIXME = candidats OPEN).

Classification par mots-clés de contexte :
  OPEN         : candidat réel à corriger (aucun marqueur de résolution/acteur)
  RESORBE      : résolution attestée dans la ligne (éteint/résorbé/fermé/done/branché)
  PROPRIETAIRE : rotation PAT / propriétaire
  AUTO         : automatique / cron / aux prochaines montées
  PROPOSITION  : proposition hors cadence (non une correction différée)
  HISTORIQUE   : zone scellée (mention datée, non item vivant)

Rapport JSON déterministe (aucune horloge) — selftest embarqué (--selftest).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HOST = Path("/home/z/my-project")
REPO = HOST / "KNOWLEDGE-repo"

# « différé » avec é aigu uniquement — exclut les verbes « diffèrent/diffère » (è grave)
MARKERS = re.compile(
    r"[Pp]endance|PENDANCE|différé|\[FUTURE\]|à corriger|reste à faire"
    r"|EN ATTENTE|TODO|FIXME|mission dédiée|reporté|PROCHAINE mission",
    re.IGNORECASE,
)

# Zone CODE : TODO/FIXME en MAJUSCULES uniquement (exclut « todo » = « tout » en pt-BR)
CODE_TODO_RX = re.compile(r"\bTODO\b|\bFIXME\b")
CODE_CORR_RX = re.compile(r"à corriger", re.IGNORECASE)

RESORBE_RX = re.compile(
    r"ÉTEINT|ÉTEINTE|RÉSORBÉ|résorbé|fermé|FERMÉE|done|DONE|branché|éteinte|éteints"
    r"|retiré|réparé|corrigé",
    re.IGNORECASE,
)
OWNER_RX = re.compile(r"propriétaire|PROPRIÉTAIRE|rotation PAT|PAT frais|révocation", re.IGNORECASE)
AUTO_RX = re.compile(r"\[AUTO|\[AUTOMATIQUE|automatique|cron 531684|prochaines montées|prochain tick", re.IGNORECASE)
PROPO_RX = re.compile(r"proposition (future|hors cadence)|HORS cadence", re.IGNORECASE)

ZONES_LIVE = [
    REPO / "worklog.md",                      # 3 dernières suites extraites
    HOST / "download" / "plan-task100-mission-f1.md",
    HOST / "download" / "rapport-cw-task99-bloc.md",
]
ZONES_HISTO = [
    HOST / "download" / "clone-chat-session-web-ecef7f80-20261115-task99.md",
    HOST / "download" / "plan-task99-verif-push-cw-bloc-clonechat-etat.md",
    HOST / "download" / "plan-task98-extinction-residus-triggers.md",
    HOST / "download" / "rapport-cw-task97-bloc.md",
    HOST / "download" / "plan-task96-rearmage-cron-triage-pendances.md",
]
ZONE_SCRIPTS = REPO / "scripts"
ZONE_SKILLS = REPO / "skills"


def last_suites(worklog_text: str, n: int = 3) -> str:
    """Extrait les n dernières suites du worklog (sections '## 2026-')."""
    idx = [m.start() for m in re.finditer(r"^## 2026-", worklog_text, re.MULTILINE)]
    if not idx:
        return worklog_text
    return worklog_text[idx[-n]:] if len(idx) >= n else worklog_text[idx[0]:]


def classify(line: str, zone: str) -> str:
    if zone == "HISTORIQUE":
        return "HISTORIQUE"
    if PROPO_RX.search(line):
        return "PROPOSITION"
    if OWNER_RX.search(line):
        return "PROPRIETAIRE"
    if AUTO_RX.search(line):
        return "AUTO"
    if RESORBE_RX.search(line):
        return "RESORBE"
    return "OPEN"


def scan_zone(path: Path, zone: str, only_tail: bool = False) -> list[dict]:
    hits: list[dict] = []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        hits.append({"zone": zone, "fichier": str(path), "erreur": str(exc), "classe": "OPEN"})
        return hits
    if only_tail:
        text = last_suites(text, 3)
    for lineno, line in enumerate(text.splitlines(), 1):
        if MARKERS.search(line):
            hits.append({
                "zone": zone,
                "fichier": path.name,
                "ligne": lineno,
                "extrait": line.strip()[:220],
                "classe": classify(line, zone),
            })
    return hits


def adjudiquer(item: dict) -> str:
    """Adjudication mécanique des candidats OPEN (règles ordonnées explicites)."""
    fichier = item.get("fichier", "")
    extrait = item.get("extrait", "")
    if fichier.startswith("skills/"):
        fichier = fichier[len("skills/"):]
    parent = fichier.split("/")[0]
    if "PROMPT-MAITRE" in fichier:
        return "ARCHIVE_R4"          # corpus prompts-maîtres versionné — R4, jamais édité
    if "references" in fichier.split("/"):
        return "DOC_METHODE"         # documentation de méthode (exemples littéraux)
    if parent in {"guizang-ppt", "team-okrs", "horizontal-craft", "design",
                  "dream-interpreter"}:
        return "PLATEFORME_NON_KB"   # règle d'or n°8 — copies informationnelles
    if "corriger manuellement en cas d'écart" in extrait or "drift à corriger" in extrait:
        return "METHODE"             # instruction utilisateur / description du comportement
    if "TODO(M7)" in extrait or "squelette" in extrait:
        return "TEMPLATE_CONCU"      # squelette généré par conception (mode M7)
    if "TODO list" in extrait:
        return "METHODE"             # description de fonctionnalité gen-plan
    if "E13" in extrait or "pendance consignée" in extrait:
        return "METHODE_ARBITRE"     # chaîne descriptive du propre arbitre
    return "OPEN"


def scan_code() -> list[dict]:
    """Marqueurs de défaut dans scripts/ et skills/ — TODO/FIXME seulement."""
    hits: list[dict] = []
    for base, zone in ((ZONE_SCRIPTS, "CODE"), (ZONE_SKILLS, "CODE")):
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*")):
            if path.suffix not in (".py", ".md", ".yaml", ".yml"):
                continue
            rel = str(path.relative_to(REPO))
            try:
                for lineno, line in enumerate(
                    path.read_text(encoding="utf-8", errors="replace").splitlines(), 1
                ):
                    if CODE_TODO_RX.search(line) or CODE_CORR_RX.search(line):
                        hits.append({
                            "zone": zone,
                            "fichier": rel,
                            "ligne": lineno,
                            "extrait": line.strip()[:400],
                            "classe": classify(line, "CODE"),
                        })
            except OSError as exc:
                hits.append({"zone": zone, "fichier": str(path), "erreur": str(exc), "classe": "OPEN"})
    return hits


def run_scan() -> dict:
    results: list[dict] = []
    for path in ZONES_LIVE:
        only_tail = path.name == "worklog.md"
        results.extend(scan_zone(path, "VIVANTE", only_tail=only_tail))
    for path in ZONES_HISTO:
        results.extend(scan_zone(path, "HISTORIQUE"))
    results.extend(scan_code())

    # Adjudication mécanique des candidats OPEN
    for item in results:
        if item["classe"] == "OPEN":
            item["classe"] = adjudiquer(item)
    counts: dict[str, int] = {}
    for item in results:
        counts[item["classe"]] = counts.get(item["classe"], 0) + 1
    open_items = [i for i in results if i["classe"] == "OPEN"]

    return {
        "task": "101-verif-differes",
        "verdict": "RESIDUS_OPEN" if open_items else "0_DIFFERE_CORRECTABLE",
        "nb_total_marqueurs": len(results),
        "comptages_par_classe": counts,
        "items_open": open_items,
        "details": results,
    }


def selftest() -> int:
    """Cas synthétiques : chaque classe doit être correctement attribuée."""
    cases = [
        ("pendance F1 véhicule rescellement [FUTURE — mission dédiée : brancher]", "HISTORIQUE", "HISTORIQUE"),
        ("pendance F1 : ÉTEINTE (Task 100, étape 2 branchée sur le scelleur v2.3)", "VIVANTE", "RESORBE"),
        ("rotation/révocation PAT [PROPRIÉTAIRE — CRITIQUE]", "VIVANTE", "PROPRIETAIRE"),
        ("PMs famille blocs §0 contenu L2 [AUTO aux prochaines montées]", "VIVANTE", "AUTO"),
        ("cron 531684 [AUTOMATIQUE — clause anti-boucle]", "VIVANTE", "AUTO"),
        ("écart structurel cas 6 voie M = proposition future hors cadence", "VIVANTE", "PROPOSITION"),
        ("le rapport contient une faille à corriger avant livraison", "VIVANTE", "OPEN"),
        ("TODO réviser la garde de ce module", "CODE", "OPEN"),
        ("# FIXME retiré — corrige en réel (Task 76)", "CODE", "RESORBE"),
    ]
    failures = []
    for text, zone, expected in cases:
        got = classify(text, zone)
        if got != expected:
            failures.append({"texte": text[:60], "attendu": expected, "obtenu": got})
    suites = last_suites("## 2026-11-01 suite 1\nA\n## 2026-11-02 suite 2\nB\n## 2026-11-03 suite 3\nC\n## 2026-11-04 suite 4\nD\n", 2)
    if "suite 4" not in suites or "suite 2" in suites:
        failures.append({"texte": "last_suites(2)", "attendu": "suites 3-4", "obtenu": suites[:80]})
    # Faux positifs éteints par conception des marqueurs
    if CODE_TODO_RX.search("todo configurado (pt-BR — tout en portugais)"):
        failures.append({"texte": "pt-BR todo", "attendu": "aucun match", "obtenu": "match"})
    if MARKERS.search("les deux états diffèrent sur 3 points"):
        failures.append({"texte": "diffèrent (verbe)", "attendu": "aucun match", "obtenu": "match"})
    # Adjudication : règles ordonnées
    adj_cases = [
        ({"fichier": "gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.43.0.md", "extrait": "- TODO list ordonnée"}, "ARCHIVE_R4"),
        ({"fichier": "skills/@PM-SKILLS/charts/references/mermaid.md", "extrait": "EnRevue --> Brouillon : retours à corriger"}, "DOC_METHODE"),
        ({"fichier": "guizang-ppt/README.pt-BR.md", "extrait": "TODO bare"}, "PLATEFORME_NON_KB"),
        ({"fichier": "skills/dream-interpreter/scripts/example.py", "extrait": "# TODO: Add actual script logic"}, "PLATEFORME_NON_KB"),
        ({"fichier": "skills/memory-engineering/SKILL.md", "extrait": "x" * 300 + " ou un drift à corriger."}, "METHODE"),
        ({"fichier": "scripts/nouveau.py", "extrait": "faille réelle à corriger en mission dédiée"}, "OPEN"),
        ({"fichier": "cahier-des-charges/scripts/scaffold_tests.py", "extrait": "# TODO(M7) : assertions exécutables"}, "TEMPLATE_CONCU"),
        ({"fichier": "auto-target-tracker/SKILL.md", "extrait": "inviter l'utilisateur à corriger manuellement en cas d'écart"}, "METHODE"),
        ({"fichier": "scripts/task47-b-precision-v3331-edits.py", "extrait": "dérive à corriger (E13)"}, "METHODE_ARBITRE"),
    ]
    for item, expected in adj_cases:
        got = adjudiquer(item)
        if got != expected:
            failures.append({"texte": item["fichier"], "attendu": expected, "obtenu": got})
    report = {"selftest": "PASS" if not failures else "FAIL", "echecs": failures,
              "nb_cas": len(cases) + 3 + len(adj_cases)}
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if not failures else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    report = run_scan()
    out = HOST / "download" / "task101-differes-report.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: report[k] for k in ("task", "verdict", "nb_total_marqueurs", "comptages_par_classe")}, ensure_ascii=False, indent=2))
    print(f"rapport: {out}")
    sys.exit(0 if report["verdict"] == "0_DIFFERE_CORRECTABLE" else 2)
