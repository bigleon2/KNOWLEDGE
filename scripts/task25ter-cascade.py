#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.11)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

"""Cascade KO-L004 Task 25ter — alias-eco v1.2.0 (dépôt KNOWLEDGE-repo).
Édits chirurgicaux : PM-INSTALL v1.8.3, KB, journal, SYNC-CONTEXT v1.5.3,
README v2.1.11, historique-autres-elements (4 lignes). Assert count==1 par edit."""
import re, sys

REPO = "/home/z/my-project/KNOWLEDGE-repo"
edits_done = []

def edit_file(path, old, new, label, count=1):
    with open(path, encoding="utf-8") as f:
        t = f.read()
    if new in t and old not in t:
        edits_done.append(label + " (déjà appliqué)")
        return
    n = t.count(old)
    assert n == count, f"FAIL {label}: {n} occurrence(s) de {old[:60]!r}"
    with open(path, "w", encoding="utf-8") as f:
        f.write(t.replace(old, new))
    edits_done.append(label)

# ── 1. PM-INSTALL v1.8.3 ─────────────────────────────────────────────
PMI = f"{REPO}/skills/@mon-ecosysteme/PROMPT-MAITRE-INSTALL-ECOSYSTEME.md"
edit_file(PMI, "Version : 1.8.2\n", "Version : 1.8.3\n", "PMI version line")
edit_file(PMI, "| alias-eco | v1.0.0 |", "| alias-eco | v1.2.0 |", "PMI A.3 row")
old_row = "| v1.8.2 | 2026-10-23 | KO-L004 v1.1.0"
new_row = ("| v1.8.3 | 2026-10-23 | KO-L004 v1.1.0 — cascade alias-eco v1.1.0→v1.2.0 "
           "(grammaire B mécanique --trigger + attribution OPT-TRIO ; v1.1.0 = Description "
           "Optimization clause d'exclusion) : §A.3 instantané recalibré — Task 25bis/25ter, "
           "session web-fdf5963c, GO propriétaire |\n" + old_row)
edit_file(PMI, old_row, new_row, "PMI history row v1.8.3")

# ── 2. KB : header + bullet ──────────────────────────────────────────
KB = f"{REPO}/skills/KNOWLEDGE.md"
edit_file(KB, "## alias-eco v1.1.0", "## alias-eco v1.2.0", "KB header")
edit_file(KB,
    "Trois déclencheurs : « alias-eco » (gestion : lister, synchroniser, ajouter, résoudre), « liste mes alias » (affichage du registre), « alias-eco (chat) » (liste TXT des phrases récurrentes de la discussion, triée par ordre alphabétique).",
    "Déclencheurs : « alias-eco » (gestion : lister, synchroniser, ajouter, résoudre), « liste mes alias » (affichage du registre), « alias-eco (chat) » (liste TXT des phrases récurrentes de la discussion, triée par ordre alphabétique), grammaire B mécanique v1.2.0 « alias-eco \"<texte>\" --add <ALIAS> » (exécutée par --trigger — variantes « » / $ALIAS) ; alias canoniques OPT-TRIO (« de façon cohérente, optimisée et fonctionnelle ») et ECO-LEON (« mon écosystème personnel »).",
    "KB bullet déclencheurs")

# ── 3. Journal alias-eco ─────────────────────────────────────────────
J = f"{REPO}/skills/@historique/historiques-par-skill/alias-eco.md"
edit_file(J, "> **Version vivante (corpus)** : v1.1.0", "> **Version vivante (corpus)** : v1.2.0", "Journal vivante")
old_j = "| v1.1.0 | 2026-10-24 |"
new_j = ("| v1.2.0 | 2026-10-23 | Task 25ter (GO propriétaire « déclencheur grammaire B », session web-fdf5963c — gen-plan(step)) : déclencheur mécanique d'attribution `alias-eco \"<texte>\" --add <ALIAS>` (variantes « » / $ALIAS) + commande `--trigger` au gestionnaire (parse + garde format, idempotent, rejet propre rc=2) ; selftest 15→21 cas (6 grammaire B) ; trigger_evals 8→9 cas (+1 positif grammaire B) ; attribution OPT-TRIO exécutée par dogfooding `--trigger` (mandat propriétaire : usage `$façon()` — nom hors format corrigé en canonique, signalé non expansé) ; recalibrage KO-L004 : KB v1.2.0, PM-INSTALL v1.8.3 (§A.3), SYNC-CONTEXT v1.5.3, README v2.1.11, ULTRA régénéré, rescellement ×2 | Le déclencheur d'attribution est mécanisé (zéro re-parsing LLM), testé 21/21 et couvert par le corpus officiel ; la phrase la plus récurrente de l'écosystème porte enfin son alias canonique $OPT-TRIO — **VERSION VIVANTE (corpus)** |\n" + old_j)
edit_file(J, old_j, new_j, "Journal row v1.2.0")

# ── 4. SYNC-CONTEXT v1.5.3 (ligne Révision remplacée in place) ──────
SC = f"{REPO}/skills/@mon-ecosysteme/SYNC-CONTEXT.md"
with open(SC, encoding="utf-8") as f:
    sc = f.read()
