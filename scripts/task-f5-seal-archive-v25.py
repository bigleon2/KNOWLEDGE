#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task F5 — scellement archive v2.5 (corpus + piliers) — discrimination PERTE / ÉVOLUTION / DÉPLACEMENT R4.

Correctif structurel du différé consigné (constat Task 12, session web-93a4f011 —
« garde anti-perte du scelleur v2.4 ne modélise pas le déplacement R4
corpus→@historique (véhicule régénéré par la voie canonique, correctif futur
possible sur directive) » ; directive Task 16 trace 1a1fbe9f0ef279fd « corrige
tous les différés consignés ») : la garde anti-perte du véhicule v2.4 traitait
TOUTE entrée corpus de l'archive entrante sans contrepartie locale comme une
PERTE (rc=2), y compris le DÉPLACEMENT R4 de déduplication N27 (PM corpus →
skills/@historique/prompts-maitres/<skill>/ — contenu byte-identique préservé),
forçant le contournement manuel documenté « régénération du véhicule depuis
l'état canonique commité » (Tasks 11/12).

Le véhicule v2.5 DISCRIMINE :

  PERTE        entrée « @mon-ecosysteme/<f> » de l'archive ENTRANTE sans
               contrepartie locale ET sans contrepartie byte-identique sous
               skills/@historique/prompts-maitres/<skill>/ → ECHEC rc=2,
               JAMAIS contournable (sémantique anti-perte v2.3 inchangée —
               aucune perte silencieuse) ;
  DÉPLACEMENT  entrée corpus sans contrepartie locale MAIS contenu byte-
  R4           identique présent sous skills/@historique/prompts-maitres/
               <skill>/<f> (convention R4/N27 — l'information vit à sa source
               d'archive) → rescellement AUTORISÉ, TRACÉ « déplacement R4
               légitime (corpus → @historique/prompts-maitres) » — l'archive
               scellée reflète le corpus canonique COURANT (l'entrée déplacée
               n'y figure plus ; le contenu reste vérifiable dans @historique) ;
  ÉVOLUTION    divergence (fichier présent des deux côtés, octets différents) :
               - contenu local == contenu commité au HEAD d'un dépôt git qui suit
                 le corpus (chaîne : BASE puis --depot-git) → rescellement
                 AUTORISÉ, tracé « évolution légitime (git) » (v2.4 inchangé) ;
               - contenu local NON prouvé commité → ECHEC rc=3 + guidance
                 (committer l'évolution, ou passer --depot-git <chemin>, ou
                 --autoriser-evolution = acceptation explicite de l'opérateur) ;
               - drapeau --autoriser-evolution → acceptation explicite TRACÉE
                 (évolution en cours de tour, pas encore commitée).

Processus (hérité v2.3/v2.4, inchangé par ailleurs) :
  1. sauvegarde .bak de l'archive entrante + lecture des entrées ;
  2. construction v2.5 = @mon-ecosysteme/* (corpus courant) + piliers/* (6 fichiers
     critiques) — les déplacements R4 y sortent naturellement du périmètre scellé ;
  3. auto-vérification round-trip complète (entrées byte-identiques) ;
  4. rollback depuis .bak en cas d'échec (rc=1) ; .bak supprimée après succès.
Idempotent : re-exécution sur état scellé = re-scellement équivalent.
Byte-stable (Task 100, mission F1) : ZipInfo explicite à époque fixe 1980-01-01
pour TOUTES les entrées — re-scellements successifs et sur trees distincts
produisent des octets IDENTIQUES (parité v2.4/v2.5 prouvée par harnais Task 16).
Racines dérivées de __file__ (L008 — portabilité des chemins).
Codes retour : 0 = scellée · 1 = échec round-trip (archive restaurée) ·
2 = PERTE anti-perte · 3 = divergence non prouvée commitée (guidance).

Usage :
  task-f5-seal-archive-v25.py [--depot-git <chemin-dépôt>] [--autoriser-evolution]
"""
# ⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.46)
# SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
# Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
# Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
# Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
# Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
# Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).

import argparse
import hashlib
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
CORPUS = BASE / "skills" / "@mon-ecosysteme"
HISTORIQUE_PROMPTS = BASE / "skills" / "@historique" / "prompts-maitres"
ARCHIVE = BASE / "download" / "mon-ecosysteme_archive.zip"
BAK = ARCHIVE.with_suffix(".zip.bak")
PILIERS = {
    "piliers/skills/gen-plan/SKILL.md": BASE / "skills" / "gen-plan" / "SKILL.md",
    "piliers/skills/correct-work/SKILL.md": BASE / "skills" / "correct-work" / "SKILL.md",
    "piliers/skills/KNOWLEDGE.md": BASE / "skills" / "KNOWLEDGE.md",
    "piliers/scripts/certification-complete.py": BASE / "scripts" / "certification-complete.py",
    "piliers/scripts/check-ecosysteme-integrity.py": BASE / "scripts" / "check-ecosysteme-integrity.py",
    "piliers/scripts/install-ecosysteme-local.sh": BASE / "scripts" / "install-ecosysteme-local.sh",
}


def sha(p: Path) -> str:
    """SHA-256 hexadécimal du fichier (empreinte round-trip)."""
    return hashlib.sha256(p.read_bytes()).hexdigest()


def octets_commites(fichier: str, racines_git: list) -> bytes | None:
    """Octets du fichier du corpus tels que commités au HEAD du PREMIER dépôt qui le suit.

    Chaîne : BASE d'abord, puis les racines --depot-git (le pipeline passe le dépôt
    canonique) ; None = engagement non prouvable (fichier non suivi / pas de dépôt).
    """
    rel = "skills/@mon-ecosysteme/" + fichier
    for racine in racines_git:
        r = subprocess.run(["git", "-C", str(racine), "show", "HEAD:" + rel],
                           capture_output=True)
        if r.returncode == 0:
            return r.stdout
    return None


def contrepartie_r4(nom: str, octets_archive: bytes) -> Path | None:
    """Contrepartie de DÉPLACEMENT R4 : chemin @historique/prompts-maitres/<skill>/<nom> byte-identique.

    Convention N27/R4 (déduplication corpus) : un PM supersédé vit à sa source
    d'archive skills/@historique/prompts-maitres/<skill>/<nom> — contenu IDENTIQUE
    à l'octet près. None = aucune contrepartie byte-identique (perte réelle).
    """
    if not HISTORIQUE_PROMPTS.is_dir():
        return None
    for cible in sorted(HISTORIQUE_PROMPTS.glob("*/" + nom)):
        if cible.is_file() and cible.read_bytes() == octets_archive:
            return cible
    return None


def main() -> int:
    """Point d'entrée : garde anti-perte (PERTE/DÉPLACEMENT R4/ÉVOLUTION) puis scellement round-trip.

    Codes retour : 0 scellée · 1 échec round-trip (archive restaurée) · 2 PERTE ·
    3 divergence non prouvée commitée.
    """
    ap = argparse.ArgumentParser(description="Scelleur archive v2.5 (corpus + piliers) — discrimination PERTE/ÉVOLUTION/DÉPLACEMENT R4")
    ap.add_argument("--depot-git", type=Path, default=None,
                    help="chemin d'un dépôt git suivant le corpus (source de vérité de l'engagement)")
    ap.add_argument("--autoriser-evolution", action="store_true",
                    help="acceptation EXPLICITE de l'opérateur : resceller une divergence non commitée (tracée)")
    args = ap.parse_args()

    corpus_fichiers = sorted(p.name for p in CORPUS.glob("*.md"))
    print(f"corpus : {len(corpus_fichiers)} fichiers .md ; piliers à sceller : {len(PILIERS)}")
    for arc, src in sorted(PILIERS.items()):
        if not src.exists():
            print(f"ECHEC : pilier absent : {src}")
            return 2

    old = {}
    if ARCHIVE.exists():
        shutil.copy2(ARCHIVE, BAK)
        with zipfile.ZipFile(BAK) as z:
            old = {n: z.read(n) for n in z.namelist() if not n.endswith("/")}
    print(f"archive entrante : {len(old)} entrées")

    # Garde anti-perte — PERTE / DÉPLACEMENT R4 (v2.5, correctif Task 16) :
    # une entrée corpus de l'archive ENTRANTE sans contrepartie locale serait
    # perdue par le rescellement → blocage systématique, SAUF contrepartie
    # byte-identique sous @historique/prompts-maitres/<skill>/ (déplacement R4
    # de déduplication — l'information vit à sa source d'archive, tracé).
    perdus = []
    deplacements = []
    for f in sorted(old):
        if f.startswith("@mon-ecosysteme/") and f.endswith(".md") and Path(f).name not in corpus_fichiers:
            cible = contrepartie_r4(Path(f).name, old[f])
            if cible is not None:
                deplacements.append((f, cible))
            else:
                perdus.append(f)
    if perdus:
        print(f"ECHEC anti-perte : entrées d'archive sans contrepartie locale ni déplacement R4 : {perdus}")
        return 2
    for f, cible in deplacements:
        print(f"déplacement R4 légitime (corpus → @historique/prompts-maitres) : {f} → {cible.relative_to(BASE)}")

    # Garde anti-perte — ÉVOLUTION (v2.4, correctif F2) : discrimination
    # dérive / évolution légitime par preuve d'engagement git.
    divergents = [f for f in corpus_fichiers
                  if f"@mon-ecosysteme/{f}" in old
                  and old[f"@mon-ecosysteme/{f}"] != (CORPUS / f).read_bytes()]
    if divergents:
        if args.autoriser_evolution:
            print(f"évolution AUTORISÉE explicitement (--autoriser-evolution) : {divergents}")
        else:
            racines_git = [BASE] + ([args.depot_git] if args.depot_git else [])
            non_prouves = []
            for f in divergents:
                commites = octets_commites(f, racines_git)
                if commites is None or commites != (CORPUS / f).read_bytes():
                    non_prouves.append(f)
            if non_prouves:
                print(f"ECHEC évolution non prouvée commitée : {non_prouves}")
                print("guidance : committer l'évolution dans le dépôt qui suit le corpus, "
                      "ou passer --depot-git <chemin-dépôt>, ou --autoriser-evolution "
                      "(acceptation explicite de l'opérateur).")
                return 3
            print(f"évolution légitime (git) : {divergents}")

    EPOQUE_FIXE = (1980, 1, 1, 0, 0, 0)  # Task 100 (mission F1) : byte-stabilité R6

    with zipfile.ZipFile(ARCHIVE, "w", zipfile.ZIP_DEFLATED) as z:
        for f in corpus_fichiers:
            zi = zipfile.ZipInfo(f"@mon-ecosysteme/{f}", date_time=EPOQUE_FIXE)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            z.writestr(zi, (CORPUS / f).read_bytes())
        for arc, src in sorted(PILIERS.items()):
            zi = zipfile.ZipInfo(arc, date_time=EPOQUE_FIXE)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            z.writestr(zi, src.read_bytes())

    with zipfile.ZipFile(ARCHIVE) as z:
        noms = [n for n in z.namelist() if not n.endswith("/")]
        div_corpus = [f for f in corpus_fichiers if z.read(f"@mon-ecosysteme/{f}") != (CORPUS / f).read_bytes()]
        div_piliers = [a for a in PILIERS if z.read(a) != PILIERS[a].read_bytes()]
    attendu = len(corpus_fichiers) + len(PILIERS)
    print(f"nouvelle archive : {len(noms)} entrées (attendu {attendu}) ; "
          f"divergences : corpus={div_corpus or '—'} piliers={div_piliers or '—'}")
    if div_corpus or div_piliers or len(noms) != attendu:
        shutil.copy2(BAK, ARCHIVE)
        print("ÉCHEC — archive restaurée depuis la sauvegarde")
        return 1
    if BAK.exists():
        BAK.unlink()
    print("Archive v2.5 scellée (corpus + piliers) — round-trip vérifié.")
    print("Pense-bête : exécuter ensuite l'arbitre en mode COMPLET pour régénérer le manifeste (SHA archive + entrées piliers).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
