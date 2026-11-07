#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.31)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).

Task 52 — Cascade gen-plan v3.34.0 → v3.35.0 (règle d'or n°9 : vérification
automatique de l'installation de l'écosystème à toute invocation post-coupure).

Ce script exécute le RECALIBRAGE CROISÉ KO-L004 manuel (le générateur
generer-pm-skill.py a déjà produit le PM v3.35.0 + recalibré SHARED v1.7.23 /
PM-INSTALL v1.9.1 / §2ter / §A.3) :
  1. Registre KB (skills/KNOWLEDGE.md) : en-tête v3.35.0 + description n°9 + calibration ;
  2. Pin ECO_SKILLS (scripts/check-ecosysteme-integrity.py) : gen-plan 3.35.0 + commentaire ;
  3. @historique/historiques-par-skill/gen-plan.md : ligne v3.35.0 VERSION VIVANTE,
     démotion v3.34.0, footer 34→35 fichiers, marqueur périmé v3.26.0 résorbé ;
  4. Lignes vives 9 disciplines (gen-plan v3.34.0 → v3.35.0) ;
  5. README @historique : §1 (35 PMs), §2 (38 versions / 35 archivés / v3.35.0 vivante),
     §5 (47 PMs + sceau v3.34.0 SHA ac9de174…) ;
  6. README corpus : révision v2.1.16 + arborescence GEN-PLAN v3.35.0 ;
  7. RETRAITS_SANCTIONNES (scripts/task21-f2-rebuild-archive.py) += PM v3.34.0.

