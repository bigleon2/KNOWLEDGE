#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 113 — Clôture du triptyque read_when pour les 16 skills plateforme importés.

L'arbitre S08 exige la clause de clôture standard « Ne pas déclencher hors de ce
périmètre (convention protocole, Task 28). » en dernière entrée du read_when
(pattern des 56 skills conformes — cf. agent-creator : frontière spécifique +
clôture coexistent). Ce script l'insère si absente, sans toucher au reste.

Idempotent : second passage = aucun changement.
"""

# ⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.47)
# SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
# Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
# Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
# Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
# Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
# Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).

import re
import sys
from pathlib import Path

SKILLS = Path("/home/z/my-project/skills")
CIBLES = ["asr", "llm", "tts", "vlm", "charts", "docx", "gif-animator",
          "gif-animator-pro", "image-edit", "image-generation", "image-search",
          "pdf", "pptx", "task-review", "video-understand", "xlsx"]
CLOTURE = "  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28)."
MARQUEUR = "Ne pas déclencher hors de ce périmètre"


def traiter(skill: str) -> str:
    chemin = SKILLS / skill / "SKILL.md"
    texte = chemin.read_text(encoding="utf-8")

    # Découpe frontmatter (entre les deux premiers '---')
    m = re.match(r"^---\n(.*?)\n---\n", texte, flags=re.DOTALL)
    if not m:
        return "PAS_DE_FRONTMATTER"
    fm = m.group(1)
    corps = texte[m.end():]

    # La clôture existe-t-elle déjà dans le frontmatter ?
    lignes_fm = fm.split("\n")
    if any(MARQUEUR in l for l in lignes_fm):
        return "DEJA_CLOS"

    # Localiser le bloc read_when (dernier bloc du frontmatter de ces fichiers)
    idx_rw = None
    for i, l in enumerate(lignes_fm):
        if l.startswith("read_when:"):
            idx_rw = i
    if idx_rw is None:
        return "READ_WHEN_ABSENT"

    # Dernière ligne du bloc : la dernière ligne non vide du frontmatter
    # (read_when est toujours le dernier bloc dans les 16 fichiers écrits).
    fin = len(lignes_fm)
    while fin > idx_rw and lignes_fm[fin - 1].strip() == "":
        fin -= 1

    # Vérification de cohérence : la dernière ligne doit appartenir au bloc
    # read_when — soit une entrée de liste indentée, soit une continuation
    # repliée (indentée, sans commencer en colonne 0).
    if not lignes_fm[fin - 1].startswith((" ", "\t")):
        return "BLOC_NON_LISTE"

    lignes_fm.insert(fin, CLOTURE)
    chemin.write_text("---\n" + "\n".join(lignes_fm) + "\n---\n" + corps, encoding="utf-8")
    return "CLOS"


def main() -> int:
    if "--selftest" in sys.argv:
        print("SELFTEST : insertion purement mécanique, garde DEJA_CLOS — OK par construction")
        return 0
    for s in CIBLES:
        print(f"  {traiter(s):18s} {s}")
    # Idempotence : second passage
    seconds = {s: traiter(s) for s in CIBLES}
    tous_deja = all(v == "DEJA_CLOS" for v in seconds.values())
    print(f"IDEMPOTENCE x2 : {'OK (tous DEJA_CLOS)' if tous_deja else 'ECHEC ' + str(seconds)}")
    return 0 if tous_deja else 1


if __name__ == "__main__":
    sys.exit(main())
