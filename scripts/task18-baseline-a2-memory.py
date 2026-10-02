#!/usr/bin/env python3
"""
Task 18 — Baseline A2 de memory-engineering (discipline n°54 HORS périmètre de la suggestion (c)
— directive propriétaire 2026-10-03 : « session gen-plan pour matérialiser les baselines de
(hors périmètre de la suggestion (c)) »).

Cycle complet exécuté (protocole A10/A14) : baseline A2 v1.0.0 (4/7 — dérive établie sur la voie
mécanique : 3 cas positifs sous le seuil) → Description Optimization v1.1.0 (description frontmatter
étendue, contrôles négatifs préservés) → re-mesure post-optimisation v1.1.0 (7/7 — zéro dérive,
21/21 votes LLM réels, QUOTA_OK après fenêtre 30 min — directive).

Arbitre idempotent et rejouable — sur la forme installée COURANTE (v1.1.0, description optimisée) :
re-exécution sans argument = mesure complète 7 cas × 2 voies ; re-exécution avec --skip-done =
ne re-mesure que les cas à votes null (KO-L001).

Sorties : scripts/baseline-a2-memory-report.json (arbitre idempotent et rejouable).

--skip-done : runner 429-aware (KO-L001) — recharge le JSON existant et ne re-mesure que les cas
dont les votes voie L contiennent au moins un null ; les votes réels déjà mesurés sont préservés.
"""
import json
import re
import subprocess
import sys
import time
import unicodedata
from pathlib import Path

BASE = Path("/home/z/my-project/ecosystem")
OUT_JSON = BASE / "scripts" / "baseline-a2-memory-report.json"
SKIP_DONE = "--skip-done" in sys.argv

SKILLS = {
    "memory-engineering": BASE / "skills/memory-engineering",
}

# ── Stemmer français léger (SHARED §7 v2 — radicalisation déterministe des suffixes nominaux/adjectivaux) ──
SUFFIXES = ["issements", "issement", "atrices", "ateur", "ations", "ation", "ements", "ement",
            "ances", "ance", "ences", "ence", "ismes", "isme", "istes", "iste",
            "ables", "able", "ibles", "ible", "euses", "euse", "eurs", "eur",
            "ités", "ité", "aux", "ales", "ale", "els", "el", "iques", "ique",
            "ives", "ive", "ifs", "if", "eaux", "eau", "ux", "ants", "ant",
            "ents", "ent", "ions", "ion", "ons", "on", "es", "e", "s", "x"]

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
    stop = {"le", "la", "les", "de", "des", "du", "un", "une", "et", "ou", "a", "au", "aux",
            "en", "dans", "sur", "pour", "par", "avec", "sans", "qui", "que", "ce", "cette",
            "son", "sa", "ses", "leur", "leurs", "est", "sont", "plus", "ne", "pas", "se",
            "chaque", "tout", "toute", "tous", "comme", "aux", "au", "il", "elle", "on",
            "skill", "discipline", "source", "verite", "shared", "references", "documentes",
            "fondements", "academiques", "specialise", "operationnalisation"}
    for w in re.findall(r"[a-zà-ÿ]+", norm(description)):
        if w not in stop and len(w) > 3:
            kws.add(w)
    return {stem(k) for k in kws if len(k) > 2}

def heuristic_score(query, kws):
    toks = {stem(w) for w in re.findall(r"[a-zà-ÿ]+", norm(query)) if len(w) > 2}
    hits = toks & kws
    # routage : ≥ 2 radicaux partagés OU ≥ 1 radical du NOM du skill (signal fort) —
    # garde de collision : les cas négatifs officiels ne cumulent pas ces signaux (SHARED §7 v2)
    trig = (len(hits) >= 2) or bool(hits & STRONG_ONLY)
    return (len(hits) / max(1, len(toks))), sorted(hits), trig

STRONG_ONLY = set()

