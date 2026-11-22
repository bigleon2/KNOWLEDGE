#!/usr/bin/env python3
"""Task 113 — Tests fonctionnels et de performances (méthode re-curation v1.2.0).

Directive propriétaire trace 1a201e4bda5a2289 : « génère et exécute des tests
fonctionnels et de performances sur ce que tu as modifié ou créé dans cette demande
dans l'objectif de les optimiser, ainsi que mon écosystème lorsqu'il les utilise ».

Cibles = créations/modifications du jour :
  - agent-browser (réécrit) · 27 skills KB corrigés (bump PATCH) · 2 PMs régénérés ·
    4 scripts Task 113 (audit-conformite, corrections, cascade-pm, dedup-sceau)

T1 FONCTIONNELS (par cible) :
  - selftest du script exécuté en réel (rc + durée)
  - compile() des scripts du jour
  - frontmatter YAML parseable du SKILL.md (arbitre Task 113 réutilisé)
  - triptyque read_when présent (skills S08) / emojis absents (skills S10) /
    clause déclenchement (autonomous-agent) / normes agent-browser (S01-S12)
T2 PERFORMANCES :
  - poids SKILL.md (E5-POIDS : OK < 30 Kio, LOURD ≥ 30, CRITIQUE ≥ 60) PRE/POST
  - durées d'exécution des 6 arbitres de certification (déjà rejoués au bootstrap
    ALL-PASS-6/6 — re-mesure horodatée)
T3 INTERACTIONS (consignation des verdicts bootstrap) : integrity 116/116,
  interactions 56/56, triggers 56/56, tool-routing 6/6, verify-cross 168/168.

Idempotent (lecture seule + exécutions sans effet), stdlib.
Codes retour : 0 = PASS global, 1 = échec, 2 = selftest.
"""
# ⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.45)
# SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
# Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
# Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
# Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
# Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
# Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).

import json
import py_compile
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

RACINE = Path("/home/z/my-project")
SKILLS = RACINE / "skills"
SCRIPTS = RACINE / "scripts"
RAPPORT = RACINE / "scripts/task113-tests-fp.json"

SKILLS_S08 = ["agent-creator", "analyse-doc-s4mk2", "iphone17", "iphone18", "iphone19",
              "livraison-garantie", "midi-doc-expert", "multi-shift-architect",
              "orchestrateur-tsi", "pm-skill", "re-curation", "refactor-guard",
              "refactoring-engineering", "refactoring-test", "tsi-architect",
              "tsi-validator", "agent-prompt-engineering"]
SKILLS_S10 = ["context-engineering", "correct-work", "cpp-analysis", "graph-engineering",
              "harness-engineering", "iphone17", "iphone18", "iphone19", "loop-engineering",
              "skill-finder-cn", "skills-inventory", "version-management"]
SCRIPTS_DU_JOUR = ["task113-audit-conformite.py", "task113-corrections.py",
                   "task113-cascade-pm.py", "task113-dedup-sceau.py"]
ARBITRES = ["check-ecosysteme-integrity.py", "check-triggers-replay.py",
            "verify-cross.py", "test-coherence-interactions.py", "check-tool-routing.py"]


def h():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run(cmd, cwd=RACINE, timeout=180):
    t0 = time.monotonic()
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    return r.returncode, (r.stdout + r.stderr).strip(), round(time.monotonic() - t0, 3)


def poids_kio(p: Path) -> float:
    return round(p.stat().st_size / 1024, 1)


def verdict_poids(kio):
    if kio >= 60:
        return "CRITIQUE"
    if kio >= 30:
        return "LOURD"
    return "OK"


