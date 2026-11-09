#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.37)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).
(SHARED §0/§1.2) : « mon skill X » = forme installée skills/X/SKILL.md.

Task 82 G6 — P3-P4 : moves R4 byte-identité (re-curation progressive disclosure iphone18,
cible P1 de la liste cibles-recursion — download/analyse-recuration-task82.md §1).
Directive propriétaire trace 1a1be717bb0fbdb1 (item 7 : « effectue ces re-curation $FACON
par ordre de priorité ») — méthode moves-r4-pur arbitrée --compare (P2, harnais v1.2.2).
3 blocs ≥ 1,5 Kio HISTORIQUES / RÉFÉRENCE déplacés vers references/ (en-têtes de provenance :
section, version, date, SHA-256) + pointeurs 1-ligne inline + résumés opérationnels + Lignage
« projection curée » :
  1. changelogs-versions.md — origines v1.0/v1.1 (~0,9 Kio, regroupées avec les changelogs :
     bloc historique cohérent, sous-seuil isolé consigné) + changelogs v1.0→v1.1 + v2.0→v1.0
     + invariants garantis (~5,6 Kio) ;
  2. preset-iphone18-max-calibrage.md — §6.1 intégral (1,75 Kio), résumé opérationnel inline ;
  3. notes-retroactives.md — §11 intégral (1,65 Kio), disciplines a-f résumées inline.
Écart seuil documenté : §6.10 `iphone19` [SPÉCULATIF] (1 375 o < 1,5 Kio) MAINTENU INLINE —
protocole respecté à la lettre (miroir de famille iphone19 documenté, aucun bloc sous-seuil
déplacé). Le cœur opérationnel (§0 rôle, §1-§5, §6.2-§6.10, §7-§10, §12-§13) demeure
intégralement inline. Version INCHANGÉE v1.1.0 (contrats intacts — précédents version-management
Task 79 G2 + iphone19 Task 81 G2).
Idempotent : re-jeu = NO-OP (détection par pointeurs déjà en place). All-or-nothing :
toutes les coupes sont validées AVANT la première écriture. Asserts count==1 par marqueur.
Usage : python3 scripts/task82-recuration-iphone18.py [--json]
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

R = Path("/home/z/my-project/KNOWLEDGE-repo")
SKILL = R / "skills" / "iphone18" / "SKILL.md"
REFS = R / "skills" / "iphone18" / "references"
VERSION = "1.1.0"
DATE = "2026-11-09"
PROTO = "protocole re-curation v1.2.2, méthode moves-r4-pur arbitrée --compare (P2)"

PROVENANCE = (
    "> **Provenance** : skill `iphone18` v{v} · section « {sec} » · déplacé R4 byte-identité "
    "vers `references/` le {d} (Task 82 G6, re-curation progressive disclosure — {p}) · "
    "**SHA-256 du bloc : `{sha}`** · le PM intégral de référence demeure "
    "`skills/@photos/iphone18-photos.md` v1.1 [COURANT — génération iPhone 18 CONFIRMÉE] — "
    "jamais édité (R2).\n\n"
)

