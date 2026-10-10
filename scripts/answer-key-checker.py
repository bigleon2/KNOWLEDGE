#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.6.8)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.

Arbitre answer-key-checker — 16 checks (propositions-qwen.md §4.1-§4.4)
Phase N20 (session B12-r41, demande n°34) — montée gen-plan v3.13.0.

Axes :
  1-4   Structurels    : références, skill knowledge-observer, SHARED §8, KB
  5-9   Fonctionnels   : answer key exécutable, Graph Diamond, ToT, Second Opinion, Task Observer
  10-12 Idempotence    : rejeu stable, marqueurs uniques, pas de régression de version
  13-16 Intégration    : hooks gen-plan E7/E8, M5 prompt-engineering, AVEUGLE correct-work, E15 knowledge-observer

Usage : python3 scripts/answer-key-checker.py [--skills-root /chemin/skills]
Code retour : 0 si et seulement si les 16 checks sont PASS.
"""

import os
import re
import sys
import hashlib

REPO_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_ROOT = os.path.join(REPO_DIR, "skills")
KB_PATH = os.path.join(SKILLS_ROOT, "KNOWLEDGE.md")
SHARED_PATH = os.path.join(SKILLS_ROOT, "@mon-ecosysteme", "PROMPT-MAITRE-SHARED.md")

EXPECTED_VERSIONS = {"gen-plan": "3.13.0", "correct-work": "2.6.0", "prompt-engineering": "2.1.0"}
MIN_VERSIONS = {"gen-plan": (3, 13, 0), "correct-work": (2, 6, 0), "prompt-engineering": (2, 1, 0)}

REFS_ATTENDUES = [
    ("gen-plan/references/answer-key-template.md", "ANSWER-KEY-TEMPLATE"),
    ("gen-plan/references/graph-diamond-pattern.md", "GRAPH-DIAMOND"),
    ("gen-plan/references/observation-patterns.md", "OBSERVATION-PATTERNS"),
    ("prompt-engineering/references/ideation-protocol.md", "IDEATION-PROTOCOL"),
    ("correct-work/references/verification-protocol.md", "VERIFICATION-PROTOCOL"),
]


def read(path):
    if not os.path.isfile(path):
        return None
    with open(path, encoding="utf-8") as f:
        return f.read()


def semver_tuple(v):
    try:
        return tuple(int(x) for x in v.split("."))
    except Exception:
        return (0, 0, 0)


def main():
    results = []
    passed = 0

    def check(n, desc, ok, detail=""):
        nonlocal passed
        status = "PASS" if ok else "FAIL"
        results.append((n, desc, status, detail))
        if ok:
            passed += 1

    # --- §4.1 Vérifications structurelles (1-4) ---
    # Check 1 : 5 fichiers de référence existent
    details = []
    for rel, _ in REFS_ATTENDUES:
        p = os.path.join(SKILLS_ROOT, rel)
        details.append(f"{rel}:{'OK' if os.path.isfile(p) else 'ABSENT'}")
    check(1, "5 fichiers de référence existent", all("ABSENT" not in d for d in details), "; ".join(details))

    # Check 2 : knowledge-observer a SKILL.md valide (frontmatter)
    ko = read(os.path.join(SKILLS_ROOT, "knowledge-observer", "SKILL.md")) or ""
    fm_ok = ko.startswith("---") and all(
        f in ko.split("---", 2)[1] for f in ("name:", "version:", "category:", "language:", "description:", "dependencies:")
    )
    check(2, "knowledge-observer SKILL.md valide", fm_ok, "frontmatter " + ("complet" if fm_ok else "incomplet"))

    # Check 3 : SHARED contient §8 (marqueur)
    shared = read(SHARED_PATH) or ""
    has8 = "## §8" in shared and "PATTERN:SHARED-8-FONDAMENTALES-v1.0.0" in shared
    check(3, "SHARED contient §8", has8, "SHARED v1.6.0 attendu")

    # Check 4 : KNOWLEDGE.md contient knowledge-observer
    kb = read(KB_PATH) or ""
    check(4, "KNOWLEDGE.md contient knowledge-observer", "## knowledge-observer v" in kb, "entrée KB")

    # --- §4.2 Vérifications fonctionnelles (5-9) ---
    # Check 5 : answer key exécutable (critère + vérification + source non vides, statuts valides)
    ak = read(os.path.join(SKILLS_ROOT, "gen-plan", "references", "answer-key-b12.md")) or ""
    decisions = re.findall(r'- id: "(D\d+)"(.+?)(?=- id: "D\d+"|```|\Z)', ak, re.S)
    ok5 = bool(decisions)
    bad = []
    for did, body in decisions:
        for champ in ("criterion:", "verification:", "source:", "priority:"):
            if champ not in body:
                ok5 = False
                bad.append(f"{did}/{champ}")
        if not re.search(r"status:\s*\"?(pending|verified|failed)\"?", body):
            ok5 = False
            bad.append(f"{did}/status")
    n_verified = len(re.findall(r'status:\s*"?verified"?', ak))
    check(5, f"Answer key exécutable ({len(decisions)} décisions, {n_verified} verified)", ok5, "; ".join(bad[:4]))

    # Check 6 : Graph Diamond cohérent (4 phases + anti-pattern)
    gd = read(os.path.join(SKILLS_ROOT, "gen-plan", "references", "graph-diamond-pattern.md")) or ""
    phases = sum(1 for m in ("Décomposition", "Exécution parallèle", "Synthèse", "Vérification") if m.lower() in gd.lower())
    anti = "effets de bord partagés" in gd or "Anti-patterns" in gd
    check(6, "Graph Diamond cohérent", phases == 4 and anti, f"{phases}/4 phases, anti-pattern={'oui' if anti else 'non'}")

    # Check 7 : ToT a un pre-check (3 questions)
    ip = read(os.path.join(SKILLS_ROOT, "prompt-engineering", "references", "ideation-protocol.md")) or ""
    q3 = sum(1 for q in ("Le problème est-il ouvert", "Les enjeux sont-ils élevés", "La demande est-elle explicite") if q in ip)
    tot_ok = q3 == 3 and "N + V + F" in ip.replace("≥", ">=")
    check(7, "ToT a un pre-check (3 questions)", tot_ok, f"{q3}/3 questions")

    # Check 8 : Second Opinion est aveugle (inputs filtrés)
    vp = read(os.path.join(SKILLS_ROOT, "correct-work", "references", "verification-protocol.md")) or ""
    blind = "sans le contexte de construction" in vp and "Historique de construction" in vp
    check(8, "Second Opinion est aveugle", blind, "inputs filtrés " + ("documentés" if blind else "absents"))

    # Check 9 : Task Observer a un cycle A-H (8 étapes)
    op = read(os.path.join(SKILLS_ROOT, "gen-plan", "references", "observation-patterns.md")) or ""
    lettres = sum(1 for l in "ABCDEFGH" if re.search(rf"\|\s*\*\*{l}\*\*\s*\|", op) or re.search(rf"\|\s*{l}\s*\|", op))
    check(9, "Task Observer a un cycle A-H", lettres == 8, f"{lettres}/8 étapes")

    # --- §4.3 Vérifications d'idempotence (10-12) ---
    # Check 10 : application 2x = même résultat (rejeu stable des marqueurs)
    def empreinte_marqueurs():
        h = hashlib.sha256()
        for rel, _ in REFS_ATTENDUES:
            c = read(os.path.join(SKILLS_ROOT, rel)) or ""
            h.update(c.encode("utf-8"))
        h.update((read(SHARED_PATH) or "").encode("utf-8"))
        return h.hexdigest()
    h1, h2 = empreinte_marqueurs(), empreinte_marqueurs()
    check(10, "Application 2x = même résultat", h1 == h2, f"sha16 {h1[:16]} stable")

    # Check 11 : pas de duplication (chaque marqueur PATTERN: apparaît exactement 1x)
    dups = []
    for rel, marqueur in REFS_ATTENDUES:
        c = read(os.path.join(SKILLS_ROOT, rel)) or ""
        n_ouvert = c.count(f"<!-- PATTERN:{marqueur}-v1.0.0 -->")
        n_ferme = c.count(f"<!-- FIN-PATTERN:{marqueur}-v1.0.0 -->")
        if n_ouvert != 1 or n_ferme != 1:
            dups.append(f"{rel}({n_ouvert}/{n_ferme})")
    n_shared8 = (shared.count("<!-- PATTERN:SHARED-8-FONDAMENTALES-v1.0.0 -->"), shared.count("<!-- FIN-PATTERN:SHARED-8-FONDAMENTALES-v1.0.0 -->"))
    if n_shared8 != (1, 1):
        dups.append(f"SHARED§8({n_shared8[0]}/{n_shared8[1]})")
    check(11, "Pas de duplication de marqueurs", not dups, "; ".join(dups) or "12 marqueurs uniques")

    # Check 12 : pas de régression (versions >= attendues)
    regs = []
    for skill, minv in MIN_VERSIONS.items():
        c = read(os.path.join(SKILLS_ROOT, skill, "SKILL.md")) or ""
        m = re.search(r"^version:\s*([\d.]+)", c, re.M)
        v = semver_tuple(m.group(1)) if m else (0, 0, 0)
        if v < minv:
            regs.append(f"{skill}={m.group(1) if m else '?'} < {minv}")
    check(12, "Pas de régression de version", not regs, "; ".join(regs) or ">= " + ", ".join(f"{k} {v}" for k, v in EXPECTED_VERSIONS.items()))

    # --- §4.4 Vérifications d'intégration (13-16) ---
    gp = read(os.path.join(SKILLS_ROOT, "gen-plan", "SKILL.md")) or ""
    pe = read(os.path.join(SKILLS_ROOT, "prompt-engineering", "SKILL.md")) or ""
    cw = read(os.path.join(SKILLS_ROOT, "correct-work", "SKILL.md")) or ""

    # Check 13 : gen-plan invoque Answer Key (hook E1 + arbitre E7/E8)
    c13 = "PATTERN:GEN-PLAN-HOOKS-PATTERNS-v1.0.0" in gp and "answer-key" in gp and "E1" in gp
    check(13, "gen-plan invoque Answer Key (E1/E7-E8)", c13, "hooks §1.2bis")

    # Check 14 : prompt-engineering a M5
    c14 = "PATTERN:PE-M5-IDEATION-v1.0.0" in pe and "M5" in pe and "Tree of Thought" in pe
    check(14, "prompt-engineering a M5 (IDÉATION)", c14, "mode + protocole")

    # Check 15 : correct-work a le mode AVEUGLE
    c15 = "AVEUGLE" in cw and "verification-protocol.md" in cw and "2nd opinion agent-driven" in cw
    check(15, "correct-work a AVEUGLE (Second Opinion)", c15, "mode + hook Étape 5")

    # Check 16 : knowledge-observer invoqué à E15 (gen-plan + KB)
    c16 = ("knowledge-observer" in gp and "E15" in gp) and ("knowledge-observer" in kb and "E15" in kb)
    check(16, "knowledge-observer invoqué à E15", c16, "gen-plan §1.2bis + KB")

    # --- Rapport ---
    total = len(results)
    print("=== Arbitre answer-key-checker (16 checks, N20) ===")
    for n, desc, status, detail in results:
        print(f"  [{status}] Check {n} : {desc} — {detail}")
    print()
    print("=== RESUME ===")
    print(f"  PASS  : {passed}/{total}")
    print(f"  FAIL  : {total - passed}/{total}")
    print(f"  VERDICT : {'ALL PASS' if passed == total else 'FAIL'}")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())
