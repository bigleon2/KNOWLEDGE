#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.6.8)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

# -*- coding: utf-8 -*-
"""
Task 21 — campagne P3 : baselines A2 (7+ cas × 2 voies, seuil 0.5, confirm 3 runs)
généralisées aux 26 skills équipés trigger_evals — généralisation de l'arbitre certifié
scripts/task18-baseline-a2-memory.py (méthode SHARED §7 v2 identique).

- Voie M : déterministe (réplique exacte arbitre V6 — y compris parsing single-line N1).
- Voie L : votes LLM réels 3 runs/cas (z-ai CLI), rythme poli KO-L001 (4 s), backoff 429
  stdout+stderr (diagnostic Task 18), AUCUNE fabrication (R3 — votes null consignés).
- --skip-done : idempotent (KO-L001) — recharge le JSON et ne re-mesure que les cas à
  votes null ; les votes réels préservés, la voie M est rejetée à l'identique.
- --skills=a,b,c : limite la mesure à un lot (lots 429-aware du plan d'extension).

Sortie : scripts/baseline-a2-all-report.json
"""
import json
import re
import subprocess
import sys
import time
import unicodedata
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
OUT_JSON = BASE / "scripts" / "baseline-a2-all-report.json"
SKIP_DONE = "--skip-done" in sys.argv
LOT = None
for a in sys.argv:
    if a.startswith("--skills="):
        LOT = set(a.split("=", 1)[1].split(","))

# ── Stemmer français léger (SHARED §7 v2 — réplique identique aux arbitres certifiés) ──
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


def load_skill(sdir):
    smd = (sdir / "SKILL.md").read_text(encoding="utf-8")
    fm = smd.split("---")[1]
    desc_m = re.search(r"description:\s*>-?\s*\n((?:[ \t]+.*\n)+)", fm)
    if desc_m:
        desc = " ".join(l.strip() for l in desc_m.group(1).splitlines())
    else:
        desc_m2 = re.search(r"description:\s*[\"']?(.+?)[\"']?\s*$", fm, re.MULTILINE)
        desc = desc_m2.group(1).strip() if desc_m2 else ""
    tags_m = re.search(r"tags:\s*\n((?:\s+-\s+.*\n)+)", fm)
    tags = re.findall(r"-\s+(.+)", tags_m.group(1)) if tags_m else []
    cases = json.loads((sdir / "evals" / "trigger_evals.json").read_text(encoding="utf-8"))
    return desc, tags, cases


def llm_vote(query, name, description, tags):
    sysp = ("Tu es le routeur de skills d'un écosystème. On te donne la fiche de routage d'un skill "
            "(nom, tags, description) et une requête utilisateur. Ce skill doit-il se déclencher "
            "(être chargé) pour traiter cette requête ? Réponds UNIQUEMENT par OUI ou par NON.")
    prompt = (f"SKILL : {name}\nTAGS : {', '.join(tags)}\nDESCRIPTION : {description}\n\n"
              f"REQUÊTE : {query}\n\nDéclenches-tu ce skill ? (OUI/NON)")
    for attempt in range(4):
        try:
            r = subprocess.run(["z-ai", "chat", "-p", prompt, "-s", sysp],
                               capture_output=True, text=True, timeout=120, cwd=str(BASE.parent))
            out = (r.stdout or "") + "\n" + (r.stderr or "")
            answers = re.findall(r'"content"\s*:\s*"([^"]*)"', out)
            if answers:
                a = answers[-1].upper()
                time.sleep(4)  # politesse inter-appels (KO-L001)
                return ("OUI" in a and "NON" not in a), ("OUI" if "OUI" in a else ("NON" if "NON" in a else a[:30]))
            if "429" in out or "Too many requests" in out:
                wait = 20 * (attempt + 1)
                print(f"    [429] backoff {wait}s (tentative {attempt+1})", flush=True)
                time.sleep(wait)
                continue
            time.sleep(4)
            return None, "pas de contenu"
        except Exception as e:
            time.sleep(10)
            if attempt == 3:
                return None, f"ERR {e}"
    return None, "429 persistant"


def main():
    equipped = []
    for sdir in sorted(BASE.joinpath("skills").iterdir()):
        if not sdir.is_dir() or sdir.name.startswith(("_", ".")) or sdir.name == "@mon-ecosysteme":
            continue
        if (sdir / "evals" / "trigger_evals.json").exists():
            if LOT is None or sdir.name in LOT:
                equipped.append(sdir)

    report = {}
    if SKIP_DONE and OUT_JSON.exists():
        try:
            report = json.loads(OUT_JSON.read_text(encoding="utf-8")).get("skills", {})
        except Exception:
            report = {}

    for sdir in equipped:
        name = sdir.name
        desc, tags, cases = load_skill(sdir)
        kws = keywords_for(name, desc, tags)
        strong = {stem(p) for p in name.split("-")}
        prior_cases = report.get(name, {}).get("cases", [])
        rows = []
        for idx, case in enumerate(cases):
            q, expected = case["query"], case["should_trigger"]
            toks = {stem(w) for w in re.findall(r"[a-zà-ÿ]+", norm(q)) if len(w) > 2}
            hits = toks & kws
            trig_m = (len(hits) >= 2) or bool(hits & strong)
            pc = prior_cases[idx] if idx < len(prior_cases) and prior_cases[idx].get("query") == q else None
            if SKIP_DONE and pc is not None and None not in pc.get("voie_l", {}).get("votes", [None]):
                rows.append(pc)
                print(f"    [skip-done] {name} cas {idx+1} préservé", flush=True)
                continue
            votes, evidences = [], []
            for run in (1, 2, 3):
                v, ev = llm_vote(q, name, desc, tags)
                votes.append(v)
                evidences.append(ev)
            valid = [v for v in votes if v is not None]
            ratio = (sum(valid) / len(valid)) if valid else None
            trig_l = (ratio >= 0.5) if ratio is not None else None
            ok = (trig_m == expected) and (trig_l == expected) if trig_l is not None else None
            rows.append({
                "query": q, "expected": expected,
                "voie_m": {"trigger": trig_m, "hits": sorted(hits)},
                "voie_l": {"votes": votes, "ratio": ratio, "trigger": trig_l, "evidence": evidences},
                "baseline_ok": ok,
            })
            print(f"    {name} cas {idx+1}/{len(cases)} : M={trig_m} L={trig_l} ({votes})", flush=True)
        n_ok = sum(1 for r in rows if r.get("baseline_ok"))
        n_null = sum(1 for r in rows if any(v is None for v in r.get("voie_l", {}).get("votes", [])))
        report[name] = {"description": desc[:200], "n_cases": len(rows),
                        "score_baseline": f"{n_ok}/{len(rows)}",
                        "derive": any(not r.get("baseline_ok") for r in rows if r.get("baseline_ok") is not None),
                        "votes_null": n_null, "cases": rows}
        print(f"--- {name} : baseline {n_ok}/{len(rows)} (nulls: {n_null})", flush=True)
        OUT_JSON.write_text(json.dumps({"date": "2026-10-03", "task": "Task 21 — campagne P3 (baselines A2 généralisées)",
                                        "seuil": 0.5, "confirm_runs": 3, "skills": report},
                                       ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"JSON : {OUT_JSON}", flush=True)


if __name__ == "__main__":
    main()
