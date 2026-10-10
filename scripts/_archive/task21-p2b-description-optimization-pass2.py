#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Task 21 — F1 (finir P2) : Description Optimization pass 2 (protocole A10/A14, R2).
Cible : 3 cas chirurgicaux (radicaux issus de la DESCRIPTION) + validation locale zéro-API.
Les 7 cas structurels (radical du NOM du skill) sont consignés (réserve 1 Task 19 / plan §6),
pas « réparés » de force — KO-L003 : jamais ajuster les cas pour coller au verdict.

Chirurgies (chacune validée contre le stemmer SHARED §7 v2 répliqué par l'arbitre V6) :
  correct-work        : « gen-plan » → « genplan » dans la description (tue le radical 'plan'
                        issu de la coupure findall du trait d'union) — FP « plan d'action…projet »
                        passe de hits={plan,projet} à {projet} → muet. PM-couplé : pas de bump.
  prompt-engineering  : desc « évaluation, itération et validation des déclencheurs (trigger_evals) »
                        → « évaluation et validation des déclencheurs officiels » ; «, évals» retiré ;
                        tag « iteration » retiré (les tags injectent des radicaux !) — FP1 passe de
                        {eval,iter,trigger} à {eval} → muet. FP2 « …à partir de ce prompt » = radical
                        du NOM → structurel consigné. Bump 2.1.0 → 2.2.0.
  script-creator      : « un nouveau script » → « un script » ; « conventions d'évals et de
                        description » → « conventions de description » — FP passe de
                        {eval,nouv,skill} à {skill} → muet. Bump 1.0.0 → 1.1.0.
Idempotent : ré-exécution = mêmes verdicts (remplacements exacts, échec si motif absent et
déjà appliqué détecté par vérification préalable).
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

ECO = Path("/home/z/my-project/ecosystem")
REPORT = ECO / "scripts" / "task21-p2b-optimization-report.json"

# ---------- charge l'arbitre V6 comme module (source de vérité du scoring) ----------
spec = importlib.util.spec_from_file_location("v6", ECO / "scripts" / "check-triggers-replay.py")
v6 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v6)

STOP = getattr(v6, "STOP", set())
stem, norm, keywords_for, heuristic_score = v6.stem, v6.norm, v6.keywords_for, v6.heuristic_score


def score_skill(name, desc, tags, cases):
    kws = keywords_for(name, desc, tags)
    strong = {stem(p) for p in name.split("-")}
    out = []
    for q, expected in cases:
        _, hits, trig = heuristic_score(q, kws, strong)
        out.append({"query": q, "expected": expected, "trigger_m": trig, "hits": hits,
                    "ok": trig == expected})
    return out


def load_evals(skill):
    ev = json.loads((ECO / "skills" / skill / "evals" / "trigger_evals.json").read_text(encoding="utf-8"))
    cases = ev["cases"] if isinstance(ev, dict) else ev
    return [(c["query"], bool(c["should_trigger"])) for c in cases]


# ---------- chirurgies ----------
EDITS = [
    {
        "skill": "correct-work", "bump": None, "note": "PM-couplé (v2.7.0) — révision documentaire sans bump (précédent pass 1)",
        "edits": [
            ("couplage gen-plan OBLIGATOIRE", "couplage genplan OBLIGATOIRE"),
        ],
        "tag_removals": [],
    },
    {
        "skill": "prompt-engineering", "bump": ("2.1.0", "2.2.0"),
        "note": "FP2 « à partir de ce prompt » = radical du NOM (structurel, consigné)",
        "edits": [
            ("évaluation, itération et validation des\n  déclencheurs (trigger_evals)",
             "évaluation et validation des\n  déclencheurs officiels"),
            ("(PMs, SKILL.md, évals)", "(PMs, SKILL.md)"),
        ],
        "tag_removals": ["iteration"],
    },
    {
        "skill": "script-creator", "bump": ("1.0.0", "1.1.0"),
        "note": "",
        "edits": [
            ("souhaite créer un nouveau script,", "souhaite créer un script,"),
            ("conventions d'évals et\n  de description héritées", "conventions\n  de description héritées"),
        ],
        "tag_removals": [],
    },
]

report = {"date": "2026-10-03", "task": "Task 21 — F1 (finir P2) : Description Optimization pass 2",
          "protocole": "A10/A14 (R2), validation locale zéro-API, contrôles négatifs préservés, KO-L003",
          "skills": {}, "structural_cases_consigned": [
              {"skill": "agent-creator", "query": "Automatise ce workflow avec Zapier plutôt qu'avec un agent.",
               "radical": "agent (nom)", "voie_l": "NON×3 (ratio 0.0) — baseline P3 19:41"},
              {"skill": "audio-metadata", "query": "Transcris le contenu parlé de ce fichier audio.",
               "radical": "audio (nom)", "voie_l": "NON×3 (ratio 0.0) — baseline P3 19:41"},
              {"skill": "pdf-llm", "query": "3 cas « rapport/génère/fusionne PDF » (génération ≠ extraction)",
               "radical": "pdf (nom)", "voie_l": "NON (0.0 / 0.0 / 0.333<0.5) — baseline P3 19:41"},
              {"skill": "prompt-engineering", "query": "Crée carrément un nouveau skill à partir de ce prompt.",
               "radical": "prompt (nom)", "voie_l": "à compléter F3 (P3 : 1 NON, 2 nulls 429)"},
              {"skill": "script-mon-ecosysteme-infrastructure", "query": "Lance l'installation complète de l'écosystème sur ce profil.",
               "radical": "ecosystem (nom)", "voie_l": "cas ambigu : L déclenche aussi (0.667) — révision du cas au propriétaire"},
              {"skill": "script-reviewer", "query": "Crée un nouveau script qui compte les entrées de la KB.",
               "radical": "script (nom)", "voie_l": "à mesurer F3"},
              {"skill": "skills-inventory", "query": "2 cas « cherche sur le hub / installe » (inventaire ≠ installation)",
               "radical": "skill (nom)", "voie_l": "NON×3 ×2 (0.0) — baseline P3 19:41"},
          ], "c006": {"skill": "version-management", "decision": "(b) voie L seule assumée et consignée — "
                      "voie M structurellement aveugle au zh (stemmer français) ; voie L réelle : positifs OUI 3/3, "
                      "négatifs 0.0 (P3) ; réversible vers (a) sur directive"}}

exit_code = 0
for spec_edit in EDITS:
    skill = spec_edit["skill"]
    smd_path = ECO / "skills" / skill / "SKILL.md"
    text = smd_path.read_text(encoding="utf-8")
    applied, already = [], []
    for old, new in spec_edit["edits"]:
        if new in text and old not in text:
            already.append(old)
            continue
        if old not in text:
            print(f"[KO] {skill}: motif absent ET remplacement absent : {old[:60]!r}")
            exit_code = 1
            continue
        text = text.replace(old, new, 1)
        applied.append(old)
    for tag in spec_edit["tag_removals"]:
        pat = re.compile(rf"^[ \t]*-[ \t]+{re.escape(tag)}[ \t]*\n", re.M)
        if pat.search(text):
            text = pat.sub("", text, count=1)
            applied.append(f"tag:{tag}")
        else:
            already.append(f"tag:{tag}")
    if spec_edit["bump"] and spec_edit["bump"][0] in text:
        text = text.replace(f"version: {spec_edit['bump'][0]}", f"version: {spec_edit['bump'][1]}", 1)
        applied.append(f"version:{spec_edit['bump'][0]}→{spec_edit['bump'][1]}")
    smd_path.write_text(text, encoding="utf-8")
    report["skills"][skill] = {"applied": applied, "already": already, "note": spec_edit["note"]}

# ---------- validation locale zéro-API (arbitre V6 comme module) ----------
print("\n=== VALIDATION LOCALE (voie M, zéro API) ===")
for spec_edit in EDITS:
    skill = spec_edit["skill"]
    cases = load_evals(skill)
    smd_path = ECO / "skills" / skill / "SKILL.md"
    fm = smd_path.read_text(encoding="utf-8").split("---")[1]
    desc_m = re.search(r"description:\s*>-?\s*\n((?:[ \t]+.*\n)+)", fm)
    desc = " ".join(l.strip() for l in desc_m.group(1).splitlines())
    tags_m = re.search(r"tags:\s*\n((?:\s+-\s+.*\n)+)", fm)
    tags = re.findall(r"-\s+(.+)", tags_m.group(1)) if tags_m else []
    res = score_skill(skill, desc, tags, cases)
    n_ok = sum(1 for r in res if r["ok"])
    fails = [r for r in res if not r["ok"]]
    report["skills"][skill]["post"] = f"{n_ok}/{len(res)}"
    report["skills"][skill]["fails_post"] = [
        {"query": f["query"], "expected": f["expected"], "hits": f["hits"]} for f in fails]
    print(f"  {skill}: {n_ok}/{len(res)}" + ("" if not fails else f"  fails: {[(f['expected'], f['hits']) for f in fails]}"))
    if any(not f["ok"] and f["expected"] is False for f in fails):
        # un FP non consigné survivrait → échec dur
        structural = [f for f in fails if not f["expected"]]
        non_consigned = [f for f in structural if f["hits"] and
                         not (set(f["hits"]) & {stem(p) for p in skill.split("-")})]
        if non_consigned:
            print(f"  [KO] FP NON consigné restant : {non_consigned}")
            exit_code = 1

REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"\nRapport : {REPORT}")
sys.exit(exit_code)
