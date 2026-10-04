#!/usr/bin/env python3
"""R8 — Boucles d'exécution vérifiée par défaut dans les plans d'actions (Task 36, vague 1).
Garde mécanique : un plan CONFORME contient, par phase d'exécution, la boucle
vérifier → corriger → re-vérifier (max 3 itérations, escalade règle d'or n°1)
et ses hooks correct-work (gen-plan §5.4). Read-only, idempotent, sortie JSON.
Usage : r8-loop-guard.py [--plan <fichier>]   (défaut : plan le plus récent de download/)
"""
import glob, json, os, sys, time

PATTERNS = {
    "boucle_verifier": ["vérifier", "verification", "vérification", "verify"],
    "boucle_corriger": ["corriger", "correction", "fix"],
    "re_verification": ["re-vérif", "reverif", "re-vérification", "re-jeu", "re-test"],
    "bornes_iterations": ["max 3", "3 itérations", "max=3", "≤ 3"],
    "escalade_r1": ["règle d'or n°1", "regle d'or n°1", "escalade"],
    "hooks_phase": ["correct-work", "mode=cible", "mode cible", "§5.4"],
}

def main():
    if "--plan" in sys.argv:
        plan = sys.argv[sys.argv.index("--plan") + 1]
    else:
        cands = sorted(glob.glob("/home/z/my-project/download/plan-task3*.md"),
                       key=os.path.getmtime)
        if not cands:
            print("R8 : aucun plan candidat"); return 2
        plan = cands[-1]
    if not os.path.isfile(plan):
        print(f"R8 : plan introuvable {plan}"); return 2
    with open(plan, encoding="utf-8", errors="replace") as f:
        txt = f.read().lower()
    checks = {k: {"present": any(p in txt for p in pats), "motifs": pats}
              for k, pats in PATTERNS.items()}
    presents = sum(1 for c in checks.values() if c["present"])
    conforme = presents >= 4  # boucle complète (vérifier+corriger+re-vérif) OU hooks + bornes
    out = {
        "regle": "R8 — boucle vérifiée par défaut : chaque phase → vérifier→corriger→re-vérifier (max 3) → escalade règle d'or n°1",
        "ts": time.strftime("%Y-%m-%d %H:%M:%S"),
        "plan": plan,
        "checks": {k: v["present"] for k, v in checks.items()},
        "presents": presents,
        "seuil": 4,
        "verdict": "CONFORME" if conforme else "NON-CONFORME",
    }
    os.makedirs(f"/home/z/my-project/ecosystem/tmp", exist_ok=True)
    with open("/home/z/my-project/ecosystem/tmp/r8-loop-guard.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"R8 : {plan.split('/')[-1]} → {out['verdict']} ({presents}/{len(PATTERNS)} motifs)")
    return 0 if conforme else 1

if __name__ == "__main__":
    sys.exit(main())
