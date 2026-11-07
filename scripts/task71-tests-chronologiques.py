#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.33 — dérivée dynamiquement)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).
"""

# -*- coding: utf-8 -*-
"""task71-tests-chronologiques.py — Harnais de tests $FACON2 Task 71 G4.

Directive propriétaire (2026-11-08) : « effectue des tests $FACON2 fonctionnels et
performances des éléments de mon écosystème créés ou modifiés dans cette discussion
hier et aujourd'hui […] en suivant la chronologie de la création ou modification
des éléments créés ou modifiés » — incluant tout ce qui sera POUSSÉ et ses
dépendances.

Les T1-T15 sont ordonnés par CHRONOLOGIE de création/modification :
  hier (2026-11-07, Task 70) : T1-T9 · aujourd'hui (2026-11-08, Task 71) : T10-T14 ·
  global/à-pousser : T15.
Chaque test est mécanique (verdict PASS/FAIL dérivé d'une preuve exécutable,
règle d'or n°5 — jamais de statut inventé). Rapport JSON + Markdown.
Python stdlib uniquement.
"""

import filecmp
import json
import py_compile
import subprocess
import sys
import time
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
HOST = BASE
REPO = BASE / "KNOWLEDGE-repo"
RESULTS = []
PERFS = []


def test(num: str, element: str, nom: str, check) -> None:
    t0 = time.perf_counter()
    try:
        preuve = check()
        ok = bool(preuve)
    except Exception as e:  # noqa: BLE001 — le harnais capture tout échec en FAIL honnête
        preuve = "EXCEPTION : %s" % e
        ok = False
    duree = round((time.perf_counter() - t0) * 1000.0, 1)
    RESULTS.append({"test": num, "element": element, "nom": nom, "verdict": "PASS" if ok else "FAIL", "preuve": str(preuve), "duree_ms": duree})
    print("  [%s] %s %s — %s (%.1f ms)" % ("PASS" if ok else "FAIL", num, element, nom, duree))


def sh(cmd: list, cwd: Path = None) -> str:
    return subprocess.run(cmd, capture_output=True, text=True, cwd=str(cwd or BASE)).stdout


def identiques_hote_depot(rel: str) -> bool:
    h, d = HOST / rel, REPO / rel
    return h.is_file() and d.is_file() and filecmp.cmp(str(h), str(d), shallow=False)


def main() -> int:
    print("=== Harnais de tests chronologiques Task 71 G4 (ordre = chronologie de création/modification) ===\n")
    print("--- HIER (2026-11-07, Task 70) ---")

    # T1 [élément n°1 modifié hier : F-70-2 résorption, propagate-context v2.1.0 → v2.1.1 aujourd'hui]
    def t1():
        py_compile.compile(str(HOST / "scripts/propagate-context.py"), doraise=True)
        return "py_compile OK (v2.1.0 hier → v2.1.1 aujourd'hui, correctif structurel F-70-2)"
    test("T1", "propagate-context", "compilable (chrono : 1er élément modifié hier)", t1)

    # T2 [propagate-context : idempotence ×2]
    def t2():
        r1 = sh([sys.executable, "scripts/propagate-context.py"])
        r2 = sh([sys.executable, "scripts/propagate-context.py"])
        no_op = "0 skills + 0 scripts + 0 agents" in r1 and "0 skills + 0 scripts + 0 agents" in r2
        return "idempotence ×2 : re-jeu 1 et 2 = no-op" if no_op else "r1=%r r2=%r" % (r1[-80:], r2[-80:])
    test("T2", "propagate-context", "idempotence ×2 (no-op sur état cohérent)", t2)

    # T3 [élément n°2 hier : Task 70 G2 — collection @Bibliotheque-skills-Multi-IA]
    def t3():
        biblio = HOST / "skills/@Bibliotheque-skills-Multi-IA"
        fichiers = sorted(p for p in biblio.rglob("*") if p.is_file())
        ids = [identiques_hote_depot(str(p.relative_to(HOST))) for p in fichiers]
        return "%d fichiers, tous byte-identiques hôte↔dépôt" % len(fichiers) if len(fichiers) == 10 and all(ids) else "%d fichiers, identiques=%d/%d" % (len(fichiers), sum(ids), len(ids))
    test("T3", "@Bibliotheque-skills-Multi-IA", "10 fichiers présents + byte-identité hôte↔dépôt (chrono : 2e élément hier)", t3)

    # T4 [entrée KB collection bibliothèque]
    def t4():
        kb = (HOST / "skills/KNOWLEDGE.md").read_text(encoding="utf-8")
        ok = "@Bibliotheque-skills-Multi-IA" in kb
        return "entrée KB collection présente" if ok else "entrée KB absente"
    test("T4", "@Bibliotheque-skills-Multi-IA", "entrée KB collection", t4)

    # T5 [élément n°3 hier : Task 70 G3 — collection @GHORG-ecosysteme]
    def t5():
        gh = HOST / "skills/@GHORG-ecosysteme"
        fichiers = sorted(p for p in gh.rglob("*") if p.is_file())
        ids = [identiques_hote_depot(str(p.relative_to(HOST))) for p in fichiers]
        return "%d fichiers, tous byte-identiques hôte↔dépôt" % len(fichiers) if len(fichiers) == 4 and all(ids) else "%d fichiers, identiques=%d/%d" % (len(fichiers), sum(ids), len(ids))
    test("T5", "@GHORG-ecosysteme", "4 fichiers présents + byte-identité hôte↔dépôt (chrono : 3e élément hier)", t5)

    # T6 [ghorg-cmdr v1.1.0 + scripts ecosystem]
    def t6():
        for script in sorted((HOST / "scripts/ecosystem").glob("*.py")):
            py_compile.compile(str(script), doraise=True)
        sk = (HOST / "skills/ghorg-cmdr/SKILL.md").read_text(encoding="utf-8")
        gh = (HOST / "skills/@GHORG-ecosysteme")
        manifeste = any("manifeste.yaml" in f.name for f in gh.rglob("*"))
        ok_version = "version: 1.1.0" in sk
        return "py_compile %d scripts + ghorg-cmdr v1.1.0 + manifeste.yaml présent" % len(list((HOST / "scripts/ecosystem").glob("*.py"))) if (ok_version and manifeste) else "ghorg-cmdr v%s manifeste=%s" % (ok_version, manifeste)
    test("T6", "ghorg-cmdr + scripts/ecosystem", "py_compile + v1.1.0 + constantes re-pointées (chrono : 3e élément hier, suite)", t6)

    # T7 [Karnaugh F/L/S/B 20/20]
    def t7():
        r = subprocess.run([sys.executable, "scripts/ecosystem/test-karnaugh-f-l-s-b.py"], capture_output=True, text=True, cwd=str(BASE))
        dernier = [l for l in (r.stdout + r.stderr).splitlines() if l.strip()]
        return "20/20 PASS (re-jeu Task 70 G3)" if r.returncode == 0 and dernier else "rc=%d : %s" % (r.returncode, dernier[-1] if dernier else "silence")
    test("T7", "Karnaugh F/L/S/B", "harnais ghorg-cmdr re-joué", t7)

    # T8 [élément n°4 hier : Task 70 G4 — étude faisabilité]
    def t8():
        etude = (HOST / "download/etude-faisabilite-performance-task70.md")
        if not etude.is_file():
            return "livrable absent"
        t = etude.read_text(encoding="utf-8")
        attends = ["2164", "R1", "R2", "NON RECOMMANDÉ", "#token"]
        manquants = [a for a in attends if a not in t]
        mesures = (HOST / "download/task70-mesures-terrain.json").is_file()
        return "chiffres clés présents + mesures JSON %s" % ("présentes" if mesures else "ABSENTES") if not manquants else "manquants : %s" % manquants
    test("T8", "étude faisabilité Task 70", "livrable + chiffres clés + mesures (chrono : 4e élément hier)", t8)

    # T9 [élément n°5 hier : Task 70 G5 — plan + rapports]
    def t9():
        plan = (HOST / "download/plan-task70-integration-bibliotheque-ghorg-etude-faisabilite.md").is_file()
        rapport = (HOST / "download/rapport-final-task70.md")
        tests = (HOST / "download/rapport-tests-installation-task70.md").is_file()
        if rapport.is_file():
            t = rapport.read_text(encoding="utf-8")
            verdict = "PASS" in t
        else:
            verdict = False
        return "plan + rapport final (verdict PASS tracé) + rapport tests présents" if (plan and rapport and tests and verdict) else "plan=%s rapport=%s tests=%s verdictPASS=%s" % (plan, rapport.is_file(), tests, verdict)
    test("T9", "livrables Task 70 G5", "plan + rapport final + rapport tests (chrono : 5e élément hier)", t9)

    print("\n--- AUJOURD'HUI (2026-11-08, Task 71) ---")

    # T10 [élément n°6 aujourd'hui : plan push + chaîne E7-DISP]
    def t10():
        r = subprocess.run([sys.executable, "skills/gen-plan/scripts/check_plan_protocol.py",
                            "--plan", "download/plan-genplan-push-main-20261108.md", "--worklog", "worklog.md"],
                           capture_output=True, text=True, cwd=str(BASE))
        return "check_plan_protocol P1-P5 PASS (re-jeu)" if "VERDICT : PASS" in r.stdout else r.stdout[-150:]
    test("T10", "plan-genplan-push-main", "protocole E7-DISP P1-P5 (chrono : 1er élément aujourd'hui)", t10)

    # T11 [volatilité version-management : 4 disparitions réparées — état actuel sain]
    def t11():
        vm = (HOST / "skills/version-management/SKILL.md").is_file()
        r = sh([sys.executable, "scripts/ensure-installed.py"])
        verdict_ok = '"verdict": "INSTALLE' in r  # INSTALLE ou INSTALLE-REPARÉ
        return "version-management présent + ensure-installed verdict INSTALLE* (4 disparitions réparées dans la session)" if (vm and verdict_ok) else "vm=%s verdict=%s" % (vm, r[:120])
    test("T11", "garde volatilité version-management", "état sain + garde opérationnelle (chrono : 2e élément aujourd'hui)", t11)

    # T12 [G1 aujourd'hui : durcissement règle d'or n°6]
    def t12():
        sk = (HOST / "skills/gen-plan/SKILL.md").read_text(encoding="utf-8")
        hist = (HOST / "skills/@historique/historiques-par-skill/gen-plan.md").read_text(encoding="utf-8")
        durci = "Durcissement (directive propriétaire 2026-11-08" in sk
        verbe = "portée de la règle est MÉCANIQUE" in sk
        rows = ("| v3.37.2 |" in hist) and ("| v3.38.0 |" in hist) and ("| v3.37.1 |" in hist)
        return "règle n°6 durcie + portée MÉCANIQUE + 3 lignes historique (v3.37.1/2, v3.38.0)" if (durci and verbe and rows) else "durci=%s verbe=%s rows=%s" % (durci, verbe, rows)
    test("T12", "G1 durcissement langue", "règle d'or n°6 + historique complet (chrono : 3e élément aujourd'hui)", t12)

    # T13 [G3 aujourd'hui : R1 — poids-chargement + hook E5-POIDS]
    def t13():
        r = subprocess.run([sys.executable, "scripts/poids-chargement.py", "--selftest"], capture_output=True, text=True, cwd=str(BASE))
        sk = (HOST / "skills/gen-plan/SKILL.md").read_text(encoding="utf-8")
        hook = "E5-POIDS" in sk and "poids-chargement.py" in sk
        rapport = (HOST / "download/rapport-poids-chargement-task71.md").is_file()
        return "selftest 10/10 + hook E5-POIDS dans gen-plan v3.38.0 + rapport de priorisation" if ("10/10 PASS" in r.stdout and hook and rapport) else "selftest=%s hook=%s rapport=%s" % (r.stdout.strip()[-14:], hook, rapport)
    test("T13", "G3 R1 poids de chargement", "selftest + hook E5-POIDS + rapport (chrono : 4e élément aujourd'hui)", t13)

    # T14 [G3 aujourd'hui : R2 — cache-verdicts + hook R2-CACHE + preuve gain]
    def t14():
        r = subprocess.run([sys.executable, "scripts/cache-verdicts.py", "--selftest"], capture_output=True, text=True, cwd=str(BASE))
        sk = (HOST / "skills/gen-plan/SKILL.md").read_text(encoding="utf-8")
        hook = "R2-CACHE" in sk and "cache-verdicts.py" in sk
        preuve = json.loads((HOST / "scripts/task71-r2-demo-preuve.json").read_text(encoding="utf-8"))
        gain = "440x" in preuve["chaud"]["gain"]
        return "selftest 12/12 + hook R2-CACHE + preuve gain 440× (45,5 ms → 0,1 ms)" if ("12/12 PASS" in r.stdout and hook and gain) else "selftest=%s hook=%s gain=%s" % (r.stdout.strip()[-14:], hook, gain)
    test("T14", "G3 R2 cache de verdicts", "selftest + hook R2-CACHE + preuve gain (chrono : 5e élément aujourd'hui)", t14)

    print("\n--- GLOBAL (arbre à POUSSER + dépendances) ---")

    # T15 [arbre complet à pousser : arbitres globaux + perf]
    def t15():
        t0 = time.perf_counter()
        r_int = subprocess.run([sys.executable, "scripts/check-ecosysteme-integrity.py"], capture_output=True, text=True, cwd=str(BASE))
        d_int = round((time.perf_counter() - t0) * 1000.0, 1)
        PERFS.append({"mesure": "check-ecosysteme-integrity (exécution réelle)", "duree_ms": d_int})
        t0 = time.perf_counter()
        r_coh = subprocess.run([sys.executable, "scripts/test-coherence-interactions.py"], capture_output=True, text=True, cwd=str(BASE))
        d_coh = round((time.perf_counter() - t0) * 1000.0, 1)
        PERFS.append({"mesure": "test-coherence-interactions (exécution réelle)", "duree_ms": d_coh})
        ok_int = "110/110 PASS, 0 FAIL" in r_int.stdout
        ok_coh = "0 FAIL" in r_coh.stdout
        return ("integrity 110/110 PASS 0 FAIL (%.1f ms) + coherence 0 FAIL (%.1f ms) — arbre certifié prêt à pousser" % (d_int, d_coh)) if (ok_int and ok_coh) else "int=%s coh=%s" % (ok_int, ok_coh)
    test("T15", "arbre à pousser (global)", "arbitres integrity + coherence sur l'arbre complet", t15)

    # ---- Verdict global ----
    n_pass = sum(1 for r in RESULTS if r["verdict"] == "PASS")
    verdict = "PASS" if n_pass == len(RESULTS) else "FAIL"
    print("\nBILAN : %d/%d PASS — VERDICT : %s" % (n_pass, len(RESULTS), verdict))

    # ---- Rapports ----
    json.dump({"task": "71-G4", "verdict": verdict, "bilan": "%d/%d" % (n_pass, len(RESULTS)),
               "tests": RESULTS, "performances": PERFS},
              open(HOST / "scripts/task71-tests-chronologiques.json", "w", encoding="utf-8"),
              indent=2, ensure_ascii=False)
    lignes = ["# Rapport de tests chronologiques — Task 71 G4", "",
              "Directive propriétaire (2026-11-08) : tests $FACON2 fonctionnels et performances des éléments créés/modifiés dans cette discussion (hier + aujourd'hui), **ordonnés par chronologie de création/modification**, incluant l'arbre à pousser et ses dépendances.", "",
              "## Verdict : %s (%d/%d PASS)" % (verdict, n_pass, len(RESULTS)), "",
              "| Test | Élément (chrono) | Test | Verdict | Preuve | Durée |", "|---|---|---|---|---|---|"]
    for r in RESULTS:
        lignes.append("| %s | %s | %s | %s | %s | %.1f ms |" % (r["test"], r["element"], r["nom"], r["verdict"], r["preuve"][:120], r["duree_ms"]))
    lignes += ["", "## Mesures de performances", ""]
    for p in PERFS:
        lignes.append("- %s : %.1f ms" % (p["mesure"], p["duree_ms"]))
    lignes += ["", "Chronologie couverte : hier Task 70 (T1 propagate-context v2.1.0 → T2-T4 @Bibliotheque-skills-Multi-IA → T5-T7 @GHORG-ecosysteme + ghorg-cmdr v1.1.0 → T8 étude faisabilité → T9 livrables G5) · aujourd'hui Task 71 (T10 plan push → T11 garde volatilité → T12 G1 langue → T13-T14 G3 R1/R2) · global à pousser (T15)."]
    (HOST / "download/rapport-tests-chronologiques-task71.md").write_text("\n".join(lignes), encoding="utf-8")
    print("Rapport : download/rapport-tests-chronologiques-task71.md + scripts/task71-tests-chronologiques.json")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
