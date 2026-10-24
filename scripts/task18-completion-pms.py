#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.13)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.

task18-completion-pms.py — Complétion agent des deltas sémantiques des 4 PMs générés
(KO-L004 v1.1.0, §2quater PM-INSTALL : « le delta sémantique n'est PAS inventé : il est
fourni via --delta ou complété par l'agent » — complétion en discipline sub_locked :
chaque substitution verrouille son motif, ABANDON SANS ÉCRITURE si compte != attendu).

Deltas appliqués (Task 18, session web-fdf5963c, 2026-10-23) :
  1. Les 4 PMs — §5 : note « mécanisme dual d'installation » (installation directe
     des formes certifiées par défaut — PM-INSTALL v1.8.0 §3.2 ; §5 = spécification
     de la forme + voie bootstrap corpus-seul).
  2. correct-work v2.8.0 — intégration alias-eco : description §4, dependencies §4,
     §2.2 Dépendances, §3 Relations, §10.1 Phase 2 (miroir exact du SKILL.md v2.8.0).
  3. Les 4 PMs — §7 : ligne d'historique affinée (remplace la ligne générique
     « deltas sémantiques à complétion agent » par la description réelle de la montée).

All-or-nothing : toute substitution en échec => AUCUNE écriture (état préservé).
"""
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPUS = os.path.join(BASE, "skills", "@mon-ecosysteme")

NOTE_DUAL_3F = (
    "## §5 — INSTRUCTIONS D'INSTALLATION\n\n"
    "> **Mécanisme dual d'installation (PM-INSTALL v1.8.0, §3.2)** : ce §5 est la "
    "SPÉCIFICATION de la forme installée et la voie bootstrap (corpus/archive seul). "
    "Lorsque le dépôt est disponible, l'installation DIRECTE des formes certifiées "
    "(clone git — règle d'or n°4, garde R2 anti-rétrogradation, arbitres) est la voie "
    "par défaut ; l'assemblage ci-dessous reconstruit la même forme à l'identique.\n\n"
    "### §5.1 Créer la structure"
)

HIST = {
    "gen-plan": "Optimisation du système d'installation (directive propriétaire 2026-10-23, session web-fdf5963c, Task 18) : §5 — note mécanisme dual (installation directe des formes certifiées par défaut — PM-INSTALL v1.8.0 §3.2 ; l'assemblage §5 demeure la spécification de la forme et la voie bootstrap corpus-seul). Montée PATCH (documentation d'installation uniquement).",
    "correct-work": "Intégration alias-eco + mécanisme dual (directive propriétaire 2026-10-23, session web-fdf5963c, Task 18) : mode PROJET — délégation de la tenue du registre des phrases récurrentes à alias-eco >= v1.0.0 (§10.1 Phase 2, registre @historique/@Alias/ — JSON trié dédupliqué) ; dependencies §4 et §2.2 += alias-eco ; §3 Relations += alias-eco ; §5 — note mécanisme dual d'installation (installation directe des formes certifiées par défaut — PM-INSTALL v1.8.0 §3.2). Montée MINOR (nouvelle intégration fonctionnelle).",
    "clone-chat": "Optimisation du système d'installation (directive propriétaire 2026-10-23, session web-fdf5963c, Task 18) : §5 — note mécanisme dual (installation directe des formes certifiées par défaut — PM-INSTALL v1.8.0 §3.2 ; l'assemblage §5 demeure la spécification de la forme et la voie bootstrap corpus-seul). Montée PATCH (documentation d'installation uniquement).",
    "refactor-guard": "Optimisation du système d'installation (directive propriétaire 2026-10-23, session web-fdf5963c, Task 18) : §5 — note mécanisme dual explicitant la cohérence de ce §5 avec PM-INSTALL v1.8.0 §3.2 (ce §5 prescrit DÉJÀ l'installation directe par copie des formes certifiées — voie par défaut ; l'assemblage depuis le corpus demeure la voie bootstrap). Montée PATCH (documentation d'installation uniquement).",
}


def sub_locked(text, motif, remplace, n, label):
    c = text.count(motif)
    if c != n:
        print("ABANDON : motif [%s] trouvé %d fois (attendu %d) : %r" % (label, c, n, motif[:70]))
        sys.exit(2)
    return text.replace(motif, remplace)


def main():
    edits = {}  # fichier -> (texte_nouveau, ops)

    # --- 1. Note mécanisme dual : 3 familles à ancre §5.1 ---
    for f in ["PROMPT-MAITRE-GEN-PLAN-v3.23.2.md",
              "PROMPT-MAITRE-CORRECT-WORK-v2.8.0.md",
              "PROMPT-MAITRE-CLONE-CHAT-v2.0.2.md"]:
        p = os.path.join(CORPUS, f)
        t = open(p, encoding="utf-8").read()
        t = sub_locked(t, "## §5 — INSTRUCTIONS D'INSTALLATION\n\n### §5.1 Créer la structure",
                       NOTE_DUAL_3F, 1, "§5 dual " + f)
        edits[f] = t

    # --- 1bis. Note mécanisme dual : refactor-guard (ancre propre) ---
    p = os.path.join(CORPUS, "PROMPT-MAITRE-REFACTOR-GUARD-v1.7.1.md")
    t = open(p, encoding="utf-8").read()
    t = sub_locked(
        t,
        "## §5 — INSTRUCTIONS D'INSTALLATION\n\n1. **Récupération du dépôt par clone git local**",
        "## §5 — INSTRUCTIONS D'INSTALLATION\n\n"
        "> **Mécanisme dual d'installation (PM-INSTALL v1.8.0, §3.2)** : ce §5 prescrit "
        "l'installation DIRECTE des formes certifiées (voie par défaut — conforme au "
        "pipeline v1.8.0) ; l'assemblage depuis le corpus demeure la voie bootstrap "
        "(corpus/archive seul).\n\n"
        "1. **Récupération du dépôt par clone git local**",
        1, "§5 dual refactor-guard")
    edits["PROMPT-MAITRE-REFACTOR-GUARD-v1.7.1.md"] = t

    # --- 2. correct-work v2.8.0 : intégration alias-eco (miroir SKILL.md) ---
    f = "PROMPT-MAITRE-CORRECT-WORK-v2.8.0.md"
    t = edits[f]
    # description §4
    t = sub_locked(t,
        "  matrice de décision agent/skill (statique + dynamique KB),",
        "  délégation alias-eco (mode PROJET — tenue du registre des phrases récurrentes, v2.8.0),\n"
        "  matrice de décision agent/skill (statique + dynamique KB),",
        1, "cw description")
    # dependencies §4 (bloc YAML du §4)
    t = sub_locked(t,
        '    used_at: "Vérification projets web"',
        '    used_at: "Vérification projets web"\n'
        '  - skill: alias-eco\n'
        '    version: ">=1.0.0"\n'
        '    used_at: "Mode PROJET — tenue du registre des phrases récurrentes (§10.1 Phase 2)"',
        1, "cw dependencies §4")
    # §2.2 Dépendances
    t = sub_locked(t,
        "| fullstack-dev | >= v1.0.0 | Vérification de projets web | Oui |",
        "| fullstack-dev | >= v1.0.0 | Vérification de projets web | Oui |\n"
        "| alias-eco | >= v1.0.0 | Mode PROJET — registre des phrases récurrentes (§10.1 Phase 2, v2.8.0) | Oui (mode PROJET seulement) |",
        1, "cw §2.2")
    # §3 Relations
    t = sub_locked(t,
        "| fullstack-dev | Vérification | Projets web : structure et dépendances, version >= v1.0.0 |",
        "| fullstack-dev | Vérification | Projets web : structure et dépendances, version >= v1.0.0 |\n"
        "| alias-eco | Délégation (v2.8.0) | Mode PROJET — tenue du registre des phrases récurrentes de la discussion analysée (§10.1 Phase 2, registre @historique/@Alias/), version >= v1.0.0 |",
        1, "cw §3")
    # §10.1 Phase 2
    t = sub_locked(t,
        "### Phase 2 — Erreurs et omissions\n- [ ] Chaque section du prompt comparée au livrable",
        "### Phase 2 — Erreurs et omissions\n"
        "- [ ] Phrases récurrentes de la discussion analysée : registre tenu à jour via alias-eco (délégation v2.8.0 — JSON trié dédupliqué dans @historique/@Alias/)\n"
        "- [ ] Chaque section du prompt comparée au livrable",
        1, "cw §10.1")
    edits[f] = t

    # --- 3. Lignes d'historique §7 affinées ---
    for f, famille in [("PROMPT-MAITRE-GEN-PLAN-v3.23.2.md", "gen-plan"),
                       ("PROMPT-MAITRE-CORRECT-WORK-v2.8.0.md", "correct-work"),
                       ("PROMPT-MAITRE-CLONE-CHAT-v2.0.2.md", "clone-chat"),
                       ("PROMPT-MAITRE-REFACTOR-GUARD-v1.7.1.md", "refactor-guard")]:
        t = edits[f]
        old_line = None
        for line in t.splitlines():
            if line.startswith("| v") and "deltas sémantiques à complétion agent" in line:
                old_line = line
                break
        if old_line is None:
            print("ABANDON : ligne d'historique générique introuvable dans %s" % f)
            sys.exit(2)
        new_line = "| %s | %s | %s |" % (
            old_line.split("|")[1].strip(),
            old_line.split("|")[2].strip(),
            HIST[famille] + " Recalibrage croisé KO-L004 : SHARED §6.1, PM-INSTALL §2ter/§A.3.")
        edits[f] = t.replace(old_line, new_line, 1)

    # --- Écriture all-or-nothing ---
    for f, t in edits.items():
        with open(os.path.join(CORPUS, f), "w", encoding="utf-8") as fh:
            fh.write(t)
        print("Complété : %s" % f)
    print("COMPLÉTION OK — 4 PMs, %d substitutions verrouillées" % (4 + 5 + 4))
    return 0


if __name__ == "__main__":
    sys.exit(main())
