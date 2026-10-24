#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""task-c2-archive-v3250.py — Archivage R4 du PM gen-plan v3.25.0 + scellage index + journaux.

Cascade KO-L004 (gen-plan v3.26.0) :
  1. git mv PM v3.25.0 → skills/@historique/prompts-maitres/gen-plan/ (byte-identité R4)
  2. Scellage SHA-256 : row insérée au README @historique §5 (table, head de famille)
  3. Heading §5 : 30 → 31 PMs
  4. Row GEN-PLAN (vue d'ensemble) : 29 versions / 23 archivés / vivante v3.26.0
  5. Label stale ligne §4 : « 18 PMs (v3.6.1 → v3.22.1) » → « 23 PMs (v3.6.1 → v3.25.0) »
     (calibré sur la réalité mesurée — KO-L003/règle d'or n°5)
  6. Journal par-skill gen-plan.md : en-tête (vivante v3.26.0, 23 archivés),
     ligne v3.25.0 amendée (supplantée/archivée), ligne v3.26.0 ajoutée,
     famille 28→29 versions, liste fichiers 22→23.
Idempotent ×2 : re-exécution sur état cohérent = no-op (garde R2/R6).
"""
import hashlib
import os
import subprocess
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPUS = os.path.join(BASE, "skills", "@mon-ecosysteme")
HIST = os.path.join(BASE, "skills", "@historique")
PM_OLD_NAME = "PROMPT-MAITRE-GEN-PLAN-v3.25.0.md"
PM_OLD = os.path.join(CORPUS, PM_OLD_NAME)
PM_DEST = os.path.join(HIST, "prompts-maitres", "gen-plan", PM_OLD_NAME)
README = os.path.join(HIST, "README.md")
JOURNAL = os.path.join(HIST, "historiques-par-skill", "gen-plan.md")


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def edit(path, subs, label):
    with open(path, encoding="utf-8") as f:
        t = f.read()
    changed = 0
    for old, new in subs:
        if new in t:
            changed += 0  # déjà appliqué (idempotence — new contient toujours old)
            continue
        c = t.count(old)
        if c == 1:
            t = t.replace(old, new)
            changed += 1
        else:
            print("[ECART] %s : motif trouvé %d fois (attendu 1) : %r"
                  % (label, c, old[:70]))
            sys.exit(2)
    if changed:
        with open(path, "w", encoding="utf-8") as f:
            f.write(t)
    print("[%s] %s : %d substitution(s)" % ("OK" if changed else "NO-OP", label, changed))


def main():
    # 1. git mv R4
    if os.path.isfile(PM_OLD):
        r = subprocess.run(["git", "mv", PM_OLD, PM_DEST], cwd=BASE,
                           capture_output=True, text=True)
        if r.returncode != 0:
            print("ABANDON : git mv échoué : %s" % r.stderr)
            sys.exit(2)
        print("[OK] git mv R4 : %s" % PM_DEST)
    elif os.path.isfile(PM_DEST):
        print("[NO-OP] archive déjà en place : %s" % PM_DEST)
    else:
        print("ABANDON : PM v3.25.0 introuvable des deux côtés")
        sys.exit(2)

    sha = sha256(PM_DEST)
    print("[OK] SHA-256 archive : %s" % sha)

    # 2-5. README @historique
    edit(README, [
        ("## 5. Index des fichiers sources archivés (30 PMs — sceau SHA-256)",
         "## 5. Index des fichiers sources archivés (31 PMs — sceau SHA-256)"),
        ("| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.24.0.md | 31ed1a5250fbadcdf91ee4fedd911439c1de4282d7a1104e850a1e57004f241a |",
         "| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.25.0.md | %s |\n| gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.24.0.md | 31ed1a5250fbadcdf91ee4fedd911439c1de4282d7a1104e850a1e57004f241a |" % sha),
        ("| GEN-PLAN | gen-plan — planification de tâches (4 modes, 15 étapes E1-E15) | 28 (v2.0.0 → v3.25.0) | 22 (v3.6.1 → v3.24.0) | v3.25.0 |",
         "| GEN-PLAN | gen-plan — planification de tâches (4 modes, 15 étapes E1-E15) | 29 (v2.0.0 → v3.26.0) | 23 (v3.6.1 → v3.25.0) | v3.26.0 |"),
        ("| `prompts-maitres/gen-plan/` | 18 PMs GEN-PLAN historiques (v3.6.1 → v3.22.1), déplacés du corpus `git mv`",
         "| `prompts-maitres/gen-plan/` | 23 PMs GEN-PLAN historiques (v3.6.1 → v3.25.0) — comptage mécanique recalibré cascade v3.26.0 (label stale « 18 » hérité documenté worklog), déplacés du corpus `git mv`"),
    ], "README @historique")

    # 6. Journal par-skill
    edit(JOURNAL, [
        ("> **Version vivante (corpus)** : v3.25.0 — `skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.25.0.md` (sa table §7 fait foi)",
         "> **Version vivante (corpus)** : v3.26.0 — `skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.26.0.md` (sa table §7 fait foi)"),
        ("> **Versions archivées** : 22 PMs (v3.6.1 → v3.24.0) dans `prompts-maitres/gen-plan/` — sceau SHA-256 au README §5 (v3.24.0 : SHA 31ed1a5250fbadcdf91ee4fedd911439c1de4282d7a1104e850a1e57004f241a)",
         "> **Versions archivées** : 23 PMs (v3.6.1 → v3.25.0) dans `prompts-maitres/gen-plan/` — sceau SHA-256 au README §5 (v3.25.0 : SHA %s)" % sha),
        ("## Famille GEN-PLAN — 28 versions (skill : gen-plan)",
         "## Famille GEN-PLAN — 29 versions (skill : gen-plan)"),
        ("lélisation = couche d'exécution) — MINOR fonctionnalité — **VERSION VIVANTE (corpus)** |",
         "lélisation = couche d'exécution) — MINOR fonctionnalité — supplantée par v3.26.0 le 2026-10-24 — archivée (SHA %s scellé index §5 README) |" % sha),
        ("discipline d'engineering avec un détecteur/évaluateur indépendant (anti-auto-certification) — **VERSION VIVANTE (corpus)** |",
         "discipline d'engineering avec un détecteur/évaluateur indépendant (anti-auto-certification) — supplantée par v3.23.1 le 2026-10-11 — archivée (label « VERSION VIVANTE » stale hérité corrigé cascade v3.26.0 — règle d'or n°5) |"),
        ("(formes du dépôt arbitrées) sans changer le comportement du skill — PATCH documentation — **VERSION VIVANTE (corpus)** |",
         "(formes du dépôt arbitrées) sans changer le comportement du skill — PATCH documentation — supplantée par v3.24.0 le 2026-10-24 — archivée (label stale hérité corrigé cascade v3.26.0 — règle d'or n°5) |"),
        ("v3.23.1, v3.23.2, v3.24.0 (22 fichiers, SHA-256 au §5).",
         "v3.23.1, v3.23.2, v3.24.0, v3.25.0 (23 fichiers, SHA-256 au §5)."),
    ], "Journal par-skill gen-plan.md")

    # 7. Ligne v3.26.0 (insertion après la ligne v3.25.0 — idempotent par présence)
    with open(JOURNAL, encoding="utf-8") as f:
        t = f.read()
    if "| v3.26.0 |" not in t:
        anchor = "\n| v3.25.0 | "
        idx = t.index(anchor)
        row = ("\n| v3.26.0 | 2026-10-24 | Leçons de la vérité source PM INSTALL (Tasks 29/30, "
               "session web-fdf5963c — dogfooding résorption A/B/C 19 skills, archive "
               "authentifiée SHA PM 31ed1a52) + règle d'or n°5 (directive propriétaire "
               "2026-10-24, session web-f90062ce) : philosophie #4 — clause dégradation "
               "gracieuse des vagues contre service externe (429 → bascule sérielle + "
               "retry/backoff + cache déterministe figé une fois, code retour seul jamais "
               "suffisant, jugement sémantique = question de ROUTAGE jamais tronqué) ; §1.5 — "
               "règle d'or n°5 anti-aspirant (journal/statuts/chiffres dérivés de l'état "
               "vérifiable — KO-L003 étendu à l'écriture, audit journaux pré-existants en "
               "reprise, recensement mécanique, périmètre dépôt/miroir — dépôt = source R4, "
               "corrections R2 append-only) ; etapes-detaillees.md — section « Leçons vagues "
               "parallèles » ; evals id 7 + id 9 étendus ; écarts hérités consignés non "
               "masqués (JSON evals PM 8/9, §9.1 snapshot pré-v3.22.0) ; PM v3.26.0 généré "
               "mécaniquement (delta verrouillé 6 substitutions count=1, projection 1496 L "
               "réelle 1495 L — plage arbitre 1200-1500), v3.25.0 archivé git mv "
               "byte-identité R4 ; SHARED v1.7.13 / PM-INSTALL v1.8.6 recalibrés ; propagate "
               "v1.7.13 (106 skills + 83 scripts + 2 agents) | Intégration des leçons "
               "d'exécution mesurées de la vérité source (dégradation gracieuse + anti-aspirant) "
               "sur la base réconciliée v3.25.0 — MINOR comportement — **VERSION VIVANTE "
               "(corpus)** |")
        t = t[:idx] + row + t[idx:]
        with open(JOURNAL, "w", encoding="utf-8") as f:
            f.write(t)
        print("[OK] ligne v3.26.0 insérée au journal")
    else:
        print("[NO-OP] ligne v3.26.0 déjà présente")

    print("\nRÉSUMÉ : SHA scellé = %s" % sha)


if __name__ == "__main__":
    main()
