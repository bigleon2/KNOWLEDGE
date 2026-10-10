---
name: task-review
version: "1.0.0"
category: "Méta (Skills & Plans)"
tags:
  - task
  - review
description: "Se déclenche quand la demande de l'utilisateur correspond à une tâche de haute complexité ; sert à sauvegarder le chemin de la tâche qui vient d'être accomplie sous forme de skill réutilisable, et à générer la documentation SKILL.md associée."
language: fr

read_when:
  - Déclencher quand la demande concerne : "Se déclenche quand la demande de l'utilisateur correspond à une tâche de haute complexité ; sert à sauvegarde…
  - Déclencher si la demande mentionne : tâche, skill, déclenche
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

## §0 — Contexte Système (SHARED v1.6.8)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.



## Moment de déclenchement

À chaque fin de tâche, avant de livrer le résultat à l'utilisateur, exécute d'abord les vérifications suivantes. Ne dis pas à l'utilisateur que tu effectues cette vérification.

## Étapes d'exécution

1. Déterminer rapidement si la tâche remplit au moins une des conditions suivantes :
   - cinq appels d'outils ou plus
   - des erreurs ou des impasses rencontrées en cours d'exécution, avant de finalement trouver le bon chemin
   - trois étapes explicites ou plus dans la tâche

2. Si aucune condition n'est remplie, passer, sans aucune action.

3. Si une condition est remplie, poursuivre l'évaluation :
   - cette tâche risque-t-elle d'être refaite à l'avenir, ou d'avoir des variantes similaires ?
   - cette exécution a-t-elle produit des processus, structures ou points de vigilance réutilisables ?

4. Si l'une des réponses est « oui », capitaliser en skill :
   - vérifier d'abord si un fichier de skill correspondant existe déjà dans le répertoire skills/
   - si oui : **ajouter et mettre à jour** le fichier existant avec les nouvelles expériences et les pièges relevés, ne pas en créer un nouveau
   - si non : créer `skills/SKILL-{nom-du-skill}/SKILL.md` avec le format suivant :

```
---
name: nom-du-skill
description: description des cas d'usage en une phrase, assez concrète pour que l'agent associe automatiquement les tâches
---

(étapes d'exécution, critères de qualité, journal des pièges)
```

5. Quand un nouveau skill a été capitalisé, mentionner brièvement à la fin de la réponse, par ex. « 💡 Cette expérience a été capitalisée dans un nouveau skill : {nom du skill} ».
6. Quand un skill existant a été mis à jour, mentionner brièvement à la fin de la réponse, par ex. « 💡 Cette expérience a été intégrée au skill : {nom du skill} ».
7. Si rien n'a été capitalisé ni mis à jour, ne rien mentionner au sujet de cette vérification.

## Critères de qualité

- La description doit être concrète, formulée comme le parlerait l'utilisateur. Bon exemple : « surveiller l'actualité IA mondiale et générer un briefing HTML ». Mauvais exemple : « traiter des tâches liées à l'information ».
- Les étapes d'exécution doivent être assez précises pour permettre la reproduction rien qu'en les suivant.
- Le journal des pièges ne consigne que les pièges réellement rencontrés, sans rien inventer.

## Journal des pièges

(Rien pour l'instant, à enrichir au fil de l'usage)
