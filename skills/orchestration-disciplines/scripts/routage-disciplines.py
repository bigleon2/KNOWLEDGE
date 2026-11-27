#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
routage-disciplines.py — C1 DÉCISION mécanique du skill orchestration-disciplines.

Dérive le PLAN DE MOBILISATION des disciplines d'ingénierie de prompts d'un plan
d'actions gen-plan à partir de 4 entrées : tâche normalisée, déclencheur (NULL /
step / step-ok / orchestre / generate / correct-work / reprise), verdict de
complexité É5-ROUTAGE (SIMPLE / COMPLEXE ≥ 2/5), état du plan. La matrice de
décision est la forme MÉCANIQUE de la spécification portée par les tables
sources (R4 une information une source) : gen-plan/references/disciplines-
mobilisation.md + SHARED §7 — jamais dupliquées ailleurs.

Création v1.0.0 — Task 12, session web-220878ed (directive propriétaire trace
1a21e208f489f7f5 : « génère des skills ou des agents spécialisés pour que
toutes ces disciplines s'exécutent et s'orchestrent »).

Usage :
  routage-disciplines.py --tache "<demande>" [--declencheur step]
                         [--complexite SIMPLE|COMPLEXE] [--json]
  routage-disciplines.py --check-coherence
  routage-disciplines.py --selftest

Codes retour : 0 = OK · 1 = incohérence détectée (--check-coherence) · 2 = usage.
Idempotent ×2 : mêmes entrées → même sortie (byte-stable, R6).
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
import sys
from pathlib import Path

SKILLS_ROOT = Path(__file__).resolve().parents[2]
SOURCE_TABLES = SKILLS_ROOT / "gen-plan" / "references" / "disciplines-mobilisation.md"

# — Matrice de décision (forme mécanique des tables sources — R4) —
SOCCLE = ["context-engineering", "loop-engineering", "graph-engineering",
          "harness-engineering", "prompt-engineering"]

TABLE_E1_E15 = {
    "E1": ["prompt-engineering", "context-engineering"],
    "E2": ["context-engineering", "graph-engineering"],
    "E3": ["prompt-engineering"],
    "E4": ["harness-engineering", "spec-driven-development", "memory-engineering",
           "refactoring-test", "refactoring-engineering"],
    "E5": ["graph-engineering", "context-engineering", "fleet-engineering"],
    "E6": ["harness-engineering", "resource-monitor"],
    "E7": ["loop-engineering", "context-engineering", "harness-engineering",
           "spec-driven-development", "fleet-engineering", "refactoring-test"],
    "E8": ["harness-engineering", "prompt-engineering"],
    "E9-E14": ["memory-engineering", "fleet-engineering", "resource-monitor",
               "refactoring-test", "refactoring-engineering"],
    "E15": ["loop-engineering", "graph-engineering", "memory-engineering",
            "refactoring-test", "resource-monitor"],
}

EXTENSIONS_DECLNCHEUR = {
    "NULL": [],
    "step": ["harness-engineering", "memory-engineering"],
    "step-ok": ["harness-engineering", "memory-engineering"],
    "orchestre": ["fleet-engineering", "graph-engineering", "memory-engineering"],
    "generate": ["spec-driven-development", "harness-engineering", "prompt-engineering"],
    "correct-work": ["harness-engineering", "refactoring-test",
                     "refactoring-engineering", "refactor-guard", "memory-engineering"],
    "reprise": ["memory-engineering", "harness-engineering", "resource-monitor"],
}

EXTENSIONS_COMPLEXE = ["fleet-engineering", "spec-driven-development", "agent-engineering"]

