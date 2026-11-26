#!/usr/bin/env python3
"""add-template-pdf — exécutant canonique du skill homonyme (v1.0.1).

Ajoute un template PDF aux skills PDF : création du squelette 9 blocs
(conforme au format blue-tech), installation au skill `pdf`
(skills/pdf/templates/<nom>/ — dépôt ET profil), inscription au registre
écosystème templates/registry.json (jamais `default` sans --default).

Idempotent ×2 (re-exécution = NO-OP). Stdlib uniquement. Portabilité L008 :
chemins dérivés de __file__ avec repli documenté.

v1.0.1 (Task 13, 2026-11-26, web-f68de5ac — correctif journal-fails #15) :
valider_template supporte les DEUX formats de template (squelette : colors dict /
page width_mm / typography.body ; riche blue-tech : colors liste de tokens nommés /
page « 210mm 297mm » / typography.fonts / sections « part-divider ») ;
réinstallation registre généralisée (tout template inscrit non installé — README
copié depuis la source de vérité) ; idempotence registre par CONTENU (entrée
existante + contenu identique → NO-OP, « created » n'est plus comparé) ;
parité profil resynchronisée même sur verdict NO-OP.
"""
import argparse
import hashlib
import json
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
NOM_OK = re.compile(r"^[a-z][a-z0-9-]{2,30}$")

PALETTES = {
    "slate": {"fond": "#111827", "surface": "#1f2937", "accent": "#38bdf8",
              "accent_secondaire": "#a5b4fc", "texte": "#f8fafc", "muted": "#94a3b8"},
}

COMPONENTS = ["cover", "toc", "part-divider", "main-content", "codeblock",
              "callout", "stat-card", "checklist", "table", "ending"]

BLOCS = ["meta", "page", "design_tokens", "typography", "components",
         "sections", "fields", "validations", "generation"]


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def resolve_repos() -> tuple:
    """Dépôt écosystème (templates/registry.json + skills/pdf) et profil."""
    here = Path(__file__).resolve()
    depot = None
    for parent in here.parents:
        if (parent / "templates" / "registry.json").exists() and (parent / "skills" / "pdf").exists():
            depot = parent
            break
    if depot is None:
        candidat = Path("/home/z/my-project/ecosysteme/KNOWLEDGE")
        if (candidat / "templates" / "registry.json").exists():
            depot = candidat
    if depot is None:
        raise SystemExit("ECHEC — dépôt écosystème introuvable (templates/registry.json)")
    # profil : racine contenant skills/pdf/ distinct du dépôt
    profil = Path("/home/z/my-project")
    if not (profil / "skills" / "pdf").exists():
        profil = None
    return depot, profil


