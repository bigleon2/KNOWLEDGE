#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.7)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

# -*- coding: utf-8 -*-
"""
Arbitre Phase A (plan Task 2 audit, E9) — @historique byte-identité + py_compile.

Vérifications exécutables (answer key D001, plan §E9) :
  1. @historique byte-identité : chaque fichier listé dans l'index §5 du README
     de @historique/ (sceau SHA-256) est recalculé et comparé au sceau —
     la table doit être complète et les fichiers conformes (garde R4 git mv).
     Contrôle documentaire : cohérence du compte annoncé en tête d'index
     (« 21 PMs ») vs nombre réel de lignes de table.
  2. py_compile : tous les scripts .py du dépôt local (scripts/ + skills/*/scripts/)
     doivent compiler — aucun échec toléré.

Usage : python3 scripts/audit-phaseA-historique.py
Sortie : scripts/audit-phaseA-report.json — exit 0 si et seulement si
         byte-identité intégrale ET 0 échec de compilation.
Idempotent : rejeu ×2 sans effet (aucune écriture d'état, rapport déterministe).
"""

import hashlib
import json
import py_compile
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
HIST = BASE / "skills" / "@historique"
README = HIST / "README.md"
RAPPORT = BASE / "scripts" / "audit-phaseA-report.json"


def sha256(chemin):
    """SHA-256 hex digest d'un fichier."""
    return hashlib.sha256(chemin.read_bytes()).hexdigest()


def extraire_index():
    """Parse la table §5 du README @historique → [(fichier, sceau), ...].

    KO-L003 (invariants dynamisés — recalibrage audit Phase B 2026-10-25) : la
    famille est matchée génériquement (n'importe quel dossier sous prompts-maitres/),
    jamais figée — la liste des familles archivées évolue avec le corpus (4e famille
    refactor-guard, 5e entrée clone-chat ajoutée Task 12 : le parseur figé
    gen-plan|correct-work la comptait pas).
    """
    texte = README.read_text(encoding="utf-8")
    section = texte.split("## 5.")[1] if "## 5." in texte else ""
    lignes = re.findall(r"^\|\s*([\w-]+)/(\S+?\.md)\s*\|\s*([0-9a-f]{64})\s*\|",
                        section, re.MULTILINE)
    return [(f"{fam}/{nom}", sceau) for fam, nom, sceau in lignes]


def verifier_historique():
    """Byte-identité @historique vs index §5 + couverture croisée index ↔ disque."""
    entrees = extraire_index()
    resultats = {"attendues": len(entrees), "conformes": 0, "ecarts": []}
    for relatif, sceau in entrees:
        chemin = HIST / "prompts-maitres" / Path(relatif)
        if not chemin.is_file():
            resultats["ecarts"].append(f"ABSENT : {relatif}")
            continue
        calcule = sha256(chemin)
        if calcule == sceau:
            resultats["conformes"] += 1
        else:
            resultats["ecarts"].append(
                f"SHA DIVERGENT : {relatif} (index {sceau[:12]}… ≠ réel {calcule[:12]}…)")
    # Couverture croisée (audit Phase B) : fichiers réels vs entrées index — les deux sens
    reels = {str(p.relative_to(HIST / "prompts-maitres"))
             for p in (HIST / "prompts-maitres").glob("*/*.md")}
    indexes = {relatif for relatif, _ in entrees}
    for absent in sorted(reels - indexes):
        resultats["ecarts"].append(f"NON INDEXÉ (présent sur disque, absent de l'index §5) : {absent}")
    for fantome in sorted(indexes - reels):
        resultats["ecarts"].append(f"FANTÔME (indexé §5, absent du disque) : {fantome}")
    resultats["fichiers_disque"] = len(reels)
    # Contrôle documentaire : compte annoncé en tête d'index vs lignes réelles
    texte = README.read_text(encoding="utf-8")
    m = re.search(r"## 5\.[^\n]*\((\d+)\s*PMs", texte)
    resultats["compte_annonce"] = int(m.group(1)) if m else None
    resultats["compte_reel"] = len(entrees)
    return resultats


def compiler_scripts():
    """py_compile tous les .py de scripts/ et skills/*/scripts/."""
    cibles = sorted((BASE / "scripts").glob("*.py"))
    cibles += sorted(BASE.glob("skills/*/scripts/*.py"))
    echecs = []
    for chemin in cibles:
        try:
            py_compile.compile(str(chemin), doraise=True, cfile="/dev/null" if False else None)
        except py_compile.PyCompileError as exc:
            echecs.append(f"{chemin.relative_to(BASE)} : {exc}")
        except Exception as exc:  # noqa: BLE001 — toute erreur de compilation est un écart
            echecs.append(f"{chemin.relative_to(BASE)} : {exc}")
    return {"tentatives": len(cibles), "echecs": echecs}


def main():
    print("=== ARBITRE PHASE A — @historique byte-identité + py_compile ===")
    hist = verifier_historique()
    print(f"[@historique] index §5 : {hist['conformes']}/{hist['attendues']} conformes ; "
          f"disque {hist.get('fichiers_disque', 0)} fichiers ; "
          f"compte annoncé {hist['compte_annonce']} vs réel {hist['compte_reel']}")
    for ecart in hist["ecarts"]:
        print(f"  [ÉCART] {ecart}")

    comp = compiler_scripts()
    print(f"[py_compile] {comp['tentatives'] - len(comp['echecs'])}/{comp['tentatives']} "
          f"compilés, {len(comp['echecs'])} échec(s)")
    for echec in comp["echecs"]:
        print(f"  [ÉCART] {echec}")

    byte_ok = not hist["ecarts"] and hist["conformes"] == hist["attendues"]
    compile_ok = not comp["echecs"]
    drift_compte = (hist["compte_annonce"] != hist["compte_reel"])
    verdict = "ALL PASS" if (byte_ok and compile_ok and not drift_compte) else (
        "PASS AVEC RÉSERVES" if (byte_ok and compile_ok) else "FAIL")

    print(f"VERDICT : {verdict}"
          + (" (réserves : drift documentaire index §5)" if drift_compte and byte_ok and compile_ok else ""))

    rapport = {
        "historique": hist,
        "compilation": {"tentatives": comp["tentatives"], "echecs": comp["echecs"]},
        "verdict": verdict,
        "drift_documentaire_index": drift_compte,
    }
    RAPPORT.write_text(json.dumps(rapport, ensure_ascii=False, indent=2, sort_keys=True),
                        encoding="utf-8")
    print(f"Rapport JSON : scripts/{RAPPORT.name}")
    sys.exit(0 if verdict != "FAIL" else 1)


if __name__ == "__main__":
    main()
