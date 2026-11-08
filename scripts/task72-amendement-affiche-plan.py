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

"""task72-amendement-affiche-plan.py — SG1.3bis (plan rév. 3, directive complémentaire 2
trace 1a1b7fe1c7238e8d) : intégration de la fenêtre native d'affichage du plan
(AFFICHE-PLAN natif — Z.ai : liste de tâches TodoWrite/TodoRead) dans E7-DISP.

Amendement de gen-plan v3.39.0 PRÉ-publication (dépôt encore à v3.38.0 — la cascade
unique SG1.4 porte la version consolidée). Éditions chirurgicales verrouillées
(count==1 ou abandon sans écriture) + compensation de taille sur résumés NON
verrouillés + append intégral « point 6 » dans references/protocoles-detailles.md
(HORS blocs déplacés R4 — byte-identité des 9 blocs préservée).

Gardes :
  - chaque old doit apparaître exactement 1 fois (sinon ABANDON rc=2, rien n'est écrit) ;
  - taille finale SKILL.md < 30 720 octets (30 Kio — D002), sinon ABANDON rc=2 ;
  - idempotent ×2 : déjà-appliqué détecté → no-op rc=0 ;
  - le bloc R4 hooks_patterns de references/protocoles-detailles.md n'est pas touché
    (l'append se fait après le marqueur FIN-BLOC-DEPLACÉ:philo4, en fin de fichier).
"""
import sys
from pathlib import Path

RACINE = Path("/home/z/my-project")
SKILL = RACINE / "skills" / "gen-plan" / "SKILL.md"
PROTO = RACINE / "skills" / "gen-plan" / "references" / "protocoles-detailles.md"
LIMITE = 30 * 1024  # 30 Kio — D002

