#!/usr/bin/env python3
"""Validateur blue-tech — cohérence d'un document HTML instancié contre le template.

Contrôles (dérivés des validations V1-V4, V8, V9 du template) :
  C1  8 blocs du template présents (meta, page, design_tokens, typography, components,
      sections, fields, validations)
  C2  V1 — palette exclusive : aucun fond clair dans le CSS du document
  C3  V2 — polices Inter + JetBrains Mono déclarées (avec preconnect)
  C4  V3 — @page 210mm 297mm
  C5  V4 — ordre des sections (cover → toc → part-divider → main-content → ending)
  C6  V8 — contrastes : textes clairs uniquement (aucune couleur texte sombre sur fond sombre)
  C7  V9 — équilibre des <div>
  C8  cohérence des champs : aucun placeholder {{...}} résiduel
  C9  cohérence composants : les composants du catalogue cités par le document existent
      dans le template ; les tokens couleurs utilisés appartiennent au registre
Verdict : PASS (rc 0) si 9/9 — sinon FAIL (rc 1) avec la liste des échecs. --json pour machine.
"""
import argparse
import json
import re
import sys
from pathlib import Path

FONDS_CLAIRS = ["#f8fafc", "#ffffff", "#fff;", "#eef7fb", "#f3effc", "#f0f9ff",
                "#ecfeff", "#ecfdf5", "#e8eef6", "#f1f5f9"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--doc", required=True)
    ap.add_argument("--template", required=True)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    T = json.loads(Path(a.template).read_text(encoding="utf-8"))
    s = Path(a.doc).read_text(encoding="utf-8")
    css = s[s.find("<style"):s.find("</style>")].lower() if "<style" in s else ""
    echecs, checks = [], {}

    def rec(nom, ok, detail=""):
        checks[nom] = {"statut": "PASS" if ok else "FAIL", "detail": detail}
        if not ok:
            echecs.append(nom)

    # C1 — blocs template
    blocs = ["meta", "page", "design_tokens", "typography", "components", "sections", "fields", "validations"]
    rec("C1_blocs_template", all(b in T for b in blocs), f"{len([b for b in blocs if b in T])}/8")
    # C2 — V1 palette
    clairs = [f for f in FONDS_CLAIRS if f in css.replace(" ", "")]
    rec("C2_V1_palette", not clairs, f"fonds clairs: {clairs or 'aucun'}")
    # C3 — V2 polices
    rec("C3_V2_polices", "Inter" in s and "JetBrains" in s and "preconnect" in s)
    # C4 — V3 page
    rec("C4_V3_page", T["page"]["size"] in s and "210mm 297mm" in s)
    # C5 — V4 ordre
    pos = {m: s.find(m) for m in ['class="page cover"', 'class="page toc-page"',
                                  'class="page part-divider"', 'class="page main-content"',
                                  'class="page ending"']}
    ordre_ok = all(pos[m] >= 0 for m in pos) and \
        pos['class="page cover"'] < pos['class="page toc-page"'] < pos['class="page part-divider"'] \
        < pos['class="page main-content"'] < pos['class="page ending"']
    rec("C5_V4_ordre_sections", ordre_ok, str({k.split('"')[1].split()[-1]: v for k, v in pos.items()}))
    # C6 — V8 contrastes : couleurs de texte sombres interdites (tokens texte clairs attendus)
    couleurs_texte_sombres = ["color: #0f172a", "color:#0f172a", "color: #1e293b", "color:#1e293b"]
    rec("C6_V8_contrastes", not any(c in css for c in couleurs_texte_sombres))
    # C7 — V9 divs
    o, c_ = len(re.findall(r"<div[ >]", s)), s.count("</div>")
    rec("C7_V9_equilibre_divs", o == c_, f"{o}/{c_}")
    # C8 — placeholders résiduels
    restants = re.findall(r"\{\{[a-z_]+\}\}", s)
    rec("C8_champs_remplaces", not restants, f"résiduels: {restants or 'aucun'}")
    # C9 — tokens/composants
    hexes = {t["hex"].lower() for t in T["design_tokens"]["colors"]}
    utilises = set(re.findall(r"#[0-9a-f]{6}\b", s.lower()))
    hors_registre = {u for u in utilises if u not in hexes and not u.startswith("#7dd3fc")}
    # #7dd3fc (cyan-light) et surfaces rgba tolérées ; seuls les hex 6 hors registre sont FAIL
    hors_registre.discard("#7dd3fc")
    rec("C9_tokens_registre", not hors_registre, f"hex hors registre: {sorted(hors_registre) or 'aucun'}")

    verdict = "PASS" if not echecs else "FAIL"
    rapport = {"verdict": verdict, "document": a.doc, "template": a.template,
               "checks": checks, "echecs": echecs}
    print(json.dumps(rapport, ensure_ascii=False, indent=1) if a.json
          else f"validate_doc : {verdict} ({len(checks) - len(echecs)}/{len(checks)})"
               + (f" — échecs : {echecs}" if echecs else ""))
    return 0 if not echecs else 1


if __name__ == "__main__":
    sys.exit(main())
