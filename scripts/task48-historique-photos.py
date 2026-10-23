#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.12)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

# -*- coding: utf-8 -*-
"""Task 48 — G3/S3 : archivage R4 des versions supplantées des PMs @photos vers
skills/@historique/photos/ (byte-identité, SHA-256 scellé dans INDEX.md).
Sources git : e62f354 (17 v2.0, 18 v1.0, 19 v0.9.0) ; 29e2de1 (19 v0.10.0).
Idempotent : re-exécution = mêmes fichiers + INDEX réécrit de façon déterministe."""
import hashlib
import subprocess
from pathlib import Path

REPO = Path("/home/z/my-project/tmp/KNOWLEDGE-repo")
HISTO = REPO / "skills" / "@historique" / "photos"
HISTO.mkdir(parents=True, exist_ok=True)

VERSIONS = [
    ("iphone17-photos-v2.0.md", "skills/@photos/iphone17-photos.md", "e62f354"),
    ("iphone18-photos-v1.0.md", "skills/@photos/iphone18-photos.md", "e62f354"),
    ("iphone19-photos-v0.9.0.md", "skills/@photos/iphone19-photos.md", "e62f354"),
    ("iphone19-photos-v0.10.0.md", "skills/@photos/iphone19-photos.md", "29e2de1"),
]

ENTETES = {
    "iphone17-photos-v2.0.md": "v2.0 — génération 17 (ARCHIVÉE au plan générationnel ; supplantée par v2.1 extension 1944 le 2026-10-21)",
    "iphone18-photos-v1.0.md": "v1.0 — génération 18 CONFIRMÉE (supplantée par v1.1 extension 1944 le 2026-10-21)",
    "iphone19-photos-v0.9.0.md": "v0.9.0 — migration ANTICIPÉE (supplantée par v0.10.0 pixel binning le 2026-10-21)",
    "iphone19-photos-v0.10.0.md": "v0.10.0 — émulation pixel binning R19 (supplantée par v0.11.0 extension 1944 le 2026-10-21)",
}

index_rows = []
for name, path, commit in VERSIONS:
    r = subprocess.run(["git", "-C", str(REPO), "show", f"{commit}:{path}"],
                       capture_output=True, text=True, check=True)
    data = r.stdout
    # garde de version : le contenu extrait porte bien la version attendue
    attendu = name.split("-v")[1].replace(".md", "")
    assert f"Version {attendu}" in data[:400], f"version inattendue dans {name} ({commit})"
    dst = HISTO / name
    if dst.exists() and hashlib.sha256(dst.read_bytes()).hexdigest() == hashlib.sha256(data.encode()).hexdigest():
        pass  # déjà archivé identique (idempotence)
    else:
        dst.write_text(data, encoding="utf-8")
    sha = hashlib.sha256(dst.read_bytes()).hexdigest()
    index_rows.append((name, attendu, commit, sha[:16], ENTETES[name]))
    print(f"archivé : {name} (sha256 {sha[:16]}…, source git {commit})")

index = ["# @historique/photos/ — Archive des versions supplantées des PMs @photos", "",
         "> Créé Task 48 (G3, session web-38713acd, 2026-10-21) — convention R4 : byte-identité",
         "> prouvée contre les blobs git du dépôt (colonne « commit source ») ; les versions",
         "> supplantées ne sont JAMAIS réinstallées (garde R2 KO-L003) et ne servent que de",
         "> référence documentaire. Les PMs courants vivent dans `skills/@photos/`.", "",
         "| Fichier archivé | Version | Commit source (byte-identité) | SHA-256 (16) | Rôle |",
         "|---|---|---|---|---|"]
for name, ver, commit, sha, role in index_rows:
    index.append(f"| `{name}` | {ver} | {commit} | `{sha}` | {role} |")
index += ["", "Règle : toute évolution d'un PM @photos = bump versionné dans le fichier vivant",
          "(changelog + note rétroactive §11 + auto-audit) + archivage de la version supplantée",
          "ici (extraction git byte-identique + scellement SHA-256) + mise à jour de la table §2",
          "du README @photos et du présent index."]
(HISTO / "INDEX.md").write_text("\n".join(index) + "\n", encoding="utf-8")
print(f"INDEX.md écrit ({len(index_rows)} versions scellées)")
