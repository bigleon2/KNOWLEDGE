#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.35)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).
"""

# -*- coding: utf-8 -*-
"""
Task 76 (D001) — Campagne de tests $FACON2 des systèmes d'installation.
Cibles : C1 PM-INSTALL (corpus v1.9.10 + exécutants canoniques) · C2 ENSURE-INSTALL
(garde É1-INSTALL skills/gen-plan/scripts/ensure-installed.py + shim racine).

Orchestration R4 : les verdicts des arbitres existants sont DÉLÉGUÉS (integrity,
poids, etc.) — le présent harnais MESURE (durées ms) et CONSIGNE, il ne duplique
aucune logique de verdict d'arbitre et n'écrit AUCUNE correction en phase PRE.
Nuance protocole : ensure-installed.py est ici la CIBLE (C2) — son invocation est
le test lui-même ; une éventuelle auto-réparation pendant C2 est son comportement
nominal (preuve vivante), consignée dans les détails du test concerné.

Modes : --phase pre|post --cible C1|C2|all · --synthese post · --protocole · --selftest
Sorties : download/rapport-campagne-task76-{pre|post}-{C1,C2}.json ·
          download/protocole-tests-installation-task76.json ·
          download/rapport-campagne-task76-post-synthese.json
Bac à sable auto-réparation : tmp/task76-sandbox/ (leçon L-75-a : sous le projet,
pas sous /tmp volatile).
"""
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DL = ROOT / "download"
SANDBOX = ROOT / "tmp" / "task76-sandbox"

PM_INSTALL_HOST = ROOT / "skills/@mon-ecosysteme/PROMPT-MAITRE-INSTALL-ECOSYSTEME.md"
PM_INSTALL_DEPOT = ROOT / "KNOWLEDGE-repo/skills/@mon-ecosysteme/PROMPT-MAITRE-INSTALL-ECOSYSTEME.md"
CORPUS = ROOT / "skills/@mon-ecosysteme"
KB = ROOT / "skills/KNOWLEDGE.md"
PIPELINE = ROOT / "scripts/eco_install_pipeline.py"
INSTALL_SH = ROOT / "scripts/install-ecosysteme-local.sh"
REBUILD_ARCHIVE = ROOT / "scripts/task21-f2-rebuild-archive.py"
ENSURE_SKILL = ROOT / "skills/gen-plan/scripts/ensure-installed.py"
ENSURE_ROOT_SHIM = ROOT / "scripts/ensure-installed.py"
FICHIERS_REFS = ROOT / "ecosysteme-travail/fichiers-refs"
ARCHIVE_HOST = DL / "mon-ecosysteme_archive.zip"
ARCHIVE_DEPOT = ROOT / "KNOWLEDGE-repo/download/mon-ecosysteme_archive.zip"

PIN_CERTIFIE = "a14f750"  # dernier commit certifié d'installation (Task 74 run 2 rc=0)
DATE_DERNIER_RECALIBRAGE = "2026-11-07"  # v1.9.10 (table des versions PM-INSTALL)

VERDICTS = ["PASS", "RÉSERVES", "FAIL"]


def sh(cmd, cwd=None, env=None, timeout=120):
    return subprocess.run(cmd, cwd=cwd, shell=isinstance(cmd, str), capture_output=True,
                          text=True, env=env, timeout=timeout)


def sha256_file(p):
    import hashlib
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def now_iso():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def pire(verdicts):
    for v in ("FAIL", "RÉSERVES", "PASS"):
        if v in verdicts:
            return v
    return "PASS"


def strict_kb_count(texte):
    return len([l for l in texte.splitlines()
                if re.match(r"^## [a-z0-9-]+ v\d+\.\d+\.\d+$", l.rstrip())])


# ---------------------------------------------------------------- C1 : PM-INSTALL

def parse_2ter(pm_texte):
    """Extrait (date_étiquette, {famille: (pm_fichier, version_cible)})."""
    m = re.search(r"### PMs sources des étapes 3-6 \(dernières versions au ([\d-]+)\)", pm_texte)
    date = m.group(1) if m else None
    familles = {}
    if m:
        seg = pm_texte[m.end():m.end() + 2500]
        for fam, pm, ver in re.findall(
                r"\|\s*(gen-plan|correct-work|clone-chat|refactor-guard)\s*\|"
                r"\s*`?(PROMPT-MAITRE-[A-Z-]+-v[\d.]+\.md)`?\s*\|"
                r"\s*\w[\w-]*\s+v([\d.]+)\s*\|", seg):
            familles[fam] = (pm, ver)
    return date, familles


def parse_pin(source):
    m = re.search(r'^PIN = "([0-9a-f]{40})"', source, re.M)
    return m.group(1) if m else None


def test_c1():
    t = []

    def add(tid, nom, fn):
        d0 = time.perf_counter()
        verdict, details = fn()
        t.append({"id": tid, "nom": nom, "verdict": verdict,
                  "duree_ms": round((time.perf_counter() - d0) * 1000, 1),
                  "details": details})

    pm = PM_INSTALL_HOST.read_text(encoding="utf-8", errors="replace")

    def f01():
        sections = ["§A", "§2 ", "§2bis", "§2ter", "§2quater", "§3 ", "§3.2", "§A.3"]
        manq = [s for s in sections if s not in pm]
        # dynamique (leçon G5 : la version attendue se dérive du fichier — la ligne
        # en-tête doit égaler la première entrée de la table §7, jamais figée)
        m_ver = re.search(r"^Version : (\d+\.\d+\.\d+)$", pm, re.M)
        v = m_ver.group(1) if m_ver else None
        m_hist = re.search(r"^\| v(\d+\.\d+\.\d+) \|", pm, re.M)
        v_hist = m_hist.group(1) if m_hist else None
        ok = (v is not None and v == v_hist and not manq)
        return ("PASS" if ok else "FAIL",
                f"version en-tête {v} == première entrée table §7 v{v_hist} "
                f"{'(cohérentes)' if v == v_hist else '(DIVERGENTES)'} ; sections "
                f"manquantes : {manq or 'aucune'} (§A/§2/§2bis/§2ter/§2quater/§3/§3.2/§A.3)")

    def f02():
        a, b = sha256_file(PM_INSTALL_HOST), sha256_file(PM_INSTALL_DEPOT)
        return ("PASS" if a == b else "FAIL",
                f"corpus hôte {'==' if a == b else '!='} dépôt (SHA {a[:12]}… / {b[:12]}…, "
                f"{PM_INSTALL_HOST.stat().st_size} o)")

    def f03():
        date, familles = parse_2ter(pm)
        manquants = [f"{f}: {pmf}" for f, (pmf, _) in familles.items()
                     if not (CORPUS / pmf).exists()]
        ok = len(familles) == 4 and not manquants
        return ("PASS" if ok else "FAIL",
                f"instantané §2ter : {len(familles)}/4 familles (gen-plan/correct-work/"
                f"clone-chat/refactor-guard) ; PM sources du corpus présents : "
                f"{'oui' if not manquants else manquants}")

    def f04():
        date, _ = parse_2ter(pm)
        ok = (date == DATE_DERNIER_RECALIBRAGE)
        return ("PASS" if ok else "FAIL",
                f"étiquette de date §2ter : « au {date} » — dernier recalibrage v1.9.10 : "
                f"{DATE_DERNIER_RECALIBRAGE} {'(à jour)' if ok else '(PÉRIMÉE — faille F5 : versions à jour mais date non rafraîchie par le générateur)'}")

    def f05():
        n = strict_kb_count(pm if False else KB.read_text(encoding="utf-8", errors="replace"))
        critere = n >= 14
        a3 = "§A.3" in pm and "skills/KNOWLEDGE.md" in pm
        return ("PASS" if (critere and a3) else "FAIL",
                f"critère §3 « ≥ 14 entrées KB » : {n} entrées au format strict "
                f"{'✓' if critere else '✗'} ; §A.3 → registre skills/KNOWLEDGE.md "
                f"{'référencé' if a3 else 'ABSENT'}")

    def f06():
        r = sh(["python3", "scripts/check-ecosysteme-integrity.py"], cwd=str(ROOT))
        ok = ("0 FAIL" in r.stdout) and r.returncode == 0
        return ("PASS" if ok else "FAIL",
                f"arbitre integrity (délégué R4) : « {[_l for _l in r.stdout.splitlines() if 'RESUME' in _l] or ['rc=' + str(r.returncode)]} »")

    def f07():
        probs = []
        for p in (PIPELINE, REBUILD_ARCHIVE):
            r = sh(["python3", "-m", "py_compile", str(p)], cwd=str(ROOT))
            if r.returncode != 0:
                probs.append(f"py_compile {p.name}")
        r = sh(["bash", "-n", str(INSTALL_SH)])
        if r.returncode != 0:
            probs.append("bash -n install-ecosysteme-local.sh")
        return ("PASS" if not probs else "FAIL",
                f"exécutants canoniques : eco_install_pipeline.py ({PIPELINE.stat().st_size} o) · "
                f"install-ecosysteme-local.sh ({INSTALL_SH.stat().st_size} o) · "
                f"task21-f2-rebuild-archive.py ({REBUILD_ARCHIVE.stat().st_size} o) — "
                f"{'tous présents et compilables' if not probs else probs}")

    def f08():
        src = PIPELINE.read_text(encoding="utf-8", errors="replace")
        a_help = ("--help" in src) or ("usage:" in src.lower())
        return ("PASS" if a_help else "FAIL",
                "contrat CLI du pipeline : gestion de --help/usage "
                f"{'PRÉSENTE' if a_help else 'ABSENTE (faille F1 — constat E2 réel : un appel --help a exécuté une installation complète le 2026-11-08, 0 contenu modifié [idempotence sauvée])'}")

    def f09():
        pin = parse_pin(PIPELINE.read_text(encoding="utf-8", errors="replace"))
        ok = pin is not None and pin.startswith(PIN_CERTIFIE)
        return ("PASS" if ok else "FAIL",
                f"PIN constant : {pin[:7] if pin else None} — dernier commit certifié "
                f"d'installation : {PIN_CERTIFIE} (Task 74 run 2 rc=0) "
                f"{'→ à jour' if ok else '→ OBSOLÈTE (faille F2 : garde anti-rétrogradation valide mais 3 commits certifiés plus récents : aa3b99d/a14f750/3171c4b)'}")

    def f10():
        d1 = (FICHIERS_REFS / "PM-INSTALL.md").exists() and \
            sha256_file(FICHIERS_REFS / "PM-INSTALL.md") == sha256_file(PM_INSTALL_HOST)
        d2 = (FICHIERS_REFS / "ensure-installed.py").exists() and \
            sha256_file(FICHIERS_REFS / "ensure-installed.py") == sha256_file(ENSURE_ROOT_SHIM)
        ok = d1 and d2
        return ("PASS" if ok else "FAIL",
                f"fichiers-refs ecosysteme-travail/ : PM-INSTALL.md "
                f"{'==' if d1 else '≠'} canonique · ensure-installed.py "
                f"{'==' if d2 else '≠'} shim racine "
                f"{'(formes de référence alignées)' if ok else '(faille F3 : copies d\'époque aa3b99d [installation Task 74] divergentes des formes canoniques courantes)'}")

    def f11():
        a, b = sha256_file(ARCHIVE_HOST), sha256_file(ARCHIVE_DEPOT)
        pareil = a == b
        return ("PASS" if pareil else "RÉSERVES",
                f"archive intégrité : hôte {a[:12]}… {'==' if pareil else '≠'} dépôt {b[:12]}… "
                + ("" if pareil else "— faille F4 à ADJUDIQUER (hypothèse règle d'or n°5 : piliers "
                                     "frais côté hôte [worklog suites postérieures au commit Task 75] ; "
                                     "stabilité byte du rescellement à tester en G4)"))

    def p01():
        taille = PM_INSTALL_HOST.stat().st_size
        tokens = len(pm) // 4
        return ("PASS", f"PM-INSTALL : {taille} o = {taille/1024:.1f} Kio · "
                        f"≈ {tokens} #token (chargé à l'installation uniquement — "
                        f"pas un chargement par défaut ; mesure de référence)")

    add("C1-F01", "structure PM-INSTALL (version + sections §A/§2/§2bis/§2ter/§2quater/§3/§3.2/§A.3)", f01)
    add("C1-F02", "sync corpus hôte ↔ dépôt (SHA-256 byte-identité)", f02)
    add("C1-F03", "§2ter instantané : 4 familles vs corpus réel", f03)
    add("C1-F04", "§2ter étiquette de date rafraîchie (F5)", f04)
    add("C1-F05", "critères §3 : ≥ 14 entrées KB + §A.3 → registre", f05)
    add("C1-F06", "critères §3 : registre certifié par l'arbitre integrity (R4)", f06)
    add("C1-F07", "exécutants canoniques présents et compilables", f07)
    add("C1-F08", "contrat CLI du pipeline — --help sans exécution (F1)", f08)
    add("C1-F09", "PIN pipeline à jour vs dernier commit certifié (F2)", f09)
    add("C1-F10", "fichiers-refs alignés aux formes canoniques (F3)", f10)
    add("C1-F11", "archive intégrité hôte ↔ dépôt (F4 — adjudication)", f11)
    add("C1-P01", "poids PM-INSTALL (mesure de référence #token)", p01)
    return t


# ---------------------------------------------------------- C2 : ENSURE-INSTALL

def build_sandbox():
    """Arbre factice isolé : ROOT factice = tmp/task76-sandbox (parents[3] du script copié)."""
    if SANDBOX.exists():
        shutil.rmtree(SANDBOX)
    fake = []
    lignes_kb = ["# KB factice Task 76", "",
                 "## @collection-factice v0.0.1  ", ""]
    for i in range(1, 15):
        nom = f"fake-skill-{i:02d}"
        fake.append(nom)
        lignes_kb.append(f"## {nom} v1.0.0")
        lignes_kb.append("")
        for base in (SANDBOX / "skills", SANDBOX / "KNOWLEDGE-repo/skills"):
            d = base / nom
            d.mkdir(parents=True, exist_ok=True)
            (d / "SKILL.md").write_text(f"---\nname: {nom}\nversion: 1.0.0\n---\n", encoding="utf-8")
    (SANDBOX / "skills/KNOWLEDGE.md").write_text("\n".join(lignes_kb), encoding="utf-8")
    # garde copiée telle quelle (ROOT dérivé = sandbox via parents[3])
    dest = SANDBOX / "skills/gen-plan/scripts"
    dest.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ENSURE_SKILL, dest / "ensure-installed.py")
    (SANDBOX / "skills/gen-plan/SKILL.md").write_text(
        "---\nname: gen-plan\nversion: 3.39.0\n---\n", encoding="utf-8")
    # FICHIERS_CLES (9) en stubs
    for rel in ("skills/correct-work/SKILL.md", "skills/skills-inventory/SKILL.md",
                "skills/@mon-ecosysteme/PROMPT-MAITRE-SHARED.md",
                "skills/@mon-ecosysteme/PROMPT-ULTRA-MAITRE-ORCHESTRATION.md",
                "skills/@mon-ecosysteme/SYNC-CONTEXT.md",
                "scripts/certification-complete.py", "scripts/ensure-installed.py"):
        p = SANDBOX / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("# stub factice Task 76\n", encoding="utf-8")
    return fake


def run_sandbox_ensure(*args):
    env = {k: v for k, v in os.environ.items() if k != "ECO_PROFILE_ROOT"}
    return sh(["python3", str(SANDBOX / "skills/gen-plan/scripts/ensure-installed.py"), *args],
              env=env)


def test_c2():
    t = []

    def add(tid, nom, fn):
        d0 = time.perf_counter()
        verdict, details = fn()
        t.append({"id": tid, "nom": nom, "verdict": verdict,
                  "duree_ms": round((time.perf_counter() - d0) * 1000, 1),
                  "details": details})

    def f01():
        probs = []
        for p in (ENSURE_SKILL, ENSURE_ROOT_SHIM):
            r = sh(["python3", "-m", "py_compile", str(p)], cwd=str(ROOT))
            if r.returncode != 0:
                probs.append(p.name)
        return ("PASS" if not probs else "FAIL",
                f"py_compile : garde skill ({ENSURE_SKILL.stat().st_size} o, 230 L) + "
                f"shim racine ({ENSURE_ROOT_SHIM.stat().st_size} o) "
                f"{'compilables' if not probs else probs}")

    def f02():
        r = sh(["python3", str(ENSURE_SKILL), "--check"], cwd=str(ROOT))
        try:
            j = json.loads(r.stdout)
        except Exception:
            return ("FAIL", f"sortie non JSON : {r.stdout[:200]} {r.stderr[:200]}")
        ok = r.returncode == 0 and j.get("verdict") == "INSTALLE"
        return ("PASS" if ok else "FAIL",
                f"--check réel : verdict {j.get('verdict')} rc={r.returncode} · "
                f"kb_entrees={j.get('kb_entrees')} · manquants={j.get('fichiers_manquants')} · "
                f"skills_kb_manquants={j.get('skills_kb_manquants')} · head miroir={j.get('head')}")

    sorties_check = []

    def f03():
        outs = []
        for _ in range(2):
            r = sh(["python3", str(ENSURE_SKILL), "--check"], cwd=str(ROOT))
            outs.append(r.stdout)
        pareil = outs[0] == outs[1]
        sorties_check.extend(outs)
        return ("PASS" if pareil else "FAIL",
                f"idempotence ×2 : sorties {'byte-identiques' if pareil else 'DIVERGENTES'} "
                f"(aucun horodatage dans la sortie → cmp direct)")

    def f04():
        r = sh(["python3", str(ENSURE_SKILL), "--preempt"], cwd=str(ROOT))
        ok = r.returncode == 0 and '"PRIORITE-NONE"' in r.stdout
        return ("PASS" if ok else "FAIL",
                f"--preempt : verdict "
                f"{json.loads(r.stdout).get('verdict') if r.stdout.strip().startswith('{') else r.stdout[:80]} "
                f"rc={r.returncode} (installé → PRIORITE-NONE attendu)")

    def f05():
        r = sh(["python3", str(ENSURE_SKILL), "--reinstall"], cwd=str(ROOT))
        ok = r.returncode == 0 and "Déjà installé" in r.stdout and "no-op" in r.stdout
        return ("PASS" if ok else "FAIL",
                f"--reinstall sur écosystème installé : {'no-op (idempotence D006) : ' if ok else ''}"
                f"{r.stdout.strip()[:120]} rc={r.returncode}")

    def f06():
        r = sh(["python3", str(ENSURE_SKILL), "--mode-inconnu"], cwd=str(ROOT))
        ok = r.returncode == 64 and "check" in r.stdout
        return ("PASS" if ok else "FAIL",
                f"mode inconnu : rc={r.returncode} (64 attendu) · docstring usage affichée "
                f"{'oui' if 'check' in r.stdout else 'NON'}")

    def f07():
        src = ENSURE_SKILL.read_text(encoding="utf-8", errors="replace")
        m = re.search(r"FICHIERS_CLES = \[(.*?)\]", src, re.S)
        fichiers = re.findall(r'"([^"]+)"', m.group(1)) if m else []
        manquants = [f for f in fichiers if not (ROOT / f).exists()]
        return ("PASS" if (fichiers and not manquants) else "FAIL",
                f"FICHIERS_CLES dérivés du source : {len(fichiers)}/9 présents · "
                f"manquants : {manquants or 'aucun'}")

    def f08():
        r = sh(["python3", str(ENSURE_SKILL), "--check"], cwd=str(ROOT))
        j = json.loads(r.stdout)
        n_indépendant = strict_kb_count(KB.read_text(encoding="utf-8", errors="replace"))
        ok = j.get("kb_entrees") == n_indépendant and not j.get("skills_kb_manquants")
        return ("PASS" if ok else "FAIL",
                f"détection KB dynamique : kb_entrees garde={j.get('kb_entrees')} == "
                f"décompte strict indépendant={n_indépendant} · skills_kb_manquants="
                f"{j.get('skills_kb_manquants')} (croisement mesure, verdict = sortie de la cible)")

    def f09():
        fake = build_sandbox()
        # scénario 1 : skill factif supprimé → AUTO-RÉPARATION attendue depuis miroir factif
        shutil.rmtree(SANDBOX / "skills" / "fake-skill-07")
        r1 = run_sandbox_ensure("--check")
        repare = (r1.returncode == 0 and "INSTALLE-REPARÉ" in r1.stdout
                  and "fake-skill-07" in r1.stdout
                  and (SANDBOX / "skills/fake-skill-07/SKILL.md").exists())
        # scénario 2 (contrôle négatif) : skill sans copie miroir → ABSENT-DERIVE rc=1
        shutil.rmtree(SANDBOX / "KNOWLEDGE-repo/skills/fake-skill-08")
        shutil.rmtree(SANDBOX / "skills/fake-skill-08")
        r2 = run_sandbox_ensure("--check")
        negatif = (r2.returncode == 1 and "ABSENT-DERIVE" in r2.stdout)
        trace = (SANDBOX / "worklog.md").exists()
        ok = repare and negatif
        return ("PASS" if ok else "FAIL",
                f"bac à sable tmp/task76-sandbox (14 skills factifs + KB factif + miroir factif, "
                f"isolé de l'écosystème réel) : (1) fake-skill-07 supprimé → "
                f"{'INSTALLE-REPARÉ rc=0, restauré depuis miroir factif, trace worklog sandbox ' + ('écrite' if trace else 'ABSENTE') if repare else 'ÉCHEC : ' + r1.stdout[:150] + r1.stderr[:100]}"
                f" ; (2) contrôle négatif fake-skill-08 sans copie miroir → "
                f"{'ABSENT-DERIVE rc=1 (aucune fausse réparation)' if negatif else 'ÉCHEC : rc=' + str(r2.returncode) + ' ' + r2.stdout[:100]}")

    def f10():
        r = sh(["python3", str(ENSURE_ROOT_SHIM), "--check"], cwd=str(ROOT))
        ok = r.returncode == 0 and '"INSTALLE"' in r.stdout
        return ("PASS" if ok else "FAIL",
                f"shim racine scripts/ensure-installed.py (délégation Task 29 D001) : "
                f"--check → verdict INSTALLE rc={r.returncode} "
                f"{'(délégation fonctionnelle)' if ok else '(échec)'}")

    def p01():
        r = sh(["python3", str(ENSURE_SKILL), "--check"], cwd=str(ROOT))
        return ("PASS", f"garde --check sur écosystème réel (54 entrées KB + git rev-parse ×2 + "
                        f"FICHIERS_CLES ×9 + scan disque) — durée mesurée au test C2-F02/F08 ; "
                        f"présent exécuté à titre de mesure isolée")

    add("C2-F01", "py_compile garde + shim (syntaxe)", f01)
    add("C2-F02", "--check réel : INSTALLE rc=0 (état installé)", f02)
    add("C2-F03", "idempotence ×2 : sorties byte-identiques", f03)
    add("C2-F04", "--preempt : PRIORITE-NONE rc=0", f04)
    add("C2-F05", "--reinstall no-op (idempotence D006)", f05)
    add("C2-F06", "mode inconnu : rc=64 + usage", f06)
    add("C2-F07", "FICHIERS_CLES 9/9 présents", f07)
    add("C2-F08", "détection KB dynamique : garde == décompte indépendant", f08)
    add("C2-F09", "auto-réparation en bac à sable (scénario + contrôle négatif)", f09)
    add("C2-F10", "shim racine : délégation fonctionnelle", f10)
    add("C2-P01", "performance garde (mesure --check isolée)", p01)
    return t


# ------------------------------------------------------------------ orchestration

def campagne(phase, cible):
    tests = []
    if cible in ("C1", "all"):
        tests += test_c1()
    if cible in ("C2", "all"):
        tests += test_c2()
    verdict = pire([x["verdict"] for x in tests])
    rapport = {"format": "campagne-task76 v1.0.0", "phase": phase, "cible": cible,
               "horodatage": now_iso(),
               "duree_totale_ms": round(sum(x["duree_ms"] for x in tests), 1),
               "verdict": verdict, "tests": tests}
    out = DL / f"rapport-campagne-task76-{phase}-{cible}.json"
    out.write_text(json.dumps(rapport, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[{phase}/{cible}] verdict {verdict} — {len(tests)} tests — "
          f"{rapport['duree_totale_ms']} ms → {out.name}")
    for x in tests:
        print(f"  {x['id']:8s} {x['verdict']:9s} {x['duree_ms']:7.1f} ms  {x['nom']}")
    return rapport


def synthese():
    donnees = {}
    for phase in ("pre", "post"):
        for c in ("C1", "C2"):
            p = DL / f"rapport-campagne-task76-{phase}-{c}.json"
            if p.exists():
                donnees[(phase, c)] = json.loads(p.read_text(encoding="utf-8"))
    if not donnees:
        sys.exit("Aucun rapport de campagne trouvé — exécuter --phase pre|post --cible d'abord")
    # non-régression test à test (leçon Task 73 : le verdict global POST n'agrège QUE les POST)
    non_regression, degradations, resorbees = True, [], []
    pre = {x["id"]: x for c in ("C1", "C2")
           for x in donnees.get(("pre", c), {}).get("tests", [])}
    post = {x["id"]: x for c in ("C1", "C2")
            for x in donnees.get(("post", c), {}).get("tests", [])}
    for tid, tpost in post.items():
        tpre = pre.get(tid)
        if tpre and VERDICTS.index(tpre["verdict"]) < VERDICTS.index(tpost["verdict"]):
            non_regression = False
            degradations.append(f"{tid}: {tpre['verdict']} -> {tpost['verdict']}")
        if tpre and tpre["verdict"] == "FAIL" and tpost["verdict"] == "PASS":
            resorbees.append(tid)
    v_post = pire([x["verdict"] for c in ("C1", "C2")
                   for x in donnees.get(("post", c), {}).get("tests", [])]) if any(
        (p, c) in donnees for p in ("post",) for c in ("C1", "C2")) else None
    v_pre = pire([x["verdict"] for c in ("C1", "C2")
                  for x in donnees.get(("pre", c), {}).get("tests", [])])
    synth = {"format": "synthese-task76 v1.0.1", "horodatage": now_iso(),
             "verdict_global_pre": v_pre, "verdict_global_post": v_post,
             "non_regression": non_regression, "degradations": degradations,
             "failles_resorbees": resorbees,
             "cibles": {f"{p}-{c}": donnees[(p, c)]["verdict"] for (p, c) in sorted(donnees)}}
    out = DL / "rapport-campagne-task76-post-synthese.json"
    out.write_text(json.dumps(synth, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(synth, ensure_ascii=False, indent=2))
    print(f"→ {out.name}")


def protocole():
    doc = {"format": "protocole-tests-installation-task76 v1.0.0", "horodatage": now_iso(),
           "echelle": "PASS < RÉSERVES < FAIL", "agregation": "pire-des-verdicts par cible",
           "phases": "PRE (capture sans correction) / POST (après corrections F1-F5)",
           "non_regression": "stricte test à test (aucun verdict dégradé PRE->POST)",
           "tolerances": ["WARN B1 coherence hérité (artefact historique propriétaire) — toléré",
                          "C1-F11 archive (F4) : RÉSERVES = divergence à adjudication mécanique en G4 "
                          "(hypothèse piliers frais — jamais affirmée sans preuve)",
                          "C2 : auto-réparation éventuelle pendant la campagne = comportement NOMINAL "
                          "de la cible (garde), consignée comme preuve vivante — pas une écriture corrective du harnais"],
           "cibles": {
               "C1": {"nom": "PM-INSTALL v1.9.10 (corpus + exécutants canoniques)",
                      "tests": [{"id": x["id"], "objet": x["nom"]} for x in
                                [{"id": t, "nom": n} for t, n in [
                                    ("C1-F01", "structure (version + sections)"),
                                    ("C1-F02", "sync corpus hôte↔dépôt"),
                                    ("C1-F03", "§2ter instantané 4 familles vs corpus"),
                                    ("C1-F04", "§2ter étiquette de date (F5)"),
                                    ("C1-F05", "critères §3 : ≥14 entrées KB + §A.3"),
                                    ("C1-F06", "registre certifié integrity (R4)"),
                                    ("C1-F07", "exécutants canoniques compilables"),
                                    ("C1-F08", "contrat CLI pipeline (F1)"),
                                    ("C1-F09", "PIN à jour (F2)"),
                                    ("C1-F10", "fichiers-refs alignés (F3)"),
                                    ("C1-F11", "archive hôte↔dépôt (F4)"),
                                    ("C1-P01", "poids #token référence")]]]},
               "C2": {"nom": "ENSURE-INSTALL (garde É1-INSTALL + shim racine)",
                      "tests": [{"id": x["id"], "objet": x["nom"]} for x in
                                [{"id": t, "nom": n} for t, n in [
                                    ("C2-F01", "py_compile garde + shim"),
                                    ("C2-F02", "--check INSTALLE rc=0"),
                                    ("C2-F03", "idempotence ×2"),
                                    ("C2-F04", "--preempt PRIORITE-NONE"),
                                    ("C2-F05", "--reinstall no-op"),
                                    ("C2-F06", "mode inconnu rc=64"),
                                    ("C2-F07", "FICHIERS_CLES 9/9"),
                                    ("C2-F08", "KB dynamique == décompte indépendant"),
                                    ("C2-F09", "auto-réparation bac à sable + contrôle négatif"),
                                    ("C2-F10", "délégation shim racine"),
                                    ("C2-P01", "performance --check")]]]}}}
    out = DL / "protocole-tests-installation-task76.json"
    out.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"protocole → {out.name} ({sum(len(c['tests']) for c in doc['cibles'].values())} tests)")


def selftest():
    """Selftest 8/8 — logique du harnais sur données synthétiques (jamais la réalité)."""
    res = []

    def check(nom, ok, info=""):
        res.append((nom, bool(ok), info))

    # 1. pire-des-verdicts
    check("agrégation pire-des-verdicts", pire(["PASS", "RÉSERVES", "PASS"]) == "RÉSERVES"
          and pire(["PASS", "PASS"]) == "PASS" and pire(["FAIL"]) == "FAIL")
    # 2. parseur §2ter sur table synthétique
    fake = ("### PMs sources des étapes 3-6 (dernières versions au 2026-11-07)\n\n"
            "| Famille | PM |\n|---|---|\n"
            "| gen-plan | `PROMPT-MAITRE-GEN-PLAN-v3.39.0.md` | gen-plan v3.39.0 | 3 |\n"
            "| correct-work | `PROMPT-MAITRE-CORRECT-WORK-v2.11.0.md` | correct-work v2.11.0 | 4 |\n")
    d, f = parse_2ter(fake)
    check("parseur §2ter (date + familles)", d == "2026-11-07" and
          f.get("gen-plan", ("",))[0] == "PROMPT-MAITRE-GEN-PLAN-v3.39.0.md" and len(f) == 2)
    # 3. parseur PIN (chaîne de test construite à 40 caractères hex exactement)
    pin40 = "a14f750" + "0" * 33
    check("parseur PIN", parse_pin(f'PIN = "{pin40}"') == pin40
          and len(pin40) == 40 and parse_pin("PIN=3") is None)
    # 4. sandbox : état INSTALLE d'emblée
    build_sandbox()
    r = run_sandbox_ensure("--check")
    check("bac à sable : INSTALLE d'emblée", r.returncode == 0 and "INSTALLE" in r.stdout,
          r.stdout[:120])
    # 5. sandbox : réparation
    shutil.rmtree(SANDBOX / "skills/fake-skill-03")
    r = run_sandbox_ensure("--check")
    check("bac à sable : INSTALLE-REPARÉ + restauration",
          r.returncode == 0 and "INSTALLE-REPARÉ" in r.stdout and "fake-skill-03" in r.stdout
          and (SANDBOX / "skills/fake-skill-03/SKILL.md").exists(), r.stdout[:120])
    # 6. sandbox : contrôle négatif
    shutil.rmtree(SANDBOX / "KNOWLEDGE-repo/skills/fake-skill-04")
    shutil.rmtree(SANDBOX / "skills/fake-skill-04")
    r = run_sandbox_ensure("--check")
    check("bac à sable : négatif ABSENT-DERIVE rc=1",
          r.returncode == 1 and "ABSENT-DERIVE" in r.stdout, r.stdout[:120])
    # 7. comptage strict KB (lâche vs strict)
    check("comptage strict KB (anti lâche)",
          strict_kb_count("## alpha v1.0.0\n## Beta v2.0.0\n## pas une entrée v1\n") == 1)
    # 8. non-régression logique (synthèse sur verdicts synthétiques)
    pre = {"A": "FAIL", "B": "PASS", "C": "PASS"}
    post = {"A": "PASS", "B": "PASS", "C": "FAIL"}
    deg = [k for k in post if k in pre and VERDICTS.index(pre[k]) < VERDICTS.index(post[k])]
    reso = [k for k in post if pre.get(k) == "FAIL" and post[k] == "PASS"]
    check("non-régression (FAIL->PASS ok, PASS->FAIL ko)",
          deg == ["C"] and reso == ["A"]
          and VERDICTS.index("FAIL") > VERDICTS.index("PASS"))
    # nettoyage
    if SANDBOX.exists():
        shutil.rmtree(SANDBOX)
    ok = sum(1 for _, o, _ in res if o)
    for nom, o, info in res:
        print(f"  [{'OK' if o else 'KO'}] {nom} {info}")
    print(f"RESUME : {'OK' if ok == len(res) else 'KO'} ({ok}/{len(res)})")
    return 0 if ok == len(res) else 1


def main():
    args = sys.argv[1:]
    if not args or "--selftest" in args:
        sys.exit(selftest())
    if "--protocole" in args:
        protocole()
        return
    if "--synthese" in args:
        synthese()
        return
    phase, cible = None, None
    if "--phase" in args:
        phase = args[args.index("--phase") + 1]
    if "--cible" in args:
        cible = args[args.index("--cible") + 1]
    if phase in ("pre", "post") and cible in ("C1", "C2", "all"):
        if cible == "all":
            campagne(phase, "C1")
            campagne(phase, "C2")
        else:
            campagne(phase, cible)
        return
    print(__doc__)
    sys.exit(64)


if __name__ == "__main__":
    main()
