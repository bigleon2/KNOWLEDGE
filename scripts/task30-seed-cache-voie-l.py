#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.13)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

# -*- coding: utf-8 -*-
"""
Task 30 (GO propriétaire) — Seed du cache voie L avec les VERDICTS FIGÉS de la
discussion PM INSTALL (source de vérité, scripts/discussion-64c90144.txt).

Deux niveaux de traçabilité :
- verdict-cite : verdict cité verbatim dans la discussion (ex. « jd → true ✓ ») ;
- confirme-eval-task30 : verdict dérivé de l'arbitrage documenté Task 25/30
  (CONFIRME-eval : les evals sont conformes aux SKILL.md — le verdict figé =
  la valeur attendue du corpus), pour les cas couverts par la campagne Task 30
  (drift list citée) dont le verdict exact est perdu (cache non commité).

Idempotent : entrée existante identique = no-op ; entrée existante différente =
refus (le cache est R4 — ne jamais écraser un verdict figé).
"""
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
CACHE = BASE / "scripts" / "voie-l-cache.json"

CITES = [
    ("jd-resume-tailor", "j'ai besoin de la tâche « jd » — quelle est la procédure ?", True,
     "Cité : « jd → true ✓ » — convention de token de tâche (discussion PM INSTALL)"),
    ("ai-news-collectors", "la tâche « ai »", True,
     "Cité : « true — cohérent avec la convention écosystème (même mécanique que « jd ») »"),
    ("cahier-des-charges", "Décompose la spécification exécutable de cette tâche en plan puis en tâches atomiques.", False,
     "Cité : « cahier → false ✓ » — décomposition en tâches = SDD/gen-plan, pas rédaction de CDC"),
    ("iphone19", "Prépare cette photo en poster A4 à 300 DPI pour impression.", False,
     "Cité : re-arbitrage de ROUTAGE documenté dans l'entrée (poster = capacité iphone19 MAIS doctrine d'époque → génération courante iphone18)"),
    ("iphone19", "Améliore cette photo qualité max.", False,
     "Cité : résiduel iphone19 « résorbé par le cache canonique (doctrine d'époque) » — amélioration générique → iphone18"),
    ("iphone19", "Restaure ce scan de photo ancienne des années 80, rendu propre et net.", False,
     "Cité : résiduel iphone19 « résorbé par le cache canonique (doctrine d'époque) » — restauration générique → iphone18"),
]

CONFIRME = [
    ("gen-plan", "gen-plan (stp) : lance ce mode pour ce projet.", False,
     "CONFIRME-eval : « (stp) » n'est pas un mode nommé (E1-E15) — la doctrine gen-plan exige le mode explicitement demandé"),
    ("refactor-guard", "je veux découper cette God Class de 2000 lignes sans rien casser", True,
     "CONFIRME-eval : découpe de God Class = cœur du périmètre refactor-guard (drift list citée : « refactor-guard (« God Class ») »)"),
    ("agent-browser", "Automatiser des interactions web", True,
     "CONFIRME-eval : automatisation d'interactions web = périmètre littéral agent-browser (drift list citée)"),
    ("agent-browser", "j'ai besoin de Automatiser des interactions web — quelle est la procédure ?", True,
     "CONFIRME-eval : idem, forme procédurale"),
    ("agent-browser", "peux-tu Automatiser des interactions web ?", True,
     "CONFIRME-eval : idem, forme interrogative"),
    ("agent-prompt-engineering", "évalue ce SKILL.md selon la grille et propose des ajustements", True,
     "CONFIRME-eval : évaluation selon grille + ajustements = périmètre agent-prompt-engineering (drift list citée)"),
    ("agent-prompt-engineering", "restructure la section §5 de ce PM sans perdre de sémantique", True,
     "CONFIRME-eval : restructuration de prompt/PM = périmètre agent-prompt-engineering"),
    ("version-management", "看看这个项目都有哪些历史版本", True,
     "CONFIRME-eval : re-arbitrage description-complète (Task 30 : « version-management ×3 » corrigés, verdicts conformes) — consultation historique versions"),
    ("version-management", "恢复到 V2，刚才那版改坏了", True,
     "CONFIRME-eval : restauration de version = cœur du périmètre version-management"),
    ("version-management", "切回我上次的那个项目", True,
     "CONFIRME-eval : bascule vers le projet précédent = périmètre version-management"),
]


def main():
    cache = json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.exists() else {}
    ajoutes, noop, conflits = 0, 0, []
    for skill, query, verdict, trace in CITES + CONFIRME:
        cle = f"{skill}::{query}"
        if cle in cache:
            if cache[cle].get("verdict") == verdict:
                noop += 1
            else:
                conflits.append(cle)
            continue
        cache[cle] = {
            "verdict": verdict,
            "statut": "fige",
            "question_type": "routage",
            "date_fixation": "2026-10-24",
            "source": "discussion PM INSTALL (Task 30, verdicts figés)" if trace.startswith("Cité")
                      else "arbitrage Task 25/30 CONFIRME-eval (discussion PM INSTALL)",
            "trace": trace,
        }
        ajoutes += 1
    CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"SEED : {ajoutes} verdict(s) figé(s) ajouté(s), {noop} déjà en place (no-op), "
          f"{len(conflits)} conflit(s) : {conflits or 'aucun'}")
    sys.exit(1 if conflits else 0)


if __name__ == "__main__":
    main()
