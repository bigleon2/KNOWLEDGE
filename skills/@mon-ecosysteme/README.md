# Écosystème Knowledge — Architecture & Guide de référence

> **Date** : 2026-10-02
> **Version** : 2.1.1
> **Architecture** : v2.2 — SHARED v1.6.3 — Contexte Système 3 niveaux
> **Révision v2.1.1 (Task 16)** : déduplication des prompts maîtres (directive propriétaire « ne garder que la dernière version ») — le corpus `@mon-ecosysteme/` ne porte plus que les PMs sources (GEN-PLAN v3.21.0, CORRECT-WORK v2.7.0, CLONE-CHAT v2.0.0) + socle ; les 19 PMs historiques sont archivés dans le nouveau dossier `skills/@historique/` (byte-identité SHA-256 scellée, distillation des particularités/améliorations/avantages par version) ; arborescence §2 recalibrée.
> **Révision v2.1.0 (Task 14)** : décision d'architecture v2.2 — canal de fichiers `download/` supprimé (déduplication, le corpus est publié uniquement via l'archive d'intégrité `download/mon-ecosysteme_archive.zip`) ; `sync-download.py` retiré de l'outillage, remplacé par la garde `scripts/task14-scan-doublons.py` ; arborescence et commandes recalibrées (certification-complete.py ajouté) ; drift SHARED §6.1 (GEN-PLAN v3.12.0 → v3.18.0) résorbé au passage.

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
├── @mon-ecosysteme/                     ← Prompts maîtres (Niveau 1) — dernières versions seules (Task 16)
│   ├── README.md                        ← Ce guide
│   ├── PROMPT-MAITRE-SHARED.md          ← Socle commun (source de vérité)
│   ├── PROMPT-MAITRE-GEN-PLAN-v3.21.0.md
│   ├── PROMPT-MAITRE-CORRECT-WORK-v2.7.0.md
│   ├── PROMPT-MAITRE-CLONE-CHAT-v2.0.0.md
│   ├── PROMPT-MAITRE-INSTALL-ECOSYSTEME.md  ← Installation (source unique v1.6.0)
│   ├── PROMPT-ULTRA-MAITRE-ORCHESTRATION.md ← Orchestration à l'usage (généré idempotent v1.0.0)
│   └── SYNC-CONTEXT.md                  ← Procédure de synchronisation
│
├── @historique/                         ← Archive des versions historiques des PMs et skills (Task 16)
│   ├── README.md                        ← Objet, règles de conservation (byte-identité R2, unicité R4)
│   ├── historiques-par-skill/{gen-plan,correct-work,clone-chat}.md ← Historique par skill (Task 17-B)
│   ├── historique-autres-elements.md ← Historique du socle non-PM (Task 17-B)
│   └── prompts-maitres/{gen-plan×15, correct-work×4} ← PMs historiques déplacés (byte-identité scellée)
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
│   ├── check-ecosysteme-integrity.py
│   ├── certification-complete.py
│   ├── task14-scan-doublons.py
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

# Certification complète (orchestrateur des 5 arbitres)
python scripts/certification-complete.py

# Garde anti-doublons download/ (décision v2.2 — 0 doublon attendu)
python scripts/task14-scan-doublons.py

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

*Fin du README.md v2.1.1*
