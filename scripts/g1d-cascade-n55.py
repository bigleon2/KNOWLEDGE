#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.11)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

# -*- coding: utf-8 -*-
"""Task 8 G1-d — cascade mécanique v3.23.1 :
PM généré (delta verrouillé) → archivage R4 v3.23.0 → @historique ×4 +
3 historiques par skill créés → SYNC v1.4.7 → README v2.1.5 → ULTRA →
propagation §0 v1.7.4 → re-scellement ×2 → recalibrages harnais task17/17b.
"""
import hashlib
import json
import os
import re
import subprocess
import sys

BASE = "/home/z/my-project/KNOWLEDGE"
CORPUS = BASE + "/skills/@mon-ecosysteme"
HIST = BASE + "/skills/@historique"
EDITS = 0


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


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def run(cmd, expect_rc=(0,), capture=True):
    r = subprocess.run(cmd, shell=isinstance(cmd, str), cwd=BASE,
                       capture_output=capture, text=True)
    if r.returncode not in expect_rc:
        print(r.stdout[-2000:])
        print(r.stderr[-2000:])
        raise SystemExit("ABANDON : rc=%d pour %r" % (r.returncode, cmd))
    return r


# ------------------------------------------------------------- 1. delta + PM
HISTORY = ("Correction outil + fusion discussion externe 468a4c26 (Task 8, session web-b4d7dd19 — gen-plan(step)) : "
           "refactoring-test n'est plus déclaré discipline — il est l'OUTIL de la discipline n°55 refactoring-engineering "
           "(directive propriétaire : « seul refactoring-engineering est une discipline, qui se sert de refactoring-test comme un outil ») ; "
           "refactor-guard v1.7.0 déclaré (garde-fous des opérations — lignée externe 468a4c26, base hôte v1.2.0 portée R4, 11 scripts stdlib) ; "
           "fullstack-dev inscrit au registre KB (précédent vue-upload) ; toilettage KB (3 blancs parasites) ; "
           "S4 déquotes frontmatters (17 fichiers, valeurs inchangées) ; bloc PATTERN §1.6 outil+garde-fous, table §1.6 +§3 relations "
           "(refactor-guard +1 ligne) ; SHARED v1.7.3→v1.7.4 (§7 outil + registre ×3 lignes) ; PM-INSTALL v1.6.3→v1.6.4")

