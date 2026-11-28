#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""task19-tests-caches-semantiques.py — Batterie $FACON2 fenêtre 15 (Task 19).

Directive (trace 1a221c134d34e9d1) : « analyse si mes skills gen-plan, correct-work
et clone-chat utilisent des caches sémantiques … optimise-les s'il le faut /
teste-les ».

6 sections S1-S6, checks binaires, stdlib uniquement :
  S1 gen-plan  : hook R2-CACHE déclaré ×2 miroirs + cache-verdicts.py présent ×2
                 (SHA identiques) + selftest 12/12 du wrapper.
  S2 cache     : comportement réel du wrapper sur fixture temporaire isolée —
                 exécution réelle 1ᵉʳ appel, REJEU au 2ᵉ (verdict identique),
                 gain mesuré, invalidation sur modification de cible, --force,
                 stats.
  S3 correct-work v2.12.2 : frontmatter ×2, §1.4bis (4 règles) ×2, matrice §12
                 v2.12.2 ×2, arbitre canonique recalibré ×2, 16/16 PASS réel.
  S4 clone-chat v2.2.0 : frontmatter ×2, §1.13 (couverture + validation) ×2,
                 grille incrémentale ×2, conventions §6 ×2, tag cache ×2.
  S5 perf réel : vrai arbitre (task15-scan-jetons.py) via cache sur cache
                 temporaire — exécution réelle figée puis rejeu, gain ≥ 10×.
  S6 cohérence : KB v2.12.2 + v2.2.0 ×2, invariants ECO_SKILLS ×2, PM v2.12.2
                 présent + v2.12.1 archivé @historique ×2, parité SHA ×2 des
                 fichiers de la montée.

