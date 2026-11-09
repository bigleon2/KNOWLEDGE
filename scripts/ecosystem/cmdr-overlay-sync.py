#!/usr/bin/env python3
"""cmdr-overlay-sync.py — D6 du PM ghorg-to-ecosysteme.md v1.1 : superposition TSI vers le clone CMDR.

Principes (règles d'or 7-8 du PM) :
  - copie à SENS UNIQUE KNOWLEDGE → cmdr/ecosystem/ (KNOWLEDGE = source de vérité) ;
  - chaque fichier copié est comparé par SHA-256 : identique = non réécrit (aucun changement git) ;
  - un fichier présent dans ecosystem/ mais plus dans la sélection n'est supprimé QUE s'il
    figurait dans le SOURCE.md précédent (jamais de suppression de fichiers inconnus) ;
  - AUCUN fichier touché hors ecosystem/ (vérifié par git diff --stat) ;
  - refus si le clone est sale (S=1) ; basculement sur la branche overlay si besoin.

Sortie : JSON {copies, inchanges, supprimes, absents, branche, source_md}. Exit 0 idempotent.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _commun import (  # noqa: E402
    BRANCHE_SUPERPOSITION, CMDR, KNOWLEDGE, branche_courante, git, horodatage,
    maj_etat, porcelain_vide, sha256_fichier,
)

# Task 70 G3 : la sélection vit désormais sous skills/@GHORG-ecosysteme/ du dépôt
# (git mv R4) ; DEST = cmdr/ecosystem/ (dans le clone CMDR) reste INCHANGÉ.
SELECTION = KNOWLEDGE / "skills" / "@GHORG-ecosysteme" / "selection-tsi.yaml"
DEST = CMDR / "ecosystem"
SOURCE_MD = DEST / "SOURCE.md"
MENTION = "fichiers générés, ne pas modifier ici"


def lire_selection(chemin):
    """Analyse la sélection YAML (sous-ensemble : entrées '- source:' + clés indentées).

    Parseur minimal stdlib : la sélection est écrite par l'écosystème, structure garantie.
    """
    entrees, cour = [], None
    for ligne in chemin.read_text(encoding="utf-8").splitlines():
        if ligne.lstrip().startswith("- source:"):
            cour = {"source": ligne.split(":", 1)[1].strip()}
            entrees.append(cour)
        elif cour is not None and ligne.startswith("  ") and ":" in ligne:
            cle, valeur = ligne.strip().split(":", 1)
            cour[cle.strip()] = valeur.strip()
    return entrees


def fichiers_du_repertoire(racine):
    """Liste triée des fichiers réguliers sous racine (chemins relatifs POSIX)."""
    return sorted(
        str(p.relative_to(racine).as_posix()) for p in racine.rglob("*") if p.is_file()
    )


def lire_ancien_source_md():
    """Ensemble des chemins listés dans le SOURCE.md précédent (pour les suppressions sûres)."""
    if not SOURCE_MD.exists():
        return {}
    connus = {}
    for ligne in SOURCE_MD.read_text(encoding="utf-8").splitlines():
        partie = ligne.strip().lstrip("- ").strip()
        if "  " in partie and partie.count(" ") >= 2:
            morceaux = partie.rsplit("  ", 1)
            if len(morceaux) == 2 and len(morceaux[1].strip()) == 64:
                connus[morceaux[0].strip()] = morceaux[1].strip()
    return connus


def main():
    rapport = {"horodatage": horodatage(), "erreurs": [], "absents": []}
    if not (CMDR / ".git").exists():
        rapport["erreurs"].append(
            f"clone cmdr ABSENT ({CMDR}) — exécuter cmdr-clone.py d'abord"
        )
        print(json.dumps(rapport, ensure_ascii=False, indent=2))
        return 1
    if not porcelain_vide(CMDR):
        rapport["erreurs"].append("clone cmdr SALE (S=1) — superposition refusée (règle 4 du Karnaugh)")
        print(json.dumps(rapport, ensure_ascii=False, indent=2))
        return 1

    # Basculement sur la branche overlay (réutilisée si elle existe).
    if branche_courante(CMDR) != BRANCHE_SUPERPOSITION:
        _, branches = git(["branch", "--list", BRANCHE_SUPERPOSITION], cwd=CMDR)
        git(["checkout"] + ([] if branches.strip() else ["-b"]) + [BRANCHE_SUPERPOSITION], cwd=CMDR)
        rapport["branche"] = BRANCHE_SUPERPOSITION + (" (créée)" if not branches.strip() else " (réutilisée)")
    else:
        rapport["branche"] = BRANCHE_SUPERPOSITION + " (courante)"

    # Sélection → liste plate de fichiers sources (répertoires développés, dédupliqués :
    # un agent listé comme fichier dédié est aussi énuméré par le parcours de son skill).
    cibles = {}  # chemin_relatif -> chemin_absolu_source (déduplication par clé)
    for entree in lire_selection(SELECTION):
        src = KNOWLEDGE / entree["source"]
        if not src.exists():
            rapport["absents"].append(entree["source"])
            continue
        if src.is_dir():
            for rel in fichiers_du_repertoire(src):
                cibles[f"{entree['source']}/{rel}"] = src / rel
        else:
            cibles[entree["source"]] = src
    cibles = [(v, k) for k, v in cibles.items()]

    # Copie unilatérale comparée par SHA-256.
    copies, inchanges = [], []
    for src, rel in cibles:
        dst = DEST / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if dst.exists() and sha256_fichier(dst) == sha256_fichier(src):
            inchanges.append(rel)
        else:
            dst.write_bytes(src.read_bytes())
            copies.append(rel)
    rapport["copies"] = copies
    rapport["inchanges"] = len(inchanges)

    # Suppressions : seulement les fichiers listés dans l'ANCIEN SOURCE.md et sortis de la sélection.
    ancien = lire_ancien_source_md()
    cibles_relatifs = {rel for _, rel in cibles}
    supprimes = []
    for rel in ancien:
        dst = DEST / rel
        if rel not in cibles_relatifs and dst.exists():
            dst.unlink()
            supprimes.append(rel)
    # Nettoyage des dossiers vides (sous ecosystem/ uniquement).
    for d in sorted((p for p in DEST.rglob("*") if p.is_dir()), reverse=True):
        if not any(d.iterdir()):
            d.rmdir()
    rapport["supprimes"] = supprimes

    # SOURCE.md régénéré (dépôt source, SHA KNOWLEDGE, liste fichiers + SHA-256).
    # Idempotence : le contenu STABLE = liste fichiers + hashes (change seulement si
    # les fichiers propagés changent). La ligne de provenance (date + SHA HEAD de
    # KNOWLEDGE) est VOLATILE par nature — l'y inclure créerait une boucle de
    # salissure (tout commit KNOWLEDGE, y compris le re-scellement du manifeste par
    # bootstrap, rendrait SOURCE.md obsolète). Elle n'est donc réécrite QUE lorsque
    # le contenu stable diffère (faille découverte par le contrat d'idempotence §8).
    _, sha_kn = git(["rev-parse", "HEAD"], cwd=KNOWLEDGE)
    corps = [
        "# SOURCE — superposition écosystème (générée, ne pas modifier ici)",
        "",
        f"- Mention : {MENTION}",
        "- Sélection : skills/@GHORG-ecosysteme/selection-tsi.yaml (famille TSI complète — MK2 ET MK3)",
        "",
        "## Fichiers (chemin relatif  SHA-256)",
        "",
    ]
    for src, rel in cibles:
        corps.append(f"- {rel}  {sha256_fichier(src)}")

    def ligne_genere():
        return (
            f"- Généré le : {horodatage()} · source : bigleon2/KNOWLEDGE @ "
            f"{sha_kn.strip()} par scripts/ecosystem/cmdr-overlay-sync.py"
        )

    ancien = SOURCE_MD.read_text(encoding="utf-8") if SOURCE_MD.exists() else ""
    ancien_stable = "\n".join(
        l for l in ancien.splitlines() if not l.startswith("- Généré le :")
    )
    nouveau_stable = "\n".join(corps)
    if ancien_stable == nouveau_stable and ancien:
        rapport["source_md"] = f"{SOURCE_MD} (inchangé — contenu stable identique)"
    else:
        texte = corps[:2] + [ligne_genere()] + corps[2:]
        SOURCE_MD.parent.mkdir(parents=True, exist_ok=True)
        SOURCE_MD.write_text("\n".join(texte) + "\n", encoding="utf-8")
        rapport["source_md"] = str(SOURCE_MD)

    _, sha = git(["rev-parse", "HEAD"], cwd=CMDR)
    maj_etat("D6_superposition_tsi", "terminé", sha.strip())
    print(json.dumps(rapport, ensure_ascii=False, indent=2))
    return 0 if not rapport["erreurs"] else 2


if __name__ == "__main__":
    sys.exit(main())
