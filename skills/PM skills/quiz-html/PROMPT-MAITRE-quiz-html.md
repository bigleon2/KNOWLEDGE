---
nom: quiz-html
source: skills/quiz-html/SKILL.md
sha256_source: bacb1754d1db
genere: 2026-10-29 (phase P2 — directive 10 tâches, tâche 2)
usage: AUTONOME hors écosystème (dossier « Prompt Maitre » — non lu par l'orchestration)
---

> ⚠️ **MARQUEUR D'EXCLUSION (garde D010)** — CE DOSSIER N'EST PAS LU PAR L'ORCHESTRATION. Les dossiers « Prompt Maitre » sont des prompts autonomes à usage HORS écosystème : ils ne sont pas indexés au registre KB, ne sont mobilisés par aucun arbitre, et ne remplacent jamais la forme installée `skills/<skill>/` (source de vérité).

# Prompt Maître autonome — quiz-html (version non déclarée)

## Comment utiliser ce prompt (hors écosystème)

Ce document encapsule la compétence sous forme autonome : copiez-le intégralement
dans un assistant IA (ou ouvrez-le en référence directe) — aucune installation,
aucun registre, aucune dépendance à l'écosystème Knowledge d'origine n'est requise.
Les variables de l'écosystème d'origine ont été résolues en valeurs littérales ;
si des ressources `references/` accompagnent ce dossier, elles sont jointes au même
emplacement et le prompt y renvoie par leur chemin relatif. La version d'origine
(source de vérité) vit dans `skills/quiz-html/SKILL.md` du dépôt KNOWLEDGE.

---

## Le prompt

---
name: quiz-html
description: Générer à partir d'un tableau de questions une **page web d'exercices autonome** (fichier HTML). Quand l'utilisateur termine le flux « quiz depuis un support » ou « import de questions depuis un fichier » de quiz-mastery, proposer activement de « s'exercer dans une page web » ; après accord, appeler ce skill pour injecter les questions dans le gabarit et produire le HTML. Se déclenche aussi quand l'utilisateur dit directement « transforme ces questions en page web / HTML / page d'exercices ». **Ne traite pas** : la génération de quiz (→ quiz-mastery), la notation (→ quiz-mastery), les plans de révision au long cours (→ study-buddy).
---

## §0 — Contexte Système (SHARED v1.7.13)

> Écosystème Knowledge : `skills/`=skills/ | `skills/KNOWLEDGE.md`=skills/KNOWLEDGE.md | `true`=true | `NORMAL`=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.



# Générateur de banque de questions web (Quiz HTML Builder)

Transformer un JSON de questions → une **page web d'exercices monofichier**, comprenant :
- 📂 filtres par catégorie (matière / sous-module) + filtres par statut (maîtrisé / non traité / erreurs)
- 🎯 4 types de questions : choix multiple / vrai-faux / texte à trous / réponse courte
- 🤖 marquage automatique des réponses, classement automatique des erreurs dans le cahier d'erreurs (une seconde chance à la première erreur)
- ⌨️ raccourcis clavier complets (A/B/C/D · Entrée · flèches · Espace)
- 📝 mode examen blanc (temps limité + soumission unique + page de résultats)
- 🌓 bascule thème clair/sombre · persistance localStorage · adaptation mobile

## Scénarios de déclenchement principaux

### Scénario 1 : proposition active après génération/import par quiz-mastery ⭐
C'est l'**entrée principale** de ce skill. Quand `quiz-mastery` termine l'un des flux :
- « quiz depuis un support » : `generate_from_material.py` → production du JSON de questions → `service.import_questions()` vers la base
- « import depuis un fichier de questions » : `import_quiz.py` → analyse en JSON de questions → base

une fois les questions prêtes et avant de les montrer, **poser la question** :
> « Les questions sont prêtes ! Veux-tu que j'en fasse une page web d'exercices ? Tu pourras les faire à ton rythme dans le navigateur, les erreurs seront notées automatiquement, avec bascule de thème et mode examen 🎯 »

Si l'utilisateur répond positivement (« oui / ok / fais la page / vas-y ») → appeler ce skill.
S'il refuse (« pas besoin / laisse tomber / je fais ici ») → poursuivre le flux d'exercice conversationnel habituel.

### Scénario 2 : demande directe d'une page web
Mots-clés déclencheurs :
- « transforme ces questions en page web », « fais une page HTML d'exercices », « génère une page web de banque de questions »
- « je veux m'exercer dans le navigateur », « fais une version web »
- « exporte les questions en HTML »

## Mode d'appel

### En une phrase
```bash
python3 scripts/build_quiz_html.py <fichier JSON de questions> [--title "..." --open]
```

### Flux standard

1. **Obtenir le JSON de questions** (tableau, un élément par question)
   - Source A : sortie LLM après génération par quiz-mastery (format standard du système)
   - Source B : tableau de questions collé directement par l'utilisateur
   - Source C : questions lues depuis la base (`data/sessions/<sid>/questions.json` de quiz-mastery)

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
       --title "📚 Physique · exercices thermodynamique" \
       --output ~/Desktop/quiz_physique-thermo_20260518.html \
       --open
   ```

4. **Analyser le JSON retourné** :
   ```json
   {
     "success": true,
     "output_path": "/Users/.../quiz_xxx.html",
     "question_count": 8,
     "title": "📚 Physique · exercices thermodynamique",
     "subtitle": "8 questions · choix×5 · vrai-faux×2 · trous×1 · Physique",
     "id": "q_1779091201",
     "size_bytes": 63752
   }
   ```

5. **Informer l'utilisateur** : lui donner le chemin du HTML et préciser « ouvert dans le navigateur, tu peux commencer ✨ »

## Standard des champs du JSON de questions

Totalement compatible avec le format de sortie de quiz-mastery, **avec champs optionnels ajoutés** `category` / `memory_tip` :

| Champ | Requis | Description |
|---|---|---|
| `type` | ✅ | `single_choice` / `true_false` / `fill_blank` / `short_answer` |
| `prompt` | ✅ | l'énoncé. Le champ `question` est aussi accepté (conversion automatique) |
| `options` | requis pour les QCM | `["A. xxx", "B. yyy", ...]` |
| `answer` | ✅ | la lettre pour un QCM ; `"True"`/`"False"` pour un vrai-faux ; le texte pour trous/réponse courte |
| `explanation` | recommandé | le corrigé (fortement conseillé, indispensable pour des élèves) |
| `knowledge_point` | recommandé | nom du point de savoir (regroupement secondaire de la barre latérale) |
| `category` | recommandé | chemin de catégorie, **au format « matière / sous-module »** : `"Physique / Électricité"`, `"Maths / Fractions"` |
| `level` | optionnel | difficulté 1-3 |
| `memory_tip` | optionnel | moyen mnémotechnique, affiché en surbrillance sur carte orange (redoutable pour réviser) |

### Exemple
```json
[
  {
    "type": "single_choice",
    "prompt": "Parmi ces affirmations sur la loi des courants dans un circuit en dérivation, laquelle est correcte (    ) ?",
    "options": [
      "A. Le courant principal vaut la différence des courants dérivés",
      "B. Le courant principal vaut la somme des courants dérivés",
      "C. Les courants dérivés sont égaux entre eux",
      "D. Le courant principal vaut plus du double de n'importe quelle branche"
    ],
    "answer": "B",
    "explanation": "Dans un circuit en dérivation, **le courant principal est la somme des courants dérivés** : I = I₁ + I₂ + ...",
    "knowledge_point": "loi des courants en dérivation",
    "category": "Physique / Électricité",
    "level": 1,
    "memory_tip": "🧠 En dérivation, pense au carrefour : ce qui entre ressort, le courant ne disparaît pas"
  }
]
```

## Principes de conception

### 1. category automatique, pour des filtres utiles
Si les questions n'ont pas de `category`, mieux vaut le renseigner (même par inférence depuis la matière). Sinon tout s'empile dans la catégorie « général » et le filtre perd son intérêt.

### 2. category au format « matière / sous-module »
- ✅ `"Physique / Électricité"`, `"Physique / Thermodynamique"` → 4 chips fines en haut de page
- ❌ `"Physique"` → une seule chip, le sous-module n'apparaît qu'en barre latérale, et la granularité du filtre se dégrade

### 3. Point de savoir et catégorie ne sont pas au même niveau
- `category` = classification transversale (matière/chapitre), pour les **chips du haut**
- `knowledge_point` = point de savoir fin, pour le **regroupement secondaire de la barre latérale gauche**

### 4. Nommage du fichier de sortie
Sortie par défaut dans le même répertoire que le JSON de questions, nom `quiz_<title_slug>_<horodatage>.html`.
**Conseillé : passer explicitement `--output`** vers `~/Desktop/` ou un répertoire fixe, plus facile à retrouver pour l'utilisateur.

## Exemple complet (enchaînement avec quiz-mastery)

```python
# 1. quiz-mastery a généré les questions, on tient le tableau
questions = [
    {"type": "single_choice", "prompt": "...", "options": [...], "answer": "A",
     "explanation": "...", "knowledge_point": "...", "category": "Physique / Électricité"},
    # ...
]

# 2. l'agent demande : « en faire une version web ? »
# 3. l'utilisateur : « oui »
# 4. l'agent écrit le fichier temporaire + appelle le skill

import json, subprocess, tempfile
from pathlib import Path

tmp_dir = Path(tempfile.mkdtemp(prefix="quiz_"))
qjson = tmp_dir / "questions.json"
qjson.write_text(json.dumps(questions, ensure_ascii=False), encoding="utf-8")

output = Path.home() / "Desktop" / "quiz_physique-electricite.html"

result = subprocess.run([
    "python3",
    str(Path.home() / "Desktop/studybuddy_4.0/skills/quiz-html/scripts/build_quiz_html.py"),
    str(qjson),
    "--title", "📚 Physique · exercices électricité",
    "--output", str(output),
    "--open",
], capture_output=True, text=True)

info = json.loads(result.stdout)
# info["output_path"] = "/Users/.../Desktop/quiz_physique-electricite.html"
```

Puis informer l'utilisateur :
> « C'est prêt ! La page s'est ouverte automatiquement ✨
> Chemin : `~/Desktop/quiz_physique-electricite.html`
> Prends ton temps, les erreurs seront consignées automatiquement — tu pourras filtrer sur « erreurs » pour les travailler en priorité 💪 »

## Frontières avec les autres skills

| Tâche | Qui s'en charge |
|---|---|
| Générer des questions depuis un support | **quiz-mastery** |
| Importer des questions depuis un fichier | **quiz-mastery** |
| Notation, suivi de maîtrise, planification Ebbinghaus | **quiz-mastery** |
| Transformer les questions en page web d'exercice | **quiz-html** (ce skill) |
| Plan d'étude, suivi au long cours | **study-buddy** |

## Gestion des échecs

- `exit 1` : erreur de paramètres / fichier inexistant / gabarit manquant → remonter l'erreur à l'utilisateur pour vérifier les chemins
- `exit 2` : problème de format JSON / données de questions invalides → indiquer quelles questions ont été ignorées, inviter à vérifier les champs
- Questions partiellement ignorées mais préservation de questions valides : la génération réussit quand même, mais stderr liste les questions ignorées — mentionner dans la réponse « N questions ignorées, motif XXX »


---

## Ressources locales du dossier

Aucune ressource annexe — ce prompt est auto-suffisant.