# ---------------------------------------------------------------------------
# Éditions SKILL.md — (étiquette, old, new)
# ---------------------------------------------------------------------------
EDITIONS = [
    # E1 — table §1.2bis, colonne Étape de la ligne E7-DISP (+ fenêtre native)
    ("E1-table-etape",
     "| **E7-DISP — Affichage obligatoire du plan** | **E7/E8/E13 + ouverture d'étape (v3.36.0)** |",
     "| **E7-DISP — Affichage obligatoire du plan** | **E7/E8/E13 + ouverture d'étape (v3.36.0)"
     " + fenêtre native début/fin d'étape (v3.39.0)** |"),
    # E2 — table §1.2bis, mécanisme E7-DISP compacté (l'intégral vit en references/)
    ("E2-table-mecanisme",
     "Toute écriture/mise à jour du fichier plan (création E7, ajustement E13, re-génération"
     " règle d'or n°2/KO-L005, reprise) n'est TERMINÉE qu'après la chaîne complète : plan écrit"
     " + answer key + verdict E8 consigné (horodatages couplés) + worklog R5 avec marqueur"
     " `PLAN-AFFICHE` + bloc récapitulatif visible au chat — verdict mécanique bloquant ;"
     " affichage REJOUABLE à toute reprise (v3.27.0) ; **à l'ouverture de chaque nouvelle étape"
     " d'exécution (v3.36.0) : bloc PLAN-AFFICHE d'évolution du déroulement (tous les groupes"
     " + statuts + compteurs + position courante — tous modes)**",
     "Toute écriture du fichier plan (création E7, E13, re-génération KO-L005, reprise) n'est"
     " TERMINÉE qu'après la chaîne : plan écrit + answer key + verdict E8 (horodatages couplés)"
     " + worklog R5 marqueur `PLAN-AFFICHE` + bloc récapitulatif au chat — verdict mécanique"
     " bloquant ; affichage REJOUABLE (v3.27.0) ; à l'ouverture de chaque étape (v3.36.0) :"
     " bloc d'évolution du déroulement (groupes + statuts + compteurs + position — tous modes)"),
    # E3 — résumé E1-RES compacté (commande intégrale dans le bloc R4 hooks_patterns)
    ("E3-resume-E1-RES",
     "**Hook E1-RES — ouverture de session (4 vérifications AVANT toute analyse)** :"
     " (1) lecture seule préalable B-11 (worklog/plan/arbitres) ; (2) collecte G-RES"
     " (`monitor.py --state-file tmp/resource-monitor-state.json` : OK/PRESSION/CRITIQUE →"
     " mode, journalisé) ; (3) fraîcheur du plan (gen-plan modifiée et valide → re-généré"
     " avant reprise) ; (4) garde post-coupure (règle d'or n°9 : piliers + integrity →"
     " rétablissement auto). **Reprise (v3.27.0)** : message pendant un plan en vol → worklog"
     " + fraîcheur + E13 + re-validation E8 + R5 + affichage ; l'état « en vol » dérive du"
     " DISQUE (RC3).",
     "**Hook E1-RES — ouverture de session (4 vérifications AVANT analyse)** : (1) lecture"
     " seule préalable B-11 (worklog/plan/arbitres) ; (2) collecte G-RES (`monitor.py` :"
     " OK/PRESSION/CRITIQUE, journalisé) ; (3) fraîcheur du plan (modifiée et valide →"
     " re-généré avant reprise) ; (4) garde post-coupure (règle d'or n°9 : piliers + integrity"
     " → rétablissement auto). **Reprise (v3.27.0)** : message pendant un plan en vol →"
     " worklog + fraîcheur + E13 + E8 + R5 + affichage ; état « en vol » dérivé du DISQUE"
     " (RC3)."),
    # E4 — résumé E7-DISP : 5 points compactés + point 6 fenêtre native (directive 2)
    ("E4-resume-E7-DISP",
     "**Hook E7-DISP — affichage obligatoire (5 points, garde bloquante)** : (1) plan écrit"
     " `download/` ; (2) answer key >= 1 décision vérifiable ; (3) validation E8 aux"
     " horodatages COUPLÉS (toute écriture = re-validation) ; (4) worklog R5 + marqueur"
     " `PLAN-AFFICHE` ; (5) bloc récapitulatif AFFICHÉ au chat. Garde :"
     " `check_plan_protocol.py --plan <plan.md> --worklog worklog.md` (P1-P5). **Affichage"
     " REJOUABLE** (jamais présumé). **Ouverture d'étape (v3.36.0, tous modes)** :"
     " PLAN-AFFICHE au début de chaque groupe G<k> (vue d'évolution, statuts du disque) ;"
     " step-ok : après confirmation.",
     "**Hook E7-DISP — affichage obligatoire (6 points, garde bloquante)** : (1) plan écrit"
     " `download/` ; (2) answer key >= 1 décision ; (3) E8 aux horodatages COUPLÉS (toute"
     " écriture = re-validation) ; (4) worklog R5 + marqueur `PLAN-AFFICHE` ; (5) bloc"
     " récapitulatif AU chat. Garde `check_plan_protocol.py` (P1-P5) ; affichage REJOUABLE ;"
     " ouverture d'étape (v3.36.0, tous modes) : PLAN-AFFICHE d'évolution au début de chaque"
     " groupe G<k> (statuts du disque ; step-ok : après confirmation). **(6) Fenêtre native"
     " (v3.39.0 — directive 1a1b7fe1c7238e8d)** : fenêtre des étapes du plan via le"
     " mécanisme NATIF de l'agent dédié à ce rôle (Z.ai : liste de tâches `TodoWrite`/"
     "`TodoRead`) — affichée au DÉBUT de l'exécution du plan d'actions, MISE À JOUR à chaque"
     " FIN d'étape ; intégral : `references/protocoles-detailles.md` (point 6)."),
    # E5 — §1.16 clause v3.35.2 compactée
    ("E5-clause-v3352",
     "**v3.35.2** : contrôle du SKILL.md de TOUTES les entrées KB (dérivation dynamique) ;"
     " skills KB manquants → AUTO-RÉPARÉS depuis le miroir `KNOWLEDGE-repo/`"
     " (INSTALLE-REPARÉ, rc=0, trace worklog).",
     "**v3.35.2** : contrôle du SKILL.md de toutes les entrées KB ; manquants → AUTO-RÉPARÉS"
     " depuis le miroir (INSTALLE-REPARÉ, rc=0, trace worklog)."),
    # E6 — §1.6 mobilisation compactée
    ("E6-mobilisation",
     "- **Mobilisation** : tables E1-E8, n°54, n°55, E15, par déclencheur × modes —"
     " intégrales : `references/disciplines-mobilisation.md` ; socle commun"
     " (context/loop/graph/harness + PEK) à TOUT déclencheur du §A. **Hook continu E9-E14** :"
     " G-RES re-collecté à chaque checkpoint E11 et entre les vagues ; PRESSION → ECO,"
     " CRITIQUE → série/PAUSE. gen-plan = détenteur principal de la méthode prompt-engineering"
     " (SHARED §7 ; PEK v4.1 — `references/prompt-engineering-kit.md`).",
     "- **Mobilisation** : tables E1-E8, n°54-55, E15, par déclencheur × modes — intégrales :"
     " `references/disciplines-mobilisation.md` ; socle commun (context/loop/graph/harness"
     " + PEK) à tout déclencheur du §A. **Hook continu E9-E14** : G-RES à chaque checkpoint"
     " E11 et entre vagues ; PRESSION → ECO, CRITIQUE → série/PAUSE. gen-plan = détenteur"
     " principal de la méthode prompt-engineering (SHARED §7 ; PEK v4.1)."),
    # E7 — §1.15 KO-L004 compactée
    ("E7-KO-L004",
     "+ génération mécanique du PM (`scripts/generer-pm-skill.py --generate <skill>`,"
     " substitutions verrouillées, anti-rétrogradation R2).",
     "+ génération mécanique du PM (`scripts/generer-pm-skill.py`, substitutions verrouillées,"
     " R2)."),
    # E8 — §5.5 cadence : début d'exécution + fin de groupe → fenêtre native
    ("E8-cadence-5-5",
     "**Cadence** : ouverture de groupe → PLAN-AFFICHE d'évolution puis tableau du groupe"
     " (step-ok : après confirmation) ; fin de tâche → ligne + compteurs ; fin de sous-groupe"
     " → rappel ; clôture → tableau final + verdict correct-work(groupe).",
     "**Cadence** : début d'exécution → fenêtre native complète (E7-DISP point 6 — Z.ai :"
     " `TodoWrite`) ; ouverture de groupe → PLAN-AFFICHE d'évolution puis tableau du groupe"
     " (step-ok : après confirmation) ; fin de tâche → ligne + compteurs ; fin de sous-groupe"
     " → rappel ; fin de groupe → fenêtre native mise à jour ; clôture → tableau final +"
     " verdict correct-work(groupe)."),
    # E9 — §5.5 queue orthogonale compactée
    ("E9-orthogonal",
     "**Orthogonal à l'exécution** : couche de LECTURE ; Graph Diamond automatique dès preuve"
     " d'indépendance (même à travers les sous-groupes, série = exception tracée) ; groupes"
     " plats normalisés à l'ouverture (R6/R2).",
     "**Orthogonal à l'exécution** : couche de LECTURE ; Graph Diamond automatique dès preuve"
     " d'indépendance (sous-groupes inclus, série = exception tracée) ; groupes plats"
     " normalisés à l'ouverture (R6/R2)."),
    # E10 — §5.6 entrée v3.39.0 : directives complémentaires 1+2 + fenêtre native
    ("E10-entree-v3390",
     "- **v3.39.0 (2026-11-08, session web-ecef7f80 — Task 72 G1, directives « Chantier R1 :"
     " re-curation progressive disclosure de gen-plan » + complémentaire 1a1b7b297b7b4975)** :"
     " 9 blocs déplacés R4 byte-identité vers `references/` (journal · règles d'or + KO ·"
     " disciplines · protocoles) + append contingences (grille-token.md) — résumés NOUVEAUX"
     " inline, aucune duplication ; contrats certifiés baseline golden master + vérif POST"
     " (T1.1.0 — scripts/task72-baseline-verifier.py) ; lecture ciblée = état par défaut"
     " (E5-POIDS). MINOR. Cascade KO-L004 complète (SG1.4 — worklog Task 72).",
     "- **v3.39.0 (2026-11-08, web-ecef7f80 — Task 72 G1, directives « Chantier R1 :"
     " re-curation progressive disclosure de gen-plan » + complémentaires 1a1b7b297b4975"
     " [skill re-curation par script] et 1a1b7fe1c7238e8d [fenêtre native AFFICHE-PLAN])** :"
     " 9 blocs déplacés R4 byte-identité vers `references/` + append contingences"
     " (grille-token.md) — résumés NOUVEAUX inline, zéro duplication ; contrats baseline"
     " golden master + vérif POST (T1.1.0) ; lecture ciblée = état par défaut (E5-POIDS) ;"
     " **E7-DISP point 6 « fenêtre native »** (Z.ai : liste de tâches `TodoWrite`/`TodoRead`"
     " — début d'exécution + chaque fin d'étape) : intégral `references/protocoles-detailles.md`."
     " MINOR. Cascade KO-L004 : SG1.4 (worklog Task 72)."),
    # E11 — note de saut §1.8→§1.14 compactée (provenance déjà portée par les en-têtes)
    ("E11-note-saut",
     "> Saut §1.8 → §1.14 intentionnel (Task 21 A7) ; provenance : `references/regles-or.md`.",
     "> Saut §1.8 → §1.14 intentionnel (Task 21 A7)."),
    # E12 — commentaire de résumé §1.2bis compacté
    ("E12-commentaire-resume",
     "<!-- RÉSUMÉ v3.39.0 — protocoles intégraux (R4) : references/protocoles-detailles.md -->",
     "<!-- RÉSUMÉ v3.39.0 — intégraux : references/protocoles-detailles.md -->"),
    # E13 — §1.16 É1-INSTALL : chemin complet raccourci (intégral dans le bloc R4 routage)
    ("E13-chemin-e1-install",
     "à l'ouverture de session, AVANT E1 : `python3 skills/gen-plan/scripts/ensure-installed.py"
     " --check` (chemin canonique).",
     "à l'ouverture de session, AVANT E1 : `ensure-installed.py --check` (chemin canonique)."),
    # E14 — §5.4 hook correct-work par phase compacté
    ("E14-hook-5-4",
     "Dès qu'une phase du plan d'actions vient de se terminer, lancer `correct-work(livrables"
     " de la phase, mode=CIBLE)` AVANT d'entamer la phase suivante : PASS → phase suivante ;"
     " PASS AVEC RÉSERVES → réserves loggées au worklog, exécution continue ; FAIL → pause"
     " jusqu'à correction puis re-vérification. Le hook E8 (fin de plan) reste la"
     " vérification finale.",
     "Dès qu'une phase du plan d'actions se termine, lancer `correct-work(livrables de la"
     " phase, mode=CIBLE)` AVANT la phase suivante : PASS → suivante ; PASS AVEC RÉSERVES →"
     " réserves au worklog, exécution continue ; FAIL → pause, correction, re-vérification."
     " Le hook E8 reste la vérification finale."),
]

