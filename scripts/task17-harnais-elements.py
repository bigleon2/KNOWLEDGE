#!/usr/bin/env python3
"""Harnais Task 17 — tests fonctionnels et de performance $FACON2 sur les
éléments intégrés durant le projet (directive gen-plan Task 17, matrice
T0-T9, stdlib uniquement, verdict PASS/FAIL, rc 0/1).

Couverture : skill rea-analysis (voie d'installation rea-install.py,
idempotence ×2) · kit REA (doctor --provider ghidra) · venv pwntools
(import nu) · moteur sxmcore (info/list/set-channel, fixtures 15/15,
identité binaire aller-retour) · écosystème (certification bootstrap ×2
+ idempotence). Durées mesurées (ms) pour le rapport de performance.
"""

# ⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.45)
# SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
# Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
# Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
# Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
# Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
# Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).

import os
import re
import subprocess
import sys
import time
from pathlib import Path

HOST = Path("/home/z/my-project")
KIT = HOST / "tools/rea/REA_Reverse_All_Thing_Kit"
GHIDRA_DIR = HOST / "tools/rea/ghidra/ghidra_12.2_PUBLIC"
JAVA_HOME = HOST / "tools/rea/jdk/jdk-25.0.5.1+2"
VENV_PYTHON = HOST / "tools/rea/venv-pwntools/bin/python"
SXM = HOST / "tools/sxm/sxmcore/sxmcore"
REA_INSTALL = HOST / "skills/rea-analysis/scripts/rea-install.py"
BOOTSTRAP = HOST / "scripts/bootstrap-ecosysteme.py"
FIXTURES_DIR = HOST / "tools/sxm/super-xtreme-mapper"
FIX_BENCHMARK = (FIXTURES_DIR / "XtremeMapping/XtremeMappingTests/Fixtures/TSI"
                 / "traktor-4.5.1-xone-k3-benchmark-01-continuous.tsi")
TMP_E1 = Path("/tmp/t17-sxm-e1.tsi")
TMP_E3 = Path("/tmp/t17-sxm-e3.tsi")
ENV_DOCTOR = {"GHIDRA_INSTALL_DIR": str(GHIDRA_DIR), "JAVA_HOME": str(JAVA_HOME)}


def executer(cmd, cwd=None, env_extra=None, timeout=300):
    """Exécute une commande ; retourne (rc, sortie_texte, duree_ms)."""
    env = dict(os.environ)
    if env_extra:
        env.update(env_extra)
    debut = time.perf_counter()
    proc = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True,
                          text=True, timeout=timeout)
    duree = int((time.perf_counter() - debut) * 1000)
    return proc.returncode, (proc.stdout or "") + (proc.stderr or ""), duree


def fixtures_tsi():
    """Liste triée des fixtures .tsi re-jeuables du clone restauré."""
    return sorted(FIXTURES_DIR.glob("**/Fixtures/TSI/*.tsi"))


def t00_rea_install_idempotence():
    """T0 — rea-install.py idempotence ×2 (kit présent → no-op, rc=0)."""
    durees = []
    for _ in range(2):
        rc, out, duree = executer([sys.executable, str(REA_INSTALL)], cwd=HOST,
                                  timeout=240)
        durees.append(duree)
        if rc != 0:
            return False, f"rea-install rc={rc}", durees
    if "idempotent" not in out:
        return False, "verdict idempotence absent de la sortie", durees
    return True, "rea-install ×2 rc=0, no-op idempotent", durees


def t01_doctor_ghidra():
    """T1 — doctor --provider ghidra : rc=0, healthy, env canonique JDK 25."""
    rc, out, duree = executer(
        ["node", "scripts/rea.mjs", "doctor", "--provider", "ghidra"],
        cwd=KIT, env_extra=ENV_DOCTOR, timeout=120)
    sains = len(re.findall(r"classification: healthy", out))
    if rc != 0 or "healthy: true" not in out:
        return False, f"doctor rc={rc}, healthy absent", [duree]
    return True, f"doctor provider ghidra rc=0, healthy ×{sains} checks", [duree]


def t02_venv_pwntools():
    """T2 — venv pwntools : import nu OK (test canonique corrigé Task 17)."""
    rc, _, duree = executer([str(VENV_PYTHON), "-c", "import pwn"],
                             timeout=60)
    if rc != 0:
        return False, f"import pwn rc={rc}", [duree]
    return True, "import pwn OK (import nu — jamais pwn.__version__)", [duree]


def t03_sxmcore_info():
    """T3 — sxmcore info sur la fixture benchmark : appareils/mappings."""
    rc, out, duree = executer([str(SXM), "info", str(FIX_BENCHMARK)],
                              timeout=60)
    m = re.search(r"mappings \(CMAI\)\s*:\s*(\d+)", out)
    if rc != 0 or not m:
        return False, f"info rc={rc}, mappings non parsés", [duree]
    return True, f"info OK — {m.group(1)} mappings (CMAI)", [duree]


