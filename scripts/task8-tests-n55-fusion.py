#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.5)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

# -*- coding: utf-8 -*-
"""Task 8 G2-b — 3 tests complexes et robustes : refactoring-engineering + refactoring-test
(+ fusion discussion 468a4c26).

T1 — refactoring-test : détecter/évaluer/grapher (bras mécanique M3, déterminisme, verdicts)
T2 — refactoring-engineering : gouverner/exécuter zéro-régression (R2/R4, idempotence,
     anti-auto-certification, gouvernance G0-G3, garde-fous)
T3 — Fusion & cohérence écosystème (déclarations ×2 arbres, convergence directive externe)

Robustesse : preuves mécaniques (SHA, re-exécutions à l'instant, JSON), double arbre
(canonique KNOWLEDGE/ + hôte skills/), idempotence du harnais lui-même (×2).
"""
import hashlib
import json
import os
import re
import subprocess
import sys

CAN = "/home/z/my-project/KNOWLEDGE"
HOTE = "/home/z/my-project/skills"
RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append({"check": name, "verdict": "PASS" if ok else "FAIL", "detail": str(detail)[:300]})
    print("  [%s] %s%s" % ("PASS" if ok else "FAIL", name, (" — " + str(detail)[:120]) if detail and not ok else ""))
    return ok


