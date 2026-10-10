---
name: quiz-mastery
version: "1.0.0"
category: "Éducation"
tags:
  - quiz
  - mastery
description: Outil de génération de questions, de quiz, de révision et de suivi de maîtrise. **Se déclenche en priorité dès que l'utilisateur emploie « réviser », « consolider » ou « revoir »**. Se déclenche aussi quand la demande touche aux « questions / révisions » : transformer un document d'apprentissage/PDF/matériel en exercices de questions (« génère quelques questions sur ce PDF »), importer un fichier de questions pour s'exercer (« j'ai un fichier de questions, aide-moi à le faire »), réviser ce qui a été appris (« révise ce qu'on a vu hier », « consolide », « revois ce d'hier », « organise mes révisions avec Ebbinghaus »), suivi de la courbe de l'oubli, notation de la maîtrise. **🔴 Règle obligatoire** : après chaque génération/import de questions réussi, **il faut impérativement demander, avant la première présentation des questions** : « veux-tu une page d'exercice web ? », et si l'utilisateur accepte → appeler le skill quiz-html. **Ne gère pas** : le suivi d'avancement des projets d'apprentissage long terme, l'élaboration de plans (→ study-buddy).
language: fr

read_when:
  - Déclencher quand la demande concerne : outil de génération de questions, de quiz, de révision et de suivi de maîtrise
  - Déclencher si la demande mentionne : questions, suivi, génération
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

## §0 — Contexte Système (SHARED v1.6.8)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.



# Quiz Mastery

## Les deux capacités centrales

### Capacité 1 : générer des questions à partir de documents d'apprentissage
1. L'utilisateur fournit un document d'apprentissage (.md / .txt / .docx / .pdf / .ppt / .pptx)
2. Appelez `generate_from_material.py` pour obtenir le prompt d'extraction des points de connaissance
3. Envoyez le prompt au LLM pour obtenir le JSON des points de connaissance
4. Appelez `service.save_knowledge_points()` pour enregistrer les points de connaissance
5. Appelez `run_quiz.py` pour générer le prompt de création de questions
6. Envoyez le prompt au LLM pour obtenir le JSON des questions
7. **⭐ Demandez à l'utilisateur s'il veut une page d'exercice web** (voir la section « Synergie avec la page web d'exercice » ci-dessous)
   - Si l'utilisateur accepte → appelez le skill `quiz-html` pour générer le HTML et l'ouvrir
   - Si l'utilisateur refuse → suivez le flux d'origine
8. Présentez les questions une à une à l'utilisateur et collectez les réponses
9. Appelez `submit_answers.py` pour soumettre à la notation

### Capacité 2 : s'exercer à partir d'un fichier de questions
1. L'utilisateur fournit un fichier de questions (.md / .txt / .docx / .pdf / .ppt / .pptx)
2. Appelez `import_quiz.py` pour obtenir le prompt d'analyse des questions
3. Envoyez le prompt au LLM pour obtenir un JSON de questions normalisé
4. Appelez `service.import_questions()` pour importer les questions et créer une session
5. **⭐ Demandez à l'utilisateur s'il veut une page d'exercice web** (voir la section « Synergie avec la page web d'exercice » ci-dessous)
   - Si l'utilisateur accepte → appelez le skill `quiz-html` pour générer le HTML et l'ouvrir
   - Si l'utilisateur refuse → suivez le flux d'origine
6. Présentez les questions une à une à l'utilisateur et collectez les réponses
7. Appelez `submit_answers.py` pour soumettre à la notation

## Quand l'utiliser (conditions de déclenchement)

1. **Demande explicite de l'utilisateur** : « génère quelques questions », « teste-moi », « un petit quiz », « des exercices », « interroge-moi »
2. **L'utilisateur dit « réviser », « consolider », « revoir »** : déclenchement direct
3. **Exercice à partir d'un fichier de questions existant** : déclenchement après téléversement d'un fichier de questions

> ⚠️ **Ne gère pas l'« exercice immédiat » de study-buddy** — cette chaîne passe par l'`exam_take` externe de study-buddy et n'appelle pas ce skill.

## Filet de sécurité sans historique de données

Quand l'utilisateur demande « réviser » mais que `data/user_progress/` est vide (nouvel utilisateur / aucune réponse enregistrée) :
- **Ne lancez pas le flux de révision de force** — il n'y a aucune donnée à réviser
- Informez proactivement l'utilisateur : « Il n'y a pas encore d'historique à réviser ; veux-tu d'abord générer des questions à partir d'un document d'apprentissage pour t'entraîner ? »
- Orientez l'utilisateur vers la « Capacité 1 : générer des questions à partir de documents d'apprentissage »

