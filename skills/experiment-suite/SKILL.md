---
name: experiment-suite
version: "1.0.0"
category: "Autres"
tags:
  - experiment
  - suite
description: À utiliser quand l'utilisateur a une question de recherche et a besoin d'un paquet d'expérience complet — document de conception, code exécutable, résultats (mesurés ou simulés avec une provenance honnête), figures de qualité publication, rapport structuré. Étape unique, sans runtime Python.
language: fr

---

# Experiment Suite

## Vue d'ensemble

Générateur de paquet d'expérience de bout en bout. **Étape unique, pleine qualité dès le départ.** L'agent (Claude Code / Cursor / Aider / Codex / …) écrit tout directement avec ses propres outils (Write, Bash, WebFetch, …). Ce skill contient une procédure + des playbooks de référence + des scripts d'exemples de figures — pas de runtime Python, pas de SDK LLM.

Le travail de fond est décomposé en playbooks de référence sous `references/` :

| Référence | Sujet |
|---|---|
| `references/00-incremental-execution.md` | comment procéder sans perdre son travail : lots, persistance, reprise — **à lire en premier** |
| `references/01-design-depth.md` | ce que contient une vraie conception d'expérience (motivation → hypothèse → jeux de données → baselines → métriques → ablations → budget) |
| `references/01a-data-contract.md` | liaison des données au runtime : source, voie d'accès, version, split et périmètre de réutilisation |
| `references/02-code-quality.md` | standards de squelette de code — `model.py`, `data.py`, `train.py`, `evaluate.py` exécutables |
| `references/03-results-protocol.md` | schéma de `results.json` ; provenance `measured` / `simulated` / `illustrative` |
| `references/04-publication-figures.md` | graphiques de qualité publication, mises en page multi-panneaux, règles de goût |
| `references/04a-figure-contract.md` | la logique de la figure avant le tracé : conclusion, carte des panneaux, risque relecteur |
| `references/04b-figure-qa.md` | bundle d'export, texte éditable, statistiques et QA d'intégrité d'image |
| `references/05-report-structure.md` | `experiment_report.md` structuré (problème → conception → méthode → résultats → analyse → limites) |
| `references/06-quality-gate.md` | auto-contrôle avant livraison |

Aussi : `figure_examples/` — scripts matplotlib de style publication plus un kit de style partagé que l'agent peut utiliser comme points de départ.

**Lisez la référence pertinente _avant_ d'écrire, pas après.** La passe complète ne tient pas en un seul tour — `references/00-incremental-execution.md` est le seul mode d'exécution qui aboutit.

## Quand l'utiliser

- L'utilisateur veut « concevoir une expérience » pour une question de recherche.
- L'utilisateur a besoin de code exécutable pour une tâche précise (classification / prévision / détection / …).
- L'utilisateur veut comparer des méthodes et obtenir un rapport structuré à la fin.
- L'utilisateur a besoin de figures de qualité publication pour des résultats expérimentaux.

## Quand NE PAS l'utiliser

- L'utilisateur ne veut qu'un extrait de code rapide (écrire le code directement).
- L'utilisateur veut un article complet → `paper-writer`.
- L'utilisateur veut une revue de littérature → `literature-survey`.

## Workflow

### Étape 1 — Comprendre la question et le mode opératoire

Confirmer avec l'utilisateur :

- **Question de recherche** — ce qu'on cherche à répondre.
- **Type de tâche** — classification / régression / prévision / détection / génération / …
- **Mode**
  - **measured** — l'utilisateur a de vraies données ou exécutera le code lui-même ; fournir un chemin vers un `results.json` mesuré ou exécuter `train.py` sur de vraies données plus tard.
  - **simulated** (défaut) — l'agent génère un `results.json` de forme plausible et déterministe, à titre de placeholder. Chaque légende de figure/tableau doit préciser « simulé ».
- **Préférence de framework** — PyTorch (défaut), JAX, TensorFlow ou sklearn.
- **Budget de calcul** — heures / GPU disponibles ; contraint le squelette de code et le plan d'hyperparamètres.

Si l'utilisateur a des données et du temps, pousser vers le mode measured. Sinon, le mode simulated est acceptable **à condition** que les mentions soient honnêtes dans chaque artefact.

### Étape 2 — Préparer le répertoire d'exécution

```bash
QUESTION="<research_question>"
SLUG=$(python3 -c "import re,hashlib,sys; t=sys.argv[1]; n=re.sub(r'[\\s_]+','-',re.sub(r'[^\\w\\s-]','',t.lower().strip())).strip('-')[:40].rstrip('-'); h=hashlib.sha1(t.encode()).hexdigest()[:8]; print(f'{n}-{h}')" "$QUESTION")
TS=$(date +%Y-%m-%d_%H%M%S)
RUN=output/experiment-suite/$SLUG/$TS

mkdir -p "$RUN/experiment" "$RUN/figures"
ln -sfn "$TS" "output/experiment-suite/$SLUG/latest"
```

