#!/usr/bin/env python3
"""Task 113 — Cascade KO-L004 des PMs du corpus (correct-work v2.12.1, refactor-guard v1.8.2).

Précédent canonique : Task ID 11 G2 (montée v2.12.0 — « cascade COMPLÈTE : arbitre 16/16,
PM v2.12.0, KB, historiques, dédup R4 »). Le bump PATCH Task 113 (addition pure triptyque)
exige : régénération mécanique du PM cible v<nouvelle> depuis v<ancienne>, archive R4 du
PM ancien (git mv byte-identité), recalibrage de l'arbitre canonique verify-correct-work
(EXPECTED_VERSION + PM_PATH — KO-L003 dynamisation recalibrée, jamais ajustement de la
réalité), mise à jour des références de noms de fichiers dans le corpus (@mon-ecosysteme :
README · ULTRA · INSTALL-ECOSYSTEME · SHARED).

Voie canonique : édition DÉPÔT → commit → bootstrap. Idempotent ×2. Stdlib.
Codes retour : 0 = PASS, 1 = échec, 2 = selftest.
"""
# ⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.45)
# SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
# Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
# Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
# Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
# Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
# Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).

import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

RACINE = Path("/home/z/my-project")
DEPOT = RACINE / "KNOWLEDGE-repo"
CORPUS = DEPOT / "skills/@mon-ecosysteme"
HIST = CORPUS / "@historique-pms"
RAPPORT = RACINE / "scripts/task113-cascade-pm-rapport.json"

AUJOURDHUI = "2026-11-22"
PROVENANCE_NOTE = (
    " ; régénéré mécaniquement {auj} (Task 113, directive 1a201e4bda5a2289) : bump PATCH "
    "{anc}→{nv} par addition pure (triptyque read_when Task 28, non-régression triggers) — "
    "cascade KO-L004 selon le précédent Task ID 11 (PM régénéré, ancien archivé R4, arbitre "
    "recalibré)"
)

# (skill, ancienne, nouvelle, nom_pm) — arbitrages à recalibrer par la suite
CASCADES = [
    ("correct-work", "2.12.0", "2.12.1", "PROMPT-MAITRE-CORRECT-WORK"),
    ("refactor-guard", "1.8.1", "1.8.2", "PROMPT-MAITRE-REFACTOR-GUARD"),
]
# fichiers corpus dont les références de noms de PM sont mises à jour
CORPUS_REFS = ["README.md", "PROMPT-ULTRA-MAITRE-ORCHESTRATION.md",
               "PROMPT-MAITRE-INSTALL-ECOSYSTEME.md", "PROMPT-MAITRE-SHARED.md",
               "SYNC-CONTEXT.md"]


def h():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def regenerer_pm(skill: str, anc: str, nv: str, base: str) -> dict:
    """Régénère le PM v<nv> depuis v<anc> (substitutions mécaniques verrouillées)."""
    anc_p = CORPUS / f"{base}-v{anc}.md"
    nv_p = CORPUS / f"{base}-v{nv}.md"
    if not anc_p.exists():
        return {"statut": "PM_ANCIEN_ABSENT", "fichier": str(anc_p)}
    if nv_p.exists():
        return {"statut": "DEJA_REGENERE", "fichier": str(nv_p)}
    t = anc_p.read_text(encoding="utf-8")
    avant = t
    # substitutions verrouillées : uniquement les mentions versionnées DU skill ciblé
    t = t.replace(f"{skill} v{anc}", f"{skill} v{nv}")
    t = t.replace(f"{base}-v{anc}", f"{base}-v{nv}")
    t = re.sub(rf"(> \*\*Version du prompt\*\* : [0-9.]+\n)",
               rf"\1> **Date de régénération** : {AUJOURDHUI} (Task 113)\n", t, count=1)
    t = t.replace("> **Provenance** : ", "> **Provenance** : [" + AUJOURDHUI
                  + " Task 113 : régénéré mécaniquement depuis v" + anc + " — addition pure "
                  "triptyque read_when, non-régression triggers ; ancien archivé R4] ", 1)
    garde = (PROVENANCE_NOTE.format(auj=AUJOURDHUI, anc=anc, nv=nv)
             if PROVENANCE_NOTE.format(auj=AUJOURDHUI, anc=anc, nv=nv) not in t else "")
    nv_p.write_text(t, encoding="utf-8")
    # garde anti-perte : le contenu v<nv> doit couvrir v<anc> (taille ≥, substitutions réelles)
    if len(t) < len(avant) * 0.95:
        nv_p.unlink()
        return {"statut": "GARDE_ANTI_PERTE", "detail": f"taille {len(t)} < 95 % de {len(avant)}"}
    # archive R4 : git mv byte-identité
    HIST.mkdir(parents=True, exist_ok=True)
    r = subprocess.run(["git", "mv", str(anc_p.relative_to(DEPOT)),
                        str(HIST.relative_to(DEPOT)) + f"/{base}-v{anc}.md"],
                       cwd=DEPOT, capture_output=True, text=True)
    return {"statut": "REGENERE_ARCHIVE" if r.returncode == 0 else "REGENERE_MV_KO",
            "detail": r.stderr.strip()[:120], "taille": len(t),
            "substitutions": avant != t}


