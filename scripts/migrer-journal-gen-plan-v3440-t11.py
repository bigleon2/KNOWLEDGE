#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Migration R4 byte-identité + montée v3.44.0 — gen-plan (Task ID 11, KO-L004/KO-L005).

(1) Extrait l'entrée courante v3.43.0 du §5.6 (SKILL.md gen-plan) SANS la réécrire
    et l'insère en tête de references/journal-versions.md (migration R4 byte-identité).
(2) Remplace l'entrée inline par l'entrée v3.44.0 (Task ID 11, directive 1a1fa816474a35ad
    — REAPPLICATION de la montée Task ID 10 perdue au recyclage du bac à sable).
Idempotence : re-jeu sans effet (l'entrée v3.43.0 n'est plus au §5.6 → assertion).
"""

# ⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.46)
# SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
# Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
# Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
# Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
# Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
# Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).

from pathlib import Path

SKILL = Path("/home/z/my-project/skills/gen-plan/SKILL.md")
JOURNAL = Path("/home/z/my-project/skills/gen-plan/references/journal-versions.md")

ANCIENNE = "- **v3.43.0 (2026-11-15, web-ecef7f80 — Task 92,"
MARQUEUR_JOURNAL = "- **v3.42.0 (2026-11-09,"

ENTREE_V3440 = '''- **v3.44.0 (2026-11-20, web-93a4f011 — Task ID 11, directive 1a1fa816474a35ad « analyse et teste mon skill "gen-plan" dans l'objectif de l'optimiser » [REAPPLICATION de la montée Task ID 10 — perdue au recyclage du bac à sable, jamais poussée au dépôt])** : **chaîne de vérification par étape terminée en mode NULL** — §5.4 étendu (titre + extension : granularité ÉTAPE, `correct-work(livrables de l'étape, mode=CIBLE)` AVANT l'étape suivante, statut `verified` subordonné au verdict CIBLE — KO-L003) + clause §A NULL + §1.5 Modes + description + dependencies used_at. MINOR, triggers inchangés (non-régression). Cascade KO-L004 COMPLÈTE (pipeline du dépôt présent — pendances Task ID 10 éteintes) : PM v3.44.0 généré mécaniquement (generer-pm-skill.py) + delta verrouillé + KB + @historique + pin ECO_SKILLS recalibré + certification locale ; v3.43.0 migré R4 byte-identité vers references/journal-versions.md (scripts/migrer-journal-gen-plan-v3440-t11.py — idempotent).'''


def main() -> int:
    s = SKILL.read_text(encoding="utf-8")
    lines = s.split("\n")
    idx = [i for i, ligne in enumerate(lines) if ligne.startswith(ANCIENNE)]
    assert len(idx) == 1, "entrée v3.43.0 non unique au §5.6 : %r" % (idx,)
    ancienne = lines[idx[0]]
    journal = JOURNAL.read_text(encoding="utf-8")
    assert journal.count(MARQUEUR_JOURNAL) == 1, "marqueur v3.42.0 non unique au journal"
    assert ancienne not in journal, "migration déjà effectuée (idempotence ×2)"
    journal2 = journal.replace(MARQUEUR_JOURNAL, ancienne + "\n\n" + MARQUEUR_JOURNAL, 1)
    JOURNAL.write_text(journal2, encoding="utf-8")
    lines[idx[0]] = ENTREE_V3440
    SKILL.write_text("\n".join(lines), encoding="utf-8")
    print("OK : v3.43.0 (%d caractères) migrée vers journal-versions.md ; v3.44.0 inline au §5.6."
          % len(ancienne))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
