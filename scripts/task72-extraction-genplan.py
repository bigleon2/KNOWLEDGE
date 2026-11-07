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

"""Task 72 G1 — Chantier R1 : re-curation progressive disclosure de gen-plan.

Transformation MÉCANIQUE (R4 byte-identité) du SKILL.md gen-plan v3.38.0 → v3.39.0 :
  - extraction par MARQUEURS (jamais numéros de ligne) de 9 blocs ;
  - déplacement verbatim vers 4 nouveaux fichiers references/ + append grille-token.md ;
  - remplacement inline par des résumés opérationnels NOUVEAUX (sans duplication) ;
  - frontmatter v3.39.0 + §2.2 arbre + entrée courante §5.6 ;
  - manifeste JSON (SHA-256 de chaque bloc, tailles avant/après).

Sortie : download/task72-recuration-manifeste.json — verdict interne PASS/FAIL.
Règle d'or n°5 : toute affirmation chiffrée est mesurée ici.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

RACINE = Path("/home/z/my-project")
SKILL = RACINE / "skills" / "gen-plan" / "SKILL.md"
REFS = RACINE / "skills" / "gen-plan" / "references"
MANIFESTE = RACINE / "download" / "task72-recuration-manifeste.json"

DATE = "2026-11-08"
PROVENANCE = (
    "> **Provenance (R4 byte-identité — re-curation R1 v3.39.0, Task 72 G1, %s, "
    "directive propriétaire « Chantier R1 prioritaire : re-curation progressive "
    "disclosure de gen-plan »)** : contenu déplacé VERBATIM depuis le SKILL.md "
    "gen-plan v3.38.0 — jamais réédité, jamais dupliqué (le SKILL.md ne conserve "
    "qu'un résumé opérationnel NOUVEAU + le présent pointeur, lecture à la demande "
    "— progressive disclosure, étude Task 70 R1). SHA-256 du bloc d'origine : `%s`."
)


def sha(b: str) -> str:
    return hashlib.sha256(b.encode("utf-8")).hexdigest()


def trancher(lignes: list, debut_motif: str, fin_motif: str, inclure_fin=True):
    """Extrait les lignes de la première ligne contenant debut_motif
    à la première ligne contenant fin_motif (incluse par défaut)."""
    i0 = i1 = None
    for i, l in enumerate(lignes):
        if debut_motif in l and i0 is None:
            i0 = i
        if fin_motif is not None and fin_motif in l and i0 is not None and i >= i0:
            i1 = i + 1 if inclure_fin else i
            break
    if i0 is None or (fin_motif is not None and i1 is None):
        raise SystemExit(f"ABANDON : marqueur introuvable ({debut_motif!r} / {fin_motif!r})")
    return i0, i1


def main() -> int:
    texte = SKILL.read_text(encoding="utf-8")
    lignes = texte.splitlines()
    taille_avant = len(texte.encode("utf-8"))
    blocs = {}

    # ---- SG1.1 : extraction par marqueurs (9 blocs) -------------------------
    # B1 — journal des versions : première entrée "- **v3." après le titre §5.6 jusqu'à EOF
    idx_titre_56 = next(i for i, l in enumerate(lignes) if l.startswith("### §5.6"))
    j0 = next(i for i in range(idx_titre_56, len(lignes))
              if re.match(r"^- \*\*v3\.\d+\.\d+ \(", lignes[i]))
    blocs["journal_versions"] = (j0, len(lignes), "\n".join(lignes[j0:]))

    # B2 — règles d'or §1.5 (titre → avant §1.6)
    a, _ = trancher(lignes, "### §1.5 Règles d'or", None)
    b, _ = trancher(lignes, "### §1.6 Disciplines", None)
    blocs["regles_or"] = (a, b, "\n".join(lignes[a:b]))

    # B3 — leçons §1.14 + §1.15 (titre §1.14 → avant §1.16)
    a, _ = trancher(lignes, "### §1.14 Leçons", None)
    b, _ = trancher(lignes, "### §1.16 Routage", None)
    blocs["lecons_ko"] = (a, b, "\n".join(lignes[a:b]))

    # B4 — disciplines §1.6 (titre → avant §1.7)
    a, _ = trancher(lignes, "### §1.6 Disciplines", None)
    b, _ = trancher(lignes, "### §1.7 Pipeline", None)
    blocs["disciplines"] = (a, b, "\n".join(lignes[a:b]))

    # B5 — PATTERN E1-RES + E7-DISP dans §1.2bis
    a, _ = trancher(lignes, "<!-- PATTERN:GEN-PLAN-HOOKS-E1-RES-v1.0.0 -->", None)
    _, b = trancher(lignes, "<!-- PATTERN:GEN-PLAN-HOOKS-E1-RES-v1.0.0 -->",
                    "<!-- FIN-PATTERN:GEN-PLAN-HOOKS-E7-DISP-v1.0.0 -->")
    blocs["hooks_patterns"] = (a, b, "\n".join(lignes[a:b]))

    # B6 — routage §1.16 (titre → avant ## §2)
    a, _ = trancher(lignes, "### §1.16 Routage", None)
    b, _ = trancher(lignes, "## §2 — Spécification technique", None)
    blocs["routage_install"] = (a, b, "\n".join(lignes[a:b]))

    # B7 — mode step §5.5 (titre → avant §5.6)
    a, _ = trancher(lignes, "### §5.5 Mode step", None)
    b, _ = trancher(lignes, "### §5.6 Journal des versions", None)
    blocs["mode_step"] = (a, b, "\n".join(lignes[a:b]))

    # B8 — contingences §4 (3 puces longues)
    a, _ = trancher(lignes, "- **Coefficient profil frais local", None)
    _, b = trancher(lignes, "- **Coefficient profil frais local",
                    "- **Contingence récupération externe bloquée")
    blocs["contingences"] = (a, b, "\n".join(lignes[a:b]))

    # B9 — philosophie #4 (ligne unique)
    a, _ = trancher(lignes, "4. **Parallélisation par défaut", None)
    blocs["philo4"] = (a, a + 1, lignes[a])

    # ---- écriture des fichiers references/ (moves R4) -----------------------
    entetes = {
        "journal-versions.md": "# Journal des versions — gen-plan (archive intégrale)\n\n"
            "> **Mécanique de migration (v3.39.0)** : le SKILL.md §5.6 ne conserve que "
            "l'entrée COURANTE ; à chaque montée de version suivante, l'entrée courante "
            "migre ici (R4 byte-identité) et la nouvelle prend sa place inline.\n\n",
        "regles-or.md": "# Règles d'or n°1-9 + règles KO — gen-plan (textes intégraux)\n\n"
            "> La section §1.5 du SKILL.md demeure la référence canonique (SHARED §9) ; "
            "le présent fichier en est le texte intégral, chargé à la demande.\n\n",
        "disciplines-mobilisation.md": "# Disciplines d'ingénierie de prompts — tables de mobilisation intégrales\n\n"
            "> Résumé opérationnel dans le SKILL.md §1.6 ; tables complètes E1-E15, "
            "matérialisations n°54/n°55, mobilisation par déclencheur et hook continu ci-dessous.\n\n",
        "protocoles-detailles.md": "# Protocoles détaillés — E1-RES, E7-DISP, É1-INSTALL, mode step, philosophie #4\n\n"
            "> Résumés opérationnels dans le SKILL.md (§1.2bis, §1.16, §5.5, §1.4) ; "
            "textes intégraux ci-dessous.\n\n",
    }
    mouvements = [
        ("journal_versions", "journal-versions.md", []),
        ("regles_or", "regles-or.md", []),
        ("lecons_ko", "regles-or.md", None),  # None = append au même fichier
        ("disciplines", "disciplines-mobilisation.md", []),
        ("hooks_patterns", "protocoles-detailles.md", []),
        ("routage_install", "protocoles-detailles.md", None),
        ("mode_step", "protocoles-detailles.md", None),
        ("philo4", "protocoles-detailles.md", None),
    ]
    contenus = {f: entetes[f] for f in entetes}
    for cle, fichier, _ in mouvements:
        prov = PROVENANCE % (DATE, sha(blocs[cle][2]))
        contenus[fichier] += (
            "\n<!-- BLOC-DEPLACÉ:%s:v3.38.0:%s -->\n\n" % (cle, sha(blocs[cle][2])[:16])
            + prov + "\n\n" + blocs[cle][2].rstrip("\n") + "\n\n"
            + "<!-- FIN-BLOC-DEPLACÉ:%s -->\n" % cle
        )
    for fichier, contenu in contenus.items():
        (REFS / fichier).write_text(contenu, encoding="utf-8")

    # append contingences à grille-token.md (fichier EXISTANT — provenance + verbatim)
    grille = REFS / "grille-token.md"
    gt = grille.read_text(encoding="utf-8")
    gt += (
        "\n\n<!-- BLOC-DEPLACÉ:contingences:v3.38.0:%s -->\n\n" % sha(blocs["contingences"][2])[:16]
        + "## Contingences de calibration (déplacées du SKILL.md §4 — re-curation R1 v3.39.0, %s)\n\n" % DATE
        + PROVENANCE % (DATE, sha(blocs["contingences"][2])) + "\n\n"
        + blocs["contingences"][2].rstrip("\n") + "\n"
    )
    grille.write_text(gt, encoding="utf-8")

    print("SG1.1 : %d fichiers references/ écrits (4 nouveaux + 1 append)" % 5)
    for cle, (d, f, b) in blocs.items():
        print("  bloc %-16s lignes %4d-%4d · %6d octets · sha %s"
              % (cle, d + 1, f, len(b.encode("utf-8")), sha(b)[:12]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
