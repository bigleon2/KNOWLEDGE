#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check-tool-routing.py — Arbitre de routage des outils dédiés (6e arbitre, Task 22, D006).

Directive propriétaire 2026-10-03 : « vérifie aussi que tu as bien utilisé mes skills
et mes agents dédiés à l'écriture de chaque type d'élément (ex : mon skill
"skill-creator" pour écrire et modifier mes skills) et si ce n'est pas le cas fais en
sorte que mon écosystème le fasse automatiquement à partir de maintenant. »

Mécanisme (harness engineering — harnais resserré sur la dérive constatée, SHARED §7) :
  N1 — preuves mécaniques par artefact modifié (invariants dynamiques KO-L003) :
       skill        -> frontmatter conforme skill-creator §2 (name/version/category/
                       language/tags/description, semver)
       agent/PM     -> traçabilité de version (en-tête « Version » ou §7 historique)
       script       -> compilable (N3) + docstring d'en-tête (conventions script-creator)
       registre KB  -> entrées « ## nom vX.Y.Z » parsables (format skills-inventory §2.1)
  N2 — routage normatif par TYPE au niveau session : le plan ou le worklog de session
       doit citer le skill dédié de chaque type d'élément touché (traçabilité d'usage).
       Table de routage (source de vérité SHARED §3.1 / §7) :
         skill -> skill-creator ; agent/PM -> agent-creator ; script -> script-creator ;
         registre KB -> skills-inventory ; infrastructure -> script-mon-ecosysteme-infrastructure ;
         vérification -> correct-work ; planification -> gen-plan ; leçons -> knowledge-observer ;
         descriptions -> prompt-engineering.

Usage :
    python3 scripts/check-tool-routing.py                 # couche = git diff HEAD + non suivis
    python3 scripts/check-tool-routing.py --worklog P     # worklog de session (défaut auto-détecté)
    python3 scripts/check-tool-routing.py --plan P        # plan de session citant le routage
