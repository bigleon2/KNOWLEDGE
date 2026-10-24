#!/usr/bin/env python3
# PROVENANCE: Task 22 — correct-work (aveugle), protocole Second Opinion.
# Cadrage à froid : les critères C01-C17 sont PRÉ-ÉCRITS (issus de l'answer key
# D001-D008 reformulée en checks mécaniques) ; les vérifications s'exécutent sur
# les ARTEFACTS seuls (aucun recours aux journaux d'exécution de la couche).
# Verdict par critère : PASS / FAIL ; convergence jugée au rapport.
"""⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.9)"""
import hashlib
import json
import re
import subprocess
import zipfile
from pathlib import Path

REPO = Path("/home/z/my-project/KNOWLEDGE-repo")
SK = REPO / "skills"
SKH = Path("/home/z/my-project/skills")
R = []

def check(cid, label, ok, detail=""):
    R.append((cid, label, bool(ok), detail))

def front(p):
    m = re.match(r"^---\n(.*?)\n---\n", p.read_text(encoding="utf-8"), re.S)
    return m.group(1) if m else None

def version_of(fm):
    return re.search(r"^version:\s*[\"']?(\d+\.\d+\.\d+)", fm, re.M).group(1)

MODIFIED = ["spec-driven-development", "cahier-des-charges", "prompt-engineering",
            "context-engineering", "memory-engineering", "fleet-engineering",
            "loop-engineering", "harness-engineering", "graph-engineering",
            "refactor-guard", "refactoring-test", "resource-monitor",
            "autonomous-agent", "inter-scripts", "agent-prompt-engineering",
            "agent-creator"]
EXPECTED = {"spec-driven-development": "1.1.0", "cahier-des-charges": "1.1.0",
            "prompt-engineering": "2.3.0", "context-engineering": "1.2.0",
            "memory-engineering": "1.2.0", "fleet-engineering": "1.1.0",
            "loop-engineering": "1.2.0", "harness-engineering": "1.2.0",
            "graph-engineering": "1.1.0", "refactor-guard": "1.8.0",
            "refactoring-test": "1.1.0", "resource-monitor": "1.1.0",
            "autonomous-agent": "1.2.0", "inter-scripts": "1.1.0",
            "agent-prompt-engineering": "1.1.0", "agent-creator": "2.2.0"}
HOTE_SEUL = {"cahier-des-charges", "inter-scripts", "agent-prompt-engineering"}

# C01 — les 16 éléments portent la version attendue (forme installée fait foi)
v_ok = all(version_of(front(SKH / s / "SKILL.md")) == v for s, v in EXPECTED.items())
check("C01", "versions des 16 éléments = attendues (hôte)", v_ok,
      "; ".join(f"{s}={version_of(front(SKH/s/'SKILL.md'))}" for s in EXPECTED))

# C02 — chaque élément modifié porte la sous-section §1.9bis (sauf agent-creator : §1.2 F1-F5)
bis_ok = all("Apports de veille 2025-2026" in (SKH / s / "SKILL.md").read_text(encoding="utf-8")
             for s in MODIFIED if s != "agent-creator") \
         and "Workflow de fabrique (5 étapes F1-F5)" in (SKH / "agent-creator" / "SKILL.md").read_text(encoding="utf-8")
check("C02", "§1.9bis présent ×15 + fabrique F1-F5 agent-creator", bis_ok)

# C03 — parse YAML des 16 frontmatters
import yaml
y_ok, y_bad = 0, []
for s in MODIFIED:
    try:
        d = yaml.safe_load(front(SKH / s / "SKILL.md"))
        assert d.get("name") == s
        y_ok += 1
    except Exception as e:
        y_bad.append(f"{s}:{e}")
check("C03", "frontmatters YAML parseables ×16", y_ok == 16, "; ".join(y_bad))

# C04 — read_when présent ×16 (agent-prompt-engineering rétabli)
rw_ok = all(re.search(r"^read_when:", front(SKH / s / "SKILL.md"), re.M) for s in MODIFIED)
check("C04", "read_when présent ×16", rw_ok)

# C05 — KB : en-têtes des 13 skills du dépôt à la version attendue
kb = (SK / "KNOWLEDGE.md").read_text(encoding="utf-8")
kb_ok = all(re.search(r"^## %s v%s\s*$" % (re.escape(s), re.escape(v)), kb, re.M)
            for s, v in EXPECTED.items() if s not in HOTE_SEUL)
check("C05", "KB en-têtes alignés (13 entrées dépôt)", kb_ok)

# C06 — ECO_SKILLS arbitre aligné (13 entrées dépôt)
arb = (REPO / "scripts" / "check-ecosysteme-integrity.py").read_text(encoding="utf-8")
eco_ok = all(f'"{s}": "{v}"' in arb for s, v in EXPECTED.items() if s not in HOTE_SEUL)
check("C06", "ECO_SKILLS aligné (13 entrées)", eco_ok)

# C07 — PM REFACTOR-GUARD v1.8.0 au corpus, v1.7.1 archivé, UNIQUEMENT là
pm_new = (SK / "@mon-ecosysteme" / "PROMPT-MAITRE-REFACTOR-GUARD-v1.8.0.md")
pm_old = (SK / "@historique" / "prompts-maitres" / "refactor-guard" / "PROMPT-MAITRE-REFACTOR-GUARD-v1.7.1.md")
check("C07", "PM v1.8.0 au corpus + v1.7.1 archivé, 0 homonyme corpus", pm_new.is_file() and pm_old.is_file()
      and not list((SK / "@mon-ecosysteme").glob("PROMPT-MAITRE-REFACTOR-GUARD-v1.7.1.md")))

