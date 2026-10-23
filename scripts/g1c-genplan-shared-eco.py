#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.12)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

# -*- coding: utf-8 -*-
"""Task 8 G1-c — gen-plan v3.23.1 (correction outil + fusion refactor-guard),
SHARED §7 (discipline n°55 + outil + registre ×3), ECO_SKILLS (+2, bumps),
S4 déquotes frontmatters (version: uniquement, valeurs inchangées).
"""
import glob
import json
import os
import re

EDITS = 0
BASE = "/home/z/my-project/KNOWLEDGE"


def sub_locked(text, old, new, label, count=1):
    global EDITS
    if new != old and text.count(new) >= 1:
        print("  [NO-OP] %s (état final déjà atteint)" % label)
        return text
    c = text.count(old)
    if c == count and old != new:
        EDITS += 1
        print("  [EDIT] %s" % label)
        return text.replace(old, new)
    print("  [FAIL] %s — occurrences old=%d (attendu %d), new=%d" % (label, c, count, text.count(new)))
    raise SystemExit("ABANDON verrouillé : %s" % label)


def genplan():
    p = BASE + "/skills/gen-plan/SKILL.md"
    with open(p, encoding="utf-8") as f:
        t = f.read()
    print("— gen-plan SKILL.md v3.23.1")
    t = sub_locked(t, "version: 3.23.0", "version: 3.23.1", "gen-plan : version 3.23.1")
    # NB : la description frontmatter gen-plan ne mentionne pas n°55 (KB-only) —
    # la correction « outil » de la description gen-plan a été faite côté KB (g1b).
    # NB : les lignes prose « Dépend de »/« Utilisé par »/« Dernière calibration »
    # sont des champs KB (g1b) — le YAML gen-plan ne liste pas les disciplines
    # (précédent n°54 : orchestration déclarée par le bloc PATTERN §1.6 + KB).
    t = sub_locked(
        t,
        "| **Refactoring engineering** | Discipline n°55 : déclaration/planification/exécution des opérations de refactoring (petites transformations préservant le comportement observable — arbitres, semver, R2/R4) ; bloc PATTERN:GEN-PLAN-REFACTORING-v1.0.0 |",
        "| **Refactoring engineering** | Discipline n°55 : déclaration/planification/exécution des opérations de refactoring (petites transformations préservant le comportement observable — arbitres, semver, R2/R4) ; se sert de refactoring-test comme d'un outil ; garde-fous : refactor-guard (fusion 468a4c26) ; bloc PATTERN:GEN-PLAN-REFACTORING-v1.0.0 |",
        "gen-plan : §1.6 ligne ref-eng")
    t = sub_locked(
        t,
        "| **Refactoring test** | Discipline n°55 : détection/évaluation des situations de refactoring + graphe d'interactions (blast radius) ; verdict machine OK/PRESSION/CRITIQUE |",
        "| **Refactoring test** | Outil de la discipline n°55 (non discipline — Task 8) : détection/évaluation des situations de refactoring + graphe d'interactions (blast radius) ; verdict machine OK/PRESSION/CRITIQUE |",
        "gen-plan : §1.6 ligne ref-test outil")
    t = sub_locked(
        t,
        "**Disciplines de refactoring n°55 (v3.23.0, directive propriétaire session web-b4d7dd19 : « le système de refactoring de mon écosystème déclaré et tagué en tant que discipline »)** : le système de refactoring effectif de l'écosystème (correct-work modes CIBLE/DIRECT + procédures cascade PM + arbitres mécaniques + archivage @historique R4) est déclaré comme discipline `refactoring-engineering` ; le détecteur/évaluateur `refactoring-test` (producteur d'information, ne modifie rien — anti-auto-certification) est appelable par tout élément (gen-plan, agents, disciplines, scripts). gen-plan les mobilise :",
        "**Discipline de refactoring n°55 et son outil (v3.23.1 — Task 8 : correction directive propriétaire « seul refactoring-engineering est une discipline, qui se sert de refactoring-test comme un outil » ; fusion discussion externe 468a4c26 : refactor-guard v1.7.0 déclaré comme garde-fous des opérations)** : le système de refactoring effectif de l'écosystème (correct-work modes CIBLE/DIRECT + procédures cascade PM + arbitres mécaniques + archivage @historique R4) est déclaré comme discipline `refactoring-engineering` ; l'outil `refactoring-test` (producteur d'information, non discipline, ne modifie rien — anti-auto-certification) est appelable par tout élément (gen-plan, agents, disciplines, scripts) ; le garde-fous `refactor-guard` (score de risque H01-H15, sandbox, échelle rollout) est mobilisé par refactoring-engineering pendant les opérations à risque. gen-plan les mobilise :",
        "gen-plan : bloc PATTERN n°55 outil+garde-fous")
    t = sub_locked(
        t,
        "Source de vérité : SHARED §7 (n°55) ; détention orchestrée : registre décentralisé §8 de chaque skill + registre KB.",
        "Source de vérité : SHARED §7 (n°55) ; détention orchestrée : registre décentralisé §8 de chaque skill + registre KB. Les opérations à risque mobilisent refactor-guard (garde-fous — fusion 468a4c26).",
        "gen-plan : règle anti-auto-certification +garde-fous")
    t = sub_locked(
        t,
        "| refactoring-engineering | Mobilisation n°55 (SHARED §7, bloc PATTERN:GEN-PLAN-REFACTORING-v1.0.0) | Conception/exécution des opérations de refactoring (E4/E7 + situations E9-E14) — version >= v1.0.0 |",
        "| refactoring-engineering | Mobilisation n°55 (SHARED §7, bloc PATTERN:GEN-PLAN-REFACTORING-v1.0.0) | Conception/exécution des opérations de refactoring (E4/E7 + situations E9-E14) — version >= v1.0.1 |\n| refactor-guard | Garde-fous de refactoring (fusion discussion 468a4c26 — lignée externe v1.7.0) | Mobilisé par refactoring-engineering pendant les opérations à risque (score H01-H15, sandbox, rollout) ; détection de besoins (hook E13) — version >= v1.7.0 |",
        "gen-plan : §3 relations ref-eng + refactor-guard")
    t = sub_locked(
        t,
        "| refactoring-test | Mobilisation n°55 (SHARED §7, bloc PATTERN:GEN-PLAN-REFACTORING-v1.0.0) | Détection/évaluation + graphe d'interactions (blast radius) — verdict machine, version >= v1.0.0 |",
        "| refactoring-test | Outil n°55 (SHARED §7, bloc PATTERN:GEN-PLAN-REFACTORING-v1.0.0) | Détection/évaluation + graphe d'interactions (blast radius) — verdict machine, version >= v1.0.1 |",
        "gen-plan : §3 relations ref-test outil")
    with open(p, "w", encoding="utf-8") as f:
        f.write(t)


