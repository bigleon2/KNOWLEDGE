# Quiz Mastery Skill

Moteur indépendant de l'agent OpenClaw pour générer des quiz, réviser et suivre le niveau de maîtrise.

## Fonctionnalités

- **Génération de quiz à partir de supports d'apprentissage** : transforme des supports PDF / Word / Markdown en tests gradués (L1/L2/L3)
- **Import de quiz depuis des fichiers de questions** : analyse des fichiers de questions existants, normalisation puis soumission à l'utilisateur
- **Notation des réponses** : évaluation automatique + feedback question par question
- **Suivi de maîtrise** : enregistrement des progrès de l'utilisateur sur les trois niveaux de difficulté
- **Points faibles** : nombre cumulé d'erreurs ≥ 3 → marqué comme point faible (**croissant uniquement, jamais décroissant**, sert d'archive historique)
- **Révision par courbe de l'oubli** : planification des révisions selon Ebbinghaus (1/2/4/7/15 jours)

## Architecture

```
quiz-mastery/
├── SKILL.md                          # Métadonnées du skill (lu par le LLM)
├── README.md                         # Ce fichier (lu par l'humain)
├── skill.yaml                        # Configuration du skill
├── scripts/
│   ├── generate_from_material.py     # Extraction des points de connaissance depuis les supports
│   ├── import_quiz.py                # Import de questions depuis un fichier
│   ├── run_quiz.py                   # Génération du prompt de quiz
│   └── submit_answers.py             # Soumission des réponses + notation
├── src/quiz_mastery/                 # Moteur principal
└── data/
    ├── knowledge_points/             # Définitions des points de connaissance des documents
    ├── user_progress/                # Données de maîtrise de l'utilisateur (marquage des points faibles, phases Ebbinghaus)
    └── sessions/                     # Historique des sessions de quiz
```

## Démarrage rapide

### 1. Extraire les points de connaissance d'un support

```bash
python3 scripts/generate_from_material.py <file_path> <document_id>
```

Produit le prompt d'extraction des points de connaissance (JSON). Envoyer `prompts.system_prompt` et `prompts.user_prompt` au LLM, puis appeler `service.save_knowledge_points()` pour enregistrer la liste de points obtenue.

### 2. Importer depuis un fichier de questions

```bash
python3 scripts/import_quiz.py <file_path> <document_id> <user_id>
```

Produit le prompt d'analyse des questions (JSON). Envoyer le prompt au LLM pour obtenir les questions normalisées, puis appeler `service.import_questions()`.

### 3. Générer un quiz

```bash
python3 scripts/run_quiz.py <user_id> <document_id>
```

Détermine automatiquement la difficulté selon le niveau de maîtrise actuel de l'utilisateur, produit le prompt de quiz (JSON).

### 4. Soumettre les réponses

```bash
python3 scripts/submit_answers.py <user_id> <document_id> <session_id> '<answers_json>'
```

Retourne : `score`, `total`, `accuracy`, `results` question par question.

## Intégration des données (relation avec l'agent OpenClaw)

Ce skill **n'écrit pas dans `memory/`**, il n'écrit que la section 3 « points de connaissance faibles » de USER.md. Toute la persistance est assurée de façon centralisée par l'agent appelant, voir SKILL.md.

| Donnée | Qui écrit | Destination |
|------|------|--------|
| Définitions des points de connaissance, résultats, phases Ebbinghaus | ce skill | répertoire `data/` |
| Points de connaissance faibles (erreurs ≥ 3) | ce skill | section 3 de USER.md (source=`quiz-mastery`) |
| Statut des projets d'apprentissage, planification DAY | study-buddy (agent amont) | section 2 de USER.md |

## Système de difficulté

| Niveau | Signification |
|------|------|
| L1 | mémorisation (mémoire et compréhension de base) |
| L2 | compréhension (compréhension approfondie, application) |
| L3 | application (utilisation combinée, résolution de problèmes) |

- Premier quiz : départ obligatoire en L1
- Bonne réponse : montée en niveau (L3 maximum) ; mauvaise réponse : descente (L1 minimum)

## Workflow

1. **Generate / Import** : création des points de connaissance + des questions depuis un support ou un fichier de questions
2. **Run** : génération du quiz
3. **Submit** : réponses de l'utilisateur → notation automatique → mise à jour de la maîtrise / marquage des points faibles
4. **Sync** : écriture des points faibles dans la section 3 de USER.md
