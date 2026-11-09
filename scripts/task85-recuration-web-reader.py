#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.37)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).
ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9).
Référence canonique (SHARED §0/§1.2) : « mon skill X » = forme installée skills/X/SKILL.md.

Task 85 G3 — P0-P4 : moves R4 byte-identité (re-curation progressive disclosure
web-reader, cible suivante de la file — directive propriétaire trace 1a1bed51ccaf78f1,
méthode P0-P7 éprouvée Tasks 81 G2 / 82 G6 / 85 G2).
3 zones DORMANTES/RÉFÉRENCE (blocs de code verbatim z-ai-web-dev-sdk — exemples
d'intégration, un seul usage par mission) déplacées vers
references/exemples-integration.md (en-tête de provenance : zones, version, date,
SHA-256 par zone) + résumés opérationnels inline + pointeurs 1-lecture :
  1. « ## Cas d'usage avancés » chapitre intégral (WebContentAnalyzer · FeedReader ·
     ScrapingPipeline) ;
  2. bloc code du « ### 5. Traitement du contenu » (ContentProcessor — titre + résumé
     + pointeur conservés dans la série numérotée Bonnes pratiques) ;
  3. « ## Exemples d'intégration » chapitre intégral (Endpoint API Express.js ·
     Récupérateur de contenu planifié node-cron).
Le cœur opérationnel (§0 canonique, CLI, fonctionnement, implémentation basique,
format de réponse, bonnes pratiques 1-4 + 5 résumé, cas d'usage courants, dépannage,
performance, sécurité, à retenir) demeure intégralement inline.
Version INCHANGÉE (contrats intacts — précédents version-management Task 79 G2).
Idempotent : re-jeu = NO-OP (détection par pointeur déjà en place). All-or-nothing :
toutes les coupes validées AVANT la première écriture. Asserts count==1 par marqueur.
Byte-identité : SHA-256(zone source) == SHA-256(zone dans la référence) — preuve R4.
Usage : python3 scripts/task85-recuration-web-reader.py [--json]
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

R = Path("/home/z/my-project/KNOWLEDGE-repo")
SKILL = R / "skills" / "web-reader" / "SKILL.md"
REF = R / "skills" / "web-reader" / "references" / "exemples-integration.md"
DATE = "2026-11-09"
PROTO = "protocole re-curation v1.2.2, méthode moves-r4-pur (P0-P7 éprouvée)"

A_ADV = "## Cas d'usage avancés".encode()
A_FMT = "## Format de réponse".encode()
A_P5 = "### 5. Traitement du contenu".encode()
A_CUR = "\n## Cas d'usage courants".encode()  # \n discriminant (### Cas d'usage courants L81 contient la sous-chaîne)
A_INT = "## Exemples d'intégration".encode()
A_DEP = "## Dépannage".encode()
POINTEUR = "references/exemples-integration.md".encode()

# Preuves de non-casse : marqueurs de CODE qui doivent disparaître du SKILL.md
CODE_MARQUEURS = [
    "class WebContentAnalyzer".encode(),
    "class FeedReader".encode(),
    "class ScrapingPipeline".encode(),
    "static extractMainContent".encode(),
    "import express from 'express'".encode(),
    "class ScheduledFetcher".encode(),
]

RESUME_ADV = """## Cas d'usage avancés

Trois intégrations typiques, déplacées R4 byte-identité dans **`references/exemples-integration.md`** (lisez la zone correspondant à votre besoin) : **Analyseur de contenu web** (`WebContentAnalyzer` — cache `Map` + analyse de contenu), **Lecteur de flux RSS** (`FeedReader` — agrégation d'articles), **Pipeline de scraping web** (`ScrapingPipeline` — chaîne de processeurs). Chaque exemple montre l'import du SDK `z-ai-web-dev-sdk` côté backend et l'appel `zai.functions.invoke('page_reader', { url })`."""

RESUME_P5 = """Le traitement du contenu (extraction du contenu principal, conversion HTML → texte brut, extraction des métadonnées via la classe `ContentProcessor` + usage `processWebPage`) est déplacé R4 byte-identité dans **`references/exemples-integration.md`** — lisez la section correspondante avant d'implémenter."""