def shared():
    p = BASE + "/skills/@mon-ecosysteme/PROMPT-MAITRE-SHARED.md"
    with open(p, encoding="utf-8") as f:
        t = f.read()
    print("— SHARED §7 (contenu — la version est bumpée par generer-pm-skill)")
    t = sub_locked(
        t,
        "ThoughtWorks (strangler fig, fitness functions), Janea Systems 2026 (revues insuffisantes). |",
        "ThoughtWorks (strangler fig, fitness functions), Janea Systems 2026 (revues insuffisantes). Se sert de refactoring-test comme d'un outil d'évaluation indépendant ; garde-fous : refactor-guard (fusion 468a4c26). |",
        "SHARED : ligne ref-eng +outil")
    t = sub_locked(
        t,
        "| **Refactoring test** (n°55) |",
        "| **Refactoring test** (outil de la discipline n°55) |",
        "SHARED : ligne ref-test outil")
    t = sub_locked(
        t,
        "Skill `refactoring-test` (matérialisation n°55, déclenchement automatique — registre ci-dessous) |",
        "Skill `refactoring-test` (outil de la matérialisation n°55 — non discipline, Task 8 ; déclenchement automatique — registre ci-dessous) |",
        "SHARED : colonne skill ref-test")
    old_reg = "| `refactoring-engineering` / `refactoring-test` | **Matérialisations skills des disciplines n°55** (Task 7, 2026-10-12 : SKILL.md + evals + trigger_evals — déclenchement automatique ; détention orchestrée : registre décentralisé §8 du skill + registre KB) | Application dédiée (opérations de refactoring zéro-régression ; détection/évaluation + graphe d'interactions) — orchestration gen-plan §1.9 |"
    new_reg = """| `refactoring-engineering` | **Matérialisation skill de la discipline n°55** (Task 7, 2026-10-12 : SKILL.md + evals + trigger_evals ; Task 8 v1.0.1 — correction directive propriétaire : seul refactoring-engineering est une discipline et se sert de refactoring-test comme d'un outil ; détention orchestrée : registre décentralisé §8 du skill + registre KB) | Application dédiée (opérations de refactoring zéro-régression) — orchestration gen-plan §1.9 |
| `refactoring-test` | **Outil de la matérialisation n°55** (Task 8 v1.0.1 — non discipline : « refactoring-test ne doit pas devenir une discipline, refactoring-engineering se sert de refactoring-test comme un outil ») | Détection/évaluation + graphe d'interactions — appelable par tout élément (gen-plan, agents, disciplines, scripts) |
| `refactor-guard` | **Skill de garde-fous de refactoring** (Task 8, fusion discussion externe 468a4c26 : lignée externe v1.7.0 déclarée — base hôte v1.2.0 portée, provenance R4) | Score de risque H01-H15, sandbox, échelle rollout — mobilisé par refactoring-engineering et gen-plan |"""
    t = sub_locked(t, old_reg, new_reg, "SHARED : registre n°55 → 3 lignes")
    with open(p, "w", encoding="utf-8") as f:
        f.write(t)