def squelette(nom: str, palette: dict) -> dict:
    """Template standard 9 blocs (format blue-tech)."""
    aujourdhui = datetime.now().strftime("%Y-%m-%d")
    return {
        "meta": {
            "name": nom, "version": "1.0.0", "standard": f"{nom} v1",
            "page_format": "A4 portrait", "language": "fr",
            "source": "add-template-pdf (skill écosystème)", "created": aujourdhui,
        },
        "page": {"format": "A4", "width_mm": 210, "height_mm": 297,
                 "background": palette["fond"], "margins_mm": {"top": 0, "right": 0, "bottom": 48, "left": 0},
                 "footer": {"style": "tamponné", "reserve_basse_px": 48}},
        "design_tokens": {
            "colors": {"background": palette["fond"], "surface": palette["surface"],
                       "accent": palette["accent"], "accent-2": palette["accent_secondaire"],
                       "text": palette["texte"], "muted": palette["muted"]},
            "rule": "palette sombre exclusive — aucun fond clair dans le rendu",
        },
        "typography": {
            "body": {"family": "Inter", "weights": [300, 400, 500, 600, 700, 800, 900]},
            "code": {"family": "JetBrains Mono", "weights": [400, 700]},
        },
        "components": [
            {"id": c, "purpose": f"composant {c} du standard blue-tech",
             "fields": [], "css_contract": "classes .{c} — tokens de design_tokens uniquement"}
            for c in COMPONENTS
        ],
        "sections": {"order": ["cover", "toc", "part", "ending"],
                     "breaks": "page-break avant chaque part-divider et ending"},
        "fields": ["{{document_title}}", "{{document_subtitle}}", "{{date}}", "{{sections}}"],
        "validations": [
            {"id": "V1", "rule": "JSON parseable — 9 blocs présents", "severity": "S1", "method": "add_template_pdf.py"},
            {"id": "V2", "rule": "palette sombre exclusive (aucun fond clair)", "severity": "S1", "method": "design_tokens.colors"},
            {"id": "V3", "rule": "polices déclarées (body + code)", "severity": "S2", "method": "typography"},
            {"id": "V4", "rule": "@page A4 210mm×297mm", "severity": "S1", "method": "page"},
            {"id": "V5", "rule": "ordre des sections conforme (cover → toc → parts → ending)", "severity": "S1", "method": "sections.order"},
            {"id": "V6", "rule": "champs {{...}} instanciables — aucun placeholder résiduel au rendu", "severity": "S2", "method": "validate_doc.py"},
        ],
        "generation": {
            "pipeline": ["validate", "rendu Paged.js (2 passes si sommaire paginé)",
                         "tampon pieds de page", "arbitres (pdf_qa + validate_doc)",
                         "inspection visuelle (pdftoppm 60dpi)"],
            "dependencies": ["node+pagedjs", "PyMuPDF", "pypdf", "reportlab", "Chromium"],
        },
    }


def readme(nom: str, palette: dict) -> str:
    return (
        f"# Template « {nom} » — ajouté par le skill add-template-pdf\n\n"
        f"**Version** 1.0.0 · **Standard** : format blue-tech v1 (9 blocs) · **Format** : A4 portrait · **Statut registre** : standard\n\n"
        f"- **Palette** : " + ", ".join(f"`{k} {v}`" for k, v in palette.items()) + "\n"
        f"- **Polices** : Inter (300-900) + JetBrains Mono\n"
        f"- **Composants** : " + ", ".join(COMPONENTS) + "\n"
        f"- **Usage** : instancier les champs `{{{{...}}}}` du bloc `fields`, suivre `generation.pipeline` ; validations V1-V6 mécaniques.\n"
        f"- **Routage** : installé au skill `pdf` (`skills/pdf/templates/{nom}/`), inscrit au registre écosystème `templates/registry.json`.\n"
    )


def valider_template(t: dict, nom: str) -> list:
    """v1.0.1 : tolérant aux deux formats — squelette (dict) ET riche (blue-tech)."""
    errs = []
    if list(t.keys()) != BLOCS and set(t.keys()) != set(BLOCS):
        errs.append(f"blocs {list(t.keys())} ≠ 9 blocs standard")
    if t.get("meta", {}).get("name") != nom:
        errs.append("meta.name ≠ nom demandé")
    if not SEMVER.match(str(t.get("meta", {}).get("version", ""))):
        errs.append("meta.version non-semver")
    cols = t.get("design_tokens", {}).get("colors", {})
    claires = {"#fff", "#ffffff", "#f8fafc", "#f1f5f9", "#e2e8f0"}
    if isinstance(cols, dict):
        # format squelette : {background, surface, accent, ...}
        if any(v.lower() in claires for k, v in cols.items() if k in ("background", "surface")):
            errs.append("fond clair détecté (palette sombre exigée)")
        if "background" not in cols:
            errs.append("design_tokens.colors.background absent")
    elif isinstance(cols, list):
        # format riche blue-tech : liste de tokens nommés {name, hex, role}
        fonds = [c for c in cols if isinstance(c, dict)
                 and ("fond" in str(c.get("role", "")).lower()
                      or str(c.get("name", "")).lower() in ("background", "fond", "dark"))]
        if not fonds:
            errs.append("design_tokens.colors : aucun token de fond déclaré")
        elif any(str(c.get("hex", "")).lower() in claires for c in fonds):
            errs.append("fond clair détecté (palette sombre exigée)")
    else:
        errs.append("design_tokens.colors : format non reconnu (dict ou liste attendus)")
    if not (t.get("typography", {}).get("body") or t.get("typography", {}).get("fonts")):
        errs.append("typography : ni body (squelette) ni fonts (riche) déclarés")
    page = t.get("page", {})
    a4_ok = (page.get("width_mm") == 210 and page.get("height_mm") == 297) or \
        ("210mm" in str(page.get("size", "")) and "297mm" in str(page.get("size", "")))
    if not a4_ok:
        errs.append("page ≠ A4 210×297")
    ordre = [str(o) for o in t.get("sections", {}).get("order", [])]
    if len(ordre) < 3 or not all(o.startswith(p) for o, p in zip(ordre[:3], ["cover", "toc", "part"])):
        errs.append("ordre de sections non conforme")
    return errs


