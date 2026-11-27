#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
task12-kb-eco-v3490.py — Inscription KB + pin ECO_SKILLS de la montée gen-plan v3.49.0 (Task 12, G4).

(1) KB skills/KNOWLEDGE.md — entrée gen-plan : « Dernière calibration » prépend v3.49.0
    (v3.48.0 démote en « précédent montée ») + Description += segment v3.49.0 ;
(2) ECO_SKILLS scripts/check-ecosysteme-integrity.py : pin gen-plan 3.48.0 → 3.49.0
    (commentaire KO-L004 prépend, ancien démote en « précédent »).

Idempotent ×2 : second passage = NO-OP (R6). Python stdlib. rc : 0 OK, 1 erreur.
"""
# ⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.47)
# SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
# Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
# Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
# Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan).

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
KB = REPO / "skills" / "KNOWLEDGE.md"
CHECKER = REPO / "scripts" / "check-ecosysteme-integrity.py"

CAL_V490 = (
    "montée v3.49.0 (2026-11-28, Task 12, web-220878ed, traces 1a21e208f489f7f5 [« analyse mon skill "
    "gen-plan et son système de réinstallation … qu'il fasse appel à mon fichier PM INSTALL pour "
    "ré-installer les éléments de mon écosystème qui sont indispensables et adaptés à l'exécution du plan "
    "d'actions à chaque nouvelle requête » + « génère des skills ou des agents spécialisés pour que toutes "
    "ces disciplines s'exécutent et s'orchestrent »] + précision déduplication 1a21e38435b96641 [audit "
    "rôles/objectifs : alignement règle d'or n°9 — rétablissement GRADUÉ, correctif placement tableau "
    "É5-DISCIPLINES §1.2bis, frontière sweep-entetes-shared.py ↔ sync-context-block.py PM-INSTALL §3.2-c, "
    "non-doublons consignés routage-disciplines ↔ routage-skills-agents et orchestration-disciplines ↔ "
    "agent-engineering/fleet-engineering/resource-monitor/orchestrateur-tsi] : É1-INSTALL garde à TOUTE "
    "invocation + point d'entrée AMORÇABLE (shim → repli bootstrap, PM-INSTALL §3.2-d) + fermeture MINIMALE "
    "adaptée au plan (verdict INSTALLE-POUR-PLAN, SEEDS-FIRST) + hook É5-DISCIPLINES orchestration-"
    "disciplines v1.0.0 [routage-disciplines.py — section « Orchestration des disciplines » du plan + "
    "protocole d'évolution E13 + re-injection résultats parallèles] ; MINOR, additions pures "
    "(non-régression triggers) ; cascade KO-L004 COMPLÈTE : PM v3.49.0 généré mécaniquement [delta "
    "verrouillé scripts/delta-genplan-v3490.json], SHARED v1.7.47 / PM-INSTALL v1.10.8 recalibrés par le "
    "générateur + note de frontière §3.2-c, KB, pin ECO_SKILLS 3.49.0, PM v3.48.0 archivé @historique R4, "
    "v3.48.0 migrée R4 byte-identité references/journal-versions.md, note de raffinement regles-or.md n°9, "
    "certification)"
)

DESC_V490 = (
    " ; garde É1-INSTALL à TOUTE invocation + fermeture MINIMALE adaptée au plan (v3.49.0 — raffinement "
    "règle d'or n°9 : rétablissement GRADUÉ, verdict INSTALLE-POUR-PLAN, point d'entrée AMORÇABLE "
    "PM-INSTALL §3.2-d, SEEDS-FIRST) ; hook É5-DISCIPLINES (v3.49.0) : orchestration-disciplines v1.0.0 — "
    "routage-disciplines.py (tables sources references/disciplines-mobilisation.md R4), section "
    "« Orchestration des disciplines » du plan + protocole d'évolution (re-injection des résultats vérifiés "
    "des tâches parallèles aux checkpoints E11 et frontières de groupes)"
)

ECO_NOUVEAU = (
    '"gen-plan": "3.49.0",  # KO-L004 (2026-11-28, web-220878ed — Task 12 : v3.49.0 É1-INSTALL à toute '
    'invocation + fermeture MINIMALE adaptée (INSTALLE-POUR-PLAN) + hook É5-DISCIPLINES '
    'orchestration-disciplines v1.0.0 + alignement règle d\'or n°9 rétablissement GRADUÉ [audit '
    'déduplication trace 1a21e38435b96641] ; précédent KO-L004 ('
)


def main() -> int:
    actions = []
    kb = KB.read_text(encoding="utf-8")

    # (1a) Description += v3.49.0
    if "hook É5-DISCIPLINES (v3.49.0)" in kb:
        actions.append("KB Description : déjà étendue (NO-OP)")
    else:
        ancre = "rappel permanent langue française §0)"
        assert kb.count(ancre) == 1, "ancre Description KB non unique"
        kb = kb.replace(ancre, ancre + DESC_V490, 1)
        actions.append("KB Description : segment v3.49.0 appendé")

    # (1b) Dernière calibration : prépend v3.49.0
    if "montée v3.49.0" in kb:
        actions.append("KB Dernière calibration : déjà à v3.49.0 (NO-OP)")
    else:
        ancre = "- **Dernière calibration** : montée v3.48.0 ("
        assert kb.count(ancre) == 1, "ancre calibration KB non unique"
        kb = kb.replace(ancre, "- **Dernière calibration** : " + CAL_V490 + " ; précédent montée v3.48.0 (", 1)
        actions.append("KB Dernière calibration : v3.49.0 en tête, v3.48.0 démote")

    KB.write_text(kb, encoding="utf-8")

    # (2) ECO_SKILLS pin
    src = CHECKER.read_text(encoding="utf-8")
    if '"gen-plan": "3.49.0"' in src:
        actions.append("ECO_SKILLS : pin déjà à 3.49.0 (NO-OP)")
    else:
        ancre = '"gen-plan": "3.48.0",  # KO-L004 ('
        assert src.count(ancre) == 1, "ancre ECO_SKILLS non unique"
        src = src.replace(ancre, ECO_NOUVEAU, 1)
        CHECKER.write_text(src, encoding="utf-8")
        actions.append("ECO_SKILLS : pin gen-plan 3.48.0 → 3.49.0")

    for a in actions:
        print("[%s]" % a)
    print("RC=0 — inscription KB + ECO_SKILLS EXÉCUTÉE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
