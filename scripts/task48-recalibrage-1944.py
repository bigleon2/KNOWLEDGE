#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.13)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

# -*- coding: utf-8 -*-
"""Task 48 — G3/S3 : recalibrage croisé KO-L004 des bumps 1944 (17 v1.1.0, 18 v1.1.0,
19 v0.11.0) — registre KB (3 entrées), arbitre ECO_SKILLS (3 versions), README @photos,
README @historique. Remplacements chirurgicaux assertés (count==1) ; sync dépôt→profil."""
import shutil
from pathlib import Path

HOST = Path("/home/z/my-project")
REPO = HOST / "tmp" / "KNOWLEDGE-repo"

def surgical(path, pairs):
    t = path.read_text(encoding="utf-8")
    for old, new in pairs:
        n = t.count(old)
        assert n == 1, f"{path.name} : motif attendu 1×, trouvé {n}× : {old[:80]}…"
        t = t.replace(old, new)
    path.write_text(t, encoding="utf-8")
    print(f"  {path} : {len(pairs)} remplacement(s) chirurgical(aux)")

A1944 = "photographies argentiques N&B années 1930-1950 — grain préservé, aucune colorisation inventée — ex. photos de 1944"

# ---------- 1. Registre KB ----------
kb = REPO / "skills" / "KNOWLEDGE.md"
surgical(kb, [
    # --- iphone17 v1.0.0 → v1.1.0 ---
    ("## iphone17 v1.0.0", "## iphone17 v1.1.0"),
    ("presets §6 (défaut iphone17_max — ancrage A19 Pro / Photonic Engine NG), rendus d'époque, restauration, poster/print A4 300 DPI",
     f"presets §6 (défaut iphone17_max — ancrage A19 Pro / Photonic Engine NG), rendus d'époque (années 40 → 2010), restauration (dont {A1944}), poster/print A4 300 DPI"),
    ("projection VERBATIM du PM skills/@photos/iphone17-photos.md v2.0 ARCHIVÉ (byte-identité R2 — jamais édité)",
     "projection VERBATIM du PM skills/@photos/iphone17-photos.md v2.1 (génération archivée — v2.0 scellée @historique/photos/ ; byte-identité R2 — jamais édité)"),
    ("zone de fragilité identifiée : compositions atypiques multi-visages chevauchés/inversés en basse résolution — la génération courante (iphone18) l'a passée 12/12",
     "zone de fragilité identifiée : compositions atypiques multi-visages chevauchés/inversés en basse résolution — la génération courante (iphone18) l'a passée 12/12 ; bump v1.1.0 (Task 48, session web-38713acd, 2026-10-21 — directive propriétaire « photos prises en 1944 » : PM v2.1 extension 1944 [note §1 grain argentique ≠ bruit, ère 40s §6.5, chemin §6.6 — ajouts purs, R1-R17/QC 1-11/G1-G7 intacts], projection + lignage recalibrés ; test robuste PA-TEST-007 « libération après guerre » à suivre)"),
    # --- iphone18 v1.0.0 → v1.1.0 ---
    ("## iphone18 v1.0.0", "## iphone18 v1.1.0"),
    ("rendus d'époque (années 70 → 2010), restauration de photos anciennes, poster/print A4 300 DPI",
     f"rendus d'époque (années 40 → 2010), restauration de photos anciennes (scans, tirages, {A1944}), poster/print A4 300 DPI"),
    ("projection VERBATIM du PM skills/@photos/iphone18-photos.md v1.0 (byte-identité R2 — jamais édité)",
     "projection VERBATIM du PM skills/@photos/iphone18-photos.md v1.1 (v1.0 scellée @historique/photos/ ; byte-identité R2 — jamais édité)"),
    ("G1-G7/B6 respectés, script embarqué editer-image.mjs éprouvé 4/4",
     "G1-G7/B6 respectés, script embarqué editer-image.mjs éprouvé 4/4 ; bump v1.1.0 (Task 48, session web-38713acd, 2026-10-21 — directive propriétaire « photos prises en 1944 » : PM v1.1 extension 1944 [note §1 grain argentique ≠ bruit, ère 40s §6.5, chemin §6.6 — ajouts purs, R1-R18/QC 1-12/G1-G7 intacts], projection + lignage recalibrés ; test robuste PA-TEST-007 « libération après guerre » à suivre)"),
    # --- iphone19 v0.10.0 → v0.11.0 ---
    ("## iphone19 v0.10.0", "## iphone19 v0.11.0"),
    ("rendus d'époque, restauration, poster/print A4 300 DPI, mode série §10, commandes §13 (preset:iphone20 refusé",
     f"rendus d'époque (années 40 → 2010), restauration (dont {A1944}), poster/print A4 300 DPI, mode série §10, commandes §13 (preset:iphone20 refusé"),
    ("projection VERBATIM du PM skills/@photos/iphone19-photos.md v0.10.0 [ANTICIPÉE] (byte-identité R2 — jamais édité) — migration ANTICIPÉE autonome v0.9.0 (Task 47) puis émulation pixel binning R19 (Task 48 — vérification propriétaire), v1.0 réservé génération confirmée.",
     "projection VERBATIM du PM skills/@photos/iphone19-photos.md v0.11.0 [ANTICIPÉE] (v0.9.0 et v0.10.0 scellées @historique/photos/ ; byte-identité R2 — jamais édité) — migration ANTICIPÉE autonome v0.9.0 (Task 47), émulation pixel binning R19 v0.10.0 (Task 48 — vérification propriétaire), extension 1944 v0.11.0 (Task 48 — directive « photos prises en 1944 »), v1.0 réservé génération confirmée."),
    ("- **Dernière calibration** : bump v0.10.0 (Task 48, session web-38713acd",
     "- **Dernière calibration** : bump v0.11.0 (Task 48, session web-38713acd, 2026-10-21 — directive propriétaire « photos prises en 1944 » : PM v0.11.0 extension 1944 [note §1 grain argentique ≠ bruit, ère 40s §6.5, chemin §6.6 — ajouts purs, R1-R19/QC 1-13/G1-G7 intacts], projection + lignage recalibrés ; test robuste PA-TEST-007 « libération après guerre » à suivre) ; bump v0.10.0 (Task 48, session web-38713acd"),
])