Dans les commandes ci-dessous, `$RUN` = `output/experiment-suite/<slug>/latest`.

L'agent créera cinq fichiers de premier niveau dans `$RUN/` :

- `experiment_design.md`
- `data_contract.md`
- `experiment/{model.py,data.py,train.py,evaluate.py,config.yaml,requirements.txt,README.md}`
- `results.json`
- `figures/*.pdf` avec leurs sources `make_*.py` et un `manifest.json`
- `experiment_report.md`

### Étape 3 — Construire le paquet (OBLIGATOIRE — c'est tout le travail)

Ouvrir d'abord `references/00-incremental-execution.md`. Puis mener les six chantiers ci-dessous sur de nombreux tours, en persistant l'état dans `$RUN/` après chaque lot.

#### 3.1 Conception — document de justification complet

**Ouvrir :** `references/01-design-depth.md` et `references/01a-data-contract.md`. Écrire d'abord `$RUN/data_contract.md` comme contrat de données de cette exécution. Il doit préciser si les données sont fournies par l'utilisateur, découvertes par l'agent, publiques réutilisées, contrôlées ou synthétiques par repli. Puis écrire `$RUN/experiment_design.md` comme une vraie conception (≥ 700 mots) : motivation → hypothèse → jeux de données → baselines → métriques → ablations → budget de calcul. Justifier chaque choix.

#### 3.2 Code — réellement exécutable

**Ouvrir :** `references/02-code-quality.md`. Remplir `$RUN/experiment/` avec du code qu'un ingénieur pourrait lancer avec `python train.py --config config.yaml`. Vraie classe de modèle (même minimale), vrai chargeur de données, vraie boucle d'entraînement, vraie évaluation. Le `data.py` et le `config.yaml` générés sont des produits d'exécution de cette run et doivent se lier à `$RUN/data_contract.md`, pas à un benchmark codé en dur à l'échelle du dépôt. Ajouter un `README.md` avec les instructions de lancement.

#### 3.2.5 Exécution (si un environnement d'exécution est disponible)

**Ordre de priorité pour l'exécution :**

1. **Sandbox MCP** (`sandbox_execute`) — préféré pour les expériences formelles.
   - Produit un `results.json` mesuré avec une vraie sortie d'exécution.
   - Timeout intelligent (calculé automatiquement selon la complexité du code), retry automatique en cas de paquet manquant.
   - Appel : `sandbox_execute(code=<script complet>, timeout=300, requirements=["torch","scikit-learn"])`

2. **Jupyter MCP** — préféré pour l'exploration interactive et le débogage.
   - Écrire le code en cellules de notebook, exécuter via `jupyter_execute_cell`.
   - Adapté à la vérification du chargement de données et aux tests de fumée rapides.

3. **Agent Bash** — repli pour les scripts simples.
   - `python experiment/train.py` directement.

Si **AUCUN** environnement d'exécution n'est disponible, revenir au mode « simulated » (comportement actuel).

**Quand l'exécution réussit :**

- Positionner `provenance.mode = "measured"` dans `results.json`
- Inclure `execution_time` issue de la sortie sandbox/Jupyter
- Passer la porte `execution-guard` **AVANT** l'exécution
- Passer la porte `correctness` **APRÈS** l'exécution

**Protocole de résultats auto-mesurés :**

Quand la sandbox exécute le code avec succès, analyser le stdout pour produire un `results.json` structuré :

```json
{
  "provenance": {
    "mode": "measured",
    "source": "sandbox_execute via SANDBOX_API_BASE",
    "execution_time": 15.3,
    "timestamp": "2026-07-08T14:30:00Z"
  }
}
```

Si l'exécution réussit partiellement (certaines métriques calculées, d'autres en échec), utiliser `"mode": "mixed"` avec une provenance `by_method` (voir `references/03-results-protocol.md`).

#### 3.3 Résultats — provenance honnête

**Ouvrir :** `references/03-results-protocol.md`. Produire `$RUN/results.json` avec un schéma bien formé : entrées par graine, moyenne et écart-type par méthode et par métrique, bloc d'ablation, et un champ `provenance` qui nomme la source.

