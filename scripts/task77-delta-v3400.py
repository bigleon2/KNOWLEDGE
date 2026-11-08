#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Task 77 G2 / T2.2.2 — Construction du delta verrouillé v3.40.0 pour la
génération mécanique du PM (scripts/generer-pm-skill.py --delta).

Les textes des subs miroirs §9.7 (journal-versions) et §9.10
(protocoles-detailles) sont EXTRAITS DES FICHIERS AMENDÉS — garantie de
cohérence byte entre la forme installée (references/) et l'intégral embarqué
au PM. À exécuter APRÈS task77-amendement-v3400.py.
"""
import json
import re
import sys
from pathlib import Path

R = Path("/home/z/my-project/KNOWLEDGE-repo")
PROTO = R / "skills/gen-plan/references/protocoles-detailles.md"
JOURNAL = R / "skills/gen-plan/references/journal-versions.md"
OUT = R / "scripts/delta-genplan-v3400.json"

proto = PROTO.read_text(encoding="utf-8")
i = proto.find("### Extension v3.40.0")
if i < 0:
    print("ABANDON : extension v3.40.0 absente de protocoles-detailles.md — "
          "exécuter task77-amendement-v3400.py d'abord")
    sys.exit(2)
ext = proto[i:].rstrip("\n")  # du titre « Extension v3.40.0 » à la fin du fichier

journal = JOURNAL.read_text(encoding="utf-8")
m = re.findall(r"^- \*\*v3\.39\.0 \([^\n]*$", journal, re.M)
if len(m) != 1:
    print("ABANDON : entrée v3.39.0 migrée introuvable dans journal-versions.md (%d trouvée)" % len(m))
    sys.exit(2)
entree = m[0]

NOTE = ("> **Mécanique de migration (v3.39.0)** : le SKILL.md §5.6 ne conserve que l'entrée "
        "COURANTE ; à chaque montée de version suivante, l'entrée courante migre ici "
        "(R4 byte-identité) et la nouvelle prend sa place inline.")

PHILO4_PM_OLD = (
    "4. **Parallélisation par défaut des tâches ET des commandes sur preuve d'indépendance** "
    "(inversion v3.24.0 ; extension aux commandes v3.32.0 — directive propriétaire 2026-11-02) — "
    "Les tâches ET les commandes (invocations d'outils lancées en un seul message multi-outils, "
    "vagues de flotte) PROUVÉES indépendantes (aucune écriture partagée, aucune dépendance d'ordre) "
    "s'exécutent en PARALLÈLE PAR DÉFAUT : le Graph Diamond s'ouvre automatiquement dès que la "
    "preuve d'indépendance existe (E9-E14). L'exécution série est l'exception justifiée et "
    "tracée : dépendance d'ordre, écriture partagée, verdict resource-monitor SERIE/PAUSE, "
    "profil ECO/VIEUX PC."
)
PHILO4_PM_NEW = PHILO4_PM_OLD + (
    " **ÉMISSION (v3.40.0 — protocole, trace 1a1ba66f3aff26e9)** : les appels indépendants sont "
    "émis ENSEMBLE dans un même bloc multi-outils (fan-out) ; la concurrence Bash VRAIE s'obtient "
    "au sein d'UNE invocation (`cmd1 & cmd2 & wait`, `xargs -P`) — le shell persistant sérialise "
    "les commandes Bash d'un même bloc (mesuré Task 77 : 4×sleep 2 → départs échelonnés en bloc, "
    "2,00 s en jobs &) ; bornes ≤ 4/vague (G-RES), preuve d'indépendance légère, tracé allégé — "
    "intégral : §9.10 (Extension v3.40.0)."
)

ROW_OLD = ("| **Graph Diamond** | **E9-E14** | Parallélisation PAR DÉFAUT des tâches ET commandes "
           "prouvées indépendantes (le série est l'exception justifiée — philosophie #4 v3.24.0, "
           "extension aux commandes v3.32.0) — tracée au worklog | `references/graph-diamond-pattern.md` |")
ROW_NEW = ("| **Graph Diamond** | **E9-E14** | Parallélisation PAR DÉFAUT des tâches ET commandes "
           "indépendantes (série = exception justifiée — #4 v3.24.0/v3.32.0/v3.40.0 émission : "
           "fan-out bloc + `&`+`wait`) — tracé worklog | `references/graph-diamond-pattern.md` |")

PM_TAIL_OLD = "jamais présumé).\n```"
PM_TAIL_NEW = "jamais présumé).\n\n---\n\n" + ext + "\n```"

HISTORY = (
    "PROTOCOLE D'ÉMISSION PARALLÈLE (directive trace 1a1ba66f3aff26e9 : « vérifie que mon "
    "écosystème te permet de lancer 4 commandes en parallèle … fais en sorte qu'il te permette "
    "de le faire ») — opérationnalisation de la philosophie #4 (doctrine présente "
    "v3.24.0/v3.32.0, jamais appliquée : plans Tasks 70-76 100 % série, zéro vague tracée) : "
    "fan-out multi-appels (un même bloc, tous outils) + concurrence intra-commande "
    "(`&`+`wait`/`xargs -P` ; mesure Task 77 : 4×sleep 2 → 2,00 s vs 8,00 s — le shell "
    "persistant sérialise les Bash d'un même bloc) ; bornes ≤ 4/vague (G-RES), preuve "
    "d'indépendance légère, exceptions série inchangées, tracé worklog allégé (une "
    "ligne/vague) — SKILL.md §1.2bis + §1.4 #4 (compensation byte < 30 Kio, description "
    "inchangée) ; intégral : §9.10 protocoles-detailles (Extension v3.40.0) + "
    "graph-diamond-pattern.md §5"
)

delta = {
    "history": HISTORY,
    "subs": [
        {"old": PHILO4_PM_OLD, "new": PHILO4_PM_NEW, "count": 1},
        {"old": ROW_OLD, "new": ROW_NEW, "count": 1},
        {"old": NOTE, "new": NOTE + "\n\n" + entree, "count": 1},
        {"old": PM_TAIL_OLD, "new": PM_TAIL_NEW, "count": 1},
    ],
}
OUT.write_text(json.dumps(delta, ensure_ascii=False, indent=1), encoding="utf-8")
print("delta écrit : %s — 4 subs verrouillées (§1.7 #4, §1.2bis, §9.7, §9.10)" % OUT)
print("extension extraite : %d caractères · entrée v3.39.0 migrée : %d caractères"
      % (len(ext), len(entree)))
