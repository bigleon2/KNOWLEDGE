#!/usr/bin/env python3
# PROVENANCE: session web-f90062ce (2026-10-24) — tâche B4 — re-wipe du workspace
# constaté post-B3 (corpus hôte effacé : @mon-ecosysteme, gen-plan, correct-work,
# KNOWLEDGE.md, @historique absents ; scripts/ et download/ workspace intacts).
# Ré-exécution de la directive « réinstalle ma dernière version de mon écosystème
# avant de continuer » depuis le dépôt local da549af (état le plus récent certifié
# B3 : gen-plan v3.25.0, KB 39, SHARED v1.7.12, PM-INSTALL v1.8.5).
# Ce script consolide le rapport d'installation B4 (structure du rapport B2).
"""Rapport d'installation B4 — réinstallation post-re-wipe (source da549af)."""
import json
import subprocess
from datetime import datetime, timezone, timedelta

REPO = "/home/z/my-project/KNOWLEDGE-repo"
OUT = "/home/z/my-project/scripts/rapport-installation-ecosysteme.json"

head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=REPO, capture_output=True,
                      text=True).stdout.strip()

rapport = {
    "type": "rapport-installation-ecosysteme",
    "date": datetime.now(timezone(timedelta(hours=1))).isoformat(timespec="seconds"),
    "session": "web-f90062ce",
    "task": ("B4 — ré-exécution directive « réinstalle avant de continuer » "
             "(re-wipe workspace post-B3 constaté)"),
    "source": (f"clone local bigleon2/KNOWLEDGE @ {head[:7]} "
               "(descendant certifié B3 de origin/main e9a68a1 ; pin descendant-tolérant b75a620)"),
    "constat_prealable": {
        "hote_wipe": ["skills/@mon-ecosysteme", "skills/gen-plan", "skills/correct-work",
                       "skills/KNOWLEDGE.md", "skills/@historique"],
        "hote_intact": ["KNOWLEDGE-repo (HEAD da549af)", "worklog.md", "download/ (livrables)",
                        "scripts/ workspace (sync0, rapport, arbitres copie)"],
        "depot_working_tree": "149 fichiers mode-only (numstat 0/0 — chmod wipe, zéro perte contenu)",
    },
    "pipeline": ("KNOWLEDGE-repo/scripts/eco_install_pipeline.py "
                 "(PM-INSTALL v1.8.5 §3.2-a — installation directe, exécutant canonique)"),
    "resultats": {
        "corpus": "9 fichiers .md (@mon-ecosysteme — vivants v3.25.0/SHARED v1.7.12/PM-INSTALL v1.8.5)",
        "skills_kb": "39 entrées installées (gen-plan 15, correct-work, clone-chat, refactor-guard 16, "
                     "alias-eco 5, cahier-des-charges 4, agent-prompt-engineering 4, disciplines…)",
        "historique": "48 fichiers (@historique)",
        "scripts": "236 fichiers",
        "post_install_sha256": "39/39 vérifiés, 0 divergence",
        "garde_R2": "0 rétrogradation — host ≤ repo partout",
        "archive": "régénérée 9 entrées, round-trip vérifié (véhicule v2.2)",
    },
    "corrections_post_install": {
        "resync_S0": ("scripts/task-eco-reinstall-sync0.py — 4 substitutions v1.7.7 → v1.7.12 "
                      "(inter-scripts, resume-youtube, web-reader, web-search — libellés console "
                      "« → v1.7.11 » cosmétiques, écriture réelle CANON_HEADER v1.7.12 vérifiée "
                      "par grep ; cahier-des-charges géré par pipeline via KB 39, SHA host==repo OK)"),
    },
    "arbitres": {
        "verify_cross_depôt": "100.0 % (0 warning, 0 error)",
        "check_ecosysteme_integrity_hote": "82/82 PASS, 0 FAIL (manifeste écrit)",
        "ensure_installed_hote": "INSTALLE (kb_entrees 39, fichiers_manquants [], "
                                  "head 67fe393 = shim connu, verdict prévaut)",
        "test_coherence_interactions_hote": ("51 PASS / 1 WARN hérité (historique B1 non cloné — "
                                              "réserve documentée H3/B2/B3 inchangée) / 0 FAIL — "
                                              "PASS AVEC RÉSERVES"),
    },
    "rejeux_idempotents": {
        "pipeline_rejeu": "no-op (39/39 SHA, 0 divergence, 0 rétrogradation, archive round-trip)",
        "sync0_rejeu": "0 substitution (no-op idempotent)",
    },
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(rapport, f, ensure_ascii=False, indent=2)
print(f"rapport B4 écrit : {OUT}")
print(f"source : {head[:7]}")
