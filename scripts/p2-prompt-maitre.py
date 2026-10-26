#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.7)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (R4)

p2-prompt-maitre.py — Phase P2 (directive 10 tâches, tâche 2) : génération des
dossiers « Prompt Maitre » par skill — prompts AUTONOMES à usage HORS écosystème,
sauvegardés UNIQUEMENT dans « skills/PM skills/ » (directive propriétaire).

Garanties :
  D010 — chaque dossier porte le marqueur d'exclusion anti-lecture orchestration ;
         AUCUNE entrée au registre KB ; ne casse AUCUN arbitre (aucun fichier
         SKILL.md généré — les arbitres scannent skills/*/SKILL.md uniquement).
  IDEMPOTENT — un dossier PM est régénéré seulement si le SKILL.md source a
         changé (SHA-256) ; re-jeu à l'identique = 0 écriture.
  AUTONOME — le prompt intègre : en-tête marqueur, guide d'usage, SKILL.md
         source intégral (francisé) avec variables écosystème résolues, liste
         des ressources locales (references/ copiées dans le dossier PM).

Usage : python3 scripts/p2-prompt-maitre.py [--racine DIR] [--seulement SK1 SK2]
Codes retour : 0 OK · 1 échec · 2 usage invalide.
"""
import hashlib
import json
import re
import shutil
import sys
from datetime import date
from pathlib import Path

BASE = Path("/home/z/my-project")
WORKTREE = BASE / ".staging" / "KNOWLEDGE-publish"
PM_ROOT = WORKTREE / "skills" / "PM skills"
ETAT = BASE / "scripts" / "p2-pm-etat.json"
AUJOURD = date.today().isoformat()

MARQUEUR = (
    "> ⚠️ **MARQUEUR D'EXCLUSION (garde D010)** — CE DOSSIER N'EST PAS LU PAR "
    "L'ORCHESTRATION. Les dossiers « Prompt Maitre » sont des prompts autonomes "
    "à usage HORS écosystème : ils ne sont pas indexés au registre KB, ne sont "
    "mobilisés par aucun arbitre, et ne remplacent jamais la forme installée "
    "`skills/<skill>/` (source de vérité)."
)

VARS_ECO = {
    "{{SKILLS_ROOT}}": "`skills/`",
    "{{KB_PATH}}": "`skills/KNOWLEDGE.md`",
    "{{KB_ENABLED}}": "`true`",
    "{{PROFILE_DEFAULT}}": "`NORMAL`",
}

GARDE_ANTI_LECTURE = re.compile(r"^(?:#\s*)?SKILL\.md\s*$|read SKILL|lire SKILL\.md")


def sh256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def parse_frontmatter(t: str) -> dict:
    fm = {}
    if t.startswith("---\n"):
        fin = t.find("\n---", 4)
        if fin > 0:
            for ligne in t[4:fin].splitlines():
                m = re.match(r"^\s*([a-zA-Z_-]+)\s*:\s*(.*)$", ligne)  # indentation acceptée (version imbriquée)
                if m:
                    fm.setdefault(m.group(1), m.group(2).strip().strip('"'))
    return fm


def resout_vars(texte: str) -> str:
    for k, v in VARS_ECO.items():
        texte = texte.replace(k, v)
    return texte


def genere_pm(skill_dir: Path, rel_skill: str) -> dict:
    src = skill_dir / "SKILL.md"
    t_src = src.read_text(encoding="utf-8", errors="replace")
    fm = parse_frontmatter(t_src)
    version = fm.get("version") or None
    if version and not re.match(r"^\d", version):
        version = None  # valeur non numérique (ex : phrase) — pas une version
    nom = fm.get("name", skill_dir.name)
    sha_src = sh256(src)
    pm_dir = PM_ROOT / skill_dir.name
    pm_file = pm_dir / f"PROMPT-MAITRE-{skill_dir.name}.md"
    resultat = {"skill": skill_dir.name, "version": version or "non déclarée", "sha_source": sha_src}

    # Idempotence : no-op si le PM existe ET porte le même SHA source scellé
    if pm_file.exists():
        try:
            if json.loads((pm_dir / ".source.json").read_text(encoding="utf-8")).get("sha_source") == sha_src:
                resultat["statut"] = "SKIP-a-jour"
                return resultat
        except Exception:
            pass

    pm_dir.mkdir(parents=True, exist_ok=True)

    # Corps du prompt = SKILL.md intégral (francisé), variables résolues
    corps = resout_vars(t_src)

    # Ressources locales : references/ copiées (autonomie réelle hors écosystème)
    refs_copiees = []
    src_refs = skill_dir / "references"
    if src_refs.is_dir():
        dst_refs = pm_dir / "references"
        if dst_refs.exists():
            shutil.rmtree(dst_refs)
        shutil.copytree(src_refs, dst_refs)
        refs_copiees = sorted(p.relative_to(pm_dir).as_posix() for p in dst_refs.rglob("*") if p.is_file())

    parties = [
        "---",
        f"nom: {nom}",
    ]
    if version:
        parties.append(f"version: {version}")
    parties += [
        f"source: skills/{rel_skill}/SKILL.md",
        f"sha256_source: {sha_src[:12]}",
        f"genere: {AUJOURD} (phase P2 — directive 10 tâches, tâche 2)",
        "usage: AUTONOME hors écosystème (dossier « Prompt Maitre » — non lu par l'orchestration)",
        "---",
        "",
        MARQUEUR,
        "",
        f"# Prompt Maître autonome — {nom}" + (f" (v{version})" if version else " (version non déclarée)"),
        "",
        "## Comment utiliser ce prompt (hors écosystème)",
        "",
        "Ce document encapsule la compétence sous forme autonome : copiez-le intégralement",
        "dans un assistant IA (ou ouvrez-le en référence directe) — aucune installation,",
        "aucun registre, aucune dépendance à l'écosystème Knowledge d'origine n'est requise.",
        "Les variables de l'écosystème d'origine ont été résolues en valeurs littérales ;",
        "si des ressources `references/` accompagnent ce dossier, elles sont jointes au même",
        "emplacement et le prompt y renvoie par leur chemin relatif. La version d'origine",
        "(source de vérité) vit dans `skills/" + skill_dir.name + "/SKILL.md` du dépôt KNOWLEDGE.",
        "",
        "---",
        "",
        "## Le prompt",
        "",
        corps,
        "",
        "---",
        "",
        "## Ressources locales du dossier",
        "",
    ]
    if refs_copiees:
        parties.append("Ressources jointes (usage autonome — lire au besoin pendant l'application du prompt) :")
        parties += [f"- `{r}`" for r in refs_copiees]
    else:
        parties.append("Aucune ressource annexe — ce prompt est auto-suffisant.")
    parties.append("")
    pm_file.write_text("\n".join(parties), encoding="utf-8")
    (pm_dir / ".source.json").write_text(
        json.dumps(resultat, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    resultat["statut"] = "GENERE"
    resultat["references"] = len(refs_copiees)
    return resultat


def main():
    args = sys.argv[1:]
    racine = WORKTREE
    if "--racine" in args:
        i = args.index("--racine")
        racine = Path(args[i + 1])
        del args[i : i + 2]
    seulement = None
    if "--seulement" in args:
        i = args.index("--seulement")
        seulement = set(args[i + 1:])
        del args[i : i + 2]
    pm_root = racine / "skills" / "PM skills"

    # Mode custom racine (tests) : recalibrer les chemins
    global PM_ROOT
    PM_ROOT = pm_root

    skills = sorted(d for d in (racine / "skills").iterdir() if d.is_dir() and (d / "SKILL.md").is_file())
    if seulement:
        skills = [d for d in skills if d.name in seulement]
    journal = json.loads(ETAT.read_text(encoding="utf-8")) if ETAT.exists() else {}
    generes, skips, echecs = 0, 0, 0
    for d in skills:
        try:
            r = genere_pm(d, d.name)
            journal[d.name] = r
            if r["statut"] == "GENERE":
                generes += 1
                print(f"  [GENERE] {d.name} v{r['version']} (refs: {r.get('references', 0)})")
            else:
                skips += 1
        except Exception as exc:
            echecs += 1
            journal[d.name] = {"statut": "ECHEC", "erreur": str(exc)[:300]}
            print(f"  [ECHEC] {d.name} : {exc}")
    # README racine : marqueur global + index
    entrees = []
    for d in skills:
        v = journal.get(d.name, {}).get("version", "?")
        entrees.append(f"| `{d.name}` | v{v} | `{d.name}/PROMPT-MAITRE-{d.name}.md` |")
    readme = [
        "# « PM skills » — Prompts Maîtres autonomes (usage hors écosystème)",
        "",
        MARQUEUR,
        "",
        "Chaque sous-dossier encapsule une skill sous forme de prompt autonome,",
        "copiable hors écosystème. Ces dossiers ne sont PAS la forme installée :",
        "la source de vérité reste `skills/<skill>/SKILL.md` (règle zéro, registre KB).",
        "",
        f"Généré le {AUJOURD} — phase P2 (directive 10 tâches, tâche 2). Idempotent :",
        "un dossier n'est réécrit que si sa source a changé (SHA-256 scellé par dossier).",
        "",
        "## Index",
        "",
        "| Skill | Version | Prompt |",
        "|-------|---------|--------|",
    ] + entrees + [""]
    (pm_root / "README.md").write_text("\n".join(readme), encoding="utf-8")
    ETAT.write_text(json.dumps(journal, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"bilan : {generes} générés · {skips} à jour · {echecs} échecs — {pm_root}")
    return 1 if echecs else 0


if __name__ == "__main__":
    sys.exit(main())