Idempotent : fixtures temporaires neuves à chaque passage (le 2ᵉ passage est
identique au 1ᵉʳ). Rapport : scripts/task19-cache-report.json.
"""
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HOST = Path("/home/z/my-project")
REPO = HOST / "KNOWLEDGE-repo"
RAPPORT = HOST / "scripts" / "task19-cache-report.json"

resultats = {"sections": {}, "ok": 0, "total": 0}


def check(section: str, nom: str, cond: bool, detail: str = "") -> None:
    resultats["total"] += 1
    resultats["sections"].setdefault(section, []).append(
        {"check": nom, "verdict": "PASS" if cond else "FAIL", "detail": detail[:180]})
    print(f"  [{'PASS' if cond else 'FAIL'}] {nom}" + (f" — {detail[:120]}" if detail and not cond else ""))


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:12]


def lire(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def section_s1() -> None:
    print("S1 — gen-plan : hook R2-CACHE + wrapper")
    for base, tag in ((HOST, "hôte"), (REPO, "dépôt")):
        sk = lire(base / "skills" / "gen-plan" / "SKILL.md")
        check("S1", f"hook R2-CACHE déclaré ({tag})", "R2-CACHE" in sk and "cache-verdicts.py" in sk)
    c1, c2 = HOST / "scripts" / "cache-verdicts.py", REPO / "scripts" / "cache-verdicts.py"
    check("S1", "cache-verdicts.py présent ×2 miroirs SHA identiques",
          c1.is_file() and c2.is_file() and sha(c1) == sha(c2), f"{sha(c1) if c1.is_file() else 'absent'}")
    r = subprocess.run([sys.executable, str(c1), "--selftest"], capture_output=True, text=True, timeout=120)
    check("S1", "selftest wrapper 12/12 PASS", "12/12 PASS" in r.stdout, r.stdout[-200:] if r.returncode else "")


def section_s2() -> None:
    print("S2 — cache : comportement réel (fixture temporaire isolée)")
    tmp = Path(tempfile.mkdtemp(prefix="t19-cache-"))
    cible = tmp / "cible.txt"
    cible.write_text("état-A", encoding="utf-8")
    grader = tmp / "grader.py"
    grader.write_text(
        "import sys, time\n"
        "time.sleep(0.2)\n"
        "print('VERDICT: PASS état-A')\n", encoding="utf-8")
    env = dict(os.environ, CACHE_VERDICTS_DIR=str(tmp / "cache"))
    cmd = [sys.executable, str(HOST / "scripts" / "cache-verdicts.py"), "run", "--",
           sys.executable, str(grader), "--cibles", str(cible)]
    t0 = time.perf_counter()
    r1 = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=120)
    d1 = time.perf_counter() - t0
    check("S2", "1ᵉʳ appel : exécution réelle (verdict grader)", "VERDICT: PASS état-A" in r1.stdout)
    check("S2", "1ᵉʳ appel : marqueur EXÉCUTION RÉELLE", "EXÉCUTION RÉELLE" in r1.stderr)
    check("S2", "durée 1ᵉʳ appel ≥ 0,2 s (grader lent)", d1 >= 0.2, f"{d1:.3f} s")
    t1 = time.perf_counter()
    r2 = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=120)
    d2 = time.perf_counter() - t1
    check("S2", "2ᵉ appel : REJEU SANS RÉ-APPEL", "REJEU SANS RÉ-APPEL" in r2.stderr)
    check("S2", "verdict figé identique", r1.stdout == r2.stdout)
    check("S2", "2ᵉ appel < 0,1 s", d2 < 0.1, f"{d2:.3f} s")
    gain = d1 / d2 if d2 > 0 else float("inf")
    check("S2", "gain mesuré ≥ 5×", gain >= 5, f"gain {gain:.0f}×")
    resultats.setdefault("mesures", {})["s2_rejeu"] = {"reel_ms": round(d1 * 1000), "rejeu_ms": round(d2 * 1000), "gain": round(gain)}
    # invalidation
    cible.write_text("état-B", encoding="utf-8")
    r3 = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=120)
    check("S2", "invalidation sur modification cible → ré-exécution réelle",
          "EXÉCUTION RÉELLE" in r3.stderr and "VERDICT: PASS état-A" in r3.stdout)
    # --force
    r4 = subprocess.run(cmd + ["--force"], capture_output=True, text=True, env=env, timeout=120)
    check("S2", "--force ré-exécute réellement", "EXÉCUTION RÉELLE" in r4.stderr)
    # stats
    r5 = subprocess.run([sys.executable, str(HOST / "scripts" / "cache-verdicts.py"), "stats"],
                        capture_output=True, text=True, env=env, timeout=60)
    check("S2", "stats lisibles (entrées)", "entrée(s)" in r5.stdout)
    import shutil as _sh
    _sh.rmtree(tmp, ignore_errors=True)


def section_s3() -> None:
    print("S3 — correct-work v2.12.2")
    regles = ("Autorisé", "Interdit", "Invalidation", "Idempotence préservée", "cache-verdicts.py")
    for base, tag in ((HOST, "hôte"), (REPO, "dépôt")):
        sk = lire(base / "skills" / "correct-work" / "SKILL.md")
        check("S3", f"frontmatter version 2.12.2 ({tag})", "version: 2.12.2" in sk)
        check("S3", f"§1.4bis présente avec les 4 règles ({tag})",
              "§1.4bis Re-jeux et cache de verdicts" in sk and all(r in sk for r in regles))
        check("S3", f"matrice §12 ligne v2.12.2 ({tag})", "| v2.12.2 | Re-jeux et cache de verdicts" in sk)
        arb = lire(base / "skills" / "correct-work" / "scripts" / "verify-correct-work.py")
        check("S3", f"arbitre canonique recalibré 2.12.2 ({tag})",
              'EXPECTED_VERSION = "2.12.2"' in arb and "v2.12.2.md" in arb)
    r = subprocess.run([sys.executable, str(REPO / "skills" / "correct-work" / "scripts" / "verify-correct-work.py")],
                       capture_output=True, text=True, timeout=120)
    check("S3", "verify-correct-work : 16/16 PASS réel", "16/16" in r.stdout or "PASS  : 16/16" in r.stdout,
          (r.stdout + r.stderr)[-200:])
    check("S3", "frontière preuve citée (JAMAIS une preuve en soi)",
          "JAMAIS une preuve en soi" in lire(HOST / "skills" / "correct-work" / "SKILL.md"))


def section_s4() -> None:
    print("S4 — clone-chat v2.2.0")
    marqueurs = ("§1.13 Cache d'analyse des clones", "Garde de couverture",
                 "Validation inchangée", "Clone incrémental (§1.13, delta worklog)",
                 "Cache d'analyse (v2.2.0)")
    for base, tag in ((HOST, "hôte"), (REPO, "dépôt")):
        sk = lire(base / "skills" / "clone-chat" / "SKILL.md")
        check("S4", f"frontmatter version 2.2.0 ({tag})", "version: 2.2.0" in sk)
        check("S4", f"tag cache présent ({tag})", "  - cache" in sk)
        check("S4", f"§1.13 complète ({tag})", all(m in sk for m in marqueurs))
        check("S4", f"note grille v2.2.0 ({tag})", "**Note v2.2.0**" in sk)
        check("S4", f"le clone complet demeure canonique ({tag})",
              "le clone complet demeure l'instantané de clôture" in sk)


def section_s5() -> None:
    print("S5 — performance réel : arbitre scan-jetons via cache")
    tmp = Path(tempfile.mkdtemp(prefix="t19-perf-"))
    env = dict(os.environ, CACHE_VERDICTS_DIR=str(tmp / "cache"))
    scan = HOST / "scripts" / "task15-scan-jetons.py"
    cibles = [str(scan), str(HOST / "skills" / "correct-work" / "SKILL.md"),
              str(HOST / "skills" / "clone-chat" / "SKILL.md")]
    cmd = [sys.executable, str(HOST / "scripts" / "cache-verdicts.py"), "run", "--",
           sys.executable, str(scan), "--cibles"] + cibles
    t0 = time.perf_counter()
    r1 = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=300)
    d1 = time.perf_counter() - t0
    check("S5", "scan jetons réel rc=0 (figé)", r1.returncode == 0, f"rc={r1.returncode}")
    t1 = time.perf_counter()
    r2 = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=300)
    d2 = time.perf_counter() - t1
    check("S5", "rejeu du scan rc figé = 0", r2.returncode == 0)
    check("S5", "rejeu marqué REJEU SANS RÉ-APPEL", "REJEU SANS RÉ-APPEL" in r2.stderr)
    gain = d1 / d2 if d2 > 0 else float("inf")
    check("S5", f"gain ≥ 10× (réel {d1:.2f} s → rejeu {d2:.3f} s)", gain >= 10, f"{gain:.0f}×")
    resultats.setdefault("mesures", {})["s5_scan"] = {"reel_s": round(d1, 2), "rejeu_s": round(d2, 3), "gain": round(gain)}
    import shutil as _sh
    _sh.rmtree(tmp, ignore_errors=True)


def section_s6() -> None:
    print("S6 — cohérence écosystème")
    for base, tag in ((HOST, "hôte"), (REPO, "dépôt")):
        kb = lire(base / "skills" / "KNOWLEDGE.md")
        check("S6", f"KB entrée correct-work v2.12.2 ({tag})", "## correct-work v2.12.2" in kb)
        check("S6", f"KB entrée clone-chat v2.2.0 ({tag})", "## clone-chat v2.2.0" in kb)
        arb = lire(base / "scripts" / "check-ecosysteme-integrity.py")
        check("S6", f"invariants ECO_SKILLS ×2 ({tag})",
              '"correct-work": "2.12.2"' in arb and '"clone-chat": "2.2.0"' in arb)
        pm_n = base / "skills" / "@mon-ecosysteme" / "PROMPT-MAITRE-CORRECT-WORK-v2.12.2.md"
        pm_a = base / "skills" / "@historique" / "prompts-maitres" / "correct-work" / "PROMPT-MAITRE-CORRECT-WORK-v2.12.1.md"
        check("S6", f"PM v2.12.2 présent + v2.12.1 archivé R4 ({tag})", pm_n.is_file() and pm_a.is_file())
    for rel in ("skills/correct-work/SKILL.md", "skills/clone-chat/SKILL.md",
                "skills/KNOWLEDGE.md", "scripts/check-ecosysteme-integrity.py",
                "skills/correct-work/scripts/verify-correct-work.py",
                "skills/@mon-ecosysteme/PROMPT-MAITRE-CORRECT-WORK-v2.12.2.md"):
        check("S6", f"parité SHA hôte/dépôt {rel.split('/')[-1]}", sha(HOST / rel) == sha(REPO / rel))


def main() -> int:
    for s in (section_s1, section_s2, section_s3, section_s4, section_s5, section_s6):
        s()
    ok = sum(1 for sec in resultats["sections"].values() for c in sec if c["verdict"] == "PASS")
    fails = [(s, c["check"]) for s, lst in resultats["sections"].items() for c in lst if c["verdict"] == "FAIL"]
    resultats["ok"] = ok
    print(f"\nBATTERIE $FACON2 TASK 19 : {ok}/{resultats['total']} PASS")
    for s, n in fails:
        print(f"  FAIL {s} — {n}")
    RAPPORT.write_text(json.dumps(resultats, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())
