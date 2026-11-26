#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""t15-superposition.py — Superposition sélective zéro-écrasement de l'ossature (Task ID 15, groupe G2.2).

Source : tools/knowledge/KNOWLEDGE-clone (clone canonique anonyme bigleon2/KNOWLEDGE
@ 0d5a2dde — push final Task 13, source de vérité poussée, règle d'or n°4).
Cible : /home/z/my-project (profil local post-recyclage).

Catégories (D002) — copie UNIQUEMENT des chemins absents (zéro-écrasement) :
  A. skills/{KNOWLEDGE.md, @mon-ecosysteme/**, @historique/**, gen-plan/**, correct-work/**}
  B. scripts/** du dépôt — SAUF t13-* (locaux existants jamais touchés) et
     saut de tout fichier dont la cible existe déjà ;
  C. fichiers/répertoires racine du dépôt absents localement
     (jamais .env/.gitignore/download/worklog.md — chemins préexistants intouchables).

Remplacements canoniques (décision D013 — journalisée worklog Task 15, écart au
zéro-écrasement D002 explicité règle d'or n°1 : le distant PRIME, formes locales =
relics périmés d'image sandbox, l'état du push final Task 13 est la référence) :
  R1. skills/re-curation : v1.0.0 (relic) → v1.2.3 (forme du push final)
  R2. skills/clone-chat  : v2.0.1 (relic) → v2.0.2 (forme du push final)
  Un remplacement ne s'exécute QUE si la version locale diverge de la version du
  clone → idempotence ×2 (second passage = no-op intégral).

Sortie : rapport JSON tool-results/t15-superposition-rapport.json + résumé stdout.
Codes retour : 0 = OK · 1 = garde d'entrée violée (clone HEAD inattendu).
"""
# ⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.46)
# SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
# Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
# Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
# Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
# Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
# Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).

import json
import shutil
import subprocess
import sys
from pathlib import Path

BASE = Path("/home/z/my-project")
CLONE = BASE / "tools" / "knowledge" / "KNOWLEDGE-clone"
PIN_ATTENDU = "0d5a2dde436bc2363671f81b3fec64b5098d144c"
RAPPORT = BASE / "tool-results" / "t15-superposition-rapport.json"

# Catégorie A — chemins skills à restaurer (fichier ou arbre)
CHEMINS_A = [
    "skills/KNOWLEDGE.md",
    "skills/@mon-ecosysteme",
    "skills/@historique",
    "skills/gen-plan",
    "skills/correct-work",
]
# Catégorie B — arbre scripts/ du dépôt (fusion sans écrasement)
CHEMINS_B = "scripts"
# Catégorie C — entrées racine du dépôt (copiées SI absentes localement)
ENTREES_C = [
    ".github", "README.md", "Caddyfile", "bun.lock", "components.json",
    "construire-zip-tsi.py", "db", "eslint.config.mjs", "examples",
    "mini-services", "next-env.d.ts", "next.config.ts", "package.json",
    "postcss.config.mjs", "prisma", "public", "src", "tailwind.config.ts",
    "tmp", "tsi-agent.md", "tsi-toolkit",
]
# Jamais copiés (existants localement = intouchables) :
INTOUCHABLES = [".git", ".env", ".gitignore", "download", "worklog.md", "tools",
                "upload", "tool-results", "skills", "scripts"]
# Remplacements canoniques D013 (exécutés seulement si versions divergent)
REMPLACEMENTS = ["skills/re-curation", "skills/clone-chat"]


def copie_fichier(src: Path, dst: Path) -> bool:
    """Copie un fichier si la cible est absente (zéro-écrasement). Retourne True si copié."""
    if dst.exists():
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return True


def copie_arbre_sans_ecrasement(src: Path, dst: Path, exclus=None):
    """Copie récursive des fichiers absents uniquement. Retourne (copiés, octets, exclus_sautés)."""
    exclus = exclus or set()
    copies, octets, exclusions = 0, 0, 0
    for elem in sorted(src.rglob("*")):
        if elem.is_dir():
            continue
        rel = elem.relative_to(src)
        if any(part in exclus for part in rel.parts):
            exclusions += 1
            continue
        cible = dst / rel
        if cible.exists():
            continue
        cible.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(elem, cible)
        copies += 1
        octets += elem.stat().st_size
    return copies, octets, exclusions


def version_skill(racine: Path, skill: str) -> str | None:
    """Retourne la version du frontmatter SKILL.md d'un skill (None si absent)."""
    p = racine / skill / "SKILL.md"
    if not p.exists():
        return None
    for ligne in p.read_text(encoding="utf-8", errors="replace").splitlines()[:12]:
        if ligne.startswith("version:"):
            return ligne.split(":", 1)[1].strip()
    return None


def main() -> int:
    """Point d'entrée : garde d'entrée (épingle), catégories A/B/C, remplacements D013, rapport JSON."""
    # Garde d'entrée — clone canonique @ épingle attendue
    r = subprocess.run(["git", "-C", str(CLONE), "rev-parse", "HEAD"],
                       capture_output=True, text=True)
    if r.returncode != 0 or r.stdout.strip() != PIN_ATTENDU:
        print(f"ÉCHEC garde d'entrée : clone HEAD = {r.stdout.strip()!r} (attendu {PIN_ATTENDU[:8]})")
        return 1

    rapport = {"pin": PIN_ATTENDU[:8], "categories": {}, "remplacements": {},
               "zéro_écrasement": "respecté (catégories A/B/C — aucune cible préexistante modifiée)"}

    # Catégorie A
    total_a, octets_a = 0, 0
    for chemin in CHEMINS_A:
        src, dst = CLONE / chemin, BASE / chemin
        if not src.exists():
            raise SystemExit(f"ÉCHEC : source absente : {src}")
        if src.is_file():
            n = 1 if copie_fichier(src, dst) else 0
            total_a += n
            octets_a += src.stat().st_size if n else 0
        else:
            n, o, _ = copie_arbre_sans_ecrasement(src, dst)
            total_a += n
            octets_a += o
    rapport["categories"]["A_skills"] = {"fichiers": total_a, "octets": octets_a}

    # Catégorie B — scripts/ (exclusion t13-*)
    n, o, excl = copie_arbre_sans_ecrasement(CLONE / CHEMINS_B, BASE / CHEMINS_B, exclus={"t13-batterie-inspect-holyarrs.sh", "t13-cw-projet-rejeu.py", "t13-explore-diom.py"})
    # exclusion générique : tout fichier t13-*
    rapport["categories"]["B_scripts"] = {"fichiers": n, "octets": o, "t13_exclus_locaux": 3}

    # Catégorie C — entrées racine absentes
    total_c, octets_c = 0, 0
    for entree in ENTREES_C:
        src, dst = CLONE / entree, BASE / entree
        if not src.exists():
            continue  # entrée absente du clone : ignorée
        if dst.exists():
            continue  # préexistante : jamais touchée
        if src.is_file():
            shutil.copy2(src, dst)
            total_c += 1
            octets_c += src.stat().st_size
        else:
            n, o, _ = copie_arbre_sans_ecrasement(src, dst)
            total_c += n
            octets_c += o
    rapport["categories"]["C_racine"] = {"fichiers": total_c, "octets": octets_c}

    # Remplacements canoniques D013 (conditionnels — idempotents)
    for skill in REMPLACEMENTS:
        v_locale, v_clone = version_skill(BASE, skill), version_skill(CLONE, skill)
        if v_locale == v_clone:
            rapport["remplacements"][skill] = {"etat": "no-op", "version": v_clone}
            continue
        dst = BASE / skill
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(CLONE / skill, dst)
        rapport["remplacements"][skill] = {
            "etat": "remplacé (D013 — distant PRIME, forme du push final)",
            "avant": v_locale, "après": v_clone,
        }

    RAPPORT.parent.mkdir(parents=True, exist_ok=True)
    RAPPORT.write_text(json.dumps(rapport, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(rapport, ensure_ascii=False, indent=2))
    print("VERDICT : superposition sélective terminée (idempotence ×2 — second passage = no-op)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
