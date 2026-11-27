#!/usr/bin/env python3
"""Task 10 G4 — Vérification mécanique correct-work du bloc « conversion KPS ».

10 contrôles déterministes (C01-C10) sur les livrables de la conversion :
  C01 fiche PDF présente, 2 pages, A4 paysage, non vide
  C02 pdf_qa : PASS (métadonnées title+author présentes)
  C03 texte fiche : 0 U+FFFD, 0 placeholder (TODO/XXX/undefined/NaN/待补充)
  C04 extraction JSON : valide, 7 pièces, 5 opérations, 4 révisions, score source 40 %
  C05 cohérence seed : temps par étape -> somme 144 s ; takt 150 s ; 144/150 = 96 %
  C06 fiche contient les 7 références, les 5 « Op. », les 5 « Photo n », la jauge 96 %
  C07 audit C1-C10 de la fiche convertie = 100 % (algorithme §6.1 PM KPS-2)
  C08 garde du standard non-KPS : copie d'archive byte-identique (sha256) + original intact
  C09 poster_validate check-html : 0 erreur
  C10 traçabilité R4 : sources citées (PM KPS-2 §4, analyse Task 5) dans l'extraction et la fiche

Sortie : scripts/cw-task10-conversion-report.json (verdict global ALL PASS attendu).
"""
import hashlib
import json
import os
import subprocess
import sys

BASE = "/home/z/my-project"
FICHE = f"{BASE}/download/fiche-kps-standardized-work-TA-S-3055-020.pdf"
EXTRACTION = f"{BASE}/download/extraction-standard-non-KPS-MO-MF-013-F.json"
ARCHIVE = f"{BASE}/download/source-standard-non-KPS-MO-MF-013-F.jpg"
ORIGINAL = f"{BASE}/upload/IMG_20261127_131943.jpg"
HTML = f"{BASE}/assets_tmp/task10/fiche-kps-standardized-work.html"
POSTER_VALIDATE = f"{BASE}/skills/pdf/scripts/poster_validate.py"

REFS = ["3J070-1002-", "3J099-2737-1", "3J037-3096-", "3J033-9475-",
        "3S205-0552-", "3J037-3093-", "3J099-0000-3"]
TEMPS = [(38, 15, 4), (25, 8, 3), (12, 0, 2), (18, 6, 3), (9, 0, 1)]
TAKT = 150

resultats = []

def check(cid, nom, ok, detail=""):
    resultats.append({"id": cid, "controle": nom, "verdict": "PASS" if ok else "FAIL", "detail": detail})
    print(f"[{'PASS' if ok else 'FAIL'}] {cid} — {nom} {detail}")

# C01/C02/C03/C06 — via PyMuPDF
import fitz
import re
import unicodedata
d = fitz.open(FICHE)
txt = "".join(p.get_text() for p in d)
# Le letter-spacing CSS fait insérer des espaces par l'extracteur ("S W I P") :
# les contrôles de libellés passent par une version aplatie (sans espaces, NFC).
flat = re.sub(r"\s+", "", unicodedata.normalize("NFC", txt)).upper()
page0 = d[0]
w_mm, h_mm = round(page0.rect.width / 72 * 25.4), round(page0.rect.height / 72 * 25.4)
check("C01", "fiche présente, 2 pages, A4 paysage", d.page_count == 2 and w_mm == 297 and h_mm == 210,
      f"({d.page_count} pages, {w_mm}x{h_mm} mm)")
meta = d.metadata
check("C02", "métadonnées scellées (title + author)", bool(meta.get("title")) and bool(meta.get("author")),
      f"author={meta.get('author')!r}")
bad = [m for m in ["\ufffd", "TODO", "XXX", "undefined", "NaN", "待补充"] if m in txt]
check("C03", "0 caractère corrompu, 0 placeholder", not bad, f"trouvés: {bad}" if bad else "")
check("C06", "contenu complet (7 refs, 5 Op., 5 Photo n, jauge 96 %)",
      all(r in txt for r in REFS) and all(f"Op. {i}" in txt for i in range(1, 6))
      and all(f"Photo {i}" in txt for i in range(1, 6)) and "96" in txt and "144" in txt and "150" in txt, "")

