#!/usr/bin/env python3
"""t13-cw-projet-rejeu.py — re-jeu mécanique correct-work (PROJET) bloc par bloc.

Task ID 13 / G6.1 — v2.12.0 : mode PROJET « bloc par bloc » PAR DÉFAUT.
Re-jeu des vérifications de l'answer key du plan maître (D001-D011) et du
plan interne (D101-D107), agrégation = pire des verdicts (§1.4).
Supersessions documentées au plan lui-même (D001/D003 : v3.44.0 → v3.45.0 —
critère substantiel intact, Task 12 KO-L005 re-validation).
"""
# ⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.47)
# SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
# Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
# Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
# Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
# Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
# Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).

import glob
import pathlib
import re
import subprocess
import sys

RACINE = "/home/z/my-project"
PLAN = RACINE + "/download/plan-actions-optimisation-skills-rea-2026-11-20T20h00Z.md"
PLAN_INTERNE = sorted(glob.glob(RACINE + "/download/plan-interne-integration-rea-*.md"))[-1]


def verifie(nom, fonction):
    """Exécute une vérification nommée en captant toute exception (diagnostic honnête, jamais un crash muet)."""
    try:
        ok, note = fonction()
    except Exception as exc:  # noqa: BLE001 — diagnostic honnête, jamais un crash muet
        ok, note = False, f"exception: {exc}"
    return (nom, ok, note)


def lit(chemin):
    """Lit un fichier texte en UTF-8 et retourne son contenu."""
    with open(chemin, encoding="utf-8") as fh:
        return fh.read()


# --- B1 : optimisations skills (D001-D003) ---


def d001():
    """D001 — supersession gen-plan v3.44.0→v3.45.0 : clauses substantielles + journal des versions."""
    s = lit(RACINE + "/skills/gen-plan/SKILL.md")
    j = lit(RACINE + "/skills/gen-plan/references/journal-versions.md")
    substantiel = (
        "granularité étape" in s
        and "par étape terminée" in s
        and "CIBLE" in s
        and "JAMAIS" in s
    )
    version = "version: 3.45.0" in s
    journal = "v3.43.0" in j and "v3.44.0" in j
    return (version and substantiel and journal,
            f"v3.45.0={version} clauses={substantiel} journal={journal} (supersession v3.44.0→v3.45.0 documentée Task 12)")


def d002():
    """D002 — correct-work v2.12.0 : §1.7 bloc par bloc PAR DÉFAUT + arbitre canonique 16/16."""
    s = lit(RACINE + "/skills/correct-work/SKILL.md")
    version_ok = re.search(r"^version: 2\.12\.0$", s, re.M) is not None
    corps_ok = "PAR DÉFAUT du mode PROJET" in s and "synonyme explicite" in s
    r = subprocess.run(
        ["python3", RACINE + "/scripts/verify-correct-work.py"],
        capture_output=True, text=True, timeout=300,
    )
    arbitre = r.returncode == 0 and "ALL PASS" in r.stdout
    return (version_ok and corps_ok and arbitre,
            f"v2.12.0={version_ok} §1.7={corps_ok} arbitre 16/16={arbitre}")


def d003():
    """D003 — cascade v3.45.0/v2.12.0 : PMs du corpus + entrées KB + @historique."""
    pm_gen = glob.glob(RACINE + "/skills/@mon-ecosysteme/*GEN-PLAN-v3.45.0*") + glob.glob(
        RACINE + "/skills/@mon-ecosysteme/*gen-plan*v3.45.0*")
    pm_cw = glob.glob(RACINE + "/skills/@mon-ecosysteme/*CORRECT-WORK-v2.12.0*") + glob.glob(
        RACINE + "/skills/@mon-ecosysteme/*correct-work*v2.12.0*")
    k = lit(RACINE + "/skills/KNOWLEDGE.md")
    kb_ok = "## gen-plan v3.45.0" in k and "## correct-work v2.12.0" in k
    h1 = lit(RACINE + "/skills/@historique/historiques-par-skill/gen-plan.md")
    h2 = lit(RACINE + "/skills/@historique/historiques-par-skill/correct-work.md")
    hist_ok = "v3.44.0" in h1 and "v3.45.0" in h1 and "v2.12.0" in h2
    return (bool(pm_gen) and bool(pm_cw) and kb_ok and hist_ok,
            f"PM gen-plan v3.45.0={bool(pm_gen)} PM cw v2.12.0={bool(pm_cw)} KB={kb_ok} @historique={hist_ok} (supersession v3.44.0 corpus → @historique R4, Task 12)")


# --- B2 : plan interne + intégration REA (D004-D005 + D101-D107) ---


