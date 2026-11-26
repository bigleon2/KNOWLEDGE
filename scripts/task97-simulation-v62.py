#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.46)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).
"""

# -*- coding: utf-8 -*-
"""
Task 97 G1 — Harnais de SIMULATION PRÉALABLE V6.2 (mission dédiée arbitre V6,
décision propriétaire trace 1a1df48b3eb8fb9d : « lance $FACON la mission dédiée
à l'arbitre V »).

Problème (écart consigné Task 86/90, suites 108/117/126/130/131/135) : le cas 6
voie M d'agent-engineering (« Lance une flotte d'agents en parallèle avec un
supervisor et agrège les résultats. », attendu False) est un FAUX POSITIF
STRUCTUREL — trig_m=True par deux chemins à la fois (radical « agent » ∈ strong
du nom ET ≥ 2 hits ['agent', 'flott'] — le radical « flott » vient de la clause
d'exclusion « → flotte : fleet-engineering » de la description optimisée A10/A14,
ironie structurelle : l'exclusion documentée alimente les keywords). Irréductible
par description (tout positif contient « agent »).

Hypothèse V6.2 — RÉSERVATION DE CORPUS CROISÉE (lexique structurel) : les corpus
trigger_evals des autres skills équipés encodent la doctrine « périmètre » (V6.1,
champ exclusifs) ; symétriquement, une requête POSITIVE d'un autre skill équipé
RÉSERVE son périmètre : si la requête du cas courant est fortement similaire
(radicaux partagés) à une requête should_trigger=true d'un AUTRE skill, le
verdict du skill courant est corrigé à False (source v62-reservation-corpus),
AVANT le recours au cache voie L.

La présente simulation MESURE la règle AVANT implémentation (règle d'or n°5 —
mesurer avant corriger ; jamais de re-jeu à l'identique) :
  S1 — baseline voie M brute (réplique exacte check-triggers-replay.py) ;
  S2 — pour chaque cas en désaccord voie M, meilleure similarité radicale
       (Jaccard sur stems, identité incluse) avec les positives des autres
       skills — diagnostic : la règle COUVRE-T-ELLE l'écart ?
  S3 — balayage de seuils (identité seule ; Jaccard 0.4/0.5/0.6/0.7 avec
       ancrage minimum) : pour chaque seuil, réparations (dérives → OK) et
       RÉGRESSIONS (cas OK voie M → veto à tort) sur les 101 skills équipés ;
  S4 — recommandation : seuil le plus STRICT qui répare l'écart cible
       (cas 6 agent-engineering) avec 0 régression ; les faux négatifs
       lexicaux (re-curation cas 1/7) sont hors périmètre V6.2 (documentés).

Sortie : scripts/task97-simulation-report.json (déterministe, sans horloge).
Idempotent (R1-R6) : lecture seule sur l'écosystème, rapport réécrit identique.
Usage : python3 scripts/task97-simulation-v62.py [--verbose]
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
SKILLS = BASE / "skills"
OUT = BASE / "scripts" / "task97-simulation-report.json"
VERBOSE = "--verbose" in sys.argv

# ── Réplique EXACTE de l'heuristique voie M (check-triggers-replay.py V6.1) ──
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


def stems_query(q):
    return {stem(w) for w in re.findall(r"[a-zà-ÿ]+", norm(q)) if len(w) > 2}


def heuristic_score(query, kws, strong):
    toks = stems_query(query)
    hits = toks & kws
    trig = (len(hits) >= 2) or bool(hits & strong)
    return (len(hits) / max(1, len(toks))), sorted(hits), trig


def jaccard(a, b):
    u = a | b
    return len(a & b) / len(u) if u else 0.0


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
    ver_m = re.search(r'version:\s*"?([0-9.]+)"?', fm)
    tevals = sdir / "evals" / "trigger_evals.json"
    cases = json.loads(tevals.read_text(encoding="utf-8")) if tevals.exists() else []
    return {"name": sdir.name, "version": ver_m.group(1) if ver_m else "?",
            "desc": desc, "tags": tags, "cases": cases}


def main():
    # S0 — périmètre dynamique (identique arbitre V6.1)
    equipped = []
    for sdir in sorted(SKILLS.iterdir()):
        if not sdir.is_dir() or sdir.name.startswith(("_", ".")) or sdir.name == "@mon-ecosysteme":
            continue
        if (sdir / "evals" / "trigger_evals.json").exists():
            equipped.append(sdir)

    skills = {}
    for sdir in equipped:
        sk = load_skill(sdir)
        if not (isinstance(sk["cases"], list)
                and all(isinstance(c, dict) and "query" in c and "should_trigger" in c
                        for c in sk["cases"])):
            continue
        sk["kws"] = keywords_for(sk["name"], sk["desc"], sk["tags"])
        sk["strong"] = {stem(p) for p in sk["name"].split("-")}
        skills[sk["name"]] = sk

    # Index des positives par skill (pour la réservation croisée)
    positives = {name: [c["query"] for c in sk["cases"] if c["should_trigger"]]
                 for name, sk in skills.items()}

    # S1 — baseline voie M brute
    baseline = {}
    for name, sk in skills.items():
        rows = []
        for c in sk["cases"]:
            _, hits, trig = heuristic_score(c["query"], sk["kws"], sk["strong"])
            rows.append({"query": c["query"], "expected": c["should_trigger"],
                         "trig_m": trig, "hits": hits,
                         "ok_m": trig == c["should_trigger"]})
        n_ok = sum(1 for r in rows if r["ok_m"])
        baseline[name] = {"rows": rows, "score": f"{n_ok}/{len(rows)}",
                          "derive": n_ok < len(rows)}

    derives = {k: v for k, v in baseline.items() if v["derive"]}

    # S2 — diagnostic : chaque cas en désaccord voie M a-t-il une positive voisine ailleurs ?
    diag = []
    for name, v in derives.items():
        for i, r in enumerate(v["rows"], 1):
            if r["ok_m"]:
                continue
            qs = stems_query(r["query"])
            best = {"jaccard": 0.0, "with": None, "inter": 0, "identique": False}
            for other, pos in positives.items():
                if other == name:
                    continue
                for p in pos:
                    ps = stems_query(p)
                    j = jaccard(qs, ps)
                    if norm(p) == norm(r["query"]):
                        j = 1.0
                    if j > best["jaccard"]:
                        best = {"jaccard": round(j, 3), "with": other,
                                "inter": len(qs & ps), "identique": norm(p) == norm(r["query"]),
                                "req": p}
            diag.append({"skill": name, "cas": i, "expected": r["expected"],
                         "trig_m": r["trig_m"], "hits": r["hits"], "query": r["query"],
                         "positive_voisine": best})

    # S3 — balayage de seuils : effet de la règle V6.2 sur les 101 skills
    seuils = [
        ("identite-seule", lambda j, inter, ident: ident),
        ("jaccard>=0.7+inter>=3", lambda j, inter, ident: j >= 0.7 and inter >= 3),
        ("jaccard>=0.6+inter>=3", lambda j, inter, ident: j >= 0.6 and inter >= 3),
        ("jaccard>=0.5+inter>=2", lambda j, inter, ident: j >= 0.5 and inter >= 2),
        ("jaccard>=0.4+inter>=3", lambda j, inter, ident: j >= 0.4 and inter >= 3),
        ("jaccard>=0.4+inter>=2", lambda j, inter, ident: j >= 0.4 and inter >= 2),
        ("jaccard>=0.3+inter>=3", lambda j, inter, ident: j >= 0.3 and inter >= 3),
    ]
    # Pré-calcul : pour chaque (skill, cas), la meilleure similarité hors skill courant
    voisines = {}
    for name, sk in skills.items():
        for c in sk["cases"]:
            qs = stems_query(c["query"])
            best = (0.0, 0, False, None)
            for other, pos in positives.items():
                if other == name:
                    continue
                for p in pos:
                    ps = stems_query(p)
                    ident = norm(p) == norm(c["query"])
                    j = 1.0 if ident else jaccard(qs, ps)
                    if j > best[0]:
                        best = (round(j, 3), len(qs & ps), ident, other)
            voisines[(name, c["query"])] = best

    balayage = []
    for label, pred in seuils:
        reparations, regressions = [], []
        for name, sk in skills.items():
            v = baseline[name]
            for i, r in enumerate(v["rows"], 1):
                j, inter, ident, other = voisines[(name, r["query"])]
                reserve = pred(j, inter, ident)
                if not reserve:
                    continue
                # règle V6.2 : requête réservée à un autre skill → verdict False
                v62_verdict = False
                if r["ok_m"] and r["expected"] is True:
                    # positif voie M tué par le veto → régression potentielle
                    regressions.append({"skill": name, "cas": i, "query": r["query"],
                                        "jaccard": j, "avec": other})
                elif (not r["ok_m"]) and r["expected"] is False and r["trig_m"] is True:
                    # faux positif voie M corrigé par le veto → réparation
                    reparations.append({"skill": name, "cas": i, "query": r["query"],
                                        "jaccard": j, "avec": other, "identique": ident})
                # (les cas expected False déjà OK voie M et les faux négatifs ne changent pas)
        # recalcul des scores V6.2 par seuil (voie M + veto V6.2)
        scores_v62, derives_v62 = {}, []
        for name, sk in skills.items():
            v = baseline[name]
            n_ok = 0
            for r in v["rows"]:
                j, inter, ident, other = voisines[(name, r["query"])]
                verdict = (not pred(j, inter, ident)) and r["trig_m"]
                if verdict == r["expected"]:
                    n_ok += 1
            scores_v62[name] = f"{n_ok}/{len(v['rows'])}"
            if n_ok < len(v["rows"]):
                derives_v62.append(name)
        balayage.append({"seuil": label, "reparations": reparations,
                         "n_reparations": len(reparations), "regressions": regressions,
                         "n_regressions": len(regressions),
                         "derives_v62": sorted(derives_v62)})

    # S4 — recommandation : seuil le plus strict réparant l'écart cible sans régression
    cible = "agent-engineering"
    reco = None
    for b in balayage:
        if b["n_regressions"] == 0 and any(r["skill"] == cible for r in b["reparations"]):
            reco = b["seuil"]
            break

    report = {
        "task": "Task 97 G1 — simulation préalable V6.2 (réservation de corpus croisée)",
        "n_skills": len(skills),
        "baseline_voie_m": {k: {"score": v["score"], "derive": v["derive"]}
                            for k, v in baseline.items()},
        "derives_baseline": sorted(derives),
        "diagnostic_s2": diag,
        "balayage_s3": balayage,
        "recommandation_s4": {"seuil_choisi": reco,
                              "cible": cible,
                              "note": "seuil le plus STRICT réparant le cas 6 agent-engineering "
                                      "avec 0 régression voie M sur les 101 skills équipés"},
    }
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"=== Task 97 G1 — SIMULATION V6.2 ({len(skills)} skills équipés) ===")
    print(f"Baseline voie M : {sum(1 for v in baseline.values() if not v['derive'])}/{len(skills)} OK — "
          f"dérives : {sorted(derives)}")
    print("\n--- S2 : diagnostic des cas en désaccord (positive voisine la plus proche) ---")
    for d in diag:
        pv = d["positive_voisine"]
        print(f"  [{d['skill']} cas {d['cas']}] expected={d['expected']} trig_m={d['trig_m']} hits={d['hits']}")
        print(f"    q: {d['query'][:90]}")
        print(f"    voisine: {pv['with']} jaccard={pv['jaccard']} inter={pv['inter']} identique={pv.get('identique', False)}")
        if VERBOSE and pv.get("req"):
            print(f"    req voisine: {pv['req'][:90]}")
    print("\n--- S3 : balayage de seuils ---")
    for b in balayage:
        print(f"  {b['seuil']:<26} réparations={b['n_reparations']} régressions={b['n_regressions']} dérives={b['derives_v62']}")
        for r in b["regressions"]:
            print(f"    REGRESSION: [{r['skill']} cas {r['cas']}] jaccard={r['jaccard']} avec {r['avec']} — {r['query'][:70]}")
    print(f"\n--- S4 : recommandation --- seuil choisi : {reco}")
    print(f"JSON : {OUT}")
    sys.exit(0)


if __name__ == "__main__":
    main()
