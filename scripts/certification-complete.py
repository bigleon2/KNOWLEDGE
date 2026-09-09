#!/usr/bin/env python3
"""certification complète de l'écosystème — orchestrateur des 5 arbitres.

Session B7 : codification en une commande unique de la chaîne de certification
gen-plan:correct-work(projet) exécutée manuellement dans les sessions B5-B9
(chaque session relançait les 5 arbitres puis consolidait les verdicts à la main).

Arbitres orchestrés (ordre canonique du worklog, chemins relatifs à __file__ —
fonctionne dans le sandbox comme dans le véhicule de publication) :
  1. verify-cross.py — axes 1-6, mode défaut (source = download/)
  2. verify-cross.py --mode correct-work — checks 7-8 (KB + frontmatter métier)
  3. skills/correct-work/scripts/verify-correct-work.py — v2.5.1 (calibré B1)
  4. check-ecosysteme-integrity.py — corpus, miroir, KB, evals (34 checks)
  5. test-coherence-interactions.py — interactions + §11b clone de référence
     (BASE codée en dur vers le sandbox, création B5 : teste le contenu source,
     identique au véhicule par construction de l'overlay rsync)

Option --environnement : pré-vol supplémentaire — clone de référence
/tmp/KNOWLEDGE_CHECK pristine (a8ffb5f), état du véhicule /tmp/KNOWLEDGE_PUSH,
HEAD distant (git ls-remote anonyme). Dégradé en ATTENTION (jamais en échec)
si le réseau ou les chemins /tmp sont indisponibles : le verdict consolidé ne
dépend que des 5 arbitres.

Option --verbose : affiche la sortie complète de chaque arbitre (sinon, la
sortie complète n'est affichée que pour un arbitre en échec, à des fins de
diagnostic).

Rapport : scripts/certification-report.json — déterministe (aucun
horodatage, clés triées) pour préserver la propriété « drift zéro » des
artefacts démontrée en Task 9 (rsync -rcn vide après régénération).

Code retour : 0 si et seulement si les 5 arbitres sont verts.
Utilisation :
  python3 scripts/certification-complete.py
  python3 scripts/certification-complete.py --environnement [--verbose]
"""

import json
import re
import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
BASE_DIR = SCRIPTS.parent
RAPPORT = SCRIPTS / "certification-report.json"

# Chemins d'environnement des sessions B5+ (option --environnement)
CLONE_REF = Path("/tmp/KNOWLEDGE_CHECK")
VEHICULE = Path("/tmp/KNOWLEDGE_PUSH")
DEPOT_DISTANT = "https://github.com/bigleon2/KNOWLEDGE.git"
BASELINE_A8FFB5F = "a8ffb5fd72ba143f5cb8b0800b33aba48d6e20ba"

MODE_ENV = "--environnement" in sys.argv
MODE_VERBOSE = "--verbose" in sys.argv

ARBITRES = [
    ("verify-cross (axes 1-6)",
     [sys.executable, str(SCRIPTS / "verify-cross.py")],
     "cross_defaut"),
    ("verify-cross (mode correct-work)",
     [sys.executable, str(SCRIPTS / "verify-cross.py"), "--mode", "correct-work"],
     "cross_correct_work"),
    ("verify-correct-work v2.5.1",
     [sys.executable, str(BASE_DIR / "skills" / "correct-work" / "scripts" / "verify-correct-work.py")],
     "correct_work"),
    ("check-ecosysteme-integrity",
     [sys.executable, str(SCRIPTS / "check-ecosysteme-integrity.py")],
     "integrite"),
    ("test-coherence-interactions (§11b)",
     [sys.executable, str(SCRIPTS / "test-coherence-interactions.py")],
     "interactions"),
]


def dernier(pattern, texte):
    """Dernière occurrence du pattern (les RESUME terminent la sortie)."""
    trouves = re.findall(pattern, texte)
    return trouves[-1] if trouves else None


