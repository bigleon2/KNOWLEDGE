#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.7)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

# -*- coding: utf-8 -*-
"""Task 8 G1-a — Corrections n°55 (refactoring-test discipline → outil) + port refactor-guard v1.7.0.

Directive propriétaire (gen-plan step, session web-b4d7dd19) :
  « tu as déclaré "refactoring-test" en tant que discipline mais je ne voulais pas
   qu'il le devienne, seul "refactoring-engineering" devait être une discipline
   qui se sert de mon skill "refactoring-test" comme un outil. »
Fusion discussion externe 468a4c26 : refactor-guard déclaré v1.7.0
(base hôte v1.2.0 portée, provenance R4 — lignée externe certifiée v1.7.0).

Règles : éditions chirurgicales assert count==1 ; idempotence ×2 ;
zéro fabrication (R3) ; jamais rétrograder (R2).
"""
import os
import shutil
import sys

BASE = "/home/z/my-project/KNOWLEDGE"
HOTE = "/home/z/my-project/skills"
EDITS = 0


def sub_locked(text, old, new, label, count=1):
    """Édition chirurgicale à critère d'ÉTAT (convention Task 27 : passe 2 = NO-OP vert) —
    le test d'état final (new présent) PRÉCÈDE le test d'occurrence de old :
    sans cela, les éditions de type insertion (new contient old comme préfixe)
    se ré-appliquent à chaque passe (incident corrigé par g1a-repair-dedup.py)."""
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


def edit_file(path, fn, label):
    print("— %s" % label)
    with open(path, encoding="utf-8") as f:
        t = f.read()
    t2 = fn(t)
    with open(path, "w", encoding="utf-8") as f:
        f.write(t2)


# ---------------------------------------------------------------- refactoring-test
def fix_ref_test(t):
    t = sub_locked(t, 'version: "1.0.0"', "version: 1.0.1", "ref-test : version 1.0.1 (déquoté)")
    t = sub_locked(
        t,
        "Skill discipline refactoring test : détecteur/évaluateur",
        "Skill outil refactoring test : détecteur/évaluateur",
        "ref-test : description discipline→outil")
    t = sub_locked(
        t,
        "Bras mécanique : scripts/refactoring-test-graph.py (stdlib). Spécialise la discipline refactoring test n°55 (source de vérité : SHARED §7).",
        "Bras mécanique : scripts/refactoring-test-graph.py (stdlib). Outil de la discipline refactoring-engineering (n°55 — source de vérité : SHARED §7) : refactoring-engineering se sert de refactoring-test comme un outil d'évaluation ; refactoring-test n'est PAS une discipline (correction directive propriétaire, Task 8) et reste appelable par tout élément (gen-plan, agents, disciplines, scripts).",
        "ref-test : spécialise→outil de la discipline n°55")
    t = sub_locked(
        t,
        "### §1.6 Fondements (n°55, 2026-10-12)",
        "### §1.6 Fondements (outil de la discipline n°55, 2026-10-12)",
        "ref-test : §1.6 titre outil")
    old_s8 = """## §8 — Registre d'assignation des disciplines (décentralisé du SHARED §7)
| Discipline | Détenteur principal | Fonction héritée |
|------------|--------------------|------------------|
| refactoring test | gen-plan (E4/E7 + situations E9-E14) | refactoring-engineering (pré-vol/post-vol obligatoire), tout élément évaluateur (agents, scripts, disciplines) |"""
    new_s8 = """## §8 — Rattachement à la discipline n°55 (décentralisé du SHARED §7)

refactoring-test est l'OUTIL de la discipline `refactoring-engineering` (n°55) — non une discipline (correction directive propriétaire, Task 8, session web-b4d7dd19 : « seul refactoring-engineering est une discipline, qui se sert de refactoring-test comme un outil » ; fusion discussion externe 468a4c26). Détenteur principal : gen-plan (E4/E7 + situations E9-E14) ; consommateur obligatoire : refactoring-engineering (pré-vol/post-vol — anti-auto-certification) ; appelable par tout élément (agents, scripts, disciplines)."""
    t = sub_locked(t, old_s8, new_s8, "ref-test : §8 registre→rattachement outil")
    t = sub_locked(
        t,
        "- v1.0.0 (n°55, 2026-10-12, session web-b4d7dd19 Task 7 — gen-plan(step) G3/G4) :",
        """- v1.0.1 (2026-10-12, session web-b4d7dd19 Task 8 — gen-plan(step), fusion discussion externe 468a4c26) : correction de déclaration — refactoring-test n'est PAS une discipline ; il est l'OUTIL de la discipline refactoring-engineering (n°55) qui se sert de lui comme d'un outil d'évaluation indépendant (directive propriétaire explicite) ; frontmatter déquoté (S4 — valeur inchangée dans le bump).
- v1.0.0 (n°55, 2026-10-12, session web-b4d7dd19 Task 7 — gen-plan(step) G3/G4) :""",
        "ref-test : §6 traçabilité v1.0.1")
    return t


