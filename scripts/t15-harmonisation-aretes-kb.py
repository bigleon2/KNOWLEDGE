#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""t15-harmonisation-aretes-kb.py — Harmonisation des arêtes KB (Task 15, bootstrap canonique).

Contexte : installation canonique PM-INSTALL §3.2-c (directive trace 1a1fbcf7b38c8af1) ;
l'arbitre test-coherence-interactions (§11b) rend 3 WARN — 2 asymétries de bidirectionnalité
(arêtes D004 G3 sans réciproque « Dépend de ») + 1 self-arête fantôme (token « tsi-validator »
capté par le parseur dans la parenthèse « Utilisé par »). Correction racine au CONTENU
(jamais d'arbitre masqué — KO-L003), appliquée identiquement à l'HÔTE et au DÉPÔT :
  E1 — rea-analysis « Dépend de » += tsi-validator >= v1.3.1, ghorg-cmdr >= v1.1.0 (réciproques D004) ;
  E2 — tsi-validator « Utilisé par » : reformulation « du seul tsi-validator » → « du seul arbitre »
       (élimination du token fantôme source de la self-arête) ;
  E3/E4 — notes de lignage « Dernière calibration » (règle d'or n°1 : jamais d'édition silencieuse).

Gardes : chaque motif doit apparaître EXACTEMENT 1 fois par fichier ; sinon ABANDON rc=2.
Idempotence ×2 : second passage = no-op (motifs E1/E2 déjà remplacés → détection d'état cible).
Codes retour : 0 = harmonisé · 1 = divergence host/repo après édition · 2 = motif introuvable/multiple.
"""
import sys
from pathlib import Path

HOST_KB = Path("/home/z/my-project/skills/KNOWLEDGE.md")
REPO_KB = Path("/home/z/my-project/KNOWLEDGE-repo/skills/KNOWLEDGE.md")

E1_OLD = ("- **Dépend de** : gen-plan >= v3.22.0 (campagnes d'analyse multi-étapes — "
          "chaîne inspect → analyze → rapport, tâche planifiée)")
E1_NEW = ("- **Dépend de** : gen-plan >= v3.22.0 (campagnes d'analyse multi-étapes — "
          "chaîne inspect → analyze → rapport, tâche planifiée), tsi-validator >= v1.3.1 "
          "(frontière analyse/validation — réciproque de l'arête D004 : l'analyse REA ne rend "
          "jamais de verdict TSI), ghorg-cmdr >= v1.1.0 (orthogonalité clonage/analyse — "
          "réciproque de l'arête D004 : l'analyse a posteriori ne clone jamais)")

E2_OLD = ("rea-analysis (arête de frontière analyse/validation — l'analyse rétro-ingénierie REA "
          "ne rend jamais de verdict TSI : la validation mécanique des mappings TSI relève du "
          "seul tsi-validator ; arête bidirectionnelle D004, Task 15)")
E2_NEW = ("rea-analysis (arête de frontière analyse/validation — l'analyse rétro-ingénierie REA "
          "ne rend jamais de verdict TSI : la validation mécanique des mappings relève du seul "
           "arbitre ; arête bidirectionnelle D004, Task 15)")

E3_OLD = ("cascade $FACON2 : KB + @historique/historiques-par-skill/rea-analysis.md + "
          "pin ECO_SKILLS 1.0.0 + certification locale)")
E3_NEW = ("cascade $FACON2 : KB + @historique/historiques-par-skill/rea-analysis.md + "
          "pin ECO_SKILLS 1.0.0 + certification locale) ; harmonisation arêtes Task 15-bootstrap "
          "(2026-11-21, installation canonique PM-INSTALL §3.2-c : réciproques « Dépend de » "
          "tsi-validator >= v1.3.1 + ghorg-cmdr >= v1.1.0 inscrites [arêtes D004 Task 15 — "
          "harmonisation bidirectionnelle arbitre §11b, zéro masquage], SKILL.md inchangé v1.0.0)")

E4_OLD = "golden NISYSTEM non-régression (valide PASS / invalide FAIL 8 catégories)."
E4_NEW = ("golden NISYSTEM non-régression (valide PASS / invalide FAIL 8 catégories). ; "
          "reformulation Task 15-bootstrap (2026-11-21, installation canonique PM-INSTALL : "
          "description de l'arête rea-analysis en « Utilisé par » reformulée — « du seul arbitre » "
          "au lieu de « du seul tsi-validator » : le token dupliquait le nom du skill dans la "
          "parenthèse et générait une self-arête fantôme à l'arbitre §11b — cause racine traitée "
          "au contenu, jamais d'arbitre masqué)")


def etat_cible(texte):
    """Vrai si les 4 éditions sont déjà appliquées (idempotence ×2)."""
    return (E1_NEW in texte and E2_NEW in texte and E3_NEW in texte and E4_NEW in texte)


def appliquer(texte, etiquettes):
    for nom, ancien, nouveau in etiquettes:
        n = texte.count(ancien)
        if n != 1:
            print(f"ÉCHEC garde : motif {nom} présent {n} fois (attendu 1)")
            return None
        texte = texte.replace(ancien, nouveau, 1)
    return texte


def main():
    host = HOST_KB.read_text(encoding="utf-8")
    repo = REPO_KB.read_text(encoding="utf-8")
    if host != repo:
        print("ÉCHEC : KB hôte et dépôt divergent AVANT édition")
        return 2
    if etat_cible(host):
        print("[DÉJÀ] état cible présent (idempotence ×2 — no-op)")
        return 0
    etiq = [("E1", E1_OLD, E1_NEW), ("E2", E2_OLD, E2_NEW),
            ("E3", E3_OLD, E3_NEW), ("E4", E4_OLD, E4_NEW)]
    host2 = appliquer(host, etiq)
    if host2 is None:
        return 2
    repo2 = appliquer(repo, etiq)
    if repo2 is None:
        return 2
    if host2 != repo2:
        print("ÉCHEC : divergence host/repo APRÈS édition")
        return 1
    HOST_KB.write_text(host2, encoding="utf-8")
    REPO_KB.write_text(repo2, encoding="utf-8")
    print("[OK] 4 éditions appliquées identiquement hôte + dépôt "
          f"(host {len(host)}→{len(host2)} octets)")
    print("VERDICT : harmonisation arêtes KB appliquée (idempotente)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
