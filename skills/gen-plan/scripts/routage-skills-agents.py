#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.44)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 — rappel permanent gen-plan v3.47.0 : dérive → correction immédiate + worklog + durcissement).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/.
"""

"""Task 114 — É5-ROUTAGE : script décisionnel de routage skills + agents (gen-plan v3.47.0).

Directive propriétaire trace 1a2025197d2a0e9d : « intégrer les déclencheurs des skills
et des agents dans le corps de gen-plan ; forcer gen-plan à utiliser ses déclencheurs ;
si l'utilisation des agents n'est justifiée que dans des cas complexes, intégrer un
script qui orchestrera cette prise de décision ».

ANALYSE (Task 114, livrable download/analyse-routage-decisionnel-task114.md) :
  - Incruster le catalogue COMPLET des déclencheurs (73 skills + 4 agents) dans le
    corps de gen-plan DÉGRADE le budget #token de chaque session (gen-plan +30-40 Kio,
    franchit le seuil CRITIQUE ≥ 60 Kio de l'arbitre poids-chargement) et viole R4
    (jamais dupliquer — les déclencheurs vivent DÉJÀ dans les frontmatters installés,
    source unique ; toute copie créerait une dérive KO-L004 par montée de version).
  - La solution OPTIMALE est le routage MÉCANIQUE À L'EXÉCUTION : le présent script
    lit les frontmatters INSTALLÉS (description + read_when — source unique, zéro
    duplication, zéro lag) et produit une recommandation compacte (~1-2 Kio JSON,
    appelé 1× par plan) ; gen-plan intègre les recommandations à E5 (sélection des
    skills) et à E7 (plan — section Routage) via le hook É5-ROUTAGE (§1.16).
  - Les AGENTS (délégation coûteuse — sous-agent = contexte plein) sont PORTE-GARDÉ :
    recommandés UNIQUEMENT si le verdict de complexité est COMPLEXE (>= 2/5 critères,
    grille alignée sur le PROMPT-GATEWAY agent-prompt-engineering §1.6) — la prise de
    décision demandée par le propriétaire est orchestrée par CE script.

Méthode : scoring lexical tolérant (mots >= 4 caractères, sans stopwords), pondération
description ×2 / read_when ×3 (le read_when est le contrat de déclenchement — convention
Task 28) ; agents scannés sur objectif/modes/gardes des fichiers .agent.

Usage :
  routage-skills-agents.py --tache "..." [--format json|text] [--limite N] [--selftest]
