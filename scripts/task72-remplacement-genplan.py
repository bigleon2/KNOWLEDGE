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

"""Task 72 G1 SG1.2 — Remplacement inline par résumés opérationnels NOUVEAUX.

Applique au SKILL.md gen-plan (v3.38.0 → v3.39.0) les remplacements des blocs
extraits par task72-extraction-genplan.py : chaque bloc déplacé en references/
est remplacé par un résumé NOUVEAU (texte inédit, pas une copie partielle —
D004 sans duplication) + pointeur à condition de lecture.
Marqueurs uniquement (jamais de numéros de ligne) — ordre descendant.
"""
import re
import sys
from pathlib import Path

RACINE = Path("/home/z/my-project")
SKILL = RACINE / "skills" / "gen-plan" / "SKILL.md"

sys.path.insert(0, str(RACINE / "scripts"))
from task72_remplacement_constantes import (  # noqa: E402
    RESUME_E1RES_E7DISP, RESUME_REGLES, RESUME_DISCIPLINES, RESUME_LECONS,
    RESUME_ROUTAGE, RESUME_PHILO4, RESUME_CONTINGENCES, RESUME_MODE_STEP,
    RESUME_JOURNAL, ARBRE,
)


def trancher(lignes, debut, fin=None):
    """[i0, i1) : de la ligne contenant debut à la ligne contenant fin (exclue)."""
    i0 = i1 = None
    for i, l in enumerate(lignes):
        if debut in l and i0 is None:
            i0 = i
        if fin is not None and fin in l and i0 is not None and i >= i0:
            i1 = i
            break
    if i0 is None or (fin is not None and i1 is None):
        raise SystemExit(f"ABANDON : marqueur introuvable ({debut!r} / {fin!r})")
    return i0, (i1 if fin is not None else i0 + 1)


def remplacer(lignes, debut, fin, nouveau, inclure_fin=False):
    a, b = trancher(lignes, debut, fin)
    if inclure_fin:
        b = b + 1  # la ligne de fin est incluse
    vieux = "\n".join(lignes[a:b])
    lignes[a:b] = nouveau.splitlines()
    return vieux


def main() -> int:
    lignes = SKILL.read_text(encoding="utf-8").splitlines()
    trace = []

    # 1. §5.6 journal : titre + toutes les entrées → titre nouveau + mécanique + entrée courante
    a, _ = trancher(lignes, "### §5.6 Journal des versions", None)
    trace.append(("journal", len(lignes[a:]), len(RESUME_JOURNAL.splitlines())))
    lignes[a:] = RESUME_JOURNAL.splitlines()

    # 2. §5.5 mode step
    vieux = remplacer(lignes, "### §5.5 Mode step", "### §5.6 Journal des versions", RESUME_MODE_STEP)
    trace.append(("mode_step", vieux.count("\n") + 1, len(RESUME_MODE_STEP.splitlines())))

    # 3. contingences §4
    vieux = remplacer(lignes, "- **Coefficient profil frais local",
                      "- **Contingence récupération externe bloquée", RESUME_CONTINGENCES, inclure_fin=True)
    trace.append(("contingences", vieux.count("\n") + 1, len(RESUME_CONTINGENCES.splitlines())))

    # 4. §1.16 routage
    vieux = remplacer(lignes, "### §1.16 Routage", "## §2 — Spécification technique", RESUME_ROUTAGE)
    trace.append(("routage", vieux.count("\n") + 1, len(RESUME_ROUTAGE.splitlines())))

    # 5. §1.14 + §1.15 leçons
    vieux = remplacer(lignes, "### §1.14 Leçons", "### §1.16 Routage", RESUME_LECONS)
    trace.append(("lecons", vieux.count("\n") + 1, len(RESUME_LECONS.splitlines())))

    # 6. §1.6 disciplines
    vieux = remplacer(lignes, "### §1.6 Disciplines", "### §1.7 Pipeline", RESUME_DISCIPLINES)
    trace.append(("disciplines", vieux.count("\n") + 1, len(RESUME_DISCIPLINES.splitlines())))

    # 7. §1.5 règles d'or
    vieux = remplacer(lignes, "### §1.5 Règles d'or", "### §1.6 Disciplines", RESUME_REGLES)
    trace.append(("regles", vieux.count("\n") + 1, len(RESUME_REGLES.splitlines())))

    # 8. philosophie #4 (ligne unique)
    a, b = trancher(lignes, "4. **Parallélisation par défaut", None)
    trace.append(("philo4", 1, 1))
    lignes[a:b] = RESUME_PHILO4.splitlines()

    # 9. PATTERN E1-RES + E7-DISP (blocs inclusifs)
    vieux = remplacer(lignes, "<!-- PATTERN:GEN-PLAN-HOOKS-E1-RES-v1.0.0 -->",
                      "<!-- FIN-PATTERN:GEN-PLAN-HOOKS-E7-DISP-v1.0.0 -->",
                      RESUME_E1RES_E7DISP, inclure_fin=True)
    trace.append(("hooks_patterns", vieux.count("\n") + 1, len(RESUME_E1RES_E7DISP.splitlines())))

    # 10. §2.2 arbre (bloc fenced contenant "├── SKILL.md")
    idx = next(i for i, l in enumerate(lignes) if "├── SKILL.md" in l)
    debut_fence = max(i for i in range(idx + 1) if lignes[i].strip() == "```")
    fin_fence = next(i for i in range(idx + 1, len(lignes)) if lignes[i].strip() == "```")
    trace.append(("arbre", fin_fence - debut_fence + 1, len(ARBRE.splitlines())))
    lignes[debut_fence:fin_fence + 1] = ARBRE.splitlines()

    # 11. frontmatter : version + description
    for i, l in enumerate(lignes):
        if l.strip() == "version: 3.38.0":
            lignes[i] = "version: 3.39.0"
            break
    else:
        raise SystemExit("ABANDON : version 3.38.0 introuvable au frontmatter")
    idx_desc = next(i for i, l in enumerate(lignes)
                    if "glossaire alias-eco inline $FACON/$FACON2" in l)
    lignes.insert(idx_desc + 1,
                  "  progressive disclosure R1 (v3.39.0) : résumés inline, intégraux en references/ à la demande")
    trace.append(("frontmatter", 0, 1))

    taille = len(("\n".join(lignes) + "\n").encode("utf-8"))
    if "--dry-run" in sys.argv:
        print(f"DRY-RUN SG1.2 : taille cible = {taille} octets = {taille/1024:.1f} Kio ≈ {taille//4} #token"
              + (" — < 30 Kio OK" if taille < 30 * 1024 else " — DÉPASSE 30 Kio, ajuster les résumés"))
        return 0
    SKILL.write_text("\n".join(lignes) + "\n", encoding="utf-8")
    for nom, avant, apres in trace:
        print(f"  {nom:<16} {avant:>4} lignes → {apres:>4} lignes")
    print(f"SG1.2 : SKILL.md v3.39.0 = {taille} octets = {taille/1024:.1f} Kio ≈ {taille//4} #token")
    return 0


if __name__ == "__main__":
    sys.exit(main())
