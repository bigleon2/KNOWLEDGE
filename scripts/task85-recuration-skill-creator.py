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

Task 85 G2 — P0-P4 : moves R4 byte-identité (re-curation progressive disclosure
skill-creator, cible P2 de la file — directive propriétaire trace 1a1bed51ccaf78f1,
méthode P0-P7 éprouvée Tasks 81 G2 / 82 G6).
2 blocs ≥ 1,5 Kio DORMANTS/RÉFÉRENCE (instructions conditionnelles d'environnement —
un seul s'applique par environnement d'exécution, les autres dorment) déplacés vers
references/instructions-plateformes.md (en-tête de provenance : sections, version,
date, SHA-256 par bloc) + résumé opérationnel inline + pointeur 1-lecture :
  1. « Instructions spécifiques à GLM.ai » (3 235 o)
  2. « Instructions spécifiques à Cowork » (2 243 o)
Le cœur opérationnel (§0 canonique, guide de rédaction, workflows eval étapes 1-5,
améliorations, optimisation de description, fichiers de référence) demeure
intégralement inline — dégradation refusée (posture Task 82 C4 iphone18).
Version INCHANGÉE v1.1.0 (contrats intacts — précédents version-management Task 79 G2).
Idempotent : re-jeu = NO-OP (détection par pointeur déjà en place). All-or-nothing :
toutes les coupes validées AVANT la première écriture. Asserts count==1 par marqueur.
Byte-identité : SHA-256(bloc source) == SHA-256(bloc dans la référence) — preuve R4.
Usage : python3 scripts/task85-recuration-skill-creator.py [--json]
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

R = Path("/home/z/my-project/KNOWLEDGE-repo")
SKILL = R / "skills" / "skill-creator" / "SKILL.md"
REF = R / "skills" / "skill-creator" / "references" / "instructions-plateformes.md"
VERSION = "1.1.0"
DATE = "2026-11-09"
PROTO = "protocole re-curation v1.2.2, méthode moves-r4-pur (P0-P7 éprouvée)"

A_GLM = "## Instructions spécifiques à GLM.ai".encode()
A_COWORK = "## Instructions spécifiques à Cowork".encode()
A_REF = "## Fichiers de référence".encode()
POINTEUR = "references/instructions-plateformes.md".encode()

RESUME = """## Instructions spécifiques à l'environnement d'exécution

Le workflow central est invariant (ébauche → test → relecture → amélioration → répétition) ; seules certaines mécaniques s'adaptent à l'environnement. Les instructions intégrales par plateforme — **GLM.ai** (pas de sous-agents : exécutions de cas de test séquentielles, relecture des résultats sans navigateur directement dans la conversation, benchmarking quantitatif sauté au profit du feedback qualitatif, comparaison à l'aveugle sautée, optimisation de description réservée à GLM Code via `glm -p`, mise à jour d'un skill existant : conserver le nom d'origine et copier vers `/tmp/` avant modification) et **Cowork** (sous-agents disponibles mais ni navigateur ni affichage : eval viewer `--static` obligatoire, GÉNÉRER l'eval viewer AVANT toute auto-évaluation des sorties, feedback via `feedback.json` téléchargé par le viewer) — sont déplacées R4 byte-identité dans **`references/instructions-plateformes.md`** : lisez la section correspondant à votre environnement AVANT d'exécuter les workflows de test/évaluation. Rappel transverse : la comparaison à l'aveugle requiert des sous-agents ; le packaging `package_skill.py` fonctionne partout où Python et un système de fichiers existent.""".encode()


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def extraire(data: bytes) -> tuple[bytes, bytes, bytes]:
    """Extrait (zone, bloc_glm, bloc_cowork) — asserts count==1, all-or-nothing."""
    assert data.count(A_GLM) == 1, "ancre GLM.ai != 1"
    assert data.count(A_COWORK) == 1, "ancre Cowork != 1"
    assert data.count(A_REF) == 1, "ancre Fichiers de référence != 1"
    i_glm = data.index(A_GLM)
    i_cowork = data.index(A_COWORK)
    i_ref = data.index(A_REF)
    assert i_glm < i_cowork < i_ref, "ordre ancres inattendu"
    zone = data[i_glm:i_ref]
    # bloc GLM : jusqu'au séparateur '---' qui précède Cowork
    sep_glm = zone.index(b"\n---\n\n")
    bloc_glm = zone[: sep_glm + 1]  # \n final inclus
    # bloc Cowork : de son titre (index relatif à ZONE) au séparateur final de la zone
    i_cowork_z = zone.index(A_COWORK)
    bloc_cowork = zone[i_cowork_z : zone.rindex(b"\n---\n\n") + 1]
    return zone, bloc_glm, bloc_cowork


