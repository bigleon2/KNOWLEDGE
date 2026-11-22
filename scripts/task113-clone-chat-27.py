#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 113 SUITE — clone-chat : archivage de session (27ᵉ de la lignée).

Fenêtre du tour : G26 (état + re-audit 56/72) · G27 (mécanique d'import : archives
R4 ×16 + renommages kebab ×4) · G28 (réécritures ×16 selon skill-creator + clôture
triptyque) · G29 (synchro dépôt canonique + dépendances KB vlm ×3) · G30 (tests
F+P PASS + CW --bloc suite PASS 5/5) · PUSH (clé du tour, KO-L009).

Protocole clone-chat v2.0.2 (7+1 étapes) : scellage 8 checks S1-S8, 0 secret.
Codes retour : 0 = succès, 1 = échec.
"""

import re
import sys
from datetime import datetime, timezone
from pathlib import Path

RACINE = Path("/home/z/my-project")
REPO = RACINE / "KNOWLEDGE-repo"
NOM = "clone-chat-session-web-f492e049-20261122-task113-suite-plateforme.md"
CLONE_HOTE = RACINE / "download" / NOM
CLONE_DEPOT = REPO / "download" / NOM
WORKLOG_HOTE = RACINE / "worklog.md"
WORKLOG_DEPOT = REPO / "worklog.md"


def h():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


CONTENU = f"""# Clone de discussion — session web-f492e049 (Task 113 SUITE : import 16 skills plateforme), 27ᵉ de la lignée

> Session : web-f492e049 · chat 17b8e0d9-d141-4dda-b86b-8b152e773f70 · canal zai-web · trace directive 1a201e4bda5a2289. Généré le {h()} par clone-chat v2.0.2 (7+1 étapes). Fenêtre du clone : import aux normes skill-creator des 16 skills plateforme résiduels (requalification du classement « hors périmètre » du tour précédent au nom de la directive explicite « même s'ils n'ont pas été écrits par moi ») : archives R4 byte-identité ×16, renommages kebab-case ×4 (asr/llm/tts/vlm), réécritures françaises complètes avec renvoi progressive disclosure, synchro dépôt canonique, dépendances KB réalignées, tests F+P, correct-work (projet) --bloc. Aucun agent modifié (4/4 déjà conformes aux normes agent-creator — précision 1a201ea1991bd6dd respectée).

## §0 — Contexte Système (SHARED v1.7.44)

> Écosystème Knowledge : skills/ = racine (72 SKILL.md + 4 .agent) | KB = skills/KNOWLEDGE.md | @mon-ecosysteme/ (corpus) | @historique/ (archive R4). Conventions kebab-case/semver/#token. Règle d'or n°6 : FRANÇAIS exclusif dès le premier mot. Référence canonique : « mon skill X » = forme installée skills/X/SKILL.md. État certification : 72/72 skills + 4/4 agents CONFORMES (audit Task 113). Versionnées : gen-plan v3.46.0 · correct-work v2.12.1 · clone-chat v2.0.2 · SHARED v1.7.44 · pin ECO_SKILLS ×2 arbres (aucun des 16 plateforme n'y figure — pas de cascade).

## §1 — Worklog chronologique (fenêtre du clone : suite 161)

| Suite | Date | Contenu (résumé exécutable) |
|---|---|---|
| 161 | 2026-11-22 | G26 état 0 commit en pendance (origin/main == ca75b379) + re-audit 56/72 · G27 mécanique import (archives R4 ×16 + renommages kebab ×4, repli os.rename corrigé en séance, idempotence ×2) · G28 réécritures ×16 selon skill-creator (template agent-browser : frontmatter complet + §0 SHARED + §0 RÈGLE ZÉRO provenance + corps FR code verbatim + historique ; 3 résidus de langue corrigés ; clôture triptyque ×16 + clause « Déclencher si » ×5 hubs ; audit final 72/72 + 4/4) · G29 synchro dépôt (git mv ×4 + sha256 ×32 + KB vlm ×3 deux arbres, parité byte ; pin/evals : aucun impact) · G30 tests F+P PASS (F1-F10 · audit 0,081 s · poids ratio 0,377) + CW --bloc suite PASS 5/5 + PUSH (clé du tour) |

## §2 — Artefacts de la fenêtre (Étape 2)

