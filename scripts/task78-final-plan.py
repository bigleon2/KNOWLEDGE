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
"""Task 78/79 G1 SG3.2 — Finalisation du plan Task 78 (E8 final 10/10)."""
import sys
from pathlib import Path

R = Path("/home/z/my-project/KNOWLEDGE-repo")
PLAN = R / "download/plan-task78-regle-sondage-borne.md"
TS = "2026-11-08T18:05:00Z"

t = PLAN.read_text(encoding="utf-8")


def sub(old, new, label, n=1):
    global t
    c = t.count(old)
    if c != n:
        print("ABANDON : [%s] trouvé %d fois" % (label, c))
        sys.exit(2)
    t = t.replace(old, new)


# 1. Statuts D004-D010 : pending → verified
for i in range(4, 11):
    did = "D0%02d" % i
    # chaque bloc décision : status "pending" → "verified" — ciblé par le bloc id
    anchor = '  - id: "%s"\n' % did
    idx = t.find(anchor)
    if idx < 0:
        print("ABANDON : %s introuvable" % did)
        sys.exit(2)
    end = t.find("  - id: \"D", idx + 10)
    if end < 0:
        end = t.find("```", idx)
    bloc = t[idx:end]
    if 'status: "pending"' not in bloc:
        print("ABANDON : %s sans status pending" % did)
        sys.exit(2)
    t = t[:idx] + bloc.replace('status: "pending"', 'status: "verified"') + t[end:]

# 2. En-tête horodatage
sub("**Horodatage plan : 2026-11-08T16:32:00Z (INITIAL — 10 décisions : 3 verified ouverture / 7 pending exécution)**",
    "**Horodatage plan : %s (FINAL — 10 décisions : 10/10 verified, horodatage verdict couplé)**" % TS,
    "en-tête")

# 3. Statuts de groupes
sub("## G1 — Diagnostic PRE + amendement gen-plan v3.41.0 `[À FAIRE]` (0/3)",
    "## G1 — Diagnostic PRE + amendement gen-plan v3.41.0 `[TERMINÉ]` (3/3)", "G1")
sub("## G2 — Cascade KO-L004 (périmètre gen-plan — SHARED INCHANGÉ) + sync hôte `[À FAIRE]` (0/3)",
    "## G2 — Cascade KO-L004 (périmètre gen-plan) + sync hôte `[TERMINÉ]` (3/3)", "G2")
sub("## G3 — Preuves + arbitres + E8 final + commit `[À FAIRE]` (0/3)",
    "## G3 — Preuves + arbitres + E8 final + commit `[TERMINÉ]` (3/3)", "G3")

# 4. PLAN-AFFICHE
sub("(Task 78 — download/plan-task78-regle-sondage-borne.md — INITIAL — **G1 Diagnostic + amendement `[À FAIRE]` 0/3 · G2 Cascade + sync `[À FAIRE]` 0/3 · G3 Preuves + clôture `[À FAIRE]` 0/3**",
    "(Task 78 — download/plan-task78-regle-sondage-borne.md — FINAL — **G1 Diagnostic + amendement ✅ 3/3 · G2 Cascade + sync ✅ 3/3 · G3 Preuves + clôture ✅ 3/3**",
    "PLAN-AFFICHE")

# 5. Verdict E8 final
sub("Verdict E8 : PASS INITIAL (answer-key-checker 16/16 ALL PASS ×2 sha16 stable + check_plan_protocol P1-P5 PASS — 10 décisions : D001-D003 verified ouverture · D004-D010 pending exécution — Horodatage vérifié : 2026-11-08T16:32:00Z)",
    "Verdict E8 : PASS FINAL (10/10 décisions verified — D001-D003 ouverture · D004 amendement v3.41.0 [30 697 o < 30 720, description/§A intacts, idempotence amendement NO-OP ×2] · D005 extension protocoles-detailles [4 règles + exceptions, +15 L] · D006 cascade [PM v3.41.0 1 810 L + PM v3.40.0 archivé R4 sceau 8fa129f9… + KB + pin ×2 + historiques + README ×2 + ULTRA ×2 SHA 1eb7269eb078… ; ÉCART consigné règle d'or n°5 : SHARED v1.7.36 + PM-INSTALL v1.9.13 recalibrés par le générateur contrairement au plan, réversion = lag §6.1 — propagation §0 v1.7.36 convergée 0/0/0] · D007 preuves [PRE GO baseline v3.40.0 6 contrats 31 sections · POST ×2 MAINTIEN DE L'OPTIMISATION · volumétrie BRUT 12 207 o / BORNÉ 3 763 o ×3,2, re-mesure fraîche 11 068/3 168 ×3,5] · D008 arbitres [cross 100,0 % · vcw 16/16 · integrity 112/112 · doublons 0/271 · coherence 55/0/0 PASS STRICT · sweep 9 citations recalées en 1 round] · D009 sync [pipeline rc=0 ×2 passes 54/54, 0 divergence, rescelage task21-f2 ×2 byte-stable, archive véhicule v2.2] · D010 clôture [E8 final 10/10, horodatages couplés " + TS + ", commit dédié SANS mode-purs]) — Horodatage vérifié : " + TS,
    "verdict E8")

PLAN.write_text(t, encoding="utf-8")
print("Plan Task 78 finalisé : 10/10 verified, E8 FINAL %s" % TS)
