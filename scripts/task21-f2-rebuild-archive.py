#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.6.8)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

# -*- coding: utf-8 -*-
"""Task 21 — F2 : régénération de l'archive d'intégrité (véhicule v2.2) après édition du corpus.
Processus établi (Tasks 16/18) : l'archive = copie byte-identique du corpus @mon-ecosysteme
+ homologues/ v2.1 (famille créateur/relecture). Idempotent : re-exécution = archive équivalente."""
import shutil
import zipfile
from pathlib import Path

BASE = Path("/home/z/my-project/work_knowledge")
CORPUS = BASE / "skills" / "@mon-ecosysteme"
HISTORIQUE = BASE / "skills" / "@historique" / "prompts-maitres"  # Task 16 : destination des PMs déplacés
ARCHIVE = BASE / "download" / "mon-ecosysteme_archive.zip"
BAK = ARCHIVE.with_suffix(".zip.bak")

# Retraits sanctionnés : entrées de l'ancienne archive à supprimer du re-scellement
# (au lieu d'échouer en « extra hors homologues » — protection anti-perte conservée
# pour tout autre extra). Traçabilité : chaque retrait = suppression propriétaire
# publiée, référencée ici avec son commit et sa décision de calibration.
RETRAITS_SANCTIONNES = {
    # suppression propriétaire d72226a (UI web, couche Task 14-push) —
    # re-scellement Task 15 (D002, plan-task15-decisions-restantes.md)
    "clone-discussion-2026-09-27-ecosysteme-knowledge-b13-r7-f.md",
    # déduplication des PMs (directive propriétaire « ne garder que la dernière
    # version ») — re-scellement Task 16 (plan-task16-corpus-pms-historique-
    # reinstallation.md) : 19 PMs historiques DÉPLACÉS git mv vers
    # skills/@historique/prompts-maitres/{gen-plan,correct-work}/ — byte-identité
    # vérifiée ci-dessous contre l'ancienne archive (garde anti-perte renforcée).
    "PROMPT-MAITRE-GEN-PLAN-v3.6.1.md", "PROMPT-MAITRE-GEN-PLAN-v3.7.0.md",
    "PROMPT-MAITRE-GEN-PLAN-v3.8.0.md", "PROMPT-MAITRE-GEN-PLAN-v3.8.1.md",
    "PROMPT-MAITRE-GEN-PLAN-v3.9.0.md", "PROMPT-MAITRE-GEN-PLAN-v3.10.0.md",
    "PROMPT-MAITRE-GEN-PLAN-v3.11.0.md", "PROMPT-MAITRE-GEN-PLAN-v3.12.0.md",
    "PROMPT-MAITRE-GEN-PLAN-v3.13.0.md", "PROMPT-MAITRE-GEN-PLAN-v3.16.0.md",
    "PROMPT-MAITRE-GEN-PLAN-v3.17.0.md", "PROMPT-MAITRE-GEN-PLAN-v3.17.1.md",
    "PROMPT-MAITRE-GEN-PLAN-v3.17.2.md", "PROMPT-MAITRE-GEN-PLAN-v3.18.0.md",
    "PROMPT-MAITRE-GEN-PLAN-v3.19.0.md",
    "PROMPT-MAITRE-CORRECT-WORK-v2.4.0.md", "PROMPT-MAITRE-CORRECT-WORK-v2.5.0.md",
    "PROMPT-MAITRE-CORRECT-WORK-v2.5.1.md", "PROMPT-MAITRE-CORRECT-WORK-v2.6.0.md",
}

# Task 16 — garde anti-perte renforcée pour les retraits DÉPLACÉS : chaque PM
# sanctionné doit exister en skills/@historique/prompts-maitres/ avec les MÊMES
# octets que l'entrée de l'ancienne archive (sinon : échec + restauration).
def dest_historique(short):
    if short.startswith("PROMPT-MAITRE-GEN-PLAN-"):
        return HISTORIQUE / "gen-plan" / short
    if short.startswith("PROMPT-MAITRE-CORRECT-WORK-"):
        return HISTORIQUE / "correct-work" / short
    return None

corpus_files = sorted(p.name for p in CORPUS.glob("*.md"))
print(f"corpus : {len(corpus_files)} fichiers .md")

shutil.copy2(ARCHIVE, BAK)
with zipfile.ZipFile(BAK) as z:
    old_names = z.namelist()
    old_bytes = {n: z.read(n) for n in old_names if not n.endswith("/")}
print(f"ancienne archive : {len(old_bytes)} entrées")

# Task 16 — vérification anti-perte des retraits déplacés (avant toute écriture)
for name, data in old_bytes.items():
    short = name.split("@mon-ecosysteme/")[-1]
    if short in RETRAITS_SANCTIONNES:
        dest = dest_historique(short)
        if dest is None:
            continue  # retrait-suppression (clone-discussion) — vérifié Task 15
        if not dest.exists() or dest.read_bytes() != data:
            print(f"ECHEC anti-perte : {short} absent ou divergent en @historique/")
            raise SystemExit(2)
print(f"garde anti-perte : {sum(1 for n in old_bytes if n.split('@mon-ecosysteme/')[-1] in RETRAITS_SANCTIONNES and dest_historique(n.split('@mon-ecosysteme/')[-1]))} PMs déplacés vérifiés byte-identiques en @historique/")

with zipfile.ZipFile(ARCHIVE, "w", zipfile.ZIP_DEFLATED) as z:
    for name in old_names:
        if name.endswith("/"):
            continue
        short = name.split("@mon-ecosysteme/")[-1]
        if short in RETRAITS_SANCTIONNES:
            continue
        if short in set(corpus_files):
            data = (CORPUS / short).read_bytes()
        else:
            data = old_bytes[name]
        z.writestr(name, data)

# auto-vérification : corpus ⊆ archive byte-identique, extras seulement homologues/
with zipfile.ZipFile(ARCHIVE) as z:
    znames = [n for n in z.namelist() if not n.endswith("/")]
    divergent = [n for n in corpus_files
                 if not any(m.split("@mon-ecosysteme/")[-1] == n and z.read(m) == (CORPUS / n).read_bytes()
                            for m in znames)]
    extras = [n for n in znames
              if (n.split("@mon-ecosysteme/")[-1] if "@mon-ecosysteme/" in n else n) not in set(corpus_files)
              and (n.split("@mon-ecosysteme/")[-1] if "@mon-ecosysteme/" in n else n) not in RETRAITS_SANCTIONNES
              and not n.startswith("homologues/")]
print(f"nouvelle archive : {len(znames)} entrées ; divergents : {divergent or '—'} ; "
      f"extras hors homologues : {extras or '—'}")
if divergent or extras:
    shutil.copy2(BAK, ARCHIVE)
    print("ÉCHEC — archive restaurée depuis la sauvegarde")
    raise SystemExit(1)
BAK.unlink()
print("Archive régénérée et round-trip vérifié (véhicule v2.2).")
