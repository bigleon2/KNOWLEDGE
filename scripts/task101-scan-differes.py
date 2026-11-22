#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 101 — Scanner mécanique des différés consignés à corriger ($FACON).

Zones (dynamiques — Task 115, KO-L003 : jamais de listes figées) :
  VIVANTE    : worklog hôte (3 dernières suites ; repli dépôt) · dernier plan
               download/plan-*.md · dernier rapport CW download/rapport-cw-*.md
               (hôte d'abord — dossier vivant persistant inter-recyclages ;
               repli miroir dépôt KNOWLEDGE-repo/download/).
  HISTORIQUE : 5 derniers clones scellés download/clone-*.md (R6 — non éditables,
               mentions = enregistrements datés).
  CODE       : scripts/*.py + skills/*/SKILL.md du dépôt (marqueurs TODO/FIXME =
               candidats OPEN ; auto-exclusion du présent scanner — ses docstrings,
               regex et cas de selftest décrivent la méthode, jamais des différés).

Classification par mots-clés de contexte :
  OPEN         : candidat réel à corriger (aucun marqueur de résolution/acteur)
  RESORBE      : résolution attestée dans la ligne (éteint/résorbé/fermé/done/branché)
  PROPRIETAIRE : rotation PAT / propriétaire
  AUTO         : automatique / cron / aux prochaines montées
  PROPOSITION  : proposition hors cadence (non une correction différée)
  HISTORIQUE   : zone scellée (mention datée, non item vivant)

