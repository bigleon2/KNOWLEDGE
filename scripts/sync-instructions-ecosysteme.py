#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.34)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).
sync-instructions-ecosysteme.py — Active le PM SHARED + les disciplines + la découverte de l'écosystème dans le contexte agent.

Directive propriétaire 2026-11-01 (traces 1a1932155da4969d + 1a1932757ab10e51) :
- toute génération/extension de plan d'actions = skill gen-plan uniquement (garde absolue) ;
- la réinstallation (ensure-installed.py) doit prendre en compte le PM SHARED et permettre
  l'usage des disciplines + la recherche/usage des skills, agents et scripts selon la situation.

Matérialisation : (re)génère le fichier d'instructions projet CLAUDE.md sur l'ESPACE DE
TRAVAIL (le répertoire qui contient worklog.md ; à défaut, la racine écosystème). Source de
vérité : le disque (R-F3) — version PM SHARED lue dans PROMPT-MAITRE-SHARED.md, version
gen-plan lue dans skills/gen-plan/SKILL.md, effectifs comptés sur l'arbre.

Conventions script-creator : Python stdlib (N3), idempotent ×2 (f(f(x))=f(x) byte-identique),
--selftest, aucune dépendance réseau.

Usage :
    sync-instructions-ecosysteme.py            # synchronise (ou constate A-JOUR)
    sync-instructions-ecosysteme.py --json     # verdict machine
    sync-instructions-ecosysteme.py --selftest
"""
from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # KNOWLEDGE-repo/
MP = Path(os.environ.get("ECO_PROFILE_ROOT", str(ROOT)))
TZ = timezone(timedelta(hours=8))

DISCIPLINES = [
    "context-engineering", "memory-engineering", "graph-engineering",
    "fleet-engineering", "harness-engineering", "loop-engineering",
    "spec-driven-development", "refactoring-engineering", "refactoring-test",
    "refactor-guard", "prompt-engineering", "agent-prompt-engineering",
    "resource-monitor", "knowledge-observer", "inter-scripts",
    "script-creator", "script-reviewer", "correct-work", "correct-py",
    "skills-inventory", "skill-finder-cn", "audit-provenance",
]


def espace_travail() -> Path:
    """L'espace de travail = répertoire dont le worklog.md est le PLUS RÉCENT (R-F3)."""
    candidats = [c for c in (MP.parent, MP) if (c / "worklog.md").exists()]
    if candidats:
        return max(candidats, key=lambda c: (c / "worklog.md").stat().st_mtime)
    return MP


def lire_version_pm(shared: Path) -> str:
    if not shared.exists():
        return "ABSENT"
    m = re.search(r"\*\*Version\*\*\s*:\s*(\d+\.\d+\.\d+)", shared.read_text(encoding="utf-8", errors="replace")[:4000])
    return m.group(1) if m else "INCONNUE"


def lire_version_skill(chemin: Path) -> str:
    if not chemin.exists():
        return "ABSENT"
    m = re.search(r"^version:\s*(\d+\.\d+\.\d+)", chemin.read_text(encoding="utf-8", errors="replace")[:2000], re.M)
    return m.group(1) if m else "INCONNUE"


def inventaire() -> dict:
    skills = MP / "skills"
    n_skills = len([d for d in skills.iterdir() if d.is_dir() and (d / "SKILL.md").exists()]) if skills.exists() else 0
    disciplines = [d for d in DISCIPLINES if (skills / d / "SKILL.md").exists()]
    n_scripts = len(list((ROOT / "scripts").glob("*.py"))) if (ROOT / "scripts").exists() else 0
    n_agents = len(list(skills.glob("*/agents/*.agent"))) + len(list(skills.glob("*.agent"))) + len(list(skills.glob("*/*.agent")))
    kb = skills / "KNOWLEDGE.md"
    kb_entrees = len(re.findall(r"^## [a-z0-9-]+ v\d+\.\d+\.\d+$", kb.read_text(encoding="utf-8", errors="replace"), re.M)) if kb.exists() else 0
    return {
        "pm_shared": str((MP / "skills/@mon-ecosysteme/PROMPT-MAITRE-SHARED.md").relative_to(MP)),
        "pm_version": lire_version_pm(MP / "skills/@mon-ecosysteme/PROMPT-MAITRE-SHARED.md"),
        "genplan_version": lire_version_skill(skills / "gen-plan/SKILL.md"),
        "skills": n_skills, "disciplines": disciplines, "scripts_eco": n_scripts,
        "agents": n_agents, "kb_entrees": kb_entrees,
    }