PROTOCOLE_EVOLUTION = {
    "nouvelle_requete_proprietaire": {
        "intègre dans le plan d'actions": "extension E13 EN PLACE (jamais réécriture destructrice R2 — règle d'or n°3)",
        "met à jour": "re-génération d'un NOUVEAU plan consolidé (statuts dérivés du disque, restes-à-faire re-planifiés, re-estimation #token, answer key re-numérotée)",
    },
    "resultats_verifies_taches_paralleles": {
        "quand": "checkpoints E11 et CHAQUE frontière de groupe",
        "comment": "scan MÉCANIQUE du disque (KO-L003 — worklog, verdicts d'arbitres JSON, empreintes de livrables) ; périmètres croisés avec les tâches parallèles liées déclarées",
        "si_impact": "ajustement E13 + re-validation E8 + PLAN-AFFICHE rejoué + décision journalisée (règle d'or n°1)",
        "si_sans_impact": "poursuite — scan consigné au worklog",
    },
    "gardes_fous": ["G-RES à chaque checkpoint (PRESSION → ECO, CRITIQUE → série/PAUSE)",
                    "FAIL découvert → FAIL-CLOSE §1.18 gen-plan (correction avant fermeture d'étape, journal-fails.md)",
                    "secret exposé → KO-L009 (jamais utiliser, révocation, push = propriétaire)",
                    "toute adaptation journalisée (règle d'or n°1)"],
}


def decider(tache: str, declencheur: str = "NULL", complexite: str = "SIMPLE"):
    """Dérive le plan de mobilisation — décision pure, idempotente."""
    declencheur = declencheur if declencheur in EXTENSIONS_DECLNCHEUR else "NULL"
    extensions = list(EXTENSIONS_DECLNCHEUR[declencheur])
    if complexite.upper() == "COMPLEXE":
        extensions += [d for d in EXTENSIONS_COMPLEXE if d not in extensions]
    mobilisation = {}
    for etape, disciplines in TABLE_E1_E15.items():
        mobilisation[etape] = sorted(set(disciplines) | set(extensions))
    mobilisation_toutes = sorted(set().union(*TABLE_E1_E15.values())
                                 | set(extensions) | set(SOCCLE))
    return {
        "tache": tache[:200],
        "declencheur": declencheur,
        "complexite": complexite.upper(),
        "socle_commun": SOCCLE,
        "mobilisation_par_etape": mobilisation,
        "disciplines_mobilisees": mobilisation_toutes,
        "protocole_evolution": PROTOCOLE_EVOLUTION,
        "source_tables": "gen-plan/references/disciplines-mobilisation.md (R4 — source unique, jamais dupliquée)",
        "note_agent_engineering": ("agent-engineering mobilisée UNIQUEMENT sur délégation d'agents — "
                                   "porte de complexité gen-plan §1.17 (verdict COMPLEXE ≥ 2/5 requis)"),
    }


def check_coherence() -> int:
    """Vérifie que chaque discipline de la matrice existe comme forme installée
    (dérivation depuis skills/ — KO-L003) et que la source des tables est présente."""
    incoherences = []
    if not SOURCE_TABLES.is_file():
        incoherences.append(f"tables sources introuvables : {SOURCE_TABLES}")
    toutes = sorted(set().union(*TABLE_E1_E15.values())
                    | set(EXTENSIONS_COMPLEXE) | set(SOCCLE))
    for discipline in toutes:
        if not (SKILLS_ROOT / discipline / "SKILL.md").is_file():
            incoherences.append(f"discipline non matérialisée : skills/{discipline}/SKILL.md absent")
    if incoherences:
        for inc in incoherences:
            print(f"  [INCOHÉRENCE] {inc}")
        print(f"CHECK-COHERENCE FAIL ({len(incoherences)} — matrice ≠ formes installées)")
        return 1
    print(f"CHECK-COHERENCE PASS ({len(toutes)} disciplines de la matrice toutes matérialisées "
          f"+ tables sources présentes — KO-L003)")
    return 0


