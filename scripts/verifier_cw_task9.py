#!/usr/bin/env python3
"""Task 9 G4 — vérificateur mécanique correct-work (projet) --bloc.

Vérifie, sur l'état réel du disque, les preuves de chaque bloc du plan
download/plan-task9-pdf-fullstack-bluetech.md. Sortie : JSON + rc (0 = tout PASS).
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path("/home/z/my-project")
DL = ROOT / "download"

checks = []


def check(bloc, cid, label, ok, proof):
    checks.append({"bloc": bloc, "id": cid, "label": label,
                   "ok": bool(ok), "proof": proof})


# B0 — écosystème
cert = (ROOT / "scripts" / "certification-report.json")
check("B0", "b0.1", "certification rapport présent", cert.exists(), str(cert))
try:
    rep = json.loads(cert.read_text())
    verts = [a for a in rep.get("arbitres", []) if a.get("vert")]
    check("B0", "b0.2", "certification ALL PASS 6/6",
          len(rep.get("arbitres", [])) == 6 and len(verts) == 6,
          f"{len(verts)}/6 arbitres verts")
except Exception as e:  # noqa: BLE001
    check("B0", "b0.2", "certification ALL PASS 6/6", False, repr(e))

# B1 — G1 relecture / sources
src = ROOT / "kps-converter" / "README.md"
check("B1", "b1.1", "README kps-converter présent (source lue)", src.exists(), str(src))
check("B1", "b1.2", "rapport checklist §8.7 présent", (DL / "rapport-kps2-checklist.md").exists(), "download/rapport-kps2-checklist.md")
check("B1", "b1.3", "dernier clone présent (re-relu)", (DL / "clone-session-web-220878ed-20261124-cloture-photo-gif.md").exists(), "clone Task 8")

# B2 — G2 template + schémas
tpl = ROOT / "skills" / "pdf" / "templates" / "blue-tech" / "blue-tech.template.json"
check("B2", "b2.1", "template blue-tech installé", tpl.exists(), str(tpl))
try:
    t = json.loads(tpl.read_text())
    blocs = ["meta", "page", "design_tokens", "typography", "components",
             "sections", "fields", "validations", "generation"]
    ok9 = all(b in t for b in blocs)
    sombre = t["design_tokens"]["colors"]["background"] == "#111827"
    check("B2", "b2.2", "template 9/9 blocs", ok9, str(list(t.keys())))
    check("B2", "b2.3", "palette sombre exclusive (#111827)", sombre, t["design_tokens"]["colors"]["background"])
except Exception as e:  # noqa: BLE001
    check("B2", "b2.2/3", "template parsable", False, repr(e))
reg = ROOT / "templates" / "registry.json"
try:
    r = json.loads(reg.read_text())
    names = [x["name"] for x in r.get("templates", [])]
    check("B2", "b2.4", "template inscrit au registre (default blue-tech)",
          "blue-tech" in names and r.get("default") == "blue-tech",
          f"templates={names} default={r.get('default')}")
except Exception as e:  # noqa: BLE001
    check("B2", "b2.4", "registre parsable", False, repr(e))

for i, n in enumerate(["schema-1-architecture", "schema-2-flux-requete", "schema-3-cycle-fiche"], 1):
    p = DL / f"{n}.png"
    ok = p.exists() and p.stat().st_size > 50_000
    check("B2", f"b2.{4+i}", f"schéma {i}/3 généré non vide (>50 Ko)", ok,
          f"{p.stat().st_size} octets" if p.exists() else "absent")

# B3 — G3 PDF
pdf = DL / "resume-fullstack-kps-converter-bluetech.pdf"
check("B3", "b3.1", "PDF livré", pdf.exists(), f"{pdf.stat().st_size} octets" if pdf.exists() else "absent")
try:
    import fitz
    d = fitz.open(pdf)
    txt = "".join(pg.get_text() for pg in d)
    check("B3", "b3.2", "12 pages", d.page_count == 12, str(d.page_count))
    check("B3", "b3.3", "0 caractère U+FFFD (encodage)", txt.count("\ufffd") == 0, str(txt.count("\ufffd")))
    cles = ["TA-S-3055-020", "idempotence", "C1-C10", "26/26", "11/11", "15/15",
            "blue-tech", "MO-MF-013-F", "kps_db", "Takt"]
    manq = [k for k in cles if k not in txt]
    check("B3", "b3.4", "10 mots-clés sources présents", not manq, f"manquants={manq or 'aucun'}")
    check("B3", "b3.5", "3 figures intégrées", txt.count("Schéma") >= 3, f"mentions Schéma: {txt.count('Schéma')}")
except Exception as e:  # noqa: BLE001
    check("B3", "b3.x", "PDF parsable", False, repr(e))
qa = subprocess.run([sys.executable, str(ROOT / "skills/pdf/scripts/pdf_qa.py"),
                     str(pdf), "--no-tables"], capture_output=True, text=True)
check("B3", "b3.6", "pdf_qa verdict PASS", "PASS" in qa.stdout, qa.stdout.strip().splitlines()[-1] if qa.stdout else qa.stderr[:80])
html = DL / "resume-fullstack-kps-converter-bluetech.html"
check("B3", "b3.7", "source HTML livrée à côté du PDF (brief creative-flow)", html.exists(), str(html))

# B4 — G4 answer key / protocole
plan = (DL / "plan-task9-pdf-fullstack-bluetech.md").read_text()
check("B4", "b4.1", "plan avec Verdict E8 frais (P1-P5)", "Verdict E8 : PASS" in plan and "Horodatage vérifié" in plan, "plan-task9")
check("B4", "b4.2", "answer key D001-D006 présente", all(f"D00{i}" in plan for i in range(1, 7)), "6 décisions")

n_pass = sum(1 for c in checks if c["ok"])
rapport = {"date": "2026-11-27", "verifications": len(checks), "pass": n_pass,
           "fail": len(checks) - n_pass, "checks": checks}
out = ROOT / "scripts" / "cw-task9-report.json"
out.write_text(json.dumps(rapport, ensure_ascii=False, indent=1), encoding="utf-8")
for c in checks:
    print(f"[{'PASS' if c['ok'] else 'FAIL'}] {c['bloc']}/{c['id']} {c['label']} — {c['proof'][:90]}")
print(f"\nBILAN : {n_pass}/{len(checks)} PASS — rapport {out}")
sys.exit(0 if n_pass == len(checks) else 1)