# ---------------------------------------------------------------------------
# Append intégral — references/protocoles-detailles.md (HORS blocs R4)
# ---------------------------------------------------------------------------
ANCRE_FIN_PROTO = "<!-- FIN-BLOC-DEPLACÉ:philo4 -->"

EXTENSION = """

---

### Extension v3.39.0 — E7-DISP point 6 : fenêtre native d'affichage du plan (AFFICHE-PLAN natif — directive complémentaire 2, trace 1a1b7fe1c7238e8d)

**Directive propriétaire (2026-11-08, session web-ecef7f80)** : « je veux que la fenêtre qui affiche les étapes du plan d'actions soit affichée via la fonction, le script ou la commande qui est dédiée à ce rôle nativement dans "Z.ai" (ou via la commande à laquelle "Z.ai" fait appel) et cela au début de l'exécution du plan d'actions, ainsi qu'à chaque fois qu'une étape du plan d'actions se terminent. intègre $FACON cette fonction, script ou commande dans "AFFICHE-PLAN" de mon écosystème. » — $FACON = de façon cohérente, optimisée et fonctionnelle (glossaire §A).

**Mécanisme natif dédié (Z.ai)** : la **liste de tâches** — fenêtre native du client dédiée à l'affichage des étapes d'un plan d'actions ; outil `TodoWrite` (écriture : création/mise à jour de la liste et des statuts) et `TodoRead` (lecture). Chez tout autre agent : l'équivalent natif dédié à ce rôle (jamais d'invention d'un canal artificiel — R2).

**Point 6 — fenêtre native (canal d'affichage SUPPLÉMENTAIRE, s'ajoute à la chaîne 5 points du hook E7-DISP du bloc hooks_patterns ci-dessus)** :

1. **au DÉBUT de l'exécution du plan d'actions** : la fenêtre native affiche toutes les étapes (groupes `G<k>`) du plan, avec statuts dérivés de l'état vérifiable (règle d'or n°5 / KO-L003 — jamais inventés) et position courante ;
2. **à chaque FIN d'étape (groupe `G<k>`)** : la fenêtre native est MISE À JOUR — l'étape terminée marquée, position et compteurs actualisés (complément du bloc PLAN-AFFICHE d'ouverture d'étape v3.36.0 affiché au chat) ; la mise à jour accompagne le verdict correct-work(groupe).

**Frontières (non-régression des canaux existants)** : la fenêtre native NE REMPLACE ni le bloc récapitulatif au chat (point 5), ni le marqueur `PLAN-AFFICHE` au worklog (point 4), ni la garde mécanique `check_plan_protocol.py` (P1-P5) — la preuve d'affichage journalisable reste le marqueur worklog ; chaque affichage/mise à jour de la fenêtre native est consigné dans la même entrée worklog (mention « fenêtre native »). Affichage REJOUABLE : à toute reprise (E1-RES) sur un plan en vol, la fenêtre native est ré-affichée avant toute autre action (même mécanique que le bloc chat — jamais présumé).
"""


