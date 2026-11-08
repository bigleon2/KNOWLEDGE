#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.36)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).
"""

# -*- coding: utf-8 -*-
"""
Task 78/79 G1 — Amendement chirurgical gen-plan v3.40.0 → v3.41.0
RÈGLE DE SONDAGE BORNÉ — directive propriétaire trace 1a1bbf9f403a2865
(« génère le plan du Task "règle de sondage borné" » ; origine : avertissement
SG2.2 Task 77 « Sortie trop volumineuse (en-tête SHARED très long) »).

Éditions chirurgicales assert count==1 (discipline refactoring-engineering) :
  1. skills/gen-plan/SKILL.md — version, §1.2bis (NOUVELLE rangée « Sondage
     borné » après la rangée Graph Diamond), §1.4 #4 (extension sondage),
     §5.6 (entrée courante v3.41.0 ; migration de l'entrée v3.40.0 vers
     journal-versions.md, R4 byte-identité) ; compensation byte conditionnelle.
  2. references/protocoles-detailles.md — append « Extension v3.41.0 »
     (intégral du protocole — 4 règles + exceptions + volumétrie mesurée).
  3. references/journal-versions.md — insertion de l'entrée v3.40.0 (migration)
     après la note de mécanique, avant l'entrée v3.39.0.

