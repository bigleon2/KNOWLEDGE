#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.46)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).

Pipeline d'installation PM-INSTALL v1.8.0 (§2 — MÉCANISME DUAL : voie (a) installation
DIRECTE des formes certifiées du dépôt ; ce script en est l'EXÉCUTANT CANONIQUE)
réinstallation hôte post-wipe (§3.4 : wipe inter-sessions = cas documenté,
ré-exécution depuis l'étape 2).
Source : clone local du dépôt bigleon2/KNOWLEDGE @ a14f750 (dernier commit certifié
d'installation — Task 74 run 2 rc=0 ; règle d'or n°4 — descendant-tolérant :
merge-base --is-ancestor, jamais un état antérieur au pin, évolution forward
tolérée).
Task 76 (2026-11-08, session web-ecef7f80 — directive « tests des systèmes
d'installation ») : F1 — CONTRAT CLI (l'absence de gestion de --help a exécuté
une installation complète sur un simple appel d'aide en conditions réelles :
usage explicite, argv[1] explicite invalide = ABANDON sans repli silencieux,
mode --dry-run lecture seule) ; F2 — PIN b75a620 → a14f750 (3 commits certifiés
plus récents : aa3b99d directive, a14f750 installation certifiée, 3171c4b
Task 75 CLOSE).
Task 18 (2026-10-23, session web-fdf5963c — directive propriétaire « optimise le
système d'installation en regénérant ») : chemin REPO PARAMÉTRABLE (ordre : argv
$1 > variable d'environnement ECO_REPO > /home/z/my-project/KNOWLEDGE-repo >
/home/z/my-project/tmp/KNOWLEDGE-repo — portabilité L008) ; PIN b944a27 → b75a620 ;
listes += alias-eco (registre d'alias $<ALIAS>, Task 18).
Task 22 (2026-10-23, même session — directive « analyse approfondie du pipeline
qui installe $ECO-LEON ») : F1 anti-faux-succès — le rc de l'étape 2
(rescellement archive) est désormais PROPAGÉ (exit 2 si échec, leçon Task 17 :
toute mutation doit échouer si son sous-traitement échoue) ; F2 — la sync de
scripts/ EXCLUT __pycache__/ *.pyc (aucune souillure projetée, union inchangée
par ailleurs) ; F3 fail-fast — VÉRIFICATION POST-INSTALL embarquée : SHA-256 de
chaque SKILL.md des entrées KB hôte vs dépôt (0 divergence attendue, exit 2 sinon,
lecture seule = idempotence byte préservée).
Task 100 (2026-11-15, session web-ecef7f80 — GO propriétaire trace
1a1dfb31d58350d5, mission F1 suite 142) : l'étape 2 est BRANCHÉE sur le scelleur
canonique v2.3 task-f5-seal-archive-v23.py (l'ancien véhicule task21-f2 v2.2
DÉSÉPILAIT silencieusement les piliers d'une archive v2.3 — piliers dans ses
RETRAITS_SANCTIONNES — et préservait des entrées périmées de l'archive entrante →
divergence émergente après restauration-sandbox ; preuve mécanique S2 au rapport
task100-mission-f1-report.json) + étape 2bis — régénération du manifeste
d'intégrité par l'arbitre canonique (pense-bête du scelleur v2.3), rc propagés
(anti-faux-succès F1 Task 22 conservé).
Task 110 (2026-11-19, session web-ecef7f80 — GO futur, directive trace 1a1f2297d90c957d,
correctif structurel F2 CW Task 107) : l'étape 2 est REPONTÉE sur le scelleur
canonique v2.4 task-f5-seal-archive-v24.py — la garde anti-perte DISCRIMINE
désormais PERTE (entrée d'archive sans contrepartie locale → rc=2, jamais
contournable) et ÉVOLUTION LÉGITIME (divergence à contenu local commité au
HEAD du dépôt — --depot-git passé par le présent pipeline → rescellement
AUTORISÉ et tracé, plus aucun ECHEC transitoire sur montée de version de
corpus ; harnais T1-T5 au rapport Task 110). Le véhicule v2.3 est CONSERVÉ
intact (R4 — précédent task21-f2 v2.2).
Task 16 (2026-11-21, session web-93a4f011 — directive trace 1a1fbe9f0ef279fd
« corrige tous les différés consignés », différé constat Task 12) : l'étape 2
est REPONTÉE sur le scelleur canonique v2.5 task-f5-seal-archive-v25.py —
la discrimination EST ÉTENDUE au DÉPLACEMENT R4 (entrée corpus de l'archive
entrante sans contrepartie locale MAIS contenu byte-identique sous
skills/@historique/prompts-maitres/<skill>/ → rescellement AUTORISÉ et tracé
déplacement R4 légitime ; sans contrepartie → PERTE rc=2 inchangée) — fin
du contournement manuel « régénération du véhicule » des déduplications N27
(Tasks 11/12) ; harnais T0-T8 au rapport Task 16, parité v2.4/v2.5 byte-stable.
Le véhicule v2.4 est CONSERVÉ intact (R4 — lignage v2.3/v2.2).

Étapes couvertes par ce script :
  1  Corpus   : sync skills/@mon-ecosysteme/ (9 PMs) + garde R2 anti-rétrogradation
  3-6 Formes  : sync skills/{gen-plan,correct-work,clone-chat,refactor-guard,disciplines,alias-eco}
  7  Registre : sync skills/KNOWLEDGE.md + @historique/@Alias/ (registre vivant)
  8  Outillage: sync scripts/ (arbitres + bootstrap), purge des reconstitutions
               provisoires non canoniques (config.json)
  2  Archive  : rescellement download/mon-ecosysteme_archive.zip (task-f5-seal-archive-v25
               — véhicule canonique v2.5 corpus+piliers, mission F1 Task 100 + discrimination
               PERTE/ÉVOLUTION Task 110 + DÉPLACEMENT R4 Task 16, --depot-git REPO) + régénération
               du manifeste d'intégrité (check-ecosysteme-integrity, mode COMPLET)

Le dépôt et l'hôte partagent le même lignage (projection hôte 109 fichiers) :
union-merge sans --delete, fichiers dépôt = source de vérité au commit épinglé.
Les skills plateforme hors dépôt et les scripts de session sont conservés.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

USAGE = """usage: eco_install_pipeline.py [--help] [--dry-run] [chemin_dépôt]
  (aucun argument)   dépôt source = env ECO_REPO > /home/z/my-project/KNOWLEDGE-repo > tmp/KNOWLEDGE-repo
  chemin_dépôt       dépôt source EXPLICITE (doit exister et contenir skills/KNOWLEDGE.md — aucun repli silencieux)
  --dry-run          rapport complet SANS AUCUNE mutation (lecture seule — F1 Task 76)
  --help | -h        cette aide — n'exécute RIEN (F1 Task 76)
"""


def _args():
    """F1 (Task 76) — contrat CLI : --help n'exécute rien ; option inconnue = rc 64 ;
    un chemin explicite invalide = ABANDON (jamais de repli silencieux)."""
    a = sys.argv[1:]
    if any(x in ("--help", "-h") for x in a):
        print(USAGE)
        sys.exit(0)
    dry = "--dry-run" in a
    inconnues = [x for x in a if x.startswith("-") and x != "--dry-run"]
    if inconnues:
        print("Option inconnue : %s" % inconnues[0])
        print(USAGE)
        sys.exit(64)
    chemins = [x for x in a if not x.startswith("-")]
    if len(chemins) > 1:
        print("Un seul chemin de dépôt attendu")
        print(USAGE)
        sys.exit(64)
    return (chemins[0] if chemins else None), dry


def _resolve_repo(explicite):
    """Chemin du dépôt source (portabilité L008) : argv $1 (EXPLICITE — aucun repli
    silencieux si invalide, F1 Task 76) > env ECO_REPO > candidats par défaut.
    Le premier répertoire contenant skills/KNOWLEDGE.md gagne."""
    if explicite is not None:
        candidats = [explicite]
    elif os.environ.get("ECO_REPO"):
        candidats = [os.environ["ECO_REPO"]]
    else:
        candidats = ["/home/z/my-project/KNOWLEDGE-repo",
                     "/home/z/my-project/tmp/KNOWLEDGE-repo"]
    for c in candidats:
        if os.path.isfile(os.path.join(c, "skills", "KNOWLEDGE.md")):
            return c
    if explicite is not None:
        sys.exit("ABANDON : chemin de dépôt explicite invalide : %r (aucun repli "
                 "silencieux sur argument explicite — faille F1 corrigée Task 76). "
                 "Essayez : %s <chemin> ou ECO_REPO=<chemin>"
                 % (explicite, sys.argv[0]))
    sys.exit("ABANDON : aucun dépôt source trouvé (essayez : %s <chemin> ou ECO_REPO=<chemin>)"
             % sys.argv[0])


_ARGS = _args()
REPO = _resolve_repo(_ARGS[0])
DRY = _ARGS[1]
HOST = "/home/z/my-project"
PIN = "a14f750caa70c7358fa5d5c6ed1e709afdc385f8"
# Task 20 (finding F1) : « scripts/verify-correct-work.py » RETIRÉ de la purge —
# ce fichier est un shim de compatibilité CERTIFIÉ (décision S2-α Task 12,
# re-validée propriétaire 2026-10-10 : délégation pure à l'arbitre canonique du
# skill, refus explicite rc=64 en mode rapport). La sync le projette
# légitimement à l'hôte (chemin relatif identique) et la purge le combattait à
# chaque run (purges != [] systématique, bruit + suppression d'un fichier
# légitime). Seules les reconstitutions réellement non canoniques sont purgées.
NON_CANONIQUES = ["config.json"]


def semver_of(skill_md):
    """Version semver lue du frontmatter d'un SKILL.md (None si absente/illisible)."""
    try:
        head = open(skill_md, encoding="utf-8", errors="replace").read(3000)
    except OSError:
        return None
    m = re.search(r"^version:\s*[\"']?(\d+\.\d+\.\d+)", head, re.M)
    return m.group(1) if m else None


def vtuple(v):
    """Version « x.y.z » → tuple d'entiers comparable ((0, 0, 0) si vide)."""
    return tuple(int(x) for x in v.split(".")) if v else (0, 0, 0)


def kb_eco_skills():
    """Entrées écosystème du registre KB dont la forme installée existe au dépôt
    (dérivation dynamique KO-L003 — périmètre COMPLET PM-INSTALL §2bis)."""
    kb = open(os.path.join(REPO, "skills", "KNOWLEDGE.md"), encoding="utf-8").read()
    noms = re.findall(r"^## ([\w-]+) v[\d.]+$", kb, re.MULTILINE)
    return [n for n in noms
            if os.path.isfile(os.path.join(REPO, "skills", n, "SKILL.md"))]


def main():
    """Point d'entrée du pipeline : préflight pin, garde R2, projection sync,
    vérification SHA post-install — rapport JSON, rc 0/2."""
    report = {"pin": PIN[:7], "etapes": {}, "garde_R2": [], "purges": []}

    # Préflight : commit épinglé (descendant-tolérant — Task 8 : le pin est une
    # garde anti-rétrogradation, pas un verrou d'égalité ; l'évolution forward
    # du dépôt est légitime, un état ANTÉRIEUR au pin reste interdit)
    cur = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO,
                         capture_output=True, text=True).stdout.strip()
    anc = subprocess.run(["git", "merge-base", "--is-ancestor", PIN, cur], cwd=REPO,
                         capture_output=True, text=True)
    if anc.returncode != 0:
        print(f"FAIL commit dépôt {cur[:7]} n'est pas un descendant du pin {PIN[:7]}")
        sys.exit(2)
    report["etapes"]["preflight"] = f"commit {cur[:7]} OK (pin {PIN[:7]} ancêtre — descendant-tolérant)"

    # Garde R2 anti-rétrogradation — périmètre DÉRIVÉ DU REGISTRE KB (KO-L003,
    # Task 18 : jamais de liste figée — le périmètre COMPLET = toutes les entrées
    # du registre KB dont la forme installée existe au dépôt)
    familles = kb_eco_skills()
    downgrades = []
    for s in familles:
        v_repo = semver_of(os.path.join(REPO, "skills", s, "SKILL.md"))
        v_host = semver_of(os.path.join(HOST, "skills", s, "SKILL.md"))
        if v_host and v_repo and vtuple(v_host) > vtuple(v_repo):
            downgrades.append(f"{s}: host {v_host} > repo {v_repo}")
    if downgrades:
        print("FAIL garde R2 (host > repo) :", downgrades)
        sys.exit(2)
    report["garde_R2"] = "0 rétrogradation — host ≤ repo partout"

    # F2 (Task 18) : exclusions de projection — artefacts de bytecode non canoniques
    EXCLUS_SYNC = ("__pycache__",)

    def sync(rel, delete=False):
        """Projection d'un chemin dépôt → hôte (fichier ou arbre, dry-run conscient)."""
        src = os.path.join(REPO, rel)
        dst = os.path.join(HOST, rel)
        if not os.path.exists(src):
            report["etapes"][rel] = "absent du dépôt (ignoré)"
            return
        if os.path.isfile(src):
            if not DRY:
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(src, dst)
            report["etapes"][rel] = "fichier sync" + (" (dry-run)" if DRY else "")
            return
        if DRY:
            n = sum(len(files) for dirpath, _, files in os.walk(src)
                    if not any(part in EXCLUS_SYNC for part in dirpath.split(os.sep)))
            report["etapes"][rel] = f"{n} fichiers (dry-run — 0 mutation)"
            return
        if delete and os.path.isdir(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns(*EXCLUS_SYNC))
        n = sum(len(files) for dirpath, _, files in os.walk(dst)
                if not any(part in EXCLUS_SYNC for part in dirpath.split(os.sep)))
        report["etapes"][rel] = f"{n} fichiers"

    # Étape 1 — Corpus canonique
    sync("skills/@mon-ecosysteme", delete=True)
    # Étape 7 — Registre KB
    sync("skills/KNOWLEDGE.md")
    # Étapes 3-6 — Formes installées (familles)
    for s in ["gen-plan", "correct-work"]:
        sync(f"skills/{s}", delete=True)
    # Sync union des formes installées — périmètre DÉRIVÉ DU REGISTRE KB (KO-L003,
    # Task 18 : corrige la liste figée incomplète — skill-creator, version-management,
    # skill-finder-cn, fullstack-dev désormais installés = périmètre COMPLET PM-INSTALL §2bis)
    for s in kb_eco_skills():
        if s in ("gen-plan", "correct-work"):
            continue  # déjà syncés avec delete=True ci-dessus
        sync(f"skills/{s}")
    # @historique (archive documentaire R4)
    sync("skills/@historique")
    # Task 70 G2/G3 — collections @ (hors registre KB versionné par construction,
    # regex `^## ([\w-]+) v` : sync EXPLICITE — périmètre PM INSTALL étendu aux
    # collections intégrées @Bibliotheque-skills-Multi-IA (G2) et @GHORG-ecosysteme
    # (G3) ; sync() ignore gracieusement une collection absente du dépôt)
    sync("skills/@Bibliotheque-skills-Multi-IA")
    sync("skills/@GHORG-ecosysteme")

    # Étape 8 — Outillage (union : scripts de session conservés)
    sync("scripts")

    # Purge des reconstitutions provisoires non canoniques
    for rel in NON_CANONIQUES:
        p = os.path.join(HOST, rel)
        if os.path.exists(p):
            if DRY:
                report["purges"].append(rel + " (dry-run)")
            else:
                os.remove(p)
                report["purges"].append(rel)
    # F2 (Task 22) : purge du bytecode hôte résiduel (hérité des runs antérieurs —
    # l'union sync ne supprime pas ; __pycache__/ n'est plus projeté depuis F2)
    _pyc = os.path.join(HOST, "scripts", "__pycache__")
    if os.path.isdir(_pyc):
        if DRY:
            report["purges"].append("scripts/__pycache__ (dry-run)")
        else:
            shutil.rmtree(_pyc)
            report["purges"].append("scripts/__pycache__")

    if DRY:
        # F1 (Task 76) : --dry-run = lecture seule — le rescellement (mutation) est
        # sauté ; la vérification post-install F3 (lecture seule) est conservée.
        report["etapes"]["2_archive"] = "non exécuté (dry-run — lecture seule)"
    else:
        # Étape 2 — Rescellement archive d'intégrité (véhicule CANONIQUE v2.5
        # corpus + piliers — mission F1 Task 100 + discrimination PERTE/ÉVOLUTION
        # Task 110 [GO futur, correctif F2 CW 107] : PERTE = rc=2 jamais contournable ;
        # ÉVOLUTION à contenu local commité (comparaison git, --depot-git REPO) =
        # rescellement AUTORISÉ et tracé — la voie opérationnelle est mécanique.
        # Task 16 [directive 1a1fbe9f0ef279fd — différé constat Task 12] : DÉPLACEMENT
        # R4 = entrée corpus sans contrepartie locale MAIS byte-identique sous
        # @historique/prompts-maitres/<skill>/ → rescellement AUTORISÉ et tracé
        # (fin du contournement « régénération du véhicule » des déduplications N27).
        # Historique : le véhicule task21-f2 (v2.2) désépilait SILENCIEUSEMENT les
        # piliers d'une archive v2.3 (RETRAITS_SANCTIONNES, entrées périmées
        # préservées → divergence émergente après restauration-sandbox).
        # F1 (Task 22) : anti-faux-succès — le rc est propagé (exit 2 si échec) ;
        # un rescellement qui échoue ne doit JAMAIS produire une installation « verte ».
        r = subprocess.run([sys.executable,
                            os.path.join(HOST, "scripts", "task-f5-seal-archive-v25.py"),
                            "--depot-git", str(REPO)],
                           capture_output=True, text=True)
        report["etapes"]["2_archive"] = (r.stdout.strip() or r.stderr.strip())[-400:]
        if r.returncode != 0:
            report["etapes"]["2_archive"] = f"ÉCHEC rc={r.returncode} — {report['etapes']['2_archive']}"
            print(json.dumps(report, ensure_ascii=False, indent=2))
            sys.exit(2)
        # Étape 2bis (Task 100) — Régénération du manifeste d'intégrité (mode
        # COMPLET) : le rescellement a changé les octets de l'archive — le
        # manifeste (SHA archive + entrées piliers) est régénéré ICI par l'arbitre
        # canonique (pense-bête imprimé par le scelleur v2.3) ; rc propagé
        # (anti-faux-succès F1 Task 22).
        r2 = subprocess.run([sys.executable,
                             os.path.join(HOST, "scripts", "check-ecosysteme-integrity.py")],
                            capture_output=True, text=True)
        report["etapes"]["2_manifeste"] = (r2.stdout.strip() or r2.stderr.strip())[-200:]
        if r2.returncode != 0:
            report["etapes"]["2_manifeste"] = f"ÉCHEC rc={r2.returncode} — {report['etapes']['2_manifeste']}"
            print(json.dumps(report, ensure_ascii=False, indent=2))
            sys.exit(2)

    # F3 (Task 22) — Vérification post-install embarquée (fail-fast, lecture seule) :
    # SHA-256 des SKILL.md des entrées KB, hôte vs dépôt — toute divergence est un
    # défaut d'installation détecté ICI plutôt qu'à l'arbitre externe.
    divergences = []
    for s in familles:
        rel = os.path.join("skills", s, "SKILL.md")
        src, dst = os.path.join(REPO, rel), os.path.join(HOST, rel)
        if os.path.isfile(src) and os.path.isfile(dst):
            h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
            if h(src) != h(dst):
                divergences.append(s)
        elif os.path.isfile(src) and not os.path.isfile(dst):
            divergences.append(f"{s} (SKILL.md hôte absent)")
    report["post_install"] = {"sha256_verifies": len(familles),
                              "divergences": divergences}
    if divergences:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        sys.exit(2)

    report["dry_run"] = DRY
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
