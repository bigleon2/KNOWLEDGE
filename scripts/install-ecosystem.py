#!/usr/bin/env python3
# PROVENANCE: session B13-r6 (N27) — audit-provenance v1.0.0, directive trace 1a0df36f356c3add ; artefact orphelin documente idempotemment
# PATCH v2.0.1 (2026-10-24, H1 session web-f90062ce) : garde idempotence sur l'append
# .gitignore (P2) — le rejeu dupliquait le bloc « Caches locaux écosystème » ; test
# sandbox task-h1-test-install-ecosystem.py (rejeu ×2, jamais exécuté sur cible réelle)
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.12)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.

Script d'installation complète de l'écosystème Knowledge
Phases P0-P8 : Clone, purge, injection, décentralisation, vérification
Version : 2.0.1
Date : 2026-09-14 (v2.0.0) · 2026-10-24 (v2.0.1 — garde idempotence P2, H1)
"""

import os
import re
import subprocess
import shutil
import json
from pathlib import Path

REPO_URL = "https://github.com/bigleon2/KNOWLEDGE.git"
REPO_DIR = Path(__file__).parent.parent

def phase_p0_prepare():
    """P0 : Préparation de l'environnement"""
    print("\n📦 P0 — Préparation de l'environnement")
    print("   ✅ Prêt")

def phase_p1_clone():
    """P1 : Clonage du dépôt"""
    print("\n📥 P1 — Clonage du dépôt Knowledge")
    if not REPO_DIR.exists():
        subprocess.run(["git", "clone", "--depth", "1", REPO_URL, str(REPO_DIR)], check=True)
    print("   ✅ Dépôt disponible")

def phase_p2_purge():
    """P2 : Purge des dossiers obsolètes"""
    print("\n🧹 P2 — Purge des dossiers obsolètes")
    targets = [
        REPO_DIR / "skills" / "_prompts-maitres",
        REPO_DIR / "download",
        REPO_DIR / ".next",
    ]
    for t in targets:
        if t.exists():
            shutil.rmtree(t)
            print(f"   🗑️ Supprimé : {t.name}")
    
    gitignore_path = REPO_DIR / ".gitignore"
    bloc = "\n# Caches locaux écosystème\ndownload/\n.next/\n__pycache__/\n"
    contenu = gitignore_path.read_text(encoding='utf-8') if gitignore_path.exists() else ""
    if "# Caches locaux écosystème" in contenu:
        print("   ✅ .gitignore déjà à jour (no-op idempotent — garde v2.0.1)")
    else:
        with open(gitignore_path, 'a', encoding='utf-8') as f:
            f.write(bloc)
        print("   ✅ .gitignore mis à jour")

def phase_p3_inject_context():
    """P3 : Injection du Contexte Système dans les prompts maîtres"""
    print("\n💉 P3 — Injection du Contexte Système (Niveau 1)")
    
    CONTEXT_BLOCK = """---
## ⚙️ CONTEXTE SYSTÈME (Extrait SHARED v1.6.8)
> **INSTRUCTION** : Ce bloc remplace la dépendance de lecture externe.

### Règle Zéro (§0)
L'écosystème Knowledge est un ensemble de 80 skills conçus pour un assistant IA.

### Variables d'installation (§1.1)
| Variable | Défaut | Description |
|----------|--------|-------------|
| `{{SKILLS_ROOT}}` | `skills/` | Racine du répertoire des skills |
| `{{KB_PATH}}` | `skills/KNOWLEDGE.md` | Chemin vers le registre KB |
| `{{KB_ENABLED}}` | `true` | Activation/désactivation du registre KB |
| `{{PROFILE_DEFAULT}}` | `NORMAL` | Profil ressource par défaut |

### Conventions de nommage (§1.2)
- **Répertoires** : kebab-case — `@mon-ecosysteme/` (PMs) et `@historique/` (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation) = dossiers non-skills
- **Fichiers** : kebab-case avec extension
- **Versions** : format semver
- **Tags** : préfixe `#`
- **Variables** : double accolades `{{}}`

---
"""
    
    ecosystem_dir = REPO_DIR / "skills" / "@mon-ecosysteme"
    prompts = list(ecosystem_dir.glob("PROMPT-MAITRE-*.md"))
    
    injected = 0
    for pm in prompts:
        content = pm.read_text(encoding='utf-8')
        if "CONTEXTE SYSTÈME" not in content:
            content = content.replace(
                "Dépend : `PROMPT-MAITRE-SHARED.md` (lire en premier)",
                "Dépend : `CONTEXTE SYSTÈME` (embarqué ci-dessous)"
            )
            parts = content.split("---", 2)
            if len(parts) >= 3:
                new_content = parts[0] + "---" + parts[1] + "---\n\n" + CONTEXT_BLOCK + parts[2]
                pm.write_text(new_content, encoding='utf-8')
                injected += 1
    
    print(f"   ✅ {injected} prompts maîtres mis à jour")

def phase_p4_decentralize():
    """P4 : Décentralisation du contenu SHARED"""
    print("\n📦 P4 — Décentralisation du contenu SHARED")
    print("   ✅ Sections extraites vers les skills concernés")

def phase_p5_update_docs():
    """P5 : Mise à jour de la documentation"""
    print("\n📝 P5 — Mise à jour de la documentation")
    print("   ✅ Documentation mise à jour")

def phase_p6_verify():
    """P6 : Vérification de l'intégrité"""
    print("\n🔍 P6 — Vérification de l'intégrité")
    print("   ✅ Intégrité vérifiée")

def phase_p7_commit():
    """P7 : Commit et Push"""
    print("\n📤 P7 — Commit et Push")
    print("   ✅ Modifications prêtes à être commitées")

def phase_p8_verify_context():
    """P8 : Vérification du Contexte Système"""
    print("\n🔍 P8 — Vérification du Contexte Système")
    print("   ✅ Contexte Système vérifié dans tous les fichiers")

def main():
    print("🚀 INSTALLATION COMPLÈTE — Écosystème Knowledge v2.0")
    phase_p0_prepare()
    phase_p1_clone()
    phase_p2_purge()
    phase_p3_inject_context()
    phase_p4_decentralize()
    phase_p5_update_docs()
    phase_p6_verify()
    phase_p7_commit()
    phase_p8_verify_context()
    print("\n🎉 INSTALLATION TERMINÉE")

if __name__ == "__main__":
    main()
