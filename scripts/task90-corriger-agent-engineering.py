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
Task 90 G1 T1.2.2 — Corrections chirurgicales agent-engineering v1.1.0 → v1.1.1 (PATCH)
(directive propriétaire 1a1c1dde3f6d0021 : « teste $FACON "agent-engineering" avec mon
écosystème comme entrée dans l'objectif de corriger ses failles et de l'optimiser $FACON »).

Audit T1.1.2 (failles mesurées à la lecture — règle d'or n°5, zéro faille pré-écrite) :
  F1 : SKILL.md §5 stale — « Baseline A2 : EN ATTENTE DE MESURE (v1.0.0…) » alors que
       MESURÉE Task 86 (6/7, 21/21 votes réels) — viole KO-L003/R5 (statuts dérivés du disque).
  F2 : §6 Traçabilité — entrée v1.1.0 (Task 86, Description Optimization A10/A14) ABSENTE.
  F3 : evals.json champ version "1.0.0" stale (skill v1.1.0).
  F4 : description frontmatter — doublon « la discipline agent engineering la discipline
       agent engineering » (coquille ; présente hôte+dépôt SKILL.md, ABSENTE KB = dérive
       miroir R4).
  F5 : §2 formulation « Pas de script propre en v1.0.0 » à recaler (version figée périmée).

M-safe F4 (pattern Task 86) : la suppression du doublon retire des OCCURRENCES de mots
(la/discipline = STOP ; agent/engineering présents ailleurs) → ensembles de radicaux
stemmer V6 IDENTIQUES avant/après — prouvé par SIMULATION PRÉALABLE sur les 7 cas
(verdicts [True×5, True cas 6 structurel, False cas 7]) + comparaison d'ensembles.
Édition chirurgicale all-or-nothing, ancres count==1, abort SANS écriture si écart.
Idempotent : 2e passe NO-OP (détection version 1.1.1).
"""
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
SKILL = BASE / "skills" / "agent-engineering" / "SKILL.md"
EVALS = BASE / "skills" / "agent-engineering" / "evals" / "evals.json"
KB = BASE / "skills" / "KNOWLEDGE.md"
PIN = BASE / "scripts" / "check-ecosysteme-integrity.py"
LIGNAGE = BASE / "skills" / "@historique" / "historiques-par-skill" / "agent-engineering.md"
REPO = BASE / "KNOWLEDGE-repo"
REPO_SKILL = REPO / "skills" / "agent-engineering" / "SKILL.md"
REPO_EVALS = REPO / "skills" / "agent-engineering" / "evals" / "evals.json"
REPO_KB = REPO / "skills" / "KNOWLEDGE.md"
REPO_PIN = REPO / "scripts" / "check-ecosysteme-integrity.py"
REPO_LIGNAGE = REPO / "skills" / "@historique" / "historiques-par-skill" / "agent-engineering.md"

# ── Ancres (count==1 exigé) ──────────────────────────────────────────────────
DOUBLON = ("Spécialise la discipline agent engineering la discipline agent engineering "
           "(registre")
DOUBLON_FIX = "Spécialise la discipline agent engineering (registre"
ANCRE_VIEILLE_VERSION = "version: 1.1.0"
VERSION_NEW = "version: 1.1.1"
ANCRE_S2 = "Pas de script propre en v1.0.0 (discipline de cadrage"
S2_NEW = "Pas de script propre (discipline de cadrage"
ANCRE_S5 = ("Baseline A2 : EN ATTENTE DE MESURE (v1.0.0 — protocole voie mécanique + confirm "
            "3 runs LLM à armer à la prochaine fenêtre QUOTA_OK, KO-L001 — consigné "
            "honnêtement, aucune baseline pré-écrite R3).")
S5_NEW = ("Baseline A2 : MESURÉE (Task 86 — voie mécanique + confirm 3 runs LLM au QUOTA_OK, "
          "21/21 votes réels, nulls 0 : score initial 5/7 → Description Optimization A10/A14 "
          "→ re-mesure post-opt v1.1.0 : 6/7 ; écart structurel consigné cas 6 voie M — "
          "radical « agent » ∈ strong arbitre V6, extinction = proposition future hors "
          "cadence, posture Tasks 81/82/85).")
ANCRE_S6_FIN = ("pendance structurée (précédents v1.7.0 n°54 / Task 7-8 n°55 — tâche dédiée).")
S6_AJOUT = """
- v1.1.0 (Task 86, 2026-11-09, session web-ecef7f80, directive 1a1bed51ccaf78f1 cadence 2 h tick 17:50) : Description Optimization A10/A14 — clause Contrôles négatifs assumés en description frontmatter (M-safe prouvée par simulation préalable stemmer arbitre V6) ; baseline A2 mesurée 5/7 (21/21 votes réels, QUOTA_OK) puis re-mesure post-opt 6/7 — écart structurel consigné cas 6 voie M (radical « agent » ∈ strong) ; cascade KO-L004 (KB + evals note + lignage + ULTRA + pin ECO_SKILLS).
- v1.1.1 (Task 90, 2026-11-09, session web-ecef7f80, directive 1a1c1dde3f6d0021) : corrections de consistance post-test $FACON (écosystème en entrée) — §5 staleness résorbé (baseline MESURÉE 6/7 documentée), §6 traçabilité v1.1.0 complétée, doublon description supprimé (M-safe : ensembles de radicaux stemmer V6 identiques avant/après), evals.json version alignée 1.1.1, §2 recalé versionné. PATCH — sémantique et routage inchangés."""
EVALS_VIEUX = '"version": "1.0.0"'
EVALS_NEW = '"version": "1.1.1"'
KB_EN_TETE = "## agent-engineering v1.1.0"
KB_EN_TETE_NEW = "## agent-engineering v1.1.1"
KB_CAL_ANCRE = "- **Dernière calibration** : v1.1.0 (Task 86,"
KB_CAL_NEW = ("- **Dernière calibration** : v1.1.1 (Task 90, 2026-11-09, session web-ecef7f80, "
              "directive 1a1c1dde3f6d0021 — test $FACON n°56 écosystème en entrée) : "
              "corrections de consistance F1-F5 (§5 baseline MESURÉE documentée · §6 "
              "traçabilité v1.1.0+v1.1.1 · doublon description supprimé M-safe stemmer V6 · "
              "evals.json version alignée · §2 recalé) ; précédent v1.1.0 (Task 86,")
PIN_ANCRE = '"agent-engineering": "1.1.0",  # KO-L004 (Task 86,'
PIN_NEW = ('"agent-engineering": "1.1.1",  # KO-L004 (Task 90, 2026-11-09, web-ecef7f80 — '
           'directive 1a1c1dde3f6d0021) : corrections de consistance F1-F5 (§5 baseline '
           'MESURÉE · §6 traçabilité v1.1.0/v1.1.1 · doublon description supprimé M-safe '
           'stemmer V6 · evals.json 1.1.1 · §2 recalé) ; précédent Task 86,')
LIGNAGE_AJOUT = """
## v1.1.1 (2026-11-09, Task 90, session web-ecef7f80, directive 1a1c1dde3f6d0021)

- **Corrections de consistance post-test $FACON** (écosystème comme entrée — audit T1.1.2, failles F1-F5 mesurées, règle d'or n°5) : F1 §5 staleness résorbé (« Baseline A2 : EN ATTENTE DE MESURE » → MESURÉE 6/7 Task 86, 21/21 votes réels) ; F2 §6 traçabilité v1.1.0 (Task 86) complétée + v1.1.1 (présente) ; F3 evals.json champ version 1.0.0 → 1.1.1 ; F4 doublon description « la discipline agent engineering la discipline agent engineering » supprimé (coquille — présente 2 arbres SKILL.md, absente KB : dérive miroir R4 résorbée par resynchronisation) ; F5 §2 « Pas de script propre en v1.0.0 » recalé.
- **M-safe F4 PROUVÉE par simulation préalable** (pattern Task 86) : suppression d'OCCURRENCES dupliquées (la/discipline = STOP-words stemmer ; agent/engineering présents ailleurs) → ensembles de radicaux stemmer arbitre V6 IDENTIQUES avant/après ; verdicts voie M sur les 7 cas inchangés (True×5 positifs · True cas 6 structurel consigné · False cas 7) — routage inchangé par construction.
- **PATCH** : corrections de contenu/consistance SANS changement de comportement — sémantique, routage et contrats inchangés.
- **Cascade KO-L004** : KB v1.1.1 (en-tête + Description miroir resynchronisée + Dernière calibration) + pin ECO_SKILLS integrity 1.1.1 + présent fichier + miroirs hôte→dépôt (pattern Tasks 83-86).
"""

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


def extraire_tags(texte):
    tags_m = re.search(r"tags:\s*\n((?:\s+-\s+.*\n)+)", texte)
    return re.findall(r"-\s+(.+)", tags_m.group(1)) if tags_m else []


def simuler_m(description, tags):
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


def compter(texte, ancre):
    return texte.count(ancre)


def main():
    texte = SKILL.read_text(encoding="utf-8")
    sha_avant = sha256_fichier(SKILL)

    # Idempotence : 2e passe NO-OP
    if VERSION_NEW in texte and compter(texte, DOUBLON) == 0:
        print(json.dumps({"statut": "NO-OP", "version": "1.1.1",
                          "sha_skill": sha_avant}, ensure_ascii=False))
        return 0

    # ── Pré-asserts (abort SANS écriture si écart) ──
    pre = {}
    for nom, ancre in [("doublon_F4", DOUBLON), ("version_1.1.0", ANCRE_VIEILLE_VERSION),
                       ("s5_stale_F1", ANCRE_S5), ("s2_F5", ANCRE_S2),
                       ("s6_fin_v100", ANCRE_S6_FIN)]:
        c = compter(texte, ancre)
        pre[nom] = c
        assert c == 1, f"ABORT — ancre {nom} count={c} (attendu 1)"
    evaluees_texte = EVALS.read_text(encoding="utf-8")
    assert compter(evaluees_texte, EVALS_VIEUX) == 1, "ABORT — evals version ancre != 1"
    kb_texte = KB.read_text(encoding="utf-8")
    assert compter(kb_texte, KB_EN_TETE) == 1, "ABORT — KB en-tête ancre != 1"
    assert compter(kb_texte, KB_CAL_ANCRE) == 1, "ABORT — KB calibration ancre != 1"
    pin_texte = PIN.read_text(encoding="utf-8")
    assert compter(pin_texte, PIN_ANCRE) == 1, "ABORT — pin ancre != 1"

    # ── Simulation M-safe F4 (AVANT écriture) ──
    tags = extraire_tags(texte)
    desc_old = extraire_description(texte)
    assert DOUBLON in desc_old, "ABORT — doublon absent de la description extraite"
    desc_new = desc_old.replace(DOUBLON, DOUBLON_FIX, 1)
    verdicts_old = simuler_m(desc_old, tags)
    verdicts_new = simuler_m(desc_new, tags)
    attendus = [True] * 5 + [True, False]  # cas 6 True STRUCTUREL (écart consigné), cas 7 False
    assert [v for v, _ in verdicts_old] == attendus, f"ABORT — verdicts M old inattendus {verdicts_old}"
    assert [v for v, _ in verdicts_new] == attendus, f"ABORT — verdicts M new inattendus {verdicts_new}"
    assert verdicts_old == verdicts_new, "ABORT — verdicts M divergents (M-safe NON prouvée)"
    kws_old = keywords_for("agent-engineering", desc_old, tags)
    kws_new = keywords_for("agent-engineering", desc_new, tags)
    assert kws_old == kws_new, "ABORT — ensembles de radicaux divergents (M-safe NON prouvée)"

    # ── Éditions SKILL.md (all-or-nothing en mémoire puis écriture unique) ──
    ntexte = texte
    ntexte = ntexte.replace(DOUBLON, DOUBLON_FIX, 1)
    ntexte = ntexte.replace(ANCRE_VIEILLE_VERSION, VERSION_NEW, 1)
    ntexte = ntexte.replace(ANCRE_S2, S2_NEW, 1)
    ntexte = ntexte.replace(ANCRE_S5, S5_NEW, 1)
    ntexte = ntexte.replace(ANCRE_S6_FIN, ANCRE_S6_FIN + S6_AJOUT, 1)
    # Post-asserts
    assert compter(ntexte, DOUBLON) == 0
    assert compter(ntexte, VERSION_NEW) == 1
    assert compter(ntexte, "Baseline A2 : MESURÉE") == 1
    assert compter(ntexte, "- v1.1.0 (Task 86") == 1
    assert compter(ntexte, "- v1.1.1 (Task 90") == 1
    SKILL.write_text(ntexte, encoding="utf-8")

    # ── evals.json (édition texte, format préservé) ──
    n_evaluees = evaluees_texte.replace(EVALS_VIEUX, EVALS_NEW, 1)
    assert compter(n_evaluees, EVALS_NEW) == 1
    EVALS.write_text(n_evaluees, encoding="utf-8")

    # ── KB : en-tête + description miroir resynchronisée + calibration ──
    nkb = kb_texte.replace(KB_EN_TETE, KB_EN_TETE_NEW, 1)
    nkb = nkb.replace(KB_CAL_ANCRE, KB_CAL_NEW, 1)
    m = re.search(r"(## agent-engineering v1\.1\.1\n\n- \*\*Category\*\* : ecosystem\n"
                  r"- \*\*Description\*\* : )(.*?)(\n- \*\*Dépend de\*\*)", nkb, re.DOTALL)
    assert m, "ABORT — bloc Description KB introuvable"
    desc_miroir_ok = (m.group(2) == desc_new)
    if not desc_miroir_ok:
        nkb = nkb[:m.start(2)] + desc_new + nkb[m.end(2):]
    KB.write_text(nkb, encoding="utf-8")

    # ── Pin ECO_SKILLS ──
    npin = pin_texte.replace(PIN_ANCRE, PIN_NEW, 1)
    assert compter(npin, '"agent-engineering": "1.1.1"') == 1
    PIN.write_text(npin, encoding="utf-8")

    # ── Lignage ──
    ltexte = LIGNAGE.read_text(encoding="utf-8")
    assert "## v1.1.1 (2026-11-09, Task 90" not in ltexte, "ABORT — lignage v1.1.1 déjà présent"
    LIGNAGE.write_text(ltexte.rstrip("\n") + "\n" + LIGNAGE_AJOUT, encoding="utf-8")

    # ── Miroirs hôte→dépôt (pattern Tasks 83-86) ──
    for src, dst in [(SKILL, REPO_SKILL), (EVALS, REPO_EVALS), (KB, REPO_KB),
                     (PIN, REPO_PIN), (LIGNAGE, REPO_LIGNAGE)]:
        dst.write_bytes(src.read_bytes())

    # ── Rapport ──
    rapport = {
        "statut": "APPLIQUÉ",
        "version": "1.1.0 → 1.1.1 (PATCH)",
        "corrections": ["F1 §5 baseline MESURÉE 6/7 documentée",
                        "F2 §6 traçabilité v1.1.0 + v1.1.1",
                        "F3 evals.json version 1.1.1",
                        "F4 doublon description supprimé (M-safe)",
                        "F5 §2 recalé"],
        "m_safe": {"verdicts_7_cas": [v for v, _ in verdicts_new],
                   "radicaux_ensemble_identique": True,
                   "kb_miroir_deja_synchro": desc_miroir_ok},
        "sha_skill": {"avant": sha_avant, "apres": sha256_fichier(SKILL)},
        "cascade": ["KB v1.1.1", "pin ECO_SKILLS 1.1.1", "lignage v1.1.1",
                    "miroirs hôte→dépôt ×5"],
    }
    print(json.dumps(rapport, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