RESUME_INT = """## Exemples d'intégration

Deux intégrations complètes, déplacées R4 byte-identité dans **`references/exemples-integration.md`** : **Endpoint API Express.js** (serveur HTTP exposant la lecture de pages) et **Récupérateur de contenu planifié** (`node-cron` — fetch récurrent). Chaque exemple est autonome (imports + code intégral)."""


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def extraire(data: bytes) -> dict:
    """Extrait les 3 zones — asserts count==1, all-or-nothing."""
    for ancre, nom in [(A_ADV, "Cas avancés"), (A_FMT, "Format"), (A_P5, "Point 5"),
                       (A_CUR, "Cas courants"), (A_INT, "Intégration"), (A_DEP, "Dépannage")]:
        assert data.count(ancre) == 1, f"ancre {nom} != 1"
    i_adv, i_fmt = data.index(A_ADV), data.index(A_FMT)
    i_p5 = data.index(A_P5)
    i_cur = data.index(A_CUR) + 1  # +1 : sauter le \n discriminant
    i_int, i_dep = data.index(A_INT), data.index(A_DEP)
    assert i_adv < i_fmt < i_p5 < i_cur < i_int < i_dep, "ordre ancres inattendu"

    zoneA = data[i_adv:i_fmt]

    # Zone B : bloc code du point 5 (du ```javascript au ``` fermant)
    t5 = data[i_p5:i_cur]
    i_code = t5.index(b"```javascript")
    i_fin = t5.rindex(b"\n```")
    blocB = t5[i_code : i_fin + 4]
    assert blocB.count(b"```") == 2, "bloc point 5 mal borné"

    zoneC = data[i_int:i_dep]
    return {"zoneA": zoneA, "blocB": blocB, "zoneC": zoneC}


def verifier_reference(zones: dict) -> dict:
    """Preuve R4-INTÈGRE : les 3 zones sont byte-identiques dans la référence."""
    ref = REF.read_bytes()
    return {
        "r4_integre_A": zones["zoneA"] in ref,
        "r4_integre_B": zones["blocB"] in ref,
        "r4_integre_C": zones["zoneC"] in ref,
        "sha_A": sha(zones["zoneA"])[:16],
        "sha_B": sha(zones["blocB"])[:16],
        "sha_C": sha(zones["zoneC"])[:16],
    }


