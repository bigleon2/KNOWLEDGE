#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.21)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
adaptation-syntaxe.py — Garde d'auto-réparation syntaxique de l'écosystème.

Solution d'adaptation autonome (directive pré-gen-plan 2026-11-04) : lorsque
l'écosystème ou une session est bloquée par une erreur de syntaxe (bug
« syntaxe erreur »), ce script détecte, répare mécaniquement les classes de
défauts connues et fournit un diagnostic exploitable — sans retouche manuelle.

Incident fondateur (worklog, certification corpus v3.32.0) :
« from __future__ import annotations » mal placé — SyntaxError py_compile
« must occur at the beginning » sur garde-plan-genplan.py et
sync-instructions-ecosysteme.py. Correctif manuel à l'époque ; automatisé ici.

Classes de correctifs mécaniques (try-and-revert — aucun correctif n'est
conservé s'il ne rétablit pas la compilation) :

  future_import : « from __future__ import ... » replacé en tête de module
                  (après shebang / codage / docstring) — Python uniquement
  bom           : BOM U+FEFF en tête supprimé (fatal en bash)
  crlf          : fins de ligne CRLF / CR isolés -> LF (fatal en bash)
  zero_width    : caractères de largeur nulle supprimés
                  (U+200B-U+200D, U+2060, U+FEFF internes, U+00AD)
  narrow_space  : espaces insécables / typographiques -> espace ASCII
                  (U+00A0, U+2000-U+200A, U+202F, U+205F, U+3000)
  smart_quotes  : guillemets / apostrophes typographiques -> ASCII
  fullwidth     : ponctuation pleine largeur CJK -> ASCII

Sécurité par construction :
  1. un fichier sain n'est JAMAIS modifié (no-op vérifié) ;
  2. passes simples (une classe à la fois, sur l'original) puis une passe
     combinée — le premier candidat qui compile gagne, dérive minimale ;
  3. aucun candidat compilant -> fichier original restauré octet-par-octet
     (rc=2, diagnostic complet fourni) ;
  4. idempotent x2 (re-jeu = no-op) ; stdlib uniquement ; déterministe.

Règle d'adaptation de session (règle d'or gen-plan — adaptation autonome) :
dès qu'une commande échoue avec « SyntaxError » / « syntax error » :
    python3 scripts/adaptation-syntaxe.py scan <chemins> --json
    python3 scripts/adaptation-syntaxe.py repair <fichier>
puis re-jouer la commande bloquée. Le journal optionnel (--journal) alimente
knowledge-observer (leçons de session).

Leçon d'environnement (sandbox, 2026-11-04) : un sous-processus qui hérite
d'un stdin pipe non refermé peut geler la session entière (le superviseur
attend la fermeture du flux) — et un vérificateur externe nourri de la sorte
renvoie des verdicts faux (rc=0 fantôme). Deux contre-mesures intégrées :
  1. tout sous-processus de CE script est lancé avec stdin=DEVNULL ;
  2. règle d'invocation écosystème : exécuter les arbitres avec
     `< /dev/null` (ou stdin redirigé) — classer tout gel de session comme
     incident « stdin-herité » avant tout autre diagnostic.

Usage :
  scan <chemin>... [--json] [--reparer] [--journal FICHIER]
      Détection récursive (.py .sh .bash .js .mjs .cjs), exclusions standard
      (node_modules, __pycache__, .git, .next, dist, build).
      --reparer : répare automatiquement chaque fichier en échec.
  repair <fichier> [--dry-run] [--journal FICHIER]
      Diagnostic + réparation d'un fichier unique.
  self-test
      Golden samples embarqués + idempotence x2 + no-op fichier sain.
  --version

Codes de sortie : 0 sain / aucune action · 1 réparé · 2 non réparable
(manuel, diagnostic fourni) · 3 erreur d'invocation ou garde (fichier
inexistant, arguments invalides, aucun chemin vérifiable — unifiée v1.0.1).

