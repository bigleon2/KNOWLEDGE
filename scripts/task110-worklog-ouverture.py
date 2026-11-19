#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 110 — Ouverture worklog suite 156 (idempotente, parité hôte↔dépôt).

Ajoute la note É1-INSTALL manquante côté dépôt (la garde E1-RES du tour a
journalisé côté hôte uniquement) puis l'entrée d'ouverture suite 156 citant
le plan Task 110 + marqueur PLAN-AFFICHE (hook E7-DISP points 3-4 : R5 +
preuve d'affichage dans la MÊME entrée que le plan). R1 : no-op si présente.
"""

# ⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.40)
# SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
# Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
# Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
# Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
# Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
# Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).

import sys
from pathlib import Path

HOST = Path("/home/z/my-project")
ARBRES = [HOST / "worklog.md", HOST / "KNOWLEDGE-repo" / "worklog.md"]
NOTE_E1 = "\n\n> É1-INSTALL Task 56 : auto-réparation garde étendue — version-management restauré(s) depuis le miroir local KNOWLEDGE-repo.\n"

ENTREE = """
## 2026-11-19 (suite 156, session web-ecef7f80) — Task 110 : directive propriétaire trace 1a1f2297d90c957d « gen-plan : "GO futur + GO-3" » — le message CONSTITUE le GO propriétaire pour les tâches 3-4-5 du livrable download/taches-restantes-task108.md (P2 F3 injecteur · P2 F2 scelleur · P3 GO-3 canons ; hors périmètre : tâches 1/6/7/8) : PLAN download/plan-task110-go-futur-f3-f2-go3-cw-clone.md (G0-G4, answer key D001-D010 schéma criterion/verification/source/priority/status, **PLAN-AFFICHE** — E7-DISP chaîne 6 points : plan écrit download/ ✓ · answer key 10 décisions ✓ · E8 horodaté 2026-11-19T05:05:00Z ✓ · worklog R5 ✓ [présente entrée] · bloc récapitulatif au chat ✓ · fenêtre native TodoWrite ✓) ; E1-RES : garde É1-INSTALL INSTALLE-REPARÉ rc=0 (version-management auto-réparé depuis le miroir — note É1 ci-dessus) · G-RES OK (disque 8,1 Go · mémoire 3,6 Go · charge 0,06 — profil NORMAL, 0 signal de pression) ; E2 inventaire MESURÉ au disque : parités md5 hôte↔dépôt vérifiées (propagate-context.py 570bc0bf… · eco_install_pipeline.py 46be4055… · task-f5-seal-archive-v23.py 6dfac1a6… · 5 scripts protégés task98/101/102/104/106 ×2 arbres) · `from __future__` présents dans task101/task102 (les 2 compilations cassées CW 107) · corpus @mon-ecosysteme/ INCHANGÉ ce tour (SYNC-CONTEXT v1.5.11 : mentions propagate/scelleur uniquement historiques R2/R6) ; E3 Type 4 · E4 ~13 100 #token (G0 600 · G1 3500 · G2 3500 · G3 2500 · G4 3000) · E5 [gen-plan · script-creator · correct-py · correct-work · clone-chat · resource-monitor] · E6 NORMAL
"""


def main() -> int:
    for wl in ARBRES:
        texte = wl.read_text(encoding="utf-8")
        if "## 2026-11-19 (suite 156" in texte:
            print(f"  ⏭️  {wl.name} ({wl.parent.name}) : suite 156 déjà présente — no-op (R1)")
            continue
        texte = texte.rstrip("\n") + "\n" + ENTREE
        wl.write_text(texte, encoding="utf-8")
        print(f"  ✅ {wl.name} ({wl.parent.name}) : suite 156 ajoutée ({len(ENTREE)} car.)")
    # Adaptation (règle d'or n°1, journalisée) : la note É1 du tour doit précéder
    # l'entrée suite 156 sur les DEUX arbres — la sous-chaîne générique matche 24
    # occurrences historiques (constat mesuré), la garde porte donc sur la POSITION
    # (note immédiatement avant l'entrée), pas sur la présence globale.
    for wl in ARBRES:
        texte = wl.read_text(encoding="utf-8")
        marqueur = "## 2026-11-19 (suite 156"
        idx = texte.find(marqueur)
        if idx == -1:
            print(f"  ❌ {wl.parent.name} : entrée suite 156 introuvable")
            return 1
        avant = texte[:idx].rstrip("\n")
        if not avant.endswith(NOTE_E1.strip()):
            texte = avant + "\n\n" + NOTE_E1 + texte[idx:]
            wl.write_text(texte, encoding="utf-8")
            print(f"  ✅ {wl.name} ({wl.parent.name}) : note É1 du tour insérée avant suite 156")
        else:
            print(f"  ⏭️  {wl.name} ({wl.parent.name}) : note É1 déjà en position — no-op")
    return 0


if __name__ == "__main__":
    sys.exit(main())