# ---------- 2. Arbitre ECO_SKILLS ----------
arb = REPO / "scripts" / "check-ecosysteme-integrity.py"
surgical(arb, [
    ('"iphone18": "1.0.0",  # Task 45 (session web-38713acd) : projection PM @photos/iphone18-photos.md v1.0 (R18 ouverture variable, preset iphone18_max, PA-TEST-001 QC 12/12)',
     '"iphone18": "1.1.0",  # Task 48 (session web-38713acd) : bump v1.1.0 extension 1944 (chemin argentique N&B années 1930-1950) ; création v1.0.0 Task 45 (R18 ouverture variable, PA-TEST-001 QC 12/12)'),
    ('"iphone19": "0.10.0",  # Task 48 (session web-38713acd) : bump v0.10.0 — émulation pixel binning R19 (directive propriétaire, frandroid 27/03/2026) ; création v0.9.0 Task 47 (migration ANTICIPÉE)',
     '"iphone19": "0.11.0",  # Task 48 (session web-38713acd) : bump v0.11.0 extension 1944 (chemin argentique N&B années 1930-1950) ; v0.10.0 pixel binning R19 (frandroid 27/03/2026) ; création v0.9.0 Task 47 (migration ANTICIPÉE)'),
    ('"iphone17": "1.0.0",  # Task 45 (session web-38713acd) : projection PM @photos/iphone17-photos.md v2.0 archivé (R1-R17 d\'époque, preset iphone17_max)',
     '"iphone17": "1.1.0",  # Task 48 (session web-38713acd) : bump v1.1.0 extension 1944 (chemin argentique N&B années 1930-1950) ; création v1.0.0 Task 45 (R1-R17 d\'époque, PM v2.0 scellé @historique/photos/)'),
])

