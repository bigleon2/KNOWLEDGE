#!/usr/bin/env python3
"""scaffold_tests.py — générateur idempotent de batterie de tests (M7 TESTER).

Skill cahier-des-charges v2.0.0 — scripts/ — stdlib Python uniquement (N3).

Crée <out>/batterie-tests-<projet>/ :
  - run_all.py              harnais d'exécution (sous-processus, journal/synthese.json)
  - matrice-couverture.md   matrice exigences <-> tests pré-remplie
  - tests_fonctionnels/     tf_NN_<exigence>.py — un squelette par exigence fournie
  - tests_materiel/         th_NN_sous_systeme.py — N squelettes (exemple PID/thermique fonctionnel)
  - journal/                journaux JSON (écrits à l'exécution des tests)

IDEMPOTENCE ×2 : un fichier existant n'est JAMAIS écrasé (création si absent seulement) —
re-scaffold sans modification = octets identiques ; les tests déjà adaptés sont conservés.
Protocole STATUT : tout squelette porte STATUT = "NON_IMPLÉMENTÉ" — run_all.py ne l'exécute
pas tant que l'implémentation ne l'a pas passé à "PRÊT" (un squelette ne prouve rien, R3).

Usage :
    python3 scaffold_tests.py --projet serre-cbd --out download \\
        [--exigences EF-01,EF-02,ENF-01] [--th 1] [--profil mini|standard|complexe]
    python3 scaffold_tests.py --selftest
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

VERSION = "2.0.0"
SKILL = "cahier-des-charges"
SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
EXIGENCE_RE = re.compile(r"^[A-Z]{2,4}-\d{2,}$")

CIBLES_COUVERTURE = {
    "mini": "exigences critiques couvertes par >= 1 test PASS + 1 TH représentatif",
    "standard": "100 % des exigences couvertes par >= 1 test PASS ; TH par sous-système matériel",
    "complexe": ("100 % des exigences couvertes ; TH par sous-système ET par interface "
                 "+ campagne de robustesse (bruit, tolérances)"),
}

# ------------------------------------------------------------ gabarits -------

RUN_ALL_TEMPLATE = '''#!/usr/bin/env python3
"""run_all.py — harnais d'exécution de la batterie batterie-tests-@PROJET@.

Généré par scaffold_tests.py v@VERSION@ (skill @SKILL@). stdlib uniquement.

Protocole STATUT (en-tête de chaque test) :
  - STATUT = "NON_IMPLÉMENTÉ" -> test NON exécuté (squelette : un squelette ne prouve rien, R3) ;
  - STATUT = "PRÊT" ou absent (patron references/simulation-materielle.md) -> exécution en
    sous-processus, verdict = code retour (0 = PASS, sinon ECHEC).

