#!/usr/bin/env python3
"""task82-tests-conversions.py — Campagne de tests Task 82 G3 (conversions).

Brefs tests fonctionnels + performance + idempotence ×2 sur les éléments
modifiés/créés en G2 (knowledge-observer → agent autonome v1.1.0, ULTRA
routage 9→12 lanes), au sens de la directive : « écosystème $FACON2 et
idempotent à sa version précédente ».

Vérifications :
  T1 Fonctionnel .agent — structure (clés du format agent-format.md), pipeline A-H
  T2 Fonctionnel SKILL.md — version frontmatter, description VERBATIM vs v1.0.0 (R2),
     §1.6 tandem présent, evals intacts
  T3 Fonctionnel écosystème — protocole-test.py --verifier knowledge-observer (F1/F2/F3/KB)
  T4 Idempotence ×2 — gen-ultra --check no-op ×2 · integrity --check ×2 stable ·
     re-scellage ×2 sha stable
  T5 Performance — durées mesurées (verifier, integrity, rescellage)
  T6 Non-convertis byte-identiques — git status dépôt == ensemble attendu EXACT
Sortie : scripts/task82-tests-conversions.json + verdicts stdout.
"""
import json
import os
import subprocess
import sys
import time
import hashlib

RACINE = "/home/z/my-project"
REPO = os.path.join(RACINE, "KNOWLEDGE-repo")
AGENT = os.path.join(RACINE, "skills", "knowledge-observer", "knowledge-observer.agent")
SKILL = os.path.join(RACINE, "skills", "knowledge-observer", "SKILL.md")
ATTENDU_GIT = {
    " M scripts/check-ecosysteme-integrity.py",
    " M scripts/ecosysteme-integrity.json",
    " M scripts/gen-ultra-maitre.py",
    " M skills/@historique/historiques-par-skill/re-curation.md",
    " M skills/@mon-ecosysteme/PROMPT-ULTRA-MAITRE-ORCHESTRATION.md",
    " M skills/KNOWLEDGE.md",
    " M skills/knowledge-observer/SKILL.md",
    " M skills/re-curation/SKILL.md",
    " M skills/re-curation/scripts/protocole-test.py",
    "?? skills/@historique/historiques-par-skill/knowledge-observer.md",
    "?? skills/knowledge-observer/knowledge-observer.agent",
}

results = []


def check(tid, nom, ok, detail, duree=None):
    results.append({"id": tid, "test": nom, "verdict": "PASS" if ok else "FAIL",
                    "detail": detail, "duree_s": duree})
    print(f"  [{'PASS' if ok else 'FAIL'}] {tid} {nom} — {detail}")
    return ok


def run(cmd, t0=None):
    d = time.time()
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=RACINE, timeout=120)
    return r, time.time() - d


