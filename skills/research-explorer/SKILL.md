---
name: research-explorer
version: "1.0.0"
category: "Autres"
tags:
  - research
  - explorer
description: À utiliser quand l'utilisateur a une direction de recherche vague et souhaite explorer des sujets spécifiques envisageables. Produit une analyse structurée avec des sujets candidats, une notation innovation/faisabilité et une pré-étude de 20 à 30 travaux représentatifs. Une seule étape, sans runtime Python.
language: fr

read_when:
  - Déclencher quand la demande concerne : à utiliser quand l'utilisateur a une direction de recherche vague et souhaite explorer des sujets spécifiques…
  - Déclencher si la demande mentionne : sujets, utiliser, quand
  - Ne pas déclencher hors de ce périmètre (convention protocole, Task 28).
---

## §0 — Contexte Système (SHARED v1.6.8)

> Écosystème Knowledge : {{SKILLS_ROOT}}=skills/ | {{KB_PATH}}=skills/KNOWLEDGE.md | {{KB_ENABLED}}=true | {{PROFILE_DEFAULT}}=NORMAL
> Conventions : kebab-case (dossiers/fichiers) | semver (versions) | #token (tags) | {{VARIABLE}} (variables) | @mon-ecosysteme/ (PMs) | @historique/ (archive documentaire des versions — R4 git mv byte-identité, R2 jamais éditer, jamais source d'installation KO-L003)
> Règle Zéro : skills auto-contenus, versionnés semver, registre KB source de vérité, dépendances YAML, cross-references bidirectionnelles.



# Research Explorer

## Vue d'ensemble

Skill d'exploration de sujets de recherche. Prend une direction large, mène une recherche web multi-dimensionnelle avec les propres outils WebSearch / WebFetch de l'agent, et produit trois livrables Markdown structurés. **Une seule étape, qualité complète dès le départ.** Pas de runtime Python, pas de SDK LLM.

## Quand l'utiliser

- L'utilisateur dit « je veux faire de la recherche sur X » sans sujet précis.
- L'utilisateur veut savoir « quels sont les sujets à la mode dans X ».
- L'utilisateur a besoin d'aide pour resserrer un domaine large en 5 à 10 sujets candidats.
- L'utilisateur demande une « vue d'ensemble du paysage de recherche ».

## Quand NE PAS l'utiliser

- L'utilisateur a déjà une question de recherche précise → utilisez `literature-survey` ou `paper-writer`.
- L'utilisateur veut une vérification de fait rapide → utilisez WebSearch directement.

## Workflow

### Étape 1 — Comprendre la direction

Confirmez avec l'utilisateur :

- **Direction** — le domaine d'intérêt large (ex. « apprentissage fédéré », « NLP pour la santé »).
- **Contraintes** — théorique vs appliquée, méthodes spécifiques, revue cible, budget de calcul, horizon temporel.
- **Langue** — par défaut l'anglais dans la conversation ; les rapports sont en anglais sauf demande contraire de l'utilisateur.

### Étape 2 — Préparer le répertoire d'exécution

```bash
DIRECTION="<direction>"
SLUG=$(python3 -c "import re,hashlib,sys; t=sys.argv[1]; n=re.sub(r'[\\s_]+','-',re.sub(r'[^\\w\\s-]','',t.lower().strip())).strip('-')[:40].rstrip('-'); h=hashlib.sha1(t.encode()).hexdigest()[:8]; print(f'{n}-{h}')" "$DIRECTION")
TS=$(date +%Y-%m-%d_%H%M%S)
RUN=output/research-explorer/$SLUG/$TS

mkdir -p "$RUN"
ln -sfn "$TS" "output/research-explorer/$SLUG/latest"
```

Dans les commandes ci-dessous, `$RUN` = `output/research-explorer/<slug>/latest`.

### Étape 3 — Exploration multi-dimensionnelle

Lancez **la recherche académique AMiner** et **la recherche web** sur les dimensions suivantes (une requête par dimension, davantage si les retours sont maigres) :

