#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.12)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

# -*- coding: utf-8 -*-
"""
Task 48 — Étape 1 directive propriétaire : RÉINSTALLATION de l'écosystème personnel
sur le profil local (profil COMPLET).

Contexte : wipe inter-sessions partiel documenté (PM-INSTALL §3.4, règle d'or n°1) —
skills/gen-plan/ et skills/correct-work/ absents du profil local au démarrage de la
session web-38713acd (suite). Le pipeline est ré-exécuté depuis l'étape 2 (corpus
@mon-ecosysteme/ = source de vérité restaurable, clone certifié local).

Source : clone certifié tmp/KNOWLEDGE-repo @ HEAD e62f354 (poussé — GitHub à jour).
Pipeline : PROMPT-MAITRE-INSTALL-ECOSYSTEME.md v1.7.1 — profil COMPLET (défaut §2bis).

Phases (identiques Task 47 D2, idempotentes) :
  A. Sync skills/      — formes installées de TOUTES les entrées (additif)
  B. Sync scripts/     — outillage (arbitres, certification, G-RES, gardes)
  C. Archive           — véhicule d'intégrité download/mon-ecosysteme_archive.zip (garde)
  D. Certification     — certification-complete.py (6 arbitres) depuis le profil local
  E. Marqueur          — install-profile.json rafraîchi (profil COMPLET) + rapport JSON

Idempotence : rejouable — A/B copies déterministes ; C vérifie ; D rejoue ; E réécrit.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time

REPO = "/home/z/my-project/tmp/KNOWLEDGE-repo"
PROFIL = "/home/z/my-project"
RAPPORT = "/home/z/my-project/download/rapport-installation-ecosysteme-task48.json"
SOURCE = "clone certifié @ e62f354 (réinstallation post-wipe inter-sessions, PM-INSTALL §3.4)"

T0 = time.time()
rapport = {"tache": "Task 48 — Étape 1 : réinstallation écosystème (profil COMPLET, post-wipe)",
           "source": SOURCE, "phases": {}, "erreurs": []}


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()[:12]


# ---------- Phase A : sync skills/ ----------
def phase_a():
    src = os.path.join(REPO, "skills")
    dst = os.path.join(PROFIL, "skills")
    ajoutes, sync, inchange = [], [], 0
    for entry in sorted(os.listdir(src)):
        s, d = os.path.join(src, entry), os.path.join(dst, entry)
        if os.path.isdir(s):
            existed = os.path.isdir(d)
            shutil.copytree(s, d, dirs_exist_ok=True)
            (sync if existed else ajoutes).append(entry + "/")
        else:
            existed = os.path.exists(d)
            same = existed and sha(s) == sha(d)
            if not same:
                shutil.copy2(s, d)
                (sync if existed else ajoutes).append(entry)
            else:
                inchange += 1
    return {"ajoutes": ajoutes, "synchronises": sync, "inchanges": inchange,
            "total_entrees_repo": len(os.listdir(src))}


# ---------- Phase B : sync scripts/ ----------
def phase_b():
    src = os.path.join(REPO, "scripts")
    dst = os.path.join(PROFIL, "scripts")
    ajoutes, sync = [], 0
    for root, dirs, files in os.walk(src):
        if "_archive" in root.split(os.sep):
            continue  # _archive/ : archive documentaire interne au repo — non déployée
        rel = os.path.relpath(root, src)
        os.makedirs(os.path.join(dst, rel), exist_ok=True)
        for f in files:
            s, d = os.path.join(root, f), os.path.join(dst, rel, f)
            if os.path.exists(d):
                if sha(s) != sha(d):
                    shutil.copy2(s, d)
                    sync += 1
            else:
                shutil.copy2(s, d)
                ajoutes.append(os.path.join(rel, f))
    return {"ajoutes": len(ajoutes), "synchronises": sync}


# ---------- Phase C : archive (garde) ----------
def phase_c():
    arch = os.path.join(PROFIL, "download", "mon-ecosysteme_archive.zip")
    repo_arch = os.path.join(REPO, "download", "mon-ecosysteme_archive.zip")
    etat = {"archive_profil": os.path.exists(arch), "archive_repo": os.path.exists(repo_arch)}
    if os.path.exists(arch):
        etat["sha_archive_profil"] = sha(arch)
    if os.path.exists(repo_arch):
        etat["sha_archive_repo"] = sha(repo_arch)
    return etat


# ---------- Phase D : certification (6 arbitres) ----------
def phase_d():
    r = subprocess.run([sys.executable, os.path.join(PROFIL, "scripts", "certification-complete.py")],
                       capture_output=True, text=True, cwd=PROFIL, timeout=600)
    return {"rc": r.returncode, "sortie_taille": len(r.stdout),
            "12_dernieres_lignes": "\n".join(r.stdout.strip().splitlines()[-12:]),
            "stderr_extrait": r.stderr.strip()[:400] if r.stderr.strip() else ""}


# ---------- Phase E : marqueur ----------
def phase_e():
    marker = os.path.join(PROFIL, "scripts", "install-profile.json")
    with open(marker, encoding="utf-8") as f:
        m = json.load(f)
    kb = os.path.join(PROFIL, "skills", "KNOWLEDGE.md")
    entrees = sum(1 for l in open(kb, encoding="utf-8", errors="replace")
                  if l.startswith("## ") and " v" in l)
    m["profil"] = "COMPLET"
    m["maj_task48"] = {"source": SOURCE, "kb_entrees": entrees,
                       "contexte": "réinstallation post-wipe inter-sessions (§3.4)"}
    with open(marker, "w", encoding="utf-8") as f:
        json.dump(m, f, ensure_ascii=False, indent=2)
    return {"profil": "COMPLET", "kb_entrees": entrees}


if __name__ == "__main__":
    print("=== Phase A : sync skills/ (COMPLET — additif) ===")
    rapport["phases"]["A_skills"] = phase_a()
    print(json.dumps(rapport["phases"]["A_skills"], ensure_ascii=False)[:600])
    print("\n=== Phase B : sync scripts/ (outillage) ===")
    rapport["phases"]["B_scripts"] = phase_b()
    print(rapport["phases"]["B_scripts"])
    print("\n=== Phase C : archive (garde) ===")
    rapport["phases"]["C_archive"] = phase_c()
    print(rapport["phases"]["C_archive"])
    print("\n=== Phase D : certification (6 arbitres) ===")
    rapport["phases"]["D_certification"] = phase_d()
    print("rc =", rapport["phases"]["D_certification"]["rc"])
    print(rapport["phases"]["D_certification"]["12_dernieres_lignes"])
    print("\n=== Phase E : marqueur install-profile.json ===")
    rapport["phases"]["E_marqueur"] = phase_e()
    print(rapport["phases"]["E_marqueur"])
    rapport["duree_s"] = round(time.time() - T0, 1)
    rapport["verdict"] = ("PASS" if rapport["phases"]["D_certification"]["rc"] == 0 else "AVEC RESERVES")
    with open(RAPPORT, "w", encoding="utf-8") as f:
        json.dump(rapport, f, ensure_ascii=False, indent=2)
    print("\nRapport :", RAPPORT, "— verdict :", rapport["verdict"])