# C08 — PM v1.8.0 : section veille présente + en-tête version
t = pm_new.read_text(encoding="utf-8")
check("C08", "PM v1.8.0 porte l'apport veille + en-tête cohérent",
      "1.9bis" in t and "Version du prompt" in t)

# C09 — archive round-trip : 9 entrées corpus byte-identiques au corpus
arch = REPO / "download" / "mon-ecosysteme_archive.zip"
n_ok = 0
with zipfile.ZipFile(arch) as z:
    names = [n for n in z.namelist() if not n.endswith("/")]
    for n in names:
        rel = n.split("@mon-ecosysteme/")[-1]
        cp = SK / "@mon-ecosysteme" / rel
        if cp.is_file() and hashlib.sha256(z.read(n)).hexdigest() == hashlib.sha256(cp.read_bytes()).hexdigest():
            n_ok += 1
check("C09", "archive 9/9 entrées byte-identiques au corpus", n_ok == 9, f"{n_ok}/9")

# C10 — pipeline : F1 (rc propagé), F2 (exclusion pycache), F3 (post_install) au code
ep = (REPO / "scripts" / "eco_install_pipeline.py").read_text(encoding="utf-8")
check("C10", "pipeline F1+F2+F3 codés", "returncode != 0" in ep and "ignore_patterns" in ep
      and "post_install" in ep and "sha256_verifies" in ep)

# C11 — post-install réelle : exécuter le pipeline et exiger rc0 + 0 divergence
r = subprocess.run(["python3", str(REPO / "scripts" / "eco_install_pipeline.py")],
                   capture_output=True, text=True, cwd=REPO)
d = json.loads(r.stdout) if r.returncode == 0 else {}
check("C11", "pipeline rc0 + post_install 0 divergence", r.returncode == 0
      and d.get("post_install", {}).get("divergences") == [],
      f"rc={r.returncode} sha={d.get('post_install', {}).get('sha256_verifies')}")

# C12 — SHARED v1.7.9 : marqueur propagé (échantillon : 3 skills + 1 script + 1 agent)
def marker(p):
    return "SHARED v1.7.9" in p.read_text(encoding="utf-8", errors="replace")
mk = all(marker(SKH / s / "SKILL.md") for s in ["gen-plan", "correct-work", "alias-eco"]) \
     and marker(REPO / "scripts" / "propagate-context.py") \
     and marker(SKH / "agent-creator" / "references" / "agent-creator.agent")
check("C12", "marqueur §0 v1.7.9 propagé (échantillon 5)", mk)

# C13 — voie L : bilan sans QUOTA, agent-creator CONFIRME, 0 null
vl = json.loads((REPO / "scripts" / "task17-voie-l-report.json").read_text(encoding="utf-8"))
ac = [c for c in vl["skills"]["agent-creator"]["cases"]]
check("C13", "voie L : agent-creator CONFIRME 3 votes réels + bilan sans QUOTA",
      all(c["decision"] == "CONFIRME" and all(v is not None for v in c["votes"]) for c in ac)
      and "QUOTA" not in vl.get("bilan", {}), json.dumps(vl.get("bilan", {})))

# C14 — journal KB : entrée Task 22 UNIQUE
n22 = kb.count("Task 22 — directive gen-plan(step) : re-mesure QUOTA agent-creator")
check("C14", "entrée journal KB Task 22 unique", n22 == 1, f"{n22} occurrence(s)")

# C15 — guide gen-plan complété (fence fermée, arbre a-b-c-d)
g = (SK / "gen-plan" / "references" / "guide-selection-agent-skill.md").read_text(encoding="utf-8")
check("C15", "guide-selection-agent-skill complété (fence + routage)",
      g.count("```") % 2 == 0 and "(a) SÉQUENTIELLE" in g and len(g) > 1200)

# C16 — agent-creator .agent : objectif fabrique + champ capacites + version 2.2.0
ag = (SK / "agent-creator" / "references" / "agent-creator.agent").read_text(encoding="utf-8")
check("C16", ".agent fabrique (objectif, capacites, v2.2.0)",
      "Fabrique d'agents persistants" in ag and "capacites:" in ag and '"2.2.0"' in ag)

# C17 — @historique : index 26 PMs + ligne SHA v1.7.1 scellée
rhi = (SK / "@historique" / "README.md").read_text(encoding="utf-8")
check("C17", "index @historique 26 PMs + SHA v1.7.1",
      "26 PMs" in rhi and "PROMPT-MAITRE-REFACTOR-GUARD-v1.7.1.md | 8fceb8c1" in rhi)

# ── Verdict ──────────────────────────────────────────────────────────────
n_pass = sum(1 for _, _, ok, _ in R if ok)
print(f"{'ID':5} {'VERDICT':6} CRITÈRE — DÉTAIL")
for cid, label, ok, det in R:
    print(f"{cid:5} {'PASS' if ok else 'FAIL':6} {label}" + (f" — {det}" if det else ""))
print(f"\nSECONDE OPINION : {n_pass}/{len(R)} PASS")
print("CONVERGENCE attendue avec le rapport correct-work (projet) Task 22.")
