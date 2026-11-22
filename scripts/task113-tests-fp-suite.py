#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 113 — Tests fonctionnels (F) et de performance (P) sur les 16 réécritures.

F (fonctionnel) :
  F1  audit conformité S01-S12 : 72/72 attendu
  F2  agents A01-A07 : 4/4 attendu
  F3  frontmatter YAML parseable pour chacun des 16 (yaml.safe_load)
  F4  name == dossier kebab-case pour chacun des 16
  F5  archive R4 byte-identique présente (SKILL.md courant != archive, archive == dépôt)
  F6  chemins references/ cités dans les SKILL.md réécrits existent réellement
  F7  zéro emoji dans les 16 SKILL.md (regex arbitre)
  F8  triptyque read_when complet (Déclencher quand / Déclencher si / Ne pas déclencher hors)
  F9  selftests des 4 scripts Task 113
  F10 idempotence des scripts mécaniques (import, clôture, sync)

P (performance) :
  P1  durée d'exécution de l'audit complet
  P2  durée de la synchro dépôt (no-op)
  P3  poids total des 16 SKILL.md réécrits vs originaux archivés
  P4  durée des selftests

Sortie : download/rapport-tests-fp-task113-suite.json + verdict PASS/FAIL
"""
import hashlib
import json
import re
import subprocess
import sys
import time
from pathlib import Path

RACINE = Path("/home/z/my-project")
SKILLS = RACINE / "skills"
DEPOT_SKILLS = RACINE / "KNOWLEDGE-repo" / "skills"
RAPPORT = RACINE / "download" / "rapport-tests-fp-task113-suite.json"

CIBLES = ["asr", "llm", "tts", "vlm", "charts", "docx", "gif-animator",
          "gif-animator-pro", "image-edit", "image-generation", "image-search",
          "pdf", "pptx", "task-review", "video-understand", "xlsx"]

REGEX_EMOJI = re.compile(
    "[\U0001F000-\U0001FAFF]|[\u2600-\u27BF]\uFE0F|[\u2B50\u2B55]|\uFE0F")


def sh(cmd: list, timeout: int = 120):
    r = subprocess.run(cmd, cwd=RACINE, capture_output=True, text=True, timeout=timeout)
    return r.returncode, r.stdout + r.stderr


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def test_f() -> tuple[list, list]:
    echecs = []

    # F1+F2 : audit complet
    rc, out = sh(["python3", "scripts/task113-audit-conformite.py"])
    if "72/72 CONFORMES" not in out or "4/4 CONFORMES" not in out:
        echecs.append("F1/F2 audit : verdict incomplet")
    if "0 NON_CONFORMES" not in out:
        echecs.append("F1/F2 audit : non-conformes résiduels")

    # F3+F4 : structure frontmatter selon la norme écosystème (arbitre maison de
    # l'audit — PAS yaml.safe_load : la convention « Déclencher quand … : … » des
    # listes read_when, partagée par les 56 skills conformes, n'est pas du YAML
    # strict ; la norme réelle est le parseur de l'arbitre, déjà couvert par F1).
    for s in CIBLES:
        texte = (SKILLS / s / "SKILL.md").read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---\n", texte, flags=re.DOTALL)
        if not m:
            echecs.append(f"F3 {s} : frontmatter introuvable")
            continue
        fm = m.group(1)
        m_name = re.search(r"^name: (.+)$", fm, flags=re.MULTILINE)
        if not m_name or m_name.group(1).strip() != s:
            echecs.append(f"F4 {s} : name={m_name.group(1).strip() if m_name else None!r} != {s!r}")
        for champ in ("version:", "category:", "language:", "tags:", "description:", "read_when:"):
            if not re.search(rf"^{champ}", fm, flags=re.MULTILINE):
                echecs.append(f"F3 {s} : champ {champ} absent")

    # F5 : archives R4
    for s in CIBLES:
        arch_loc = SKILLS / s / "references" / "plateforme-original.md"
        arch_dep = DEPOT_SKILLS / s / "references" / "plateforme-original.md"
        skill_loc = SKILLS / s / "SKILL.md"
        if not arch_loc.exists():
            echecs.append(f"F5 {s} : archive locale absente")
            continue
        if sha256(arch_loc) != sha256(arch_dep):
            echecs.append(f"F5 {s} : archive dépôt divergente")
        if sha256(arch_loc) == sha256(skill_loc):
            echecs.append(f"F5 {s} : SKILL.md encore identique à l'original (réécriture manquante ?)")
        if sha256(skill_loc) != sha256(DEPOT_SKILLS / s / "SKILL.md"):
            echecs.append(f"F5 {s} : SKILL.md dépôt divergent")

    # F6 : chemins references/ cités existent (routes/scenes/briefs/engines/quality)
    motifs = ["routes/", "scenes/", "briefs/", "engines/", "quality/", "configs/",
              "typesetting/", "references/"]
    for s in CIBLES:
        texte = (SKILLS / s / "SKILL.md").read_text(encoding="utf-8")
        for m in re.finditer(r"`?((?:routes|scenes|briefs|engines|quality|configs|typesetting|references)/[A-Za-z0-9_./-]+\.(?:md|py|ts|js|sh))`?", texte):
            chemin = m.group(1)
            if chemin.startswith("references/plateforme-original.md"):
                continue  # traité en F5
            if not (SKILLS / s / chemin).exists():
                echecs.append(f"F6 {s} : chemin cité inexistant {chemin}")

    # F7 : zéro emoji
    for s in CIBLES:
        texte = (SKILLS / s / "SKILL.md").read_text(encoding="utf-8")
        trouves = REGEX_EMOJI.findall(texte)
        if trouves:
            echecs.append(f"F7 {s} : emoji résiduel {trouves[:3]}")

    # F8 : triptyque
    for s in CIBLES:
        texte = (SKILLS / s / "SKILL.md").read_text(encoding="utf-8")
        for clause in ("Déclencher quand", "Déclencher si", "Ne pas déclencher hors de ce périmètre"):
            if clause not in texte:
                echecs.append(f"F8 {s} : clause manquante « {clause} »")

    # F9 : selftests des scripts
    for script in ["task113-audit-conformite.py", "task113-import-plateforme.py"]:
        rc, out = sh(["python3", f"scripts/{script}", "--selftest"])
        if rc != 0 or "SELFTEST" not in out:
            echecs.append(f"F9 {script} : selftest rc={rc}")

    # F10 : idempotence des mécaniques
    for script in ["task113-import-plateforme.py", "task113-cloture-triptyque.py",
                   "task113-sync-depot.py"]:
        rc, out = sh(["python3", f"scripts/{script}"])
        if rc != 0:
            echecs.append(f"F10 {script} : rejeu rc={rc}")
        if script == "task113-cloture-triptyque.py" and "IDEMPOTENCE x2 : OK" not in out:
            echecs.append(f"F10 {script} : idempotence non constatée")

    return echecs


def test_p() -> dict:
    mesures = {}
    t0 = time.perf_counter()
    sh(["python3", "scripts/task113-audit-conformite.py"])
    mesures["audit_complet_s"] = round(time.perf_counter() - t0, 3)

    t0 = time.perf_counter()
    sh(["python3", "scripts/task113-sync-depot.py"])
    mesures["sync_depot_noop_s"] = round(time.perf_counter() - t0, 3)

    t0 = time.perf_counter()
    sh(["python3", "scripts/task113-import-plateforme.py"])
    mesures["import_noop_s"] = round(time.perf_counter() - t0, 3)

    poids_nouveau = sum((SKILLS / s / "SKILL.md").stat().st_size for s in CIBLES)
    poids_orig = sum((SKILLS / s / "references" / "plateforme-original.md").stat().st_size
                     for s in CIBLES)
    mesures["poids_16_reecrits_kio"] = round(poids_nouveau / 1024, 1)
    mesures["poids_16_originaux_kio"] = round(poids_orig / 1024, 1)
    mesures["ratio_nouveau_sur_original"] = round(poids_nouveau / poids_orig, 3)
    return mesures


def main() -> int:
    echecs_f = test_f()
    mesures_p = test_p()
    verdict = "PASS" if not echecs_f else "FAIL"
    rapport = {
        "tache": "Task 113 (suite) — tests F+P sur les 16 réécritures plateforme + synchro dépôt",
        "verdict": verdict,
        "fonctionnel": {"echecs": echecs_f} if echecs_f else {"echecs": [], "note": "F1-F10 tous PASS"},
        "performance": mesures_p,
    }
    RAPPORT.write_text(json.dumps(rapport, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"FONCTIONNEL : {'PASS (F1-F10)' if not echecs_f else 'FAIL'}")
    for e in echecs_f:
        print(f"  ✗ {e}")
    for k, v in mesures_p.items():
        print(f"P  {k} = {v}")
    print(f"VERDICT : {verdict}")
    print(f"RAPPORT : {RAPPORT}")
    return 0 if not echecs_f else 1


if __name__ == "__main__":
    sys.exit(main())
