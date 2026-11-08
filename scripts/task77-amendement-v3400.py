#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Task 77 G2 / T2.2.1 — Amendement chirurgical gen-plan v3.39.0 → v3.40.0
PROTOCOLE D'ÉMISSION PARALLÈLE — directive propriétaire trace 1a1ba66f3aff26e9
(« vérifie que mon écosystème te permet de lancer 4 commandes en parallèle …
fais en sorte qu'il te permette de le faire à partir de maintenant »).

Éditions chirurgicales assert count==1 (discipline refactoring-engineering) :
  1. skills/gen-plan/SKILL.md — version, §1.2bis (rangée Graph Diamond étendue),
     §1.4 #4 (extension émission), §1.4 #7 + §1.2bis point (5) + §4 (compensations
     byte — budget < 30 Kio maintenu), §5.6 (entrée courante v3.40.0 ; migration
     de l'entrée v3.39.0 vers journal-versions.md, R4 byte-identité).
  2. references/protocoles-detailles.md — append « Extension v3.40.0 » (intégral
     du protocole, APRÈS le bloc FIN-BLOC-DEPLACÉ:philo4 → contrat R4 préservé).
  3. references/graph-diamond-pattern.md — append « §5 Émission des vagues »
     (après la note de provenance — bloc PATTERN byte-identique préservé).
  4. references/journal-versions.md — insertion de l'entrée v3.39.0 (migration)
     après la note de mécanique, avant le BLOC-DEPLACÉ v3.38.0.

Garde-fous : budget SKILL.md ≤ 30719 octets UTF-8 ; idempotence (re-jeu = no-op,
rc=0) ; ABANDON rc=2 sans AUCUNE écriture si un ancrage ou le budget échoue.
"""
import re
import sys
from pathlib import Path

RACINE = Path("/home/z/my-project/KNOWLEDGE-repo")
SKILL = RACINE / "skills/gen-plan/SKILL.md"
PROTO = RACINE / "skills/gen-plan/references/protocoles-detailles.md"
DIAMOND = RACINE / "skills/gen-plan/references/graph-diamond-pattern.md"
JOURNAL = RACINE / "skills/gen-plan/references/journal-versions.md"
BUDGET = 30719  # < 30 Kio strict (contrat re-curation R1)

# ----------------------------------------------------------------- textes

ROW_GD_OLD = ("| **Graph Diamond** | **E9-E14** | Parallélisation PAR DÉFAUT des tâches ET commandes "
              "prouvées indépendantes (le série est l'exception justifiée — philosophie #4 v3.24.0, "
              "extension aux commandes v3.32.0) — tracée au worklog | `references/graph-diamond-pattern.md` |")
ROW_GD_NEW = ("| **Graph Diamond** | **E9-E14** | Parallélisation PAR DÉFAUT des tâches ET commandes "
              "indépendantes (série = exception justifiée — #4 v3.24.0/v3.32.0/v3.40.0 émission : "
              "fan-out bloc + `&`+`wait`) — tracé worklog | `references/graph-diamond-pattern.md` |")

PHILO4_OLD = ("4. **Parallélisation par défaut des tâches ET des commandes sur preuve d'indépendance** "
              "(v3.24.0/v3.32.0) — vagues indépendantes prouvées en PARALLÈLE : Graph Diamond automatique "
              "(E9-E14), série = exception tracée ; dégradation gracieuse 429 — intégral : "
              "`references/protocoles-detailles.md` (#4).")
PHILO4_NEW = ("4. **Parallélisation par défaut des tâches ET des commandes sur preuve d'indépendance** "
              "(v3.24.0/v3.32.0 + **émission v3.40.0**) — vagues indépendantes en PARALLÈLE : Graph Diamond "
              "(E9-E14), série = exception tracée ; émission : fan-out multi-appels + concurrence "
              "`&`+`wait` ; dégradation 429 — intégral : `references/protocoles-detailles.md` (#4).")

# Compensations byte (résumés compactés — intégraux intacts dans references/)
LECTURE7_OLD = ("7. **Lecture bloc par bloc** — Fichiers > 500 lignes : lire par blocs successifs "
                "(limit/offset), produire une synthèse intermédiaire entre chaque bloc. Ne jamais lire "
                "un fichier > 500 lignes d'un seul coup. Voir `references/profils-ressource.md` "
                "(VIEUX PC règle 4 : troncature 500 lignes).")
LECTURE7_NEW = ("7. **Lecture bloc par bloc** — Fichiers > 500 lignes : lire par blocs successifs "
                "(limit/offset) avec synthèse intermédiaire — jamais d'un seul coup "
                "(détail : `references/profils-ressource.md`).")

E7DISP5_OLD = "(statuts du disque ; step-ok : après confirmation)"
E7DISP5_NEW = "(statuts du disque)"

CONTING_OLD = "- **Coefficients de contingence (détail et preuves : `references/grille-token.md`)** :"
CONTING_NEW = "- **Contingences (preuves : `references/grille-token.md`)** :"

# Compensations complémentaires (round 2 — résumés compactés, intégraux intacts)
C1_OLD = ("rc=0 → no-op ; rc≠0 → suspension de toute tâche + `--reinstall` (pipeline PM-INSTALL, "
          "clone éphémère) AVANT toute autre étape ; directive post-réinstallation intégrée au plan ; idempotente.")
C1_NEW = ("rc=0 → no-op ; rc≠0 → suspension + `--reinstall` (pipeline PM-INSTALL) AVANT toute autre "
          "étape ; directive post-réinstall intégrée au plan ; idempotente.")

C2_OLD = "├── SKILL.md                          # < 30 Kio — progressive disclosure (v3.39.0)"
C2_NEW = "├── SKILL.md                          # < 30 Kio — progressive disclosure"

C3_OLD = "— JAMAIS de lecture intégrale par défaut pour un skill LOURD/CRITIQUE | `scripts/poids-chargement.py` |"
C3_NEW = "— JAMAIS de lecture intégrale par défaut | `scripts/poids-chargement.py` |"

C4A_OLD = "re-jeu sans ré-appel (démo mesurée : gain 440×)"
C4A_NEW = "re-jeu sans ré-appel (gain 440×)"

C4B_OLD = "invalidation automatique par état des fichiers cibles (taille/mtime)"
C4B_NEW = "invalidation auto par état des cibles (taille/mtime)"

C5_OLD = "(recommandation R1 de l'étude de faisabilité Task 70 — le goulot réel de l'écosystème est le budget #token)"
C5_NEW = "(recommandation R1 étude Task 70 — le goulot réel est le budget #token)"

ENTREE_V3400 = (
    "- **v3.40.0 (2026-11-08, web-ecef7f80 — Task 77 G2, directive trace 1a1ba66f3aff26e9 : « vérifie "
    "que mon écosystème te permet de lancer 4 commandes en parallèle »)** : PROTOCOLE D'ÉMISSION "
    "PARALLÈLE — opérationnalise la philosophie #4 (doctrine présente v3.24.0/v3.32.0 mais jamais "
    "appliquée : plans Tasks 70-76 100 % « série justifiée », zéro vague tracée) : fan-out multi-appels "
    "(un même bloc, tous outils) + concurrence intra-commande (`&`+`wait`/`xargs -P` ; mesure : "
    "4×sleep 2 → 2,00 s vs 8,00 s — le shell persistant sérialise les Bash d'un même bloc) ; bornes "
    "≤ 4/vague (G-RES), preuve d'indépendance légère, exceptions série inchangées, tracé worklog "
    "allégé (une ligne/vague). Inline : §1.2bis + §1.4 #4 (compensation byte — description inchangée, "
    "non-régression triggers) ; intégral : protocoles-detailles.md (extension v3.40.0) + "
    "graph-diamond-pattern.md §5. MINOR. Cascade KO-L004 : PM v3.40.0 + SHARED v1.7.35 + "
    "PM-INSTALL v1.9.12 (Task 77 G2)."
)

PROTOCOLE_EXT = (
    "\n\n---\n\n"
    "### Extension v3.40.0 — protocole d'émission parallèle (#4 — directive trace 1a1ba66f3aff26e9)\n\n"
    "**Directive propriétaire (2026-11-08, session web-ecef7f80)** : « vérifie que mon écosystème te "
    "permet de lancer 4 commandes en parallèle car j'ai l'impression que tu ne le fais jamais lorsque "
    "je t'envoie mes demandes en utilisant mon écosystème… si effectivement mon écosystème ne te le "
    "permet pas alors fais en sorte qu'il te permette de le faire à partir de maintenant. » — "
    "Diagnostic Task 77 G2 : la doctrine #4 était PRÉSENTE (v3.24.0/v3.32.0) mais NON opérationnalisée "
    "(aucun protocole d'émission, plans récents 100 % série, aucune vague tracée) ; la présente "
    "extension opère le pont entre la doctrine et l'ÉMISSION effective des appels.\n\n"
    "**PROTOCOLE D'ÉMISSION PARALLÈLE — deux niveaux distincts et complémentaires :**\n\n"
    "1. **FAN-OUT MULTI-APPELS (niveau émission)** : dès que ≥ 2 appels d'outils (Bash, Read, Grep, "
    "Glob, LS…) sont PROUVÉS indépendants (cibles distinctes, aucune écriture partagée, aucune "
    "dépendance d'ordre), les émettre ENSEMBLE dans un MÊME bloc d'appels (un seul message "
    "multi-outils — Graph Diamond phase 2) plutôt qu'un par un : réduit les allers-retours, active la "
    "spéculation, couvre tous les types d'outils. **Réalité harnais (mesurée, preuve Task 77 "
    "T2.1.1-a)** : le shell persistant de l'environnement SÉRIALISE les commandes Bash d'un même bloc "
    "(4×sleep 2 : départs échelonnés ~2,5 s) — le fan-out reste bénéfique (latence d'émission, outils "
    "non-shell) mais ne crée PAS de concurrence Bash↔Bash.\n"
    "2. **CONCURRENCE INTRA-COMMANDE (niveau exécution)** : lorsque ≥ 2 COMMANDES shell indépendantes "
    "et que le temps mural compte, les lancer en jobs arrière-plan AU SEIN D'UNE SEULE invocation : "
    "`cmd1 & cmd2 & … & wait` (ou `xargs -P N`). Concurrence VRAIE mesurée : 4×sleep 2 → 2,00 s "
    "(vs 8,00 s en série — gain ×4, preuve Task 77 T2.1.2). Discipline : sorties redirigées vers des "
    "fichiers DISTINCTS puis agrégées (jamais d'entrelacement non maîtrisé) ; codes retour vérifiés "
    "par job (`wait` ne propage que le dernier — capturer chaque `$!`/rc si un échec doit être "
    "détecté).\n\n"
    "**Bornes et garde-fous :**\n"
    "- **≤ 4 jobs/appels par vague par défaut** — piloté par G-RES (PARALLELE=4 · PARALLELE_REDUIT=2 · "
    "SERIE=1), re-verdict entre les vagues (hook continu E9-E14).\n"
    "- **Preuve d'indépendance LÉGÈRE** : une ligne au moment de l'émission (cibles distinctes / "
    "aucune écriture partagée / aucune dépendance d'ordre). Cérémonie proportionnée : vague en lecture "
    "seule = preuve en une ligne ; vague avec écritures = la preuve nomme les fichiers et l'absence "
    "de recouvrement.\n"
    "- **Série OBLIGATOIRE (exceptions tracées — inchangées)** : écriture partagée (même fichier, même "
    "registre, worklog), dépendance d'ordre (B lit la sortie de A), chaîne golden-master → "
    "modification → re-test, opérations git sur le même dépôt, verdict resource-monitor SERIE/PAUSE, "
    "profil ECO/VIEUX PC.\n"
    "- **Tracé worklog ALLÉGÉ pour les vagues de commandes** : une ligne par vague (`VAGUE-PAR "
    "T<n>-a∥T<n>-b∥… [preuve : …]`). Le tracé complet Task IDs `N-a`/`N-b` + re-verdict inter-vagues "
    "demeure pour les vagues de TÂCHES et d'agents (Graph Diamond §3) ; une vague de commandes en "
    "lecture seule n'exige AUCUN re-verdict intermédiaire (aucune mutation entre les lectures).\n"
    "- **Anti-régression** : émettre un appel par un pour des actions indépendantes = sériographie "
    "(anti-pattern Graph Diamond §4) — le défaut est le BLOC, l'exception est la file.\n"
)

DIAMOND_S5 = (
    "\n\n## §5 — Émission des vagues (v3.40.0)\n\n"
    "> Extension Task 77 G2 (directive propriétaire trace 1a1ba66f3aff26e9) — intégral du protocole : "
    "`protocoles-detailles.md` (Extension v3.40.0). Le bloc PATTERN ci-dessus demeure byte-identique "
    "(R4).\n\n"
    "Deux niveaux d'émission, distincts et complémentaires :\n"
    "- **fan-out multi-appels** (phase 2 ci-dessus) : les appels indépendants sont émis ENSEMBLE dans "
    "un même bloc multi-outils — réalité harnais mesurée : le shell persistant sérialise les "
    "commandes Bash d'un même bloc (le fan-out réduit la latence d'émission et conserve la concurrence "
    "pour les outils non-shell) ;\n"
    "- **concurrence intra-commande** : pour une concurrence Bash VRAIE, lancer les commandes "
    "indépendantes en jobs arrière-plan au sein d'UNE invocation (`cmd1 & cmd2 & wait`, `xargs -P`) — "
    "mesuré : 4×sleep 2 → 2,00 s vs 8,00 s (gain ×4) ; sorties dans des fichiers distincts, agrégées "
    "ensuite.\n\n"
    "Bornes ≤ 4 par vague (G-RES), preuve d'indépendance légère (une ligne), tracé worklog une ligne "
    "par vague — exceptions série inchangées (§3).\n"
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

    if "version: 3.40.0" in skill:
        print("[NO-OP] SKILL.md déjà en v3.40.0 (idempotence — re-jeu sans effet)")
        for p, marqueur in ((PROTO, "Extension v3.40.0"), (DIAMOND, "§5 — Émission des vagues")):
            t = p.read_text(encoding="utf-8")
            print("  %s : %s" % (p.name, "présent" if marqueur in t else "ABSENT (incohérent)"))
        return 0

    # --- 1. capture de l'entrée v3.39.0 (migration R4) AVANT remplacement
    m = re.findall(r"^- \*\*v3\.39\.0 \([^\n]*$", skill, re.M)
    if len(m) != 1:
        print("ABANDON : entrée §5.6 v3.39.0 trouvée %d fois (attendu 1)" % len(m))
        return 2
    entree_v3390 = m[0]

    # --- 2. SKILL.md : toutes les substitutions en mémoire
    t = skill
    t = sub(t, "version: 3.39.0", "version: 3.40.0", "version frontmatter")
    t = sub(t, ROW_GD_OLD, ROW_GD_NEW, "§1.2bis rangée Graph Diamond")
    t = sub(t, PHILO4_OLD, PHILO4_NEW, "§1.4 philosophie #4")
    t = sub(t, LECTURE7_OLD, LECTURE7_NEW, "§1.4 #7 compensation")
    t = sub(t, E7DISP5_OLD, E7DISP5_NEW, "§1.2bis point 5 compensation")
    t = sub(t, CONTING_OLD, CONTING_NEW, "§4 contingences compensation")
    t = sub(t, C1_OLD, C1_NEW, "§1.16 compensation r2")
    t = sub(t, C2_OLD, C2_NEW, "§2.2 commentaire compensation r2")
    t = sub(t, C3_OLD, C3_NEW, "§1.2bis E5-POIDS compensation r2")
    t = sub(t, C4A_OLD, C4A_NEW, "§1.2bis R2-CACHE compensation r2-a")
    t = sub(t, C4B_OLD, C4B_NEW, "§1.2bis R2-CACHE compensation r2-b")
    t = sub(t, C5_OLD, C5_NEW, "§1.2bis E5-POIDS compensation r2-c")
    t = sub(t, entree_v3390, ENTREE_V3400, "§5.6 entrée courante")

    taille_avant = len(skill.encode("utf-8"))
    taille_apres = len(t.encode("utf-8"))
    print("SKILL.md : %d → %d octets (delta %+d, budget %d)" % (
        taille_avant, taille_apres, taille_apres - taille_avant, BUDGET))
    if taille_apres > BUDGET:
        print("ABANDON : budget < 30 Kio dépassé de %d octets — compensations supplémentaires requises"
              % (taille_apres - BUDGET))
        return 2

    # --- 3. fichiers references (en mémoire, écritures seulement si tout passe)
    proto = PROTO.read_text(encoding="utf-8")
    if "Extension v3.40.0" in proto:
        print("ABANDON : protocoles-detailles.md contient déjà l'extension v3.40.0")
        return 2
    proto_new = proto.rstrip("\n") + PROTOCOLE_EXT

    diamond = DIAMOND.read_text(encoding="utf-8")
    if "§5 — Émission des vagues" in diamond:
        print("ABANDON : graph-diamond-pattern.md contient déjà §5")
        return 2
    diamond_new = diamond.rstrip("\n") + DIAMOND_S5

    journal = JOURNAL.read_text(encoding="utf-8")
    if entree_v3390.split("(")[0] + "(2026-11-08" in journal:
        print("ABANDON : journal-versions.md contient déjà l'entrée v3.39.0 migrée")
        return 2
    journal_new = sub(journal, NOTE_MIGRATION, NOTE_MIGRATION + "\n\n" + entree_v3390,
                      "journal-versions insertion v3.39.0")

    # --- 4. écritures (tout est validé — aucune écriture partielle possible)
    SKILL.write_text(t, encoding="utf-8")
    PROTO.write_text(proto_new, encoding="utf-8")
    DIAMOND.write_text(diamond_new, encoding="utf-8")
    JOURNAL.write_text(journal_new, encoding="utf-8")

    print("Écrit : SKILL.md v3.40.0 (%d o) · protocoles-detailles.md (%d → %d o) · "
          "graph-diamond-pattern.md (%d → %d o) · journal-versions.md (+ entrée v3.39.0 migrée, %d → %d o)"
          % (taille_apres, len(proto.encode("utf-8")), len(proto_new.encode("utf-8")),
             len(diamond.encode("utf-8")), len(diamond_new.encode("utf-8")),
             len(journal.encode("utf-8")), len(journal_new.encode("utf-8"))))
    print("Entrée v3.39.0 migrée (%d caractères, R4 byte-identité)" % len(entree_v3390))
    return 0


if __name__ == "__main__":
    sys.exit(main())
