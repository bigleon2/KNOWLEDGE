#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.12)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

# PROVENANCE: Task 22 (2026-10-23, session web-fdf5963c) — cascade documentaire
# KO-L004 de la montée refactor-guard v1.7.1→v1.8.0 (PM régénéré mécaniquement)
# + journal KB Task 22 (re-mesure QUOTA, optimisations pipeline, disciplines).
# Échec si 0 match ; idempotent ×2.
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
SHA_171 = "8fceb8c1ac1dbb2848b87a8d154d9970a5b6418551898065caee56f9392de33e"


def sub1(t, old, new, label):
    n = t.count(old)
    assert n == 1, f"{label}: {n} occurrences (attendu 1)"
    return t.replace(old, new, 1)


# ── 1. README @historique ────────────────────────────────────────────────
rh = BASE / "skills" / "@historique" / "README.md"
t = rh.read_text(encoding="utf-8")
if "PROMPT-MAITRE-REFACTOR-GUARD-v1.7.1.md" not in t:
    t = sub1(t,
             "| REFACTOR-GUARD | refactor-guard — garde-fous de refactoring (H01-H15, échelle rollout) | 2 (v1.7.0 → v1.7.1) | 1 (v1.7.0) | v1.7.1 |",
             "| REFACTOR-GUARD | refactor-guard — garde-fous de refactoring (H01-H15, échelle rollout) | 3 (v1.7.0 → v1.8.0) | 2 (v1.7.0, v1.7.1) | v1.8.0 |",
             "README @historique ligne famille")
    t = sub1(t, "## 5. Index des fichiers sources archivés (25 PMs — sceau SHA-256)",
             "## 5. Index des fichiers sources archivés (26 PMs — sceau SHA-256)",
             "README @historique index heading")
    t = sub1(t,
             "| refactor-guard/PROMPT-MAITRE-REFACTOR-GUARD-v1.7.0.md | 74438d695d2fb7b4d7b406f576b16d7fa2706d0b4113183ea6e55fb84215e62e |",
             "| refactor-guard/PROMPT-MAITRE-REFACTOR-GUARD-v1.7.0.md | 74438d695d2fb7b4d7b406f576b16d7fa2706d0b4113183ea6e55fb84215e62e |\n"
             "| refactor-guard/PROMPT-MAITRE-REFACTOR-GUARD-v1.7.1.md | " + SHA_171 + " |",
             "README @historique index row")
    t = sub1(t,
             "Complément cascade gen-plan v3.22.1 (2026-10-11, session web-b4d7dd19) :",
             "Complément cascade Task 22 (2026-10-23, session web-fdf5963c — directive « disciplines/techniques », veille 2025-2026) : `PROMPT-MAITRE-REFACTOR-GUARD-v1.7.1.md` archivé par `mv` byte-identité (fichier non suivi — jamais commité, adaptation règle d'or n°1 journalisée ; SHA-256 scellé ci-dessous ; provenance : le fichier corpus v1.7.1 était la source de l'archive scellée Task 20 — même octets). Complément cascade gen-plan v3.22.1 (2026-10-11, session web-b4d7dd19) :",
             "README @historique provenance note")
    rh.write_text(t, encoding="utf-8")
    print("README @historique : index §5 25→26 + ligne v1.7.1 + famille REFACTOR-GUARD recalibrée")
else:
    print("README @historique : déjà à jour (idempotence)")

# ── 2. README corpus ─────────────────────────────────────────────────────
rc = BASE / "skills" / "@mon-ecosysteme" / "README.md"
t = rc.read_text(encoding="utf-8")
if "Révision v2.1.9" not in t:
    t = sub1(t, "> **Révision v2.1.8 (2026-10-23, Task 18",
             "> **Révision v2.1.9 (2026-10-23, Task 22 — session web-fdf5963c, directive propriétaire gen-plan(step) « analyse pipeline d'installation + disciplines/techniques »)** : refactor-guard v1.7.1→v1.8.0 (§1.9bis apports de veille 2025-2026 : golden master AVANT + mutation testing léger + rollback automatique armé — 12 disciplines/techniques enrichies, agent-creator v2.2.0 dérive critique résorbée) ; PM REFACTOR-GUARD v1.8.0 généré mécaniquement KO-L004, v1.7.1 archivé @historique/prompts-maitres/refactor-guard/ (SHA scellé) ; PM-INSTALL v1.8.0→v1.8.1 (F1 anti-faux-succès rc propagé + F2 exclusion __pycache__ + F3 vérification post-install SHA-256 embarquée) ; SHARED v1.7.9 ; arborescence §2 recalibrée.\n> **Révision v2.1.8 (2026-10-23, Task 18", "README corpus rev")
    t = sub1(t, "│   ├── PROMPT-MAITRE-REFACTOR-GUARD-v1.7.1.md  ← 4e famille (décision D009)",
             "│   ├── PROMPT-MAITRE-REFACTOR-GUARD-v1.8.0.md  ← 4e famille (décision D009)",
             "README corpus arbo")
    rc.write_text(t, encoding="utf-8")
    print("README corpus : v2.1.9 + arbo v1.8.0")
else:
    print("README corpus : déjà à jour (idempotence)")

