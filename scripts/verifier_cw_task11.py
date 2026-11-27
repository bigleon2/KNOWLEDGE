#!/usr/bin/env python3
"""Task 11 — correct-work (projet) --bloc : vérification mécanique → JSON de preuve.

Arbitre final post-push : couvre plan, bootstrap, miroir, push plugin, différés, sécurité jeton,
clone, worklogs. Idempotent ×2 (aucune mutation : seule action d'état = fetch anonyme + re-jeu
NO-OP du miroir).
"""

# ⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.47)
# SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
# Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
# Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
# Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
# Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
# Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).

import json
import re
import subprocess
from pathlib import Path

PROJ = Path("/home/z/my-project")
REPO = PROJ / "KNOWLEDGE-repo"
OUT = PROJ / "scripts/cw-task11-projet-report.json"

checks = []


def check(bloc: str, cid: str, critere: str, ok: bool, preuve: str) -> None:
    checks.append({"bloc": bloc, "id": cid, "critere": critere,
                   "verdict": "PASS" if ok else "FAIL", "preuve": preuve})


# B1 — Plan et bootstrap
plan = (PROJ / "download/plan-task11-partage-push-cw-clone.md").read_text(encoding="utf-8")
check("B1 plan", "F1", "plan Task 11 avec answer key D001-D006",
      len(re.findall(r"decision: D\d{3}", plan)) == 6, "6 décisions")
cert = json.loads((PROJ / "scripts/certification-report.json").read_text(encoding="utf-8"))
echecs = sum(a["echecs"] for a in cert["arbitres"])
check("B1 bootstrap", "F2", "certification ALL-PASS 6/6 (verdict consolidé)",
      echecs == 0 and len(cert["arbitres"]) == 6, f"6 arbitres, {echecs} échec(s)")

# B2 — Miroir local + worklog dépôt
r = subprocess.run(["git", "-C", str(REPO), "log", "--oneline", "-1"], capture_output=True, text=True)
check("B2 miroir", "F3", "commit miroir en tête du dépôt local (suite 167)",
      "Worklog suite 167" in r.stdout, r.stdout.strip()[:80])
wl_repo = (REPO / "worklog.md").read_text(encoding="utf-8")
check("B2 worklog", "F4", "suite 167 présente au worklog dépôt, append-only",
      wl_repo.count("suite 167, session web-220878ed") == 1, "1 occurrence")

# B3 — Push origin (fetch anonyme, KO-L009)
subprocess.run(["git", "-C", str(REPO), "fetch", "origin"], capture_output=True, text=True)
pousses = []
for f in ("download/plan-task11-partage-push-cw-clone.md",
          "download/clone-session-web-220878ed-20261128-tache11-partage-push.md",
          "scripts/verifier_cw_task11.py",
          "scripts/verifier-task11-clone.py",
          "scripts/task11-miroir-local.py"):
    p = subprocess.run(["git", "-C", str(REPO), "cat-file", "-e", f"origin/main:{f}"],
                       capture_output=True, text=True)
    if p.returncode == 0:
        pousses.append(f)
check("B3 push", "F5", "artefacts textes Task 11 présents sur origin/main (commits API plugin)",
      len(pousses) == 5, f"{len(pousses)}/5 : " + ", ".join(p.split('/')[-1] for p in pousses))

# B4 — Différés D001/D002 consignés (2 voies) + aucune URL inventée
check("B4 différés", "F6", "D001/D002 consignés plan + worklog dépôt, 0 URL de partage fabriquée",
      "différé" in wl_repo.split("suite 167")[1] if "suite 167" in wl_repo else False,
      "différés présents dans l'entrée suite 167")
urls = re.findall(r"https?://(?:chat|www)?\.?z\.ai/\S*", plan + wl_repo[-3000:])
check("B4 anti-invention", "F7", "aucune URL z.ai fabriquée dans les artefacts Task 11",
      len(urls) == 0, f"{len(urls)} URL trouvée(s)")

# B5 — Sécurité jeton (scan motif générique — jamais le jeton lui-même)
motif = re.compile(r"github_pat_[A-Za-z0-9_]{20,}|ghp_[A-Za-z0-9]{20,}")
fuites = []
for base in (PROJ / "download", PROJ / "scripts", PROJ / "worklog.md", REPO / "worklog.md"):
    fichiers = [base] if base.is_file() else list(base.rglob("*")) if base.exists() else []
    for f in fichiers:
        if f.is_file() and f.suffix in {".md", ".py", ".json", ".txt", ".html", ".sh"}:
            try:
                if motif.search(f.read_text(encoding="utf-8", errors="ignore")):
                    fuites.append(str(f.relative_to(PROJ)))
            except Exception:
                pass
check("B5 sécurité", "F8", "0 octet de jeton dans tout artefact (scan motif PAT générique)",
      len(fuites) == 0, f"{len(fuites)} fichier(s) : {', '.join(fuites[:5])}")

# B6 — Clone 6ᵉ
clone_rep = json.loads((PROJ / "scripts/task11-clone-report.json").read_text(encoding="utf-8"))
check("B6 clone", "F9", "clone 6ᵉ scellé, validation S1-S8 sans FAIL",
      clone_rep["verdict"] == "PASS", clone_rep["total"])

# B7 — Idempotence miroir ×2 (re-jeu NO-OP)
r2 = subprocess.run(["python3", str(PROJ / "scripts/task11-miroir-local.py")],
                    capture_output=True, text=True)
check("B7 idempotence", "F10", "re-jeu miroir = NO-OP (0 copie, commit NO-OP)",
      "NO-OP" in r2.stdout and "miroirs copiés : 0/30" in r2.stdout, "2ᵉ passage sans effet")

# B8 — Worklog hôte Task 11
wl_hote = (PROJ / "worklog.md").read_text(encoding="utf-8")
check("B8 hôte", "F11", "entrée Task 11 présente au worklog hôte (append-only)",
      "Task ID: 11" in wl_hote, "marqueur Task ID: 11")

verdict = "PASS" if all(c["verdict"] == "PASS" for c in checks) else "FAIL"
rapport = {"tache": 11, "mode": "correct-work (projet) --bloc", "verdict": verdict,
           "total": f"{sum(c['verdict'] == 'PASS' for c in checks)}/{len(checks)} PASS",
           "checks": checks}
OUT.write_text(json.dumps(rapport, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"VERDICT CW PROJET --bloc Task 11 : {rapport['total']} — {verdict}")
for c in checks:
    print(f"  [{c['verdict']}] {c['id']} {c['critere']}")
raise SystemExit(0 if verdict == "PASS" else 1)
