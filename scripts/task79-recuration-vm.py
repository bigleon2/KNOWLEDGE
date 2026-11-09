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
Task 79 G2 — Re-curation version-management (P3-P4, méthode moves-r4-pur
arbitrée par protocole-test.py --compare : la plus optimisée R4-compliante,
projection 21,9 Kio).

7 blocs ≥ 1,6 Kio (cartographie re-mesurée SG2.1) déplacés R4 byte-identité
vers skills/version-management/references/ avec en-têtes de provenance
(section, version, date, SHA-256 du bloc) ; pointeurs 1-ligne inline.

Contrats intacts (protocole-test --post) : frontmatter description, §0
normalisé, read_when, evals. Idempotence : NO-OP si déjà appliqué.
Garde : all-or-nothing — tout en mémoire, ABANDON rc=2 sans écriture si un
ancrage échoue.
"""
import hashlib
import re
import sys
from pathlib import Path

R = Path("/home/z/my-project/KNOWLEDGE-repo")
SK = R / "skills/version-management/SKILL.md"
REF = R / "skills/version-management/references"
DATE = "2026-11-08"

# (ancre d'en-tête exacte, nom de fichier references, résumé honnête 1-ligne)
BLOCS = [
    ("### 1.2 Contrôle obligatoire des chemins (règle critique)",
     "controle-chemins.md",
     "tous les fichiers sous `mes-projets/{nom-projet}/` — prévention d'abord, "
     "contrôle avant commit, répertoire projet auto-contenu obligatoire"),
    ("### 1.3 Règles de structure des fichiers",
     "regles-structure-fichiers.md",
     "répertoire projet auto-contenu — mono-fichier vs multi-fichiers selon le "
     "type de projet (landing, H5, vitrine, application)"),
    ("### 3.1 Points d'entrée d'édition et détermination de la version",
     "points-entree-edition.md",
     "table des points d'entrée d'édition (commentaire, carte, restauration) et "
     "détermination de la version de base du projet"),
    ("### 3.4 Sortie dans le flux de conversation (send_file)",
     "sortie-flux-send-file.md",
     "règle send_file : chaque version générée impose un appel — paramètres par "
     "défaut et variantes mono/multi-fichiers (§3.4.1 et suivantes)"),
    ("## 5. Structure de meta.json",
     "structure-meta-json.md",
     "exemplaire unique par projet, exclu du dépôt git (.gitignore) — schéma "
     "complet des champs de l'état global du projet"),
    ("## 6. Aide-mémoire des opérations",
     "aide-memoire-operations.md",
     "table « Action utilisateur → Opération exécutée » pour tous les cas "
     "(création, édition, restauration, multi-projets)"),
    ("## 8. Résorption structurelle — neutralisation résiliente (Task 69)",
     "resorption-structurelle.md",
     "diagnostic consolidé Task 69 (32 incidents : disparition entre les tours "
     "par processus externe) et mécanisme de neutralisation résiliente"),
]

HDR = re.compile(r"^#{2,3} ", re.M)


def bloc_suivant(texte, debut):
    """Fin du bloc : prochain en-tête ## ou ### après debut."""
    m = HDR.search(texte, debut + 1)
    return m.start() if m else len(texte)


def main():
    t = SK.read_text(encoding="utf-8")
    if "references/regles-structure-fichiers.md" in t:
        print("[NO-OP] re-curation déjà appliquée (pointeur §1.3 présent)")
        return 0
    if not all(a in t for a, _, _ in BLOCS):
        manq = [a for a, _, _ in BLOCS if a not in t]
        print("ABANDON : ancres introuvables : %s" % manq)
        return 2
    if t.count("### 1.2 Contrôle obligatoire") != 1 or t.count("## 5. Structure de meta.json") != 1:
        print("ABANDON : ancre non unique")
        return 2

    REF.mkdir(exist_ok=True)
    nouveau = t
    total_deplace = 0
    for ancre, fname, resume in BLOCS:
        debut = nouveau.find(ancre)
        fin = bloc_suivant(nouveau, debut)
        bloc = nouveau[debut:fin].rstrip("\n") + "\n"
        sha = hashlib.sha256(bloc.encode("utf-8")).hexdigest()
        kio = len(bloc.encode("utf-8")) / 1024
        # fichier references/ : en-tête de provenance + bloc byte-identité
        titre = ancre.lstrip("# ").strip()
        ref_texte = (
            "# %s — version-management (bloc archivé R4)\n\n"
            "> **Provenance** : skill `version-management` v1.3.0 · section « %s » · "
            "déplacé R4 byte-identité vers `references/` le %s (Task 79 G2, re-curation — "
            "protocole re-curation v1.0.0, méthode moves-r4-pur arbitrée --compare) · "
            "**SHA-256 du bloc : %s**\n\n%s"
            % (titre, titre, DATE, sha, bloc)
        )
        (REF / fname).write_text(ref_texte, encoding="utf-8")
        # pointeur 1-ligne inline (en-tête conservé + pointeur)
        pointeur = (
            "%s\n\n> **Intégral archivé R4** : `references/%s` (%s Kio — SHA-256 %s…) — %s. "
            "Chargé à la demande (lecture ciblée E5-POIDS — jamais par défaut).\n\n"
            % (ancre, fname, ("%.1f" % kio).replace(".", ","), sha[:16], resume)
        )
        nouveau = nouveau[:debut] + pointeur + nouveau[fin:]
        total_deplace += len(bloc.encode("utf-8"))
        print("  §%-28s → references/%-32s %6d o (SHA %s…)"
              % (titre[:28], fname, len(bloc.encode("utf-8")), sha[:12]))

    avant = len(t.encode("utf-8"))
    SK.write_text(nouveau, encoding="utf-8")
    apres = len(nouveau.encode("utf-8"))
    print("SKILL.md : %d → %d o (%s Kio, −%.1f %% · déplacé %d o ≈ %.1f Kio)"
          % (avant, apres, ("%.1f" % (apres / 1024)).replace(".", ","),
             100 * (1 - apres / avant), total_deplace, total_deplace / 1024))
    return 0


if __name__ == "__main__":
    sys.exit(main())
