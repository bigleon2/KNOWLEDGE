---
nom: quiz-mastery
source: skills/quiz-mastery/SKILL.md
sha256_source: 7fbbca7a1791
genere: 2026-10-29 (phase P2 — directive 10 tâches, tâche 2)
usage: AUTONOME hors écosystème (dossier « Prompt Maitre » — non lu par l'orchestration)
---

> ⚠️ **MARQUEUR D'EXCLUSION (garde D010)** — CE DOSSIER N'EST PAS LU PAR L'ORCHESTRATION. Les dossiers « Prompt Maitre » sont des prompts autonomes à usage HORS écosystème : ils ne sont pas indexés au registre KB, ne sont mobilisés par aucun arbitre, et ne remplacent jamais la forme installée `skills/<skill>/` (source de vérité).

# Prompt Maître autonome — quiz-mastery (version non déclarée)

## Comment utiliser ce prompt (hors écosystème)

Ce document encapsule la compétence sous forme autonome : copiez-le intégralement
dans un assistant IA (ou ouvrez-le en référence directe) — aucune installation,
aucun registre, aucune dépendance à l'écosystème Knowledge d'origine n'est requise.
Les variables de l'écosystème d'origine ont été résolues en valeurs littérales ;
si des ressources `references/` accompagnent ce dossier, elles sont jointes au même
emplacement et le prompt y renvoie par leur chemin relatif. La version d'origine
(source de vérité) vit dans `skills/quiz-mastery/SKILL.md` du dépôt KNOWLEDGE.

---

## Le prompt

---
name: quiz-mastery
description: Outil de génération de quiz, tests, révisions et suivi de maîtrise. **Ce skill se déclenche en priorité dès que l'utilisateur dit « réviser », « consolider », « revoir »**. Il s'active quand la demande touche aux « questions / révision » : transformer un support d'apprentissage/PDF en exercices (« fais-moi quelques questions sur ce PDF »), importer un fichier de questions pour s'exercer (« j'ai un fichier de questions, aide-moi »), réviser des acquis (« révise hier », « consolide », « revois hier », « planifie-moi avec Ebbinghaus »), suivi de la courbe de l'oubli, notation du niveau de maîtrise. **🔴 Règle impérative** : après chaque génération/import réussi, **avant de montrer les questions au premier tour, il FAUT demander** « veux-tu une page web d'exercices ? » ; si oui → appeler le skill quiz-html. **Ne traite pas** : le suivi de progression et la planification des projets d'apprentissage au long cours (→ study-buddy).
---

## §0 — Contexte Système (SHARED v1.7.14)

> Écosystème Knowledge : `skills/`=skills/ | `skills/KNOWLEDGE.md`=skills/KNOWLEDGE.md | `true`=true | `NORMAL`=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.



# Quiz Mastery

## Deux capacités principales

### Capacité 1 : générer des questions depuis un support d'apprentissage
1. L'utilisateur fournit un support (.md / .txt / .docx / .pdf / .ppt / .pptx)
2. Appeler `generate_from_material.py` pour obtenir le prompt d'extraction des points de savoir
3. Envoyer le prompt au LLM, obtenir le JSON des points de savoir
4. Appeler `service.save_knowledge_points()` pour les enregistrer
5. Appeler `run_quiz.py` pour générer le prompt de questions
6. Envoyer le prompt au LLM, obtenir le JSON des questions
7. **⭐ Demander à l'utilisateur s'il veut une page web d'exercices** (voir « Articulation avec la page web » ci-dessous)
   - Oui → appeler le skill `quiz-html` pour générer le HTML et l'ouvrir
   - Non → poursuivre le flux normal
8. Présenter les questions une à une, collecter les réponses
9. Appeler `submit_answers.py` pour soumettre la notation

### Capacité 2 : s'exercer depuis un fichier de questions
1. L'utilisateur fournit un fichier de questions (.md / .txt / .docx / .pdf / .ppt / .pptx)
2. Appeler `import_quiz.py` pour obtenir le prompt d'analyse des questions
3. Envoyer le prompt au LLM, obtenir le JSON normalisé des questions
4. Appeler `service.import_questions()` pour importer et créer la session
5. **⭐ Demander à l'utilisateur s'il veut une page web d'exercices** (voir « Articulation avec la page web » ci-dessous)
   - Oui → appeler le skill `quiz-html` pour générer le HTML et l'ouvrir
   - Non → poursuivre le flux normal
6. Présenter les questions une à une, collecter les réponses
7. Appeler `submit_answers.py` pour soumettre la notation

## Quand l'utiliser (conditions de déclenchement)

1. **Demande explicite** : « fais-moi des questions », « teste-moi », « un petit quiz », « des exercices », « interroge-moi »
2. **L'utilisateur dit « réviser », « consolider », « revoir »** : déclenchement direct
3. **Exercice depuis un fichier de questions** : se déclenche après le téléversement du fichier

> ⚠️ **Ne pas traiter l'« exercice immédiat » de study-buddy** — cette chaîne passe par study-buddy avec son `exam_take` externe, sans appeler ce skill.

## Repli quand il n'y a pas d'historique

Quand l'utilisateur dit « réviser » mais que `data/user_progress/` est vide (nouvel utilisateur / aucune réponse) :
- **Ne pas lancer mécaniquement le flux de révision** — rien à réviser
- Dire activement à l'utilisateur : « il n'y a pas encore d'historique à réviser ; veux-tu d'abord générer des questions depuis un support d'apprentissage ? »
- L'orienter vers la « Capacité 1 : générer des questions depuis un support »

## Système de difficulté

| Niveau | Signification | Description |
|------|------|------|
| L1 | mémorisation | mémoire et compréhension de base, reconnaissance de concepts et faits élémentaires |
| L2 | compréhension | compréhension approfondie, distinction de concepts, explication de principes et application simple |
| L3 | application | usage combiné, application à des cas réels, analyse et résolution de problèmes |

- **Première génération** : départ obligatoire en L1
- **Bonne réponse au niveau courant** : monter d'un cran (L3 maximum)
- **Mauvaise réponse au niveau courant** : descendre d'un cran (L1 minimum)

## Répartition des types de questions

| Niveau | Choix multiple | Vrai-faux | Texte à trous | Réponse courte |
|------|--------|--------|--------|--------|
| L1 | 70 % | 30 % | - | - |
| L2 | 50 % | 20 % | 30 % | - |
| L3 | 40 % | 20 % | 20 % | 20 % |

## Nombre de questions

- **Par défaut, 3 questions par génération** (3 questions affichées dans un même tour, l'utilisateur répond à tout puis notation globale)
- Maximum **15 questions par tour** (l'utilisateur peut demander à ajuster)
- Réponses courtes aussi rares que possible : pas de notation automatique (marquées `needs_review`, jugées par un LLM/contrôle humain externe)

## Suivi des points de savoir faibles

- **Marquage en point faible** : nombre cumulé d'erreurs ≥ 3
- **Jamais levé** : les points faibles ne font que s'accumuler, conservés comme archive historique
- Les données internes sont dans `data/user_progress/` (compte d'erreurs, phases Ebbinghaus, etc.)
- **Synchronisation vers la section 3 « points de savoir faibles » de USER.md** (écrite directement par ce skill, source=`quiz-mastery`) :
  | Point de savoir | Nombre d'erreurs | Source | Notes |
  - déjà présent → mettre à jour le compte d'erreurs
  - absent → ajouter une ligne

## Mécanisme de révision par courbe de l'oubli

Basé sur la courbe d'Ebbinghaus, révisions espacées selon **1 jour → 2 jours → 4 jours → 7 jours → 15 jours** :
- Bonne réponse : review_stage +1 (passe à l'intervalle suivant)
- Mauvaise réponse : review_stage remis à 0 (on repart du début)
- Les révisions recommandées regroupent : les points de savoir sur le point d'être oubliés + les points faibles des 3 derniers jours

## Mode d'appel des scripts

### 1. Extraire les points de savoir d'un support

```bash
python3 scripts/generate_from_material.py <file_path> <document_id>
```

Produit le prompt d'extraction (JSON) ; envoyer prompts.system_prompt et prompts.user_prompt au LLM.

### 2. Importer des questions depuis un fichier

```bash
python3 scripts/import_quiz.py <file_path> <document_id> <user_id>
```

Produit le prompt d'analyse (JSON) ; envoyer prompts.system_prompt et prompts.user_prompt au LLM.

### 3. Générer un quiz

```bash
python3 scripts/run_quiz.py <user_id> <document_id>
```

Détermine automatiquement la difficulté selon les points de savoir enregistrés et la maîtrise courante ; produit le prompt de questions (JSON).

### 4. Soumettre les réponses

```bash
python3 scripts/submit_answers.py <user_id> <document_id> <session_id> '<answers_json>'
```

Description du paramètre :
- `answers_json` : dictionnaire de réponses en JSON, ex. `{"q_001": "A", "q_002": "True"}`

Retourne la notation : score, total, accuracy, results question par question.

## Flux de génération (notice pour study-buddy)

1. Déterminer la source des points de savoir (support d'apprentissage ou fichier de questions)
2. Exécuter le flux d'extraction/import correspondant
3. Appeler `run_quiz.py` pour générer le prompt de questions
4. **Présenter 3 questions à l'utilisateur à chaque fois** (en une seule fois, numérotation claire, pas une par une) ; après une réponse globale unique, notation groupée
5. Collecter les réponses (l'utilisateur peut répondre aux 3 questions d'un coup)
6. Appeler `submit_answers.py` pour soumettre la notation
7. Renvoyer le résultat de notation à study-buddy, qui l'écrit dans ses fichiers memory

⚠️ **Ce skill n'écrit que dans la section 3 « points de savoir faibles » de USER.md** (source=`quiz-mastery`) ; aucune autre section, ni `memory/`. Le reste de la persistance relève de study-buddy.

## Structure du répertoire de données

```
skills/quiz-mastery/data/
├── knowledge_points/     ← définitions des points de savoir (par document_id)
├── sessions/             ← historique des sessions de quiz
└── user_progress/        ← données de maîtrise (marquage des faiblesses, courbe de l'oubli)
```

## ⭐ Articulation avec la page web d'exercices (collaboration avec quiz-html)

Chaque fois qu'un JSON de questions est obtenu (capacité 1 étape 7, capacité 2 étape 5), **poser activement la question** :

> « Les questions sont prêtes ! Veux-tu que j'en fasse une page web d'exercices ? Tu pourras les faire à ton rythme dans le navigateur, les erreurs seront notées automatiquement, avec bascule de thème et mode examen 🎯 »

### Interprétation des réponses

| L'utilisateur dit | Interprétation | Action |
|---|---|---|
| « oui / ok / hm / vas-y / génère / page web / navigateur » | ✅ oui | appeler `quiz-html` |
| « pas besoin / non / laisse / je fais ici » | ❌ non | poursuivre le flux conversationnel |
| pas de réponse / ambigu | ❌ non par défaut | poursuivre le flux, sans insister |

### Étapes concrètes d'appel de quiz-html

```python
import json, subprocess, tempfile
from pathlib import Path

# 1. Écrire le JSON de questions dans un fichier temporaire
tmp_dir = Path(tempfile.mkdtemp(prefix="quiz_"))
qjson = tmp_dir / "questions.json"
qjson.write_text(json.dumps(questions, ensure_ascii=False), encoding="utf-8")

# 2. Décider du chemin de sortie (~/Desktop recommandé)
output = Path.home() / "Desktop" / f"quiz_{title_slug}.html"

# 3. Appeler le script
result = subprocess.run([
    "python3",
    str(Path.home() / "Desktop/studybuddy_4.0/skills/quiz-html/scripts/build_quiz_html.py"),
    str(qjson),
    "--title", page_title,        # ex. « 📚 Physique · exercices électricité »
    "--output", str(output),
    "--open",                     # ouvrir automatiquement dans le navigateur après génération
], capture_output=True, text=True)

info = json.loads(result.stdout)  # {"success": true, "output_path": "...", ...}
```

### Recommandations de complément des champs

Avant l'appel, idéalement compléter chaque question avec les champs suivants (s'ils n'ont pas été générés) :
- `category` : **catégorie de premier niveau, mot court** (2 à 6 caractères conseillés), pour les chips de filtrage en haut de page.
  - ✅ recommandé : `Physique` / `Maths` / `Droit` / `Histoire` / `Programmation` / `Général`
  - ❌ à éviter : les longues chaînes avec dates/numéros/barres obliques du type `Général / 1. Loi sur les valeurs mobilières (29/12/1998…)`
  - Si deux niveaux sont nécessaires, séparer par `/` avec un second niveau court : `Physique / Électricité`
- `knowledge_point` : nom du point de savoir (regroupement en barre latérale ; peut reprendre le titre du KP de quiz-mastery, sans préfixe hiérarchique)
- `memory_tip` : moyen mnémotechnique (optionnel, très utile aux élèves)

Ainsi les filtres de catégories, le regroupement latéral et les cartes mémoire de la page pourront pleinement jouer.

## Frontières

| Tâche | Qui s'en charge |
|---|---|
| Générer et extraire des questions | ce skill (quiz-mastery) |
| Notation, suivi de maîtrise | ce skill (quiz-mastery) |
| **Questions → page web d'exercices** | **quiz-html** |

Après l'appel de quiz-html, **le flux de notation de quiz-mastery reste à exécuter** — l'état des réponses dans la page sert à l'auto-vérification de l'utilisateur ; les données officielles de maîtrise passent par `submit_answers.py`. Les deux chemins sont parallèles et sans conflit.


---

## Ressources locales du dossier

Aucune ressource annexe — ce prompt est auto-suffisant.
