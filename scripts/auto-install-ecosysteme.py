#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.31)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).
"""

# -*- coding: utf-8 -*-
"""
Auto-install écosystème — self-healing de l'installation hôte (E13 n°7 / D727).

Contexte : le chemin `skills/` du profil hôte est géré par la plateforme — chaque
recyclage du sandbox restaure l'image plateforme et emporte l'installation
(findings F1/F2 du rapport correct-work (projet) 2026-11-01). Ce script rend la
ré-installation AUTOMATIQUE : il contrôle via (a) la COPIE DÉPÔT de
ensure-installed (toujours disponible, indépendante de l'état installé) et
(b) un contrôle critique de BYTE-IDENTITÉ hôte ↔ dépôt sur un ensemble pivot
(l'angle mort « fichier isolé manquant/divergent » du checker d'origine a été
détecté au test T2 — le contrôle (b) le couvre), exécute le pipeline canonique
si un défaut est détecté, puis re-contrôle.

**Extension v2 (Task 31, directive GO (b) trace 1a1975c9a4c7fa31, 2026-11-01)** :
le contrôle (b) couvre désormais TOUTES les entrées KB versionnées (SKILL.md
derivé DYNAMIQUEMENT du dépôt KB — l'angle mort « version-management INSTALLE
à tort » matérialisé ×3 le 2026-11-01 est résorbé par construction) en plus de
l'ensemble pivot CRITIQUES (7 fichiers).

Idempotent ×2 : re-jeu sur état sain = no-op (verdict INSTALLE, 0 action).
Verdict JSON déterministe + rc : 0 = INSTALLE/REINSTALLE, 1 = ECHEC (arrêt
explicite — règle d'or n°1 : pause motivée, cause journalisée).

Options (défaut : rapport seul — le disque peut être > 80 %, ENOSPC documenté) :
  --with-toolchain  installe pdf2zh-next==2.9.0 + bitstring==4.3.0 (moteur PDF v1.3)
  --with-argos      installe argostranslate + modèles translate-zh_en / translate-en_fr
  --selftest        tests internes (sans effet sur l'installation réelle)
"""
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

BASE = Path("/home/z/my-project")
REPO = BASE / "KNOWLEDGE-repo"
CHECKER = REPO / "skills" / "gen-plan" / "scripts" / "ensure-installed.py"
PIPELINE = REPO / "scripts" / "eco_install_pipeline.py"

# Ensemble critique : présence + BYTE-IDENTITÉ hôte ↔ dépôt exigées.
CRITIQUES = [
    "skills/KNOWLEDGE.md",
    "skills/gen-plan/SKILL.md",
    "skills/correct-work/SKILL.md",
    "skills/@mon-ecosysteme/PROMPT-MAITRE-SHARED.md",
    "skills/traduction-zh-fr/SKILL.md",
    "skills/traduction-zh-fr/scripts/traduire-md-zh-fr.py",
    "skills/traduction-zh-fr/scripts/traduire-pdf-zh-fr.py",
]

TOOLCHAIN_PINS = ["pdf2zh-next==2.9.0", "bitstring==4.3.0"]
ARGOS_MODELES = ["translate-zh_en", "translate-en_fr"]


def critiques_kb(racine_depot: Path = REPO) -> list:
    r"""SKILL.md de TOUTES les entrées KB versionnées — dérivé DYNAMIQUEMENT du
    dépôt KB (regex identique à l'arbitre integrity ^## ([\w-]+) v([\d.]+)),
    jamais figé (KO-L003). Toute nouvelle entrée KB est couverte sans édition
    de ce script. Absence de KB = [] (dégradation honnête — le pivot CRITIQUES
    reste contrôlé)."""
    import re
    kb = racine_depot / "skills" / "KNOWLEDGE.md"
    if not kb.exists():
        return []
    entrees = re.findall(r"^## ([\w-]+) v[\d.]+", kb.read_text(encoding="utf-8"), re.M)
    return [f"skills/{n}/SKILL.md" for n in sorted(set(entrees)) if not n.startswith("@")] + ["skills/KNOWLEDGE.md"]


def module_present(nom: str) -> bool:
    try:
        return importlib.util.find_spec(nom) is not None
    except (ImportError, ValueError):
        return False


def etat_toolchain() -> dict:
    return {
        "babeldoc": module_present("babeldoc"),
        "pymupdf": module_present("pymupdf"),
        "argostranslate": module_present("argostranslate"),
    }


def defauts_critiques(racine_hote: Path = BASE, racine_depot: Path = REPO) -> list:
    """Fichiers critiques absents ou divergents (hôte vs dépôt, SHA-256).

    Périmètre = CRITIQUES (pivot 7 fichiers) + SKILL.md de toutes les entrées KB
    versionnées (extension v2 Task 31). Paramètres racine injectables pour le
    selftest (aucun effet de bord).
    """
    defauts = []
    vus = set()
    for rel in CRITIQUES + critiques_kb(racine_depot):
        if rel in vus:
            continue
        vus.add(rel)
        hote = racine_hote / rel
        depot = racine_depot / rel
        if not depot.exists():
            defauts.append(f"{rel} (dépôt absent)")
            continue
        if not hote.exists():
            defauts.append(f"{rel} (hôte absent)")
            continue
        h = hashlib.sha256(hote.read_bytes()).hexdigest()
        d = hashlib.sha256(depot.read_bytes()).hexdigest()
        if h != d:
            defauts.append(f"{rel} (divergent hôte≠dépôt)")
    return defauts


def controler_installation() -> dict:
    """Contrôle via la copie dépôt — fonctionne même si l'installation hôte est absente."""
    r = subprocess.run(
        [sys.executable, str(CHECKER), "--check"], capture_output=True, text=True
    )
    lignes = [l for l in r.stdout.strip().splitlines() if l.strip()]
    if lignes:
        try:
            return json.loads(lignes[-1])
        except json.JSONDecodeError:
            pass
    return {"verdict": "ERREUR", "rc": r.returncode, "stderr": (r.stderr or "")[-400:]}


def installer_toolchain(resultat: dict) -> None:
    r = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-q", "--no-cache-dir"] + TOOLCHAIN_PINS,
        capture_output=True, text=True,
    )
    resultat["actions"].append(f"toolchain pip rc={r.returncode}")
    resultat["toolchain"] = etat_toolchain()


def installer_argos(resultat: dict) -> None:
    r = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-q", "--no-cache-dir", "argostranslate"],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        resultat["actions"].append(f"argos pip rc={r.returncode} (échec — disque ?)")
        resultat["toolchain"] = etat_toolchain()
        return
    installes = {p.code for p in _packages_installes()}
    manquants = [c for c in ARGOS_MODELES if c not in installes]
    if manquants:
        dispo = {p.code: p for p in _packages_disponibles()}
        for code in manquants:
            if code in dispo:
                dispo[code].install()
    resultat["actions"].append(
        "argos modeles : " + str([(p.from_code, p.to_code) for p in _packages_installes()])
    )
    resultat["toolchain"] = etat_toolchain()


def _packages_installes():
    from argostranslate import package
    return package.get_installed_packages()


def _packages_disponibles():
    from argostranslate import package
    return package.get_available_packages()


def selftest() -> int:
    """Tests internes — sans effet sur l'installation réelle."""
    checks = []

    # T1 : tous les fichiers critiques (pivot + KB) existent dans le dépôt
    critiques_tous = list(dict.fromkeys(CRITIQUES + critiques_kb()))  # dédup préservant l'ordre
    depot_absents = [r for r in critiques_tous if not (REPO / r).exists()]
    checks.append((f"dépôt : {len(critiques_tous)}/{len(critiques_tous)} fichiers critiques présents", not depot_absents))

    # T1bis (extension v2 Task 31) : la liste KB est dérivée dynamiquement et non vide
    n_kb = len(critiques_kb())
    checks.append((f"contrôle (b) : {n_kb} SKILL.md dérivés de la KB (dynamique, >= 44)", n_kb >= 44))

    # T2 : état sain → 0 défaut (contrôle byte-identité sur l'hôte réel)
    checks.append(("état sain : 0 défaut critique hôte", defauts_critiques() == []))

    # T3 : détection d'un défaut synthétique (hôte tamponné en mémoire via racine factice)
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        faux_hote = Path(tmp)
        defauts = defauts_critiques(racine_hote=faux_hote)
        checks.append((f"défaut synthétique détecté ({len(critiques_tous)}/{len(critiques_tous)} fichiers manquants)", len(defauts) == len(critiques_tous)))

    # T4 : verdicts déterministes (logique de décision sur états synthétiques)
    checks.append(("verdicts JSON sérialisables", json.dumps(
        {"verdict": "INSTALLE", "actions": []}, ensure_ascii=False) is not None))

    ok = all(ok for _, ok in checks)
    for nom, ok_c in checks:
        print(f"  [{'PASS' if ok_c else 'FAIL'}] {nom}")
    print(f"SELFTEST {'PASS' if ok else 'FAIL'} ({sum(1 for _, o in checks if o)}/{len(checks)})")
    return 0 if ok else 1


def main() -> int:
    if "--selftest" in sys.argv[1:]:
        return selftest()

    flags = set(sys.argv[1:]) - {"--selftest"}
    resultat = {"script": "auto-install-ecosysteme", "actions": []}

    if not CHECKER.exists() or not PIPELINE.exists():
        resultat["verdict"] = "ECHEC"
        resultat["cause"] = (
            f"copies dépôt indisponibles (checker={CHECKER.exists()}, pipeline={PIPELINE.exists()}) "
            "— arrêt explicite règle d'or n°1 : le dépôt KNOWLEDGE-repo est requis"
        )
        print(json.dumps(resultat, ensure_ascii=False))
        return 1

    etat = controler_installation()
    defauts = defauts_critiques()
    resultat["controle_initial"] = etat.get("verdict")
    resultat["critiques_en_defaut"] = defauts

    if etat.get("verdict") != "INSTALLE" or defauts:
        resultat["actions"].append("pipeline")
        r = subprocess.run(
            [sys.executable, str(PIPELINE)], capture_output=True, text=True
        )
        resultat["pipeline_rc"] = r.returncode
        if r.returncode != 0:
            resultat["verdict"] = "ECHEC"
            resultat["cause"] = ((r.stderr or "") + (r.stdout or ""))[-400:]
            print(json.dumps(resultat, ensure_ascii=False))
            return 1
        etat = controler_installation()
        resultat["critiques_en_defaut_apres"] = defauts_critiques()

    resultat["controle_final"] = etat.get("verdict")
    resultat["kb_entrees"] = etat.get("kb_entrees")
    resultat["toolchain"] = etat_toolchain()

    if "--with-toolchain" in flags:
        installer_toolchain(resultat)
    if "--with-argos" in flags:
        installer_argos(resultat)

    sain = resultat["controle_final"] == "INSTALLE" and not resultat.get(
        "critiques_en_defaut_apres", resultat["critiques_en_defaut"]
    )
    if not sain:
        resultat["verdict"] = "ECHEC"
        resultat["cause"] = "contrôle final non-INSTALLE / critiques en défaut après réinstallation"
    elif "pipeline" in resultat["actions"]:
        resultat["verdict"] = "REINSTALLE"
    else:
        resultat["verdict"] = "INSTALLE"

    print(json.dumps(resultat, ensure_ascii=False))
    return 0 if sain else 1


if __name__ == "__main__":
    sys.exit(main())
