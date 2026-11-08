#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.36)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).
"""

"""Task 48 — Sync miroir hôte (dépôt→hôte, convention R4).

Direction UNIQUE : dépôt (clone de travail) → hôte (skills/ du sandbox).
- copie de chaque fichier du dépôt skills/ dont la contrepartie hôte diverge ou manque ;
- délétion contrôlée côté hôte des fichiers déplacés au @historique du dépôt (R4 :
  aucun homonyme des deux côtés — vérification byte-identité AVANT suppression) ;
- signalement (sans action) des fichiers hôte-seuls (aucune suppression aveugle).
Idempotent : re-exécution = 0 divergence résiduelle attendue.
"""

import filecmp
import shutil
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent          # dépôt (clone de travail)
HOST = Path("/home/z/my-project")                       # hôte (sandbox)
REPO_SKILLS = BASE / "skills"
HOST_SKILLS = HOST / "skills"

copiés, inchangés = [], 0
for src in sorted(REPO_SKILLS.rglob("*")):
    if src.is_dir() or "__pycache__" in src.parts:
        continue
    rel = src.relative_to(REPO_SKILLS)
    dst = HOST_SKILLS / rel
    if dst.exists() and filecmp.cmp(src, dst, shallow=False):
        inchangés += 1
    else:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        copiés.append(str(rel))

# Délétion contrôlée : PM supplantés déplacés vers @historique côté dépôt mais encore
# présents au corpus hôte (R4). Vérification byte-identité contre la copie @historique.
supprimés, résiduels = [], []
repo_files = {p.relative_to(REPO_SKILLS).as_posix() for p in REPO_SKILLS.rglob("*") if p.is_file() and "__pycache__" not in p.parts}
for dst in sorted(HOST_SKILLS.rglob("*")):
    if dst.is_dir() or "__pycache__" in dst.parts:
        continue
    rel = dst.relative_to(HOST_SKILLS).as_posix()
    if rel in repo_files:
        continue
    # hôte-seul : délétion UNIQUEMENT si homonyme @historique byte-identique au dépôt
    candidats = list(REPO_SKILLS.glob(f"@historique/**/{dst.name}"))
    if candidats and all(c.read_bytes() == dst.read_bytes() for c in candidats):
        dst.unlink()
        supprimés.append(rel)
    else:
        résiduels.append(rel)

print(f"Sync miroir dépôt→hôte : {len(copiés)} copiés · {inchangés} inchangés · {len(supprimés)} supprimés R4 · {len(résiduels)} hôte-seuls (non touchés)")
for f in copiés[:8]:
    print(f"  + {f}")
if len(copiés) > 8:
    print(f"  … et {len(copiés) - 8} autres")
for f in supprimés:
    print(f"  - {f} (déplacé @historique, byte-identité vérifiée)")
for f in résiduels[:10]:
    print(f"  ? hôte-seul : {f}")
