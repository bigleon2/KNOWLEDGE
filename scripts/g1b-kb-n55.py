#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.13)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

# -*- coding: utf-8 -*-
"""Task 8 G1-b — KB : corrections n°55 (outil), inscription refactor-guard v1.7.0
+ fullstack-dev v1.0.0 (fusion discussion 468a4c26, précédent Task 27 externe),
réciproques ×5 + correct-work, toilettage (blancs parasites).

Critère d'état (passe 2 = NO-OP vert), éditions chirurgicales.
"""
import re
import sys

EDITS = 0


def sub_locked(text, old, new, label, count=1):
    """Critère d'ÉTAT (passe 2 = NO-OP vert) — new-first, même sémantique que g1a."""
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

KB = "/home/z/my-project/KNOWLEDGE/skills/KNOWLEDGE.md"

ENTRY_REFGUARD = """## refactor-guard v1.7.0

- **Category** : ecosystem
- **Description** : Skill de garde-fous de refactoring (fusion discussion externe 468a4c26 — lignée externe certifiée v1.7.0, base hôte v1.2.0 portée, provenance R4) : refactorisation agnostique appelé par gen-plan lorsqu'un besoin de refactoring est détecté (métriques, dette technique, demande explicite) ; taxonomie de signaux H01-H15, score de risque pondéré (scripts/risk_score.py — stdlib), scan de dépendances (scripts/graph_scan.py — stdlib), spécification formelle (spec-driven-development), sandbox obligatoire (harness-engineering), maker-checker (loop-engineering), gouvernance N0-N5, principe zéro-régression (« aucune modification ne doit altérer le comportement, la stabilité ou les performances tant qu'elle n'a pas été prouvée, isolée, validée, réversible et observée »), 9 couches de sécurité, échelle de déploiement disabled → shadow → recommend_only → sandbox_only → human_approved → canary → enabled (défaut : shadow, enabled:false), contrats de performance (latence < 2 %, CPU < 5 %, mémoire < 5 %, erreurs 0), validation finale par correct-work v2.7.0 (couplage gen-plan OBLIGATOIRE). Complément triangulaire de la discipline n°55 : refactoring-engineering (exécutant) + refactoring-test (évaluateur) + refactor-guard (garde-fous).
- **Dépend de** : gen-plan >= v3.21.0 (appel hook, plan d'actions de refactorisation R6, E13 — frontmatter dependencies v1.7.0), correct-work >= v2.7.0 (R8 validation finale + par phase — couplage gen-plan OBLIGATOIRE), resource-monitor >= v1.0.0 (G-RES avant tout scan/sandbox), graph-engineering >= v1.0.1 (H02 — graphe de dépendances, centralité, cycles), spec-driven-development >= v1.0.0 (H07 — spécification comme contrat exécutable), harness-engineering >= v1.1.0 (H04/H09 — sandbox, arbitres, audit), loop-engineering >= v1.1.0 (H05/H08 — maker-checker, rollout itératif)
- **Utilisé par** : gen-plan (détection de besoins de refactoring — hook E13), refactoring-engineering (frontmatter dependencies v1.0.1 — garde-fous des opérations D3/D4, fusion discussion 468a4c26)
- **Dernière calibration** : Task 8 (2026-10-12, session web-b4d7dd19 — gen-plan(step), fusion discussion 468a4c26) : matérialisation canonique (port hôte v1.2.0 → v1.7.0 convergence ; 11 scripts stdlib + evals + references ×2) ; lignée externe documentée (double-montée Tasks 23-24, rollout enabled H15 terminal, 6 PM instance source — non portés, réserve R3/D009) ; arêtes bidirectionnelles ×7
- **Statut** : stable

## fullstack-dev v1.0.0

- **Category** : ecosystem
- **Description** : Développement web fullstack (Next.js 16, TypeScript, Tailwind CSS 4, shadcn/ui, Prisma ORM) — construire des applications web complètes, composants UI, schémas de base de données, routes API, websocket/socket.io ; inscrit au registre (Task 8, fusion discussion 468a4c26 Task 27 externe : référencé par correct-work « Dépend de » sans entrée au registre — précédent exact vue-upload Task 36) ; standards du registre respectés (§0 SHARED + trigger_evals au format liste)
- **Utilisé par** : correct-work (>= v1.0.0, projets web — « Dépend de » côté correct-work)
- **Dernière calibration** : Task 8 (2026-10-12, session web-b4d7dd19 — gen-plan(step), fusion discussion 468a4c26 Task 27) : inscription au registre + bidirectionnalité correct-work ; §0 présent (marqueur propagé) ; trigger_evals.json déjà au format liste — conforme ; frontmatter déquoté (S4)
- **Statut** : stable

"""