def extraire(cle, sortie):
    """(pass, total, échecs, avertissements, verdict brut) du RESUME/BILAN de l'arbitre.

    Formats stables observés B4-B9 (les libellés générateur suivent les
    conventions de session documentées au worklog) :
      verify-cross        : « PASS : N » / « FAIL : M » / « VERDICT : ALL PASS »
      verify-correct-work : « PASS  : N/N » / « FAIL  : M/N » / « VERDICT : ... »
      check-ecosystème    : « === RESUME : N/N PASS, M FAIL === »
      interactions        : « BILAN : N PASS / W WARN / M FAIL — N checks »
    """
    if cle in ("cross_defaut", "cross_correct_work"):
        p = dernier(r"PASS\s*:\s*(\d+)", sortie)
        f = dernier(r"FAIL\s*:\s*(\d+)", sortie)
        v = dernier(r"VERDICT\s*:\s*(.+)", sortie)
        if p is None or f is None:
            return 0, 0, 1, 0, "NON PARSÉ"
        pass_, echecs = int(p), int(f)
        return pass_, pass_ + echecs, echecs, 0, (v.strip() if v else "ABSENT")

    if cle == "correct_work":
        p = dernier(r"PASS\s*:\s*(\d+)/(\d+)", sortie)
        f = dernier(r"FAIL\s*:\s*(\d+)/(\d+)", sortie)
        v = dernier(r"VERDICT\s*:\s*(.+)", sortie)
        if p is None:
            return 0, 0, 1, 0, "NON PARSÉ"
        pass_, total = int(p[0]), int(p[1])
        echecs = int(f[0]) if f else total - pass_
        return pass_, total, echecs, 0, (v.strip() if v else "ABSENT")

    if cle == "integrite":
        m = dernier(r"(\d+)/(\d+)\s*PASS,\s*(\d+)\s*FAIL", sortie)
        if m is None:
            return 0, 0, 1, 0, "NON PARSÉ"
        pass_, total, echecs = int(m[0]), int(m[1]), int(m[2])
        verdict = "ALL PASS" if (echecs == 0 and pass_ == total) else "FAIL"
        return pass_, total, echecs, 0, verdict

    m = dernier(r"BILAN\s*:\s*(\d+)\s*PASS\s*/\s*(\d+)\s*WARN\s*/\s*(\d+)\s*FAIL", sortie)
    v = dernier(r"VERDICT\s*:\s*(.+)", sortie)
    if m is None:
        return 0, 0, 1, 0, "NON PARSÉ"
    pass_, avert, echecs = int(m[0]), int(m[1]), int(m[2])
    return pass_, pass_ + avert + echecs, echecs, avert, (v.strip() if v else "ABSENT")


def est_vert(cle, pass_, total, echecs, avert, verdict):
    """Critère de verdure par arbitre (calqué sur les verdicts de session)."""
    if cle in ("cross_defaut", "cross_correct_work"):
        return echecs == 0 and verdict == "ALL PASS"
    if cle == "correct_work":
        return echecs == 0 and pass_ == total and verdict == "ALL PASS"
    if cle == "integrite":
        return echecs == 0 and pass_ == total
    return echecs == 0 and avert == 0 and "PASS STRICT" in verdict


def lancer_arbitre(nom, commande, cle):
    """Exécute un arbitre, parse son bilan, renvoie l'entrée de rapport."""
    print(f"--- {nom} ---")
    try:
        proc = subprocess.run(commande, capture_output=True, text=True,
                              encoding="utf-8", errors="replace", timeout=900)
        sortie = (proc.stdout or "") + (proc.stderr or "")
    except subprocess.TimeoutExpired:
        print("  [ÉCHEC] ERREUR D'EXÉCUTION (timeout 900 s)")
        return {"nom": nom, "cle": cle, "pass": 0, "total": 0, "echecs": 1,
                "avertissements": 0, "verdict": "ERREUR D'EXÉCUTION (timeout)",
                "vert": False}

    pass_, total, echecs, avert, verdict = extraire(cle, sortie)
    vert = est_vert(cle, pass_, total, echecs, avert, verdict)
    if MODE_VERBOSE or not vert:
        print(sortie.rstrip())
    etat = "OK" if vert else "ÉCHEC"
    print(f"  [{etat}] {verdict} ({pass_}/{total} — {echecs} échec, {avert} avertissement)")
    return {"nom": nom, "cle": cle, "pass": pass_, "total": total,
            "echecs": echecs, "avertissements": avert, "verdict": verdict,
            "vert": vert}


def git(*args, cwd=None, timeout=30):
    return subprocess.run(["git", *args], capture_output=True, text=True,
                          encoding="utf-8", errors="replace", timeout=timeout, cwd=cwd)