## Système de difficulté

| Niveau | Signification | Description |
|------|------|------|
| L1 | Mémorisation | Mémorisation et compréhension de base ; vérifie la reconnaissance des concepts et des faits élémentaires |
| L2 | Compréhension | Compréhension approfondie ; vérifie la distinction des concepts, l'explication des principes et l'application simple |
| L3 | Application | Mise en œuvre combinée ; vérifie l'application en situation réelle, l'analyse et la résolution de problèmes |

- **Première génération de questions** : démarrage forcé à L1
- **Réponse correcte à la difficulté courante** : monte d'un niveau (plafond L3)
- **Réponse incorrecte à la difficulté courante** : descend d'un niveau (plancher L1)

## Règles de répartition des types de questions

| Niveau | QCM | Vrai-faux | Texte à trous | Réponse courte |
|------|--------|--------|--------|--------|
| L1 | 70% | 30% | - | - |
| L2 | 50% | 20% | 30% | - |
| L3 | 40% | 20% | 20% | 20% |

## Nombre de questions

- **Par défaut, 3 questions par génération** (une même conversation présente 3 questions ; l'utilisateur répond en une fois, puis la notation est globale)
- Au maximum **15 questions par round** (l'utilisateur peut demander un ajustement du nombre)
- Générez le moins possible de questions à réponse courte, sans notation automatique (marquées `needs_review`, jugées par un LLM externe ou un humain)

## Suivi des points de connaissance faibles

- **Marquage comme faible** : nombre cumulé d'erreurs ≥ 3
- **Pas de retrait** : les points faibles ne font qu'augmenter, jamais diminuer, et restent archivés comme historique
- Les données internes sont stockées dans `data/user_progress/` (nombre d'erreurs, stade Ebbinghaus, etc.)
- **Synchronisation vers la section 3 de USER.md « points de connaissance faibles »** (écriture directe par ce skill, source=`quiz-mastery`) :
  | Point de connaissance | Nombre d'erreurs | Source | Remarques |
  - Si le point existe déjà → mettre à jour le nombre d'erreurs
  - Si absent du tableau → ajouter une ligne

## Mécanisme de révision selon la courbe de l'oubli

Basé sur la courbe de l'oubli d'Ebbinghaus, avec des révisions espacées de **1 jour → 2 jours → 4 jours → 7 jours → 15 jours** :
- Réponse correcte : review_stage +1 (progression vers l'intervalle suivant)
- Réponse incorrecte : review_stage réinitialisé à 0 (on repart du début)
- Les recommandations de révision incluent : les points de connaissance sur le point d'être oubliés + les points faibles des 3 derniers jours

## Comment appeler les scripts

### 1. Extraire les points de connaissance d'un document d'apprentissage

```bash
python3 scripts/generate_from_material.py <file_path> <document_id>
```

Sortie : le prompt d'extraction des points de connaissance (JSON) ; envoyez prompts.system_prompt et prompts.user_prompt au LLM.

### 2. Importer des questions depuis un fichier de questions

```bash
python3 scripts/import_quiz.py <file_path> <document_id> <user_id>
```

Sortie : le prompt d'analyse des questions (JSON) ; envoyez prompts.system_prompt et prompts.user_prompt au LLM.

### 3. Générer un quiz

```bash
python3 scripts/run_quiz.py <user_id> <document_id>
```

Décide automatiquement de la difficulté selon les points de connaissance enregistrés et la maîtrise actuelle de l'utilisateur, et produit le prompt de génération de questions (JSON).

### 4. Soumettre les réponses

```bash
python3 scripts/submit_answers.py <user_id> <document_id> <session_id> '<answers_json>'
```

Description des paramètres :
- `answers_json` : dictionnaire de réponses au format JSON, ex. `{"q_001": "A", "q_002": "True"}`

Retourne le résultat de la notation : score, total, accuracy, results question par question.

## Flux de génération de questions (mode d'emploi pour study-buddy)

1. Déterminez la source des points de connaissance (document d'apprentissage ou fichier de questions existant)
2. Exécutez le flux d'extraction/import correspondant
3. Appelez `run_quiz.py` pour générer le prompt de création de questions
4. **Présentez à chaque fois 3 questions à l'utilisateur** (présentation en une fois, numérotation claire, pas question par question) ; l'utilisateur répond en une fois, puis la notation est globale
5. Collectez les réponses de l'utilisateur (l'utilisateur peut renvoyer les réponses des 3 questions en une fois)
6. Appelez `submit_answers.py` pour soumettre à la notation
7. Renvoyez le résultat de la notation à study-buddy, qui l'écrira dans le fichier memory

⚠️ **Ce skill n'écrit que la section 3 de USER.md « points de connaissance faibles »** (source=`quiz-mastery`) ; il n'écrit aucune autre zone, ni `memory/`. Les autres persistances sont gérées de façon centralisée par study-buddy.

## Structure des répertoires de données

```
skills/quiz-mastery/data/
├── knowledge_points/     ← 知识点定义（按 document_id）
├── sessions/             ← 测验会话记录
└── user_progress/        ← 用户掌握度数据（含薄弱标记、遗忘曲线）
```

## ⭐ Synergie avec la page web d'exercice (coopération avec quiz-html)

Chaque fois que vous obtenez le JSON de questions (étape 7 de la « Capacité 1 », étape 5 de la « Capacité 2 »), **posez spontanément la question à l'utilisateur** :

> « Les questions sont prêtes ! Veux-tu que je les transforme en page d'exercice web ? Tu peux les faire tranquillement dans le navigateur, les erreurs sont notées automatiquement, et tu peux changer de thème ou passer un examen simulé 🎯 »

### Interprétation de la réponse de l'utilisateur

| L'utilisateur dit | Interprétation | Action |
|---|---|---|
| « oui / d'accord / vas-y / génère / page web / navigateur » | ✅ Oui | Appelez `quiz-html` |
| « non / pas la peine / laisse tomber / faisons-le ici » | ❌ Non | Suivez le flux de conversation habituel |
| Pas de réponse / ambigu | Par défaut ❌ Non | Suivez le flux d'origine, sans insister |

### Étapes concrètes d'appel de quiz-html

```python
import json, subprocess, tempfile
from pathlib import Path

# 1. 把已经拿到的题目 JSON 写到临时文件
tmp_dir = Path(tempfile.mkdtemp(prefix="quiz_"))
qjson = tmp_dir / "questions.json"
qjson.write_text(json.dumps(questions, ensure_ascii=False), encoding="utf-8")

# 2. 决定输出路径（推荐放 ~/Desktop）
output = Path.home() / "Desktop" / f"quiz_{title_slug}.html"

# 3. 调脚本
result = subprocess.run([
    "python3",
    str(Path.home() / "Desktop/studybuddy_4.0/skills/quiz-html/scripts/build_quiz_html.py"),
    str(qjson),
    "--title", page_title,        # 如 "📚 物理 · 电学练习"
    "--output", str(output),
    "--open",                     # 生成后自动用浏览器打开
], capture_output=True, text=True)

info = json.loads(result.stdout)  # {"success": true, "output_path": "...", ...}
```

### Suggestions de complétion des champs des questions

Avant l'appel, complétez idéalement les champs suivants pour chaque question (s'ils n'ont pas été générés lors de la création) :
- `category` : **catégorie de premier niveau, mot court** (2-6 caractères conseillés), pour le chip de filtrage par catégorie en haut de la page web.
  - ✅ Recommandé : `物理` / `数学` / `法律` / `历史` / `编程` / `通用`
  - ❌ À éviter : les longues chaînes avec dates/numéros/barres obliques comme `通用类 / 1.中华人民共和国证券法（1998年12月29日…）`
  - Si vous tenez à deux niveaux, séparez par `/` avec un second niveau également court : `物理 / 电学`
- `knowledge_point` : nom du point de connaissance (pour le regroupement de la barre latérale ; peut reprendre le titre KP de quiz-mastery, sans préfixe de hiérarchie)
- `memory_tip` : astuce mnémotechnique (optionnel, très utile pour les élèves du primaire/secondaire)

C'est ainsi que le filtrage par catégorie, le regroupement de la barre latérale et les cartes mémoire de la page web produisent leur effet.

### Frontières

| Tâche | Qui s'en charge |
|---|---|
| Générer des questions, extraire des questions | Ce skill (quiz-mastery) |
| Notation, suivi de maîtrise | Ce skill (quiz-mastery) |
| **Questions → page web d'exercice** | **quiz-html** |

Après avoir appelé quiz-html, **le flux de notation de quiz-mastery reste obligatoire** — l'état des réponses dans la page web sert uniquement à l'auto-vérification de l'utilisateur ; les données officielles de maîtrise doivent être écrites via `submit_answers.py`. Les deux coexistent sans conflit.