def main() -> int:
    ap = argparse.ArgumentParser(prog="add-template-pdf")
    ap.add_argument("--name", help="nom du template (kebab-case)")
    ap.add_argument("--palette", default="slate", choices=sorted(PALETTES))
    ap.add_argument("--palette-json", help="fichier de palette personnalisée")
    ap.add_argument("--dry-run", action="store_true", help="rapport sans écriture")
    ap.add_argument("--json", action="store_true", dest="as_json")
    ap.add_argument("--force", action="store_true", help="écraser un template divergent existant")
    ap.add_argument("--default", action="store_true", help="réassigner le modèle default du registre")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        ok = []
        ok.append(("garde nom valide", bool(NOM_OK.match("slate"))))
        ok.append(("garde nom invalide refusé", not bool(NOM_OK.match("Slate!"))))
        ok.append(("garde nom trop court refusé", not bool(NOM_OK.match("ab"))))
        s = squelette("demo", PALETTES["slate"])
        ok.append(("squelette 9 blocs", set(s.keys()) == set(BLOCS)))
        ok.append(("squelette valide", valider_template(s, "demo") == []))
        r = {"name": "x", "templates": [], "default": "blue-tech"}
        ok.append(("registre minimal parsable", isinstance(r.get("templates"), list)))
        for label, v in ok:
            print(("PASS" if v else "FAIL"), label)
        return 0 if all(v for _, v in ok) else 1

    if not args.selftest and not args.name:
        ap.error("--name est requis (sauf --selftest)")

    nom = args.name.strip().lower() if args.name else ""
    rapport = {"name": nom, "actions": [], "validations": [], "warnings": []}

    if not NOM_OK.match(nom):
        rapport["validations"].append(f"REFUS — nom non conforme kebab-case ^[a-z][a-z0-9-]{{2,30}}$ : « {args.name} »")
        if args.as_json:
            print(json.dumps(rapport, ensure_ascii=False, indent=1))
        return 2

    depot, profil = resolve_repos()
    palette = PALETTES.get(args.palette, PALETTES["slate"])
    if args.palette_json:
        palette = json.loads(Path(args.palette_json).read_text(encoding="utf-8"))

    reg_path = depot / "templates" / "registry.json"
    registre = json.loads(reg_path.read_text(encoding="utf-8"))
    entrees = {t["name"]: t for t in registre.get("templates", [])}

    dest_depot = depot / "skills" / "pdf" / "templates" / nom
    tpl_path_depot = dest_depot / f"{nom}.template.json"

    src_readme = None
    if nom in entrees:
        p_src = depot / str(entrees[nom].get("path", ""))
        if p_src.is_file():
            cand = p_src.parent / "README.md"
            if cand.is_file():
                src_readme = cand
    if nom in entrees and not tpl_path_depot.exists() and src_readme is not None:
        # réinstallation depuis la source de vérité du registre (v1.0.1 : tout
        # template inscrit et non installé — ex. blue-tech depuis templates/<nom>/)
        src = depot / str(entrees[nom]["path"])
        rapport["actions"].append(f"réinstallation registre → {src}")
        if not args.dry_run:
            dest_depot.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, tpl_path_depot)
        tpl_bytes = src.read_bytes()
    elif nom in entrees and tpl_path_depot.exists():
        tpl_bytes = tpl_path_depot.read_bytes()
    else:
        tpl = squelette(nom, palette)
        rapport["validations"].extend(valider_template(tpl, nom))
        if rapport["validations"]:
            rapport["verdict"] = "FAIL"
            if args.as_json:
                print(json.dumps(rapport, ensure_ascii=False, indent=1))
            return 1
        tpl_bytes = json.dumps(tpl, ensure_ascii=False, indent=2).encode("utf-8") + b"\n"

    # idempotence (v1.0.1) : fichiers identiques + entrée registre cohérente par
    # CONTENU → NO-OP (« created » n'est plus comparé — une entrée existante dont
    # le path désigne un fichier de même contenu est conservée, R4)
    no_op = tpl_path_depot.exists() and sha256(tpl_path_depot) == hashlib.sha256(tpl_bytes).hexdigest()
    entree_attendue = {
        "name": nom, "version": "1.0.0", "status": "default" if args.default else "standard",
        "path": f"skills/pdf/templates/{nom}/{nom}.template.json",
        "documentation": f"skills/pdf/templates/{nom}/README.md",
        "standard": f"{nom} v1", "page_format": "A4 portrait",
        "source": "add-template-pdf", "created": datetime.now().strftime("%Y-%m-%d"),
    }
    src_entree_ok = False
    if nom in entrees and tpl_bytes:
        p_src = depot / str(entrees[nom].get("path", ""))
        try:
            src_entree_ok = p_src.is_file() and sha256(p_src) == hashlib.sha256(tpl_bytes).hexdigest()
        except OSError:
            src_entree_ok = False
    entree_ok = False
    if nom in entrees:
        entree_ok = src_entree_ok or all(
            entrees[nom].get(k) == v for k, v in entree_attendue.items() if k in entrees[nom])

    if no_op and entree_ok:
        # v1.0.1 : auto-réparation — README dépôt + parité profil, même sur NO-OP
        resyncs = []
        rd_depot = dest_depot / "README.md"
        if src_readme is not None and (not rd_depot.exists() or sha256(rd_depot) != sha256(src_readme)):
            shutil.copy2(src_readme, rd_depot)
            resyncs.append("README dépôt resynchronisé (source de vérité)")
        if profil:
            dest_profil = profil / "skills" / "pdf" / "templates" / nom
            tpl_profil = dest_profil / f"{nom}.template.json"
            rd_profil = dest_profil / "README.md"
            if (not tpl_profil.exists() or sha256(tpl_profil) != sha256(tpl_path_depot)
                    or not rd_profil.exists() or sha256(rd_profil) != sha256(rd_depot)):
                dest_profil.mkdir(parents=True, exist_ok=True)
                shutil.copy2(tpl_path_depot, tpl_profil)
                shutil.copy2(rd_depot, rd_profil)
                resyncs.append(f"parité profil resynchronisée : {dest_profil}")
        if resyncs:
            rapport["actions"] += resyncs
            rapport["verdict"] = "PASS"
            rapport["validations"].append("dépôt + registre déjà cohérents (idempotence) — " + " · ".join(resyncs))
            if args.as_json:
                print(json.dumps(rapport, ensure_ascii=False, indent=1))
            else:
                for a in rapport["actions"]:
                    print("  •", a)
                print("VERDICT : PASS —", rapport["validations"][-1])
            return 0
        rapport["verdict"] = "NO-OP (déjà installé et inscrit — idempotence)"
        if args.as_json:
            print(json.dumps(rapport, ensure_ascii=False, indent=1))
        else:
            print(f"NO-OP — « {nom} » déjà installé et inscrit au registre (idempotence)")
        return 0

    if args.dry_run:
        rapport["verdict"] = "DRY-RUN — aucune écriture"
        action_registre = ("registre : NO-OP (entrée déjà cohérente par contenu — conservée)"
                           if (nom in entrees and src_entree_ok)
                           else f"inscrirait registre {reg_path} (status={entree_attendue['status']})")
        rapport["actions"] += [f"écrirait {tpl_path_depot}",
                               f"écrirait {dest_depot}/README.md",
                               action_registre]
        if args.as_json:
            print(json.dumps(rapport, ensure_ascii=False, indent=1))
        else:
            print(json.dumps(rapport["actions"], ensure_ascii=False, indent=1))
        return 0

    # — écritures —
    dest_depot.mkdir(parents=True, exist_ok=True)
    tpl_path_depot.write_bytes(tpl_bytes)
    rapport["actions"].append(f"template écrit : {tpl_path_depot}")
    if src_readme is not None and str(src_readme) != str(dest_depot / "README.md"):
        shutil.copy2(src_readme, dest_depot / "README.md")
        rapport["actions"].append("README copié depuis la source de vérité du registre")
    else:
        (dest_depot / "README.md").write_text(readme(nom, palette), encoding="utf-8")
        rapport["actions"].append("README écrit")

    # registre (v1.0.1 : entrée existante cohérente par contenu → NO-OP R4,
    # jamais de réécriture silencieuse ; REFUS conservé pour divergence réelle)
    if nom in entrees and src_entree_ok:
        rapport["actions"].append("registre : entrée existante cohérente par contenu — NO-OP (conservée, R4)")
    else:
        if nom in entrees:
            if entrees[nom] != entree_attendue and not args.force:
                diffs = {k: (entrees[nom].get(k), v) for k, v in entree_attendue.items() if entrees[nom].get(k) != v}
                rapport["validations"].append(f"REFUS — entrée registre divergente {diffs} (relancez avec --force)")
                rapport["verdict"] = "FAIL"
                if args.as_json:
                    print(json.dumps(rapport, ensure_ascii=False, indent=1))
                return 1
            entrees[nom].update({k: v for k, v in entree_attendue.items() if k != "created"})
        else:
            registre["templates"].append(entree_attendue)
        if args.default:
            registre["default"] = nom
        registre["updated"] = datetime.now().strftime("%Y-%m-%d")
        reg_path.write_text(json.dumps(registre, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        rapport["actions"].append(f"registre mis à jour : {reg_path} ({len(registre['templates'])} entrées)")

    # installation au profil (skill pdf)
    if profil:
        dest_profil = profil / "skills" / "pdf" / "templates" / nom
        dest_profil.mkdir(parents=True, exist_ok=True)
        shutil.copy2(tpl_path_depot, dest_profil / f"{nom}.template.json")
        shutil.copy2(dest_depot / "README.md", dest_profil / "README.md")
        rapport["actions"].append(f"installé au skill pdf (profil) : {dest_profil}")

    # validation finale mécanique
    t_final = json.loads(tpl_path_depot.read_text(encoding="utf-8"))
    vfin = valider_template(t_final, nom)
    reg_final = json.loads(reg_path.read_text(encoding="utf-8"))
    if reg_final.get("default") != "blue-tech" and not args.default:
        vfin.append("default du registre réassigné sans --default (garde anti-écrasement)")
    if vfin:
        rapport["validations"] += vfin
        rapport["verdict"] = "FAIL"
        if args.as_json:
            print(json.dumps(rapport, ensure_ascii=False, indent=1))
        return 1
    rapport["verdict"] = "PASS"
    rapport["validations"].append("template 9/9 blocs · registre cohérent · default inchangé · parité dépôt écrit")
    if args.as_json:
        print(json.dumps(rapport, ensure_ascii=False, indent=1))
    else:
        for a in rapport["actions"]:
            print("  •", a)
        print("VERDICT : PASS —", rapport["validations"][0])
    return 0


if __name__ == "__main__":
    sys.exit(main())
