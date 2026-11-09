#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.37)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).
"""

"""Task 71 G1 — cascade KO-L004 (après génération mécanique PM v3.37.2).

Étapes : (1) archive R4 du PM v3.37.1, (2) pin ECO_SKILLS 3.37.2,
(3) entrée KB gen-plan v3.37.2, (4) historique-par-skill v3.37.2,
(5) sync dépôt (miroir source R4), liste des fichiers modifiés.
Python stdlib uniquement — idempotent par gardes count==1.
"""
import json
import re
import shutil
import subprocess
from pathlib import Path

BASE = Path("/home/z/my-project")
HOST = BASE
REPO = BASE / "KNOWLEDGE-repo"

NOUVELLE = "3.37.2"
ANCIENNE = "3.37.1"

# ---------- 1. Archive R4 du PM supplanté ----------
pm_vieux_h = HOST / "skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.37.1.md"
pm_vieux_r = REPO / "skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.37.1.md"
dest_h = HOST / "skills/@historique/prompts-maitres/gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.37.1.md"
dest_r = REPO / "skills/@historique/prompts-maitres/gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.37.1.md"
if pm_vieux_h.exists():
    shutil.move(str(pm_vieux_h), str(dest_h))
    print("[1] archive hôte : PM v3.37.1 → @historique/prompts-maitres/gen-plan/")
if pm_vieux_r.exists():
    subprocess.run(["git", "-C", str(REPO), "mv",
                    "skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.37.1.md",
                    "skills/@historique/prompts-maitres/gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.37.1.md"],
                   check=True, capture_output=True)
    print("[1] archive dépôt : git mv OK")

# ---------- 2. Pin ECO_SKILLS ----------
for integ in [HOST / "scripts/check-ecosysteme-integrity.py", REPO / "scripts/check-ecosysteme-integrity.py"]:
    t = integ.read_text(encoding="utf-8")
    motif = '"gen-plan": "3.37.1",'
    if t.count(motif) == 1:
        t = t.replace(motif, '"gen-plan": "%s",' % NOUVELLE)
        integ.write_text(t, encoding="utf-8")
        print("[2] pin ECO_SKILLS gen-plan → %s : %s" % (NOUVELLE, integ))
    elif '"gen-plan": "%s",' % NOUVELLE in t:
        print("[2] pin déjà à jour : %s" % integ)
    else:
        raise SystemExit("pin introuvable : %s" % integ)

# ---------- 3. Entrée KB ----------
CALIBRATION = ("**Dernière calibration** : montée v3.37.2 (2026-11-08, Task 71 G1 — directive propriétaire : « tu communiques à nouveau depuis quelques instants dans d'autres langues que le français […] "
"durcis l'application de cette règle au sein de mon écosystème pour que cette erreur ne se reproduise plus ») : **durcissement règle d'or n°6** — portée MÉCANIQUE étendue à TOUT texte produit par l'agent "
"(raisonnements et analyses affichés, titres et intertitres, libellés de statuts et compteurs, légendes de tableaux, blocs récapitulatifs PLAN-AFFICHE, résumés de continuation, reformulations de sorties d'outils — "
"seuls les artefacts techniques verbatim [chemins, commandes, identifiants, extraits de code, contenu de fichiers tiers, identifiants de session/trace] restent dans leur langue d'origine) ; un raisonnement interne dans une "
"autre langue est une DÉRIVE au même titre qu'une réponse, correction immédiate sans transition ; constat propriétaire → correction + worklog + durcissement de la règle ; PATCH, description frontmatter inchangée "
"(non-régression triggers) ; cascade KO-L004 : PM v3.37.2 (delta verrouillé scripts/delta-genplan-v3372.json), SHARED v1.7.32 / PM-INSTALL v1.9.8 recalibrés mécaniquement (générateur), PM v3.37.1 archivé R4, "
"pin ECO_SKILLS 3.37.2, ULTRA régénéré, replay arbitres ; précédente montée ")
for kb in [HOST / "skills/KNOWLEDGE.md", REPO / "skills/KNOWLEDGE.md"]:
    t = kb.read_text(encoding="utf-8")
    if "## gen-plan v%s" % NOUVELLE in t:
        print("[3] KB déjà à jour : %s" % kb)
        continue
    assert t.count("## gen-plan v3.37.1") == 1, kb
    t = t.replace("## gen-plan v3.37.1", "## gen-plan v3.37.2")
    ancien = "**Dernière calibration** : montée v3.37.1 ("
    assert t.count(ancien) == 1, kb
    t = t.replace(ancien, CALIBRATION + "v3.37.1 (", 1)
    kb.write_text(t, encoding="utf-8")
    print("[3] KB gen-plan v%s : %s" % (NOUVELLE, kb))

# ---------- 4. Historique-par-skill ----------
HIST_ROW = ("| v3.37.2 | 2026-11-08 | Task 71 G1 (session web-ecef7f80 — directive propriétaire : « je te signale que tu communiques à nouveau depuis quelques instants dans d'autres langues que le \"français\" "
"alors que nous avons établi une règle dans mon écosystème qui t'obliges à communiquer avec moi en \"français\". durcis l'application de cette règle au sein de mon écosystème pour que cette erreur ne se reproduise plus. ») : "
"**durcissement règle d'or n°6** — 2ᵉ constat de dérive (textes de raisonnement affichés en anglais/chinois alors que la réponse finale était conforme) ; portée MÉCANIQUE étendue à TOUT texte produit par l'agent pendant "
"une session : raisonnements et analyses affichés au chat, titres et intertitres, libellés de statuts et compteurs, légendes de tableaux, blocs récapitulatifs PLAN-AFFICHE, résumés de continuation, reformulations de "
"sorties d'outils — TOUS en français ; seuls les artefacts techniques cités verbatim conservent leur langue d'origine ; un raisonnement interne dans une autre langue est une DÉRIVE au même titre qu'une réponse — "
"correction immédiate, sans transition ni justification différée ; constat propriétaire → correction + journalisation worklog + durcissement de la règle si faille d'application identifiée (le présent durcissement suit ce "
"cycle) ; PATCH addition pure, description frontmatter inchangée ; cascade KO-L004 : PM v3.37.2 (delta verrouillé scripts/delta-genplan-v3372.json, générateur mécanique), SHARED v1.7.32 / PM-INSTALL v1.9.8 recalibrés "
"automatiquement, PM v3.37.1 archivé R4, pin ECO_SKILLS 3.37.2, ULTRA régénéré ×2, replay arbitres ×2 | La règle de langue couvre mécaniquement tout texte produit par l'agent, raisonnements inclus — "
"**VERSION VIVANTE (corpus)** |\n")
for hist in [HOST / "skills/@historique/historiques-par-skill/gen-plan.md", REPO / "skills/@historique/historiques-par-skill/gen-plan.md"]:
    t = hist.read_text(encoding="utf-8")
    if "| v3.37.2 |" in t:
        print("[4] historique déjà à jour : %s" % hist)
        continue
    # v3.37.1 et v3.37.0 ne sont plus vivantes (dérive héritée v3.37.0 résorbée au passage)
    v371 = "Non-régression triggers prouvée par éval du second déclencheur verbatim — **VERSION VIVANTE (corpus)** |"
    v370 = "et le skill se lit sans alias-eco — **VERSION VIVANTE (corpus)** |"
    if t.count(v371) == 1:
        t = t.replace(v371, "Non-régression triggers prouvée par éval du second déclencheur verbatim — supplantée par v3.37.2 le 2026-11-08 (durcissement règle d'or n°6) |")
    if t.count(v370) == 1:
        t = t.replace(v370, "et le skill se lit sans alias-eco — supplantée par v3.37.1 le 2026-11-07 (résorption dérive héritée : la ligne n'avait pas été marquée lors de la cascade v3.37.1 — règle d'or n°5) |")
    # nouvelle ligne v3.37.2 juste après la ligne v3.37.1
    m = re.search(r"^\| v3\.37\.1 \|.*\|$", t, re.MULTILINE)
    assert m, hist
    t = t[:m.end()] + "\n" + HIST_ROW.rstrip("\n") + t[m.end():]
    # liste des fichiers archivés : 40 → 41 + v3.37.1
    assert t.count("v3.36.0 (40 fichiers, SHA-256 au §5)") == 1, hist
    t = t.replace("v3.36.0 (40 fichiers, SHA-256 au §5)",
                  "v3.36.0, v3.37.0, v3.37.1 (43 fichiers, SHA-256 au §5 — recalage mécanique Task 71 G1 : les sceaux antérieurs portaient 40 en excluant v3.37.0/v3.37.1 générés depuis)")
    hist.write_text(t, encoding="utf-8")
    print("[4] historique-par-skill v3.37.2 : %s" % hist)

# ---------- 5. Sync dépôt (fichiers corpus régénérés) ----------
SYNC = [
    "skills/gen-plan/SKILL.md",  # déjà synchronisé à l'édition
    "skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.37.2.md",
    "skills/@mon-ecosysteme/PROMPT-MAITRE-SHARED.md",
    "skills/@mon-ecosysteme/PROMPT-MAITRE-INSTALL-ECOSYSTEME.md",
    "scripts/generer-pm-report.json",
]
for rel in SYNC[1:]:
    src = HOST / rel
    dst = REPO / rel
    if src.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(src), str(dst))
        print("[5] sync dépôt : %s" % rel)

print("CASCADE-LOCALE-OK")
