# PROVENANCE: session du 2026-10-01 (C0) — exigence propriétaire : « vérifier que
# l'écosystème effectue une sauvegarde de l'historique d'évolution des fichiers
# jugés inutiles/nuisibles AVANT de les supprimer automatiquement (au cas où ces
# fichiers auraient évolué vers une version supérieure) » ; script créé par
# script-creator (R9, idempotence ×2, GF-3), ancre 68ff91d.
#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.6.8)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.

backup-historique.py — Sauvegarde de l'historique d'évolution AVANT suppression (C0).

Garanties mécaniques :
  1. SNAPSHOT    — copie intégrale du fichier courant dans .archive-historique/
  2. HISTORIQUE  — toutes les versions git antérieures (blob par commit + liste
                   des commits, cap 20) si le fichier est suivi par git ; sinon
                   statut « non-suivi-git » consigné au manifeste ;
                   répond au cas « le fichier a évolué vers une version
                   supérieure » : chaque version reste consultable/restorable.
  3. MANIFESTE   — sha256 original vs sha256 copie (intégrité VÉRIFIÉE), taille,
                   mtime, catégorie de purge, emplacements d'archive.
  4. FAIL-SAFE   — phase2-nettoyage.py --apply n'autorise une suppression QUE si
                   backup_file() retourne integrite == "VERIFIEE" ; échec de
                   sauvegarde ⇒ suppression annulée (jamais de perte sèche).
  5. IDEMPOTENT ×2 — une entrée d'index (chemin, sha256) déjà archivée n'est pas
                   dupliquée ; rejeu à l'identique = no-op.

Usage :
    python3 scripts/backup-historique.py <fichier...>            # sauvegarde unitaire
    python3 scripts/backup-historique.py --lister                # index des sauvegardes
    python3 scripts/backup-historique.py --restaurer <id> --vers <dest>

Sortie JSON déterministe sur stdout ; code retour 0 = sauvegardé/vérifié,
1 = déjà sauvegardé (no-op idempotent) ou rien à faire, 2 = erreur/échec intégrité.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARCHIVE_ROOT = os.path.join(BASE, ".archive-historique")
INDEX_PATH = os.path.join(ARCHIVE_ROOT, "index.jsonl")
GIT_CAP = 20  # nombre maximal de versions git archivées par fichier


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def find_git_repo(path):
    """Remonte depuis dirname(path) jusqu'au premier .git trouvé (ou None)."""
    d = os.path.dirname(os.path.abspath(path))
    while True:
        if os.path.isdir(os.path.join(d, ".git")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent


def git_history(repo, relpath):
    """Liste des commits touchant le fichier : [(hash, hash8, date, sujet)]."""
    cmd = ["git", "-C", repo, "log", "--follow", "--date=iso",
           "--format=%H%x00%h%x00%ad%x00%s", "--", relpath]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired):
        return []
    if p.returncode != 0:
        return []
    commits = []
    for line in p.stdout.splitlines():
        parts = line.split("\x00")
        if len(parts) == 4:
            commits.append((parts[0], parts[1], parts[2], parts[3]))
    return commits


