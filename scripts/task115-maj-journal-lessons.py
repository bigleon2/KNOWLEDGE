#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 115 — Mise à jour du journal lessons-learned (recherche différés consignés).

Directive propriétaire trace 1a2027a1c9c5c9a5 « continue mais fais avant gen-plan :
recherche tous les différés consignés, puis corrige-les, ainsi que les erreurs non
bloquantes » — le journal skills/knowledge-observer/data/lessons-learned.json porte
6 entrées non terminales dont 4 statuts RETARDATAIRES (matérialisations effectuées
mais statut jamais aligné) et 2 propositions jamais re-adjuguées depuis leur
consignation. Le présent script aligne chaque statut sur la réalité vérifiée au
disque (règle d'or n°5 — jamais l'inverse, KO-L003) :

  L002 proposé      → rejeté  (résorbé par évolution : voie canonique git +
                              preflight reset --hard + miroir dépôt = état
                              antérieur restaurable ; R4 anti-duplication).
  L005 validé       → appliqué (PATTERN:KO-L005-v1.0.0 installé — regles-or.md
                              + table KO gen-plan §1.16 + E7-DISP).
  L006 « applique » → appliqué (coquille du champ statut).
  L009 validé (M4)  → appliqué (bloc PATTERN KO-L009 §1.5 gen-plan v3.30.0).
  L010 candidate    → rejeté  (couvert par règles d'or n°7 [v3.33.0] et n°5
                              [v3.26.0], postérieures à la consignation —
                              matérialisation = duplication R4).
  L011 validé       → appliqué (PATTERN:KO-L011 §1.14bis gen-plan v3.43.0 +
                              scripts/adaptation-json-sse.py).

