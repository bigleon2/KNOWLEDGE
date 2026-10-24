#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.13)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.

task18-kb.py — Mise à jour du registre KB (Task 18, session web-fdf5963c) :
entrée alias-eco v1.0.0 (template SHARED §2.2, bidirectionnalité correct-work),
montées de version 4 familles, réciproque correct-work → alias-eco, décision
d'architecture Task 18. Discipline sub_locked (ABANDON sans écriture).
"""
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KB = os.path.join(BASE, "skills", "KNOWLEDGE.md")


def sub_locked(text, motif, remplace, n, label):
    c = text.count(motif)
    if c != n:
        print("ABANDON : motif [%s] trouvé %d fois (attendu %d)" % (label, c, n))
        sys.exit(2)
    return text.replace(motif, remplace)


ALIAS_ECO_ENTRY = """## alias-eco v1.0.0

- **Category** : ecosystem
- **Description** : Gestionnaire du système d'alias $<ALIAS> de l'écosystème Knowledge — remplace les grandes phrases récurrentes des discussions par des alias (ex : « mon écosystème personnel » → $ECO-LEON : « de $ECO-LEON » se lit « de mon écosystème personnel »). Trois déclencheurs : « alias-eco » (gestion : lister, synchroniser, ajouter, résoudre), « liste mes alias » (affichage du registre), « alias-eco (chat) » (liste TXT des phrases récurrentes de la discussion, triée par ordre alphabétique). Le registre JSON (phrases récurrentes triées alphabétiquement, aucun doublon strictement identique — détection n-grammes maximaux ≥ 3 occurrences, virgule intra-phrase, jamais à cheval sur 2 phrases) est sauvegardé dans `@historique/@Alias/aliases.json` ; résolution à la lecture : tout $<ALIAS> d'un message propriétaire est expansé avant interprétation ; l'alias n'est jamais inventé par la détection (attribution explicite traçable). Gestionnaire mécanique `scripts/alias-manager.py` (--selftest 15/15, --scan, --chat, --list, --add, --resolve) ; `references/format-alias.md` (conventions du format et du registre) ; evals 6 cas + trigger_evals 8 cas (5 positifs / 3 négatifs).
- **Dépend de** : —
- **Utilisé par** : correct-work (mode PROJET — tenue du registre des phrases récurrentes lors de l'analyse des discussions, délégation §10.1 Phase 2, v2.8.0)
- **Dernière calibration** : création v1.0.0 (2026-10-23, Task 18, session web-fdf5963c — directive propriétaire « remplacer les phrases récurrentes par les alias $<ALIAS> ») : amorçage ECO-LEON = « mon écosystème personnel » (exemple canonique propriétaire) + 6 phrases récurrentes détectées de la discussion ; selftest 15/15 (détection, tri, déduplication, résolution, garde format, mode chat TXT trié)
- **Statut** : stable

"""

DECISION = """**Task 18 (2026-10-23) — optimisation du système d'installation + skill alias-eco (directive propriétaire, session web-fdf5963c)** :
- **Mécanisme dual d'installation (PM-INSTALL v1.8.0 §3.2)** : l'installation DIRECTE des formes certifiées du dépôt (clone git règle d'or n°4, garde R2, arbitres — exécutant canonique `scripts/eco_install_pipeline.py`, chemin REPO paramétrable, pin descendant-tolérant) devient la voie PAR DÉFAUT ; l'assemblage depuis les PMs demeure la voie BOOTSTRAP (corpus/archive seul) — les §5 des 4 PMs familles (régénérés mécaniquement KO-L004 : gen-plan v3.23.2, correct-work v2.8.0, clone-chat v2.0.2, refactor-guard v1.7.1 — note §5 mécanisme dual, complétion agent 13 substitutions verrouillées) restent la SPÉCIFICATION de la forme installée. Justification (réponse au prérequis A « assemble au lieu d'installer ») : l'assemblage garantissait l'unique source (R4), l'authenticité (archive scellée) et la portabilité (le corpus suffit à reconstruire) ; depuis KO-L004 v1.1.0 la génération est SKILL.md → PM (le PM est dérivé mécaniquement) et le dépôt porte les formes certifiées par les arbitres — la copie directe est devenue la voie la plus judicieuse quand le dépôt est disponible, les deux voies produisant des formes byte-identiques.
- **Système d'alias $<ALIAS>** : skill alias-eco v1.0.0 (déclencheurs « alias-eco », « liste mes alias », « alias-eco (chat) » — liste TXT triée alphabétique) ; registre JSON `@historique/@Alias/aliases.json` (trié, dédupliqué strict) ; délégation correct-work v2.8.0 mode PROJET (§10.1 Phase 2) ; résolution à la lecture avant interprétation ; l'alias est un raccourci d'ENTRÉE, jamais une transformation des livrables.

"""


def main():
    t = open(KB, encoding="utf-8").read()

    # 1. Entrée alias-eco — insérée avant les Décisions d'architecture
    t = sub_locked(t, "## Décisions d'architecture (corrige-ecosysteme v2.0.0)",
                   ALIAS_ECO_ENTRY + "## Décisions d'architecture (corrige-ecosysteme v2.0.0)",
                   1, "insertion alias-eco")

    # 2. Décision Task 18 — en tête de la section Décisions
    t = sub_locked(t,
                   "## Décisions d'architecture (corrige-ecosysteme v2.0.0)\n\n**Task 23 (2026-10-03)",
                   "## Décisions d'architecture (corrige-ecosysteme v2.0.0)\n\n" + DECISION + "**Task 23 (2026-10-03)",
                   1, "décision Task 18")

    # 3. Montées de version — headings
    t = sub_locked(t, "## gen-plan v3.23.1", "## gen-plan v3.23.2", 1, "heading gen-plan")
    t = sub_locked(t, "## correct-work v2.7.0", "## correct-work v2.8.0", 1, "heading correct-work")
    t = sub_locked(t, "## clone-chat v2.0.1", "## clone-chat v2.0.2", 1, "heading clone-chat")
    t = sub_locked(t, "## refactor-guard v1.7.0", "## refactor-guard v1.7.1", 1, "heading refactor-guard")

    # 4. Lignes de calibration — préparation des montées
    t = sub_locked(t,
                   "**Dernière calibration** : montée v3.23.1 (2026-10-12, Task 8",
                   "**Dernière calibration** : montée v3.23.2 (2026-10-23, Task 18 — session web-fdf5963c : PATCH documentation — note §5 mécanisme dual [installation directe des formes certifiées par défaut, PM-INSTALL v1.8.0 §3.2] ; PM v3.23.2 généré mécaniquement KO-L004, complétion agent) ; montée v3.23.1 (2026-10-12, Task 8",
                   1, "calibration gen-plan")
    # 4b. correct-work : calibration unique — édition bornée à la section correct-work
    # (la ligne Task 21 F1 est partagée par 3 entrées : correct-work, prompt-engineering, script-creator)
    start = t.index("## correct-work v2.8.0")
    end = t.index("\n## ", start + 10)
    section = t[start:end]
    section = sub_locked(section,
                         "- **Dernière calibration : 2026-10-03 (Task 21 F1",
                         "- **Dernière calibration : 2026-10-23 (Task 18 — session web-fdf5963c : MINOR v2.8.0 — intégration alias-eco [délégation mode PROJET §10.1 Phase 2, registre @historique/@Alias/, dependencies += alias-eco >= v1.0.0] + note §5 mécanisme dual [PM-INSTALL v1.8.0 §3.2] ; PM v2.8.0 généré mécaniquement KO-L004, complétion agent 5 substitutions verrouillées)**\n- **Dernière calibration (historique)** : 2026-10-03 (Task 21 F1",
                         1, "calibration correct-work (bornée)")
    t = t[:start] + section + t[end:]
    # 4c. clone-chat : calibration partagée (clone-chat + refactoring-engineering + refactoring-test) — édition bornée
    start = t.index("## clone-chat v2.0.2")
    end = t.index("\n## ", start + 10)
    section = t[start:end]
    section = sub_locked(section,
                         "**Dernière calibration** : Task 12 (2026-10-12, session web-b4d7dd19 — gen-plan(step), directive propriétaire « appliquer les corrections »)",
                         "**Dernière calibration** : Task 18 (2026-10-23, session web-fdf5963c : PATCH v2.0.2 — note §5 mécanisme dual [installation directe des formes certifiées par défaut, PM-INSTALL v1.8.0 §3.2] ; PM v2.0.2 généré mécaniquement KO-L004, complétion agent) ; Task 12 (2026-10-12, session web-b4d7dd19 — gen-plan(step), directive propriétaire « appliquer les corrections »)",
                         1, "calibration clone-chat (bornée)")
    t = t[:start] + section + t[end:]
    # 4d. refactor-guard : calibration partagée (refactor-guard + fullstack-dev) — édition bornée
    start = t.index("## refactor-guard v1.7.1")
    end = t.index("\n## ", start + 10)
    section = t[start:end]
    section = sub_locked(section,
                         "**Dernière calibration** : Task 8 (2026-10-12, session web-b4d7dd19 — gen-plan(step), fusion discussion 468a4c26)",
                         "**Dernière calibration** : Task 18 (2026-10-23, session web-fdf5963c : PATCH v1.7.1 — note §5 mécanisme dual [ce §5 prescrit déjà l'installation directe par copie — cohérence explicite avec PM-INSTALL v1.8.0 §3.2] ; PM v1.7.1 généré mécaniquement KO-L004, complétion agent) ; Task 8 (2026-10-12, session web-b4d7dd19 — gen-plan(step), fusion discussion 468a4c26)",
                         1, "calibration refactor-guard (bornée)")
    t = t[:start] + section + t[end:]

    # 5. correct-work — description + Dépend de += alias-eco (réciproque de l'entrée alias-eco)
    t = sub_locked(t,
                   "intégration KB (Registre, kb_path, --kb-skill), matrice de décision agent/skill (statique + dynamique KB), métriques de performance. Contrôler la cohérence avant de livrer",
                   "intégration KB (Registre, kb_path, --kb-skill), délégation alias-eco (mode PROJET — tenue du registre des phrases récurrentes @historique/@Alias/, v2.8.0), matrice de décision agent/skill (statique + dynamique KB), métriques de performance. Contrôler la cohérence avant de livrer",
                   1, "description correct-work")
    t = sub_locked(t,
                   "fullstack-dev >= v1.0.0 (projets web), skills-inventory >= v1.0.0 (scan dynamique KB)",
                   "fullstack-dev >= v1.0.0 (projets web), skills-inventory >= v1.0.0 (scan dynamique KB), alias-eco >= v1.0.0 (mode PROJET — tenue du registre des phrases récurrentes, v2.8.0)",
                   1, "Dépend de correct-work")

    with open(KB, "w", encoding="utf-8") as f:
        f.write(t)
    print("KB mis à jour — 12 substitutions verrouillées (entrée alias-eco + 4 montées + décision + réciproques)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
