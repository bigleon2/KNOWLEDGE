#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.37)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).
task43-replay-answer-key.py — Replay mécanique de l'answer key Task 43 (D001-D012).

Rejoue, de façon exécutable et déterministe (précédents Task 40 G5 / Task 42 G4),
les 12 décisions du plan `download/plan-task43-test-adaptation-syntaxe-correct-work-projet.md`
(test $FACON de la solution « syntaxe erreur » + correct-work (projet) avec le mapping
DJTT comme source de vérité / exemple de mapping avancé). Sous-processus lancés avec
stdin=DEVNULL (leçon d'environnement 2026-11-04 — verdicts fantômes).

Usage : python3 scripts/task43-replay-answer-key.py   (racine = /home/z/my-project)
Codes de sortie : 0 si 12/12 verified, 1 sinon. Idempotent ×2 (aucun effet de bord
hors journaux ; la batterie et le vérificateur sont eux-mêmes idempotents).
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLONE = os.path.join(RACINE, "work", "knowledge-clone-fddbe94")
DOWNLOAD = os.path.join(RACINE, "download")

BRUIT_TEMPLATE = [
    "src/app/api/API Design", "src/app/api/API Knowledge", "src/app/api/KNOWLEDGE.md",
    "src/app/api/README.md", "src/app/api/knowledge-export.yaml", "src/app/api/config",
    "src/app/api/knowledge", "src/app/api/skills", "src/lib/skills-reader.ts",
]


def _exec(args, cwd=RACINE, timeout=420):
    """Exécute une commande (stdin=DEVNULL — leçon stdin-hérité)."""
    return subprocess.run(
        args, capture_output=True, text=True, timeout=timeout,
        check=False, cwd=cwd, stdin=subprocess.DEVNULL,
    )


def _existe(chemin):
    return os.path.isfile(chemin) and os.path.getsize(chemin) > 0


def _identique(relatif_hote, relatif_clone=None):
    """Compare byte-à-byte un fichier hôte et son miroir dépôt."""
    clone = relatif_clone or relatif_hote
    chemin_hote = os.path.join(RACINE, relatif_hote)
    chemin_clone = os.path.join(CLONE, relatif_clone) if relatif_clone else os.path.join(CLONE, relatif_hote)
    if not (_existe(chemin_hote) and _existe(chemin_clone)):
        return False
    with open(chemin_hote, "rb") as a, open(chemin_clone, "rb") as b:
        return a.read() == b.read()


def d001():
    """Batterie d'injection de pannes : 13/13 PASS, re-jeu ×2."""
    for _ in range(2):
        fini = _exec([sys.executable, "scripts/task43-tests-adaptation-syntaxe.py", "--batterie"])
        if fini.returncode != 0 or not re.search(r"BATTERIE : 13/13 PASS", fini.stdout):
            return False
    return True


def d002():
    """Scénario E2E incident fondateur débloqué + surface CLI : 6/6 PASS."""
    fini = _exec([sys.executable, "scripts/task43-tests-adaptation-syntaxe.py", "--e2e"])
    return fini.returncode == 0 and "E2E : 6/6 PASS" in fini.stdout


def d003():
    """Self-test 11/11 + scan écosystème étendu : PASS, ≥ 320 fichiers, 0 erreur."""
    essai = _exec([sys.executable, "scripts/adaptation-syntaxe.py", "self-test"], timeout=300)
    if essai.returncode != 0 or "SELF-TEST 11/11 PASS" not in essai.stdout:
        return False
    scan = _exec(
        [sys.executable, "scripts/adaptation-syntaxe.py", "scan",
         "scripts/", os.path.join("work", "knowledge-clone-fddbe94", "scripts"),
         "src/lib/", "src/data/", os.path.join("work", "knowledge-clone-fddbe94", "tsi-toolkit"),
         "--json"],
        timeout=600,
    )
    try:
        rapport = json.loads(scan.stdout)
    except ValueError:
        return False
    return (
        scan.returncode == 0
        and rapport.get("verdict") == "PASS"
        and rapport.get("erreurs") == []
        and rapport.get("fichiers_verifies", 0) >= 320
    )


def d004():
    """Rapport de tests persisté + script de batterie miroir dépôt byte-identique."""
    return (
        _existe(os.path.join(DOWNLOAD, "rapport-tests-adaptation-syntaxe.md"))
        and _identique(os.path.join("scripts", "task43-tests-adaptation-syntaxe.py"))
        and _identique(os.path.join("scripts", "adaptation-syntaxe.py"))
    )


def d005():
    """Étape 2 — comptes DJTT re-dérivés de la source de vérité : DONNEES PASS."""
    fini = _exec([sys.executable, "scripts/task43-verifier-projet.py", "--donnees"], timeout=420)
    return fini.returncode == 0 and "DONNEES : PASS" in fini.stdout


def d006():
    """Étape 3 — 9 reliquats template retirés + 0 dérive de modes (index git)."""
    for relatif in BRUIT_TEMPLATE:
        if os.path.exists(os.path.join(CLONE, relatif)):
            return False
    fini = _exec(["git", "diff", "--numstat"], cwd=CLONE)
    restants = [l for l in fini.stdout.splitlines() if re.match(r"^0\t0\t", l)]
    return len(restants) == 0


def d007():
    """Étape 4 — interactions + E2E mapping avancé DJTT : INTERACTIONS PASS."""
    fini = _exec([sys.executable, "scripts/task43-verifier-projet.py", "--interactions"], timeout=600)
    return fini.returncode == 0 and "INTERACTIONS : PASS" in fini.stdout


def d008():
    """Étape 5 — rapport correct-work au format §2.4, verdict PASS."""
    chemin = os.path.join(DOWNLOAD, "rapport-correct-work-projet-task43.md")
    if not _existe(chemin):
        return False
    with open(chemin, encoding="utf-8") as poignee:
        contenu = poignee.read()
    return "Verdict : PASS" in contenu and all(m in contenu for m in ("Étape 2", "Étape 3", "Étape 4", "Étape 5"))


def d009():
    """Sync miroir clôture : rapports Task 42 + Task 43 byte-identiques hôte↔dépôt."""
    paires = [
        (os.path.join("download", "rapport-final-task42.md"),),
        (os.path.join("download", "plan-task42-taches-restantes-decks.md"),),
        (os.path.join("download", "rapport-tests-task42.md"),),
        (os.path.join("download", "rapport-adaptation-syntaxe.md"),),
        (os.path.join("download", "plan-task43-test-adaptation-syntaxe-correct-work-projet.md"),),
        (os.path.join("download", "rapport-tests-adaptation-syntaxe.md"),),
        (os.path.join("download", "rapport-correct-work-projet-task43.md"),),
        (os.path.join("download", "rapport-final-task43.md"),),
        (os.path.join("scripts", "task43-verifier-projet.py"),),
        (os.path.join("scripts", "task43-replay-answer-key.py"),),
    ]
    for (relatif,) in paires:
        if not _identique(relatif):
            return False
    # données vitales inchangées : comptes DJTT stables (source de vérité)
    return _identique(os.path.join("work", "task42-matrice-decks.json"))


def d010():
    """Replay mécanique : script présent + miroir byte-identique (l'exécution ×2
    est prouvée par les DEUX invocations externes — chacune doit rendre 12/12)."""
    return _existe(os.path.join(RACINE, "scripts", "task43-replay-answer-key.py")) and _identique(
        os.path.join("scripts", "task43-replay-answer-key.py"))


def d011():
    """Clôture : rapport final + PLAN-AFFICHE au worklog + intégrité 98/98."""
    if not _existe(os.path.join(DOWNLOAD, "rapport-final-task43.md")):
        return False
    with open(os.path.join(CLONE, "worklog.md"), encoding="utf-8") as poignee:
        if "PLAN-AFFICHE" not in poignee.read():
            return False
    fini = _exec([sys.executable, "scripts/check-ecosysteme-integrity.py"], cwd=CLONE, timeout=300)
    return "98/98 PASS" in fini.stdout


def d012():
    """Bilan E15 : calibration + pendances (PUSH, S4 MK2) consignées au rapport final."""
    chemin = os.path.join(DOWNLOAD, "rapport-final-task43.md")
    if not _existe(chemin):
        return False
    with open(chemin, encoding="utf-8") as poignee:
        contenu = poignee.read()
    return "E15" in contenu and "PUSH" in contenu and "S4 MK2" in contenu


DECISIONS = [
    ("D001", d001), ("D002", d002), ("D003", d003), ("D004", d004),
    ("D005", d005), ("D006", d006), ("D007", d007), ("D008", d008),
    ("D009", d009), ("D010", d010), ("D011", d011), ("D012", d012),
]


def main():
    """Rejoue les 12 décisions et affiche le verdict consolidé."""
    resultats = []
    for identifiant, verifier in DECISIONS:
        try:
            ok = bool(verifier())
        except (OSError, ValueError, subprocess.SubprocessError) as erreur:
            ok = False
            print(f"  ({identifiant} : exception {type(erreur).__name__}: {erreur})")
        resultats.append((identifiant, ok))
        print(f"  {identifiant} {'PASS' if ok else 'ÉCHEC'}")
    pass_ok = sum(1 for _, ok in resultats if ok)
    print(f"REPLAY ANSWER KEY : {pass_ok}/{len(resultats)} verified")
    return 0 if pass_ok == len(resultats) else 1


if __name__ == "__main__":
    sys.exit(main())