def generer(inv: dict, ts: str) -> str:
    disc = "\n".join(f"- `{d}`" for d in inv["disciplines"])
    return f"""# Règles projet — écosystème Knowledge

> Généré mécaniquement par `sync-instructions-ecosysteme.py` — NE PAS ÉDITER À LA MAIN (régénéré idempotent byte-stable ; source de vérité : le disque, R-F3).
> Réinstallation écosystème : `python3 scripts/auto-install-ecosysteme.py` (self-healing — contrôle via copie dépôt → pipeline canonique si non-INSTALLE ; rc≠0 = arrêt explicite) PUIS `python3 scripts/sync-instructions-ecosysteme.py`.

## Règle 1 — Référentiel PM SHARED (fait foi — s'applique à toute session)

Le référentiel de gestion de projet est **PM SHARED v{inv['pm_version']}** — fichier `skills/@mon-ecosysteme/PROMPT-MAITRE-SHARED.md` (dans l'arbre écosystème). Le LIRE en début de session si le contexte est perdu ou compressé. Règles vitales : R-F1..R-F4 — **R-F2 : vérification mécanique > confiance** ; **R-F3 : le filesystem fait foi** (état dérivé du disque, jamais de la mémoire de session) ; disciplines SHARED §7 ; routage §1.16 (local → ClawHub → web) ; règle d'or n°3 (E13 — extension de plan, jamais réécriture destructrice R2).

## Règle 2 — Routage des plans d'actions (GARDE ABSOLUE — 100 % des situations)

Toute génération, mise à jour, extension ou reprise d'un plan d'actions se fait UNIQUEMENT via le skill **gen-plan v{inv['genplan_version']}** :

1. **Lire d'abord** `skills/gen-plan/SKILL.md` avant toute écriture de plan.
2. **Protocole obligatoire** : hook E1-RES (lecture worklog + plan en vol + `ensure-installed.py --check`) → plan écrit dans `download/` avec answer key YAML (`decisions:` avec `criterion` + `verification` mécaniques) → verdict E8 par l'arbitre `python3 scripts/check_plan_protocol.py --plan <plan.md> --worklog worklog.md` (verdict + « Horodatage plan » COUPLÉS) → worklog R5 avec marqueur `PLAN-AFFICHE` → bloc récapitulatif affiché au chat.
3. **Toute demande utilisateur pendant un plan en vol** (compression de contexte, coupure, erreur plateforme, nouvelle directive) = extension E13 (règle d'or n°3) : directive verbatim consignée + groupes/decisions ajoutés + re-validation E8. Extension, jamais réécriture (R2).
4. **INTERDIT** de produire un fichier `download/plan-*.md` HORS de ce protocole — y compris après compression de contexte ou coupure. Dans ces situations : reprendre par le disque (worklog + plan + arbitre), jamais de mémoire de session.
5. **Vérification mécanique en ouverture de session** : `python3 scripts/garde-plan-genplan.py` — verdict PASS/FAIL ; FAIL = plan hors protocole détecté → le replacer dans le protocole gen-plan AVANT toute autre action.

## Règle 3 — Utiliser l'écosystème selon la situation (disciplines + découverte)

- **Chercher un skill** : registre KB `skills/KNOWLEDGE.md` ({inv['kb_entrees']} entrées — grep d'abord) ; inventaire complet : skill `skills-inventory` ; recherche externe : skill `skill-finder-cn` (ClawHub) ; sonde web : recherche GitHub/PyPI avec audit-provenance avant adoption (licence, provenance).
- **Chercher un agent** : fichiers `*.agent` sous `skills/` ({inv['agents']} référencés) — format et création : skill `agent-creator`.
- **Chercher un script d'écosystème** : `{inv['scripts_eco']} scripts Python` dans `scripts/` (arbitres, garde-fous, collecteurs — stdlib, idempotents) ; interconnexion multi-langages : skill `inter-scripts`.
- **Disciplines à mobiliser selon la situation** ({len(inv['disciplines'])} détectées) :
{disc}
- **Règle de routage** : mobiliser les skills/disciplines de l'écosystème AVANT d'improviser ; toute adoption externe passe par audit-provenance ; toute création par script-creator (stdlib, idempotent ×2, selftest) ; toute certification par correct-work.

## Règle 4 — Ouverture de session (chaîne mécanique, dans l'ordre)

1. `python3 scripts/auto-install-ecosysteme.py` (self-healing : contrôle via copie dépôt, réinstallation pipeline canonique si non-INSTALLE ; rc≠0 = arrêt explicite règle d'or n°1 — options `--with-toolchain`/`--with-argos` pour la toolchain pip, rapport seul par défaut ; si `scripts/` hôte est absent : `python3 KNOWLEDGE-repo/scripts/auto-install-ecosysteme.py`) ;
2. `python3 scripts/sync-instructions-ecosysteme.py` (maintient CE fichier — PM SHARED actif) ;
3. `python3 scripts/garde-plan-genplan.py` (plans hors protocole ?) ;
4. lecture `worklog.md` (dernière Task) + plan en vol le plus récent de `download/` — reprise par le disque (R-F3), hook E1-RES.
"""