SUBS = [
    {"old": "| **Refactoring engineering** | Discipline n°55 : déclaration/planification/exécution des opérations de refactoring (petites transformations préservant le comportement observable — arbitres, semver, R2/R4) ; évaluation indépendante obligatoire (anti-auto-certification) | §1.9 bloc n°55 ; E4/E7 ; E9-E14 |",
     "new": "| **Refactoring engineering** | Discipline n°55 : déclaration/planification/exécution des opérations de refactoring (petites transformations préservant le comportement observable — arbitres, semver, R2/R4) ; se sert de refactoring-test comme d'un outil ; garde-fous : refactor-guard (fusion 468a4c26) | §1.9 bloc n°55 ; E4/E7 ; E9-E14 |", "count": 1},
    {"old": "| **Refactoring test** | Discipline n°55 : détection/évaluation des situations de refactoring + graphe d'interactions (blast radius) ; verdict machine OK/PRESSION/CRITIQUE — producteur d'information, ne modifie rien | §1.9 bloc n°55 ; E4/E7 ; E9-E14 |",
     "new": "| **Refactoring test** | Outil de la discipline n°55 (non discipline — Task 8) : détection/évaluation des situations de refactoring + graphe d'interactions (blast radius) ; verdict machine OK/PRESSION/CRITIQUE — producteur d'information, ne modifie rien | §1.9 bloc n°55 ; E4/E7 ; E9-E14 |", "count": 1},
    {"old": "**Disciplines de refactoring n°55 (v3.23.0, directive propriétaire session web-b4d7dd19 : « le système de refactoring de mon écosystème déclaré et tagué en tant que discipline »)** : le système de refactoring effectif de l'écosystème (correct-work modes CIBLE/DIRECT + procédures cascade PM + arbitres mécaniques + archivage @historique R4) est déclaré comme discipline `refactoring-engineering` ; le détecteur/évaluateur `refactoring-test` (producteur d'information, ne modifie rien — anti-auto-certification) est appelable par tout élément (gen-plan, agents, disciplines, scripts). gen-plan les mobilise :",
     "new": "**Discipline de refactoring n°55 et son outil (v3.23.1 — Task 8 : correction directive propriétaire « seul refactoring-engineering est une discipline, qui se sert de refactoring-test comme un outil » ; fusion discussion externe 468a4c26 : refactor-guard v1.7.0 déclaré comme garde-fous des opérations)** : le système de refactoring effectif de l'écosystème (correct-work modes CIBLE/DIRECT + procédures cascade PM + arbitres mécaniques + archivage @historique R4) est déclaré comme discipline `refactoring-engineering` ; l'outil `refactoring-test` (producteur d'information, non discipline, ne modifie rien — anti-auto-certification) est appelable par tout élément (gen-plan, agents, disciplines, scripts) ; le garde-fous `refactor-guard` (score de risque H01-H15, sandbox, échelle rollout) est mobilisé par refactoring-engineering pendant les opérations à risque. gen-plan les mobilise :", "count": 1},
    {"old": "| Étape | Disciplines n°55 mobilisées | Mécanisme |",
     "new": "| Étape | Discipline n°55, outil et garde-fous mobilisés | Mécanisme |", "count": 1},
    {"old": "Source de vérité : SHARED §7 (n°55) ; détention orchestrée : registre décentralisé §8 de chaque skill + registre KB.",
     "new": "Source de vérité : SHARED §7 (n°55) ; détention orchestrée : registre décentralisé §8 de chaque skill + registre KB. Les opérations à risque mobilisent refactor-guard (garde-fous — fusion 468a4c26).", "count": 1},
    {"old": "| refactoring-engineering | Mobilisation n°55 (SHARED §7, bloc PATTERN:GEN-PLAN-REFACTORING-v1.0.0) | Conception/exécution des opérations de refactoring (E4/E7 + situations E9-E14) — version >= v1.0.0 |",
     "new": "| refactoring-engineering | Mobilisation n°55 (SHARED §7, bloc PATTERN:GEN-PLAN-REFACTORING-v1.0.0) | Conception/exécution des opérations de refactoring (E4/E7 + situations E9-E14) — version >= v1.0.1 |\n| refactor-guard | Garde-fous de refactoring (fusion discussion 468a4c26 — lignée externe v1.7.0) | Mobilisé par refactoring-engineering pendant les opérations à risque (score H01-H15, sandbox, rollout) ; détection de besoins (hook E13) — version >= v1.7.0 |", "count": 1},
    {"old": "| refactoring-test | Mobilisation n°55 (SHARED §7, bloc PATTERN:GEN-PLAN-REFACTORING-v1.0.0) | Détection/évaluation + graphe d'interactions (blast radius) — verdict machine, version >= v1.0.0 |",
     "new": "| refactoring-test | Outil n°55 (SHARED §7, bloc PATTERN:GEN-PLAN-REFACTORING-v1.0.0) | Détection/évaluation + graphe d'interactions (blast radius) — verdict machine, version >= v1.0.1 |", "count": 1},
]


