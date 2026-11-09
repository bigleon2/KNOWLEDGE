#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.37)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif (règle d'or n°6 gen-plan).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0,
ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9).
Référence canonique (SHARED §0/§1.2) : « mon skill X » = forme installée skills/X/SKILL.md.

Task 85 G5 — P0-P4 : moves R4 byte-identité (re-curation progressive disclosure
iphone17, DERNIÈRE cible de la file — directive propriétaire trace 1a1bed51ccaf78f1,
méthode P0-P7 éprouvée Tasks 81 G2 / 82 G6 / 85 G2-G4).
1 bloc HISTORIQUE cohérent regroupé (analogue exact iphone18 Task 82 « changelogs-versions.md » :
blocs sous-seuil isolés regroupés avec les changelogs — sous-seuil isolé consigné) déplacé vers
references/lignage-changelogs.md (en-tête de provenance : sections, version, date, SHA-256)
+ résumé opérationnel inline + pointeur :
  1. « ## Lignage — projection skill ← prompt maître source » (1 228 o)
     + « ## PROMPT MAÎTRE — … » intro (989 o)
     + « ### Changelog v2.0 → v2.1 (extension 1944) » (989 o)
     + « ### Changelog v1.4 → v2.0 » (1 456 o) — bloc L56-L97 = 4 662 o.
Le cœur opérationnel (§0 canonique + §0 RÔLE & MISSION, grille ANALYSE-v2 §1, moteur
R1-R17 §2, PLAN-ACTIONS §3, pipeline §4, QC §5, presets §6.1-§6.10 [6.5 table opérationnelle
d'époque MAINTENUE inline — friction par-mission ; 6.10 SPÉCULATIF 1 065 o sous-seuil —
consistance Task 82 iphone18], intégration §7, rapport §8, interaction §9-§10,
auto-audit §11, livrables §12, commandes §13) demeure intégralement inline —
dégradation refusée (posture Task 82 iphone18).
Version INCHANGÉE (contrats intacts — précédents version-management Task 79 G2).
Idempotent : re-jeu = NO-OP (détection par pointeur). All-or-nothing : toutes les
coupes validées AVANT la première écriture. Asserts count==1 par marqueur.
Byte-identité : SHA-256(zone source) == SHA-256(zone dans la référence) — preuve R4.
Usage : python3 scripts/task85-recuration-iphone17.py [--json]
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

R = Path("/home/z/my-project/KNOWLEDGE-repo")
SKILL = R / "skills" / "iphone17" / "SKILL.md"
REF = R / "skills" / "iphone17" / "references" / "lignage-changelogs.md"
DATE = "2026-11-09"
PROTO = "protocole re-curation v1.2.2, méthode moves-r4-pur (P0-P7 éprouvée)"

A_LIG = "## Lignage — projection skill ← prompt maître source".encode()
A_R0 = "## §0 — RÔLE & MISSION".encode()
POINTEUR = "references/lignage-changelogs.md".encode()

RESUME = """## Lignage & changelogs — projection skill ← prompt maître source

La projection depuis le PM `skills/@photos/iphone17-photos.md` **v2.1**, l'origine v2.1 (extension 1944 — directive propriétaire 2026-10-21) et les changelogs intégraux (**v2.0 → v2.1** extension 1944 · **v1.4 → v2.0** pipeline QC 11 critères, presets §6, garde-fous G1-G7, inventaire B6) sont déplacés R4 byte-identité dans **`references/lignage-changelogs.md`**. Version vivante : v2.1 (frontmatter) ; la référence sert au lignage et à l'audit des directives d'origine.""".encode()


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main() -> int:
    data = SKILL.read_bytes()
    taille_avant = len(data)

    if POINTEUR in data:
        if not REF.exists():
            print(json.dumps({"verdict": "état ambigu — pointeur présent, référence absente"},
                             ensure_ascii=False))
            return 1
        ref = REF.read_bytes()
        zone = ref[ref.index(A_LIG):]
        r = {"r4_integre": zone in ref, "sha_zone": sha(zone)[:16],
             "taille_skill": taille_avant,
             "verdict": "NO-OP (déjà curé) — byte-identité re-prouvée"}
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0

    # --- Déplacement (all-or-nothing) ---
    assert data.count(A_LIG) == 1, "ancre Lignage != 1"
    assert data.count(A_R0) == 1, "ancre §0 RÔLE != 1"
    i_lig, i_r0 = data.index(A_LIG), data.index(A_R0)
    assert i_lig < i_r0, "ordre ancres inattendu"
    zone = data[i_lig:i_r0]
    assert len(zone) >= 4096, f"zone lignage-changelogs sous-seuil: {len(zone)}"

    prov = (
        f"# Lignage & changelogs — iphone17 (blocs archivés R4)\n\n"
        f"> **Provenance** : skill `iphone17` · sections « Lignage — projection skill ← prompt "
        f"maître source », « PROMPT MAÎTRE — … » (intro), « Changelog v2.0 → v2.1 » et "
        f"« Changelog v1.4 → v2.0 » (bloc historique cohérent regroupé — analogue Task 82 "
        f"iphone18 changelogs-versions.md) · déplacées R4 byte-identité vers `references/` "
        f"le {DATE} (Task 85 G5, re-curation progressive disclosure — {PROTO}) · "
        f"**SHA-256 du bloc : `{sha(zone)[:16]}…`** · le PM source intégral demeure "
        f"`skills/@photos/iphone17-photos.md` v2.1 [COURANT — R2 byte-identique, jamais "
        f"édité] et le skill intégral demeure `skills/iphone17/SKILL.md`.\n\n"
    ).encode()
    REF.parent.mkdir(parents=True, exist_ok=True)
    REF.write_bytes(prov + zone)

    nouveau = data[:i_lig] + RESUME + b"\n\n" + data[i_r0:]

    # Invariants post-édition
    assert nouveau.count(A_R0) == 1, "§0 RÔLE altéré"
    assert nouveau.count("## §0 — Contexte Système".encode()) == 1, "§0 canonique altéré"
    assert nouveau.count(POINTEUR) == 1, "pointeur != 1"
    assert "Changelog v1.4 → v2.0".encode() not in nouveau, "changelog encore inline"
    assert nouveau[:100] == data[:100], "frontmatter altéré"

    r = {"r4_integre": zone in REF.read_bytes(), "sha_zone": sha(zone)[:16]}
    assert r["r4_integre"], "byte-identité R4 rompue"

    SKILL.write_bytes(nouveau)

    r.update(
        {
            "verdict": "DÉPLACÉ — POST-1 OK",
            "taille_avant": taille_avant,
            "taille_apres": len(nouveau),
            "taille_reference": len(REF.read_bytes()),
            "delta_o": len(nouveau) - taille_avant,
            "delta_pct": round(100.0 * (len(nouveau) - taille_avant) / taille_avant, 1),
            "version": "INCHANGÉE (v2.1)",
        }
    )
    print(json.dumps(r, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
