#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.37)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0,
ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
"""

# -*- coding: utf-8 -*-
"""
Task 86 G2 — Description Optimization A10/A14 agent-engineering (directive 1a1bed51ccaf78f1
cadence 2 h tick 17:50, extinction pendance baseline A2 n°56 R3).

Contexte mesuré : baseline A2 n°56 exécutée (voie M + confirm 3 runs LLM au QUOTA_OK,
21/21 votes réels, nulls 0) — score 5/7, dérive détectée :
  - cas 6 (contrôle négatif fleet-engineering) : M=True ET L=True → faux positif 2 voies ;
    M=True est STRUCTUREL (radical `agent` ∈ strong du nom — règle arbitre V6
    `trig_m = len(hits)>=2 or bool(hits & strong)` — irreducible par description).
  - cas 7 (contrôle négatif skill-creator/agent-creator) : M=False correct, L=True → faux
    positif voie L (3/3 OUI).

Remède (protocole A10/A14 — précédents Task 18 memory-engineering, Task 25
version-management) : clause d'exclusion discriminante en description frontmatter → la voie L
(routeur LLM) vote NON sur les 2 contrôles négatifs. M-safety prouvée par SIMULATION PRÉALABLE :
aucun radical ajouté ne intersecte les toks du cas 7 (hits restent ['ecosystem'] → M=False
préservé) ; positifs 1-5 inconstructibles (`agent` ∈ strong).

Édition chirurgicale all-or-nothing, ancres count==1 :
  1. SKILL.md : version 1.0.0 → 1.1.0 (MINOR — précédent Task 18)
  2. SKILL.md : description += clause Contrôles négatifs assumés (A10/A14)