def step_pm():
    print("— 1. PM v3.23.1 (delta verrouillé : dry-run puis réel)")
    delta_path = BASE + "/scripts/delta-genplan-v3231.json"
    if not os.path.isfile("skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.23.1.md"):
        with open(delta_path, "w", encoding="utf-8") as f:
            json.dump({"history": HISTORY, "subs": SUBS}, f, ensure_ascii=False, indent=1)
        run([sys.executable, "scripts/generer-pm-skill.py", "--generate", "gen-plan",
             "--delta", "scripts/delta-genplan-v3231.json", "--dry-run"])
        print("  [DRY-RUN OK]")
        r = run([sys.executable, "scripts/generer-pm-skill.py", "--generate", "gen-plan",
                 "--delta", "scripts/delta-genplan-v3231.json"])
        tail = [l for l in r.stdout.splitlines() if "PM" in l or "SHARED" in l or "INSTALL" in l or "couvert" in l.lower()]
        print("  " + "\n  ".join(tail[-8:]))
    else:
        print("  [NO-OP] PM v3.23.1 déjà généré")


def step_archive():
    print("— 2. Archivage R4 PM v3.23.0 (git mv byte-identité)")
    src = "skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.23.0.md"
    dst = "skills/@historique/prompts-maitres/gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.23.0.md"
    if os.path.isfile(dst):
        print("  [NO-OP] déjà archivé")
        return sha256(BASE + "/" + dst)
    h = sha256(BASE + "/" + src)
    run(["git", "mv", src, dst])
    print("  [MV] SHA-256 %s…" % h[:12])
    return h


