---
name: task-review
description: Lorsque l'instruction de l'utilisateur est une tâche à haute complexité, elle est déclenchée pour enregistrer le chemin de la tâche terminée comme une réutilisable compétence, et générer le document SKILL.md correspondant.
---

## §0 — Contexte Système (SHARED v1.7.14)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.



## Moment de déclenchement (chù fā shí jī)

Avant de livrer les résultats à l'utilisateur à la fin de chaque tâche, exécutez d'abord les vérifications suivantes. Ne dites pas à l'utilisateur que vous effectuez ces vérifications.

## Étapes d'exécution

1. Vérifier rapidement si la tâche remplit l'une des conditions suivantes :
   - 5 appels d'outils ou plus
   - des erreurs ou des impasses rencontrées pendant l'exécution, avec le bon chemin finalement trouvé
   - la tâche comporte 3 étapes explicites ou plus

2. Si aucune des conditions ci-dessus n'est remplie, passez à la suite, sans effectuer aucune opération.

3. Si satisfait, continuer l'évaluation :
   - Cette tâche sera-t-elle susceptible d'être répétée ou d'avoir des variantes similaires à l'avenir ?
   - Durant cette exécution, y a-t-il des processus, structures ou points d'attention réutilisables ?

4. Si l'un est "oui", alors consolider en compétences :
   - D'abord vérifier s'il existe déjà un fichier de compétence correspondant dans le répertoire skills/
   - Si oui : ajouter et mettre à jour les nouvelles expériences et les enregistrements d'échecs dans le fichier original, ne pas créer de nouveau
   - Si non : créer un nouveau `skills/SKILL-{Jineng Mingcheng}/SKILL.md`, formaté comme suit :

```
---
name: nom de la skill (Jineng Mingcheng)
description: description en une phrase du scénario d'usage, assez précise pour que l'agent apparie automatiquement les tâches (Yi juhua miaoshu shiyong changjing, yao juti dao neng rang agent zidong pipei renwu)
---

（Étapes d'exécution, standards de qualité, enregistrement des pièges）
```

5. Quand une nouvelle skill est capitalisée, il faut le mentionner brièvement en fin de réponse, par exemple"💡 cette expérience est désormais consolidée en une nouvelle skill :{nom de la skill}" (jīngyàn yǐ chéndiàn wéi xīn jìnéng)。
6. Quand une skill existante est mise à jour, il faut le mentionner brièvement en fin de réponse, par exemple"💡 cette expérience a été intégrée à la skill :{nom de la skill}" (jìnéng)。
7. Quand aucune skill n'est capitalisée ni mise à jour, ne rien mentionner de ce contrôle.

## Standards de qualité

- description doit être spécifique, rédigée en utilisant les mots que l'utilisateur emploierait. Bon exemple : "Surveiller les actualités mondiales sur l'IA et générer un bulletin HTML". Mauvais exemple : "Traiter des tâches liées à l'information".
- Les étapes d'exécution doivent être suffisamment détaillées pour pouvoir être reproduites en suivant les instructions.
- Les notes sur les difficultés rencontrées doivent uniquement documenter les vrais obstacles, ne pas inventer.

## Journal des pièges (Cai Ji Lu)

（aucun pour l'instant, s'accumulera à l'usage）
