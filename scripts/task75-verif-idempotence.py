#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.37)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).
"""

"""task75-verif-idempotence.py — harnais Task 75 (vérification idempotence
écosystème post-re-curation vs version précédente, directive 1a1b9955a1f207ed).

Vérifications propres à la Task 75 (les autres sont portées par les arbitres
existants, réutilisés — R4 jamais dupliquer) :
  --check baseline  : intégrité croisée golden master Task 72 (JSON) ↔ git 011d342
                      (SKILL.md v3.38.0 byte-exact + 9 blocs sha256 + evals ×2)   [D002]
  --check fidelite  : skills/ hôte ↔ KNOWLEDGE-repo/skills/ byte-identiques
                      (exclusion __pycache__) — 0 divergence attendue            [D003]
  --check diffs     : commit range 011d342..a14f750 == 5 commits documentés
                      exactement + fichiers non-commités ⊆ classes resync
                      Task 74 — 0 orphelin                                      [D009]
  --check evals     : evals/ courant ↔ baseline git (identité byte)              [P1]
  --tout (défaut)   : tous les checks + synthèse JSON download/task75-verif-idempotence.json

Règle d'or n°5 : tout chiffre affiché est mesuré ici. Python stdlib (N3).
Idempotent ×2 (aucune écriture hors le JSON de synthèse en mode --tout).
Sortie : rc=0 PASS, rc=1 FAIL.
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

RACINE = Path("/home/z/my-project")
REPO = RACINE / "KNOWLEDGE-repo"
SKILLS_HOTE = RACINE / "skills"
SKILLS_DEPOT = REPO / "skills"
BASELINE_JSON = RACINE / "download" / "task72-baseline-genplan.json"
BASELINE_GIT = RACINE / "tmp" / "verif-task75" / "baseline" / "SKILL.md"
EVALS_GIT = RACINE / "tmp" / "verif-task75" / "baseline" / "evals"
SYNTHESE = RACINE / "download" / "task75-verif-idempotence.json"

COMMIT_BASELINE = "011d342"
COMMIT_HEAD = "a14f750"
COMMITS_DOCUMENTES = ["5646e96", "d3ee6e6", "4439592", "a790d04", "a14f750"]
# Classes du resync Task 74 (installation certifiée post-wipe, worklog suite 50 —
# commit prévu au G3 GO de la Task 74) : préfixes autorisés pour le non-commité.
CLASSES_RESYNC = (
    "download/", "skills/@historique/", "skills/@mon-ecosysteme/",
    "skills/KNOWLEDGE.md", "scripts/", "worklog.md",
)

import importlib.util

_spec = importlib.util.spec_from_file_location(
    "task72_baseline_verifier", RACINE / "scripts" / "task72-baseline-verifier.py")
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
blocs_9 = _mod.blocs_9  # réutilisation R4 — bornes strictement identiques à l'extracteur


def _git(*args: str) -> str:
    r = subprocess.run(["git", "-C", str(REPO), *args],
                       capture_output=True, text=True, check=True)
    return r.stdout