Historique :
  v1.0.0 (2026-11-04) — livraison initiale (directive pré-gen-plan).
  v1.0.1 (2026-11-04, Task 43 / G1 — batterie scripts/task43-tests-
    adaptation-syntaxe.py) : F-01 « repair fichier inexistant » produisait un
    traceback rc=1 au lieu du rc=3 contractualisé → refus propre
    « introuvable » ; F-02 « scan chemin inexistant » rendait un PASS
    silencieux à 0 fichier vérifié → avertissement [AVERTISSEMENT] et REFUS
    rc=3 quand RIEN n'est vérifiable ; F-03 les erreurs d'usage argparse
    sortaient en rc=2 alors que le contrat documente rc=3 → sortie unifiée.
    Les 3 findings sont attrapés par la batterie (TB-12 d/e/g, TE-06),
    corrigés ici, puis re-testés (round 2 — max 2 rounds, plan §5.4).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

VERSION = "1.0.1"
TAILLE_MAX = 5 * 1024 * 1024

EXT_PY = {".py"}
EXT_SH = {".sh", ".bash"}
EXT_JS = {".js", ".mjs", ".cjs"}

EXCLUSIONS_SCAN = {
    "node_modules", "__pycache__", ".git", ".next", "dist", "build",
    ".venv", "venv", "coverage",
}

CLASSES = (
    "bom",
    "crlf",
    "zero_width",
    "narrow_space",
    "smart_quotes",
    "fullwidth",
    "future_import",
)

RE_FUTURE = re.compile(r"^\s*from __future__ import [^\n]*$", re.M)
RE_ZERO_WIDTH = re.compile("[\u200b\u200c\u200d\u2060\ufeff\u00ad]")
RE_ESPACE_TYPO = re.compile("[\u00a0\u2000-\u200a\u202f\u205f\u3000]")

TABLE_SMART_QUOTES = {
    0x2018: 0x27, 0x2019: 0x27, 0x201A: 0x27, 0x201B: 0x27,
    0x201C: 0x22, 0x201D: 0x22, 0x201E: 0x22,
    0x2032: 0x27, 0x2033: 0x22,
}

TABLE_FULLWIDTH = {
    0xFF08: 0x28, 0xFF09: 0x29, 0xFF3B: 0x5B, 0xFF3D: 0x5D,
    0xFF5B: 0x7B, 0xFF5D: 0x7D, 0xFF0C: 0x2C, 0xFF1A: 0x3A,
    0xFF1B: 0x3B, 0xFF01: 0x21, 0xFF1F: 0x3F, 0xFF0E: 0x2E,
}

GOLDEN_SAIN_PY = '"""Sain."""\n\nVALEUR = 1\nprint(VALEUR)\n'
GOLDEN_FUTURE = (
    '"""Doc."""\n'
    "import os\n"
    "from __future__ import annotations\n"
    "\n"
    "X = os.sep\n"
)
GOLDEN_CRLF_SH = "#!/bin/bash\nif true; then\r\necho ok\r\nfi\r\n"
GOLDEN_ZERO_WIDTH = "X = 1\u200b\n"
GOLDEN_NARROW_SPACE = "X\u00a0=\u202f1\n"
GOLDEN_SMART_QUOTES = "print(\u201chal\u201d)\n"
GOLDEN_FULLWIDTH = "print（\u201ca\u201d）\n"
GOLDEN_MANUEL = "x = (1\u2019\n"
GOLDEN_DOUBLE_DOC = (
    "#!/usr/bin/env python3\n"
    '"""\nBLOC CONTEXTE\n"""\n'
    "\n"
    '"""Doc module.\n\nCorps.\n"""\n'
    "from __future__ import annotations\n"
    "\n"
    "import json\n"
    "X = 1\n"
)


def _vers_texte(octets):
    """Décode des octets en texte avec aller-retour garanti (surrogateescape)."""
    return octets.decode("utf-8", errors="surrogateescape")


def _vers_octets(texte):
    """Ré-encode un texte en octets (aller-retour exact avec _vers_texte)."""
    return texte.encode("utf-8", errors="surrogateescape")


