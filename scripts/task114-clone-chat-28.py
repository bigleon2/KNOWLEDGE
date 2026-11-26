#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 114 — clone-chat : archivage de session (28ᵉ de la lignée).

Fenêtre du tour : bootstrap INSTALLE-RÉPARÉ (réinjection) · réparation 13+4 sous
garde R4 · audit 73/73 + 4/4 · dérive langue corrigée + rappel permanent · script
routage-skills-agents.py v1.0.0 · gen-plan v3.47.0 (É5-ROUTAGE + §1.17) · garde
réinjection ensure-installed.py · cascade KO-L004 complète · certification ALL PASS
6/6 · analyse + tests F+P 32/32 + CW --bloc PASS 5/5 · plan E13d/D015 · PUSH (clé
du tour, KO-L009).

Protocole clone-chat v2.0.2 (7+1 étapes) : scellage 8 checks S1-S8, 0 secret.
Codes retour : 0 = succès, 1 = échec.
"""
# ⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.46)
# SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
# Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
# Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
# Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
# Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
# Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).

import re
import sys
from datetime import datetime, timezone
from pathlib import Path

RACINE = Path("/home/z/my-project")
REPO = RACINE / "KNOWLEDGE-repo"
NOM = "clone-chat-session-web-f492e049-20261122-task114-routage.md"
CLONE_HOTE = RACINE / "download" / NOM
CLONE_DEPOT = REPO / "download" / NOM
WORKLOG_HOTE = RACINE / "worklog.md"
WORKLOG_DEPOT = REPO / "worklog.md"


def h():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


CONTENU = f"""# Clone de discussion — session web-f492e049 (Task 114 : routage décisionnel + rappel langue), 28ᵉ de la lignée

> Session : web-f492e049 · chat 17b8e0d9-d141-4dda-b86b-8b152e773f70 · canal zai-web · traces directives 1a2025197d2a0e9d + 1a2025ce4a6ed095. Généré le {h()} par clone-chat v2.0.2 (7+1 étapes). Fenêtre du clone : automatisation des appels skills/agents via gen-plan (déclencheurs intégrés en corps + forcés + script décisionnel pour les agents complexes) et correction de la dérive de langue (chinois → rappel permanent français dans gen-plan). Chaîne G1-G14 du plan-2026-11-21 préalablement close (worklog suites 155-160), Task 114 exécutée en E13d (D015).

## §0 — Contexte Système (SHARED v1.7.45)

> Écosystème Knowledge : skills/ = racine (73 SKILL.md + 4 .agent) | KB = skills/KNOWLEDGE.md | @mon-ecosysteme/ (corpus) | @historique/ (archive R4). Conventions kebab-case/semver/#token. Règle d'or n°6 : FRANÇAIS exclusif dès le premier mot — rappel permanent §0 gen-plan v3.47.0 (dérive chinois corrigée). Référence canonique : « mon skill X » = forme installée skills/X/SKILL.md. État certification : ALL PASS 6/6 (verify-cross 168/168 · correct-work 16/16 · integrity 116/116 · interactions PASS STRICT 59/59 · tool-routing 7/7) · audit 73/73 skills + 4/4 agents CONFORMES · gen-plan v3.47.0 · correct-work v2.12.1 · clone-chat v2.0.2 · SHARED v1.7.45 · pin ECO_SKILLS ×2 arbres.

## §1 — Worklog chronologique (fenêtre du clone : suite 162)

| Suite | Date | Contenu (résumé exécutable) |
|---|---|---|
| 162 | 2026-11-22 | T1 état : récidive réinjection plateforme (17 SKILL.md écrasés + 4 majuscules recréés) → bootstrap INSTALLE-RÉPARÉ + réparation Task 114 (13+4, garde archive R4 byte-identité, idempotence ×2) + audit 73/73 + 4/4 · T2 dérive langue chinois → correction immédiate + worklog + durcissement · T3 routage-skills-agents.py v1.0.0 (selftest 9/9 ×2, 44 ms, porte agents) · T4 gen-plan v3.46.0→v3.47.0 (§0 RAPPEL PERMANENT LANGUE + É5-ROUTAGE + §1.17, 10 patchs verrouillés) + ensure-installed.py garde réinjection (testé INSTALLE-RÉPARÉ → INSTALLE ×2) · T5 cascade KO-L004 complète (PM v3.47.0 + dédup R4 + KB + pin ×2 + evals + 9 citations vives + propagation §0 v1.7.45 ×2 + rescellement ×2) → certification ALL PASS 6/6 · T6 livrables : analyse (139,1 Kio rejeté → OPTIMISE) + tests F+P 32/32 + CW --bloc PASS 5/5 + plan E13d/D015 (P1-P5 PASS) + PUSH (clé du tour) |

## §2 — Artefacts de la fenêtre (Étape 2)

| Artefact | Rôle | État |
|---|---|---|
| skills/gen-plan/scripts/routage-skills-agents.py | Script décisionnel É5-ROUTAGE (scores frontmatters installés — source unique R4, porte agents COMPLEXE >= 2/5) | CERTIFIÉ ×2 arbres |
| skills/gen-plan/scripts/ensure-installed.py | Garde réinjection plateforme (signature native, réparation miroir, stale majuscules sous garde R4) | CERTIFIÉ ×2 arbres |
| skills/gen-plan/SKILL.md | gen-plan v3.47.0 (§0 rappel langue + §1.16 É5-ROUTAGE + §1.17 + §2.2 + §3 + §4 + journal) | INSTALLED ×2 arbres |
| skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.47.0.md | PM généré mécaniquement (delta verrouillé scripts/delta-genplan-v3470.json) | SCELLÉ |
| download/analyse-routage-decisionnel-task114.md | Analyse mesurée (options A/B/C, verdict OPTIMISE, extension autres éléments) | SCELLÉ |
| download/rapport-task114-tests-fp.json | Tests F+P 32/32 PASS | SCELLÉ |
| download/rapport-cw-task114-projet.md | CW --bloc Task 114 PASS 5/5 | SCELLÉ |
| download/rapport-task114-reparation-reinjection.json | Réparation réinjection 13+4 | SCELLÉ |
| download/rapport-audit-conformite-task113.json | Audit 73/73 skills + 4/4 agents CONFORMES | SCELLÉ |
| download/plan-2026-11-21-optimisation-ecosysteme.md | Plan étendu E13d/D015 (P1-P5 PASS) | SCELLÉ |
| scripts/t114-genplan-v3470.py · scripts/task114-tests-fp.py · scripts/task114-reparation-reinjection.py | Cascade + tests + réparation | CERTIFIÉS |

