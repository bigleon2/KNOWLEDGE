#!/usr/bin/env python3
"""verifier_structure.py — arbitre mécanique de la structure du skill cahier-des-charges v2.0.0.

Skill cahier-des-charges v2.0.0 — scripts/ — stdlib Python uniquement (N3).

Vérifie mécaniquement l'état cible v2.0.0 (validation voie mécanique, SKILL.md §5) :
frontmatter (nom, version), les 7 modes M1-M7, les 12 règles opérationnelles, les 7 dépendances
YAML, les 4 references (v2.0.0), le template (annexes D/T, en-tête domaine/profil), les
livrables et formats Engineering Design (SS-xx, I-xx, TF-xx, TH-xx, [HYP-xx]), les evals
(12 requêtes : 9 positives / 3 négatives, cohérence trigger_evals <-> evals.json) et la
présence/compilation des scripts.

Usage :
    python3 verifier_structure.py [--racine <dossier du skill>] [--json]
    python3 verifier_structure.py --selftest

Sortie : 0 = tous les checks PASS ; 1 = au moins un ECHEC ; 2 = erreur d'exécution.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

VERSION_CIBLE = "2.0.1"
NOM_SKILL = "cahier-des-charges"
DEPENDANCES_ATTENDUES = {"skill-creator", "web-search", "web-reader",
                         "spec-driven-development", "inter-scripts", "pdf",
                         "prompt-engineering"}
REFERENCES_ATTENDUES = ["template-cahier-des-charges.md", "workflow-engineering-design.md",
                        "domaines-techniques.md", "simulation-materielle.md"]
LIVRABLES_V2 = ["fiche-domaine-", "dossier-conception-", "batterie-tests-",
                "rapport-couverture-"]

# ------------------------------------------------------------- utilitaires ---


def lire(racine, relatif):
    chemin = racine / relatif
    if not chemin.is_file():
        return None
    return chemin.read_text(encoding="utf-8")


def frontmatter(texte):
    """Retourne le bloc YAML frontmatter (entre les deux premières lignes ---)."""
    lignes = texte.splitlines()
    if not lignes or lignes[0].strip() != "---":
        return ""
    for i in range(1, len(lignes)):
        if lignes[i].strip() == "---":
            return "\n".join(lignes[1:i])
    return ""


def corps_sans_frontmatter(texte):
    lignes = texte.splitlines()
    if not lignes or lignes[0].strip() != "---":
        return texte
    for i in range(1, len(lignes)):
        if lignes[i].strip() == "---":
            return "\n".join(lignes[i + 1:])
    return texte


# ----------------------------------------------------------------- checks ----

def checker_frontmatter(racine, checks):
    texte = lire(racine, "SKILL.md")
    if texte is None:
        checks.append(("SKILL.md présent", False, "SKILL.md introuvable"))
        return None
    checks.append(("SKILL.md présent", True, "trouvé"))
    fm = frontmatter(texte)
    nom = re.search(r"^name:\s*(\S+)", fm, re.M)
    version = re.search(r"^version:\s*\"?([\d.]+)\"?", fm, re.M)
    checks.append(("frontmatter name", nom is not None and nom.group(1) == NOM_SKILL,
                   f"name={nom.group(1) if nom else 'absent'}"))
    checks.append(("frontmatter version = " + VERSION_CIBLE,
                   version is not None and version.group(1) == VERSION_CIBLE,
                   f"version={version.group(1) if version else 'absent'}"))
    description_ok = ("engineering design" in fm.lower() and "système complexe" in fm.lower()
                      and "conception" in fm.lower() and "tests" in fm.lower())
    checks.append(("description couvre le périmètre Engineering Design", description_ok,
                   "mots-clés requis : engineering design, système complexe, conception, tests"))
    return texte


def checker_modes_et_regles(texte, checks):
    corps = corps_sans_frontmatter(texte)
    modes = [f"| {m} " for m in ("M1", "M2", "M3", "M4", "M5", "M6", "M7")]
    manquants = [m.strip("| ") for m in modes if m not in corps]
    checks.append(("7 modes M1-M7 déclarés", not manquants,
                   "tous présents" if not manquants else f"manquants : {manquants}"))
    noms_modes = all(n in corps for n in ("CADRER", "RÉDIGER", "VALIDER", "FAIRE ÉVOLUER",
                                          "ANALYSER", "CONCEVOIR", "TESTER"))
    checks.append(("noms des 7 modes présents", noms_modes,
                   "CADRER/RÉDIGER/VALIDER/FAIRE ÉVOLUER/ANALYSER/CONCEVOIR/TESTER"))
    regles = re.findall(r"^(\d+)\. \*\*", corps, re.M)
    regles_uniques = sorted({int(r) for r in regles})
    checks.append(("12 règles opérationnelles (1-12)",
                   regles_uniques[:len(regles_uniques)] != []
                   and set(range(1, 13)).issubset(set(regles_uniques)),
                   f"règles numérotées trouvées : {regles_uniques}"))
    compat = "Les modes M1-M4 conservent leur sémantique v1.0.0" in corps
    checks.append(("compatibilité v1.0.0 déclarée (M1-M4 inchangés)", compat,
                   "phrase de compatibilité présente" if compat else "phrase absente"))


def checker_dependances(texte, checks):
    fm = frontmatter(texte)
    trouvees = set(re.findall(r"^\s*-\s*skill:\s*(\S+)\s*$", fm, re.M))
    manquantes = DEPENDANCES_ATTENDUES - trouvees
    checks.append(("7 dépendances YAML déclarées", not manquantes,
                   f"{len(trouvees & DEPENDANCES_ATTENDUES)}/{len(DEPENDANCES_ATTENDUES)} "
                   + ("" if not manquantes else f"— manquantes : {sorted(manquantes)}")))


def checker_references(racine, checks):
    for nom in REFERENCES_ATTENDUES:
        texte = lire(racine, f"references/{nom}")
        checks.append((f"reference présente : {nom}", texte is not None,
                       "présente" if texte is not None else "introuvable"))
        if texte is not None:
            checks.append((f"reference v{VERSION_CIBLE} : {nom}", f"v{VERSION_CIBLE}" in texte,
                           "bannière v2.0.0" if f"v{VERSION_CIBLE}" in texte
                           else "bannière de version absente"))
    template = lire(racine, "references/template-cahier-des-charges.md")
    if template is not None:
        for marqueur, libelle in (("## Annexe D", "annexe D (fiche domaine)"),
                                  ("## Annexe T", "annexe T (stratégie de vérification)"),
                                  ("**Domaine**", "en-tête Domaine"),
                                  ("**Profil SE**", "en-tête Profil SE")):
            checks.append((f"template — {libelle}", marqueur in template,
                           "présent" if marqueur in template else "absent"))


def checker_livrables_et_formats(texte, checks):
    corps = corps_sans_frontmatter(texte)
    manquants = [l for l in LIVRABLES_V2 if l not in corps]
    checks.append(("livrables Engineering Design déclarés", not manquants,
                   "fiche-domaine/dossier-conception/batterie-tests/rapport-couverture"
                   if not manquants else f"manquants : {manquants}"))
    formats = {"SS-xx": "SS-xx", "I-xx": "I-xx", "TF-xx": "TF-xx", "TH-xx": "TH-xx",
               "[HYP-xx]": "[HYP-xx]", "EF-xx": "EF-xx", "ENF-xx": "ENF-xx"}
    manquants = [f for f, motif in formats.items() if motif not in corps]
    checks.append(("formats de traçabilité 3 niveaux", not manquants,
                   "SS-xx/I-xx/TF-xx/TH-xx/[HYP-xx]/EF-xx/ENF-xx"
                   if not manquants else f"manquants : {manquants}"))


def checker_evals(racine, checks):
    try:
        trigger = json.loads(lire(racine, "evals/trigger_evals.json") or "null")
    except json.JSONDecodeError as err:
        checks.append(("trigger_evals.json JSON valide", False, f"erreur : {err}"))
        return
    checks.append(("trigger_evals.json JSON valide", isinstance(trigger, list), ""))
    if not isinstance(trigger, list):
        return
    positifs = sum(1 for e in trigger if e.get("should_trigger") is True)
    negatifs = sum(1 for e in trigger if e.get("should_trigger") is False)
    checks.append(("trigger_evals : 12 requêtes", len(trigger) == 12,
                   f"{len(trigger)} requête(s)"))
    checks.append(("trigger_evals : 9 positives / 3 négatives", positifs == 9 and negatifs == 3,
                   f"{positifs} positives / {negatifs} négatives"))
    positifs_couverts = all(any(mot in e["query"].lower() for mot in ("cahier des charges", "cdc",
                                                                      "exigences", "conce", "test", "domaine",
                                                                      "cadrage"))
                            for e in trigger if e.get("should_trigger"))
    checks.append(("trigger_evals : positives ancrées sur le périmètre", positifs_couverts,
                   "cadrage/exigences/conception/tests/domaine/cahier des charges"))
    negatifs_ok = any("dessin" in e["query"].lower() for e in trigger
                      if e.get("should_trigger") is False)
    checks.append(("trigger_evals : contrôle négatif dessin-technique", negatifs_ok,
                   "présent" if negatifs_ok else "absent"))
    try:
        evals = json.loads(lire(racine, "evals/evals.json") or "null")
    except json.JSONDecodeError as err:
        checks.append(("evals.json JSON valide", False, f"erreur : {err}"))
        return
    coherent = (isinstance(evals, dict) and evals.get("version") == VERSION_CIBLE
                and isinstance(evals.get("evals"), list))
    checks.append(("evals.json version " + VERSION_CIBLE, coherent,
                   f"version={evals.get('version') if isinstance(evals, dict) else '?'}"))
    if coherent:
        q_trigger = {e["query"] for e in trigger}
        q_evals = {e.get("query") for e in evals["evals"]}
        checks.append(("evals.json cohérent avec trigger_evals (mêmes requêtes)",
                       q_trigger == q_evals,
                       f"{len(q_trigger & q_evals)}/{len(q_trigger | q_evals)} requêtes communes"))
        checks.append(("evals.json : 12 entrées", len(evals["evals"]) == 12,
                       f"{len(evals['evals'])} entrée(s)"))


def checker_scripts(racine, checks):
    for nom in ("scaffold_tests.py", "verifier_structure.py"):
        chemin = racine / "scripts" / nom
        checks.append((f"script présent : scripts/{nom}", chemin.is_file(),
                       "présent" if chemin.is_file() else "introuvable"))
    chemin_scaffold = racine / "scripts" / "scaffold_tests.py"
    if chemin_scaffold.is_file():
        try:
            compile(chemin_scaffold.read_text(encoding="utf-8"), str(chemin_scaffold), "exec")
            checks.append(("scaffold_tests.py compile", True, "compile() OK"))
        except (SyntaxError, ValueError) as err:
            checks.append(("scaffold_tests.py compile", False, str(err)[:200]))


def checker_cohérence_croisée(texte, racine, checks):
    corps = corps_sans_frontmatter(texte)
    manquants = [n for n in REFERENCES_ATTENDUES if n not in corps]
    checks.append(("SKILL.md cite les 4 references par nom", not manquants,
                   "toutes citées" if not manquants else f"non citées : {manquants}"))
    scripts_cites = "scaffold_tests.py" in corps and "verifier_structure.py" in corps
    checks.append(("SKILL.md cite ses scripts", scripts_cites,
                   "scaffold_tests.py + verifier_structure.py"
                   if scripts_cites else "citation manquante"))
    checks.append(("SKILL.md §5 déclare la voie mécanique",
                   "verifier_structure.py" in corps and "selftest" in corps.lower(),
                   "arbitre + selftest déclarés"))


def verifier(racine):
    checks = []
    texte = checker_frontmatter(racine, checks)
    if texte is not None:
        checker_modes_et_regles(texte, checks)
        checker_dependances(texte, checks)
        checker_livrables_et_formats(texte, checks)
        checker_cohérence_croisée(texte, racine, checks)
    checker_references(racine, checks)
    checker_evals(racine, checks)
    checker_scripts(racine, checks)
    return checks


def rapport(checks, as_json=False):
    echecs = [c for c in checks if not c[1]]
    document = {
        "skill": NOM_SKILL,
        "version_cible": VERSION_CIBLE,
        "total_checks": len(checks),
        "passes": len(checks) - len(echecs),
        "echecs": len(echecs),
        "verdict_global": "PASS" if not echecs else "ECHEC",
        "checks": [{"check": n, "ok": ok, "detail": d} for n, ok, d in checks],
    }
    if as_json:
        print(json.dumps(document, indent=2, ensure_ascii=False))
    else:
        for n, ok, d in checks:
            print(("PASS" if ok else "ECHEC").ljust(6) + f" {n}" + (f" — {d}" if d else ""))
        print(f"VERDICT GLOBAL : {document['verdict_global']} — "
              f"{document['passes']}/{document['total_checks']} checks PASS")
    return 0 if not echecs else 1


def selftest():
    """Auto-test : l'arbitre doit SAVOIR ÉCHOUER (pas un tampon en caoutchouc)."""
    sandbox = Path(tempfile.mkdtemp(prefix="verifier-selftest-"))
    try:
        # Fixture A — racine vide : au moins un ECHEC, code sortie 1
        checks = verifier(sandbox)
        assert any(not ok for _, ok, _ in checks), "l'arbitre ne détecte pas une racine vide"
        # Fixture B — version dépassée détectée spécifiquement
        faux = sandbox / "v1"
        (faux / "scripts").mkdir(parents=True)
        (faux / "SKILL.md").write_text(
            "---\nname: cahier-des-charges\nversion: \"1.0.0\"\n"
            "description: skill v1\n---\n\n# Titre\n", encoding="utf-8")
        checks = verifier(faux)
        version_ko = any(n == "frontmatter version = " + VERSION_CIBLE and not ok
                         for n, ok, _ in checks)
        assert version_ko, "l'arbitre ne détecte pas une version dépassée"
        # Fixture C — sortie JSON valide et verdict cohérent
        proc = subprocess.run([sys.executable, str(Path(__file__).resolve()),
                               "--racine", str(faux), "--json"],
                              capture_output=True, text=True)
        document = json.loads(proc.stdout)
        assert document["verdict_global"] == "ECHEC" and document["echecs"] >= 1
        assert proc.returncode == 1, "code sortie incohérent avec le verdict"
        print("SELFTEST OK — l'arbitre détecte racine vide, version dépassée, "
              "et sa sortie JSON est cohérente avec ses codes sortie.")
        return 0
    finally:
        shutil.rmtree(sandbox, ignore_errors=True)


def main():
    p = argparse.ArgumentParser(
        description=f"Arbitre de structure {NOM_SKILL} v{VERSION_CIBLE}")
    p.add_argument("--racine", default=str(Path(__file__).resolve().parent.parent),
                   help="dossier racine du skill (défaut : parent de scripts/)")
    p.add_argument("--json", action="store_true", help="sortie JSON machine")
    p.add_argument("--selftest", action="store_true",
                   help="auto-test : l'arbitre sait détecter des structures fausses")
    args = p.parse_args()
    if args.selftest:
        raise SystemExit(selftest())
    try:
        checks = verifier(Path(args.racine))
    except Exception as err:  # garde-fou : une erreur d'exécution n'est pas un ECHEC de check
        print(f"ERREUR D'EXÉCUTION — {err}")
        raise SystemExit(2)
    raise SystemExit(rapport(checks, as_json=args.json))


if __name__ == "__main__":
    main()