- **mode measured** — l'utilisateur exécute `experiment/train.py` (ou fournit un JSON de résultats) et l'agent le charge dans `$RUN/results.json`, en réglant `"simulated": false` et `"provenance": "loaded from <path>"`.
- **mode measured, données découvertes par l'agent** — l'agent peut chercher et lier lui-même un jeu de données ouvert, mais la source choisie, le split et la voie d'accès doivent d'abord être consignés dans `$RUN/data_contract.md` ; la provenance de `results.json` doit renvoyer à cette liaison.
- **mode simulated** — l'agent écrit un JSON déterministe et seedé de forme plausible, en réglant `"simulated": true`.

#### 3.4 Figures — 3 à 6 de qualité publication

**Ouvrir :** `references/04-publication-figures.md`, `references/04a-figure-contract.md`, `references/04b-figure-qa.md`, et `figure_examples/`. Avant d'écrire le code de tracé, définir le contrat de figure dans une petite note de travail sous `$RUN/figures/figure_contract.md` :

- conclusion en une phrase,
- archétype de figure,
- carte des panneaux,
- hiérarchie des preuves,
- statistiques nécessaires,
- risque relecteur.

Ensuite, planifier et générer au minimum :

- 1 graphique de comparaison de méthodes (barres ou courbes).
- 1 décomposition d'ablation.
- Optionnel : courbes d'entraînement, tracé de scaling, carte de chaleur.

Enregistrer chaque figure dans `$RUN/figures/<basename>.pdf` avec sa source `make_*.py` à côté. Préférer l'enregistrement d'un `.svg` éditable et d'un `.tiff` qualité impression à côté du PDF quand l'environnement le permet. Ajouter des entrées à `$RUN/figures/manifest.json` en ne stockant que des **basenames** (jamais de chemins absolus) afin que paper-writer puisse les copier directement. Appliquer le style de publication partagé (polices embarquées, palette explicite, étiquettes de panneaux, filigrane « simulé » le cas échéant).

En cas de simulation, apposer un filigrane sur les figures ou toujours mentionner « simulé » dans leurs légendes dans le rapport.

#### 3.5 Rapport — structuré

**Ouvrir :** `references/05-report-structure.md`. Écrire `$RUN/experiment_report.md` avec les sections : énoncé du problème → raisonnement de conception → méthode → mise en œuvre → résultats → analyse → limites. Référencer les figures par nom de fichier. Ce rapport est le livrable principal pour les utilisateurs qui veulent seulement le paquet d'expérience (sans relance paper-writer).

#### 3.6 Porte de qualité

**Ouvrir :** `references/06-quality-gate.md`. Cibles : conception ≥ 700 mots, imports du code propres (`python -c "import experiment.model"` depuis l'intérieur de `$RUN`), `results.json` passe la vérification de schéma, ≥ 3 figures, rapport ≥ 6 sections.

### Étape 4 — Livrer

Rapporter :

1. `output/experiment-suite/<slug>/latest/experiment_design.md`
2. `output/experiment-suite/<slug>/latest/experiment/` — paquet de code exécutable.
3. `output/experiment-suite/<slug>/latest/results.json` — avec provenance.
4. `output/experiment-suite/<slug>/latest/figures/` — graphiques de qualité publication + `manifest.json`.
5. `output/experiment-suite/<slug>/latest/experiment_report.md` — rapport structuré.
6. Statistiques selon le format de rapport de `references/06-quality-gate.md`.

## Flux de données inter-skills (convention de chemins)

Le skill `paper-writer` calculant le même slug pour le même sujet cherchera ici :

- `output/experiment-suite/<slug>/latest/results.json` — source des chiffres et du drapeau `"simulated"` (pilote la clause de divulgation de l'article).
- `output/experiment-suite/<slug>/latest/figures/*.pdf` (+ `manifest.json`) — figures à réutiliser plutôt qu'à retracer.

Toujours stocker des **basenames** dans `manifest.json`. Les chemins absolus dans le manifeste cassent le `\includegraphics{figures/<basename>}` de paper-writer.

## Règles importantes

- **Pas de SDK LLM dans ce skill.** Pas de `import anthropic` / `import openai`. Le skill se limite à SKILL.md + références + exemples de figures.
- **Les résultats simulés doivent rester visiblement étiquetés** — dans `results.json` (`"simulated": true`), dans les légendes des figures, dans la divulgation en tête du rapport, et dans la note `\thanks` de tout article en aval.
- **Ne jamais présenter des résultats simulés comme mesurés.** En cas de doute, traiter comme simulé et divulguer.
- Le code exécutable est un point de départ, pas une reproduction de l'état de l'art. Être honnête sur son périmètre dans `experiment/README.md`.
- Un vrai paquet d'expérience nécessiterait normalement des jours de calcul pour de vrais chiffres ; la voie simulée permet au workflow de se poursuivre quand ce n'est pas possible, avec une divulgation honnête tout du long.