def verifier_reference(bloc_glm: bytes, bloc_cowork: bytes) -> dict:
    """Preuve R4-INTÈGRE : les 2 blocs sont byte-identiques dans la référence."""
    ref = REF.read_bytes()
    ok_glm = bloc_glm in ref
    ok_cowork = bloc_cowork in ref
    return {
        "r4_integre_glm": ok_glm,
        "r4_integre_cowork": ok_cowork,
        "sha_glm": sha(bloc_glm)[:16],
        "sha_cowork": sha(bloc_cowork)[:16],
    }


def main() -> int:
    data = SKILL.read_bytes()
    taille_avant = len(data)

    if POINTEUR in data:
        # Idempotence : déjà curé — re-vérification byte-identité + NO-OP
        zone, bloc_glm, bloc_cowork = extraire(data) if A_GLM in data else (b"", b"", b"")
        if bloc_glm:
            return noop("blocs encore présents MAIS pointeur présent — état ambigu", taille_avant)
        if not REF.exists():
            return noop("pointeur présent mais référence absente — état ambigu", taille_avant)
        # Recalcul des SHA attendus depuis la référence (prouve la stabilité)
        ref = REF.read_bytes()
        i1 = ref.index(A_GLM)
        i2 = ref.index(A_COWORK)
        i3 = len(ref)
        b1 = ref[i1:i2]
        b2 = ref[i2:i3]
        r = verifier_reference(b1, b2)
        r["verdict"] = "NO-OP (déjà curé) — byte-identité re-prouvée"
        r["taille_skill"] = taille_avant
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0

    # --- Déplacement (all-or-nothing : extraction validée avant écriture) ---
    zone, bloc_glm, bloc_cowork = extraire(data)
    assert len(bloc_glm) >= 1536, f"bloc GLM sous-seuil: {len(bloc_glm)}"
    assert len(bloc_cowork) >= 1536, f"bloc Cowork sous-seuil: {len(bloc_cowork)}"
    assert zone.count(A_GLM) == 1 and zone.count(A_COWORK) == 1

    prov = (
        f"# Instructions plateforme — skill-creator (blocs archivés R4)\n\n"
        f"> **Provenance** : skill `skill-creator` v{VERSION} · sections « Instructions "
        f"spécifiques à GLM.ai » et « Instructions spécifiques à Cowork » · déplacées R4 "
        f"byte-identité vers `references/` le {DATE} (Task 85, re-curation progressive "
        f"disclosure — {PROTO}) · **SHA-256 bloc GLM.ai : `{sha(bloc_glm)[:16]}…`** · "
        f"**SHA-256 bloc Cowork : `{sha(bloc_cowork)[:16]}…`** · le skill intégral demeure "
        f"`skills/skill-creator/SKILL.md` v{VERSION} — les blocs archivés ne sont jamais "
        f"édités (R4 byte-identité).\n\n"
    ).encode()
    REF.write_bytes(prov + bloc_glm + b"\n" + bloc_cowork + b"\n")

    remplacement = RESUME + b"\n\n---\n\n"
    nouveau = data[: data.index(A_GLM)] + remplacement + data[data.index(A_REF):]

    # Invariants post-édition
    assert nouveau.count(A_GLM) == 0, "bloc GLM encore présent après édition"
    assert nouveau.count(A_COWORK) == 0, "bloc Cowork encore présent après édition"
    assert nouveau.count(A_REF) == 1, "section Fichiers de référence altérée"
    assert nouveau.count(POINTEUR) == 1, "pointeur != 1"
    assert "## §0 — Contexte Système".encode() in nouveau, "§0 altéré"

    r = verifier_reference(bloc_glm, bloc_cowork)
    assert r["r4_integre_glm"] and r["r4_integre_cowork"], "byte-identité R4 rompue"

    SKILL.write_bytes(nouveau)
    taille_apres = len(nouveau)

    r.update(
        {
            "verdict": "DÉPLACÉ — POST-1 OK",
            "taille_avant": taille_avant,
            "taille_apres": taille_apres,
            "taille_reference": len(REF.read_bytes()),
            "delta_o": taille_apres - taille_avant,
            "delta_pct": round(100.0 * (taille_apres - taille_avant) / taille_avant, 1),
            "version": f"{VERSION} INCHANGÉE",
        }
    )
    print(json.dumps(r, ensure_ascii=False, indent=2))
    return 0


def noop(msg: str, taille: int) -> int:
    print(json.dumps({"verdict": msg, "taille_skill": taille}, ensure_ascii=False, indent=2))
    return 1


if __name__ == "__main__":
    sys.exit(main())