def selftest() -> int:
    """Tests internes — AUCUNE mutation (lecture seule)."""
    checks = []
    r1 = decider("corrige le document", "NULL", "SIMPLE")
    checks.append(("socle commun toujours présent (5 disciplines, déclencheur NULL)",
                   r1["socle_commun"] == SOCCLE and r1["declencheur"] == "NULL"))
    r2 = decider("vérifie et corrige le projet", "correct-work", "SIMPLE")
    checks.append(("déclencheur correct-work → trio refactoring mobilisé (refactor-guard inclus)",
                   "refactor-guard" in r2["disciplines_mobilisees"]
                   and "refactoring-engineering" in r2["disciplines_mobilisees"]))
    r3 = decider("orchestre la migration multi-domaines", "step", "COMPLEXE")
    checks.append(("complexité COMPLEXE → extensions fleet + spec-driven + agent-engineering",
                   all(d in r3["disciplines_mobilisees"]
                       for d in EXTENSIONS_COMPLEXE)))
    r4 = decider("reprise après coupure", "reprise", "SIMPLE")
    checks.append(("reprise E1-RES → memory-engineering + resource-monitor",
                   "memory-engineering" in r4["disciplines_mobilisees"]
                   and "resource-monitor" in r4["disciplines_mobilisees"]))
    r5a = json.dumps(decider("tâche X", "step", "SIMPLE"), sort_keys=True, ensure_ascii=False)
    r5b = json.dumps(decider("tâche X", "step", "SIMPLE"), sort_keys=True, ensure_ascii=False)
    checks.append(("idempotence ×2 : mêmes entrées → sortie byte-stable", r5a == r5b))
    r6 = decider("tâche X", "step", "SIMPLE")
    checks.append(("protocole d'évolution complet (2 sources + garde-fous)",
                   len(r6["protocole_evolution"]["nouvelle_requete_proprietaire"]) == 2
                   and "resultats_verifies_taches_paralleles" in r6["protocole_evolution"]
                   and len(r6["protocole_evolution"]["gardes_fous"]) >= 4))
    ok = all(o for _, o in checks)
    for nom, ok_c in checks:
        print(f"  [{'PASS' if ok_c else 'FAIL'}] {nom}")
    print(f"SELFTEST {'PASS' if ok else 'FAIL'} ({sum(1 for _, o in checks if o)}/{len(checks)})")
    return 0 if ok else 1


def main() -> int:
    parse = argparse.ArgumentParser(description="C1 décision mécanique — mobilisation des disciplines du plan")
    parse.add_argument("--tache", help="demande normalisée (texte)")
    parse.add_argument("--declencheur", default="NULL",
                       choices=sorted(EXTENSIONS_DECLNCHEUR),
                       help="déclencheur gen-plan (défaut NULL)")
    parse.add_argument("--complexite", default="SIMPLE", choices=["SIMPLE", "COMPLEXE"],
                       help="verdict de complexité É5-ROUTAGE (défaut SIMPLE)")
    parse.add_argument("--json", action="store_true", help="sortie JSON machine")
    parse.add_argument("--check-coherence", action="store_true",
                       help="vérifie matrice ↔ formes installées + tables sources")
    parse.add_argument("--selftest", action="store_true", help="tests internes (aucune mutation)")
    args = parse.parse_args()
    if args.selftest:
        return selftest()
    if args.check_coherence:
        return check_coherence()
    if not args.tache:
        parse.error("--tache requis (ou --check-coherence / --selftest)")
        return 2
    rapport = decider(args.tache, args.declencheur, args.complexite)
    if args.json:
        print(json.dumps(rapport, ensure_ascii=False, indent=2))
    else:
        print(f"MOBILISATION DES DISCIPLINES — déclencheur {rapport['declencheur']}, "
              f"complexité {rapport['complexité']}")
        print(f"  socle commun : {', '.join(rapport['socle_commun'])}")
        print(f"  disciplines mobilisées ({len(rapport['disciplines_mobilisees'])}) : "
              f"{', '.join(rapport['disciplines_mobilisees'])}")
        print(f"  source : {rapport['source_tables']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