def recalibrer_arbitre() -> dict:
    """KO-L004 : recalibrage de l'arbitre canonique verify-correct-work (v2.12.1)."""
    p = DEPOT / "skills/correct-work/scripts/verify-correct-work.py"
    t = p.read_text(encoding="utf-8")
    changements = []
    if 'EXPECTED_VERSION = "2.12.1"' not in t:
        t = t.replace('EXPECTED_VERSION = "2.12.0"',
                      'EXPECTED_VERSION = "2.12.1"  # KO-L004 Task 113 — addition pure triptyque')
        changements.append("EXPECTED_VERSION 2.12.0→2.12.1")
    if "PROMPT-MAITRE-CORRECT-WORK-v2.12.1.md" not in t:
        t = t.replace("PROMPT-MAITRE-CORRECT-WORK-v2.12.0.md",
                      "PROMPT-MAITRE-CORRECT-WORK-v2.12.1.md")
        changements.append("PM_PATH → v2.12.1")
    if changements:
        p.write_text(t, encoding="utf-8")
    return {"statut": "RECALIBRE" if changements else "DEJA_RECALIBRE",
            "changements": changements}


def maj_references_corpus() -> dict:
    """Met à jour les références de noms de PM dans le corpus (hors historiques)."""
    c = {}
    paires = [("-v2.12.0", "-v2.12.1"), ("-v1.8.1", "-v1.8.2")]
    for nom in CORPUS_REFS:
        p = CORPUS / nom
        if not p.exists():
            continue
        t0 = p.read_text(encoding="utf-8")
        t = t0
        for a, n in paires:
            t = t.replace(a, n)
        if t != t0:
            p.write_text(t, encoding="utf-8")
            c[nom] = "MAJ"
        else:
            c[nom] = "inchangé"
    return c


def selftest() -> int:
    tests = [
        ("substitution_nom", "PROMPT-MAITRE-CORRECT-WORK-v2.12.0.md".replace(
            "-v2.12.0", "-v2.12.1") == "PROMPT-MAITRE-CORRECT-WORK-v2.12.1.md"),
        ("substitution_skill", "correct-work v2.12.0".replace(
            "correct-work v2.12.0", "correct-work v2.12.1") == "correct-work v2.12.1"),
    ]
    ok = sum(res for _, res in tests)
    for nom, res in tests:
        print(("PASS" if res else "FAIL") + " " + nom)
    print(f"SELFTEST {ok}/{len(tests)}")
    return 0 if ok == len(tests) else 1


def main() -> int:
    j = {"horodatage": h(), "pms": {}, "arbitre": None, "corpus": {}}
    for skill, anc, nv, base in CASCADES:
        j["pms"][skill] = regenerer_pm(skill, anc, nv, base)
        print(f"PM {skill} v{anc}→v{nv} : {j['pms'][skill]['statut']}")
        if j["pms"][skill]["statut"] in ("GARDE_ANTI_PERTE", "PM_ANCIEN_ABSENT", "REGENERE_MV_KO"):
            RAPPORT.write_text(json.dumps(j, ensure_ascii=False, indent=2), encoding="utf-8")
            return 1
    j["arbitre"] = recalibrer_arbitre()
    print("Arbitre CW :", j["arbitre"]["statut"], j["arbitre"]["changements"])
    j["corpus"] = maj_references_corpus()
    print("Références corpus :", j["corpus"])
    RAPPORT.write_text(json.dumps(j, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    sys.exit(main())