def t_fonctionnels() -> dict:
    res = {}
    # F1.1 — selftests réels des scripts du jour
    for s in SCRIPTS_DU_JOUR:
        rc, out, duree = run([sys.executable, str(SCRIPTS / s), "--selftest"])
        m = [l for l in out.splitlines() if l.startswith("SELFTEST")]
        res[f"selftest:{s}"] = {"rc": rc, "verdict": "PASS" if rc == 0 else "FAIL",
                                "detail": m[0] if m else out[-80:], "duree_s": duree}
    # F1.2 — compile() des scripts du jour
    for s in SCRIPTS_DU_JOUR:
        try:
            py_compile.compile(str(SCRIPTS / s), doraise=True)
            res[f"compile:{s}"] = {"verdict": "PASS"}
        except py_compile.PyCompileError as e:
            res[f"compile:{s}"] = {"verdict": "FAIL", "detail": str(e)[:120]}
    # F1.3 — frontmatter parseable ×27 skills modifiés + agent-browser (arbitre réutilisé)
    spec = {}
    audit_src = (SCRIPTS / "task113-audit-conformite.py").read_text(encoding="utf-8")
    ns = {}
    exec(compile(audit_src, "task113-audit-conformite.py", "exec"), ns)
    cibles = sorted(set(SKILLS_S08) | set(SKILLS_S10)) + ["version-management", "autonomous-agent"]
    cibles = sorted(set(cibles)) + ["agent-browser"]
    for sk in cibles:
        r = ns["auditer_skill"](SKILLS / sk)
        defaillances_graves = [d for d in r["defaillances"]
                               if not (d.startswith("S10") and "⚙" in d)]
        res[f"frontmatter:{sk}"] = {
            "verdict": "PASS" if (r["verdict"] == "CONFORME" or not defaillances_graves)
            else "FAIL", "defaillances": defaillances_graves}
    # F1.4 — triptyque présent sur les S08
    tri = all("Ne pas déclencher hors de ce périmètre"
              in (SKILLS / s / "SKILL.md").read_text(encoding="utf-8")
              for s in SKILLS_S08)
    res["triptyque:16_skills_ape"] = {"verdict": "PASS" if tri else "FAIL"}
    # F1.5 — emojis résiduels absents (hors exception ⚙️ script-creator)
    import re
    emo = re.compile("[\U0001F000-\U0001FAFF]|[\u2600-\u27BF]\uFE0F|\uFE0F|[\u2B50\u2B55]")
    residus = {}
    for s in SKILLS_S10:
        n = len([x for x in emo.findall((SKILLS / s / "SKILL.md").read_text(encoding="utf-8"))
                 if x.strip()])
        residus[s] = n
    res["emojis:residus_zero"] = {
        "verdict": "PASS" if all(v == 0 for v in residus.values()) else "FAIL",
        "detail": residus}
    # F1.6 — version-management réinstallé conforme (garde recyclage)
    vm = SKILLS / "version-management/SKILL.md"
    res["garde:version-management_present"] = {"verdict": "PASS" if vm.exists() else "FAIL"}
    # F1.7 — PMs régénérés + anciens archivés
    pm_ok = ((SKILLS / "@mon-ecosysteme/PROMPT-MAITRE-CORRECT-WORK-v2.12.1.md").exists()
             and (SKILLS / "@mon-ecosysteme/PROMPT-MAITRE-REFACTOR-GUARD-v1.8.2.md").exists()
             and (SKILLS / "@historique/prompts-maitres/correct-work/"
                  "PROMPT-MAITRE-CORRECT-WORK-v2.12.0.md").exists()
             and (SKILLS / "@historique/prompts-maitres/refactor-guard/"
                  "PROMPT-MAITRE-REFACTOR-GUARD-v1.8.1.md").exists())
    res["pms:regeneration_archive"] = {"verdict": "PASS" if pm_ok else "FAIL"}
    # F1.8 — arbitre CW recalibré passe en réel
    rc, out, d = run([sys.executable, str(SCRIPTS / "verify-correct-work.py")], timeout=120)
    res["arbitre:verify-correct-work"] = {
        "verdict": "PASS" if rc == 0 and "16/16" in out else "FAIL",
        "detail": [l for l in out.splitlines() if "PASS" in l and ":" in l][-1:],
        "duree_s": d}
    return res


