#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.6.8)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

"""R1 — Couplage systématique spécification-evals (Task 36, vague 1).
Audit mécanique : tout skill de l'écosystème doit naître avec evals/ rempli
(evals.json + trigger_evals.json). Read-only, idempotent, sortie JSON.
Baselines manquantes armées au QUOTA_OK (KO-L001 — aucune sonde API ici).
"""
import glob, json, os, sys, time

BASE = "/home/z/my-project/work_knowledge"
OUT = f"{BASE}/tmp/r1-evals-coverage.json"

def main():
    os.makedirs(f"{BASE}/tmp", exist_ok=True)
    skills = sorted(glob.glob(f"{BASE}/skills/*/SKILL.md"))
    rows, missing = [], []
    for sp in skills:
        name = os.path.basename(os.path.dirname(sp))
        d = os.path.dirname(sp)
        has_e = os.path.isfile(f"{d}/evals/evals.json")
        has_t = os.path.isfile(f"{d}/evals/trigger_evals.json")
        statut = "complet" if (has_e and has_t) else ("partiel" if (has_e or has_t) else "absent")
        if statut != "complet":
            missing.append({"skill": name, "evals.json": has_e, "trigger_evals.json": has_t})
        rows.append({"skill": name, "statut": statut})
    complet = sum(1 for r in rows if r["statut"] == "complet")
    report = {
        "regle": "R1 — tout nouveau skill naît avec son dossier evals/ rempli (couplage spécification-evals)",
        "ts": time.strftime("%Y-%m-%d %H:%M:%S"),
        "skills_total": len(rows),
        "complets": complet,
        "couverture_pct": round(100 * complet / max(len(rows), 1), 1),
        "manquants": missing,
        "baselines_au_quota_ok": [m["skill"] for m in missing],
        "garde": "skill-creator : création d'un skill SANS evals/ = refusée par la convention R1 (KB Task 36 vague 1)",
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"R1 : {complet}/{len(rows)} skills complets ({report['couverture_pct']} %) — "
          f"{len(missing)} manquant(s) — baseline(s) armée(s) au QUOTA_OK")
    return 0

if __name__ == "__main__":
    sys.exit(main())