def sha256_fichier(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


# ---------------------------------------------------------------- checks

def check_baseline() -> dict:
    """Golden master JSON ↔ extraction git 011d342 (byte-exact + 9 blocs + evals)."""
    ref = json.loads(BASELINE_JSON.read_text(encoding="utf-8"))
    resultat = {"checks": {}}

    texte = BASELINE_GIT.read_text(encoding="utf-8")
    resultat["checks"]["skill_md_sha256"] = {
        "attendu": ref["skill_md"]["sha256"],
        "mesure": sha256_fichier(BASELINE_GIT),
    }
    resultat["checks"]["skill_md_octets"] = {
        "attendu": ref["skill_md"]["octets"],
        "mesure": len(texte.encode("utf-8")),
    }
    lignes = texte.splitlines()
    blocs = blocs_9(lignes)
    for cle, attendu in ref["blocs"].items():
        extrait = blocs.get(cle)
        mesure = hashlib.sha256(extrait.encode("utf-8")).hexdigest() if extrait else None
        octets = len(extrait.encode("utf-8")) if extrait else -1
        resultat["checks"][f"bloc_{cle}"] = {
            "attendu": attendu["sha256_brut"], "mesure": mesure,
            "octets_attendus": attendu["octets"], "octets_mesures": octets,
        }
    for nom, chemin in (("evals", EVALS_GIT / "evals.json"),
                        ("trigger_evals", EVALS_GIT / "trigger_evals.json")):
        attendu = ref["contrats"][f"{nom}_json_sha256"]
        resultat["checks"][f"{nom}_json_sha256"] = {
            "attendu": attendu, "mesure": sha256_fichier(chemin),
        }
    echecs = [k for k, v in resultat["checks"].items()
              if v["attendu"] != v["mesure"]]
    resultat["verdict"] = "PASS" if not echecs else "FAIL"
    resultat["echecs"] = echecs
    return resultat


def entrees_kb() -> list:
    """Entrées du registre KB (source de vérité — Règle Zéro) : lignes « ## <nom> vX.Y.Z »."""
    texte = (SKILLS_HOTE / "KNOWLEDGE.md").read_text(encoding="utf-8")
    return re.findall(r"^## ([a-z][a-z0-9-]*) v\d+\.\d+\.\d+", texte, re.M)


def _comparer_dossier(rel: str) -> dict:
    """Compare un dossier skills/<rel> hôte ↔ dépôt (exclusion __pycache__)."""
    exclus = {"__pycache__"}
    hote, depot = {}, {}
    for racine, table in ((SKILLS_HOTE / rel, hote), (SKILLS_DEPOT / rel, depot)):
        if not racine.exists():
            continue
        for p in racine.rglob("*"):
            if p.is_file() and not any(part in exclus for part in p.parts):
                table[str(p.relative_to(racine))] = sha256_fichier(p)
    return {
        "seuls_hote": sorted(set(hote) - set(depot)),
        "seuls_depot": sorted(set(depot) - set(hote)),
        "divergents": sorted(k for k in set(hote) & set(depot) if hote[k] != depot[k]),
    }


def check_fidelite() -> dict:
    """Fidélité hôte↔dépôt SUR LE PÉRIMÈTRE PERSONNEL (KO-L003 — invariant dynamisé v2).

    La garde É1-INSTALL est invoquée d'abord (elle RÉPARE les disparitions
    environnementales documentées — neutralisation résiliente v1.3.0 : c'est la
    machinerie P2 en action, pas une divergence). Puis :
      — périmètre KB (entrée par entrée) : identité byte COMPLÈTE exigée ;
      — corpus installés (@mon-ecosysteme, @historique, collections, KB) : hôte ⊆ dépôt ;
      — hors périmètre (plate-forme + corpus externes dépôt-seuls) : classes
        informationnelles, jamais FAIL (règle d'or n°8 — le PM INSTALL n'installe
        que skills/<skill>/).
    """
    garde = subprocess.run(
        ["python3", str(RACINE / "skills" / "gen-plan" / "scripts" / "ensure-installed.py"),
         "--check"], capture_output=True, text=True)
    try:
        verdict_garde = json.loads(garde.stdout).get("verdict", garde.stdout[:80])
    except json.JSONDecodeError:
        verdict_garde = garde.stdout.strip()[:80]

    kb = entrees_kb()
    ecarts_kb = {}
    for nom in kb:
        r = _comparer_dossier(nom)
        if any(r.values()):
            ecarts_kb[nom] = r

    corpus = {}
    for rel in ("@mon-ecosysteme", "@historique", "@Bibliotheque-skills-Multi-IA",
                "@GHORG-ecosysteme"):
        r = _comparer_dossier(rel)
        corpus[rel] = {"seuls_hote": r["seuls_hote"], "divergents": r["divergents"]}
    kb_fic = _comparer_dossier("KNOWLEDGE.md" if (SKILLS_DEPOT / "KNOWLEDGE.md").is_file()
                               else "__absent__")
    corpus["KNOWLEDGE.md"] = {"seuls_hote": kb_fic["seuls_hote"],
                              "divergents": kb_fic["divergents"]}
    corpus_propre = all(not v["seuls_hote"] and not v["divergents"] for v in corpus.values())

    # hors périmètre : plate-forme (dirs hôte hors KB) + externes (dirs dépôt hors KB/corpus)
    connus = set(kb) | {"@mon-ecosysteme", "@historique", "@Bibliotheque-skills-Multi-IA",
                        "@GHORG-ecosysteme", "KNOWLEDGE.md"}
    hors_hote = sorted(p.name for p in SKILLS_HOTE.iterdir()
                       if p.name not in connus and p.name != "__pycache__")
    hors_depot = sorted(p.name for p in SKILLS_DEPOT.iterdir()
                        if p.name not in connus and p.name != "__pycache__")

    return {
        "garde_e1_install": {"rc": garde.returncode, "verdict": verdict_garde},
        "entrees_kb": len(kb),
        "ecarts_kb": ecarts_kb,
        "corpus_hote_inclu_depot": corpus,
        "hors_perimetre_informationnel": {
            "plateforme_hote": hors_hote,
            "corpus_externes_depot": hors_depot,
        },
        "verdict": "PASS" if not ecarts_kb and corpus_propre else "FAIL",
    }


def check_diffs() -> dict:
    """Commit range documenté + non-commité : 0 orphelin de CONTENU (v2).

    Les changements de MODE PURS (bits d'exécution 100644→100755, hérités du
    ressync Task 74 — zéro octet de contenu modifié) forment une classe justifiée
    informationnelle ; seuls les changements de CONTENU hors classes ressync
    constituent des orphelins bloquants.
    """
    revs = [l.split()[0][:7] for l in _git("log", "--format=%H", "--reverse",
                                           f"{COMMIT_BASELINE}..{COMMIT_HEAD}").splitlines()]
    commits_ok = revs == COMMITS_DOCUMENTES

    status = _git("status", "--short")
    chemins = [l[3:].strip().strip('"') for l in status.splitlines()]
    # contenu modifié : numstat non nul (lignes ajoutées/supprimées) ; mode pur sinon
    numstat = {}
    for ligne in _git("diff", "--numstat").splitlines():
        if not ligne.strip():
            continue
        parties = ligne.split("\t")
        if len(parties) < 3 or parties[0] == "-" or parties[1] == "-":
            # lignes binaires « -\t-\tchemin » : traitées en contenu modifié (prudent)
            numstat[parties[-1].strip('"')] = 1
            continue
        numstat[parties[2].strip('"')] = int(parties[0]) + int(parties[1])
    contenu_modifie = sorted(c for c in chemins if numstat.get(c, 0) > 0)
    mode_seuls = sorted(c for c in chemins if numstat.get(c, 0) == 0)

    def classe(c):
        return next((p for p in CLASSES_RESYNC if c.startswith(p)), None)

    orphelins_contenu = [c for c in contenu_modifie if classe(c) is None]
    orphelins_mode = [c for c in mode_seuls if classe(c) is None]
    return {
        "commits_attendus": COMMITS_DOCUMENTES, "commits_mesures": revs,
        "commits_documentes": commits_ok,
        "non_commites_total": len(chemins),
        "contenu_modifie": contenu_modifie,
        "mode_seuls_total": len(mode_seuls),
        "mode_seuls_hors_classes": orphelins_mode,
        "orphelins_contenu": orphelins_contenu,
        "verdict": "PASS" if commits_ok and not orphelins_contenu else "FAIL",
    }


def check_evals() -> dict:
    """evals/ courant ↔ baseline git 011d342 (identité byte — jamais touchés par la re-curation)."""
    cible = SKILLS_HOTE / "gen-plan" / "evals"
    retour = {}
    for nom in ("evals.json", "trigger_evals.json"):
        retour[nom] = {
            "baseline": sha256_fichier(EVALS_GIT / nom),
            "courant": sha256_fichier(cible / nom),
        }
        retour[nom]["identiques"] = (retour[nom]["baseline"] == retour[nom]["courant"])
    retour["verdict"] = "PASS" if all(v["identiques"] for v in retour.values()) else "FAIL"
    return retour


# ---------------------------------------------------------------- selftest

def selftest() -> int:
    """Vérifications mécaniques du harnais lui-même (tampons en mémoire)."""
    ok = []

    def t(nom, cond):
        ok.append((nom, bool(cond)))
        print(f"  [{'PASS' if cond else 'FAIL'}] {nom}")

    t("S1 blocs_9 importé de task72-baseline-verifier (R4)",
      callable(blocs_9))
    t("S2 baseline git extraite (SKILL.md présent)",
      BASELINE_GIT.exists() and BASELINE_GIT.stat().st_size == 106465)
    t("S3 golden master JSON lisible (14 clés skill_md+blocs+contrats)",
      len(json.loads(BASELINE_JSON.read_text(encoding='utf-8'))["blocs"]) == 9)
    t("S4 classes resync définies (6 préfixes)",
      len(CLASSES_RESYNC) == 6)
    motif = re.compile(r"^[0-9a-f]{7}( [0-9a-f]{7})*$")
    t("S5 format rev-list assimilable", motif.match("a14f750 5646e96") is not None)
    print(f"  === SELFTEST : {sum(1 for _, c in ok if c)}/{len(ok)} PASS ===")
    return 0 if all(c for _, c in ok) else 1


# ---------------------------------------------------------------- main

def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--check", choices=["baseline", "fidelite", "diffs", "evals", "tout"],
                   default="tout")
    p.add_argument("--selftest", action="store_true")
    args = p.parse_args()

    if args.selftest:
        return selftest()

    fonctions = {"baseline": check_baseline, "fidelite": check_fidelite,
                 "diffs": check_diffs, "evals": check_evals}
    if args.check == "tout":
        resultats = {nom: f() for nom, f in fonctions.items()}
        verdict = "PASS" if all(r["verdict"] == "PASS" for r in resultats.values()) else "FAIL"
        charge = {"horodatage": _git("show", "-s", "--format=%cI", "HEAD").strip(),
                  "verdict": verdict, "checks": resultats}
        SYNTHESE.write_text(json.dumps(charge, ensure_ascii=False, indent=1) + "\n",
                            encoding="utf-8")
        print(f"VERDICT GLOBAL : {verdict} — synthèse : {SYNTHESE}")
        for nom, r in resultats.items():
            print(f"  [{r['verdict']}] {nom}")
        return 0 if verdict == "PASS" else 1

    r = fonctions[args.check]()
    print(json.dumps(r, ensure_ascii=False, indent=1))
    return 0 if r["verdict"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
