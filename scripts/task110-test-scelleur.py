#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 110 — Harnais de test du scelleur v2.4 (T2.2, correctif structurel F2).

Règle d'or n°5 (mesurer avant corriger) : monte un bac à sable — mini-arbre
(skills/@mon-ecosysteme 9 corpus SYNTHÉTIQUES + 6 piliers + scripts/scelleur +
download/) avec DÉPÔT GIT LOCAL initialisé et commité — puis exécute la
matrice F2 (CW Task 107, critère d'extinction tâche 4 du livrable Task 108) :

  T0  état propre → rc=0, 15 entrées, round-trip ; idempotence byte-stable ×2
  T1  ÉVOLUTION LÉGITIME COMMITÉE (bump corpus + git commit) → rc=0 SANS ECHEC
      ni intervention manuelle (critère d'extinction F2), tracé « évolution
      légitime (git) », octets nouveaux dans l'archive
  T2  PERTE (entrée d'archive sans contrepartie locale) → rc=2 bloqué, archive
      inchangée (sémantique anti-perte v2.3 préservée)
  T3  divergence NON commitée → rc=3 + guidance, archive inchangée
  T3b --autoriser-evolution → rc=0, acceptation EXPLICITE tracée
  T3c restauration git checkout → divergence archive↔corpus résorbée par la
      voie mécanique (évolution commitée) → rc=0
  T4  idempotence finale ×2 byte-stable
  T5  parité v2.3/v2.4 sur état propre — SHA d'archive IDENTIQUES (EPOQUE_FIXE)

Lecture seule sur l'arbre réel (copies vers bac à sable tempfile).
Sortie : verdicts par cas + résumé ; rc 0 ssi tous PASS.
"""

# ⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.46)
# SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
# Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
# Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
# Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
# Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
# Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).

import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

HOTE = Path("/home/z/my-project")
SCELLEUR_V24 = HOTE / "scripts" / "task-f5-seal-archive-v24.py"
SCELLEUR_V23 = HOTE / "scripts" / "task-f5-seal-archive-v23.py"

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
    return subprocess.run(list(args), capture_output=True, text=True, cwd=str(cwd))


def sceller(base: Path, *options: str) -> subprocess.CompletedProcess:
    return shell(base, sys.executable, str(base / "scripts" / "task-f5-seal-archive-v24.py"), *options)


def sha_archive(base: Path) -> str:
    import hashlib
    return hashlib.sha256((base / "download" / "mon-ecosysteme_archive.zip").read_bytes()).hexdigest()


def lire_entree(base: Path, nom: str) -> bytes:
    with zipfile.ZipFile(base / "download" / "mon-ecosysteme_archive.zip") as z:
        return z.read(nom)


def monter_sandbox(base: Path) -> None:
    """Mini-arbre + dépôt git local : 9 corpus synthétiques + 6 piliers + scelleurs."""
    (base / "skills" / "@mon-ecosysteme").mkdir(parents=True)
    for i, nom in enumerate(CORPUS_NOMS):
        (base / "skills" / "@mon-ecosysteme" / nom).write_text(
            "# %s (corpus synthétique %d)\n\nContenu factice v1 — bac à sable Task 110.\n" % (nom, i), encoding="utf-8")
    for rel in PILIERS_REL:
        p = base / rel  # rel est relatif à BASE (préfixes skills/ et scripts/ explicites)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("# pilier synthétique : %s\n" % rel, encoding="utf-8")
    (base / "scripts").mkdir(exist_ok=True)
    (base / "download").mkdir(exist_ok=True)
    shutil.copy2(SCELLEUR_V24, base / "scripts" / "task-f5-seal-archive-v24.py")
    shutil.copy2(SCELLEUR_V23, base / "scripts" / "task-f5-seal-archive-v23.py")
    assert shell(base, "git", "init", "-q").returncode == 0
    assert shell(base, "git", "config", "user.email", "test@local").returncode == 0
    assert shell(base, "git", "config", "user.name", "test-task110").returncode == 0
    assert shell(base, "git", "add", "-A").returncode == 0
    assert shell(base, "git", "commit", "-qm", "état initial bac à sable").returncode == 0


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="task110-scelleur-"))
    res = []

    def add(cas, ok, detail):
        res.append((cas, bool(ok), detail))
        print("  [%s] %s — %s" % ("PASS" if ok else "FAIL", cas, detail))

    try:
        base = tmp / "arbre"
        base.mkdir()
        monter_sandbox(base)
        archive = base / "download" / "mon-ecosysteme_archive.zip"

        # T0 — état propre
        r = sceller(base)
        add("T0: état propre scellé rc=0 (15 entrées)", r.returncode == 0 and "15 entrées" in r.stdout,
            "rc=%d · %s" % (r.returncode, (r.stdout or r.stderr).strip()[-140:]))
        sha_1 = sha_archive(base)
        r = sceller(base)
        add("T0b: idempotence byte-stable", r.returncode == 0 and sha_archive(base) == sha_1, "SHA stable ×2")

        # T1 — évolution légitime commitée (critère d'extinction F2)
        cible = base / "skills" / "@mon-ecosysteme" / "PROMPT-MAITRE-SHARED.md"
        cible.write_text(cible.read_text(encoding="utf-8") + "\nÉVOLUTION LÉGITIME v2 — bump commité (Task 110 T1).\n", encoding="utf-8")
        assert shell(base, "git", "add", "-A").returncode == 0
        assert shell(base, "git", "commit", "-qm", "bump corpus").returncode == 0
        r = sceller(base)
        octets = lire_entree(base, "@mon-ecosysteme/PROMPT-MAITRE-SHARED.md")
        add("T1: bump corpus commité rescellé SANS ECHEC (rc=0, tracé git)",
            r.returncode == 0 and "évolution légitime (git)" in r.stdout
            and "ÉVOLUTION LÉGITIME v2".encode("utf-8") in octets,
            "rc=%d · évolution mécanique sans intervention manuelle" % r.returncode)

        # T2 — PERTE (entrée d'archive sans contrepartie locale)
        sha_avant = sha_archive(base)
        (base / "skills" / "@mon-ecosysteme" / "README.md").unlink()
        r = sceller(base)
        add("T2: PERTE bloquée rc=2, archive inchangée",
            r.returncode == 2 and "anti-perte" in r.stdout and sha_archive(base) == sha_avant,
            "rc=%d · sémantique v2.3 préservée" % r.returncode)
        shell(base, "git", "checkout", "-q", "--", "skills/@mon-ecosysteme/README.md")

        # T3 — divergence non commitée
        sha_avant = sha_archive(base)
        cible.write_text(cible.read_text(encoding="utf-8") + "\nDIVERGENCE NON COMMITÉE — Task 110 T3.\n", encoding="utf-8")
        r = sceller(base)
        add("T3: divergence non commitée → rc=3 + guidance",
            r.returncode == 3 and "guidance" in r.stdout and sha_archive(base) == sha_avant,
            "rc=%d · archive inchangée" % r.returncode)

        # T3b — drapeau d'acceptation explicite
        r = sceller(base, "--autoriser-evolution")
        add("T3b: --autoriser-evolution → rc=0 tracé",
            r.returncode == 0 and "AUTORISÉE explicitement" in r.stdout
            and "DIVERGENCE NON COMMITÉE".encode("utf-8") in lire_entree(base, "@mon-ecosysteme/PROMPT-MAITRE-SHARED.md"),
            "rc=%d · acceptation explicite de l'opérateur" % r.returncode)

        # T3c — restauration + résorption mécanique de la divergence
        shell(base, "git", "checkout", "-q", "--", "skills/@mon-ecosysteme/PROMPT-MAITRE-SHARED.md")
        r = sceller(base)
        add("T3c: divergence résorbée par la voie mécanique (commitée)",
            r.returncode == 0 and "évolution légitime (git)" in r.stdout
            and "DIVERGENCE NON COMMITÉE".encode("utf-8") not in lire_entree(base, "@mon-ecosysteme/PROMPT-MAITRE-SHARED.md"),
            "rc=%d · retour à l'état commité scellé" % r.returncode)

        # T4 — idempotence finale
        sha_a = sha_archive(base)
        r1, r2 = sceller(base), sceller(base)
        add("T4: idempotence finale ×2 byte-stable",
            r1.returncode == 0 and r2.returncode == 0 and sha_archive(base) == sha_a,
            "SHA stable ×2 sur état scellé")

        # T5 — parité v2.3/v2.4 sur état propre
        sha_v24 = sha_archive(base)
        r23 = shell(base, sys.executable, str(base / "scripts" / "task-f5-seal-archive-v23.py"))
        add("T5: parité v2.3/v2.4 (SHA identiques, EPOQUE_FIXE)",
            r23.returncode == 0 and sha_archive(base) == sha_v24,
            "v23 rc=%d · octets identiques" % r23.returncode)

        passes = sum(1 for _, ok, _ in res if ok)
        print("=== RESUME : %d/%d PASS ===" % (passes, len(res)))
        return 0 if passes == len(res) else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