Sortie : scripts/tool-routing-report.json — exit 0 ssi verdict PASS.
Idempotent (R1-R6) : lecture seule, déterministe, aucun effet de bord.
"""
import hashlib, json, os, py_compile, re, subprocess, sys, tempfile
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
SKILLS = BASE / "skills"
OUT_JSON = BASE / "scripts" / "tool-routing-report.json"

# --- Table de routage (source de vérité) ---
ROUTING = {
    "skill": "skill-creator",
    "agent/PM": "agent-creator",
    "script": "script-creator",
    "infrastructure": "script-mon-ecosysteme-infrastructure",
    "registre KB": "skills-inventory",
}

def sh(cmd):
    p = subprocess.run(cmd, cwd=BASE, shell=True, capture_output=True, text=True, timeout=120)
    return p.stdout + p.stderr

CERT_ARTIFACTS = re.compile(r"^scripts/([^/]+-report\.json|ecosysteme-integrity\.json)$")


def layer_files():
    """Couche courante (D001) : fichiers CONTENU-modifiés vs HEAD (hors .next, hors
    drift de mode 100644->100755 S4) + non suivis. Invariant dynamique KO-L003.

    Exclusion B2 (Task 22, preuve d'idempotence par élément) : les rapports JSON
    que les arbitres réécrivent PENDANT la certification (*-report.json,
    ecosysteme-integrity.json) sont des SORTIES de la preuve, pas des entrées de
    la couche — sans exclusion, l'entrée de f dépend de sa propre sortie et
    f(f(x)) != f(x) (défaut constaté M1 != M2, corrigé à la source)."""
    out = sh("git diff --numstat HEAD -- ':(exclude).next'")
    files = {l.split("\t")[2].strip() for l in out.splitlines()
             if len(l.split("\t")) >= 3
             and l.split("\t")[0] not in ("0", "-")
             and l.split("\t")[1] not in ("-",)}
    files |= {l.strip() for l in sh("git ls-files --others --exclude-standard").splitlines() if l.strip()}
    return sorted(f for f in files if not CERT_ARTIFACTS.match(f))

def classify(rel):
    if rel == "skills/KNOWLEDGE.md":
        return "registre KB"
    if rel.startswith("skills/@mon-ecosysteme/"):
        return "agent/PM"
    m = re.match(r"skills/([^/]+)/SKILL\.md$", rel)
    if m:
        return "skill"
    if re.match(r"scripts/[^/]+\.py$", rel):
        name = Path(rel).stem
        if name in ("gen-ultra-maitre",) or "infrastructure" in name or name.startswith(("task14-", "task21-")):
            return "infrastructure"
        return "script"
    return None  # rapports download/, images, JSON de rapport : hors routage N1

def check_skill(path):
    txt = Path(path).read_text(encoding="utf-8")
    fm = re.match(r"^---\n(.*?)\n---", txt, re.S)
    if not fm:
        return False, "frontmatter absent"
    need = ["name:", "version:", "category:", "language:", "tags:", "description:"]
    missing = [f for f in need if f not in fm.group(1)]
    if missing:
        return False, f"frontmatter incomplet : {missing}"
    if not re.search(r"^version:\s*\"?[0-9]+\.[0-9]+\.[0-9]+", fm.group(1), re.M):
        return False, "version non semver"
    return True, "frontmatter skill-creator §2 conforme"

def check_agent(path):
    txt = Path(path).read_text(encoding="utf-8")
    # Traçabilité de version : « Version : », « **Version du prompt** : », ou §7 historique
    if re.search(r"^\s*>?\s*\**Version[^:\n]*:", txt, re.M) or "§7 — Historique" in txt:
        return True, "traçabilité de version présente"
    return False, "ni Version ni §7 historique"

def check_script(path):
    try:
        py_compile.compile(str(path), cfile=tempfile.mkstemp(suffix=".pyc")[1], doraise=True)
    except Exception as e:
        return False, f"non compilable : {e}"
    head = Path(path).read_text(encoding="utf-8", errors="replace")[:600]
    if '"""' in head or "'''" in head:
        return True, "compilable + docstring (N3)"
    return False, "docstring d'en-tête absente"

def check_kb(path):
    txt = Path(path).read_text(encoding="utf-8")
    n = len(re.findall(r"^##\s+\S+\s+v[0-9]+\.[0-9]+\.[0-9]+\s*$", txt, re.M))
    return (n >= 26, f"{n} entrées versionnées parsables (>=26 attendues)")

CHECKS = {"skill": check_skill, "agent/PM": check_agent, "script": check_script,
          "infrastructure": check_script, "registre KB": check_kb}

def main():
    wl_arg = next((sys.argv[i + 1] for i, a in enumerate(sys.argv) if a == "--worklog"), None)
    plan_arg = next((sys.argv[i + 1] for i, a in enumerate(sys.argv) if a == "--plan"), None)
    layer = layer_files()
    typed = {}
    for rel in layer:
        t = classify(rel)
        if t:
            typed.setdefault(t, []).append(rel)

    # N1 — preuves mécaniques
    n1, n1_fails = {}, []
    for t, files in sorted(typed.items()):
        paths = [(BASE / f) for f in files if (BASE / f).exists()]
        if not paths:
            continue
        verdicts = [CHECKS[t](p) for p in paths]
        ok = all(v[0] for v in verdicts)
        n1[t] = {"n": len(paths), "ok": ok,
                 "detail": (verdicts[0][1] if ok else next(d for s, d in verdicts if not s))}
        if not ok:
            n1_fails.append((t, [str(f) for f, (s, _) in zip(paths, verdicts) if not s]))
    # registre KB : uniquement si le fichier est dans la couche
    if "registre KB" not in typed and (BASE / "skills/KNOWLEDGE.md").exists():
        ok, d = check_kb(BASE / "skills/KNOWLEDGE.md")
        n1["registre KB (état)"] = {"n": 1, "ok": ok, "detail": d}

    # N2 — routage normatif cité au plan/worklog de session
    trace_sources = []
    for p in [plan_arg, wl_arg]:
        if p and Path(p).exists():
            trace_sources.append(Path(p).read_text(encoding="utf-8"))
    if not trace_sources:
        for pat in ["/home/z/my-project/download/plan-task*.md", "/home/z/my-project/worklog.md"]:
            hits = sorted(Path("/").glob(pat.lstrip("/")))
            trace_sources.extend(h.read_text(encoding="utf-8") for h in hits[-3:])
    trace = "\n".join(trace_sources)
    n2 = {}
    for t, skill in ROUTING.items():
        if t not in typed and t == "registre KB":
            continue  # KB non touchée par la couche : routage non requis
        hit = (skill in trace) and (
            t == "skill" and "skill-creator" in trace or
            t == "agent/PM" and "agent-creator" in trace or
            t == "script" and "script-creator" in trace or
            t == "infrastructure" and "infrastructure" in trace or
            t == "registre KB" and "skills-inventory" in trace)
        n2[t] = {"dedie": skill, "trace": bool(hit)}
    n2_fails = [t for t, v in n2.items() if not v["trace"]]

    verdict = "PASS" if not n1_fails and not n2_fails else "FAIL"
    # Provenance B2 (Task 22) : le rapport enregistre SON contexte d'invocation —
    # un rapport N1-seul n'est pas comparable à un rapport N1+N2(plan) sans ce champ.
    mode = ("N1+N2 (plan explicite)" if plan_arg else "N1+N2 (fallback glob)")
    date_commit = sh("git log -1 --format=%cd --date=short").strip() or "2026-10-03"
    rep = {"date": date_commit, "mode": mode,
           "plan": plan_arg or None,
           "task": "Task 22 — arbitre de routage (D006)",
           "couche": {"n_fichiers": len(layer), "par_type": {t: len(f) for t, f in typed.items()}},
           "N1_mecanique": n1, "N1_fails": [(t, f) for t, f in n1_fails],
           "N2_normatif": n2, "N2_manquants": n2_fails, "verdict": verdict}
    OUT_JSON.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"=== Arbitre check-tool-routing (Task 22, D006) ===")
    print(f"  Couche : {len(layer)} fichiers — {rep['couche']['par_type']}")
    for t, v in n1.items():
        print(f"  [N1 {'PASS' if v['ok'] else 'FAIL'}] {t:18} ({v['n']}) {v['detail'][:80]}")
    for t, v in n2.items():
        print(f"  [N2 {'PASS' if v['trace'] else 'FAIL'}] {t:18} -> {v['dedie']}")
    if n2_fails:
        print(f"  N2 manquants : {n2_fails} — citer les skills dédiés au plan/worklog de session")
    print(f"VERDICT : {verdict}")
    sys.exit(0 if verdict == "PASS" else 1)

if __name__ == "__main__":
    main()
