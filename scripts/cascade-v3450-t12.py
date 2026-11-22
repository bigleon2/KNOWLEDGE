#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cascade KO-L004 v3.45.0 — étapes mécaniques (Task ID 12, directive 1a1faad3d26c524d).

(1) Dédup N27 : PM gen-plan v3.44.0 du corpus @mon-ecosysteme/ déplacé (R4, move) vers
    @historique/prompts-maitres/gen-plan/ — le corpus ne porte que la dernière version.
(2) Recalibrage croisé — citations vives : « gen-plan v3.44.0 » → « gen-plan v3.45.0 »
    dans les 9 SKILL.md vivants (5 disciplines + 4 skills).
(3) Propagation §0 : « SHARED v1.7.42 » → « SHARED v1.7.43 » dans les 54 SKILL.md vivants.
Assertions strictes : 1 occurrence exacte par fichier et par motif — abandon sans écriture
si un compte diverge (garde KO-L003, jamais de remplacement silencieux multiple).
Idempotence ×2 : re-jeu → assertion « déjà effectuée » (le PM source n'existe plus).
"""

# ⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.45)
# SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
# Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
# Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
# Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
# Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
# Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).

import json
import shutil
from pathlib import Path

BASE = Path("/home/z/my-project")
CORPUS = BASE / "skills/@mon-ecosysteme"
ARCHIVE = BASE / "skills/@historique/prompts-maitres/gen-plan"

PM_ANCIEN = CORPUS / "PROMPT-MAITRE-GEN-PLAN-v3.44.0.md"

CITATIONS = [
    "skills/refactoring-engineering/SKILL.md",
    "skills/refactoring-test/SKILL.md",
    "skills/memory-engineering/SKILL.md",
    "skills/spec-driven-development/SKILL.md",
    "skills/loop-engineering/SKILL.md",
    "skills/graph-engineering/SKILL.md",
    "skills/context-engineering/SKILL.md",
    "skills/harness-engineering/SKILL.md",
    "skills/fleet-engineering/SKILL.md",
]

def remplacer(path: Path, motif: str, nouveau: str) -> int:
    s = path.read_text(encoding="utf-8")
    n = s.count(motif)
    assert n == 1, "%s : %d occurrence(s) de %r (attendu 1)" % (path, n, motif)
    path.write_text(s.replace(motif, nouveau, 1), encoding="utf-8")
    return n

def main() -> int:
    bilan = {}
    # (1) dédup N27 — R4 move
    if PM_ANCIEN.exists():
        assert ARCHIVE.is_dir(), "archive prompts-maitres/gen-plan/ absente"
        assert not (ARCHIVE / PM_ANCIEN.name).exists(), "cible d'archivage déjà présente"
        shutil.move(str(PM_ANCIEN), str(ARCHIVE / PM_ANCIEN.name))
        bilan["dedup_n27"] = PM_ANCIEN.name
    else:
        assert (ARCHIVE / PM_ANCIEN.name).exists(), "ni corpus ni archive : état incohérent"
        bilan["dedup_n27"] = "DEJA (idempotence ×2)"
    # (2) citations vives
    cites = []
    for rel in CITATIONS:
        remplacer(BASE / rel, "gen-plan v3.44.0", "gen-plan v3.45.0")
        cites.append(rel)
    bilan["citations_v3450"] = cites
    # (3) propagation §0 (54 en-têtes vivants, dérivation dynamique KO-L003)
    têtes = []
    for p in sorted((BASE / "skills").glob("*/SKILL.md")):
        if "@historique" in str(p) or "@mon-ecosysteme" in str(p):
            continue
        s = p.read_text(encoding="utf-8")
        if "SHARED v1.7.42" in s:
            remplacer(p, "SHARED v1.7.42", "SHARED v1.7.43")
            têtes.append(str(p.relative_to(BASE)))
    bilan["propagation_shared_v1743"] = len(têtes)
    bilan["propagation_fichiers"] = têtes
    print(json.dumps(bilan, ensure_ascii=False, indent=2)[:2000])
    print("OK : dédup %s · %d citations recalibrées · %d en-têtes §0 propagés"
          % (bilan["dedup_n27"], len(cites), len(têtes)))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