def verifier_environnement():
    """Pré-vol B9 : clone §11b pristine, véhicule, HEAD distant (anonyme).

    Renvoie [(libellé, statut 'OK'/'ATTENTION'/'INFO', détail)] — jamais
    comptabilisé dans le verdict consolidé (dégradation en ATTENTION).
    """
    notes = []

    # 1. Clone de référence §11b
    if CLONE_REF.is_dir():
        tete = git("rev-parse", "HEAD", cwd=str(CLONE_REF))
        statut = git("status", "--porcelain", cwd=str(CLONE_REF))
        propre = statut.returncode == 0 and statut.stdout.strip() == ""
        a_la_base = tete.returncode == 0 and tete.stdout.strip() == BASELINE_A8FFB5F
        court = tete.stdout.strip()[:7] if tete.returncode == 0 else "?"
        ok = propre and a_la_base
        detail = f"HEAD {court}" + (", 0 fichier modifié" if propre else ", fichiers modifiés")
        notes.append(("clone de référence §11b (pristine a8ffb5f)",
                      "OK" if ok else "ATTENTION", detail))
    else:
        notes.append(("clone de référence §11b (pristine a8ffb5f)",
                      "INFO", "absent de cet environnement (§11b non vérifiable)"))

    # 2. Véhicule de publication
    tete_vehicule = None
    if VEHICULE.is_dir():
        tete = git("rev-parse", "HEAD", cwd=str(VEHICULE))
        statut = git("status", "--porcelain", cwd=str(VEHICULE))
        propre = statut.returncode == 0 and statut.stdout.strip() == ""
        tete_vehicule = tete.stdout.strip() if tete.returncode == 0 else None
        court = tete_vehicule[:7] if tete_vehicule else "?"
        notes.append(("véhicule de publication /tmp/KNOWLEDGE_PUSH",
                      "OK" if propre else "ATTENTION",
                      f"HEAD {court}, statut " + ("propre" if propre else "sale")))
    else:
        notes.append(("véhicule de publication /tmp/KNOWLEDGE_PUSH",
                      "INFO", "absent de cet environnement"))

    # 3. HEAD distant (anonyme — aucun jeton requis ni utilisé)
    try:
        r = git("ls-remote", DEPOT_DISTANT, "refs/heads/main", timeout=30)
        if r.returncode == 0 and r.stdout.strip():
            tete_distante = r.stdout.split()[0]
            if tete_vehicule:
                synchronise = tete_distante == tete_vehicule
                notes.append(("dépôt distant (ls-remote anonyme)",
                              "OK" if synchronise else "ATTENTION",
                              f"main = {tete_distante[:7]}"
                              + ("" if synchronise else f" (diffère du véhicule {tete_vehicule[:7]})")))
            else:
                notes.append(("dépôt distant (ls-remote anonyme)",
                              "INFO", f"main = {tete_distante[:7]} (véhicule absent, non comparé)"))
        else:
            notes.append(("dépôt distant (ls-remote anonyme)",
                          "ATTENTION", "inaccessible (réseau ?)"))
    except (subprocess.TimeoutExpired, OSError):
        notes.append(("dépôt distant (ls-remote anonyme)",
                      "ATTENTION", "inaccessible (réseau ?)"))

    return notes


def main():
    print("=== CERTIFICATION COMPLÈTE — orchestrateur des 5 arbitres (session B7) ===")
    resultats = [lancer_arbitre(nom, commande, cle) for nom, commande, cle in ARBITRES]
    notes_env = verifier_environnement() if MODE_ENV else []

    verts = sum(1 for r in resultats if r["vert"])
    if verts == len(ARBITRES):
        verdict_global = "CERTIFICATION COMPLÈTE : ALL PASS"
    else:
        verdict_global = (f"CERTIFICATION INCOMPLÈTE : "
                          f"{len(ARBITRES) - verts} arbitre(s) en échec")

    print()
    print("=" * 64)
    print("=== RESUME CONSOLIDÉ ===")
    for i, r in enumerate(resultats, 1):
        etat = "OK" if r["vert"] else "ÉCHEC"
        print(f"  [{i}/{len(resultats)}] {r['nom']:<40} "
              f"{r['verdict']} ({r['pass']}/{r['total']}) [{etat}]")
    if notes_env:
        print("  --- environnement (--environnement) : informational, hors verdict ---")
        for libelle, statut, detail in notes_env:
            print(f"  {libelle:<56} [{statut}] {detail}")
    print(f"  VERDICT : {verdict_global} ({verts}/{len(ARBITRES)})")
    print(f"Rapport JSON : scripts/{RAPPORT.name}")

    rapport = {
        "arbitres": resultats,
        "consolide": {
            "arbitres_verts": verts,
            "arbitres_total": len(ARBITRES),
            "verdict": verdict_global,
        },
    }
    if notes_env:
        rapport["environnement"] = [
            {"verifiant": libelle, "statut": statut, "detail": detail}
            for libelle, statut, detail in notes_env
        ]
    RAPPORT.write_text(json.dumps(rapport, ensure_ascii=False, indent=2,
                                  sort_keys=True), encoding="utf-8")

    sys.exit(0 if verts == len(ARBITRES) else 1)


if __name__ == "__main__":
    main()