## §3 — Décisions et leçons de la fenêtre (Étape 3)

| ID | Décision / leçon | Portée |
|---|---|---|
| Option C — routage mécanique | Incruster le catalogue complet des déclencheurs DÉGRADE (139,1 Kio = 2,3× seuil CRITIQUE 60 Kio + violation R4 + cascade KO-L004 ×73 skills) ; routage à l'exécution OPTIMISE (+3,99 Kio une fois, 44 ms/plan, ~300 #token, source unique) | Task 114 |
| Rappel permanent langue | Dérive chinois constatée → correction immédiate + worklog + durcissement : §0 gen-plan rappelle le FRANÇAIS exclusif à CHAQUE exécution (directive 1a2025ce4a6ed095) | Task 114 |
| Garde réinjection durable | La plateforme réinjecte ses skills natifs entre-tours (9ᵉ récidive environnement) → ensure-installed.py étendu : détection signature native (clawdbot/absence §0), réparation miroir, suppression majuscules SOUS garde archive R4 byte-identité (jamais détruire sans preuve) | Task 114 |
| KO-L003 (×2) | F6 : champ volatile duree_ms = métadonnée de mesure, idempotence testée sémantiquement · F2 : propagation §0 = étape de cascade (dépôt PUIS hôte puis rescellement) — arbitres corrigés, réalité inchangée | Task 114 |
| Extension décisionnelle | Système pertinent UNIQUEMENT pour les orchestrateurs : gen-plan modifié, orchestrateur-tsi inchangé (routage de domaine propre — preuve score 13 au test), 4 agents = cibles du routage | Task 114 |

## §4 — État des pendances (Étape 4)

| Pendance | État |
|---|---|
| PUSH des commits du tour (clé du tour — KO-L009 mémoire de commande, sortie masquée) | Exécutée en fin de fenêtre |
| RÉVOCATION PATs antérieurs (Task 107 + Task 112 + tour précédent) | CONSERVÉE — action propriétaire UNIQUE [CRITIQUE] |
| Révocation du PAT fourni après usage | CONSERVÉE — rappel propriétaire [CRITIQUE] |
| Décision cron 531684 (0 job — vérification récurrente) | CONSERVÉE — escalade propriétaire |

## §5 — Lignage et scellage (Étape 5)

Lignée : … → Task 112 (24ᵉ) → Task 113 audit conformité (26ᵉ) → Task 113 SUITE plateforme (27ᵉ) → **Task 114 routage décisionnel (28ᵉ)**. Session web-f492e049, fenêtre suite 162.

Drifts typés de la fenêtre : MODIFICATION gen-plan v3.46.0→v3.47.0 ×2 arbres · CREATION routage-skills-agents.py v1.0.0 ×2 arbres · MODIFICATION ensure-installed.py (garde réinjection) ×2 arbres · CREATION PM v3.47.0 + delta verrouillé · RENOMMAGE R4 PM v3.46.0 → @historique · MODIFICATION KB + pin ×2 + evals + 9 citations vives + propagation §0 ×2 arbres · RESCELLEMENT archive v2.5 ×2 arbres · CREATION livrables download/ ×5 + scripts Task 114 ×3 + clone 28ᵉ.
"""

def sceller() -> list:
    """8 checks S1-S8 (protocole clone-chat v2.0.2)."""
    texte = CLONE_HOTE.read_text(encoding="utf-8")
    checks = [
        ("S1_sections_0_a_5", all(f"## §{i}" in texte for i in range(6))),
        ("S2_worklog_table", "| 162 | 2026-11-22 |" in texte),
        ("S3_artefacts_table", "| Artefact | Rôle | État |" in texte),
        ("S4_decisions_table", "| ID | Décision / leçon | Portée |" in texte),
        ("S5_pendances_table", "| Pendance | État |" in texte),
        ("S6_lignage_28e", "28ᵉ de la lignée" in texte),
        ("S7_pas_de_secret", not re.search(r"github_pat_[A-Za-z0-9_]{20,}", texte)),
        ("S8_horodatage", "2026-11-22" in texte),
    ]
    return checks


def main() -> int:
    CLONE_HOTE.write_text(CONTENU, encoding="utf-8")
    CLONE_DEPOT.parent.mkdir(parents=True, exist_ok=True)
    CLONE_DEPOT.write_text(CONTENU, encoding="utf-8")
    # parité worklog hôte→dépôt (R5)
    WORKLOG_DEPOT.write_text(WORKLOG_HOTE.read_text(encoding="utf-8"), encoding="utf-8")
    checks = sceller()
    ok = all(r for _, r in checks)
    for nom, res in checks:
        print(("PASS" if res else "FAIL") + " " + nom)
    print(f"SCELLAGE {sum(1 for _, r in checks if r)}/{len(checks)} — clone 28ᵉ :",
          CLONE_HOTE)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
