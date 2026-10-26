---
nom: task-review
source: skills/task-review/SKILL.md
sha256_source: 54f81e9d2608
genere: 2026-10-26 (phase P2 — directive 10 tâches, tâche 2)
usage: AUTONOME hors écosystème (dossier « Prompt Maitre » — non lu par l'orchestration)
---

> ⚠️ **MARQUEUR D'EXCLUSION (garde D010)** — CE DOSSIER N'EST PAS LU PAR L'ORCHESTRATION. Les dossiers « Prompt Maitre » sont des prompts autonomes à usage HORS écosystème : ils ne sont pas indexés au registre KB, ne sont mobilisés par aucun arbitre, et ne remplacent jamais la forme installée `skills/<skill>/` (source de vérité).

# Prompt Maître autonome — task-review (version non déclarée)

## Comment utiliser ce prompt (hors écosystème)

Ce document encapsule la compétence sous forme autonome : copiez-le intégralement
dans un assistant IA (ou ouvrez-le en référence directe) — aucune installation,
aucun registre, aucune dépendance à l'écosystème Knowledge d'origine n'est requise.
Les variables de l'écosystème d'origine ont été résolues en valeurs littérales ;
si des ressources `references/` accompagnent ce dossier, elles sont jointes au même
emplacement et le prompt y renvoie par leur chemin relatif. La version d'origine
(source de vérité) vit dans `skills/task-review/SKILL.md` du dépôt KNOWLEDGE.

---

## Le prompt

---
name: task-review
description: Lorsque l'instruction de l'utilisateur est une tâche à haute complexité, elle est déclenchée pour enregistrer le chemin de la tâche terminée comme une réutilisable compétence, et générer le document SKILL.md correspondant.
---

## §0 — Contexte Système (SHARED v1.7.13)

> Écosystème Knowledge : `skills/`=skills/ | `skills/KNOWLEDGE.md`=skills/KNOWLEDGE.md | `true`=true | `NORMAL`=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.



## 触发时机 (chù fā shí jī)

Avant de livrer les résultats à l'utilisateur à la fin de chaque tâche, exécutez d'abord les vérifications suivantes. Ne dites pas à l'utilisateur que vous effectuez ces vérifications.

## 执行步骤

1. 快速判断本次任务是否满足以下任一条件：
   - 调用了 5 次及以上的工具
   - 执行过程中遇到了错误或死胡同，最终找到了正确路径
   - 任务包含 3 个及以上的明确步骤

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
name: 技能名称 (Jineng Mingcheng)
description: 一句话描述适用场景，要具体到能让 agent 自动匹配任务 (Yi juhua miaoshu shiyong changjing, yao juti dao neng rang agent zidong pipei renwu)
---

（Étapes d'exécution, standards de qualité, enregistrement des pièges）
```

5. 当积累了新技能时，必须在回复末尾简短提一句，例如"💡 本次经验已沉淀为新技能：{技能名称}" (jīngyàn yǐ chéndiàn wéi xīn jìnéng)。
6. 当更新了已有技能时，必须在回复末尾简短提一句，例如"💡 本次经验已更新到技能中：{技能名称}" (jìnéng)。
7. 当没有积累或更新技能时，不提及任何关于此检查的内容。

## Standards de qualité

- description doit être spécifique, rédigée en utilisant les mots que l'utilisateur emploierait. Bon exemple : "Surveiller les actualités mondiales sur l'IA et générer un bulletin HTML". Mauvais exemple : "Traiter des tâches liées à l'information".
- Les étapes d'exécution doivent être suffisamment détaillées pour pouvoir être reproduites en suivant les instructions.
- Les notes sur les difficultés rencontrées doivent uniquement documenter les vrais obstacles, ne pas inventer.

## 踩坑记录 (Cai Ji Lu)

（暂无，随使用积累）


---

## Ressources locales du dossier

Aucune ressource annexe — ce prompt est auto-suffisant.