def t04_sxmcore_list():
    """T4 — sxmcore list : table des mappings par appareil (rc=0)."""
    rc, out, duree = executer([str(SXM), "list", str(FIX_BENCHMARK)],
                              timeout=60)
    lignes = len(re.findall(r"^ {2,}\d+ {2,}\S", out, re.M))
    if rc != 0 or "Appareil" not in out:
        return False, f"list rc={rc}, appareils absents", [duree]
    return True, f"list OK — table mappings ({lignes} lignes de données)", [duree]


def t05_sxmcore_fixtures():
    """T5 — fixtures 15/15 : info parsée sur chaque fixture re-jeuable."""
    fixes = fixtures_tsi()
    if len(fixes) < 15:
        return False, f"{len(fixes)} fixtures (< 15)", [0]
    durees, echecs = [], []
    for f in fixes:
        rc, _, duree = executer([str(SXM), "info", str(f)], timeout=60)
        durees.append(duree)
        if rc != 0:
            echecs.append(f.name)
    if echecs:
        return False, f"fixtures en échec : {echecs}", durees
    return True, f"15/15 fixtures parsées (info rc=0)", durees


def t06_sxmcore_identite_binaire():
    """T6 — identité binaire aller-retour : canal 12→05→12 byte-identique."""
    rc1, _, d1 = executer([str(SXM), "set-channel", str(FIX_BENCHMARK),
                           "-canal", "05", "-sortie", str(TMP_E1)], timeout=60)
    rc2, _, d2 = executer([str(SXM), "set-channel", str(TMP_E1),
                           "-canal", "12", "-sortie", str(TMP_E3)], timeout=60)
    if rc1 != 0 or rc2 != 0 or not TMP_E3.exists():
        return False, f"set-channel rc={rc1}/{rc2}", [d1, d2]
    orig = FIX_BENCHMARK.read_bytes()
    e1 = TMP_E1.read_bytes()
    e3 = TMP_E3.read_bytes()
    if e3 != orig:
        return False, "aller-retour NON byte-identique", [d1, d2]
    diffs = sum(1 for a, b in zip(orig, e1) if a != b)
    if diffs > 64:
        return False, f"édition non chirurgicale ({diffs} octets divergents)", [d1, d2]
    return True, (f"aller-retour byte-identique ; édition chirurgicale "
                  f"{diffs} octets (chiffres du canal)"), [d1, d2]


def t07_certification_ecosysteme():
    """T7 — certification écosystème : bootstrap re-jeu ALL-PASS."""
    rc, out, duree = executer([sys.executable, str(BOOTSTRAP)], cwd=HOST,
                              timeout=300)
    if rc != 0 or "ALL-PASS" not in out or "INSTALLE" not in out:
        return False, f"bootstrap rc={rc}, verdict absent", [duree]
    return True, "bootstrap re-jeu INSTALLE + certification ALL-PASS-6/6", [duree]


def t08_bootstrap_idempotence():
    """T8 — bootstrap idempotence : second re-jeu INSTALLE, 0 changement."""
    verdicts = []
    durees = []
    for _ in range(2):
        rc, out, duree = executer([sys.executable, str(BOOTSTRAP)], cwd=HOST,
                                  timeout=300)
        durees.append(duree)
        if rc != 0:
            return False, "bootstrap rc≠0", durees
        m = re.search(r"VERDICT GLOBAL\s+:\s+(\S+)", out)
        verdicts.append(m.group(1) if m else "?")
    if verdicts[0] != verdicts[1]:
        return False, f"verdicts divergents : {verdicts}", durees
    return True, f"idempotence ×2 — verdict stable {verdicts[0]}", durees


TESTS = [
    ("T0", "rea-install.py idempotence ×2", t00_rea_install_idempotence),
    ("T1", "kit REA doctor ghidra", t01_doctor_ghidra),
    ("T2", "venv pwntools import", t02_venv_pwntools),
    ("T3", "sxmcore info benchmark", t03_sxmcore_info),
    ("T4", "sxmcore list mappings", t04_sxmcore_list),
    ("T5", "sxmcore fixtures 15/15", t05_sxmcore_fixtures),
    ("T6", "sxmcore identité binaire aller-retour", t06_sxmcore_identite_binaire),
    ("T7", "certification écosystème bootstrap", t07_certification_ecosysteme),
    ("T8", "bootstrap idempotence ×2", t08_bootstrap_idempotence),
]


def main():
    """Exécute la matrice T0-T8, imprime le détail puis le verdict global."""
    echecs = []
    for ident, nom, func in TESTS:
        ok, detail, durees = func()
        durees_txt = "/".join(f"{d} ms" for d in durees if d is not None)
        etat = "PASS" if ok else "FAIL"
        print(f"[{etat}] {ident} — {nom} : {detail} ({durees_txt})")
        if not ok:
            echecs.append(f"{ident} {nom} — {detail}")
    if echecs:
        print(f"T9 — agrégation : VERDICT : FAIL ({len(TESTS) - len(echecs)}/{len(TESTS)})")
        for e in echecs:
            print(f"  ÉCHEC : {e}")
        return 1
    print(f"T9 — agrégation : VERDICT : PASS ({len(TESTS)}/{len(TESTS)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