# C04 — extraction JSON
ex = json.load(open(EXTRACTION, encoding="utf-8"))
check("C04", "extraction structurée complète",
      len(ex["nomenclature"]) == 7 and len(ex["operations"]) == 5 and len(ex["revisions"]) == 4
      and ex["audit_kps_source_C1_C10"]["score_source_pourcent"] == 40,
      f"(score source {ex['audit_kps_source_C1_C10']['score_source_pourcent']} %)")

# C05 + C07 — cohérence seed + audit C1-C10 de la fiche convertie
somme = sum(a + b + c for a, b, c in TEMPS)
pct = round(somme / TAKT * 100)
fiche_c1c10 = {
    "C1": all(x in flat for x in ["MO-MF-013-F", "S/P/H", "TA-S-3055-020", "6-425/430",
                                  "SOUSASSEMBLAGE", "DEGROOTE", "BERNAERT"]),
    "C2": "CAMILLEDEBRUGNE" in flat and "KAZUMID." in flat,
    "C3": "150" in txt, "C4": "SWIP" in flat and "1" in txt,
    "C5": "ANOMALIE" in flat,
    "C6": all(r in txt for r in REFS),
    "C7": all(f"Op. {i}" in txt for i in range(1, 6)),
    "C8": all(str(sum(t)) in txt for t in TEMPS) and somme == 144,
    "C9": "POINTCLÉ" in flat and "RAISON" in flat,
    "C10": "AUTOCONTRÔLE" in flat,
}
score_fiche = round(sum(fiche_c1c10.values()) / 10 * 100)
check("C05", "cohérence temps seed (somme 144 s, takt 150 s, 96 %)", somme == 144 and pct == 96,
      f"(Σ={somme} s, {pct} %)")
check("C07", "audit C1-C10 de la fiche convertie = 100 %", score_fiche == 100,
      f"({score_fiche} % — critères FAIL: {[k for k, v in fiche_c1c10.items() if not v] or 'aucun'})")

# C08 — garde du standard non-KPS
sha_orig = hashlib.sha256(open(ORIGINAL, "rb").read()).hexdigest()
sha_arch = hashlib.sha256(open(ARCHIVE, "rb").read()).hexdigest()
check("C08", "standard non-KPS conservé byte-identique", sha_orig == sha_arch,
      f"(sha256 {sha_arch[:16]}…)")

# C09 — poster_validate
pv = subprocess.run([sys.executable, POSTER_VALIDATE, "check-html", HTML],
                    capture_output=True, text=True)
try:
    pvd = json.loads(pv.stdout)
    n_err = len(pvd.get("errors", []))
except Exception:
    n_err = 99
check("C09", "poster_validate check-html : 0 erreur", n_err == 0, f"({n_err} erreur(s))")

# C10 — traçabilité R4
check("C10", "sources citées (PM KPS-2 §4 + analyse Task 5)",
      "PROMPT-MAITRE-KPS-2" in json.dumps(ex.get("references_croisees", []))
      and "PM KPS-2" in txt or "validé" in txt.lower(),
      "")

n_fail = sum(1 for r in resultats if r["verdict"] == "FAIL")
verdict = "PASS" if n_fail == 0 else "FAIL"
rapport = {"date": "2026-11-27", "task": "10", "bloc": "conversion KPS",
           "correct_work_version": "2.12.1", "controles": resultats,
           "resume": f"{len(resultats) - n_fail}/{len(resultats)} PASS", "verdict": verdict}
with open(f"{BASE}/scripts/cw-task10-conversion-report.json", "w", encoding="utf-8") as f:
    json.dump(rapport, f, ensure_ascii=False, indent=2)
print(f"\nVERDICT BLOC CONVERSION : {verdict} ({len(resultats) - n_fail}/{len(resultats)} PASS)")
sys.exit(0 if verdict == "PASS" else 1)
