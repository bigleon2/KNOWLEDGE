#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.37)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan).
"""

# -*- coding: utf-8 -*-
"""
Task 86 G2 suite — cascade KO-L004 de la Description Optimization A10/A14 agent-engineering
v1.0.0 → v1.1.0 (directive 1a1bed51ccaf78f1 cadence 2 h tick 17:50).

Éditions chirurgicales all-or-nothing, ancres count==1, idempotent (2e passe NO-OP) :
  1. skills/KNOWLEDGE.md — entrée agent-engineering :
     a. en-tête « ## agent-engineering v1.0.0 » → v1.1.0
     b. Description miroir += clause A10/A14 (miroir exact du frontmatter)
     c. « Dernière calibration » : prepend v1.1.0 (mesure baseline + optimisation + re-mesure)
  2. skills/agent-engineering/evals/evals.json — note : état baseline MESURÉE
  3. skills/@historique/historiques-par-skill/agent-engineering.md — entrée v1.1.0

SHARED §7 : no-op (KO-L003 — version fait foi frontmatter + KB, lignes sans version figée).
gen-plan §1.6 : no-op (plancher >= v1.0.0 conforme à v1.1.0).
"""
import hashlib
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
KB = BASE / "skills" / "KNOWLEDGE.md"
EVALS = BASE / "skills" / "agent-engineering" / "evals" / "evals.json"
LIGNAGE = BASE / "skills" / "@historique" / "historiques-par-skill" / "agent-engineering.md"

CLAUSE_KB = ("Contrôles négatifs assumés (A10/A14) : ne se déclenche PAS pour la coordination "
             "d'une flotte (fleet-engineering détient les patterns de coordination opérationnels) "
             "ni pour la création d'un skill (fabrique skill-creator/agent-creator) — n°56 route "
             "ces requêtes vers ces détenteurs.")

CALIBRATION_V110 = (
    "- **Dernière calibration** : v1.1.0 (Task 86, 2026-11-09, session web-ecef7f80, "
    "directive 1a1bed51ccaf78f1 cadence 2 h tick 17:50 — extinction pendance baseline A2 n°56 R3) : "
    "**baseline A2 MESURÉE puis Description Optimization A10/A14 appliquée** — mesure initiale 5/7 "
    "(voie mécanique + confirm 3 runs LLM au QUOTA_OK, 21/21 votes réels, nulls 0) : dérive détectée "
    "sur les 2 contrôles négatifs [cas 6 flotte = faux positif 2 voies (M structurel + L 3/3 OUI) · "
    "cas 7 fabrique = faux positif voie L (3/3 OUI)] ; protocole A10/A14 (précédents Task 18 "
    "memory-engineering / Task 25 version-management) : clause d'exclusion discriminante en "
    "description frontmatter [M-safe prouvée par simulation préalable du stemmer arbitre V6 — hits "
    "cas 7 inchangés ['ecosystem'], positifs 1-5 inconstructibles ; ancres count==1, all-or-nothing, "
    "idempotence NO-OP ×2, +325 o] — re-mesure post-optimisation **6/7** (21/21 votes réels, "
    "nulls 0) : cas 6 et 7 voie L corrigés NON×3 (routeur réel : flotte → fleet-engineering, "
    "création → skill-creator), cas 7 conforme sur les 2 voies ; **écart structurel consigné cas 6 "
    "voie M** (radical « agent » ∈ strong du nom — règle arbitre V6 « hits ≥ 2 ou hits ∩ strong » : "
    "toute requête contenant « agent(s) » déclenche M, contrôle négatif voisin du nom inévitable — "
    "posture écart assumé Tasks 81/82/85) ; version 1.0.0 → 1.1.0 ; "
)


def sha256_fichier(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    # ── 1. KB ──
    kb = KB.read_text(encoding="utf-8")
    sha_kb_avant = sha256_fichier(KB)
    if "## agent-engineering v1.1.0" in kb:
        print("NO-OP KB : v1.1.0 déjà scellée (idempotent)")
    else:
        assert kb.count("## agent-engineering v1.0.0") == 1
        assert kb.count("fondements 2026. Spécialise la discipline agent engineering (registre décentralisé") == 1
        assert kb.count("- **Dernière calibration** : v1.0.0 (Task 83,") == 1
        kb2 = kb.replace("## agent-engineering v1.0.0", "## agent-engineering v1.1.0")
        kb2 = kb2.replace(
            "fondements 2026. Spécialise la discipline agent engineering (registre décentralisé",
            "fondements 2026. " + CLAUSE_KB + " Spécialise la discipline agent engineering (registre décentralisé")
        kb2 = kb2.replace("- **Dernière calibration** : v1.0.0 (Task 83,", CALIBRATION_V110 + "v1.0.0 (Task 83,")
        assert kb2.count("## agent-engineering v1.1.0") == 1
        assert kb2.count(CLAUSE_KB) == 1
        KB.write_text(kb2, encoding="utf-8")
        print(f"KB re-sealée : v1.1.0 (SHA {sha_kb_avant[:8]}… → {sha256_fichier(KB)[:8]}…)")

    # ── 2. evals.json note ──
    ev = json.loads(EVALS.read_text(encoding="utf-8"))
    if "MESURÉE" in ev.get("note", ""):
        print("NO-OP evals : note déjà à jour (idempotent)")
    else:
        ancienne = "baseline A2 en attente de mesure (KO-L001 — aucune baseline pré-écrite, R3)."
        nouvelle = ("baseline A2 MESURÉE (Task 86 — voie mécanique + confirm 3 runs LLM au QUOTA_OK, "
                    "21/21 votes réels, R3) puis Description Optimization A10/A14 (re-mesure post-opt "
                    "6/7 ; écart structurel consigné cas 6 voie M : radical « agent » ∈ strong arbitre V6).")
        assert ev["note"].endswith(ancienne), "ancre note evals introuvable"
        ev["note"] = ev["note"][:-len(ancienne)] + nouvelle
        EVALS.write_text(json.dumps(ev, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"evals.json note re-sealée (SHA {sha256_fichier(EVALS)[:8]}…)")

    # ── 3. lignage ──
    lg = LIGNAGE.read_text(encoding="utf-8")
    if "## v1.1.0" in lg:
        print("NO-OP lignage : v1.1.0 déjà consignée (idempotent)")
    else:
        entree = """