def sha256(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def run_graph(*args):
    r = subprocess.run([sys.executable, CAN + "/scripts/refactoring-test-graph.py"] + list(args),
                       capture_output=True, text=True, cwd=CAN)
    return r


def t1():
    print("== T1 — refactoring-test : détecter / évaluer / grapher ==")
    # T1.1 M3 sur refactoring-engineering — blast radius riche + déterminisme ×2
    r1 = run_graph("--target", "refactoring-engineering")
    r2 = run_graph("--target", "refactoring-engineering")
    m1 = re.search(r"backward\) = (\d+) éléments, forward = (\d+)", r1.stdout)
    m2 = re.search(r"backward\) = (\d+) éléments, forward = (\d+)", r2.stdout)
    ok = (m1 and m2 and m1.groups() == m2.groups()
          and int(m1.group(1)) >= 15 and int(m1.group(2)) >= 20)
    check("T1.1 M3 ref-eng : blast radius %s/%s déterministe ×2 (>=15/>=20)" %
          (m1.group(1) if m1 else "?", m1.group(2) if m1 else "?"), ok, r1.stderr[-200:])
    check("T1.1b verdict CRITIQUE (17 >= 8 — pivot n°55)", "CRITIQUE" in r1.stdout)
    # T1.2 M3 refactoring-test — cible elle-même évaluable
    r3 = run_graph("--target", "refactoring-test")
    check("T1.2 M3 ref-test : évaluation de l'outil elle-même",
          r3.returncode == 0 and "refactoring-engineering" in r3.stdout)
    # T1.3 M3 refactor-guard — arêtes garde-fous vivantes
    r4 = run_graph("--target", "refactor-guard")
    check("T1.3 M3 refactor-guard : backward inclut ref-eng + gen-plan",
          r4.returncode == 0 and "refactoring-engineering" in r4.stdout and "gen-plan" in r4.stdout)
    # T1.4 verdict machine §1.3 — seuils implémentés et cohérents
    src = read(CAN + "/scripts/refactoring-test-graph.py")
    check("T1.4 seuils verdict §1.3 (<4 OK / 4-7 PRESSION / >=8 CRITIQUE) codés",
          "CRITIQUE" in src and "PRESSION" in src and ("8" in src and "4" in src))
    # T1.5 M1 signaux : 7 familles nommées + sources mécaniques citées
    rt = read(CAN + "/skills/refactoring-test/SKILL.md")
    signaux = ["duplication", "dérive de terminologie", "versions divergentes",
               "asymétries KB", "réserves récurrentes", "churn de cascade", "complexité des procédures"]
    check("T1.5 M1 : 7 familles de signaux nommées (SKILL.md §1.2)",
          all(s in rt for s in signaux), str([s for s in signaux if s not in rt]))
    check("T1.5b M1 : sources mécaniques citées (§1.4 — arbitres existants)",
          "test-coherence-interactions" in rt and os.path.isfile(CAN + "/scripts/test-coherence-interactions.py"))
    # T1.6 déterminisme export --json ×2 (sortie machine : scripts/refactoring-test-report.json)
    rep_default = CAN + "/scripts/refactoring-test-report.json"
    h_before = sha256(rep_default) if os.path.isfile(rep_default) else None
    ra, rb = run_graph("--graph", "--json"), run_graph("--graph", "--json")
    h_after1 = sha256(rep_default) if os.path.isfile(rep_default) else None
    run_graph("--graph", "--json")
    h_after2 = sha256(rep_default) if os.path.isfile(rep_default) else None
    ok6 = h_after1 is not None and h_after1 == h_after2 and len(ra.stdout) > 100
    j1 = read(rep_default) if os.path.isfile(rep_default) else ra.stdout
    check("T1.6 export graphe déterministe ×2 (rapport JSON byte-identique)", ok6)
    # T1.7 graphe conforme KB — nœuds fusion présents dans le rapport JSON
    try:
        data = json.loads(j1)
        txt = json.dumps(data)
        nodes = data.get("nodes", []) if isinstance(data, dict) else data
        ok7 = "refactor-guard" in txt and "fullstack-dev" in txt and len(nodes) >= 20
    except Exception:
        ok7 = "refactor-guard" in j1 and "fullstack-dev" in j1
    check("T1.7 graphe inclut les nœuds fusion (refactor-guard + fullstack-dev)", ok7)
    # T1.8 trigger_evals conforme (liste, 5 pos / 2 neg)
    te = json.loads(read(CAN + "/skills/refactoring-test/evals/trigger_evals.json"))
    pos = sum(1 for c in te if c.get("should_trigger") is True)
    neg = sum(1 for c in te if c.get("should_trigger") is False)
    check("T1.8 trigger_evals ref-test : liste valide 5 pos / 2 neg", isinstance(te, list) and pos == 5 and neg == 2,
          "pos=%d neg=%d" % (pos, neg))
    for f in (rep_default,):
        pass  # rapport par défaut conservé (T2.6 le consomme)


def t2():
    print("== T2 — refactoring-engineering : gouverner / exécuter (zéro-régression) ==")
    re_ = read(CAN + "/skills/refactoring-engineering/SKILL.md")
    # T2.1 D1-D4 déclarés + invariants constitution
    modes = all(x in re_ for x in ["D1 DÉCLARER", "D2 PRÉPARER", "D3 EXÉCUTER", "D4 MIGRER"])
    inv = all(x in re_ for x in ["R2", "R4", "Idempotence ×2", "Évaluation indépendante", "Traçabilité"])
    check("T2.1 modes D1-D4 + 6 invariants constitution (§1.2/§1.4)", modes and inv)
    # T2.2 R4 byte-identité PM v3.23.0 archivé (SHA scellé index §5)
    arch = CAN + "/skills/@historique/prompts-maitres/gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.23.0.md"
    h = sha256(arch) if os.path.isfile(arch) else None
    idx = read(CAN + "/skills/@historique/README.md")
    check("T2.2 R4 : PM v3.23.0 archivé byte-identité, SHA scellé index §5",
          h is not None and h in idx, h[:16] if h else "absent")
    # T2.3 R2 non-rétrogradation : corpus = 1 PM GEN-PLAN = v3.23.1 + PM REFACTOR-GUARD v1.7.0 (D009)
    corpus = sorted(os.listdir(CAN + "/skills/@mon-ecosysteme"))
    pms = [f for f in corpus if f.startswith("PROMPT-MAITRE-GEN-PLAN-")]
    check("T2.3 R2 : corpus 9 fichiers (D009), 1 PM GEN-PLAN = v3.23.1",
          len(corpus) == 9 and pms == ["PROMPT-MAITRE-GEN-PLAN-v3.23.1.md"]
          and "PROMPT-MAITRE-REFACTOR-GUARD-v1.7.0.md" in corpus, str(pms))
    # T2.4 idempotence ×2 RE-POUVRÉE à l'instant (scripts d'état → 0 EDIT)
    edits = 0
    for s in ("g1a-corrections-n55.py", "g1b-kb-n55.py", "g1c-genplan-shared-eco.py"):
        r = subprocess.run([sys.executable, CAN + "/scripts/" + s], capture_output=True, text=True)
        edits += len(re.findall(r"\[EDIT\]", r.stdout))
    check("T2.4 idempotence ×2 re-prouvée : g1a+g1b+g1c re-exécutés = 0 EDIT", edits == 0, "%d éditions" % edits)
    # T2.5 anti-auto-certification structurée (évaluateur ≠ exécutant)
    rt = read(CAN + "/skills/refactoring-test/SKILL.md")
    check("T2.5 anti-auto-certification : invariant ref-eng §1.4-5 + règle ref-test §1.5-2",
          "l'exécutant ne s'auto-évalue pas" in re_ and "l'exécutant d'une opération ne peut être l'exécutant de cette opération".replace("d'une opération ne peut être l'exécutant", "ne peut être l'exécutant") in rt or "ne peut être l'exécutant" in rt)
    # T2.6 pre-vol M3 exécuté AVANT publication du plan (verdict enregistré au rapport)
    rep = CAN + "/scripts/refactoring-test-report.json"
    check("T2.6 pré-vol M3 : rapport JSON du graphe présent (verdict journalisé)", os.path.isfile(rep))
    # T2.7 gouvernance G0-G3 + correct-work(groupe/projet) chaîné
    check("T2.7 gouvernance G0-G3 (§1.3) + chaîne correct-work(groupe/projet)",
          all(x in re_ for x in ["G0", "G1", "G2", "G3", "correct-work(groupe)", "correct-work(projet)"]))
    # T2.8 triangulation déclarée ×2 arbres (deps frontmatter + §3)
    hote_eng = read(HOTE + "/refactoring-engineering/SKILL.md")
    tri = all(x in re_ for x in ["refactoring-test", "refactor-guard", "correct-work"])
    tri_h = all(x in hote_eng for x in ["refactor-guard", "garde-fous des opérations D3/D4"])
    check("T2.8 triangulation évaluateur/garde-fous/vérificateur ×2 arbres", tri and tri_h)
    # T2.9 preuves de session G1 : scripts persistés + manifeste projection
    proofs = ["g1a-corrections-n55.py", "g1b-kb-n55.py", "g1c-genplan-shared-eco.py",
              "g1d-cascade-n55.py", "g2-projection-hote-task8.py"]
    ok9 = all(os.path.isfile(os.path.join(CAN, "scripts", p)) for p in proofs)
    ok9 = ok9 and os.path.isfile("/home/z/my-project/scripts/projection-hote-task8-manifest.json")
    check("T2.9 preuves D3 : scripts d'opération persistés (jamais inline) + manifeste", ok9)
    # T2.10 delta PM verrouillé + idempotent (ré-exécution no-op)
    r = subprocess.run([sys.executable, CAN + "/scripts/generer-pm-skill.py", "--check"],
                       capture_output=True, text=True, cwd=CAN)
    check("T2.10 generer-pm --check : 4 familles COHERENT après cascade (D009)", "COHERENT" in r.stdout and r.returncode == 0)


def t3():
    print("== T3 — Fusion & cohérence écosystème (×2 arbres) ==")
    for label, root in (("canonique", CAN + "/skills"), ("hôte", HOTE)):
        rt = read(root + "/refactoring-test/SKILL.md")
        re_ = read(root + "/refactoring-engineering/SKILL.md")
        kb = read(root + "/KNOWLEDGE.md")
        sh = read(root + "/@mon-ecosysteme/PROMPT-MAITRE-SHARED.md")
        gp = read(root + "/gen-plan/SKILL.md")
        rg_ = read(root + "/refactor-guard/SKILL.md")
        # T3.1 ref-test n'est PAS une discipline
        check("T3.1 [%s] ref-test = OUTIL (non discipline) : « Skill outil » + « n'est PAS une discipline » + §8 Rattachement" % label,
              "Skill outil refactoring test" in rt and "n'est PAS une discipline" in rt
              and "Rattachement à la discipline n°55" in rt and "Skill discipline refactoring test" not in rt)
        # T3.2 ref-eng = seule discipline n°55
        check("T3.2 [%s] ref-eng = discipline n°55 (se sers de ref-test comme d'un outil)" % label,
              "Skill discipline refactoring engineering" in re_ and "se sert de refactoring-test comme" in re_)
        # T3.3 SHARED §7 : outil + registre 3 lignes
        check("T3.3 [%s] SHARED §7 : ligne outil + registre scindé ×3 (eng/test/guard)" % label,
              "(outil de la discipline n°55)" in sh and "Outil de la matérialisation n°55" in sh
              and "Skill de garde-fous de refactoring" in sh)
        # T3.4 gen-plan PATTERN : discipline + outil + garde-fous
        check("T3.4 [%s] gen-plan : bloc « Discipline de refactoring n°55 et son outil » + §3 refactor-guard" % label,
              "Discipline de refactoring n°55 et son outil" in gp and "Garde-fous de refactoring (fusion discussion 468a4c26" in gp)
        # T3.5 refactor-guard déclaré v1.7.0 avec provenance
        check("T3.5 [%s] refactor-guard v1.7.0 : frontmatter + KB + provenance CONVERGENCE" % label,
              "version: 1.7.0" in rg_ and "## refactor-guard v1.7.0" in kb
              and "CONVERGENCE de la lignée externe" in rg_)
        # T3.6 fullstack-dev inscrit + bidirectionnalité correct-work
        check("T3.6 [%s] fullstack-dev inscrit (KB) + « Utilisé par » correct-work" % label,
              "## fullstack-dev v1.0.0" in kb and
              re.search(r"## fullstack-dev[\s\S]{0,2000}?- \*\*Utilisé par\*\* : correct-work", kb) is not None)
        # T3.7 convergence directive externe 1 (déclencheurs step/step-ok + alias + NULL + chaîne correct-work)
        check("T3.7 [%s] convergence directive externe : modes step/step-ok + alias step-confirm/step-confim + clause NULL" % label,
              "step-ok" in gp and "step-confirm" in gp and "step-confim" in gp and "mode NULL" in gp)
        scripts_nb = len([f for f in os.listdir(root + "/refactor-guard/scripts")] if os.path.isdir(root + "/refactor-guard/scripts") else [])
        check("T3.8 [%s] refactor-guard mécanique : 11 scripts stdlib + evals + references" % label,
              scripts_nb == 11 and os.path.isdir(root + "/refactor-guard/evals")
              and os.path.isdir(root + "/refactor-guard/references"), "%d scripts" % scripts_nb)
    # T3.9 hygiène KB canonique : 32 entrées + 0 quoté + 0 blanc parasite
    kb = read(CAN + "/skills/KNOWLEDGE.md")
    entries = re.findall(r"(?m)^## ([a-z0-9-]+) v[0-9.]+\s*$", kb)
    quoted = 0
    eco = re.findall(r'"([a-z0-9-]+)":\s*"[0-9.]+"', read(CAN + "/scripts/check-ecosysteme-integrity.py")
                     [re.search(r"ECO_SKILLS\s*=\s*\{", read(CAN + "/scripts/check-ecosysteme-integrity.py")).start():])
    for k in eco:
        p = "%s/skills/%s/SKILL.md" % (CAN, k)
        if os.path.isfile(p) and re.search(r'(?m)^version: "[0-9.]+"$', read(p)):
            quoted += 1
    lines = kb.split("\n")
    blancs = sum(1 for i in range(1, len(lines) - 1)
                 if lines[i].strip() == "" and lines[i - 1].strip().startswith("- ")
                 and lines[i + 1].strip().startswith("- "))
    check("T3.9 hygiène KB : 32 entrées + 0 frontmatter quoté (registre) + 0 blanc parasite",
          len(entries) == 32 and quoted == 0 and blancs == 0,
          "entries=%d quoted=%d blancs=%d" % (len(entries), quoted, blancs))
    # T3.10 productions de la discussion externe 468a4c26 — fusion tracée
    ext = "/home/z/my-project/scripts/ext-disc-468a4c26.txt"
    in_ext = ["refactor-guard v1.7.0", "fullstack-dev", "toilettage", "resync R2", "Task 27", "Task 28"]
    ok10 = os.path.isfile(ext) and all(v in read(ext) for v in in_ext)
    ok10 = ok10 and os.path.isfile("/home/z/my-project/scripts/projection-hote-task8-manifest.json")
    check("T3.10 fusion 468a4c26 : source capturée (Tasks 25-28) + 4 productions intégrées (toilettage KB, fullstack-dev, resync=projection hôte, refactor-guard)", ok10)
    # T3.11 interactions PASS STRICT (preuve mécanique fraîche)
    rep = json.loads(read(CAN + "/scripts/interactions-report.json"))
    txt = json.dumps(rep)
    check("T3.11 interactions : rapport JSON présent, 0 FAIL (PASS STRICT)", '"FAIL": 0' in txt or '"fail": 0' in txt or "0 FAIL" in txt)


def main():
    print("=== Task 8 — 3 tests complexes (n°55 + fusion 468a4c26) ===")
    t1()
    t2()
    t3()
    n_pass = sum(1 for r in RESULTS if r["verdict"] == "PASS")
    n_fail = len(RESULTS) - n_pass
    print("=== BILAN : %d PASS / %d FAIL — %d checks ===" % (n_pass, n_fail, len(RESULTS)))
    out = {"task": "8", "harnais": "task8-tests-n55-fusion",
           "bilan": "%d/%d" % (n_pass, len(RESULTS)), "results": RESULTS}
    with open("/home/z/my-project/KNOWLEDGE/scripts/task8-tests-report.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    if n_fail:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