# (fichier, titre, section, début inclus, fin exclue, remplacement — {sha16}/{kio} remplis à l'exécution)
BLOCS = [
    {
        "fichier": "changelogs-versions.md",
        "titre": "# Origines + changelogs versionnés v2.0 → v1.1 — iphone18 (bloc archivé R4)",
        "section": "en-tête PROMPT MAÎTRE — origines, tables changelog + invariants",
        "debut": "> **Origine v1.0 (reset de version",
        "fin": "## §0 — RÔLE & MISSION",
        "remplacement": (
            "> **Origines et changelogs versionnés archivés R4** : `references/changelogs-versions.md` "
            "({kio} Kio — SHA-256 {sha16}…) — origine v1.0 (reset : migration depuis `iphone17-photos.md` "
            "v2.0 le 2026-10-09, génération 18 confirmée par Apple le 9/9/2026 — règle §6.10 activée) · "
            "origine v1.1 (extension 1944 — argentiques N&B années 1930-1950, grain préservé, aucune "
            "colorisation inventée — ajouts purs) · changelogs v1.0→v1.1 (ère 40s §6.5, extension §6.6) "
            "et v2.0→v1.0 (R18 ouverture variable ƒ/1.48-ƒ/4.0, QC 12, renommage `iphone18_max` — "
            "contrainte 5.2, correction typographique R17) · invariants garantis par version (aucune "
            "règle R1-R17 modifiée ni affaiblie, G1-G7 et B6 intacts, QC 1-11 inchangés — ajout pur "
            "R18/QC 12, règles absolues 1-13 inchangées, règle 14 généralisée au squelette `iphone19`). "
            "Chargé à la demande (lecture ciblée — jamais par défaut).\n\n---\n\n"
        ),
    },
    {
        "fichier": "preset-iphone18-max-calibrage.md",
        "titre": "# §6.1 Preset `iphone18_max` — calibrage labo (bloc archivé R4)",
        "section": "§6.1 `iphone18_max`",
        "debut": "### 6.1 `iphone18_max`",
        "fin": "### 6.2",
        "remplacement": (
            "### 6.1 `iphone18_max` (défaut — ancrage matériel iPhone 18 Pro Max)\n"
            "**Résumé opérationnel (re-curation v1.1)** : preset par défaut — baseline **triple 48 MP "
            "Fusion** (principal 24 mm à ouverture variable **ƒ/1.48-ƒ/4.0** — R18 ; UGA 13 mm ; télé "
            "4x/8x jusqu'à 200 mm), nouveau capteur principal (sensor-shift OIS 2e génération, 100 % "
            "Focus Pixels), **Photographic Styles 3** (texture et grain), Photonic Engine, puce **A20 "
            "Pro** — Dual Neural Engine 32 cœurs ; rendu **calibré labo** (DXOMARK 172 pts, nuit 150 — "
            "record) : netteté max sur zones utiles (visages prioritaires), piqué accru, dynamique "
            "étendue sans HDR visible, teintes chair fidèles, mode nuit propre (ouverture auto ƒ/1.48), "
            "texture naturelle jamais plastique (G4), groupes nets de l'avant à l'arrière (ƒ/4.0 — R18) ; "
            "limites honnêtes (télé longue portée derrière certains concurrents, bokeh très basse "
            "lumière) ; périmètre : images statiques. **Calibrage labo réel, génération CONFIRMÉE** "
            "(aucune extrapolation — à la différence du squelette §6.10).\n"
            "> **Intégral archivé R4** : `references/preset-iphone18-max-calibrage.md` ({kio} Kio — "
            "SHA-256 {sha16}…) — baseline de référence v1.0 + rendu simulé + limites honnêtes + "
            "périmètre. Chargé à la demande (lecture ciblée — jamais par défaut).\n\n"
        ),
    },
    {
        "fichier": "notes-retroactives.md",
        "titre": "# §11 Auto-audit + notes rétroactives v2.0/v1.0/v1.1 — iphone18 (bloc archivé R4)",
        "section": "§11 AUTO-AUDIT DU DOCUMENT — disciplines + notes rétroactives",
        "debut": "## §11 — AUTO-AUDIT DU DOCUMENT",
        "fin": "## §12",
        "remplacement": (
            "## §11 — AUTO-AUDIT DU DOCUMENT (après chaque modification)\n\n"
            "**Disciplines a-f (résumé opérationnel)** : références croisées §/R/G cohérentes · "
            "numérotation continue (sections, règles, garde-fous, QC) · champs YAML vérifiés · toute "
            "nouvelle règle répercutée en §3 (YAML) + §5 (QC) + §8 (rapport) · version incrémentée · "
            "notes rétroactives si des QC passés seraient réévalués différemment.\n"
            "> **Disciplines intégrales + notes rétroactives archivées R4** : `references/notes-retroactives.md` "
            "({kio} Kio — SHA-256 {sha16}…) — note v2.0 (intégrations génération 17 : ajouts purs, QC 11 "
            "+ règle 14 nouveaux) · note v1.0 (R18, re-ancrage §6.1, renommages contrainte 5.2, correction "
            "typographique R17, squelette `iphone19` — QC 12 nouveau) · note v1.1 (extension 1944 : "
            "ajout pur) — aucune règle R1-R18, aucun garde-fou G1-G7, aucun critère QC 1-12 modifié ni "
            "affaibli, aucun QC antérieur requalifié. Chargé à la demande (lecture ciblée — jamais par "
            "défaut).\n\n---\n\n"
        ),
    },
]