sc_new, n = re.subn(r"> \*\*Révision v1\.5\.2 \(2026-10-23[^\n]*?",
    "> **Révision v1.5.3 (2026-10-23, cascade Task 25bis/25ter — session web-fdf5963c, GO propriétaire)** : alias-eco v1.2.0 (grammaire B --trigger + OPT-TRIO ; v1.1.0 Description Optimization) ; KB recalibrée ; PM-INSTALL v1.8.3 (§A.3) ; ULTRA régénéré ; registre @Alias : OPT-TRIO attribué (état vivant, non-cible resync). Précédent — ", sc, count=1)
assert n == 1, "FAIL SYNC-CONTEXT revision line"
with open(SC, "w", encoding="utf-8") as f:
    f.write(sc_new)
edits_done.append("SYNC-CONTEXT v1.5.3")

# ── 5. README v2.1.11 ────────────────────────────────────────────────
RD = f"{REPO}/skills/@mon-ecosysteme/README.md"
with open(RD, encoding="utf-8") as f:
    rd = f.read()
rd_new, n = re.subn(r"> \*\*Révision v2\.1\.10 \(2026-10-23[^\n]*?",
    "> **Révision v2.1.11 (2026-10-23, Task 25bis/25ter — session web-fdf5963c, GO propriétaire)** : alias-eco v1.2.0 — grammaire B mécanique (`--trigger`) + attribution OPT-TRIO ; v1.1.0 Description Optimization (clause d'exclusion sans radicaux étrangers — replay 8/8) ; registre @Alias vivant (ECO-LEON, OPT-TRIO) ; KB, PM-INSTALL v1.8.3 (§A.3), SYNC v1.5.3, ULTRA recalibrés. Précédent — ", rd, count=1)
assert n == 1, "FAIL README revision line"
with open(RD, "w", encoding="utf-8") as f:
    f.write(rd_new)
edits_done.append("README v2.1.11")

# ── 6. historique-autres-elements.md : 4 lignes ─────────────────────
H = f"{REPO}/skills/@historique/historique-autres-elements.md"
with open(H, encoding="utf-8") as f:
    h = f.read()
# SYNC table : insérer après l'en-tête de table §2
sc_head = "## 2. SYNC-CONTEXT.md (procédure de synchronisation des blocs)\n\n| Version | Date | Résumé de révision |\n|---------|------|--------------------|\n"
assert h.count(sc_head) == 1
h = h.replace(sc_head, sc_head + "| v1.5.3 | 2026-10-23 | Cascade Task 25bis/25ter (GO propriétaire, session web-fdf5963c) : alias-eco v1.1.0→v1.2.0 (grammaire B --trigger + OPT-TRIO ; v1.1.0 Description Optimization replay 8/8) ; KB, PM-INSTALL v1.8.3 (§A.3), ULTRA recalibrés ; registre @Alias vivant (ECO-LEON, OPT-TRIO — non-cible resync) |\n", 1)
# README table §3
rd_head = "## 3. README.md (guide de référence de l'écosystème)\n\n| Version | Date | Résumé de révision |\n|---------|------|--------------------|\n"
assert h.count(rd_head) == 1
h = h.replace(rd_head, rd_head + "| v2.1.11 | 2026-10-23 | Cascade Task 25bis/25ter (GO propriétaire, session web-fdf5963c) : alias-eco v1.2.0 (grammaire B --trigger + OPT-TRIO ; v1.1.0 Description Optimization) ; KB, PM-INSTALL v1.8.3, SYNC v1.5.3, ULTRA recalibrés |\n", 1)
# PM-INSTALL table §5
pmi_head = "## 5. PROMPT-MAITRE-INSTALL-ECOSYSTEME.md (pipeline d'installation — source unique)\n\n| Version | Date | Résumé de révision |\n|---------|------|--------------------|\n"
assert h.count(pmi_head) == 1
h = h.replace(pmi_head, pmi_head + "| v1.8.3 | 2026-10-23 | Cascade alias-eco v1.2.0 (Task 25bis/25ter, GO propriétaire) : §A.3 instantané recalibré (alias-eco v1.0.0→v1.2.0) — bump PATCH conformité semver |\n", 1)
# KB table §6 — insérer en tête de table
kb_head = re.search(r"## 6\. Registre KB[^\n]*\n\n\| Version \| Date \| Résumé de révision \|\n\|-+\|-+\|-+\|\n", h)
assert kb_head, "FAIL KB table header"
h = h[:kb_head.end()] + "| 2026-10-23 | Task 25bis/25ter (GO propriétaire) : alias-eco v1.0.0→v1.2.0 — en-tête + bullet déclencheurs (grammaire B --trigger, alias canoniques ECO-LEON/OPT-TRIO) |\n" + h[kb_head.end():]
with open(H, "w", encoding="utf-8") as f:
    f.write(h)
edits_done.append("historique-autres-elements ×4")

print("CASCADE OK — %d edits :" % len(edits_done))
for e in edits_done:
    print(" -", e)
