#!/usr/bin/env python3
# PROVENANCE: session B13-r6 (N27) — audit-provenance v1.0.0, directive trace 1a0df36f356c3add ; artefact orphelin documente idempotemment
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.33 — dérivée dynamiquement)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).

Script de propagation du Contexte Système à tous les fichiers
Version : 2.1.1 (Task 71 G3 — résorption STRUCTURELLE de la classe F-70-2, 3ᵉ occurrence : la version SHARED des gabarits est désormais DÉRIVÉE DYNAMIQUEMENT du corpus vivant (KO-L003, même mécanique que generer-pm-skill.py) — un bump SHARED sans montée de l'injecteur ne peut plus jamais rétrograder les étiquettes §0 ; précédent 2.1.0 (F-70-2 Task 70 G1 : extension périmètre scripts embarqués skills/*/scripts/*.py — mise à jour idempotente des seuls porteurs d'en-tête §0, jamais d'injection ; précédent 2.0.10 (porte §0 SHARED v1.7.31 — montée gen-plan v3.37.1, session web-c30e6506 2026-11-07 : bump mécanique des 3 blocs L2/L3/L3_INNER, résorption du lag v1.7.27 hérité [cause racine : le bump SHARED v1.7.28 Task 58 G2 a propagé les 70 étiquettes manuellement SANS monter l'injecteur — toute propagation ultérieure rétrogradait les étiquettes, constat + correctif v3.37.0] ; précédent 2.0.8 : Task 60 G2 directive propriétaire : ligne « Référence canonique skill/agent » [désambiguïsation — toute référence propriétaire à « mon skill X »/« mon agent X » pointe la forme installée à la racine skills/X/, jamais le PM du corpus @mon-ecosysteme/, ex-nommé @PM-SKILLS/] ; résorption du lag L3_BLOCK_INNER resté en forme v1.7.24 au bump v2.0.7 — les trois blocs L2/L3/L3_INNER désormais alignés ; précédent 2.0.7 : ligne protocole « Règles d'or & lecture SHARED à l'exécution » [§9 SHARED])
"""

import os
import re
from pathlib import Path

REPO_DIR = Path(__file__).parent.parent
SKILLS_ROOT = REPO_DIR / "skills"

CONTEXT_BLOCK_L2 = """## §0 — Contexte Système (SHARED v1.7.31)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.
> Langue : FRANÇAIS exclusif pour tous les échanges avec le propriétaire (règle d'or n°6 gen-plan — directive 2026-10-31, renforcée 2026-11-06) : dès le PREMIER mot de toute session ou reprise, la langue d'un message, d'un résumé de continuation ou d'un canal ne dérive JAMAIS la réponse ; toute dérive est corrigée immédiatement.
> Règles d'or & lecture SHARED à l'exécution (directive propriétaire 2026-11-06 — SHARED §9) : tout skill/agent/script exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or de l'écosystème (résumé §9 — canonique gen-plan §1.5).
> Référence canonique skill/agent (directive propriétaire 2026-11-07 — SHARED §0/§1.2) : toute référence à « mon skill X »/« mon agent X » désigne la forme installée à la racine `skills/X/SKILL.md`, JAMAIS le prompt maître du corpus `@mon-ecosysteme/` (ex-nommé `@PM-SKILLS/`) — les PMs sont des spécifications générées mécaniquement (KO-L004), les skills installés sont les formes exécutables.

"""

CONTEXT_HEADER_L3 = '''"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.36)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.
Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).
Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).
Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).
"""

'''

# Contenu interne de l'en-tête L3 (utilisé par le remplacement idempotent)
# v2.0.9 : aligné sur la forme v1.7.30 (résorption du lag v1.7.27 hérité — le bump SHARED v1.7.28 Task 58 G2 avait propagé les 70 étiquettes manuellement sans monter l'injecteur)
L3_BLOCK_INNER = (
    "⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.7.31)\n"
    "SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL\n"
    "Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)\n"
    "Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.\n"
    "Langue : FRANÇAIS exclusif pour les échanges avec le propriétaire (règle d'or n°6 gen-plan — dès le premier mot de toute session ou reprise, aucune dérive).\n"
    "Règles d'or & lecture SHARED à l'exécution (SHARED §9) : tout élément exécuté lit le §0, ses sections dédiées du PM SHARED (§3/§4/§7) et les règles d'or (résumé §9 — canonique gen-plan §1.5).\n"
    "Référence canonique skill/agent (SHARED §0/§1.2) : « mon skill X »/« mon agent X » = forme installée skills/X/ à la racine, JAMAIS le PM du corpus @mon-ecosysteme/ (ex-@PM-SKILLS/).\n"
)

# v2.1.1 (Task 71 G3) : la version SHARED des gabarits est dérivée DYNAMIQUEMENT du
# corpus vivant (KO-L003) — jamais figée dans l'injecteur. Résorption structurelle
# de la classe F-70-2 (3ᵉ occurrence : le bump SHARED v1.7.32/§1.7.33 sans montée
# de l'injecteur rétrogradait les étiquettes §0 à chaque propagation).
def _version_shared():
    m = re.search(r">\s*\*\*Version\*\*\s*:\s*([0-9.]+)",
                  (REPO_DIR / "skills" / "@mon-ecosysteme" / "PROMPT-MAITRE-SHARED.md").read_text(encoding="utf-8"))
    return m.group(1) if m else "1.7.31"

_VSH = _version_shared()
CONTEXT_BLOCK_L2 = CONTEXT_BLOCK_L2.replace("(SHARED v1.7.31)", "(SHARED v%s)" % _VSH)
CONTEXT_HEADER_L3 = CONTEXT_HEADER_L3.replace("(SHARED v1.7.31)", "(SHARED v%s)" % _VSH)
L3_BLOCK_INNER = L3_BLOCK_INNER.replace("(SHARED v1.7.31)", "(SHARED v%s)" % _VSH)

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
            # Idempotence v2 : remplacement du bloc résumé existant (mise à jour de version SHARED)
            old_pattern = r'## §0 — Contexte Système \(SHARED v[0-9.]+\)\n\n(?:> [^\n]*\n)+\n'
            new_content = re.sub(old_pattern, CONTEXT_BLOCK_L2, content, count=1)
            if new_content != content:
                skill_md.write_text(new_content, encoding='utf-8')
                count += 1
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
    # F-70-2 (Task 70 G1 — tests installation $FACON2, leçon F-63-1 : le périmètre
    # doit être PROUVÉ, pas présumé) : le périmètre couvre désormais AUSSI les scripts
    # embarqués des skills (skills/*/scripts/*.py) — en MISE À JOUR idempotente des
    # seuls scripts portant déjà un en-tête §0 (jamais d'injection dans un script
    # qui n'en porte pas : les 3 STALE v1.7.17 alias-manager/orchestrer/is_client
    # étaient invisibles à la propagation précédente)
    embarques = sorted((REPO_DIR / "skills").glob("*/scripts/*.py"))
    embarques_set = set(embarques)
    for script in sorted(scripts_dir.glob("*.py")) + embarques:
        content = script.read_text(encoding='utf-8')
        
        if "CONTEXTE SYSTÈME" in content:
            # Idempotence v2 : remplacement de l'en-tête docstring résumé existant (mise à jour de version SHARED)
            # v2.0.8 : le motif consomme TOUTES les lignes normatives connues (Langue, Règles d'or §9,
            # Référence canonique §0/§1.2) — sinon les en-têtes v1.7.26+ laissent des lignes pendantes dupliquées
            old_doc = re.compile(
                r'⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge \(SHARED v[0-9.]+\)\n'
                r'SKILLS_ROOT = [^\n]*\n'
                r'Conventions : [^\n]*\n'
                r'Règle Zéro : [^\n]*\n'
                r'(?:Langue : [^\n]*\n)?'
                r"(?:Règles d'or & lecture SHARED[^\n]*\n)?"
                r'(?:Référence canonique skill/agent[^\n]*\n)?'
            )
            new_content = old_doc.sub(L3_BLOCK_INNER, content, count=1)
            if new_content != content:
                script.write_text(new_content, encoding='utf-8')
                count += 1
            continue
        
        if script in embarques_set:
            continue  # F-70-2 : jamais d'injection dans les scripts embarqués des skills
        
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
            # Idempotence v2 : remplacement du bloc résumé existant (mise à jour de version SHARED)
            old_pattern = r'## §0 — Contexte Système \(SHARED v[0-9.]+\)\n\n(?:> [^\n]*\n)+\n'
            new_content = re.sub(old_pattern, CONTEXT_BLOCK_L2, content, count=1)
            if new_content != content:
                agent_file.write_text(new_content, encoding='utf-8')
                count += 1
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