def main() -> int:
    data = SKILL.read_bytes()
    taille_avant = len(data)

    if POINTEUR in data:
        if any(m in data for m in CODE_MARQUEURS):
            print(json.dumps({"verdict": "état ambigu — pointeur présent mais code encore inline"},
                             ensure_ascii=False))
            return 1
        if not REF.exists():
            print(json.dumps({"verdict": "état ambigu — pointeur présent mais référence absente"},
                             ensure_ascii=False))
            return 1
        ref = REF.read_bytes()
        # Re-découpage aux marqueurs UNIQUES (coutures : prov + zoneA + \n + blocB + \n + zoneC + \n)
        # bloc B est précédé de 'class ContentProcessor' — le 1er ```javascript de la réf est DANS zoneA
        i1 = ref.index(A_ADV)
        i_cp = ref.index(b"class ContentProcessor")
        i2 = ref.rindex(b"```javascript", 0, i_cp)
        i3 = ref.index(A_INT)
        zoneA = ref[i1:i2 - 1]                       # -1 : couture \n
        blocB = ref[i2:ref.index(b"\n" + A_INT)]     # se termine par ```
        zoneC = ref[i3:len(ref) - 1]                 # -1 : couture \n finale
        r = verifier_reference({"zoneA": zoneA, "blocB": blocB, "zoneC": zoneC})
        # Preuve de NON-ÉDITION : SHA re-calculés == SHA consignés dans la provenance
        sha_head = ref[:ref.index(b"\n\n## ")].decode("utf-8", errors="replace")
        consignes = re.findall(r"`([0-9a-f]{16})…`", sha_head)
        recalcules = [r["sha_A"], r["sha_B"], r["sha_C"]]
        r["sha_conformes"] = len(consignes) == 3 and consignes == recalcules
        r["verdict"] = ("NO-OP (déjà curé) — byte-identité re-prouvée"
                        if r["sha_conformes"] else "DIVERGENCE SHA vs provenance")
        r["taille_skill"] = taille_avant
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0 if r["sha_conformes"] else 1

    # --- Déplacement (all-or-nothing) ---
    z = extraire(data)
    assert len(z["zoneA"]) >= 1536, "zoneA sous-seuil"
    assert len(z["blocB"]) >= 1536, "blocB sous-seuil"
    assert len(z["zoneC"]) >= 1536, "zoneC sous-seuil"

    prov = (
        f"# Exemples d'intégration — web-reader (zones archivées R4)\n\n"
        f"> **Provenance** : skill `web-reader` · zones « Cas d'usage avancés » (intégral), "
        f"bloc code « 5. Traitement du contenu » et « Exemples d'intégration » (intégral) · "
        f"déplacées R4 byte-identité vers `references/` le {DATE} (Task 85 G3, re-curation "
        f"progressive disclosure — {PROTO}) · **SHA-256 zone A : `{sha(z['zoneA'])[:16]}…`** · "
        f"**SHA-256 bloc B : `{sha(z['blocB'])[:16]}…`** · **SHA-256 zone C : `{sha(z['zoneC'])[:16]}…`** · "
        f"le skill intégral demeure `skills/web-reader/SKILL.md` — les zones archivées ne sont "
        f"jamais éditées (R4 byte-identité).\n\n"
    ).encode()
    REF.parent.mkdir(parents=True, exist_ok=True)
    REF.write_bytes(prov + z["zoneA"] + b"\n" + z["blocB"] + b"\n" + z["zoneC"] + b"\n")

    # Reconstruction : avant-avancés + résuméA + format..point5-titre + résuméB + courants..intégration + résuméC + dépannage..
    i_adv, i_fmt = data.index(A_ADV), data.index(A_FMT)
    i_p5, i_cur = data.index(A_P5), data.index(A_CUR) + 1  # +1 : \n discriminant
    i_int, i_dep = data.index(A_INT), data.index(A_DEP)

    nouveau = (
        data[:i_adv]
        + RESUME_ADV.encode() + b"\n\n"
        + data[i_fmt : data.index(A_P5)]
        + A_P5 + b"\n\n"          # titre du point 5 CONSERVÉ (continuité de la série numérotée)
        + RESUME_P5.encode() + b"\n\n"
        + data[i_cur:i_int]
        + RESUME_INT.encode() + b"\n\n"
        + data[i_dep:]
    )

    # Invariants post-édition
    for m in CODE_MARQUEURS:
        assert m not in nouveau, f"marqueur code encore présent: {m[:40]}"
    for ancre, n in [(A_FMT, "Format"), (A_P5, "Point 5"), (A_CUR, "Cas courants"),
                     (A_DEP, "Dépannage"), ("## §0 — Contexte Système".encode(), "§0")]:
        assert nouveau.count(ancre) == 1, f"ancre {n} altérée"
    assert nouveau.count(POINTEUR) == 3, f"pointeur {nouveau.count(POINTEUR)} != 3 (A/B/C)"
    assert nouveau[:100] == data[:100], "frontmatter altéré"

    r = verifier_reference(z)
    assert r["r4_integre_A"] and r["r4_integre_B"] and r["r4_integre_C"], "byte-identité R4 rompue"

    SKILL.write_bytes(nouveau)

    r.update(
        {
            "verdict": "DÉPLACÉ — POST-1 OK",
            "taille_avant": taille_avant,
            "taille_apres": len(nouveau),
            "taille_reference": len(REF.read_bytes()),
            "delta_o": len(nouveau) - taille_avant,
            "delta_pct": round(100.0 * (len(nouveau) - taille_avant) / taille_avant, 1),
            "version": "INCHANGÉE",
        }
    )
    print(json.dumps(r, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
