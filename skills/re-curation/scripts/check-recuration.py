#!/usr/bin/env python3
"""check-recuration.py — Arbitre mécanique d'une re-curation progressive disclosure
(skill re-curation v1.0.0).

Vérifie, sur l'état du disque (KO-L003 — jamais de mémoire de session) :
  C1 pointeurs valides      — chaque `references/<fichier>` cité dans le SKILL.md existe ;
  C2 non-duplication R4      — aucune fenêtre 1024 octets d'un fichier references/
                               dupliquée inline dans le SKILL.md (pas 512) ;
  C3 marqueurs de provenance — les paires <!-- BLOC-DEPLACÉ:clé… --> / FIN-BLOC-DEPLACÉ
                               éventuelles sont bien appariées ;
  C4 seuils de poids         — SKILL.md vs seuils OK < 12 / LOURD >= 30 / CRITIQUE >= 60 Kio.

Usage :
  python3 skills/re-curation/scripts/check-recuration.py <skill>
  python3 skills/re-curation/scripts/check-recuration.py --selftest

Verdict : PASS (rc 0) si 4/4 — sinon FAIL (rc 1). Python stdlib (N3), idempotent
(lecture seule), selftest sait échouer.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

RACINE = Path("/home/z/my-project")


def pointeurs(d: Path, texte: str) -> tuple[bool, list[str]]:
    manquants = [m for m in sorted(set(re.findall(r"references/([A-Za-z0-9_.-]+)", texte)))
                 if not (d / "references" / m).is_file()]
    return (not manquants, manquants)


def duplication(d: Path, sk_b: bytes) -> list[str]:
    ecarts = []
    if not (d / "references").is_dir():
        return ecarts
    for rf in sorted((d / "references").glob("*")):
        if not rf.is_file():
            continue
        rb = rf.read_text(encoding="utf-8").encode("utf-8")
        for i in range(0, max(0, len(rb) - 1024 + 1), 512):
            if rb[i:i + 1024] in sk_b:
                ecarts.append(f"{rf.name}@{i}")
                break
    return ecarts


def marqueurs(texte: str) -> tuple[bool, list[str]]:
    ecarts = []
    ouverts = re.findall(r"<!-- BLOC-DEPLACÉ:([A-Za-z0-9_]+):", texte)
    fermes = re.findall(r"<!-- FIN-BLOC-DEPLACÉ:([A-Za-z0-9_]+)", texte)
    for o in ouverts:
        if ouverts.count(o) != 1 or o not in fermes:
            ecarts.append(f"non apparié : {o}")
    for f in fermes:
        if f not in ouverts:
            ecarts.append(f"fermeture orpheline : {f}")
    return (not ecarts, ecarts)


def verifier(nom: str, racine: Path = RACINE) -> dict:
    d = racine / "skills" / nom
    sk = d / "SKILL.md"
    if not sk.is_file():
        return {"verdict": "ABANDON", "detail": f"skills/{nom}/SKILL.md introuvable"}
    texte = sk.read_text(encoding="utf-8")
    octets = len(texte.encode("utf-8"))
    c1, manq = pointeurs(d, texte)
    dup = duplication(d, texte.encode("utf-8"))
    c2 = not dup
    c3, marc = marqueurs(texte)
    poids = ("OK" if octets < 12 * 1024 else "INTERMÉDIAIRE" if octets < 30 * 1024
             else "LOURD" if octets < 60 * 1024 else "CRITIQUE")
    c4 = octets < 30 * 1024
    checks = {
        "C1_pointeurs": (c1, "tous les references/ cités existent" if c1 else f"manquants : {manq}"),
        "C2_non_duplication": (c2, "aucune fenêtre 1024 o dupliquée" if c2 else f"duplications : {dup}"),
        "C3_marqueurs": (c3, "paires BLOC-DEPLACÉ appariées" if c3 else f"écarts : {marc}"),
        "C4_seuils": (c4, f"{octets} o ({octets/1024:.1f} Kio) — verdict poids {poids}"
                     + ("" if c4 else " — au-dessus du seuil LOURD 30 Kio")),
    }
    fails = [k for k, (ok, _) in checks.items() if not ok]
    return {"verdict": "PASS" if not fails else "FAIL", "skill": nom,
            "octets": octets, "verdict_poids": poids,
            "checks": {k: {"statut": "PASS" if ok else "FAIL", "detail": det}
                       for k, (ok, det) in checks.items()}}


def selftest() -> int:
    import tempfile
    tmp = Path(tempfile.mkdtemp(prefix="check-recuration-selftest-"))
    d = tmp / "skills" / "temoin"
    (d / "references").mkdir(parents=True)
    (d / "references" / "grille.md").write_text("# Grille\n\n" + ("contenu intégral déplacé. " * 200), encoding="utf-8")
    (d / "SKILL.md").write_text(
        "---\nname: temoin\n---\n## §1\n\nRésumé + pointeur `references/grille.md`.\n\n"
        "<!-- BLOC-DEPLACÉ:grille:v1.0.0:abc -->\n\n<!-- FIN-BLOC-DEPLACÉ:grille -->\n",
        encoding="utf-8")
    r = []
    v = verifier("temoin", tmp)
    r.append(("état sain → PASS 4/4", v["verdict"] == "PASS"))
    # pointeur cassé
    (d / "SKILL.md").write_text((d / "SKILL.md").read_text(encoding="utf-8")
                                .replace("references/grille.md", "references/absent.md"), encoding="utf-8")
    v2 = verifier("temoin", tmp)
    r.append(("pointeur cassé → C1 FAIL", v2["checks"]["C1_pointeurs"]["statut"] == "FAIL" and v2["verdict"] == "FAIL"))
    # duplication inline d'une fenêtre du fichier déplacé
    gros = (d / "references" / "grille.md").read_text(encoding="utf-8")[:1100]
    (d / "SKILL.md").write_text("---\nname: temoin\n---\n## §1\n\n" + gros + "\n", encoding="utf-8")
    v3 = verifier("temoin", tmp)
    r.append(("bloc dupliqué inline → C2 FAIL", v3["checks"]["C2_non_duplication"]["statut"] == "FAIL"))
    v4 = verifier("inconnu", tmp)
    r.append(("skill introuvable → ABANDON", v4["verdict"] == "ABANDON"))
    print("=== SELFTEST check-recuration.py ===")
    ok = True
    for label, passe in r:
        print(f"  [{'PASS' if passe else 'FAIL'}] {label}")
        ok = ok and passe
    print(f"SELFTEST : {'PASS' if ok else 'FAIL'} ({sum(1 for _, p in r if p)}/{len(r)})")
    return 0 if ok else 1


def main() -> int:
    p = argparse.ArgumentParser(description="check-recuration.py — arbitre re-curation")
    p.add_argument("skill", nargs="?")
    p.add_argument("--selftest", action="store_true")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    if a.selftest:
        return selftest()
    if not a.skill:
        p.print_usage()
        return 3
    v = verifier(a.skill)
    if a.json:
        print(json.dumps(v, ensure_ascii=False, indent=1))
        return 0 if v["verdict"] == "PASS" else 1
    if v["verdict"] == "ABANDON":
        print(f"ABANDON : {v['detail']}")
        return 2
    print(f"=== Arbitre re-curation — skills/{a.skill} ({v['octets']} o / {v['verdict_poids']}) ===")
    for k, c in v["checks"].items():
        print(f"  [{c['statut']}] {k} — {c['detail']}")
    print(f"VERDICT : {v['verdict']}")
    return 0 if v["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
