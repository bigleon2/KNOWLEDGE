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
Task 84 G3 — P1 inscription socle n°56 (pendance Task 83 §4) : amendement chirurgical.

Éditions assert count==1 (discipline refactoring-engineering) :
  1. skills/@mon-ecosysteme/PROMPT-MAITRE-SHARED.md — §7 table de définitions :
     ligne « Agent engineering (n°56) » APRÈS la ligne Refactoring test ;
     §7 registre d'assignation : ligne `agent-engineering` APRÈS `refactor-guard`.
     (PAS de bump version — le générateur KO-L004 fait v1.7.36→v1.7.37 ;
     la révision sera amendée par task84-cascade-socle.py pour couvrir §7.)
  2. skills/gen-plan/SKILL.md — v3.41.0→v3.42.0 : version frontmatter,
     §1.6 ligne « Agent engineering », §3 Relations ligne agent-engineering,
     §5.6 entrée courante v3.42.0 (migration R4 de l'entrée v3.41.0 vers
     references/journal-versions.md).
  3. skills/gen-plan/references/journal-versions.md — insertion v3.41.0 (migrée).

Garde-fous : budget SKILL.md ≤ 30719 o ; idempotence (re-jeu = no-op rc=0) ;
ABANDON rc=2 SANS AUCUNE écriture si un ancrage échoue (tout en mémoire).
Description frontmatter gen-plan INCHANGÉE (non-régression triggers R2).
"""
import re
import sys
from pathlib import Path

R = Path("/home/z/my-project/KNOWLEDGE-repo")
SHARED = R / "skills/@mon-ecosysteme/PROMPT-MAITRE-SHARED.md"
SKILL = R / "skills/gen-plan/SKILL.md"
JOURNAL = R / "skills/gen-plan/references/journal-versions.md"
BUDGET = 30719  # < 30 Kio strict (contrat re-curation R1)

# ------------------------------------------------------------------ SHARED §7
RT_ROW = ("| **Refactoring test** (outil de la discipline n°55) | Détecter les situations où un refactoring est nécessaire, "
          "les évaluer (risque/urgence/portée — scoring principal/intérêt) et produire le graphe d'interactions "
          "(blast radius) des modifications futures ; verdict machine OK/PRESSION/CRITIQUE ; producteur "
          "d'information — ne modifie rien. Ancrage 2026 : SQALE (principal/intérêt), Tornhill (hotspots), "
          "change impact analysis (program dependency graphs), blast radius avant action d'agent. | gen-plan PM "
          "§1.9 (détection/évaluation E4/E7 + situations) ; consommateurs : refactoring-engineering "
          "(pré-vol/post-vol obligatoires), tout élément (agents, disciplines, scripts) ; bras mécanique : "
          "scripts/refactoring-test-graph.py | Skill `refactoring-test` (outil de la matérialisation n°55 — "
          "non discipline, Task 8 ; déclenchement automatique — registre ci-dessous) |")

AE_ROW = ("| **Agent engineering** (n°56) | Orchestration cohérente, optimisée et fonctionnelle — et autonome — des tâches "
          "des trois domaines : **Agent-Based Engineering** (agents comme blocs de construction — méthodologies "
          "ABSE/Tropos), **Agent Engineering** (processus itératif de transformation de LLMs en systèmes fiables — "
          "la fiabilité est le premier frein, LangChain 2026) et **Multi-Agent Systems Engineering** "
          "(conception/évaluation de systèmes multi-agents : patterns documentés, coordination, gardes anti-flotte, "
          "traçabilité par agent). Discipline ENGBLANTE : CADRE/ROUTE/OUTILLE/VEILLE — ne détient la méthode d'aucun "
          "détenteur (zéro duplication — règle §6.3). Ancrage 2026 : State of Agent Engineering (LangChain), "
          "Building Effective Agents (Anthropic 12/2024), multi-agent research system (Anthropic 06/2025), "
          "Don't Build Multi-Agents (Cognition 2025), Patterns and problems in emerging multiagent systems "
          "(Anthropic 08/2026). | gen-plan §1.6/§3 (mobilisation v3.42.0) ; agent-engineering SKILL.md §1 (mission + "
          "table 3 domaines + routage 8 détenteurs + cycle 6 étapes) ; fondements : `references/fondements-academiques.md` "
          "| Skill `agent-engineering` (matérialisation n°56, déclenchement automatique — registre ci-dessous) |")

RG_ROW = ("| `refactor-guard` | **Skill de garde-fous de refactoring** (Task 8, fusion discussion externe 468a4c26 : "
          "lignée externe v1.7.0 déclarée — base hôte v1.2.0 portée, provenance R4) | Score de risque H01-H15, "
          "sandbox, échelle rollout — mobilisé par refactoring-engineering et gen-plan |")

AE_REG = ("| `agent-engineering` | **Matérialisation skill de la discipline n°56** (Task 83, 2026-11-09 : SKILL.md + "
          "fondements + evals ; inscription socle §7 + gen-plan §1.6/§3 : Task 84 — pendance P1 éteinte ; détention "
          "orchestrée : registre décentralisé §8 du skill + registre KB) | Cadrage/routage/outillage/veille des tâches "
          "ABE/AE/MASE — application dédiée (orchestration autonome des 3 domaines) — orchestration gen-plan §1.6 |")

# ------------------------------------------------------------------ gen-plan
S16_ANCHOR = ("| **Refactoring test** | Outil n°55 (anti-auto-certification) : évaluation + blast radius, "
              "verdict OK/PRESSION/CRITIQUE |")
S16_ROW = ("| **Agent engineering** | Discipline n°56 : cadrage/routage/outillage/veille des tâches d'agents "
           "(ABE/AE/MASE) — (SHARED §7, registre §8 du skill) |")

S3_ANCHOR = ("| refactoring-test | Outil n°55 (SHARED §7, bloc PATTERN:GEN-PLAN-REFACTORING-v1.0.0) | "
             "Détection/évaluation + graphe d'interactions (blast radius) — verdict machine, version >= v1.0.1 |")
S3_ROW = ("| agent-engineering | Mobilisation n°56 (SHARED §7, registre décentralisé §8 du skill) | "
          "Cadrage/routage des tâches d'agents (ABE/AE/MASE) — version >= v1.0.0 |")

ENTREE_V3420 = (
    "- **v3.42.0 (2026-11-09, web-ecef7f80 — Task 84 G3, directive 1a1bed51ccaf78f1 « continue »)** : "
    "INSCRIPTION SOCLE n°56 — agent-engineering (ABE/AE/MASE, créée Task 83, pendance P1) inscrite : "
    "SHARED §7 (définition + registre, v1.7.37) + §1.6 + §3. MINOR, description/§A inchangés. "
    "Cascade KO-L004 : PM v3.42.0, SHARED v1.7.37, PM-INSTALL v1.9.14."
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
    shared = SHARED.read_text(encoding="utf-8")

    if "version: 3.42.0" in skill and "**Agent engineering** (n°56)" in shared:
        print("[NO-OP] socle n°56 déjà inscrit (v3.42.0 + SHARED §7 — idempotence)")
        return 0

    # --- 1. capture de l'entrée §5.6 v3.41.0 (migration R4) AVANT remplacement
    m = re.findall(r"^- \*\*v3\.41\.0 \([^\n]*$", skill, re.M)
    if len(m) != 1:
        print("ABANDON : entrée §5.6 v3.41.0 trouvée %d fois (attendu 1)" % len(m))
        return 2
    entree_v3410 = m[0]

    # --- 2. SHARED §7 (en mémoire)
    s = shared
    s = sub(s, RT_ROW, RT_ROW + "\n" + AE_ROW, "§7 table ligne n°56 (après Refactoring test)")
    s = sub(s, RG_ROW, RG_ROW + "\n" + AE_REG, "§7 registre ligne agent-engineering (après refactor-guard)")

    # --- 3. gen-plan SKILL.md v3.42.0 (en mémoire)
    t = skill
    t = sub(t, "version: 3.41.0", "version: 3.42.0", "version frontmatter")
    t = sub(t, S16_ANCHOR, S16_ANCHOR + "\n" + S16_ROW, "§1.6 ligne Agent engineering")
    t = sub(t, S3_ANCHOR, S3_ANCHOR + "\n" + S3_ROW, "§3 Relations ligne agent-engineering")
    t = sub(t, entree_v3410, ENTREE_V3420, "§5.6 entrée courante v3.42.0")

    taille_avant = len(skill.encode("utf-8"))
    taille_apres = len(t.encode("utf-8"))
    print("SKILL.md : %d → %d octets (delta %+d, budget %d)" % (
        taille_avant, taille_apres, taille_apres - taille_avant, BUDGET))
    if taille_apres > BUDGET:
        print("ABANDON : budget < 30 Kio dépassé de %d octets" % (taille_apres - BUDGET))
        return 2

    # --- 4. journal-versions.md : insertion v3.41.0 migrée (en mémoire)
    journal = JOURNAL.read_text(encoding="utf-8")
    if entree_v3410.split("(")[0] + "(2026-11-08" in journal:
        print("ABANDON : journal-versions.md contient déjà l'entrée v3.41.0 migrée")
        return 2
    journal_new = sub(journal, NOTE_MIGRATION, NOTE_MIGRATION + "\n\n" + entree_v3410,
                      "journal-versions insertion v3.41.0")

    # --- 5. écritures (tout validé — aucune écriture partielle)
    SHARED.write_text(s, encoding="utf-8")
    SKILL.write_text(t, encoding="utf-8")
    JOURNAL.write_text(journal_new, encoding="utf-8")
    print("Écrit : SHARED §7 (+2 lignes n°56) · SKILL.md v3.42.0 (%d o) · journal-versions.md (+ v3.41.0 migrée)"
          % taille_apres)
    return 0


if __name__ == "__main__":
    sys.exit(main())
