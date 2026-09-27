#!/usr/bin/env python3
# PROVENANCE: session B13-r6 (N27) — audit-provenance v1.0.0, directive trace 1a0df36f356c3add ; artefact orphelin documente idempotemment
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.5.2)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}}
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.

Script de propagation du Contexte Système à tous les fichiers
Version : 2.0.0
"""

import os
import re
from pathlib import Path

REPO_DIR = Path(__file__).parent.parent
SKILLS_ROOT = REPO_DIR / "skills"

CONTEXT_BLOCK_L2 = """## §0 — Contexte Système (SHARED v1.5.2)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (exception)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.

"""

CONTEXT_HEADER_L3 = '''"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.5.2)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}}
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
"""

'''

def propagate_to_skills():
    """Injecte le Niveau 2 dans tous les SKILL.md"""
    print("🔄 Propagation du Contexte Système (Niveau 2) aux skills...")
    
    count = 0
    for skill_dir in sorted(SKILLS_ROOT.iterdir()):
        if not skill_dir.is_dir():
            continue
        if skill_dir.name.startswith('@') or skill_dir.name.startswith('_'):
            continue
        
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue
        
        content = skill_md.read_text(encoding='utf-8')
        
        if "§0 — Contexte Système" in content:
            continue
        
        if "§0 — Règle zéro" in content:
            old_pattern = r'## §0 — Règle zéro.*?(?=\n## §1|\n## —)'
            new_content = re.sub(old_pattern, CONTEXT_BLOCK_L2.rstrip(), content, flags=re.DOTALL)
            if new_content != content:
                skill_md.write_text(new_content, encoding='utf-8')
                count += 1
        else:
            parts = content.split("---", 2)
            if len(parts) >= 3:
                new_content = parts[0] + "---" + parts[1] + "---\n\n" + CONTEXT_BLOCK_L2 + parts[2]
            else:
                new_content = CONTEXT_BLOCK_L2 + content
            
            skill_md.write_text(new_content, encoding='utf-8')
            count += 1
    
    print(f"   ✅ {count} skills mis à jour")
    return count

def propagate_to_scripts():
    """Injecte le Niveau 3 dans tous les scripts Python"""
    print("\n🔄 Propagation du Contexte Système (Niveau 3) aux scripts...")
    
    scripts_dir = REPO_DIR / "scripts"
    if not scripts_dir.exists():
        return 0
    
    count = 0
    for script in sorted(scripts_dir.glob("*.py")):
        content = script.read_text(encoding='utf-8')
        
        if "CONTEXTE SYSTÈME" in content:
            continue
        
        if content.startswith("#!"):
            lines = content.split('\n', 1)
            new_content = lines[0] + "\n" + CONTEXT_HEADER_L3 + lines[1]
        else:
            new_content = CONTEXT_HEADER_L3 + content
        
        script.write_text(new_content, encoding='utf-8')
        count += 1
    
    print(f"   ✅ {count} scripts mis à jour")
    return count

def propagate_to_agents():
    """Injecte le Niveau 2 dans tous les fichiers .agent"""
    print("\n🔄 Propagation du Contexte Système (Niveau 2) aux agents...")
    
    agent_files = list(SKILLS_ROOT.rglob("*.agent"))
    if not agent_files:
        print("   ⚠️ Aucun fichier .agent trouvé")
        return 0
    
    count = 0
    for agent_file in sorted(agent_files):
        content = agent_file.read_text(encoding='utf-8')
        
        if "§0 — Contexte Système" in content:
            continue
        
        lines = content.split('\n')
        insert_index = 0
        for i, line in enumerate(lines):
            if line.startswith('# Agent') or line.startswith('# [nom-agent]'):
                insert_index = i + 1
                break
        
        new_lines = lines[:insert_index] + [''] + CONTEXT_BLOCK_L2.split('\n') + lines[insert_index:]
        new_content = '\n'.join(new_lines)
        
        agent_file.write_text(new_content, encoding='utf-8')
        count += 1
    
    print(f"   ✅ {count} agents mis à jour")
    return count

def main():
    print("🚀 PROPAGATION DU CONTEXTE SYSTÈME — Architecture v2.0\n")
    print("=" * 60)
    
    skills_count = propagate_to_skills()
    scripts_count = propagate_to_scripts()
    agents_count = propagate_to_agents()
    
    print("\n" + "=" * 60)
    print(f"🎉 TERMINÉ : {skills_count} skills + {scripts_count} scripts + {agents_count} agents")

if __name__ == "__main__":
    main()