Verdict global : PASS si >= 1 test et tous PASS ; ECHEC si >= 1 ECHEC ; NON_IMPLÉMENTÉ si des
squelettes restent à adapter ; AUCUN_TEST si la batterie est vide.
Code sortie : 0 tout PASS ; 1 au moins un ECHEC ; 2 au moins un NON_IMPLÉMENTÉ (sans ECHEC) ;
3 aucun test.
"""
import json
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

RACINE = Path(__file__).resolve().parent
PROJET = "@PROJET@"
TIMEOUT_S = 300
RE_STATUT = re.compile(r'^STATUT\\s*=\\s*"([^"]+)"', re.M)
RE_ID = re.compile(r"^(tf|th)_(\\d+)", re.I)
JOURNAL = RACINE / "journal" / "synthese.json"


def statut_du_test(chemin):
    m = RE_STATUT.search(chemin.read_text(encoding="utf-8"))
    return m.group(1) if m else "PRÊT"


def id_du_test(chemin):
    m = RE_ID.match(chemin.stem)
    if m:
        return f"{m.group(1).upper()}-{int(m.group(2)):02d}"
    return chemin.stem.upper()


def decouvrir():
    tests = []
    for sous_dossier, motif in (("tests_fonctionnels", "tf_*.py"), ("tests_materiel", "th_*.py")):
        dossier = RACINE / sous_dossier
        if dossier.is_dir():
            tests.extend(sorted(dossier.glob(motif)))
    return tests


def main():
    resultats = []
    for chemin in decouvrir():
        statut = statut_du_test(chemin)
        if statut == "NON_IMPLÉMENTÉ":
            resultats.append({"id": id_du_test(chemin), "test": chemin.name, "statut": statut,
                              "verdict": "NON_IMPLÉMENTÉ", "code_retour": None, "duree_s": 0.0,
                              "sortie": "squelette non exécuté — à adapter puis STATUT=PRÊT"})
            continue
        debut = time.monotonic()
        try:
            proc = subprocess.run([sys.executable, str(chemin)], capture_output=True,
                                  text=True, timeout=TIMEOUT_S, cwd=str(RACINE))
            code = proc.returncode
            sortie = ((proc.stdout or "") + (proc.stderr or "")).strip()
        except subprocess.TimeoutExpired:
            code, sortie = 1, f"ECHEC — TIMEOUT > {TIMEOUT_S} s"
        resultats.append({"id": id_du_test(chemin), "test": chemin.name, "statut": statut,
                          "verdict": "PASS" if code == 0 else "ECHEC", "code_retour": code,
                          "duree_s": round(time.monotonic() - debut, 3), "sortie": sortie[-2000:]})
    verdicts = [r["verdict"] for r in resultats]
    if not resultats:
        verdict_global, code_sortie = "AUCUN_TEST", 3
    elif "ECHEC" in verdicts:
        verdict_global, code_sortie = "ECHEC", 1
    elif "NON_IMPLÉMENTÉ" in verdicts:
        verdict_global, code_sortie = "NON_IMPLÉMENTÉ", 2
    else:
        verdict_global, code_sortie = "PASS", 0
    synthese = {
        "projet": PROJET,
        "horodatage": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "verdict_global": verdict_global,
        "total": len(resultats),
        "passes": verdicts.count("PASS"),
        "echecs": verdicts.count("ECHEC"),
        "non_implementes": verdicts.count("NON_IMPLÉMENTÉ"),
        "tests": resultats,
    }
    JOURNAL.parent.mkdir(parents=True, exist_ok=True)
    JOURNAL.write_text(json.dumps(synthese, indent=2, ensure_ascii=False), encoding="utf-8")
    for r in resultats:
        derniere = r["sortie"].splitlines()[-1] if r["sortie"] else ""
        print(f"{r['verdict']:<16} {r['id']} ({r['test']}) {derniere}")
    print(f"VERDICT GLOBAL : {verdict_global} — {synthese['passes']} PASS / "
          f"{synthese['echecs']} ECHEC / {synthese['non_implementes']} NON_IMPLÉMENTÉ "
          f"(journal : journal/synthese.json)")
    raise SystemExit(code_sortie)


if __name__ == "__main__":
    main()
'''

TF_TEMPLATE = '''#!/usr/bin/env python3
"""@TF_ID@ : vérifie @EXIGENCE@ — <capacité observable : recopier du CDC §5/§6>.

