#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.9)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.

Pipeline d'installation PM-INSTALL v1.8.0 (§2 — MÉCANISME DUAL : voie (a) installation
DIRECTE des formes certifiées du dépôt ; ce script en est l'EXÉCUTANT CANONIQUE)
réinstallation hôte post-wipe (§3.4 : wipe inter-sessions = cas documenté,
ré-exécution depuis l'étape 2).
Source : clone local du dépôt bigleon2/KNOWLEDGE @ b75a620 (règle d'or n°4 —
descendant-tolérant : merge-base --is-ancestor, jamais un état antérieur au pin,
évolution forward tolérée).
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

Étapes couvertes par ce script :
  1  Corpus   : sync skills/@mon-ecosysteme/ (9 PMs) + garde R2 anti-rétrogradation
  3-6 Formes  : sync skills/{gen-plan,correct-work,clone-chat,refactor-guard,disciplines,alias-eco}
  7  Registre : sync skills/KNOWLEDGE.md + @historique/@Alias/ (registre vivant)
  8  Outillage: sync scripts/ (arbitres + bootstrap), purge des reconstitutions
               provisoires non canoniques (config.json)
  2  Archive  : rescellement download/mon-ecosysteme_archive.zip (task21-f2)

Le dépôt et l'hôte partagent le même lignage (projection hôte 109 fichiers) :
union-merge sans --delete, fichiers dépôt = source de vérité au commit épinglé.
Les skills plateforme hors dépôt et les scripts de session sont conservés.
"""
import json
import os
import re
import shutil
import subprocess
import sys


def _resolve_repo():
    """Chemin du dépôt source (portabilité L008) : argv $1 > env ECO_REPO >
    candidats par défaut. Le premier répertoire contenant skills/KNOWLEDGE.md gagne."""
    candidats = []
    if len(sys.argv) > 1:
        candidats.append(sys.argv[1])
    if os.environ.get("ECO_REPO"):
        candidats.append(os.environ["ECO_REPO"])
    candidats += ["/home/z/my-project/KNOWLEDGE-repo",
                  "/home/z/my-project/tmp/KNOWLEDGE-repo"]
    for c in candidats:
        if os.path.isfile(os.path.join(c, "skills", "KNOWLEDGE.md")):
            return c
    sys.exit("ABANDON : aucun dépôt source trouvé (essayez : %s <chemin> ou ECO_REPO=<chemin>)"
             % sys.argv[0])


REPO = _resolve_repo()
HOST = "/home/z/my-project"
PIN = "b75a62066791a8cce8c1ec5d1dbe7d976bae4244"
# Task 20 (finding F1) : « scripts/verify-correct-work.py » RETIRÉ de la purge —
# ce fichier est un shim de compatibilité CERTIFIÉ (décision S2-α Task 12,
# re-validée propriétaire 2026-10-10 : délégation pure à l'arbitre canonique du
# skill, refus explicite rc=64 en mode rapport). La sync le projette
# légitimement à l'hôte (chemin relatif identique) et la purge le combattait à
# chaque run (purges != [] systématique, bruit + suppression d'un fichier
# légitime). Seules les reconstitutions réellement non canoniques sont purgées.
NON_CANONIQUES = ["config.json"]


def semver_of(skill_md):
    try:
        head = open(skill_md, encoding="utf-8", errors="replace").read(3000)
    except OSError:
        return None
    m = re.search(r"^version:\s*[\"']?(\d+\.\d+\.\d+)", head, re.M)
    return m.group(1) if m else None


def vtuple(v):
    return tuple(int(x) for x in v.split(".")) if v else (0, 0, 0)


def kb_eco_skills():
    """Entrées écosystème du registre KB dont la forme installée existe au dépôt
    (dérivation dynamique KO-L003 — périmètre COMPLET PM-INSTALL §2bis)."""
    import re as _re
    kb = open(os.path.join(REPO, "skills", "KNOWLEDGE.md"), encoding="utf-8").read()
    noms = _re.findall(r"^## ([\w-]+) v[\d.]+$", kb, _re.MULTILINE)
    return [n for n in noms
            if os.path.isfile(os.path.join(REPO, "skills", n, "SKILL.md"))]


def main():
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

    # F2 (Task 22) : exclusions de projection — artefacts de bytecode non canoniques
    EXCLUS_SYNC = ("__pycache__",)

    def sync(rel, delete=False):
        src = os.path.join(REPO, rel)
        dst = os.path.join(HOST, rel)
        if not os.path.exists(src):
            report["etapes"][rel] = "absent du dépôt (ignoré)"
            return
        if os.path.isfile(src):
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(src, dst)
            report["etapes"][rel] = "fichier sync"
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

    # Étape 8 — Outillage (union : scripts de session conservés)
    sync("scripts")

    # Purge des reconstitutions provisoires non canoniques
    for rel in NON_CANONIQUES:
        p = os.path.join(HOST, rel)
        if os.path.exists(p):
            os.remove(p)
            report["purges"].append(rel)
    # F2 (Task 22) : purge du bytecode hôte résiduel (hérité des runs antérieurs —
    # l'union sync ne supprime pas ; __pycache__/ n'est plus projeté depuis F2)
    _pyc = os.path.join(HOST, "scripts", "__pycache__")
    if os.path.isdir(_pyc):
        shutil.rmtree(_pyc)
        report["purges"].append("scripts/__pycache__")

    # Étape 2 — Rescellement archive d'intégrité (round-trip v2.2)
    # F1 (Task 22) : anti-faux-succès — le rc est propagé (exit 2 si échec) ;
    # un rescellement qui échoue ne doit JAMAIS produire une installation « verte ».
    r = subprocess.run([sys.executable,
                        os.path.join(HOST, "scripts", "task21-f2-rebuild-archive.py")],
                       capture_output=True, text=True)
    report["etapes"]["2_archive"] = (r.stdout.strip() or r.stderr.strip())[-400:]
    if r.returncode != 0:
        report["etapes"]["2_archive"] = f"ÉCHEC rc={r.returncode} — {report['etapes']['2_archive']}"
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
            import hashlib
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

    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
