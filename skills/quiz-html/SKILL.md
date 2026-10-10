---
name: quiz-html
version: "1.0.0"
category: "Éducation"
tags:
  - quiz
  - html
description: Transforme un tableau de questions en une **page d'exercice web autonome** (fichier HTML). Lorsque l'utilisateur vient de terminer le flux « générer des questions à partir d'un document » ou « extraire des questions d'un fichier » de quiz-mastery, proposez proactivement de « s'entraîner dans une page web » ; après confirmation, appelez ce skill pour injecter les questions dans le template et générer un HTML à l'utilisateur. Se déclenche aussi quand l'utilisateur dit directement « fais-moi une page web / HTML / d'exercice avec ces questions ». **Ne gère pas** : la génération de questions (→ quiz-mastery), la notation (→ quiz-mastery), les plans de révision long terme (→ study-buddy).
language: fr

read_when:
  - Déclencher quand la demande concerne : transforme un tableau de questions en une **page d'exercice web autonome** (fichier HTML)
  - Déclencher si la demande mentionne : questions, page, html
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

## §0 — Contexte Système (SHARED v1.6.8)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.



# Générateur de banque de questions web (Quiz HTML Builder)

Transforme un tableau JSON de questions → une **page web d'exercice HTML en fichier unique**, comprenant :
- 📂 Filtres par catégorie (matière / sous-module) + filtres par statut d'apprentissage (maîtrisé / non traité / erreurs)
- 🎯 Prise en charge de 4 types de questions : QCM / vrai-faux / texte à trous / réponse courte
- 🤖 Marquage automatique des réponses, les erreurs partent automatiquement dans le cahier d'erreurs (une seconde chance au premier échec)
- ⌨️ Raccourcis clavier complets (A/B/C/D · Entrée · flèches · Espace)
- 📝 Mode examen simulé (temps limité + soumission unique + page de résultats)
- 🌓 Bascule thème clair/sombre · persistance localStorage · adaptation mobile

## Scénarios de déclenchement principaux

### Scénario 1 : proposition proactive après génération/import par quiz-mastery ⭐
C'est **l'entrée principale** de ce skill. Quand `quiz-mastery` vient de terminer l'un des flux suivants :
- « Générer des questions à partir d'un document » : `generate_from_material.py` → génère le JSON de questions → `service.import_questions()` enregistre en base
- « Extraire depuis un fichier de questions » : `import_quiz.py` → parse le JSON de questions → enregistre en base

Après la génération par quiz-mastery et avant de présenter les questions à l'utilisateur, **posez spontanément la question** :
> « Les questions sont prêtes ! Veux-tu que je les transforme en page d'exercice web ? Tu peux les faire tranquillement dans le navigateur, les erreurs sont notées automatiquement, et tu peux changer de thème ou passer un examen simulé 🎯 »