Squelette généré par scaffold_tests.py v@VERSION@ (skill @SKILL@).
À ADAPTER (M7) :
  1. recopier le critère d'acceptation exécutable du CDC dans l'en-tête et dans verifier() ;
  2. implémenter les assertions — un check = (nom citant l'exigence, booléen, détail mesurable) ;
  3. passer STATUT à "PRÊT" — run_all.py exécutera alors ce test réellement.
Règle 12 : une exigence sans test couvrant est NON VÉRIFIABLE — jamais PASS allégué (R3).
"""
import json
from pathlib import Path

STATUT = "NON_IMPLÉMENTÉ"  # -> "PRÊT" après implémentation
EXIGENCES = @EXIGENCES_JSON@
JOURNAL = Path(__file__).resolve().parent.parent / "journal" / "@FICHIER@.json"


def verifier():
    """Retourne [(nom_check, bool, détail)] — chaque check cite son exigence (règle 12)."""
    # TODO(M7) : assertions exécutables du critère d'acceptation du CDC.
    return [("@EXIGENCE@ : critère d'acceptation à implémenter", False,
             "NON IMPLÉMENTÉ — squelette à adapter (voir en-tête du fichier)")]


def main():
    checks = verifier()
    verdict = "PASS" if all(ok for _, ok, _ in checks) else "ECHEC"
    JOURNAL.parent.mkdir(parents=True, exist_ok=True)
    JOURNAL.write_text(json.dumps(
        {"test": "@TF_ID@", "exigences": EXIGENCES, "statut": STATUT, "verdict": verdict,
         "checks": [{"nom": n, "ok": ok, "detail": d} for n, ok, d in checks]},
        indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    for nom, ok, detail in checks:
        print(("PASS" if ok else "ECHEC") + f" {nom} — {detail}")
    raise SystemExit(0 if verdict == "PASS" else 1)


if __name__ == "__main__":
    main()
'''

TH_TEMPLATE = '''#!/usr/bin/env python3
"""@TH_ID@ : simule <sous-système matériel à nommer> — boucle PID sur procédé thermique 1er ordre.

Squelette généré par scaffold_tests.py v@VERSION@ (skill @SKILL@) — exemple FONCTIONNEL selon
les patrons references/simulation-materielle.md (§2 Euler, §3 1er ordre, §4 capteur virtuel,
§5 actionneur saturé, §6 PID anti-windup). Déterministe (graine fixe), stdlib uniquement.

À ADAPTER (M7) : remplacer le procédé, les tolérances et les exigences rattachées par ceux du
dossier de conception (SS-xx), puis passer STATUT à "PRÊT". Tant que STATUT vaut
"NON_IMPLÉMENTÉ", run_all.py n'exécute PAS ce test (un squelette ne prouve rien, R3).
"""
import json
import random
from pathlib import Path

STATUT = "NON_IMPLÉMENTÉ"  # -> "PRÊT" après adaptation
EXIGENCES = @EXIGENCES_JSON@
JOURNAL = Path(__file__).resolve().parent.parent / "journal" / "@FICHIER@.json"

SEED = 42          # graine fixe — même verdict à chaque re-exécution (idempotence R1)
DT = 0.1           # s — pas discret (au moins 20x plus petit que TAU, patron §2)
T_END = 600.0      # s — durée simulée
TAU = 60.0         # s — constante de temps thermique du procédé
K_PROC = 15.0      # °C — gain statique (u=1 -> +K_PROC au-dessus de l'ambiant)
Y_AMB = 15.0       # °C — température ambiante (condition initiale)
CONSIGNE = 22.0    # °C
SIGMA = 0.2        # °C — bruit capteur (gaussien seedé)
BIAS = 0.1         # °C — biais capteur systématique
QUANT = 0.1        # °C — quantification du CAN
U_MIN, U_MAX = 0.0, 1.0       # saturation actionneur (patron §5)
KP, KI, KD = 0.12, 0.02, 0.8  # gains PID (à recaler sur le vrai procédé)
I_MIN, I_MAX = -20.0, 20.0    # bornage intégral (anti-windup, patron §6)
SEUIL_DEPASSEMENT = 1.5       # °C — exigence performance (à rattacher au CDC)
SEUIL_ERREUR = 0.5            # °C — erreur statique admise
SEUIL_STABILITE = 0.5         # °C — écart-type en régime établi


def mesurer(y, rng):
    """Capteur virtuel (patron §4) : bruit + biais + quantification."""
    return round((y + rng.gauss(0.0, SIGMA) + BIAS) / QUANT) * QUANT


def commander(u):
    """Actionneur virtuel (patron §5) : saturation."""
    return max(U_MIN, min(U_MAX, u))


def simuler():
    """Chaîne complète (patron §6) : consigne -> PID -> actionneur -> physique -> capteur."""
    rng = random.Random(SEED)
    y = Y_AMB
    integ = 0.0
    err_prec = CONSIGNE - Y_AMB
    trace = []
    t = 0.0
    while t <= T_END:
        y_mes = mesurer(y, rng)
        err = CONSIGNE - y_mes
        integ = max(I_MIN, min(I_MAX, integ + err * DT))
        deriv = (err - err_prec) / DT
        u = commander(KP * err + KI * integ + KD * deriv)
        err_prec = err
        y += DT * (K_PROC * u - (y - Y_AMB)) / TAU   # physique discrétisée (patron §3)
        trace.append({"t": round(t, 3), "y": y, "y_mes": y_mes, "u": u})
        t += DT
    return trace


def verifier(trace):
    """Vérifications à seuils — chaque check cite son exigence rattachée (règle 12)."""
    dernier = [p for p in trace if p["t"] >= T_END - 60.0]
    y_max = max(p["y"] for p in trace)
    moyenne = sum(p["y_mes"] for p in dernier) / len(dernier)
    ecart_type = (sum((p["y_mes"] - moyenne) ** 2 for p in dernier) / len(dernier)) ** 0.5
    return [
        ("dépassement < SEUIL_DEPASSEMENT (exigence ENF à rattacher)",
         y_max - CONSIGNE < SEUIL_DEPASSEMENT,
         f"max(y)={y_max:.2f} °C, consigne={CONSIGNE:.2f} °C, dépassement={y_max - CONSIGNE:.2f} °C"),
        ("erreur statique < SEUIL_ERREUR (exigence ENF à rattacher)",
         abs(moyenne - CONSIGNE) < SEUIL_ERREUR,
         f"moyenne(y_mes, 60 dernières s)={moyenne:.2f} °C"),
        ("stabilité en régime établi < SEUIL_STABILITE (exigence ENF à rattacher)",
         ecart_type < SEUIL_STABILITE,
         f"écart-type(y_mes, 60 dernières s)={ecart_type:.2f} °C"),
    ]


def main():
    trace = simuler()
    checks = verifier(trace)
    verdict = "PASS" if all(ok for _, ok, _ in checks) else "ECHEC"
    JOURNAL.parent.mkdir(parents=True, exist_ok=True)
    JOURNAL.write_text(json.dumps(
        {"test": "@TH_ID@", "exigences": EXIGENCES, "statut": STATUT, "verdict": verdict,
         "graine": SEED, "dt": DT,
         "checks": [{"nom": n, "ok": ok, "detail": d} for n, ok, d in checks]},
        indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    for nom, ok, detail in checks:
        print(("PASS" if ok else "ECHEC") + f" {nom} — {detail}")
    raise SystemExit(0 if verdict == "PASS" else 1)


if __name__ == "__main__":
    main()
'''

MATRICE_TEMPLATE = '''# Matrice de couverture — batterie-tests-@PROJET@

> Générée par `scaffold_tests.py` v@VERSION@ (skill @SKILL@) — profil SE : **@PROFIL@**.
> Protocole STATUT : chaque squelette porte `STATUT = "NON_IMPLÉMENTÉ"` — `run_all.py` ne
> l'exécute pas tant qu'il n'est pas adapté et passé à `"PRÊT"` (un squelette ne prouve rien, R3).
> Exécution : `python3 run_all.py` (verdicts par test + `journal/synthese.json`).
> Cible de couverture (profil @PROFIL@) : @CIBLE@ — grille complète :
> `references/workflow-engineering-design.md` §3.

## Exigences ↔ tests fonctionnels

| Exigence | Test | Squelette | Verdict | Détail |
|----------|------|-----------|---------|--------|
@TF_ROWS@

## Sous-systèmes matériels ↔ tests TH

| TH | Sous-système (à nommer — SS-xx du dossier de conception) | Exigences rattachées | Verdict |
|----|-----------------------------------------------------------|---------------------|---------|
@TH_ROWS@

## Non-couverture assumée

| Exigence | Raison NON VÉRIFIABLE | Levier pour la couvrir |
|----------|----------------------|------------------------|
| (aucune au scaffold — compléter si une exigence reste sans test, règle 12) | | |
'''

TF_PRET_AUTO = '''#!/usr/bin/env python3
"""TF-90 : auto-test du harnais (fixture du selftest scaffold_tests.py)."""
STATUT = "PRÊT"


def verifier():
    return [("EF-01 : vérification mécanique du protocole PRÊT", True,
             "check trivial — le harnais exécute les tests PRÊT")]


def main():
    checks = verifier()
    for nom, ok, detail in checks:
        print(("PASS" if ok else "ECHEC") + f" {nom} — {detail}")
    raise SystemExit(0 if all(ok for _, ok, _ in checks) else 1)


if __name__ == "__main__":
    main()
'''

# ------------------------------------------------------------ génération -----


def analyser_exigences(texte):
    """Parse --exigences : IDs séparés par virgules, dédupliqués, ordre conservé."""
    ids, vus = [], set()
    for brut in filter(None, (morceau.strip() for morceau in texte.split(","))):
        if not EXIGENCE_RE.match(brut):
            sys.exit(f"ERREUR — exigence invalide : {brut!r} (format attendu XX-01, ex : EF-01)")
        if brut not in vus:
            vus.add(brut)
            ids.append(brut)
    return ids


def generer_batterie(projet, exigences, nb_th, profil):
    """Retourne [(chemin_relatif, contenu)] — contenu déterministe (idempotence ×2)."""
    fichiers = []
    fichiers.append(("run_all.py",
                     RUN_ALL_TEMPLATE.replace("@PROJET@", projet)
                                     .replace("@VERSION@", VERSION)
                                     .replace("@SKILL@", SKILL)))
    lignes_tf = []
    for i, exigence in enumerate(exigences, 1):
        tf_id = f"TF-{i:02d}"
        nom = f"tf_{i:02d}_{exigence.split('-')[0].lower()}_{exigence.split('-')[1]}.py"
        contenu = (TF_TEMPLATE.replace("@VERSION@", VERSION)
                              .replace("@SKILL@", SKILL)
                              .replace("@TF_ID@", tf_id)
                              .replace("@EXIGENCE@", exigence)
                              .replace("@EXIGENCES_JSON@", json.dumps([exigence]))
                              .replace("@FICHIER@", nom[:-3]))
        fichiers.append((f"tests_fonctionnels/{nom}", contenu))
        lignes_tf.append(f"| {exigence} | {tf_id} | `{nom}` | NON VÉRIFIABLE | test à implémenter |")
    if not exigences:
        lignes_tf.append("| (aucune exigence fournie) | — | — | — | "
                         "re-scaffold avec --exigences EF-01,ENF-01,… |")
    lignes_th = []
    for i in range(1, nb_th + 1):
        nom = f"th_{i:02d}_sous_systeme.py"
        contenu = (TH_TEMPLATE.replace("@VERSION@", VERSION)
                              .replace("@SKILL@", SKILL)
                              .replace("@TH_ID@", f"TH-{i:02d}")
                              .replace("@EXIGENCES_JSON@",
                                       json.dumps(exigences if exigences
                                                  else ["ENF-01 (à remplacer)"]))
                              .replace("@FICHIER@", nom[:-3]))
        fichiers.append((f"tests_materiel/{nom}", contenu))
        lignes_th.append(f"| TH-{i:02d} | <à nommer> | (à rattacher aux EF/ENF allouées au SS) | "
                         "NON VÉRIFIABLE (squelette) |")
    matrice = (MATRICE_TEMPLATE.replace("@PROJET@", projet)
                               .replace("@VERSION@", VERSION)
                               .replace("@SKILL@", SKILL)
                               .replace("@PROFIL@", profil)
                               .replace("@CIBLE@", CIBLES_COUVERTURE[profil])
                               .replace("@TF_ROWS@", "\n".join(lignes_tf))
                               .replace("@TH_ROWS@", "\n".join(lignes_th)))
    fichiers.append(("matrice-couverture.md", matrice))
    return fichiers


def scaffold(projet, out, exigences_texte, nb_th, profil):
    """Crée la batterie (fichiers absents seulement) et affiche le compte-rendu."""
    exigences = analyser_exigences(exigences_texte)
    racine = Path(out) / f"batterie-tests-{projet}"
    crees, conserves = [], []
    for relatif, contenu in generer_batterie(projet, exigences, nb_th, profil):
        chemin = racine / relatif
        chemin.parent.mkdir(parents=True, exist_ok=True)
        if chemin.exists():
            conserves.append(relatif)
        else:
            chemin.write_text(contenu, encoding="utf-8")
            crees.append(relatif)
    (racine / "journal").mkdir(parents=True, exist_ok=True)
    print(f"Batterie : {racine}  (profil {profil}, {len(exigences)} exigence(s), {nb_th} TH)")
    for relatif in crees:
        print(f"  créé       {relatif}")
    for relatif in conserves:
        print(f"  conservé   {relatif}")
    print("Étape suivante : adapter les squelettes puis les passer à STATUT = \"PRÊT\", "
          "ensuite : python3 run_all.py")
    return racine


def manifeste(racine):
    """Empreinte sha256 de tous les fichiers (vérification d'idempotence)."""
    return {str(p.relative_to(racine)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(racine.rglob("*")) if p.is_file()}


def executer_run_all(racine, timeout=180):
    proc = subprocess.run([sys.executable, str(racine / "run_all.py")],
                          capture_output=True, text=True, timeout=timeout)
    return proc.returncode


def lire_synthese(racine):
    return json.loads((racine / "journal" / "synthese.json").read_text(encoding="utf-8"))


def selftest():
    """Auto-test complet en sandbox temporaire (nettoyé en sortie)."""
    sandbox = Path(tempfile.mkdtemp(prefix="scaffold-selftest-"))
    try:
        argv = ["--projet", "essai-selftest", "--out", str(sandbox),
                "--exigences", "EF-01,ENF-01", "--th", "1", "--profil", "standard"]
        # 1. scaffold initial + structure complète
        racine = scaffold(*_args_scaffold(argv))
        attends = ["run_all.py", "matrice-couverture.md",
                   "tests_fonctionnels/tf_01_ef_01.py", "tests_fonctionnels/tf_02_enf_01.py",
                   "tests_materiel/th_01_sous_systeme.py"]
        manquants = [a for a in attends if not (racine / a).is_file()]
        assert not manquants, f"fichiers manquants : {manquants}"
        assert (racine / "journal").is_dir(), "journal/ absent"
        # 2. idempotence ×2 — re-scaffold : octets identiques
        avant = manifeste(racine)
        scaffold(*_args_scaffold(argv))
        assert manifeste(racine) == avant, "re-scaffold a modifié des octets — idempotence rompue"
        # 3. re-scaffold n'écrase pas un test déjà implémenté
        implemente = racine / "tests_fonctionnels" / "tf_01_ef_01.py"
        implemente.write_text("# test implémenté par l'utilisateur\n", encoding="utf-8")
        scaffold(*_args_scaffold(argv))
        assert implemente.read_text(encoding="utf-8") == "# test implémenté par l'utilisateur\n"
        # restauration du squelette d'origine (le fichier modifié ci-dessus est un commentaire
        # sans STATUT -> traité PRÊT ; il fausserait l'étape 4 du protocole)
        implemente.unlink()
        scaffold(*_args_scaffold(argv))
        assert manifeste(racine) == avant, "re-scaffold post-suppression non conforme au gabarit"
        # 4. run_all sur batterie neuve : tout NON_IMPLÉMENTÉ -> verdict global, code 2
        assert executer_run_all(racine) == 2, "run_all attendu code 2 sur batterie neuve"
        synthese = lire_synthese(racine)
        assert synthese["verdict_global"] == "NON_IMPLÉMENTÉ"
        assert synthese["total"] == 3 and synthese["non_implementes"] == 3
        # 5. protocole PRÊT : un test adapté est exécuté et PASS
        (racine / "tests_fonctionnels" / "tf_90_auto.py").write_text(TF_PRET_AUTO, encoding="utf-8")
        assert executer_run_all(racine) == 2  # les squelettes restent à adapter
        synthese = lire_synthese(racine)
        passes = {t["id"] for t in synthese["tests"] if t["verdict"] == "PASS"}
        assert "TF-90" in passes, "le test PRÊT n'a pas été exécuté/PASS par run_all"
        # 6. l'exemple TH (patron simulation-materielle) PASSe une fois passé à PRÊT
        th = racine / "tests_materiel" / "th_01_sous_systeme.py"
        th.write_text(th.read_text(encoding="utf-8")
                      .replace('STATUT = "NON_IMPLÉMENTÉ"', 'STATUT = "PRÊT"'), encoding="utf-8")
        executer_run_all(racine)
        verdict_th = next(t["verdict"] for t in lire_synthese(racine)["tests"]
                          if t["id"] == "TH-01")
        assert verdict_th == "PASS", f"l'exemple TH devrait PASS, reçu : {verdict_th}"
        # 7. slug invalide rejeté mécaniquement
        rc = subprocess.run([sys.executable, str(Path(__file__).resolve()),
                             "--projet", "Mauvais_Slug", "--out", str(sandbox)],
                            capture_output=True, text=True)
        assert rc.returncode != 0, "slug invalide accepté — validation rompue"
        print("SELFTEST OK — structure, idempotence ×2, conservation des implémentés, "
              "protocole STATUT (NON_IMPLÉMENTÉ/PRÊT), exemple TH fonctionnel, "
              "rejet du slug invalide.")
        return 0
    finally:
        shutil.rmtree(sandbox, ignore_errors=True)


def _args_scaffold(argv):
    args = parse_args(argv)
    return args.projet, args.out, args.exigences, args.th, args.profil


def parse_args(argv=None):
    p = argparse.ArgumentParser(
        description="Générateur idempotent de batterie de tests (M7 TESTER, "
                    f"skill {SKILL} v{VERSION})")
    p.add_argument("--projet", help="slug kebab-case du projet (ex : serre-cbd)")
    p.add_argument("--out", default="download", help="dossier de sortie (défaut : download)")
    p.add_argument("--exigences", default="",
                   help="IDs séparés par virgules (ex : EF-01,EF-02,ENF-01)")
    p.add_argument("--th", type=int, default=1,
                   help="nombre de squelettes TH (défaut : 1)")
    p.add_argument("--profil", choices=("mini", "standard", "complexe"), default="standard",
                   help="profil SE calibré en M5 (défaut : standard)")
    p.add_argument("--selftest", action="store_true",
                   help="auto-test complet en sandbox temporaire")
    return p.parse_args(argv)


def main():
    args = parse_args()
    if args.selftest:
        raise SystemExit(selftest())
    if not args.projet:
        sys.exit("ERREUR — --projet est requis (ou --selftest)")
    if not SLUG_RE.match(args.projet):
        sys.exit(f"ERREUR — --projet doit être un slug kebab-case (reçu : {args.projet!r})")
    if args.th < 0:
        sys.exit("ERREUR — --th doit être >= 0")
    scaffold(args.projet, args.out, args.exigences, args.th, args.profil)


if __name__ == "__main__":
    main()
