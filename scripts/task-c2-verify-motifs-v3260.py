#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.13)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

# -*- coding: utf-8 -*-
"""task-c2-verify-motifs-v3260.py — Vérification mécanique des motifs du delta v3.26.0.

Vérifie que chaque motif `old` des substitutions du delta gen-plan v3.26.0
apparaît exactement `count` fois dans le PM de base (v3.25.0) — préflight
de la génération KO-L004 (sub_locked abandonnerait sinon sans écriture).
Idempotent : lecture seule, re-exécution = même verdict.
"""
import json
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PM = os.path.join(BASE, "skills", "@mon-ecosysteme", "PROMPT-MAITRE-GEN-PLAN-v3.25.0.md")
DELTA = os.path.join(BASE, "scripts", "delta-genplan-v3260.json")

PHILO4_OLD_SUFFIX = (
    "Toute vague parallèle est journalisée au worklog (Task IDs) et re-vérifiée "
    "(re-verdict resource-monitor entre les vagues, arbitre sur l'ensemble fusionné, correct-work par phase)."
)
PHILO4_NEW_SUFFIX = PHILO4_OLD_SUFFIX + (
    " **Dégradation gracieuse des vagues contre un service externe** (leçons Task 29/30, "
    "session web-fdf5963c — vérité source PM INSTALL, v3.26.0) : rate limit (429) détecté → "
    "bascule sérielle + retry/backoff + cache déterministe (verdicts figés une fois, consultés "
    "en lecture seule — jamais re-décidés) ; le code retour seul ne fait jamais foi (purge du "
    "fichier de sortie périmé avant appel — un CLI peut sortir rc=0 en erreur) ; tout jugement "
    "sémantique délégué pose la question de ROUTAGE du référentiel (jamais une appartenance de "
    "domaine) avec la référence complète, jamais tronquée."
)
REGLE5_ANCRE = (
    "5. **Continuité** — la règle change le MOYEN d'accès (clone d'abord), jamais l'objectif "
    "des tâches ; première application : session web-b93f42fa (rate-limiting API 403 contourné "
    "par clone shallow au commit épinglé)."
)
REGLE5_BLOC = REGLE5_ANCRE + """

**Règle d'or n°5 — Journal, statuts et chiffres dérivés de l'état vérifiable — anti-aspirant** (leçons Task 30, session web-fdf5963c — discussion PM INSTALL, v3.26.0) :

Opérationnalisation dans gen-plan :

1. **Anti-aspirant** — aucun statut, compteur ou chiffre pré-écrit dans un plan ou un journal : tout statut dérive d'un artefact vérifiable existant sur disque (KO-L003 étendu à l'écriture) ; un journal qui annonce des artefacts inexistants est une contamination aspirante.
2. **Reprise post-coupure** — tout journal pré-existant est audité contre ses artefacts annoncés (existence réelle sur disque) AVANT de lui faire confiance.
3. **Chiffres mécaniques** — les chiffres documentés viennent d'un recensement mécanique, jamais d'un libellé de mémoire (précédent off-by-one « 14→13 vetos », Task 30).
4. **Périmètre d'abord** — avant de qualifier des données d'aspirantes, vérifier le périmètre : dépôt et miroir hôte = deux copies distinctes (inodes différents) ; convention : dépôt = source R4, sync miroir dans cette direction uniquement.
5. **Correction honnête** — contamination avérée → réécriture des livrables vivants + corrections apposées R2 (append-only) sur @historique, jamais de masquage."""


def main():
    with open(PM, encoding="utf-8") as f:
        pm = f.read()
    delta = json.load(open(DELTA, encoding="utf-8")) if os.path.isfile(DELTA) else {"subs": []}

    # Preflight structurels (ancres des subs majeurs, avant lecture du delta)
    checks = [("philosophie #4 (suffixe)", PHILO4_OLD_SUFFIX, 1),
              ("ancre règle 5", REGLE5_ANCRE, 1)]
    for s in delta.get("subs", []):
        checks.append(("delta: %s..." % s["old"][:50], s["old"], int(s.get("count", 1))))

    echec = False
    for label, motif, attendu in checks:
        c = pm.count(motif)
        etat = "OK " if c == attendu else "ECART"
        if c != attendu:
            echec = True
        print("[%s] %-42s count=%d (attendu %d)" % (etat, label, c, attendu))

    # Projection du nombre de lignes du PM après application
    # (les subs philosophie/règle-5 sont comptés UNE SEULE FOIS — via le delta)
    proj = pm.count("\n") + 1
    proj += 1  # ligne d'historique auto (row §7)
    for s in delta.get("subs", []):
        proj += s["new"].count("\n") - s["old"].count("\n")
    print("\nProjection lignes PM v3.26.0 : %d (plage arbitre 1200-1500) → %s"
          % (proj, "OK" if 1200 <= proj <= 1500 else "HORS PLAGE"))
    return 1 if echec or not (1200 <= proj <= 1500) else 0


if __name__ == "__main__":
    sys.exit(main())
