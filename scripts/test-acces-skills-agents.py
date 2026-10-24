#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.13)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

# -*- coding: utf-8 -*-
"""
Task 6 (gen-plan) — T1 : test d'accès de l'écosystème local à ses skills et agents spécialisés.
Axes :
  A1. Chargeabilité des 32 ECO_SKILLS : SKILL.md présent, lisible, frontmatter name+version,
      version cohérente avec le registre KB (skills/KNOWLEDGE.md).
  A2. Routage D006 (routage normatif de session, worklog Task 1) : les 10 skills dédiées
      par type de tâche sont présentes et chargeables + arbitre check-tool-routing exécuté.
  A3. Agents spécialisés matérialisés (*.agent sous skills/*/references/) : lisibles,
      frontmatter présent, skill hôte présente ; usine à agents (agent-creator) disponible.
  A4. Sondes d'exécution réelle (rc==0 = preuve d'accès fonctionnelle) :
      garde É1-INSTALL --preempt, check-tool-routing, refactoring-test-graph --target,
      resource-monitor (monitor.py), skills-inventory (generate_skills_md.py inline).
Rapport : console (PASS/FAIL par axe) + JSON scripts/outputs/test-acces-<ts>.json
Convention : stdlib uniquement, lecture seule (aucune écriture hors rapport), idempotent.
"""
import json, re, subprocess, sys, time
from pathlib import Path

LOCAL = Path(__file__).resolve().parents[1]
SK = LOCAL / "skills"
KB = SK / "KNOWLEDGE.md"
OUT = LOCAL / "scripts" / "outputs"

ROUTAGE_D006 = [
    ("skill-creator", "création/modification de SKILL"),
    ("agent-creator", "création/modification d'agent/PM"),
    ("script-creator", "création/modification de script"),
    ("script-reviewer", "relecture de script"),
    ("script-mon-ecosysteme-infrastructure", "infrastructure de l'écosystème"),
    ("correct-work", "vérification"),
    ("gen-plan", "planification"),
    ("knowledge-observer", "leçons"),
    ("resource-monitor", "ressources"),
    ("skills-inventory", "inventaire"),
]

def sh(cmd):
    return subprocess.run([sys.executable] + cmd, capture_output=True, text=True, cwd=str(LOCAL))

def frontmatter(path: Path) -> dict:
    txt = path.read_text(encoding="utf-8", errors="replace")
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", txt, re.DOTALL)
    if not m:
        return {}
    fm = {}
    for line in m.group(1).splitlines():
        # Clés de TÊTE uniquement (colonne 0) — les clés indentées appartiennent aux
        # blocs imbriqués (ex. dependencies: version: ">=x") et ne doivent PAS
        # écraser la version propre du skill (leçon KO-L003 appliquée au testeur).
        kv = re.match(r"^(name|version|description):\s*(.*)$", line)
        if kv and kv.group(1) not in fm:
            fm[kv.group(1)] = kv.group(2).strip().strip('"').strip("'")
    return fm

def kb_entries() -> dict:
    txt = KB.read_text(encoding="utf-8", errors="replace")
    return {m.group(1): m.group(2)
            for m in re.finditer(r"^## ([a-z0-9-]+) v(\d+\.\d+\.\d+)$", txt, re.MULTILINE)}

