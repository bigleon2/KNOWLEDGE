#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.47)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).
Référence canonique : « mon skill X » = forme installée skills/X/, JAMAIS le PM.
"""

"""Task 114 — gen-plan v3.46.0 → v3.47.0 : É5-ROUTAGE + porte d'agents + rappel
permanent langue (trace 1a2025197d2a0e9d + 1a2025ce4a6ed095, mode t112-g16).

Directive propriétaire 1a2025197d2a0e9d : « intégrer les déclencheurs des skills et des
agents dans le corps de gen-plan ; forcer gen-plan à utiliser ses déclencheurs ; si
l'utilisation des agents n'est justifiée que dans des cas complexes, intégrer un script
qui orchestrera cette prise de décision ».
Directive propriétaire 1a2025ce4a6ed095 : « corrige la dérive de langue (chinois) et
intègre cette règle directement dans le corps de gen-plan pour te la rappeler à chaque
exécution ».

CORRECTIF (MINOR additions pures, non-régression triggers) :
 1. §0 += RAPPEL PERMANENT — LANGUE DU DIALOGUE (français exclusif à chaque exécution)
 2. §1.16 += hook É5-ROUTAGE (script routage-skills-agents.py — scores depuis les
    frontmatters installés [source unique R4] + verdict complexité 5 critères + porte
    agents COMPLEXE >= 2/5)
 3. §1.17 (nouvelle) = Décision d'agents — porte de complexité + matrice DYNAMIQUE R4
 4. §2.2 += routage-skills-agents.py (structure du skill)
 5. §3 += ligne agents écosystème (délégation porte-gardée)
 6. §4 += coût routage (~300 #token/plan — économie nette vs incrustation catalogue)
 7. §5.6 entrée v3.47.0 (v3.46.0 migrée R4 byte-identité references/journal-versions.md)
 8. description frontmatter += clauses (routage + rappel langue)
 9. ensure-installed.py (companion Task 114) : garde réinjection plateforme — déployé
    séparément (déjà en place ×2 arbres, testé INSTALLE-REPARÉ → INSTALLE idempotent)

Cascade KO-L004 COMPLÈTE : delta verrouillé scripts/delta-genplan-v3470.json + PM
v3.47.0 généré mécaniquement (generer-pm-skill.py) + PM v3.46.0 dédup @historique R4 +
KB (titre + Description + Dernière calibration) + pin ECO_SKILLS 3.47.0 ×2 arbres +
evals sync →3.47.0 + historiques-par-skill append + worklog. Commit AVANT bootstrap
(règle d'or n°4) exécuté par la chaîne appelante.

Codes retour : 0 = PASS, 1 = échec (garde anti-boucle D013 : au plus 1 redémarrage).
"""
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

RACINE = Path("/home/z/my-project")
REPO = RACINE / "KNOWLEDGE-repo"
P_SKILL = REPO / "skills/gen-plan/SKILL.md"
P_JOURNAL = REPO / "skills/gen-plan/references/journal-versions.md"
P_DELTA = REPO / "scripts/delta-genplan-v3470.json"
P_KB = REPO / "skills/KNOWLEDGE.md"
P_EVALS = REPO / "skills/gen-plan/evals/evals.json"
P_PIN_REPO = REPO / "scripts/check-ecosysteme-integrity.py"
P_PIN_HOTE = RACINE / "scripts/check-ecosysteme-integrity.py"
P_HISTO = REPO / "skills/@historique/historiques-par-skill/gen-plan.md"
PM_346 = REPO / "skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.46.0.md"
PM_347 = REPO / "skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.47.0.md"
ARCHIVE_PM = REPO / "skills/@historique/prompts-maitres/gen-plan"
WORKLOG = RACINE / "worklog.md"
TRACE_A = "1a2025197d2a0e9d"
TRACE_B = "1a2025ce4a6ed095"

RAPPEL_LANGUE = (
    "**RAPPEL PERMANENT — LANGUE DU DIALOGUE (règle d'or n°6 durcie, v3.47.0 — "
    "directive propriétaire trace " + TRACE_B + ", rappel à CHAQUE exécution de "
    "gen-plan, AVANT tout autre rappel)** : le dialogue avec le propriétaire est en "
    "FRANÇAIS exclusif — JAMAIS de chinois, jamais d'anglais, dès le PREMIER mot de "
    "tout message, TODO/fenêtre de tâches, résumé de continuation ou livrable ; toute "
    "dérive constatée (langue du tour précédent ou en cours) est CORRIGÉE IMMÉDIATEMENT "
    "dans le même message et journalisée au worklog (correction + worklog + "
    "durcissement) ; artefacts techniques verbatim exceptés (code, CLI, identifiants "
    "d'API — règle d'or n°6)."
)

HOOK_116 = (
    "- **É5-ROUTAGE — décision mécanique de routage skills + agents (v3.47.0, "
    "Task 114 — directive trace " + TRACE_A + ")** : à E5 (sélection des skills) et à "
    "E7 (écriture du plan — section « Routage »), exécuter "
    "`python3 skills/gen-plan/scripts/routage-skills-agents.py --tache \"<demande "
    "normalisée>\" --format json` : le script lit les frontmatters INSTALLÉS "
    "(description + read_when — source unique, zéro duplication R4, zéro lag KO-L004) "
    "et rend une recommandation compacte (skills scorés + verdict de complexité "
    "5 critères) ; les skills recommandés alimentent la sélection E5 (croisement avec "
    "le registre KB et l'arbitre poids-chargement) ; les AGENTS ne sont recommandés "
    "QUE si le verdict est COMPLEXE (>= 2/5 critères — porte-garde §1.17) ; sortie "
    "consignée download/routage-dernier.json ; idempotent, < 1 s."
)

SEC_117 = (
    "### §1.17 Décision d'agents — porte de complexité et matrice dynamique "
    "(v3.47.0, Task 114)\n\n"
    "La délégation à un agent (sous-agent = contexte plein — coût #token élevé) est "
    "JUSTIFIÉE uniquement dans les cas complexes : verdict COMPLEXE du script de "
    "routage (>= 2/5 critères : multi_livrables, multi_domaines >= 3 skills, "
    "horizon_long, parallele, integration_externe — grille alignée sur le "
    "PROMPT-GATEWAY §1.6). En dessous du seuil : skills directs, aucun agent (motif "
    "journalisé par le script — portegardes_agents).\n\n"
    "| Agent | Cas justifiés (COMPLEXE requis) | Moteur de recommandation |\n"
    "|-------|----------------------------------|--------------------------|\n"
    "| agents écosystème (.agent installés) | Sous-tâches autonomes multi-phases d'un "
    "cas complexe — recommandation dérivée À L'EXÉCUTION du score objectif/modes des "
    ".agent | `routage-skills-agents.py` (matrice dynamique — R4, jamais de copie "
    "statique dans le corps) |\n\n"
    "> La matrice des agents est DYNAMIQUE (objectifs .agent lus à l'exécution — "
    "source unique) : gen-plan ne duplique JAMAIS les descriptions d'agents dans son "
    "corps (R4) ; le verdict COMPLEXE est la PORTE, le score du script est le MOTEUR, "
    "la décision finale reste à E5/E7 avec l'arbitre poids-chargement (budget "
    "#token)."
)

LIGNE_S3 = (
    "| agents écosystème (4 .agent) | Délégation porte-gardée (§1.17) | "
    "Recommandation dérivée à l'exécution par routage-skills-agents.py — verdict "
    "COMPLEXE >= 2/5 requis ; matrice dynamique R4 |"
)

LIGNE_S4 = (
    "- **Routage É5-ROUTAGE (v3.47.0)** : ~300 #token par plan (exécution script + "
    "intégration section Routage) — sortie JSON ~1-2 Kio, < 1 s ; économie nette : le "
    "catalogue des déclencheurs N'EST PAS incrusté dans le corps (R4 + poids gen-plan "
    "maîtré sous le seuil CRITIQUE 60 Kio)."
)

STRUCTURE_SCRIPTS = (
    "│   ├── ensure-installed.py           # É1-INSTALL — préemption (v3.35.2) + "
    "garde réinjection plateforme (Task 114)\n"
    "│   ├── routage-skills-agents.py      # É5-ROUTAGE — décision skills + agents "
    "(v3.47.0)\n"
    "│   └── check_plan_protocol.py        # Arbitre E7-DISP — P1-P5 (v3.27.0)"
)

JOURNAL_347 = (
    "- **v3.47.0 (2026-11-22, web-f492e049 — Task 114, directives " + TRACE_A + " "
    "« intégrer les déclencheurs des skills et des agents dans le corps de gen-plan + "
    "forcer leur usage + script de décision pour les agents complexes » et " + TRACE_B
    + " « rappel permanent langue française dans le corps »)** : **É5-ROUTAGE + porte "
    "d'agents + rappel permanent langue** — analyse Task 114 "
    "(download/analyse-routage-decisionnel-task114.md) : incruster le catalogue complet "
    "des déclencheurs DÉGRADERAIT chaque session (gen-plan +30-40 Kio → franchit le "
    "seuil CRITIQUE 60 Kio de l'arbitre poids-chargement) et violerait R4 (les "
    "déclencheurs vivent déjà dans les frontmatters installés — source unique) ; "
    "solution retenue : routage MÉCANIQUE à l'exécution — §1.16 += hook É5-ROUTAGE "
    "(routage-skills-agents.py : scores depuis les frontmatters installés, verdict "
    "complexité 5 critères, porte-garde agents, sortie download/routage-dernier.json) "
    "+ §1.17 (porte COMPLEXE >= 2/5 + matrice agents DYNAMIQUE R4) + §2.2 (script au "
    "structure) + §3 (ligne agents écosystème) + §4 (coût ~300 #token/plan) + §0 += "
    "RAPPEL PERMANENT LANGUE (français exclusif à chaque exécution — correction "
    "immédiate + worklog + durcissement ; dérive chinois constatée et corrigée "
    "Task 114) + ensure-installed.py += garde réinjection plateforme (Task 114 : "
    "réparation native→miroir + stale majuscules, archives R4 byte-identité ; testé "
    "INSTALLE-REPARÉ → INSTALLE idempotent). MINOR, additions pures (non-régression "
    "triggers). Cascade KO-L004 COMPLÈTE : PM v3.47.0 généré mécaniquement (delta "
    "verrouillé scripts/delta-genplan-v3470.json) + KB + @historique + pin ECO_SKILLS "
    "×2 arbres + evals sync →3.47.0 + v3.46.0 migrée R4 byte-identité "
    "references/journal-versions.md."
)

CLAUSES_DESC = (
    ",\n"
    "  routage décisionnel É5-ROUTAGE (v3.47.0) : script routage-skills-agents.py — "
    "recommandation de skills depuis les frontmatters installés (source unique R4) + "
    "verdict de complexité 5 critères + porte COMPLEXE >= 2/5 pour la délégation "
    "d'agents (§1.17),\n"
    "  rappel permanent langue française (règle d'or n°6 durcie — §0, v3.47.0)"
)


def h():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run(cmd, cwd=RACINE):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip()


def remplacer(txt, ancien, nouveau, label, mutations):
    n = txt.count(ancien)
    assert n == 1, f"ancre {label} : {n} occurrence(s) (attendu 1)"
    mutations.append(label)
    return txt.replace(ancien, nouveau, 1)


def patch_skill():
    txt = P_SKILL.read_text(encoding="utf-8")
    mut = []
    if "version: 3.47.0" in txt:
        return ["SKILL.md déjà v3.47.0"]
    txt = remplacer(txt, "version: 3.46.0", "version: 3.47.0", "frontmatter 3.47.0", mut)
    # description frontmatter
    txt = remplacer(
        txt,
        "pré-traitement PROMPT-GATEWAY : agent-prompt-engineering v1.2.0 invoqué en "
        "tête de chaîne (É1-PROMPT-GATEWAY §1.16, v3.46.0) — réécriture des demandes "
        "complexes AVANT l'analyse E1",
        "pré-traitement PROMPT-GATEWAY : agent-prompt-engineering v1.2.0 invoqué en "
        "tête de chaîne (É1-PROMPT-GATEWAY §1.16, v3.46.0) — réécriture des demandes "
        "complexes AVANT l'analyse E1" + CLAUSES_DESC,
        "description", mut)
    # §0 : rappel permanent après le bloc SHARED (dernière ligne du §0)
    txt = remplacer(
        txt,
        "les PMs sont des spécifications générées mécaniquement (KO-L004), les skills "
        "installés sont les formes exécutables.\n",
        "les PMs sont des spécifications générées mécaniquement (KO-L004), les skills "
        "installés sont les formes exécutables.\n\n" + RAPPEL_LANGUE + "\n",
        "§0 rappel permanent langue", mut)
    # §1.16 : hook É5-ROUTAGE après l'entrée É1-PROMPT-GATEWAY
    txt = remplacer(
        txt,
        "les demandes courtes/simples passent directement (phases C-D by-passées, "
        "passage journalisé).",
        "les demandes courtes/simples passent directement (phases C-D by-passées, "
        "passage journalisé).\n" + HOOK_116,
        "§1.16 hook É5-ROUTAGE", mut)
    # §1.17 après la ligne Routage (E5) de §1.16, avant ## §2
    txt = remplacer(
        txt,
        "contrôle `audit-provenance` AVANT adoption ; bascule unidirectionnelle.\n"
        "## §2 — Spécification technique",
        "contrôle `audit-provenance` AVANT adoption ; bascule unidirectionnelle.\n"
        + SEC_117 + "\n## §2 — Spécification technique",
        "§1.17 décision d'agents", mut)
    # §2.2 structure scripts
    txt = remplacer(
        txt,
        "│   ├── ensure-installed.py           # É1-INSTALL — préemption (v3.35.2)\n"
        "│   └── check_plan_protocol.py        # Arbitre E7-DISP — P1-P5 (v3.27.0)",
        STRUCTURE_SCRIPTS,
        "§2.2 structure", mut)
    # §3 ligne agents
    txt = remplacer(
        txt,
        "optimisation fine des prompts (SHARED "
        "§3.1) — version >= v1.2.0 |",
        "optimisation fine des prompts (SHARED "
        "§3.1) — version >= v1.2.0 |\n" + LIGNE_S3,
        "§3 ligne agents écosystème", mut)
    # §4 coût routage
    txt = remplacer(
        txt,
        "budget propre AVANT l'étape requérante, v3.28.2).",
        "budget propre AVANT l'étape requérante, v3.28.2).\n" + LIGNE_S4,
        "§4 coût routage", mut)
    # §5.6 : capturer l'entrée v3.46.0 (migration R4), écrire v3.47.0
    m = re.search(r"^- \*\*v3\.46\.0 .*$", txt, re.M)
    assert m, "entrée v3.46.0 introuvable au §5.6"
    ancienne = m.group(0)
    txt = txt.replace(ancienne, JOURNAL_347, 1)
    mut.append("§5.6 entrée v3.47.0")
    P_SKILL.write_text(txt, encoding="utf-8")
    j = P_JOURNAL.read_text(encoding="utf-8")
    if "v3.46.0 (2026-11-22" not in j:
        ancre = "\n- **v3.45.0 (2026-11-21"
        assert ancre in j, "ancre journal v3.45.0 introuvable"
        j = j.replace(ancre, "\n" + ancienne + "\n\n" + ancre.lstrip("\n"), 1)
        P_JOURNAL.write_text(j, encoding="utf-8")
        mut.append("journal R4 v3.46.0 migrée")
    return mut


def ecrire_delta():
    if P_DELTA.exists():
        return ["delta déjà présent"]
    history = (
        "É5-ROUTAGE + porte d'agents + rappel permanent langue (Task 114, directives "
        + TRACE_A + " et " + TRACE_B + ") : §0 += RAPPEL PERMANENT LANGUE (français "
        "exclusif à chaque exécution) + §1.16 += hook É5-ROUTAGE "
        "(routage-skills-agents.py — scores depuis les frontmatters installés, source "
        "unique R4, verdict complexité 5 critères, porte agents COMPLEXE >= 2/5) + "
        "§1.17 (porte + matrice agents dynamique) + §2.2 + §3 + §4 + description + "
        "ensure-installed.py garde réinjection plateforme. MINOR additions pures. "
        "Cascade KO-L004 : PM + delta + KB + pin ×2 + evals sync →3.47.0 + "
        "@historique R4."
    )
    P_DELTA.write_text(json.dumps({"history": history, "subs": []},
                                  ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return ["delta v3470 écrit"]


def generer_pm():
    mut = []
    if PM_347.exists():
        return ["PM v3.47.0 déjà présent"]
    rc, s = run(["python3", "scripts/generer-pm-skill.py", "--generate", "gen-plan",
                 "--delta", "scripts/delta-genplan-v3470.json"], cwd=REPO)
    if rc != 0 or not PM_347.exists():
        raise SystemExit(f"ÉCHEC génération PM : {s[-500:]}")
    mut.append("PM v3.47.0 généré (générateur — SHARED/PM-INSTALL recalibrés inclus)")
    if PM_346.exists() and ARCHIVE_PM.exists():
        shutil.move(str(PM_346), str(ARCHIVE_PM / PM_346.name))
        mut.append("PM v3.46.0 archivé @historique R4 (dédup N27)")
    return mut


def cascade_kb_pin_evals():
    mut = []
    kb = P_KB.read_text(encoding="utf-8")
    if "## gen-plan v3.46.0" in kb:
        kb = kb.replace("## gen-plan v3.46.0", "## gen-plan v3.47.0", 1)
        mut.append("KB titre v3.47.0")
    if "routage décisionnel É5-ROUTAGE" not in kb:
        kb = remplacer(
            kb,
            "pour réécrire les demandes complexes quand le PROMPT-GATEWAY n'a pas "
            "déjà traité le prompt)",
            "pour réécrire les demandes complexes quand le PROMPT-GATEWAY n'a pas "
            "déjà traité le prompt ; routage décisionnel É5-ROUTAGE (v3.47.0) : "
            "routage-skills-agents.py — recommandation skills depuis les frontmatters "
            "installés [source unique R4] + porte COMPLEXE >= 2/5 pour la délégation "
            "d'agents §1.17 + rappel permanent langue française §0)",
            "KB Description", mut)
    if "montée v3.47.0 (2026-11-22, Task 114" not in kb:
        kb = remplacer(
            kb,
            "- **Dernière calibration** : montée v3.46.0 (2026-11-22, Task 112 G16",
            "- **Dernière calibration** : montée v3.47.0 (2026-11-22, Task 114 — "
            "directives " + TRACE_A + " [intégration déclencheurs + script décision "
            "agents : §1.16 hook É5-ROUTAGE + §1.17 porte COMPLEXE >= 2/5 matrice "
            "dynamique R4 + §2.2/§3/§4 + description + ensure-installed.py garde "
            "réinjection plateforme] et " + TRACE_B + " [§0 rappel permanent langue "
            "française — dérive chinois corrigée, durcissement règle d'or n°6] ; "
            "MINOR additions pures non-régression triggers ; cascade KO-L004 "
            "COMPLÈTE : PM v3.47.0 généré mécaniquement [delta verrouillé "
            "scripts/delta-genplan-v3470.json], SHARED/PM-INSTALL recalibrés par le "
            "générateur, pin ECO_SKILLS 3.47.0 ×2 arbres, evals sync →3.47.0, PM "
            "v3.46.0 archivé @historique R4 [dédup N27], v3.46.0 migrée R4 "
            "byte-identité references/journal-versions.md, replay arbitres) ; "
            "précédente montée v3.46.0 (2026-11-22, Task 112 G16",
            "KB Dernière calibration", mut)
    P_KB.write_text(kb, encoding="utf-8")
    for p in (P_PIN_REPO, P_PIN_HOTE):
        if p.exists():
            t = p.read_text(encoding="utf-8")
            nouveau = t.replace('"gen-plan": "3.46.0"', '"gen-plan": "3.47.0"', 1)
            if nouveau != t:
                p.write_text(nouveau, encoding="utf-8")
                mut.append(f"pin {p.parent.parent.name}/scripts → 3.47.0")
    d = json.loads(P_EVALS.read_text(encoding="utf-8"))
    if d.get("version") != "3.47.0":
        anc = d.get("version")
        d["version"] = "3.47.0"
        P_EVALS.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
        mut.append(f"evals sync {anc}→3.47.0")
    hh = P_HISTO.read_text(encoding="utf-8")
    if "v3.46.0 archivé Task 114" not in hh:
        hh = hh.replace(
            ", v3.45.0 (49 fichiers",
            ", v3.45.0, v3.46.0 (50 fichiers", 1)
        hh = hh.replace(
            "v3.45.0 archivé Task 112 G16 [dédup N27 — montée v3.46.0]).",
            "v3.45.0 archivé Task 112 G16 [dédup N27 — montée v3.46.0] ; v3.46.0 "
            "archivé Task 114 [dédup N27 — montée v3.47.0]).", 1)
        P_HISTO.write_text(hh, encoding="utf-8")
        mut.append("historiques-par-skill append")
    return mut


def certifications():
    out = {}
    rc, s = run(["python3", "scripts/check-ecosysteme-integrity.py"], cwd=REPO)
    out["integrity_repo"] = (rc, s[-300:])
    rc, s = run(["python3", "scripts/check-triggers-replay.py"], cwd=RACINE)
    out["triggers_replay"] = (rc, s[-300:])
    rc, s = run(["python3", "scripts/verify-cross.py"], cwd=REPO)
    out["verify_cross"] = (rc, s[-300:])
    return out


def main():
    mutations = {}
    try:
        mutations["skill"] = patch_skill()
        mutations["delta"] = ecrire_delta()
        mutations["pm"] = generer_pm()
        mutations["cascade"] = cascade_kb_pin_evals()
    except AssertionError as exc:
        print("ÉCHEC garde ancre :", exc)
        return 1
    arbitres = certifications()
    mutations["arbitres"] = {k: f"rc={v[0]}" for k, v in arbitres.items()}
    with open(WORKLOG, "a", encoding="utf-8") as f:
        f.write(f"\n> Task 114 ({h()}) — gen-plan v3.46.0→v3.47.0 : É5-ROUTAGE + porte "
                "agents + rappel permanent langue + garde réinjection ensure-installed "
                "— mutations : " + " · ".join(f"{k}: {len(v) if isinstance(v, list) else v}"
                                               for k, v in mutations.items()) + "\n")
    print(json.dumps({"verdict": "PASS" if all(
        v[0] == 0 for v in arbitres.values()) else "ECHEC-ARBITRE",
        "mutations": mutations, "arbitres": {k: v[0] for k, v in arbitres.items()}},
        ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
