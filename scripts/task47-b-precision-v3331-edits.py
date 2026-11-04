#!/usr/bin/env python3
"""⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.21)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""
"""Task 47 (b) — précision sémantique de la règle d'or n°7 — PATCH v3.33.0 → v3.33.1.
Directive propriétaire verbatim (2026-11-04, session web-6058b3ba) :
  « prend en compte que lorsque je précise que lorsque je disais "ce que tu as oublié"
  alors je voulais dire "les éléments oubliés à cause d'une coupure et que tu as
  partiellement réussi à reconstituer". »
Étapes (TOUTES AVANT scripts/generer-pm-skill.py --generate) :
  1. skills/gen-plan/SKILL.md : précision n°7 §1.5 (2 substitutions — définition de
     l'« oubli » + clause reconstitution partielle) + bump v3.33.1 + §5.6 ligne
  2. skills/KNOWLEDGE.md : en-tête gen-plan v3.33.1 + calibration (ancienne → « Précédent — »)
  3. skills/@historique/historiques-par-skill/gen-plan.md : en-tête + ligne v3.33.1
     (marqueur VERSION VIVANTE déplacé) + compteurs
  4. Lignes vives : 9 disciplines + ULTRA (2 mentions) : gen-plan v3.33.0 → v3.33.1
  5. skills/@historique/README.md : sceau §5 v3.33.0 + labels recalibrés (comptage mécanique)
  6. scripts/propagate-context.py : constantes §0 v1.7.19 → v1.7.20 (suit le bump SHARED)
  7. scripts/delta-genplan-v3331.json écrit (history + subs point 2 précisé + point 5 ajouté)
Substitutions verrouillées count==1 (abandon SANS écriture si dérive). Idempotent : re-jeu = NO-OP.
"""
import hashlib
import json
import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(BASE, *a)

FICHES = [
    "skills/gen-plan/SKILL.md",
    "skills/KNOWLEDGE.md",
    "skills/@historique/historiques-par-skill/gen-plan.md",
    "skills/@mon-ecosysteme/PROMPT-ULTRA-MAITRE-ORCHESTRATION.md",
    "skills/@historique/README.md",
    "scripts/propagate-context.py",
]
DISCIPLINES = [
    "loop-engineering", "graph-engineering", "refactoring-engineering", "fleet-engineering",
    "context-engineering", "refactoring-test", "spec-driven-development", "memory-engineering",
    "harness-engineering",
]

# --- SUB 1 : définition de l'« oubli » (SKILL.md §1.5, règle d'or n°7) ---
S1_OLD = (
    "et, si un élément a été oublié — notamment à cause d'une coupure de contexte (compression, "
    "recyclage sandbox, interruption plateforme) — il RELIT les clones et sauvegardes de la discussion"
)
S1_NEW = (
    "et, si un élément a été oublié — l'« oubli » visé désigne les éléments perdus à cause d'une "
    "coupure de contexte (compression, recyclage sandbox, interruption plateforme) et que l'agent "
    "n'a que PARTIELLEMENT réussi à reconstituer (précision sémantique, directive propriétaire "
    "2026-11-04 : « ce que tu as oublié » = « les éléments oubliés à cause d'une coupure et que tu "
    "as partiellement réussi à reconstituer ») — il RELIT les clones et sauvegardes de la discussion"
)

# --- SUB 2 : reconstitution partielle ≠ mémoire complète (SKILL.md §1.5, règle d'or n°7) ---
S2_OLD = (
    "pour prendre en compte les parties oubliées, AVANT de générer ou re-générer le plan ; "
    "la relecture des clones est l'opération première de toute reprise post-coupure"
)
S2_NEW = (
    "pour prendre en compte les parties oubliées, AVANT de générer ou re-générer le plan ; "
    "une reconstitution PARTIELLE (résumé de session, mémoire résiduelle) n'est JAMAIS une "
    "mémoire complète — les parties partiellement reconstituées sont complétées par la relecture, "
    "et l'état vérifiable du disque (règle d'or n°5) prévaut sur toute reconstruction mémorielle ; "
    "la relecture des clones est l'opération première de toute reprise post-coupure"
)

V3331_SKILL = (
    "- **v3.33.1 (2026-11-04, session web-6058b3ba — directive propriétaire préalable : « prend en "
    "compte que lorsque je précise que lorsque je disais \"ce que tu as oublié\" alors je voulais "
    "dire \"les éléments oubliés à cause d'une coupure et que tu as partiellement réussi à "
    "reconstituer\". »)** : "
    "**précision sémantique de la règle d'or n°7** — l'« oubli » visé par la règle est redéfini : ce "
    "sont les éléments perdus à cause d'une coupure de contexte et que l'agent n'a que PARTIELLEMENT "
    "réussi à reconstituer ; une reconstitution PARTIELLE (résumé de session, mémoire résiduelle) "
    "n'est JAMAIS une mémoire complète — les parties partiellement reconstituées sont complétées par "
    "la relecture des clones et sauvegardes, et l'état vérifiable du disque (règle d'or n°5) prévaut "
    "sur toute reconstruction mémorielle. Preuve vivante : la reprise Task 47 post-compression (le "
    "résumé de session affirmait « règle d'or non persistée / plan non commencé » alors que le disque "
    "portait déjà v3.33.0 + plan + recensement — reconstitution partielle PARTIELLEMENT FAUSSE, "
    "corrigée par l'audit disque). PATCH — addition pure, aucun comportement modifié, description "
    "frontmatter inchangée (non-régression triggers). Cascade KO-L004 : PM v3.33.1 généré "
    "mécaniquement (delta verrouillé `scripts/delta-genplan-v3331.json` — point 2 précisé + point 5 "
    "ajouté au §1.8 + history) + SHARED/PM-INSTALL recalibrés ; PM v3.33.0 archivé @historique R4 "
    "git mv byte-identité ; recalibrage croisé : KB (en-tête + calibration), pin ECO_SKILLS, "
    "`@historique/historiques-par-skill/gen-plan.md`, lignes vives disciplines, sceaux README §5, "
    "propagation §0 v1.7.20, rescellement archive v2.3 ; replay arbitres ×2 ; plan Task 47 "
    "re-généré via v3.33.1 (KO-L005)."
)

# --- Delta PM §1.8 : point 2 précisé + point 5 ajouté ---
P2_OLD = (
    "2. **Relecture des clones** — si un élément a été oublié (notamment à cause d'une coupure de "
    "contexte : compression, recyclage sandbox, interruption plateforme), l'agent RELIT les clones "
    "et sauvegardes de la discussion (clones clone-chat, rapports finals, worklog R5, journaux) pour "
    "prendre en compte les parties oubliées, AVANT de générer ou re-générer le plan."
)
P2_NEW = (
    "2. **Relecture des clones** — si un élément a été oublié (l'« oubli » visé désigne les éléments "
    "perdus à cause d'une coupure de contexte — compression, recyclage sandbox, interruption "
    "plateforme — et que l'agent n'a que PARTIELLEMENT réussi à reconstituer ; précision "
    "sémantique, directive propriétaire 2026-11-04 : « ce que tu as oublié » = « les éléments "
    "oubliés à cause d'une coupure et que tu as partiellement réussi à reconstituer »), l'agent "
    "RELIT les clones et sauvegardes de la discussion (clones clone-chat, rapports finals, worklog "
    "R5, journaux) pour prendre en compte les parties oubliées, AVANT de générer ou re-générer le plan."
)
P5_OLD = (
    "4. **Couverture vérifiable** — chaque élément recensé ∈ {tâche du plan, livrable certifié "
    "existant, pendance consignée} ; un élément absent des trois est une dérive à corriger (E13)."
)
P5_NEW = (
    "4. **Couverture vérifiable** — chaque élément recensé ∈ {tâche du plan, livrable certifié "
    "existant, pendance consignée} ; un élément absent des trois est une dérive à corriger (E13).\n"
    "5. **Reconstitution partielle ≠ mémoire complète** — une reconstitution PARTIELLE (résumé de "
    "session, mémoire résiduelle) n'est JAMAIS une mémoire complète : les parties partiellement "
    "reconstituées sont complétées en relisant les clones et sauvegardes, et l'état vérifiable du "
    "disque (règle d'or n°5) prévaut sur toute reconstruction mémorielle (précision sémantique, "
    "directive propriétaire 2026-11-04 : « ce que tu as oublié » = « les éléments oubliés à cause "
    "d'une coupure et que tu as partiellement réussi à reconstituer »)."
)

DELTA_HISTORY = (
    "Précision sémantique de la règle d'or n°7 (directive propriétaire 2026-11-04, session "
    "web-6058b3ba — « prend en compte que lorsque je précise que lorsque je disais \"ce que tu as "
    "oublié\" alors je voulais dire \"les éléments oubliés à cause d'une coupure et que tu as "
    "partiellement réussi à reconstituer\". ») : §1.8 — point 2 précisé (l'« oubli » visé = les "
    "éléments perdus à cause d'une coupure et que l'agent n'a que partiellement réussi à "
    "reconstituer) + point 5 ajouté (une reconstitution PARTIELLE n'est jamais une mémoire "
    "complète — complétée par la relecture des clones et sauvegardes ; l'état vérifiable du disque, "
    "règle d'or n°5, prévaut sur toute reconstruction mémorielle) ; PATCH — addition pure ; "
    "description frontmatter inchangée (non-régression triggers) ; recalibrage croisé KO-L004 : "
    "SHARED §6.1, PM-INSTALL §2ter/§A.3"
)


def abandon(msg, code=1):
    print("[ABANDON] %s" % msg)
    sys.exit(code)


def lire(path):
    if not os.path.isfile(path):
        abandon("fichier introuvable : %s" % path)
    with open(path, encoding="utf-8") as f:
        return f.read()


def sub(text, motif, remplace, n, label):
    c = text.count(motif)
    if c != n:
        abandon("motif [%s] trouvé %d fois (attendu %d) : %r" % (label, c, n, motif[:70]))
    return text.replace(motif, remplace)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def main():
    plan_initial = {}
    for rel in FICHES:
        plan_initial[rel] = lire(P(rel))
    for d in DISCIPLINES:
        rel = "skills/%s/SKILL.md" % d
        plan_initial[rel] = lire(P(rel))

    # --- No-op idempotence ---
    if "version: 3.33.1" in plan_initial["skills/gen-plan/SKILL.md"]:
        print("[NO-OP] v3.33.1 déjà installée — rien à faire")
        return 0

    # --- 1. SKILL.md gen-plan ---
    t = plan_initial["skills/gen-plan/SKILL.md"]
    t = sub(t, "version: 3.33.0", "version: 3.33.1", 1, "version SKILL")
    t = sub(t, S1_OLD, S1_NEW, 1, "n°7 sub1 — définition oubli")
    t = sub(t, S2_OLD, S2_NEW, 1, "n°7 sub2 — reconstitution partielle")
    t = sub(t,
            "- **v3.33.0 (2026-11-04, session web-6058b3ba — directive propriétaire préalable :",
            V3331_SKILL + "\n- **v3.33.0 (2026-11-04, session web-6058b3ba — directive propriétaire préalable :",
            1, "ligne §5.6 v3.33.1")
    plan_initial["skills/gen-plan/SKILL.md"] = t

    # --- 2. KB ---
    t = plan_initial["skills/KNOWLEDGE.md"]
    t = sub(t, "## gen-plan v3.33.0", "## gen-plan v3.33.1", 1, "en-tête KB gen-plan")
    ancienne_cal = ("- **Dernière calibration** : montée v3.33.0 (2026-11-04, session web-6058b3ba — "
                    "gen-plan(step), directive propriétaire : règle d'or n°7")
    nouvelle_cal = (
        "- **Dernière calibration** : montée v3.33.1 (2026-11-04, session web-6058b3ba — directive "
        "propriétaire : précision sémantique de la règle d'or n°7 — « ce que tu as oublié » = « les "
        "éléments oubliés à cause d'une coupure et que tu as partiellement réussi à reconstituer » : "
        "l'« oubli » visé = les éléments perdus post-coupure PARTIELLEMENT reconstitués ; une "
        "reconstitution PARTIELLE (résumé de session, mémoire résiduelle) n'est JAMAIS une mémoire "
        "complète — les parties partiellement reconstituées sont complétées par la relecture des "
        "clones et sauvegardes, l'état vérifiable du disque (règle d'or n°5) prévaut sur toute "
        "reconstruction mémorielle ; preuve vivante : reprise Task 47 post-compression, résumé "
        "partiellement faux corrigé par audit disque) : PATCH — addition pure ; description "
        "frontmatter inchangée (non-régression triggers) ; cascade KO-L004 : PM v3.33.1 généré "
        "mécaniquement (delta verrouillé scripts/delta-genplan-v3331.json) + SHARED + PM-INSTALL "
        "recalibrés ; PM v3.33.0 archivé @historique R4 ; pin ECO_SKILLS 3.33.1 ; propagation §0 "
        "v1.7.20 ; rescellement archive v2.3 ; replay arbitres ×2 ; plan Task 47 re-généré via "
        "v3.33.1 (KO-L005). Précédent — montée v3.33.0 (2026-11-04, session web-6058b3ba — "
        "gen-plan(step), directive propriétaire : règle d'or n°7"
    )
    t = sub(t, ancienne_cal, nouvelle_cal, 1, "calibration KB")
    plan_initial["skills/KNOWLEDGE.md"] = t

    # --- 3. historiques-par-skill/gen-plan.md ---
    t = plan_initial["skills/@historique/historiques-par-skill/gen-plan.md"]
    t = sub(t,
            "> **Version vivante (corpus)** : v3.33.0 — `skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.33.0.md` (sa table §7 fait foi)",
            "> **Version vivante (corpus)** : v3.33.1 — `skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.33.1.md` (sa table §7 fait foi)",
            1, "hist. version vivante")
    arch_dir = P("skills", "@historique", "prompts-maitres", "gen-plan")
    n_archives = len([x for x in os.listdir(arch_dir) if x.endswith(".md")])
    if n_archives != 32:
        abandon("archives gen-plan : %d fichiers (attendu 32)" % n_archives)
    t = sub(t, "> **Versions archivées** : 32 PMs (v3.6.1 → v3.32.0)",
            "> **Versions archivées** : 33 PMs (v3.6.1 → v3.33.0)", 1, "hist. versions archivées")
    t = sub(t, "## Famille GEN-PLAN — 35 versions (skill : gen-plan)",
            "## Famille GEN-PLAN — 36 versions (skill : gen-plan)", 1, "hist. compte famille")
    ligne_v3330_fin = "une coupure de contexte ne peut plus faire perdre d'éléments du plan — **VERSION VIVANTE (corpus)** |"
    ligne_v3331 = (
        "| v3.33.1 | 2026-11-04 | Précision sémantique de la règle d'or n°7 (directive propriétaire, "
        "session web-6058b3ba — « ce que tu as oublié » = « les éléments oubliés à cause d'une coupure "
        "et que tu as partiellement réussi à reconstituer ») : l'« oubli » visé = les éléments perdus "
        "post-coupure PARTIELLEMENT reconstitués ; une reconstitution PARTIELLE n'est jamais une "
        "mémoire complète — complétée par la relecture des clones et sauvegardes, l'état du disque "
        "(règle d'or n°5) prévaut sur toute reconstruction mémorielle ; PATCH addition pure ; "
        "cascade KO-L004 : PM v3.33.1 (delta verrouillé scripts/delta-genplan-v3331.json), SHARED + "
        "PM-INSTALL recalibrés, PM v3.33.0 archivé R4, pin ECO_SKILLS 3.33.1, propagation §0 v1.7.20, "
        "rescellement archive v2.3, replay arbitres, plan Task 47 re-généré (KO-L005) | La règle n°7 "
        "vise précisément les éléments partiellement reconstitués — une coupure ne peut plus laisser "
        "croire à une mémoire complète — **VERSION VIVANTE (corpus)** |"
    )
    t = sub(t, ligne_v3330_fin,
            "une coupure de contexte ne peut plus faire perdre d'éléments du plan |\n" + ligne_v3331,
            1, "ligne table v3.33.1")
    plan_initial["skills/@historique/historiques-par-skill/gen-plan.md"] = t

    # --- 4. Lignes vives : disciplines + ULTRA ---
    for d in DISCIPLINES:
        rel = "skills/%s/SKILL.md" % d
        plan_initial[rel] = sub(plan_initial[rel], "gen-plan v3.33.0", "gen-plan v3.33.1", 1,
                                "ligne vive %s" % d)
    t = plan_initial["skills/@mon-ecosysteme/PROMPT-ULTRA-MAITRE-ORCHESTRATION.md"]
    t = sub(t, "PROMPT-MAITRE-GEN-PLAN-v3.33.0.md (la plus récente)",
            "PROMPT-MAITRE-GEN-PLAN-v3.33.1.md (la plus récente)", 1, "ULTRA réf PM")
    t = sub(t, "| `gen-plan` | 3.33.0 |", "| `gen-plan` | 3.33.1 |", 1, "ULTRA version")
    plan_initial["skills/@mon-ecosysteme/PROMPT-ULTRA-MAITRE-ORCHESTRATION.md"] = t

    # --- 5. @historique/README.md : sceau §5 v3.33.0 + labels ---
    t = plan_initial["skills/@historique/README.md"]
    sha33 = sha256(P("skills", "@mon-ecosysteme", "PROMPT-MAITRE-GEN-PLAN-v3.33.0.md"))
    lignes_3320 = re.findall(r"^\| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3\.32\.0\.md \| [0-9a-f]{64} \|$",
                             t, re.MULTILINE)
    if len(lignes_3320) != 1:
        abandon("sceau v3.32.0 : %d lignes (attendu 1)" % len(lignes_3320))
    t = sub(t, lignes_3320[0],
            lignes_3320[0] + "\n| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.33.0.md | %s |" % sha33,
            1, "sceau §5 v3.33.0")
    t = sub(t, "| `prompts-maitres/gen-plan/` | 32 PMs GEN-PLAN historiques (v3.6.1 → v3.32.0)",
            "| `prompts-maitres/gen-plan/` | 33 PMs GEN-PLAN historiques (v3.6.1 → v3.33.0)",
            1, "label §4 gen-plan")
    m = re.search(r"## 5\. Index des fichiers sources archivés \((\d+) PMs — sceau SHA-256\)", t)
    if not m:
        abandon("en-tête §5 README @historique introuvable")
    idx5 = t.index(m.group(0))
    n_lignes = len(re.findall(r"^\| [\w.-]+/PROMPT-MAITRE", t[idx5:], re.MULTILINE))
    if int(m.group(1)) != n_lignes:
        print("[RESORPTION] label §5 (%s) ≠ comptage mécanique (%d) — lag résorbé au passage"
              % (m.group(1), n_lignes))
    t = sub(t, m.group(0),
            "## 5. Index des fichiers sources archivés (%d PMs — sceau SHA-256)" % (n_lignes + 1),
            1, "en-tête §5 recompté")
    plan_initial["skills/@historique/README.md"] = t

    # --- 6. propagate-context.py : constantes §0 v1.7.20 ---
    t = plan_initial["scripts/propagate-context.py"]
    t = sub(t, "## §0 — Contexte Système (SHARED v1.7.19)",
            "## §0 — Contexte Système (SHARED v1.7.20)", 1, "L2 propagate")
    c3 = t.count("⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.19)")
    if c3 != 3:
        abandon("L3 propagate : %d occurrences (attendu 3 — 2 docstrings + 1 constante)" % c3)
    t = t.replace("⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.19)",
                  "⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.20)")
    t = sub(t, "Version : 2.0.1 (porte §0 SHARED v1.7.19)", "Version : 2.0.2 (porte §0 SHARED v1.7.20)",
            1, "version propagate")
    plan_initial["scripts/propagate-context.py"] = t

    # --- 7. delta-genplan-v3331.json ---
    delta = {
        "history": DELTA_HISTORY,
        "subs": [
            {"old": P2_OLD, "new": P2_NEW, "count": 1},
            {"old": P5_OLD, "new": P5_NEW, "count": 1},
        ],
    }

    # --- Écritures (tout a passé : on écrit) ---
    for rel, texte in plan_initial.items():
        with open(P(rel), "w", encoding="utf-8") as f:
            f.write(texte)
        print("[OK] %s" % rel)
    with open(P("scripts", "delta-genplan-v3331.json"), "w", encoding="utf-8") as f:
        json.dump(delta, f, indent=1, ensure_ascii=False)
    print("[OK] scripts/delta-genplan-v3331.json")
    print("Sceau v3.33.0 : %s…" % sha33[:16])
    print("Task 47 (b) précision v3.33.1 — pré-générateur : %d fichiers écrits + delta"
          % (len(plan_initial)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
