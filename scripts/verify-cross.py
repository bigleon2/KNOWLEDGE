#!/usr/bin/env python3
"""
⚙️ CONTEXTE SYSTÈME — Écosystème Knowledge (SHARED v1.6.8)
SKILLS_ROOT = skills/ | KB_PATH = skills/KNOWLEDGE.md | PROFILE = NORMAL
Conventions : kebab-case | semver | #token | {{VARIABLE}} | @historique/ (archive R4)
Règle Zéro : skills auto-contenus, KB source de vérité, dépendances YAML.

Script de vérification croisée des relations inter-skills
Version : 1.0.0
"""

import os
import json
import re
import sys
from pathlib import Path

REPO_DIR = Path(__file__).parent.parent
SKILLS_ROOT = REPO_DIR / "skills"
KB_PATH = SKILLS_ROOT / "KNOWLEDGE.md"

class VerifyCross:
    def __init__(self):
        self.checks = 0
        self.passed = 0
        self.warnings = []
        self.errors = []
    
    def check_yaml_frontmatter(self, skill_dir):
        """Vérifie la conformité du frontmatter YAML"""
        self.checks += 1
        skill_md = skill_dir / "SKILL.md"
        
        if not skill_md.exists():
            self.errors.append(f"❌ SKILL.md manquant dans {skill_dir.name}")
            return False
        
        content = skill_md.read_text(encoding='utf-8')
        
        if not content.startswith("---"):
            self.errors.append(f"❌ Frontmatter YAML manquant dans {skill_dir.name}")
            return False
        
        parts = content.split("---", 2)
        if len(parts) < 3:
            self.errors.append(f"❌ Frontmatter mal formé dans {skill_dir.name}")
            return False
        
        frontmatter = parts[1]
        required_fields = ["name:", "version:", "category:", "language:", "description:"]
        for field in required_fields:
            if field not in frontmatter:
                self.errors.append(f"❌ Champ '{field}' manquant dans {skill_dir.name}")
                return False
        
        self.passed += 1
        return True
    
    def check_context_system(self, skill_dir):
        """Vérifie la présence du §0 Contexte Système"""
        self.checks += 1
        skill_md = skill_dir / "SKILL.md"
        
        if not skill_md.exists():
            return False
        
        content = skill_md.read_text(encoding='utf-8')
        
        if "§0 — Contexte Système" not in content and "§0 — Règle zéro" not in content:
            self.errors.append(f"❌ §0 Contexte Système manquant dans {skill_dir.name}")
            return False
        
        if "Écosystème Knowledge" not in content:
            self.errors.append(f"❌ §0 incomplet dans {skill_dir.name}")
            return False
        
        if "SHARED v" not in content:
            self.warnings.append(f"⚠️ Version SHARED non spécifiée dans {skill_dir.name}")
        
        self.passed += 1
        return True
    
    def check_trigger_evals(self, skill_dir):
        """Vérifie la présence de trigger_evals.json"""
        self.checks += 1
        trigger_path = skill_dir / "evals" / "trigger_evals.json"
        
        if not trigger_path.exists():
            self.warnings.append(f"⚠️ trigger_evals.json manquant dans {skill_dir.name}")
            return False
        
        try:
            with open(trigger_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not isinstance(data, list):
                self.errors.append(f"❌ trigger_evals.json invalide dans {skill_dir.name}")
                return False
            
            for case in data:
                if "query" not in case or "should_trigger" not in case:
                    self.errors.append(f"❌ Cas invalide dans {skill_dir.name}")
                    return False
            
            self.passed += 1
            return True
        except json.JSONDecodeError:
            self.errors.append(f"❌ JSON invalide dans {skill_dir.name}")
            return False
    
    def run_full_verification(self):
        """Exécute la vérification complète"""
        print("🔍 DÉMARRAGE — Vérification croisée de l'écosystème")
        print("=" * 60)
        
        # [B13-r5 recalibrage L003] périmètre dérivé du registre KB
        # (source de vérité de l'écosystème) + skills métier du calibre
        # integrity — le scan global des 93 skills plateau ne relève pas
        # de l'écosystème personnel (skills plateforme sans version/§0,
        # régénérés par la plateforme : hors périmètre certifiable).
        kb_text = KB_PATH.read_text(encoding="utf-8") if KB_PATH.exists() else ""
        kb_names = re.findall(r"^## ([a-z0-9-]+) v\d+\.\d+\.\d+", kb_text, re.M)
        metier = ["audio-metadata", "cpp-analysis", "pdf-llm"]
        names = sorted(set(kb_names) | set(metier))
        skill_dirs = [SKILLS_ROOT / n for n in names
                      if (SKILLS_ROOT / n).is_dir()]
        
        print(f"\n📊 {len(skill_dirs)} skills détectés")
        print("-" * 60)
        
        for skill_dir in sorted(skill_dirs):
            print(f"\n🔧 Audit : {skill_dir.name}")
            self.check_yaml_frontmatter(skill_dir)
            self.check_context_system(skill_dir)
            self.check_trigger_evals(skill_dir)
        
        print("\n" + "=" * 60)
        print(f"📈 RAPPORT FINAL")
        print(f"   Vérifications : {self.checks}")
        print(f"   PASS : {self.passed}")
        print(f"   WARNINGS : {len(self.warnings)}")
        print(f"   ERRORS : {len(self.errors)}")
        
        if self.errors:
            print(f"\n❌ ERRORS :")
            for e in self.errors[:10]:
                print(f"   {e}")

        if self.warnings:
            print(f"\n⚠️ WARNINGS détaillés :")
            for w in self.warnings:
                print(f"   {w}")

        score = (self.passed / self.checks * 100) if self.checks > 0 else 0
        print(f"\n🎯 Score de conformité : {score:.1f}%")
        
        return len(self.errors) == 0

if __name__ == "__main__":
    verifier = VerifyCross()
    success = verifier.run_full_verification()
    sys.exit(0 if success else 1)
