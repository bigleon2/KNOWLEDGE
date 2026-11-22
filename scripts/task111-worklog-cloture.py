#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 111 — Clôture worklog suite 157 (idempotente, parité hôte↔dépôt).

Ajoute la phrase de clôture du tour (G4-G6 : arbitres, CW --bloc PASS,
clone 23ᵉ scellé) à la FIN de l'entrée suite 157 dans les deux arbres.
R1 : no-op si la phrase de clôture est déjà présente.
"""

# ⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.45)
# SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
# Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
# Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
# Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
# Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
# Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).

from pathlib import Path

HOST = Path("/home/z/my-project")
ARBRES = [HOST / "worklog.md", HOST / "KNOWLEDGE-repo" / "worklog.md"]
MARQUEUR = "clone-chat-session-web-ecef7f80-20261120-task111.md"
CLOTURE = (
    " ; G4-G6 CLÔTURE — arbitres ALL PASS (certification 6/6 · integrity 114/114 · vpw 16/16 · "
    "answer-key plan 16/16 · triggers 101/101 0 dérive · doublons 0) · CW PROJET --bloc PASS 5/5 "
    "blocs (rapport-cw-task111-projet.md — 3 findings S4, KO-L009 prouvé mécaniquement : scan "
    "0 jeton complet sur tout le dépôt) · clone 23ᵉ scellé 8/8 S1-S8 0 secret "
    "(download/clone-chat-session-web-ecef7f80-20261120-task111.md) · commit SUIVI poussé "
    "(E15 38ᵉ) — E15 tour : 36ᵉ/37ᵉ/38ᵉ"
)


def clore() -> int:
    import json

    resultat = []
    for arbre in ARBRES:
        if not arbre.exists():
            resultat.append({"arbre": str(arbre), "statut": "ABSENT — ignoré"})
            continue
        texte = arbre.read_text(encoding="utf-8")
        if MARQUEUR in texte:
            resultat.append({"arbre": str(arbre), "statut": "NO-OP (déjà présente)"})
            continue
        idx = texte.find("suite 157, session web-ecef7f80")
        if idx == -1:
            resultat.append({"arbre": str(arbre), "statut": "ERREUR — entrée suite 157 introuvable"})
            continue
        fin_entree = texte.find("\n\n", idx)
        if fin_entree == -1:
            fin_entree = len(texte)
        texte = texte[:fin_entree] + CLOTURE + texte[fin_entree:]
        arbre.write_text(texte, encoding="utf-8")
        resultat.append({"arbre": str(arbre), "statut": "CLOTURÉE"})
    import hashlib

    parite = "N/A"
    presents = [a for a in ARBRES if a.exists()]
    if len(presents) == 2:
        h = [hashlib.md5(a.read_bytes()).hexdigest() for a in presents]
        parite = "OK" if h[0] == h[1] else f"DIVERGENCE {h[0][:8]}≠{h[1][:8]}"
    print(json.dumps({"verdict": "CLOTUREE" if any(r["statut"] == "CLOTURÉE" for r in resultat) else "NO-OP",
                      "arbres": resultat, "parite_md5": parite}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(clore())
