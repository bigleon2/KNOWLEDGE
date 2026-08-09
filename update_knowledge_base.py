#!/usr/bin/env python3
"""
Script de mise à jour automatisée de l'écosystème KNOWLEDGE (Version Windows/Universelle).
Met à jour cpp-analysis (v2.0.0), correct-work (v2.0.0), gen-plan (v3.1.0),
applique la règle S4 MK2, sauvegarde l'environnement et synchronise avec Git.
"""
import os
import sys
import shutil
import subprocess
import zipfile
from pathlib import Path
from datetime import datetime

# --- CONFIGURATION ---
# Utilise le dossier courant (d'où le script est lancé) comme environnement cible
ENV_DIR = Path.cwd() 
BACKUP_DIR = ENV_DIR / "backups"

SKILL_CPP_FILE = ENV_DIR / "skills" / "cpp-analysis" / "SKILL.md"
SKILL_CORRECT_FILE = ENV_DIR / "skills" / "correct-work" / "SKILL.md"
SKILL_GENPLAN_FILE = ENV_DIR / "skills" / "gen-plan" / "SKILL.md"
KNOWLEDGE_FILE = ENV_DIR / "knowledge" / "knowledge.md"
README_FILE = ENV_DIR / "knowledge" / "readme.md"

# --- CONTENU DES SKILLS ---

CPP_ANALYSIS_V2 = """---
name: cpp-analysis
version: 2.0.0
date: 2026-07-10
authors: [Z AI, Francois]
description: >
  Advanced C/C++ Code Analysis — Bug detection, performance optimization, 
  real-time audio/DSP optimization, complexity analysis, and documentation. 
  Supports C, C++11/14/17/20/23.
description-fr: >
  Analyse avancée de code C/C++ — Détection de bugs, optimisation des performances,
  optimisation audio temps réel (DSP), analyse de complexité et génération de documentation.
  Supporte C, C++11/14/17/20/23.
---

# cpp-analysis

## Description
Skill d'analyse de code C/C++ pour détection de bugs, optimisation, traitement audio temps réel et documentation.

## Capacités
### 1. Détection de Bugs
* Fuites de mémoire, Buffer overflows, Null pointer, Race conditions, Undefined behavior.
### 2. Optimisation de Performance & Temps Réel
* **Optimisation Audio/DSP (Temps Réel)** : Détection d'allocations mémoire dans le "hot path", vérification de code lock-free, prévention des xruns/dropouts pour les setups DJ (ex: TRAKTOR, KONTROL S4 MK2).
### 3. Analyse de Qualité & Documentation & Refactoring
* Métriques, Doxygen, Graphviz, Modernisation C++11 → C++20/23.

## Outils d'Analyse
* **Static** : cppcheck, clang-tidy, flawfinder.
* **Dynamic & Sanitizers** : GCC/Clang Sanitizers (ASan, UBSan, TSan), Valgrind, gprof.

## Scripts d'Analyse Typiques
### Script 3 : Analyse de Complexité Cyclomatique (Robuste)
*Note : Nécessite l'installation de `lizard` (`pip install lizard`)*
```python
import subprocess, json, sys
def analyze_project(directory):
    try:
        result = subprocess.run(["lizard", "-l", "cpp", "-J", directory], capture_output=True, text=True, check=True)
        return json.loads(result.stdout).get('functions', [])
    except FileNotFoundError:
        print("❌ lizard n'est pas installé. Installez-le avec: pip install lizard")
        sys.exit(1)