#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.35)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).

Task 53 (2026-11-06, session web-c30e6506) — RESTAURATION de l'état certifié Task 52
(cascade gen-plan v3.34.0→v3.35.0, commit perdu 9346385 au recyclage sandbox n°3).

Lignage : Task 52 (2026-11-05) avait certifié gen-plan v3.35.0 (règle d'or n°9)
sur son clone local — JAMAIS POUSSÉ (clé lecture seule, 4×403). Le recyclage
sandbox a détruit le clone. CE SCRIPT reconstruit l'état certifié :
  1. corpus restauré BYTE-EXACT depuis l'archive d'intégrité scellée Task 52
     (download/mon-ecosysteme_archive.zip, 9 entrées — véhicule d'intégrité
     v2.2 : GEN-PLAN v3.35.0, SHARED v1.7.23, PM-INSTALL v1.9.1, ULTRA,
     README v2.1.16) — la garde anti-perte de task21-f2-rebuild-archive.py
     avait refusé de perdre le PM v3.35.0 (extra hors homologues) ;
  2. PM v3.34.0 déplacé vers @historique/prompts-maitres/gen-plan/ (R4 git mv) ;
  3. SKILL.md gen-plan v3.35.0 reconstruit (version + règle d'or n°9 §1.5 +
     hook E1-RES §1.2bis étendu trois→quatre + point (4) + bullet §5.6) —
     substitutions verrouillées méthode B1 (ABANDON sans écriture si ancre
     absente), le texte du PM v3.35.0 archivé fait foi pour le contenu n°9 ;
  4. le recalibrage croisé KO-L004 est rejoué par task52-cascade-genplan-v3350.py
     (idempotent — ops 1-7 : KB, pin ECO_SKILLS, historiques, disciplines,
     READMEs, RETRAITS_SANCTIONNES) et la propagation §0 v1.7.23 par
     propagate-context.py (bump v2.0.5).

Vérifications intégrées : byte-identité corpus ↔ archive (9/9), ancrage des
substitutions (count exact), idempotence (re-jeu = no-op).
"""

import json
import os
import shutil
import subprocess
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RECOVERY = os.path.expanduser("~/GitHub/_recuperation-task52/corpus-extrait/@mon-ecosysteme")
HOST_SCRIPTS = "/home/z/my-project/scripts"

CORPUS_FILES = [
    "PROMPT-MAITRE-GEN-PLAN-v3.35.0.md",
    "PROMPT-MAITRE-SHARED.md",
    "PROMPT-MAITRE-INSTALL-ECOSYSTEME.md",
    "PROMPT-ULTRA-MAITRE-ORCHESTRATION.md",
    "README.md",
]

OPS = []


def sub_locked(text, old, new, count, label):
    """Substitution verrouillée (méthode B1) : ABANDON si ancre != count fois.
    Idempotence : new déjà présent → no-op signalé."""
    if new in text:
        OPS.append("%s : DÉJÀ APPLIQUÉ (no-op)" % label)
        return text
    c = text.count(old)
    if c != count:
        print("ABANDON — %s : ancre trouvée %d fois (attendu %d)" % (label, c, count))
        sys.exit(2)
    OPS.append("%s : appliqué" % label)
    return text.replace(old, new)


def step1_corpus():
    """Restaure les 5 fichiers corpus depuis l'archive (byte-exact) + git mv v3.34.0."""
    corpus = os.path.join(BASE, "skills", "@mon-ecosysteme")
    for f in CORPUS_FILES:
        src, dst = os.path.join(RECOVERY, f), os.path.join(corpus, f)
        if not os.path.isfile(src):
            print("ABANDON — fichier de récupération absent : %s" % src)
            sys.exit(2)
        if os.path.isfile(dst) and open(src, "rb").read() == open(dst, "rb").read():
            OPS.append("corpus %s : déjà identique (no-op)" % f)
            continue
        shutil.copy2(src, dst)
        OPS.append("corpus %s : restauré byte-exact depuis l'archive Task 52" % f)
    # V3.34.0 → @historique (R4 : git mv, jamais copier)
    v3340 = os.path.join(corpus, "PROMPT-MAITRE-GEN-PLAN-v3.34.0.md")
    hist = os.path.join(BASE, "skills", "@historique", "prompts-maitres", "gen-plan",
                        "PROMPT-MAITRE-GEN-PLAN-v3.34.0.md")
    if os.path.isfile(hist):
        OPS.append("PM v3.34.0 : déjà archivé @historique (no-op)")
    elif os.path.isfile(v3340):
        r = subprocess.run(["git", "mv", "skills/@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN-v3.34.0.md",
                            "skills/@historique/prompts-maitres/gen-plan/PROMPT-MAITRE-GEN-PLAN-v3.34.0.md"],
                           cwd=BASE, capture_output=True, text=True)
        if r.returncode != 0:
            print("ABANDON — git mv v3.34.0 : %s" % r.stderr.strip())
            sys.exit(2)
        OPS.append("PM v3.34.0 : archivé @historique (git mv, R4)")
    else:
        print("ABANDON — PM v3.34.0 introuvable (corpus et @historique)")
        sys.exit(2)


# Règle d'or n°9 — texte intégral (source : PM v3.35.0 archivé, §1.8 — fait foi)
N9 = ("**Règle d'or n°9 — Vérification automatique de l'installation de l'écosystème à toute "
      "invocation de gen-plan (post-coupure)** (directive propriétaire 2026-11-04, session "
      "web-c30e6506 — gen-plan : « avant de continuer vérifie que mon écosystème est encore "
      "installé (si mon écosystème doit-être installé alors la lecture de PM SHARED doit-être "
      "faite et lorsque que mon écosystème sera installé alors génère à nouveau le plan d'action "
      "via mon skill gen-plan) et fais en sorte que cette vérification devienne automatique "
      "(si mon écosystème doit-être installé alors la lecture de PM SHARED doit-être faite et "
      "lorsque que mon écosystème sera installé alors génère à nouveau le plan d'action via mon "
      "skill gen-plan) lorsque mon skill gen-plan est appelé après une coupure. ») : à TOUTE "
      "invocation de gen-plan — modes step/step-ok comme invocation NULL, la coupure n'étant "
      "jamais présupposée mais DÉTECTÉE par la vérification — l'agent vérifie MÉCANIQUEMENT, "
      "AVANT toute planification, que l'écosystème est encore installé sur le profil : "
      "(i) piliers — registre KB `skills/KNOWLEDGE.md`, corpus "
      "`skills/@mon-ecosysteme/PROMPT-MAITRE-SHARED.md`, forme installée "
      "`skills/gen-plan/SKILL.md` ; (ii) si les piliers sont présents, arbitre "
      "`scripts/check-ecosysteme-integrity.py` (0 FAIL attendu) ; si l'écosystème est absent "
      "ou endommagé (coupure de contexte, wipe inter-sessions, recyclage sandbox — cas "
      "documenté PM-INSTALL §3.4), le chemin de rétablissement s'exécute AUTOMATIQUEMENT, "
      "dans l'ordre : (a) **lecture intégrale du PM SHARED** "
      "(`skills/@mon-ecosysteme/PROMPT-MAITRE-SHARED.md` — étape 0 du pipeline PM-INSTALL, "
      "préalable obligatoire à toute installation) ; (b) **réinstallation par le pipeline "
      "PM-INSTALL**, voie directe (`scripts/eco_install_pipeline.py` depuis le clone certifié "
      "— règle d'or n°4 : le clone git local fait foi, jamais une lecture distante ; si le "
      "clone manque, le cloner d'abord) ; (c) **certification complète par les arbitres** "
      "(verify-cross 100 %, check-ecosysteme-integrity 0 FAIL, verify-correct-work — "
      "PM-INSTALL §3.3) ; (d) **l'écosystème étant installé, le plan d'actions est généré à "
      "nouveau via le skill gen-plan réinstallé** (règle d'or n°2 + KO-L005), l'invocation "
      "courante se poursuivant sur l'état réinstallé ; chaque déclenchement de la garde est "
      "journalisé au worklog (cause, piliers vérifiés, solution, coût #token — règle d'or "
      "n°1). La garde est portée par le hook E1-RES (§1.2bis — quatrième vérification "
      "préalable) ; elle est LÉGÈRE (présence des piliers + un arbitre) : une session saine "
      "la franchit sans coût perceptible, une session post-coupure la déclenche — preuve "
      "vivante : session web-c30e6506 des 2026-11-04/05 (profil post-coupure 14/52 → "
      "PM SHARED lu intégralement → réinstallation → arbitres 98/98 + verify-cross 141/141 "
      "+ verify-correct-work 16/16 → plan régénéré via v3.35.0).")

# Point (4) du hook E1-RES (adapté §1.2bis SKILL.md — référence §1.5)
E1RES4 = (" ; (4) **garde post-coupure écosystème (règle d'or n°9, v3.35.0)** — vérification "
          "mécanique de l'installation de l'écosystème (piliers — registre KB, corpus SHARED, "
          "forme installée gen-plan — puis arbitre `scripts/check-ecosysteme-integrity.py`) : "
          "écosystème absent ou endommagé (coupure, wipe inter-sessions, recyclage sandbox) → "
          "lecture intégrale du PM SHARED + réinstallation PM-INSTALL (voie directe "
          "`eco_install_pipeline.py` depuis le clone certifié, règle d'or n°4) + certification "
          "arbitres + re-génération du plan via le gen-plan réinstallé (règle d'or n°2 + "
          "KO-L005), AVANT toute analyse (détail : règle d'or n°9 au §1.5)")

BULLET = ("- **v3.35.0 (2026-11-05, session web-c30e6506 — directive propriétaire, gen-plan : "
          "« avant de continuer vérifie que mon écosystème est encore installé (si mon "
          "écosystème doit-être installé alors la lecture de PM SHARED doit-être faite et "
          "lorsque que mon écosystème sera installé alors génère à nouveau le plan d'action "
          "via mon skill gen-plan) et fais en sorte que cette vérification devienne "
          "automatique (…) lorsque mon skill gen-plan est appelé après une coupure. »)** : "
          "**règle d'or n°9 — Vérification automatique de l'installation de l'écosystème à "
          "toute invocation de gen-plan (post-coupure)** ajoutée au §1.5 (après n°8, règles "
          "contiguës — la coupure étant DÉTECTÉE par la vérification, jamais présupposée) : "
          "vérification mécanique des piliers (registre KB + corpus SHARED + forme installée "
          "gen-plan) puis arbitre check-ecosysteme-integrity à TOUTE invocation ; écosystème "
          "absent/endommagé → chemin automatique : lecture intégrale PM SHARED → "
          "réinstallation PM-INSTALL voie directe eco_install_pipeline.py depuis le clone "
          "certifié [règle d'or n°4] → certification arbitres → re-génération du plan via le "
          "gen-plan réinstallé [règle d'or n°2 + KO-L005] ; journalisation worklog règle "
          "d'or n°1 ; hook E1-RES étendu (§1.2bis — trois → quatre vérifications préalables, "
          "point (4) garde post-coupure). MINOR — addition pure (précédent v3.34.0 règle "
          "n°8), description frontmatter inchangée (non-régression triggers). Cascade "
          "KO-L004 : PM v3.35.0 généré mécaniquement (delta verrouillé "
          "`scripts/delta-genplan-v3350.json` — insertion n°9 §1.8 + extension E1-RES §1.12 "
          "+ history), SHARED v1.7.23 / PM-INSTALL v1.9.1 recalibrés ; PM v3.34.0 archivé "
          "@historique R4 git mv byte-identité (SHA ac9de174…) ; recalibrage croisé : KB "
          "(en-tête + description n°9 + calibration), pin ECO_SKILLS, "
          "`@historique/historiques-par-skill/gen-plan.md`, lignes vives disciplines, sceaux "
          "README §5, propagation §0 v1.7.23, rescellement archive ; replay arbitres ×2 ; "
          "plan Task 52 généré via v3.35.0 (KO-L005).")


def step2_skill_md():
    """Reconstruit skills/gen-plan/SKILL.md v3.35.0 (subs verrouillées)."""
    path = os.path.join(BASE, "skills", "gen-plan", "SKILL.md")
    with open(path, encoding="utf-8") as f:
        t = f.read()
    # 2a. version frontmatter
    t = sub_locked(t, "version: 3.34.0", "version: 3.35.0", 1, "version frontmatter")
    # 2b. règle d'or n°9 après n°8 (§1.5 — même ancre que le delta PM, count=1 vérifié)
    t = sub_locked(t,
                   "garde post-installation dans l'installateur (0 fichier `PROMPT-MAITRE-*` sous "
                   "`skills/<skill>/` hors corpus autorisés, 0 déploiement `@PM-SKILLS/` — PM-INSTALL "
                   "§3.5, v1.9.0) ; toute dérive détectée = correction puis re-certification par les "
                   "arbitres AVANT toute autre action (§3.3 PM-INSTALL).",
                   "garde post-installation dans l'installateur (0 fichier `PROMPT-MAITRE-*` sous "
                   "`skills/<skill>/` hors corpus autorisés, 0 déploiement `@PM-SKILLS/` — PM-INSTALL "
                   "§3.5, v1.9.0) ; toute dérive détectée = correction puis re-certification par les "
                   "arbitres AVANT toute autre action (§3.3 PM-INSTALL).\n\n" + N9,
                   1, "règle d'or n°9 (§1.5)")
    # 2c. E1-RES : trois → quatre (§1.2bis)
    t = sub_locked(t, "l'étape E1 ouvre par trois vérifications préalables",
                   "l'étape E1 ouvre par quatre vérifications préalables", 1,
                   "E1-RES trois→quatre (§1.2bis)")
    # 2d. E1-RES : insertion du point (4) avant « Provenance : »
    t = sub_locked(t,
                   "le plan est re-généré AVANT toute reprise). Provenance : le hook n67-1",
                   "le plan est re-généré AVANT toute reprise)" + E1RES4 + ". Provenance : le hook n67-1",
                   1, "E1-RES point (4) (§1.2bis)")
    # 2e. bullet §5.6 (avant le bullet v3.34.0)
    t = sub_locked(t, "- **v3.34.0 (2026-11-04, session web-c30e6506",
                   BULLET + "\n- **v3.34.0 (2026-11-04, session web-c30e6506", 1,
                   "bullet §5.6 v3.35.0")
    with open(path, "w", encoding="utf-8") as f:
        f.write(t)


def step3_outillage():
    """Restaure les scripts de session Task 52 (cascade + delta) au dépôt."""
    for f in ["task52-cascade-genplan-v3350.py", "delta-genplan-v3350.json"]:
        src, dst = os.path.join(HOST_SCRIPTS, f), os.path.join(BASE, "scripts", f)
        if not os.path.isfile(src):
            print("ABANDON — script Task 52 absent de l'hôte : %s" % src)
            sys.exit(2)
        if os.path.isfile(dst) and open(src, "rb").read() == open(dst, "rb").read():
            OPS.append("scripts/%s : déjà présent (no-op)" % f)
        else:
            shutil.copy2(src, dst)
            OPS.append("scripts/%s : restauré (session Task 52)" % f)


def step4_verification():
    """Byte-identité corpus ↔ archive (9/9) + cohérence version SKILL.md."""
    corpus = os.path.join(BASE, "skills", "@mon-ecosysteme")
    n_ok = 0
    for f in sorted(os.listdir(RECOVERY)):
        src, dst = os.path.join(RECOVERY, f), os.path.join(corpus, f)
        if os.path.isfile(src) and os.path.isfile(dst) and \
                open(src, "rb").read() == open(dst, "rb").read():
            n_ok += 1
    if n_ok != 9:
        print("ABANDON — byte-identité corpus ↔ archive : %d/9" % n_ok)
        sys.exit(2)
    OPS.append("byte-identité corpus ↔ archive : 9/9")
    head = open(os.path.join(BASE, "skills", "gen-plan", "SKILL.md"), encoding="utf-8").read(200)
    if "version: 3.35.0" not in head:
        print("ABANDON — SKILL.md gen-plan pas en v3.35.0")
        sys.exit(2)
    OPS.append("SKILL.md gen-plan : v3.35.0 confirmé")


def main():
    print("=== Task 53 — Restauration état certifié Task 52 (gen-plan v3.35.0) ===")
    step1_corpus()
    step2_skill_md()
    step3_outillage()
    step4_verification()
    print("=== %d opérations ===" % len(OPS))
    for op in OPS:
        print("  - %s" % op)


if __name__ == "__main__":
    main()
