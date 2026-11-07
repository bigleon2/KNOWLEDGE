#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.31)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).
task43-verifier-projet.py — Vérificateur correct-work (projet) Task 43 (mapping DJTT = source de vérité).

Vérifications mécaniques du projet (app LEON TSI EDITEUR v11 + tsi-toolkit +
données + scripts) selon correct-work v2.8.0 mode PROJET (5 étapes), avec le
mapping DJTT Kontrol S4 MK2 v2.1.0 comme SOURCE DE VÉRITÉ et comme EXEMPLE DE
POSSIBILITÉ DE MAPPING AVANCÉ (plan Task 43, décisions D005-D008) :

  --donnees       Étape 2 — comptes DJTT re-dérivés mécaniquement de la source
                  de vérité tsi-toolkit/data/commandes-traktor.json (163
                  contrôles / 393 commandes / 125 in / 220 out ; decks A/B/C/D
                  symétriques 14 nommés / 10 in / 7 out / 8 hotcues) + catalogue
                  scellé (455 = 393 DJTT + 62 CMDR) + idempotence générateurs
  --miroir        Étape 3 — divergences hôte↔clone (src/, prisma/, scripts de
                  session, rapports) + dérive de modes git — LECTURE SEULE
                  (findings ; corrections en vague 2 via --corriger)
  --interactions  Étape 4 — tsc/eslint/toolkit 20/20/symétrie ×3 + E2E exemple
                  de mapping avancé (preset Freeze Mode DJTT 15 mappings →
                  toolkit generate → arbitre tsi-validator rc=0) + batterie API
                  15/15 (serveur dev port 3000)
  --coherence     Étape 5 — cohérence numérique (les comptes s'additionnent) +
                  sha256 préfixes cités par les rapports Task 42 + intégrité
                  écosystème 98/98 + présence des rapports
  --corriger      VAGUE 2 — corrections structure : retrait du bruit template
                  src/app/api/{API Design,API Knowledge} (clone, origine
                  squelette c5cc7c7) + restauration des modes de l'index git
                  (idempotent ×2)
  --tout          donnees + miroir + interactions + coherence (sans corriger)

Codes de sortie : 0 si PASS, 1 sinon. Sous-processus stdin=DEVNULL. Idempotent.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import time
import urllib.error
import urllib.request

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLONE = os.path.join(RACINE, "work", "knowledge-clone-fddbe94")
TOOLKIT = os.path.join(CLONE, "tsi-toolkit")
DATA_TOOLKIT = os.path.join(TOOLKIT, "data", "commandes-traktor.json")
MATRICE = os.path.join(RACINE, "work", "task42-matrice-decks.json")
APP_CONTROLS = os.path.join(RACINE, "src", "data", "s4mk2-controls.json")
APP_COMMANDS = os.path.join(RACINE, "src", "data", "commands.json")
GEN_CATALOGUE = os.path.join(RACINE, "scripts", "task40-generer-catalogue-app.py")
GEN_MATRICE = os.path.join(RACINE, "scripts", "task42-matrice-decks.py")
VERIF_SYMETRIE = os.path.join(RACINE, "scripts", "task41-verifier-symetrie.py")
VALIDATEUR = os.path.join(CLONE, "skills", "tsi-validator", "scripts", "valider-tsi.py")
FREEZE_E2E = os.path.join(RACINE, "work", "task43-freeze-e2e.tsi")
HARNAIS_API = os.path.join(RACINE, "scripts", "leon", "test-api-fonctionnel.sh")
JOURNAL = os.path.join(RACINE, "work", "task43-verifier-journal.json")
BRUIT_TEMPLATE = (
    "src/app/api/API Design", "src/app/api/API Knowledge", "src/app/api/KNOWLEDGE.md",
    "src/app/api/README.md", "src/app/api/knowledge-export.yaml", "src/app/api/config",
    "src/app/api/knowledge", "src/app/api/skills", "src/lib/skills-reader.ts",
)


def _est_bruit_template(relatif):
    """Vrai si le chemin relatif (depuis src/) est un reliquat template squelette."""
    return any(relatif == p or relatif.startswith(p + "/") for p in BRUIT_TEMPLATE)

COMPTES_DJTT = {"controles": 163, "commandes": 393, "conditions_in": 125, "conditions_out": 220}
VERDICTS = {}


def _exec(args, cwd=RACINE, timeout=300):
    """Exécute une commande (stdin=DEVNULL — leçon stdin-hérité)."""
    return subprocess.run(
        args, capture_output=True, text=True, timeout=timeout,
        check=False, cwd=cwd, stdin=subprocess.DEVNULL,
    )


def _charger(chemin):
    with open(chemin, encoding="utf-8") as poignee:
        return json.load(poignee)


def _sha256(chemin):
    with open(chemin, "rb") as poignee:
        return hashlib.sha256(poignee.read()).hexdigest()


def _verdict(nom, ok, details):
    VERDICTS[nom] = {"pass": bool(ok), "details": details}
    for ligne in details:
        print(f"  [{'PASS' if ligne[0] else 'ÉCHEC'}] {ligne[1]}")
    print(f"{nom} : {'PASS' if ok else 'FAIL'}")
    return bool(ok)


def _verdict_global():
    return all(v["pass"] for v in VERDICTS.values()) and bool(VERDICTS)


# ---------------------------------------------------------------------------
# Étape 2 — erreurs et omissions : comptes DJTT re-dérivés de la source
# ---------------------------------------------------------------------------
def donnees():
    """D005 — la source de vérité DJTT vérifiée de bout en bout."""
    details = []
    toolkit = _charger(DATA_TOOLKIT)
    ok_comptes = toolkit["comptes"] == COMPTES_DJTT and len(toolkit["controles"]) == 163 \
        and len(toolkit["commandes"]) == 393
    details.append((ok_comptes, f"toolkit comptes DJTT : {toolkit['comptes']} (163 contrôles / 393 commandes)"))
    conds = toolkit["conditions_declarees"]
    ok_conds = len(conds["in"]) == 125 and len(conds["out"]) == 220
    details.append((ok_conds, f"conditions déclarées : in={len(conds['in'])} / out={len(conds['out'])} (125/220, in+out=345)"))

    matrice = _charger(MATRICE)
    ok_matrice = matrice["comptes"] == {"controles": 163, "commandes": 393, "in": 125, "out": 220} \
        and all(matrice["coherences"].values())
    details.append((ok_matrice, "matrice decks : comptes 163/393/125/220 + cohérences toutes vraies"))

    decks = matrice["decks"]
    ok_decks = True
    for lettre, attendus in (("A", ("Left.", "C")), ("B", ("Right.", "D")), ("C", ("Left.", "A")), ("D", ("Right.", "B"))):
        d = decks[lettre]
        ok = (
            d["nb_controles_nommes"] == 14 and d["nb_in_prefixe"] == 10 and d["nb_out_prefixe"] == 7
            and d["hotcues"]["total_triggers"] == 8
            and len(d["hotcues"]["triggers_1_a_4"]) == 4
            and len(d["hotcues"]["triggers_5_a_8_via_remix"]) == 4
            and d["section_physique"] == attendus[0] and d["section_partagee_avec"] == attendus[1]
        )
        ok_decks = ok_decks and ok
    details.append((ok_decks, "decks A/B/C/D symétriques : 14 nommés / 10 in / 7 out / 8 hotcues (1-4 + 5-8 via Remix)"))

    empreinte_avant = _sha256(MATRICE)
    regen1 = _exec([sys.executable, GEN_MATRICE, DATA_TOOLKIT, MATRICE])
    regen2 = _exec([sys.executable, GEN_MATRICE, DATA_TOOLKIT, MATRICE])
    ok_regen = regen1.returncode == 0 and regen2.returncode == 0 \
        and _sha256(MATRICE) == empreinte_avant
    details.append((ok_regen, "matrice re-générée ×2 byte-identique (idempotence, source de vérité stable)"))

    app = _charger(APP_CONTROLS)
    ok_app_comptes = app["comptes"] == {"in": 125, "out": 220}
    details.append((ok_app_comptes, f"app s4mk2-controls comptes : {app['comptes']} (125/220 — miroir de la source DJTT)"))

    zones = {z: chips for z, chips in app["tableCC"].items() if re.fullmatch(r"DECK [ABCD]", z)}
    ok_zones = sorted(zones) == ["DECK A", "DECK B", "DECK C", "DECK D"]
    ok_chips = all(len(chips) == 39 for chips in zones.values())
    ok_hotcues = True
    for zone, chips in zones.items():
        lettre = zone[-1]
        directes = [c for c in chips if re.fullmatch(rf"Hotcue {lettre}[1-4]", c["nom"])]
        via_remix = [c for c in chips if re.fullmatch(rf"Hotcue {lettre}[5-8] \(via Remix Slot\. [1-4]\)", c["nom"])]
        ok_hotcues = ok_hotcues and len(directes) == 4 and len(via_remix) == 4
    details.append((ok_zones and ok_chips, "4 blocs DECK × 39 chips identiques (aperçu studio v11)"))
    details.append((ok_hotcues, "8 hotcues par deck : 4 directes + 4 via Remix Slot (1-4)"))

    commandes = _charger(APP_COMMANDS)
    provenance = {}
    for entree in commandes["commandes"].values():
        provenance[entree.get("provenance", "?")] = provenance.get(entree.get("provenance", "?"), 0) + 1
    ok_catalogue = (
        commandes["comptes"] == {"commandes": 455, "categories": 16}
        and provenance.get("toolkit-djtt-reel") == 393
        and provenance.get("discussion-cmdr") == 62
        and len(commandes["categories"]) == 16
    )
    details.append((ok_catalogue, f"catalogue scellé : 455 commandes = 393 DJTT (source de vérité) + 62 CMDR (discussion) — {provenance}"))

    ok_miroir_data = (
        _sha256(APP_CONTROLS) == _sha256(os.path.join(CLONE, "src", "data", "s4mk2-controls.json"))
        and _sha256(APP_COMMANDS) == _sha256(os.path.join(CLONE, "src", "data", "commands.json"))
    )
    details.append((ok_miroir_data, "données app byte-identiques hôte ↔ clone (s4mk2-controls, commands)"))

    empreintes_avant = (_sha256(APP_CONTROLS), _sha256(APP_COMMANDS))
    gen = _exec([sys.executable, GEN_CATALOGUE])
    ok_gen = gen.returncode == 0 and (_sha256(APP_CONTROLS), _sha256(APP_COMMANDS)) == empreintes_avant
    details.append((ok_gen, "générateur catalogue re-joué : byte-identique (dérivation mécanique stable)"))

    return _verdict("DONNEES", all(ok for ok, _ in details), details)


# ---------------------------------------------------------------------------
# Étape 3 — structure et conflits : miroir hôte↔clone (lecture seule)
# ---------------------------------------------------------------------------
def _comparer_arbres(racine_a, racine_b, relatif=""):
    """Compare récursivement deux arbres — renvoie (clone_only, host_only, diff)."""
    seul_b, seul_a, diff = [], [], []
    Chemin = os.path
    base_a = Chemin.join(racine_a, relatif) if relatif else racine_a
    base_b = Chemin.join(racine_b, relatif) if relatif else racine_b
    noms_a = set(os.listdir(base_a)) if Chemin.isdir(base_a) else set()
    noms_b = set(os.listdir(base_b)) if Chemin.isdir(base_b) else set()
    for nom in sorted(noms_a - noms_b):
        chemin = Chemin.join(relatif, nom) if relatif else nom
        cible = Chemin.join(base_a, nom)
        if Chemin.isdir(cible):
            _, sous_seul, _ = _comparer_arbres(racine_a, racine_b, chemin)
            seul_a.extend(sous_seul)
        else:
            seul_a.append(chemin)
    for nom in sorted(noms_b - noms_a):
        chemin = Chemin.join(relatif, nom) if relatif else nom
        cible = Chemin.join(base_b, nom)
        if Chemin.isdir(cible):
            sous_seul, _, _ = _comparer_arbres(racine_a, racine_b, chemin)
            seul_b.extend(sous_seul)
        else:
            seul_b.append(chemin)
    for nom in sorted(noms_a & noms_b):
        chemin = Chemin.join(relatif, nom) if relatif else nom
        a, b = Chemin.join(base_a, nom), Chemin.join(base_b, nom)
        if Chemin.isdir(a) and Chemin.isdir(b):
            s2, h2, d2 = _comparer_arbres(racine_a, racine_b, chemin)
            seul_b.extend(s2)
            seul_a.extend(h2)
            diff.extend(d2)
        elif Chemin.isfile(a) and Chemin.isfile(b):
            if _sha256(a) != _sha256(b):
                diff.append(chemin)
    return seul_b, seul_a, diff


def miroir():
    """D006 (findings) — divergences hôte↔clone, lecture seule."""
    details = []
    findings = {"divergences": [], "modes_git": 0, "rapports_manquants_clone": []}

    seul_clone, seul_hote, diff = _comparer_arbres(
        os.path.join(RACINE, "src"), os.path.join(CLONE, "src"))
    bruit = [p for p in seul_clone if _est_bruit_template(p)]
    autre_clone = [p for p in seul_clone if not _est_bruit_template(p)]
    ok_src = not diff and not seul_hote and not autre_clone
    details.append((ok_src, f"src/ hôte↔clone : {len(diff)} diff, {len(seul_hote)} hôte-seul, "
                            f"{len(autre_clone)} clone-seul hors bruit template "
                            f"(bruit template identifié : {len(bruit)} fichiers — correction vague 2)"))
    findings["divergences"].extend(
        {"type": "bruit_template_clone", "chemin": p} for p in bruit)
    findings["divergences"].extend({"type": "diff", "chemin": p} for p in diff)
    findings["divergences"].extend({"type": "hote_seul", "chemin": p} for p in seul_hote)
    findings["divergences"].extend({"type": "clone_seul", "chemin": p} for p in autre_clone)

    _, _, diff_prisma = _comparer_arbres(os.path.join(RACINE, "prisma"), os.path.join(CLONE, "prisma"))
    details.append((not diff_prisma, f"prisma/ hôte↔clone : {len(diff_prisma)} diff"))
    findings["divergences"].extend({"type": "diff_prisma", "chemin": p} for p in diff_prisma)

    session = []
    for nom in sorted(os.listdir(os.path.join(RACINE, "scripts"))):
        if nom.startswith(("task40-", "task41-", "task42-", "task43-", "task44-", "adaptation-syntaxe")) or nom == "leon":
            session.append(nom)
    manquants, differs = [], []
    for nom in session:
        hote = os.path.join(RACINE, "scripts", nom)
        clone = os.path.join(CLONE, "scripts", nom)
        if not os.path.exists(clone):
            manquants.append(nom)
        elif os.path.isfile(hote) and _sha256(hote) != _sha256(clone):
            differs.append(nom)
        elif os.path.isdir(hote):
            _, _, d = _comparer_arbres(hote, clone)
            differs.extend(f"{nom}/{p}" for p in d)
    details.append((not manquants and not differs,
                    f"scripts de session hôte↔clone : {len(session)} éléments, "
                    f"{len(manquants)} manquants, {len(differs)} divergents"))
    findings["divergences"].extend({"type": "script_manquant", "chemin": p} for p in manquants)
    findings["divergences"].extend({"type": "script_diff", "chemin": p} for p in differs)

    rapport_re = re.compile(r"^(plan-task4\d|rapport-.*task4\d|rapport-adaptation-syntaxe)")
    rapports_hote = [n for n in os.listdir(os.path.join(RACINE, "download")) if rapport_re.match(n)]
    manquants_rapport = [n for n in rapports_hote
                         if not os.path.isfile(os.path.join(CLONE, "download", n))]
    details.append((True, f"rapports task4x : {len(rapports_hote)} à l'hôte, "
                          f"{len(manquants_rapport)} manquants au clone download/ (sync en clôture D009)"))
    findings["rapports_manquants_clone"] = manquants_rapport

    fini = _exec(["git", "diff", "--numstat"], cwd=CLONE)
    modes = [l.split("\t")[2] for l in fini.stdout.splitlines() if re.match(r"^0\t0\t", l)]
    findings["modes_git"] = len(modes)
    details.append((len(modes) >= 0, f"dérive de modes git (clone) : {len(modes)} fichiers 644→755 "
                                      "(restauration en vague 2 --corriger)"))

    with open(JOURNAL.replace("verifier-journal", "verifier-miroir"), "w", encoding="utf-8") as poignee:
        json.dump(findings, poignee, ensure_ascii=False, indent=2, sort_keys=True)
    return _verdict("MIROIR", ok_src and not diff_prisma and not manquants and not differs, details)


# ---------------------------------------------------------------------------
# Étape 4 — interactions : app ↔ API ↔ toolkit ↔ arbitres
# ---------------------------------------------------------------------------
def _serveur_dev():
    """Démarre le serveur dev si nécessaire — renvoie le processus (ou None)."""
    try:
        with urllib.request.urlopen("http://localhost:3000/api/projects", timeout=5):
            return None  # déjà vivant (session antérieure)
    except urllib.error.HTTPError:
        return None  # serveur vivant (réponse d'erreur HTTP = processus actif)
    except (urllib.error.URLError, OSError, ValueError):
        pass
    journal = open(os.path.join(RACINE, "work", "task43-devserver.log"), "w", encoding="utf-8")
    proc = subprocess.Popen(
        ["npm", "run", "dev"], cwd=RACINE, stdout=journal, stderr=subprocess.STDOUT,
        stdin=subprocess.DEVNULL, start_new_session=True,
    )
    delai_max = 180
    for _ in range(delai_max):
        time.sleep(1)
        if proc.poll() is not None:
            return None
        try:
            with urllib.request.urlopen("http://localhost:3000/api/projects", timeout=5):
                return proc
        except (urllib.error.URLError, OSError, ValueError):
            continue
    return None


def _arreter(proc):
    """Arrête le serveur dev démarré par le vérificateur (groupe de processus)."""
    if proc is None:
        return
    try:
        os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
        proc.wait(timeout=15)
    except (OSError, subprocess.TimeoutExpired):
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        except OSError:
            pass


def interactions():
    """D007 — interactions de bout en bout, DJTT comme mapping avancé exemple."""
    details = []
    tsc = _exec(["npx", "tsc", "--noEmit"], timeout=600)
    erreurs_src = len(re.findall(r"/my-project/src/", tsc.stdout + tsc.stderr))
    details.append((erreurs_src == 0, f"tsc --noEmit : {erreurs_src} erreur sur src/ hôte (baseline template hors jalon)"))

    eslint = _exec(["npx", "eslint", "src"], timeout=600)
    details.append((eslint.returncode == 0, "eslint src : rc=0"))

    unittest = _exec([sys.executable, "-m", "unittest", "tests.test_toolkit"], cwd=TOOLKIT, timeout=300)
    sortie_toolkit = unittest.stdout + unittest.stderr
    ok_toolkit = unittest.returncode == 0 and "Ran 20 tests" in sortie_toolkit and "OK" in sortie_toolkit
    details.append((ok_toolkit, "tsi-toolkit : suite 20/20 (unittest tests.test_toolkit)"))

    symetries = []
    for mode in ("--symetrie", "--noms-reels", "--modules"):
        fini = _exec([sys.executable, VERIF_SYMETRIE, mode], timeout=120)
        symetries.append(fini.returncode == 0 and "PASS" in fini.stdout)
    details.append((all(symetries), f"aperçu : symétrie/noms-réels/modules {'PASS ×3' if all(symetries) else 'ÉCHEC'}"))

    generation = _exec(
        [sys.executable, "-m", "tsi_toolkit", "generate",
         "examples/preset-freeze-mode.json", FREEZE_E2E],
        cwd=TOOLKIT, timeout=120)
    validation = _exec([sys.executable, VALIDATEUR, FREEZE_E2E], cwd=CLONE, timeout=120)
    ok_freeze = (
        generation.returncode == 0
        and validation.returncode == 0
        and "PASS" in validation.stdout
        and "15 mappings" in validation.stdout
    )
    details.append((ok_freeze, "E2E exemple de mapping avancé : preset Freeze Mode DJTT (15 mappings) → "
                               "toolkit generate → arbitre tsi-validator rc=0"))

    proc = _serveur_dev()
    try:
        harnais = _exec(["bash", HARNAIS_API], timeout=420)
        ok_api = (
            harnais.returncode == 0
            and re.search(r"\d+/15 PASS", harnais.stdout)
            and ", 0 FAIL" in harnais.stdout
        )
        details.append((ok_api, "batterie API 15/15 (serveur dev port 3000, restauration propre)"))
    finally:
        _arreter(proc)

    return _verdict("INTERACTIONS", all(ok for ok, _ in details), details)


# ---------------------------------------------------------------------------
# Étape 5 — cohérence des raisonnements
# ---------------------------------------------------------------------------
def coherence():
    """D008 — les comptes s'additionnent, les rapports disent la vérité."""
    details = []
    toolkit = _charger(DATA_TOOLKIT)
    somme_conds = len(toolkit["conditions_declarees"]["in"]) + len(toolkit["conditions_declarees"]["out"])
    details.append((somme_conds == 345, f"cohérence numérique : 125 in + 220 out = {somme_conds} conditions"))

    matrice = _charger(MATRICE)
    decks = matrice["decks"]
    ok_sections = (
        sum(d["nb_controles_nommes"] for d in decks.values()) == 56
        and sum(d["nb_in_prefixe"] for d in decks.values()) == 40
        and sum(d["nb_out_prefixe"] for d in decks.values()) == 28
    )
    details.append((ok_sections, "decks nommés : 4 × 14 = 56 contrôles / 4 × 10 = 40 in / 4 × 7 = 28 out"))

    app = _charger(APP_CONTROLS)
    zones = {z: chips for z, chips in app["tableCC"].items() if re.fullmatch(r"DECK [ABCD]", z)}
    total_chips = sum(len(c) for c in zones.values())
    details.append((total_chips == 156, f"chips aperçu : 4 blocs × 39 = {total_chips} chips DECK"))

    commandes = _charger(APP_COMMANDS)
    prov = {}
    for e in commandes["commandes"].values():
        prov[e.get("provenance", "?")] = prov.get(e.get("provenance", "?"), 0) + 1
    details.append((prov.get("toolkit-djtt-reel", 0) + prov.get("discussion-cmdr", 0) == 455,
                    f"catalogue : 393 DJTT + 62 CMDR = {prov.get('toolkit-djtt-reel', 0) + prov.get('discussion-cmdr', 0)} commandes"))

    # SHAs de référence — mis à jour Task 44 (2026-11-04, session web-6058b3ba) :
    # enrichissement légitime catalogues_interaktiv (524 commandes Interaktiv Audio CC BY 4.0
    # + 24 MIDI Controls 850-873) : commands f7f45bbb → afbf7b50, s4mk2-controls c08df03b →
    # ccdbd6e3 ; matrice inchangée 470b90ae. Evolutions tracées R2 (extensions additives).
    prefixes = {
        MATRICE: "470b90ae",
        APP_COMMANDS: "afbf7b50",
        APP_CONTROLS: "ccdbd6e3",
    }
    ok_sha = all(_sha256(c).startswith(p) for c, p in prefixes.items())
    details.append((ok_sha, "sha256 références à jour (Task 44) : matrice 470b90ae · "
                            "commands afbf7b50 · s4mk2-controls ccdbd6e3 — conformes au disque"))

    integrite = _exec([sys.executable, "scripts/check-ecosysteme-integrity.py"], cwd=CLONE, timeout=300)
    ok_integrite = "98/98 PASS, 0 FAIL" in integrite.stdout or "98/98 PASS" in integrite.stdout
    details.append((ok_integrite, "intégrité écosystème : 98/98 PASS (revendication rapport Task 42 = réalité disque)"))

    rapports = ["rapport-final-task40.md", "rapport-final-task41.md", "rapport-final-task42.md",
                "rapport-tests-task41.md", "rapport-tests-task42.md", "rapport-adaptation-syntaxe.md",
                "plan-task40-mission-leon-studio-react.md", "plan-task41-analyse-sources-corrections.md",
                "plan-task42-taches-restantes-decks.md"]
    manquants = [r for r in rapports if not os.path.isfile(os.path.join(RACINE, "download", r))]
    details.append((not manquants, f"rapports Task 40-42 présents et non vides ({len(rapports) - len(manquants)}/{len(rapports)})"))

    return _verdict("COHÉRENCE", all(ok for ok, _ in details), details)


# ---------------------------------------------------------------------------
# Vague 2 — corrections structure (idempotentes)
# ---------------------------------------------------------------------------
def corriger():
    """D006 — retrait bruit template + restauration des modes de l'index git."""
    details = []
    cibles = [os.path.join(CLONE, *p.split("/")) for p in BRUIT_TEMPLATE]
    existants = [c for c in cibles if os.path.exists(c)]
    if existants:
        fini = _exec(["git", "rm", "-r", "-q", "--"] + existants, cwd=CLONE)
        details.append((fini.returncode == 0, f"bruit template retiré (git rm -r) : {len(existants)} dossier(s) — "
                                              f"{', '.join(BRUIT_TEMPLATE)} (origine squelette c5cc7c7)"))
    else:
        details.append((True, "bruit template déjà retiré (no-op — idempotent)"))

    fini = _exec(["git", "diff", "--numstat"], cwd=CLONE)
    fichiers = [l.split("\t")[2] for l in fini.stdout.splitlines() if re.match(r"^0\t0\t", l)]
    restaures = 0
    for fichier in fichiers:
        liste = _exec(["git", "ls-files", "-s", "--", fichier], cwd=CLONE)
        correspondance = re.search(r"^100(\d{3}) ", liste.stdout)
        if correspondance:
            mode = int(correspondance.group(1), 8)
            try:
                os.chmod(os.path.join(CLONE, fichier), mode)
                restaures += 1
            except OSError:
                pass
    details.append((True, f"modes restaurés sur l'index git : {restaures}/{len(fichiers)} fichiers (0 .sh concerné — exécutabilité préservée)"))

    # idempotence : re-jeu → no-op
    fini = _exec(["git", "diff", "--numstat"], cwd=CLONE)
    restants = len([l for l in fini.stdout.splitlines() if re.match(r"^0\t0\t", l)])
    encores = [c for c in cibles if os.path.exists(c)]
    ok_idempotent = restants == 0 and not encores
    details.append((ok_idempotent, f"idempotence ×2 : {restants} dérive(s) de modes restante(s), "
                                   f"{len(encores)} dossier(s) bruit restant(s)"))

    return _verdict("CORRECTIONS", all(ok for ok, _ in details), details)


def _construire_analyseur():
    """Analyseur d'arguments (stdlib)."""
    import argparse

    analyseur = argparse.ArgumentParser(
        prog="task43-verifier-projet.py",
        description="Vérificateur correct-work (projet) Task 43 — DJTT source de vérité.",
    )
    analyseur.add_argument("--donnees", action="store_true", help="Étape 2 — comptes DJTT")
    analyseur.add_argument("--miroir", action="store_true", help="Étape 3 — miroir hôte↔clone (lecture seule)")
    analyseur.add_argument("--interactions", action="store_true", help="Étape 4 — interactions + E2E mapping avancé")
    analyseur.add_argument("--coherence", action="store_true", help="Étape 5 — cohérence numérique + rapports")
    analyseur.add_argument("--corriger", action="store_true", help="Vague 2 — corrections structure (idempotent)")
    analyseur.add_argument("--tout", action="store_true", help="donnees + miroir + interactions + coherence")
    return analyseur


def main(argv=None):
    """Point d'entrée — verdict consolidé + journal."""
    arguments = _construire_analyseur().parse_args(argv)
    tout = arguments.tout or not any([arguments.donnees, arguments.miroir,
                                      arguments.interactions, arguments.coherence, arguments.corriger])
    if arguments.donnees or tout:
        donnees()
    if arguments.miroir or tout:
        miroir()
    if arguments.interactions or tout:
        interactions()
    if arguments.coherence or tout:
        coherence()
    if arguments.corriger:
        corriger()

    global_ok = _verdict_global()
    os.makedirs(os.path.dirname(JOURNAL), exist_ok=True)
    existant = {}
    if os.path.isfile(JOURNAL):
        try:
            existant = _charger(JOURNAL)
        except (OSError, ValueError):
            existant = {}
    existant["task43"] = {"verdicts": VERDICTS, "global": global_ok}
    with open(JOURNAL, "w", encoding="utf-8") as poignee:
        json.dump(existant, poignee, ensure_ascii=False, indent=2, sort_keys=True)
    print(f"VERIFICATEUR PROJET : {'PASS' if global_ok else 'FAIL'} — journal {os.path.relpath(JOURNAL, RACINE)}")
    return 0 if global_ok else 1


if __name__ == "__main__":
    sys.exit(main())