def octets(t: str) -> int:
    return len(t.encode("utf-8"))


def main() -> int:
    texte = SKILL.read_text(encoding="utf-8")

    # Idempotence ×2 : déjà appliqué ?
    deja = all(o not in texte and n in texte for _, o, n in EDITIONS)
    proto = PROTO.read_text(encoding="utf-8")
    if deja and "Extension v3.39.0 — E7-DISP point 6" in proto:
        print("DÉJÀ APPLIQUÉ — no-op (14/14 éditions + extension présentes).")
        print(f"SKILL.md : {octets(texte)} octets ({octets(texte)/1024:.1f} Kio)")
        return 0

    avant = octets(texte)
    print(f"AVANT : {avant} octets ({avant/1024:.2f} Kio) — limite {LIMITE} octets")

    # Verrouillage : chaque old exactement 1 fois, AVANT toute écriture
    manquants = [(lbl, texte.count(o)) for lbl, o, _ in EDITIONS if texte.count(o) != 1]
    if manquants:
        for lbl, c in manquants:
            print(f"ABANDON : édition {lbl} — old trouvé {c} fois (attendu 1)")
        return 2
    if proto.count(ANCRE_FIN_PROTO) != 1:
        print("ABANDON : ancre FIN-BLOC-DEPLACÉ:philo4 introuvable ou ambiguë dans "
              "references/protocoles-detailles.md")
        return 2

    # Application (en mémoire) + delta par édition
    total = 0
    for lbl, old, new in EDITIONS:
        texte = texte.replace(old, new, 1)
        d = octets(new) - octets(old)
        total += d
        print(f"  [{lbl:<22}] {d:+5d} octets")
    apres = octets(texte)
    print(f"APRÈS : {apres} octets ({apres/1024:.2f} Kio) — delta éditions {total:+d}")

    if apres >= LIMITE:
        print(f"ABANDON : {apres} octets >= limite D002 ({LIMITE}) — compensation insuffisante")
        return 2

    # Écritures (SKILL.md + append intégral dans protocoles-detailles.md)
    SKILL.write_text(texte, encoding="utf-8")
    PROTO.write_text(proto.rstrip("\n") + "\n" + EXTENSION, encoding="utf-8")
    print(f"ÉCRIT : SKILL.md {apres} octets ({apres/1024:.2f} Kio < 30 Kio — D002 maintenu)")
    print(f"ÉCRIT : references/protocoles-detailles.md +{octets(EXTENSION)} octets "
          "(extension point 6, HORS blocs R4)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