## v1.1.0 (2026-11-09, Task 86, session web-ecef7f80, directive 1a1bed51ccaf78f1 cadence 2 h tick 17:50)

- **Baseline A2 MESURÉE puis Description Optimization A10/A14** (extinction pendance R3) : mesure initiale 5/7 (voie mécanique + confirm 3 runs LLM au QUOTA_OK — 21/21 votes réels, nulls 0 ; harnais `scripts/task21-baseline-a2-all.py --skills=agent-engineering`) ; dérive : cas 6 [contrôle négatif fleet-engineering] faux positif 2 voies + cas 7 [contrôle négatif skill-creator/agent-creator] faux positif voie L.
- **Optimisation A10/A14** : clause « Contrôles négatifs assumés » en description frontmatter (route vers fleet-engineering / fabrique skill-creator-agent-creator) — M-safe prouvée par simulation préalable du stemmer arbitre V6 (hits cas 7 inchangés, positifs 1-5 inconstructibles) ; édition chirurgicale count==1 all-or-nothing, idempotence NO-OP ×2, +325 o (16 346 → 16 671 o) ; SKILL.md SHA 1e043b4f… → 5c65a8a7….
- **Re-mesure post-optimisation : 6/7** (21/21 votes réels, nulls 0) : cas 6/7 voie L corrigés NON×3 ; cas 7 conforme 2 voies ; **écart structurel consigné cas 6 voie M** (radical « agent » ∈ strong — limite arbitre V6, posture Tasks 81/82/85).
- **Cascade KO-L004** : KB v1.1.0 (en-tête + Description miroir + Dernière calibration) + evals.json note + présent fichier ; ULTRA regen ×2 (table versions, KO-L003 dérivation dynamique) ; SHARED §7 no-op (KO-L003 sans version figée) ; gen-plan §1.6 no-op (plancher >= v1.0.0 conforme).
"""
        LIGNAGE.write_text(lg.rstrip("\n") + "\n" + entree, encoding="utf-8")
        print(f"lignage v1.1.0 consigné (SHA {sha256_fichier(LIGNAGE)[:8]}…)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
