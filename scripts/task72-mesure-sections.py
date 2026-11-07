#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.34)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).
"""

"""Task 72 E2 — Mesure des poids par section du SKILL.md gen-plan.

Mesure mécanique (règle d'or n°5) : poids réel de chaque bloc sectionnaire
du SKILL.md, pour piloter la re-curation progressive disclosure (Chantier R1).
Sortie JSON : download/task72-poids-sections-genplan.json
"""
import json
import re
import sys
from pathlib import Path

RACINE = Path("/home/z/my-project")
SKILL = RACINE / "skills" / "gen-plan" / "SKILL.md"
SORTIE = RACINE / "download" / "task72-poids-sections-genplan.json"

MOTIF_SECTION = re.compile(r"^(#{2,3})\s+(.*)$")
MOTIF_BLOC = re.compile(r"^<!--\s*(PATTERN|FIN-PATTERN):([A-Za-z0-9-]+)")


def mesurer() -> dict:
    lignes = SKILL.read_text(encoding="utf-8").splitlines()
    sections: list[dict] = []
    frontmatter_fin = 0
    # frontmatter : jusqu'à la 2e ligne '---'
    nb = 0
    for i, ligne in enumerate(lignes):
        if ligne.strip() == "---":
            nb += 1
            if nb == 2:
                frontmatter_fin = i + 1
                break
    sections.append({
        "section": "(frontmatter)",
        "ligne_debut": 1,
        "ligne_fin": frontmatter_fin,
        "octets": len("\n".join(lignes[:frontmatter_fin]).encode("utf-8")),
    })
    courante = None
    debut = frontmatter_fin
    for i in range(frontmatter_fin, len(lignes)):
        m = MOTIF_SECTION.match(lignes[i])
        if m:
            if courante is not None:
                sections.append(courante)
            courante = {
                "section": m.group(2).strip(),
                "niveau": len(m.group(1)),
                "ligne_debut": i + 1,
                "octets": 0,
                "_debut": i,
            }
    if courante is not None:
        sections.append(courante)
    # remplissage
    for s in sections:
        d = s.get("_debut", 0)
        f = len(lignes)
        for autre in sections:
            if autre is not s and autre.get("_debut", 0) > d and autre["_debut"] < f:
                f = autre["_debut"]
        s["ligne_fin"] = f
        s["octets"] = len("\n".join(lignes[d:f]).encode("utf-8"))
        s.pop("_debut", None)
        s["kio"] = round(s["octets"] / 1024, 1)
        s["tokens_estimes"] = s["octets"] // 4
    total = sum(s["octets"] for s in sections)
    sections_triees = sorted(sections, key=lambda s: -s["octets"])
    return {
        "fichier": str(SKILL),
        "taille_octets": SKILL.stat().st_size,
        "taille_kio": round(SKILL.stat().st_size / 1024, 1),
        "tokens_estimes": SKILL.stat().st_size // 4,
        "nb_lignes": len(lignes),
        "total_sections_octets": total,
        "sections_par_poids": sections_triees,
    }


def main() -> int:
    rapport = mesurer()
    SORTIE.write_text(json.dumps(rapport, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Taille : {rapport['taille_kio']} Kio · ~{rapport['tokens_estimes']} #token · {rapport['nb_lignes']} lignes")
    print(f"{'Octets':>8} {'Kio':>6} {'~tok':>6}  Section (lignes)")
    for s in rapport["sections_par_poids"][:18]:
        print(f"{s['octets']:>8} {s['kio']:>6} {s['tokens_estimes']:>6}  "
              f"{s['section'][:70]} ({s['ligne_debut']}-{s['ligne_fin']})")
    print(f"\nRapport complet : {SORTIE}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
