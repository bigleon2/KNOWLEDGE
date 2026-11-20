#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 111 — Ouverture worklog suite 157 (idempotente, parité hôte↔dépôt).

Ajoute l'entrée d'ouverture suite 157 citant le plan Task 111 + marqueur
PLAN-AFFICHE (hook E7-DISP points 3-4 : R5 + preuve d'affichage dans la
MÊME entrée que le plan) + le constat de surveillance F3 (tâche 7 du
livrable Task 108 : bootstrap du tour exécuté — 0 récidive). R1 : no-op
si l'entrée est déjà présente dans l'un des deux arbres.
"""

# ⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.40)
# SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
# Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
# Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
# Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
# Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
# Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).

import json
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

HOST = Path("/home/z/my-project")
ARBRES = [HOST / "worklog.md", HOST / "KNOWLEDGE-repo" / "worklog.md"]

ENTREE = """
## {date} (suite 157, session web-ecef7f80) — Task 111 : directive propriétaire trace 1a1f7d3e607663f1 « installe mon écosystème personnel via PM-INSTALL [URL commit a5daa964] + gen-plan(step) : relecture intégrale via le dernier clone + dernières tâches avec la clé + correct-work --bloc + clone-chat » : G0 GO-1 installation VERDICT INSTALLE-REPARÉ (entrée canonique bootstrap-ecosysteme.py : preflight dérive recyclage 2778 modes auto-réparée · dry-run 55 divergences hôte · installation 55 SHA 0 divergence · certification ALL-PASS-6/6 · garde É1 INSTALLE rc=0 · re-check ensure-installed rc=0 hôte=d4e228f4 ; PM-INSTALL byte-identique ×3 sources SHA b2fe8371… — upload/a5daa964/HEAD) ; G1 relecture intégrale (clone 22ᵉ task110 + download/taches-restantes-task108.md fait foi + worklog suites 155-156 — 0 trou, tâches 3-4-5 éteintes confirmées) ; PLAN download/plan-task111-push-pendance-etat-cw-clone.md (G2-G6, answer key D001-D010, **PLAN-AFFICHE** — E7-DISP chaîne 6 points : plan écrit download/ ✓ · answer key ✓ · E8 horodaté ✓ · worklog R5 ✓ [présente entrée] · bloc récapitulatif au chat ✓ · fenêtre native TodoWrite ✓) ; G2 dernières tâches avec la clé du tour : PUSH pendance d4e228f4 → main rc=0 (a5daa964..d4e228f4 — KO-L009 mémoire de commande, sortie masquée, 0 trace de clé — E15 36ᵉ) + atterrissage vérifié ls-remote ANONYNE : refs/heads/main = d4e228f4, parité HEAD = origin ✓ (pendance PUSH Task 110 ÉTEINTE) + cron list = 0 job (4ᵉ dispositif perdu — escalade propriétaire MAINTENUE, clause anti-boucle règle d'or n°5, 0 recréation) ; G3 surveillance F3 (tâche 7) : constat consigné — bootstrap du tour exécuté, branche injection v2.2.0 SAIN (0 récidive, 0 SyntaxError, 55 SHA 0 divergence, certification 6/6) → tâche 7 ÉTEINTE (critère d'extinction satisfait) ; E1-RES : G-RES OK (disque {disque} · mémoire {memoire} · charge {charge} — profil NORMAL, 0 signal de pression) ; E2 Type 4 (exécution d'état) · E3 E4 ~6 200 #token (G2 1 200 · G3 1 000 · G4 1 500 · G5 1 500 · G6 1 000) · E5 [gen-plan · correct-work · clone-chat · resource-monitor] · E6 NORMAL
"""


def _gres() -> dict:
    res = {}
    try:
        disque = subprocess.run(
            ["df", "-BG", "--output=size,used", str(HOST)],
            capture_output=True, text=True, check=True, timeout=10,
        ).stdout.strip().splitlines()[-1].split()
        res["disque"] = f"{int(disque[1][:-1])}/{int(disque[0][:-1])} Go"
        memoire = subprocess.run(
            ["free", "-g"], capture_output=True, text=True, check=True, timeout=10
        ).stdout.splitlines()[1].split()
        res["memoire"] = f"{memoire[2]}/{memoire[1]} Go"
        charge = open("/proc/loadavg").read().split()[0]
        res["charge"] = charge
    except Exception as exc:  # noqa: BLE001 — G-RES : dégradé, jamais bloquant
        res = {"disque": "n/d", "memoire": "n/d", "charge": f"n/d ({exc})"}
    return res


def ouvrir() -> int:
    entree = ENTREE.format(
        date=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        **_gres(),
    )
    resultat = []
    for arbre in ARBRES:
        if not arbre.exists():
            resultat.append({"arbre": str(arbre), "statut": "ABSENT — ignoré"})
            continue
        texte = arbre.read_text(encoding="utf-8")
        if "suite 157, session web-ecef7f80" in texte:
            resultat.append({"arbre": str(arbre), "statut": "NO-OP (déjà présente)"})
            continue
        if not texte.endswith("\n"):
            texte += "\n"
        arbre.write_text(texte + entree, encoding="utf-8")
        resultat.append({"arbre": str(arbre), "statut": "AJOUTÉE", "octets": len(entree)})
    # Parité md5 des deux arbres (preuve R5)
    parite = "N/A"
    presents = [a for a in ARBRES if a.exists()]
    if len(presents) == 2:
        import hashlib
        h = [hashlib.md5(a.read_bytes()).hexdigest() for a in presents]
        parite = "OK" if h[0] == h[1] else f"DIVERGENCE {h[0][:8]}≠{h[1][:8]}"
    rapport = {"verdict": "OUVERTE" if any(r["statut"] == "AJOUTÉE" for r in resultat) else "NO-OP",
               "arbres": resultat, "parite_md5": parite}
    print(json.dumps(rapport, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(ouvrir())