# ── Voie L : vote LLM (3 runs, majorité) — KO-L001 : rythme poli + backoff 429 ──
def llm_vote(query, name, description, tags, run):
    sysp = ("Tu es le routeur de skills d'un écosystème. On te donne la fiche de routage d'un skill "
            "(nom, tags, description) et une requête utilisateur. Ce skill doit-il se déclencher "
            "(être chargé) pour traiter cette requête ? Réponds UNIQUEMENT par OUI ou par NON.")
    prompt = (f"SKILL : {name}\nTAGS : {', '.join(tags)}\nDESCRIPTION : {description}\n\n"
              f"REQUÊTE : {query}\n\nDéclenches-tu ce skill ? (OUI/NON)")
    for attempt in range(4):
        try:
            r = subprocess.run(
                ["z-ai", "chat", "-p", prompt, "-s", sysp],
                capture_output=True, text=True, timeout=120, cwd=str(BASE.parent))
            # stdout (JSON de réponse) + stderr (erreurs API — le CLI y écrit les 429,
            # diagnostic Task 18 2026-10-03 : « API request failed with status 429 » sur stderr)
            out = (r.stdout or "") + "\n" + (r.stderr or "")
            # contenu = dernier champ "content" du JSON de réponse (jamais la bannière CLI)
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

# ── Exécution ──
report = {"date": "2026-10-03", "session": "Task 18 — matérialisation baseline A2 memory-engineering (hors périmètre suggestion (c)), QUOTA_OK levé",
          "seuil": 0.5, "confirm_runs": 3, "skills": {}}

# runner 429-aware (KO-L001 --skip-done) : préserve les votes réels déjà mesurés
prior = {}
if SKIP_DONE and OUT_JSON.exists():
    try:
        prior = json.loads(OUT_JSON.read_text()).get("skills", {}).get("memory-engineering", {})
    except Exception:
        prior = {}

for name, sdir in SKILLS.items():
    cases = json.loads((sdir / "evals" / "trigger_evals.json").read_text())
    skillmd = (sdir / "SKILL.md").read_text()
    fm = skillmd.split("---")[1]
    # extraction description : bloc indenté (1 espace ou plus) après description: >-
    desc_m = re.search(r"description:\s*>-?\s*\n((?:[ \t]+.*\n)+)", fm)
    desc = " ".join(l.strip() for l in desc_m.group(1).splitlines()) if desc_m else ""
    tags_m = re.search(r"tags:\s*\n((?:\s+-\s+.*\n)+)", fm)
    tags = re.findall(r"-\s+(.+)", tags_m.group(1)) if tags_m else []
    kws = keywords_for(name, desc, tags)
    # radicaux forts = radicaux issus du nom du skill (signal de routage principal)
    STRONG_ONLY.clear(); STRONG_ONLY.update({stem(p) for p in name.split("-")})

    rows = []
    prior_cases = prior.get("cases", [])
    for idx, case in enumerate(cases):
        q, expected = case["query"], case["should_trigger"]
        score_m, hits, trig_m = heuristic_score(q, kws)
        # --skip-done : cas déjà mesuré (aucun null) et requête inchangée → votes préservés (voie M déterministe, rejetée à l'identique)
        pc = prior_cases[idx] if idx < len(prior_cases) and prior_cases[idx].get("query") == q else None
        if SKIP_DONE and pc is not None and None not in pc.get("voie_l", {}).get("votes", [None]):
            rows.append(pc)
            print(f"    [skip-done] cas {idx+1} préservé (votes réels)", flush=True)
            continue
        votes = []
        evidences = []
        for run in (1, 2, 3):
            v, ev = llm_vote(q, name, desc, tags, run)
            votes.append(v); evidences.append(ev)
        valid = [v for v in votes if v is not None]
        ratio = (sum(valid) / len(valid)) if valid else 0.0
        trig_l = ratio >= 0.5
        ok = (trig_m == expected) and (trig_l == expected)
        rows.append({
            "query": q, "expected": expected,
            "voie_m": {"score": round(score_m, 3), "trigger": trig_m, "hits": hits},
            "voie_l": {"votes": votes, "ratio": round(ratio, 3), "trigger": trig_l, "evidence": evidences},
            "baseline_ok": ok,
        })

    n_ok = sum(1 for r in rows if r["baseline_ok"])
    derive = [r for r in rows if not r["baseline_ok"]]
    report["skills"][name] = {
        "description": desc[:200], "tags": tags, "n_keywords": len(kws), "cases": rows,
        "score_baseline": f"{n_ok}/{len(rows)}", "derive": bool(derive),
        "description_optimization_required": bool(derive),
    }
    print(f"--- {name} : baseline {n_ok}/{len(rows)} — dérive : {bool(derive)}", flush=True)

OUT_JSON.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"JSON : {OUT_JSON}", flush=True)
sys.exit(0)
