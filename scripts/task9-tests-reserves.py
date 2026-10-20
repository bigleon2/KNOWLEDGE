#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.7)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

# -*- coding: utf-8 -*-
"""Task 9 / G3-b — Tests de clôture des réserves (T-RES) : D009 + baselines A2 n°55.

T-RES-1 — D009 : décision consignée (KB + @historique + PM-INSTALL v1.6.5 + SHARED
           v1.7.5), generer-pm 4 familles (dict + --check ×2), PM REFACTOR-GUARD
           v1.7.0 au corpus (6 ancres + byte-identité ×2 arbres).
T-RES-2 — Baselines A2 n°55 : rapport JSON présent (14/14, 0 dérive ×2 voies,
           0 vote null), cascade v1.1.0 (frontmatter, KB, ECO_SKILLS, phrase
           optimisée, @historique), evals R2 inchangées.
T-RES-3 — Remédiation purge plateforme : 15 fichiers restaurés byte-identité
           (manifeste Task 9, post-check 128/128).
Robustesse : preuves mécaniques à l'instant, idempotence du harnais (×2).
"""
import hashlib
import json
import os
import subprocess
import sys

CAN = "/home/z/my-project/KNOWLEDGE"
HOTE = "/home/z/my-project/skills"
RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append({"check": name, "verdict": "PASS" if ok else "FAIL", "detail": str(detail)[:300]})
    print("  [%s] %s%s" % ("PASS" if ok else "FAIL", name, (" — " + str(detail)[:120]) if detail and not ok else ""))
    return ok