def step_hist(pm_sha):
    global EDITS
    print("— 3. @historique (par-skill ×3 créés + gen-plan.md + autres-elements + README index)")
    # 3a. gen-plan.md : ligne v3.23.1
    p = HIST + "/historiques-par-skill/gen-plan.md"
    t = open(p, encoding="utf-8").read()
    row31 = "| v3.23.1 | 2026-10-12 | Correction outil + fusion discussion externe 468a4c26 (Task 8 — gen-plan(step), directive propriétaire « seul refactoring-engineering est une discipline, qui se sert de refactoring-test comme un outil ») : bloc PATTERN §1.6 outil+garde-fous, table §1.6 +§3 relations (refactor-guard +1), fullstack-dev inscrit, toilettage KB, S4 déquotes ×17 ; SHARED v1.7.4 (§7 : ligne outil + registre ×3 lignes — refactoring-engineering / refactoring-test outil / refactor-guard), PM-INSTALL v1.6.4 ; v3.23.0 archivé par git mv byte-identité (SHA %s scellé index §5 README) | **VERSION VIVANTE (corpus)** |" % pm_sha[:64]
    anchor = t.index("| v3.23.0 |")
    line_end = t.index("\n", anchor)
    if "v3.23.1 |" not in t:
        t = t[:line_end + 1] + row31 + "\n" + t[line_end + 1:]
        EDITS += 1
        print("  [EDIT] gen-plan.md += v3.23.1")
    open(p, "w", encoding="utf-8").write(t)

    # 3b. 3 historiques par skill (n°55 + garde-fous — convention Task 17-B)
    h_eng = """# Historique — refactoring-engineering (discipline n°55)

> **Objet** : lignée versionnée du skill `refactoring-engineering` (convention SHARED §1.2 — @historique R4 ; une information une source : les détails vivent dans les entrées KB + SKILL.md §6).

| Version | Date | Contenu |
|---------|------|---------|
| v1.0.1 | 2026-10-12 | Task 8 (gen-plan(step), session web-b4d7dd19, fusion discussion externe 468a4c26) : calibration de déclaration — « refactoring-engineering se sert de refactoring-test comme un outil » (seule discipline n°55 — directive propriétaire) ; dependencies += refactor-guard >=1.7.0 (garde-fous des opérations D3/D4) ; §3/§8 triangulation évaluateur (refactoring-test) / garde-fous (refactor-guard) / vérificateur (correct-work) ; KB + SHARED §7 registre synchronisés |
| v1.0.0 | 2026-10-12 | Task 7 (gen-plan(step) G3/G4, session web-b4d7dd19) : matérialisation de la discipline n°55 (directive propriétaire : le système de refactoring effectif déclaré comme discipline d'engineering) ; système déclaré = correct-work v2.7.0 + procédures cascade PM + arbitres + @historique R4 (prouvé cascades v3.22.0/v3.22.1) ; sources : recherche web approfondie (Fowler, Feathers, SQALE, Tornhill, strangler/branch-by-abstraction, Janea Systems 2026) ; baseline A2 en attente QUOTA_OK |
"""
    h_test = """# Historique — refactoring-test (outil de la discipline n°55)

> **Objet** : lignée versionnée du skill `refactoring-test` (convention SHARED §1.2 — @historique R4). NB Task 8 : refactoring-test n'est PAS une discipline — il est l'outil de la discipline refactoring-engineering (n°55).

| Version | Date | Contenu |
|---------|------|---------|
| v1.0.1 | 2026-10-12 | Task 8 (gen-plan(step), session web-b4d7dd19, fusion discussion externe 468a4c26) : correction de déclaration — refactoring-test = OUTIL de la discipline n°55, non une discipline (directive propriétaire explicite) ; appelable par tout élément (gen-plan, agents, disciplines, scripts) ; frontmatter déquoté (S4) |
| v1.0.0 | 2026-10-12 | Task 7 (gen-plan(step) G3/G4, session web-b4d7dd19) : matérialisation (détecteur/évaluateur des situations de refactoring + graphe d'interactions/blast radius, verdict machine OK/PRESSION/CRITIQUE) ; bras mécanique `scripts/refactoring-test-graph.py` (M3 testable sans QUOTA — gen-plan : blast radius 14 backward / 19 forward, verdict CRITIQUE élément pivot) ; sources SQALE/Tornhill/program dependency graphs ; baseline A2 en attente QUOTA_OK |
"""
    h_guard = """# Historique — refactor-guard (garde-fous de refactoring)

> **Objet** : lignée versionnée du skill `refactor-guard` (convention SHARED §1.2 — @historique R4). Matérialisation canonique issue de la FUSION de la discussion externe 468a4c26 (Task 8, session web-b4d7dd19).

| Version | Date | Contenu |
|---------|------|---------|
| v1.7.0 | 2026-10-12 | Task 8 — CONVERGENCE de la lignée externe (discussion 468a4c26 : double-montée Tasks 23-24 de l'instance source — 6 PM v1.2.0→v1.7.0, rollout enabled échelle H15 terminale, ledger N6, verif-finale-n6 réconcilié Task 26 « périmées-par-conception ») ; matérialisation canonique = base mécanique v1.2.0 portée à l'identique (11 scripts stdlib + evals + references ×2) + calibration de provenance ; diffs v1.3.0→v1.6.0 non verbatim consignés par preuves de discussion (R4 — réserve : PMs externes non portés, extension generer-pm 3→4 familles = décision propriétaire D009 reportée) ; arêtes bidirectionnelles ×7 (gen-plan hook E13, refactoring-engineering garde-fous, correct-work validation, resource-monitor, graph/spec/harness/loop) |
| v1.2.0 | 2026-10-10 | Première exécution N1 shadow réelle (3 cibles vivantes) + calibration grille #token §2.5 ; scripts/shadow_run.py (self-tests 79/79 ×2) — version d'origine du port hôte (contenu intégré à l'identique) |
| v1.1.0 | 2026-10-10 | Matérialisation des 8 modules C-SAFE-1 (config, audit_ledger H09, spec_builder H07, policy_engine H10, sandbox_runner H04, checker H05, human_gate H15, rollout H08) — chaîne script-creator → correct-py → script-reviewer |
| v1.0.0 | 2026-10-10 | Matérialisation initiale (projet « Skill Refactorisation Plan » — discussion Qwen T1-T46 : conception C05/C-SAFE-1, zéro-régression, gouvernance N0-N5) |
"""
    for rel, content in [("refactoring-engineering", h_eng), ("refactoring-test", h_test), ("refactor-guard", h_guard)]:
        p2 = "%s/historiques-par-skill/%s.md" % (HIST, rel)
        if not os.path.isfile(p2):
            open(p2, "w", encoding="utf-8").write(content)
            EDITS += 1
            print("  [CREATE] historiques-par-skill/%s.md" % rel)
        else:
            print("  [NO-OP] %s.md déjà présent" % rel)

    # 3c. autres-elements : SHARED v1.7.4 + PM-INSTALL v1.6.4 + SYNC v1.4.7 + instantané
    p3 = HIST + "/historique-autres-elements.md"
    t3 = open(p3, encoding="utf-8").read()
    row_sh = "| v1.7.4 | 2026-10-12 | §7 correction outil (ligne « Refactoring test » = outil de la discipline n°55 — Task 8, directive propriétaire) + registre scindé en 3 lignes (refactoring-engineering discipline / refactoring-test outil / refactor-guard garde-fous — fusion discussion 468a4c26) ; §6.1 référence gen-plan portée à v3.23.1 (recalibrage mécanique KO-L004 — `generer-pm-skill.py`, bump PATCH conformité semver) — session web-b4d7dd19 Task 8 gen-plan(step) |"
    t3 = sub_locked(t3, "| v1.7.3 | 2026-10-12 | §7 matérialisation des définitions normatives des 2 disciplines de refactoring n°55",
                    row_sh + "\n| v1.7.3 | 2026-10-12 | §7 matérialisation des définitions normatives des 2 disciplines de refactoring n°55",
                    "autres : SHARED v1.7.4 (insertion avant v1.7.3)")
    row_pi = "| v1.6.4 | 2026-10-12 | §2ter + §A.3 instantané rafraîchi gen-plan v3.23.1 (recalibrage mécanique KO-L004 — `generer-pm-skill.py`, bump PATCH conformité semver ; correction outil n°55 + refactor-guard/fullstack-dev inscrits) |"
    m_pi = re.search(r"^\| v1\.6\.3 \|.*$", t3, re.M)
    if m_pi and "| v1.6.4 |" not in t3:
        t3 = t3[:m_pi.start()] + row_pi + "\n" + t3[m_pi.start():]
        EDITS += 1
        print("  [EDIT] autres : PM-INSTALL v1.6.4")
    row_sy = "| v1.4.7 | 2026-10-12 | Révision Task 8 (cascade gen-plan v3.23.1 — gen-plan(step), fusion discussion 468a4c26) : propagation marqueur §0 v1.7.3→v1.7.4 (constantes recalibrées — skills + scripts + agents, idempotent ×2) |"
    m_sy = re.search(r"^\| v1\.4\.6 \|.*$", t3, re.M)
    if m_sy and "| v1.4.7 |" not in t3:
        t3 = t3[:m_sy.start()] + row_sy + "\n" + t3[m_sy.start():]
        EDITS += 1
        print("  [EDIT] autres : SYNC v1.4.7")
    t3 = sub_locked(t3, "| refactoring-engineering | v1.0.0 | refactoring-test | v1.0.0 |",
                    "| refactoring-engineering | v1.0.1 | refactoring-test | v1.0.1 |\n| refactor-guard | v1.7.0 | fullstack-dev | v1.0.0 |",
                    "autres : instantané KB n°55 + fusion")
    open(p3, "w", encoding="utf-8").write(t3)

    # 3d. README @historique : index §5 += v3.23.0
    p4 = HIST + "/README.md"
    t4 = open(p4, encoding="utf-8").read()
    if "PROMPT-MAITRE-GEN-PLAN-v3.23.0.md" not in t4:
        row = "| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.23.0.md | %s |" % pm_sha
        anchor4 = "| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.22.1.md |"
        i4 = t4.index(anchor4)
        le4 = t4.index("\n", i4)
        t4 = t4[:le4 + 1] + row + "\n" + t4[le4 + 1:]
        EDITS += 1
        print("  [EDIT] README @historique : index §5 += v3.23.0")
    open(p4, "w", encoding="utf-8").write(t4)


