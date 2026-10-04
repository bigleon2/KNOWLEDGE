#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""task39 — GÉNÉRATION des PROMPT-MAITRE-GEN-PLAN v3.19.0 et v3.20.0 manquants.

Méthode fidèle au protocole écosystème : montée incrémentale depuis le dernier PM
existant (v3.18.0), par substitutions verrouillées (chaque motif doit apparaître
exactement n fois, sinon ABANDON sans écriture).

Deltas v3.19.0 (Task 23, 2026-10-03) :
  - §1.16 routage de découverte des skills + garde É1-INSTALL (D006, --check/--reinstall)
  - §3 relations : skills-inventory promu routage prioritaire (>=1.1.0) + ajout skill-finder-cn
  - §4 YAML version 3.19.0 ; §7 ligne d'historique

Deltas v3.20.0 (Task 29, 2026-10-04) :
  - §1.16 garde fusionnée : script maître INTÉGRÉ au skill, mode --preempt (D002),
    directive plan-post-reinstall-<ts>.json (D004), préemption comportement AGENT (D003)
  - §4 YAML version 3.20.0 ; §7 ligne d'historique

Déploiement ×3 (convention établie) : ecosystem/skills/@mon-ecosysteme/,
chat-assets/, archive-extract/@mon-ecosysteme/.
Sortie : 6 fichiers + résumé console.
"""
import os
import sys

BASE = "/home/z/my-project"
SRC = os.path.join(BASE, "ecosystem/skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.18.0.md")
DESTS = [
    os.path.join(BASE, "ecosystem/skills/@mon-ecosysteme"),
    os.path.join(BASE, "chat-assets"),
    os.path.join(BASE, "archive-extract/@mon-ecosysteme"),
]

TXT = open(SRC, encoding="utf-8").read()

SEC1_16_V319 = """### §1.16 Routage de découverte des skills + garde d'installation (v3.19.0, Task 23)