LIGNAGE_ANCIEN = (
    "Le corps ci-dessous (« ## PROMPT MAÎTRE » → §13) est repris **VERBATIM** de cette source ;"
)
LIGNAGE_NOUVEAU = (
    "Depuis la re-curation v1.1 (Task 82 G6, 2026-11-09 — protocole P0-P7 v1.2.2, méthode "
    "moves-r4-pur arbitrée --compare), le corps ci-dessous (« ## PROMPT MAÎTRE » → §13) est la "
    "**projection curée** (progressive disclosure) de cette source : les blocs historiques et de "
    "référence (origines + changelogs versionnés, calibrage §6.1, auto-audit + notes rétroactives "
    "§11) vivent en `references/` en copies R4 byte-identité pointées inline ; le cœur opérationnel "
    "(§0 rôle, §1-§5, §6.2-§6.10, §7-§10, §12-§13) demeure intégralement inline ; le PM source "
    "demeure l'intégral de référence ;"
)


def sha256(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def main() -> int:
    texte = SKILL.read_text(encoding="utf-8")
    ancienne_taille = len(texte.encode("utf-8"))

    # Idempotence : fichiers references présents + pointeurs cités + Lignage curée → NO-OP
    deja = (all((REFS / b["fichier"]).is_file() and f"`references/{b['fichier']}`" in texte
                for b in BLOCS) and LIGNAGE_NOUVEAU[:60] in texte)
    if deja:
        print(json.dumps({"verdict": "NO-OP", "octets": ancienne_taille,
                          "fichiers": [b["fichier"] for b in BLOCS]},
                         ensure_ascii=False))
        return 0

    # Phase 1 — validation de toutes les coupes (all-or-nothing, count==1)
    coupes = []
    for b in BLOCS:
        assert texte.count(b["debut"]) == 1, f"marqueur début non unique : {b['debut'][:50]}"
        assert texte.count(b["fin"]) == 1, f"marqueur fin non unique : {b['fin'][:50]}"
        i = texte.index(b["debut"])
        j = texte.index(b["fin"])
        assert j > i, f"fin avant début : {b['fichier']}"
        bloc = texte[i:j]
        assert len(bloc.encode("utf-8")) >= 1536, f"bloc sous 1,5 Kio : {b['fichier']}"
        coupes.append((b, i, j, bloc))
    assert texte.count(LIGNAGE_ANCIEN) == 1, "phrase Lignage VERBATIM non unique"

    # Phase 2 — écritures (répertoire references + fichiers avec provenance)
    REFS.mkdir(exist_ok=True)
    rapport = {"blocs": [], "octets_avant": ancienne_taille}
    for b, _i, _j, bloc in coupes:
        sha = sha256(bloc)
        contenu = (b["titre"] + "\n\n" +
                   PROVENANCE.format(v=VERSION, sec=b["section"], d=DATE, p=PROTO, sha=sha) +
                   bloc)
        (REFS / b["fichier"]).write_text(contenu, encoding="utf-8")
        rapport["blocs"].append({"fichier": b["fichier"], "section": b["section"],
                                 "octets": len(bloc.encode("utf-8")), "sha256": sha})

    # Phase 3 — remplacements inline (pointeurs 1-ligne + résumés), du bas vers le haut
    for b, i, j, bloc in sorted(coupes, key=lambda c: -c[1]):
        sha = sha256(bloc)
        taille_kio = round(len(bloc.encode("utf-8")) / 1024, 1)
        remplacement = b["remplacement"].format(
            sha16=sha[:16], kio=f"{taille_kio:.1f}".replace(".", ","))
        texte = texte[:i] + remplacement + texte[j:]

    # Phase 4 — Lignage « projection curée »
    texte = texte.replace(LIGNAGE_ANCIEN, LIGNAGE_NOUVEAU)

    SKILL.write_text(texte, encoding="utf-8")
    nouvelle_taille = len(texte.encode("utf-8"))
    rapport.update({
        "verdict": "MOVES-R4-PUR APPLIQUÉ",
        "octets_apres": nouvelle_taille,
        "kio_avant": round(ancienne_taille / 1024, 1),
        "kio_apres": round(nouvelle_taille / 1024, 1),
        "gain_pct": round((1 - nouvelle_taille / ancienne_taille) * 100, 1),
    })
    print(json.dumps(rapport, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
