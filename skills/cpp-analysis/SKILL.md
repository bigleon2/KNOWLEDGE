---
name: cpp-analysis
version: 1.0.0
date: 2026-06-21
description: >
  Analyse de code C/C++ — Détection de bugs, optimisation de performance, 
  analyse de complexité, génération de documentation. Supporte C, C++, C++11/14/17/20.
  Use when the user needs to analyze C/C++ code, find bugs, optimize performance, 
  or generate documentation.
description-fr: >
  Analyse de code C/C++ — Détection de bugs, optimisation de performance,
  analyse de complexité, génération de documentation. Supporte C, C++, C++11/14/17/20.
  Utiliser quand l'utilisateur a besoin d'analyser du code C/C++, trouver des bugs,
  optimiser les performances, ou générer de la documentation.
---

# cpp-analysis

## Description

Skill d'analyse de code C/C++ pour détection de bugs, optimisation et documentation.

## Capacités

### 1. Détection de Bugs
- Fuites de mémoire (memory leaks)
- Buffer overflows
- Null pointer dereferences
- Race conditions (multithreading)
- Undefined behavior
- Violations de règles (MISRA, CERT)

### 2. Optimisation de Performance
- Analyse de complexité algorithmique (O(n))
- Détection de code inefficace
- Suggestions d'optimisation
- Profiling et benchmarking
- Optimisation mémoire

### 3. Analyse de Qualité
- Métriques de code (lignes, complexité, couverture)
- Détection de code dupliqué
- Analyse de dépendances
- Respect des standards (ISO C/C++)

### 4. Génération de Documentation
- Documentation automatique (Doxygen)
- Génération de diagrammes
- Documentation d'API
- Commentaires inline

### 5. Refactoring
- Suggestions de refactoring
- Modernisation de code (C++11 → C++20)
- Amélioration de lisibilité
- Réduction de complexité

## Outils d'Analyse

### Static Analysis
- **cppcheck** : Détection de bugs et de problèmes de sécurité
- **clang-tidy** : Linting et suggestions de refactoring
- **flawfinder** : Détection de vulnérabilités de sécurité
- **rats** : Rough audit tool for security

### Dynamic Analysis
- **valgrind** : Détection de fuites mémoire
- **gprof** : Profiling de performance
- **gcov** : Couverture de code

### Documentation
- **doxygen** : Génération de documentation
- **graphviz** : Diagrammes de dépendances

## Scripts d'Analyse Typiques

### Script 1 : Analyse Complète avec cppcheck
```bash
#!/bin/bash
# Analyse complète d'un projet C/C++

PROJECT_DIR="/home/z/my-project/cpp-project"
REPORT_DIR="/home/z/my-project/reports/cpp"

mkdir -p $REPORT_DIR

echo "🔍 Analyse avec cppcheck..."
cppcheck --enable=all --inconclusive --xml $PROJECT_DIR 2> $REPORT_DIR/cppcheck.xml

echo "📊 Génération rapport HTML..."
cppcheck --enable=all --html-report=$REPORT_DIR/cppcheck-report $PROJECT_DIR

echo "✅ Analyse terminée"
echo "Rapport : $REPORT_DIR/cppcheck-report/index.html"
```

### Script 2 : Détection de Fuites Mémoire avec Valgrind
```bash
#!/bin/bash
# Détection de fuites mémoire

EXECUTABLE="./my-program"
REPORT="valgrind-report.txt"

echo "🔍 Analyse avec valgrind..."
valgrind --leak-check=full --show-leak-kinds=all --track-origins=yes \
  --log-file=$REPORT $EXECUTABLE

echo "✅ Analyse terminée"
echo "Rapport : $REPORT"
```

### Script 3 : Analyse de Complexité
```python
#!/usr/bin/env python3
"""Analyse de complexité de code C/C++"""
import re
from pathlib import Path

def analyze_complexity(file_path):
    """Analyse la complexité cyclomatique d'un fichier C/C++"""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Compter les structures de contrôle
    complexity = 1  # Complexité de base
    
    # Boucles
    complexity += len(re.findall(r'\b(for|while|do)\b', content))
    
    # Conditions
    complexity += len(re.findall(r'\b(if|else if|switch|case)\b', content))
    
    # Opérateurs logiques
    complexity += len(re.findall(r'&&|\|\|', content))
    
    return complexity

def analyze_project(directory):
    """Analyse tous les fichiers C/C++ d'un projet"""
    results = []
    
    for ext in ['*.c', '*.cpp', '*.cc', '*.cxx', '*.h', '*.hpp']:
        for file_path in Path(directory).rglob(ext):
            complexity = analyze_complexity(file_path)
            results.append({
                'file': str(file_path),
                'complexity': complexity,
                'lines': len(file_path.read_text().splitlines())
            })
    
    return results

if __name__ == '__main__':
    results = analyze_project('/home/z/my-project/cpp-project')
    
    print(f"Analysé {len(results)} fichiers")
    for r in sorted(results, key=lambda x: x['complexity'], reverse=True)[:10]:
        print(f"  {r['file']}: complexité {r['complexity']}, {r['lines']} lignes")
```

### Script 4 : Génération de Documentation Doxygen
```bash
#!/bin/bash
# Génération de documentation avec Doxygen

PROJECT_DIR="/home/z/my-project/cpp-project"
DOXYFILE="Doxyfile"

# Créer le fichier de configuration Doxygen
cat > $DOXYFILE << 'EOF'
PROJECT_NAME           = "Mon Projet C++"
OUTPUT_DIRECTORY       = docs
INPUT                  = src
RECURSIVE              = YES
GENERATE_HTML          = YES
GENERATE_LATEX         = NO
EXTRACT_ALL            = YES
EXTRACT_PRIVATE        = YES
EXTRACT_STATIC         = YES
EOF

echo "📚 Génération de documentation..."
doxygen $DOXYFILE

echo "✅ Documentation générée"
echo "Ouvrir : docs/html/index.html"
```

## Intégration avec Autres Skills

- **coding-agent** : Workflow de développement C/C++
- **python-executor** : Exécution de scripts d'analyse
- **pdf-expert** : Génération de rapports d'analyse

## Cas d'Usage

1. "Analyse ce code C++ et trouve les bugs"
2. "Optimise les performances de ce programme"
3. "Génère la documentation de mon projet C++"
4. "Détecte les fuites mémoire"
5. "Analyse la complexité de mon code"

## Déclenches

- "analyse code C++"
- "détecte bugs C/C++"
- "optimise performance C++"
- "génération documentation C++"
- "analyse complexité"

---

**Skill créé le 2026-06-21 pour François — DJ TRAKTOR, développeur C/C++**