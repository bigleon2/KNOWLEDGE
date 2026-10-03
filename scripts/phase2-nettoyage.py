# PROVENANCE: session du 2026-10-01 (C2, amendée C0) — recommandation C2 du rapport de simulation @68ff91d ;
# script cree par script-creator (R9, idempotence x2, GF-3) pour periodiser le nettoyage de l'ecosysteme.
# Amendement C0 (exigence propriétaire du 2026-10-01) : AUCUNE suppression n'a lieu sans
# sauvegarde préalable de l'historique d'évolution du fichier (backup-historique.py,
# intégrité sha256 VERIFIEE) — échec de sauvegarde ⇒ suppression annulée (fail-safe).
#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.6.0)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | {{VARIABLE}} | worklog SHARED §1.4
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.

phase2-nettoyage.py — Estimation puis nettoyage PÉRIODIQUE des fichiers inutiles
(recommandation C2 — simulation du 2026-10-01, ancre 68ff91d).
Sauvegarde obligatoire de l'historique d'évolution avant suppression (C0).

Complète phase1-nettoyage.py (purge ponctuelle historique) : conçu pour être
rejoué au fil du projet, en mode CHECK (par défaut, ne modifie rien, estime
le gaspillage) ou en mode --apply (purge effective des catégories sûres).

Garantie C0 (backup-avant-suppression) : en mode --apply, chaque fichier des
catégories 1-6 est d'abord archivé par backup-historique.py (snapshot courant +
versions git antérieures + manifeste sha256 dans .archive-historique/) ; la
suppression n'a lieu QUE si integrite == VERIFIEE. Échec de sauvegarde ⇒
fichier conservé et consigné dans "echecs" (jamais de perte sèche). Les
répertoires vides (catégorie 7) ne contiennent rien à archiver.