def step_sync_readme():
    global EDITS
    print("— 4. SYNC-CONTEXT v1.4.7 + README @mon-ecosysteme v2.1.5")
    p = CORPUS + "/SYNC-CONTEXT.md"
    t = open(p, encoding="utf-8").read()
    t = sub_locked(t, "> **Version** : 1.4.6", "> **Version** : 1.4.7", "SYNC : version 1.4.7")
    rev = "> **Révision v1.4.7 (2026-10-12, cascade gen-plan v3.23.1 — session web-b4d7dd19 Task 8 gen-plan(step), fusion discussion externe 468a4c26, KO-L004)** : état du corpus recalibré — PM GEN-PLAN v3.23.1 vivant (correction outil n°55 : refactoring-test = outil de la discipline refactoring-engineering — directive propriétaire ; refactor-guard v1.7.0 garde-fous déclaré, fullstack-dev inscrit), v3.23.0 archivé en `skills/@historique/prompts-maitres/gen-plan/` par `git mv` byte-identité (19 PMs GEN-PLAN archivés) ; propagation du marqueur §0 v1.7.3→v1.7.4 recalibrée (constantes `propagate-context.py`) et exécutée (idempotent ×2) ; recalibrage croisé inclus (SHARED v1.7.4 §6.1 + §7 outil/registre ×3, PM-INSTALL v1.6.4, KB entrée gen-plan + 2 entrées n°55 corrigées + refactor-guard + fullstack-dev + réciproques ×6, ULTRA régénéré, README @mon-ecosysteme v2.1.5, ECO_SKILLS arbitre 3.23.1/1.0.1/1.0.1/1.7.0/1.0.0, @historique ×3 par-skill créés + index §5)."
    if "Révision v1.4.7" not in t:
        anchor = "> **Révision v1.4.6"
        i = t.index(anchor)
        t = t[:i] + rev + "\n" + t[i:]
        EDITS += 1
        print("  [EDIT] SYNC : révision v1.4.7")
    open(p, "w", encoding="utf-8").write(t)

    p2 = CORPUS + "/README.md"
    t2 = open(p2, encoding="utf-8").read()
    t2 = sub_locked(t2, "> **Version** : 2.1.4", "> **Version** : 2.1.5", "README : version 2.1.5")
    rev2 = "> **Révision v2.1.5 (cascade gen-plan v3.23.1, session web-b4d7dd19 Task 8 gen-plan(step) — fusion discussion externe 468a4c26)** : PM GEN-PLAN v3.23.1 vivant (correction outil n°55 — refactoring-test = outil de la discipline refactoring-engineering, directive propriétaire), v3.23.0 archivé (19 PMs GEN-PLAN) ; SHARED v1.7.4 (§7 : outil + registre ×3 lignes), PM-INSTALL v1.6.4 ; KB 32 entrées (+refactor-guard v1.7.0 garde-fous, +fullstack-dev — fusion 468a4c26 ; n°55 corrigées) ; propagation §0 v1.7.4 (idempotent ×2) ; arborescence §2 recalibrée."
    if "Révision v2.1.5" not in t2:
        i2 = t2.index("> **Révision v2.1.4")
        t2 = t2[:i2] + rev2 + "\n" + t2[i2:]
        EDITS += 1
        print("  [EDIT] README : révision v2.1.5")
    t2 = sub_locked(t2, "│   ├── PROMPT-MAITRE-GEN-PLAN-v3.23.0.md", "│   ├── PROMPT-MAITRE-GEN-PLAN-v3.23.1.md",
                    "README : arborescence PM v3.23.1")
    t2 = sub_locked(
        t2,
        "9 skills écosystème + 71 skills métier + 6 skills de discipline — dont les 2 disciplines de refactoring n°55).",
        "9 skills écosystème + 71 skills métier + 6 skills de discipline — dont la discipline de refactoring n°55 refactoring-engineering (refactoring-test = son outil, non discipline — Task 8) ; + refactor-guard (garde-fous) et fullstack-dev inscrits au registre, fusion discussion 468a4c26).",
        "README : ligne 16 n°55 corrigée")
    open(p2, "w", encoding="utf-8").write(t2)


