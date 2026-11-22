#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 16 — Harnais de test du scelleur v2.5 (correctif structurel du différé R4).

Règle d'or n°5 (mesurer avant corriger) : monte un bac à sable — mini-arbre
(skills/@mon-ecosysteme 9 corpus SYNTHÉTIQUES + 6 piliers + scelleurs v2.4/v2.5
+ skills/@historique/prompts-maitres/ + download/) avec DÉPÔT GIT LOCAL initialisé
et commité — puis exécute la matrice du correctif (différé consigné Task 12,
directive trace 1a1fbe9f0ef279fd « corrige tous les différés consignés ») :

  T0  état propre → rc=0, 15 entrées, round-trip ; idempotence byte-stable ×2
  T0b idempotence initiale ×2 byte-stable
  T1  ÉVOLUTION LÉGITIME COMMITÉE (bump corpus + git commit) → rc=0 SANS ECHEC
      ni intervention manuelle, tracé « évolution légitime (git) » (v2.4 hérité)
  T2  PERTE (entrée d'archive sans contrepartie locale NI @historique) → rc=2
      bloqué, archive inchangée (sémantique anti-perte v2.3 préservée)
  T3  divergence NON commitée → rc=3 + guidance, archive inchangée
  T3b --autoriser-evolution → rc=0, acceptation EXPLICITE tracée
  T3c restauration git checkout → divergence résorbée voie mécanique → rc=0
  T4  idempotence finale ×2 byte-stable
  T5  parité v2.4/v2.5 sur état propre — SHA d'archive IDENTIQUES (EPOQUE_FIXE)
  T6  DÉPLACEMENT R4 avec v2.4 → rc=2 FAUX POSITIF (le différé démontré :
      entrée corpus déplacée byte-identique vers @historique bloquée PERTE)
  T6b DÉPLACEMENT R4 avec v2.5 → rc=0 TRACÉ « déplacement R4 légitime », entrée
      absente de la nouvelle archive, contenu byte-identique préservé
      dans @historique/prompts-maitres/<skill>/ (LE CORRECTIF)
  T7  PERTE RÉELLE (suppression corpus SANS contrepartie @historique) avec
      v2.5 → rc=2 bloqué, archive inchangée (anti-perte INTACT malgré le
      correctif — aucune perte silencieuse permise)
  T8  restauration git + re-scellement v2.5 → rc=0 (retour état scellé)

Lecture seule sur l'arbre réel (copies vers bac à sable tempfile).
Sortie : verdicts par cas + résumé ; rc 0 ssi tous PASS (13/13).
"""

# ⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.45)
# SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
# Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
# Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
# Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
# Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
# Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).

import hashlib
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

HOTE = Path("/home/z/my-project")
SCELLEUR_V25 = HOTE / "scripts" / "task-f5-seal-archive-v25.py"
SCELLEUR_V24 = HOTE / "scripts" / "task-f5-seal-archive-v24.py"

CORPUS_NOMS = [
    "PROMPT-MAITRE-CLONE-CHAT.md", "PROMPT-MAITRE-CORRECT-WORK.md",
    "PROMPT-MAITRE-GEN-PLAN.md", "PROMPT-MAITRE-INSTALL-ECOSYSTEME.md",
    "PROMPT-MAITRE-REFACTOR-GUARD.md", "PROMPT-MAITRE-SHARED.md",
    "PROMPT-ULTRA-MAITRE-ORCHESTRATION.md", "README.md", "SYNC-CONTEXT.md",
]
PILIERS_REL = [
    "skills/gen-plan/SKILL.md", "skills/correct-work/SKILL.md", "skills/KNOWLEDGE.md",
    "scripts/certification-complete.py", "scripts/check-ecosysteme-integrity.py",
    "scripts/install-ecosysteme-local.sh",
]


def shell(cwd: Path, *args: str) -> subprocess.CompletedProcess:
    """Exécuter une commande dans le bac à sable (sortie capturée)."""
    return subprocess.run(list(args), capture_output=True, text=True, cwd=str(cwd))


def sceller(base: Path, véhicule: str = "v25", *options: str) -> subprocess.CompletedProcess:
    """Exécuter le scelleur du bac à sable (v25 par défaut, v24 pour parité/différé)."""
    return shell(base, sys.executable, str(base / "scripts" / f"task-f5-seal-archive-{véhicule}.py"), *options)


def sha_archive(base: Path) -> str:
    """SHA-256 de l'archive du bac à sable (stabilité byte)."""
    return hashlib.sha256((base / "download" / "mon-ecosysteme_archive.zip").read_bytes()).hexdigest()


def lire_entree(base: Path, nom: str) -> bytes:
    """Lire les octets d'une entrée de l'archive du bac à sable."""
    with zipfile.ZipFile(base / "download" / "mon-ecosysteme_archive.zip") as z:
        return z.read(nom)


def noms_entrees(base: Path) -> list:
    """Lister les entrées fichiers de l'archive du bac à sable."""
    with zipfile.ZipFile(base / "download" / "mon-ecosysteme_archive.zip") as z:
        return [n for n in z.namelist() if not n.endswith("/")]


def monter_sandbox(base: Path) -> None:
    """Mini-arbre + dépôt git local : 9 corpus synthétiques + 6 piliers + scelleurs + @historique."""
    (base / "skills" / "@mon-ecosysteme").mkdir(parents=True)
    for i, nom in enumerate(CORPUS_NOMS):
        (base / "skills" / "@mon-ecosysteme" / nom).write_text(
            "# %s (corpus synthétique %d)\n\nContenu factice v1 — bac à sable Task 16.\n" % (nom, i), encoding="utf-8")
    for rel in PILIERS_REL:
        p = base / rel  # rel est relatif à BASE (préfixes skills/ et scripts/ explicites)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("# pilier synthétique : %s\n" % rel, encoding="utf-8")
    (base / "scripts").mkdir(exist_ok=True)
    (base / "download").mkdir(exist_ok=True)
    shutil.copy2(SCELLEUR_V25, base / "scripts" / "task-f5-seal-archive-v25.py")
    shutil.copy2(SCELLEUR_V24, base / "scripts" / "task-f5-seal-archive-v24.py")
    # Arbre @historique/prompts-maitres/<skill>/ (convention R4/N27 — vide à l'état propre)
    (base / "skills" / "@historique" / "prompts-maitres" / "gen-plan").mkdir(parents=True)
    assert shell(base, "git", "init", "-q").returncode == 0
    assert shell(base, "git", "config", "user.email", "test@local").returncode == 0
    assert shell(base, "git", "config", "user.name", "test-task16").returncode == 0
    assert shell(base, "git", "add", "-A").returncode == 0
    assert shell(base, "git", "commit", "-qm", "état initial bac à sable").returncode == 0


def main() -> int:
    """Point d'entrée : monter le bac à sable puis exécuter la matrice T0-T8 (13 cas).

    rc 0 ssi tous les cas PASS (13/13) — lecture seule sur l'arbre réel.
    """
    tmp = Path(tempfile.mkdtemp(prefix="task16-scelleur-"))
    res = []

    def add(cas, ok, detail):
        """Enregistrer et imprimer le verdict d'un cas de la matrice."""
        res.append((cas, bool(ok), detail))
        print("  [%s] %s — %s" % ("PASS" if ok else "FAIL", cas, detail))

    try:
        base = tmp / "arbre"
        base.mkdir()
        monter_sandbox(base)

        # T0 — état propre (véhicule v2.5)
        r = sceller(base)
        add("T0: état propre scellé rc=0 (15 entrées)", r.returncode == 0 and "15 entrées" in r.stdout,
            "rc=%d · %s" % (r.returncode, (r.stdout or r.stderr).strip()[-140:]))
        sha_1 = sha_archive(base)
        r = sceller(base)
        add("T0b: idempotence initiale byte-stable", r.returncode == 0 and sha_archive(base) == sha_1, "SHA stable ×2")

        # T1 — évolution légitime commitée (v2.4 hérité)
        cible = base / "skills" / "@mon-ecosysteme" / "PROMPT-MAITRE-SHARED.md"
        cible.write_text(cible.read_text(encoding="utf-8") + "\nÉVOLUTION LÉGITIME v2 — bump commité (Task 16 T1).\n", encoding="utf-8")
        assert shell(base, "git", "add", "-A").returncode == 0
        assert shell(base, "git", "commit", "-qm", "bump corpus").returncode == 0
        r = sceller(base)
        octets = lire_entree(base, "@mon-ecosysteme/PROMPT-MAITRE-SHARED.md")
        add("T1: bump corpus commité rescellé SANS ECHEC (rc=0, tracé git)",
            r.returncode == 0 and "évolution légitime (git)" in r.stdout
            and "ÉVOLUTION LÉGITIME v2".encode("utf-8") in octets,
            "rc=%d · voie mécanique héritée v2.4" % r.returncode)

        # T2 — PERTE sans contrepartie NI @historique
        sha_avant = sha_archive(base)
        (base / "skills" / "@mon-ecosysteme" / "README.md").unlink()
        r = sceller(base)
        add("T2: PERTE bloquée rc=2, archive inchangée",
            r.returncode == 2 and "anti-perte" in r.stdout and sha_archive(base) == sha_avant,
            "rc=%d · sémantique v2.3 préservée" % r.returncode)
        shell(base, "git", "checkout", "-q", "--", "skills/@mon-ecosysteme/README.md")

        # T3 — divergence non commitée
        sha_avant = sha_archive(base)
        cible.write_text(cible.read_text(encoding="utf-8") + "\nDIVERGENCE NON COMMITÉE — Task 16 T3.\n", encoding="utf-8")
        r = sceller(base)
        add("T3: divergence non commitée → rc=3 + guidance",
            r.returncode == 3 and "guidance" in r.stdout and sha_archive(base) == sha_avant,
            "rc=%d · archive inchangée" % r.returncode)

        # T3b — drapeau d'acceptation explicite
        r = sceller(base, "v25", "--autoriser-evolution")
        add("T3b: --autoriser-evolution → rc=0 tracé",
            r.returncode == 0 and "AUTORISÉE explicitement" in r.stdout
            and "DIVERGENCE NON COMMITÉE".encode("utf-8") in lire_entree(base, "@mon-ecosysteme/PROMPT-MAITRE-SHARED.md"),
            "rc=%d · acceptation explicite de l'opérateur" % r.returncode)

        # T3c — restauration + résorption mécanique
        shell(base, "git", "checkout", "-q", "--", "skills/@mon-ecosysteme/PROMPT-MAITRE-SHARED.md")
        r = sceller(base)
        add("T3c: divergence résorbée par la voie mécanique (commitée)",
            r.returncode == 0 and "évolution légitime (git)" in r.stdout
            and "DIVERGENCE NON COMMITÉE".encode("utf-8") not in lire_entree(base, "@mon-ecosysteme/PROMPT-MAITRE-SHARED.md"),
            "rc=%d · %s" % (r.returncode, (r.stdout or r.stderr).strip()[-160:]))

        # T4 — idempotence finale
        sha_a = sha_archive(base)
        r1, r2 = sceller(base), sceller(base)
        add("T4: idempotence finale ×2 byte-stable",
            r1.returncode == 0 and r2.returncode == 0 and sha_archive(base) == sha_a,
            "SHA stable ×2 sur état scellé")

        # T5 — parité v2.4/v2.5 sur état propre (EPOQUE_FIXE)
        sha_v25 = sha_archive(base)
        r24 = sceller(base, "v24")
        add("T5: parité v2.4/v2.5 (SHA identiques, EPOQUE_FIXE)",
            r24.returncode == 0 and sha_archive(base) == sha_v25,
            "v24 rc=%d · octets identiques" % r24.returncode)

        # T6 — DÉPLACEMENT R4 : v2.4 démontre le différé (faux positif rc=2)
        source = base / "skills" / "@mon-ecosysteme" / "PROMPT-MAITRE-GEN-PLAN.md"
        cible_r4 = base / "skills" / "@historique" / "prompts-maitres" / "gen-plan" / "PROMPT-MAITRE-GEN-PLAN.md"
        cible_r4.write_bytes(source.read_bytes())  # déplacement byte-identique (N27/R4)
        source.unlink()
        assert shell(base, "git", "add", "-A").returncode == 0
        assert shell(base, "git", "commit", "-qm", "déduplication N27 : déplacement R4 corpus → @historique").returncode == 0
        sha_avant = sha_archive(base)
        r = sceller(base, "v24")
        add("T6: DÉPLACEMENT R4 avec v2.4 → rc=2 FAUX POSITIF (différé démontré)",
            r.returncode == 2 and "anti-perte" in r.stdout and sha_archive(base) == sha_avant,
            "rc=%d · le différé Task 12 était réel" % r.returncode)

        # T6b — DÉPLACEMENT R4 : v2.5 corrige (rc=0 tracé, contenu préservé)
        r = sceller(base)
        entrees = noms_entrees(base)
        add("T6b: DÉPLACEMENT R4 avec v2.5 → rc=0 TRACÉ, entrée sortie, contenu préservé",
            r.returncode == 0 and "déplacement R4 légitime" in r.stdout
            and "@mon-ecosysteme/PROMPT-MAITRE-GEN-PLAN.md" not in entrees
            and len(entrees) == 14,
            "rc=%d · 14 entrées (8 corpus + 6 piliers)" % r.returncode)

        # T7 — PERTE RÉELLE avec v2.5 (anti-perte INTACT malgré le correctif)
        sha_avant = sha_archive(base)
        (base / "skills" / "@mon-ecosysteme" / "PROMPT-MAITRE-CLONE-CHAT.md").unlink()
        r = sceller(base)
        add("T7: PERTE réelle (sans contrepartie @historique) → rc=2, archive inchangée",
            r.returncode == 2 and "anti-perte" in r.stdout and sha_archive(base) == sha_avant,
            "rc=%d · aucune perte silencieuse permise" % r.returncode)

        # T8 — restauration git + re-scellement v2.5
        shell(base, "git", "checkout", "-q", "--", "skills/@mon-ecosysteme/PROMPT-MAITRE-CLONE-CHAT.md")
        r = sceller(base)
        add("T8: restauration git + re-scellement v2.5 → rc=0 (retour état scellé)",
            r.returncode == 0 and len(noms_entrees(base)) == 14,
            "rc=%d · 14 entrées stables" % r.returncode)

        passes = sum(1 for _, ok, _ in res if ok)
        print("=== RESUME : %d/%d PASS ===" % (passes, len(res)))
        return 0 if passes == len(res) else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
