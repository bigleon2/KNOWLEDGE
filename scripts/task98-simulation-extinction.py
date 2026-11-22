#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Task 98 — Harnais de SIMULATION PRÉALABLE (règle d'or n°5 : mesurer avant corriger).

Directives couvertes : GO propriétaire trace 1a1df74c670cddc1 (« GO avec ma clé
<PAT> » — item 2 : extinction des résidus triggers, voies documentées Task 97
G1.5) ; contexte : arbitre check-triggers-replay.py V6.2 (Task 97) rejeu 99/101,
2 skills en dérive, 4 cas non résolus :
  - midi-doc-expert cas 5 « Valide la conformité de ce TSI au schéma de
    référence. » (attendu False, trig True — hits {refer, valid}) ;
  - re-curation cas 1 « Re-cure mon skill version-management, il est trop lourd
    à charger. » (attendu True, trig False — hits {skill}) ;
  - re-curation cas 7 « re-cure l'élément n°1 de la liste priorisée. » (attendu
    True, trig False — hits {elem}) ;
  - re-curation cas 10 « Optimise les dépendances npm de ce projet web. »
    (attendu False, trig True — hits {depend, optimis}).

Voies d'extinction à simuler (AVANT toute modification — jamais de re-jeu à
l'identique sans mesure) :
  Δ1 — champ `exclusifs` (veto V6.1, par cas, précédent Task 30 « vetos croisés »)
       sur midi-doc-expert cas 5 : ["valide la conformité"] (sémantique : la
       validation de conformité relève de tsi-validator, jamais de la doc) ;
  Δ2 — champ `exclusifs` sur re-curation cas 10 : ["npm"] (terme distinctif,
       absent de toute positive re-curation) ;
  Δ3 — enrichissement lexique ADDITIF de la description de re-curation :
       ' (forme verbale : "re-cure")' — la découpe [a-zà-ÿ]+ de keywords_for
       produit le radical « cure » ∈ lexique (les TAGS ne conviennent PAS :
       non découpés sur le tiret, un tag « re-cure » ne matcherait jamais le
       token « cure » — constat d'enquête E1-E2 Task 98) → les cas 1/7 passent
       à ≥ 2 hits {skill, cure} / {elem, cure} → voie M True attendue.

Sections :
  S1 — baseline 4 couches (veto → voie M → cache L → V6.2, réplique EXACTE de
       main() de check-triggers-replay.py par import de ses fonctions — zéro
       duplication R4) → attendu 99/101 (contrôle de cohérence avec le rapport
       en place) ;
  S2 — effet de chaque delta isolément (diagnostic) ;
  S3 — rejeu global avec Δ1+Δ2+Δ3 → attendu 101/101 avec EXACTEMENT les 4
       réparations cibles et 0 régression / 0 autre changement de verdict ;
  S4 — recommandation GO/NO-GO.

Sortie : task98-simulation-report.json À CÔTÉ DU PRÉSENT SCRIPT (déterministe,
sans horloge — idempotent : re-exécution = rapport identique). Lecture seule
sur l'écosystème (aucune écriture dans le dépôt cible).
rc : 0 = GO (101/101 simulé, 0 régression) · 1 = NO-GO · 2 = usage.
Usage : python3 task98-simulation-extinction.py [CHEMIN_DÉPÔT]
"""
# ⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.45)
# SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
# Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
# Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
# Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
# Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
# Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).

import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else HERE.parent
ARBITRE = REPO / "scripts" / "check-triggers-replay.py"
OUT = HERE / "task98-simulation-report.json"

# ── Deltas simulés (aucun n'est appliqué aux fichiers — mémoire seulement) ──
EXCLUSIFS_DELTAS = {
    ("midi-doc-expert",
     "Valide la conformité de ce TSI au schéma de référence."): ["valide la conformité"],
    ("re-curation",
     "Optimise les dépendances npm de ce projet web."): ["npm"],
}
DESC_EXTRA = {
    "re-curation": ' (forme verbale : "re-cure")',
}
CIBLES = [
    ("midi-doc-expert", "Valide la conformité de ce TSI au schéma de référence."),
    ("re-curation", "Re-cure mon skill version-management, il est trop lourd à charger."),
    ("re-curation", "re-cure l'élément n°1 de la liste priorisée."),
    ("re-curation", "Optimise les dépendances npm de ce projet web."),
]


def charger_arbitre():
    spec = importlib.util.spec_from_file_location("ctr_task98", ARBITRE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def rejeu(ctr, exclusifs_delta=None, desc_extra=None):
    """Réplique EXACTE du pipeline de verdict de main() (passe 1-3, couches 1-4)
    — via les fonctions de l'arbitre importé (aucune divergence de réplique)."""
    exclusifs_delta = exclusifs_delta or {}
    desc_extra = desc_extra or {}
    equipped = []
    for sdir in sorted(ctr.SKILLS.iterdir()):
        if not sdir.is_dir() or sdir.name.startswith(("_", ".")) or sdir.name == "@mon-ecosysteme":
            continue
        if (sdir / "evals" / "trigger_evals.json").exists():
            equipped.append(sdir)
    loaded, ignores = [], []
    for sdir in equipped:
        sk = ctr.load_skill(sdir)
        if not (isinstance(sk["cases"], list)
                and all(isinstance(c, dict) and "query" in c and "should_trigger" in c
                        for c in sk["cases"])):
            ignores.append(sdir.name)
            continue
        desc = sk["desc"] + desc_extra.get(sk["name"], "") if desc_extra.get(sk["name"]) else sk["desc"]
        sk["kws"] = ctr.keywords_for(sk["name"], desc, sk["tags"])
        sk["strong"] = {ctr.stem(p) for p in sk["name"].split("-")}
        loaded.append(sk)
    idx_positives = ctr.build_index_positives(loaded)
    cache_l = ctr.load_cache_voie_l()
    verdicts = {}
    for sk in loaded:
        kws, strong = sk["kws"], sk["strong"]
        for c in sk["cases"]:
            q, exp = c["query"], c["should_trigger"]
            exclusifs = c.get("exclusifs")
            if (sk["name"], q) in exclusifs_delta:
                exclusifs = list(exclusifs or []) + exclusifs_delta[(sk["name"], q)]
            # couche 1 — veto exclusifs V6.1 (avant scoring)
            if ctr.veto_exclusif(q, exclusifs):
                verdicts[(sk["name"], q)] = {"ok": exp is False, "source": "veto-exclusif"}
                continue
            # couche 2 — voie M (scoring, inchangé)
            score, hits, trig = ctr.heuristic_score(q, kws, strong)
            if trig == exp:
                verdicts[(sk["name"], q)] = {"ok": True, "source": "voie-m",
                                             "hits": hits, "score": round(score, 3)}
                continue
            # couche 3 — cache voie L (lecture seule, désaccord)
            entree = cache_l.get(f"{sk['name']}::{q}")
            if isinstance(entree, dict) and "verdict" in entree:
                ok = bool(entree["verdict"]) == bool(exp)
                verdicts[(sk["name"], q)] = {"ok": ok,
                                             "source": "voie-l-cache" if ok else "voie-l-cache-desaccord",
                                             "hits": hits}
                continue
            # couche 4 — V6.2 réservation de corpus croisée (non-résolus seulement)
            resv = ctr.reserve_corpus(q, sk["name"], idx_positives)
            if resv:
                verdicts[(sk["name"], q)] = {"ok": exp is False, "source": "v62-reservation-corpus",
                                             "hits": hits}
            else:
                verdicts[(sk["name"], q)] = {"ok": False, "source": "non-resorbe", "hits": hits}
    return verdicts, ignores


def bilan(verdicts):
    """Agrège par skill : score officiel ok/total (comme le rapport de l'arbitre)."""
    par_skill = {}
    for (name, q), v in verdicts.items():
        s = par_skill.setdefault(name, {"ok": 0, "total": 0})
        s["total"] += 1
        s["ok"] += 1 if v["ok"] else 0
    derives = sorted(n for n, s in par_skill.items() if s["ok"] < s["total"])
    return {"n_skills": len(par_skill), "skills_ok": len(par_skill) - len(derives),
            "skills_derive": derives, "par_skill": par_skill}


def main():
    if not ARBITRE.exists():
        print(f"ABANDON : arbitre introuvable — {ARBITRE}")
        return 2
    ctr = charger_arbitre()

    # S1 — baseline (4 couches, aucun delta)
    v1, ignores = rejeu(ctr)
    b1 = bilan(v1)

    # S2 — deltas isolés (diagnostic)
    v_d1, _ = rejeu(ctr, exclusifs_delta={k: EXCLUSIFS_DELTAS[k] for k in
                     [k for k in EXCLUSIFS_DELTAS if k[0] == "midi-doc-expert"]})
    v_d2, _ = rejeu(ctr, exclusifs_delta={k: EXCLUSIFS_DELTAS[k] for k in
                     [k for k in EXCLUSIFS_DELTAS if k[0] == "re-curation" and "npm" in EXCLUSIFS_DELTAS[k]]})
    v_d3, _ = rejeu(ctr, desc_extra=DESC_EXTRA)
    iso = {}
    for label, vd in (("Δ1 exclusifs midi-doc-expert cas 5", v_d1),
                      ("Δ2 exclusifs re-curation cas 10", v_d2),
                      ("Δ3 lexique description re-curation", v_d3)):
        repar = [(f"{n} :: {q[:60]}", vd[(n, q)]["source"])
                 for (n, q) in v1 if not v1[(n, q)]["ok"] and vd[(n, q)]["ok"]]
        regre = [(f"{n} :: {q[:60]}", vd[(n, q)]["source"])
                 for (n, q) in v1 if v1[(n, q)]["ok"] and not vd[(n, q)]["ok"]]
        iso[label] = {"reparations": repar, "regressions": regre}

    # S3 — rejeu global avec Δ1+Δ2+Δ3
    v3, _ = rejeu(ctr, exclusifs_delta=EXCLUSIFS_DELTAS, desc_extra=DESC_EXTRA)
    b3 = bilan(v3)
    reparations, regressions, autres = [], [], []
    for cle in v1:
        a, b = v1[cle], v3[cle]
        if not a["ok"] and b["ok"]:
            reparations.append({"skill": cle[0], "query": cle[1],
                                "source_avant": a["source"], "source_apres": b["source"],
                                "cible": [cle[0], cle[1]] in [[c[0], c[1]] for c in CIBLES]})
        elif a["ok"] and not b["ok"]:
            regressions.append({"skill": cle[0], "query": cle[1],
                                "source_avant": a["source"], "source_apres": b["source"]})
        elif a["source"] != b["source"]:
            autres.append({"skill": cle[0], "query": cle[1],
                           "source_avant": a["source"], "source_apres": b["source"]})

    cibles_reparees = {c for c in CIBLES if not v1[c]["ok"] and v3[c]["ok"]}
    go = (b3["n_skills"] == b1["n_skills"]
          and not b3["skills_derive"]
          and not regressions
          and len(reparations) == len(cibles_reparees) == 4
          and cibles_reparees == set(CIBLES)
          and not [r for r in reparations if not r["cible"]])

    rapport = {
        "task": "Task 98 — simulation préalable extinction résidus triggers (GO propriétaire 1a1df74c670cddc1)",
        "depot": str(REPO),
        "methode": "réplique exacte des 4 couches de main() par import des fonctions de check-triggers-replay.py (zéro duplication R4)",
        "s1_baseline": {"verdict": f"{b1['skills_ok']}/{b1['n_skills']}",
                        "skills_derive": b1["skills_derive"],
                        "attendu": "99/101 (contrôle cohérence rapport en place)",
                        "coherent": b1["skills_ok"] == 99 and b1["n_skills"] == 101},
        "s2_deltas_isoles": iso,
        "s3_rejeu_global": {"verdict": f"{b3['skills_ok']}/{b3['n_skills']}",
                            "skills_derive": b3["skills_derive"],
                            "reparations": reparations,
                            "regressions": regressions,
                            "autres_changements_source": autres},
        "s4_recommandation": {
            "verdict": "GO" if go else "NO-GO",
            "conditions": ["101/101 simulé", "exactement 4 réparations = les 4 cibles",
                           "0 régression", "0 autre changement de verdict"],
            "deltas_a_implanter": {
                "exclusifs": [f"{n} :: {q[:60]} → {t}" for (n, q), t in EXCLUSIFS_DELTAS.items()],
                "description_additive": {n: t for n, t in DESC_EXTRA.items()},
            },
        },
        "ignores_schema_non_canonique": ignores,
    }
    OUT.write_text(json.dumps(rapport, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")

    print(f"S1 baseline : {b1['skills_ok']}/{b1['n_skills']} — dérives : {b1['skills_derive'] or 'aucune'}")
    for label, d in iso.items():
        print(f"S2 {label} : réparations {len(d['reparations'])} · régressions {len(d['regressions'])}")
    print(f"S3 rejeu global : {b3['skills_ok']}/{b3['n_skills']} — dérives : {b3['skills_derive'] or 'aucune'}")
    print(f"S3 réparations : {len(reparations)} (cibles : {sum(1 for r in reparations if r['cible'])}/4) · "
          f"régressions : {len(regressions)} · autres changements de source : {len(autres)}")
    print(f"S4 RECOMMANDATION : {'GO' if go else 'NO-GO'} — rapport : {OUT}")
    return 0 if go else 1


if __name__ == "__main__":
    sys.exit(main())
