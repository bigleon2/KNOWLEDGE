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

# -*- coding: utf-8 -*-
"""
Task 78/79 G1 — Construction du delta verrouillé v3.41.0 pour la
génération mécanique du PM (scripts/generer-pm-skill.py --delta).

Les textes des subs miroirs §9.7 (journal-versions) et §9.10
(protocoles-detailles) sont EXTRAITS DES FICHIERS AMENDÉS — garantie de
cohérence byte entre la forme installée (references/) et l'intégral embarqué
au PM. À exécuter APRÈS task78-amendement-v3410.py.
"""
import json
import re
import sys
from pathlib import Path

R = Path("/home/z/my-project/KNOWLEDGE-repo")
PROTO = R / "skills/gen-plan/references/protocoles-detailles.md"
JOURNAL = R / "skills/gen-plan/references/journal-versions.md"
OUT = R / "scripts/delta-genplan-v3410.json"

proto = PROTO.read_text(encoding="utf-8")
i = proto.find("### Extension v3.41.0")
if i < 0:
    print("ABANDON : extension v3.41.0 absente de protocoles-detailles.md — "
          "exécuter task78-amendement-v3410.py d'abord")
    sys.exit(2)
ext = proto[i:].rstrip("\n")  # du titre « Extension v3.41.0 » à la fin du fichier

journal = JOURNAL.read_text(encoding="utf-8")
m = re.findall(r"^- \*\*v3\.40\.0 \([^\n]*$", journal, re.M)
if len(m) != 1:
    print("ABANDON : entrée v3.40.0 migrée introuvable dans journal-versions.md (%d trouvée)" % len(m))
    sys.exit(2)
entree = m[0]

NOTE = ("> **Mécanique de migration (v3.39.0)** : le SKILL.md §5.6 ne conserve que l'entrée "
        "COURANTE ; à chaque montée de version suivante, l'entrée courante migre ici "
        "(R4 byte-identité) et la nouvelle prend sa place inline.")

PHILO4_ANCRE = "intégral : §9.10 (Extension v3.40.0)."
PHILO4_NEW = PHILO4_ANCRE + (
    " **SONDAGE BORNÉ (v3.41.0 — trace 1a1bbf9f403a2865)** : toute inspection transverse "
    "sur l'arbre skills/ est BORNÉE — mode fichiers (-l) d'abord, greps multi-fichiers "
    "tronqués + limite de résultats, §0/contrats jamais affichés en entier (exceptions : "
    "golden-master et contrats PRE/POST, un fichier à la fois) ; mesuré : « Contexte "
    "Système » BRUT 12 207 o vs BORNÉ 3 763 o (gain ×3,2) — intégral : §9.10 "
    "(Extension v3.41.0)."
)

ROW_OLD = ("| **Graph Diamond** | **E9-E14** | Parallélisation PAR DÉFAUT des tâches ET commandes "
           "indépendantes (série = exception justifiée — #4 v3.24.0/v3.32.0/v3.40.0 émission : "
           "fan-out bloc + `&`+`wait`) — tracé worklog | `references/graph-diamond-pattern.md` |")
ROW_NEW = ROW_OLD + "\n" + (
    "| **Sondage borné** | **E9-E14** | Inspection transverse sur l'arbre skills/ TOUJOURS "
    "bornée : mode fichiers (-l) d'abord, greps multi-fichiers tronqués + limite de "
    "résultats ; §0/contrats jamais affichés en entier | `references/protocoles-detailles.md` |")

PM_TAIL_OLD = "l'exception est la file.\n```"
PM_TAIL_NEW = "l'exception est la file.\n\n---\n\n" + ext + "\n```"

HISTORY = (
    "RÈGLE DE SONDAGE BORNÉ (directive trace 1a1bbf9f403a2865 : « génère le plan du "
    "Task \"règle de sondage borné\" » ; origine : avertissement SG2.2 Task 77 « Sortie "
    "trop volumineuse (en-tête SHARED très long) ») — extension de la lecture ciblée "
    "(E5-POIDS v3.38.0) aux commandes d'inspection transverses : (1) jamais de pattern "
    "générique sur l'arbre sans mode -l ; (2) greps multi-fichiers tronqués + limite de "
    "résultats ; (3) §0/contrats jamais en entier — plages ciblées ; (4) exceptions "
    "golden-master/contrats PRE-POST. Mesures : BRUT 12 207 o / BORNÉ 3 763 o (×3,2), "
    "ligne max 1 458 o, §0 dupliqué 119 SKILL.md — SKILL.md §1.2bis rangée + §1.4 #4 "
    "(budget 30 697 o < 30 Kio tenu, compensation byte, description/§A inchangés — "
    "non-régression triggers) ; intégral : §9.10 protocoles-detailles (Extension v3.41.0)"
)

delta = {
    "history": HISTORY,
    "subs": [
        {"old": PHILO4_ANCRE, "new": PHILO4_NEW, "count": 1},
        {"old": ROW_OLD, "new": ROW_NEW, "count": 1},
        {"old": NOTE, "new": NOTE + "\n\n" + entree, "count": 1},
        {"old": PM_TAIL_OLD, "new": PM_TAIL_NEW, "count": 1},
    ],
}
OUT.write_text(json.dumps(delta, ensure_ascii=False, indent=1), encoding="utf-8")
print("delta écrit : %s — 4 subs verrouillées (§1.7 #4, §1.2bis, §9.7, §9.10)" % OUT)
print("extension extraite : %d caractères · entrée v3.40.0 migrée : %d caractères"
      % (len(ext), len(entree)))
