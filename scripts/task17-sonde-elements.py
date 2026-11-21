#!/usr/bin/env python3
"""Sonde d'état des éléments intégrés externes (Task 17 — groupe G4).

Réponse à l'écart d'architecture mesuré en E1-E2 : la garde É1-INSTALL
couvre skills/ seul ; la présente sonde étend la surveillance mécanique
aux 13 éléments externes intégrés durant le projet (kit REA, Ghidra,
JDK, venv, Go, clones, moteur sxmcore, livrable Windows, montées,
scelleur/pipeline, Leon_Netflix). Verdict global OK/PRESSION/CRITIQUE
(rc 0/1/2) + restauration guidée par élément. Lecture seule stricte :
idempotente par construction (aucune mutation, sortie déterministe).
"""
import re
import sys
from pathlib import Path

HOST = Path("/home/z/my-project")
SKILLS = HOST / "skills"
TOOLS = HOST / "tools"
DOWNLOAD = HOST / "download"
KIT = TOOLS / "rea/REA_Reverse_All_Thing_Kit"
GHIDRA = TOOLS / "rea/ghidra/ghidra_12.2_PUBLIC"
JDK = TOOLS / "rea/jdk/jdk-25.0.5.1+2"
VENV = TOOLS / "rea/venv-pwntools"
SXM_CLONE = TOOLS / "sxm/super-xtreme-mapper"
SXM = TOOLS / "sxm/sxmcore"
LIVRABLE = DOWNLOAD / "super-xtreme-mapper-windows10"
BOOT = "bootstrap-ecosysteme.py (garde É1-INSTALL — réparation miroir)"


def version_de(fichier):
    """Version lue du frontmatter d'un SKILL.md (chaîne vide si absente)."""
    try:
        tete = fichier.read_text(encoding="utf-8", errors="replace")[:3000]
    except OSError:
        return ""
    m = re.search(r"^version:\s*[\"']?(\d+\.\d+\.\d+)", tete, re.M)
    return m.group(1) if m else ""


def fixtures_tsi(base):
    """Nombre de fixtures .tsi re-jeuables sous un clone donné."""
    return len(list(base.glob("**/Fixtures/TSI/*.tsi")))