Garde-fous : budget SKILL.md ≤ 30719 octets UTF-8 ; idempotence (re-jeu = no-op,
rc=0) ; ABANDON rc=2 sans AUCUNE écriture si un ancrage ou le budget échoue.
"""
import re
import sys
from pathlib import Path

RACINE = Path("/home/z/my-project/KNOWLEDGE-repo")
SKILL = RACINE / "skills/gen-plan/SKILL.md"
PROTO = RACINE / "skills/gen-plan/references/protocoles-detailles.md"
JOURNAL = RACINE / "skills/gen-plan/references/journal-versions.md"
BUDGET = 30719  # < 30 Kio strict (contrat re-curation R1)

# ----------------------------------------------------------------- textes

ROW_GD = ("| **Graph Diamond** | **E9-E14** | Parallélisation PAR DÉFAUT des tâches ET commandes "
          "indépendantes (série = exception justifiée — #4 v3.24.0/v3.32.0/v3.40.0 émission : "
          "fan-out bloc + `&`+`wait`) — tracé worklog | `references/graph-diamond-pattern.md` |")

ROW_SONDAGE = ("| **Sondage borné** | **E9-E14** | Inspection transverse sur l'arbre skills/ TOUJOURS "
               "bornée : mode fichiers (-l) d'abord, greps multi-fichiers tronqués + limite de "
               "résultats ; §0/contrats jamais affichés en entier | `references/protocoles-detailles.md` |")

PHILO4_OLD = ("4. **Parallélisation par défaut des tâches ET des commandes sur preuve d'indépendance** "
              "(v3.24.0/v3.32.0 + **émission v3.40.0**) — vagues indépendantes en PARALLÈLE : Graph "
              "Diamond (E9-E14), série = exception tracée ; émission : fan-out multi-appels + concurrence "
              "`&`+`wait` ; dégradation 429 — intégral : `references/protocoles-detailles.md` (#4).")
PHILO4_NEW = ("4. **Parallélisation par défaut des tâches ET des commandes sur preuve d'indépendance** "
              "(v3.24.0/v3.32.0 + émission v3.40.0 + **sondage borné v3.41.0**) — vagues indépendantes en "
              "PARALLÈLE : Graph Diamond (E9-E14), série = exception tracée ; émission : fan-out "
              "multi-appels + concurrence `&`+`wait` ; sondage : inspection bornée (§1.2bis) ; dégradation "
              "429 — intégral : `references/protocoles-detailles.md` (#4).")

ENTREE_V3410 = (
    "- **v3.41.0 (2026-11-08, web-ecef7f80 — Task 78/79 G1, directive 1a1bbf9f403a2865 « règle de "
    "sondage borné »)** : SONDAGE BORNÉ — extension de la lecture ciblée (E5-POIDS) aux inspections "
    "transverses : jamais de pattern générique sur l'arbre sans -l, greps multi-fichiers tronqués + "
    "limite de résultats, §0/contrats jamais en entier (exceptions : golden-master et contrats "
    "PRE/POST). Motivation et mesures (SG2.2 Task 77 « Sortie trop volumineuse » — BRUT 12 207 o vs "
    "BORNÉ 3 763 o, gain ×3,2) : intégral protocoles-detailles.md. Inline : §1.2bis rangée + §1.4 #4. "
    "MINOR, description/§A inchangés (non-régression triggers). Cascade KO-L004 : PM v3.41.0, SHARED "
    "INCHANGÉ (règle gen-plan-scopée) (Task 79 G1)."
)

# Compensation byte conditionnelle (résumé compacté — intégral intact dans references/)
COMP1_OLD = ("un skill CRITIQUE (≥ 60 Kio) ou LOURD (≥ 30 Kio) déclenche la voie lecture ciblée : "
             "§0 Contexte Système + sommaire d'abord, sections dédiées ensuite, `references/` chargées "
             "à la demande — JAMAIS de lecture intégrale par défaut")
COMP1_NEW = ("un skill CRITIQUE (≥ 60 Kio) ou LOURD (≥ 30 Kio) déclenche la lecture ciblée : §0 + "
             "sommaire d'abord, sections dédiées ensuite, `references/` à la demande — JAMAIS de "
             "lecture intégrale par défaut")

PROTOCOLE_EXT = (
    "\n\n---\n\n"
    "### Extension v3.41.0 — sondage borné (inspection transverse — origine Task 77 SG2.2 / Task 78, directive trace 1a1bbf9f403a2865)\n\n"
    "**Origine mesurée** : durant SG2.2 du Task 77 (cascade SHARED v1.7.35), un grep transverse a "
    "déclenché l'avertissement « Sortie trop volumineuse (en-tête SHARED très long) » — le réflexe "
    "borné (reprise en greps ciblés, lignes tronquées) avait été appliqué au vol mais n'était codifié "
    "nulle part. Mesures (2026-11-08, session web-ecef7f80) : grep « Contexte Système » sur "
    "skills/*/SKILL.md → **BRUT : 126 lignes / 12 207 octets émis** (ligne la plus longue 1 458 o) vs "
    "**BORNÉ (-l) : 119 lignes / 3 763 octets** — gain ×3,2 ; le §0 SHARED est dupliqué dans 119 "
    "SKILL.md (moyenne 2,0 Kio, max 15,1 Kio), et chaque match de grep imprime la ligne ENTIÈRE. La "
    "discipline « lecture ciblée » existante (hook E5-POIDS v3.38.0) ne couvrait que les LECTURES de "
    "skills LOURD/CRITIQUE — la présente extension la généralise aux COMMANDES D'INSPECTION "
    "TRANSVERSES (greps, lectures d'arbre) pendant l'exécution des plans (E9-E14).\n\n"
    "**RÈGLES (toute inspection transverse sur l'arbre skills/ — et par extension tout arbre de "
    "fichiers technique) :**\n\n"
    "1. **Jamais de pattern générique sans mode fichiers** : un pattern large (« SHARED », « Contexte "
    "Système », « v3. »…) sur l'arbre complet est d'abord lancé en mode `-l` / `--files-with-matches` "
    "(liste de fichiers uniquement) ; le grep de contenu ne porte ensuite QUE sur les fichiers retenus.\n"
    "2. **Greps multi-fichiers bornés** : toute commande de grep de contenu multi-fichiers porte une "
    "troncature de ligne (`--max-columns` ≈ 200) ET une limite de résultats (head_limit) — jamais de "
    "sortie intégrale non bornée.\n"
    "3. **§0 et contrats jamais affichés en entier** : les blocs §0 (en-têtes SHARED), les lignes de "
    "changelog et les contrats (evals, read_when) se lisent par plages de lignes ciblées "
    "(offset/limit), jamais par cat/grep intégral — ce sont les lignes les plus longues du dépôt "
    "(jusqu'à 1 458 o mesurés).\n"
    "4. **Exceptions (lectures intégrales légitimes)** : captures golden-master et lecture de contrats "
    "en PRE/POST d'une re-curation ou d'un amendement — UN fichier à la fois, jamais en transverse.\n\n"
    "**Anti-régression** : le sondage borné ne réduit JAMAIS la preuve mécanique (les vérifications "
    "comptent les MATCHES, pas les octets affichés — `-l` + `rg -c` suffisent aux comptages) ; il ne "
    "retarde pas non plus une lecture exigée par un verdict (l'exception 4 prime). Sa non-application "
    "reproduit le symptôme SG2.2 : plafond de sortie atteint, diagnostic perdu puis repris manuellement.\n"
)

NOTE_MIGRATION = ("> **Mécanique de migration (v3.39.0)** : le SKILL.md §5.6 ne conserve que l'entrée "
                  "COURANTE ; à chaque montée de version suivante, l'entrée courante migre ici "
                  "(R4 byte-identité) et la nouvelle prend sa place inline.")


def sub(text, old, new, label, n=1):
    c = text.count(old)
    if c != n:
        print("ABANDON : ancrage [%s] trouvé %d fois (attendu %d) : %r" % (label, c, n, old[:70]))
        sys.exit(2)
    return text.replace(old, new)


def main():
    skill = SKILL.read_text(encoding="utf-8")

    if "version: 3.41.0" in skill:
        print("[NO-OP] SKILL.md déjà en v3.41.0 (idempotence — re-jeu sans effet)")
        proto = PROTO.read_text(encoding="utf-8")
        print("  protocoles-detailles.md : %s" % ("Extension v3.41.0 présente" if "Extension v3.41.0" in proto else "ABSENTE (incohérent)"))
        return 0

    # --- 1. capture de l'entrée v3.40.0 (migration R4) AVANT remplacement
    m = re.findall(r"^- \*\*v3\.40\.0 \([^\n]*$", skill, re.M)
    if len(m) != 1:
        print("ABANDON : entrée §5.6 v3.40.0 trouvée %d fois (attendu 1)" % len(m))
        return 2
    entree_v3400 = m[0]

    # --- 2. SKILL.md : substitutions en mémoire
    t = skill
    t = sub(t, "version: 3.40.0", "version: 3.41.0", "version frontmatter")
    t = sub(t, ROW_GD, ROW_GD + "\n" + ROW_SONDAGE, "§1.2bis rangée Sondage borné (après Graph Diamond)")
    t = sub(t, PHILO4_OLD, PHILO4_NEW, "§1.4 philosophie #4 + sondage")
    t = sub(t, entree_v3400, ENTREE_V3410, "§5.6 entrée courante v3.41.0")

    taille_avant = len(skill.encode("utf-8"))
    taille_apres = len(t.encode("utf-8"))
    print("SKILL.md : %d → %d octets (delta %+d, budget %d)" % (
        taille_avant, taille_apres, taille_apres - taille_avant, BUDGET))

    # --- 2bis. compensation byte conditionnelle
    if taille_apres > BUDGET:
        t = sub(t, COMP1_OLD, COMP1_NEW, "§1.2bis E5-POIDS compensation")
        taille_apres = len(t.encode("utf-8"))
        print("Compensation appliquée : %d octets (delta %+d, budget %d)" % (
            taille_apres, taille_apres - taille_avant, BUDGET))
    if taille_apres > BUDGET:
        print("ABANDON : budget < 30 Kio dépassé de %d octets — compensations supplémentaires requises"
              % (taille_apres - BUDGET))
        return 2

    # --- 3. fichiers references (en mémoire, écritures seulement si tout passe)
    proto = PROTO.read_text(encoding="utf-8")
    if "Extension v3.41.0" in proto:
        print("ABANDON : protocoles-detailles.md contient déjà l'extension v3.41.0")
        return 2
    proto_new = proto.rstrip("\n") + PROTOCOLE_EXT

    journal = JOURNAL.read_text(encoding="utf-8")
    if entree_v3400.split("(")[0] + "(2026-11-08" in journal:
        print("ABANDON : journal-versions.md contient déjà l'entrée v3.40.0 migrée")
        return 2
    journal_new = sub(journal, NOTE_MIGRATION, NOTE_MIGRATION + "\n\n" + entree_v3400,
                      "journal-versions insertion v3.40.0")

    # --- 4. écritures (tout est validé — aucune écriture partielle possible)
    SKILL.write_text(t, encoding="utf-8")
    PROTO.write_text(proto_new, encoding="utf-8")
    JOURNAL.write_text(journal_new, encoding="utf-8")

    print("Écrit : SKILL.md v3.41.0 (%d o) · protocoles-detailles.md (%d → %d o) · "
          "journal-versions.md (+ entrée v3.40.0 migrée %d o, %d → %d o)"
          % (taille_apres, len(proto.encode("utf-8")), len(proto_new.encode("utf-8")),
             len(entree_v3400.encode("utf-8")),
             len(journal.encode("utf-8")), len(journal_new.encode("utf-8"))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