# ------------------------------------------------------- refactoring-engineering
def fix_ref_eng(t):
    t = sub_locked(t, 'version: "1.0.0"', "version: 1.0.1", "ref-eng : version 1.0.1 (déquoté)")
    t = sub_locked(
        t,
        "Évaluation INDÉPENDANTE obligatoire par refactoring-test (pré-vol/post-vol — anti-auto-certification) ; vérification par correct-work et les arbitres.",
        "Se sert de refactoring-test comme d'un OUTIL d'évaluation indépendante (pré-vol/post-vol — anti-auto-certification ; refactoring-test est l'outil de la présente discipline, non une discipline — correction directive propriétaire Task 8) ; vérification par correct-work et les arbitres.",
        "ref-eng : description outil")
    t = sub_locked(
        t,
        "Appelé par gen-plan (conception de plan E4/E7 + situations de refactoring détectées en E9-E14) et mobilisable par tout élément.",
        "Appelé par gen-plan (conception de plan E4/E7 + situations de refactoring détectées en E9-E14) et mobilisable par tout élément. Garde-fous mobilisés pendant les opérations : refactor-guard (score de risque H01-H15, sandbox, échelle rollout — fusion discussion 468a4c26, lignée externe v1.7.0).",
        "ref-eng : description garde-fous refactor-guard")
    old_dep = """  - skill: correct-work
    version: ">=2.7.0"
    used_at: "vérification post-opératoire — correct-work(groupe) après chaque groupe d'opérations, correct-work(projet) en fin de chaîne"
read_when:"""
    new_dep = """  - skill: correct-work
    version: ">=2.7.0"
    used_at: "vérification post-opératoire — correct-work(groupe) après chaque groupe d'opérations, correct-work(projet) en fin de chaîne"
  - skill: refactor-guard
    version: ">=1.7.0"
    used_at: "garde-fous des opérations D3/D4 — score de risque H01-H15, sandbox obligatoire, échelle rollout, maker-checker (fusion discussion 468a4c26)"
read_when:"""
    t = sub_locked(t, old_dep, new_dep, "ref-eng : dependencies += refactor-guard")
    t = sub_locked(
        t,
        "- `correct-work` — bras de vérification (correct-work(groupe)/projet) ; correct-work vérifie post-hoc, refactoring-engineering transforme — complémentaires, non fusionnés.",
        "- `correct-work` — bras de vérification (correct-work(groupe)/projet) ; correct-work vérifie post-hoc, refactoring-engineering transforme — complémentaires, non fusionnés.\n- `refactor-guard` — garde-fous des opérations : score de risque (H01-H15), sandbox obligatoire, échelle de déploiement, maker-checker ; mobilisé pendant D3/D4 pour les opérations à risque ; triangulation avec refactoring-test (évaluation) et correct-work (vérification).",
        "ref-eng : §3 relations += refactor-guard")
    t = sub_locked(
        t,
        "| refactoring engineering | gen-plan (E4/E7 conception + situations E9-E14) | correct-work (vérification post-opératoire), refactoring-test (évaluation indépendante obligatoire), tout élément transformateur supervisé |",
        "| refactoring engineering | gen-plan (E4/E7 conception + situations E9-E14) | correct-work (vérification post-opératoire), refactoring-test (OUTIL — évaluation indépendante obligatoire), refactor-guard (garde-fous des opérations), tout élément transformateur supervisé |",
        "ref-eng : §8 registre outil+garde-fous")
    t = sub_locked(
        t,
        "- v1.0.0 (n°55, 2026-10-12, session web-b4d7dd19 Task 7 — gen-plan(step) G3/G4) :",
        """- v1.0.1 (2026-10-12, session web-b4d7dd19 Task 8 — gen-plan(step), fusion discussion externe 468a4c26) : calibration de déclaration — « refactoring-engineering se sert de refactoring-test comme un outil » (seule discipline n°55) ; dependencies += refactor-guard >=1.7.0 (garde-fous) ; §3/§8 triangulation évaluateur/garde-fous/vérificateur.
- v1.0.0 (n°55, 2026-10-12, session web-b4d7dd19 Task 7 — gen-plan(step) G3/G4) :""",
        "ref-eng : §6 traçabilité v1.0.1")
    return t