Si l'utilisateur répond par l'affirmative (« oui », « d'accord », « vas-y », « génère la page »…) → appelez ce skill.
Si l'utilisateur refuse (« non », « pas la peine », « faisons-le ici ») → suivez le flux habituel d'exercice en conversation.

### Scénario 2 : l'utilisateur demande directement une page web
Mots-clés déclencheurs :
- « transforme ces questions en page web », « fais une page d'exercice HTML », « génère une page de banque de questions »
- « je veux m'entraîner dans le navigateur », « fais une version web »
- « exporte les questions en HTML »

## Comment l'appeler

### En une phrase
```bash
python3 scripts/build_quiz_html.py <题目JSON文件> [--title "..." --open]
```

### Flux standard

1. **Obtenir le JSON de questions** (tableau ; chaque élément est une question)
   - Source A : sortie LLM de quiz-mastery après génération (déjà au format standard côté système)
   - Source B : tableau de questions collé directement par l'utilisateur
   - Source C : questions lues depuis la base (quiz-mastery, `data/sessions/<sid>/questions.json`)

2. **Écrire dans un fichier JSON temporaire** :
   ```python
   import json, tempfile
   from pathlib import Path
   tmp = Path(tempfile.mkdtemp()) / "questions.json"
   tmp.write_text(json.dumps(questions, ensure_ascii=False), encoding="utf-8")
   ```

3. **Appeler le script** :
   ```bash
   python3 ~/Desktop/studybuddy_4.0/skills/quiz-html/scripts/build_quiz_html.py \
       /tmp/xxx/questions.json \
       --title "📚 物理 · 热学练习" \
       --output ~/Desktop/quiz_物理热学_20260518.html \
       --open
   ```

4. **Parser le JSON retourné** :
   ```json
   {
     "success": true,
     "output_path": "/Users/.../quiz_xxx.html",
     "question_count": 8,
     "title": "📚 物理 · 热学练习",
     "subtitle": "共 8 题 · 选择×5 · 判断×2 · 填空×1 · 物理",
     "id": "q_1779091201",
     "size_bytes": 63752
   }
   ```

5. **Informer l'utilisateur** : indiquez le chemin du HTML et précisez « la page est déjà ouverte dans le navigateur, tu peux commencer ✨ »

## Standard des champs JSON des questions

Totalement compatible avec le format de sortie de quiz-mastery, **champs optionnels ajoutés** : `category` / `memory_tip` :

| Champ | Obligatoire | Description |
|---|---|---|
| `type` | ✅ | `single_choice` / `true_false` / `fill_blank` / `short_answer` |
| `prompt` | ✅ | Énoncé. Le champ `question` est aussi accepté (conversion automatique) |
| `options` | Obligatoire pour les QCM | `["A. xxx", "B. yyy", ...]` |
| `answer` | ✅ | Lettre pour les QCM ; `"True"`/`"False"` pour vrai-faux ; texte pour trous/réponse courte |
| `explanation` | Recommandé | Corrigé (fortement recommandé, indispensable pour les élèves du primaire/secondaire) |
| `knowledge_point` | Recommandé | Nom du point de connaissance (utilisé pour le regroupement secondaire de la barre latérale) |
| `category` | Recommandé | Chemin de catégorie, **au format « matière / sous-module »** : `"物理 / 电学"`, `"数学 / 分数"` |
| `level` | Optionnel | Difficulté 1-3 |
| `memory_tip` | Optionnel | Astuce mnémotechnique, mise en évidence par une carte orange (arme fatale K12) |

### Exemple
```json
[
  {
    "type": "single_choice",
    "prompt": "下列关于并联电路电流规律的说法，正确的是（    ）。",
    "options": [
      "A. 干路电流等于各支路电流之差",
      "B. 干路电流等于各支路电流之和",
      "C. 各支路电流相等",
      "D. 干路电流大于任一支路电流的两倍"
    ],
    "answer": "B",
    "explanation": "并联电路中，**干路电流等于各支路电流之和**：I = I₁ + I₂ + ...",
    "knowledge_point": "并联电路电流规律",
    "category": "物理 / 电学",
    "level": 1,
    "memory_tip": "🧠 并联看路口：进多少、出多少，电流不会消失"
  }
]
```

## Principes de conception

### 1. Category automatique, pour que les filtres aient du sens
Si le champ `category` manque, ajoutez-le autant que possible (même par déduction de la matière). Sinon toutes les questions s'entassent dans la catégorie « général » et le filtre par catégorie devient inutile.

### 2. Category au format « matière / sous-module »
- ✅ `"物理 / 电学"`, `"物理 / 热学"` → 4 chips de sous-catégories apparaissent en haut de page
- ❌ `"物理"` → une seule puce ; les sous-modules apparaissent dans la barre latérale, mais la granularité du filtrage devient grossière

### 3. Points de connaissance et catégories ne sont pas le même niveau
- `category` = catégorie horizontale (quelle matière / quel chapitre), pour le **filtrage par chips en haut de page**
- `knowledge_point` = point de connaissance à granularité fine, pour le **regroupement secondaire de la barre latérale gauche**

### 4. Nommage du fichier de sortie
Par défaut, la sortie va dans le même répertoire que le JSON de questions, avec un nom `quiz_<title_slug>_<horodatage>.html`.
**Il est conseillé de passer explicitement `--output`**, vers `~/Desktop/` ou un répertoire fixe pour que l'utilisateur le retrouve facilement.

## Exemple de travail (chaîne complète avec quiz-mastery)

```python
# 1. quiz-mastery 已完成出题，拿到题目数组
questions = [
    {"type": "single_choice", "prompt": "...", "options": [...], "answer": "A",
     "explanation": "...", "knowledge_point": "...", "category": "物理 / 电学"},
    # ...
]

# 2. agent 问用户："要不要做成网页版？"
# 3. 用户："要"
# 4. agent 写临时文件 + 调用 skill

import json, subprocess, tempfile
from pathlib import Path

tmp_dir = Path(tempfile.mkdtemp(prefix="quiz_"))
qjson = tmp_dir / "questions.json"
qjson.write_text(json.dumps(questions, ensure_ascii=False), encoding="utf-8")

output = Path.home() / "Desktop" / "quiz_物理电学.html"

result = subprocess.run([
    "python3",
    str(Path.home() / "Desktop/studybuddy_4.0/skills/quiz-html/scripts/build_quiz_html.py"),
    str(qjson),
    "--title", "📚 物理 · 电学练习",
    "--output", str(output),
    "--open",
], capture_output=True, text=True)

info = json.loads(result.stdout)
# info["output_path"] = "/Users/.../Desktop/quiz_物理电学.html"
```

Puis informez l'utilisateur :
> « C'est prêt ! La page s'est ouverte automatiquement ✨
> Chemin : `~/Desktop/quiz_物理电学.html`
> Fais les questions tranquillement ; les erreurs seront enregistrées automatiquement, et tu pourras filtrer sur « erreurs » la prochaine fois pour les retravailler 💪 »

## Frontières avec les autres skills

| Tâche | Qui s'en charge |
|---|---|
| Générer des questions à partir d'un document | **quiz-mastery** |
| Extraire des questions d'un fichier | **quiz-mastery** |
| Notation, suivi de maîtrise, planification Ebbinghaus | **quiz-mastery** |
| Transformer les questions en page web à faire dans le navigateur | **quiz-html** (ce skill) |
| Plan d'apprentissage, suivi long terme | **study-buddy** |

## Gestion des échecs

- `exit 1` : erreur de paramètres / fichier inexistant / template manquant → signalez l'erreur à l'utilisateur et faites vérifier les chemins
- `exit 2` : problème de format JSON / données de question invalides → indiquez quelles questions ont été ignorées et faites vérifier les champs
- Des questions ignorées mais des questions valides présentes : la génération réussit quand même, mais stderr liste les questions sautées ; il faut mentionner dans la réponse « N questions ignorées, raison : XXX »