# ── 3. SYNC-CONTEXT ──────────────────────────────────────────────────────
sc = BASE / "skills" / "@mon-ecosysteme" / "SYNC-CONTEXT.md"
t = sc.read_text(encoding="utf-8")
if "Révision v1.5.1" not in t:
    t = sub1(t, "> **Révision v1.5.0 (2026-10-23, cascade Task 18",
             "> **Révision v1.5.1 (2026-10-23, cascade Task 22 — session web-fdf5963c, KO-L004)** : état du corpus recalibré — refactor-guard v1.7.1→v1.8.0 (§1.9bis veille 2025-2026 — golden master AVANT + mutation testing + rollback armé), PM v1.8.0 généré mécaniquement, v1.7.1 archivé @historique (mv byte-identité, SHA scellé) ; 12 disciplines/techniques + §1.9bis (dont agent-creator v2.2.0 dérive critique résorbée — SKILL.md re-écrit fabrique F1-F5, .agent ré-écrit champ capacites A2A) ; PM-INSTALL v1.8.1 (F1/F2/F3 fail-fast) ; SHARED v1.7.9 ; propagation du marqueur §0 exécutée (idempotent) ; rescelleur dynamisé (dest_historique += refactor-guard — KO-L003) ; archive rescellée round-trip 9/9 ×2 ; re-mesure QUOTA agent-creator LEVÉE (voie L 3/3 CONFIRME — bilan 31/31 sans QUOTA).\n> **Révision v1.5.0 (2026-10-23, cascade Task 18", "SYNC rev")
    sc.write_text(t, encoding="utf-8")
    print("SYNC-CONTEXT : v1.5.1")
else:
    print("SYNC-CONTEXT : déjà à jour (idempotence)")

# ── 4. Journal KB — entrée Task 22 ───────────────────────────────────────
kb = BASE / "skills" / "KNOWLEDGE.md"
t = kb.read_text(encoding="utf-8")
if "Task 22 — directive gen-plan(step) : re-mesure QUOTA" not in t:
    anchor = "- **Task 18 — directive gen-plan : correct-work(projet) + boucle QUOTA"
    idx = t.find(anchor)
    assert idx > 0, "ancre journal KB introuvable"
    entry = ("- **Task 22 — directive gen-plan(step) : re-mesure QUOTA agent-creator + optimisation installation + disciplines/techniques (veille 2025-2026)** : "
             "directive propriétaire (session web-fdf5963c, 2026-10-23 ; $ECO-LEON = mon écosystème personnel). (1) **Re-mesure QUOTA LEVÉE** : "
             "sonde KO-L001 QUOTA_OK au premier tour → `task17-remeasure-voie-l.py --skip-done --retry-quota` — 3/3 votes réels, décision CONFIRME "
             "(cas négatif officiel préservé, 0 révision) — bilan voie L final 31/31 (22 CONFIRME + 7 REFUTE_UNANIME + 2 AMBIGU), 0 QUOTA. "
             "(2) **Pipeline d'installation optimisé** (eco_install_pipeline.py) : F1 anti-faux-succès (rc rescellement PROPAGÉ — exit 2 si échec), "
             "F2 exclusion/purge __pycache__ (aucune souillure projetée), F3 vérification post-install embarquée (SHA-256 34/34 SKILL.md hôte==dépôt, "
             "fail-fast exit 2) — idempotent ×2, purges propres. (3) **Disciplines/techniques** (périmètre : skills + agents tagués « discipline » — "
             "8 disciplines n°54/n°55 + outils/gardes + hôte-seuls + 2 agents) : recherches web ciblées (Spec Kit/Kiro/arXiv From Code to Contract ; "
             "Anthropic context/harness/effective-agents ; AgeMem/survey mémoire ; Cognition/Anthropic multi-agents ; Graphiti/GraphRAG ; TRACE/VPR/RLVR ; "
             "A2A/MCP) → §1.9bis « Apports de veille 2025-2026 » inséré dans 15 SKILL.md + bumps semver (SDD 1.1.0, CDC 1.1.0, PE 2.3.0, APE 1.1.0 "
             "+ read_when rétabli 1/94 Task 28, context 1.2.0, memory 1.2.0, fleet 1.1.0 gate anti-flotte, loop 1.2.0 calibration graders, harness 1.2.0 "
             "checkpoint/reprise, graph 1.1.0 bi-temporel, refactor-guard 1.8.0, refactoring-test 1.1.0, resource-monitor 1.1.0, autonomous-agent 1.2.0 "
             "G2 re-planification, inter-scripts 1.1.0 retry/heartbeat) ; **agent-creator v2.2.0 — DÉRIVE CRITIQUE résorbée** (copie quasi verbatim "
             "d'autonomous-agent → VRAIE fabrique F1-F5, .agent ré-écrit champ capacites style Agent Card A2A, read_when réparé) ; gen-plan/references/"
             "guide-selection-agent-skill.md complété (fichier quasi vide résorbé — arbre de routage a-b-c-d) ; KO-L004 : ECO_SKILLS + KB recalibrés "
             "(16 entrées), PM REFACTOR-GUARD v1.8.0 généré (couverture OK), v1.7.1 archivé R4, rescelleur dynamisé (dest_historique += refactor-guard), "
             "SHARED v1.7.9 / PM-INSTALL v1.8.1, ULTRA régénéré, propagate exécuté, archive round-trip 9/9 ×2.\n")
    t = t[:idx] + entry + t[idx:]
    kb.write_text(t, encoding="utf-8")
    print("KB : entrée journal Task 22 insérée")
else:
    print("KB : entrée Task 22 déjà présente (idempotence)")

print("Cascade documentaire Task 22 : terminée.")
return_code = 0
sys.exit(return_code)