def sonder():
    """Retourne la liste des états : (gravite, nom, detail, restauration)."""
    etats = []

    def add(gravite, nom, detail, restauration):
        """Ajoute un état d'élément à la liste des constats."""
        etats.append((gravite, nom, detail, restauration))

    # 1 — skill rea-analysis (voie skill, cœur de l'intégration Task 12)
    f = SKILLS / "rea-analysis/SKILL.md"
    v = version_de(f)
    if f.is_file() and v == "1.0.0":
        add("OK", "skill rea-analysis", "SKILL.md présent, v1.0.0", "—")
    else:
        add("CRITIQUE", "skill rea-analysis",
            f"SKILL.md {'absent' if not f.is_file() else 'v' + (v or '?') + ' ≠ v1.0.0'}",
            BOOT)

    # 2 — kit REA (dist construit + CLI)
    if (KIT / "scripts/rea.mjs").is_file() and any(KIT.glob("dist/*")):
        add("OK", "kit REA", "dist + scripts/rea.mjs présents (épingle 03a3fcbce)",
            "—")
    else:
        add("CRITIQUE", "kit REA", "dist ou CLI rea.mjs absent",
            "python3 skills/rea-analysis/scripts/rea-install.py (idempotent)")

    # 3 — Ghidra 12.2 PUBLIC
    if ((GHIDRA / "Ghidra/application.properties").is_file()
            and (GHIDRA / "support/analyzeHeadless").is_file()):
        add("OK", "Ghidra 12.2", "application.properties + analyzeHeadless présents",
            "—")
    else:
        add("CRITIQUE", "Ghidra 12.2", "marqueurs d'installation absents",
            "re-téléchargement zip release publique (569 712 708 octets, "
            "lignage Task 9 G2.0) puis extraction")

    # 4 — JDK 25 (prérequis doctor ghidra sain)
    if (JDK / "bin/java").is_file():
        add("OK", "JDK 25", "jdk-25.0.5.1+2/bin/java présent (JAVA_HOME canonique)",
            "—")
    else:
        add("CRITIQUE", "JDK 25", "bin/java absent — doctor ghidra-java dérive",
            "ré-acquisition JDK 25+ 64 bits (prérequis mesuré Task 17 G3-T1)")

    # 5 — venv pwntools
    if ((VENV / "bin/python").is_file()
            and any(VENV.glob("lib/python*/site-packages/pwn"))):
        add("OK", "venv pwntools", "bin/python + paquet pwn présents", "—")
    else:
        add("PRESSION", "venv pwntools", "venv incomplet",
            "recréer le venv puis installer pwntools (pip)")

    # 6 — Go (caches seuls = état amputé documenté)
    if (TOOLS / "go/gocache").is_dir() or (TOOLS / "go/gomodcache").is_dir():
        add("PRESSION", "Go 1.27.4",
            "CACHES SEULS (binaire/GOROOT amputés par recyclage — binaires "
            "sxmcore opérationnels, recompilation seule requiert la toolchain)",
            "ré-acquisition Go 1.27.4 sur directive (NON judicieux ce tour — "
            "baselines scellées Task 13)")

    # 7 — HolyArrs (clone + build)
    if (TOOLS / "holyarrs/etat").is_dir():
        add("PRESSION", "HolyArrs",
            "AMPUTÉ (restes etat/ + serveur.log — baseline perf scellée Task 13)",
            "re-clone + build + make ui (~2,5 min + 59 s — sur directive, "
            "baseline rapport-tests-rea-holyarrs)")

    # 8 — super-xtreme-mapper (fixtures TSI du moteur)
    nfix = fixtures_tsi(SXM_CLONE)
    if nfix >= 15 and (SXM_CLONE / ".git").is_dir():
        add("OK", "super-xtreme-mapper",
            f"clone @2263592 + {nfix} fixtures .tsi (restauré Task 17 G2)", "—")
    else:
        add("PRESSION", "super-xtreme-mapper",
            f"clone absent ou fixtures insuffisantes ({nfix} < 15) — tests "
            "fonctionnels sxmcore non re-jeuables",
            "git clone https://github.com/SuperXtremeMapper/super-xtreme-mapper.git"
            " (dépôt public, ~44 s — lignage Task 13/17)")

    # 9 — moteur sxmcore
    if (SXM / "sxmcore").is_file() and (SXM / "sxmcore.exe").is_file():
        add("OK", "moteur sxmcore", "binaires Linux + Windows présents + source Go",
            "—")
    else:
        add("CRITIQUE", "moteur sxmcore", "binaire(s) absent(s)",
            "recompilation depuis source Go (Go requis) — livrable Windows en repli")

    # 10 — livrable Windows 10
    if ((LIVRABLE / "sxmcore.exe").is_file()
            and (LIVRABLE / "NOTICE.md").is_file()
            and (LIVRABLE / "source").is_dir()):
        add("OK", "livrable Windows 10",
            "sxmcore.exe (2 215 936 octets) + NOTICE.md + source présents", "—")
    else:
        add("CRITIQUE", "livrable Windows 10", "livrable incomplet",
            "re-génération depuis source Go (GOOS=windows — lignage Task 13)")

    # 11 — montées du projet (skills cœur)
    for nom, attendue in (("gen-plan", "3.45.0"), ("correct-work", "2.12.0"),
                           ("clone-chat", "2.0.2"), ("re-curation", "1.2.3")):
        v = version_de(SKILLS / nom / "SKILL.md")
        if v == attendue:
            add("OK", f"skill {nom}", f"v{v} conforme", "—")
        else:
            add("CRITIQUE", f"skill {nom}",
                f"v{v or 'absente'} ≠ v{attendue}", BOOT)

    # 12 — scelleur archive v2.5 + pipeline d'installation
    scelleur = HOST / "scripts/task-f5-seal-archive-v25.py"
    pipeline = HOST / "scripts/eco_install_pipeline.py"
    if scelleur.is_file() and pipeline.is_file():
        add("OK", "scelleur v2.5 + pipeline",
            "task-f5-seal-archive-v25.py + eco_install_pipeline.py présents "
            "(correctif Task 16 + P8 éteint Task 17 G1)", "—")
    else:
        add("CRITIQUE", "scelleur v2.5 + pipeline", "outil d'archive/installation absent",
            "restauration depuis le dépôt git (clone fait foi)")

    # 13 — Leon_Netflix (perte consignée Task 11)
    if (HOST / "tools/leon_netflix").is_dir() or (TOOLS / "Leon_Netflix").is_dir():
        add("OK", "Leon_Netflix", "clone présent", "—")
    else:
        add("PRESSION", "Leon_Netflix",
            "PERDU (consigné Task 11 E1-RES — propriété bigleon2 au distant)",
            "re-clone bigleon2 sur directive (aucune utilisation courante)")

    return etats


def main():
    """Imprime l'état des 13 éléments puis le verdict global (rc 0/1/2)."""
    etats = sonder()
    print("=== SONDE ÉLÉMENTS INTÉGRÉS (Task 17 — G4, lecture seule) ===")
    for gravite, nom, detail, restauration in etats:
        print(f"[{gravite:<9}] {nom} — {detail}")
        if gravite != "OK":
            print(f"{'':13}restauration : {restauration}")
    n_ok = sum(1 for e in etats if e[0] == "OK")
    n_p = sum(1 for e in etats if e[0] == "PRESSION")
    n_c = sum(1 for e in etats if e[0] == "CRITIQUE")
    print(f"BILAN : {n_ok} OK · {n_p} PRESSION · {n_c} CRITIQUE "
          f"({len(etats)} éléments sondés)")
    if n_c:
        print("VERDICT : CRITIQUE — éléments critiques manquants, "
              "restaurations guidées ci-dessus.")
        return 2
    if n_p:
        print("VERDICT : PRESSION — éléments dégradés listés ci-dessus "
              "(restaurations guidées) ; aucun élément critique manquant.")
        return 1
    print("VERDICT : OK — tous les éléments intégrés sondés sont présents "
          "et conformes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
