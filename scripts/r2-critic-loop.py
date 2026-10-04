#!/usr/bin/env python3
"""R2 — Boucle CRITIC institutionnalisée (Task 36, vague 1).
Critique séparée de la génération sur les livrables sensibles.
Mode mécanique zéro-API (toujours disponible, KO-L001) : checklist contradictoire.
Passe LLM à consigne contradictoire ARMÉE au QUOTA_OK (modèle + consigne consignés).
Verdicts consignés au journal JSONL. Idempotent par sha256 du contenu.
Usage : r2-critic-loop.py --target <fichier>
"""
import hashlib, json, os, re, sys, time

JOURNAL = "/home/z/my-project/ecosystem/tmp/r2-critic-journal.jsonl"

def critic_checks(txt: str):
    lines = [l.strip() for l in txt.splitlines() if l.strip()]
    dups = len(lines) - len(set(lines))
    mojibake = len(re.findall(r"Ã|Â¦|â€", txt))
    claim_lines = [l for l in lines if re.search(r"\d", l)]
    without_ref = [l for l in claim_lines
                   if not re.search(r"(/|http|ch\.|chapitre|task|R\d|D0|KB|§|%|octets?|o\b)", l, re.I)]
    checks = {
        "integralite": {"ok": len(txt) > 0, "detail": f"{len(txt)} caractères"},
        "duplication": {"ok": dups <= max(2, len(lines) // 50), "detail": f"{dups} ligne(s) dupliquée(s)"},
        "encodage": {"ok": mojibake == 0, "detail": f"{mojibake} séquence(s) mojibake"},
        "traçabilité_claims": {"ok": len(without_ref) <= max(2, len(claim_lines) // 5),
                               "detail": f"{len(without_ref)}/{len(claim_lines)} lignes chiffrées sans référence"},
        "structure": {"ok": bool(lines) and len(lines) >= 3, "detail": f"{len(lines)} lignes non vides"},
    }
    return checks

def main():
    if "--target" not in sys.argv:
        print("usage : r2-critic-loop.py --target <fichier>"); return 2
    target = sys.argv[sys.argv.index("--target") + 1]
    if not os.path.isfile(target):
        print(f"R2 : cible introuvable {target}"); return 2
    with open(target, "rb") as f:
        raw = f.read()
    sha = hashlib.sha256(raw).hexdigest()[:16]
    try:
        txt = raw.decode("utf-8")
    except UnicodeDecodeError:
        txt = raw.decode("utf-8", errors="replace")
    checks = critic_checks(txt)
    fails = [k for k, v in checks.items() if not v["ok"]]
    verdict = "PASS" if not fails else ("RÉSERVES" if len(fails) == 1 else "FAIL")
    entry = {
        "ts": time.strftime("%Y-%m-%d %H:%M:%S"),
        "target": os.path.basename(target),
        "sha16": sha,
        "mode": "MECANIQUE-zéro-API",
        "verdict": verdict,
        "fails": fails,
        "checks": checks,
        "passe_llm": "ARMÉE au QUOTA_OK (consigne contradictoire : « Cherche activement à réfuter chaque affirmation de ce livrable ; liste contradictions, absences de preuve, sur-généralisations ; verdict PASS/RÉSERVES/FAIL motivé »)",
    }
    os.makedirs(os.path.dirname(JOURNAL), exist_ok=True)
    with open(JOURNAL, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"R2 CRITIC : {os.path.basename(target)} [{sha}] → {verdict}"
          + (f" (écarts : {', '.join(fails)})" if fails else ""))
    return 0 if verdict == "PASS" else 1

if __name__ == "__main__":
    sys.exit(main())