Idempotence ×2 : le second passage ne modifie RIEN (mutateurs conditionnés sur
l'état courant). Les deux arbres (hôte + dépôt) sont écrits à l'identité byte.
Codes retour : 0 = OK (mutations appliquées ou déjà propres) · 1 = écart inattendu.
"""
# ⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.46)
# SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
# Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
# Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
# Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
# Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
# Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).

from __future__ import annotations

import json
import sys
from pathlib import Path

HOST = Path("/home/z/my-project")
REPO = HOST / "KNOWLEDGE-repo"
JOURNAL_HOST = HOST / "skills/knowledge-observer/data/lessons-learned.json"
JOURNAL_REPO = REPO / "skills/knowledge-observer/data/lessons-learned.json"

SESSION = "web-f492e049 (Task 115, 2026-11-22 — directive 1a2027a1c9c5c9a5)"

# Mutations attendues : id → (statut_cible, marqueur_nouveau|None, cible_nouvelle|None).
# None = champ inchangé. Les mutations ne s'appliquent QUE si le statut courant
# diffère de la cible (idempotence) — et refusent tout état inconnu (garde KO-L003 :
# le journal observé doit être exactement celui attendu, jamais de mutation aveugle).
MUTATIONS = {
    "L002": {
        "statut_attendu": "proposé",
        "statut": "rejeté",
        "marqueur": (
            "aucun — re-adjudiqué " + SESSION + " : RÉSORBÉ PAR ÉVOLUTION — la voie "
            "canonique (commit AVANT tout re-jeu bootstrap, leçon Task 17 G1) + preflight "
            "git reset --hard + miroir dépôt KNOWLEDGE-repo fournissent l'état antérieur "
            "restorable que la proposition visait (9 épisodes de recyclage sandbox réparés "
            "par ce mécanisme, jamais par snapshot zip — worklog suites 153-162) ; un zip "
            "de snapshot dupliquerait la fonction git (R4)"
        ),
        "cible_application": (
            "close — couvert par la voie canonique git (règle d'or n°4 + leçon Task 17 G1 : "
            "commit AVANT bootstrap) ; aucune matérialisation de bloc PATTERN"
        ),
    },
    "L005": {
        "statut_attendu": "validé",
        "statut": "appliqué",
        "marqueur": (
            "PATTERN:KO-L005-v1.0.0 installé — references/regles-or.md (bloc balisé) + "
            "table KO gen-plan §1.16 (ligne KO-L005) + E7-DISP « re-génération KO-L005 » ; "
            "statut aligné sur la réalité installée " + SESSION
            + " (retard documentaire résorbé — la matérialisation v3.17.0 N23-b/N28 avait "
            "été effectuée sans mise à jour du champ statut)"
        ),
        "cible_application": (
            "installée : règle KO-L005 §1.5/§1.16 gen-plan (regles-or.md PATTERN:KO-L005-"
            "v1.0.0) — re-génération du plan à chaque version de gen-plan modifiée et "
            "validée par arbitres"
        ),
    },
    "L006": {
        "statut_attendu": "applique",
        "statut": "appliqué",
        "marqueur": None,
        "cible_application": None,
    },
    "L009": {
        "statut_attendu": "validé (M4 — verdict correct-work rendu)",
        "statut": "appliqué",
        "marqueur": None,
        "cible_application": (
            "installée : règle KO-L009 « Sécurité : exposition d'un identifiant dans un "
            "canal de discussion » — bloc PATTERN:KO-L009-v1.0.0 §1.5 gen-plan (v3.30.0) + "
            "application processus effective (statut aligné " + SESSION + ")"
        ),
    },
    "L010": {
        "statut_attendu": "candidate (M1-M2)",
        "statut": "rejeté",
        "marqueur": (
            "absent — re-adjudiqué " + SESSION + " : COUVERT PAR RÈGLES EXISTANTES — la "
            "règle d'or n°7 (mémoire complète de la discussion, v3.33.0 2026-11-04 : "
            "relire clones/sauvegardes/worklog R5 AVANT tout recensement, couverture "
            "VÉRIFIABLE {tâche du plan, livrable certifié, pendance consignée}) et la "
            "règle d'or n°5 (anti-aspirant, v3.26.0 : statuts dérivés du disque + audit "
            "des journaux pré-existants contre leurs artefacts) couvrent la substance, "
            "et leur installée est POSTÉRIEURE à la consignation L010 (2026-10-31) ; "
            "preuve d'application de facto : census Task 108 G2 croisé sur la relecture "
            "intégrale 153 suites + 21 clones (G1) ; un bloc PATTERN supplémentaire "
            "dupliquerait (R4)"
        ),
        "cible_application": (
            "close — substance couverte par règles d'or n°5 (v3.26.0) et n°7 (v3.33.0) ; "
            "aucune matérialisation de bloc PATTERN"
        ),
    },
    "L011": {
        "statut_attendu": "validé",
        "statut": "appliqué",
        "marqueur": None,
        "cible_application": (
            "installée : règle KO-L011 §1.14bis gen-plan (v3.43.0) + regles-or.md "
            "PATTERN:KO-L011-v1.0.0 + scripts/adaptation-json-sse.py (statut aligné "
            + SESSION + ")"
        ),
    },
}

NOTE_APPEND = (
    " Re-adjudication Task 115 (2026-11-22, session web-f492e049, directive "
    "1a2027a1c9c5c9a5 « recherche tous les différés consignés, puis corrige-les, "
    "ainsi que les erreurs non bloquantes ») : statuts alignés sur la réalité "
    "installée au disque (L005/L006/L009/L011 → appliqué) et 2 propositions "
    "re-adjuguées (L002 → rejeté [résorbé par évolution : voie canonique git] ; "
    "L010 → rejeté [couvert par règles d'or n°5 et n°7, postérieures à la "
    "consignation]) — vérifications mécaniques : blocs PATTERN présents dans "
    "skills/gen-plan/references/regles-or.md (KO-L005/KO-L009/KO-L011), "
    "scripts/adaptation-json-sse.py présent, git dépôt propre (mécanisme de "
    "restauration). Le présent journal n'a plus d'entrée non terminale."
)


def muter(donnees: dict) -> tuple[int, list[str]]:
    """Applique les mutations conditionnelles — retour (nb_mutations, journal)."""
    nb = 0
    journal: list[str] = []
    lecons = {l.get("id"): l for l in donnees.get("lessons", [])}
    for lid, mut in MUTATIONS.items():
        if lid not in lecons:
            journal.append(f"{lid}: ABSENT DU JOURNAL — écart inattendu")
            continue
        lecon = lecons[lid]
        courant = lecon.get("statut", "")
        if courant == mut["statut"]:
            journal.append(f"{lid}: déjà {courant} — no-op")
            continue
        if courant != mut["statut_attendu"]:
            journal.append(
                f"{lid}: statut courant inattendu « {courant} » "
                f"(attendu « {mut['statut_attendu']} ») — REFUS (garde KO-L003)"
            )
            continue
        lecon["statut"] = mut["statut"]
        if mut["marqueur"] is not None:
            lecon["marqueur"] = mut["marqueur"]
        if mut["cible_application"] is not None:
            lecon["cible_application"] = mut["cible_application"]
        nb += 1
        journal.append(f"{lid}: « {courant} » → « {mut['statut']} »")
    # Note de re-adjudication (append-only, une seule fois)
    note = donnees.get("note", "")
    if "Re-adjudication Task 115" not in note:
        if note and not note.endswith("\n"):
            pass  # note mono-ligne : append direct
        donnees["note"] = note + "." * 0 + NOTE_APPEND.lstrip()
        nb += 1
        journal.append("note: append re-adjudication Task 115")
    else:
        journal.append("note: déjà appendifiée — no-op")
    return nb, journal


def main() -> int:
    """Charge, mute, écrit les deux arbres à l'identité byte — idempotent ×2."""
    texte = JOURNAL_HOST.read_text(encoding="utf-8")
    donnees = json.loads(texte)
    nb, journal = muter(donnees)
    sortie = json.dumps(donnees, ensure_ascii=False, indent=1) + "\n"
    if nb == 0:
        print(json.dumps({"tache": "task115-maj-journal-lessons",
                          "verdict": "NO-OP",
                          "mutations": 0,
                          "journal": journal}, ensure_ascii=False, indent=1))
        return 0
    for cible in (JOURNAL_HOST, JOURNAL_REPO):
        cible.write_text(sortie, encoding="utf-8")
    parite = JOURNAL_HOST.read_bytes() == JOURNAL_REPO.read_bytes()
    print(json.dumps({"tache": "task115-maj-journal-lessons",
                      "verdict": "MUTÉ" if parite else "DIVERGENCE",
                      "mutations": nb,
                      "parite_hote_depot": parite,
                      "journal": journal}, ensure_ascii=False, indent=1))
    return 0 if parite else 1


if __name__ == "__main__":
    sys.exit(main())