def eco_skills():
    p = BASE + "/scripts/check-ecosysteme-integrity.py"
    with open(p, encoding="utf-8") as f:
        t = f.read()
    print("— ECO_SKILLS (checker intégrité)")
    t = sub_locked(t, '"gen-plan": "3.23.0",', '"gen-plan": "3.23.1",', "ECO gen-plan 3.23.1")
    t = sub_locked(
        t,
        '"refactoring-engineering": "1.0.0",  # n°55 (session web-b4d7dd19, 2026-10-12) : matérialisation Task 7 gen-plan(step) — disciplines de refactoring',
        '"refactoring-engineering": "1.0.1",  # n°55 (session web-b4d7dd19, 2026-10-12) : Task 8 — seule discipline de refactoring, outil refactoring-test, garde-fous refactor-guard\n    "refactor-guard": "1.7.0",  # Task 8 (fusion discussion 468a4c26) : garde-fous de refactoring — lignée externe v1.7.0, base hôte v1.2.0 portée\n    "fullstack-dev": "1.0.0",  # Task 8 (fusion discussion 468a4c26 Task 27 externe) : inscrit au registre — précédent vue-upload',
        "ECO ref-eng +refactor-guard +fullstack-dev")
    t = sub_locked(
        t,
        '"refactoring-test": "1.0.0",  # KO-L004 (session web-b4d7dd19, 2026-10-11) : read_when + dependencies gen-plan — bump PATCH cascade n°54',
        '"refactoring-test": "1.0.1",  # Task 8 (session web-b4d7dd19, 2026-10-12) : OUTIL de la discipline n°55 (non discipline — correction directive propriétaire)',
        "ECO ref-test outil +commentaire corrigé")
    with open(p, "w", encoding="utf-8") as f:
        f.write(t)


def dequotes():
    print("— S4 déquotes frontmatters (compétences du registre — version: uniquement)")
    with open(BASE + "/scripts/check-ecosysteme-integrity.py", encoding="utf-8") as f:
        m = re.search(r"ECO_SKILLS\s*=\s*\{(.*?)\}", f.read(), re.S)
    keys = re.findall(r'"([a-z0-9-]+)":\s*"[0-9.]+"', m.group(1))
    n_done = 0
    for k in keys:
        p = "%s/skills/%s/SKILL.md" % (BASE, k)
        if not os.path.isfile(p):
            print("  [WARN] %s : SKILL.md absent (consigné)" % k)
            continue
        with open(p, encoding="utf-8") as f:
            t = f.read()
        t2, n = re.subn(r'(?m)^(version:) "([0-9.]+)"$', r"\1 \2", t)
        if n:
            with open(p, "w", encoding="utf-8") as f:
                f.write(t2)
            n_done += n
            print("  [EDIT] %s : version déquotée (%d)" % (k, n))
    print("  déquotes totales : %d (état final : 0 frontmatter quoté au registre)" % n_done)


def main():
    genplan()
    shared()
    eco_skills()
    dequotes()
    # preuve d'état : plus aucun version: quoté parmi les compétences du registre
    with open(BASE + "/scripts/check-ecosysteme-integrity.py", encoding="utf-8") as f:
        m = re.search(r"ECO_SKILLS\s*=\s*\{(.*?)\}", f.read(), re.S)
    keys = re.findall(r'"([a-z0-9-]+)":\s*"[0-9.]+"', m.group(1))
    restants = []
    for k in keys:
        p = "%s/skills/%s/SKILL.md" % (BASE, k)
        if os.path.isfile(p) and re.search(r'(?m)^version: "[0-9.]+"$', open(p, encoding="utf-8").read()):
            restants.append(k)
    print("=== G1-c OK — %d compétences quotées restantes ===" % len(restants))
    if restants:
        print(json.dumps(restants, indent=1))
        raise SystemExit("S4 incomplet")


if __name__ == "__main__":
    main()
