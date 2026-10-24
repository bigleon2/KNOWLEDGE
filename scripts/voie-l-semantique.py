#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.13)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

# -*- coding: utf-8 -*-
"""
Option B (Task 30, GO propriétaire) — Voie L sémantique à cache déterministe.

Routage sémantique par LLM (CLI z-ai chat, glm) pour les cas trigger_evals que
l'heuristique voie M ne discrimine pas. Non-détermination neutralisée :
- CACHE DÉTERMINISTE scripts/voie-l-cache.json — verdict figé une fois (R4),
  consulté en lecture seule par l'arbitre V6.1, JAMAIS réécrit (sauf --purge-indecis
  en phase de construction, avant figeage) ;
- QUESTION DE ROUTAGE (leçon Task 30) : la question posée au juge est la question
  de routage du référentiel (« cette requête doit-elle être routée vers CE skill
  selon son périmètre officiel »), jamais une question d'appartenance de domaine ;
- DESCRIPTION COMPLÈTE (leçon Task 30) : la description SKILL.md est donnée au
  juge SANS troncature (la doctrine de périmètre peut figurer en fin de description) ;
- MODE SÉRIEL + retry/backoff (leçon Task 29/30 : burst parallèle → 429 rate limit) ;
- FICHIER -o PURGÉ avant chaque appel (le CLI sort exit 0 même en erreur — risque
  de parsing d'un fichier périmé) ; verdict parsé strict (true/false, sinon INDECIS).

Usage :
  python scripts/voie-l-semantique.py                # arbitre les cas non-resorbe du rapport replay
  python scripts/voie-l-semantique.py --skill X      # limite au skill X
  python scripts/voie-l-semantique.py --purge-indecis  # purge les entrées INDECIS (construction)
  python scripts/voie-l-semantique.py --delai N      # délai entre appels (défaut 3 s)
"""
import json
import subprocess
import sys
import time
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
SKILLS = BASE / "skills"
CACHE = BASE / "scripts" / "voie-l-cache.json"
RAPPORT = BASE / "scripts" / "triggers-replay-report.json"
SOURCE_DISCUSSION = "scripts/discussion-64c90144.txt (verdicts figés Task 30, GO propriétaire)"

args = sys.argv[1:]
DELAI = 3
if "--delai" in args:
    DELAI = int(args[args.index("--delai") + 1])
SKILL_FILTRE = args[args.index("--skill") + 1] if "--skill" in args else None
PURGE_INDECIS = "--purge-indecis" in args


def charger_cache():
    return json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.exists() else {}


def ecrire_cache(cache):
    CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def meta_skill(name):
    smd = (SKILLS / name / "SKILL.md").read_text(encoding="utf-8")
    fm = smd.split("---")[1]
    import re
    desc_m = re.search(r"description:\s*>-?\s*\n((?:[ \t]+.*\n)+)", fm)
    if desc_m:
        return " ".join(l.strip() for l in desc_m.group(1).splitlines())
    desc_m2 = re.search(r"description:\s*[\"']?(.+?)[\"']?\s*$", fm, re.MULTILINE)
    return desc_m2.group(1).strip() if desc_m2 else ""


def question_routage(query, name, description):
    return (
        f"Un utilisateur demande : « {query} ».\n\n"
        f"Le skill « {name} » a pour description officielle COMPLÈTE :\n"
        f"\"\"\"{description}\"\"\"\n\n"
        f"Question de ROUTAGE (pas d'appartenance de domaine) : selon le périmètre "
        f"officiel et la doctrine de déclenchement de cette description, cette requête "
        f"doit-elle être routée vers CE skill ? Réponds UNIQUEMENT par true ou false."
    )


SYSTEME = (
    "Tu es un arbitre de routage strict pour un écosystème de skills. Tu réponds "
    "uniquement par le mot true ou le mot false, sans explication."
)


def appel_llm(query, name, description):
    """Appel CLI sériel, blindé : -o purgé avant appel, retry/backoff sur échec."""
    import tempfile, os
    outfile = BASE / "scripts" / ".voie-l-reponse.tmp.json"
    if outfile.exists():
        outfile.unlink()
    q = question_routage(query, name, description)
    for tentative in range(3):
        r = subprocess.run(
            ["z-ai", "chat", "-p", q, "-s", SYSTEME, "-o", str(outfile)],
            capture_output=True, text=True, timeout=120, start_new_session=True,
            stdin=subprocess.DEVNULL,
        )
        if outfile.exists():
            try:
                data = json.loads(outfile.read_text(encoding="utf-8"))
                contenu = data["choices"][0]["message"]["content"].strip().lower()
                if "true" in contenu and "false" not in contenu:
                    outfile.unlink()
                    return True
                if "false" in contenu:
                    outfile.unlink()
                    return False
            except Exception:
                pass
            outfile.unlink()
        time.sleep(DELAI * (2 ** tentative))  # backoff exponentiel
    return None  # INDECIS (dégradation honnête)


def main():
    cache = charger_cache()
    if PURGE_INDECIS:
        purges = [k for k, v in cache.items()
                  if isinstance(v, dict) and v.get("verdict") is None]
        for k in purges:
            del cache[k]
        if purges:
            ecrire_cache(cache)
        print(f"purge INDECIS : {len(purges)} entrée(s) supprimée(s) (phase de construction)")
        return

    rapport = json.loads(RAPPORT.read_text(encoding="utf-8"))
    cibles = []
    for name, sk in sorted(rapport.get("skills", {}).items()):
        if SKILL_FILTRE and name != SKILL_FILTRE:
            continue
        for row in sk.get("cases", []):
            if row.get("source") == "non-resorbe":
                cle = f"{name}::{row['query']}"
                if cle not in cache:
                    cibles.append((name, row["query"], row["expected"]))
    if not cibles:
        print("aucun cas non-resorbe à arbitrer (cache-first : tout est déjà figé)")
        return

    print(f"{len(cibles)} cas à arbitrer (mode sériel, délai {DELAI}s) :")
    figes = indecis = 0
    for i, (name, query, expected) in enumerate(cibles, 1):
        cle = f"{name}::{query}"
        print(f"[{i}/{len(cibles)}] {name} :: {query[:70]} ... ", flush=True)
        verdict = appel_llm(query, name, meta_skill(name))
        if verdict is None:
            cache[cle] = {"verdict": None, "statut": "INDECIS",
                          "question_type": "routage", "date_fixation": None}
            indecis += 1
            print("    INDECIS (CLI échec — retry/backoff épuisé)")
        else:
            cache[cle] = {
                "verdict": verdict,
                "statut": "fige",
                "question_type": "routage",
                "date_fixation": time.strftime("%Y-%m-%d"),
                "attendu_eval": expected,
                "source": "voie L z-ai chat (glm), description complète, sériel+backoff",
            }
            figes += 1
            print(f"    figé : {verdict} (attendu eval : {expected})")
        ecrire_cache(cache)  # écriture incrémentale (un verdict = une écriture)
        time.sleep(DELAI)
    print(f"\nBILAN : {figes} figé(s), {indecis} INDECIS — cache : {len(cache)} entrée(s)")


if __name__ == "__main__":
    main()
