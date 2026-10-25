#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.7)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

# -*- coding: utf-8 -*-
"""E15 knowledge-observer M1-M2 — journalisation des leçons de l'audit (Task 5).

Ajoute L009-L011 au journal skills/knowledge-observer/data/lessons-learned.json
(format exact : id, pattern, occurrences, sources, proposition, marqueur,
cible_application, statut, session, verdict_correct_work).

Idempotent : rejeu ×2 sans effet (clé d'unicité = id ; entrée déjà présente
=> no-op). Vérification : len(lessons) attendu 11 après passage.
Usage : python3 scripts/audit-e15-lessons.py
"""

import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
JOURNAL = BASE / "skills" / "knowledge-observer" / "data" / "lessons-learned.json"

NOUVELLES = [
    {
        "id": "L009",
        "pattern": "Avertissement sans porte (WARN-without-gate) : un outil écrit son artefact avec un code retour 0 et un simple [WARN] alors qu'un invariant n'est pas satisfait — l'artefact incomplet entre dans l'état, les arbitres en place ne contrôlent pas l'axe manquant, et l'écart devient invisible de bout en bout. Cas d'espèce KO-L004 : generer-pm-skill.py écrit le PM malgré coverage_missing non vide (« deltas sémantiques à complétion agent » auto-documenté dans la ligne d'historique), --check ne vérifie que les versions (COHERENT), aucun des 6 arbitres ne contrôle la complétude sémantique PM ↔ SKILL.md — un PM « coquille » version-cohérent mais sémantiquement vide passe pour vert (cause identifiée du bug « GEN-PLAN oublie de générer les plans d'actions depuis v3.24.0 »)",
        "occurrences": 2,
        "sources": [
            "Génération KO-L004 v1.1.0 (2026-10-09, PM-INSTALL §2quater v1.6.0) : mécanisme coverage_missing + complétion agent introduit sans gate",
            "Audit Task 5 (2026-10-25, session web-eb6c8580, Phase C sandbox) : reproduction directe — bump gen-plan v3.23.1→v3.24.0, [WARN] §1.13, exit 0, PM v3.24.0 écrit (1476 L), --check COHERENT — diff intégral : 6 substitutions de version, aucun bloc perdu (rapport download/rapport-test-bug-genplan-v3240.md)"
        ],
        "proposition": "Tout WARN d'un outil générateur doit être adossé à une porte : code retour dédié (exit 4 ÉCART-COMPLÉTUDE) + marqueur d'état dans l'artefact (remplacé à la complétion) + vérification de l'axe par un arbitre de la chaîne de certification (--check renforcé PM-SHELL + arbitre de complétude sémantique sections SKILL.md ⊆ PM). Correctif proposé en 5 points — application = décision propriétaire (D007).",
        "marqueur": "PATTERN:KO-L009-v1.0.0 (à matérialiser dans gen-plan §1.15 / PM-INSTALL §2quater au prochain bump, si le correctif est adopté)",
        "cible_application": "scripts/generer-pm-skill.py (gate + --complete) ; certification-complete.py (arbitre de complétude) ; PM-INSTALL §2quater ; PM gen-plan §1.15",
        "statut": "proposé",
        "session": "web-eb6c8580 (suite) — Task 5 audit, 2026-10-25",
        "verdict_correct_work": "en attente (proposition — validation à l'application)"
    },
    {
        "id": "L010",
        "pattern": "Couche documentaire @historique hors recalibrage croisé KO-L004 : les montées de version du socle (SHARED, PM-INSTALL, SYNC-CONTEXT, README, registre KB) déclenchent le recalibrage des outils et de l'archive d'intégrité, mais PAS la mise à jour des tables @historique (procédure §4/§7 du dossier non exécutée) — la couche documentaire prend 3-4 versions de retard et ses comptes internes divergent (en-tête « 21 PMs » vs 23 lignes vs 24 fichiers ; instantané KB « 30 entrées » vs table 32 vs registre 33 ; marqueur « VERSION VIVANTE » résiduel sur une version supplantée)",
        "occurrences": 4,
        "sources": [
            "Montée gen-plan v3.23.1/Task 8 (2026-10-12) : SHARED v1.7.4, PM-INSTALL v1.6.4 — aucune ligne @historique",
            "Montée refactor-guard/Task 9 D009 (2026-10-12) : SHARED v1.7.5, PM-INSTALL v1.6.5 — aucune ligne @historique",
            "Directive PM-INSTALL v1.7.0 (2026-10-12) : SHARED v1.7.6, SYNC v1.4.8, README v2.1.6 — aucune ligne @historique",
            "Montée clone-chat v2.0.1/Task 12 (2026-10-12) : SHARED v1.7.7, PM-INSTALL v1.7.1, SYNC v1.4.9, README v2.1.7 — aucune ligne @historique (commit b75a620 matérialise l'état : corpus v1.7.7/v1.7.1/v1.4.9/v2.1.7 vs tables figées ≤ v1.7.4/≤ v1.6.3/≤ v1.4.7/≤ v2.1.4)"
        ],
        "proposition": "Étendre le recalibrage croisé KO-L004 à la couche @historique : à chaque montée, l'étape 4/§4/§7 du dossier (ajout de ligne + rafraîchissement §2 + index §5) est exécutée et vérifiée par un arbitre dédié (adossé à scripts/audit-phaseA-historique.py — ALL PASS 24/24 : byte-identité + couverture croisée index ↔ disque + cohérence des comptes). L'arbitre est déjà en place (correction appliquée drift e/g de l'audit Task 5) ; reste à l'intégrer au sweep arbitres avant commit.",
        "marqueur": "PATTERN:KO-L010-v1.0.0 (à matérialiser dans SYNC-CONTEXT / PM-INSTALL §2quater au prochain bump)",
        "cible_application": "scripts/audit-phaseA-historique.py (existant — arbitre Phase A) ; certification-complete.py (intégration au sweep) ; @historique/README.md §4 (rappel de l'obligation)",
        "statut": "appliqué (corrections drift e/g — 12 lignes + instantané 33 + README §2 + marqueurs ; arbitre ALL PASS ; re-certification 6/6)",
        "session": "web-eb6c8580 (suite) — Task 5 audit, 2026-10-25",
        "verdict_correct_work": "correct-work(CIBLE) Phase B : PASS AVEC RÉSERVES — corrections vérifiées (golden master, R2 intacts, 6/6)"
    },
    {
        "id": "L011",
        "pattern": "Invariants figés dans les arbitres (anti-KO-L003) : listes codées en dur (familles de PMs, chemins, compte attendu) au lieu d'être dérivées du filesystem — l'arbitre ignore les entrées nouvelles et rend un verdict faux-vert sur un état pourtant élargi (le nouveau v3.23.0 puis clone-chat v2.0.0 archivés n'étaient pas comptés ; l'en-tête d'index §5 annoncé restait « 21 PMs » à travers 3 élargissements successifs)",
        "occurrences": 2,
        "sources": [
            "Index §5 README @historique : en-tête « 21 PMs » inchangé à travers l'ajout v3.22.1 (22e), v3.23.0 (23e, Task 8) et clone-chat v2.0.0 (24e, Task 12) — découvert audit Task 5 Phase A (compte annoncé 21 vs réel 23 vs disque 24)",
            "Arbitre audit-phaseA-historique.py v1 (créé Task 5 Phase A) : parseur figé gen-plan|correct-work — la ligne clone-chat/PROMPT-MAITRE-CLONE-CHAT-v2.0.0.md (sceau 403435c9…) n'était pas matchée (compte annoncé 24 vs réel 23 après correction de l'en-tête) — recalibré le même jour : familles génériques [\\w-]+ + couverture croisée index ↔ disque"
        ],
        "proposition": "Règle générale : tout invariant de périmètre dérive du filesystem (glob/génération dynamique), jamais d'une liste ; tout compte annoncé est vérifié contre le compte réel à chaque rejeu (couverture croisée dans les deux sens — entrées non indexées et entrées fantômes). Appliqué : parseur générique + compte annoncé vs réel + couverture croisée (ALL PASS 24/24).",
        "marqueur": "PATTERN:KO-L011-v1.0.0 (généralisation du marqueur KO-L003 existant — même famille, angle périmètre vs invariant)",
        "cible_application": "scripts/audit-phaseA-historique.py (appliqué) ; relecture des arbitres à listes figées (sweep : certification-complete.py ECO_SKILLS, check-ecosysteme-integrity, verify-cross) — proposition au propriétaire",
        "statut": "appliqué (arbitre recalibré) / proposé (généralisation aux autres arbitres)",
        "session": "web-eb6c8580 (suite) — Task 5 audit, 2026-10-25",
        "verdict_correct_work": "correct-work(CIBLE) Phase A/B : PASS AVEC RÉSERVES puis ALL PASS après recalibrage"
    },
]


def main():
    journal = json.loads(JOURNAL.read_text(encoding="utf-8"))
    existants = {l.get("id") for l in journal["lessons"]}
    ajoutees = [l for l in NOUVELLES if l["id"] not in existants]
    if not ajoutees:
        print("No-op : L009-L011 déjà journalisées (idempotence ✓).")
        return
    journal["lessons"].extend(ajoutees)
    JOURNAL.write_text(json.dumps(journal, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")
    print(f"Leçons journalisées : {', '.join(l['id'] for l in ajoutees)} "
          f"(total {len(journal['lessons'])})")


if __name__ == "__main__":
    main()