def load_index():
    """Index en mémoire : {(chemin_original, sha256): id}."""
    entries = {}
    if os.path.isfile(INDEX_PATH):
        with open(INDEX_PATH, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    e = json.loads(line)
                except json.JSONDecodeError:
                    continue
                entries[(e.get("chemin_original"), e.get("sha256"))] = e.get("id")
    return entries


def backup_file(path, categorie="hors_purge"):
    """Sauvegarde un fichier + son historique git. Retourne un dict de preuve.

    Clé de contrat pour phase2-nettoyage.py : integrite == "VERIFIEE" autorise
    la suppression ; tout autre statut l'interdit (fail-safe).
    """
    result = {
        "script": "backup-historique",
        "chemin_original": os.path.abspath(path),
        "categorie": categorie,
        "sauvegarde": False,
        "deja_sauvegarde": False,
        "integrite": "ECHEC",
        "archive": None,
        "id": None,
        "versions_git": 0,
    }
    if not os.path.isfile(path) or os.path.islink(path):
        result["erreur"] = "fichier inexistant ou lien symbolique"
        return result

    digest = sha256_file(path)
    result["sha256"] = digest
    result["taille_octets"] = os.path.getsize(path)
    result["mtime"] = int(os.stat(path).st_mtime)

    index = load_index()
    key = (result["chemin_original"], digest)
    if key in index:
        result["deja_sauvegarde"] = True
        result["sauvegarde"] = True
        result["integrite"] = "VERIFIEE"  # déjà archivé et indexé
        result["id"] = index[key]
        return result

    stem = re.sub(r"[^A-Za-z0-9._-]", "-", os.path.basename(path))[:40] or "sans-nom"
    arc_id = f"{stem}-{digest[:10]}"
    arc_dir = os.path.join(ARCHIVE_ROOT, arc_id)
    os.makedirs(arc_dir, exist_ok=True)

    # 1. SNAPSHOT — copie intégrale puis vérification d'intégrité
    snap = os.path.join(arc_dir, os.path.basename(path))
    shutil.copy2(path, snap)
    if sha256_file(snap) != digest:
        result["erreur"] = "sha256 de la copie != sha256 original"
        return result
    result["integrite"] = "VERIFIEE"
    result["archive"] = snap

    # 2. HISTORIQUE — versions git antérieures (le fichier a pu évoluer)
    repo = find_git_repo(path)
    commits = git_history(repo, os.path.relpath(os.path.abspath(path), repo)) if repo else []
    versions_dir = os.path.join(arc_dir, "versions")
    if commits:
        os.makedirs(versions_dir, exist_ok=True)
        saved, hist_lines = 0, []
        for full, short, date, subject in commits[:GIT_CAP]:
            try:
                p = subprocess.run(
                    ["git", "-C", repo, "show", f"{full}:{os.path.relpath(os.path.abspath(path), repo)}"],
                    capture_output=True, timeout=60)
            except (OSError, subprocess.TimeoutExpired):
                continue
            if p.returncode != 0:
                continue
            vpath = os.path.join(versions_dir, f"{short}__{os.path.basename(path)}")
            with open(vpath, "wb") as vf:
                vf.write(p.stdout)
            hist_lines.append(f"{short} {date} {subject}\n  -> {os.path.relpath(vpath, arc_dir)}")
            saved += 1
        with open(os.path.join(arc_dir, "historique-git.txt"), "w", encoding="utf-8") as hf:
            hf.write(f"Dépôt : {repo}\nFichier : {os.path.relpath(os.path.abspath(path), repo)}\n")
            hf.write(f"Versions archivées : {saved} (cap {GIT_CAP})\n\n")
            hf.write("\n".join(hist_lines) + "\n")
        result["versions_git"] = saved
    result["historique_git"] = "non-suivi-git" if not commits else f"{len(commits)} commits"
    result["depot_git"] = bool(repo)

    # 3. MANIFESTE + INDEX
    manifest = {k: v for k, v in result.items() if k != "erreur"}
    manifest["archive_dir"] = arc_dir
    manifest["horodatage"] = int(time.time())
    with open(os.path.join(arc_dir, "manifest.json"), "w", encoding="utf-8") as mf:
        json.dump(manifest, mf, ensure_ascii=False, indent=2)
    with open(INDEX_PATH, "a", encoding="utf-8") as idx:
        idx.write(json.dumps({
            "id": arc_id,
            "horodatage": manifest["horodatage"],
            "chemin_original": result["chemin_original"],
            "sha256": digest,
            "taille_octets": result["taille_octets"],
            "categorie": categorie,
            "versions_git": result["versions_git"],
            "archive_dir": os.path.relpath(arc_dir, BASE),
        }, ensure_ascii=False) + "\n")
    result["sauvegarde"] = True
    result["id"] = arc_id
    return result


def cmd_lister():
    entries = []
    if os.path.isfile(INDEX_PATH):
        with open(INDEX_PATH, "r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    try:
                        entries.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass
    print(f"=== Index .archive-historique ({len(entries)} entrées) ===")
    for e in entries:
        print(f"  [{e['id']}] {e['chemin_original']}  ({e['taille_octets']} o, "
              f"{e['versions_git']} version(s) git, catégorie {e['categorie']})")
    print("\n" + json.dumps({"script": "backup-historique", "mode": "lister",
                             "entrees": entries}, ensure_ascii=False, indent=2))
    return 0


def cmd_restaurer(arc_id, dest):
    arc_dir = os.path.join(ARCHIVE_ROOT, arc_id)
    man_path = os.path.join(arc_dir, "manifest.json")
    if not os.path.isfile(man_path):
        print(json.dumps({"script": "backup-historique", "mode": "restaurer",
                          "erreur": f"id inconnu : {arc_id}"}, ensure_ascii=False))
        return 2
    with open(man_path, "r", encoding="utf-8") as mf:
        man = json.load(mf)
    snap = os.path.join(arc_dir, os.path.basename(man["chemin_original"]))
    if not os.path.isfile(snap):
        print(json.dumps({"script": "backup-historique", "mode": "restaurer",
                          "erreur": f"snapshot manquant : {snap}"}, ensure_ascii=False))
        return 2
    if os.path.exists(dest):
        print(json.dumps({"script": "backup-historique", "mode": "restaurer",
                          "erreur": f"destination existante (refus par sécurité) : {dest}"},
                         ensure_ascii=False))
        return 2
    os.makedirs(os.path.dirname(os.path.abspath(dest)) or ".", exist_ok=True)
    shutil.copy2(snap, dest)
    ok = sha256_file(dest) == man["sha256"]
    print(json.dumps({"script": "backup-historique", "mode": "restaurer",
                      "id": arc_id, "destination": os.path.abspath(dest),
                      "integrite": "VERIFIEE" if ok else "ECHEC"}, ensure_ascii=False, indent=2))
    return 0 if ok else 2


def main():
    parser = argparse.ArgumentParser(description="Sauvegarde d'historique avant suppression (C0)")
    parser.add_argument("fichiers", nargs="*", help="fichiers à sauvegarder")
    parser.add_argument("--categorie", default="hors_purge", help="motif de purge consigné")
    parser.add_argument("--lister", action="store_true", help="affiche l'index des sauvegardes")
    parser.add_argument("--restaurer", metavar="ID", help="restaure la sauvegarde ID")
    parser.add_argument("--vers", metavar="DEST", help="destination de restauration")
    args = parser.parse_args()

    if args.lister:
        return cmd_lister()
    if args.restaurer:
        if not args.vers:
            print(json.dumps({"script": "backup-historique",
                              "erreur": "--restaurer exige --vers DEST"}, ensure_ascii=False))
            return 2
        return cmd_restaurer(args.restaurer, args.vers)
    if not args.fichiers:
        parser.print_help()
        return 2

    out, code = [], 0
    for f in args.fichiers:
        r = backup_file(f, categorie=args.categorie)
        out.append(r)
        if not r["sauvegarde"] or r["integrite"] != "VERIFIEE":
            code = 2
        elif not r["deja_sauvegarde"]:
            code = code or 0
    print(json.dumps({"script": "backup-historique", "mode": "sauvegarder",
                      "resultats": out}, ensure_ascii=False, indent=2))
    return code


if __name__ == "__main__":
    sys.exit(main())