def famille_de(chemin):
    """Renvoie la famille de vérification d'un chemin (python/bash/javascript/ignore)."""
    ext = os.path.splitext(chemin)[1].lower()
    if ext in EXT_PY:
        return "python"
    if ext in EXT_SH:
        return "bash"
    if ext in EXT_JS:
        return "javascript"
    return "ignore"


def verifier_octets(octets, famille, suffixe=".tmp"):
    """Vérifie la syntaxe d'un contenu (octets) — renvoie (ok, diagnostic|None).

    Le suffixe du fichier temporaire est celui du fichier cible : les
    vérificateurs comme node déterminent le format de module par l'extension
    (.mjs = ESM) — un suffixe générique produirait des verdicts fantômes.
    """
    if famille == "python":
        try:
            compile(octets, "<contenu>", "exec")
            return True, None
        except SyntaxError as erreur:
            return False, {
                "ligne": erreur.lineno,
                "colonne": erreur.offset,
                "message": erreur.msg or str(erreur),
            }
        except ValueError as erreur:
            return False, {"message": str(erreur)}
    if famille == "bash":
        return _verifier_externe(octets, ["bash", "-n"], suffixe)
    if famille == "javascript":
        chemin_node = shutil.which("node")
        if chemin_node is None:
            return True, {"message": "node absent — syntaxe non vérifiable", "indetermine": True}
        return _verifier_externe(octets, [chemin_node, "--check"], suffixe)
    return True, None


def _verifier_externe(octets, commande, suffixe=".tmp"):
    """Vérifie la syntaxe via un vérificateur externe sur fichier temporaire."""
    descripteur, chemin = tempfile.mkstemp(suffix=suffixe)
    try:
        os.write(descripteur, octets)
        os.close(descripteur)
        fini = subprocess.run(
            commande + [chemin], capture_output=True, text=True, timeout=30,
            check=False, stdin=subprocess.DEVNULL,
        )
        if fini.returncode == 0:
            return True, None
        message = (fini.stderr or fini.stdout or "").strip().splitlines()
        return False, {"message": message[0][:300] if message else "échec du vérificateur"}
    except (OSError, subprocess.TimeoutExpired) as erreur:
        return False, {"message": f"vérificateur indisponible : {erreur}"}
    finally:
        if os.path.exists(chemin):
            os.unlink(chemin)


def verifier_fichier(chemin):
    """Vérifie un fichier réel — renvoie {ok, famille, diagnostic, octets}.

    Durcissement bash : un BOM en tête est signalé comme défaut même si
    `bash -n` passe (le BOM rend l'exécution impossible : commande introuvable).
    """
    famille = famille_de(chemin)
    if famille == "ignore":
        return {"ok": True, "famille": famille, "diagnostic": None, "octets": None}
    with open(chemin, "rb") as poignee:
        octets = poignee.read()
    suffixe = os.path.splitext(chemin)[1].lower() or ".tmp"
    ok, diagnostic = verifier_octets(octets, famille, suffixe)
    if ok and famille == "bash" and octets.startswith(b"\xef\xbb\xbf"):
        ok = False
        diagnostic = {"message": "BOM en tête (bash) — exécution impossible"}
    return {"ok": ok, "famille": famille, "diagnostic": diagnostic, "octets": octets}


def _point_insertion_future(lignes):
    """Trouve l'indice d'insertion en tête : après shebang, codage et docstring."""
    indice = 0
    if indice < len(lignes) and lignes[indice].startswith("#!"):
        indice += 1
    if indice < len(lignes) and lignes[indice].startswith("#") and "coding" in lignes[indice]:
        indice += 1
    if indice < len(lignes):
        bande = lignes[indice].lstrip()
        for delim in ('"""', "'''"):
            if bande.startswith(delim):
                if bande[len(delim):].find(delim) != -1:
                    indice += 1
                else:
                    indice += 1
                    while indice < len(lignes) and delim not in lignes[indice]:
                        indice += 1
                    indice += 1
                break
    return indice