Idempotent (lecture seule), stdlib uniquement, cible < 1 s.
Sortie JSON : download/routage-dernier.json (artefact de travail consigné).
Codes retour : 0 = OK · 2 = usage.
"""
import argparse
import json
import re
import sys
import time
from pathlib import Path

VERSION = "1.0.0"
ROOT = Path(__file__).resolve().parents[3]
SKILLS = ROOT / "skills"
RAPPORT = ROOT / "download" / "routage-dernier.json"

# Rappel permanent langue (règle d'or n°6 — v3.47.0) : toute sortie texte est française.

STOPWORDS = {
    "dans", "avec", "pour", "cette", "être", "avoir", "faire", "mais", "aussi",
    "tout", "tous", "leur", "nos", "vos", "chez", "puis", "ensuite", "alors",
    "cela", "celui", "celle", "lesquels", "quelle", "quel", "quels", "quand",
    "comme", "entre", "vers", "sans", "sous", "sur", "par", "est", "sont",
    "plus", "moins", "très", "bien", "peut", "doit", "veux", "souhaite",
    "demande", "demandes", "faut", "essaie", "essaye", "merci", "bonjour",
    "des", "une", "les", "aux", "son", "ses", "mes", "tes", "lui", "eux",
    "nous", "vous", "que", "qui", "quoi", "dont", "cet", "ces", "donc",
    "mais", "pas", "ête", "ét", "the", "and", "that", "this", "with", "for",
    "from", "into", "are", "was", "were", "have", "has", "you", "your", "our",
    "out", "get", "not", "but", "all", "can", "will", "use", "used", "using",
}

LIVRABLES = re.compile(
    r"\b(génère|générer|crée|créer|produis|produire|rapport|document|tableau|"
    r"présentation|script|plan|test|tests|livrable|fichier|dataset|dashboard|"
    r"diagramme|graphique|liste|rapports)\b", re.I)
HORIZON = re.compile(
    r"\b(chaîne|enchaîn\w*|étape|étapes|pipeline|progressif\w*|poursuiv\w*|"
    r"continue\w*|hebdomad\w*|long\s+terme|automatis\w*|récurren\w*|journali\w*)\b", re.I)
PARALLELE = re.compile(
    r"\b(puis|ensuite|parallèle\w*|indépendan\w*|en\s+même\s+temps|fan-out|"
    r"vagues|ensemble|simultané\w*)\b", re.I)
EXTERNE = re.compile(
    r"\b(push|git|api|web|url|http\w*|clé|token|jeton|dépôt|remote|cron|"
    r"serve\w*|cloud\w*|réseau|github)\b", re.I)

MOTIF_GATE = ("verdict SIMPLE — délégation d'agents réservée aux cas complexes "
              "(>= 2/5 critères, grille PROMPT-GATEWAY §1.6 ; gen-plan §1.17)")


def jetons(texte):
    """Mots normalisés >= 3 caractères (pdf/tts/asr utiles), stopwords retirés."""
    mots = re.findall(r"[a-zàâäéèêëïîôöùûüç]{3,}", texte.lower())
    return [m for m in mots if m not in STOPWORDS]


def extraire_frontmatter(texte):
    """Parseur tolérant (convention écosystème — read_when en clauses françaises,
    PAS du YAML strict — KO-L003 Task 113) : rend (description, [read_when])."""
    if not texte.startswith("---"):
        return "", []
    fin = texte.find("\n---", 3)
    if fin < 0:
        return "", []
    fm = texte[3:fin]
    desc, rw, en_rw = "", [], False
    for ligne in fm.splitlines():
        if ligne.startswith("description:"):
            desc, en_rw = ligne[len("description:"):].strip(), False
        elif ligne.startswith("read_when:"):
            en_rw = True
        elif en_rw and ligne.strip().startswith("- "):
            rw.append(ligne.strip()[2:].strip())
        elif en_rw and ligne and not ligne.startswith((" ", "-")):
            en_rw = False
        elif desc and not ligne.startswith((" ", "-", "read_when:")) and ":" in ligne:
            # nouvelle clé racine après description multi-ligne (bloc >) — fin
            if not ligne.startswith("  "):
                pass
        elif desc and ligne.startswith("  ") and not en_rw:
            desc += " " + ligne.strip()
    return desc, rw


def scan_skills(exclure="gen-plan"):
    """Inventaire (nom -> texte pondéré) depuis les frontmatters INSTALLÉS."""
    inventaire = {}
    for dossier in sorted(SKILLS.iterdir()):
        if not dossier.is_dir() or dossier.name.startswith("@"):
            continue
        p = dossier / "SKILL.md"
        if not p.exists() or dossier.name == exclure:
            continue
        desc, rw = extraire_frontmatter(p.read_text(encoding="utf-8", errors="replace"))
        inventaire[dossier.name] = {"desc": desc, "read_when": rw}
    return inventaire


def scan_agents():
    """Inventaire agents (.agent) — objectif + modes + gardes."""
    inventaire = {}
    for p in sorted(SKILLS.glob("*/*.agent")):
        t = p.read_text(encoding="utf-8", errors="replace")
        inventaire[p.stem] = t[:4000]
    return inventaire


def scorer(inventaire, jetons_tache, champ_desc, champ_rw, poids_desc, poids_rw):
    resultats = []
    for nom, entree in inventaire.items():
        if champ_rw is not None:
            texte_desc = entree["desc"]
            texte_rw = " ".join(entree["read_when"])
        else:
            texte_desc = entree
            texte_rw = ""
        jd, jr = set(jetons(texte_desc)), set(jetons(texte_rw))
        score = 2 * len(jetons_tache & jd) + 3 * len(jetons_tache & jr)
        extraits = []
        if isinstance(entree, dict):
            extraits = [r for r in entree.get("read_when", [])[:4]
                        if any(j in jetons(r.lower()) for j in jetons_tache)][:1]
        if score > 0:
            resultats.append({"nom": nom, "score": score,
                              "extraits": [e[:140] for e in extraits]})
    resultats.sort(key=lambda x: (-x["score"], x["nom"]))
    return resultats


def verdict_complexite(tache, nb_skills, nb_agents):
    criteres = {
        "multi_livrables": len(set(LIVRABLES.findall(tache))) >= 2,
        "multi_domaines": nb_skills >= 3,
        "horizon_long": bool(HORIZON.search(tache)),
        "parallele": len(set(PARALLELE.findall(tache))) >= 2 or len(set(PARALLELE.findall(tache))) >= 1 and bool(re.search(r"\bet\b.*\bet\b", tache, re.I)),
        "integration_externe": bool(EXTERNE.search(tache)),
    }
    n = sum(criteres.values())
    return ("COMPLEXE" if n >= 2 else "SIMPLE"), n, criteres


def router(tache, limite=8):
    t0 = time.perf_counter()
    jt = set(jetons(tache))
    skills = scan_skills()
    agents = scan_agents()
    hits_s = scorer(skills, jt, "desc", "rw", 2, 3)
    hits_a = scorer(agents, jt, None, None, 2, 3)
    verdict, n_criteres, criteres = verdict_complexite(tache, len(hits_s), len(hits_a))
    if verdict == "COMPLEXE":
        agents_rec = hits_a[:4]
        gate = None
    else:
        agents_rec = []
        gate = MOTIF_GATE
    resultat = {
        "script": "routage-skills-agents",
        "version": VERSION,
        "tache": tache[:400],
        "verdict_complexite": verdict,
        "criteres_complexite": criteres,
        "criteres_remplis": n_criteres,
        "skills_recommandes": hits_s[:limite],
        "agents_recommandes": agents_rec,
        "portegardes_agents": gate,
        "metadonnees": {
            "skills_scannes": len(skills), "agents_scannes": len(agents),
            "duree_ms": round((time.perf_counter() - t0) * 1000, 2),
            "langue": "fr (règle d'or n°6 — rappel permanent gen-plan v3.47.0)",
        },
    }
    RAPPORT.parent.mkdir(parents=True, exist_ok=True)
    RAPPORT.write_text(json.dumps(resultat, ensure_ascii=False, indent=1) + "\n",
                       encoding="utf-8")
    return resultat


def texte_lisible(r):
    lignes = [
        "ROUTAGE É5-ROUTAGE (v" + VERSION + ") — verdict : " + r["verdict_complexite"]
        + f" ({r['criteres_remplis']}/5 critères)",
        "Skills recommandés :",
    ]
    for s in r["skills_recommandes"]:
        lignes.append(f"  - {s['nom']} (score {s['score']})"
                      + (f" — {s['extraits'][0]}" if s['extraits'] else ""))
    if r["agents_recommandes"]:
        lignes.append("Agents recommandés (délégation justifiée — cas complexe) :")
        for a in r["agents_recommandes"]:
            lignes.append(f"  - {a['nom']} (score {a['score']})")
    elif r["portegardes_agents"]:
        lignes.append("Agents : aucun — " + r["portegardes_agents"])
    lignes.append(f"Métadonnées : {r['metadonnees']['skills_scannes']} skills, "
                  f"{r['metadonnees']['agents_scannes']} agents, "
                  f"{r['metadonnees']['duree_ms']} ms")
    return "\n".join(lignes)


def selftest():
    ok = 0
    tests = []
    d, rw = extraire_frontmatter((SKILLS / "asr" / "SKILL.md").read_text(encoding="utf-8"))
    tests.append(("fm_description", "Transcription" in d or "transcri" in d.lower()))
    tests.append(("fm_read_when", any("déclencher" in x.lower() for x in rw)))
    r1 = router("transcrire un enregistrement audio en texte sous-titres")
    tests.append(("score_asr", any(x["nom"] == "asr" for x in r1["skills_recommandes"][:3])))
    tests.append(("exclusion_genplan", all(x["nom"] != "gen-plan" for x in r1["skills_recommandes"])))
    r2 = router("quelle heure est-il ?")
    tests.append(("complexite_simple", r2["verdict_complexite"] == "SIMPLE"))
    tests.append(("gate_agents", r2["agents_recommandes"] == [] and r2["portegardes_agents"] is not None))
    r3 = router("génère un rapport pdf et une présentation pptx puis pousse sur le dépôt git avec la clé")
    tests.append(("complexite_complexe", r3["verdict_complexite"] == "COMPLEXE"))
    r4 = router("traduire le document pdf en français")
    tests.append(("score_pdf", any(x["nom"] == "pdf" for x in r4["skills_recommandes"][:5])))
    tests.append(("agents_complexe_liste", isinstance(r3["agents_recommandes"], list)))
    for nom, res in tests:
        print(("PASS " if res else "FAIL ") + nom)
        ok += bool(res)
    print(f"SELFTEST {ok}/{len(tests)}")
    return 0 if ok == len(tests) else 1


def main():
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--tache", help="description de la tâche à router")
    ap.add_argument("--format", choices=["json", "text"], default="json")
    ap.add_argument("--limite", type=int, default=8)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(selftest())
    if not a.tache:
        print("Usage : --tache \"...\" [--format json|text] [--selftest]")
        sys.exit(2)
    r = router(a.tache, limite=a.limite)
    if a.format == "text":
        print(texte_lisible(r))
    else:
        print(json.dumps(r, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