1. **Sujets à la mode** — "<direction> 2024 2025 hot topics" / "recent advances".
2. **Problèmes ouverts** — "<direction> open problems" / "challenges".
3. **Surveys** — "<direction> survey 2024" / "<direction> review".
4. **Benchmarks** — "<direction> benchmark" / "<direction> evaluation dataset".
5. **Applications** — "<direction> applications" / "<direction> industry use cases".
6. **Inter-champs** — "<direction> + <champ adjacent>" (choisissez 1 à 2 champs adjacents).
7. ** percées récentes** — articles des 6 à 12 derniers mois dans les grandes conférences/revues.

**Stratégie de recherche (préférez la recherche académique structurée au web générique) :**

- **AMiner `search_papers`** — utilisez-ceci EN PREMIER pour chaque dimension. Il renvoie des articles avec des métadonnées structurées (citations, venue, DOI, auteurs) que la recherche web ne fournit pas. Exemple : `search_papers(query="federated learning survey 2024", max_results=10, sort_by_citation=true)`.
- **AMiner `search_authors`** — utilisez pour trouver les chercheurs de premier plan de la direction. Exemple : `search_authors(query="federated learning", max_results=10)`.
- **`web_search`** — utilisez en complément quand AMiner renvoie des résultats insuffisants, ou pour des sources non académiques (blogs, documentation, benchmarks).

Pour chaque candidat retenu, extrayez titre canonique / auteurs / année / venue / nombre de citations depuis la réponse AMiner. Pour les résultats issus uniquement de la recherche web, faites un **WebFetch** de l'URL du résumé pour extraire les métadonnées. Persistez les notes intermédiaires dans `$RUN/search_notes.md` après chaque dimension pour permettre une reprise propre du travail.

### Étape 4 — Produire les trois livrables

Écrivez-les dans `$RUN/` :

#### 4.1 `research_exploration.md`

Analyse structurée contenant :

- **Rappel de la direction et contraintes**.
- **Cartographie du paysage** — les principaux sous-champs et les relations entre eux.
- **5 à 10 sujets candidats**, chacun avec :
  - Titre (assez précis pour servir de titre d'article).
  - Motivation (pourquoi c'est pertinent maintenant).
  - Angle d'innovation (ce qui serait nouveau).
  - Score de faisabilité (faible / moyen / élevé) avec une brève justification (disponibilité des données, besoins de calcul, densité des travaux antérieurs).
  - Risque / question ouverte.
- **Recommandation** — les 1 à 3 sujets que l'utilisateur devrait poursuivre, et pourquoi.

#### 4.2 `topic_matrix.md`

Plan hiérarchique Markdown de l'espace de sujets :

```
# <Direction>
## Subfield A
### Topic A.1
### Topic A.2
## Subfield B
### Topic B.1
```

Ce fichier est exploitable par le skill `mindmap-render` pour produire une carte mentale visuelle.

#### 4.3 `literature_pre_survey.md`

Un tableau de pré-étude des **20 à 30 travaux représentatifs** découverts ci-dessus, avec les colonnes : titre, auteurs, année, venue, URL, note de pertinence en une phrase. Chaque entrée doit avoir une URL que l'agent a récupérée dans cette session.

### Étape 5 — Passation optionnelle

Si l'utilisateur choisit un sujet, suggérez le skill suivant :

- Pour un article : le skill `paper-writer` (avec le sujet choisi).
- Pour une revue de littérature : le skill `literature-survey`.
- Pour un paquet d'expériences : le skill `experiment-suite`.
- Pour une carte de sujets visuelle : le skill `mindmap-render` consommant `topic_matrix.md`.

## Flux de données inter-skills (convention de chemins)

Un skill en aval peut localiser cette exploration via le slug :

- `output/research-explorer/<slug>/latest/topic_matrix.md`
- `output/research-explorer/<slug>/latest/literature_pre_survey.md`

Si l'utilisateur retient un sujet de la matrice, les skills aval calculent leur propre slug à partir du **sujet** (et non de la direction d'origine), de sorte que les chemins de slugs divergent à partir de ce skill — ce qui est correct.

## Règles importantes

- **Pas de SDK LLM dans ce skill.** Juste une procédure + ce `SKILL.md`.
- **Les candidats sont des suggestions, pas des garanties de nouveauté** — l'utilisateur doit vérifier l'originalité avant de s'engager.
- **Les scores de faisabilité sont heuristiques** — signalez explicitement l'incertitude quand c'est pertinent.
- Chaque entrée de littérature doit avoir une URL récupérée dans cette session ; pas d'entrées uniquement de mémoire.