Rapport JSON déterministe (aucune horloge) — selftest embarqué (--selftest).
"""

# ⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.45)
# SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
# Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
# Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
# Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
# Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
# Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HOST = Path("/home/z/my-project")
REPO = HOST / "KNOWLEDGE-repo"

# « différé » avec é aigu uniquement — exclut les verbes « diffèrent/diffère » (è grave) ;
# « pendance » avec frontières de mots (Task 115) — exclut « indépendance/dépendance » (sous-chaîne)
MARKERS = re.compile(
    r"\b[Pp]endances?\b|\bPENDANCES?\b|différé|\[FUTURE\]|à corriger|reste à faire"
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

ZONES_LIVE_WORKLOG = [HOST / "worklog.md", REPO / "worklog.md"]
ZONE_DL_HOTE = HOST / "download"
ZONE_DL_DEPOT = REPO / "download"
ZONE_SCRIPTS = REPO / "scripts"
ZONE_SKILLS = REPO / "skills"


def _latest(pattern: str, n: int = 1) -> list:
    """Plus récents fichiers download/ (hôte d'abord — dossier vivant ; repli
    miroir dépôt), tri mtime décroissant. Une base non vide ÉPUISE la sélection
    (les archives profondes du dépôt ne polluent jamais la zone vivante)."""
    for base in (ZONE_DL_HOTE, ZONE_DL_DEPOT):
        if base.is_dir():
            fichiers = sorted(
                base.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True
            )
            if fichiers:
                return fichiers[:n]
    return []


def zones_vivantes() -> list:
    """Journal vivant + dernier plan + dernier rapport CW (dynamique — Task 115)."""
    zones = []
    for wl in ZONES_LIVE_WORKLOG:
        if wl.exists():
            zones.append((wl, "VIVANTE"))
            break
    zones.extend((p, "VIVANTE") for p in _latest("plan-*.md", 1))
    zones.extend((p, "VIVANTE") for p in _latest("rapport-cw-*.md", 1))
    return zones


def zones_historiques() -> list:
    """5 derniers clones scellés (dynamique — Task 115)."""
    return [(p, "HISTORIQUE") for p in _latest("clone-*.md", 5)]


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
                "extrait": line.strip()[:400],
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
    if re.match(r"^(criterion|verification|source|priority|status)\s*:", extrait):
        return "METHODE_ARBITRE"     # lignes answer key = contrat de méthode du plan (Task 115)
    if "corriger manuellement en cas d'écart" in extrait or "drift à corriger" in extrait:
        return "METHODE"             # instruction utilisateur / description du comportement
    if "TODO(M7)" in extrait or "squelette" in extrait:
        return "TEMPLATE_CONCU"      # squelette généré par conception (mode M7)
    if "TODO list" in extrait or "TODO/fenêtre" in extrait or "fenêtre de tâches" in extrait:
        return "METHODE"             # description de fonctionnalité gen-plan / concept fenêtre de tâches (TodoWrite)
    if "différées au worklog" in extrait or "explicitement différées" in extrait:
        return "METHODE"             # politique de report documenté — canal worklog (D005, Task 115)
    if "pendances héritées" in extrait or "vérification croisée pendances" in extrait:
        return "METHODE"             # langage d'analyse (sujets d'examen, non items ouverts — Task 115)
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
            if path.name == "task101-scan-differes.py":
                continue  # auto-exclusion (Task 115) : docstrings/regex/selftest = méthode
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
    for path, zone in zones_vivantes() + zones_historiques():
        only_tail = zone == "VIVANTE" and path.name == "worklog.md"
        results.extend(scan_zone(path, zone, only_tail=only_tail))
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
    if MARKERS.search("parallélisation par défaut sur preuve d'indépendance, application série"):
        failures.append({"texte": "indépendance (sous-chaîne)", "attendu": "aucun match", "obtenu": "match"})
    if not MARKERS.search("PENDANCES PROPRIÉTAIRE : rotation PAT"):
        failures.append({"texte": "PENDANCES (mot entier)", "attendu": "match", "obtenu": "aucun"})
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
        # Règles Task 115 (dynamisation — faux positifs réels constatés au re-jeu)
        ({"fichier": "scripts/t114-genplan-v3470.py", "extrait": '"tout message, TODO/fenêtre de tâches, résumé de continuation ou livrable"'}, "METHODE"),
        ({"fichier": "download/plan-courant.md", "extrait": 'criterion: "G2-G8 : ... appliquées ou explicitement différées au worklog"'}, "METHODE_ARBITRE"),
        ({"fichier": "download/plan-courant.md", "extrait": "**G1b** | Analyse approfondie ... (contexte, décisions, pendances héritées, leçons)"}, "METHODE"),
        ({"fichier": "download/plan-courant.md", "extrait": "vérification croisée pendances↔plan courant (recontextualisation avant continuation)"}, "METHODE"),
        ({"fichier": "scripts/ancien.py", "extrait": "# TODO vrai marqueur résiduel à traiter"}, "OPEN"),
    ]
    for item, expected in adj_cases:
        got = adjudiquer(item)
        if got != expected:
            failures.append({"texte": item["fichier"], "attendu": expected, "obtenu": got})
    # Zones dynamiques (Task 115) : _latest résout hôte d'abord puis dépôt (mtime décroissant)
    import tempfile
    import time
    global ZONE_DL_HOTE, ZONE_DL_DEPOT  # noqa: PLW0603 — swap de test restauré en finally
    with tempfile.TemporaryDirectory() as td:
        hote = Path(td) / "h"
        miroir = Path(td) / "r"
        for dossier in (hote, miroir):
            dossier.mkdir()
        (miroir / "plan-a.md").write_text("A", encoding="utf-8")
        time.sleep(0.02)
        (hote / "plan-b.md").write_text("B", encoding="utf-8")
        ancien_h, ancien_r = ZONE_DL_HOTE, ZONE_DL_DEPOT
        try:
            ZONE_DL_HOTE, ZONE_DL_DEPOT = hote, miroir
            got = [p.name for p in _latest("plan-*.md", 5)]
            if got != ["plan-b.md"]:
                failures.append({"texte": "_latest hôte épuise la sélection", "attendu": ["plan-b.md"], "obtenu": got})
            ZONE_DL_HOTE = Path(td) / "inexistant"
            got2 = [p.name for p in _latest("plan-*.md", 5)]
            if got2 != ["plan-a.md"]:
                failures.append({"texte": "_latest repli dépôt", "attendu": ["plan-a.md"], "obtenu": got2})
        finally:
            ZONE_DL_HOTE, ZONE_DL_DEPOT = ancien_h, ancien_r
    report = {"selftest": "PASS" if not failures else "FAIL", "echecs": failures,
              "nb_cas": len(cases) + 3 + len(adj_cases) + 2}
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
