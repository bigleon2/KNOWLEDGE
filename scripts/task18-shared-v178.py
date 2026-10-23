#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.10)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.

task18-shared-v178.py — Complétion SHARED v1.7.8 (Task 18, session web-fdf5963c) :
la ligne de révision auto-écrite par generer-pm-skill.py est étendue (PM-INSTALL
v1.8.0 — mécanisme dual + alias-eco) et la ligne §6.1 PM-INSTALL est portée à v1.8.0.
Discipline sub_locked (ABANDON sans écriture).
"""
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHARED = os.path.join(BASE, "skills", "@mon-ecosysteme", "PROMPT-MAITRE-SHARED.md")


def sub_locked(text, motif, remplace, n, label):
    c = text.count(motif)
    if c != n:
        print("ABANDON : motif [%s] trouvé %d fois (attendu %d)" % (label, c, n))
        sys.exit(2)
    return text.replace(motif, remplace)


def main():
    t = open(SHARED, encoding="utf-8").read()

    # 1. Extension de la ligne de révision v1.7.8 (auto-écrite par generer-pm-skill.py)
    t = sub_locked(t,
        "— **v1.7.8** : §6.1 — référence(s) PM portée(s) à la/les version(s) générée(s) mécaniquement (`scripts/generer-pm-skill.py` — substitutions verrouillées, recalibrage inclus). 2026-10-12 (Task 12",
        "— **v1.7.8** : §6.1 — référence(s) PM portée(s) à la/les version(s) générée(s) mécaniquement (`scripts/generer-pm-skill.py` — substitutions verrouillées, recalibrage inclus). Complétion même jour (Task 18, session web-fdf5963c — directive propriétaire « optimise le système d'installation en regénérant » + skill alias-eco) : §6.1 — référence PM-INSTALL portée à v1.8.0 (MÉCANISME DUAL d'installation — installation directe des formes certifiées du dépôt par défaut + assemblage bootstrap corpus-seul ; intégration alias-eco au périmètre §2bis/§4/§A.3) ; les 4 PMs familles (v3.23.2/v2.8.0/v2.0.2/v1.7.1) portent la note §5 mécanisme dual. 2026-10-12 (Task 12",
        1, "révision v1.7.8")

    # 2. Ligne §6.1 PM-INSTALL — version cell + parenthétique étendue
    t = sub_locked(t,
        "cascade KO-L004), v1.7.1) | v1.7.1 |",
        "cascade KO-L004), v1.7.1 ; mécanisme dual d'installation — installation directe des formes certifiées par défaut (exécutant canonique eco_install_pipeline.py) + assemblage bootstrap, périmètre += alias-eco, v1.8.0) | v1.8.0 |",
        1, "§6.1 PM-INSTALL v1.8.0")

    with open(SHARED, "w", encoding="utf-8") as f:
        f.write(t)
    print("SHARED v1.7.8 complété — 2 substitutions verrouillées")
    return 0


if __name__ == "__main__":
    sys.exit(main())