def main():
    with open(KB, encoding="utf-8") as f:
        t = f.read()
    print("— KB : entrée refactoring-engineering v1.0.1")
    t = sub_locked(t, "## refactoring-engineering v1.0.0", "## refactoring-engineering v1.0.1",
                   "KB ref-eng : heading v1.0.1")
    t = sub_locked(
        t,
        "pré-checks verrouillés = golden master ; évaluation indépendante obligatoire par refactoring-test (anti-auto-certification) ; vérification par correct-work et les arbitres.",
        "pré-checks verrouillés = golden master ; se sert de refactoring-test comme d'un outil d'évaluation indépendante (anti-auto-certification — refactoring-test est l'outil de la présente discipline, non une discipline) ; vérification par correct-work et les arbitres.",
        "KB ref-eng : description outil")
    t = sub_locked(
        t,
        "- **Dépend de** : gen-plan >= v3.15.0 (détenteur principal — E4/E7 + situations E9-E14, frontmatter dependencies v1.0.0), refactoring-test >= v1.0.0 (évaluation indépendante pré-vol/post-vol — anti-auto-certification), correct-work >= v2.7.0 (vérification post-opératoire — correct-work(groupe/projet))",
        "- **Dépend de** : gen-plan >= v3.15.0 (détenteur principal — E4/E7 + situations E9-E14, frontmatter dependencies v1.0.1), refactoring-test >= v1.0.1 (outil d'évaluation indépendante pré-vol/post-vol — anti-auto-certification), correct-work >= v2.7.0 (vérification post-opératoire — correct-work(groupe/projet)), refactor-guard >= v1.7.0 (garde-fous des opérations D3/D4 — fusion discussion 468a4c26)",
        "KB ref-eng : Dépend de +refactor-guard")
    t = sub_locked(
        t,
        "- **Utilisé par** : gen-plan (mobilisation n°55 — SKILL.md §1.6 bloc PATTERN:GEN-PLAN-REFACTORING-v1.0.0 + §3 relations v3.23.0, PM §1.9 — déclenchement automatique SHARED §7 ; conception des opérations E4/E7, situations E9-E14)",
        "- **Utilisé par** : gen-plan (mobilisation n°55 — SKILL.md §1.6 bloc PATTERN:GEN-PLAN-REFACTORING-v1.0.0 + §3 relations v3.23.1, PM §1.9 — déclenchement automatique SHARED §7 ; conception des opérations E4/E7, situations E9-E14)",
        "KB ref-eng : Utilisé par v3.23.1")
    t = sub_locked(
        t,
        "- **Dernière calibration** : v1.0.0 (Task 7, 2026-10-12, session web-b4d7dd19 — gen-plan(step) G3/G4) : matérialisation de la discipline n°55 (directive propriétaire) ; sources : recherche web approfondie (rapport Task 7) ; baseline A2 en attente QUOTA_OK",
        "- **Dernière calibration** : v1.0.1 (Task 8, 2026-10-12, session web-b4d7dd19 — gen-plan(step), fusion discussion 468a4c26) : « refactoring-engineering se sert de refactoring-test comme un outil » (seule discipline n°55 — directive propriétaire) ; dependencies += refactor-guard v1.7.0 (garde-fous) ; précédente : v1.0.0 (Task 7 — matérialisation n°55, recherche web approfondie, baseline A2 en attente QUOTA_OK)",
        "KB ref-eng : calibration v1.0.1")

    print("— KB : entrée refactoring-test v1.0.1 (outil)")
    t = sub_locked(t, "## refactoring-test v1.0.0", "## refactoring-test v1.0.1",
                   "KB ref-test : heading v1.0.1")
    t = sub_locked(
        t,
        "- **Description** : Skill discipline refactoring test : détecteur/évaluateur",
        "- **Description** : Skill outil refactoring test : détecteur/évaluateur",
        "KB ref-test : description outil")
    t = sub_locked(
        t,
        "Bras mécanique : scripts/refactoring-test-graph.py (stdlib). Spécialise la discipline refactoring test n°55 (source de vérité : SHARED §7).",
        "Bras mécanique : scripts/refactoring-test-graph.py (stdlib). Outil de la discipline refactoring-engineering (n°55 — source de vérité : SHARED §7) : refactoring-engineering se sert de refactoring-test comme un outil ; refactoring-test n'est PAS une discipline (correction directive propriétaire Task 8).",
        "KB ref-test : spécialise→outil")
    t = sub_locked(
        t,
        "- **Dépend de** : gen-plan >= v3.15.0 (détenteur principal — E4/E7 + situations E9-E14, frontmatter dependencies v1.0.0)\n- **Utilisé par** : gen-plan (mobilisation n°55 — SKILL.md §1.6 bloc + §3 relations v3.23.0, PM §1.9 — déclenchement automatique SHARED §7), refactoring-engineering (frontmatter dependencies v1.0.0 — évaluation indépendante pré-vol/post-vol obligatoire, anti-auto-certification)",
        "- **Dépend de** : gen-plan >= v3.15.0 (détenteur principal — E4/E7 + situations E9-E14, frontmatter dependencies v1.0.1)\n- **Utilisé par** : gen-plan (mobilisation n°55 — SKILL.md §1.6 bloc + §3 relations v3.23.1, PM §1.9 — déclenchement automatique SHARED §7), refactoring-engineering (frontmatter dependencies v1.0.1 — outil d'évaluation indépendante pré-vol/post-vol obligatoire, anti-auto-certification), tout élément (agents, disciplines, scripts — appel direct documenté)",
        "KB ref-test : Dépend de + Utilisé par outil")
    t = sub_locked(
        t,
        "- **Dernière calibration** : v1.0.0 (Task 7, 2026-10-12, session web-b4d7dd19 — gen-plan(step) G3/G4) : matérialisation de la discipline n°55 ; bras mécanique scripts/refactoring-test-graph.py (M3 testable sans QUOTA — gen-plan : blast radius 14 backward / 19 forward, verdict CRITIQUE élément pivot) ; baseline A2 en attente QUOTA_OK",
        "- **Dernière calibration** : v1.0.1 (Task 8, 2026-10-12, session web-b4d7dd19 — gen-plan(step), fusion discussion 468a4c26) : correction de déclaration — refactoring-test = OUTIL de la discipline n°55, non une discipline (directive propriétaire explicite) ; précédente : v1.0.0 (Task 7 — matérialisation, bras mécanique M3 blast radius 14/19 verdict CRITIQUE, baseline A2 en attente QUOTA_OK)",
        "KB ref-test : calibration v1.0.1")

    print("— KB : correct-work Utilisé par += refactor-guard")
    t = sub_locked(
        t,
        "refactoring-engineering (vérification post-opératoire des opérations de refactoring en mode groupe/projet — frontmatter dependencies v1.0.0)",
        "refactoring-engineering (vérification post-opératoire des opérations de refactoring en mode groupe/projet — frontmatter dependencies v1.0.1), refactor-guard (R8 validation finale des opérations de refactoring — couplage OBLIGATOIRE, frontmatter dependencies v1.7.0, fusion discussion 468a4c26)",
        "KB correct-work : Utilisé par += refactor-guard")

    print("— KB : entrée gen-plan v3.23.1")
    t = sub_locked(
        t,
        "matérialisations n°55 (Task 7, v3.23.0) : refactoring-engineering E4/E7 + situations E9-E14, refactoring-test détection/évaluation + graphe d'interactions/blast radius), méthode",
        "matérialisation n°55 (Task 7, v3.23.0) : refactoring-engineering — seule discipline, se sert de refactoring-test comme d'un outil (correction Task 8, v3.23.1 : refactoring-test n'est PAS une discipline) ; refactor-guard v1.7.0 garde-fous déclaré (fusion discussion 468a4c26)), méthode",
        "KB gen-plan : description n°55 corrigée")
    t = sub_locked(
        t,
        "refactoring-engineering >= v1.0.0 (mobilisation n°55 — bloc PATTERN:GEN-PLAN-REFACTORING-v1.0.0 §1.6, PM §1.9), refactoring-test >= v1.0.0 (détection/évaluation n°55 — E4/E7 + situations E9-E14, PM §1.9)",
        "refactoring-engineering >= v1.0.1 (mobilisation n°55 — bloc PATTERN:GEN-PLAN-REFACTORING-v1.0.0 §1.6, PM §1.9), refactoring-test >= v1.0.1 (outil de détection/évaluation n°55 — E4/E7 + situations E9-E14, PM §1.9), refactor-guard >= v1.7.0 (garde-fous de refactoring — détection de besoins, hook E13, fusion discussion 468a4c26)",
        "KB gen-plan : Dépend de ×3")
    t = sub_locked(
        t,
        "refactoring-engineering (frontmatter dependencies v1.0.0 — détenteur principal, n°55), refactoring-test (frontmatter dependencies v1.0.0 — détenteur principal, n°55)",
        "refactoring-engineering (frontmatter dependencies v1.0.1 — détenteur principal, n°55), refactoring-test (frontmatter dependencies v1.0.1 — outil de la discipline n°55), refactor-guard (frontmatter dependencies v1.7.0 — appel hook, plan d'actions R6)",
        "KB gen-plan : Utilisé par ×3")
    t = sub_locked(
        t,
        "- **Dernière calibration** : montée v3.23.0 (2026-10-12, Task 7 — gen-plan(step), session web-b4d7dd19) :",
        "- **Dernière calibration** : montée v3.23.1 (2026-10-12, Task 8 — gen-plan(step), session web-b4d7dd19, fusion discussion externe 468a4c26) : correction outil (refactoring-test n'est plus déclaré discipline — seul refactoring-engineering est la discipline n°55 et se sert de refactoring-test comme d'un outil), refactor-guard v1.7.0 déclaré (garde-fous — base hôte v1.2.0 portée R4), fullstack-dev inscrit au registre (précédent vue-upload, Task 27 externe), toilettage KB (3 blancs parasites), S4 déquotes frontmatters (valeurs inchangées) ; montée v3.23.0 (2026-10-12, Task 7 — gen-plan(step), session web-b4d7dd19) :",
        "KB gen-plan : calibration v3.23.1")

    print("— KB : réciproques ×5 (refactor-guard)")
    recips = {
        "resource-monitor": "G-RES avant tout scan/sandbox",
        "graph-engineering": "H02 — graphe de dépendances, centralité, cycles",
        "spec-driven-development": "H07 — spécification de refactorisation comme contrat exécutable",
        "harness-engineering": "H04/H09 — sandbox, arbitres, audit",
        "loop-engineering": "H05/H08 — maker-checker, rollout itératif",
    }
    for skill, used_at in recips.items():
        m = re.search(r"(## %s v[0-9.]+\n.*?)(?=\n## )" % re.escape(skill), t, re.S)
        if not m:
            raise SystemExit("ABANDON : entrée KB %s introuvable" % skill)
        block = m.group(1)
        mu = re.search(r"- \*\*Utilisé par\*\* : (.*)", block)
        if not mu:
            raise SystemExit("ABANDON : Utilisé par absent pour %s" % skill)
        line = mu.group(0)
        if "refactor-guard" in line:
            print("  [NO-OP] réciproque %s (déjà présente)" % skill)
            continue
        new_line = line.rstrip() + ", refactor-guard (%s — frontmatter dependencies v1.7.0, fusion discussion 468a4c26)" % used_at
        t = sub_locked(t, line, new_line, "KB réciproque %s" % skill)

    print("— KB : inscription refactor-guard + fullstack-dev")
    anchor = "## Décisions d'architecture (corrige-ecosysteme v2.0.0)"
    if "## refactor-guard v1.7.0" in t:
        print("  [NO-OP] entrées déjà inscrites")
    else:
        c = t.count(anchor)
        if c != 1:
            raise SystemExit("ABANDON : ancre Décisions (%d)" % c)
        t = t.replace(anchor, ENTRY_REFGUARD + anchor)
        print("  [EDIT] 2 entrées inscrites avant Décisions")

    print("— KB : toilettage blancs parasites entre puces")
    lines = t.split("\n")
    keep = [l for i, l in enumerate(lines)
            if not (l.strip() == "" and 0 < i < len(lines) - 1
                    and lines[i - 1].strip().startswith("- ") and lines[i + 1].strip().startswith("- "))]
    removed = len(lines) - len(keep)
    if removed:
        t = "\n".join(keep)
        print("  [EDIT] %d blanc(s) parasites supprimé(s)" % removed)
    else:
        print("  [NO-OP] 0 blanc parasite")

    with open(KB, "w", encoding="utf-8") as f:
        f.write(t)
    print("=== G1-b OK ===")


if __name__ == "__main__":
    main()