Substitutions verrouillées (méthode B1) : ABANDON sans écriture si un motif
n'apparaît pas exactement n fois. Idempotent : chaque sub déjà appliquée = no-op.
"""

import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

OPS = []


def p(rel):
    return os.path.join(BASE, rel)


def sub_locked(text, old, new, count, label):
    """Substitution verrouillée : old doit apparaître exactement count fois.
    Idempotence : si new déjà présent → no-op signalé."""
    if new in text:
        OPS.append("%s : DÉJÀ APPLIQUÉ (no-op)" % label)
        return text
    c = text.count(old)
    if c != count:
        print("ABANDON — %s : motif trouvé %d fois (attendu %d)" % (label, c, count))
        sys.exit(2)
    OPS.append("%s : appliqué" % label)
    return text.replace(old, new)


def edit(rel, subs):
    """Applique une liste de subs verrouillées à un fichier."""
    path = p(rel)
    with open(path, encoding="utf-8") as f:
        t = f.read()
    for old, new, count, label in subs:
        t = sub_locked(t, old, new, count, label)
    with open(path, "w", encoding="utf-8") as f:
        f.write(t)


N9_COURT = ("n°9 vérification automatique de l'installation de l'écosystème à toute invocation "
            "post-coupure — piliers (KB + corpus SHARED + forme installée) + arbitre integrity, "
            "rétablissement automatique en 4 temps (lecture intégrale PM SHARED → réinstallation "
            "PM-INSTALL voie directe → certification arbitres → re-génération du plan via le "
            "gen-plan réinstallé), preuve vivante session web-c30e6506 (v3.35.0, Task 52)")

# --- 1. Registre KB ---
edit("skills/KNOWLEDGE.md", [
    ("## gen-plan v3.34.0", "## gen-plan v3.35.0", 1, "KB en-tête"),
    ("garantie mécanique par garde post-installation (v3.34.0, Task 49) ; déclencheurs de mode",
     "garantie mécanique par garde post-installation (v3.34.0, Task 49) ; " + N9_COURT + " ; déclencheurs de mode",
     1, "KB description n°9"),
    ("- **Dernière calibration** : montée v3.34.0 (2026-11-04, session web-c30e6506 — Task 49, "
     "directive propriétaire : règle d'or n°8 « PM INSTALL installe toujours les skills (SKILL.md), "
     "jamais les prompts maîtres » + renommage @PM-SKILLS + rafraîchissement miroirs + test PM INSTALL "
     "— cascade KO-L004 : PM v3.34.0 généré mécaniquement (delta verrouillé scripts/delta-genplan-v3340.json, "
     "révision B1 — substitutions verrouillées), SHARED v1.7.22 / PM-INSTALL v1.8.16 recalibrés "
     "automatiquement, PM v3.33.1 archivé @historique R4 byte-identité (SHA 01a57da5…))",
     "- **Dernière calibration** : montée v3.35.0 (2026-11-05, session web-c30e6506 — Task 52, "
     "directive propriétaire : « avant de continuer vérifie que mon écosystème est encore installé "
     "(si mon écosystème doit-être installé alors la lecture de PM SHARED doit-être faite et lorsque "
     "que mon écosystème sera installé alors génère à nouveau le plan d'action via mon skill gen-plan) "
     "et fais en sorte que cette vérification devienne automatique (…) lorsque mon skill gen-plan est "
     "appelé après une coupure. » — cascade KO-L004 : PM v3.35.0 généré mécaniquement (delta verrouillé "
     "scripts/delta-genplan-v3350.json — insertion n°9 §1.8 + extension E1-RES §1.12 + history), "
     "SHARED v1.7.23 / PM-INSTALL v1.9.1 recalibrés automatiquement, PM v3.34.0 archivé @historique "
     "R4 byte-identité (SHA ac9de174…))",
     1, "KB calibration"),
])

# --- 2. Pin ECO_SKILLS ---
edit("scripts/check-ecosysteme-integrity.py", [
    ('"gen-plan": "3.34.0",  # KO-L004 (Task 49 règle d\'or n°8, session web-c30e6506 2026-11-04',
     '"gen-plan": "3.35.0",  # KO-L004 (Task 52 règle d\'or n°9 post-coupure, session web-c30e6506 '
     '2026-11-05 — vérification automatique installation écosystème, cascade PM v3.35.0/SHARED '
     'v1.7.23/PM-INSTALL v1.9.1) ; précédent KO-L004 (Task 49 règle d\'or n°8, session web-c30e6506 2026-11-04',
     1, "Pin ECO_SKILLS gen-plan"),
])

# --- 3. historiques-par-skill/gen-plan.md ---
ROW_V3350 = ("| v3.35.0 | 2026-11-05 | Task 52 (session web-c30e6506 — directive propriétaire, gen-plan : "
             "« avant de continuer vérifie que mon écosystème est encore installé (si mon écosystème "
             "doit-être installé alors la lecture de PM SHARED doit-être faite et lorsque que mon "
             "écosystème sera installé alors génère à nouveau le plan d'action via mon skill gen-plan) "
             "et fais en sorte que cette vérification devienne automatique (…) lorsque mon skill gen-plan "
             "est appelé après une coupure. ») : **règle d'or n°9 « Vérification automatique de "
             "l'installation de l'écosystème à toute invocation de gen-plan (post-coupure) »** au §1.5 "
             "(après n°8, règles contiguës) — vérification mécanique des piliers (registre KB + corpus "
             "SHARED + forme installée) + arbitre check-ecosysteme-integrity à TOUTE invocation "
             "(coupure DÉTECTÉE par la vérification, jamais présupposée) ; écosystème absent/endommagé → "
             "chemin automatique en 4 temps : lecture intégrale PM SHARED (étape 0 PM-INSTALL) → "
             "réinstallation voie directe eco_install_pipeline.py (clone certifié, règle d'or n°4) → "
             "certification arbitres (verify-cross + integrity + verify-correct-work) → re-génération du "
             "plan via le gen-plan réinstallé (règle d'or n°2 + KO-L005) ; hook E1-RES étendu (trois → "
             "quatre vérifications préalables, point (4)) ; description frontmatter inchangée "
             "(non-régression triggers) ; cascade KO-L004 : PM v3.35.0 (delta verrouillé "
             "scripts/delta-genplan-v3350.json), SHARED v1.7.23 / PM-INSTALL v1.9.1 recalibrés, "
             "PM v3.34.0 archivé R4 (SHA ac9de174…), pin ECO_SKILLS 3.35.0, marqueur périmé v3.26.0 "
             "résorbé, propagation §0 v1.7.23, rescellement archive, replay arbitres ×2 ; preuve vivante : "
             "session courante (14/52 → 98/98 + 141/141 + 16/16 → plan via v3.35.0) | La reprise "
             "post-coupure vérifie et rétablit l'écosystème automatiquement avant toute planification — "
             "**VERSION VIVANTE (corpus)** |")

edit("skills/@historique/historiques-par-skill/gen-plan.md", [
    # 3a. démotion du marqueur v3.34.0
    ("Installation exclusive des formes installées — garantie structurelle formes/PM — **VERSION VIVANTE (corpus)** |",
     "Installation exclusive des formes installées — garantie structurelle formes/PM — supplantée par v3.35.0 le 2026-11-05 (Task 52) |",
     1, "Historique démotion v3.34.0"),
    # 3b. insertion ligne v3.35.0 après la ligne v3.34.0 (démotionnée), avant le footer
    ("supplantée par v3.35.0 le 2026-11-05 (Task 52) |\n\nFichiers archivés de la famille",
     "supplantée par v3.35.0 le 2026-11-05 (Task 52) |\n" + ROW_V3350 + "\n\nFichiers archivés de la famille",
     1, "Historique ligne v3.35.0"),
    # 3c. footer 34 → 35 fichiers
    ("v3.33.1 (34 fichiers, SHA-256 au §5).",
     "v3.33.1, v3.34.0 (35 fichiers, SHA-256 au §5).",
     1, "Historique footer 35 fichiers"),
    # 3d. résorption du marqueur périmé v3.26.0 (dérive héritée — un seul VIVANT désormais : v3.35.0)
    ("MINOR comportement — **VERSION VIVANTE (corpus)** |",
     "MINOR comportement — supplantée par v3.27.0 le 2026-10-25 (marqueur périmé résorbé Task 52) |",
     1, "Historique marqueur périmé v3.26.0 résorbé"),
])

# --- 4. Lignes vives 9 disciplines ---
for f in ["memory-engineering", "refactoring-test", "fleet-engineering",
          "spec-driven-development", "context-engineering", "graph-engineering",
          "harness-engineering", "refactoring-engineering", "loop-engineering"]:
    edit("skills/%s/SKILL.md" % f, [
        ("gen-plan v3.34.0", "gen-plan v3.35.0", 1, "Ligne vive %s" % f),
    ])

# --- 5. README @historique ---
edit("skills/@historique/README.md", [
    ("| `prompts-maitres/gen-plan/` | 34 PMs GEN-PLAN historiques (v3.6.1 → v3.33.1) —",
     "| `prompts-maitres/gen-plan/` | 35 PMs GEN-PLAN historiques (v3.6.1 → v3.34.0) —",
     1, "README @historique §1 gen-plan 35 PMs"),
    ("| GEN-PLAN | gen-plan — planification de tâches (4 modes, 15 étapes E1-E15) | 37 (v2.0.0 → v3.34.0) | 34 (v3.6.1 → v3.33.1) | v3.34.0 |",
     "| GEN-PLAN | gen-plan — planification de tâches (4 modes, 15 étapes E1-E15) | 38 (v2.0.0 → v3.35.0) | 35 (v3.6.1 → v3.34.0) | v3.35.0 |",
     1, "README @historique §2 stats GEN-PLAN"),
    ("## 5. Index des fichiers sources archivés (46 PMs — sceau SHA-256)",
     "## 5. Index des fichiers sources archivés (47 PMs — sceau SHA-256)",
     1, "README @historique §5 47 PMs"),
    ("| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.33.1.md | 01a57da54b8d0ea81abd623d7cb08a19c8299dde53c5abb97524f2d2d927c5fb |",
     "| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.33.1.md | 01a57da54b8d0ea81abd623d7cb08a19c8299dde53c5abb97524f2d2d927c5fb |\n"
     "| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.34.0.md | ac9de1747cd99cd7908d381ad5c4932f078391a200858847371b2f0a434d64c4 |",
     1, "README @historique §5 sceau v3.34.0"),
])

# --- 6. README corpus ---
edit("skills/@mon-ecosysteme/README.md", [
    ("│   ├── PROMPT-MAITRE-GEN-PLAN-v3.34.0.md",
     "│   ├── PROMPT-MAITRE-GEN-PLAN-v3.35.0.md",
     1, "README corpus arborescence GEN-PLAN v3.35.0"),
    ("> **Révision v2.1.15 (2026-11-04, Task 49",
     "> **Révision v2.1.16 (2026-11-05, Task 52 — session web-c30e6506, gen-plan, directive "
     "propriétaire « avant de continuer vérifie que mon écosystème est encore installé (si mon "
     "écosystème doit-être installé alors la lecture de PM SHARED doit-être faite et lorsque que "
     "mon écosystème sera installé alors génère à nouveau le plan d'action via mon skill gen-plan) "
     "et fais en sorte que cette vérification devienne automatique (…) lorsque mon skill gen-plan "
     "est appelé après une coupure. »)** : gen-plan v3.34.0→v3.35.0 (**règle d'or n°9** — "
     "vérification automatique de l'installation de l'écosystème à toute invocation post-coupure : "
     "piliers + arbitre integrity ; absent/endommagé → lecture intégrale PM SHARED → réinstallation "
     "PM-INSTALL voie directe → certification arbitres → re-génération du plan [règle d'or n°2 + "
     "KO-L005]) ; hook E1-RES étendu (quatrième vérification préalable) ; PM v3.35.0 généré "
     "mécaniquement KO-L004 (delta verrouillé scripts/delta-genplan-v3350.json), v3.34.0 archivé "
     "`@historique/prompts-maitres/gen-plan/` (git mv byte-identité R4, SHA ac9de174…) ; SHARED "
     "v1.7.23 / PM-INSTALL v1.9.1 ; propagation §0 v1.7.23 ; ULTRA régénéré ; KB gen-plan v3.35.0 + "
     "pin ECO_SKILLS 3.35.0 ; arborescence §2 recalibrée (GEN-PLAN v3.35.0). "
     "Précédent — **Révision v2.1.15 (2026-11-04, Task 49",
     1, "README corpus révision v2.1.16"),
])

# --- 7. RETRAITS_SANCTIONNES ---
edit("scripts/task21-f2-rebuild-archive.py", [
    ('    # cascade gen-plan v3.34.0 (Task 49, session web-c30e6506 — gen-plan(step),\n'
     '    # directive propriétaire règle d\'or n°8 « PM INSTALL installe toujours les\n'
     '    # skills, jamais les prompts maîtres ») — re-scellement Task 49 : PM GEN-PLAN\n'
     '    # v3.33.1 DÉPLACÉ git mv vers skills/@historique/prompts-maitres/gen-plan/\n'
     '    # — byte-identité vérifiée ci-dessous (garde anti-perte ; SHA 01a57da54b8d…).\n'
     '    "PROMPT-MAITRE-GEN-PLAN-v3.33.1.md",',
     '    # cascade gen-plan v3.35.0 (Task 52, session web-c30e6506 — gen-plan,\n'
     '    # directive propriétaire : vérification automatique de l\'installation de\n'
     '    # l\'écosystème à l\'invocation de gen-plan après coupure) — re-scellement\n'
     '    # Task 52 : PM GEN-PLAN v3.34.0 DÉPLACÉ git mv vers\n'
     '    # skills/@historique/prompts-maitres/gen-plan/ — byte-identité vérifiée\n'
     '    # ci-dessous (garde anti-perte ; SHA ac9de1747cd9…).\n'
     '    "PROMPT-MAITRE-GEN-PLAN-v3.34.0.md",\n\n'
     '    # cascade gen-plan v3.34.0 (Task 49, session web-c30e6506 — gen-plan(step),\n'
     '    # directive propriétaire règle d\'or n°8 « PM INSTALL installe toujours les\n'
     '    # skills, jamais les prompts maîtres ») — re-scellement Task 49 : PM GEN-PLAN\n'
     '    # v3.33.1 DÉPLACÉ git mv vers skills/@historique/prompts-maitres/gen-plan/\n'
     '    # — byte-identité vérifiée ci-dessous (garde anti-perte ; SHA 01a57da54b8d…).\n'
     '    "PROMPT-MAITRE-GEN-PLAN-v3.33.1.md",',
     1, "RETRAITS_SANCTIONNES += v3.34.0"),
])

print("=== Cascade Task 52 — gen-plan v3.35.0 : %d opérations ===" % len(OPS))
for op in OPS:
    print("  - %s" % op)
no_op = sum(1 for o in OPS if "DÉJÀ APPLIQUÉ" in o)
print("Résultat : %d appliquées, %d déjà appliquées (idempotence %s)" %
      (len(OPS) - no_op, no_op, "OK" if no_op in (0, len(OPS)) else "PARTIELLE — vérifier"))
