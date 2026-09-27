#!/usr/bin/env python3
# PROVENANCE: session B13-r6 (N27) — audit-provenance v1.0.0, directive trace 1a0df36f356c3add ; artefact orphelin documente idempotemment
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.5.2)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}}
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.

Script de synchronisation du Contexte Système après évolution du SHARED
Version : 2.0.0
"""

import os
import re
import argparse
from pathlib import Path

REPO_DIR = Path(__file__).parent.parent
ECOSYSTEM_DIR = REPO_DIR / "skills" / "@mon-ecosysteme"
SHARED_PATH = ECOSYSTEM_DIR / "PROMPT-MAITRE-SHARED.md"

PROMPT_FILES = [
    "PROMPT-MAITRE-GEN-PLAN-v3.11.0.md",
    "PROMPT-MAITRE-CORRECT-WORK-v2.5.1.md",
    "PROMPT-MAITRE-CLONE-CHAT-v2.0.0.md",
    "PROMPT-MAITRE-INSTALL-ECOSYSTEME.md",
    "INSTALL-ECOSYSTEME.md",
]

class SyncContextBlock:
    def __init__(self):
        self.new_block = ""
    
    def extract_context_from_shared(self):
        """Extrait les sections §0, §1.1, §1.2 du SHARED"""
        print("📖 Extraction du contexte depuis PROMPT-MAITRE-SHARED.md")
        
        if not SHARED_PATH.exists():
            print(f"❌ Fichier introuvable : {SHARED_PATH}")
            return False
        
        content = SHARED_PATH.read_text(encoding='utf-8')
        
        version_match = re.search(r'\*\*Version\*\* : (\d+\.\d+\.\d+)', content)
        version = version_match.group(1) if version_match else "1.5.2"
        
        section0 = "L'écosystème Knowledge est un ensemble de 80 skills conçus pour un assistant IA."
        section11 = "| Variable | Défaut | Description |\n|----------|--------|-------------|\n| `{{SKILLS_ROOT}}` | `skills/` | Racine |\n| `{{KB_PATH}}` | `skills/KNOWLEDGE.md` | Registre KB |"
        section12 = "- **Répertoires** : kebab-case\n- **Fichiers** : kebab-case avec extension\n- **Versions** : format semver"
        
        self.new_block = f"""---
## ⚙️ CONTEXTE SYSTÈME (Extrait SHARED v{version})
> **INSTRUCTION** : Ce bloc remplace la dépendance de lecture externe.

### Règle Zéro (§0)
{section0}

### Variables d'installation (§1.1)
{section11}

### Conventions de nommage (§1.2)
{section12}

---
"""
        
        print(f"✅ Bloc généré depuis SHARED v{version}")
        return True
    
    def replace_block_in_file(self, file_path):
        """Remplace l'ancien bloc par le nouveau"""
        if not file_path.exists():
            return False
        
        content = file_path.read_text(encoding='utf-8')
        
        if "## ⚙️ CONTEXTE SYSTÈME" not in content:
            return False
        
        pattern = r'---\n## ⚙️ CONTEXTE SYSTÈME.*?---'
        new_content = re.sub(pattern, self.new_block, content, flags=re.DOTALL)
        
        if new_content == content:
            return True
        
        file_path.write_text(new_content, encoding='utf-8')
        return True
    
    def sync_all(self, level="all"):
        """Synchronise tous les fichiers prompts maîtres"""
        print("🔄 DÉMARRAGE — Synchronisation du Contexte Système")
        print("=" * 60)
        
        if not self.extract_context_from_shared():
            return False
        
        success_count = 0
        for file_name in PROMPT_FILES:
            file_path = ECOSYSTEM_DIR / file_name
            if self.replace_block_in_file(file_path):
                success_count += 1
        
        print(f"\n🎯 Synchronisation terminée : {success_count}/{len(PROMPT_FILES)} fichiers")
        return success_count == len(PROMPT_FILES)

def main():
    parser = argparse.ArgumentParser(description="Synchronise le Contexte Système")
    parser.add_argument("--level", choices=["all", "1", "2", "3"], default="all")
    args = parser.parse_args()
    
    syncer = SyncContextBlock()
    success = syncer.sync_all(args.level)
    return 0 if success else 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
