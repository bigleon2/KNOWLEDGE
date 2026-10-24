#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.13)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

"""Diagnostic filet : liste concrète des fichiers qui divergent en 60 s (run 4)."""
import hashlib
import time
from pathlib import Path

HOST = Path("/home/z/my-project")
EXCL = {".git", "__pycache__", "node_modules", ".venv", ".next", ".turbo", ".cache"}


def empreinte():
    etat = {}
    for p in HOST.rglob("*"):
        rel = str(p.relative_to(HOST))
        if any(part in EXCL for part in p.relative_to(HOST).parts):
            continue
        if p.is_file():
            try:
                st = p.stat()
            except OSError:
                continue
            etat[rel] = (st.st_size, int(st.st_mtime))
    return etat


a = empreinte()
print(f"[diag] empreinte A : {len(a)} fichiers")
time.sleep(60)
b = empreinte()
print(f"[diag] empreinte B : {len(b)} fichiers")
ajoutes = sorted(set(b) - set(a))
supprimes = sorted(set(a) - set(b))
modifies = [f for f in sorted(set(a) & set(b)) if a[f] != b[f]]
print(f"[diag] ajoutés ({len(ajoutes)}):")
for f in ajoutes[:15]:
    print("   +", f)
print(f"[diag] supprimés ({len(supprimes)}):")
for f in supprimes[:15]:
    print("   -", f)
print(f"[diag] modifiés ({len(modifies)}):")
for f in modifies[:15]:
    print("   ~", f, a.get(f), "->", b.get(f))