# ------------------------------------------------------------ refactor-guard port
REFOG_HISTORY_ROW = """| 1.7.0 | 2026-10-12 | CONVERGENCE de la lignée externe (fusion discussion 468a4c26 — Task 8, session web-b4d7dd19, gen-plan(step)) : l'instance source a certifié refactor-guard v1.7.0 (double-montée Tasks 23-24 — 6 PM v1.2.0→v1.7.0, rollout enabled = échelle H15 terminale, ledger N6, verif-finale-n6 réconcilié « périmées-par-conception » Task 26) ; matérialisation canonique = base mécanique v1.2.0 portée à l'identique (11 scripts stdlib + evals + references ×2) + présente calibration ; diffs intermédiaires v1.3.0→v1.6.0 non verbatim consignés par leurs preuves de discussion (R4 provenance — réserve : PMs de la lignée externe non portés, génération PM 3→4 familles = décision propriétaire D009 reportée) ; déclaration KB + ECO_SKILLS + arêtes bidirectionnelles (gen-plan hook E13, refactoring-engineering garde-fous D3/D4 — discipline n°55). |"""


def port_refactor_guard():
    src = os.path.join(HOTE, "refactor-guard")
    dst = os.path.join(BASE, "skills", "refactor-guard")
    print("— Port refactor-guard (hôte v1.2.0 → canonique)")
    if os.path.isdir(dst):
        print("  [NO-OP] skills/refactor-guard déjà présent (idempotence)")
    else:
        shutil.copytree(src, dst)
        print("  [COPY] %s → %s" % (src, dst))
    p = os.path.join(dst, "SKILL.md")
    with open(p, encoding="utf-8") as f:
        t = f.read()
    t = sub_locked(t, "version: 1.2.0", "version: 1.7.0", "ref-guard : version 1.7.0 (convergence fusion)")
    t = sub_locked(
        t,
        "## §0 — Contexte Système (SHARED v1.6.7)",
        "## §0 — Contexte Système (SHARED v1.7.4)",
        "ref-guard : marqueur §0 → v1.7.4")
    t = sub_locked(
        t,
        "Conçu pour la combinaison C-SAFE-1 = H02 + H04 +\n  H05 + H07 + H08 + H09 + H10 + H14 + H15.",
        "Conçu pour la combinaison C-SAFE-1 = H02 + H04 +\n  H05 + H07 + H08 + H09 + H10 + H14 + H15. Déclaré dans l'arbre canonique par la\n  fusion de la discussion externe 468a4c26 (Task 8) : lignée externe certifiée v1.7.0\n  (rollout enabled — échelle H15 terminale), base de contenu = hôte v1.2.0 porté\n  (provenance R4). Complément triangulaire de la discipline n°55 :\n  refactoring-engineering (exécutant) + refactoring-test (évaluateur) + refactor-guard\n  (garde-fous).",
        "ref-guard : description provenance fusion")
    anchor_hist = " 1.2.0 | 2026-10-10 | Première exécution N1 shadow réelle"
    if "CONVERGENCE de la lignée externe" in t:
        print("  [NO-OP] ref-guard : §5 historique v1.7.0 (état final déjà atteint)")
    else:
        c = t.count(anchor_hist)
        if c != 1:
            raise SystemExit("ABANDON : ancre historique refactor-guard introuvable (%d)" % c)
        idx = t.index("| 1.2.0 | 2026-10-10 | Première exécution N1 shadow réelle")
        end_of_row = t.index("\n", idx)
        t = t[:end_of_row + 1] + REFOG_HISTORY_ROW + "\n" + t[end_of_row + 1:]
        print("  [EDIT] ref-guard : §5 historique += v1.7.0 convergence")
        global EDITS
        EDITS += 1
    with open(p, "w", encoding="utf-8") as f:
        f.write(t)


def main():
    print("=== Task 8 G1-a — corrections n°55 + port refactor-guard ===")
    edit_file(os.path.join(BASE, "skills/refactoring-test/SKILL.md"),
              fix_ref_test, "skills/refactoring-test/SKILL.md")
    edit_file(os.path.join(BASE, "skills/refactoring-engineering/SKILL.md"),
              fix_ref_eng, "skills/refactoring-engineering/SKILL.md")
    port_refactor_guard()
    print("=== G1-a OK — %d éditions ===" % EDITS)


if __name__ == "__main__":
    main()