def step_ultra():
    print("— 5. ULTRA régénéré")
    r = run([sys.executable, BASE + "/scripts/gen-ultra-maitre.py"])
    print("  " + "\n  ".join([l for l in r.stdout.splitlines() if l.strip()][-3:]))


def step_propagation():
    print("— 6. Propagation §0 v1.7.4")
    p = BASE + "/scripts/propagate-context.py"
    t = open(p, encoding="utf-8").read()
    n = t.count("v1.7.3")
    t2 = t.replace("v1.7.3", "v1.7.4")
    open(p, "w", encoding="utf-8").write(t2)
    print("  [EDIT] constantes propagate-context : %d occurrence(s) v1.7.3→v1.7.4" % n)
    r = run([sys.executable, p])
    print("  " + "\n  ".join([l for l in r.stdout.splitlines() if l.strip()][-4:]))
    r2 = run([sys.executable, p])
    print("  [IDEMPOTENCE] 2e passe : " + " / ".join([l for l in r2.stdout.splitlines() if l.strip()][-2:]))


def step_rescellement():
    print("— 7. Re-scellement archive ×2 (round-trip)")
    for i in (1, 2):
        r = run([sys.executable, BASE + "/scripts/task21-f2-rebuild-archive.py"])
        last = [l for l in r.stdout.splitlines() if l.strip()][-2:]
        print("  passe %d : %s" % (i, " / ".join(last)))


