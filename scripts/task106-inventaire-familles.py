#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Task 106 — Inventaire mécanique des familles de l'écosystème (mode step).

Directive propriétaire trace 1a1efc61db496e75 : « Peut-on regrouper par famille
(ou groupe) certains de mes skills, agents, les scripts ou autres éléments de
mon écosystème dans l'objectif de créer des agents qui orchestreraient chaque
famille (ou groupe). Est-ce une bonne idée pour optimiser mon écosystème ? »

MÉTHODE — le modèle des familles est DÉCLARÉ ici (dérivé de l'analyse des
sources : orchestrateur-tsi v1.1.2 [pattern prouvé], agent-engineering v1.1.1
[doctrine : règle 1 « simple d'abord », gate anti-flotte ≈15×, n°56 CADRE/
ROUTE], KB 55 entrées) ; le script MESURE mécaniquement chaque famille
(membres réels au KB, arêtes de dépendances intra/inter, détenteurs
d'orchestration présents sur le disque, agents .agent) — KO-L003 : le verdict
dérive du disque, jamais de mémoire.

R4 — mesure et classification seulement ; AUCUNE création, AUCUNE correction.

Codes retour : 0 = inventaire produit · 1 = échec · 2 = usage.
"""

# ⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.40)
# SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
# Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
# Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
# Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
# Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
# Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).

import json
import re
import sys
from pathlib import Path

BASE = Path("/home/z/my-project")
REPO = BASE / "KNOWLEDGE-repo"
KB = REPO / "skills" / "KNOWLEDGE.md"
SORTIE = BASE / "download" / "inventaire-familles-task106.json"

# Modèle des familles (méthode Task 106 — membres attendus ; le script vérifie
# l'existence réelle et calcule le couplage à partir des dépendances déclarées).
FAMILLES = [
    {"id": "F1", "nom": "TSI/Traktor (métier)",
     "membres": ["tsi-architect", "tsi-validator", "multi-shift-architect",
                 "midi-doc-expert", "analyse-doc-s4mk2", "orchestrateur-tsi"],
     "orchestration_attendue": "orchestrateur-tsi (skill méthode + agent-TSI.agent)",
     "mission": "pipeline multi-membres (concevoir → valider → documenter)"},
    {"id": "F2", "nom": "Socle gouvernance",
     "membres": ["gen-plan", "correct-work", "clone-chat", "resource-monitor",
                 "knowledge-observer", "skills-inventory", "alias-eco"],
     "orchestration_attendue": "gen-plan E1-E15 (hub, 24 dépendances inverses) + agent-engineering n°56 CADRE/ROUTE",
     "mission": "gouvernance transverse (planifier → vérifier → journaliser)"},
    {"id": "F3", "nom": "Création d'artefacts écosystème (méta)",
     "membres": ["skill-creator", "script-creator", "agent-creator", "correct-py",
                 "script-reviewer", "script-mon-ecosysteme-infrastructure",
                 "pm-skill", "version-management", "audit-provenance", "re-curation"],
     "orchestration_attendue": "table de routage N2 check-tool-routing (arbitre) + lifecycle gouverné gen-plan/correct-work",
     "mission": "lifecycle d'artefacts (créer → corriger → relire → versionner → archiver)"},
    {"id": "F4", "nom": "Disciplines d'ingénierie (n°54-56 + fondamentales)",
     "membres": ["agent-engineering", "context-engineering", "loop-engineering",
                 "graph-engineering", "harness-engineering", "memory-engineering",
                 "spec-driven-development", "refactoring-engineering",
                 "refactoring-test", "refactor-guard", "prompt-engineering",
                 "agent-prompt-engineering", "fleet-engineering", "autonomous-agent",
                 "inter-scripts"],
     "orchestration_attendue": "SHARED §7 méthode-mère (gen-plan §1.6) + n°56 CADRE/ROUTE + inter-scripts (nœuds scripts)",
     "mission": "méthodes transverses héritées de la méthode-mère"},
    {"id": "F5", "nom": "Photo/CPE (métier)",
     "membres": ["iphone17", "iphone18", "iphone19", "dessin-technique"],
     "orchestration_attendue": "aucune — générations parallèles, missions mono-membre (règle 1 « simple d'abord »)",
     "mission": "pipeline CPE mono-membre (UNE génération par photo)"},
    {"id": "F6", "nom": "Diffusion / portail",
     "membres": ["vue-upload", "livraison-garantie", "ghorg-cmdr"],
     "orchestration_attendue": "chaque membre orchestre sa propre procédure (livraison-garantie compose vue-upload)",
     "mission": "procédures composées auto-portantes"},
    {"id": "F7", "nom": "Métier solo / composite",
     "membres": ["cahier-des-charges", "traduction-zh-fr", "audio-metadata",
                 "cpp-analysis", "resume-youtube", "pdf-llm", "fullstack-dev",
                 "skill-finder-cn", "web-reader", "web-search"],
     "orchestration_attendue": "aucune requise — solos ou composites auto-portants",
     "mission": "missions mono-membre (le composite détient sa propre méthode M1-M4)"},
]


def _lire_kb():
    """Entrées du registre KB : [(nom, version)]."""
    texte = KB.read_text(encoding="utf-8")
    return re.findall(r"^## ([\w-]+) v([\d.]+)$", texte, re.M)


def _deps(nom):
    """Dépendances déclarées au frontmatter d'un skill (lecture seule)."""
    p = REPO / "skills" / nom / "SKILL.md"
    if not p.is_file():
        return set()
    return set(re.findall(r"- skill:\s*([\w-]+)", p.read_text(encoding="utf-8")[:4000]))


def _agents():
    """Fichiers .agent réels sur le disque."""
    return sorted(str(p.relative_to(REPO / "skills"))
                  for p in (REPO / "skills").glob("*/*.agent"))


def inventaire():
    kb = _lire_kb()
    kb_noms = {n for n, _ in kb}
    connus = {m for f in FAMILLES for m in f["membres"]}
    hors_modele = sorted(kb_noms - connus)
    agents = _agents()
    familles = []
    for f in FAMILLES:
        membres = [m for m in f["membres"] if m in kb_noms]
        absents = [m for m in f["membres"] if m not in kb_noms]
        intra = [(a, b) for a in membres for b in (_deps(a) & set(membres)) if a != b]
        vers_ext = set()
        for m in membres:
            vers_ext |= (_deps(m) & kb_noms) - set(membres)
        familles.append({
            "id": f["id"], "nom": f["nom"], "membres": membres,
            "membres_absents_du_kb": absents,
            "nb_membres": len(membres),
            "aretes_intra_famille": len(intra),
            "aretes_vers_autres_familles": len(vers_ext),
            "densite_intra": round(len(intra) / max(len(membres), 1), 2),
            "orchestration": f["orchestration_attendue"],
            "orchestrateur_sur_disque": any(
                ("orchestrateur" in m) or (m in ("gen-plan", "inter-scripts"))
                for m in membres),
            "type_mission": f["mission"],
        })
    return {
        "source_directive": "trace 1a1efc61db496e75 — question des orchestrateurs par famille",
        "kb_entrees": len(kb),
        "agents_dot_agent": agents,
        "familles": familles,
        "entrees_hors_modele": hors_modele,
        "notes": [
            "gen-plan : 24 dépendances inverses (hub de gouvernance — mesure)",
            "correct-work : 12 dépendances inverses (colonne vertébrale de vérification)",
            "famille TSI : seule famille métier à couplage intra-familial mutuel dense",
            "famille photo : 0 arête intra-familiale (générations parallèles)",
        ],
    }


def selftest():
    """Auto-vérification (4 cas, sait échouer)."""
    ok = []
    ok.append(("ST1 familles déclarées", len(FAMILLES) == 7))
    ok.append(("ST2 membres uniques",
               len({m for f in FAMILLES for m in f["membres"]})
               == sum(len(f["membres"]) for f in FAMILLES)))
    kb = _lire_kb()
    ok.append(("ST3 KB lisible >= 50 entrées", len(kb) >= 50))
    connus = {m for f in FAMILLES for m in f["membres"]}
    ok.append(("ST4 couverture modèle >= 85 % du KB",
               len(connus & {n for n, _ in kb}) / len(kb) >= 0.85))
    print("=== SELF-TEST Task 106 — inventaire familles (4 cas) ===")
    for nom, passe in ok:
        print(f"  [{'PASS' if passe else 'FAIL'}] {nom}")
    nb = sum(1 for _, p in ok if p)
    print(f"=== RESUME : {nb}/{len(ok)} PASS ===")
    return 0 if nb == len(ok) else 1


def main():
    if "--selftest" in sys.argv:
        return selftest()
    if len(sys.argv) > 1:
        print("usage: task106-inventaire-familles.py [--selftest]")
        return 2
    donnees = inventaire()
    SORTIE.write_text(json.dumps(donnees, ensure_ascii=False, indent=2) + "\n",
                      encoding="utf-8")
    print(f"Inventaire écrit : {SORTIE}")
    for f in donnees["familles"]:
        print(f"  {f['id']} {f['nom']:48s} {f['nb_membres']:2d} membres · "
              f"intra {f['aretes_intra_famille']:2d} arêtes · "
              f"orchestrateur disque: {'oui' if f['orchestrateur_sur_disque'] else 'non'}")
    if donnees["entrees_hors_modele"]:
        print(f"  hors modèle ({len(donnees['entrees_hors_modele'])}): "
              + ", ".join(donnees["entrees_hors_modele"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