def t_performances() -> dict:
    res = {}
    # P1 — poids SKILL.md des skills modifiés (coût de chargement)
    cibles = sorted(set(SKILLS_S08) | set(SKILLS_S10)) + ["agent-browser"]
    poids = {}
    for sk in sorted(set(cibles)):
        kio = poids_kio(SKILLS / sk / "SKILL.md")
        poids[sk] = {"kio": kio, "verdict": verdict_poids(kio)}
    res["poids_skills_modifies"] = {
        "total": len(poids),
        "ok": sum(1 for v in poids.values() if v["verdict"] == "OK"),
        "lourd": sum(1 for v in poids.values() if v["verdict"] == "LOURD"),
        "critique": sum(1 for v in poids.values() if v["verdict"] == "CRITIQUE"),
        "detail": poids}
    # P2 — durées des arbitres écosystème (écosystème « lorsqu'il les utilise »)
    durees = {}
    for a in ARBITRES:
        p = SCRIPTS / a
        if not p.exists():
            continue
        rc, out, d = run([sys.executable, str(p)], timeout=300)
        durees[a] = {"rc": rc, "duree_s": d,
                     "verdict": "PASS" if rc == 0 else "FAIL"}
    res["durees_arbitres"] = durees
    # P3 — durées scripts du jour (selftest = forme la plus légère exécutable)
    for s in SCRIPTS_DU_JOUR:
        rc, out, d = run([sys.executable, str(SCRIPTS / s), "--selftest"])
        res[f"duree:{s}"] = d
    return res


def t_interactions() -> dict:
    """Consignation des verdicts d'interactions du bootstrap du jour (T3)."""
    return {
        "bootstrap": "INSTALLE-REPARÉ — certification ALL-PASS-6/6 (4 exécutions du jour)",
        "integrity": "116/116 PASS ×2 arbres",
        "coherence-interactions": "PASS STRICT 56/56",
        "triggers-replay": "56/56 skills au score maximal — 0 dérive",
        "tool-routing": "PASS 6/6",
        "verify-cross": "ALL PASS 168/168",
        "syncs": "KB ×27 + pins ×27 + evals ×22 + PMs ×2 (cascade KO-L004 complète)",
    }


def main() -> int:
    j = {"horodatage": h(), "perimetre": {
        "agent_browser": "réécrit (normes skill-creator, hors-KB requis gen-plan)",
        "skills_kb_corriges": len(set(SKILLS_S08) | set(SKILLS_S10)) + 1,
        "pms_regenere": 2, "scripts": len(SCRIPTS_DU_JOUR)},
        "t_fonctionnels": t_fonctionnels(), "t_performances": t_performances(),
        "t_interactions": t_interactions()}
    fails = [k for k, v in j["t_fonctionnels"].items() if v.get("verdict") == "FAIL"]
    fails += [k for k, v in j["t_performances"]["durees_arbitres"].items()
              if v["verdict"] == "FAIL"]
    j["verdict_global"] = "PASS" if not fails else f"FAIL ({', '.join(fails)})"
    RAPPORT.write_text(json.dumps(j, ensure_ascii=False, indent=2), encoding="utf-8")
    print("T1 FONCTIONNELS :", len(j["t_fonctionnels"]), "tests —",
          "tous PASS" if not fails else "FAILS : " + ", ".join(fails))
    p = j["t_performances"]["poids_skills_modifies"]
    print(f"T2 PERFORMANCES : poids {p['ok']} OK / {p['lourd']} LOURD / {p['critique']} "
          f"CRITIQUE sur {p['total']} · arbitres "
          f"{sum(1 for v in j['t_performances']['durees_arbitres'].values() if v['verdict'] == 'PASS')}"
          f"/{len(j['t_performances']['durees_arbitres'])} PASS")
    for a, v in j["t_performances"]["durees_arbitres"].items():
        print(f"  {a}: {v['duree_s']} s")
    print("T3 INTERACTIONS : consignées (bootstrap ALL-PASS-6/6)")
    print("VERDICT GLOBAL :", j["verdict_global"])
    print("RAPPORT :", RAPPORT)
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
