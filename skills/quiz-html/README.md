# quiz-html · Générateur de banque de questions web

Convertit un tableau de questions → une page web d'exercices HTML ouvrable indépendamment.

## ✨ Vue d'ensemble des fonctionnalités

- 📂 **Double filtrage** : catégorie (matière/sous-module) + statut d'apprentissage (maîtrisé/non fait/mauvaise réponse)
- 🎯 **4 types de questions** : choix / vrai/faux / à trous / réponse courte
- 🤖 **Réponses intelligentes** : sélection ≠ soumission, modification possible à plusieurs reprises ; une chance de réessai en cas de mauvaise réponse
- ⌨️ **Raccourcis clavier** : A/B/C/D · Entrée · ← → · Espace
- 📝 **Mode examen simulé** : nombre de questions + limite de temps + soumission unique + page de résultats
- 🧠 **Astuces de mémorisation** : les questions avec un champ `memory_tip` seront mis en surbrillance
- 🌓 **Thème switchable** : thème clair/sombre double, mémorisation avec localStorage
- 💾 **Persistance du progrès** : le navigateur se souvient de l'état de chaque question, le statut reste après fermeture et réouverture
- 📱 **Adaptation mobile** : utilisation possible sur téléphone

## 🚀 Prise en main rapide

```bash
# 1. Préparer un fichier JSON de questions (tableau)
cat > /tmp/q.json << 'EOF'
[
  {"type":"single_choice","prompt":"1+1=?","options":["A. 1","B. 2","C. 3"],"answer":"B",
   "explanation":"Calcul de base","category":"Mathématiques / Addition et soustraction","level":1}
]
EOF

# 2. Générer le HTML
python3 scripts/build_quiz_html.py /tmp/q.json --title "Exercices de mathématiques" --open
```

## 📁 Structure des répertoires

```
quiz-html/
├── SKILL.md                  # Description du skill (pour l'agent)
├── README.md                 # Ce fichier (pour les humains)
├── skill.yaml                # Métadonnées du skill
├── scripts/
│   └── build_quiz_html.py    # Script d'injection
├── templates/
│   └── quiz_template.html    # Modèle HTML (contient {{placeholders}})
└── examples/
    └── demo.html             # Exemple : démo déjà injectable et directement ouvrable
```

## 🔗 Intégration avec quiz-mastery

Ce skill ne crée pas directement de questions, il se spécialise dans l'étape "questions → page web".
Pour créer des questions/importer, utilisez `quiz-mastery`. Chaîne complète :

```
quiz-mastery crée les questions
       ↓
   Fichier JSON des questions
       ↓
  Demande à l'utilisateur : "Voulez-vous faire une page web ?"
       ↓ L'utilisateur dit oui
   quiz-html ← vous êtes ici
       ↓
  Génère .html
       ↓
 Ouvre dans le navigateur → l'utilisateur commence à s'exercer
```

## 📝 Champs des questions

| Champ | Obligatoire | Type | Description |
|---|---|---|---|
| `type` | ✅ | string | `single_choice` / `true_false` / `fill_blank` / `short_answer` |
| `prompt` | ✅ | string | Énoncé de la question |
| `options` | Choix multiples | array | `["A. xxx", "B. yyy", ...]` |
| `answer` | ✅ | string | Réponse standard |
| `explanation` | Recommandé | string | Explication (supporte `**gras**` `*italique*` `\` code \``) |
| `knowledge_point` | Recommandé | string | Point de connaissance (pour le groupement dans la barre latérale) |
| `category` | Recommandé | string | Chemin de classification, format suggéré `"Matière / Sous-module"` |
| `level` | Optionnel | int | Difficulté 1-3 |
| `memory_tip` | Optionnel | string | Astuce de mémorisation, affichée en surbrillance dans une carte orange |

## ⌨️ Raccourcis clavier pour l'utilisateur

| Touche | Fonction |
|---|---|
| `A` `B` `C` `D` | Sélectionner une option |
| `T` `F` | Pour les questions vrai/faux |
| `Entrée` | Soumettre |
| `←` `→` | Question précédente / suivante |
| `Espace` | Voir la réponse |
| `Ctrl/⌘+Entrée` | Soumettre tout d'un coup pour l'examen simulé |

## 🛠️ Arguments en ligne de commande

```
python3 build_quiz_html.py <questions.json> [options]

  --output, -o    Chemin de sortie HTML (par défaut : même répertoire que les questions)
  --title         Titre de la page
  --subtitle      Sous-titre (généré automatiquement par défaut)
  --id            ID de la banque de questions (pour l'isolation localStorage)
  --open          Ouvrir dans le navigateur après génération
```

## 🔍 Codes de sortie

| Code | Signification |
|---|---|
| 0 | Succès |
| 1 | Erreur de paramètre / fichier inexistant / modèle manquant |
| 2 | Échec de l'analyse JSON / format de données invalide |

## 📌 Limites

| Tâche | À utiliser avec |
|---|---|
| Création de questions / notation / suivi de la maîtrise | `quiz-mastery` |
| Plan d'étude à long terme | `study-buddy` |
| **Transformer les questions en page web pour que l'utilisateur s'exerce dans le navigateur** | **`quiz-html` (ce skill)** |