def main():
    ts = time.strftime("%Y%m%d-%H%M%S")
    res = {"date": ts, "axes": []}

    # --- A1. Chargeabilité des 32 ECO_SKILLS ---
    kb = kb_entries()
    a1 = {"axe": "A1 chargeabilité ECO_SKILLS", "attendu": len(kb), "echecs": [], "pass": 0}
    for nom, ver in sorted(kb.items()):
        f = SK / nom / "SKILL.md"
        if not f.exists():
            a1["echecs"].append(f"{nom}: SKILL.md ABSENT")
            continue
        try:
            fm = frontmatter(f)
        except Exception as exc:
            a1["echecs"].append(f"{nom}: illisible ({exc})")
            continue
        if not fm.get("version"):
            a1["echecs"].append(f"{nom}: frontmatter sans version")
        elif fm["version"] != ver:
            a1["echecs"].append(f"{nom}: v{fm['version']} != KB v{ver}")
        else:
            a1["pass"] += 1
    a1["verdict"] = "PASS" if not a1["echecs"] else "FAIL"
    res["axes"].append(a1)

    # --- A2. Routage D006 ---
    a2 = {"axe": "A2 routage D006 (10 skills dédiées)", "echecs": [], "pass": 0}
    for nom, usage in ROUTAGE_D006:
        f = SK / nom / "SKILL.md"
        fm = frontmatter(f) if f.exists() else {}
        if fm.get("version"):
            a2["pass"] += 1
        else:
            a2["echecs"].append(f"{nom} ({usage}): inaccessible")
    r = sh(["scripts/check-tool-routing.py"])
    a2["arbitre_tool_routing"] = {"rc": r.returncode,
                                  "apercu": (r.stdout or r.stderr).strip().splitlines()[-1:] }
    if r.returncode != 0:
        a2["echecs"].append("arbitre check-tool-routing en échec")
    a2["verdict"] = "PASS" if not a2["echecs"] else "FAIL"
    res["axes"].append(a2)

    # --- A3. Agents spécialisés ---
    a3 = {"axe": "A3 agents matérialisés", "agents": [], "echecs": []}
    agents = sorted(SK.glob("*/references/*.agent"))
    for ag in agents:
        hote = ag.parents[1].name
        try:
            txt = ag.read_text(encoding="utf-8")
            ok_fm = bool(re.match(r"^---\s*\n", txt))
            a3["agents"].append({"fichier": str(ag.relative_to(LOCAL)),
                                 "hote": hote, "frontmatter": "oui" if ok_fm else "non",
                                 "octets": ag.stat().st_size})
        except Exception as exc:
            a3["echecs"].append(f"{ag.name}: illisible ({exc})")
    if not (SK / "agent-creator" / "SKILL.md").exists():
        a3["echecs"].append("usine à agents agent-creator ABSENTE")
    a3["verdict"] = "PASS" if not a3["echecs"] and a3["agents"] else "FAIL"
    res["axes"].append(a3)

    # --- A4. Sondes d'exécution réelle ---
    probes = [
        ("garde É1-INSTALL --preempt", ["skills/gen-plan/scripts/ensure-installed.py", "--preempt"]),
        ("arbitre check-tool-routing", ["scripts/check-tool-routing.py"]),
        ("évaluateur refactoring-test (gen-plan)", ["scripts/refactoring-test-graph.py", "--target", "gen-plan"]),
        ("resource-monitor (collecte)", ["skills/resource-monitor/scripts/monitor.py"]),
        ("skills-inventory (scan inline)", ["skills/skills-inventory/scripts/generate_skills_md.py"]),
    ]
    a4 = {"axe": "A4 sondes d'exécution réelle", "sondes": [], "echecs": []}
    for nom, cmd in probes:
        p = sh(cmd)
        entry = {"sonde": nom, "rc": p.returncode,
                 "apercu": (p.stdout or p.stderr).strip().splitlines()[-1][:120] if (p.stdout or p.stderr).strip() else ""}
        a4["sondes"].append(entry)
        if p.returncode != 0:
            a4["echecs"].append(f"{nom}: rc={p.returncode}")
    a4["verdict"] = "PASS" if not a4["echecs"] else "FAIL"
    res["axes"].append(a4)

    res["verdict_global"] = "PASS" if all(a["verdict"] == "PASS" for a in res["axes"]) else "FAIL"

    OUT.mkdir(parents=True, exist_ok=True)
    out_json = OUT / f"test-acces-{ts}.json"
    out_json.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"=== T1 ACCÈS SKILLS + AGENTS — {ts} ===")
    for a in res["axes"]:
        print(f"[{a['verdict']}] {a['axe']}")
        if a["axe"].startswith("A1"):
            print(f"    {a1['pass']}/{a1['attendu']} skills chargeables et cohérents KB")
            for e in a1["echecs"][:5]:
                print(f"    ⚠ {e}")
        if a["axe"].startswith("A2"):
            print(f"    {a2['pass']}/10 skills de routage accessibles ; arbitre rc={a2['arbitre_tool_routing']['rc']}")
            for e in a2["echecs"][:5]:
                print(f"    ⚠ {e}")
        if a["axe"].startswith("A3"):
            print(f"    {len(a3['agents'])} agent(s) matérialisé(s) : " + ", ".join(x['fichier'].split('/')[-1] for x in a3['agents']))
            for e in a3["echecs"][:5]:
                print(f"    ⚠ {e}")
        if a["axe"].startswith("A4"):
            for s in a4["sondes"]:
                print(f"    sonde '{s['sonde']}' : rc={s['rc']} — {s['apercu']}")
    print(f"=== VERDICT GLOBAL T1 : {res['verdict_global']} ===")
    print(f"Rapport JSON : {out_json.relative_to(LOCAL)}")
    sys.exit(0 if res["verdict_global"] == "PASS" else 1)

if __name__ == "__main__":
    main()
