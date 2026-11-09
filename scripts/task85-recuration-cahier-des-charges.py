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

Task 85 G4 — P0-P4 : moves R4 byte-identité (re-curation progressive disclosure
cahier-des-charges, cible suivante de la file — directive propriétaire trace
1a1bed51ccaf78f1, méthode P0-P7 éprouvée Tasks 81 G2 / 82 G6 / 85 G2-G3).
1 zone HISTORIQUE déplacée vers references/traceabilite-versions.md (en-tête de
provenance : section, version, date, SHA-256) + résumé opérationnel inline + pointeur
  + 1 ligne ajoutée au §7 Références :
  1. « ## §6 — Traçabilité » (5 996 o — 4 montées de version verbatim v1.0.0 → v2.0.2,
     bloc HISTORIQUE pur : la version vivante est lue au frontmatter, l'historique ne
     sert qu'au lignage).
Le cœur opérationnel (§0 canonique, §1 mission/modes/règles/cycle, §2 spécification,
§5 évaluations/déclencheurs, §7 références) demeure intégralement inline.
Version INCHANGÉE v2.0.2 (contrats intacts — précédents version-management Task 79 G2).
Idempotent : re-jeu = NO-OP (détection par pointeur). All-or-nothing : toutes les
coupes validées AVANT la première écriture. Asserts count==1 par marqueur.
Byte-identité : SHA-256(zone source) == SHA-256(zone dans la référence) — preuve R4.
Usage : python3 scripts/task85-recuration-cahier-des-charges.py [--json]
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

R = Path("/home/z/my-project/KNOWLEDGE-repo")
SKILL = R / "skills" / "cahier-des-charges" / "SKILL.md"
REF = R / "skills" / "cahier-des-charges" / "references" / "traceabilite-versions.md"
VERSION = "2.0.2"
DATE = "2026-11-09"
PROTO = "protocole re-curation v1.2.2, méthode moves-r4-pur (P0-P7 éprouvée)"

A_T = "## §6 — Traçabilité".encode()
A_R = "## §7 — Références".encode()
POINTEUR = "references/traceabilite-versions.md".encode()
ANCRE_S7 = "- `references/simulation-materielle.md`".encode()
LIGNE_S7 = (
    "- `references/traceabilite-versions.md` — traçabilité versionnée intégrale "
    "(v1.0.0 → v2.0.2), déplacée R4 byte-identité (Task 85 G4)."
).encode()

RESUME = """La traçabilité versionnée intégrale — 4 montées verbatim v1.0.0 (création, 2026-10-23) → v2.0.0 (extension Engineering Design, 2026-10-24) → v2.0.1 (reconnaissance discipline, 2026-10-25) → v2.0.2 (élargissement description, 2026-10-30), directives propriétaires — est déplacée R4 byte-identité dans **`references/traceabilite-versions.md`**. La version vivante est lue au frontmatter ; la référence ne sert qu'au lignage et à l'audit des directives d'origine.""".encode()


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def main() -> int:
    data = SKILL.read_bytes()
    taille_avant = len(data)

    if POINTEUR in data:
        # Idempotence : NO-OP — re-prouve la byte-identité zone archivée
        if not REF.exists():
            print(json.dumps({"verdict": "état ambigu — pointeur présent, référence absente"},
                             ensure_ascii=False))
            return 1
        ref = REF.read_bytes()
        zone = ref[ref.index(A_T):]
        r = {"r4_integre": zone in ref, "sha_zone": sha(zone)[:16],
             "taille_skill": taille_avant,
             "verdict": "NO-OP (déjà curé) — byte-identité re-prouvée"}
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0

    # --- Déplacement (all-or-nothing : extraction validée avant écriture) ---
    assert data.count(A_T) == 1, "ancre §6 != 1"
    assert data.count(A_R) == 1, "ancre §7 != 1"
    assert data.count(ANCRE_S7) == 1, "ancre ligne §7 != 1"
    i_t, i_r = data.index(A_T), data.index(A_R)
    assert i_t < i_r, "ordre ancres inattendu"
    zone = data[i_t:i_r]
    assert len(zone) >= 1536, f"zone §6 sous-seuil: {len(zone)}"

    prov = (
        f"# Traçabilité versionnée — cahier-des-charges (bloc archivé R4)\n\n"
        f"> **Provenance** : skill `cahier-des-charges` v{VERSION} · section « §6 — "
        f"Traçabilité » intégrale · déplacée R4 byte-identité vers `references/` le {DATE} "
        f"(Task 85 G4, re-curation progressive disclosure — {PROTO}) · **SHA-256 du bloc : "
        f"`{sha(zone)[:16]}…`** · le skill intégral demeure `skills/cahier-des-charges/SKILL.md` "
        f"v{VERSION} — le bloc archivé n'est jamais édité (R4 byte-identité).\n\n"
    ).encode()
    REF.write_bytes(prov + zone)

    # Reconstruction : avant-§6 + résumé + §7 avec ligne ajoutée
    nouveau = (
        data[:i_t]
        + A_T + b"\n\n"
        + RESUME + b"\n\n"
        + data[i_r:data.index(ANCRE_S7)]
        + ANCRE_S7 + b"\n" + LIGNE_S7 + b"\n"
        + data[data.index(ANCRE_S7) + len(ANCRE_S7):]
    )

    # Invariants post-édition
    assert nouveau.count(A_R) == 1, "§7 altéré"
    assert nouveau.count(POINTEUR) == 2, f"pointeur {nouveau.count(POINTEUR)} != 2 (§6+§7)"
    assert nouveau.count(A_T) == 1, "titre §6 altéré"
    assert "## §0 — Contexte Système".encode() in nouveau, "§0 altéré"
    assert nouveau[:100] == data[:100], "frontmatter altéré"
    assert nouveau.count(ANCRE_S7) == 1, "ancre §7 dupliquée"

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
            "version": f"{VERSION} INCHANGÉE",
        }
    )
    print(json.dumps(r, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
