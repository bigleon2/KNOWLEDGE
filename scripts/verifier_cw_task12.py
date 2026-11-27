#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 12 — correct-work (projet) --bloc : vérification mécanique → JSON de preuve.

Couvre : plan + amendement E13 (D011, précision trace 1a21e38435b96641), PM-INSTALL
v1.10.7/8 + exécuteurs (D001-D002), skill orchestration-disciplines v1.0.0 (D005),
gen-plan v3.49.0 + cascade KO-L004 + adaptations audit F1-F3 (D003-D004-D006-D011),
sécurité jeton (KO-L009), différés + pendances (D010), worklogs. Idempotent ×2
(lecture seule : seuls selftests/arbitres sans mutation sont re-joués).
"""
# ⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.47)
# SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
# Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
# Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
# Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan).

import json
import re
import subprocess
from pathlib import Path

PROJ = Path("/home/z/my-project")
REPO = PROJ / "KNOWLEDGE-repo"
OUT = PROJ / "scripts/cw-task12-projet-report.json"

checks = []


def check(bloc, cid, critere, ok, preuve):
    checks.append({"bloc": bloc, "id": cid, "critere": critere,
                   "verdict": "PASS" if ok else "FAIL", "preuve": preuve})


def run(cmd, cwd=None):
    return subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)


# B1 — Plan + amendement E13 (D011)
plan = (PROJ / "download/plan-task12-optimisation-gen-plan-pm-install.md").read_text(encoding="utf-8")
check("B1 plan", "F1", "plan Task 12 avec answer key D001-D011 (11 décisions)",
      len(re.findall(r"decision: D\d{3}", plan)) == 11, "11 décisions")
check("B1 amendement", "F2", "amendement E13 intégré (trace 1a21e38435b96641 + D011 audit déduplication)",
      "1a21e38435b96641" in plan and "D011" in plan and "F1" in plan and "F5" in plan,
      "amendement + conclusions F1-F5 au plan")
check("B1 E8", "F3", "verdict E8 re-validé après amendement (PASS 11 décisions, horodatage 18:25Z)",
      "Verdict E8 : PASS" in plan and "2026-11-28T18:25Z" in plan, "re-validation consignée")
pp = run(["python3", str(REPO / "skills/gen-plan/scripts/check_plan_protocol.py"),
          "--plan", str(PROJ / "download/plan-task12-optimisation-gen-plan-pm-install.md"),
          "--worklog", str(PROJ / "worklog.md")])
check("B1 protocole", "F4", "check_plan_protocol P1-P5 PASS (re-validation mécanique)",
      pp.returncode == 0, pp.stdout.strip().splitlines()[-1] if pp.stdout else "rc=%d" % pp.returncode)
wl_hote = (PROJ / "worklog.md").read_text(encoding="utf-8")
check("B1 worklog-hôte", "F5", "worklog hôte : entrée E13 (précision déduplication) + PLAN-AFFICHE",
      "1a21e38435b96641" in wl_hote and "PLAN-AFFICHE" in wl_hote.split("1a21e38435b96641")[-1][:2000],
      "journalisation E13 append-only")

# B2 — PM-INSTALL v1.10.7/8 + exécuteurs (D001, D002)
pmi = (REPO / "skills/@mon-ecosysteme/PROMPT-MAITRE-INSTALL-ECOSYSTEME.md").read_text(encoding="utf-8")
check("B2 pm-install", "F6", "PM-INSTALL v1.10.8 + historiques v1.10.7 (C1-C5) et v1.10.8",
      "Version : 1.10.8" in pmi and "| v1.10.7 |" in pmi and "| v1.10.8 |" in pmi,
      "v1.10.8 courante, 2 entrées §7")
check("B2 clauses", "F7", "5 correctifs C1-C5 présents (garde AMORÇABLE, sweep, core.fileMode, pin tolérant, SEEDS-FIRST)",
      all(k in pmi for k in ("AMORÇABLE", "core.fileMode", "SEEDS-FIRST", "sweep-entetes-shared.py", "descendant-tolérant")),
      "C1-C5 dans §7 v1.10.7")
sw = run(["python3", str(REPO / "scripts/sweep-entetes-shared.py"), "--selftest"])
check("B2 sweep", "F8", "sweep-entetes-shared.py selftest OK (idempotent)",
      sw.returncode == 0, (sw.stdout.strip().splitlines() or ["rc=0"])[-1][:80])
shim = (PROJ / "scripts/ensure-installed.py").read_text(encoding="utf-8")
check("B2 shim", "F9", "shim hôte : repli bootstrap canonique (ECO_REPLI_ACTIF)",
      "ECO_REPLI_ACTIF" in shim and "bootstrap-ecosysteme" in shim, "repli amnésie en place")

# B3 — orchestration-disciplines v1.0.0 (D005)
od_repo = (REPO / "skills/orchestration-disciplines/SKILL.md").read_text(encoding="utf-8")
od_host = (PROJ / "skills/orchestration-disciplines/SKILL.md").read_text(encoding="utf-8")
check("B3 skill", "F10", "orchestration-disciplines v1.0.0 installé dépôt + hôte (byte-identique)",
      od_repo == od_host and "version: 1.0.0" in od_repo, "SKILL.md ×2 arbres")
rd = run(["python3", str(REPO / "skills/orchestration-disciplines/scripts/routage-disciplines.py"), "--selftest"])
cc = run(["python3", str(REPO / "skills/orchestration-disciplines/scripts/routage-disciplines.py"), "--check-coherence"])
check("B3 scripts", "F11", "routage-disciplines.py selftest 6/6 + check-coherence rc=0",
      rd.returncode == 0 and cc.returncode == 0,
      "selftest rc=%d · coherence rc=%d" % (rd.returncode, cc.returncode))
kb = (REPO / "skills/KNOWLEDGE.md").read_text(encoding="utf-8")
check("B3 kb", "F12", "KB 57ᵉ entrée + pin ECO_SKILLS 1.0.0",
      "## orchestration-disciplines v1.0.0" in kb and '"orchestration-disciplines": "1.0.0"' in
      (REPO / "scripts/check-ecosysteme-integrity.py").read_text(encoding="utf-8"),
      "entrée KB + ECO_SKILLS")
ev = json.loads((REPO / "skills/orchestration-disciplines/evals/trigger_evals.json").read_text(encoding="utf-8"))
n_pos = sum(1 for c in ev if c.get("should_trigger") is True)
n_neg = sum(1 for c in ev if c.get("should_trigger") is False)
check("B3 evals", "F13", "evals ≥ 5 positifs / ≥ 4 négatifs",
      n_pos >= 5 and n_neg >= 4, "%d+ / %d-" % (n_pos, n_neg))

# B4 — gen-plan v3.49.0 + cascade KO-L004 (D003, D006, D004)
gp = (REPO / "skills/gen-plan/SKILL.md").read_text(encoding="utf-8")
gp_h = (PROJ / "skills/gen-plan/SKILL.md").read_text(encoding="utf-8")
check("B4 version", "F14", "gen-plan v3.49.0 dépôt + hôte (byte-identique)",
      gp == gp_h and "version: 3.49.0" in gp, "SKILL.md ×2 arbres")
check("B4 garde", "F15", "É1-INSTALL v3.49.0 : garde à TOUTE invocation + AMORÇABLE + INSTALLE-POUR-PLAN + SEEDS-FIRST",
      all(k in gp for k in ("garde à TOUTE invocation", "AMORÇABLE", "INSTALLE-POUR-PLAN", "SEEDS-FIRST")),
      "§1.16 étendu")
check("B4 hook-tableau", "F16", "F1 — ligne É5-DISCIPLINES DANS le tableau §1.2bis (adjacente à R2-CACHE, 0 ligne vide intercalée)",
      "| `scripts/cache-verdicts.py` |\n| **É5-DISCIPLINES" in gp, "placement corrigé")
check("B4 dependencies", "F17", "dependencies += orchestration-disciplines >= 1.0.0 + §3 relations",
      "orchestration-disciplines" in gp.split("dependencies:")[1].split("read_when:")[0] and
      "orchestration-disciplines | Hook É5-DISCIPLINES" in gp, "YAML + table §3")
check("B4 pm", "F18", "PM v3.49.0 au corpus + PM v3.48.0 archivé @historique (R4)",
      (REPO / "skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.49.0.md").exists() and
      (REPO / "skills/@historique/prompts-maitres/gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.48.0.md").exists(),
      "corpus v3.49.0 + archive v3.48.0")
shared = (REPO / "skills/@mon-ecosysteme/PROMPT-MAITRE-SHARED.md").read_text(encoding="utf-8")
check("B4 cascade", "F19", "SHARED v1.7.47 + PM-INSTALL v1.10.8 + delta v3490 verrouillé",
      "> **Version** : 1.7.47" in shared and "Version : 1.10.8" in pmi and
      (REPO / "scripts/delta-genplan-v3490.json").exists(),
      "recalibrage croisé générateur")
check("B4 kb-genplan", "F20", "KB gen-plan v3.49.0 (en-tête + Dernière calibration) + pin ECO_SKILLS 3.49.0",
      "## gen-plan v3.49.0" in kb and "montée v3.49.0" in kb and
      '"gen-plan": "3.49.0"' in (REPO / "scripts/check-ecosysteme-integrity.py").read_text(encoding="utf-8"),
      "KB + pin synchrones")
jv = (REPO / "skills/gen-plan/references/journal-versions.md").read_text(encoding="utf-8")
n_entrees = len(re.findall(r"^- \*\*v3\.4[0-9]\.", gp.split("### §5.6")[1], re.M))
check("B4 migration", "F21", "§5.6 entrée courante unique (v3.49.0) + v3.48.0 migrée R4 journal-versions.md",
      n_entrees == 1 and "- **v3.48.0 (" in jv, "1 entrée §5.6 · v3.48.0 en archive")
check("B4 propagation", "F22", "propagation §0 v1.7.47 convergée (0 SKILL.md dépôt à v1.7.46)",
      len(list((REPO / "skills").glob("*/SKILL.md"))) > 0 and
      not any("SHARED v1.7.46)" in p.read_text(encoding="utf-8", errors="ignore")
              for p in (REPO / "skills").glob("*/SKILL.md")),
      "123 skills alignés SHARED vivant")
check("B4 recalibrage", "F23", "recalibrage croisé §11b : 0 citation vive « gen-plan v3.48.0 » dans skills/*/SKILL.md",
      not any("gen-plan v3.48.0" in p.read_text(encoding="utf-8", errors="ignore")
              for p in (REPO / "skills").glob("*/SKILL.md")),
      "classe éteinte (9 lignes : 5 + 4)")
cert = json.loads((PROJ / "scripts/certification-report.json").read_text(encoding="utf-8"))
echecs = sum(a.get("echecs", 1 if "FAIL" in str(a.get("statut", "FAIL")) else 0) for a in cert["arbitres"])
check("B4 certification", "F24", "certification 6 arbitres rc=0 (verdict consolidé, réserves non bloquantes)",
      len(cert["arbitres"]) == 6 and echecs == 0, "6 arbitres, %d échec(s)" % echecs)

# B5 — Audit déduplication D011 (précision propriétaire trace 1a21e38435b96641)
rg = (REPO / "skills/gen-plan/references/regles-or.md").read_text(encoding="utf-8")
check("B5 F2", "F25", "F2 — alignement règle d'or n°9 : §1.16 cite n°9 + regles-or.md porte le raffinement v3.49.0 (rétablissement GRADUÉ)",
      "règle d'or n°9" in gp.split("### §1.16")[1][:4000] and "Raffinement v3.49.0" in rg and "GRADUÉ" in rg,
      "une seule description : n°9 source, É1-INSTALL implémentation")
check("B5 F3", "F26", "F3 — frontière documentée PM-INSTALL §3.2-c (sweep RÉPARATION ↔ sync-context-block INJECTION)",
      "sync-context-block.py" in pmi and "INJECTION" in pmi and "RÉPARATION" in pmi,
      "note de frontière v1.10.8")
rdp = (REPO / "skills/orchestration-disciplines/scripts/routage-disciplines.py").read_text(encoding="utf-8")
check("B5 F4", "F27", "F4 — non-doublon routage-disciplines ↔ routage-skills-agents (tables sources vs frontmatters, verdict = entrée)",
      "disciplines-mobilisation.md" in rdp and "complexite" in rdp and
      (REPO / "skills/gen-plan/scripts/routage-skills-agents.py").exists(),
      "objets distincts, dépendance documentée")
check("B5 F5", "F28", "F5 — non-doublon orchestration-disciplines (garde §1.4 + cross-référence KB resource-monitor « Utilisé par »)",
      "Ce que ce skill N'EST PAS" in od_repo and "orchestration-disciplines (couche C3" in kb,
      "garde anti-duplication + références croisées")

# B6 — Sécurité jeton (KO-L009 — scan motif générique, jamais le jeton)
motif = re.compile(r"github_pat_[A-Za-z0-9_]{20,}|ghp_[A-Za-z0-9]{20,}")
fuites = []
for base in (PROJ / "download", PROJ / "scripts", PROJ / "worklog.md", REPO / "worklog.md", REPO / "skills"):
    fichiers = [base] if base.is_file() else (list(base.rglob("*")) if base.exists() else [])
    for f in fichiers:
        if f.is_file() and f.suffix in {".md", ".py", ".json", ".txt", ".sh", ".html"}:
            try:
                if motif.search(f.read_text(encoding="utf-8", errors="ignore")):
                    fuites.append(str(f.relative_to(PROJ)))
            except Exception:
                pass
check("B6 sécurité", "F29", "0 octet de jeton dans tout artefact (scan PAT générique)",
      len(fuites) == 0, "%d fichier(s) : %s" % (len(fuites), ", ".join(fuites[:5])))

# B7 — Pendances + différés (D010) + anti-invention
check("B7 pendances", "F30", "D010 pendances reconduites au plan (RÉVOCATION PATs, PUSH git final, cron 531684, différés partage, GIF)",
      all(k in plan for k in ("RÉVOCATION", "cron 531684", "GIF")), "5 pendances au plan")
urls = re.findall(r"https?://(?:chat|www)?\.?z\.ai/\S*", plan + wl_hote[-3000:])
check("B7 anti-invention", "F31", "aucune URL z.ai fabriquée dans les artefacts Task 12",
      len(urls) == 0, "%d URL trouvée(s)" % len(urls))

# B8 — Miroir dépôt (commits Task 12) + langue
r = run(["git", "-C", str(REPO), "log", "--oneline", "-10"])
n_commits_t12 = len(re.findall(r"Task 12", r.stdout))
check("B8 miroir", "F32", "commits Task 12 en tête du dépôt local (G2+G3+G4+correctifs)",
      n_commits_t12 >= 6, "%d commits Task 12" % n_commits_t12)
check("B8 langue", "F33", "français exclusif — 0 caractère CJK dans plan + rapport CW",
      not re.search(r"[\u4e00-\u9fff]", plan), "plan sans dérive")

verdict = "PASS" if all(c["verdict"] == "PASS" for c in checks) else "FAIL"
rapport = {"tache": 12, "mode": "correct-work (projet) --bloc", "verdict": verdict,
           "total": "%d/%d PASS" % (sum(c["verdict"] == "PASS" for c in checks), len(checks)),
           "amendement_e13": "précision propriétaire trace 1a21e38435b96641 — audit déduplication rôles/objectifs (D011, F1-F5)",
           "checks": checks}
OUT.write_text(json.dumps(rapport, ensure_ascii=False, indent=2), encoding="utf-8")
print("VERDICT CW PROJET --bloc Task 12 : %s — %s" % (rapport["total"], verdict))
for c in checks:
    print("  [%s] %s %s" % (c["verdict"], c["id"], c["critere"]))
raise SystemExit(0 if verdict == "PASS" else 1)
