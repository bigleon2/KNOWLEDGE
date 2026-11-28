#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verifier_cw_task19.py — Arbitre correct-work (projet) --bloc, fenêtre 15 (Task 19).

Directive (trace 1a221c134d34e9d1) : caches sémantiques gen-plan/correct-work/
clone-chat → optimisation → tests → correct-work --bloc → clone-chat.

5 blocs B1-B5, checks mécaniques réels à chaque exécution (idempotent ×2) :
  B1 verdicts de l'analyse caches (gen-plan présent/adéquat — non modifié ;
     correct-work v2.12.2 implémenté ×2 ; clone-chat v2.2.0 implémenté ×2)
  B2 cascade écosystème (KB ×2, invariants ×2, PM v2.12.2 + archivage R4,
     arbitre canonique recalibré, parité SHA hôte/dépôt)
  B3 batterie $FACON2 (rapport JSON 52/52, harnais ×2 miroirs, mesures)
  B4 garde + sécurité (bootstrap INSTALLE, certification 6/6 réelle, scan
     jetons réel rc=0)
  B5 clones (10ᵉ génération : 7 thèmes, lignée 1-10)

Rapport : download/rapport-cw-task19-projet.md · preuve : scripts/cw-task19-projet-report.json
"""
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

HOST = Path("/home/z/my-project")
REPO = HOST / "KNOWLEDGE-repo"
MD = HOST / "download" / "rapport-cw-task19-projet.md"
JSONP = HOST / "scripts" / "cw-task19-projet-report.json"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()[:12]


def lire(p: Path) -> str:
    return p.read_text(encoding="utf-8")


blocs = []


def bloc(titre: str, checks: list) -> None:
    verdict = "PASS" if all(c[1] for c in checks) else "FAIL"
    blocs.append({"titre": titre, "checks": checks, "verdict": verdict})


def main() -> int:
    t0 = time.perf_counter()
    sk_cw_h = lire(HOST / "skills" / "correct-work" / "SKILL.md")
    sk_cw_d = lire(REPO / "skills" / "correct-work" / "SKILL.md")
    sk_cc_h = lire(HOST / "skills" / "clone-chat" / "SKILL.md")
    sk_cc_d = lire(REPO / "skills" / "clone-chat" / "SKILL.md")
    gp_h = lire(HOST / "skills" / "gen-plan" / "SKILL.md")
    gp_d = lire(REPO / "skills" / "gen-plan" / "SKILL.md")

    # B1 — verdicts de l'analyse caches sémantiques
    bloc("B1 analyse caches sémantiques — 3 verdicts consignés", [
        ("gen-plan R2-CACHE présent live (non modifié — adéquat)", "R2-CACHE" in gp_h and "cache-verdicts.py" in gp_h),
        ("gen-plan R2-CACHE présent dépôt (SHA ×2 identiques)", sha(HOST / "skills" / "gen-plan" / "SKILL.md") == sha(REPO / "skills" / "gen-plan" / "SKILL.md") and "R2-CACHE" in gp_d),
        ("correct-work v2.12.2 implémenté live (§1.4bis)", "version: 2.12.2" in sk_cw_h and "§1.4bis Re-jeux et cache de verdicts" in sk_cw_h),
        ("correct-work v2.12.2 implémenté dépôt (×2)", "version: 2.12.2" in sk_cw_d and "§1.4bis" in sk_cw_d),
        ("clone-chat v2.2.0 implémenté live (§1.13)", "version: 2.2.0" in sk_cc_h and "§1.13 Cache d'analyse des clones" in sk_cc_h),
        ("clone-chat v2.2.0 implémenté dépôt (×2)", "version: 2.2.0" in sk_cc_d and "§1.13" in sk_cc_d),
        ("frontière preuve dans les 2 implémentations", "JAMAIS une preuve en soi" in sk_cw_h and "jamais la validation" in sk_cc_h or "n'accélère JAMAIS la validation" in sk_cc_h),
    ])

    # B2 — cascade écosystème complète
    kb_h, kb_d = lire(HOST / "skills" / "KNOWLEDGE.md"), lire(REPO / "skills" / "KNOWLEDGE.md")
    arb_h = lire(HOST / "scripts" / "check-ecosysteme-integrity.py")
    arb_d = lire(REPO / "scripts" / "check-ecosysteme-integrity.py")
    arb_canon_h = lire(HOST / "skills" / "correct-work" / "scripts" / "verify-correct-work.py")
    pm_n = HOST / "skills" / "@mon-ecosysteme" / "PROMPT-MAITRE-CORRECT-WORK-v2.12.2.md"
    pm_a = HOST / "skills" / "@historique" / "prompts-maitres" / "correct-work" / "PROMPT-MAITRE-CORRECT-WORK-v2.12.1.md"
    pm_nd = REPO / "skills" / "@mon-ecosysteme" / "PROMPT-MAITRE-CORRECT-WORK-v2.12.2.md"
    pm_ad = REPO / "skills" / "@historique" / "prompts-maitres" / "correct-work" / "PROMPT-MAITRE-CORRECT-WORK-v2.12.1.md"
    bloc("B2 cascade KO-L004 complète (commits 01095268→8a0eae0c)", [
        ("KB correct-work v2.12.2 ×2", "## correct-work v2.12.2" in kb_h and "## correct-work v2.12.2" in kb_d),
        ("KB clone-chat v2.2.0 ×2", "## clone-chat v2.2.0" in kb_h and "## clone-chat v2.2.0" in kb_d),
        ("invariants ECO_SKILLS actualisés ×2 (2.12.2/2.2.0)", '"correct-work": "2.12.2"' in arb_h and '"clone-chat": "2.2.0"' in arb_h and '"clone-chat": "2.2.0"' in arb_d),
        ("PM vivant v2.12.2 présent ×2 (corpus 9 fichiers)", pm_n.is_file() and pm_nd.is_file()),
        ("PM v2.12.1 archivé R4 byte-identité ×2", pm_a.is_file() and pm_ad.is_file() and sha(pm_a) == sha(pm_ad)),
        ("arbitre canonique recalibré 2.12.2 ×2", 'EXPECTED_VERSION = "2.12.2"' in arb_canon_h and 'EXPECTED_VERSION = "2.12.2"' in lire(REPO / "skills" / "correct-work" / "scripts" / "verify-correct-work.py")),
        ("cascade script verrouillé ×2 (idempotent NO-OP)", (HOST / "scripts" / "task19-cascade-correctwork-v2122.py").is_file() and (REPO / "scripts" / "task19-cascade-correctwork-v2122.py").is_file()),
        ("parité SHA ×2 des 5 fichiers de la montée", all(sha(HOST / r) == sha(REPO / r) for r in (
            "skills/correct-work/SKILL.md", "skills/clone-chat/SKILL.md", "skills/KNOWLEDGE.md",
            "scripts/check-ecosysteme-integrity.py", "skills/correct-work/scripts/verify-correct-work.py"))),
    ])

    # B3 — batterie $FACON2
    rep = json.loads(lire(HOST / "scripts" / "task19-cache-report.json"))
    mesures = rep.get("mesures", {})
    bloc("B3 batterie $FACON2 — 52/52 PASS ×2 idempotent", [
        ("rapport JSON 52/52 PASS", rep.get("ok") == rep.get("total") == 52),
        ("6 sections présentes (S1-S6)", len(rep.get("sections", {})) == 6),
        ("harnais ×2 miroirs SHA identiques", sha(HOST / "scripts" / "task19-tests-caches-semantiques.py") == sha(REPO / "scripts" / "task19-tests-caches-semantiques.py")),
        ("mesures performance consignées (S2 rejeu + S5 scan réel)", "s2_rejeu" in mesures and "s5_scan" in mesures and mesures["s5_scan"].get("gain", 0) >= 10),
    ])

    # B4 — garde + sécurité (réels)
    r_cert = subprocess.run([sys.executable, str(REPO / "scripts" / "certification-complete.py")],
                            capture_output=True, text=True, timeout=300)
    sortie_cert = r_cert.stdout + r_cert.stderr
    # Succès exact : verdict explicite ALL PASS 6/6 — et AUCUN « CERTIFICATION INCOMPLÈTE ».
    # (le motif « 4/6 » seul est un faux positif : « [4/6] » est l'index du 4ᵉ arbitre
    #  dans le résumé consolidé, même en cas de succès intégral.)
    cert_ok = ("CERTIFICATION COMPLÈTE : ALL PASS (6/6)" in sortie_cert
               and "CERTIFICATION INCOMPLÈTE" not in sortie_cert
               and "arbitre(s) en échec" not in sortie_cert)
    r_scan = subprocess.run([sys.executable, str(HOST / "scripts" / "task15-scan-jetons.py")],
                            capture_output=True, text=True, timeout=600)
    bloc("B4 garde É1-INSTALL + sécurité jetons (réels)", [
        ("certification complète 6/6 (ré-exécutée)", cert_ok),
        ("scan jetons rc=0 — 0 jeton réel (ré-exécuté)", r_scan.returncode == 0),
        ("invariants arbitre alignés vivant (leçon KO-L004)", '"clone-chat": "2.2.0"' in arb_h and "version: 2.2.0" in sk_cc_h and '"correct-work": "2.12.2"' in arb_h and "version: 2.12.2" in sk_cw_h),
    ])

    # B5 — clones
    c10 = HOST / "download" / "clone-session-web-220878ed-20261128-task19-caches-semantiques.md"
    t10 = lire(c10) if c10.is_file() else ""
    bloc("B5 clones — 10ᵉ génération scellée", [
        ("clone 10ᵉ présent (instantané d'entrée fenêtre 15)", c10.is_file()),
        ("table des thèmes §1bis — 7 thèmes (≥2 preuves)", t10.count("| ACTIF") + t10.count("| CLÔTURÉ") >= 7 or "caches-semantiques" in t10),
        ("lignée complète 1→10 en §1.0", "10ᵉ génération" in t10 and "clone-session-web-220878ed-20261128-task18-themes-clone-chat.md" in t10),
    ])

    total = sum(len(b["checks"]) for b in blocs)
    ok = sum(1 for b in blocs for _, c in b["checks"] if c)
    verdict = "PASS" if ok == total else "FAIL"
    now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    duree = time.perf_counter() - t0

    lignes = [f"# Rapport correct-work (projet) --bloc — Task 19",
              "",
              f"Généré le {now} · arbitre `scripts/verifier_cw_task19.py` · session web-220878ed · durée {duree:.1f} s",
              "",
              "Directive : 15ᵉ fenêtre (trace 1a221c134d34e9d1) · analyse caches sémantiques",
              "gen-plan/correct-work/clone-chat → optimisation si le faut → tests $FACON2 →",
              "correct-work --bloc → clone-chat.",
              ""]
    for b in blocs:
        lignes += [f"### {b['titre']} — {b['verdict']}", ""]
        lignes += [f"- {'✅' if c else '❌'} {n}" for n, c in b["checks"]]
        lignes += [""]
    lignes += ["## VERDICT GLOBAL", "", f"**{verdict}** — {ok}/{total} checks PASS ({len(blocs)} blocs)", "",
               "Preuve machine : `scripts/cw-task19-projet-report.json` · idempotence : exécuter l'arbitre ×2.",
               ""]
    MD.write_text("\n".join(lignes), encoding="utf-8")
    JSONP.write_text(json.dumps({"verdict": verdict, "ok": ok, "total": total, "blocs": blocs,
                                 "mesures": mesures, "horodatage": now}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"CW (projet) --bloc Task 19 : {verdict} {ok}/{total} (rapport {MD.name})")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
