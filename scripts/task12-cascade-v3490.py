#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
task12-cascade-v3490.py — Cascade KO-L004 de la montée gen-plan v3.48.0 → v3.49.0 (Task 12, G4).

Étapes mécaniques :
  (1) migration R4 byte-identité : l'entrée v3.48.0 du SKILL.md §5.6 migre vers
      references/journal-versions.md (en tête d'archive, après la note de mécanique) ;
      §5.6 ne conserve que l'entrée courante v3.49.0 (mécanique v3.39.0) ;
  (2) delta verrouillé scripts/delta-genplan-v3490.json (history = résumé de la montée
      pour la table des versions du PM — consommé par scripts/generer-pm-skill.py).

Idempotent ×2 : second passage = NO-OP (R6). Python stdlib. rc : 0 OK, 1 erreur.

Usage : python3 scripts/task12-cascade-v3490.py [--check]
"""
# ⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.46)
# SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
# Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
# Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
# Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan).

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SKILL = REPO / "skills" / "gen-plan" / "SKILL.md"
JOURNAL = REPO / "skills" / "gen-plan" / "references" / "journal-versions.md"
DELTA = REPO / "scripts" / "delta-genplan-v3490.json"

PREFIX_V48 = "- **v3.48.0 ("
PREFIX_V49 = "- **v3.49.0 ("

HISTORY = (
    "É1-INSTALL étendu — garde à TOUTE invocation (directive propriétaire trace 1a21e208f489f7f5 : chaque "
    "nouvelle requête, plus seulement l'ouverture de session) + point d'entrée AMORÇABLE (shim "
    "scripts/ensure-installed.py → repli bootstrap canonique PM-INSTALL §3.2-d v1.10.7 — fin de "
    "l'œuf-et-la-poule) + réinstallation des éléments INDISPENSABLES ADAPTÉS au plan (fermeture MINIMALE + "
    "skills routés É5-ROUTAGE, jamais l'arbre complet sauf directive — verdict INSTALLE-POUR-PLAN) + "
    "SEEDS-FIRST ; hook É5-DISCIPLINES : orchestration-disciplines v1.0.0 (routage-disciplines.py → section "
    "« Orchestration des disciplines » du plan : mobilisation par étape + protocole d'évolution — E13 règle "
    "d'or n°3 + re-injection MÉCANIQUE des résultats vérifiés des tâches parallèles aux checkpoints E11 et "
    "frontières de groupes, scan disque KO-L003) ; dependencies += orchestration-disciplines >= 1.0.0 ; "
    "§3 relations += orchestration-disciplines ; précision propriétaire trace 1a21e38435b96641 (E13 en vol — "
    "audit de déduplication rôles/objectifs) : alignement règle d'or n°9 (rétablissement GRADUÉ — fermeture "
    "MINIMALE adaptée au plan quand les piliers sont sains, voie complète 4 temps conservée sinon ; n°9 = "
    "règle source, É1-INSTALL = implémentation — note de raffinement regles-or.md) + correctif placement "
    "ligne É5-DISCIPLINES dans le tableau §1.2bis + frontière documentée sweep-entetes-shared.py (réparation "
    "§0 au bootstrap) ↔ sync-context-block.py (injection §0 à la génération — PM-INSTALL §3.2-c v1.10.8). "
    "MINOR, additions pures (non-régression triggers). Cascade KO-L004 : PM v3.49.0 généré mécaniquement + "
    "KB + v3.48.0 migrée R4 byte-identité references/journal-versions.md + pin ECO_SKILLS recalibré + "
    "certification."
)


def main() -> int:
    check = "--check" in sys.argv
    actions = []
    texte = SKILL.read_text(encoding="utf-8")
    journal = JOURNAL.read_text(encoding="utf-8")

    if PREFIX_V49 not in texte:
        print("[ERREUR] entrée v3.49.0 absente du SKILL.md §5.6 — prérequis non satisfait")
        return 1

    # (1) migration R4 byte-identité v3.48.0 → journal-versions.md
    if PREFIX_V48 in texte:
        lignes = texte.split("\n")
        entree = next(l for l in lignes if l.startswith(PREFIX_V48))
        if any(l.startswith(PREFIX_V48) for l in journal.split("\n")):
            print("[ERREUR] entrée v3.48.0 déjà présente au journal — état incohérent (R2)")
            return 1
        if check:
            actions.append("MIGRATION v3.48.0 → journal-versions.md (à faire)")
        else:
            nouvelles = [l for l in lignes if l != entree]
            # retirer une éventuelle ligne vide double résultante en §5.6
            SKILL.write_text("\n".join(nouvelles), encoding="utf-8")
            ancre = "- **v3.47.0 ("
            idx = journal.index(ancre)
            journal = journal[:idx] + entree + "\n\n" + journal[idx:]
            JOURNAL.write_text(journal, encoding="utf-8")
            actions.append("MIGRATION v3.48.0 → journal-versions.md (byte-identité, en tête d'archive)")
    else:
        actions.append("MIGRATION v3.48.0 : déjà migrée (NO-OP)")

    # (2) delta verrouillé
    delta = {"history": HISTORY, "subs": []}
    if DELTA.exists() and json.loads(DELTA.read_text(encoding="utf-8")) == delta:
        actions.append("DELTA v3490 : déjà écrit identique (NO-OP)")
    elif check:
        actions.append("DELTA v3490 : à écrire")
    else:
        DELTA.write_text(json.dumps(delta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        actions.append("DELTA v3490 : écrit (history verrouillée, subs [])")

    for a in actions:
        print("[%s]" % a)
    print("RC=0 — cascade préparation %s" % ("VÉRIFIÉE (--check)" if check else "EXÉCUTÉE"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
