#!/usr/bin/env python3
"""Task 10 G6 — correct-work (projet) : vérification mécanique de clôture du projet de conversion.

P01 fiche KPS livrée : 2 pages A4 paysage, métadonnées scellées
P02 résumé illustré livré : 8 pages, métadonnées scellées, 0 U+FFFD, 0 placeholder
P03 folios du sommaire conformes à la réalité du rendu (5 repères de titres)
P04 audit mise-en-page M3 : verdict PASS consigné (audit-m3.json)
P05 correct-work bloc conversion : 10/10 PASS consigné (cw-task10-conversion-report.json)
P06 garde du standard non-KPS : copie byte-identique + original intact
P07 extraction structurée : complète (7 pièces, 5 opérations, 4 révisions, audit source 40 %)
P08 inventaire des livrables du résumé : chaque chemin cité existe réellement
P09 livrable HTML source + images livrés avec le PDF (chemins réécrits vérifiés)
P10 KO-L009 : aucun secret (ghp_/github_pat_/AKIA) dans les textes livrés

Sortie : scripts/cw-task10-projet-report.json
"""
import hashlib
import json
import os
import re
import sys

BASE = "/home/z/my-project"
DL = f"{BASE}/download"
resultats = []

def check(pid, nom, ok, detail=""):
    resultats.append({"id": pid, "controle": nom, "verdict": "PASS" if ok else "FAIL", "detail": detail})
    print(f"[{'PASS' if ok else 'FAIL'}] {pid} — {nom} {detail}")

import fitz
fic = fitz.open(f"{DL}/fiche-kps-standardized-work-TA-S-3055-020.pdf")
w_mm = round(fic[0].rect.width / 72 * 25.4); h_mm = round(fic[0].rect.height / 72 * 25.4)
check("P01", "fiche KPS livrée (2 p. A4 paysage, scellée)",
      fic.page_count == 2 and w_mm == 297 and h_mm == 210
      and bool(fic.metadata.get("title")) and bool(fic.metadata.get("author")),
      f"(author={fic.metadata.get('author')!r})")

res = fitz.open(f"{DL}/resume-conversion-kps-bluetech.pdf")
txt_res = "".join(p.get_text() for p in res)
bad = [m for m in ["\ufffd", "TODO", "XXX", "undefined", "NaN", "待补充"] if m in txt_res]
check("P02", "résumé illustré livré (8 p., scellé, propre)",
      res.page_count == 8 and bool(res.metadata.get("author")) and not bad,
      f"(author={res.metadata.get('author')!r})")

repères = {2: "Objet et matériau", 3: "Ce que dit le standard", 4: "La cible : la fiche KPS",
           5: "La conversion, donnée par donnée", 6: "Contrôles et traçabilité"}
folio_ok = all(t in res[p - 1].get_text() for p, t in repères.items())
check("P03", "folios du sommaire conformes au rendu réel", folio_ok, "(5 repères)")

m3 = json.load(open(f"{BASE}/assets_tmp/task10/audit-m3.json", encoding="utf-8"))
check("P04", "audit mise-en-page M3 = PASS", m3.get("verdict") == "PASS",
      f"(titres sans keepNext: {m3.get('mesures', {}).get('titres_sans_keepnext', 'n/a')})")

cw = json.load(open(f"{BASE}/scripts/cw-task10-conversion-report.json", encoding="utf-8"))
n_pass = sum(1 for c in cw["controles"] if c["verdict"] == "PASS")
check("P05", "correct-work bloc conversion consigné 10/10", cw["verdict"] == "PASS" and n_pass == 10,
      f"({n_pass}/10)")

sha_up = hashlib.sha256(open(f"{BASE}/upload/IMG_20261127_131943.jpg", "rb").read()).hexdigest()
sha_ar = hashlib.sha256(open(f"{DL}/source-standard-non-KPS-MO-MF-013-F.jpg", "rb").read()).hexdigest()
check("P06", "garde du standard non-KPS byte-identique", sha_up == sha_ar, f"(sha256 {sha_ar[:16]}…)")

ex = json.load(open(f"{DL}/extraction-standard-non-KPS-MO-MF-013-F.json", encoding="utf-8"))
check("P07", "extraction structurée complète",
      len(ex["nomenclature"]) == 7 and len(ex["operations"]) == 5 and len(ex["revisions"]) == 4
      and ex["audit_kps_source_C1_C10"]["score_source_pourcent"] == 40, "")

inventaire = [
    f"{DL}/fiche-kps-standardized-work-TA-S-3055-020.pdf",
    f"{DL}/extraction-standard-non-KPS-MO-MF-013-F.json",
    f"{DL}/source-standard-non-KPS-MO-MF-013-F.jpg",
    f"{DL}/resume-conversion-kps-bluetech.pdf",
    f"{DL}/rapport-cw-task10-conversion.md",
    f"{BASE}/assets_tmp/task10-crops/photo1-valve-bolt.png",
    f"{BASE}/assets_tmp/task10-crops/cartouche-source.png",
]
manquants = [p for p in inventaire if not os.path.exists(p)]
check("P08", "inventaire des livrables cités : tout existe", not manquants,
      f"(manquants: {manquants or 'aucun'})")

html_livre = open(f"{DL}/resume-conversion-kps-bluetech.html", encoding="utf-8").read()
imgs_ok = ('src="assets-resume-task10/' in html_livre
           and os.path.exists(f"{DL}/assets-resume-task10/page1-thumb.jpg")
           and os.path.exists(f"{DL}/assets-resume-task10/source-full.jpg"))
check("P09", "source HTML + images livrées (chemins réécrits)", imgs_ok, "")

secrets = re.findall(r"ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[A-Z0-9]{16}",
                     txt_res + html_livre)
check("P10", "KO-L009 : aucun secret dans les livrables", not secrets, f"({len(secrets)} motif(s))")

n_fail = sum(1 for r in resultats if r["verdict"] == "FAIL")
verdict = "PASS" if n_fail == 0 else "FAIL"
rapport = {"date": "2026-11-27", "task": "10", "bloc": "projet (clôture)",
           "correct_work_version": "2.12.1", "controles": resultats,
           "resume": f"{len(resultats) - n_fail}/{len(resultats)} PASS", "verdict": verdict}
with open(f"{BASE}/scripts/cw-task10-projet-report.json", "w", encoding="utf-8") as f:
    json.dump(rapport, f, ensure_ascii=False, indent=2)
print(f"\nVERDICT CORRECT-WORK (PROJET) : {verdict} ({len(resultats) - n_fail}/{len(resultats)} PASS)")
sys.exit(0 if verdict == "PASS" else 1)
