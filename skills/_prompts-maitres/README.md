# Écosystème Knowledge — Architecture & Guide de référence

> **Date** : 2026-09-14
> **Version** : 2.0.0
> **Architecture** : v2.0 — SHARED v1.5.2 — Contexte Système 3 niveaux

---

## 1. Vue d'ensemble

L'écosystème Knowledge est un ensemble de **84 skills** conçus pour un assistant IA (9 skills écosystème + 71 skills métier + 4 skills de discipline).

### Principes fondamentaux

1. **Autonomie** : Chaque skill est auto-porteur avec son Contexte Système embarqué
2. **Décentralisation** : Le contenu spécifique est dans les skills, pas dans le SHARED
3. **Vérification** : Scripts d'arbitres pour valider la cohérence
4. **Traçabilité** : Références 📎 pour retrouver le contenu décentralisé

---

## 2. Architecture des répertoires

```
KNOWLEDGE/
├── @mon-ecosysteme/                     ← Prompts maîtres (Niveau 1)
│   ├── README.md                        ← Ce guide
│   ├── INSTALL-ECOSYSTEME.md            ← Procédure d'installation
│   ├── PROMPT-MAITRE-SHARED.md          ← Socle commun (source de vérité)
│   ├── PROMPT-MAITRE-GEN-PLAN-v3.12.0.md
│   ├── PROMPT-MAITRE-CORRECT-WORK-v2.5.1.md
│   ├── PROMPT-MAITRE-CLONE-CHAT-v2.0.0.md
│   ├── PROMPT-MAITRE-INSTALL-ECOSYSTEME.md
│   └── SYNC-CONTEXT.md                  ← Procédure de synchronisation
│
├── skills/                              ← Skills métier (Niveau 2)
│   ├── gen-plan/
│   ├── correct-work/
│   ├── clone-chat/
│   ├── skill-creator/
│   ├── autonomous-agent/
│   ├── context-engineering/
│   ├── loop-engineering/
│   ├── graph-engineering/
│   ├── harness-engineering/
│   └── ...
│
├── scripts/                             ← Scripts d'arbitres (Niveau 3)
│   ├── verify-cross.py
│   ├── verify-correct-work.py
│   ├── verify-by-sha.py
│   ├── spell-check.py
│   ├── sync-download.py
│   ├── sync-context-block.py
│   ├── propagate-context.py
│   ├── install-ecosystem.py
│   └── back-depot.py
│
├── config.json                          ← Configuration centralisée
└── .gitignore                           ← Fichiers ignorés
```

---

## 3. Les 3 niveaux de Contexte Système

### Niveau 1 : Bloc complet (Prompts maîtres)
- **Cibles** : 5 fichiers `PROMPT-MAITRE-*.md`
- **Contenu** : Règle Zéro + Variables + Conventions (complet)
- **Position** : Après le frontmatter, avant §A
- **Taille** : ~1 250 caractères

### Niveau 2 : Bloc compact (Skills et Agents)
- **Cibles** : 84 `SKILL.md` + N fichiers `.agent`
- **Contenu** : 3 lignes (Variables, Conventions, Règle Zéro)
- **Position** : `§0 — Contexte Système` (après frontmatter)
- **Taille** : ~400 caractères

### Niveau 3 : En-tête commenté (Scripts Python)
- **Cibles** : 9 scripts `.py`
- **Contenu** : 3 lignes en docstring
- **Position** : Après le shebang, avant le code
- **Taille** : ~250 caractères

---

## 4. Workflow d'utilisation

> **⚠️ NOTE (Architecture v2.0)** : Les prompts maîtres sont **auto-porteurs**. Le contexte système est embarqué directement dans chaque fichier. Aucune lecture externe n'est requise.

1. **Invoquer le prompt maître souhaité**
2. **Le contexte est automatiquement chargé** via le bloc embarqué
3. **Suivre les instructions** du fichier spécifique
4. **Utiliser les scripts** pour vérifier la cohérence

---

## 5. Décentralisation du SHARED

Les informations spécifiques à un skill ont été extraites du SHARED et intégrées directement dans les fichiers concernés.

### Sections décentralisées

| Section SHARED | Fichier destination | Référence |
| :--- | :--- | :--- |
| §1.3 YAML frontmatter | `skill-creator/SKILL.md §2` | 📎 Décentralisé |
| §1.4 Worklog | `autonomous-agent/SKILL.md §2.1` | 📎 Décentralisé |
| §2.2 Template entrées KB | `skills-inventory/SKILL.md §2.1` | 📎 Décentralisé |
| §2.3 Protocole Découverte | `skills-inventory/SKILL.md §2.2` | 📎 Décentralisé |
| §3.2 Cross-references | `correct-work/SKILL.md §3` | 📎 Décentralisé |
| §4 Matrice agents | `autonomous-agent/SKILL.md §2.2` | 📎 Décentralisé |
| §5 Format SKILL.md | `skill-creator/SKILL.md §3` | 📎 Décentralisé |

### Sections conservées dans le SHARED

- §0 : Règle Zéro
- §1.1 : Variables d'installation
- §1.2 : Conventions de nommage
- §2.1 : Rôle du registre KB
- §3.1 : Tableau complet des relations
- §6 : Architecture des prompts maîtres
- §7 : Définitions des 5 disciplines

---

## 6. Scripts d'arbitres

### Scripts de vérification

```bash
# Vérification croisée des relations
python scripts/verify-cross.py --check-context

# Vérification des outputs correct-work
python scripts/verify-correct-work.py

# Vérification par empreinte SHA
python scripts/verify-by-sha.py --generate  # Première exécution
python scripts/verify-by-sha.py              # Vérifications suivantes

# Vérification orthographique
python scripts/spell-check.py
```

### Scripts de propagation

```bash
# Propagation du Contexte Système à tous les fichiers
python scripts/propagate-context.py

# Synchronisation après évolution du SHARED
python scripts/sync-context-block.py --level all
```

### Scripts d'infrastructure

```bash
# Installation complète de l'écosystème
python scripts/install-ecosystem.py

# Synchronisation du cache download
python scripts/sync-download.py

# Backup du dépôt
python scripts/back-depot.py
```

---

## 7. Procédure de synchronisation

Voir `SYNC-CONTEXT.md` pour la procédure détaillée.

**Commande rapide** :
```bash
python scripts/sync-context-block.py --level all
```

---

## 8. Configuration centralisée

Le fichier `config.json` à la racine contient toutes les variables globales :

```json
{
  "ecosystem": {
    "name": "Knowledge",
    "version": "2.0.0",
    "skills_root": "skills/",
    "kb_path": "skills/KNOWLEDGE.md"
  },
  "context_system": {
    "enabled": true,
    "shared_version": "1.5.2",
    "levels": { ... }
  }
}
```

---

## 9. Installation

```bash
# Cloner le dépôt
git clone https://github.com/bigleon2/KNOWLEDGE.git
cd KNOWLEDGE

# Exécuter le script d'installation
python scripts/install-ecosystem.py

# Vérifier l'installation
python scripts/verify-cross.py --check-context
```

---

## 10. Correction de l'écosystème

Pour exécuter la correction complète de l'écosystème :

```bash
# Exécution complète
corrige-ecosysteme

# Ou phase par phase
corrige-ecosysteme:phase-A
corrige-ecosysteme:phase-B
...
corrige-ecosysteme:phase-I
```

**Durée estimée** : 3h30
**Résultat** : Écosystème stable, autonome, vérifiable

---

*Fin du README.md v2.0.0*