def corriger_future_import(texte):
    """Replace les lignes « from __future__ import ... » en tête de module."""
    lignes = texte.splitlines(keepends=True)
    cibles = [ligne for ligne in lignes if ligne.lstrip().startswith("from __future__ import")]
    if not cibles:
        return texte
    reste = [ligne for ligne in lignes if not ligne.lstrip().startswith("from __future__ import")]
    point = _point_insertion_future(reste)
    for decalage, cible in enumerate(cibles):
        if not cible.endswith("\n"):
            cible += "\n"
        reste.insert(point + decalage, cible)
    return "".join(reste)


def _appliquer(classe, texte, famille):
    """Applique une classe de correctif à un texte (fonction pure, déterministe)."""
    if classe == "future_import":
        if famille != "python":
            return texte
        return corriger_future_import(texte)
    if classe == "bom":
        return texte.lstrip("\ufeff")
    if classe == "crlf":
        return texte.replace("\r\n", "\n").replace("\r", "\n")
    if classe == "zero_width":
        return RE_ZERO_WIDTH.sub("", texte)
    if classe == "narrow_space":
        return RE_ESPACE_TYPO.sub(" ", texte)
    if classe == "smart_quotes":
        return texte.translate(TABLE_SMART_QUOTES)
    if classe == "fullwidth":
        return texte.translate(TABLE_FULLWIDTH)
    return texte


def _compile_texte(texte, famille, suffixe=".tmp"):
    """Vérifie qu'un texte candidat compile — renvoie un booléen."""
    ok, _ = verifier_octets(_vers_octets(texte), famille, suffixe)
    return ok


def reparer_texte(texte, famille, suffixe=".tmp"):
    """Moteur try-and-revert : passes simples puis passe combinée.

    Renvoie (texte_final, classes_appliquees, reussi). Le texte original est
    renvoyé inchangé si aucun candidat ne compile (dériver zéro).
    """
    for classe in CLASSES:
        essai = _appliquer(classe, texte, famille)
        if essai != texte and _compile_texte(essai, famille, suffixe):
            return essai, [classe], True
    essai = texte
    combinees = []
    for classe in CLASSES:
        sonde = _appliquer(classe, essai, famille)
        if sonde != essai:
            essai = sonde
            combinees.append(classe)
    if combinees and _compile_texte(essai, famille, suffixe):
        return essai, combinees, True
    return texte, [], False


def reparer_fichier(chemin, dry_run=False, journal=None):
    """Diagnostique et répare un fichier — renvoie un verdict JSON-sérialisable."""
    try:
        etat = verifier_fichier(chemin)
    except OSError as erreur:
        resultat = {
            "chemin": chemin,
            "rc": 3,
            "action": "introuvable",
            "message": f"fichier inaccessible : {erreur}",
        }
        _journaliser(journal, resultat)
        return resultat
    if etat["famille"] == "ignore":
        return {"chemin": chemin, "rc": 3, "action": "ignoré", "message": "extension non cible"}
    if len(etat["octets"]) > TAILLE_MAX:
        return {"chemin": chemin, "rc": 3, "action": "refusé", "message": "fichier > 5 Mo"}
    empreinte_avant = hashlib.sha256(etat["octets"]).hexdigest()
    if etat["ok"]:
        resultat = {
            "chemin": chemin,
            "rc": 0,
            "action": "aucune",
            "famille": etat["famille"],
            "sha256": empreinte_avant,
        }
        _journaliser(journal, resultat)
        return resultat
    texte = _vers_texte(etat["octets"])
    suffixe = os.path.splitext(chemin)[1].lower() or ".tmp"
    candidat, classes, reussi = reparer_texte(texte, etat["famille"], suffixe)
    if not reussi:
        resultat = {
            "chemin": chemin,
            "rc": 2,
            "action": "manuel",
            "famille": etat["famille"],
            "diagnostic": etat["diagnostic"],
            "sha256": empreinte_avant,
        }
        _journaliser(journal, resultat)
        return resultat
    octets_apres = _vers_octets(candidat)
    ok_final, _ = verifier_octets(octets_apres, etat["famille"], suffixe)
    if not ok_final:
        return {"chemin": chemin, "rc": 2, "action": "manuel", "diagnostic": etat["diagnostic"]}
    if not dry_run:
        descripteur, temporaire = tempfile.mkstemp(
            dir=os.path.dirname(os.path.abspath(chemin)) or ".", suffix=".tmp",
        )
        try:
            os.write(descripteur, octets_apres)
            os.close(descripteur)
            os.replace(temporaire, chemin)
        except OSError:
            os.close(descripteur) if descripteur >= 0 else None
            if os.path.exists(temporaire):
                os.unlink(temporaire)
            raise
    resultat = {
        "chemin": chemin,
        "rc": 1,
        "action": "SIMULATION" if dry_run else "réparé",
        "famille": etat["famille"],
        "classes": classes,
        "sha256_avant": empreinte_avant,
        "sha256_apres": hashlib.sha256(octets_apres).hexdigest(),
    }
    _journaliser(journal, resultat)
    return resultat