Pré-asserts : simulation M sur les 7 cas avec la NOUVELLE description AVANT écriture
(cas 1-5 True · cas 6 True structurel · cas 7 False) — abort sans écriture si écart.
Idempotent : 2e passe NO-OP (détection version 1.1.0 + clause présente).
"""
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
SKILL = BASE / "skills" / "agent-engineering" / "SKILL.md"

ANCRE_VERSION = "version: 1.0.0"
VERSION_NEW = "version: 1.1.0"
ANCRE_DESC = "fondements 2026. Spécialise la discipline agent engineering"
CLAUSE = ("fondements 2026. Contrôles négatifs assumés (A10/A14) : ne se déclenche PAS pour la "
          "coordination d'une flotte (fleet-engineering détient les patterns de coordination "
          "opérationnels) ni pour la création d'un skill (fabrique skill-creator/agent-creator) — "
          "n°56 route ces requêtes vers ces détenteurs. Spécialise la discipline agent engineering")

# ── Réplique exacte du stemmer arbitre V6 (task21-baseline-a2-all.py — voie M) ──
SUFFIXES = ["issements", "issement", "atrices", "ateur", "ations", "ation", "ements", "ement",
            "ances", "ance", "ences", "ence", "ismes", "isme", "istes", "iste",
            "ables", "able", "ibles", "ible", "euses", "euse", "eurs", "eur",
            "ités", "ité", "aux", "ales", "ale", "els", "el", "iques", "ique",
            "ives", "ive", "ifs", "if", "eaux", "eau", "ux", "ants", "ant",
            "ents", "ent", "ions", "ion", "ons", "on", "es", "e", "s", "x"]
STOP = {"le", "la", "les", "de", "des", "du", "un", "une", "et", "ou", "a", "au", "aux",
        "en", "dans", "sur", "pour", "par", "avec", "sans", "qui", "que", "ce", "cette",
        "son", "sa", "ses", "leur", "leurs", "est", "sont", "plus", "ne", "pas", "se",
        "chaque", "tout", "toute", "tous", "comme", "aux", "au", "il", "elle", "on",
        "skill", "discipline", "source", "verite", "shared", "references", "documentes",
        "fondements", "academiques", "specialise", "operationnalisation"}


def stem(w):
    w = w.lower()
    for suf in SUFFIXES:
        if w.endswith(suf) and len(w) - len(suf) >= 4:
            return w[: len(w) - len(suf)]
    return w


def norm(t):
    t = unicodedata.normalize("NFKD", t)
    return "".join(c for c in t if not unicodedata.combining(c)).lower()


def keywords_for(name, description, tags):
    kws = set(name.split("-"))
    kws |= {norm(t) for t in tags}
    for w in re.findall(r"[a-zà-ÿ]+", norm(description)):
        if w not in STOP and len(w) > 3:
            kws.add(w)
    return {stem(k) for k in kws if len(k) > 2}


def simuler_m(description):
    tags_m = re.search(r"tags:\s*\n((?:\s+-\s+.*\n)+)", SKILL.read_text(encoding="utf-8"))
    tags = re.findall(r"-\s+(.+)", tags_m.group(1)) if tags_m else []
    kws = keywords_for("agent-engineering", description, tags)
    strong = {stem(p) for p in "agent-engineering".split("-")}
    cases = json.loads((SKILL.parent / "evals" / "trigger_evals.json").read_text(encoding="utf-8"))
    out = []
    for case in cases:
        q = case["query"]
        toks = {stem(w) for w in re.findall(r"[a-zà-ÿ]+", norm(q)) if len(w) > 2}
        hits = toks & kws
        out.append(((len(hits) >= 2) or bool(hits & strong), sorted(hits)))
    return out


def extraire_description(texte):
    fm = texte.split("---")[1]
    m = re.search(r"description:\s*>-?\s*\n((?:[ \t]+.*\n)+)", fm)
    return " ".join(l.strip() for l in m.group(1).splitlines())


def sha256_fichier(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    texte = SKILL.read_text(encoding="utf-8")
    sha_avant = sha256_fichier(SKILL)

    # ── Idempotence : 2e passe = NO-OP ──
    if VERSION_NEW in texte and "Contrôles négatifs assumés (A10/A14)" in texte:
        print("NO-OP : version 1.1.0 + clause déjà présentes (idempotent)")
        return 0

    # ── Pré-asserts ancres count==1 ──
    assert texte.count(ANCRE_VERSION) == 1, f"ancre version != 1 : {texte.count(ANCRE_VERSION)}"
    assert texte.count(ANCRE_DESC) == 1, f"ancre description != 1 : {texte.count(ANCRE_DESC)}"

    # ── Pré-simulation M avec la NOUVELLE description (règle d'or n°5 — mesuré avant corrigé) ──
    desc_actuelle = extraire_description(texte)
    # reconstruction : la clause complète remplace le tronçon 'Spécialise...' dans la ligne fondements
    desc_nouvelle = desc_actuelle.replace("fondements 2026. Spécialise",
                                          "fondements 2026. Contrôles négatifs assumés (A10/A14) : ne se "
                                          "déclenche PAS pour la coordination d'une flotte "
                                          "(fleet-engineering détient les patterns de coordination "
                                          "opérationnels) ni pour la création d'un skill (fabrique "
                                          "skill-creator/agent-creator) — n°56 route ces requêtes vers "
                                          "ces détenteurs. Spécialise")
    sim = simuler_m(desc_nouvelle)
    attendu_m = [True, True, True, True, True, True, False]  # cas 6 = True STRUCTUREL (consigné)
    reels = [s[0] for s in sim]
    assert reels == attendu_m, f"pré-simulation M diverge : {reels} vs {attendu_m} — ABORT sans écriture"
    print("Pré-simulation M OK :", [sorted(s[1]) for s in sim])

    # ── Édition all-or-nothing ──
    assert texte.count("fondements 2026. Spécialise") == 1
    nouveau = texte.replace(ANCRE_VERSION, VERSION_NEW)
    assert nouveau.count(VERSION_NEW) == 1
    nouveau = nouveau.replace("fondements 2026. Spécialise", CLAUSE)
    assert nouveau.count("Contrôles négatifs assumés (A10/A14)") == 1
    # post-vérification : re-simulation depuis le texte final écrit
    SKILL.write_text(nouveau, encoding="utf-8")
    verif = extraire_description(SKILL.read_text(encoding="utf-8"))
    sim2 = simuler_m(verif)
    reels2 = [s[0] for s in sim2]
    assert reels2 == attendu_m, f"post-simulation M diverge : {reels2}"

    sha_apres = sha256_fichier(SKILL)
    print(f"ÉDITÉ : version 1.0.0 → 1.1.0 + clause A10/A14 (7 lignes description)")
    print(f"SHA-256 avant : {sha_avant}")
    print(f"SHA-256 après : {sha_apres}")
    print(f"Poids : {len(texte.encode('utf-8'))} → {len(nouveau.encode('utf-8'))} o "
          f"({len(nouveau.encode('utf-8')) - len(texte.encode('utf-8')):+d} o)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
