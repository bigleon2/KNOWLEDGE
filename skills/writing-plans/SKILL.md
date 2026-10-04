---
name: writing-plans
version: "1.0.0"
category: "Méta (Skills & Plans)"
tags:
  - writing
  - plans
description: À utiliser lorsque vous disposez d'un cahier des charges ou d'exigences pour une tâche en plusieurs étapes, avant de toucher au code
language: fr

read_when:
  - Déclencher quand la demande concerne : à utiliser lorsque vous disposez d'un cahier des charges ou d'exigences pour une tâche en plusieurs étapes, av…
  - Déclencher si la demande mentionne : utiliser, lorsque, vous
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

# Writing Plans

## Vue d'ensemble

Rédigez des plans d'implémentation complets en supposant que l'ingénieur n'a aucun contexte sur notre base de code et un goût discutable. Documentez tout ce qu'il doit savoir : quels fichiers modifier pour chaque tâche, le code, les tests, la documentation qu'il pourrait consulter, comment tester. Donnez-leur l'intégralité du plan sous forme de tâches de petite taille. DRY. YAGNI. TDD. Commits fréquents.

Supposez que c'est un développeur compétent, mais qui ne connaît presque rien à notre outillage ni à notre domaine métier. Supposez qu'il ne maîtrise pas bien la conception de bons tests.

**Annoncez au démarrage :** « J'utilise le skill writing-plans pour créer le plan d'implémentation. »

**Contexte :** ceci doit être exécuté dans un worktree dédié (créé par le skill brainstorming).

**Enregistrez les plans dans :** `docs/plans/YYYY-MM-DD-<nom-de-la-fonctionnalite>.md`

## Granularité des tâches en petites unités

**Chaque étape est une seule action (2 à 5 minutes) :**
- « Écrire le test qui échoue » — une étape
- « L'exécuter pour vérifier qu'il échoue » — une étape
- « Implémenter le code minimal pour faire passer le test » — une étape
- « Exécuter les tests et vérifier qu'ils passent » — une étape
- « Committer » — une étape

## En-tête du document de plan

**Chaque plan DOIT commencer par cet en-tête :**

```markdown
# [Feature Name] Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

---
```

## Structure des tâches

```markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**Step 1: Write the failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

**Step 3: Write minimal implementation**

```python
def function(input):
    return expected
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
```

## À retenir
- Toujours des chemins de fichiers exacts
- Du code complet dans le plan (pas « ajouter la validation »)
- Des commandes exactes avec la sortie attendue
- Référencer les skills pertinents avec la syntaxe @
- DRY, YAGNI, TDD, commits fréquents

## Transfert d'exécution

Après avoir enregistré le plan, proposez un choix d'exécution :

**« Plan terminé et enregistré dans `docs/plans/<filename>.md`. Deux options d'exécution :**

**1. Piloté par sous-agents (cette session)** — je dispatche un sous-agent neuf par tâche, revue entre les tâches, itération rapide

**2. Session parallèle (séparée)** — ouvrir une nouvelle session avec executing-plans, exécution par lots avec points de contrôle

**Quelle approche ? »**

**Si « Piloté par sous-agents » est choisi :**
- **SKILL REQUIS :** utiliser superpowers:subagent-driven-development
- Rester dans cette session
- Sous-agent neuf par tâche + revue de code

**Si « Session parallèle » est choisi :**
- Guider l'utilisateur pour ouvrir une nouvelle session dans le worktree
- **SKILL REQUIS :** la nouvelle session utilise superpowers:executing-plans