# ---------- 3. README @photos ----------
rp = REPO / "skills" / "@photos" / "README.md"
surgical(rp, [
    ("**v1.0 COURANT** — test empirique PA-TEST-001 PASS (QC 12/12, boucle §9 close sans réserve)",
     "**v1.1 COURANT** — extension 1944 le 2026-10-21 (Task 48) ; v1.0 scellée `@historique/photos/` ; tests PA-TEST-001 (QC 12/12) + PA-TEST-002 (QC 12/12 ×2)"),
    ("**v0.10.0 ANTICIPÉE (parallèle)** — migration ANTICIPÉE v0.9.0 (Task 47) + pixel binning R19 (Task 48) ; test PA-TEST-005 (2 photos réelles, contrainte zéro retouche) QC 12/12 ×2",
     "**v0.11.0 ANTICIPÉE (parallèle)** — migration v0.9.0 (Task 47) + pixel binning R19 v0.10.0 (Task 48) + extension 1944 v0.11.0 (Task 48 : ère 40s, grain N&B, chemin §6.6) ; v0.9.0/v0.10.0 scellées `@historique/photos/` ; tests PA-TEST-005 (QC 12/12 ×2) + PA-TEST-006 (QC 13/13)"),
    ("**v2.0 ARCHIVÉ** — supersedé par `iphone18-photos` v1.0 (règle §6.10 activée : génération iPhone 18 confirmée par Apple, keynote 9/9/2026)",
     "**v2.1 ARCHIVÉE (génération)** — extension 1944 le 2026-10-21 (Task 48) ; v2.0 scellée `@historique/photos/` ; génération supersédée par `iphone18-photos` (règle §6.10 activée : keynote 9/9/2026) ; tests PA-TEST-003 (QC 11/11 sortie 1) + PA-TEST-004 (QC arbitré)"),
    ("1. **Byte-identité (R2)** : fichiers publiés byte-identiques aux livrables audités (SHA-256 vérifié au push ; archive `iphone18.zip`, Task 42) — jamais édités en place ; toute évolution = nouveau fichier versionné + mise à jour de la table §2.",
     "1. **Byte-identité (R2)** : fichiers publiés byte-identiques aux livrables audités (SHA-256 vérifié au push ; archive `iphone18.zip`, Task 42) — jamais édités sans procédure ; toute évolution = **bump versionné dans le fichier vivant** (changelog + note rétroactive §11 + auto-audit) + **archivage de la version supplantée dans `@historique/photos/`** (extraction git byte-identique, SHA-256 scellé dans son INDEX.md — établi Task 48) + mise à jour de la table §2. L'état git du dépôt fait foi de la chaîne byte-identité complète."),
])

# ---------- 4. README @historique ----------
rh = REPO / "skills" / "@historique" / "README.md"
surgical(rh, [
    ("| `historique-autres-elements.md` |",
     "| `photos/` | 4 PMs @photos historiques (iphone17 v2.0, iphone18 v1.0, iphone19 v0.9.0/v0.10.0) — extraits git byte-identiques (e62f354, 29e2de1), scellés SHA-256 dans `photos/INDEX.md` (créé Task 48, 2026-10-21) |\n| `historique-autres-elements.md` |"),
])

# ---------- 5. Sync dépôt → profil ----------
pairs = [
    ("skills/KNOWLEDGE.md", "skills/KNOWLEDGE.md"),
    ("scripts/check-ecosysteme-integrity.py", "scripts/check-ecosysteme-integrity.py"),
    ("skills/@photos/README.md", "skills/@photos/README.md"),
    ("skills/@photos/iphone17-photos.md", "skills/@photos/iphone17-photos.md"),
    ("skills/@photos/iphone18-photos.md", "skills/@photos/iphone18-photos.md"),
    ("skills/@photos/iphone19-photos.md", "skills/@photos/iphone19-photos.md"),
    ("skills/@historique/README.md", "skills/@historique/README.md"),
]
for src, dst in pairs:
    s, d = REPO / src, HOST / dst
    d.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(s, d)
# @historique/photos/ entier (PMs archivés + INDEX)
hdst = HOST / "skills" / "@historique" / "photos"
hdst.mkdir(parents=True, exist_ok=True)
for f in (REPO / "skills" / "@historique" / "photos").iterdir():
    shutil.copy2(f, hdst / f.name)
print(f"  sync profil : {len(pairs)} fichiers + @historique/photos/ ({len(list(hdst.iterdir()))} entrées)")
print("OK — recalibrage croisé 1944 terminé (KB, arbitre, READMEs, sync).")