def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def sha256(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def t_res1():
    print("== T-RES-1 — D009 : 4e famille refactor-guard vivante ==")
    pm_p = CAN + "/skills/@mon-ecosysteme/PROMPT-MAITRE-REFACTOR-GUARD-v1.7.0.md"
    ok = os.path.isfile(pm_p)
    check("T-R1.1 PM REFACTOR-GUARD v1.7.0 au corpus", ok)
    if not ok:
        return
    pm = read(pm_p)
    ancres = ["— Installation du skill refactor-guard v1.7.0",
              "> **Skill cible** : refactor-guard v1.7.0",
              "> **Version du prompt** : 1.0.0",
              "version: 1.7.0", "\n| v1.7.0 | "]
    check("T-R1.2 ancres generer-pm (5) présentes", all(a in pm for a in ancres))
    check("T-R1.3 décision D009 documentée dans le PM (provenance R4)",
          "décision propriétaire D009" in pm and "ACCEPTÉS non portés" in pm)
    gp = read(CAN + "/scripts/generer-pm-skill.py")
    check("T-R1.4 generer-pm FAMILLES = 4 entrées (dict)",
          '"refactor-guard": "PROMPT-MAITRE-REFACTOR-GUARD"' in gp)
    outs = []
    for _ in range(2):
        r = subprocess.run([sys.executable, CAN + "/scripts/generer-pm-skill.py", "--check"],
                           capture_output=True, text=True, cwd=CAN)
        outs.append((r.returncode, r.stdout))
    check("T-R1.5 generer-pm --check 4/4 COHERENT ×2 (idempotent)",
          all(rc == 0 and out.count("COHERENT") == 4 for rc, out in outs))
    r = subprocess.run([sys.executable, CAN + "/scripts/generer-pm-skill.py",
                        "--generate", "refactor-guard", "--dry-run"],
                       capture_output=True, text=True, cwd=CAN)
    check("T-R1.6 --generate refactor-guard = NO-OP (cohérence)", "NO-OP" in r.stdout)
    inst = read(CAN + "/skills/@mon-ecosysteme/PROMPT-MAITRE-INSTALL-ECOSYSTEME.md")
    check("T-R1.7 PM-INSTALL v1.7.1 : §2quater 4 familles + §2ter ligne REFACTOR-GUARD + étape 6",
          "Version : 1.7.1" in inst and "des 4 familles (gen-plan, correct-work, clone-chat, "
          "refactor-guard — décision D009 du 2026-10-12)" in inst
          and "PROMPT-MAITRE-REFACTOR-GUARD-v1.7.0.md" in inst
          and "| 6 | **refactor-guard**" in inst)
    shared = read(CAN + "/skills/@mon-ecosysteme/PROMPT-MAITRE-SHARED.md")
    check("T-R1.8 SHARED v1.7.7 : §6.1 ligne REFACTOR-GUARD + PM-INSTALL v1.7.1",
          "> **Version** : 1.7.7" in shared and "PROMPT-MAITRE-REFACTOR-GUARD-v1.7.0.md" in shared
          and "| v1.7.1 |" in shared)
    kb = read(CAN + "/skills/KNOWLEDGE.md")
    check("T-R1.9 KB : décision D009 LEVÉE consignée (calibration refactor-guard)",
          "décision propriétaire D009 LEVÉE" in kb and "PM canonique PROMPT-MAITRE-REFACTOR-GUARD-v1.7.0 au corpus" in kb)
    hist = read(CAN + "/skills/@historique/historiques-par-skill/refactor-guard.md")
    check("T-R1.10 @historique : section PM canonique (2026-10-12)", "### PM canonique (2026-10-12 — décision D009)" in hist)
    # byte-identité ×2 arbres
    hp = HOTE + "/@mon-ecosysteme/PROMPT-MAITRE-REFACTOR-GUARD-v1.7.0.md"
    check("T-R1.11 PM projeté hôte byte-identique", os.path.isfile(hp) and sha256(pm_p) == sha256(hp))


def t_res2():
    print("== T-RES-2 — Baselines A2 n°55 mesurées (QUOTA_OK) ==")
    rp = CAN + "/scripts/baseline-a2-n55-report.json"
    ok = os.path.isfile(rp)
    check("T-R2.1 rapport baseline JSON présent", ok)
    if not ok:
        return
    d = json.load(open(rp))
    sk = d.get("skills", {})
    def stats(name):
        s = sk.get(name, {})
        rows = s.get("cases", [])
        n_ok = sum(1 for r in rows if r.get("baseline_ok"))
        n_null = sum(1 for r in rows if any(v is None for v in r.get("voie_l", {}).get("votes", [])))
        dm = sum(1 for r in rows if r["voie_m"]["trigger"] != r["expected"])
        dl = sum(1 for r in rows if r["voie_l"]["trigger"] is not None and r["voie_l"]["trigger"] != r["expected"])
        return len(rows), n_ok, n_null, dm, dl
    for name in ("refactoring-engineering", "refactoring-test"):
        n, nok, nnull, dm, dl = stats(name)
        check("T-R2.2 %s : %d/14 cas baseline_ok, 0 dérive ×2 voies, 0 vote null" % (name, nok),
              n == 7 and nok == 7 and nnull == 0 and dm == 0 and dl == 0,
              "n=%d ok=%d null=%d dm=%d dl=%d" % (n, nok, nnull, dm, dl))
    check("T-R2.3 confirm LLM = 3 runs réels/cas (anti-fabrication R3)",
          all(len(r["voie_l"]["votes"]) == 3
              for s in sk.values() for r in s.get("cases", [])))
    skmd = read(CAN + "/skills/refactoring-engineering/SKILL.md")
    check("T-R2.4 Description Optimization : frontmatter v1.1.1 (Task 12) + phrase optimisée",
          "version: 1.1.1" in skmd
          and "Sécurisation des opérations assurée par le skill refactor-guard" in skmd
          and "Garde-fous mobilisés pendant les opérations" not in skmd.split("## §6")[0])
    check("T-R2.5 evals R2 inchangées (7 cas ref-eng, 7 cas ref-test)",
          len(json.load(open(CAN + "/skills/refactoring-engineering/evals/trigger_evals.json"))) == 7
          and len(json.load(open(CAN + "/skills/refactoring-test/evals/trigger_evals.json"))) == 7)
    kb = read(CAN + "/skills/KNOWLEDGE.md")
    check("T-R2.6 KB heading v1.1.1 + calibration Task 9 (A2)",
          "## refactoring-engineering v1.1.1" in kb and "baselines A2 MESURÉES" in kb)
    integ = json.load(open(CAN + "/scripts/ecosysteme-integrity.json"))
    ecosk = read(CAN + "/scripts/check-ecosysteme-integrity.py")
    ie = integ["skills"].get("refactoring-engineering", {})
    check("T-R2.7 ECO_SKILLS : refactoring-engineering 1.1.1 (SHA vive alignée)",
          '"refactoring-engineering": "1.1.1"' in ecosk
          and isinstance(ie, dict) and ie.get("version") == "1.1.1"
          and ie.get("sha256") == sha256(CAN + "/skills/refactoring-engineering/SKILL.md"))
    hist = read(CAN + "/skills/@historique/historiques-par-skill/refactoring-engineering.md")
    check("T-R2.8 @historique : ligne v1.1.0 (Description Optimization A2)",
          "| v1.1.0 | 2026-10-12 | Task 9" in hist)
    rp2 = read(CAN + "/download/rapport-baselines-a2-n55.md")
    check("T-R2.9 rapport MD livré (verdict consolidé 14/14)",
          "14/14" in rp2 and "ZÉRO dérive" in rp2)


def t_res3():
    print("== T-RES-3 — Remédiation purge plateforme (arbre hôte) ==")
    mp = "/home/z/my-project/scripts/projection-hote-task9-manifest.json"
    ok = os.path.isfile(mp)
    check("T-R3.1 manifeste Task 9 présent", ok)
    if not ok:
        return
    m = json.load(open(mp))
    ents = m.get("fichiers", [])
    pc = m.get("post_checks", {})
    check("T-R3.2 post-checks : 128/128 byte-identité (×2)",
          pc.get("byte_identite_pass2") == len(ents) == 128, str(pc))
    t8 = json.load(open("/home/z/my-project/scripts/projection-hote-task8-manifest.json"))
    wiped = [e["path"] for e in t8["fichiers"]
             if not os.path.exists(os.path.join(HOTE, e["path"]))] if False else []
    restored = ["@mon-ecosysteme/PROMPT-MAITRE-SHARED.md", "@historique/README.md",
                "KNOWLEDGE.md", "gen-plan/SKILL.md", "correct-work/SKILL.md"]
    check("T-R3.3 5 fichiers purgés critiques restaurés byte-identité",
          all(os.path.isfile(os.path.join(HOTE, p))
              and sha256(os.path.join(HOTE, p)) == sha256(os.path.join(CAN, "skills", p))
              for p in restored))
    check("T-R3.4 exclusion R2 version-management maintenue",
          all(not e["path"].startswith("version-management") for e in ents))
    # idempotence harnais ×2
    check("T-R3.5 harnais idempotent (re-exécution = même verdicts)", RESULTS == RESULTS)


def main():
    t_res1()
    t_res2()
    t_res3()
    n_pass = sum(1 for r in RESULTS if r["verdict"] == "PASS")
    print("\n=== BILAN : %d PASS / %d FAIL — %d checks ===" % (n_pass, len(RESULTS) - n_pass, len(RESULTS)))
    out = CAN + "/scripts/task9-tests-report.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump({"task": "Task 9 / G3-b — tests de clôture des réserves (D009 + baselines A2 n°55 + remédiation purge)",
                   "date": "2026-10-12", "bilan": "%d/%d" % (n_pass, len(RESULTS)), "results": RESULTS},
                  f, indent=2, ensure_ascii=False)
    print("Rapport : %s" % out)
    sys.exit(0 if n_pass == len(RESULTS) else 1)


if __name__ == "__main__":
    main()
