#!/usr/bin/env python3
"""R5 — Mesure d'économie de jetons (Task 36, vague 2).
Tableau de bord de campagne : consolide les tags #token des plans download/
(estimate par plan) + alerte sur dérive (plan sans estimation, seuils
recalibration §2.3 gen-plan : 0-20 % rien, 20-35 % ajustement, >35 % recalib).
Idempotent, sortie JSON.
"""
import glob, json, os, re, sys, time

OUT = "/home/z/my-project/ecosystem/tmp/r5-token-dashboard.json"

def main():
    plans = {}
    for p in sorted(glob.glob("/home/z/my-project/download/plan-*.md")):
        with open(p, encoding="utf-8", errors="replace") as f:
            txt = f.read()
        tags = re.findall(r"#token\s*~?(\d{2,6})", txt)
        plans[os.path.basename(p)] = {
            "estimation_token": sum(int(t) for t in tags) if tags else None,
            "tags": len(tags),
            "statut": "estimé" if tags else "DRIFT — aucune estimation #token",
        }
    sans_tag = [k for k, v in plans.items() if v["estimation_token"] is None]
    total = sum(v["estimation_token"] for v in plans.values() if v["estimation_token"])
    out = {
        "regle": "R5 — compteur par appel consolidé en tableau de bord de campagne ; alerte sur dérive ; seuils recalibration §2.3 (0-20 % rien / 20-35 % ajustement / >35 % recalibration)",
        "ts": time.strftime("%Y-%m-%d %H:%M:%S"),
        "plans_suivis": len(plans),
        "total_estime_token": total,
        "plans_sans_estimation": sans_tag,
        "alerte_derive": f"{len(sans_tag)} plan(s) sans tag #token (convention : toute phase consigne son estimation)",
        "par_plan": plans,
        "note_honnetete": "compteur d'usage réel par appel LLM non exposé par la plateforme en session — le dashboard consolide les ESTIMATIONS consignées (niveau preuve : consigne, pas consommation mesurée)",
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"R5 : {len(plans)} plans suivis, total estimé {total} #token, "
          f"dérive : {len(sans_tag)} plan(s) sans estimation")
    return 0

if __name__ == "__main__":
    sys.exit(main())