def d004():
    """D004 — arbitre P1-P5 du plan interne (check_plan_protocol.py)."""
    r = subprocess.run(
        ["python3", RACINE + "/skills/gen-plan/scripts/check_plan_protocol.py",
         "--plan", PLAN_INTERNE, "--worklog", RACINE + "/worklog.md"],
        capture_output=True, text=True, timeout=300,
    )
    return (r.returncode == 0 and "PASS" in r.stdout, "arbitre P1-P5 plan interne : " + r.stdout.strip().splitlines()[-1][:80] if r.stdout else "sans sortie")


def d005():
    """D005 — skill rea-analysis v1.0.0 : SKILL.md + entrée KB + rea-install.py présent."""
    s = lit(RACINE + "/skills/rea-analysis/SKILL.md")
    k = lit(RACINE + "/skills/KNOWLEDGE.md")
    ok = (
        "name: rea-analysis" in s
        and re.search(r"^version: 1\.0\.0$", s, re.M) is not None
        and "## rea-analysis" in k
    )
    script = pathlib.Path(RACINE + "/skills/rea-analysis/scripts/rea-install.py")
    return (ok and script.exists(), f"SKILL.md={ok} KB='## rea-analysis'={'## rea-analysis' in k} rea-install.py={script.exists()}")


def d101():
    """D101 — kit REA opérationnel : arbre + dist + node_modules + sonde CLI rc=0."""
    kit = pathlib.Path(RACINE + "/tools/rea/REA_Reverse_All_Thing_Kit")
    r = subprocess.run(
        ["node", "scripts/rea.mjs", "--help"],
        cwd=kit, capture_output=True, text=True, timeout=120,
    )
    ok = kit.exists() and (kit / "dist").exists() and (kit / "node_modules").exists() and r.returncode == 0
    return (ok, f"kit présent={kit.exists()} dist={(kit / 'dist').exists()} node_modules={(kit / 'node_modules').exists()} CLI rc={r.returncode}")


def d102_d103_d104():
    """D102-D104 — auto-contenance rea-analysis : frontmatter, scripts/références, py_compile, KB/@historique."""
    p = pathlib.Path(RACINE + "/skills/rea-analysis")
    s = (p / "SKILL.md").read_text()
    ok_102 = "name: rea-analysis" in s and "version: 1.0.0" in s
    ok_103 = (p / "scripts" / "rea-install.py").exists() and (p / "references" / "referentiel-kit-rea.md").exists()
    r = subprocess.run(
        ["python3", "-m", "py_compile", str(p / "scripts" / "rea-install.py")],
        capture_output=True,
    )
    k = lit(RACINE + "/skills/KNOWLEDGE.md")
    h = pathlib.Path(RACINE + "/skills/@historique/historiques-par-skill/rea-analysis.md")
    i = lit(RACINE + "/scripts/check-ecosysteme-integrity.py")
    ok_104 = "## rea-analysis v1.0.0" in k and h.exists() and '"rea-analysis": "1.0.0"' in i
    return (ok_102 and ok_103 and r.returncode == 0 and ok_104,
            f"D102={ok_102} D103={ok_103}+py_compile rc={r.returncode} D104={ok_104}")


def d105():
    """D105 — idempotence rea-install.py (re-jeu no-op attendu)."""
    r = subprocess.run(
        ["python3", RACINE + "/skills/rea-analysis/scripts/rea-install.py"],
        capture_output=True, text=True, timeout=590,
    )
    return (r.returncode == 0, "re-jeu rea-install.py rc=" + str(r.returncode) + " (no-op idempotent attendu)")


def d106_d107():
    """D106-D107 — GO anonyme KO-L009 au worklog + statut D005 verified au plan maître."""
    s = lit(RACINE + "/worklog.md")
    i = s.find("Task ID: 12")
    ok_106 = i > 0 and "anonyme" in s[i:].lower() and "KO-L009" in s[i:]
    m = re.search(r'id: "D005"[^}]*?status: "(\w+)"', lit(PLAN), re.S)
    ok_107 = m is not None and m.group(1) == "verified"
    return (ok_106 and ok_107, f"D106 GO anonyme+KO-L009 worklog={ok_106} D107 D005 verified={ok_107}")


# --- B3 : tests REA×HolyArrs (D006) ---


def d006():
    """D006 — rapport tests REA×HolyArrs : sections T1/T2/T3/VERDICT présentes."""
    p = sorted(glob.glob(RACINE + "/download/rapport-tests-rea-holyarrs-*.md"))
    if not p:
        return (False, "rapport absent")
    s = lit(p[-1])
    ok = all(m in s for m in ("T1", "T2", "T3", "VERDICT")) and len(s) > 3000
    return (ok, f"rapport {p[-1].split('/')[-1]} {len(s)} o — T1/T2/T3/VERDICT={'OK' if ok else 'KO'}")