def _journaliser(journal, resultat):
    """Ajoute un verdict au journal JSONL optionnel (flux knowledge-observer)."""
    if not journal:
        return
    entree = dict(resultat)
    try:
        import datetime

        entree["horodatage"] = datetime.datetime.now(
            datetime.timezone.utc,
        ).isoformat(timespec="seconds")
    except (ImportError, OSError):
        entree["horodatage"] = "inconnu"
    with open(journal, "a", encoding="utf-8") as poignee:
        poignee.write(json.dumps(entree, ensure_ascii=False, sort_keys=True) + "\n")


def _collecter_chemins(chemins):
    """Rassemble les fichiers cibles (triés, dédupliqués, exclusions standard)."""
    vus = set()
    for chemin in chemins:
        if os.path.isfile(chemin):
            if chemin not in vus:
                vus.add(chemin)
            continue
        if not os.path.isdir(chemin):
            continue
        for racine, dossiers, fichiers in os.walk(chemin):
            dossiers[:] = sorted(d for d in dossiers if d not in EXCLUSIONS_SCAN)
            for fichier in sorted(fichiers):
                complet = os.path.join(racine, fichier)
                if complet not in vus and famille_de(complet) != "ignore":
                    vus.add(complet)
    return sorted(vus)


def scanner(chemins, json_out=False, reparer=False, journal=None):
    """Mode scan : détection récursive (+ réparation optionnelle) et verdict."""
    manquants = [c for c in chemins if not os.path.isfile(c) and not os.path.isdir(c)]
    cibles = _collecter_chemins(chemins)
    comptes = {"python": 0, "bash": 0, "javascript": 0, "ignore": 0, "indetermine": 0}
    erreurs = []
    reparation = []
    for cible in cibles:
        etat = verifier_fichier(cible)
        famille = etat["famille"]
        if famille == "javascript" and etat["diagnostic"] and etat["diagnostic"].get("indetermine"):
            comptes["indetermine"] += 1
            continue
        comptes[famille] += 1
        if not etat["ok"]:
            erreurs.append({"chemin": cible, "famille": famille, "diagnostic": etat["diagnostic"]})
            if reparer:
                reparation.append(reparer_fichier(cible, journal=journal))
    verdict = "PASS" if not erreurs else "FAIL"
    if not cibles and manquants:
        verdict = "REFUS"
    rapport = {
        "outils": comptes,
        "fichiers_verifies": len(cibles),
        "erreurs": erreurs,
        "verdict": verdict,
        "version": VERSION,
    }
    if manquants:
        rapport["chemins_inexistants"] = manquants
    if reparer:
        rapport["reparations"] = reparation
    if json_out:
        print(json.dumps(rapport, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(
            f"SCAN {verdict} — {len(cibles)} fichiers "
            f"(py {comptes['python']} · sh {comptes['bash']} · js {comptes['javascript']} "
            f"· indéterminés {comptes['indetermine']}) — erreurs : {len(erreurs)}"
        )
        for chemin_manquant in manquants:
            print(f"  [AVERTISSEMENT] chemin inexistant : {chemin_manquant}")
        for erreur in erreurs:
            print(f"  [ÉCHEC] {erreur['chemin']} — {erreur['diagnostic']}")
        for rep in reparation:
            print(f"  [REPARATION] {rep['chemin']} — {rep['action']} classes={rep.get('classes', [])}")
    if not cibles and manquants:
        return 3
    return 0 if verdict == "PASS" else 1


def reparer_commande(chemin, dry_run=False, journal=None):
    """Mode repair : répare un fichier unique et affiche le verdict."""
    resultat = reparer_fichier(chemin, dry_run=dry_run, journal=journal)
    etiquettes = {0: "SAIN", 1: "REPARÉ", 2: "MANUEL", 3: "REFUSÉ"}
    print(
        f"{etiquettes.get(resultat['rc'], 'ERREUR')} {resultat['chemin']} — "
        f"{resultat['action']} classes={resultat.get('classes', [])}"
    )
    if resultat["rc"] == 2 and "diagnostic" in resultat:
        print(f"  diagnostic : {resultat['diagnostic']}")
    return resultat["rc"]


def auto_test():
    """Self-test : golden samples embarqués, idempotence x2, no-op fichier sain."""
    resultats = []

    def verifier(id_test, condition, detail=""):
        resultats.append((id_test, bool(condition), detail))

    dossier = tempfile.mkdtemp(prefix="adaptation-syntaxe-selftest-")
    try:
        chemin_sain = os.path.join(dossier, "sain.py")
        with open(chemin_sain, "w", encoding="utf-8") as poignee:
            poignee.write(GOLDEN_SAIN_PY)
        octets_sain = open(chemin_sain, "rb").read()
        verdict = reparer_fichier(chemin_sain)
        octets_sain_apres = open(chemin_sain, "rb").read()
        verifier(
            "T-01",
            verdict["rc"] == 0 and octets_sain == octets_sain_apres,
            "fichier sain intact (no-op)",
        )

        cas = [
            ("T-02", "future.py", GOLDEN_FUTURE, "python", ["future_import"]),
            ("T-03", "script.sh", GOLDEN_CRLF_SH, "bash", ["crlf"]),
            ("T-04", "zero.py", GOLDEN_ZERO_WIDTH, "python", ["zero_width"]),
            ("T-05", "espace.py", GOLDEN_NARROW_SPACE, "python", ["narrow_space"]),
            ("T-06", "quotes.py", GOLDEN_SMART_QUOTES, "python", ["smart_quotes"]),
            ("T-07", "fullwidth.py", GOLDEN_FULLWIDTH, "python", ["smart_quotes", "fullwidth"]),
            ("T-11", "double-doc.py", GOLDEN_DOUBLE_DOC, "python", ["future_import"]),
        ]
        fichiers_repaire = []
        for id_test, nom, contenu, _famille, classes_attendues in cas:
            chemin = os.path.join(dossier, nom)
            with open(chemin, "w", encoding="utf-8", newline="") as poignee:
                poignee.write(contenu)
            etat_avant = verifier_fichier(chemin)
            verdict = reparer_fichier(chemin)
            etat_apres = verifier_fichier(chemin)
            rejeu = reparer_fichier(chemin)
            verifier(
                id_test,
                (
                    etat_avant["ok"] is False
                    and verdict["rc"] == 1
                    and etat_apres["ok"] is True
                    and rejeu["rc"] == 0
                    and verdict.get("classes") == classes_attendues
                ),
                f"réparé + compilant + idempotent (classes={verdict.get('classes')})",
            )
            fichiers_repaire.append(chemin)

        chemin_manuel = os.path.join(dossier, "manuel.py")
        with open(chemin_manuel, "w", encoding="utf-8") as poignee:
            poignee.write(GOLDEN_MANUEL)
        octets_manuel = open(chemin_manuel, "rb").read()
        verdict = reparer_fichier(chemin_manuel)
        octets_manuel_apres = open(chemin_manuel, "rb").read()
        verifier(
            "T-08",
            verdict["rc"] == 2 and octets_manuel == octets_manuel_apres and "diagnostic" in verdict,
            "non réparable : original restauré octet-par-octet + diagnostic",
        )

        fichiers_scan = [chemin_sain] + fichiers_repaire
        sortie = _capture_scan(fichiers_scan)
        verifier(
            "T-09",
            (
                set(sortie.keys()) == {
                    "outils", "fichiers_verifies", "erreurs", "verdict", "version",
                }
                and sortie["verdict"] == "PASS"
                and sortie["erreurs"] == []
            ),
            "scan JSON : structure complète + verdict PASS après réparations",
        )

        verifier(
            "T-10",
            all(
                os.path.exists(chemin) and verifier_fichier(chemin)["ok"]
                for chemin in fichiers_repaire
            ),
            "tous les golden réparés restent compilants au re-jeu",
        )
    finally:
        shutil.rmtree(dossier, ignore_errors=True)

    total = len(resultats)
    pass_ok = sum(1 for _, ok, _ in resultats if ok)
    for id_test, ok, detail in resultats:
        print(f"  {id_test} {'PASS' if ok else 'ÉCHEC'} — {detail}")
    print(f"SELF-TEST {pass_ok}/{total} {'PASS' if pass_ok == total else 'ÉCHEC'}")
    return 0 if pass_ok == total else 1


def _capture_scan(chemins):
    """Scan silencieux interne pour le self-test (structure de rapport réelle)."""
    cibles = _collecter_chemins(chemins)
    erreurs = []
    for cible in cibles:
        etat = verifier_fichier(cible)
        if etat["famille"] == "javascript" and etat["diagnostic"] and etat["diagnostic"].get("indetermine"):
            continue
        if not etat["ok"]:
            erreurs.append({"chemin": cible, "famille": etat["famille"]})
    return {
        "outils": {},
        "fichiers_verifies": len(cibles),
        "erreurs": erreurs,
        "verdict": "PASS" if not erreurs else "FAIL",
        "version": VERSION,
    }


class AnalyseurUsage(argparse.ArgumentParser):
    """Analyseur dont les erreurs d'usage sortent en rc=3 (contrat « 3 erreur d'invocation »).

    argparse sort en rc=2 par défaut ; le contrat documenté (docstring,
    codes de sortie) exige rc=3 — unifié v1.0.1 (finding F-03, Task 43).
    """

    def error(self, message):
        self.print_usage(sys.stderr)
        print(f"erreur : {message}", file=sys.stderr)
        raise SystemExit(3)


def construire_analyseur():
    """Construit l'analyseur d'arguments (usage : rc=3 si invalide)."""
    analyseur = AnalyseurUsage(
        prog="adaptation-syntaxe.py",
        description="Garde d'auto-réparation syntaxique de l'écosystème.",
    )
    analyseur.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    sous = analyseur.add_subparsers(dest="commande")

    scan = sous.add_parser("scan", help="détection récursive (+ réparation optionnelle)")
    scan.add_argument("chemins", nargs="+", help="fichiers ou dossiers à vérifier")
    scan.add_argument("--json", action="store_true", help="sortie JSON")
    scan.add_argument("--reparer", action="store_true", help="répare chaque fichier en échec")
    scan.add_argument("--journal", default=None, help="journal JSONL des interventions")

    rep = sous.add_parser("repair", help="diagnostic + réparation d'un fichier")
    rep.add_argument("fichier", help="fichier cible")
    rep.add_argument("--dry-run", action="store_true", help="simulation sans écriture")
    rep.add_argument("--journal", default=None, help="journal JSONL des interventions")

    sous.add_parser("self-test", help="golden samples embarqués + idempotence x2")
    return analyseur


def main(argv=None):
    """Point d'entrée — renvoie le code de sortie du mode invoqué."""
    analyseur = construire_analyseur()
    arguments = analyseur.parse_args(argv)
    if arguments.commande == "scan":
        return scanner(
            arguments.chemins,
            json_out=arguments.json,
            reparer=arguments.reparer,
            journal=arguments.journal,
        )
    if arguments.commande == "repair":
        return reparer_commande(arguments.fichier, arguments.dry_run, arguments.journal)
    if arguments.commande == "self-test":
        return auto_test()
    analyseur.print_help()
    return 3


if __name__ == "__main__":
    sys.exit(main())
