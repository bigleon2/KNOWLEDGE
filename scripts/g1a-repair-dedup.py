#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.9)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

# -*- coding: utf-8 -*-
"""Task 8 G1-a-réparation —塌缩 les blocs insérés en doublons (incident d'idempotence
des éditions de type insertion où new contient old comme préfixe).

Leçon consignée (convergence Task 27 externe) : le critère d'édition doit être
l'ÉTAT FINAL CORRECT, jamais l'action faite — et le test d'état doit précéder
le test d'occurrence de old (new-first).
"""
import re

BASE = "/home/z/my-project/KNOWLEDGE"

GARDEFOUS = " Garde-fous mobilisés pendant les opérations : refactor-guard (score de risque H01-H15, sandbox, échelle rollout — fusion discussion 468a4c26, lignée externe v1.7.0)."
RELATION_RG = "- `refactor-guard` — garde-fous des opérations : score de risque (H01-H15), sandbox obligatoire, échelle de déploiement, maker-checker ; mobilisé pendant D3/D4 pour les opérations à risque ; triangulation avec refactoring-test (évaluation) et correct-work (vérification)."
TRAC_REFENG = "- v1.0.1 (2026-10-12, session web-b4d7dd19 Task 8 — gen-plan(step), fusion discussion externe 468a4c26) : calibration de déclaration — « refactoring-engineering se sert de refactoring-test comme un outil » (seule discipline n°55) ; dependencies += refactor-guard >=1.7.0 (garde-fous) ; §3/§8 triangulation évaluateur/garde-fous/vérificateur."
TRAC_REFTEST = "- v1.0.1 (2026-10-12, session web-b4d7dd19 Task 8 — gen-plan(step), fusion discussion externe 468a4c26) : correction de déclaration — refactoring-test n'est PAS une discipline ; il est l'OUTIL de la discipline refactoring-engineering (n°55) qui se sert de lui comme d'un outil d'évaluation indépendant (directive propriétaire explicite) ; frontmatter déquoté (S4 — valeur inchangée dans le bump)."
PROVENANCE_RG = " Déclaré dans l'arbre canonique par la\n  fusion de la discussion externe 468a4c26 (Task 8) : lignée externe certifiée v1.7.0\n  (rollout enabled — échelle H15 terminale), base de contenu = hôte v1.2.0 porté\n  (provenance R4). Complément triangulaire de la discipline n°55 :\n  refactoring-engineering (exécutant) + refactoring-test (évaluateur) + refactor-guard\n  (garde-fous)."


def collapse_block(text, block):
    """Remplace N occurrences consécutives (séparées par \n) par 1 ; N inline par 1."""
    n0 = text.count(block)
    if n0 <= 1:
        return text, n0
    # cas inline : bloc répété immédiatement (sans séparateur)
    while block + block in text:
        text = text.replace(block + block, block)
    # cas multi-lignes : blocs séparés par \n
    pat = re.compile("(?:%s\n?)+" % re.escape(block))
    def _one(m):
        return block + ("\n" if m.group(0).endswith("\n") else "")
    text = pat.sub(_one, text)
    return text, n0


def main():
    total_removed = 0
    jobs = [
        ("skills/refactoring-engineering/SKILL.md", [GARDEFOUS, RELATION_RG, TRAC_REFENG]),
        ("skills/refactoring-test/SKILL.md", [TRAC_REFTEST]),
        ("skills/refactor-guard/SKILL.md", [PROVENANCE_RG]),
    ]
    for rel, blocks in jobs:
        p = BASE + "/" + rel
        with open(p, encoding="utf-8") as f:
            t = f.read()
        for b in blocks:
            t, n0 = collapse_block(t, b)
            if n0 > 1:
                print("%s : doublons %d → 1 (%s...)" % (rel, n0, b[:60]))
                total_removed += n0 - 1
        with open(p, "w", encoding="utf-8") as f:
            f.write(t)
    print("=== Réparation OK — %d doublons résorbés ===" % total_removed)
    # Vérification d'état final
    checks = [
        ("skills/refactoring-engineering/SKILL.md", GARDEFOUS.strip(), 1),
        ("skills/refactoring-engineering/SKILL.md", RELATION_RG, 1),
        ("skills/refactoring-engineering/SKILL.md", TRAC_REFENG, 1),
        ("skills/refactoring-test/SKILL.md", TRAC_REFTEST, 1),
        ("skills/refactor-guard/SKILL.md", PROVENANCE_RG.strip(), 1),
    ]
    ok = True
    for rel, needle, want in checks:
        with open(BASE + "/" + rel, encoding="utf-8") as f:
            c = f.read().count(needle)
        status = "OK" if c == want else "FAIL"
        if c != want:
            ok = False
        print("  [%s] %s : %d occurrence(s) de %r" % (status, rel, c, needle[:50]))
    if not ok:
        raise SystemExit("ÉTAT FINAL NON CONFORME")
    print("=== État final vérifié : 1 occurrence partout ===")


if __name__ == "__main__":
    main()
