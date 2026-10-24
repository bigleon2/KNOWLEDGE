#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""task-c3-recalibrage-v3260.py — Recalibrage croisé KO-L004 cascade gen-plan v3.26.0.

  1. KB (skills/KNOWLEDGE.md) : heading v3.26.0, description (philosophie #4 + règle n°5),
     calibration v3.26.0 préfixée
  2. ECO_SKILLS (check-ecosysteme-integrity.py) : pin gen-plan 3.25.0 → 3.26.0
  3. Références vives : gen-plan v3.25.0 → v3.26.0 (skills porteurs)
  4. README corpus : arborescence PM v3.26.0 + ligne révision v2.1.14
  5. SYNC-CONTEXT : ligne révision v1.5.6
  6. historique-autres-elements.md : SHARED v1.7.13 / PM-INSTALL v1.8.6 / SYNC / README
Idempotent ×2 (garde new-in-t avant application — même convention task-c2-archive).
"""
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHA_V3250 = "cc6cdcdf8cb89bd6da03552dc7e57d0b8c8d1681ec957ce8fa315823c1e95197"


def edit(path, subs, label):
    with open(path, encoding="utf-8") as f:
        t = f.read()
    changed = 0
    for old, new in subs:
        if new in t:
            continue  # déjà appliqué
        c = t.count(old)
        if c == 1:
            t = t.replace(old, new)
            changed += 1
        else:
            print("[ECART] %s : motif %d fois (attendu 1) : %r" % (label, c, old[:70]))
            sys.exit(2)
    if changed:
        with open(path, "w", encoding="utf-8") as f:
            f.write(t)
    print("[%s] %s : %d substitution(s)" % ("OK" if changed else "NO-OP", label, changed))


def main():
    # 1. KB
    edit(os.path.join(BASE, "skills", "KNOWLEDGE.md"), [
        ("## gen-plan v3.25.0", "## gen-plan v3.26.0"),
        ("classification Type 1-4 (E3), règles d'or §1.5 (n°1 adaptation autonome,",
         "classification Type 1-4 (E3), philosophie #4 parallélisation par défaut + dégradation "
         "gracieuse des vagues contre service externe (429 → bascule sérielle + retry/backoff + "
         "cache déterministe figé une fois, code retour seul jamais suffisant, question de "
         "ROUTAGE du référentiel jamais tronquée — v3.26.0), règles d'or §1.5 (n°1 adaptation "
         "autonome,"),
        ("déclencheur verbatim « intègre dans le plan d'actions » v3.17.2 ; déclencheurs de mode gen-plan(step)/gen-plan(step-ok)",
         "déclencheur verbatim « intègre dans le plan d'actions » v3.17.2 ; n°5 anti-aspirant — "
         "journal/statuts/chiffres dérivés de l'état vérifiable (KO-L003 étendu à l'écriture), "
         "audit des journaux pré-existants en reprise post-coupure, recensement mécanique vs "
         "libellé de mémoire, périmètre dépôt/miroir avant qualification — dépôt = source R4, "
         "corrections R2 append-only sur @historique (v3.26.0) ; déclencheurs de mode gen-plan(step)/gen-plan(step-ok)"),
        ("- **Dernière calibration** : montée v3.25.0 (2026-10-24, SG7.4 Task B2",
         "- **Dernière calibration** : montée v3.26.0 (2026-10-24, session web-f90062ce — "
         "leçons de la vérité source PM INSTALL [Tasks 29/30, session web-fdf5963c, archive "
         "authentifiée SHA PM 31ed1a52] + directive propriétaire) : philosophie #4 — clause "
         "dégradation gracieuse ; §1.5 — règle d'or n°5 anti-aspirant ; etapes-detaillees.md — "
         "section « Leçons vagues parallèles » ; evals id 7 + id 9 étendus ; PM v3.26.0 généré "
         "mécaniquement KO-L004 — delta verrouillé 6 substitutions count=1, 1495 L (plage "
         "arbitre 1200-1500), v3.25.0 archivé R4 mv byte-identité SHA %s… ; SHARED v1.7.13 / "
         "PM-INSTALL v1.8.6 recalibrés ; propagate v1.7.13 ×106 skills + 83 scripts + 2 "
         "agents ; écarts hérités consignés non masqués (JSON evals PM 8/9, §9.1 snapshot "
         "pré-v3.22.0) ; montée v3.25.0 (2026-10-24, SG7.4 Task B2" % SHA_V3250[:8]),
    ], "KB gen-plan")

    # 2. ECO_SKILLS pin
    edit(os.path.join(BASE, "scripts", "check-ecosysteme-integrity.py"), [
        ('"gen-plan": "3.25.0",  # KO-L004 (SG7.4 Task B2, session web-f90062ce, 2026-10-24) : re-matérialisation structure hiérarchique du mode step sur base v3.24.0 (parallélisation conservée — couches orthogonales) ; précédent Task 26 : parallélisation par défaut',
         '"gen-plan": "3.26.0",  # KO-L004 (session web-f90062ce, 2026-10-24) : leçons vérité source PM INSTALL (dégradation gracieuse philosophie #4 + règle d\'or n°5 anti-aspirant) ; précédent SG7.4 Task B2 : re-matérialisation structure hiérarchique ; précédent Task 26 : parallélisation par défaut'),
    ], "ECO_SKILLS pin")

    # 4. README corpus
    edit(os.path.join(BASE, "skills", "@mon-ecosysteme", "README.md"), [
        ("PROMPT-MAITRE-GEN-PLAN-v3.25.0.md", "PROMPT-MAITRE-GEN-PLAN-v3.26.0.md"),
        ("> **Version** : 2.1.13", "> **Version** : 2.1.14"),
        ("> **Révision v2.1.13 (2026-10-24, cascade SG7.4 Task B2 — session web-f90062ce, GO propriétaire)** : ",
         "> **Révision v2.1.14 (2026-10-24, cascade gen-plan v3.26.0 — session web-f90062ce)** : "
         "leçons de la vérité source PM INSTALL intégrées à gen-plan (philosophie #4 dégradation "
         "gracieuse + règle d'or n°5 anti-aspirant) ; PM GEN-PLAN v3.26.0 généré mécaniquement "
         "KO-L004 (delta 6 substitutions, 1495 L), v3.25.0 archivé R4 mv byte-identité (SHA %s…) ; "
         "SHARED v1.7.13 / PM-INSTALL v1.8.6 recalibrés ; propagate v1.7.13 ; KB recalibrée. "
         "Précédent — **Révision v2.1.13 (2026-10-24, cascade SG7.4 Task B2 — session web-f90062ce, GO propriétaire)** : " % SHA_V3250[:8]),
    ], "README corpus")

    # 5. SYNC-CONTEXT
    edit(os.path.join(BASE, "skills", "@mon-ecosysteme", "SYNC-CONTEXT.md"), [
        ("> **Version** : 1.5.5\n> **Date** : 2026-10-23",
         "> **Version** : 1.5.6\n> **Date** : 2026-10-24"),
        ("> **Révision v1.5.5 (2026-10-24, cascade SG7.4 Task B2 — session web-f90062ce, GO propriétaire)** : ",
         "> **Révision v1.5.6 (2026-10-24, cascade gen-plan v3.26.0 — session web-f90062ce)** : "
         "état du corpus recalibré — gen-plan v3.25.0→v3.26.0 (leçons vérité source PM INSTALL : "
         "dégradation gracieuse + règle d'or n°5 anti-aspirant) ; PM GEN-PLAN v3.26.0 généré "
         "mécaniquement KO-L004, v3.25.0 archivé R4 (SHA %s…) ; SHARED v1.7.13 / PM-INSTALL "
         "v1.8.6 ; propagate v1.7.13 ; Contexte Système N2/N3 propagé (106 skills + 83 scripts "
         "+ 2 agents). Précédent — **Révision v1.5.5 (2026-10-24, cascade SG7.4 Task B2 — "
         "session web-f90062ce, GO propriétaire)** : " % SHA_V3250[:8]),
    ], "SYNC-CONTEXT")

    # 6. historique-autres-elements.md — nouvelles lignes (R2 : l'historique s'ajoute, jamais réédité)
    edit(os.path.join(BASE, "skills", "@historique", "historique-autres-elements.md"), [
        ("| v1.7.12 | 2026-10-24 | §6.1 — référence PM GEN-PLAN portée à v3.25.0",
         "| v1.7.13 | 2026-10-24 | §6.1 — référence PM GEN-PLAN portée à v3.26.0 (génération mécanique "
         "`scripts/generer-pm-skill.py` — session web-f90062ce — leçons vérité source PM INSTALL : "
         "dégradation gracieuse philosophie #4 + règle d'or n°5 anti-aspirant ; delta verrouillé 6 "
         "substitutions, 1495 L)\n| v1.7.12 | 2026-10-24 | §6.1 — référence PM GEN-PLAN portée à v3.25.0"),
        ("| v1.5.5 | 2026-10-24 | Cascade SG7.4 Task B2 (session web-f90062ce, GO propriétaire) : gen-plan",
         "| v1.5.6 | 2026-10-24 | Cascade gen-plan v3.26.0 (session web-f90062ce) : état du corpus "
         "recalibré — gen-plan v3.25.0→v3.26.0, PM v3.26.0 généré mécaniquement, v3.25.0 archivé R4 "
         "(SHA %s…), SHARED v1.7.13 / PM-INSTALL v1.8.6, propagate v1.7.13 (106 skills + 83 scripts "
         "+ 2 agents)\n| v1.5.5 | 2026-10-24 | Cascade SG7.4 Task B2 (session web-f90062ce, GO propriétaire) : gen-plan" % SHA_V3250[:8]),
        ("| v2.1.13 | 2026-10-24 | Recalibrage état gen-plan v3.25.0",
         "| v2.1.14 | 2026-10-24 | Cascade gen-plan v3.26.0 (session web-f90062ce) : leçons vérité "
         "source PM INSTALL (dégradation gracieuse + règle d'or n°5) ; arborescence v3.26.0/v1.8.6/"
         "SHARED v1.7.13 ; PM v3.26.0 généré mécaniquement, v3.25.0 archivé R4 (SHA %s…)\n| v2.1.13 | 2026-10-24 | Recalibrage état gen-plan v3.25.0" % SHA_V3250[:8]),
        ("| v1.8.5 | 2026-10-24 | §2ter + §A.3 instantané rafraîchi gen-plan v3.25.0",
         "| v1.8.6 | 2026-10-24 | KO-L004 v1.1.0 — génération mécanique du PM (`scripts/"
         "generer-pm-skill.py`) : gen-plan v3.25.0→v3.26.0 ; recalibrage croisé : SHARED v1.7.13 "
         "(§6.1), §2ter, §A.3 — session web-f90062ce\n| v1.8.5 | 2026-10-24 | §2ter + §A.3 instantané rafraîchi gen-plan v3.25.0"),
        ("| gen-plan | v3.25.0 | audit-provenance | v1.1.0 |",
         "| gen-plan | v3.26.0 | audit-provenance | v1.1.0 |"),
        ("(source : registre KB, instantané rafraîchi 2026-10-24 — SG7.4 Task B2 : +cahier-des-charges",
         "(source : registre KB, instantané rafraîchi 2026-10-24 — SG7.4 Task B2 : +cahier-des-charges"),
    ], "historique-autres-elements")

    print("\nRecalibrage croisé v3.26.0 terminé.")


if __name__ == "__main__":
    main()
