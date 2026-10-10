#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.6.8)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

# -*- coding: utf-8 -*-
"""
Arbitre V6 — check-triggers-replay.py (Task 21, campagne P0 — plan d'extension
verifications-tous-skills-agents.md, recommandation R1 Task 19).

Rôle institutionnel : re-jouer MÉCANIQUEMENT (voie M, zéro API) les corpus officiels
de trigger_evals de TOUS les skills équipés, à chaque montée/optimisation (garde
KO-L004). Résorbe l'angle mort Task 19 : aucun arbitre ne re-jouait les triggers
(verify-cross = présence/schéma ; baselines task17/task18 one-shot limitées aux 3 n°54).

Heuristique : réplique EXACTE de SHARED §7 v2 (stemmer français, keywords_for,
routage « ≥ 2 radicaux partagés OU ≥ 1 radical du nom du skill ») — identique au
harnais Task 19 (test-triggers-genplan-memory.py) et au runner certifié
task18-baseline-a2-memory.py.

KO-L003 : invariants DYNAMISÉS — le périmètre est dérivé du filesystem
(skills/*/evals/trigger_evals.json), jamais figé ; la comparaison à la baseline
précédente est conditionnelle à la présence du rapport antérieur.

Usage :
  python scripts/check-triggers-replay.py                # rejeu + verdict global
  python scripts/check-triggers-replay.py --quiet        # JSON seulement
  python scripts/check-triggers-replay.py --compare      # compare au rapport précédent

Sortie : scripts/triggers-replay-report.json — exit 0 si 100 % voie M, exit 1 sinon.
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent          # ecosystem/
SKILLS = BASE / "skills"
OUT_JSON = BASE / "scripts" / "triggers-replay-report.json"
QUIET = "--quiet" in sys.argv
COMPARE = "--compare" in sys.argv

# ── Stemmer français léger (SHARED §7 v2 — réplique identique aux runners certifiés) ──
SUFFIXES = ["issements", "issement", "atrices", "ateur", "ations", "ation", "ements", "ement",
            "ances", "ance", "ences", "ence", "ismes", "isme", "istes", "iste",
            "ables", "able", "ibles", "ible", "euses", "euse", "eurs", "eur",
            "ités", "ité", "aux", "ales", "ale", "els", "el", "iques", "ique",
            "ives", "ive", "ifs", "if", "eaux", "eau", "ux", "ants", "ant",
            "ents", "ent", "ions", "ion", "ons", "on", "es", "e", "s", "x"]

STOP = {"le", "la", "les", "de", "des", "du", "un", "une", "et", "ou", "a", "au", "aux",
        "en", "dans", "sur", "pour", "par", "avec", "sans", "qui", "que", "ce", "cette",
        "son", "sa", "ses", "leur", "leurs", "est", "sont", "plus", "ne", "pas", "se",
        "chaque", "tout", "toute", "tous", "comme", "aux", "au", "il", "elle", "on",
        "skill", "discipline", "source", "verite", "shared", "references", "documentes",
        "fondements", "academiques", "specialise", "operationnalisation"}


def stem(w):
    w = w.lower()
    for suf in SUFFIXES:
        if w.endswith(suf) and len(w) - len(suf) >= 4:
            return w[: len(w) - len(suf)]
    return w


def norm(t):
    t = unicodedata.normalize("NFKD", t)
    return "".join(c for c in t if not unicodedata.combining(c)).lower()


def keywords_for(name, description, tags):
    kws = set(name.split("-"))
    kws |= {norm(t) for t in tags}
    for w in re.findall(r"[a-zà-ÿ]+", norm(description)):
        if w not in STOP and len(w) > 3:
            kws.add(w)
    return {stem(k) for k in kws if len(k) > 2}


def heuristic_score(query, kws, strong):
    toks = {stem(w) for w in re.findall(r"[a-zà-ÿ]+", norm(query)) if len(w) > 2}
    hits = toks & kws
    trig = (len(hits) >= 2) or bool(hits & strong)
    return (len(hits) / max(1, len(toks))), sorted(hits), trig


def load_skill(sdir):
    smd = (sdir / "SKILL.md").read_text(encoding="utf-8")
    fm = smd.split("---")[1]
    desc_m = re.search(r"description:\s*>-?\s*\n((?:[ \t]+.*\n)+)", fm)
    if desc_m:
        desc = " ".join(l.strip() for l in desc_m.group(1).splitlines())
    else:
        # N1 (Task 21, KO-L003) : descriptions single-line (ex : version-management zh)
        desc_m2 = re.search(r"description:\s*[\"']?(.+?)[\"']?\s*$", fm, re.MULTILINE)
        desc = desc_m2.group(1).strip() if desc_m2 else ""
    tags_m = re.search(r"tags:\s*\n((?:\s+-\s+.*\n)+)", fm)
    tags = re.findall(r"-\s+(.+)", tags_m.group(1)) if tags_m else []
    ver_m = re.search(r'version:\s*"?([0-9.]+)"?', fm)
    tevals = sdir / "evals" / "trigger_evals.json"
    cases = json.loads(tevals.read_text(encoding="utf-8")) if tevals.exists() else []
    return {"name": sdir.name, "version": ver_m.group(1) if ver_m else "?",
            "desc": desc, "tags": tags, "cases": cases}


def main():
    # Périmètre DYNAMIQUE (KO-L003) : tout skill équipé au moment du rejeu
    equipped = []
    for sdir in sorted(SKILLS.iterdir()):
        if not sdir.is_dir() or sdir.name.startswith(("_", ".")) or sdir.name == "@mon-ecosysteme":
            continue
        if (sdir / "evals" / "trigger_evals.json").exists():
            equipped.append(sdir)

    registry = {}
    ignores = []
    for sdir in equipped:
        sk = load_skill(sdir)
        if not (isinstance(sk["cases"], list)
                and all(isinstance(c, dict) and "query" in c and "should_trigger" in c
                        for c in sk["cases"])):
            ignores.append(sdir.name)
            continue
        kws = keywords_for(sk["name"], sk["desc"], sk["tags"])
        strong = {stem(p) for p in sk["name"].split("-")}
        rows = []
        for c in sk["cases"]:
            q, exp = c["query"], c["should_trigger"]
            score, hits, trig = heuristic_score(q, kws, strong)
            rows.append({"query": q, "expected": exp, "trigger_m": trig,
                         "score": round(score, 3), "hits": hits, "ok": trig == exp})
        n_ok = sum(1 for r in rows if r["ok"])
        registry[sk["name"]] = {"version": sk["version"], "n_cases": len(rows),
                                "n_keywords": len(kws),
                                "score_officiel": f"{n_ok}/{len(rows)}",
                                "ok": n_ok == len(rows), "derive_m": n_ok < len(rows),
                                "cases": rows}

    n_ok_skills = sum(1 for v in registry.values() if v["ok"])
    derives = sorted(k for k, v in registry.items() if v["derive_m"])

    # Comparaison conditionnelle au rapport précédent (dynamisé — jamais figé)
    comparison = None
    if COMPARE and OUT_JSON.exists():
        try:
            prev = json.loads(OUT_JSON.read_text(encoding="utf-8"))
            prev_scores = {k: v["score_officiel"] for k, v in prev.get("skills", {}).items()}
            cur_scores = {k: v["score_officiel"] for k, v in registry.items()}
            comparison = {
                "prev_run": prev.get("date"),
                "regressions": sorted(k for k in cur_scores
                                      if k in prev_scores and cur_scores[k] < prev_scores[k]),
                "ameliorations": sorted(k for k in cur_scores
                                        if k in prev_scores and cur_scores[k] > prev_scores[k]),
                "nouveaux": sorted(k for k in cur_scores if k not in prev_scores),
                "retires": sorted(k for k in prev_scores if k not in cur_scores),
            }
        except Exception as e:  # rapport illisible → comparaison annulée, jamais masquée
            comparison = {"erreur": f"rapport précédent illisible : {e}"}

    # Date du commit audité (B2 Task 22) : déterministe par commit — plus d'horloge murale,
    # sinon le rapport change entre deux re-exécutions le lendemain (f(f(x)) != f(x)).
    try:
        import subprocess as _sp
        _git_date = (_sp.run(["git", "-C", "/home/z/my-project/work_knowledge", "log", "-1",
                              "--format=%cd", "--date=short"],
                             capture_output=True, text=True, timeout=10).stdout.strip()
                     or "2026-10-03")
    except Exception:
        _git_date = "2026-10-03"
    report = {
        "date": _git_date,
        "task": "Task 21 — campagne P0-P6, arbitre V6 (recommandation R1 Task 19)",
        "heuristique": "SHARED §7 v2 (réplique exacte harnais Task 19 / runner Task 18 — voie M, zéro API)",
        "seuil_routage": "≥ 2 radicaux partagés OU ≥ 1 radical du nom du skill",
        "invariants": "dynamisés KO-L003 (périmètre = skills/*/evals/trigger_evals.json au moment du rejeu)",
        "n_skills": len(registry),
        "skills_ok": n_ok_skills,
        "skills_derive": len(derives),
        "verdict": "PASS" if not derives else "FAIL",
        "derives": derives,
        "skills": registry,
        "ignores_schema_non_canonique": ignores,
    }
    if comparison:
        report["comparaison_run_precedent"] = comparison
    OUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    if not QUIET:
        print("=" * 70)
        print(f"ARBITRE V6 — rejeu voie M des corpus trigger_evals ({len(registry)} skills)")
        print("=" * 70)
        for k in sorted(registry):
            v = registry[k]
            print(f"  [{'OK ' if v['ok'] else 'DÉRIVE'}] {k:<38} {v['score_officiel']}")
        if comparison and "regressions" in comparison:
            print(f"\nComparaison run précédent ({comparison.get('prev_run')}): "
                  f"régressions={comparison['regressions'] or '0'} · "
                  f"améliorations={comparison['ameliorations'] or '0'} · "
                  f"nouveaux={comparison['nouveaux'] or '0'} · retirés={comparison['retires'] or '0'}")
        if ignores:
            print(f"IGNORÉS (schéma non canonique, hors périmètre voie M) : {len(ignores)}")
        print(f"\nBILAN : {n_ok_skills}/{len(registry)} skills au score maximal — "
              f"dérives : {derives or 'aucune'}")
        print(f"VERDICT : {report['verdict']} — JSON : {OUT_JSON}")
    sys.exit(0 if not derives else 1)


if __name__ == "__main__":
    main()