def step_harnais():
    print("— 8. Recalibrages harnais task17 / task17b")
    p = BASE + "/scripts/task17-answer-key-check.py"
    t = open(p, encoding="utf-8").read()
    t = t.replace("SHARED v1.7.3", "SHARED v1.7.4").replace('"**Version** : 1.4.6"', '"**Version** : 1.4.7"')
    open(p, "w", encoding="utf-8").write(t)
    print("  [EDIT] task17 : v1.7.4 + SYNC 1.4.7")
    p2 = BASE + "/scripts/task17b-answer-key-check.py"
    t2 = open(p2, encoding="utf-8").read()
    m = re.search(r"sum\(1 for l in gp\.splitlines\(\) if l\.startswith\(\"\\| v\"\)\) == (\d+)", t2)
    if m:
        old = m.group(0)
        new = m.group(0).replace("== %s" % m.group(1), "== %d" % (int(m.group(1)) + 1))
        t2 = t2.replace(old, new)
        print("  [EDIT] task17b C02 : lignes de versions %s→%d" % (m.group(1), int(m.group(1)) + 1))
    m2 = re.search(r'readme\.count\("PROMPT-MAITRE-"\) == (\d+)', t2)
    if m2:
        old2 = m2.group(0)
        new2 = m2.group(0).replace("== %s" % m2.group(1), "== %d" % (int(m2.group(1)) + 1))
        t2 = t2.replace(old2, new2)
        print("  [EDIT] task17b C12 : occurrences PM %s→%d" % (m2.group(1), int(m2.group(1)) + 1))
    open(p2, "w", encoding="utf-8").write(t2)


def main():
    print("=== Task 8 G1-d — cascade mécanique v3.23.1 ===")
    step_pm()
    pm_sha = step_archive()
    step_hist(pm_sha)
    step_sync_readme()
    step_ultra()
    step_propagation()
    step_rescellement()
    step_harnais()
    print("=== G1-d OK — %d éditions ===" % EDITS)


if __name__ == "__main__":
    main()
