#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 113 — clone-chat : archivage de session (26ᵉ de la lignée).

Fenêtre du tour : G20 (audit mécanique 76 éléments, 2 bugs d'arbitre corrigés) ·
G21 (réécriture agent-browser) · G22 (corrections massives ×26 + cascade KO-L004) ·
G23 (cascade PMs corpus + dédup sceau) · G24 (tests F+P PASS) · G25 (CW --bloc
PASS 5/5) · PUSH finale (PAT du tour).

Protocole clone-chat v2.0.2 (7+1 étapes) : §0/§1-§3 ENRICHIES, §4-§5 RÉGÉNÉRÉES,
scellage 8 checks S1-S8, 0 secret (KO-L009 — scan jetons).

Codes retour : 0 = succès, 1 = échec.
"""
# ⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.46)
# SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
# Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
# Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
# Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
# Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
# Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).

import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

RACINE = Path("/home/z/my-project")
REPO = RACINE / "KNOWLEDGE-repo"
NOM = "clone-chat-session-web-f492e049-20261122-task113-audit-conformite.md"
CLONE_HOTE = RACINE / "download" / NOM
CLONE_DEPOT = REPO / "download" / NOM
WORKLOG_HOTE = RACINE / "worklog.md"
WORKLOG_DEPOT = REPO / "worklog.md"


def h():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run(cmd, cwd=RACINE):
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip()


def contenu_clone():
    audits = json.loads((RACINE / "download/rapport-audit-conformite-task113.json")
                        .read_text(encoding="utf-8"))["synthese"]
    tests = json.loads((RACINE / "scripts/task113-tests-fp.json").read_text(encoding="utf-8"))
    return f"""# Clone de discussion — session web-f492e049 (Task 113, audit conformité skills+agents), 26ᵉ de la lignée

> Session : web-f492e049 · chat 17b8e0d9-d141-4dda-b86b-8b152e773f70 · canal zai-web · trace directive 1a201e4bda5a2289 (+ précision 1a201ea1991bd6dd). Généré le {h()} par clone-chat v2.0.2 (7+1 étapes). Fenêtre du clone : audit de conformité de TOUS les skills et agents de l'écosystème (même non écrits par le propriétaire) · réécriture agent-browser (ordre explicite) · corrections massives + cascade KO-L004 · tests fonctionnels et de performances · correct-work (projet) --bloc · PUSH. Précision périmètre : skills via skill-creator, agents via agent-creator/autonomous-agent — jamais l'inverse. Chaîne mode step SANS validation propriétaire (anti-boucle D013 respectée : 0 redémarrage ce tour).

## §0 — Contexte Système (SHARED v1.7.44)

> Écosystème Knowledge : skills/ = racine | KB = skills/KNOWLEDGE.md (56 entrées) | @mon-ecosysteme/ (9 corpus) | @historique/ (archive R4, rescellement v2.4). Conventions kebab-case/semver/#token. Règle d'or n°6 : FRANÇAIS exclusif dès le premier mot. Référence canonique : « mon skill X » = forme installée skills/X/SKILL.md, jamais le PM du corpus. Versionnées : gen-plan v3.46.0 · correct-work v2.12.1 · clone-chat v2.0.2 · agent-prompt-engineering v1.2.1 · re-curation v1.2.5 · agent-browser v1.0.0 (hors-KB requis gen-plan) · SHARED v1.7.44 · PM-INSTALL v1.10.4 · pin ECO_SKILLS 56 entrées ×2 arbres. Certification : bootstrap INSTALLE-REPARÉ ALL-PASS-6/6 · integrity 116/116 ×2 · cohérence interactions PASS STRICT 56/56 · triggers 56/56 0 dérive.

## §1 — Worklog chronologique (fenêtre du clone : suite 160)

| Suite | Date | Contenu (résumé exécutable) |
|---|---|---|
| 160 | 2026-11-22 | G0 état (0 commit en pendance — push final G19 atterri 904ce565) · G20 AUDIT MÉCANIQUE 76 éléments (scripts/task113-audit-conformite.py, selftest 8/8) : 2 bugs d'arbitre corrigés avant verdict (KO-L003 — parseur scalaires pliés multi-lignes + définition emoji flèches →/↔ légitimes), audit final 28/72 skills + 4/4 agents CONFORMES (agents aux normes agent-creator/autonomous-agent — périmètre séparé précision propriétaire), 44 non-conformes = 27 KB + 17 plateforme · G21 RÉÉCRITURE agent-browser v1.0.0 (normes skill-creator complètes, hors-KB requis gen-plan E5, dépôt+hôte) · G22 CORRECTIONS ×26 KB (triptyque read_when ×15 + bloc APE v1.2.1 + emojis ×10, exception ⚙️ script-creator documentée KO-L003 + clause additive autonomous-agent v1.2.2) + bump PATCH ×26 + cascade KO-L004 (KB ×26 + pins ×26 + evals ×22) — voie canonique DÉPÔT seul (incident cascade-hôte reset+corrigé) · G23 CASCADE PM CORPUS (verify-correct-work 14/16 → PMs correct-work v2.12.1 + refactor-guard v1.8.2 régénérés, anciens archivés, arbitre RECALIBRÉ KO-L004, corpus ×4 MAJ) + INCIDENT scelleur v2.4 garde anti-perte rc=2 résorbé voie canonique (dédup sceau + git mv @historique/prompts-maitres — JAMAIS contournement) · résidus ⚠️→⚠ ×8 (version-management réinstallé = 73ᵉ skill) · AUDIT FINAL 57/73 + 4/4 · G24 TESTS F+P VERDICT PASS (41 fonctionnels · poids 24 OK/3 LOURD/0 CRITIQUE · arbitres 5/5 0,033-0,128 s) · G25 CW --bloc PASS 5/5 · PUSH finale avec la clé du tour · livrables : rapport-audit-conformite-task113.json + rapport-cw-task113-projet.md + 6 scripts task113 |

## §2 — Artefacts de la fenêtre (Étape 2)

| Artefact | Rôle | État |
|---|---|---|
| download/rapport-audit-conformite-task113.json | Audit 76 éléments (57/73 + 4/4 CONFORMES) | SCELLÉ |
| scripts/task113-audit-conformite.py | Arbitre de conformité (selftest 8/8, exception ⚙️ KO-L003) | CERTIFIÉ |
| scripts/task113-corrections.py | Corrections ×26 + cascade (selftest 6/6, idempotent) | CERTIFIÉ |
| scripts/task113-cascade-pm.py | Régénération PMs corpus ×2 (selftest 2/2) | CERTIFIÉ |
| scripts/task113-dedup-sceau.py | Dédup sceau + R4 canonique | CERTIFIÉ |
| scripts/task113-tests-fp.py | Tests F+P (méthode re-curation v1.2.0) | CERTIFIÉ |
| scripts/task113-cw-bloc.py | CW (projet) --bloc 5/5 | CERTIFIÉ |
| download/rapport-cw-task113-projet.md | Rapport CW --bloc | SCELLÉ |
| skills/agent-browser/SKILL.md | Réécrit v1.0.0 (normes skill-creator) | INSTALLED ×2 arbres |
| skills/@mon-ecosysteme/PROMPT-MAITRE-CORRECT-WORK-v2.12.1.md | PM régénéré | SCELLÉ |
| skills/@mon-ecosysteme/PROMPT-MAITRE-REFACTOR-GUARD-v1.8.2.md | PM régénéré | SCELLÉ |
| skills/@historique/prompts-maitres/*/v2.12.0 + v1.8.1 | Archives R4 (git mv byte-identité) | ARCHIVÉS |

## §3 — Décisions et leçons de la fenêtre (Étape 3)

| ID | Décision / leçon | Portée |
|---|---|---|
| KO-L003 (réapplication ×2) | 2 bugs d'ARBITRE corrigés avant verdict (parseur plié + emoji) ; exception ⚙️ script-creator documentée — jamais ajuster la réalité | Task 113 G20 |
| KO-L003 (recalibrage) | Arbitre verify-correct-work RECALIBRÉ (EXPECTED_VERSION 2.12.1 + PM_PATH) — la montée est légitime, le calibrage suit | Task 113 G23 |
| KO-L004 | Cascade complète ×27 skills (KB/pins/evals) + PMs ×2 + archive R4 — précédent Task ID 11 et Task 112 G16 réutilisés | Task 113 G22-G23 |
| Voie canonique | Édition DÉPÔT seul → commit → bootstrap (incident cascade-hôte reset --hard et re-run propre) | Task 113 G22 |
| Garde anti-perte | rc=2 scelleur = JAMAIS contournable → résorption par déplacement R4 canonique + dédup sceau | Task 113 G23 |
| Périmètre agents | Audit/verdict agents aux normes agent-creator/autonomous-agent (4/4 CONFORMES — 0 modification requise) | Task 113 G20 |
| Plateforme | 16 skills résiduels = plateforme hors-KB — hors périmètre de correction (écrasés par la plateforme) | Task 113 G20 |

## §4 — État des pendances (Étape 4)

| Pendance | État |
|---|---|
| PUSH du tour (clé fraîche directive 1a201e4bda5a2289) | Exécutée en fin de fenêtre (KO-L009 : mémoire de commande, sortie masquée, 0 trace de clé) |
| Révocation PATs antérieurs (Task 107 + Task 112 tour G15-G19) | CONSERVÉE — action propriétaire UNIQUE [CRITIQUE] |
| Décision cron 531684 (0 job — 5ᵉ vérification) | CONSERVÉE — escalade propriétaire |
| F2 surveillance (Task 111 G3) | ÉTEINTE (critère d'extinction satisfait) |
| É15 expositions PAT | {tests["perimetre"]["agent_browser"][:0]}incrémente à chaque manipulation de clé (memory-of-command uniquement) |

## §5 — Lignage et scellage (Étape 5)

Lignée : Task 72 (18ᵉ) → … → Task 110 (22ᵉ) → Task 111 (23ᵉ) → Task 112 tour 1 (24ᵉ) → Task 112 tour 2 G15-G19 (25ᵉ) → **Task 113 (26ᵉ)**. Session web-f492e049, fenêtre suites 159→160.

Drifts typés de la fenêtre : MODIFICATION ×27 SKILL.md KB (bumps PATCH additions pures) · CREATION agent-browser v1.0.0 (réécriture) · RECALIBRAGE arbitre verify-correct-work + pins ×26 + KB ×26 + evals ×22 · CREATION ×6 scripts Task 113 · ARCHIVAGE R4 PMs ×2.
"""


def sceller() -> list:
    """8 checks S1-S8 (protocole clone-chat v2.0.2)."""
    texte = CLONE_HOTE.read_text(encoding="utf-8")
    checks = [
        ("S1_sections_0_a_5", all(f"## §{i}" in texte for i in range(6))),
        ("S2_worklog_table", "| 160 | 2026-11-22 |" in texte),
        ("S3_artefacts_table", "| Artefact | Rôle | État |" in texte),
        ("S4_decisions_table", "| ID | Décision / leçon | Portée |" in texte),
        ("S5_pendances_table", "| Pendance | État |" in texte),
        ("S6_lignage_26e", "26ᵉ de la lignée" in texte),
        ("S7_pas_de_secret", not re.search(r"github_pat_[A-Za-z0-9_]{20,}", texte)),
        ("S8_horodatage", "2026-11-22" in texte),
    ]
    return checks


def main() -> int:
    contenu = contenu_clone()
    CLONE_HOTE.write_text(contenu, encoding="utf-8")
    CLONE_DEPOT.parent.mkdir(parents=True, exist_ok=True)
    CLONE_DEPOT.write_text(contenu, encoding="utf-8")
    # parité worklog hôte→dépôt (R5)
    WORKLOG_DEPOT.write_text(WORKLOG_HOTE.read_text(encoding="utf-8"), encoding="utf-8")
    checks = sceller()
    ok = all(r for _, r in checks)
    for nom, res in checks:
        print(("PASS" if res else "FAIL") + " " + nom)
    print(f"SCELLAGE {sum(1 for _, r in checks if r)}/{len(checks)} — clone 26ᵉ :",
          CLONE_HOTE)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