def main() -> int:
    if "--selftest" in sys.argv:
        echecs = []
        stub = Path("/tmp/selftest-pm-stub.md")
        stub.write_text("> **Version** : 9.9.9\n", encoding="utf-8")
        if lire_version_pm(stub) != "9.9.9":
            echecs.append("lire-version")
        inv = inventaire()
        if inv["pm_version"] in ("ABSENT", "INCONNUE"):
            echecs.append("pm-version-ecosysteme")
        if inv["genplan_version"] in ("ABSENT", "INCONNUE"):
            echecs.append("genplan-version")
        if not inv["disciplines"]:
            echecs.append("disciplines-vide")
        essai = generer(inv, "TS-TEST")
        for marqueur in ("GARDE ABSOLUE", "PROMPT-MAITRE-SHARED.md", "disciplines", "skills-inventory", "garde-plan-genplan"):
            if marqueur not in essai:
                echecs.append("marqueur-manquant:" + marqueur)
        # idempotence : deux générations consécutives = byte-identiques
        if essai != generer(inv, "TS-TEST"):
            echecs.append("non-idempotent")
        print("SELFTEST FAIL : " + str(echecs) if echecs else "SELFTEST PASS (5/5 — version PM, version gen-plan, disciplines, marqueurs, idempotence)")
        return 1 if echecs else 0

    inv = inventaire()
    cible = espace_travail() / "CLAUDE.md"
    ts = datetime.now(TZ).strftime("%Y-%m-%dT%H:%M:%S+08:00")
    contenu = generer(inv, ts)
    verdict = "A-JOUR" if cible.exists() and cible.read_text(encoding="utf-8") == contenu else "SYNCHRONISE"
    if verdict == "SYNCHRONISE":
        cible.write_text(contenu, encoding="utf-8")
    rapport = {"verdict": verdict, "cible": str(cible), "pm_shared": inv["pm_version"],
               "gen_plan": inv["genplan_version"], "skills": inv["skills"],
               "disciplines_actives": len(inv["disciplines"]), "scripts_eco": inv["scripts_eco"]}
    print(json.dumps(rapport, ensure_ascii=False) if "--json" in sys.argv else
          f"  {verdict} : {cible} (PM SHARED v{inv['pm_version']}, gen-plan v{inv['genplan_version']}, {inv['skills']} skills, {len(inv['disciplines'])} disciplines, {inv['scripts_eco']} scripts)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
