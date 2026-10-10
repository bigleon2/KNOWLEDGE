#!/usr/bin/env python3
# PROVENANCE: session B13-r6 (N27) — audit-provenance v1.0.0, directive trace 1a0df36f356c3add ; artefact orphelin documente idempotemment
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.6.1)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}}
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.

Script de synchronisation du Contexte Système après évolution du SHARED
Version : 2.0.1 — fix arrêt précoce (test-avant-push 2026-10-02) : l'ancien
motif non-greedy « .*?--- » s'arrêtait au premier « --- », y compris À
L'INTÉRIEUR d'une ligne de séparation de tableau « |---| », laissant un
fragment orphelin dans le bloc remplacé. Le nouveau motif ancre le remplacement
de l'en-tête du bloc jusqu'au prochain titre H2 (ou fin de fichier).
"""

import os
import re
import argparse
from pathlib import Path

REPO_DIR = Path(__file__).parent.parent
ECOSYSTEM_DIR = REPO_DIR / "skills" / "@mon-ecosysteme"
SHARED_PATH = ECOSYSTEM_DIR / "PROMPT-MAITRE-SHARED.md"

PROMPT_FILES = [
    "PROMPT-MAITRE-CLONE-CHAT-v2.0.0.md",
    "PROMPT-MAITRE-INSTALL-ECOSYSTEME.md",
]
# Recalibrage fusion v1.1.0 (2026-10-02) : INSTALL-ECOSYSTEME.md supprimé —
# source d'installation unique PROMPT-MAITRE-INSTALL-ECOSYSTEME.md (R4).
# Recalibrage Task 16 (2026-10-11) : PMs GEN-PLAN v3.11.0 et CORRECT-WORK v2.5.1
# déplacés vers skills/@historique/prompts-maitres/ (byte-identité scellée) —
# non-cibles de resynchronisation (R2, byte-identité historique assumée).
# Cibles vivantes restantes : CLONE-CHAT v2.0.0 + INSTALL-ECOSYSTEME.
# PM CORRECT-WORK v2.7.0 : porteur du bloc FIGÉ hérité de v2.5.1 (reconstitution
# méthode B1) — non-cible (SYNC-CONTEXT v1.4.1, bloc gelé R2).

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
        version = version_match.group(1) if version_match else "1.6.1"
        
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
        """Remplace l'ancien bloc par le nouveau

        Motif ancré : de l'en-tête « ## ⚙️ CONTEXTE SYSTÈME » jusqu'au
        prochain titre H2 (ou fin de fichier). Les lignes internes du bloc
        (séparateurs « --- », séparations de tableaux « |---| ») ne peuvent
        plus couper le remplacement (fix v2.0.1 — arrêt précoce).
        """
        if not file_path.exists():
            return False
        
        content = file_path.read_text(encoding='utf-8')
        
        if "## ⚙️ CONTEXTE SYSTÈME" not in content:
            return False
        
        pattern = r'## ⚙️ CONTEXTE SYSTÈME.*?(?=^## |\Z)'
        # new_block commence par « ---\n » : on le retire, le fichier porte
        # déjà son séparateur d'entrée juste avant l'en-tête du bloc.
        body = self.new_block[4:].rstrip("\n") + "\n\n---\n\n"
        new_content = re.sub(pattern, lambda m: body, content, count=1,
                             flags=re.DOTALL | re.MULTILINE)
        
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
