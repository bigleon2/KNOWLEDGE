# Procédure de Synchronisation du Contexte Système

> **Version** : 1.0.0
> **Date** : 2026-09-14
> **Objet** : Maintenir la cohérence entre `PROMPT-MAITRE-SHARED.md` (source de vérité) et les blocs `## ⚙️ CONTEXTE SYSTÈME` embarqués dans les prompts maîtres.

## Contexte

Le bloc `## ⚙️ CONTEXTE SYSTÈME` présent dans chaque prompt maître actif est une **copie figée** des sections §0, §1.1 et §1.2 du fichier `PROMPT-MAITRE-SHARED.md` à la version v1.5.2.

Si le SHARED évolue (nouvelles conventions, nouvelles variables, correction de règles), les blocs embarqués doivent être resynchronisés.

## Fichiers concernés par la synchronisation

| # | Fichier | Niveau | Emplacement du bloc |
| :--- | :--- | :---: | :--- |
| 1 | `PROMPT-MAITRE-GEN-PLAN-v3.12.0.md` | N1 | Après le frontmatter |
| 2 | `PROMPT-MAITRE-CORRECT-WORK-v2.5.1.md` | N1 | Après le frontmatter |
| 3 | `PROMPT-MAITRE-CLONE-CHAT-v2.0.0.md` | N1 | Après le frontmatter |
| 4 | `PROMPT-MAITRE-INSTALL-ECOSYSTEME.md` | N1 | Après le frontmatter |
| 5 | `INSTALL-ECOSYSTEME.md` | N1 | Après l'en-tête |
| 6 | Tous les `SKILL.md` (84 fichiers) | N2 | §0 — Contexte Système |
| 7 | Tous les fichiers `.agent` | N2 | Après le titre |
| 8 | Tous les scripts `.py` (9 fichiers) | N3 | Docstring en en-tête |

## Procédure étape par étape

### Étape 1 : Modifier la source de vérité
Éditer `PROMPT-MAITRE-SHARED.md` avec les nouvelles informations.

### Étape 2 : Incrémenter la version
Mettre à jour le champ `Version` dans l'en-tête du SHARED.
Exemple : `v1.5.2` → `v1.6.0` (si nouvelle convention), `v1.5.3` (si correction mineure).

### Étape 3 : Exécuter le script de synchronisation
```bash
python scripts/sync-context-block.py --level all
```

### Étape 4 : Vérifier avec verify-cross.py
```bash
python scripts/verify-cross.py --check-context
```

### Étape 5 : Commit
```bash
git add .
git commit -m "chore(shared): synchronisation Contexte Système v[X.Y.Z]"
git push origin main
```

## Fréquence recommandée

- **À chaque modification du SHARED** : Synchronisation immédiate requise.
- **Audit trimestriel** : Vérifier que les blocs embarqués correspondent toujours à la version courante du SHARED.

## Commandes rapides

```bash
# Synchroniser uniquement les prompts maîtres (Niveau 1)
python scripts/sync-context-block.py --level 1

# Synchroniser uniquement les skills (Niveau 2)
python scripts/propagate-context.py

# Synchroniser uniquement les scripts (Niveau 3)
# (propagate-context.py couvre aussi les scripts)
python scripts/propagate-context.py
```

## En cas de conflit

Si la synchronisation automatique échoue :
1. Identifier le fichier problématique
2. Supprimer manuellement l'ancien bloc Contexte Système
3. Réexécuter le script de synchronisation
4. Vérifier avec `verify-cross.py`
