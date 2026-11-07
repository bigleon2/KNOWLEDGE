#!/usr/bin/env python3
"""⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.31)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).

Inventaire mécanique de l'écosystème — Task 70 G4/SG4.1 (T4.1.1 + T4.1.2).
Mesures terrain pour l'étude de faisabilité performance (OOP / noyau) :
comptages fichiers, volumes, profondeur, répartition par type, tailles SKILL.md,
et temps de lecture séquentielle de l'arbre (baseline arbre vs lecture zippée).
Sortie : JSON sur stdout (rejeu stable — idempotence R6).
"""

import json
import os
import sys
import time
import zipfile

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(BASE, "skills")
SCRIPTS = os.path.join(BASE, "scripts")


def inventaire():
    data = {"skills": {}, "total": {}}
    tous = []
    for racine in (SKILLS, SCRIPTS):
        for dirpath, _dirs, files in os.walk(racine):
            if "__pycache__" in dirpath or ".git" in dirpath:
                continue
            for f in files:
                p = os.path.join(dirpath, f)
                try:
                    taille = os.path.getsize(p)
                except OSError:
                    continue
                tous.append((p, taille))
    nb = len(tous)
    octets = sum(t for _, t in tous)
    data["total"] = {
        "fichiers": nb,
        "octets": octets,
        "mio": round(octets / 1024 / 1024, 2),
    }
    # Répartition par extension
    ext = {}
    for p, t in tous:
        e = os.path.splitext(p)[1].lower() or "(sans-ext)"
        c = ext.setdefault(e, [0, 0])
        c[0] += 1
        c[1] += t
    data["par_extension"] = {e: {"n": v[0], "octets": v[1]} for e, v in
                             sorted(ext.items(), key=lambda kv: -kv[1][1])}
    # Nombre de dossiers de skills (dont collections @)
    entrees = sorted(os.listdir(SKILLS))
    data["skills"]["dossiers"] = len(entrees)
    data["skills"]["collections_at"] = [e for e in entrees if e.startswith("@")]
    # SKILL.md : nombre + taille cumulée
    sm = [(p, t) for p, t in tous if os.path.basename(p) == "SKILL.md"]
    data["skills"]["skill_md"] = {
        "n": len(sm),
        "octets": sum(t for _, t in sm),
        "kio_moyen": round(sum(t for _, t in sm) / len(sm) / 1024, 1) if sm else 0,
    }
    # Profondeur max sous skills/
    prof = 0
    for dirpath, _d, _f in os.walk(SKILLS):
        prof = max(prof, dirpath[len(SKILLS):].count(os.sep))
    data["skills"]["profondeur_max"] = prof
    # Scripts .py racine
    pys = [(p, t) for p, t in tous if p.endswith(".py")]
    data["scripts_py"] = {"n": len(pys), "octets": sum(t for _, t in pys)}
    return data


def mesure_temps():
    """Baseline arbre : lecture séquentielle de tous les fichiers (cold-ish cache
    OS), vs lecture des mêmes contenus depuis un zip unique (simulation noyau)."""
    chemins = []
    for racine in (SKILLS, SCRIPTS):
        for dirpath, _dirs, files in os.walk(racine):
            if "__pycache__" in dirpath or ".git" in dirpath:
                continue
            for f in files:
                p = os.path.join(dirpath, f)
                if os.path.isfile(p):
                    chemins.append(p)
    # Arbre : open() par fichier
    t0 = time.perf_counter()
    lus = 0
    for p in chemins:
        with open(p, "rb") as fh:
            fh.read()
        lus += 1
    t_arbre = time.perf_counter() - t0
    # Zip unique (simulation noyau) : écriture puis lecture intégrale
    zpath = os.path.join(BASE, "tmp", "task70-simulation-noyau.zip")
    os.makedirs(os.path.dirname(zpath), exist_ok=True)
    t0 = time.perf_counter()
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for p in chemins:
            z.write(p, os.path.relpath(p, BASE))
    t_zip_ecriture = time.perf_counter() - t0
    taille_zip = os.path.getsize(zpath)
    t0 = time.perf_counter()
    with zipfile.ZipFile(zpath) as z:
        for nom in z.namelist():
            z.read(nom)
    t_zip_lecture = time.perf_counter() - t0
    # Re-lecture arbre (cache chaud — pour honnêteté)
    t0 = time.perf_counter()
    for p in chemins:
        with open(p, "rb") as fh:
            fh.read()
    t_arbre_chaud = time.perf_counter() - t0
    os.remove(zpath)
    return {
        "fichiers_lus": lus,
        "arbre_froid_s": round(t_arbre, 3),
        "arbre_chaud_s": round(t_arbre_chaud, 3),
        "zip_ecriture_s": round(t_zip_ecriture, 3),
        "zip_lecture_s": round(t_zip_lecture, 3),
        "zip_octets": taille_zip,
        "zip_mio": round(taille_zip / 1024 / 1024, 2),
    }


def main():
    rapport = {"inventaire": inventaire(), "temps": mesure_temps()}
    json.dump(rapport, sys.stdout, ensure_ascii=False, indent=1)
    print()


if __name__ == "__main__":
    main()
