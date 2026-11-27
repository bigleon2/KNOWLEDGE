#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sweep-entetes-shared.py — Balayage des en-têtes §0 « Contexte Système (SHARED vX) ».

PM-INSTALL §3.2-c v1.10.7 (correctif C2 — Task 12, session web-220878ed,
directive trace 1a21e208f489f7f5) : le bootstrap aligne MÉCANIQUEMENT les
en-têtes §0 des SKILL.md installés sur la version du PM SHARED vivant
(dérivation KO-L003 — même source que l'arbitre test-coherence-interactions.py
§11b : l'en-tête « > **Version** : X.Y.Z » du corpus). Extinction de la classe
d'échec récidive « en-têtes §0 STALE » : la plateforme réinjecte ses skills
natifs (copies périmées) au démarrage de session — Tasks 11-12 : asr, llm,
tts, vlm (v1.7.44), mise-en-page (v1.7.40) ≠ SHARED v1.7.46 → FAIL
certification 59/60, boucle E12-E13 manuelle à chaque session.

Usage :
  sweep-entetes-shared.py [--dry-run] [--json] [--root DIR]
  sweep-entetes-shared.py --selftest

Codes retour : 0 = OK (0 ou N alignements) · 1 = PM SHARED introuvable ou
version non dérivable (KO-L003 : jamais de valeur figée en repli).
Idempotent ×2 : second passage = 0 alignement (byte-stable, R6).
"""
# ⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.46)
# SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
# Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
# Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
# Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan).
# Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0,
# ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).

import argparse
import json
import re
import sys
import tempfile
from pathlib import Path

ROOT_DEFAUT = Path(__file__).resolve().parents[1]
PM_SHARED = Path("skills") / "@mon-ecosysteme" / "PROMPT-MAITRE-SHARED.md"
RE_VERSION_SHARED = re.compile(r"\*\*Version\*\*\s*:\s*([0-9]+\.[0-9]+\.[0-9]+)")
RE_LIGNE_ENTETE = re.compile(r"^(?P<avant>##\s+§0\s+—\s+Contexte Système\s+\(SHARED\s+v)"
                              r"(?P<version>[0-9]+\.[0-9]+\.[0-9]+)"
                              r"(?P<apres>\)\s*)$")


def version_shared(root: Path) -> str:
    """Dérive la version courante du PM SHARED vivant (KO-L003 — jamais figée)."""
    chemin = root / PM_SHARED
    if not chemin.is_file():
        raise FileNotFoundError(f"PM SHARED introuvable : {chemin}")
    texte = chemin.read_text(encoding="utf-8", errors="replace")
    m = RE_VERSION_SHARED.search(texte)
    if not m:
        raise ValueError(f"Version non dérivable depuis {chemin} (pattern « **Version** : X.Y.Z » absent)")
    return m.group(1)


def balayer(root: Path, dry_run: bool = False):
    """Balaye les SKILL.md des formes installées (dossiers non-@) et aligne les
    en-têtes §0 sur la version SHARED courante. Retourne la liste des actions."""
    cible = version_shared(root)
    actions = []
    racine_skills = root / "skills"
    if not racine_skills.is_dir():
        raise FileNotFoundError(f"Racine skills/ introuvable : {racine_skills}")
    for dossier in sorted(racine_skills.iterdir()):
        if not dossier.is_dir() or dossier.name.startswith("@"):
            continue  # dossiers @ = non-skills (corpus, archive) — jamais balayés
        skill_md = dossier / "SKILL.md"
        if not skill_md.is_file():
            continue
        lignes = skill_md.read_text(encoding="utf-8", errors="replace").splitlines(keepends=True)
        modifie = False
        for i, ligne in enumerate(lignes):
            m = RE_LIGNE_ENTETE.match(ligne.rstrip("\r\n"))
            if m and m.group("version") != cible:
                nouvelle = (m.group("avant") + cible + m.group("apres") + "\n")
                if not dry_run:
                    lignes[i] = nouvelle
                    skill_md.write_text("".join(lignes), encoding="utf-8")
                actions.append({"fichier": str(skill_md), "ligne": i + 1,
                                "avant": m.group("version"), "apres": cible})
                modifie = True
                break  # un seul en-tête §0 par SKILL.md (règle zéro)
        _ = modifie  # lisibilité du trace
    return {"version_shared_cible": cible, "nb_alignes": len(actions), "actions": actions,
            "dry_run": dry_run}


def selftest() -> int:
    """Tests internes sur fixture temporaire — AUCUNE mutation du profil réel."""
    checks = []
    with tempfile.TemporaryDirectory() as tmp:
        racine = Path(tmp)
        corpus = racine / "skills" / "@mon-ecosysteme"
        corpus.mkdir(parents=True)
        (corpus / "PROMPT-MAITRE-SHARED.md").write_text(
            "# PROMPT MAÎTRE SHARED\n\n> **Version** : 9.9.9\n> **Révision** : test\n",
            encoding="utf-8")
        stale = racine / "skills" / "skill-a"
        stale.mkdir()
        (stale / "SKILL.md").write_text(
            "---\nname: skill-a\nversion: 1.0.0\n---\n\n## §0 — Contexte Système (SHARED v1.0.0)\n\ncorps\n",
            encoding="utf-8")
        propre = racine / "skills" / "skill-b"
        propre.mkdir()
        (propre / "SKILL.md").write_text(
            "---\nname: skill-b\nversion: 1.0.0\n---\n\n## §0 — Contexte Système (SHARED v9.9.9)\n\ncorps\n",
            encoding="utf-8")
        hors = racine / "skills" / "@historique"
        hors.mkdir()
        (hors / "SKILL.md").write_text(
            "## §0 — Contexte Système (SHARED v1.0.0)\n", encoding="utf-8")

        r1 = balayer(racine, dry_run=False)
        checks.append(("alignement : 1 en-tête corrigé (stale→9.9.9), 0 ailleurs",
                       r1["nb_alignes"] == 1
                       and r1["actions"][0]["avant"] == "1.0.0"
                       and r1["actions"][0]["apres"] == "9.9.9"))
        r2 = balayer(racine, dry_run=False)
        checks.append(("idempotence ×2 : second passage 0 alignement",
                       r2["nb_alignes"] == 0))
        apres = (stale / "SKILL.md").read_text(encoding="utf-8")
        checks.append(("substitution exacte : en-tête à 9.9.9, corps intact",
                       "## §0 — Contexte Système (SHARED v9.9.9)" in apres
                       and "corps\n" in apres and "v1.0.0" not in apres.split("---")[-1].split("\n")[2]))
        checks.append(("dossiers @ exclus : @historique/SKILL.md non touché",
                       "(SHARED v1.0.0)" in (hors / "SKILL.md").read_text(encoding="utf-8")))
        r3 = balayer(racine, dry_run=True)
        checks.append(("dry-run : 0 action (déjà aligné), aucun effet",
                       r3["nb_alignes"] == 0 and r3["dry_run"] is True))
    (corpus_manquant := Path(tempfile.mkdtemp()) / "vide")
    try:
        version_shared(corpus_manquant.parent)
        checks.append(("garde : PM SHARED absent → exception (rc 1 attendu)", False))
    except (FileNotFoundError, ValueError):
        checks.append(("garde : PM SHARED absent → exception (rc 1 attendu)", True))
    ok = all(o for _, o in checks)
    for nom, ok_c in checks:
        print(f"  [{'PASS' if ok_c else 'FAIL'}] {nom}")
    print(f"SELFTEST {'PASS' if ok else 'FAIL'} ({sum(1 for _, o in checks if o)}/{len(checks)})")
    return 0 if ok else 1


def main() -> int:
    parse = argparse.ArgumentParser(description="Balayage des en-têtes §0 vers le SHARED vivant")
    parse.add_argument("--dry-run", action="store_true", help="lecture seule : aucune écriture")
    parse.add_argument("--json", action="store_true", help="sortie JSON machine")
    parse.add_argument("--root", default=str(ROOT_DEFAUT),
                       help="racine du profil (défaut : parent du dossier scripts/)")
    parse.add_argument("--selftest", action="store_true", help="tests internes (aucune mutation)")
    args = parse.parse_args()
    if args.selftest:
        return selftest()
    try:
        rapport = balayer(Path(args.root), dry_run=args.dry_run)
    except (FileNotFoundError, ValueError) as exc:
        if args.json:
            print(json.dumps({"erreur": str(exc)}, ensure_ascii=False))
        else:
            print(f"ERREUR : {exc}")
        return 1
    if args.json:
        print(json.dumps(rapport, ensure_ascii=False, indent=2))
    else:
        print(f"SWEEP §0 — SHARED cible v{rapport['version_shared_cible']} : "
              f"{rapport['nb_alignes']} en-tête(s) aligné(s)"
              f"{' (dry-run)' if args.dry_run else ''}")
        for a in rapport["actions"]:
            print(f"  {a['fichier']}:{a['ligne']} v{a['avant']} → v{a['apres']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
