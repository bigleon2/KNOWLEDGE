#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Task 21 — F2 (finir P4) : résorption A1, A2, A6, A7 + A3 vivant.
Chaque édition est un remplacement exact idempotent (échec si motif absent et pas déjà appliqué).
KO-L007 : le compte de skills est vérifié mécaniquement avant toute correction « 80 → 93 ».
"""
import subprocess
import sys
from pathlib import Path

ECO = Path("/home/z/my-project/ecosystem")
log = []

def edit(path: Path, old: str, new: str, label: str, count: int = 1):
    t = path.read_text(encoding="utf-8")
    if new in t and old not in t:
        log.append(f"[DÉJÀ] {label}")
        return
    if old not in t:
        log.append(f"[KO] {label} — motif introuvable : {old[:70]!r}")
        sys.exit(1)
    path.write_text(t.replace(old, new, count), encoding="utf-8")
    log.append(f"[OK] {label}")

# ---------- vérification mécanique du compte (KO-L007) ----------
out = subprocess.run(["bash", "-c",
                      "ls skills/ | grep -v KNOWLEDGE.md | grep -v '@mon-ecosysteme' | wc -l"],
                     cwd=ECO, capture_output=True, text=True)
n_sub = int(out.stdout.strip())
out2 = subprocess.run(["bash", "-c", "ls skills/ | grep -v KNOWLEDGE.md | wc -l"],
                      cwd=ECO, capture_output=True, text=True)
n_all = int(out2.stdout.strip())
log.append(f"[KO-L007] comptage : {n_all} dossiers skills/ (dont @mon-ecosysteme) = "
           f"{n_sub} + 1 ; l'inventaire campagne (C003) = 93")
N = n_all  # le PM dit « ensemble de N skills » : le dossier skills/ EST l'écosystème

# ---------- A1 : références v3.15.0 + statut baseline dans les 3 n°54 ----------
A1_OLD = "intégration gen-plan v3.15.0 §1.9 ; baseline en attente QUOTA (D017)."
A1_NEW = {
    "fleet-engineering":
        "intégration gen-plan §1.9 (version d'alors v3.15.0 — PM courant : v3.18.0) ; "
        "baseline MESURÉE 7/7 les 2 voies (Task 17 — 42/42 votes réels).",
    "spec-driven-development":
        "intégration gen-plan §1.9 (version d'alors v3.15.0 — PM courant : v3.18.0) ; "
        "baseline MESURÉE 7/7 les 2 voies (Task 17 — 42/42 votes réels).",
    "memory-engineering":
        "intégration gen-plan §1.9 (version d'alors v3.15.0 — PM courant : v3.18.0) ; "
        "baseline MESURÉE 7/7 les 2 voies (Task 18-b — 21/21 votes réels).",
}
for skill, new in A1_NEW.items():
    edit(ECO / "skills" / skill / "SKILL.md", A1_OLD, new, f"A1 {skill}")

# ---------- A2 : registre d'assignation SHARED §7 — les 3 n°54 ----------
shared = ECO / "skills" / "@mon-ecosysteme" / "PROMPT-MAITRE-SHARED.md"
A2_ANCHOR = ("| `context-engineering` / `loop-engineering` / `graph-engineering` / `harness-engineering` "
             "| **Matérialisations skills des disciplines** (session A12 : SKILL.md + evals + "
             "trigger_evals — déclenchement automatique ; remplacement des agents `_disciplines/` A11) "
             "| Application dédiée de leur discipline respective dans les sessions d'ingénierie ; "
             "socle normatif : présent §7 |")
A2_ROW = ("| `fleet-engineering` / `spec-driven-development` / `memory-engineering` "
          "| **Matérialisations skills des disciplines n°54** (N34, Tasks 16-18 : SKILL.md + evals + "
          "trigger_evals — déclenchement automatique ; détention orchestrée : registre décentralisé "
          "§8 du skill + registre KB) | Application dédiée (orchestration de flottes d'agents ; "
          "développement piloté par specs ; mémoire longue de session) — orchestration gen-plan §1.9 |")
edit(shared, A2_ANCHOR, A2_ANCHOR + "\n" + A2_ROW, "A2 SHARED §7 registre n°54")

# ---------- A6 : clone-chat PM (80→N, v1.6.4, §0 canonique) ----------
pm = ECO / "skills" / "@mon-ecosysteme" / "PROMPT-MAITRE-CLONE-CHAT-v2.0.0.md"
edit(pm, "## ⚙️ CONTEXTE SYSTÈME (Extrait SHARED v1.6.1)",
          "## ⚙️ CONTEXTE SYSTÈME (Extrait SHARED v1.6.4)", "A6/A3 PM SHARED v1.6.4")
edit(pm, "### Règle Zéro (§0)\nL'écosystème Knowledge est un ensemble de 80 skills",
          f"### Règle Zéro (§0) — résumé de travail (le §0 canonique du présent PM : "
          f"« §0 — RÈGLE ZÉRO — CONTEXTE PERDU », infra)\n"
          f"L'écosystème Knowledge est un ensemble de {N} skills", f"A6 PM §0 résumé + {N} skills")
edit(pm, "mention 80 skills", f"mention {N} skills", "A6 PM l.335")
edit(pm, "80 skills mentionnés", f"{N} skills mentionnés", "A6 PM l.377")

# ---------- A7 : note de numérotation gen-plan SKILL.md ----------
gp = ECO / "skills" / "gen-plan" / "SKILL.md"
A7_ANCHOR = "### §1.14 Leçons knowledge-observer — économie API et arbitres (re-curation B13, modes M3-M4)"
A7_NOTE = ("\n\n> **Note de numérotation (Task 21, résorption A7)** : le saut §1.8 → §1.14 est "
           "intentionnel — les sections §1.14/§1.15 portent leurs numéros d'origine du PM "
           "(re-curation B13) afin de préserver la traçabilité des références croisées (KB, "
           "changelogs PM) ; les sections PM intermédiaires (§1.9-§1.13) ne sont pas miroitées "
           "ici — leurs contenus figurent en §1.6-§1.8, chaque en-tête citant sa source PM.")
t = gp.read_text(encoding="utf-8")
if A7_NOTE.strip() not in t:
    if A7_ANCHOR not in t:
        log.append("[KO] A7 ancre introuvable"); sys.exit(1)
    gp.write_text(t.replace(A7_ANCHOR, A7_ANCHOR + A7_NOTE, 1), encoding="utf-8")
    log.append("[OK] A7 note de numérotation consignée")
else:
    log.append("[DÉJÀ] A7 note présente")

print("\n".join(log))
print(f"\nCompte consigné dans le PM clone-chat : {N} skills.")
