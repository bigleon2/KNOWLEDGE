#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix KB — déplace l'entrée rea-analysis mal insérée (entre le heading inter-scripts
et son corps) vers sa position correcte : après l'entrée inter-scripts complète,
avant « ## resume-youtube v1.1.0 ». Idempotent : no-op si déjà en place."""

# ⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.47)
# SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
# Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
# Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
# Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
# Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
# Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).

from pathlib import Path

KB = Path("/home/z/my-project/skills/KNOWLEDGE.md")
DEBUT = "## rea-analysis v1.0.0"
FIN_ORPHELIN = "- **Category** : ecosystem\n- **Description** : Orchestre"
CIBLE = "## resume-youtube v1.1.0"


def main() -> int:
    s = KB.read_text(encoding="utf-8")
    if DEBUT in s and s.find(DEBUT) < s.find(FIN_ORPHELIN) < s.find(CIBLE):
        # Bloc mal placé : entre le heading inter-scripts et son corps orphelin.
        i = s.find(DEBUT)
        j = s.find(FIN_ORPHELIN)
        bloc = s[i:j]
        s = s.replace("## inter-scripts v1.0.0\n\n" + bloc, "## inter-scripts v1.0.0\n\n", 1)
        s = s.replace(CIBLE, bloc.rstrip() + "\n\n" + CIBLE, 1)
        KB.write_text(s, encoding="utf-8")
        print("OK : bloc rea-analysis déplacé avant « %s » (%d caractères)" % (CIBLE, len(bloc)))
        return 0
    print("NO-OP : bloc déjà en place (ou structure inattendue — inspecter)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
