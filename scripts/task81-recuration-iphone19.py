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

Task 81 G2 — P3-P4 : moves R4 byte-identité (re-curation progressive disclosure iphone19).
Directive propriétaire trace 1a1bcf4fecbf5f29 (item 2 : « effectue $FACON la re-curation
divulgation progressive d'iPhone19 (P1→P7) ») — méthode moves-r4-pur arbitrée --compare
(P2). 6 blocs ≥ 1,5 Kio HISTORIQUES / RÉFÉRENCE / DORMANTS déplacés vers references/
(en-têtes de provenance : section, version, date, SHA-256) + pointeurs 1-ligne inline +
résumé opérationnel §6.1 + Lignage « projection curée ». Le cœur opérationnel
(§0 règles absolues 1-15, §1-§5, §6.2-§6.9, §7-§10, §13) demeure intégralement inline.
Idempotent : re-jeu = NO-OP (détection par pointeurs déjà en place). All-or-nothing :
toutes les coupes sont validées AVANT la première écriture. Asserts count==1 par marqueur.
Usage : python3 scripts/task81-recuration-iphone19.py [--json]
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

R = Path("/home/z/my-project/KNOWLEDGE-repo")
SKILL = R / "skills" / "iphone19" / "SKILL.md"
REFS = R / "skills" / "iphone19" / "references"
VERSION = "0.12.0"
DATE = "2026-11-09"
PROTO = "protocole re-curation v1.2.0, méthode moves-r4-pur arbitrée --compare (P2)"

PROVENANCE = (
    "> **Provenance** : skill `iphone19` v{v} · section « {sec} » · déplacé R4 byte-identité "
    "vers `references/` le {d} (Task 81 G2, re-curation progressive disclosure — {p}) · "
    "**SHA-256 du bloc : `{sha}`** · le PM intégral de référence demeure "
    "`skills/@photos/iphone19-photos.md` v{v} [ANTICIPÉE] — jamais édité (R2).\n\n"
)

# (fichier, titre, section, début inclus, fin exclue, remplacement — {sha16}/{kio} remplis à l'exécution)
BLOCS = [
    {
        "fichier": "origines-versions.md",
        "titre": "# Origines versionnées v0.9.0 → v0.12.0 — iphone19 (bloc archivé R4)",
        "section": "en-tête PROMPT MAÎTRE — blocs origine",
        "debut": "> **Origine v0.9.0 (migration ANTICIPÉE",
        "fin": "### Changelog `iphone19-photos.md` v0.11.0",
        "remplacement": (
            "> **Origines versionnées archivées R4** : `references/origines-versions.md` "
            "({kio} Kio — SHA-256 {sha16}…) — blocs origine v0.9.0 (migration ANTICIPÉE depuis la "
            "génération 18, Task 47) · v0.10.0 (émulation pixel binning R19 — [RUMEUR] DCS via "
            "Frandroid 27/03/2026) · v0.11.0 (extension 1944 — chemin argentique N&B années "
            "1930-1950) · v0.12.0 (règle absolue 15 fidélité — directive propriétaire 2026-11-09). "
            "Chargé à la demande (lecture ciblée — jamais par défaut).\n\n"
        ),
    },
    {
        "fichier": "changelogs-versions.md",
        "titre": "# Changelogs versionnés v0.11.0 → v0.12.0 et antérieurs — iphone19 (bloc archivé R4)",
        "section": "en-tête PROMPT MAÎTRE — tables changelog + invariants",
        "debut": "### Changelog `iphone19-photos.md` v0.11.0",
        "fin": "---\n\n## §0 — RÔLE",
        "remplacement": (
            "> **Changelogs versionnés archivés R4** : `references/changelogs-versions.md` "
            "({kio} Kio — SHA-256 {sha16}…) — v0.11.0→v0.12.0 (règle fidélité : règle absolue 15 + "
            "QC 14, ajouts purs) · v0.10.0→v0.11.0 (extension 1944) · v0.9.0→v0.10.0 (pixel binning "
            "R19 + QC 13) · v1.0→v0.9.0 (migration ANTICIPÉE), avec invariants garantis par version. "
            "Chargé à la demande (lecture ciblée — jamais par défaut).\n\n"
        ),
    },
    {
        "fichier": "preset-iphone19-max-calibrage.md",
        "titre": "# §6.1 Preset `iphone19_max` — calibrage ANTICIPÉ (bloc archivé R4)",
        "section": "§6.1 `iphone19_max`",
        "debut": "### 6.1 `iphone19_max`",
        "fin": "### 6.2",
        "remplacement": (
            "### 6.1 `iphone19_max` (défaut — ancrage matériel ANTICIPÉ iPhone 19 Pro Max [2027])\n"
            "**Résumé opérationnel (re-curation v0.12.0)** : preset par défaut — extrapolation prudente "
            "de la baseline confirmée 18 + delta rumeuré génération 19 (A21 Pro [RUMEUR] · capteur 200 MP "
            "Sony Lytia 901 à pixel binning 16-en-1 — R19 [RUMEUR — DCS via Frandroid 27/03/2026] · "
            "Photonic Engine NG+ [EXTRAPOLATION]) : netteté max sur zones utiles (visages prioritaires), "
            "piqué accru, dynamique étendue sans HDR visible, colorimétrie naturelle et teintes chair "
            "fidèles, mode nuit propre (ouverture auto ƒ/1.48 — R18), caractère « pixels fusionnés » du "
            "binning 16-en-1 (R19 : SNR accru, micro-détail préservé, recadrage élargi), texture naturelle "
            "jamais plastique (G4), groupes nets de l'avant à l'arrière (ƒ/4.0 — R18). **Calibration "
            "extrapolée, JAMAIS mesurée en labo** — statut ANTICIPÉ, re-ancrage au bump v1.0.0 (§6.10, "
            "règle 14) ; périmètre : images statiques.\n"
            "> **Intégral archivé R4** : `references/preset-iphone19-max-calibrage.md` ({kio} Kio — "
            "SHA-256 {sha16}…) — baseline de référence (structure photo génération 18 + delta rumeuré) · "
            "rendu simulé complet · limites honnêtes renforcées. Chargé à la demande (lecture ciblée — "
            "jamais par défaut).\n\n"
        ),
    },
    {
        "fichier": "squelette-iphone20-speculatif.md",
        "titre": "# §6.10 Squelette `iphone20` [SPÉCULATIF] — section inactive (bloc archivé R4)",
        "section": "§6.10 `iphone20` [SPÉCULATIF]",
        "debut": "### 6.10 `iphone20`",
        "fin": "## §7",
        "remplacement": (
            "### 6.10 `iphone20` — **[SPÉCULATIF] — SECTION INACTIVE**\n"
            "> Squelette conditionnel vide (règle 14) — génération 20 non confirmée : ne déclenche jamais "
            "de traitement, ne fournit jamais de valeur par défaut, n'est jamais appliquée aux images. "
            "**Intégral archivé R4** : `references/squelette-iphone20-speculatif.md` ({kio} Kio — SHA-256 "
            "{sha16}…) — statut de la génération 19 (ANTICIPÉE, consommée sans règle d'activation) · règle "
            "d'activation de la migration de CONFIRMATION (bump v1.0.0 : re-ancrage §0/§6.1/R19, règles "
            "R20+ si confirmées, archivage PM génération 18) · squelette `iphone20` INACTIF. Chargé à la "
            "demande (lecture ciblée — jamais par défaut).\n\n---\n\n"
        ),
    },
    {
        "fichier": "notes-retroactives.md",
        "titre": "# §11 Notes rétroactives v0.12.0 et antérieures — iphone19 (bloc archivé R4)",
        "section": "§11 AUTO-AUDIT — notes rétroactives",
        "debut": "**Note rétroactive v0.12.0 :**",
        "fin": "## §12",
        "remplacement": (
            "> **Notes rétroactives archivées R4** : `references/notes-retroactives.md` ({kio} Kio — "
            "SHA-256 {sha16}…) — invariants garantis par version (v0.12.0 règle fidélité · v2.0 · v1.0 · "
            "v0.9.0 · v0.10.0 · v0.11.0 : ajouts purs, aucune règle absolue, aucune règle R1-R19, aucun "
            "garde-fou G1-G7, aucun critère QC modifié ni affaibli, aucun QC antérieur requalifié). "
            "Chargé à la demande (lecture ciblée — jamais par défaut).\n\n---\n\n"
        ),
    },
    {
        "fichier": "livrables-projet.md",
        "titre": "# §12 Livrables du projet — iphone19 (bloc archivé R4)",
        "section": "§12 LIVRABLES DU PROJET",
        "debut": "## §12 — LIVRABLES DU PROJET",
        "fin": "## §13",
        "remplacement": (
            "## §12 — LIVRABLES DU PROJET\n\n"
            "> **Intégral archivé R4** : `references/livrables-projet.md` ({kio} Kio — SHA-256 {sha16}…) — "
            "PMs générationnels (`iphone19-photos.md` v0.12.0 présent · `iphone18-photos.md` v1.1 "
            "génération CONFIRMÉE · `iphone17-photos.md` v2.1 archivée · `iphone-photos-migration.md` "
            "v1.0) · `crop_utils.py` (post-recadrage P8b) · livrables historiques CLUB (PA-CLUB-001→007, "
            "scripts PIL consolidés). Les sorties PA-<CAS>-<seq> demeurent déclarées au plan (§3, "
            "règle 13). Chargé à la demande (lecture ciblée — jamais par défaut).\n\n---\n\n"
        ),
    },
]

LIGNAGE_ANCIEN = (
    "Le corps ci-dessous (« ## PROMPT MAÎTRE » → §13) est repris **VERBATIM** de cette source ;"
)
LIGNAGE_NOUVEAU = (
    "Depuis la re-curation v0.12.0 (Task 81 G2, 2026-11-09 — protocole P0-P7, méthode moves-r4-pur "
    "arbitrée --compare), le corps ci-dessous (« ## PROMPT MAÎTRE » → §13) est la **projection curée** "
    "(progressive disclosure) de cette source : les blocs historiques et de référence (origines, "
    "changelogs, calibrage §6.1, squelette §6.10 [SPÉCULATIF], notes rétroactives §11, livrables §12) "
    "vivent en `references/` en copies R4 byte-identité pointées inline ; le cœur opérationnel "
    "(§0 règles absolues 1-15, §1-§5, §6.2-§6.9, §7-§10, §13) demeure intégralement inline ; le PM "
    "source demeure l'intégral de référence ;"
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
        taille_kio = round(len(bloc.encode("utf-8")) / 1024, 1)
        contenu = (b["titre"] + "\n\n" +
                   PROVENANCE.format(v=VERSION, sec=b["section"], d=DATE, p=PROTO, sha=sha) +
                   bloc)
        (REFS / b["fichier"]).write_text(contenu, encoding="utf-8")
        rapport["blocs"].append({"fichier": b["fichier"], "section": b["section"],
                                 "octets": len(bloc.encode("utf-8")), "sha256": sha})

    # Phase 3 — remplacements inline (pointeurs 1-ligne + résumé §6.1), du bas vers le haut
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
