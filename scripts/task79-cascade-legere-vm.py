#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.37)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).
"""

# -*- coding: utf-8 -*-
"""
Task 79 G2 SG2.3 — Cascade légère re-curation version-management :
  A. skills/KNOWLEDGE.md — Dernière calibration (mention re-curation).
  B. skills/@historique/historiques-par-skill/version-management.md — création
     (vivante v1.3.0 + note re-curation).
  C. pin ECO_SKILLS — commentaire re-curation (version 1.3.0 INCHANGÉE).
Garde-fous : idempotence (NO-OP) ; assert count==1 ; ABANDON rc=2 sans écriture.
"""
import sys
from pathlib import Path

R = Path("/home/z/my-project/KNOWLEDGE-repo")
KB = R / "skills/KNOWLEDGE.md"
HIST = R / "skills/@historique/historiques-par-skill/version-management.md"
PIN = R / "scripts/check-ecosysteme-integrity.py"


def sub(text, old, new, label, n=1):
    c = text.count(old)
    if c != n:
        print("ABANDON : [%s] trouvé %d fois" % (label, c))
        sys.exit(2)
    return text.replace(old, new)


def main():
    if HIST.is_file():
        print("[NO-OP] cascade légère déjà appliquée (historique version-management présent)")
        return 0

    # --- A. KB
    a = KB.read_text(encoding="utf-8")
    a = sub(a, "- **Dernière calibration** : 2026-11-07 (Task 69 G2 — directive n°8 item 1 « effectue $FACON la résorption structurelle de la volatilité de version-management »",
            "- **Dernière calibration** : 2026-11-08 (Task 79 G2 — directive trace 1a1bc0ad4607c95d « re-curation version-management si judicieuse » — "
            "**re-curation progressive disclosure** : 47 244 → 25 783 o [46,1 → 25,2 Kio, −45,4 %, LOURD → INTERMÉDIAIRE] ; 7 blocs ≥ 1,6 Kio "
            "déplacés R4 byte-identité vers references/ [controle-chemins · regles-structure-fichiers · points-entree-edition · "
            "sortie-flux-send-file · structure-meta-json · aide-memoire-operations · resorption-structurelle] avec en-têtes de provenance "
            "SHA-256 ; méthode moves-r4-pur arbitrée --compare ; pointeurs 1-ligne inline ; contrats intacts [§0 byte-identique prouvé git, "
            "read_when/evals/description PASS] ; POST ×2 MAINTIEN DE L'OPTIMISATION ; check-recuration C1-C4 PASS ; sync miroir même passe "
            "[contrainte file Task 72]) ; précédente calibration 2026-11-07 (Task 69 G2 — directive n°8 item 1 « effectue $FACON la résorption structurelle de la volatilité de version-management »",
            "KB Dernière calibration")

    # --- B. historiques-par-skill/version-management.md (création)
    b = (
        "# Historique du skill version-management\n\n"
        "> **Version vivante (installée)** : v1.3.0 — `skills/version-management/SKILL.md` (le registre KB "
        "`skills/KNOWLEDGE.md` fait foi)\n"
        "> **Version vivante (corpus PM)** : — (version-management n'est pas une famille PM — skill métier)\n"
        "> **Versions archivées** : 0 (aucune montée archivée — le skill n'est pas passé par KO-L004)\n\n"
        "## Re-curations et calibrations\n\n"
        "| Version | Date | Événement |\n"
        "|---------|------|-----------|\n"
        "| v1.3.0 | 2026-11-08 | Task 79 G2 (session web-ecef7f80 — directive trace 1a1bc0ad4607c95d) : re-curation "
        "progressive disclosure — 47 244 → 25 783 o (−45,4 %, LOURD → INTERMÉDIAIRE) ; 7 blocs ≥ 1,6 Kio déplacés R4 "
        "byte-identité vers `references/` (controle-chemins · regles-structure-fichiers · points-entree-edition · "
        "sortie-flux-send-file · structure-meta-json · aide-memoire-operations · resorption-structurelle) ; méthode "
        "moves-r4-pur arbitrée --compare ; POST ×2 MAINTIEN ; C1-C4 PASS ; sync miroir même passe |\n"
        "| v1.3.0 | 2026-11-07 | Task 69 G2 : MINOR v1.2.0→v1.3.0 — résorption structurelle (watchdog + journal "
        "forensique + §8 neutralisation résiliente) |\n"
        "| v1.1.0 | 2026-10-04 | Task 25 : Description Optimization A10/A14 (radicaux discriminants ajoutés) |\n"
        "| v1.0.0 | 2026-10-02 | Note P-H : entrée KB créée, frontmatter normalisé |\n"
    )

    # --- C. pin (commentaire, version inchangée)
    c = PIN.read_text(encoding="utf-8")
    c = sub(c, '    "version-management": "1.3.0",\n',
            '    "version-management": "1.3.0",  # re-curation Task 79 G2 (2026-11-08) : 46,1→25,2 Kio, 7 blocs R4 references/ — version inchangée (contrats intacts)\n',
            "pin commentaire")

    KB.write_text(a, encoding="utf-8")
    HIST.write_text(b, encoding="utf-8")
    PIN.write_text(c, encoding="utf-8")
    print("Cascade légère écrite : KB (Dernière calibration re-curation) · historiques-par-skill/version-management.md "
          "(créé) · pin ECO_SKILLS (commentaire, v1.3.0 inchangée)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