**É1-INSTALL — garde d'installation (décision D006, Task 23)** : à l'ouverture de session, AVANT E1, exécuter `python3 scripts/ensure-installed.py --check`. rc=0 : écosystème installé (no-op — jamais de réinstallation d'un état à jour). rc≠0 : écosystème absent ou dérivé → **PRÉEMPTION** : l'agent SUSPEND toute tâche, y compris celles en cours d'exécution, et exécute `python3 scripts/ensure-installed.py --reinstall` (pipeline PM-INSTALL §2/§2bis ; clone éphémère SANS persistance de jeton — anti-persistance Task 8/14) AVANT toute autre étape. La garde est idempotente (f(f(x))=f(x)).

**Routage de découverte (décision D004)** — quand gen-plan doit trouver, sélectionner ou inventorier des skills (E5, §3) :

1. **skills-inventory en PRIORITÉ** : scanner `{{SKILLS_ROOT}}` via son script (`generate_skills_md.py --json` / `--search` / `--category`). Les performances des éléments trouvés sont comparées aux éléments natifs (couverture, fraîcheur, pertinence des métadonnées) et la comparaison est MÉMORISÉE au registre KB (section Décisions d'architecture) — la mémoire évite de re-comparer à chaque session et alimente le choix du routeur.
2. **skill-finder-cn en FALLBACK** : UNIQUEMENT si skills-inventory échoue (script absent, arbre vide, erreur d'exécution). Tout élément trouvé par le fallback passe un **contrôle cybersécurité `audit-provenance`** (provenance, permissions, contenu dangereux) AVANT adoption ; un échec du contrôle disqualifie l'élément et est consigné au KB. La bascule est unidirectionnelle au cours d'une même recherche : pas de retour à skills-inventory après activation du fallback.

---

"""

SEC1_16_V320 = """### §1.16 Routage de découverte des skills + garde d'installation (v3.20.0, Task 23 + Task 29)

**É1-INSTALL — garde d'installation avec PRÉEMPTION (décision D006 Task 23 + D001-D004 Task 29)** : à l'ouverture de session, AVANT E1, et EN PREMIER (préemption), exécuter `python3 skills/gen-plan/scripts/ensure-installed.py --check` (chemin canonique — le script maître est INTÉGRÉ au skill ; le fichier racine `scripts/ensure-installed.py` est un shim de compatibilité qui délègue). rc=0 : écosystème installé (no-op, jamais de réinstallation d'un état à jour). rc≠0 : écosystème absent ou dérivé → **PRÉEMPTION** : l'agent SUSPEND toute tâche, y compris celles en cours d'exécution, et exécute `python3 skills/gen-plan/scripts/ensure-installed.py --reinstall` (pipeline PM-INSTALL §2/§2bis ; clone éphémère SANS persistance de jeton — anti-persistance Task 8/14) AVANT toute autre étape. Le mode `--preempt` concentre la décision : INSTALLE → PRIORITE-NONE (rc 0) ; ROOT absent → réinstallation IMMÉDIATE (PRIORITE-REINSTALL-OK) ; dérivé → PRIORITE-REINSTALL-REQUISE (rc 2, aucune action destructive). Après une réinstallation réussie, le script génère une **directive de mise à jour du plan d'actions en cours** (`download/plan-post-reinstall-<ts>.json`) : l'agent l'intègre au plan de façon COHÉRENTE et OPTIMISÉE (étapes interrompues → statut INTERRUPT-REINSTALL, étapes idempotentes KO-L001 reprennent en l'état, re-validation par arbitres E7/E8 avant reprise), puis journalise au worklog. La garde est idempotente (f(f(x))=f(x)).

**Routage de découverte (décision D004)** — quand gen-plan doit trouver, sélectionner ou inventorier des skills (E5, §3) :

1. **skills-inventory en PRIORITÉ** : scanner `{{SKILLS_ROOT}}` via son script (`generate_skills_md.py --json` / `--search` / `--category`). Les performances des éléments trouvés sont comparées aux éléments natifs (couverture, fraîcheur, pertinence des métadonnées) et la comparaison est MÉMORISÉE au registre KB (section Décisions d'architecture) — la mémoire évite de re-comparer à chaque session et alimente le choix du routeur.
2. **skill-finder-cn en FALLBACK** : UNIQUEMENT si skills-inventory échoue (script absent, arbre vide, erreur d'exécution). Tout élément trouvé par le fallback passe un **contrôle cybersécurité `audit-provenance`** (provenance, permissions, contenu dangereux) AVANT adoption ; un échec du contrôle disqualifie l'élément et est consigné au KB. La bascule est unidirectionnelle au cours d'une même recherche : pas de retour à skills-inventory après activation du fallback.

---

"""

LIGNE_V319 = ("| v3.19.0 | 2026-10-03 | Task 23 — routage de découverte des skills (D004) : skills-inventory "
              "PRIORITAIRE à E5/§3 (comparaison des éléments trouvés vs natifs MÉMORISÉE au registre KB), "
              "fallback skill-finder-cn avec contrôle cybersécurité audit-provenance AVANT adoption, bascule "
              "unidirectionnelle ; garde É1-INSTALL (D006) : `scripts/ensure-installed.py --check` à l'ouverture "
              "de session, préemption (suspension de toute tâche en cours) puis `--reinstall` via pipeline "
              "PM-INSTALL §2/§2bis sans persistance de jeton (anti-persistance Task 8/14) ; §3 relations "
              "(skills-inventory >=1.1.0, ajout skill-finder-cn) ; francisation D007 (skill-creator 1.1.0, "
              "version-management 1.1.0) ; recalibrage KO-L004 |")

LIGNE_V320 = ("| v3.20.0 | 2026-10-04 | Task 29 — intégration de la garde É1-INSTALL au skill (D001 : script "
              "maître `skills/gen-plan/scripts/ensure-installed.py`, le fichier racine `scripts/ensure-installed.py` "
              "devient un shim délégant) ; mode `--preempt` (D002 : INSTALLE→PRIORITE-NONE rc 0, ROOT absent→"
              "réinstallation IMMÉDIATE PRIORITE-REINSTALL-OK, dérivé→PRIORITE-REINSTALL-REQUISE rc 2 non "
              "destructif — doctrine Task 23 conservée) ; PRÉEMPTION prescrite au §1.16 comme comportement AGENT "
              "(D003 : suspendre toute tâche, réinstaller, puis mettre à jour le plan) ; après réinstallation "
              "réussie, génération automatique d'une directive de mise à jour du plan en cours "
              "`download/plan-post-reinstall-<ts>.json` (D004 : étapes interrompues → INTERRUPT-REINSTALL, "
              "étapes idempotentes KO-L001 reprennent en l'état, re-validation arbitres E7/E8 avant reprise) ; "
              "bump 3.19.0→3.20.0 (D005, description inchangée) ; réinstallation exécutée via la garde = no-op "
              "idempotent honnête (D007-D008 : 0 modification, audit stable 74 CONFORME / 20 PARTIEL) |")


def sub1(text, motif, remplace, n=1):
    """Substitution verrouillée : le motif doit apparaître exactement n fois."""
    c = text.count(motif)
    if c != n:
        print("ABANDON : motif trouvé %d fois (attendu %d) : %s" % (c, n, motif[:80]))
        sys.exit(1)
    return text.replace(motif, remplace)


# ═══════════════ v3.19.0 (deltas Task 23) ═══════════════
v319 = TXT
v319 = sub1(v319, "# PROMPT MAÎTRE — Installation du skill gen-plan v3.18.0",
            "# PROMPT MAÎTRE — Installation du skill gen-plan v3.19.0")
v319 = sub1(v319, "> **Version du prompt** : 1.9.0", "> **Version du prompt** : 1.10.0")
v319 = sub1(v319, "> **Skill cible** : gen-plan v3.18.0", "> **Skill cible** : gen-plan v3.19.0")
v319 = sub1(v319, "> **Date** : 2026-10-02", "> **Date** : 2026-10-03")
v319 = sub1(v319, "\n## §2 — SPÉCIFICATION TECHNIQUE",
            "\n---\n\n" + SEC1_16_V319 + "## §2 — SPÉCIFICATION TECHNIQUE")
v319 = sub1(v319, "| skills-inventory | Consultation à E5 | Sélection des skills, version >= v1.0.0 |",
            "| skills-inventory | Routage prioritaire de découverte (§1.16) + consultation à E5 | "
            "Sélection des skills, version >= v1.1.0 |\n"
            "| skill-finder-cn | Fallback de découverte (§1.16) | Recherche externe UNIQUEMENT si "
            "skills-inventory échoue — contrôle cybersécurité audit-provenance obligatoire avant adoption |")
v319 = sub1(v319, "version: 3.18.0", "version: 3.19.0")
v319 = sub1(v319, "| v3.18.0 | 2026-10-02 |", LIGNE_V319 + "\n| v3.18.0 | 2026-10-02 |")

# ═══════════════ v3.20.0 (deltas Task 29) ═══════════════
v320 = v319
v320 = sub1(v320, "# PROMPT MAÎTRE — Installation du skill gen-plan v3.19.0",
            "# PROMPT MAÎTRE — Installation du skill gen-plan v3.20.0")
v320 = sub1(v320, "> **Version du prompt** : 1.10.0", "> **Version du prompt** : 1.11.0")
v320 = sub1(v320, "> **Skill cible** : gen-plan v3.19.0", "> **Skill cible** : gen-plan v3.20.0")
v320 = sub1(v320, "> **Date** : 2026-10-03", "> **Date** : 2026-10-04")
v320 = sub1(v320, SEC1_16_V319, SEC1_16_V320)
v320 = sub1(v320, "version: 3.19.0", "version: 3.20.0")
v320 = sub1(v320, "| v3.19.0 | 2026-10-03 |", LIGNE_V320 + "\n| v3.19.0 | 2026-10-03 |")

# ═══════════════ écriture ×3 ═══════════════
for d in DESTS:
    if not os.path.isdir(d):
        print("ABANDON : répertoire de déploiement absent : %s" % d)
        sys.exit(1)
    open(os.path.join(d, "PROMPT-MAITRE-GEN-PLAN-v3.19.0.md"), "w", encoding="utf-8").write(v319)
    open(os.path.join(d, "PROMPT-MAITRE-GEN-PLAN-v3.20.0.md"), "w", encoding="utf-8").write(v320)
    print("déployé ×2 fichiers → %s" % d)

print("\nOK : PM v3.19.0 = %d lignes, PM v3.20.0 = %d lignes (base v3.18.0 = %d)"
      % (v319.count("\n"), v320.count("\n"), TXT.count("\n")))
