#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.36)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).
"""

"""Task 71 G3 — cascade KO-L004 v3.37.2 → v3.38.0 (après génération mécanique).

Archive R4 du PM v3.37.2, pin ECO_SKILLS, entrée KB, historique-par-skill,
sync dépôt, sweep §0 SHARED v1.7.33. Python stdlib — gardes count==1.
"""
import re
import shutil
import subprocess
from pathlib import Path

BASE = Path("/home/z/my-project")
HOST = BASE
REPO = BASE / "KNOWLEDGE-repo"

NOUVELLE, ANCIENNE = "3.38.0", "3.37.2"
SH_STALE, SH_VIF = "Contexte Système (SHARED v1.7.32)", "Contexte Système (SHARED v1.7.33)"

# 1. Archive R4 du PM v3.37.2
pm_vieux_h = HOST / "skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.37.2.md"
pm_vieux_r = REPO / "skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.37.2.md"
if pm_vieux_h.exists():
    shutil.move(str(pm_vieux_h), str(HOST / "skills/@historique/prompts-maitres/gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.37.2.md"))
    print("[1] archive hôte PM v3.37.2 OK")
if pm_vieux_r.exists():
    subprocess.run(["git", "-C", str(REPO), "mv",
                    "skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.37.2.md",
                    "skills/@historique/prompts-maitres/gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.37.2.md"],
                   check=True, capture_output=True)
    print("[1] archive dépôt git mv OK")

# 2. Pin ECO_SKILLS
for integ in [HOST / "scripts/check-ecosysteme-integrity.py", REPO / "scripts/check-ecosysteme-integrity.py"]:
    t = integ.read_text(encoding="utf-8")
    motif = '"gen-plan": "3.37.2",'
    if t.count(motif) == 1:
        integ.write_text(t.replace(motif, '"gen-plan": "%s",' % NOUVELLE), encoding="utf-8")
        print("[2] pin %s : %s" % (NOUVELLE, integ))
    elif '"gen-plan": "%s",' % NOUVELLE in t:
        print("[2] pin déjà à jour : %s" % integ)
    else:
        raise SystemExit("pin introuvable : %s" % integ)

# 3. Entrée KB
CALIBRATION = ("**Dernière calibration** : montée v3.38.0 (2026-11-08, Task 71 G3 — directive propriétaire : « je veux appliquer tes recommandations \"R1\" et \"R2\". analyse comment les intégrer $FACON à mon écosystème "
"(dans l'objectif d'optimiser $FACON le fonctionnement de mon écosystème pour qu'il soit $FACON2, fais des tests $FACON2 avant de les intégrer pour trouver la méthode la plus optimisée et performante pour les intégrer ») : "
"**(1) hook E5-POIDS** — arbitre de poids de chargement `scripts/poids-chargement.py` [R1 progressive disclosure : mesure Kio + #token estimés par skill, seuils OK < 12 Kio / LOURD ≥ 30 Kio / CRITIQUE ≥ 60 Kio ; skill "
"LOURD/CRITIQUE → lecture ciblée §0 + sommaire + sections dédiées, references/ à la demande — jamais de lecture intégrale par défaut ; selftest 10/10, idempotence ×2 ; rapport de priorisation download/rapport-poids-chargement-task71.md : "
"gen-plan CRITIQUE 102,8 Kio ≈ 26 312 tokens = cible n°1 de la curation R1 future] ; **(2) hook R2-CACHE** — cache de verdicts généralisé `scripts/cache-verdicts.py` [R2 : verdict figé une fois, re-jeu sans ré-appel, clé SHA-256 "
"commande + état des cibles, invalidation automatique, --force = re-exécution réelle ; selftest 12/12, idempotence ×2 ; démo mesurée sur check-ecosysteme-integrity.py : gain 440× (45,5 ms → 0,1 ms), verdict figé identique, "
"invalidation sur touch OK — preuve scripts/task71-r2-demo-preuve.json] ; MINOR additions pures, description frontmatter inchangée ; cascade KO-L004 : PM v3.38.0 (delta verrouillé scripts/delta-genplan-v3380.json), "
"SHARED v1.7.33 / PM-INSTALL v1.9.9 recalibrés mécaniquement, PM v3.37.2 archivé R4, pin ECO_SKILLS 3.38.0, ULTRA régénéré, replay arbitres ; précédente montée ")
for kb in [HOST / "skills/KNOWLEDGE.md", REPO / "skills/KNOWLEDGE.md"]:
    t = kb.read_text(encoding="utf-8")
    if "## gen-plan v%s" % NOUVELLE in t:
        print("[3] KB déjà à jour : %s" % kb)
        continue
    assert t.count("## gen-plan v3.37.2") == 1, kb
    t = t.replace("## gen-plan v3.37.2", "## gen-plan v%s" % NOUVELLE)
    ancien = "**Dernière calibration** : montée v3.37.2 ("
    assert t.count(ancien) == 1, kb
    t = t.replace(ancien, CALIBRATION + "v3.37.2 (", 1)
    kb.write_text(t, encoding="utf-8")
    print("[3] KB gen-plan v%s : %s" % (NOUVELLE, kb))

# 4. Historique-par-skill
HIST_ROW = ("| v3.38.0 | 2026-11-08 | Task 71 G3 (session web-ecef7f80 — directive propriétaire : « je veux appliquer tes recommandations \"R1\" et \"R2\". analyse comment les intégrer $FACON à mon écosystème […] "
"fais des tests $FACON2 avant de les intégrer pour trouver la méthode la plus optimisée et performante pour les intégrer ») : **(1) hook E5-POIDS** — arbitre de poids de chargement scripts/poids-chargement.py v1.0.0 [R1 : "
"progressive disclosure — le goulot réel = budget #token ; mesure par skill Kio + #token estimés (caractères/4) + references/ récursif ; verdicts OK < 12 Kio / LOURD ≥ 30 Kio / CRITIQUE ≥ 60 Kio ; skill LOURD/CRITIQUE → "
"lecture ciblée obligatoire §0 + sommaire + sections dédiées, references/ à la demande ; selftest 10/10, idempotence ×2 ; rapport de priorisation download/rapport-poids-chargement-task71.md — bilan 70 skills : 28 OK · "
"32 intermédiaires · 9 LOURD · 1 CRITIQUE ; cible n°1 = gen-plan 102,8 Kio ≈ 26 312 tokens, curation R1 future] ; **(2) hook R2-CACHE** — cache de verdicts généralisé scripts/cache-verdicts.py v1.0.0 [R2 : pattern "
"« verdict figé une fois, re-jeu sans ré-appel » ; clé SHA-256(commande + état des cibles [taille, mtime_ns]) ; invalidation automatique sur modification ; --force = re-exécution réelle (un verdict figé n'est jamais une "
"preuve en soi) ; selftest 12/12, idempotence ×2 ; démo mesurée sur check-ecosysteme-integrity.py : froid 45,5 ms → chaud 0,1 ms = gain 440×, verdict figé identique 110/110, invalidation sur touch OK — preuve "
"scripts/task71-r2-demo-preuve.json] ; MINOR additions pures (2 lignes table §1.2bis), description inchangée ; cascade KO-L004 : PM v3.38.0 (delta verrouillé scripts/delta-genplan-v3380.json, générateur mécanique — "
"WARN couverture §1.13 = faux positif hérité Task 21), SHARED v1.7.33 / PM-INSTALL v1.9.9 recalibrés, PM v3.37.2 archivé R4, pin ECO_SKILLS 3.38.0, ULTRA régénéré ×2, replay arbitres ×2 | Les deux leviers du goulot "
"réel #token sont outillés : mesure du poids de chargement à E5 + verdicts figés ré-jouables sans ré-appel — **VERSION VIVANTE (corpus)** |\n")
for hist in [HOST / "skills/@historique/historiques-par-skill/gen-plan.md", REPO / "skills/@historique/historiques-par-skill/gen-plan.md"]:
    t = hist.read_text(encoding="utf-8")
    if "| v3.38.0 |" in t:
        print("[4] historique déjà à jour : %s" % hist)
        continue
    v372 = "supplantée par v3.37.2 le 2026-11-08 (durcissement règle d'or n°6) |"
    # marquer v3.37.2 supplantée (sa ligne actuelle se termine par VERSION VIVANTE)
    m = re.search(r"^\| v3\.37\.2 \|.+\|$", t, re.MULTILINE)
    assert m, hist
    ligne = m.group(0)
    assert "VERSION VIVANTE (corpus)" in ligne, ligne[-200:]
    t = t.replace(ligne, ligne.replace("**VERSION VIVANTE (corpus)** |", "supplantée par v3.38.0 le 2026-11-08 (R1+R2 — étude Task 70) |"))
    t = t[: m.end()] + "\n" + HIST_ROW.rstrip("\n") + t[m.end():]
    t = t.replace("v3.36.0, v3.37.0, v3.37.1 (43 fichiers, SHA-256 au §5",
                  "v3.36.0, v3.37.0, v3.37.1, v3.37.2 (44 fichiers, SHA-256 au §5")
    hist.write_text(t, encoding="utf-8")
    print("[4] historique v3.38.0 : %s" % hist)

# 5. Sync dépôt des fichiers corpus régénérés + sweep §0 v1.7.33
for rel in ["skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.38.0.md",
            "skills/@mon-ecosysteme/PROMPT-MAITRE-SHARED.md",
            "skills/@mon-ecosysteme/PROMPT-MAITRE-INSTALL-ECOSYSTEME.md",
            "scripts/generer-pm-report.json"]:
    src, dst = HOST / rel, REPO / rel
    if src.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(src), str(dst))
        print("[5] sync dépôt : %s" % rel)

n_h = n_r = 0
for base in [HOST, REPO]:
    for sp in sorted((base / "skills").glob("*/SKILL.md")):
        if sp.parent.name == "@mon-ecosysteme":
            continue
        t = sp.read_text(encoding="utf-8")
        if SH_STALE in t:
            sp.write_text(t.replace(SH_STALE, SH_VIF), encoding="utf-8")
            if base is HOST:
                n_h += 1
            else:
                n_r += 1
print("[6] sweep §0 v1.7.33 : %d hôte / %d dépôt" % (n_h, n_r))
print("CASCADE-G3-OK")
