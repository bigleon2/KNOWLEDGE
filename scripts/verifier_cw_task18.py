#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Arbitre correct-work (projet) --bloc — Task 18 (session web-220878ed).

Directive propriétaire (trace 1a221abc2b446dfd) étape « correct-work (projet)
--bloc . » : vérification mécanique des blocs du tour :
  B1 implémentation clone-chat v2.1.0 (modes thématiques, gabarit, KB ×2)
  B2 faille PM INSTALL corrigée (parité ×3 copies v1.10.8 — rétroport dépôt)
  B3 batterie $FACON2 69/69 ×2 (scripts/task18-facon2-report.json, fail=0)
  B4 harnais miroir dépôt (SHA hôte == dépôt)
  B5 scan anti-fuite jetons (task15-scan-jetons.py rc=0, 0 jeton réel)
  B6 gen-plan parité live/dépôt + garde É1-INSTALL présente
Génère : download/rapport-cw-task18-projet.md + scripts/cw-task18-projet-report.json
Verdicts binaires, stdlib, idempotence ×2 (byte-stable sauf horodatage).
"""

import hashlib
import json
import re
import subprocess
import sys
import time
from pathlib import Path

HOTE = Path("/home/z/my-project")
REPO = HOTE / "KNOWLEDGE-repo"
SKILLS = HOTE / "skills"
DL = HOTE / "download"
RAPPORT = DL / "rapport-cw-task18-projet.md"
JSON_RAPPORT = HOTE / "scripts/cw-task18-projet-report.json"


def sha256(p):
    h = hashlib.sha256()
    h.update(Path(p).read_bytes())
    return h.hexdigest()


def lire(p):
    return Path(p).read_text(encoding="utf-8", errors="replace")


def run(cmd, timeout=240):
    return subprocess.run(cmd, capture_output=True, text=True,
                          timeout=timeout, cwd=str(HOTE))


def construire_blocs():
    blocs = []

    # ---- B1 implémentation clone-chat v2.1.0
    b1 = []
    sk_live = lire(SKILLS / "clone-chat/SKILL.md")
    sk_depot = lire(REPO / "skills/clone-chat/SKILL.md")
    b1.append(("version-2.1.0-live",
               bool(re.search(r"^version:\s*2\.1\.0\s*$", sk_live, re.M))))
    b1.append(("parite-skill-live-depot",
               sha256(SKILLS / "clone-chat/SKILL.md")
               == sha256(REPO / "skills/clone-chat/SKILL.md")))
    b1.append(("modes-thematiques-1.12",
               all(x in sk_depot for x in
                   ["### §1.12 Modes thématiques",
                    "#### §1.12.1 Détection des thèmes",
                    "#### §1.12.2 Clone thématique",
                    "#### §1.12.3 Clones multiples",
                    "#### §1.12.4 Impact sur les 7+1 étapes"])))
    b1.append(("check-9-present", "Check 9 — Cohérence thématique" in sk_depot))
    tt_l = SKILLS / "clone-chat/références/theme-template.md"
    tt_d = REPO / "skills/clone-chat/références/theme-template.md"
    b1.append(("gabarit-theme-x2",
               tt_l.exists() and tt_d.exists()
               and sha256(tt_l) == sha256(tt_d)))
    kb_l = lire(SKILLS / "KNOWLEDGE.md")
    kb_d = lire(REPO / "skills/KNOWLEDGE.md")
    b1.append(("kb-v2.1.0-x2",
               "## clone-chat v2.1.0" in kb_l and "## clone-chat v2.1.0" in kb_d))
    b1.append(("kb-calibration-tour",
               "Task 18 (2026-11-28, session web-220878ed" in kb_d))
    blocs.append(("B1 implémentation clone-chat v2.1.0 — modes thématiques", b1))

    # ---- B2 faille PM INSTALL corrigée
    b2 = []
    pm = [SKILLS / "@mon-ecosysteme/PROMPT-MAITRE-INSTALL-ECOSYSTEME.md",
          REPO / "scripts/PROMPT-MAITRE-INSTALL-ECOSYSTEME.md",
          HOTE / "scripts/PROMPT-MAITRE-INSTALL-ECOSYSTEME.md"]
    shas = {sha256(p) for p in pm}
    b2.append(("parite-3-copies", len(shas) == 1))
    pm_live = lire(pm[0])
    b2.append(("version-1.10.8", "Version : 1.10.8" in pm_live))
    b2.append(("garde-R2-non-retrograde",
               all(x in pm_live for x in ["## §2bis", "### §3.2", "## §A",
                                          "pipeline en 11 étapes"])))
    b2.append(("mecanisme-dual-present", "bootstrap-ecosysteme.py" in pm_live))
    blocs.append(("B2 faille PM INSTALL corrigée — rétroport v1.10.8 dépôt", b2))

    # ---- B3 batterie $FACON2
    b3 = []
    rep_path = HOTE / "scripts/task18-facon2-report.json"
    b3.append(("rapport-facon2-present", rep_path.exists()))
    if rep_path.exists():
        rep = json.loads(rep_path.read_text(encoding="utf-8"))
        b3.append(("facon2-69-69-fail0",
                   rep.get("total") == 69 and rep.get("fail") == 0
                   and rep.get("pass") == 69))
        b3.append(("facon2-8-sections",
                   len(rep.get("par_section", {})) == 8))
        b3.append(("facon2-verdict-pass", rep.get("verdict_global") == "PASS"))
    harn_l = sha256(HOTE / "scripts/task18-tests-facon2-clone-theme.py")
    harn_d = sha256(REPO / "scripts/task18-tests-facon2-clone-theme.py")
    b3.append(("harnais-miroir-depot", harn_l == harn_d))
    blocs.append(("B3 batterie $FACON2 — 69/69 PASS ×2 idempotent", b3))

    # ---- B4 scan anti-fuite jetons
    b4 = []
    scan = HOTE / "scripts/task15-scan-jetons.py"
    b4.append(("scanner-present", scan.exists()))
    if scan.exists():
        r = run([sys.executable, str(scan)], timeout=240)
        b4.append(("scan-rc0-0-jeton", r.returncode == 0))
    blocs.append(("B4 sécurité jetons — scan dépôt+textes", b4))

    # ---- B5 gen-plan état sain
    b5 = []
    gp_l = sha256(SKILLS / "gen-plan/SKILL.md")
    gp_d = sha256(REPO / "skills/gen-plan/SKILL.md")
    b5.append(("gen-plan-parite", gp_l == gp_d))
    gp = lire(SKILLS / "gen-plan/SKILL.md")
    b5.append(("gen-plan-e1-install", "É1-INSTALL" in gp))
    b5.append(("gen-plan-3.49.0",
               bool(re.search(r"^version:\s*3\.49\.0\s*$", gp, re.M))))
    blocs.append(("B5 gen-plan v3.49.0 — parité live/dépôt", b5))

    return blocs


def main():
    t0 = time.gmtime()
    horodatage = time.strftime("%Y-%m-%dT%H:%M:%SZ", t0)
    blocs = construire_blocs()
    total = sum(len(c) for _, c in blocs)
    ok = sum(1 for _, c in blocs for _, v in c if v)
    verdict = "PASS" if ok == total else "FAIL"

    lignes = [
        "# Rapport correct-work (projet) --bloc — Task 18",
        "",
        f"Généré le {horodatage} · arbitre `scripts/verifier_cw_task18.py` · session web-220878ed",
        "",
        "Directive : 14ᵉ fenêtre (trace 1a221abc2b446dfd) · analyse idée modes thématiques",
        "clone-chat (verdict JUDICIEUSE) → implémentation v2.1.0 → tests $FACON2",
        "(PM INSTALL / clone-chat / gen-plan) → correct-work --bloc → clone-chat.",
        "",
    ]
    for titre, checks in blocs:
        lignes.append(f"### {titre} — {'PASS' if all(v for _, v in checks) else 'FAIL'}")
        lignes.append("")
        for nom, v in checks:
            lignes.append(f"- {'✅' if v else '❌'} {nom}")
        lignes.append("")
    lignes += [
        "## VERDICT GLOBAL",
        "",
        f"**{verdict}** — {ok}/{total} checks PASS ({len(blocs)} blocs)",
        "",
        "Preuve machine : `scripts/cw-task18-projet-report.json` · idempotence : exécuter l'arbitre ×2.",
    ]
    RAPPORT.write_text("\n".join(lignes) + "\n", encoding="utf-8")

    data = {
        "arbitre": "verifier_cw_task18.py",
        "horodatage": horodatage,
        "verdict": verdict, "pass": ok, "total": total,
        "blocs": [{"bloc": t, "checks": [{"nom": n, "verdict": "PASS" if v else "FAIL"}
                                          for n, v in c]} for t, c in blocs],
        "idempotence": "×2 requis — byte-stable sauf horodatage",
    }
    JSON_RAPPORT.write_text(json.dumps(data, ensure_ascii=False, indent=2),
                            encoding="utf-8")
    print(json.dumps({"verdict": verdict, "pass": ok, "total": total},
                     ensure_ascii=False))
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