# --- B4 : reproduction SXM WINDOWS (D007) ---


def d007():
    """D007 — rapport reproduction SXM + binaire sxmcore.exe > 1 Mo."""
    p = sorted(glob.glob(RACINE + "/download/rapport-reproduction-sxm-windows-*.md"))
    if not p:
        return (False, "rapport absent")
    s = lit(p[-1])
    exe = pathlib.Path(RACINE + "/download/super-xtreme-mapper-windows10/sxmcore.exe")
    ok = "VERDICT" in s and "WINDOWS" in s.upper() and exe.exists() and exe.stat().st_size > 1000000
    return (ok, f"rapport {p[-1].split('/')[-1]} + sxmcore.exe {exe.stat().st_size if exe.exists() else 0} o")


# --- B5 : clôtures (D008-D011) ---


def segment_worklog():
    """Retourne le worklog à partir de l'entrée Task ID 11 (segment des clôtures)."""
    s = lit(RACINE + "/worklog.md")
    i = s.find("Task ID: 11")
    return s[i:] if i > 0 else ""


def d008():
    """D008 — trace correct-work (projet) bloc par bloc au worklog."""
    s = segment_worklog()
    ok = "correct-work (projet)" in s and "bloc" in s.lower() and "PASS" in s
    return (ok, "worklog post-Task 11 : trace cw(projet) bloc par bloc + verdict")


def d009():
    """D009 — clone-chat scellé 8/8 présent en download/."""
    p = sorted(glob.glob(RACINE + "/download/clone-chat-session-web-93a4f011-*.md"))
    if not p:
        return (False, "clone absent")
    s = lit(p[-1])
    ok = "web-93a4f011" in s and ("8/8" in s or "S1-S8" in s or "S8" in s)
    return (ok, f"clone {p[-1].split('/')[-1]} {len(s)} o")


def d010():
    """D010 — langue française + trace directive consignées."""
    s = segment_worklog()
    ok = "française" in s.lower() and "1a1fa860dff81f4d" in s
    return (ok, "langue française + trace 1a1fa860dff81f4d consignées")


def d011():
    """D011 — KO-L009 ONE-SHOT + rotation + scan 0 occurrence consignés."""
    s = segment_worklog()
    ok = (
        "KO-L009" in s
        and "ONE-SHOT" in s
        and "rotation" in s.lower()
        and ("0 occurrence" in s or "0 hit" in s or "rc=1" in s)
    )
    return (ok, "KO-L009 ONE-SHOT + rotation + scan 0 occurrence consignés")


def main():
    """Re-jeu intégral bloc par bloc, agrégation = pire des verdicts (§1.4)."""
    blocs = [
        ("B1 — optimisations skills (G1-G2)", [verifie("D001", d001), verifie("D002", d002), verifie("D003", d003)]),
        ("B2 — plan interne + intégration REA (G3)", [verifie("D004", d004), verifie("D005", d005), verifie("D101", d101), verifie("D102-D104", d102_d103_d104), verifie("D105", d105), verifie("D106-D107", d106_d107)]),
        ("B3 — tests REA×HolyArrs (G4)", [verifie("D006", d006)]),
        ("B4 — reproduction SXM WINDOWS 10 (G5)", [verifie("D007", d007)]),
        ("B5 — clôtures (G6)", [verifie("D008", d008), verifie("D009", d009), verifie("D010", d010), verifie("D011", d011)]),
    ]
    print("correct-work (PROJET) — re-jeu bloc par bloc (v2.12.0, agrégation = pire des verdicts §1.4)")
    print()
    total_ok = 0
    total = 0
    verdicts = []
    for nom_bloc, checks in blocs:
        tous_ok = all(ok for _, ok, _ in checks)
        verdicts.append((nom_bloc, tous_ok))
        print(f"[{nom_bloc}] verdict : {'PASS' if tous_ok else 'FAIL'}")
        for nom, ok, note in checks:
            marque = "PASS" if ok else "FAIL"
            print(f"    {nom:12s} {marque} — {note}")
            total += 1
            total_ok += 1 if ok else 0
    print()
    global_ok = all(ok for _, ok in verdicts)
    print(f"AGRÉGATION (pire des verdicts) : {'PASS' if global_ok else 'FAIL'} — {total_ok}/{total} vérifications PASS")
    return 0 if global_ok else 1


if __name__ == "__main__":
    sys.exit(main())
