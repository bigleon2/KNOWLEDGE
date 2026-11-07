#!/usr/bin/env python3
"""⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.31)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).
"""
"""Task 47 — règle d'or n°7 « Mémoire complète de la discussion » — cascade KO-L004, pré-générateur.
Étapes (TOUTES AVANT scripts/generer-pm-skill.py --generate) :
  1. skills/gen-plan/SKILL.md : insertion n°7 §1.5 (après n°6, avant PATTERN:KO-L009) + bump v3.33.0 + §5.6 ligne
  2. skills/KNOWLEDGE.md : en-tête gen-plan v3.33.0 + calibration Task 47 (ancienne → « Précédent — »)
  3. skills/@historique/historiques-par-skill/gen-plan.md : en-tête + ligne v3.33.0 (marqueur VERSION VIVANTE déplacé)
  4. Lignes vives : 9 disciplines + ULTRA (2 mentions vivantes) : gen-plan v3.32.0 → v3.33.0
  5. skills/@historique/README.md : sceaux §5 v3.31.0 + v3.32.0 (lag résorbé) + labels recalibrés (comptage mécanique)
  6. scripts/propagate-context.py : constantes §0 v1.7.18 → v1.7.19 (suit le bump SHARED du générateur)
  7. scripts/delta-genplan-v3330.json écrit (history + sub insertion n°7 §1.8 PM)
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

N7_SKILL = (
    "**Règle d'or n°7 — Mémoire complète de la discussion avant et pendant la planification (relire les clones et sauvegardes)** "
    "(directive propriétaire 2026-11-04, session web-6058b3ba — « je précise que tu dois te rappeler précisément de tous les éléments "
    "de la discussion que tu dois traiter dans tes taches du plan d'actions et pour cela si tu as oublié quelque chose à cause "
    "d'une coupure alors tu dois relire les clones et les sauvegardes de la discussion pour prendre en compte les parties que tu "
    "as oubliées ») : le plan d'actions couvre TOUS les éléments de la discussion que ses tâches doivent traiter — directives "
    "verbatim, tâches antérieures de la lignée, livrables, pendances, préceptes ; l'agent s'en rappelle précisément AVANT de "
    "générer (E1-E2 : recensement) et, si un élément a été oublié — notamment à cause d'une coupure de contexte (compression, "
    "recyclage sandbox, interruption plateforme) — il RELIT les clones et sauvegardes de la discussion (clones clone-chat de "
    "`download/`, rapports finals, worklog R5, journaux) pour prendre en compte les parties oubliées, AVANT de générer ou "
    "re-générer le plan ; la relecture des clones est l'opération première de toute reprise post-coupure (E1-RES : mémoire "
    "reconstituée depuis la lignée documentée + état dérivé du disque, règle d'or n°5) ; la couverture est VÉRIFIABLE : chaque "
    "élément recensé ∈ {tâche du plan, livrable certifié existant, pendance consignée} — un élément absent des trois est une "
    "dérive à corriger (E13)."
)

V3330_SKILL = (
    "- **v3.33.0 (2026-11-04, session web-6058b3ba — directive propriétaire préalable : « tu dois te rappeler précisément de "
    "tous les éléments de la discussion que tu dois traiter dans tes taches du plan d'actions et pour cela si tu as oublié "
    "quelque chose à cause d'une coupure alors tu dois relire les clones et les sauvegardes de la discussion pour prendre en "
    "compte les parties que tu as oubliées » + « recommence en utilisant le mode STEP »)** : **règle d'or n°7 — Mémoire "
    "complète de la discussion avant et pendant la planification** ajoutée au §1.5 (après n°6, avant le bloc "
    "PATTERN:KO-L009 — les règles d'or restent contiguës) : couverture totale des éléments de la discussion par le plan ; "
    "oubli dû à une coupure → relecture des clones et sauvegardes AVANT génération/re-génération ; reprise E1-RES = relecture "
    "première + état disque (règle d'or n°5) ; couverture vérifiable (élément ∈ {tâche du plan, livrable certifié, pendance "
    "consignée} — absence des trois = dérive E13). Application immédiate : relecture des clones task39/45/46 + worklog intégral "
    "AVANT la génération du plan Task 47 (mode step). Description frontmatter inchangée (non-régression triggers). Cascade "
    "KO-L004 : PM v3.33.0 généré mécaniquement (delta verrouillé `scripts/delta-genplan-v3330.json` — insertion n°7 §1.8 + "
    "history) + SHARED/PM-INSTALL recalibrés ; PM v3.32.0 archivé @historique R4 git mv byte-identité ; recalibrage croisé : "
    "KB (en-tête + calibration), pin ECO_SKILLS, `@historique/historiques-par-skill/gen-plan.md`, lignes vives disciplines, "
    "sceaux README §5 (v3.31.0/v3.32.0 — lag résorbé), propagation §0 v1.7.19, rescellement archive v2.3 ; replay arbitres ×2."
)

N7_PM = (
    "**Règle d'or n°7 — Mémoire complète de la discussion avant et pendant la planification** "
    "(ajoutée à la demande de l'utilisateur, 2026-11-04, session web-6058b3ba) :\n\n"
    "> « Je précise que tu dois te rappeler précisément de tous les éléments de la discussion que tu dois traiter dans tes "
    "taches du plan d'actions et pour cela si tu as oublié quelque chose à cause d'une coupure alors tu dois relire les clones "
    "et les sauvegardes de la discussion pour prendre en compte les parties que tu as oubliées. »\n\n"
    "Opérationnalisation dans gen-plan :\n\n"
    "1. **Couverture totale** — le plan d'actions couvre TOUS les éléments de la discussion que ses tâches doivent traiter : "
    "directives verbatim, tâches antérieures de la lignée, livrables, pendances, préceptes (E1-E2 : recensement).\n"
    "2. **Relecture des clones** — si un élément a été oublié (notamment à cause d'une coupure de contexte : compression, "
    "recyclage sandbox, interruption plateforme), l'agent RELIT les clones et sauvegardes de la discussion (clones clone-chat, "
    "rapports finals, worklog R5, journaux) pour prendre en compte les parties oubliées, AVANT de générer ou re-générer le plan.\n"
    "3. **Reprise post-coupure** — la relecture des clones est l'opération première de toute reprise E1-RES : mémoire "
    "reconstituée depuis la lignée documentée + état dérivé du disque (règle d'or n°5).\n"
    "4. **Couverture vérifiable** — chaque élément recensé ∈ {tâche du plan, livrable certifié existant, pendance consignée} ; "
    "un élément absent des trois est une dérive à corriger (E13)."
)

DELTA_HISTORY = (
    "Règle d'or n°7 — Mémoire complète de la discussion avant et pendant la planification (directive propriétaire 2026-11-04, "
    "session web-6058b3ba — « tu dois te rappeler précisément de tous les éléments de la discussion que tu dois traiter dans "
    "tes taches du plan d'actions et pour cela si tu as oublié quelque chose à cause d'une coupure alors tu dois relire les "
    "clones et les sauvegardes de la discussion pour prendre en compte les parties que tu as oubliées » + « recommence en "
    "utilisant le mode STEP ») : §1.8 — insertion n°7 (couverture totale des éléments de la discussion par le plan ; oubli dû "
    "à une coupure → relecture des clones et sauvegardes AVANT génération/re-génération ; reprise E1-RES = relecture première "
    "+ état disque règle d'or n°5 ; couverture vérifiable — élément ∈ {tâche du plan, livrable certifié, pendance consignée}, "
    "absence = dérive E13) ; description frontmatter inchangée (non-régression triggers) ; recalibrage croisé KO-L004 : SHARED "
    "§6.1, PM-INSTALL §2ter/§A.3"
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
    if "Règle d'or n°7 — Mémoire complète" in plan_initial["skills/gen-plan/SKILL.md"]:
        print("[NO-OP] règle d'or n°7 déjà installée — rien à faire")
        return 0

    # --- 1. SKILL.md gen-plan ---
    t = plan_initial["skills/gen-plan/SKILL.md"]
    t = sub(t, "version: 3.32.0", "version: 3.33.0", 1, "version SKILL")
    t = sub(t,
            "(les échanges restent en français), sauf demande explicite contraire du propriétaire.\n\n<!-- PATTERN:KO-L009-v1.0.0 -->",
            "(les échanges restent en français), sauf demande explicite contraire du propriétaire.\n\n"
            + N7_SKILL + "\n\n<!-- PATTERN:KO-L009-v1.0.0 -->",
            1, "insertion n°7 §1.5")
    t = sub(t,
            "- **v3.32.0 (2026-11-02, session web-6058b3ba — préalable propriétaire avant gen-plan :",
            V3330_SKILL + "\n- **v3.32.0 (2026-11-02, session web-6058b3ba — préalable propriétaire avant gen-plan :",
            1, "ligne §5.6 v3.33.0")
    plan_initial["skills/gen-plan/SKILL.md"] = t

    # --- 2. KB ---
    t = plan_initial["skills/KNOWLEDGE.md"]
    t = sub(t, "## gen-plan v3.32.0", "## gen-plan v3.33.0", 1, "en-tête KB gen-plan")
    ancienne_cal = ("- **Dernière calibration** : montée v3.32.0 (2026-11-02, session web-6058b3ba — "
                    "préalable propriétaire avant gen-plan :")
    nouvelle_cal = (
        "- **Dernière calibration** : montée v3.33.0 (2026-11-04, session web-6058b3ba — gen-plan(step), directive "
        "propriétaire : règle d'or n°7 « mémoire complète de la discussion — relire les clones et sauvegardes en cas "
        "d'oubli dû à une coupure » + re-génération du plan en mode STEP) : §1.5 — insertion règle d'or n°7 après n°6 "
        "(le plan couvre TOUS les éléments de la discussion à traiter : directives verbatim, tâches antérieures, "
        "livrables, pendances ; oubli post-coupure → relecture des clones et sauvegardes AVANT génération/re-génération ; "
        "reprise E1-RES = relecture première + état disque règle d'or n°5 ; couverture vérifiable — chaque élément "
        "recensé ∈ {tâche du plan, livrable certifié, pendance consignée}, absence = dérive E13) ; description "
        "frontmatter inchangée (non-régression triggers) ; cascade KO-L004 : PM v3.33.0 généré mécaniquement (delta "
        "verrouillé scripts/delta-genplan-v3330.json) + SHARED + PM-INSTALL recalibrés ; PM v3.32.0 archivé "
        "@historique R4 ; pin ECO_SKILLS 3.33.0 ; propagation §0 v1.7.19 ; rescellement archive v2.3 ; replay arbitres "
        "×2. Précédent — montée v3.32.0 (2026-11-02, session web-6058b3ba — préalable propriétaire avant gen-plan :"
    )
    t = sub(t, ancienne_cal, nouvelle_cal, 1, "calibration KB")
    plan_initial["skills/KNOWLEDGE.md"] = t

    # --- 3. historiques-par-skill/gen-plan.md ---
    t = plan_initial["skills/@historique/historiques-par-skill/gen-plan.md"]
    t = sub(t,
            "> **Version vivante (corpus)** : v3.31.0 — `skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.31.0.md` (sa table §7 fait foi)",
            "> **Version vivante (corpus)** : v3.33.0 — `skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.33.0.md` (sa table §7 fait foi)",
            1, "hist. version vivante")
    arch_dir = P("skills", "@historique", "prompts-maitres", "gen-plan")
    n_archives = len([x for x in os.listdir(arch_dir) if x.endswith(".md")])
    if n_archives != 31:
        abandon("archives gen-plan : %d fichiers (attendu 31)" % n_archives)
    t = sub(t, "> **Versions archivées** : 31 PMs (v3.6.1 → v3.31.0)",
            "> **Versions archivées** : 32 PMs (v3.6.1 → v3.32.0)", 1, "hist. versions archivées")
    t = sub(t, "## Famille GEN-PLAN — 34 versions (skill : gen-plan)",
            "## Famille GEN-PLAN — 35 versions (skill : gen-plan)", 1, "hist. compte famille")
    ligne_v3320_fin = ("Graph Diamond préservé byte-identique — **VERSION VIVANTE (corpus)** |")
    ligne_v3330 = (
        "| v3.33.0 | 2026-11-04 | Règle d'or n°7 — Mémoire complète de la discussion avant et pendant la planification "
        "(directive propriétaire, session web-6058b3ba — gen-plan(step) mode STEP) : §1.5 insertion n°7 après n°6 (le plan "
        "couvre TOUS les éléments de la discussion à traiter ; oubli dû à une coupure → relire les clones et sauvegardes "
        "AVANT génération ; reprise E1-RES = relecture première + état disque n°5 ; couverture vérifiable — dérive E13) ; "
        "cascade KO-L004 : PM v3.33.0 (delta verrouillé scripts/delta-genplan-v3330.json), SHARED + PM-INSTALL recalibrés, "
        "PM v3.32.0 archivé R4, pin ECO_SKILLS 3.33.0, propagation §0 v1.7.19, rescellement archive v2.3, replay arbitres | "
        "La mémoire de la discussion devient une obligation structurelle vérifiable — une coupure de contexte ne peut plus "
        "faire perdre d'éléments du plan — **VERSION VIVANTE (corpus)** |"
    )
    t = sub(t, ligne_v3320_fin,
            "Graph Diamond préservé byte-identique |\n" + ligne_v3330, 1, "ligne table v3.33.0")
    plan_initial["skills/@historique/historiques-par-skill/gen-plan.md"] = t

    # --- 4. Lignes vives : disciplines + ULTRA ---
    for d in DISCIPLINES:
        rel = "skills/%s/SKILL.md" % d
        plan_initial[rel] = sub(plan_initial[rel], "gen-plan v3.32.0", "gen-plan v3.33.0", 1,
                                "ligne vive %s" % d)
    t = plan_initial["skills/@mon-ecosysteme/PROMPT-ULTRA-MAITRE-ORCHESTRATION.md"]
    t = sub(t, "PROMPT-MAITRE-GEN-PLAN-v3.32.0.md (la plus récente)",
            "PROMPT-MAITRE-GEN-PLAN-v3.33.0.md (la plus récente)", 1, "ULTRA réf PM")
    t = sub(t, "| `gen-plan` | 3.32.0 |", "| `gen-plan` | 3.33.0 |", 1, "ULTRA version")
    plan_initial["skills/@mon-ecosysteme/PROMPT-ULTRA-MAITRE-ORCHESTRATION.md"] = t

    # --- 5. @historique/README.md : sceaux §5 (lag v3.31.0/v3.32.0 résorbé) + labels ---
    t = plan_initial["skills/@historique/README.md"]
    sha31 = sha256(P("skills", "@historique", "prompts-maitres", "gen-plan",
                     "PROMPT-MAITRE-GEN-PLAN-v3.31.0.md"))
    sha32 = sha256(P("skills", "@mon-ecosysteme", "PROMPT-MAITRE-GEN-PLAN-v3.32.0.md"))
    anchor_30 = "| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.30.0.md | 40baba35daab12f15d2d2cb92dbeeba1ae4884b3d38634810a4efdddf91cb375 |"
    t = sub(t, anchor_30,
            anchor_30 + "\n| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.31.0.md | %s |\n"
            "| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.32.0.md | %s |" % (sha31, sha32),
            1, "sceaux §5 v3.31.0/v3.32.0")
    t = sub(t, "| `prompts-maitres/gen-plan/` | 23 PMs GEN-PLAN historiques (v3.6.1 → v3.25.0)",
            "| `prompts-maitres/gen-plan/` | 32 PMs GEN-PLAN historiques (v3.6.1 → v3.32.0)",
            1, "label §4 gen-plan")
    m = re.search(r"## 5\. Index des fichiers sources archivés \((\d+) PMs — sceau SHA-256\)", t)
    if not m:
        abandon("en-tête §5 README @historique introuvable")
    idx5 = t.index(m.group(0))
    n_lignes = len(re.findall(r"^\| [\w.-]+/PROMPT-MAITRE", t[idx5:], re.MULTILINE))
    if int(m.group(1)) != n_lignes:
        print("[RESORPTION] label §5 (%s) ≠ comptage mécanique (%d) — lag hérité résorbé au passage"
              % (m.group(1), n_lignes))
    t = sub(t, m.group(0),
            "## 5. Index des fichiers sources archivés (%d PMs — sceau SHA-256)" % (n_lignes + 2),
            1, "en-tête §5 recompté")
    plan_initial["skills/@historique/README.md"] = t

    # --- 6. propagate-context.py : constantes §0 v1.7.19 ---
    t = plan_initial["scripts/propagate-context.py"]
    t = sub(t, "## §0 — Contexte Système (SHARED v1.7.18)",
            "## §0 — Contexte Système (SHARED v1.7.19)", 1, "L2 propagate")
    c3 = t.count("⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.18)")
    if c3 != 3:
        abandon("L3 propagate : %d occurrences (attendu 3 — 2 docstrings + 1 constante)" % c3)
    t = t.replace("⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.18)",
                  "⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.19)")
    t = sub(t, "Version : 2.0.0", "Version : 2.0.1 (porte §0 SHARED v1.7.19)", 1, "version propagate")
    plan_initial["scripts/propagate-context.py"] = t

    # --- 7. delta-genplan-v3330.json ---
    delta = {
        "history": DELTA_HISTORY,
        "subs": [{
            "old": ("4. **Primauté** — la règle prime sur la langue du message utilisateur : un message dans une autre "
                    "langue n'infirme pas la règle (les échanges restent en français), sauf demande explicite contraire "
                    "du propriétaire.\n\n**Règle KO-L009"),
            "new": ("4. **Primauté** — la règle prime sur la langue du message utilisateur : un message dans une autre "
                    "langue n'infirme pas la règle (les échanges restent en français), sauf demande explicite contraire "
                    "du propriétaire.\n\n" + N7_PM + "\n\n**Règle KO-L009"),
            "count": 1,
        }],
    }

    # --- Écritures (tout n'a passé : on écrit) ---
    for rel, texte in plan_initial.items():
        with open(P(rel), "w", encoding="utf-8") as f:
            f.write(texte)
        print("[OK] %s" % rel)
    with open(P("scripts", "delta-genplan-v3330.json"), "w", encoding="utf-8") as f:
        json.dump(delta, f, indent=1, ensure_ascii=False)
    print("[OK] scripts/delta-genplan-v3330.json")
    print("Sceau v3.31.0 : %s…" % sha31[:16])
    print("Sceau v3.32.0 : %s…" % sha32[:16])
    print("Task 47 cascade pré-générateur : %d fichiers écrits + delta" % (len(plan_initial)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