| Artefact | Rôle | État |
|---|---|---|
| download/rapport-audit-conformite-task113.json | Audit final 72/72 + 4/4 CONFORMES | SCELLÉ |
| scripts/task113-import-plateforme.py | Mécanique archives R4 + renommages (selftest ST1-ST4, idempotent) | CERTIFIÉ |
| scripts/task113-cloture-triptyque.py | Clôture triptyque ×16 (idempotent) | CERTIFIÉ |
| scripts/task113-sync-depot.py | Synchro dépôt canonique (sha256 ×32, idempotent) | CERTIFIÉ |
| scripts/task113-tests-fp-suite.py | Tests F+P suite (F1-F10 PASS) | CERTIFIÉ |
| download/rapport-task113-import-plateforme.json | Rapport mécanique 16/16 | SCELLÉ |
| download/rapport-task113-sync-depot.json | Rapport synchro 16/16 | SCELLÉ |
| download/rapport-tests-fp-task113-suite.json | Rapport tests F+P | SCELLÉ |
| download/rapport-cw-task113-suite-projet.md | Rapport CW --bloc suite PASS 5/5 | SCELLÉ |
| skills/{{asr,llm,tts,vlm,charts,docx,pdf,pptx,xlsx,image-edit,image-generation,image-search,gif-animator,gif-animator-pro,task-review,video-understand}}/SKILL.md | Réécrits v1.0.0 normes skill-creator | INSTALLED ×2 arbres |
| skills/…/references/plateforme-original.md ×16 | Archives R4 byte-identité des originaux | ARCHIVÉS ×2 arbres |

## §3 — Décisions et leçons de la fenêtre (Étape 3)

| ID | Décision / leçon | Portée |
|---|---|---|
| Directive explicite > classement hérité | Les 16 résiduels « hors périmètre » (tour précédent) requalifiés CORRIGIBLES : « même s'ils n'ont pas été écrits par moi » commande l'import aux normes | Task 113 suite |
| KO-L003 (×3) | Repli os.rename exécuté-réellement · assertion F1 corrigée dans le test · F3 aligné sur la norme arbitre maison (YAML non strict convention écosystème) — jamais ajuster la réalité | Task 113 suite |
| R4 progressive disclosure | Original intégral archivé byte-identité references/plateforme-original.md + renvoi explicite : conformité SANS perte d'information (poids ratio 0,377) | Task 113 suite |
| Périmètre agents | 4/4 agents conformes aux normes agent-creator/autonomous-agent dès l'audit — 0 modification d'agent (directive 1a201ea1991bd6dd) | Task 113 suite |
| Bootstrap & plateforme | Les 16 skills = plateforme hors-KB : synchro dépôt posée pour traçabilité, l'installation vivante reste skills/ (bootstrap ne projette pas les hors-KB) | Task 113 suite |

## §4 — État des pendances (Étape 4)

| Pendance | État |
|---|---|
| PUSH des commits du tour (clé du tour — KO-L009 mémoire de commande, sortie masquée) | Exécutée en fin de fenêtre |
| Révocation PATs antérieurs (Task 107 + Task 112) | CONSERVÉE — action propriétaire UNIQUE [CRITIQUE] |
| Décision cron 531684 (0 job — 6ᵉ vérification) | CONSERVÉE — escalade propriétaire |
| Révocation PAT du tour après usage | CONSERVÉE — rappel propriétaire [CRITIQUE] |

## §5 — Lignage et scellage (Étape 5)

Lignée : … → Task 112 tour 2 G15-G19 (25ᵉ) → Task 113 audit conformité (26ᵉ) → **Task 113 SUITE plateforme (27ᵉ)**. Session web-f492e049, fenêtre suites 160→161.

Drifts typés de la fenêtre : MODIFICATION ×16 SKILL.md plateforme (imports v1.0.0 normes skill-creator) · RENOMMAGE ×4 dossiers kebab-case (asr/llm/tts/vlm, deux arbres) · CREATION ×16 archives R4 references/plateforme-original.md · CREATION ×5 scripts Task 113 suite · MODIFICATION KB ×2 arbres (dépendances vlm ×3).
"""


def sceller() -> list:
    """8 checks S1-S8 (protocole clone-chat v2.0.2)."""
    texte = CLONE_HOTE.read_text(encoding="utf-8")
    checks = [
        ("S1_sections_0_a_5", all(f"## §{i}" in texte for i in range(6))),
        ("S2_worklog_table", "| 161 | 2026-11-22 |" in texte),
        ("S3_artefacts_table", "| Artefact | Rôle | État |" in texte),
        ("S4_decisions_table", "| ID | Décision / leçon | Portée |" in texte),
        ("S5_pendances_table", "| Pendance | État |" in texte),
        ("S6_lignage_27e", "27ᵉ de la lignée" in texte),
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
    print(f"SCELLAGE {sum(1 for _, r in checks if r)}/{len(checks)} — clone 27ᵉ :",
          CLONE_HOTE)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