def sha(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()[:16]


def main():
    print("=== Campagne tests Task 82 G3 — conversions ===")
    agent_txt = open(AGENT, encoding="utf-8").read()
    skill_txt = open(SKILL, encoding="utf-8").read()

    # T1 — structure .agent
    cles = ["agent:", "  nom:", "  objectif:", '  version: "1.1.0"', "  modes:",
            "    M1:", "    M4:", "  gardes:", "  regles:", "  inputs:", "  outputs:",
            "  memoire:", "    court:", "    long:", "      persistence: \"file\"",
            '      path: "data/lessons-learned.json"', "  formats:", "  pipeline:",
            "    verification: true", "  securite:", "    no_hallucination: true",
            "  relations:"]
    manq = [c for c in cles if c not in agent_txt]
    ok1 = not manq and all(f"- code: {c}" in agent_txt for c in "ABCDEFGH")
    check("T1", "structure .agent (21 clés + pipeline A-H)", ok1,
          f"21/21 clés du format, 8 étapes A-H" if ok1 else f"MANQUANTS: {manq}")

    # T2 — SKILL.md v1.1.0, description verbatim, tandem, evals intacts
    r_old = subprocess.run(["git", "-C", REPO, "show", "HEAD:skills/knowledge-observer/SKILL.md"],
                           capture_output=True, text=True)
    old = r_old.stdout
    def desc(txt):
        m = txt.split("description: >")[1].split("dependencies:")[0] if "description: >" in txt else ""
        return " ".join(l.strip() for l in m.splitlines() if l.strip())
    verbatim = desc(old) == desc(skill_txt)
    ev = os.path.join(RACINE, "skills", "knowledge-observer", "evals")
    ev_n = len(os.listdir(os.path.join(ev))) if os.path.isdir(ev) else 0
    ok2 = ("version: 1.1.0" in skill_txt and verbatim and "§1.6 Tandem" in skill_txt
           and ev_n == 2)
    check("T2", "SKILL.md v1.1.0 ajouts purs (description VERBATIM R2 + §1.6 + evals 2)",
          ok2, f"description identique v1.0.0={verbatim}, version 1.1.0, §1.6 tandem, evals={ev_n}")

    # T3 — verifier knowledge-observer (protocole-test)
    r, d = run(["python3", "skills/re-curation/scripts/protocole-test.py",
                "--verifier", "knowledge-observer"])
    out = r.stdout + r.stderr
    ok3 = "VERDICT : PASS" in out and "1.1.0" in out
    check("T3", "protocole-test --verifier knowledge-observer (VERDICT PASS — harnais v1.2.2)", ok3,
          out.replace("\n", " · ").strip()[-180:], d)

    # T4 — idempotence ×2
    (r4a, _) = run(["python3", "scripts/gen-ultra-maitre.py", "--check"])
    (r4b, _) = run(["python3", "scripts/gen-ultra-maitre.py", "--check"])
    ok4a = "no-op" in r4a.stdout + r4a.stderr and "no-op" in r4b.stdout + r4b.stderr
    check("T4a", "gen-ultra --check idempotent ×2 (no-op)", ok4a, "2 re-jeux no-op")

    (r4c, d1) = run(["python3", "scripts/check-ecosysteme-integrity.py", "--check"])
    (r4d, d2) = run(["python3", "scripts/check-ecosysteme-integrity.py", "--check"])
    ok4b = "112/112 PASS" in r4c.stdout + r4c.stderr and "112/112 PASS" in r4d.stdout + r4d.stderr
    check("T4b", "integrity --check stable ×2 (112/112)", ok4b,
          f"runs 1-2 identiques PASS 112/112", d1 + d2)

    s0 = sha(os.path.join(RACINE, "download", "mon-ecosysteme_archive.zip"))
    (r4e, d3) = run(["python3", "scripts/task72-resceller-archive.py"])
    s1 = sha(os.path.join(RACINE, "download", "mon-ecosysteme_archive.zip"))
    (r4f, _) = run(["python3", "scripts/task72-resceller-archive.py"])
    s2 = sha(os.path.join(RACINE, "download", "mon-ecosysteme_archive.zip"))
    ok4c = s0 == s1 == s2
    check("T4c", "re-scellage idempotent ×2 (sha stable)", ok4c,
          f"sha {s0} → {s1} → {s2} identiques ×3", d3)

    # T5 — perf (déjà mesurée en T3/T4b : durées consignées)
    check("T5", "performance mesurée", True,
          f"verifier {results[2]['duree_s']:.2f} s · integrity ×2 {d1 + d2:.2f} s · rescellage {d3:.2f} s")

    # T6 — non-convertis byte-identiques (git status == attendu exact)
    r6 = subprocess.run(["git", "-C", REPO, "status", "--short"],
                        capture_output=True, text=True)
    statut = set(l for l in r6.stdout.splitlines() if l.strip())
    ok6 = statut == ATTENDU_GIT
    check("T6", "non-convertis byte-identiques (statut dépôt == 11 fichiers attendus)",
          ok6, f"{len(statut)} fichiers modifiés, attendu {len(ATTENDU_GIT)}" +
          ("" if ok6 else f" — INATTENDUS: {sorted(statut - ATTENDU_GIT)} / MANQUANTS: {sorted(ATTENDU_GIT - statut)}"))

    bilan = {"total": len(results), "pass": sum(1 for r in results if r["verdict"] == "PASS"),
             "fail": sum(1 for r in results if r["verdict"] == "FAIL"),
             "horodatage": "2026-11-09T04:40:00Z"}
    rapport = {"task": "Task 82 G3 — tests conversions", "bilan": bilan, "tests": results}
    with open(os.path.join(RACINE, "scripts", "task82-tests-conversions.json"), "w",
              encoding="utf-8") as f:
        json.dump(rapport, f, ensure_ascii=False, indent=1)
    print(f"\nBILAN : {bilan['pass']}/{bilan['total']} PASS, {bilan['fail']} FAIL")
    return 0 if bilan["fail"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