Catégories couvertes (liste blanche conservatrice — rien d'autre n'est touché) :
  1. tmp/** plus vieux que 7 jours (artefacts de session périmés)
  2. doublons d'arbitres dans download/ (verify-cross.py, answer-key-checker.py, sync-download.py)
  3. archives *.zip dans download/ (règle .gitignore *.zip)
  4. READMEs stubs brand-inspiration (< 200 caractères contenant getdesign.md)
  5. scripts obsolètes déjà archivés (generate-knowledge-v3.py, generate-clone-genplan.py)
  6. registre racine périmé (KNOWLEDGE.md v3.0.0 à la racine ; registre officiel = skills/KNOWLEDGE.md)
  7. répertoires vides sous scripts/ et skills/

Usage :
    python3 scripts/phase2-nettoyage.py            # CHECK : estimation seule, exit 0
    python3 scripts/phase2-nettoyage.py --apply    # APPLY  : purge effective, exit 0
    python3 scripts/phase2-nettoyage.py --max-age-days 30

Sortie JSON déterministe sur stdout ; code retour 0 = OK (rien à faire ou purge faite),
1 = findings en attente en mode CHECK, 2 = erreur interne.
"""
import argparse
import importlib.util
import json
import os
import sys
import time

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# C0 — chargeur du module de sauvegarde (nom de fichier avec tirets → importlib)
spec = importlib.util.spec_from_file_location(
    "backup_historique", os.path.join(os.path.dirname(os.path.abspath(__file__)), "backup-historique.py"))
try:
    backup_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(backup_mod)
    BACKUP_DISPONIBLE = True
except Exception:  # pragma: no cover — fail-safe : mode dégradé documenté
    backup_mod = None
    BACKUP_DISPONIBLE = False
SKILLS = os.path.join(BASE, "skills")
SCRIPTS = os.path.join(BASE, "scripts")
DOWNLOAD = os.path.join(BASE, "download")
TMP = os.path.join(BASE, "tmp")

DUP_ARBITERS = ["verify-cross.py", "answer-key-checker.py", "sync-download.py"]
OBSOLETE_SCRIPTS = ["generate-knowledge-v3.py", "generate-clone-genplan.py"]
DEFAULT_MAX_AGE_DAYS = 7
STUB_MAX_CHARS = 200
STUB_MARKER = "getdesign.md"


def findings(max_age_days: int):
    """Collecte les findings (catégorie, chemin, octets estimés). Ne modifie rien."""
    out = []
    now = time.time()
    cutoff = now - max_age_days * 86400

    # 1. tmp/ périmé
    if os.path.isdir(TMP):
        for root, dirs, files in os.walk(TMP):
            for f in files:
                p = os.path.join(root, f)
                try:
                    st = os.stat(p)
                except OSError:
                    continue
                if st.st_mtime < cutoff and not os.path.islink(p):
                    out.append(("tmp_perime", p, st.st_size))

    # 2. doublons d'arbitres dans download/
    if os.path.isdir(DOWNLOAD):
        for name in DUP_ARBITERS:
            p = os.path.join(DOWNLOAD, name)
            if os.path.isfile(p) and not os.path.islink(p):
                out.append(("doublon_download", p, os.path.getsize(p)))

    # 3. *.zip dans download/
    if os.path.isdir(DOWNLOAD):
        for f in sorted(os.listdir(DOWNLOAD)):
            p = os.path.join(DOWNLOAD, f)
            if f.lower().endswith(".zip") and os.path.isfile(p) and not os.path.islink(p):
                out.append(("zip_download", p, os.path.getsize(p)))

    # 4. READMEs stubs brand-inspiration
    brand_root = os.path.join(SKILLS, "design", "design-systems", "brand-inspiration")
    if os.path.isdir(brand_root):
        for brand in sorted(os.listdir(brand_root)):
            readme = os.path.join(brand_root, brand, "README.md")
            if os.path.isfile(readme) and not os.path.islink(readme):
                try:
                    with open(readme, "r", encoding="utf-8", errors="replace") as fh:
                        content = fh.read()
                except OSError:
                    continue
                if STUB_MARKER in content and len(content.strip()) < STUB_MAX_CHARS:
                    out.append(("readme_stub", readme, os.path.getsize(readme)))

    # 5. scripts obsolètes déjà archivés
    for name in OBSOLETE_SCRIPTS:
        p = os.path.join(SCRIPTS, name)
        if os.path.isfile(p) and not os.path.islink(p):
            out.append(("script_obsolete", p, os.path.getsize(p)))

    # 6. registre racine périmé
    root_kb = os.path.join(BASE, "KNOWLEDGE.md")
    if os.path.isfile(root_kb) and not os.path.islink(root_kb):
        out.append(("registre_racine", root_kb, os.path.getsize(root_kb)))

    # 7. répertoires vides sous scripts/ et skills/
    for root_dir in (SCRIPTS, SKILLS):
        if not os.path.isdir(root_dir):
            continue
        for root, dirs, files in os.walk(root_dir, topdown=False):
            if "_archive" in root.split(os.sep):
                continue  # l'archive est un dépôt volontaire, on ne la touche pas
            for d in dirs:
                p = os.path.join(root, d)
                if os.path.islink(p):
                    continue
                try:
                    if not os.listdir(p):
                        out.append(("rep_vide", p, 0))
                except OSError:
                    continue
    return out


def apply_cleanup(items):
    """Purge effective APRÈS sauvegarde vérifiée (C0).

    Retourne (supprimés, échecs, sauvegardes). Jamais de suppression hors liste,
    et JAMAIS de suppression sans sauvegarde intégrité-VERIFIEE au préalable.
    """
    cleaned, failed, saved = [], [], []
    for cat, path, _size in items:
        try:
            if cat == "rep_vide":
                os.rmdir(path)  # échoue si non vide entre-temps : garde-fou naturel
                cleaned.append({"categorie": cat, "chemin": path})
                continue
            # C0 — sauvegarde obligatoire de l'historique d'évolution AVANT suppression
            if not BACKUP_DISPONIBLE:
                failed.append({"categorie": cat, "chemin": path,
                               "erreur": "backup-historique indisponible — suppression annulée (fail-safe C0)"})
                continue
            bres = backup_mod.backup_file(path, categorie=cat)
            if not bres.get("sauvegarde") or bres.get("integrite") != "VERIFIEE":
                failed.append({"categorie": cat, "chemin": path,
                               "erreur": f"sauvegarde non vérifiée ({bres.get('erreur', 'intégrité ECHEC')}) — suppression annulée (fail-safe C0)"})
                continue
            saved.append({"chemin": path, "archive": bres.get("archive"), "id": bres.get("id"),
                          "sha256": bres.get("sha256"), "versions_git": bres.get("versions_git", 0),
                          "deja_sauvegarde": bres.get("deja_sauvegarde", False)})
            os.remove(path)
            cleaned.append({"categorie": cat, "chemin": path})
        except OSError as exc:
            failed.append({"categorie": cat, "chemin": path, "erreur": str(exc)})
    return cleaned, failed, saved


def main():
    parser = argparse.ArgumentParser(description="Estimation puis nettoyage périodique (C2)")
    parser.add_argument("--apply", action="store_true", help="purge effective (défaut : CHECK)")
    parser.add_argument("--max-age-days", type=int, default=DEFAULT_MAX_AGE_DAYS,
                        help=f"âge maximal de tmp/ en jours (défaut : {DEFAULT_MAX_AGE_DAYS})")
    args = parser.parse_args()

    items = findings(args.max_age_days)
    by_cat = {}
    for cat, _path, size in items:
        by_cat[cat] = by_cat.get(cat, {"fichiers": 0, "octets": 0})
        by_cat[cat]["fichiers"] += 1
        by_cat[cat]["octets"] += size

    report = {
        "script": "phase2-nettoyage",
        "mode": "APPLY" if args.apply else "CHECK",
        "base": BASE,
        "max_age_days": args.max_age_days,
        "estimation": {"total_fichiers": len(items), "total_octets": sum(s for _, _, s in items)},
        "par_categorie": by_cat,
    }

    if args.apply:
        report["backup_c0"] = {"actif": BACKUP_DISPONIBLE,
                                "politique": "sauvegarde historique d'évolution AVANT suppression ; échec ⇒ suppression annulée",
                                "archive_dir": os.path.join(BASE, ".archive-historique")}
        # Convergence bornée : chaque purge peut dégager de nouveaux répertoires
        # vides (ex. README stub supprimé -> répertoire de marque vide) ; on
        # rejoue estime+purge jusqu'à stabilité, 5 itérations maximum.
        all_cleaned, all_failed, all_saved = [], [], []
        iterations = 0
        for _ in range(5):
            iterations += 1
            items = findings(args.max_age_days)
            if not items:
                break
            cleaned, failed, saved = apply_cleanup(items)
            all_cleaned.extend(cleaned)
            all_failed.extend(failed)
            all_saved.extend(saved)
            if failed:
                break
        reste = len(findings(args.max_age_days))
        report["iterations"] = iterations
        report["sauvegardes"] = all_saved
        report["purges"] = all_cleaned
        report["echecs"] = all_failed
        report["reste"] = {"fichiers": reste}
    else:
        report["attente"] = [{"categorie": c, "chemin": p} for c, p, _ in items]

    print(json.dumps(report, ensure_ascii=False, indent=2))

    if args.apply:
        return 0 if not report["echecs"] else 2
    return 0 if not items else 1


if __name__ == "__main__":
    sys.exit(main())
